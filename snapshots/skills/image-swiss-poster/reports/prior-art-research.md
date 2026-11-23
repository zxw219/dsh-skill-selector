# 先前研究记录 · image-swiss-poster

检索日期：2026-09-28

---

## 1. 检索方法与本轮缺口

| 路径 | 状态 |
|---|---|
| 官方脚本 `qiaomu-meta-skill/scripts/research_prior_art.py` | ❌ **未能运行** |
| 本机技能库全量查重（137 项顶层技能） | ✅ 完成 |
| 外部网页检索（目标模型参数） | ✅ 完成 |
| skills.sh / SkillsMP 注册表检索 | ❌ **missing evidence** |

**官方脚本失败原因（如实记录）**：

```
FileNotFoundError: [WinError 2] 系统找不到指定的文件。
  File "scripts/research_prior_art.py", line 67, in run_skills_sh
    completed = subprocess.run(["npx", "--yes", "skills", "find", query], ...)
```

脚本用 `subprocess.run(["npx", ...])` 调起 npx，**未处理 Windows 下需要 `.cmd` 后缀**的问题。补上 node 目录到 PATH 后仍失败——因为 `CreateProcess` 不会自动补后缀。**属脚本自身的跨平台缺陷，非本机环境问题。**

**后果**：外部技能市场的采纳度与星级数据**未取得**。本包的先前研究**降级为本机查重 + 公开网页检索**，外部注册表覆盖标为 `missing evidence`。

---

## 2. 本机技能库查重（137 项）

### 2.1 同名 / 近名

| 探测词 | 结果 |
|---|---|
| `swiss` | **无** |
| `character-poster` | **无** |
| `typographic` | **无** |
| `poster` | `cinematic-poster-designer`、`semantic-concept-poster` |

**结论**：无同名技能，可直接新建。

### 2.2 触发面碰撞面评估

| 既有技能 | 重叠点 | 风险 | 处置 |
|---|---|---|---|
| `cinematic-poster-designer` | 「海报」+ 角色 | 🟡 中 | 本包专做**平面排版海报**；对方做**电影剧照感海报**。已在 SKILL.md 与 README 写死边界 |
| `semantic-concept-poster` | 「海报」+ typography + cover | 🟡 中 | 对方从**词/短语/概念**出发；本包从**角色**出发。已在边界表列出 |
| `industrial-brutalist-ui` | **唯一含 `swiss` 关键词**的既有技能 | 🟢 低 | 对方是 **UI 界面**设计（"Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics"），不是海报。避开路径：本包 description 不写 "UI / interface / web" |
| `brandkit` | brand / editorial / grid / typograph | 🟢 低 | 对方做**品牌规范板**；本包做**单张角色海报**。已在边界表列出 |
| `dreamy-motion-editorial` | editorial / 海报 / 封面 | 🟢 低 | 对方做**朦胧梦幻动态编辑图**；风格取向相反 |
| `world-visual-development-director` | 提到 GPT Image 2 | 🟢 低 | 对方做**世界观视觉开发**；本包只做海报排版 |
| `character-casting-studio` | 角色 | 🟢 低 | 对方做**选角定妆表**；本包不碰角色设计 |
| `visual-style-aesthetic-direction` | 视觉风格总控 | 🟢 低 | 对方是方法论总控；本包是具体风格落地 |

**边界策略**：本包以 **「瑞士主义 / 国际主义平面设计 + 角色海报」** 这一组合为独占触发面，description 中同时出现 `瑞士主义`、`国际主义平面设计`、`Modern Swiss Style`、`竖版角色海报`、`超大无衬线标题`、`非对称网格` 等独占词。

---

## 3. 外部检索发现

### 3.2 目标模型参数

来源：第三方公开登记与自测（检索日 2026-09-28）。
可信度**中等**。分歧点（参考图数量 5 / 16）已在 `references/02-model-adaptation.md` 如实标注。

---

## 4. keep / adapt / reject / invent

| 决策 | 内容 |
|---|---|
| **keep** | 源提示词**九层结构逐字保留**。这是本包的价值主干，不做改写 |
| **keep** | 「只保留一种高饱和强调色」「不使用传统居中立绘」「字体本身成为主要图形元素」三条硬约束原样保留 |
| **adapt** | 把「自动提取强调色」升级为**可由用户显式指定**——实测四张成片的强调色都取自角色自身元素，主动权应交回用户 |
| **adapt** | 把「文字内容自动生成」升级为**显式列出全部文字**——画面文字准确度是这套风格唯一的高失败率点 |
| **adapt** | 补入 GPT Image 2 / 2.5 的分辨率、质量档、画幅与成本建议 |
| **reject** | ❌ **不采纳示例图中的品牌元素**。成片带有品牌签名与相关标记；按指示，这类内容**不进入本技能的规则或模板** |
| **reject** | ❌ 不做成「出图执行型」技能。本包**只输出提示词** |
| **invent** | **10 类失败模式与修法补句**（`04-failure-modes.md`）——由模板逻辑与成片反推，源材料无此内容 |
| **invent** | **版式配方与字号尺度比 20:6:2:1**（`03-visual-anatomy.md`）——由四张成片实测归纳 |
| **invent** | **九层功能拆解表**——说明每层删掉会怎样，用于判断「能不能删」 |

---

## 5. 公平性声明

本包的贡献是**结构化与可执行化**：把一段约 700 字的自然语言提示词，拆成可判断、可修补、可选参数的操作单元，并配齐视觉证据与失败诊断。

**不主张**它比其他海报类技能更优——本机既有的 `cinematic-poster-designer`、`semantic-concept-poster` 解决的是**不同**任务（电影感 / 概念表达），本包只覆盖**瑞士国际主义平面排版**这一个方向。**没有做过横向生成质量对照实验**，任何"更高质量"的说法都缺乏证据，故不提出。
