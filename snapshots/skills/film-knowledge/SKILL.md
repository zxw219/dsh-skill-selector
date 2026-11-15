---
name: film-knowledge
description: "影视知识库总入口。覆盖摄影布光、镜头设计、大师镜头、导演叙事、声音设计、调色、场景转场共 90 个专题技能。当用户问到布光、灯光、机位、焦段、景深、构图、轴线、景别、镜头调度、分镜、对话场面、声音、音效、配乐、调色、色温、肤色、转场、节奏、场面张力、摄影语言时，先加载本技能定位板块，再进入对应专题技能，不要凭印象直接回答。"
metadata: {"openclaw":{"source":"本地知识库，由 10 本影视专著整理"}}
---

# film-knowledge：影视知识库路由

识别用户问题落在哪个板块，再加载对应专题技能。**不要跳过本入口直接凭记忆作答**——每个专题技能都带有具体的操作步骤和判断标准，比通用建议更准。

## 使用方式

1. 判断问题落在下表哪个板块
2. 用 skill 工具加载该板块里对应的专题技能
3. 一个技能不够时再补同板块的相邻技能（下表「常配套」列）
4. 只有确实没有匹配项时，才用本技能的通用判断回答

## 板块一：摄影与布光（8）

| 用户问的是 | 加载 |
|---|---|
| 该用什么机身/镜头/焦段组合 | `camera-lens-anchoring` |
| 180 度法则、轴线、画面方向、机位该放哪边 | `cinematography-180-degree-rule` |
| 从后场打光、实景光源不够亮、台灯窗户光 | `cinematography-back-lighting` |
| 硬光软光、阴影清晰或模糊、光源大小 | `cinematography-hard-soft-light` |
| 灯光方向、侧光背光、主光位置、要戏剧感或神秘感 | `cinematography-light-direction-mood` |
| 主场景法、先拍什么、镜头顺序、覆盖策略、备选镜头 | `cinematography-master-scene` |
| 三点布光、灯光比、主光补光背光怎么配 | `cinematography-three-point-lighting` |
| 分区曝光、第 V 区、中灰 18%、想更亮或更暗 | `cinematography-zone-system` |

常配套：布光问题先看 `cinematography-three-point-lighting`，再按方向查 `cinematography-light-direction-mood`，光质查 `cinematography-hard-soft-light`。

## 板块二：镜头设计（8）

| 用户问的是 | 加载 |
|---|---|
| 摄影角度、仰拍俯拍、低角度怎么用、画面感觉不对 | `shot-design-angle-context` |
| 轴线、跳轴、空间连续性、银幕方向 | `shot-design-axis-of-action` |
| 构图、特写怎么构图、剪辑节奏 | `shot-design-continuity-composition` |
| 对话场景怎么拍、两三人多人对话、调度 staging | `shot-design-dialogue-staging` |
| 纵深调度、前景中景后景、景深、空间分隔 | `shot-design-dramatic-range` |
| 视点、POV、主观镜头、观众代入感 | `shot-design-pov-spectrum` |
| 视线方向、怎么切镜头、空间关系 | `shot-design-sightline-cut` |
| 画分镜、故事板、把剧本变成镜头 | `shot-design-storyboard-rapid` |

## 板块三：大师镜头 I — 动作与摄影编舞（6）

| 用户问的是 | 加载 |
|---|---|
| 演员怎么走位、摄影机怎么配合、人机同时运动 | `shot-camera-choreography` |
| 怎么吓人、分散注意、出其不意、打破预期 | `shot-distract-and-scare` |
| 双机位、不同运动状态、手持对推车、力量对比 | `shot-dual-camera-tension` |
| 等长镜头、平行剪辑、节奏控制、打破节奏 | `shot-equal-length-rhythm` |
| 角色做决定的瞬间、静止与运动对比 | `shot-still-vs-motion-decision` |
| 借位打斗、让距离看起来更近、长焦压缩 | `shot-telephoto-compression` |

## 板块四：大师镜头 II — 对话场面（14）

| 用户问的是 | 加载 |
|---|---|
| 障碍物、物理隔离、隔窗隔墙隔栏杆对峙 | `dialogue-barrier-narrative` |
| 对话时死盯眼睛、表演舞台化、手没处放 | `dialogue-busy-hands-no-eye-contact` |
| 追逐跟拍时摄影机该跟谁 | `dialogue-camera-follow-identity` |
| 机位高度、观众立场、仰俯拍怎么定 | `dialogue-camera-height-stance` |
| 特写切太多、错过表情、不确定何时切入 | `dialogue-closeup-timing` |
| 深布景、三层空间、小空间显得不挤 | `dialogue-deep-staging` |
| 延迟揭示、角色出场、背影、关键台词 | `dialogue-delayed-reveal` |
| 情绪崩溃后回到日常、推近表达情感深入 | `dialogue-distance-collapse-arc` |
| 同一角色要显得更友好或更可怕、焦距选型 | `dialogue-focal-character-temperament` |
| 焦距变化、走近、逐步缩近距离 | `dialogue-focal-progression` |
| 三人以上群戏交代空间、不用全景建立关系 | `dialogue-gaze-mapping` |
| 位置交换、权力转移、主导地位变化 | `dialogue-position-swap` |
| 任务过载、本能表演、演员反对、靠动作演 | `dialogue-task-overload` |
| 听到无法承受的消息、直视眼睛、制造窒息感 | `dialogue-telephoto-claustrophobia` |

## 板块五：大师镜头 III — 情绪与视觉叙事（6）

| 用户问的是 | 加载 |
|---|---|
| 肢体表演、特写与全景怎么配合 | `msv3-body-performance` |
| 焦距选择、镜头情感、长焦广角的效果 | `msv3-lens-emotion-mapping` |
| 权力关系、人物距离、谁更有力量 | `msv3-power-distance` |
| 速度感、紧迫感、追逐怎么拍 | `msv3-speed-conveyance` |
| 象征性调度、用镜头讲关系 | `msv3-symbolic-staging` |
| 揭示、意外、悬念怎么留 | `msv3-unexpected-reveal` |

## 板块六：导演叙事（15）

| 用户问的是 | 加载 |
|---|---|
| 这段有用吗、要不要删、为什么看起来无聊 | `directing-activity-vs-action` |
| 太模糊、观众能不能看懂、要不要解释清楚 | `directing-ambiguity-diagnosis` |
| 巧合太假、转折突兀、运气成分太重 | `directing-coincidence-trouble` |
| 元素太多不知突出什么、该放大还是收敛 | `directing-contrast-emphasis` |
| 这个设定合理吗、观众会信吗、太假 | `directing-credible-impossible` |
| 戏剧反讽、信息差、观众知道角色不知道 | `directing-dramatic-irony` |
| 不知从哪开头、不知道怎么收、结构散了 | `directing-end-before-begin` |
| 想不到点子、灵感枯竭、卡住了 | `directing-idea-generation` |
| 摄影机放哪、观众该认同谁、怎么引导注意力 | `directing-invisible-witness` |
| 对话像聊天不像交锋、信息平铺直叙 | `directing-odets-rewrite` |
| 多个重要角色、不确定谁是主角、主角存在感弱 | `directing-protagonist-endangered` |
| 重大事件但观众反应平淡、该拍事件还是反应 | `directing-reaction-over-action` |
| 这段要不要删、场景松散、结构拖沓 | `directing-scene-necessity` |
| 故事结构、叙事框架、支线怎么设计 | `directing-story-framework` |
| 场景为什么无聊、只有期待没有不确定 | `directing-tension-formula` |

## 板块七：声音设计（13）

| 用户问的是 | 加载 |
|---|---|
| 三层听觉层级、前景中景背景声音怎么排 | `sound-design-auditory-hierarchy` |
| 声画一致性、声音与画面脱节 | `sound-design-consistency` |
| 声音太平、戏剧性不足、靠对比制造张力 | `sound-design-contrast-drama` |
| 声源分类、画内画外、叙事内叙事外 | `sound-design-diegetic-taxonomy` |
| 四层声音能量模型、整体声音设计框架 | `sound-design-energy-model` |
| 用节律牵引观众生理反应、心跳呼吸节奏 | `sound-design-entrainment` |
| 声音的期待与回报、怎么建立和打破预期 | `sound-design-expectation` |
| 声音太满、元素太多、要更精简有力 | `sound-design-less-is-more` |
| 四种聆听模式、观众怎么听 | `sound-design-listening-modes` |
| 音乐与故事平行结构、旋律对应角色 | `sound-design-music-story-parallel` |
| 控制声源听感大小、远近感 | `sound-design-size-control` |
| 奏鸣曲式对应戏剧结构 | `sound-design-sonata-drama` |
| 同步幻觉、声画对位的心理效应 | `sound-design-sync-illusion` |

## 板块八：调色（11）

| 用户问的是 | 加载 |
|---|---|
| 色温、偏色、冷暖、混合光源 | `color-grading-color-temperature` |
| 调对比后颜色变了、调色顺序 | `color-grading-contrast-before-color` |
| 对比度与饱和度互相影响、RGB 处理 | `color-grading-contrast-saturation` |
| 滤镜效果、模拟光学、数字滤镜 | `color-grading-filter-nonlinear` |
| Log 素材（RED/ARRI/Sony RAW）处理流程 | `color-grading-log-workflow` |
| 建立创意色彩风格 Look | `color-grading-look-development` |
| 肤色不对、色彩准确性、观众心理预期 | `color-grading-memory-colors` |
| 严重过曝、高光救不回来 | `color-grading-overexposure-recovery` |
| 一级校色、Lift/Gamma/Gain 怎么调 | `color-grading-primary-workflow` |
| 同场景多镜头不一致、镜头匹配 | `color-grading-shot-matching` |
| 肤色示波器、I-bar、各人种肤色范围 | `color-grading-skin-tone-vectorscope` |

## 板块九：场景转场（9）

| 用户问的是 | 加载 |
|---|---|
| 场景对比、二元对立、场所并置产生张力 | `scene-transition-binary-opposition` |
| 场景多余、要不要删、节奏拖沓、末节场景 | `scene-transition-caboose-diagnosis` |
| 转场该怎么做、场景怎么衔接、过场风格 | `scene-transition-four-function-diagnosis` |
| 场景太紧张、观众需要休息、审美疲劳 | `scene-transition-low-point-no-plot` |
| 观众认同谁、角色转换、配角戏份 | `scene-transition-loyalty-transfer` |
| 转场用什么音乐、静默还是配乐、音频过渡 | `scene-transition-music-quadrant` |
| 无缝过渡、观众没意识到在休息 | `scene-transition-seamless-pause` |
| 多线叙事、故事线怎么交汇、同步节点 | `scene-transition-synch-node` |
| 天气、天气配合情绪、天气对比 | `scene-transition-weather-contrast` |

## 跨板块问题的处理

用户的问题经常横跨两个板块，按下面的顺序组合：

- **"这场戏不抓人"** → 先 `directing-tension-formula` 诊断，再看 `scene-transition-caboose-diagnosis` 是否该删
- **"对话戏怎么拍"** → `shot-design-dialogue-staging` 定调度，再从板块四挑具体手法
- **"画面不好看"** → 先分清是构图问题（板块二）还是布光问题（板块一）还是调色问题（板块八）
- **"声音不对"** → 先 `sound-design-auditory-hierarchy` 分层，再按问题类型进具体技能
- **"这场戏没张力"** → 走板块六的 `directing-tension-formula` 诊断，再看板块九决定是否该删

一次最多加载 2–3 个专题技能，够用就停，不要把整块知识库一次性拉进来。
