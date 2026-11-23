# 维护记录：情绪曲线与双向情趣（2026-10-17）

## 触发

用户在前一轮完成动作、运镜、构图、表演、分镜五项优化后追问“情趣方面呢”，确认两块都补。

## 现状核对

- **情绪侧**：`performance-scene-director` 有 12 类情绪画像（怒、哭、哀、喜、乐、惧、焦虑、羞耻、嫉妒、厌恶、惊讶）与转折组合，覆盖“单点怎么演”。缺口在整段：没有四拍、没有起点与终点的差别要求、没有释放触发、受击后只有“反应链正确”而没有落点选择、双人没有两条曲线交错。`execution-rules.md` 20 条中第 3、6、14 条涉及情绪，均为反应正确性，未管整段走向。
- **情趣侧**：`adult-combat-detail-direction.md` 94 行，覆盖展示方式（正面推进、斜侧上身、腰胯腿线、他人反应交接）、衣料受力、腿技、动态身体。全部是“一个人被观看”。缺口在互动：没有发起—接收—回应三跳、没有张力来源分类、没有节拍、没有与交锋共时的窗口要求、没有相邻互动差异门槛。

## 根因

与上一轮动作单一同源：素材齐但选用层没有门槛。情趣只有展示层，所以写出来永远是“她被看着”而不是“两人在来回”；情绪只有单点画像，所以每簇从头起、受击只会忍。

## 改动

| 文件 | 变更 |
|---|---|
| `an-workflow/references/emotion-arc-design.md` | 新建，120 行。四拍总谱、情绪决定攻击端（6 行倾向表）、压制三载体、释放三类触发、受击四落点、双线三交错、台词身体错位、六项门槛、An 分栏实例 |
| `an-workflow/references/adult-combat-detail-direction.md` | 94→174 行。新增「双向情趣：发起、接收与回应」「张力的三个来源」「情趣节拍：试探、确认、升温、收手」「与交锋共时」「反用：情趣也是战术」「相邻互动的差异门槛」；开头加两层分工与采用条件，同次检查加互动四项。章节顺序为展示层→动作层→互动层→实例→检查，互动层整体置于动作层之后 |
| `an-performance-direction/references/execution-rules.md`（由 json 生成） | 20→22 条，新增第 21 条情绪曲线、第 22 条情趣三跳 |
| `an-workflow/references/director-handbook.md` | 新增「情绪曲线与动作绑定（按需）」小节；成年魅力节补双向情趣一段 |
| `an-workflow/references/final-check.md` | 完整人物表演专项新增「情绪曲线」「情趣互动」两条 |
| `an-workflow/references/storyboard-sequence-design.md` | 每簇观看发展允许情绪位移单独成立，接情绪曲线与情趣回应 |
| `an-workflow/references/storyboard-visual.md` | 成人魅力节补互动层构图分配 |
| `an-workflow/SKILL.md` | 路由表 +2 行；「全面优化采用增量并入」检查项加入情绪曲线与情趣互动 |
| `an-workflow/references/source-decisions.md` | 追加本轮决策记录 |
| `an-workflow/assets/functional-skills.json` | 表演模块 rules +2、routes +2、sources +1（emotion-arc-design）；动作、质检模块 sources +1；动作 routes +1；质检 routes +1 |

新增来源 `an-workflow/references/emotion-arc-design.md` 接入三个模块：an-performance-direction（主）、an-action-design（情绪决定攻击端）、an-quality-review（终检）。

## 打包路径纠正

本轮发现维护路径问题：权威源在 `~/.codex/skills/`，`D:\An工作流\skills\` 是分发副本。直接在分发目录改源会被 `sync_bundle.py` 的手工改动保护拦下。正确流程是改 `~/.codex/skills/` 下对应文件，再运行打包，由脚本覆盖分发副本。

另修正：extracted 版 `execution-rules.md` 的规则文本不能带跨目录链接（模块目录是独立根，链接会 escape），规则内改为文字指路，链接统一放在入口路由表。

## 验证

- 打包：`status=updated`，3395 受管文件，15819 条链接，14627 条模块内链接，12 功能技能 + 11 原始技能，13 个 ZIP 校验通过，`section_anchors_validated=true`。
- 内容核对：`emotion-arc-design.md` 进入 12 个功能技能库；`execution-rules.md` 26 行（22 条）；`adult-combat-detail-direction.md` 172 行；四个模块入口各含新路由。
- 未做：未生成试片，未做独立试写对照。文本结构通过不等于成片情绪与情趣张力成立，需要实际生成后观看验证。

## 边界

情趣互动保持成年身份、双方自愿、非露骨、衣料覆盖四项；本场未采用时不强制执行，与展示层一样属于可选表现空间。情绪曲线为通用要求，整体压制或整体冷静按本段目的成立，仍要能指出余量变化。
