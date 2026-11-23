# 现成视频后期：framecraft 3.0

基于系统里的 FFmpeg 和 FFprobe，只用 Python 标准库。它不生成动作，只在**已经确定的接触帧**上精准叠加效果。原文件永远不动，输出永远是新文件。

需要：Python 3.9+、FFmpeg、FFprobe（终端里 `ffmpeg -version` 能跑通）。

## 一、推荐流程

1. `inspect` 看帧率、时长、有无音轨。
2. `detect` 自动列出画面突变点，作为候选击点。
3. `sheet` 导出候选时刻前后的连帧图，确认哪一帧是真正的接触帧。
4. `apply` 用配方或击点表渲染。
5. 原速、带声音复看；需要时 `safety` 再查一次闪烁。

不想记命令：`python scripts/framecraft.py menu`，跟着数字走。

## 二、命令

```bash
python scripts/framecraft.py inspect --input fight.mp4
python scripts/framecraft.py recipes
python scripts/framecraft.py detect  --input fight.mp4 --top 8
python scripts/framecraft.py sheet   --input fight.mp4 --at 3.40 --span 4 --output hit-3.40.png
python scripts/framecraft.py apply   --input fight.mp4 --at 3.40 --recipe heavy --focus 0.58,0.42 --output fight-hit.mp4
python scripts/framecraft.py apply   --input fight.mp4 --at 1.2,2.05,3.4 --recipe light --output fight-combo.mp4
python scripts/framecraft.py apply   --input fight.mp4 --cues cues.json --output fight-all.mp4
python scripts/framecraft.py apply   --input fight.mp4 --at 3.40 --style still --frames 2 --image my-impact.png --output fight-art.mp4
python scripts/framecraft.py safety  --input fight-all.mp4
python scripts/framecraft.py preview --input fight.mp4 --at 3.40 --folder preview_frames   # 导出前、中、后三张截图
```

- `--at`：接触发生的秒数，从 0 开始；多个用逗号分隔。
- `--focus x,y`：推近的焦点，0–1 比例（0,0 左上角，1,1 右下角），对准接触点。
- `--style`：兼容 1.x 的单一效果（white / dark / invert / ink / punch / still），配 `--frames`。
- `--fps`：指定输出恒定帧率（如 24、30000/1001）。
- `--allow-intense`：明确需要时才用，允许每秒超过 3 次闪烁类效果。
- `--no-scan`：跳过输出后的闪烁扫描（长视频想省时间时）。

## 三、配方

| 配方 | 组成 | 适合 |
|---|---|---|
| `cinema` | 克制明暗脉冲 1 帧＋小幅震动 140 ms | 写实片 L1 |
| `light` | 明暗脉冲 1 帧＋轻震 120 ms | 普通攻防 L2 |
| `heavy` | 顿帧 80 ms＋明暗冲击 1 帧＋衰减震动 220 ms＋推近 1.06 | 转折一击 L3 |
| `manga` | 墨色硬对比 2 帧＋震动＋小推近 | 漫画打击 L3 |
| `anime` | 顿帧 60 ms＋负片 1 帧＋推近 1.08＋震动 | 动画重击 L4 |
| `energy` | RGB 色散 200 ms＋半强度白闪 1 帧＋推近 | 能量对轰 L4 |
| `blackout` | 先顿帧让观众看清命中，再黑 2 帧 | 暗帧顿挫 |
| `crit` | 顿帧 140 ms＋白闪＋墨色 2 帧＋推近 1.10＋强震 | 终结技 L5，一场一次 |

时长用毫秒定义，按视频帧率换算成最接近的整帧，不同帧率下观感接近（会有几毫秒的取整误差）。

## 四、击点表（多击点、自定义图层）

```json
{
  "cues": [
    {"at": 1.20, "recipe": "light"},
    {"at": 3.40, "recipe": "heavy", "focus": [0.58, 0.42]},
    {"at": 6.30, "layers": [
      {"type": "hitstop", "ms": 70},
      {"type": "rgbsplit", "ms": 160, "shift": 0.005},
      {"type": "flash", "frames": 1, "color": "#FFC21A", "strength": 0.5},
      {"type": "shake", "ms": 200, "amp": 0.007}
    ]}
  ]
}
```

图层类型与参数：

| type | 作用 | 参数 |
|---|---|---|
| `hitstop` | 把接触帧定格，替换其后几帧（总时长不变，音画不错位） | `ms` 或 `frames` |
| `flash` | 全画面闪色 | `color`（white/black/red/yellow/orange/cyan/blue/magenta 或 #RRGGBB）、`strength` 0.05–1 |
| `invert` | 负片 | `frames` |
| `ink` | 去色硬对比 | `contrast` 1.2–4 |
| `punch` | 亮度对比脉冲 | `contrast` 1–2.5、`brightness` -0.3–0.4 |
| `rgbsplit` | 红蓝通道错开 | `shift`（占画宽比例，0.001–0.05） |
| `shake` | 衰减震屏 | `amp`（占画宽比例，0.001–0.05）、`direction`（both／h 横震／v 竖震） |
| `zoom` | 冲击推近后回弹 | `zoom` 1.005–1.6、`focus` [x,y] |
| `still` | 用你的冲击图整幅替换几帧 | `image` 路径 |

通用参数：`ms` 或 `frames`（持续），`offset_frames`（相对接触帧延后几帧，或 `"after_hold"` 表示顿帧结束后开始）。图层的叠加顺序固定：先顿帧，再色调类效果，最后镜头运动。

## 五、安全与边界

- **不覆盖**：输出路径已存在、等于输入、是链接时一律拒绝；渲染到临时文件，检查时长和音轨后才发布。
- **闪烁预算**：计划中任意 1 秒内闪烁类效果（闪色、负片、墨色、插图）超过 3 次会被拦下；强度低于 0.25 的柔闪和 `punch` 明暗脉冲不计入。Python 里直接调用旧版 `apply()` 时不做渲染后扫描。渲染后自动做全画面亮度近似扫描，结果写在输出 JSON 的 `safety_scan` 里。扫描不计算面积和红闪，正式播出前用专业工具复检。
- **顿帧的代价**：定格替换了后面几帧的内容，动作会在定格结束后"跳"一下，这正是顿帧的观感；需要完全不跳，就在生成阶段做慢动作。
- **转码**：输出为 H.264 + AAC 的 MP4。额外音轨、字幕、HDR 元数据不保证保留，专业母版走剪辑软件。
- **帧率**：先换算为恒定帧率再按帧号处理（帧号 = round(秒数 × fps)）。可变帧率、起始时间戳异常的素材，输出后务必复看。
- **插图**：`still` 会等比放大并裁切填满画面，插图最好事先做成同样的长宽比。
- **候选击点**：`detect` 找的是画面突变，可能是命中、闪光，也可能是剪辑点，必须用 `sheet` 复查。

## 六、运行测试

```bash
python -m unittest discover -s tests -v
```
