# 参数化 LUT 配方

`scripts/grade_engine.py` 依赖 NumPy；`validate` 还需要 FFmpeg（PATH 或 `--ffmpeg`）。不依赖 SciPy。建议 `python -B` 避免向技能目录写入缓存。

该引擎将经过视觉设计的配方烘焙为 LUT。它不自动分析参考、不训练颜色迁移模型，也不把参考画面的平均色强加给所有素材。先检查参考和目标关键帧，再从 `neutral-recipe.json` 开始调整。`chunye-example.json` 只是本次冷青绿美学的近似演示配方，不是旧版 Chunye 函数的精确复制，更不是通用默认值。

## 颜色管理边界

- 输入和输出均为 **display-referred、编码 RGB、0..1**。`working_space` 必须声明为 `Rec709` 或 `sRGB`，本字段只作声明，**不会执行 transfer、primaries、ICC、range、Log 或 HDR 转换**。
- Rec.709 与 sRGB 共用色度坐标，但传递函数和显示约定不同。不要因为都叫 SDR 就声称二者可精确互换。视频及图片应在媒体步骤先规范到明确的工作空间，或分别创建配方／交付版本，并在说明中写明假设。
- 未知视频标签、未知相机 Log、HDR、未经管理的图片 ICC 不应默认为已准确规范。先解决输入解释；不要把 gamma 修正偷偷混进“风格匹配”。
- 曲线的“亮度”是编码 RGB 按 `[0.2126, 0.7152, 0.0722]` 的加权值，不是线性光曝光或物理亮度。gain/offset 也只是简洁的 RGB 色彩平衡，不是开尔文白平衡。
- 颗粒、模糊、锐化、光晕、暗角、局部照明、按人脸或物体选择的调色都不能写入这种静态 3D LUT。

## JSON 字段

所有数字必须有限。未知键、重复键、明显坏曲线会报错。除 `schema_version` 和 `working_space` 必填外，省略项采用中性默认值；嵌套对象也按其字段补默认。

| 字段 | 类型／范围 | 含义 |
|---|---|---|
| `schema_version` | 整数 `1` | 当前配方版本 |
| `working_space` | `"Rec709"` 或 `"sRGB"` | 已规范素材的工作空间声明 |
| `description` | 字符串，至多 2000 字符 | 人类可读的风格目标与输入假设 |
| `curve` | 2–32 个 `[input, output]` | 输入从 0 到 1，严格递增，间距 ≥ 0.00001；输出在 0..1 且不递减；总输出跨度 ≥ 0.1。单调 PCHIP 插值，可提黑或压白 |
| `gain` | 3 个数，各 0.25..4；默认 `[1,1,1]` | 编码 RGB 逐通道乘数 |
| `offset` | 3 个数，各 -0.25..0.25；默认 `[0,0,0]` | 编码 RGB 逐通道偏移 |
| `saturation` | 0..2，默认 1 | 围绕亮度轴的全局色度倍率 |
| `hue_selections` | 至多 12 个对象，默认空 | 柔和色相选区，见下文 |
| `tints` | `shadows`、`midtones`、`highlights` | 每项为 RGB 三元组，各 -0.2..0.2，默认全零；输出编码 RGB 偏移，自动去掉加权亮度分量 |
| `near_black` | `start`、`end`、`amount` | `start` 0..0.1 默认 0；`end` 0.005..0.25 默认 0.06，必须比 start 大至少 0.005；`amount` 0..1 默认 1 |
| `skin_protection` | `amount`、`center`、`width` | `amount` 0..1 默认 0；center 0..360 度默认 35；width 5..90 度默认 30 |
| `strength` | 0..1，默认 1 | 与原始输入 RGB 的总混合强度；烘焙后导入软件建议先用 100% |

色相选区格式：

```json
{"center": 225, "width": 50, "hue_shift": -10, "saturation": 0.85}
```

`center` 与 `width` 必填，单位为度。center 范围 0..360，width 是选区半宽 5..180；红 0、黄 60、绿 120、青 180、蓝 240、品红 300。权重从中心平滑降至半宽处的零，跨 0/360 连续；低饱和度区域自动减弱影响。`hue_shift` -90..90 度，默认 0；`saturation` 0..2 倍，默认 1。多个选区同时基于修改前的色相计算，色相偏移相加、饱和倍率相乘；避免过多重叠的强选区。

三段 tint 依据平衡后的输入亮度混合：阴影由 0.15 到 0.5 平滑退去，高光由 0.5 到 0.85 平滑进入，中间调填余量。它们改变色度，不直接改变曲线目标亮度。

`near_black.amount=1` 时，start 以下不施加颜色变化，end 以上恢复完整颜色变化；亮度曲线仍生效。`skin_protection` 仅对原始 RGB 的某段色相／饱和度减少颜色变化，同色衣物、木材等也会被保护，**不是语义人脸蒙版**。这两项向“保持原色相的亮度曲线结果”混合，不取消亮度变化。

计算顺序：RGB gain/offset → 亮度曲线 → HSV 色相选区与全局色度 → 三段 tint → 近黑和类肤色保护 → 沿亮度轴压缩越界色度 → 总强度混合。超出 0..1 的色度被压回 RGB 立方体，强设置可能压缩鲜艳色的色差；必须检查目标画面。

## 命令

```powershell
python -B scripts/grade_engine.py init --out work/recipe.json
python -B scripts/grade_engine.py build --recipe work/recipe.json --out-dir work/LUT --name MyLook_Rec709 --sizes 33 65
python -B scripts/grade_engine.py validate --recipe work/recipe.json --lut work/LUT/MyLook_Rec709_33.cube --report work/validation_33.json
python -B scripts/grade_engine.py validate --recipe work/recipe.json --lut work/LUT/MyLook_Rec709_65.cube --report work/validation_65.json
```

`init --working-space sRGB` 创建 sRGB 声明版本。`--name` 使用简短 ASCII 文件名（字母、数字、下划线、短横线、点）。文件默认不覆盖；明确需要替换自己的旧输出时追加 `--overwrite`。已有交付应优先版本化保存。

Python 集成接口：`load_recipe(path)` 返回校验并补全的字典；`grade(rgb, recipe)` 接受 `(..., 3)` 浮点数组；`write_cube(recipe, size, path, overwrite=False)` 输出 .cube。直接调用 `grade` 的配方应先经 `load_recipe` 或 `normalize_recipe` 校验。

## 验收报告

33³ 和 65³ 均按 **red-fastest** 顺序写出。`validate` 读取实际文件检查条目数、domain、边界和有限值，然后把 **65536 个随机 RGB 与 4096 级灰阶**作为 float RGB 帧送入 FFmpeg，让 `lut3d` 实际加载该 .cube 并采用 tetrahedral 插值。结果与配方函数比较；不会只测内存函数。

报告包含 .cube SHA-256、规范化配方 SHA-256、条目数、边界、随机样本的平均／p99／最大误差（8-bit code units）、实际灰阶输出的亮度单调性、RGB 各通道单调诊断和端点。灰阶亮度允许 0.000002 浮点容差；RGB 各通道诊断不单独作为失败条件。

默认误差阈值：mean ≤ 0.35、p99 ≤ 1.5、max ≤ 12。失败返回退出码 2 并保留报告；输入或执行错误返回 1。中性 identity 应远低于这些阈值。若强烈局部色相操作使 33³ 超限，优先平滑配方或测试 65³；不要为通过而随意放宽阈值。定制阈值 `--max-mae8`、`--max-p99-8`、`--max-error8` 会记录在报告中，需解释理由。

数值通过只确认格式、插值和基本灰阶连续性。它不证明匹配参考、不证明每个场景好看，也不代替用实际交付 LUT 渲染目标并检查皮肤、黑白端、鲜艳颜色与三栏对比。
