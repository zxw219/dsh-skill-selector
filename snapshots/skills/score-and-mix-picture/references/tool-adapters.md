# Tool Adapter Contract

Keep the workflow stable while tools change. Choose adapters by capability, not brand.

## 1. Picture Inspection Adapter

### Required input

- local video path, accessible URL, or active editor timeline;
- original audio when it exists.

### Required output

- duration, frame rate, resolution, and audio-stream facts;
- time-aware visual observations;
- transcript/dialogue or an explicit statement that speech is unavailable;
- scene/transition candidates and silence candidates;
- enough evidence to build a semantic spotting map.

### Current implementations

- Preferred local semantic path: the host's video-understanding capability plus `scripts/probe_media.py`; optional `$watch` can supply the former.
- Editor-only media: use the editor's frame/timeline inspection capability and project state.
- Metadata-only fallback is insufficient for final musical judgment.

## 2. Music Generation Adapter

### Required input

- exact target duration or section durations;
- timecoded form;
- musical controls and ending behavior;
- optional reference audio roles;
- requested master/stems format.

### Required output

- playable audio file with known duration and format;
- stable source identity or path;
- model/settings when available;
- stems when requested and supported.

### Failure types

- `NO_GENERATOR`: deliver prompts and await returned audio.
- `DURATION_MISMATCH`: edit if musical form survives; otherwise regenerate.
- `STRUCTURE_MISS`: revise the timecoded prompt rather than stretching aggressively.
- `ARTIFACTS_OR_CLIPPING`: request a cleaner render or alternate take.

Do not hard-code current platform controls into the core method. Verify official controls when a named platform matters.

## 3. Audio Edit / Mix Adapter

### Required input

- locked picture;
- one or more music files/stems;
- edit map with source and timeline ranges;
- original-audio policy;
- ducking and loudness targets.

### Required output

- score-only master aligned to picture;
- optional SFX stem aligned to picture;
- full mix when original audio exists;
- probe/loudness report and hashes;
- editable timeline when explicitly requested.

### Current implementations

- Deterministic local master render: `scripts/render_picture_mix.py` using FFmpeg.
- Editable NLE: reproduce the same clip placements, fades, levels, and ducking with the available editor; export only after verification or explicit delivery request.

## 3A. SFX Asset Adapter

### Required input

- physical/source description, material, action, scale, perspective, and target timecode.

### Required output

- playable local audio path;
- duration/channel/sample-rate metadata;
- source/license identity and SHA-256;
- tags that help retrieval but do not replace auditioning.

### Current implementation

- `scripts/search_sfx.py` queries the bundled 360-file CC0 catalog.
- `scripts/build_sfx_catalog.py` verifies files and rebuilds metadata after approved expansion.
- `references/sfx-sources.json` is the provenance authority; `references/sfx-catalog.json` is the retrieval index.

If no local asset matches, acquire a new clearly licensed source, archive its provenance, rebuild the catalog, and audition before timeline use.

## 4. Compatibility Test

A replacement adapter passes only if it can handle:

1. one full-length cue with an intentional silent opening;
2. multiple cue instances with overlaps/crossfades;
3. a picture with dialogue that triggers music ducking while SFX remain on a separate bus;
4. a silent picture without falsely claiming dialogue protection;
5. exact-duration WAV output and a machine-readable report;
6. a failed case such as insufficient source duration without looping.
