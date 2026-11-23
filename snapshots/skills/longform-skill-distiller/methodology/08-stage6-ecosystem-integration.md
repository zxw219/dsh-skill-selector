# 阶段 6 — 生态接入

## 目标

蒸馏出来的 Skill 不应成为一组孤岛，也不能靠增加“相关 Skill”名单制造虚假整合。本阶段把它们接入目标宿主的真实 Skill 生态，使每个保留项都有唯一控制面、明确交接、最小中央路由和可回归的跨生态测试。

## 第 1 步 — 盘点真实生态

1. 确认安装目标：Codex 通常是 `~/.codex/skills/`，其他宿主使用其实际 skills 根目录。
2. 枚举现有 `*/SKILL.md`；先读取 `name` 与 `description`，再精读与新方法最接近的 Skill、中央 orchestrator、governor、ledger/review/iteration 层。
3. 精确路径和名称用 literal search；概念分散时可使用本地 semantic recall，但最终结论必须回读原文件。
4. 记录每个相关既有 Skill 的：trigger、控制面 owner、输入、输出、上游、下游和明确边界。

禁止凭模型记忆、旧 INDEX 或聊天摘要认定某 Skill 存在或拥有某职责。

## 第 2 步 — 四类归宿判定

对每个通过阶段 4 的新 Skill 做一次生态判定：

| 分类 | 判定 | 动作 |
|---|---|---|
| 独立 owner | 现有生态没有同一控制面，且新方法能产生独立可验收输出 | 保留并安装，接入最小路由 |
| 收窄互补 | 与既有 Skill 相邻但输入/输出不同 | 收紧 description 和边界，写明确 handoff |
| 并入既有 | 与既有 Skill 触发、步骤、输出和验收高度重叠 | 不安装重复目录；把独特证据并入既有 Skill 后回归测试 |
| reference / capsule | 有价值但不足以独立触发，或只是案例/规则 | 存入正确 reference、case、capsule 或审计层，不伪造新 Skill |

至少回答：删掉这个新 Skill，哪一个可观察决策会失去 owner？如果答不出来，优先合并或降级。

## 第 3 步 — 写可执行交接

每个保留新 Skill 增加“现有生态接入”小节，只写 2–4 个高价值关系：

- `receives-from`：从谁接收什么已批准输入；
- `hands-off-to`：输出交给谁、对方如何消费；
- `routes-to`：本 Skill 只做决策，具体执行交给谁；
- `checked-by` / `verified-by`：用什么实际证据验收；
- `compiled-by`：项目级文档如何变成单次可执行输入；
- `governed-by`：架构变化由谁决定保留、回退或传播。

每条都必须写出 owner 边界。只写“与 X 配合”不合格。

## 第 4 步 — 最小中央接入

1. 优先创建或更新一个 bridge reference，由现有中央 orchestrator 按任务规模和风险读取。
2. 中央路由只列新 Skill 的控制面和 load gate，不复制完整方法正文。
3. 既有 specialist 只有在真实触发、输入或交接改变时才反向更新；没有改变就不碰。
4. 新项目级方法不得自动成为每个单次任务的 mandatory baseline。
5. 保持一个控制面一个 owner；支持 Skill 只能提供约束或证据，不能抢写最终输出。

禁止：

- 所有新旧 Skill 两两互链；
- 把同义方法换名后同时保留；
- 为了显得完整而修改十几个无关 Skill；
- 把完整 Bible、治理文档或 Skill 名单粘进模型提示词。

## 第 5 步 — 生成生态接入图

按 `templates/ECOSYSTEM_INTEGRATION.md.template` 输出 `books/<slug>/ECOSYSTEM_INTEGRATION.md`。必须包含：

- 接入原则；
- 新 Skill × 控制面 × 既有 owner × handoff × 不拥有的矩阵；
- 3–5 条真实组合路线；
- 不重复造轮子的边界；
- 安装和验证状态。

## 第 6 步 — 跨生态路由测试

在 `eval/ecosystem-routing-tests.json` 中至少覆盖：

1. **新 Skill 应拥有**：既有 Skill 不应吞掉新控制面；
2. **既有 Skill 应拥有**：出现相邻词不应误触发新 Skill；
3. **顺序组合**：输出 `primary_owner` 与最多 3 个 `route`，顺序必须反映输入/输出交接；
4. **低风险跳过**：一次性简单任务不应加载项目级治理链；
5. **硬边界**：对原内容中的关键反例继续零容错。

优先用独立 Agent 盲测。修改 `description` 时必须重跑阶段 4 全量测试；只改正文交接时，至少重跑原边界例和本阶段生态测试。

## 第 7 步 — 同步与收尾

1. 运行 skill validator、JSON/YAML 解析、链接存在性和占位符检查。
2. 将最终新 Skill 同步到安装目录；比较源/目标哈希。
3. 对被修改的既有 Skill 一并验证。
4. 若宿主有本地语义索引，完成修改后重建或刷新。
5. 在 `PIPELINE_STATE.md` 记录：四类归宿、中央路由改动、生态测试结果、安装位置和验证结果。

只有以上全部完成，蒸馏流水线才算完成。
