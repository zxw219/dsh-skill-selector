---
name: evidence-driven-self-iteration
description: 证据驱动自迭代工具：基于近期工作、用户纠正、案例、知识胶囊、技能状态和来源新鲜度开展周期性自审，形成可验证、可回滚的改进。用于技能栈和工作流持续优化。
version: 1.0.0
---

# Evidence-Driven Self Iteration

## Bottom-Layer Reasoning

Apply `sophia-mode`, `think-one-step-further`, `creative-research-first`, and `capsule-engine`:

- Review evidence, not imagined shortcomings.
- Separate a one-off mistake from a recurring system weakness.
- Search current primary sources only for relevant gaps or stale areas.
- Prefer the smallest safe improvement.
- Validate every edit and keep a reversible record.

## Core Intent

Periodically inspect how the system actually performed:

```text
recent evidence -> recurring patterns -> root cause -> research if needed
-> safe improvement or recommendation -> validation -> case/capsule update
```

The purpose is to reduce repeated user correction, failed generations, stale knowledge, workflow friction, and skill drift. It is not to produce activity logs or invent daily growth.

## Evidence Sources

Use the smallest relevant set:

1. User-confirmed corrections and recent inspected outputs.
2. `$creative-casebook` cases and retry deltas.
3. Capsule events, counterexamples, pending spores, and active capsules.
4. Recent custom-skill changes and validation results.
5. Sophia session state, memory index, commitments, and unresolved items.
6. Current official/primary web sources for selected stale or changing topics.

Do not claim access to conversation history that is not available to the current run. State which evidence was actually inspected.

## Cadence

Default:

- light audit twice per week;
- deeper architecture review monthly or after repeated user correction;
- immediate review after a serious failure, unsafe action, or major workflow redesign.

Do not change mechanisms merely because a scheduled run occurred.

## Workflow

1. Run `scripts/self_iteration_audit.py audit --record`.
2. Review findings by severity and evidence.
3. Inspect recent capsule events and repeated finding fingerprints.
4. Select at most three meaningful improvement targets.
5. For each target, identify:
   - symptom;
   - evidence;
   - user impact;
   - root cause;
   - smallest fix;
   - validation method;
   - rollback path.
6. Research current information only when:
   - a source is stale;
   - platform/model behavior may have changed;
   - an unfamiliar domain caused weak output;
   - a new technique could solve a documented gap.
7. Apply automatically only if the change is:
   - low-risk;
   - reversible;
   - within custom skill/reference files or non-destructive metadata;
   - supported by evidence;
   - testable now.
8. Do not automatically:
   - delete files or capsules;
   - change credentials or external accounts;
   - install software;
   - publish or message externally;
   - make broad persona/value changes;
   - rewrite many skills from one weak signal.
9. Validate:
   - run all custom-skill validators;
   - validate capsule database;
   - inspect modified files;
   - run relevant scripts or focused forward tests.
10. Record:
   - concrete results become a case card;
   - repeated validated lessons become capsule candidates;
   - architecture changes require user confirmation unless already covered by active policy.

Read `references/review-protocol.md` before a scheduled review.

## Deterministic Audit

```powershell
python scripts/self_iteration_audit.py audit --record
python scripts/self_iteration_audit.py history --limit 8
python scripts/self_iteration_audit.py recurring --minimum 2
```

The audit checks:

- skill structure and metadata;
- unresolved TODOs and duplicate headings;
- missing referenced files;
- oversized skill bodies;
- source-map dates;
- recent skill changes;
- capsule integrity and lifecycle signals;
- Sophia memory routing files;
- cold-start automation claims versus actual automation TOML files;
- cold-start skill inventory freshness after major custom-skill changes;
- prior recurring audit findings.

The script does not edit skills.

## Research Rotation

Do not scan the entire internet every run. Choose one lane tied to real work:

- AI video platform/model changes;
- audiovisual language and editing;
- film music and sound design;
- visual aesthetics and rendering;
- action/choreography;
- storytelling and short-form structure;
- reference/control workflows.

Use `$creative-research-first`. Report only developments that change an existing decision, prompt, skill, or capsule.

## Decision Rules

- **One isolated issue**: repair locally; do not generalize yet.
- **Same fingerprint twice**: investigate shared cause and consider a candidate capsule.
- **Same user correction across domains**: inspect bottom-layer or orchestration rules.
- **Stale source only**: refresh source notes; do not rewrite the workflow unless facts changed.
- **New technique with no demonstrated need**: save as a spore, not an active rule.
- **No meaningful issue**: record a clean audit and stop.

## Output Shape

```text
自检范围：
证据来源：

发现：
1. 问题 / 证据 / 影响 / 根因

本轮已改：
- 修改 / 验证 / 回滚

仅建议：
- 高风险或证据不足的方向

新东西：
- 变化 / 为什么相关 / 应更新哪里

胶囊处理：
- 新孢子 / 候选 / 反例 / 无

下一次重点：
```

## Guardrails

- Do not invent errors to justify an audit.
- Do not optimize for the number of changes.
- Do not treat self-reflection as evidence.
- Do not silently rewrite user-confirmed architecture.
- Do not promote web discoveries directly into active capsules.
- Do not repeatedly notify the user when nothing meaningful changed; provide a compact clean-audit summary.
- Do not use the cadence as permission for uncontrolled background behavior.
