---
name: suno-music-prompts
description: "Suno AI v5.5 音乐提示词专家（2026-03-27 规范对齐）。覆盖 Voices 个人声模型、Custom Models 自定义模型、My Taste 偏好学习、颗粒化参数（BPM / Key / Instrumentation / Weirdness / Style Influence / Section Steering）、Stems 分轨与 MIDI 导出。内嵌专业音乐知识图谱（246 条曲风 × 19 大类、24 种语言、80 个人声标签、799 条乐器×技法 × 17 个家族、20 种曲式结构），覆盖流行、摇滚、电子、嘻哈、爵士、古典、民谣、金属、国风、拉丁、世界音乐、中国传统乐器等全品类。当用户提及「Suno提示词、Suno v5.5、Suno风格标签、AI音乐生成、Suno prompt、音乐风格标签、写一首歌、AI作曲、Suno创作、生成音乐、AI编曲、Voices 声音模型、Custom Models、Stems 分轨、Section Steering」时触发。"
---

# Suno AI 音乐提示词专家 v5.5

基于专业音乐知识图谱，为 Suno AI v5.5（2026-03-27 发布）生成精准、高质量的音乐提示词。

---

## 📚 完整音乐知识图谱（参考索引）

本技能内嵌完整版音乐知识图谱（由 Moke 提供的 `音乐知识图谱.xlsx` 导出）。当 SKILL.md 主文档的精简库不够用、或需要更冷门/更细分的标签时，**按需读取下列参考文档**：

| 参考文件 | 内容 | 何时读取 |
|---------|------|---------|
| `references/genre-library-full.md` | **246 条曲风** × 19 大类 × 带定义 | 需要冷门曲风 / 融合风格 / 精确风味锚定时 |
| `references/vocals-library-full.md` | **80 个人声标签** × 4 大类（性别/人声类型/音色/唱法） | 需要精细人声控制，超出主文档 ~19 个音色词范围时 |
| `references/instruments-library-full.md` | **799 条乐器×技法** × 17 个家族（含中国传统乐器、民族乐器、技法细分如 Legato/Staccato/Tremolo 等） | 需要指定演奏技法、冷门民族乐器、复杂配器时 |
| `references/language-structure-tags.md` | **24 种语言** + **20 种曲式结构**（含定义） | 需要多语言 / 精确段落控制时 |
| `references/music-knowledge-graph.json` | 结构化 JSON 原始数据 | 脚本处理 / 批量筛选 / 自动组装 prompt 时 |
| `references/music-knowledge-graph.xlsx` | 原始 Excel 文件 | 人工审阅 / 更新维护 |

**使用原则**：SKILL.md 主文档覆盖 80% 高频场景，**先用主文档**；当用户提出更精细/冷门的需求时，再按需读取对应参考文件。**不要把所有参考文件一次性灌入上下文**。

---

## v5.5 版本核心升级（必须知晓）

> Suno v5.5 的关键转向：**从"纯文本提示词"升级为"文本 + 结构化参数 + 个人化"三轨控制**。写提示词的策略要跟着变。

### A. 三大个性化功能（Pro / Premier 限定）

| 功能 | 说明 | 对提示词工程的影响 |
|------|------|----------------------|
| **Voices（声音）** | 录制/上传 30s–4min 个人人声（含实时验证读句防盗用），训练出专属人声模型 | 使用 Voices 时 Style 标签中 **不要再写 `Female Vocals / Male Vocals`**，会和 Voice 模型打架；保留音色形容词（如 `Warm`, `Breathy`）即可 |
| **Custom Models（自定义模型）** | 上传 ≥6 首原创曲训练风格微调模型 | 触发自定义模型后 Style 标签**改走"补充风格"策略**，不要堆主风格，只写差异化修饰词（tempo/instrument/mood）|
| **My Taste（我的品味）** | 自动记录用户偏好并应用到后续生成 | 与"Style Influence"协作；熟用户的常用风格可**省略**，让系统自动套用 |

### B. 颗粒化创作控制（所有用户可用）

v5.5 允许在生成**前**显式设定以下参数，不再只靠文本：

| 控制项 | 填写方式 | 建议 |
|--------|---------|------|
| **Tempo（速度）** | 直接填 BPM 数值（40–200） | **优先用数值，不要只写 "Slow / Fast"** —— v5.5 对 BPM 数字识别非常准 |
| **Key Signature（调性）** | 填 `C Major` / `A Minor` / `F# Minor` 等 | 阴暗=小调，明亮=大调；武侠/悲情 → `D Minor` / `A Minor` |
| **Instrumentation（配器）** | 主奏乐器列表（独立于 Style 字段）| 关键乐器放这里，Style 字段留给风格描述 |
| **Section Steering（段落控制）** | 开关，开启后 `[Verse]` `[Chorus]` 等标记有强控制力 | 长结构（>3 段）或段落情绪跳变大 → **必开** |
| **Weirdness（怪异度）** | 0–100 滑杆 | 主流 20–35 / 实验 50–70 / 极端 80+ |
| **Style Influence（风格强度）** | 0–100 滑杆 | 一般 70–85 / 强风格锁定 90–95 |
| **Audio Influence（音频强度）** | 0–100 滑杆，配合 Voices / 参考音频 | 70–85 为日常，90 以上会过拟合 |

### C. 工程级导出

- **Stems Export（分轨导出）**：鼓 / Bass / 人声 / 乐器分轨 WAV，可带入 DAW 精修
- **MIDI Export**：旋律/和声/鼓点 MIDI 导出，可手动编辑
- **Mix Layers**：v5.5 显著改善乐器分离度，堆叠 6+ 乐器也不会糊

### D. 模型层面升级
- 人声真实度（呼吸、气息、换气口）提升
- 混音层次（Low / Mid / High 分离度）提升
- 过渡段平滑度（Bridge → Chorus）提升
- **对英文标签的识别仍然 > 中文**，Style 字段继续用英文

---

## 核心能力

1. **Style of Music 标签生成** — 从 257 种曲风中精准匹配，组装 Suno 可识别的风格标签
2. **歌词结构标记** — 使用 Suno 标准结构标记 `[Verse]` `[Chorus]` `[Bridge]` 等
3. **人声与音色描述** — 精确指定演唱性别、音色特征、唱法技巧（或配合 Voices 个人声模型）
4. **乐器编配建议** — 从 11 大类 60+ 乐器中推荐配器方案，分离填入 Style 字段 / Instrumentation 字段
5. **多语言支持** — 覆盖 24 种语言/方言的音乐创作
6. **v5.5 参数建议** — 为每个方案给出推荐的 BPM / Key / Weirdness / Style Influence / Section Steering 设置

---

## 使用流程

### Step 1: 收集创作意图

向用户确认以下要素（缺失项主动推荐）：

| 要素 | 说明 | 示例 | v5.5 填入位置 |
|------|------|------|---------------|
| **主题/故事** | 歌曲讲什么 | 夏日海边的初恋回忆 | Lyrics |
| **情绪/氛围** | 整体情感基调 | 甜蜜、怀旧、微苦 | Style |
| **曲风** | 一级+二级风格 | City Pop / Dream Pop | Style |
| **语言** | 演唱语种 | Chinese / English | Style + Lyrics |
| **人声** | 性别+音色 | Female, Warm, Gentle | Style（或使用 Voices 模型）|
| **速度** | **BPM 数值**（优先）| 92 BPM | **Tempo 字段**（非 Style）|
| **调性** | Major/Minor | A Minor | **Key 字段**（非 Style）|
| **主奏乐器** | 关键乐器 | Piano, Strings | **Instrumentation 字段**（或 Style）|
| **时长** | 目标长度 | 3 分钟 | 结构长度 |
| **参考** | 类似的歌/艺人 | 类似山下达郎的感觉 | Style 中的时代/地域词 |
| **Weirdness** | 怪异度偏好 | 主流 30 / 实验 60 | v5.5 滑杆 |
| **Style Influence** | 风格锁定强度 | 80 | v5.5 滑杆 |

### Step 2: 组装 Style of Music 标签

**核心公式：**
```
[主曲风], [子曲风/融合风格], [情绪词], [人声描述], [关键乐器], [速度/节奏], [氛围修饰]
```

**Suno Style 标签规则：**
- 使用 **英文** 标签（Suno 对英文标签识别最佳）
- 标签间用 **逗号** 分隔
- 控制在 **120字符以内**（Suno 有长度限制）
- 最重要的风格放在 **最前面**
- 可叠加 2-3 个风格实现融合效果
- 避免矛盾标签（如 Aggressive + Soothing）

**示例：**
```
City Pop, Dream Pop, Female Vocals, Warm, Nostalgic, Synth, Electric Guitar, Groovy, 80s Japanese
```

### Step 3: 编写歌词 + 结构标记

使用 Suno 支持的标准结构标记：

```
[Intro]          — 前奏（器乐）
[Verse]          — 主歌
[Pre-Chorus]     — 连副段（过渡）
[Chorus]         — 副歌（高潮）
[Post-Chorus]    — 副歌后段
[Bridge]         — 过渡段/桥段
[Interlude]      — 间奏（器乐）
[Outro]          — 尾奏
[Hook]           — 记忆点
[Break]          — 衔接段/能量下降
[Build]          — 渐进段
[Drop]           — 高潮（电子乐）
[Solo]           — 即兴演奏段
[Instrumental]   — 纯器乐段
[Ad lib]         — 即兴人声
```

**结构标记进阶用法：**
```
[Verse 1]        — 第一段主歌
[Verse 2]        — 第二段主歌
[Chorus x2]      — 副歌重复两次
[Soft Verse]     — 柔和的主歌
[Energetic Chorus] — 充满能量的副歌
[Whispered Verse] — 轻声主歌
[Spoken Word]    — 念白
[Rap Verse]      — 说唱段
[Fade Out]       — 渐出
```

### Step 4: 输出完整提示词（v5.5 格式）

**v5.5 标准交付格式**（所有字段分开，不要全塞进 Style）：

```
📎 Style of Music:
City Pop, Dream Pop, Warm, Nostalgic, Silky Vocals, 80s Japanese

📎 Instrumentation:
Synth, Electric Guitar, Bass Guitar, Electric Piano, Drums

📎 Tempo: 92 BPM
📎 Key: A Major
📎 Weirdness: 30
📎 Style Influence: 85
📎 Audio Influence: 70 （使用 Voices 时）
📎 Section Steering: ON

📎 Title:
海风的记忆

📎 Lyrics:
[Intro]
[Verse 1]
夕阳染红了整片海岸线
你的笑容像是夏天的明信片
...

[Pre-Chorus]
时间在指缝间悄悄溜走
...

[Chorus]
海风轻轻吹过你的发梢
带走了那年夏天的烦恼
...

[Interlude]

[Verse 2]
...

[Bridge]
...

[Chorus]
...

[Outro]
```

**v5.5 写作要点**：
- **BPM 用数字**，不要只写 "Slow / Mid-Tempo"
- **调性显式写出**（Major/Minor），情绪才准
- **Style 字段只放风格词**，乐器挪到 Instrumentation
- **Section Steering 段落情绪差异大时必开**
- **使用 Voices 模型** → Style 中删除 `Female/Male Vocals`，保留音色形容词

---

## 曲风知识库（Genre Library）

### 一、流行 Pop

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Chinese Ballad Pop | 国语抒情 | `Chinese Ballad Pop, Emotional, Melodic` | 中慢速，旋律性极强，哀婉动听 |
| Chinese Pop | 国语流行 | `Chinese Pop, Mandarin, Modern` | 普通话演绎的主流流行乐 |
| Modern Pop Ballad | 现代抒情 | `Pop Ballad, Emotional, Storytelling` | 中慢速，爱情/友情/成长主题 |
| K-Pop | 韩国流行 | `K-Pop, Energetic, Dance` | 融合嘻哈/R&B/电子/舞曲 |
| J-Pop | 日本流行 | `J-Pop, Japanese, Upbeat` | 西化制作+日式旋律美学 |
| Indian Pop | 印度流行 | `Indian Pop, Bollywood` | 与宝莱坞紧密关联 |
| Teen Pop | 青少年流行 | `Teen Pop, Catchy, Dance` | Auto-tune, 舞蹈编排, 青春主题 |
| Indie Pop | 独立流行 | `Indie Pop, Melodic, Lo-Fi` | 旋律优美, 地下音乐柔和一面 |
| Dream Pop | 梦幻流行 | `Dream Pop, Ethereal, Reverb, Dreamy` | 飘渺氛围, 层叠音效, 回音人声 |
| City Pop | 都市流行 | `City Pop, Groovy, Funky, 80s Japanese` | Smooth Jazz+AOR, 80年代日本 |
| Synth Pop | 合成器流行 | `Synth Pop, Synthesizer, Retro` | 电子合成器点缀, 流行旋律 |
| Dance Pop | 流行舞曲 | `Dance Pop, Upbeat, Danceable, Rhythmic` | 律动感强, 节奏鲜明 |
| Electropop | 电音流行 | `Electropop, Electronic, Dark Pop` | 低频合成器, 温润/扭曲/暗沉 |
| Chamber Pop | 室内流行 | `Chamber Pop, Orchestral, Elegant` | 弦乐管乐, 巴洛克典雅感 |
| Celtic Pop | 凯尔特流行 | `Celtic Pop, Irish, Folk Pop` | 风笛/竖琴, 爱尔兰风味 |
| Deep Dance Pop | 深流行舞曲 | `Deep Dance Pop, Soulful, Groovy` | 融入Soul/Jazz, 深邃感 |
| Acapella | 无伴奏合唱 | `Acapella, Vocal Only, Harmonies` | 纯人声, 无器乐伴奏 |

### 二、乡村 Country

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Country Pop | 乡村流行 | `Country Pop, Upbeat, Guitar` | 乡村+流行融合, 轻快活力 |
| Bluegrass | 蓝草 | `Bluegrass, Acoustic, Banjo, Fiddle` | 原声乐器, 轮流主导旋律 |
| Country Rock | 乡村摇滚 | `Country Rock, Southern Rock, Guitar` | 乡村+摇滚融合 |
| Country Folk | 乡村民谣 | `Country Folk, Acoustic, Heartfelt` | 乡村+民谣融合 |
| Yodeling | 约德尔 | `Yodeling, Country, Alpine` | 约德尔唱法 |
| Early Country | 早期乡村 | `Early Country, Vintage, Lo-Fi` | 1920-1960传统乡村 |

### 三、民谣 Folk

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Chinese Folk | 国语民谣 | `Chinese Folk, Acoustic Guitar, Gentle` | 吉他/钢琴, 简单旋律, 生活/爱情 |
| Folk Pop | 民谣流行 | `Folk Pop, Acoustic, Melodic, Warm` | 温和优雅, 偏向流行 |
| Indie Folk | 独立民谣 | `Indie Folk, Acoustic, Intimate, Warm` | 独立摇滚+传统民谣结合 |
| Contemporary Folk | 当代民谣 | `Contemporary Folk, Singer-Songwriter` | 传统根源+流行/摇滚制作 |
| Irish Folk | 爱尔兰民谣 | `Irish Folk, Celtic, Fiddle, Tin Whistle` | 风笛/竖琴, 宁静致远 |
| Celtic Folk | 凯尔特民谣 | `Celtic Folk, Harp, Bagpipe, Ancient` | 凯尔特乐器, 早期民谣 |
| Traditional Folk | 传统民谣 | `Traditional Folk, World Music, Acoustic` | 世界音乐/根源音乐 |
| English Folk | 英国民谣 | `English Folk, Medieval, Storytelling` | 叙事性, 中世纪晚期传统 |
| French Folk | 法国民谣 | `French Folk, Accordion, Romantic` | 风笛/双簧管, 吉普赛元素 |
| Korean Folk | 韩国民谣 | `Korean Folk, Traditional, Emotional` | 清唱, 情感/社会批判 |
| Japanese Folk | 日本民谣 | `Japanese Folk, Shamisen, Serene` | 三味线/尺八, 抒情叙事 |
| African Folk | 非洲民谣 | `African Folk, Rhythmic, Community` | 即兴节奏, 独唱+合唱 |
| Arabic Folk | 阿拉伯民谣 | `Arabic Folk, Oud, Middle Eastern` | 木卡姆旋律, 乌德琴/手鼓 |

### 四、电子 Electronic

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| EDM | 电子舞曲 | `EDM, Electronic, Dance, High Energy` | 派对/舞厅背景音乐总称 |
| House | 浩室 | `House, Four on the Floor, Groovy` | 四拍底鼓, 律动为主 |
| Tropical House | 热带浩室 | `Tropical House, Summer, Chill, Upbeat` | 热带风情, 轻快明亮 |
| Deep House | 深邃浩室 | `Deep House, Smooth, Atmospheric` | 低沉旋律, 氛围感 |
| Future Bass | 未来贝斯 | `Future Bass, Synth, Emotional, Bright` | 合成器和弦, 明亮情感 |
| Dubstep | 回响贝斯 | `Dubstep, Heavy Bass, Wobble` | 重低音, 摇摆贝斯 |
| Trance | 出神舞曲 | `Trance, Euphoric, Build, Atmospheric` | 层层递进, 迷幻出神 |
| Techno | 科技舞曲 | `Techno, Minimal, Industrial, Dark` | 机械节拍, 简约暗沉 |
| Drum & Bass | 鼓贝斯 | `Drum and Bass, Fast, Breakbeat` | 快节奏碎拍, 重贝斯线 |
| Ambient | 氛围电子 | `Ambient, Atmospheric, Ethereal, Calm` | 无节拍, 环境音景 |
| Dark Ambient | 黑暗氛围 | `Dark Ambient, Ominous, Cinematic` | 阴暗, 恐怖, 电影感 |
| Downtempo | 缓拍 | `Downtempo, Chill, Relaxed, Groovy` | 慢节拍, 放松 |
| Trip Hop | 神游舞曲 | `Trip Hop, Dark, Atmospheric, Beats` | 暗色调, 氛围节拍 |
| Synthwave | 合成器潮 | `Synthwave, Retro, 80s, Neon` | 80年代复古, 霓虹美学 |
| Vaporwave | 蒸汽波 | `Vaporwave, Lo-Fi, Retro, Slowed` | 放慢采样, 复古拼贴 |
| Chillwave | 寒潮 | `Chillwave, Dreamy, Lo-Fi, Nostalgic` | 梦幻低保真, 怀旧 |
| Breakbeat | 碎拍 | `Breakbeat, Funky, Rhythmic` | 不规则鼓组节奏 |
| 8-Bit | 8比特 | `8-Bit, Chiptune, Retro Game` | 游戏机音色, 像素风 |
| Phonk | 冯克 | `Phonk, Memphis, Dark, Bass` | 孟菲斯采样+暗黑美学 |
| Hardstyle | 硬派舞曲 | `Hardstyle, Hard Kick, Euphoric` | 硬核底鼓, 高能量 |
| Disco | 迪斯科 | `Disco, Funky, Groovy, 70s` | 放克节奏, 70年代 |
| EDM Trap | 陷阱舞曲 | `EDM Trap, Heavy, Bass, 808` | TR-808鼓机, 重低音 |
| Folktronica | 电子民谣 | `Folktronica, Organic Electronic, Folk` | 民谣+电子融合 |
| Sci-Fi | 科幻音乐 | `Sci-Fi, Futuristic, Space, Electronic` | 太空/未来感电子 |

### 五、国风 Chinese Style

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| China-Wave | 中国风流行 | `Chinese Style Pop, Guzheng, Erhu` | 中国风+流行融合 |
| GuFeng Music | 古风音乐 | `Ancient Chinese, Traditional, Guzheng` | 古典诗词意境 |
| Chinoiserie Rap | 国风嘻哈 | `Chinese Hip Hop, Traditional Fusion` | 国风+嘻哈 |
| Chinoiserie Electronic | 国风电子 | `Chinese Electronic, Fusion, Modern` | 国风+电子 |
| Chinoiserie Rock | 国风摇滚 | `Chinese Rock, Traditional Fusion, Bold` | 国风+摇滚 |

### 六、摇滚 Rock

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Pop Rock | 流行摇滚 | `Pop Rock, Catchy, Guitar Driven` | 流行旋律+摇滚能量 |
| Indie Rock | 独立摇滚 | `Indie Rock, Alternative, Raw` | 独立厂牌, 原始质感 |
| Alternative Rock | 另类摇滚 | `Alternative Rock, 90s, Grunge-Adjacent` | 非主流摇滚 |
| Hard Rock | 硬摇滚 | `Hard Rock, Powerful, Distortion Guitar` | 失真吉他, 强力 |
| Psychedelic Rock | 迷幻摇滚 | `Psychedelic Rock, Trippy, Reverb` | 迷幻效果, 混响 |
| Post-Rock | 后摇 | `Post-Rock, Atmospheric, Crescendo` | 渐进高潮, 氛围叙事 |
| Brit Pop | 英伦流行 | `Britpop, British, Melodic Rock` | 英伦旋律, 吉他为主 |
| Shoegaze | 自赏 | `Shoegaze, Noise, Dreamy, Wall of Sound` | 噪音墙, 梦幻 |
| Math Rock | 数学摇滚 | `Math Rock, Complex Rhythm, Technical` | 复杂变拍, 技术性 |
| Surf Rock | 冲浪摇滚 | `Surf Rock, Reverb Guitar, Summer` | 混响吉他, 夏日感 |
| Progressive Rock | 前卫摇滚 | `Progressive Rock, Epic, Complex` | 复杂编曲, 史诗 |
| Soft Rock | 轻摇滚 | `Soft Rock, Gentle, Melodic` | 柔和, 旋律优先 |
| Grunge | 油渍摇滚 | `Grunge, 90s, Raw, Distortion` | 90年代, 粗糙失真 |
| J-Rock | 日本摇滚 | `J-Rock, Japanese, Energetic` | 日本摇滚, 热血 |
| Lo-Fi Rock | 低保真摇滚 | `Lo-Fi Rock, Raw, Garage` | 粗糙录音, 车库感 |
| Glam Rock | 华丽摇滚 | `Glam Rock, Flamboyant, 70s` | 华丽造型, 70年代 |

### 七、朋克 Punk

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Pop Punk | 流行朋克 | `Pop Punk, Fast, Catchy, Youthful` | 快节奏, 上口旋律 |
| Post-Punk | 后朋克 | `Post-Punk, Dark, Atmospheric, Bass` | 暗色调, 贝斯驱动 |
| New Wave | 新浪潮 | `New Wave, 80s, Synth, Quirky` | 80年代合成器, 怪趣 |
| Emo Punk | 情绪朋克 | `Emo, Emotional, Raw, Confessional` | 情绪宣泄, 告白式 |
| Hardcore Punk | 硬核朋克 | `Hardcore Punk, Aggressive, Fast, Loud` | 激烈, 快速, 大音量 |
| Ska Punk | 斯卡朋克 | `Ska Punk, Upbeat, Brass, Offbeat` | 铜管乐, 弱拍强调 |
| Dance Punk | 舞曲朋克 | `Dance Punk, Groovy, Punk, Electronic` | 朋克+舞曲融合 |

### 八、爵士 Jazz

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Jazz Pop | 流行爵士 | `Jazz Pop, Smooth, Sophisticated` | 流行+爵士融合, 精致 |
| Bossa Nova | 巴萨诺瓦 | `Bossa Nova, Brazilian, Gentle, Guitar` | 巴西风情, 柔和吉他 |
| Smooth Jazz | 柔顺爵士 | `Smooth Jazz, Saxophone, Relaxed` | 萨克斯, 放松 |
| Swing | 摇摆乐 | `Swing, Big Band, Vintage, Upbeat` | 大乐队, 复古摇摆 |
| Vocal Jazz | 人声爵士 | `Vocal Jazz, Scatting, Intimate` | 人声为主, 拟声吟唱 |
| Cool Jazz | 冷爵士 | `Cool Jazz, Mellow, Understated` | 低调柔和 |
| Bebop | 波普 | `Bebop, Fast, Improvisation, Complex` | 快速即兴, 复杂和声 |
| Jazz Fusion | 爵士融合 | `Jazz Fusion, Funky, Electric, Complex` | 融合放克/摇滚 |
| Nu Jazz | 新爵士 | `Nu Jazz, Electronic, Modern Jazz` | 爵士+电子融合 |
| Acid Jazz | 酸性爵士 | `Acid Jazz, Funky, Groovy, Soulful` | 放克/灵魂乐融合 |
| Gypsy Jazz | 吉普赛爵士 | `Gypsy Jazz, Acoustic Guitar, Fast` | 吉普赛吉他, 快速 |
| Free Jazz | 自由爵士 | `Free Jazz, Avant-Garde, Experimental` | 实验性, 自由即兴 |
| Big Band | 大乐队 | `Big Band, Brass, Swing, Orchestra` | 铜管+大编制 |
| Japanese Jazz Fusion | 日本爵士融合 | `Japanese Jazz Fusion, City Pop, Funky` | 日本爵士融合, City Pop关联 |

### 九、嘻哈 Hip Hop / Rap

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Trap | 陷阱说唱 | `Trap, 808, Hi-Hat, Dark` | 808鼓机, 密集踩镲 |
| Boombap | 蹦啪 | `Boom Bap, Old School, Sampled` | 采样+鼓组, 经典质感 |
| Pop Rap | 流行说唱 | `Pop Rap, Catchy, Melodic, Mainstream` | 流行旋律+说唱 |
| R&B Rap | 旋律说唱 | `Melodic Rap, R&B, Smooth, Singing` | R&B融合, 旋律性 |
| Old School | 老派说唱 | `Old School Hip Hop, Classic, Funky` | 经典放克采样 |
| Jazz Hip Hop | 爵士嘻哈 | `Jazz Rap, Lo-Fi, Sophisticated` | 爵士采样, Lo-Fi |
| Alternative Hip Hop | 另类嘻哈 | `Alternative Hip Hop, Experimental` | 实验性嘻哈 |
| Drill | 钻头说唱 | `Drill, Dark, Aggressive, Sliding 808` | 滑音808, 暗黑攻击性 |
| Emo Rap | 情绪说唱 | `Emo Rap, Sad, Guitar, Lo-Fi` | 悲伤, 吉他, 情绪化 |
| Gangsta Rap | 匪帮说唱 | `Gangsta Rap, West Coast, G-Funk` | 西海岸, G-Funk |
| Chill Beats | 弛放节拍 | `Chill Beats, Lo-Fi Hip Hop, Relaxed` | 放松的Lo-Fi节拍 |
| Afrobeats | 非洲节奏 | `Afrobeats, Dancehall, Rhythmic` | 非洲节奏+舞场 |
| Comedy Hip Hop | 喜剧说唱 | `Comedy Rap, Funny, Playful` | 搞笑, 幽默 |

### 十、古典 Classical

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Baroque | 巴洛克 | `Baroque, Harpsichord, Ornamental` | 羽管键琴, 装饰性 |
| Classical Period | 古典主义 | `Classical, Mozart, Elegant, Balanced` | 平衡, 优雅, 对称 |
| Romantic | 浪漫主义 | `Romantic, Orchestral, Emotional, Grand` | 大编制管弦, 情感丰富 |
| Impressionism | 印象主义 | `Impressionist, Dreamy, Debussy, Fluid` | 梦幻, 流动色彩 |
| Contemporary Classical | 现代古典 | `Contemporary Classical, Experimental` | 当代实验古典 |
| Renaissance | 文艺复兴 | `Renaissance, Choral, Ancient, Sacred` | 合唱, 神圣 |
| Medieval | 中世纪 | `Medieval, Ancient, Lute, Chant` | 鲁特琴, 吟唱 |

### 十一、R&B / 灵魂乐

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Contemporary R&B | 当代R&B | `R&B, Smooth, Groovy, Soulful` | 当代节奏布鲁斯 |
| Neo Soul | 新灵魂乐 | `Neo Soul, Warm, Organic, Jazz-Influenced` | 爵士影响, 有机质感 |
| Funk | 放克 | `Funk, Groovy, Bass, Slap, Rhythmic` | 贝斯律动, 切分节奏 |
| Soul | 灵魂乐 | `Soul, Emotional, Gospel-Influenced, Warm` | 福音影响, 温暖情感 |
| Pop Soul | 流行灵魂 | `Pop Soul, Catchy, Soulful, Smooth` | 灵魂+流行融合 |
| Gospel | 福音 | `Gospel, Choir, Uplifting, Spiritual` | 合唱, 灵性 |
| Progressive R&B | 前卫R&B | `Progressive R&B, Experimental, Dark R&B` | 实验性, 暗色调 |
| Neo Funk | 新放克 | `Neo Funk, Modern Funk, Groovy, Synth` | 现代放克, 合成器 |

### 十二、布鲁斯 Blues

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Country Blues | 乡村布鲁斯 | `Country Blues, Acoustic, Delta` | 原声吉他, 三角洲 |
| Jazz Blues | 爵士布鲁斯 | `Jazz Blues, Sophisticated, Smooth` | 爵士和声 |
| Rock Blues | 摇滚布鲁斯 | `Blues Rock, Electric Guitar, Gritty` | 电吉他, 粗犷 |
| Contemporary Blues | 当代布鲁斯 | `Modern Blues, Soulful, Electric` | 当代电声布鲁斯 |
| Boogie Woogie | 布基乌基 | `Boogie Woogie, Piano, Upbeat, Swing` | 钢琴律动, 摇摆 |

### 十三、金属 Metal

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Heavy Metal | 重金属 | `Heavy Metal, Powerful, Guitar Riff` | 力量感, 吉他Riff |
| Death Metal | 死亡金属 | `Death Metal, Growling, Blast Beat` | 嘶吼, 爆破鼓点 |
| Black Metal | 黑金属 | `Black Metal, Dark, Tremolo, Shriek` | 黑暗, 颤音拾取 |
| Power Metal | 力量金属 | `Power Metal, Epic, Fast, Soaring Vocals` | 史诗, 高亢人声 |
| Progressive Metal | 前卫金属 | `Progressive Metal, Complex, Technical` | 复杂技术编曲 |
| Metalcore | 金属核 | `Metalcore, Breakdown, Screaming, Melodic` | 崩塌段, 嘶吼+旋律 |
| Nu Metal | 新金属 | `Nu Metal, Rap Metal, Heavy, 2000s` | 说唱+金属融合 |
| Gothic Metal | 哥特金属 | `Gothic Metal, Dark, Symphonic, Dramatic` | 暗黑, 交响, 戏剧性 |
| Folk Metal | 民谣金属 | `Folk Metal, Epic, Medieval, Bagpipe` | 中世纪民谣+金属 |
| Industrial Metal | 工业金属 | `Industrial Metal, Mechanical, Electronic` | 机械+电子质感 |
| Doom Metal | 厄运金属 | `Doom Metal, Slow, Heavy, Dark` | 极慢, 极重, 极暗 |
| Thrash Metal | 激流金属 | `Thrash Metal, Fast, Aggressive, Riff` | 快速攻击性Riff |
| Kawaii Metal | 可爱金属 | `Kawaii Metal, J-Pop, Cute, Heavy` | 可爱J-Pop+金属 |

### 十四、雷鬼 Reggae

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Dancehall | 舞场雷鬼 | `Dancehall, Jamaican, Riddim, Bouncy` | 牙买加节奏, 弹性 |
| Dub | 回响 | `Dub, Reverb, Echo, Bass Heavy` | 重混响/回声, 重贝斯 |

### 十五、拉丁 Latin

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Latin Pop | 拉丁流行 | `Latin Pop, Spanish, Romantic` | 西语, 浪漫 |
| Reggaeton | 雷击顿 | `Reggaeton, Dembow, Latin, Dance` | Dembow节奏, 拉丁舞曲 |
| Tango | 探戈 | `Tango, Dramatic, Accordion, Passionate` | 手风琴, 热情戏剧 |
| Samba | 桑巴 | `Samba, Brazilian, Percussion, Festive` | 巴西打击乐, 节庆 |
| Bossa Nova | 巴萨诺瓦 | `Bossa Nova, Brazilian, Gentle, Guitar` | 巴西柔和吉他 |
| Cha-Cha-Cha | 恰恰 | `Cha Cha Cha, Latin Dance, Playful` | 拉丁舞曲, 俏皮 |
| Rumba | 伦巴 | `Rumba, Latin, Passionate, Dance` | 浪漫拉丁舞 |

### 十六、中国传统 Chinese Tradition

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Chinese Opera | 中国戏曲 | `Chinese Opera, Traditional, Dramatic` | 传统戏曲唱腔 |
| Traditional Chinese Folk | 传统民歌 | `Chinese Folk Song, Traditional, Ethnic` | 各地方民歌 |
| Chinese Traditional Instrumental | 中国器乐 | `Chinese Instrumental, Guzheng, Erhu, Pipa` | 古筝/二胡/琵琶等 |
| Red Song | 红歌 | `Red Song, March, Patriotic, Choir` | 军旅/爱国歌曲 |
| New Chinese Folk | 新民歌 | `New Chinese Folk, Modern, Traditional Vocal` | 现代新民歌 |
| Prairie Style | 草原风情 | `Prairie, Mongolian, Matouqin, Vast` | 草原/蒙古风, 马头琴 |

### 十七、世界音乐 World Music

| 风格标签 | 中文 | Suno推荐标签 | 核心特征 |
|----------|------|-------------|---------|
| Flamenco | 弗拉明戈 | `Flamenco, Spanish Guitar, Passionate` | 西班牙吉他, 热情 |
| Chanson | 香颂 | `Chanson, French, Romantic, Cabaret` | 法国浪漫小曲 |
| Fado | 法朵 | `Fado, Portuguese, Melancholy, Guitar` | 葡萄牙忧郁 |
| Enka | 演歌 | `Enka, Japanese, Traditional, Melancholy` | 日本演歌, 哀愁 |
| Bhangra | 印度舞曲 | `Bhangra, Indian, Energetic, Dhol` | 印度鼓乐, 活力 |
| Worldbeat | 世界打击乐 | `Worldbeat, Percussion, Global, Tribal` | 全球打击乐融合 |

---

## 人声标签库（Vocal Tags）

### 性别/编制

| 标签 | Suno标签 | 说明 |
|------|---------|------|
| Female | `Female Vocals` | 女性主唱 |
| Male | `Male Vocals` | 男性主唱 |
| Neutral | `Androgynous Vocals` | 中性声线 |
| Child | `Child Vocals` | 童声 |
| Choir | `Choir, Choral` | 合唱团 |
| Multiple | `Group Vocals, Ensemble` | 多人演唱 |
| Duet | `Duet, Male and Female` | 男女对唱 |

### 音色特征（可叠加1-2个）

| 标签 | Suno标签 | 核心特征 |
|------|---------|---------|
| Deep | `Deep Voice` | 低沉饱满, 低频震动 |
| Warm | `Warm Vocals` | 温暖舒适, 中频圆润 |
| Bright | `Bright Vocals` | 明亮清晰, 高频突出 |
| Smooth | `Smooth Vocals` | 流畅无棱角 |
| Silky | `Silky Vocals` | 丝滑精致, 高级质感 |
| Soulful | `Soulful` | 灵魂感, 深层情感 |
| Smoky | `Smoky Voice` | 烟嗓, 略沙哑 |
| Gritty | `Gritty Vocals` | 粗犷, 大气沙哑 |
| Husky | `Husky Voice` | 沙哑粗糙 |
| Ethereal | `Ethereal Vocals` | 空灵梦幻, 悬浮感 |
| Powerful | `Powerful Vocals` | 厚嗓, 共振强 |
| Gentle | `Gentle Voice` | 温柔绵密 |
| Magnetic | `Magnetic Voice` | 磁性, 抓耳 |
| Sweet | `Sweet Voice` | 甜美细腻 |
| Lazy | `Lazy Vocals` | 慵懒, Layback |
| Refreshing | `Fresh Vocals` | 清新轻盈 |
| Soothing | `Soothing Voice` | 治愈包容 |
| Energetic | `Energetic Vocals` | 热血, 感染力 |
| Sexy | `Sexy Voice` | 性感, 亲密感 |

### 唱法技巧

| 标签 | Suno标签 | 说明 |
|------|---------|------|
| Rap | `Rap, Rapping` | 说唱 |
| Breathy | `Breathy Vocals` | 气声, 气息推动 |
| Whisper | `Whispered` | 轻声/耳语 |
| Falsetto | `Falsetto` | 假声 |
| Belting | `Belting` | 高音嘶吼 |
| Vibrato | `Vibrato` | 颤音 |
| Runs | `Vocal Runs` | 转音 |
| Yodeling | `Yodeling` | 约德尔唱法 |
| Growling | `Growling` | 嘶吼（金属） |
| Screaming | `Screaming` | 咆哮 |
| Spoken Word | `Spoken Word` | 念白 |
| Storytelling | `Storytelling` | 叙事式演唱 |
| Bel Canto | `Operatic, Bel Canto` | 美声唱法 |
| Scat | `Scatting` | 拟声吟唱（爵士） |
| Auto-Tune | `Auto-Tune` | 电子修音效果 |
| Ad Libs | `Ad Libs` | 即兴短句 |

---

## 乐器标签库（Instrument Tags）

### Suno 高识别率乐器标签

**弦乐器：**
`Acoustic Guitar`, `Electric Guitar`, `Bass Guitar`, `Violin`, `Cello`, `Strings`, `Ukulele`, `Banjo`, `Mandolin`, `Harp`

**键盘：**
`Piano`, `Electric Piano`, `Organ`, `Synthesizer`, `Accordion`, `Harpsichord`

**管乐器：**
`Saxophone`, `Trumpet`, `Flute`, `Clarinet`, `Trombone`, `French Horn`, `Harmonica`, `Tin Whistle`

**打击乐：**
`Drums`, `Percussion`, `Congas`, `Bongos`, `Tambourine`, `Shaker`, `Claps`

**电子/合成：**
`Synth Pad`, `Synth Lead`, `Synth Bass`, `808`, `Drum Machine`, `Arpeggiator`

**中国传统乐器：**
`Guzheng`, `Erhu`, `Pipa`, `Dizi`, `Xiao`, `Suona`, `Guqin`, `Yangqin`, `Hulusi`

**民族乐器：**
`Sitar`, `Bagpipe`, `Shamisen`, `Oud`, `Tabla`, `Djembe`, `Kalimba`, `Didgeridoo`

---

## 情绪/氛围修饰词库

### 正面情绪
`Happy`, `Joyful`, `Uplifting`, `Euphoric`, `Celebratory`, `Hopeful`, `Romantic`, `Passionate`, `Playful`, `Whimsical`, `Nostalgic`, `Warm`, `Comforting`, `Peaceful`

### 负面/深沉情绪
`Sad`, `Melancholy`, `Bittersweet`, `Heartbroken`, `Dark`, `Ominous`, `Haunting`, `Lonely`, `Anxious`, `Aggressive`, `Angry`, `Intense`

### 氛围修饰
`Ethereal`, `Atmospheric`, `Cinematic`, `Epic`, `Intimate`, `Lo-Fi`, `Dreamy`, `Psychedelic`, `Retro`, `Futuristic`, `Minimalist`, `Lush`, `Raw`, `Polished`, `Vintage`, `Modern`, `Underground`, `Mainstream`

### 能量/速度
`Energetic`, `Chill`, `Relaxed`, `High Energy`, `Mellow`, `Groovy`, `Bouncy`, `Slow`, `Fast`, `Mid-Tempo`, `Uptempo`, `Downtempo`

---

## 语言标签（Language Tags）

| Suno标签 | 语种 | 备注 |
|---------|------|------|
| `Chinese` / `Mandarin` | 普通话 | Suno对中文支持良好 |
| `Cantonese` | 粤语 | 需在歌词中体现粤语用词 |
| `English` | 英文 | Suno默认最佳语言 |
| `Japanese` | 日语 | 配合J-Pop/Enka等风格 |
| `Korean` | 韩语 | 配合K-Pop等风格 |
| `French` | 法语 | 配合Chanson等风格 |
| `Spanish` | 西班牙语 | 配合Latin等风格 |
| `Portuguese` | 葡萄牙语 | 配合Bossa Nova等 |
| `Italian` | 意大利语 | 配合Italian Pop |
| `German` | 德语 | 配合German Pop |
| `Russian` | 俄语 | 配合Russian Pop |
| `Arabic` | 阿拉伯语 | 配合Arabic风格 |
| `Hindi` | 印度语 | 配合Indian风格 |
| `Thai` | 泰语 | 东南亚风格 |
| `Turkish` | 土耳其语 | 配合Turkish Pop |
| `Instrumental` | 纯器乐 | 无人声 |

---

## 经典曲风组合模板

### 1. 华语流行抒情
```
Style: Chinese Ballad Pop, Emotional, Piano, Strings, Female Vocals, Warm, Gentle
结构: [Intro] → [Verse 1] → [Pre-Chorus] → [Chorus] → [Interlude] → [Verse 2] → [Chorus] → [Bridge] → [Chorus] → [Outro]
```

### 2. City Pop 复古
```
Style: City Pop, Funky, Groovy, Synth, Electric Guitar, Bass, 80s Japanese, Female Vocals, Silky
结构: [Intro] → [Verse 1] → [Chorus] → [Verse 2] → [Chorus] → [Interlude] → [Bridge] → [Chorus] → [Outro]
```

### 3. Lo-Fi 嘻哈
```
Style: Lo-Fi Hip Hop, Chill Beats, Jazz Samples, Vinyl Crackle, Mellow, Relaxed, Instrumental
结构: [Intro] → [Beat Loop A] → [Beat Loop B] → [Beat Loop A] → [Outro]
```

### 4. 独立民谣
```
Style: Indie Folk, Acoustic Guitar, Gentle, Intimate, Male Vocals, Warm, Storytelling
结构: [Intro] → [Verse 1] → [Verse 2] → [Chorus] → [Verse 3] → [Chorus] → [Bridge] → [Chorus] → [Outro]
```

### 5. 电子舞曲
```
Style: Future Bass, Synth, Emotional, Bright, Female Vocals, Ethereal, Drop
结构: [Intro] → [Verse] → [Build] → [Drop] → [Breakdown] → [Build] → [Drop] → [Outro]
```

### 6. 后摇氛围
```
Style: Post-Rock, Atmospheric, Crescendo, Reverb Guitar, Drums, Epic, Instrumental
结构: [Intro] → [Build A] → [Build B] → [Climax] → [Decay] → [Build C] → [Climax 2] → [Outro]
```

### 7. 国风流行
```
Style: Chinese Style Pop, Guzheng, Pipa, Erhu, Modern, Emotional, Female Vocals, Ethereal
结构: [Intro] → [Verse 1] → [Pre-Chorus] → [Chorus] → [Interlude] → [Verse 2] → [Chorus] → [Bridge] → [Chorus] → [Outro]
```

### 8. Trap 说唱
```
Style: Trap, 808, Hi-Hat, Dark, Male Vocals, Aggressive, Autotune
结构: [Intro] → [Verse 1] → [Hook] → [Verse 2] → [Hook] → [Bridge] → [Hook] → [Outro]
```

### 9. 爵士酒廊
```
Style: Vocal Jazz, Smooth, Intimate, Piano, Upright Bass, Saxophone, Female Vocals, Silky
结构: [Head In] → [Verse 1] → [Chorus] → [Solo] → [Verse 2] → [Chorus] → [Head Out]
```

### 10. 金属核
```
Style: Metalcore, Heavy, Breakdown, Screaming, Melodic, Guitar Riff, Double Bass Drums
结构: [Intro] → [Verse 1] → [Pre-Chorus] → [Chorus] → [Verse 2] → [Breakdown] → [Chorus] → [Solo] → [Chorus] → [Outro]
```

### 11. 梦幻流行
```
Style: Dream Pop, Ethereal, Reverb, Synth Pad, Dreamy, Female Vocals, Whispered, Lo-Fi
结构: [Intro] → [Verse 1] → [Chorus] → [Verse 2] → [Chorus] → [Bridge] → [Chorus] → [Fade Out]
```

### 12. 巴西Bossa Nova
```
Style: Bossa Nova, Acoustic Guitar, Gentle, Romantic, Brazilian, Female Vocals, Warm, Intimate
结构: [Intro] → [Verse 1] → [Chorus] → [Verse 2] → [Chorus] → [Instrumental Break] → [Chorus] → [Outro]
```

---

## 高级技巧

### 1. 风格融合策略
- **主风格 + 子风格**：`Indie Pop, Dream Pop` — 在独立流行基础上增加梦幻质感
- **跨类融合**：`Jazz, Electronic, Lo-Fi` — 爵士+电子+低保真
- **时代锚定**：`80s, Synth Pop, Retro` — 锁定80年代合成器美学
- **地域风味**：`Japanese, City Pop, Groovy` — 日本都市流行风味

### 2. 人声精确控制
```
# 指定性别+音色+唱法
Female Vocals, Ethereal, Breathy, Gentle

# 说唱+旋律混合
Male Vocals, Rap, Melodic, Auto-Tune

# 无人声器乐
Instrumental, No Vocals
```

### 3. 节奏与速度暗示
- **BPM 暗示词**：`Slow` (60-80), `Mid-Tempo` (90-110), `Uptempo` (120-140), `Fast` (150+)
- **律动词**：`Groovy`, `Bouncy`, `Swinging`, `Driving`, `Laid-Back`

### 4. 制作质感词
- `Lo-Fi` — 低保真, 温暖瑕疵
- `Polished` — 精致打磨
- `Raw` — 粗糙原始
- `Vintage` — 复古质感
- `Hi-Fi` — 高保真清晰
- `Analog` — 模拟质感
- `Vinyl` — 黑胶唱片感
- `Tape` — 磁带温暖感

### 5. Suno v5.5 专属技巧

**Metatags 控制**（歌词内嵌）：
- `[Soft]` `[Loud]` `[Whispered]` — 控制段落强度
- `[Guitar Solo]` `[Saxophone Solo]` `[Piano Solo]` — 触发器乐独奏
- `[Slow Down]` `[Speed Up]` — 控制速度变化
- `[Chorus x2]` — 重复段落
- `[Fade Out]` `[End]` — 控制结尾方式
- `[Build]` → `[Drop]` — 电子乐的蓄力-释放
- `[Cut Dead]` `[Silence 3s]` — v5.5 新增，精确空白控制
- `[Breath]` `[Ad Lib]` — 人声细节注入
- `[Harmony]` `[Double]` — 和声/叠声

### 6. v5.5 分轨导出工作流

生成后在 Editor 里可以：
1. **Stems Export** → 导出 Drums / Bass / Vocals / Other 四轨 WAV
2. 在 Logic / Cubase / FL 里精修，比如替换鼓组、重新 EQ 人声
3. **MIDI Export** → 拿到旋律/和声 MIDI，可无限改编
4. **回传 Audio Reference** → 把精修后的版本作为参考，Audio Influence 70 左右重新生成，保留精修气质

### 7. v5.5 三大个性化功能的提示词协作

**① 使用 Voices 模型**
```
# Voices 已锁定了你的声线特征（性别/音色/口音/气息）
# Style 字段中要做减法：
❌ Female Vocals, Warm, Breathy
✅ Warm, Breathy, Gentle Delivery
# 否则会和 Voices 打架，声线被稀释
```

**② 使用 Custom Models**
```
# 自定义模型已吸收你的 6+ 首作品风格
# Style 字段只写"这首要跟那些作品不同的地方"
❌ Indie Pop, Dream Pop, Lo-Fi, Warm, Female Vocals, Synth, ...（全部堆）
✅ Slightly Faster, More Acoustic, Brighter Mood
```

**③ 使用 My Taste**
```
# 系统已学习你的偏好
# 常用元素（你 80% 的歌都有的东西）可以省略
# 只写本次创作的"变量"
```

---

## 参数推荐矩阵（按场景）

| 场景 | BPM | Key | Weirdness | Style Inf. | Section | 备注 |
|------|-----|-----|-----------|-----------|---------|------|
| 华语抒情 | 70–85 | C/G Major 或 A/E Minor | 25 | 80 | ON | 标准流行结构 |
| City Pop | 92–108 | F Major / D Major | 30 | 85 | ON | 80s 复古必备 |
| Lo-Fi 嘻哈 | 70–90 | A Minor / D Minor | 35 | 75 | OFF | 氛围优先 |
| EDM Drop | 126–135 | C Minor / A Minor | 40 | 90 | ON | Drop 段必须精控 |
| 摇滚 | 110–140 | E Minor / A Minor | 30 | 85 | ON | — |
| 金属 | 140–180 | E Minor / D Minor | 35 | 90 | ON | 标签宜狠宜快 |
| 武侠纯音乐 | 60–90（沉）/ 120–140（激烈）| D Minor / A Minor | 40 | 90 | ON | 中国调式 + 戏曲结构 |
| 古典/后摇 | 60–90 | 按情绪选 | 30 | 85 | ON | 长段落 |
| 电子实验 | 自由 | 自由 | 65 | 80 | OFF | 要怪才对 |
| 儿歌/童声 | 100–120 | C Major / G Major | 15 | 80 | ON | 低 Weirdness |

---

## 禁忌与注意事项（v5.5 更新版）

1. **避免矛盾标签**：不要同时使用 `Aggressive` + `Gentle`，`Fast` + `Slow`
2. **标签数量控制**：Style 字段限 120 字符，建议 **5–8 个标签**为最佳
3. **语言一致性**：Style 标签统一英文，歌词使用目标语言
4. **不要过度堆叠乐器**：Style 字段里 2–4 个关键乐器即可；更详细的配器**挪到 Instrumentation 字段**
5. **v5.5 新禁忌**：
   - 使用 Voices 时 **不要再写性别**（会和声线模型冲突）
   - BPM 优先用**数字**，"Slow/Fast" 留给辅助
   - 调性写错会让情绪偏离（Minor 标成 Major = 悲歌变欢歌）
   - Weirdness 不要随便拉到 80+（实验性失控）
6. **Suno v5.5 仍不擅长的**：
   - 极端复杂拍号频繁切换（7/8 → 5/4 → 3/4）
   - 超过 5 分钟的精确全曲结构控制（比 v5 好一点，但仍有漂移）
   - 完全忠实翻唱特定艺人（会被版权识别拦截）
   - 同一首歌内切换 3+ 种完全不同的曲风
7. **最佳实践**：
   - 先简洁标签 + 标准参数试水 → 开 Section Steering 控段落 → 分轨导出精修
   - 强风格锁定用 Style Influence 90+，**不要**靠堆标签
   - 重要作品**开 Stems Export** 留后手

## 曲式结构参考（Song Structure）

### Pop/流行标准结构
```
[Intro] → [Verse 1] → [Pre-Chorus] → [Chorus] → [Interlude] → [Verse 2] → [Pre-Chorus] → [Chorus] → [Bridge] → [Chorus] → [Outro]
```

### EDM/电子标准结构
```
[Intro] → [Build] → [Drop] → [Breakdown] → [Build] → [Drop] → [Outro]
```

### Jazz/爵士标准结构
```
[Head In] → [Solo 1] → [Solo 2] → [Head Out] → [Coda]
```

### Hip Hop/嘻哈标准结构
```
[Intro] → [Verse 1] → [Hook] → [Verse 2] → [Hook] → [Verse 3] → [Hook] → [Outro]
```

### Rock/摇滚标准结构
```
[Intro] → [Verse 1] → [Chorus] → [Verse 2] → [Chorus] → [Guitar Solo] → [Bridge] → [Chorus] → [Outro]
```

### Classical/古典结构
```
[Exposition] → [Development] → [Recapitulation] → [Cadenza] → [Coda]
```

### Progressive/渐进结构
```
[Intro] → [Theme A] → [Theme B] → [Development] → [Theme A Variation] → [Theme B Variation] → [Climax] → [Outro]
```

---

*基于专业音乐知识图谱构建 | Suno v5.5 (2026-03-27) 规范对齐 | 覆盖 246 条曲风 · 24 种语言 · 80 个人声标签 · 799 条乐器×技法（17 家族） · 20 种曲式结构 · v5.5 Voices / Custom Models / My Taste / Stems / MIDI 全功能覆盖 | 完整图谱见 `references/`*
