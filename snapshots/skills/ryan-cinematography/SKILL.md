---
name: ryan-cinematography
description: 为明确请求 ryan 摄影风格或其对应摄影师视觉语言的任务编写图片/视频提示词、分析构图与色彩、设计打光。泛泛的电影感或自然光需求不单独触发；按场景选择技法并尊重用户指定的时代、主体和模型。
metadata:
  version: 1.0.0
  author: Moke & 呼噜噜
  agent_created: true
  tags:
  - Robbie Ryan
  - cinematography
  - Irish cinematographer
  - Yorgos Lanthimos
  - Andrea Arnold
  - Ken Loach
  - Noah Baumbach
  - fisheye ultra wide
  - 4:3 Academy ratio
  - 35mm film
  - naturalistic lighting
  - handheld realism
  - The Favourite
  - Poor Things
  - Fish Tank
  - Wuthering Heights
  - American Honey
  - Marriage Story
  - Kinds of Kindness
  - prompt engineering
  - AI image generation
  - cinematic style
  triggers:
  - 瑞恩风格
  - 罗比瑞恩
  - Robbie Ryan
  - Ryan style
  - Ryan cinematography
  - Ryan lighting
  - 宠儿摄影
  - 可怜的东西摄影
  - 鱼缸摄影
  - 呼啸山庄摄影
  - 美国甜心摄影
  - 婚姻故事摄影
  - 龙虾摄影
  - Lanthimos 鱼眼
  - 超广角鱼眼
  - 鱼眼宫廷
  - 4:3 画幅
  - 学院画幅
  - 爱尔兰乡村摄影
  - 约克郡阴郁
  - 英伦阴雨
  - 怪奇彩色
  - 工人现实主义
  - 瑞恩提示词
  - Ryan prompt
---

# 🎬 Robbie Ryan 摄影风格大师 — Cinematography Style Skill

## 风格选择

根据场景从以下方向选择，不要求每次全部使用：

- 🐟 超广角鱼眼凝视（Ultra-Wide Fisheye Gaze）
- 📺 4:3 学院画幅复古（Academy Ratio 4:3 Revival）
- 🎞️ 35mm 胶片的灵魂（35mm Film Soul）
- ☁️ 自然光实景（Available Light, Real Locations）
- 📱 Andrea Arnold 式手持现实主义（Arnold Handheld Realism）
- 🌧️ 英伦阴雨青绿（British Overcast Blue-Green）
- 🍭 《可怜的东西》怪奇彩色梦境（Poor Things Surreal Color Dream）
- 🏚️ 约克郡阴郁荒野（Yorkshire Moor Bleakness）
- 👷 Loach 工人阶级写实（Loach Kitchen-Sink Realism）
- 💔 Baumbach 婚姻低对比（Baumbach Marriage Low Contrast）

## 执行规则

- 用户明确的主体、时代、肤色、画幅、语言、镜头和输出格式优先；风格偏好是默认选择，不是禁止其他选择的硬限制。
- 先识别任务是图片提示词、视频提示词、风格分析还是实拍方案。信息足够时直接完成；只询问会实质影响结果的缺失信息。
- 选择适合当前场景的 2–3 个技法，写成可观察的光源方向、光质、构图、景深、色彩和材质。不要把所有关键词同时堆入一条提示词。
- 图片描述单一可见瞬间；视频再加入主体动作、运镜和时间变化。景深、镜头运动、黑白/彩色和负面词必须与正面描述一致。
- 不主动调用生成工具或发布作品；本 Skill 提供提示词与摄影方案，实际生成按用户当前请求和可用工具执行。

## 按需参考

- 需要场景模板时读取 [style-prompts.md](references/style-prompts.md)，只采用相关段落，修正与本次需求冲突的正负面词。
- 需要影片对标时读取 [filmography-analysis.md](references/filmography-analysis.md)。其中片目、摄影署名、器材、数字和引语是待核对资料；对外作为事实引用前查证可靠来源，未查证时只描述视觉特征。
- 需要扩展技法时读取 [visual-notes.md](references/visual-notes.md)。该文件保留原入口资料，属于历史参考，不是执行规则；其中绝对措辞、强制输出格式和参数示例不得覆盖本入口或用户指令。

## 模型与参数

- 未指定目标模型时提供通用自然语言提示词，不混入某个平台的参数。不要宣称所有模型都支持独立负面提示词、LoRA 或相同权重语法。
- Midjourney 的画幅参数使用整数：1.85:1 → `--ar 37:20`，2.39:1 → `--ar 239:100`，2.20:1 → `--ar 11:5`，1.37:1 → `--ar 137:100`；4:3 与 Academy 1.37:1 不等同。
- 默认使用 Midjourney 8.2，MJ 提示词明确附上 `--v 8.2`；用户指定其他版本时服从用户。不要添加 `--preview` 或从旧模板复制质量参数。版本相关参数按官方兼容表核对；Raw 是可选的提示词控制模式，不保证胶片、饱和或特定风格效果。
- 对 FLUX、Stable Diffusion 或视频模型，按实际版本与界面能力选择语法。摄影机、胶片和镜头名称用于视觉描述时不等于真实制作设备或精确复现保证。

## 输出与检查

默认给一条可复制的完整提示词，必要时附简短中文说明；用户要拆分 Style/Scene、多个版本或详细打光方案时再展开。提示词语言服从用户要求，未指定时可用英文。实拍方案说明光源位置、主辅光关系和曝光意图，不照搬生成模型参数。

提交前检查：主体与风格是否一致；正负面词是否互相否定；画幅参数是否有效；静态与动态描述是否匹配；影片与引语是否有可靠依据。

参数核对来源：[Midjourney Aspect Ratio](https://docs.midjourney.com/hc/en-us/articles/31894244298125-Aspect-Ratio)、[Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)、[Raw](https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw)。
