#!/usr/bin/env python3
"""Local media preparation, real LUT rendering, comparisons and explicit packaging."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

from PIL import Image, ImageCms, ImageDraw, ImageFont, ImageOps

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webp', '.bmp'}
HDR_TRANSFERS = {'smpte2084', 'arib-std-b67'}


def executable(name):
    env = os.environ.get(name.upper())
    value = env or shutil.which(name)
    if not value:
        raise ValueError(f'{name} not found. Put it on PATH or set {name.upper()} to its executable path.')
    return value


def run(arguments, cwd=None):
    result = subprocess.run([str(x) for x in arguments], cwd=cwd, capture_output=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}): {result.stderr[-6000:]}')
    return result.stdout


def source_path(value):
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f'Input is not a local file: {path}. Download remote media separately first.')
    return path


def available(paths, overwrite):
    normalized = [Path(p).resolve() for p in paths]
    if len(set(normalized)) != len(normalized):
        raise ValueError('Duplicate output paths.')
    for path in normalized:
        if path.exists() and (not overwrite or not path.is_file()):
            raise ValueError(f'Output exists: {path}; choose a new path or use --overwrite.')
        path.parent.mkdir(parents=True, exist_ok=True)


def save_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def ffprobe(path):
    return json.loads(run([executable('ffprobe'), '-v', 'error', '-show_format', '-show_streams', '-of', 'json', path]))


def video_context(path, matrix):
    metadata = ffprobe(path)
    streams = [s for s in metadata.get('streams', []) if s.get('codec_type') == 'video' and not s.get('disposition', {}).get('attached_pic')]
    if not streams:
        raise ValueError('No video stream found.')
    stream = streams[0]
    transfer = stream.get('color_transfer', 'unknown')
    primaries = stream.get('color_primaries', 'unknown')
    detected = stream.get('color_space', 'unknown')
    if transfer in HDR_TRANSFERS or primaries == 'bt2020':
        raise ValueError('HDR PQ/HLG or BT.2020 input needs a documented color-managed SDR Rec.709 conversion first. Bit depth alone is not HDR detection.')
    if primaries not in {'bt709', 'unknown', 'unspecified', None}:
        raise ValueError(f'Unsupported primaries {primaries}; normalize to Rec.709 with a documented color-managed conversion first.')
    if transfer not in {'bt709', 'unknown', 'unspecified', None}:
        raise ValueError(f'Unsupported transfer {transfer}; normalize to SDR Rec.709 first (Log is not supported automatically).')
    assumptions = []
    if matrix == 'auto':
        if detected != 'bt709':
            raise ValueError(f'Video matrix is {detected}. Confirm the source; use --matrix bt709 only when justified, or convert correctly first.')
    elif detected != 'bt709':
        assumptions.append(f'User explicitly overrides source matrix {detected} as bt709.')
    if primaries != 'bt709':
        assumptions.append(f'Unspecified source primaries ({primaries}) assumed BT.709; visually confirm against the source application.')
    if transfer in {'unknown', 'unspecified', None}:
        assumptions.append('Unknown transfer assumed SDR display-referred; this does not identify untagged Log/HDR.')
    if stream.get('color_range', 'unknown') not in {'tv', 'pc'}:
        assumptions.append('Range unspecified: FFmpeg decoder defaults used; inspect shadow/highlight levels.')
    return metadata, stream, assumptions


def image_rgb(path):
    """Normalize orientation/profile, rejecting unsupported precision/alpha modes."""
    with Image.open(path) as opened:
        opened.load()
        original_mode = opened.mode
        if getattr(opened, 'n_frames', 1) > 1:
            raise ValueError('Animated/multipage images require a chosen still frame first.')
        if original_mode in {'I', 'F', 'I;16', 'I;16B', 'I;16L'}:
            raise ValueError('High-bit-depth/float image requires explicit color-managed 8-bit preview conversion first.')
        if path.suffix.lower() == '.png':
            with path.open('rb') as stream:
                header = stream.read(29)
            if len(header) >= 25 and header[24] > 8:
                raise ValueError('16-bit PNG is not silently reduced to 8-bit. Prepare a color-managed preview first.')
        if path.suffix.lower() in {'.tif', '.tiff'}:
            bits = opened.tag_v2.get(258, (8,))
            bits = (bits,) if isinstance(bits, int) else bits
            if max(bits) > 8:
                raise ValueError('High-bit-depth TIFF requires explicit preview conversion first.')
        if 'A' in opened.getbands() or 'transparency' in opened.info:
            rgba = opened.convert('RGBA')
            if rgba.getchannel('A').getextrema() != (255, 255):
                raise ValueError('Transparent image requires explicit compositing onto a chosen background first.')
        profile = opened.info.get('icc_profile')
        assumptions = []
        oriented = ImageOps.exif_transpose(opened)
        if profile:
            try:
                src = ImageCms.ImageCmsProfile(io.BytesIO(profile))
                dst = ImageCms.createProfile('sRGB')
                work = oriented
                if work.mode in {'P', 'RGBA', 'LA', '1'}:
                    work = work.convert('RGB')
                normalized = ImageCms.profileToProfile(work, src, dst, outputMode='RGB')
                profile_note = f'ICC converted to sRGB: {ImageCms.getProfileName(src).strip()}'
            except Exception as error:
                raise ValueError(f'ICC conversion failed; refusing to discard the profile: {error}') from error
        else:
            if original_mode not in {'RGB', 'RGBA', 'L', 'LA', 'P', '1'}:
                raise ValueError(f'Untagged {original_mode} image cannot safely be assumed sRGB.')
            normalized = oriented.convert('RGB')
            profile_note = 'No ICC profile; assumed sRGB.'
            assumptions.append(profile_note)
            gamma = opened.info.get('gamma')
            if gamma is not None and abs(float(gamma) - .45455) > .02 and 'srgb' not in opened.info:
                raise ValueError(f'PNG gamma {gamma} is not an ordinary sRGB preview. Convert with color management first.')
        metadata = {'format': opened.format, 'original_mode': original_mode, 'width': normalized.width, 'height': normalized.height,
                    'orientation': 'EXIF applied', 'profile': profile_note, 'output_encoding': 'sRGB display-referred 8-bit RGB'}
        return normalized.copy(), metadata, assumptions


def srgb_bytes():
    return ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()


def font(size, supplied=None):
    candidates = [supplied] if supplied else []
    candidates += [r'C:\Windows\Fonts\msyh.ttc', r'C:\Windows\Fonts\simhei.ttf',
                   '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/System/Library/Fonts/PingFang.ttc']
    for item in candidates:
        if item and Path(item).is_file():
            return ImageFont.truetype(str(item), size)
    raise ValueError('No Chinese font found. Pass --font with a Chinese-capable TTF/TTC/OTF font.')


def fit_image(image, size):
    return ImageOps.contain(image, size, Image.Resampling.LANCZOS)


def paste_fit(canvas, image, box):
    x, y, w, h = box
    fitted = fit_image(image, (w, h))
    canvas.paste(fitted, (x + (w - fitted.width) // 2, y + (h - fitted.height) // 2))


def shortened(draw, text, chosen_font, width):
    text = str(text).replace('\n', ' ')
    while text and draw.textbbox((0, 0), text, font=chosen_font)[2] > width:
        text = text[:-2] + '…' if len(text) > 2 else ''
    return text


def make_contacts(frames, outputs, supplied_font=None):
    text_font = font(19, supplied_font)
    for page, output in enumerate(outputs):
        items = frames[page * 24:(page + 1) * 24]
        cols, cellw, cellh = 4, 320, 212
        canvas = Image.new('RGB', (cols * cellw, math.ceil(len(items) / cols) * cellh + 54), '#15181c')
        draw = ImageDraw.Draw(canvas)
        draw.text((14, 14), '候选帧｜时间为请求 seek 时间；请视觉筛选', font=text_font, fill='#eeeeee')
        for idx, frame in enumerate(items):
            x, y = (idx % cols) * cellw, 54 + (idx // cols) * cellh
            with Image.open(frame['path']) as picture:
                paste_fit(canvas, picture.convert('RGB'), (x + 4, y, cellw - 8, 176))
            label = frame.get('label', frame['filename'])
            draw.text((x + 6, y + 183), shortened(draw, label, text_font, cellw - 12), font=text_font, fill='#eeeeee')
        canvas.save(output, quality=94, subsampling=0, icc_profile=srgb_bytes())


def command_probe(args):
    path = source_path(args.input)
    if path.suffix.lower() in IMAGE_EXTENSIONS:
        _, metadata, assumptions = image_rgb(path)
        result = {'source': str(path), 'image': metadata, 'assumptions': assumptions, 'ffprobe': ffprobe(path)}
    else:
        result = ffprobe(path)
    if args.out:
        if Path(args.out).expanduser().resolve() == path:
            raise ValueError('Metadata output must differ from the input.')
        available([args.out], args.overwrite)
        save_json(args.out, result)
    return result


def command_extract(args):
    source = source_path(args.input)
    out = Path(args.out).expanduser().resolve()
    if source.suffix.lower() in IMAGE_EXTENSIONS:
        picture, metadata, assumptions = image_rgb(source)
        output = out / 'frame_001.png'
        contacts = [out / 'contacts_01.jpg']
        if source in [output, *contacts, out / 'manifest.json']:
            raise ValueError('Extraction output would overwrite the source.')
        available([output, *contacts, out / 'manifest.json'], args.overwrite)
        picture.save(output, icc_profile=srgb_bytes())
        frames = [{'path': str(output), 'filename': output.name, 'label': '01｜原图（EXIF / ICC 归一化）', 'requested_seek_seconds': None}]
        selection = 'single normalized still image'
    else:
        metadata, stream, assumptions = video_context(source, args.matrix)
        duration = float(stream.get('duration') or metadata.get('format', {}).get('duration') or 0)
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError('A finite video duration is required.')
        if args.times:
            times = [float(x.strip()) for x in args.times.split(',')]
            selection = 'explicit requested timestamps; agent must visually confirm their suitability'
        else:
            times = [(idx + .5) * duration / args.count for idx in range(args.count)]
            selection = 'uniform temporal candidates, NOT codec I-frames and NOT visually selected keyframes'
        if any(not math.isfinite(t) or t < 0 or t >= duration for t in times):
            raise ValueError(f'Each time must be finite and in [0, {duration}).')
        outputs = [out / f'frame_{idx + 1:03d}_{t:010.3f}s.png' for idx, t in enumerate(times)]
        contacts = [out / f'contacts_{idx + 1:02d}.jpg' for idx in range(math.ceil(len(times) / 24))]
        if source in [*outputs, *contacts, out / 'manifest.json']:
            raise ValueError('Extraction output would overwrite the source.')
        available([*outputs, *contacts, out / 'manifest.json'], args.overwrite)
        frames = []
        for idx, (time, output) in enumerate(zip(times, outputs)):
            run([executable('ffmpeg'), '-hide_banner', '-loglevel', 'error', '-y', '-i', source,
                 '-ss', f'{time:.9f}', '-map', f'0:{stream["index"]}', '-frames:v', '1',
                 '-vf', 'scale=in_color_matrix=bt709:out_color_matrix=bt709,format=rgb24', '-threads', '1', output])
            # RGB screenshots follow the common SDR display-code-value convention.
            with Image.open(output) as frame_image:
                frame_image.save(output, icc_profile=srgb_bytes())
            frames.append({'path': str(output), 'filename': output.name, 'label': f'{idx + 1:02d}｜请求 {time:.3f} 秒',
                           'requested_seek_seconds': time, 'actual_frame_pts_seconds': None})
        assumptions.append('seek timestamps are requested positions; exact decoded frame PTS was not measured, especially relevant for VFR.')
        assumptions.append('Preview PNG uses decoded SDR display RGB code values tagged sRGB; no transfer-curve remapping is performed.')
    make_contacts(frames, contacts, args.font)
    manifest = {'source': str(source), 'selection': selection, 'metadata': metadata, 'assumptions': assumptions,
                'frames': frames, 'contacts': [str(x) for x in contacts]}
    save_json(out / 'manifest.json', manifest)
    return {'manifest': str(out / 'manifest.json'), 'frames': len(frames), 'contacts': manifest['contacts']}


def validate_cube(path):
    size, entries, domain_min, domain_max = None, 0, [0., 0., 0.], [1., 1., 1.]
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        stripped = line.split('#', 1)[0].strip()
        if not stripped:
            continue
        parts = stripped.split()
        token = parts[0].upper()
        if token == 'TITLE':
            continue
        if token == 'LUT_3D_SIZE':
            size = int(parts[1])
        elif token == 'DOMAIN_MIN':
            domain_min = list(map(float, parts[1:]))
        elif token == 'DOMAIN_MAX':
            domain_max = list(map(float, parts[1:]))
        elif token.startswith('LUT_'):
            raise ValueError('Only a standalone 3D .cube is supported; no combined 1D shaper.')
        else:
            values = list(map(float, parts))
            if len(values) != 3 or not all(math.isfinite(v) and 0 <= v <= 1 for v in values):
                raise ValueError('LUT must contain finite normalized RGB triples in [0,1].')
            entries += 1
    if size is None or size < 2 or size > 256 or entries != size ** 3:
        raise ValueError(f'Invalid cube dimensions: size={size}, data rows={entries}.')
    if domain_min != [0., 0., 0.] or domain_max != [1., 1., 1.]:
        raise ValueError('This workflow requires DOMAIN_MIN 0 0 0 and DOMAIN_MAX 1 1 1.')
    return {'size': size, 'rows': entries, 'sha256': file_sha256(path)}


def command_render(args):
    source, lut = source_path(args.input), source_path(args.lut)
    destination = Path(args.out).expanduser().resolve()
    if destination in {source, lut}:
        raise ValueError('Render output must differ from input and LUT.')
    sidecar = Path(str(destination) + '.json')
    if sidecar in {source, lut}:
        raise ValueError('Render sidecar must differ from input and LUT.')
    available([destination, sidecar], args.overwrite)
    cube = validate_cube(lut)
    is_image = source.suffix.lower() in IMAGE_EXTENSIONS
    if is_image:
        if destination.suffix.lower() not in {'.jpg', '.jpeg', '.png'}:
            raise ValueError('Image preview output must be PNG or JPEG.')
        picture, metadata, assumptions = image_rgb(source)
    else:
        if destination.suffix.lower() not in {'.mp4', '.mov', '.mkv'}:
            raise ValueError('Video preview output must be MP4, MOV or MKV.')
        metadata, stream, assumptions = video_context(source, args.matrix)
        if stream.get('width', 0) % 2 or stream.get('height', 0) % 2:
            raise ValueError('yuv420p H.264 preview requires even dimensions; prepare a reviewed canvas first.')
    # LUT path inside filter is ASCII and relative to cwd, avoiding Windows colon/backslash escaping.
    with tempfile.TemporaryDirectory(prefix='lut-render-') as temp:
        work = Path(temp)
        shutil.copyfile(lut, work / 'look.cube')
        if is_image:
            picture.save(work / 'input.png', icc_profile=srgb_bytes())
            run([executable('ffmpeg'), '-hide_banner', '-loglevel', 'error', '-y', '-i', 'input.png',
                 '-vf', 'format=gbrp,lut3d=file=look.cube:interp=tetrahedral,format=rgb24',
                 '-frames:v', '1', '-threads', '1', 'graded.png'], cwd=work)
            with Image.open(work / 'graded.png') as graded:
                options = {'icc_profile': srgb_bytes()}
                if destination.suffix.lower() in {'.jpg', '.jpeg'}:
                    options.update(quality=96, subsampling=0)
                graded.save(destination, **options)
        else:
            filter_chain = ('scale=in_color_matrix=bt709:out_color_matrix=bt709,format=gbrp16le,'
                            'lut3d=file=look.cube:interp=tetrahedral,'
                            'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p')
            common = [executable('ffmpeg'), '-hide_banner', '-loglevel', 'error', '-y', '-i', source,
                      '-map', f'0:{stream["index"]}', '-map', '0:a?', '-map_metadata', '0', '-vf', filter_chain,
                      '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-fps_mode', 'passthrough',
                      '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv',
                      '-bsf:v', 'h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0']
            tail = ['-movflags', '+faststart'] if destination.suffix.lower() in {'.mp4', '.mov'} else []
            run(common + ['-c:a', 'copy'] + tail + [destination], cwd=work)
            output_probe = ffprobe(destination)
            output_video = next(s for s in output_probe['streams'] if s.get('codec_type') == 'video')
            # FFmpeg honors display rotation; dimensions may be transposed accordingly.
            before_dimensions = sorted([stream['width'], stream['height']])
            after_dimensions = sorted([output_video['width'], output_video['height']])
            if before_dimensions != after_dimensions:
                raise RuntimeError('Unexpected output dimension change; inspect the render before delivery.')
            if any(output_video.get(key) != 'bt709' for key in ['color_primaries', 'color_transfer', 'color_space']):
                raise RuntimeError('Output BT.709 tags were not preserved; inspect color management before delivery.')
            input_audio = sum(s.get('codec_type') == 'audio' for s in metadata['streams'])
            output_audio = sum(s.get('codec_type') == 'audio' for s in output_probe['streams'])
            if input_audio != output_audio:
                raise RuntimeError('Output audio stream count changed unexpectedly.')
            assumptions.append('Preview is 8-bit H.264 yuv420p CRF 18; audio copied without re-encoding. Source frame timestamps passed through.')
    result = {'input': str(source), 'lut': str(lut), 'lut_validation': cube, 'output': str(destination),
              'interpolation': 'FFmpeg lut3d tetrahedral', 'lut_strength': 1.0,
              'input_metadata': metadata, 'assumptions': assumptions}
    save_json(sidecar, result)
    return {'output': str(destination), 'manifest': str(sidecar), 'lut_sha256': cube['sha256']}


def command_compare(args):
    spec_path = source_path(args.spec)
    spec = json.loads(spec_path.read_text(encoding='utf-8-sig'))
    rows = spec.get('rows')
    if not isinstance(rows, list) or not rows:
        raise ValueError('Comparison spec needs a nonempty rows array.')
    paths = []
    for row in rows:
        resolved = []
        for key in ['reference', 'before', 'after']:
            value = Path(row[key])
            resolved.append(source_path(value if value.is_absolute() else spec_path.parent / value))
        paths.append(resolved)
    destination = Path(args.out).expanduser().resolve()
    if destination.suffix.lower() not in {'.jpg', '.jpeg', '.png'}:
        raise ValueError('Comparison output must be JPG or PNG.')
    per_page = args.rows_per_page or len(rows)
    pages = math.ceil(len(rows) / per_page)
    outputs = [destination if idx == 0 else destination.with_name(f'{destination.stem}_{idx + 1:02d}{destination.suffix}') for idx in range(pages)]
    inputs = {spec_path, *(path for group in paths for path in group)}
    if any(path in inputs for path in outputs):
        raise ValueError('Comparison output must differ from all inputs and the spec.')
    available(outputs, args.overwrite)
    title_font, label_font, small_font = font(32, args.font), font(23, args.font), font(18, args.font)
    margin, gap, cellw, cellh = 24, 12, args.cell_width, args.cell_height
    width = margin * 2 + cellw * 3 + gap * 2
    for page, output in enumerate(outputs):
        start, stop = page * per_page, min((page + 1) * per_page, len(rows))
        canvas = Image.new('RGB', (width, 152 + (stop - start) * (cellh + 45) + margin), '#14181c')
        draw = ImageDraw.Draw(canvas)
        draw.text((margin, 16), shortened(draw, spec.get('title', '参考风格与 LUT 实际效果'), title_font, width - 2 * margin), font=title_font, fill='#ffffff')
        draw.text((margin, 62), shortened(draw, spec.get('subtitle', '同一目标帧｜完整画幅｜实际加载最终 LUT'), small_font, width - 2 * margin), font=small_font, fill='#aab5bc')
        for column, label in enumerate(['参考风格', '目标原片', '最终 LUT 实渲']):
            draw.text((margin + column * (cellw + gap), 104), label, font=label_font, fill='#dcebdc')
        for index in range(start, stop):
            top = 152 + (index - start) * (cellh + 45)
            for column, path in enumerate(paths[index]):
                picture, _, _ = image_rgb(path)
                left = margin + column * (cellw + gap)
                draw.rectangle((left, top, left + cellw - 1, top + cellh - 1), fill='#050607')
                paste_fit(canvas, picture, (left, top, cellw, cellh))
            draw.text((margin, top + cellh + 10), shortened(draw, rows[index].get('label', f'样本 {index + 1}'), small_font, width - 2 * margin), font=small_font, fill='#bec9ce')
        options = {'icc_profile': srgb_bytes()}
        if output.suffix.lower() in {'.jpg', '.jpeg'}:
            options.update(quality=95, subsampling=0)
        canvas.save(output, **options)
    return {'outputs': [str(x) for x in outputs], 'rows': len(rows), 'layout': 'reference / before / actual LUT render; letterbox, no cropping'}


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def command_package(args):
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError('Package root must be a directory.')
    output = Path(args.out).expanduser().resolve()
    available([output], args.overwrite)
    files, names = [], set()
    for value in args.files:
        relative = Path(value)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError(f'Package entries must be explicit relative paths without traversal: {value}')
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file() or path == output:
            raise ValueError(f'Invalid, missing, escaping, directory or self-referential package entry: {value}')
        name = relative.as_posix()
        if name.lower() in names or name.lower() == 'sha256_manifest.json':
            raise ValueError(f'Duplicate or reserved package entry: {value}')
        names.add(name.lower())
        files.append((path, name))
    manifest = {'algorithm': 'SHA-256', 'files': [{'path': name, 'bytes': path.stat().st_size, 'sha256': file_sha256(path)} for path, name in files]}
    handle, temporary = tempfile.mkstemp(prefix='lut-package-', suffix='.zip', dir=output.parent)
    os.close(handle)
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for path, name in files:
                archive.write(path, name)
            archive.writestr('SHA256_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2))
        with zipfile.ZipFile(temporary, 'r') as archive:
            bad = archive.testzip()
            if bad:
                raise RuntimeError(f'ZIP CRC validation failed: {bad}')
        os.replace(temporary, output)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return {'output': str(output), 'entries': len(files) + 1, 'bytes': output.stat().st_size, 'sha256': file_sha256(output)}


def positive_int(value):
    result = int(value)
    if result <= 0:
        raise argparse.ArgumentTypeError('Must be a positive integer.')
    return result


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    probe = commands.add_parser('probe', help='Print/save media metadata without changing the input.')
    probe.add_argument('input')
    probe.add_argument('--out')
    extract = commands.add_parser('extract', help='Normalize a still or extract timed video candidates plus contacts and manifest.')
    extract.add_argument('input')
    extract.add_argument('--out', required=True)
    extract.add_argument('--count', type=positive_int, default=16)
    extract.add_argument('--times', help='Comma-separated selected seconds; overrides --count.')
    extract.add_argument('--matrix', choices=['auto', 'bt709'], default='auto')
    extract.add_argument('--font')
    render = commands.add_parser('render', help='Load a real cube and render it with tetrahedral interpolation at 100%%.')
    render.add_argument('input')
    render.add_argument('--lut', required=True)
    render.add_argument('--out', required=True)
    render.add_argument('--matrix', choices=['auto', 'bt709'], default='auto')
    compare = commands.add_parser('compare', help='Build labeled reference/before/after rows with full-image letterboxing.')
    compare.add_argument('--spec', required=True)
    compare.add_argument('--out', required=True)
    compare.add_argument('--rows-per-page', type=positive_int)
    compare.add_argument('--cell-width', type=positive_int, default=640)
    compare.add_argument('--cell-height', type=positive_int, default=360)
    compare.add_argument('--font')
    package = commands.add_parser('package', help='ZIP only explicit relative files and an embedded SHA-256 manifest.')
    package.add_argument('--root', required=True)
    package.add_argument('--files', nargs='+', required=True)
    package.add_argument('--out', required=True)
    for command in [probe, extract, render, compare, package]:
        command.add_argument('--overwrite', action='store_true', help='Allow replacing named output files; input is never overwritten.')
    args = parser.parse_args()
    try:
        result = globals()[f'command_{args.command}'](args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, RuntimeError, OSError, KeyError, json.JSONDecodeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
