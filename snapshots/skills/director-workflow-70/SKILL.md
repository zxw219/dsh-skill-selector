---
name: director-workflow-70
description: 导演工作流总控工具：组织一套覆盖研究、世界观、角色、视觉、分镜、动作、提示词、生成检查、复盘和资产管理的完整AI影视生产流程。用于大型或多环节AI视频项目的统一调度。
version: 1.0.0
---

# Director Workflow 70

## Operating Contract

Act as the single front door for this bundle. Select the smallest complete specialist stack; do not load all skills by default.

This is a portable profile. Use only skills physically included beside this Skill. If a bundled specialist mentions an unavailable optional handoff, keep its local method and omit that handoff. Do not install missing tools, invoke private memory, or invent machine-specific paths.

Keep backstage analysis compact. Deliver the artifact the user needs: a plan, shot structure, copyable prompt, review, or targeted rewrite.

## Phase 0: Read the Directorial Job

Before routing, lock five facts:

1. **Narrative job** — what changes for the audience during this clip.
2. **Primary visual job** — the one result that must read immediately.
3. **Current state** — character form, location, held assets, relative scale, and accepted prior endpoint.
4. **Movement geometry** — where bodies, camera, force, and effects travel in space.
5. **Delivery surface** — still image, storyboard, 5–15 second clip, connected sequence, Seedance, or 即梦 SD2.

Keep one primary goal and at most one supporting goal. Ask only when a missing answer would change the whole route.

## Mandatory Baseline

For every substantial moving-image task, cover these owners:

- audiovisual and shot logic: `$cinematic-audiovisual-language`;
- shot design and coverage: `$professional-storyboard-director`;
- material, light, grounding, and texture behavior: `$ai-material-realism`;
- sound events and mix hierarchy: `$cinematic-music-sound-design`;
- platform packaging: `$jimeng-sd2-prompting` or `$seedance-20`;
- final source-trace and prompt audit: `$ai-video-prompt-preflight`.

Add `$character-continuity-bible` when references, recurring characters, transformations, weapons, monsters, or multiple clips are involved.

## Routing Matrix

| Need | Route |
|---|---|
| Vague idea, story function, clip architecture | `$creative-anchor-director` -> `$video-structure-design` |
| Cultural grounding or unfamiliar reference | `$creative-research-first` -> `$reference-hunting-board` |
| Analyze a successful or failed reference clip | `$film-breakdown-distiller` |
| Story scene, dialogue, dramatic beat | `$screenwriting-story-craft` -> `$performance-scene-director` |
| Shot list, storyboard, camera coverage | `$shot-information-progression` -> `$master-shot-camera-planning` -> `$professional-storyboard-director` |
| Unconventional camera tension | `$cinema-language-atlas` -> `$high-tension-shot-design` |
| World, location, production design | `$production-design-worldbuilding` -> `$world-visual-development-director` -> `$mokeaigc-v9` when a world-image exploration layer is useful |
| Style, named anchors, medium grammar | `$visual-style-aesthetic-direction` -> `$visual-reference-vocabulary` -> `$aesthetic-style-intelligence` |
| Character/reference identity and sequence state | `$character-continuity-bible` -> `$entity-continuity-system` -> `$cross-shot-consistency-audit` |
| Explore variants without losing identity | `$invariant-exploration-director` -> `$bounded-explore-select` |
| Fight, weapon, pursuit, physical action | `$action-choreography-reference` -> `$action-rhythm-editing` -> `$seedance-fight-director` |
| Pure solo action showcase | add `$action-showcase-direction` |
| Transformation or mechanical reconfiguration | `$mechanical-transformation-design` |
| VFX, magic, impact, destruction, transformation FX | `$cinematic-vfx-director` -> `$vfx-effect-construction-engine` -> bundled `$seedance-vfx` for Seedance wording |
| Music, SFX, silence, rhythm sync | `$cinematic-music-sound-design` -> bundled `$seedance-audio` |
| Prompt compilation for 即梦 SD2 | `$jimeng-sd2-prompting` |
| Prompt compilation for Seedance | `$seedance-20` plus only the needed bundled subskills |
| Review generated output | `$ai-video-output-review` -> `$ai-video-iteration-doctor` |
| Decide text vs image/video/constraint evidence | `$constraint-input-router` |
| Calibrate a visual direction before generation | `$minimum-visual-bible` -> `$visual-calibration-loop` |

## Core Pipelines

### A. Single Prompt

```text
Phase 0 intent -> continuity locks -> visual/material master -> camera master ->
event beats -> sound -> positive stability locks -> platform compiler -> preflight
```

### B. Action / Fight

```text
role and force asymmetry -> distance and line -> attack/defense response ->
position change -> rhythm escalation -> camera proof -> environment response ->
VFX support -> sound transient/tail -> platform compiler -> preflight
```

Do not let style, blur, or VFX hide missing contact or receiver response. Every exchange must alter posture, distance, support, weapon line, injury/state, or environment.

### C. VFX

```text
effect job -> source/owner -> trigger/formation -> material and shape ->
path/spatial layer -> contact/operation -> receiver/environment response ->
peak -> decay/residue -> sound sync -> platform compression
```

Use one dominant effect family per beat. Effects need a visible origin, route, result, and endpoint.

### D. Connected Sequence

```text
sequence objective -> ordered major beats -> accepted observed endpoint ->
current clip job -> current clip endpoint -> continuity audit -> next clip
```

Accepted footage overrides the plan. Do not replay completed beats or leak future beats early. When exact terminal frames differ, bridge with a new functional shot scale or motivated transition rather than pretending to reproduce the old frame.

### E. Review and Rewrite

```text
inspect actual output -> preserve successful layers -> identify the mechanism-level failure ->
change the smallest responsible layer -> rerun preflight
```

Do not convert one surface symptom into a universal blacklist.

## Prompt Delivery Contract

For a complete copyable AI-video prompt, use this order unless the user explicitly requests another format:

```text
角色/资产锁定
视觉材质总控
镜头语言总控
事件节拍
声音
正向稳定约束
```

Rules:

- The copyable block contains only current positive facts: what exists, moves, sounds, and remains stable.
- Every concrete noun, style anchor, prop, ability, transition, sound, and camera routine must trace to current instructions, inspected references, accepted continuity, or an approved reusable rule.
- Put platform parameters outside the prompt when the user sets them in the interface.
- Use `{{Image 1}}`, `{{Video 1}}`, and `{{Audio 1}}` for reference mapping.
- Material and camera layers are mandatory but concise. Events inherit them instead of repeating them.
- Negative diagnostics, old failures, and backstage reasoning stay outside the paste-ready block.

## Quality Gates

Before delivery, verify:

1. current scene and movement path are not contaminated by an older template;
2. identity, form, weapon, scale, and reference roles are explicit enough for the task;
3. each shot adds information, proves contact, proves movement, reveals state, or hands off the next beat;
4. camera position, height, scale, path, and cut trigger are not merely style labels;
5. feet, support, center of mass, cloth drag, weapon mass, recoil, and braking match the action;
6. VFX has source, path, interaction, environment response, decay, and endpoint;
7. material language describes actual surface behavior, controlled highlights, AO/contact occlusion, and stable texture density;
8. sound identifies onset, transient, resonance, space, tail, and silence where relevant;
9. the final prompt has one primary goal and no mutually competing hero events;
10. `$ai-video-prompt-preflight` passes before delivery.

## Stop Rule

Stop when the requested production artifact is complete and audited. Do not expand into generation, browser operation, local archive automation, Blender, mocap, editing, or long-term memory unless the host system provides those abilities and the user explicitly asks for them.


