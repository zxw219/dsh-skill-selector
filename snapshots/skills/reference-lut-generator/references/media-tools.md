# 媒体准备与交付脚本

`scripts/media_tools.py` 负责真实素材抽帧、实际 LUT 渲染、三栏排版和显式打包。调色模型由 `grade_engine.py` 负责。本脚本不会自动判定哪一帧具有代表性，也不会把网页截图当作视频源。

## 环境

需要 Python 3.10+、Pillow（含 ImageCms）以及带 `lut3d` 和 `libx264` 的 FFmpeg/ffprobe。命令示例中的 `python` 代表当前可用解释器，不要求全局安装。FFmpeg/ffprobe 通过 PATH 查找，也可以设置 `FFMPEG`、`FFPROBE` 为可执行文件绝对路径。中文排版自动尝试微软雅黑、黑体、Noto CJK、苹方；缺少字体时通过 `--font` 指定字体文件。

所有输出默认拒绝覆盖，确认需要重做时使用 `--overwrite`。脚本不覆盖输入原件。调用 subprocess 使用参数数组，Windows 下实际 LUT 被复制为临时目录中的 ASCII 文件名 `look.cube`，避免 filter 中盘符、反斜杠及中文路径转义问题。

## 1. 检查媒体

```powershell
python media_tools.py probe "reference.mp4" --out "work/reference_probe.json"
```

视频返回 ffprobe 原始 JSON，图片额外返回 EXIF/ICC 归一化信息。先检查时长、帧率、尺寸、像素格式、色域、transfer、matrix 和 range。10 bit 不是 HDR 的充分证据；未标注 transfer 也不证明它是 SDR。

## 2. 提取候选帧，再按视觉选择的时间重提

```powershell
python media_tools.py extract "reference.mp4" --out "work/reference_candidates" --count 20
python media_tools.py extract "reference.mp4" --out "work/reference_selected" --times "2.4,14.8,37.2,56.0"
python media_tools.py extract "target.jpg" --out "work/target_image"
```

均匀采样覆盖时长内的等分中点，是候选帧，不是压缩编码 I 帧，也不是自动选出的审美关键帧。查看 `contacts_*.jpg`，排除黑场、转场、字幕遮挡和异常闪光，并按人物、室内、室外、明暗、肤色及主要色相选代表帧。随后用 `--times` 记录人工选择。每张输出 PNG 保留整幅画面，manifest 中写入源文件、元数据、假设和 `requested_seek_seconds`。

FFmpeg 在输入后执行 seek；时间标记是请求的位置，不声称为测得的精确帧 PTS。manifest 的 `actual_frame_pts_seconds` 为 null，VFR 素材尤其需保留这个区别。

未标注 matrix 的视频会拒绝处理。确认普通 SDR BT.709 后可显式追加 `--matrix bt709`，该选择记录为假设；不能仅凭 10 bit 或分辨率做此判断。已标注的非 BT.709 色域、PQ/HLG 或 BT.2020 会拒绝处理；标记 sRGB transfer 的视频也要求先正确归一化，避免直接改标签成 BT.709。需要先用明确的色彩管理流程转为 SDR Rec.709。本脚本没有 Log/HDR 识别、色域变换或色调映射功能。`--matrix bt709` 不是 HDR→SDR 转换。

普通图片会应用 EXIF 方向、用 ICC 转成 sRGB，再输出有 sRGB ICC 的 RGB PNG。无 ICC 的普通 RGB/灰度图会注明 sRGB 假设。ICC 转换失败、有透明像素、多帧图片、未标注 CMYK、16 bit/float 图会明确报错，要求先准备可确认的 SDR 预览；不会静默丢弃配置。视频截帧沿用常见 SDR 显示 RGB 数值并标记 sRGB，不宣称对 Rec.709 OETF 与 sRGB 做了精确互转。

## 3. 用最终交付的 cube 实际渲染

```powershell
python media_tools.py render "work/target_image/frame_001.png" --lut "LUT/look_33.cube" --out "预览/目标图_调色.png"
python media_tools.py render "target.mp4" --lut "LUT/look_33.cube" --out "预览/目标视频_调色.mp4" --matrix bt709
```

加载真正的 `.cube`，使用 FFmpeg `lut3d` 的 tetrahedral 插值、100% 强度。验证 3D 网格行数、有限值、0–1 数值范围以及标准 DOMAIN；不接受 1D shaper+3D 组合文件。输出同名 `.json` 记录输入元数据、LUT SHA-256、插值和假设。

图片支持输出 PNG/JPG，并保留 sRGB ICC。视频完整渲染首个实际视频流并保留所有音频流，保持画幅与源时间戳，输出 H.264 CRF 18、8 bit yuv420p 和显式 BT.709 / limited-range 标签；同时用 H.264 metadata bitstream filter 写入码流标签，并通过 ffprobe 检查色彩标签及音频流数量。显示旋转由 FFmpeg 处理，竖拍文件可能交换编码宽高以保持正确显示方向。音频直接复制；若源音频无法放入所选容器，命令会报错，可改用 MKV 或经明确决定转码音频。奇数宽高拒绝自动补边，需要先确认画幅处理。此输出是审片预览，不是无损或 10 bit 母版。

不要用另一套近似 Python 调色函数生成“最终效果”栏来冒充交付 LUT 的输出；三栏右侧应使用上述真实渲染结果，或从实际渲染视频相同时间提取的帧。若调色模型或 LUT 强度改变，要重新渲染。

## 4. 三栏对比

准备 JSON，图片相对路径按 JSON 所在目录解析：

```json
{
  "title": "参考风格与最终 LUT 对比",
  "subtitle": "完整画幅｜右栏为最终交付 LUT 的实际输出",
  "rows": [
    {
      "reference": "reference/frame_003.png",
      "before": "target/frame_002.png",
      "after": "graded/frame_002.png",
      "label": "室内人像｜参考请求 12.400 秒｜目标请求 6.800 秒"
    }
  ]
}
```

```powershell
python media_tools.py compare --spec "work/comparison.json" --out "预览/三栏对比.jpg" --rows-per-page 4
```

列顺序固定为参考风格、目标原片、最终 LUT 实渲。不同画幅等比例缩入统一画框并留黑边，保留完整画面，禁止为凑齐版式裁切人物。默认每格 640×360，可用 `--cell-width`、`--cell-height` 设置。分页第一张使用请求文件名，其余追加 `_02` 等。说明文字过长会截断；每行标签应简洁，详细时间及来源放 manifest。

脚本只能排版，不能验证 before/after 是否相同帧，也不能证明右栏来源。代理必须根据渲染记录和视觉核对这些条件。

## 5. 只打包明确的交付文件

```powershell
python media_tools.py package --root "deliverable" --files "LUT/look_33.cube" "LUT/look_65.cube" "预览/三栏对比.jpg" "预览/目标视频_调色.mp4" "使用说明.md" "制作记录.json" --out "look_完整交付包.zip"
```

`--files` 是明确的相对文件路径列表，不接受目录、越界路径、缺失文件、重复路径或 ZIP 自身。不会递归塞入整个工作区或源素材；调用者应只列必要交付物。ZIP 内自动增加 `SHA256_MANIFEST.json`，列出各文件字节数和 SHA-256，并在交付前验证 ZIP CRC。输出 JSON 另给整个 ZIP 的 SHA-256。

对已有作品的公开链接，先取得允许访问的真实媒体文件并记录 URL；下载或登录能力由当前环境的授权工具提供，本脚本不下载、不绕过访问限制。不要把下载方法或目录结构当作最终审美质量的保证。
