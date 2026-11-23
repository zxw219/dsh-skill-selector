---
name: global-skill-evolution
description: 全局Skill进化系统：通过证据发现、根因诊断、方案合成、对比评估、可回滚升级和治理记录，持续改善整个Skill体系。用于技能栈巡检、合并、修复与版本迭代。
version: 1.0.0
---

# Global Skill Evolution

Improve the skill system only when evidence shows a real workflow gain. Do not equate evolution with more files, longer instructions, or constant modification.

## Governing Objective

Optimize for:

- fewer repeated user corrections;
- clearer triggers and routing;
- more executable workflows;
- stronger validation and regression control;
- better cross-task reuse;
- lower maintenance cost without sacrificing capability.

Anti-bloat is a tool, not the mission.

## Core Loop

```text
discover -> diagnose -> synthesize -> validate -> ratchet -> propagate
```

Read [governance-loop.md](references/governance-loop.md) for the detailed loop.

### 1. Discover

Accept concrete signals:

- direct user correction;
- repeated failure fingerprint;
- inspected success worth reusing;
- duplicated, stale, broken, or weakly triggered skill logic;
- relevant external method that can be adapted;
- audit finding with inspectable evidence.

### 2. Diagnose

Classify the real level before editing:

1. local wording or metadata;
2. missing workflow step or guardrail;
3. routing or orchestration conflict;
4. reusable cross-skill rule;
5. stable global operating policy;
6. weak evidence — no change.

Name the mechanism, not only the symptom.

### 3. Synthesize — Nuwa Lane

Distill the smallest reusable mechanism. Merge into an existing owner when possible. Preserve important tensions such as concise-but-complete and proactive-but-reversible.

Read [nuwa-distillation-lanes.md](references/nuwa-distillation-lanes.md) before adapting an outside method or restructuring multiple skills.

### 4. Validate — Darwin Lane

For meaningful changes:

- compare old and new behavior;
- check trigger, scope, executionability, honesty, anti-bloat, and runtime neutrality;
- run structural validation and relevant scripts;
- forward-test independently when the change is complex or high-impact;
- reject changes that merely sound smarter.

Read [adapted-darwin-rubric.md](references/adapted-darwin-rubric.md).

### 5. Ratchet

Keep the change only when evidence supports a workflow improvement. Revert or narrow it when the improvement is cosmetic, unverified, or creates a larger control surface.

### 6. Propagate

Route the result to the smallest correct durable layer:

- local skill edit;
- reference file;
- new skill;
- capsule;
- orchestrator/global policy;
- audit backlog;
- nowhere.

Read [promotion-routing.md](references/promotion-routing.md). Conversation summaries are not durable propagation.

## Audit Workflow

Use `scripts/skill_evolution_audit.py` for a deterministic structural and evidence pass.

```powershell
python scripts/skill_evolution_audit.py audit
python scripts/skill_evolution_audit.py audit --record
python scripts/skill_evolution_audit.py history --limit 10
python scripts/skill_evolution_audit.py recurring --minimum 2
```

Portable environment variables:

```text
CODEX_HOME          default: ~/.codex
SKILLS_ROOT         default: $CODEX_HOME/skills
AUTOMATIONS_ROOT    default: $CODEX_HOME/automations
EVOLUTION_STATE_ROOT default: $CODEX_HOME/global-skill-evolution
CAPSULE_DB          default: $EVOLUTION_STATE_ROOT/evolution.sqlite
```

The audit checks:

- required `SKILL.md` files and frontmatter;
- name/folder alignment;
- duplicate skill names and duplicate headings;
- missing local references/scripts/assets;
- stale source dates and oversized skill surfaces;
- capsule database integrity and unconsumed evidence;
- automation metadata and optional state-file drift;
- recurring finding fingerprints.

Read [review-protocol.md](references/review-protocol.md) before deciding whether an audit finding justifies a change.

## Capsule Workflow

Use `scripts/capsule_engine.py` to store reusable rules without turning memory into a diary.

```powershell
python scripts/capsule_engine.py init
python scripts/capsule_engine.py stats
python scripts/capsule_engine.py create ...
python scripts/capsule_engine.py record --id CAPSULE_ID --outcome success ...
python scripts/capsule_engine.py activate --id CAPSULE_ID --target-skill target-skill
python scripts/capsule_engine.py validate
```

Lifecycle:

```text
candidate -> provisional -> validated -> active -> deprecated -> archived
```

An explicit user-confirmed architecture policy may activate early only when it is marked as a policy decision, has clear boundaries, and has high evidence confidence. Empirical claims still require real applications.

Read [capsule-architecture.md](references/capsule-architecture.md) and [capsule-schema.md](references/capsule-schema.md).

## Recurring Automation

Use [automation-setup.md](references/automation-setup.md) and load [automation-prompt.txt](assets/automation-prompt.txt) when creating the recurring task through the Codex automation tool.

Recommended cadence: twice weekly. Each run should:

1. inspect recent changes and user corrections;
2. run the deterministic audit;
3. choose at most one or two high-value targets;
4. auto-apply only low-risk, reversible, immediately verifiable edits;
5. record keep/revert decisions and pending recommendations;
6. finish with a concise report.

A clean audit is a valid outcome.

## Change Gate

Automatic edits are allowed only when all are true:

- evidence is named;
- scope is small;
- action is reversible;
- validation is available now;
- no destructive, public, paid, credentialed, or account-bound side effect occurs;
- the edit does not override a user-confirmed value or project decision.

Otherwise report a recommendation and stop.

## Validation Gates

1. **Trigger integrity** — description says what and when.
2. **Scope control** — one coherent owner per workflow.
3. **Executionability** — another Codex instance can act without hidden thread context.
4. **Honesty** — limitations and dependencies remain explicit.
5. **Anti-bloat** — every added rule changes behavior.
6. **Runtime neutrality** — paths and tools are portable or configurable.
7. **Propagation fit** — durable knowledge reaches the correct layer.
8. **Keep/revert rule** — define what evidence will retain or reverse the change.

## Guardrails

- Do not create a rule from one ambiguous result.
- Do not let the change author be the only evaluator for high-impact changes.
- Do not create a new skill to avoid fixing an existing owner.
- Do not promote thread summaries as durable memory.
- Do not install tools, publish content, use credentials, or change live systems during an audit.
- Do not modify merely because the automation ran.
- Do not delete evidence history; deprecate or supersede it.
- Do not store secrets or private assets in audit logs or capsules.

## Output Contract

```text
Evidence:
Finding:
Action class:
Smallest safe change:
Validation:
Keep / revert rule:
Propagation target:
Pending recommendation:
```

Keep the user-facing report concise. Detailed evidence belongs in the audit database or project state file.
