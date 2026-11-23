---
name: prompt-contamination-guard
description: 提示词污染防护工具：清理图像和视频提示词中的上下文残留、否定联想、纠错痕迹、默认模板、内部术语和互相冲突的控制语句。用于正式生成前获得干净、单一目标的模型输入。
version: 1.0.0
---

# Prompt Contamination Guard

## Purpose

Treat a generation prompt as one weighted semantic field. Headings, paragraphs, and positive wording do not isolate concepts from one another.

This skill removes accidental associations and accidental weighting while preserving the user's current creative intent and every unique control needed by the active prompt.

## Ownership Boundary

This skill owns:

- contamination detection;
- source tracing for model-facing clauses;
- clean-slate reset;
- positive visible rewrites;
- cross-section semantic deduplication;
- final contamination PASS / FAIL.

This skill does not invent or redesign story, action, camera, character, material, sound, or VFX facts. Their domain owners decide those facts. This skill decides whether each approved fact is cleanly compiled and how often it appears.

Do not create a fixed blacklist from old failures. Reassess association risk from the current task, target model, supplied references, and prompt.

## Contamination Classes

### Old-context residue

A noun, prop, character, enemy, location, palette, power, transition, movement mode, or failure term came from an earlier project or attempt rather than the current task.

A positive stability sentence can still be contaminated when it names an old object merely to keep it absent.

### Correction and exclusion leakage

The prompt explains the unwanted result through wording such as `不要`, `别`, `不是`, `避免`, `不能`, `不再`, `no`, `not`, `without`, or `avoid`.

The unwanted noun remains semantically active even when the sentence rejects it.

### Default-template contamination

The prompt imports a habitual opening, room, floor, stage, fight route, camera orbit, transformation shell, environment, or ending that the user did not request.

A familiar template is contamination when it competes with the current scene or event, even if it produced good results previously.

### Loaded-label contamination

A role name, camera label, style label, action verb, or abstract intention carries a stronger familiar association than the intended visible result.

Examples include vague labels such as `压迫感`, `史诗感`, `处刑者`, `动态镜头`, `高速战斗`, or `次元斩` when the prompt relies on the label instead of defining the current visible evidence.

The label may remain as a short handle only after the visible meaning is owned elsewhere.

### Positive semantic over-weighting

Several positive clauses describe the same visible fact through different words. The repetition can make one effect, object, pose, camera behavior, or result persistent, oversized, or globally dominant.

Audit concepts rather than exact strings. For example:

- `断面 / 切面 / 裂面` may repeat one geometry;
- `刃线 / 主刃线 / 横向亮线` may repeat one path;
- `延迟展开 / 半拍后显现 / 随后错位` may repeat one lifecycle;
- `镜头环绕 / 摄影机转出 / 旋转跟随` may repeat one camera behavior.

### Internal-control leakage

The paste-ready prompt contains workflow language, agent notes, failure analysis, prompt strategy, reference IDs without roles, backstage codes, or conversation-dependent phrases such as `上一个`, `之前那版`, `本段`, or `继续保持`.

### Conflicting semantic anchors

Two clauses assign incompatible priorities to the same surface, such as restrained and explosive VFX, locked and freely changing camera, photoreal materials and flat graphic rendering, or a fixed scene and an unrelated default environment.

Resolve the conflict through the user's current priority and the appropriate domain owner; do not keep both as a compromise.

## Workflow

Run the following workflow in order.

### Establish current truth

Before editing, record only current sources:

```text
current user request
supplied references and their assigned roles
active project or continuity locks
current owner-approved story/action/camera/style/material/VFX/sound facts
explicitly approved reusable rules
```

Anything else requires a source trace or removal.

### Trace every suspicious clause

Use a compact backstage table:

```text
clause | source | current job | contamination class | keep / rewrite / delete
```

PASS sources are the current user request, supplied assets, active project truth, an active domain owner, or a user-approved reusable rule.

A clause does not become valid merely because it sounds professional or appears in an old successful prompt.

### Run the clean-slate reset

For a new concept, reconstruct the desired frame without contrasting it with an old frame:

- state the current subject and identity;
- state the current environment only when required;
- state the active prop or power ownership;
- state the current action path and result;
- state the current palette, material, light, and camera relation;
- retain only current, evidence-backed stability locks.

Delete old nouns rather than negating them.

### Rewrite risky labels as visible evidence

For each loaded or abstract word, ask:

```text
What would the lens or microphone actually record?
Which body, object, surface, direction, contact, displacement, light response, or sound proves it?
```

Replace the label with the smallest current observable clause that preserves the intended choice.

Examples:

```text
“不要出现火环”
-> “雷电紧贴武器与接触路径，命中后沿受体表面短促分叉并迅速熄灭”

“镜头更有压迫感”
-> “近侧肩背压入前景，目标被挤在纵深另一端，攻击路线持续朝镜头方向逼近”
```

Use examples as reasoning patterns, not reusable prompt text.

### Build the cross-section semantic ledger

For each hero mechanism, effect, transition, signature object, or special camera behavior, map:

```text
mechanism | appearance/material | trigger/source | path/contact | result | decay/endpoint | current risk lock | owner section
```

Each visible fact gets one authoritative occurrence.

Typical placement:

- visual/material section: appearance, medium, color, light, optical and surface behavior;
- camera section: only the camera's own response, continuity, or proof task;
- event section: indispensable trigger, progression, contact, result, and lifecycle;
- sound section: synchronized audible evidence;
- stability section: only a current drift risk not already controlled elsewhere.

A mechanism name may recur briefly as a handle. Its geometry, path, lifecycle, result, or endpoint may not be paraphrased across sections.

### Apply the deletion test

For every repeated-looking clause, ask:

```text
If this clause is removed, does any unique visible or audible generation choice disappear?
```

- If yes, keep it at its authoritative owner surface.
- If no, delete it as accidental semantic weight.
- If two clauses conflict, return the fact to its domain owner or retain the one matching the user's current priority.

Do not thin a prompt by deleting unique identity, material, camera, sound, continuity, or risk-control facts. Character count is not an omission reason.

### Run the stateless-generator read

Read the final prompt as if the generator knows nothing about the conversation.

Confirm:

- every reference has an explicit role;
- every pronoun or continuity phrase resolves inside the prompt;
- no old project noun survives without a current source;
- no unwanted object is named only to exclude it;
- no internal workflow or failure explanation remains;
- no habitual template competes with the current scene;
- no hero mechanism is accidentally re-weighted through synonyms;
- every surviving cross-section clause adds different information;
- current creative facts remain complete.

## Binary Gate

```text
PASS = every model-facing clause has a current source and unique job;
       exclusions have become positive current facts;
       each hero-mechanism fact has one authoritative occurrence;
       cross-section clauses add non-overlapping information;
       no unique owner control was lost during cleanup.

FAIL = an old or habitual concept remains active;
       the prompt explains the unwanted result;
       an abstract or loaded label substitutes for visible evidence;
       one shape, path, lifecycle, result, endpoint, pose, or camera behavior
       is repeated through synonyms and receives accidental global weight;
       cleanup removed a unique current control.
```

## Output Contract

When asked to audit only, return:

```text
Contamination findings:
- clause / semantic cluster
- contamination class
- source problem
- keep / rewrite / delete decision

Cross-section collisions:
- repeated fact
- current locations
- authoritative owner location

Verdict: PASS / FAIL
```

When asked to clean or rewrite, return:

1. a short diagnosis outside the paste target;
2. one clean, self-contained model-facing prompt;
3. no audit language inside the copyable prompt.

## Handoffs

- Receive approved facts from story, continuity, character, action, camera, style, material, VFX, sound, and platform owners.
- Return unresolved creative conflicts to the relevant owner instead of guessing.
- Hand the cleaned prompt to the platform compiler and final preflight.
- For generation results, compare the output against the semantic ledger before adding more wording; do not treat every failure as a request for more detail.
