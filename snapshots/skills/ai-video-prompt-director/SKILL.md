---
name: ai-video-prompt-director
description: AI视频提示词导演工具：以研究、结构、剧作、镜头、表演、动作、声音和生成约束为一体，组织完整的电影化视频提示词工作流。用于导演模式、片场模式或复杂AI视频提示词制作。
version: 1.0.0
---

# Portable Profile Note

When installed from `director-workflow-portable-70`, route through `$director-workflow-70` and use only bundled skills. Missing private-memory, automation, tool-control, or archive handoffs are optional and must not block prompt work.


# AI Video Prompt Director

## Bottom-Layer Reasoning

Apply the `think-one-step-further` mechanism as a lightweight check:

- Confirm this skill is solving the user's real intent, not only the surface request.
- Make the output immediately usable and name any unavoidable next action.
- Extract the reusable structure and, when aligned, propagate it to adjacent prompts, skills, checklists, or workflows.
- Add one guardrail for the most likely next failure while preserving this skill's primary workflow.

## Core Intent

Use this as the top-level orchestration skill for the user's AI video work. It routes a loose idea through the right specialist skills and returns one coherent prompt package.

Do not merge every specialist into every answer. Choose only the useful layers for the current shot.

Default task-card orchestration policy: for Liu's AI-video and creative production tasks, do not jump straight to prompt writing or run every specialist. Use the fixed flow: task-stage diagnosis -> global bible / continuity locks -> director breakdown / shot function -> Task Cards assigned by concrete shot problem -> only-needed specialist work -> specialist result package plus `state_patch_request` -> script-supervisor/orchestrator state arbitration -> platform compiler packaging -> QC -> targeted redispatch on failure -> ledger/case/capsule preservation when useful. Keep Task Cards backstage unless Liu asks to see the production-management view.

Prompt delivery hard gate, user-corrected 2026-07-09 and superseded by positive-only update: the task-card workflow and anti-contamination rules are not optional reminders. Before delivering any copyable AI-video / SD2 / Seedance prompt, stop and verify the final paste-ready block follows Liu's fixed six-part order unless Liu explicitly asks otherwise:

```text
角色/资产锁定
视觉材质总控
镜头语言总控
事件节拍
声音
正向稳定约束
```

Paste-ready prompt policy: the model-ready code block is positive-only. It states only what is present, visible, audible, active, and locked in the current shot. Exclusion, absence, correction, comparison to old attempts, and previous-failure wording stay outside the copyable block. If a risk must be controlled, translate it into a positive present-state lock before delivery. The former exclusion slot is now 正向稳定约束; it must contain only positive continuity/stability locks such as subject identity, lens attention, scene relationship, color ownership, material response, and readable action path.

Source-trace gate: every concrete phrase, including existing subjects, props, locations, palettes, camera routines, transitions, powers, sounds, and stability locks, must trace to Liu's current instruction, a supplied/inspected asset, the active global bible/continuity lock, or a user-approved reusable rule. If the trace fails, omit the phrase from the paste-ready prompt or move it outside as a question/assumption. Named-anchor gate: Name-style anchors mean director, cinematographer, photographer, production designer, animation director, manga artist, studio, film title, game title, or art/design reference names. `镜头语言总控` selects a compact compatible name-style camera-anchor set for substantial camera-sensitive prompts; bounded camera grammar supports those anchors and never replaces them. These anchors own composition, blocking, lens feeling, camera motion, edit rhythm, shot scale, and reveal logic. `视觉材质总控` always carries concrete material/light/color/render controls, while its name-style anchors are conditional. Use visual-material name anchors when material, light, color, render finish, production-design surface, or atmosphere is a decisive creative variable, the source lacks clear material identity, or Liu requests named aesthetic references. When the material direction is already clear, neutral, reference-driven, prompt-budget constrained, or contamination-prone, write direct visible material behavior without a visual-material name anchor. Use 2-4 compatible anchors total when anchors are useful. In the paste-ready prompt, write each used anchor as `[Name/Work/Studio]风格 + [concrete positive visible material/camera result]`; keep role-assignment wording backstage and do not use duty verbs such as `负责` inside the copyable block. Technical camera/material terms support the style-result phrase. The copyable block must not contain workflow notes, old-project context, conversation-dependent wording, template residue, or agent-only diagnostics. If the six-part order, positive-only gate, or traceability check fails, do not send the prompt; rewrite first.

Assume `$sophia-mode` is already active as the global operating layer. This skill is the full creative/video director workflow under Sophia, not a separate persona. Use Sophia's database routing: ledger for exact attempts, casebook for inspected generation lessons, capsule-engine for reusable validated mechanisms, and memory for stable preferences or commitments.

Liu should be able to speak naturally, without naming modes, phases, or skills. Phrases such as “想做个更狠的打斗”, “这个感觉不对”, “帮我弄得高级一点”, “下一段来个情绪爆发”, or “这个想法能不能做成片” are sufficient instructions. Infer intent, choose the front-stage mode, select backstage skills, and output the useful result. Do not ask Liu which skill to use unless two materially different deliverables would be equally plausible.

## Phase 0: Creative Intent Reading

Before research, structure, or prompt writing, automatically run a short internal thinking stage to infer what Liu is really trying to get, including what is not explicitly said.

This is a creative taste inference, not a psychological diagnosis. Ground it in Liu's wording, supplied references, current project state, previous corrections visible in context, and the user-calibrated lessons.

Do not wait for Liu to say “意图判断”, “第 0 阶段”, “潜意识”, or “导演模式”. Natural language is the trigger. Treat vague wording as signal: infer the creative pressure behind it, then either execute directly or present 2-3 routes when the choice changes the whole piece.

Ask internally:

```text
1. Surface request: what did Liu literally ask for?
2. Hidden desire: what feeling, status, pleasure, irritation, or creative itch is probably behind it?
3. Taste fit: which direction matches Liu's recurring preferences for cinematic force, readable motion, high material truth, strong visual hierarchy, cultural/design sedimentation, and controlled iteration?
4. Bad-fit directions: what would likely feel generic, cheap, over-explained, too static, too soft, too pretty, or off-brand for Liu?
5. Best route: should this become a fight prompt, emotion scene, world board, style direction, diagnostic pass, or a set of 2-3 options?
6. Confidence: am I confident enough to execute directly, or should I show two route options first?
```

Use the result to choose the route. Do not expose a long chain-of-thought. By default, keep this reasoning backstage. Show a compact `意图判断` block only when it helps Liu understand a route choice, when the request is broad, or when Liu asks why:

```text
意图判断：你表面上是在要 X，但真正想要的更像 Y。
适合你的方向：A，因为它更符合你的“强视觉母版 + 可生成动作/情绪 + 不廉价”的偏好。
我会避开：B/C，因为它们容易变成泛泛酷炫、静态摆拍或 AI 味。
```

Default behavior:

### Template Contamination Check

Before adding any familiar scene, transformation, opening, transition, floor, lighting setup, or camera routine, verify it was requested by Liu or directly required by the current segment. The user's explicit scene, movement goal, active form/state, and handoff state outrank all reusable templates.

Core failure to prevent: importing an old/default prompt template into a new task and letting it override the current scene or motion. Record and fix this as a priority/order error, not as isolated symptoms such as a wrong floor, wrong background, or static pose.

Run three checks before final wording:

```text
1. Current scene: where is this happening now?
2. Current movement: what is the subject doing through space?
3. Handoff state: what state must the final frame naturally prepare for?
```

If a phrase does not serve one of those three answers, remove it or rewrite it. Treat this as a hard block: remove the contaminated phrase at the source; a later stability line cannot cancel a wrong positive association already fed into the model.
- If Liu says “整 / 直接 / 来吧”, infer and execute; do not stop for questions.
- If Liu gives only a natural-language desire, still infer and execute; do not ask him to choose a skill, workflow, or phase.
- If the request is broad and taste-defining, give 2-3 route options with one recommended route.
- If Liu sounds dissatisfied but the failure evidence is missing, ask for or inspect the generated output before rewriting the full prompt.
- If the inferred direction conflicts with Liu's explicit instruction, obey the explicit instruction and mention the tradeoff briefly.

## Non-Self-Deception Gate

Apply this gate before final creative decisions, reference transfer, diagnosis, and paste-ready prompts.

Core rule: do not pretend to know, see, remember, verify, or infer something that is not actually grounded in available evidence.

Separate internally:

```text
Confirmed: directly visible in the user message, supplied asset, inspected file/video, validated skill, or cited source.
Inferred: reasonable creative inference from confirmed evidence and Liu's known workflow.
Assumed: low-risk default chosen to keep work moving.
Unknown: missing information that could materially change the result.
```

Ask Liu directly when an unknown affects the core output. Do not hide a material unknown inside a confident prompt.

Ask instead of guessing when:

- the target model, duration, format, or reference role changes how the prompt must be written;
- a referenced image/video/link/file has not actually been inspected;
- the user asks to follow “that article / that video / this reference” but the transferable mechanism is unclear;
- identity, outfit, weapon, scene, or continuity locks depend on missing assets;
- the user asks for a diagnosis but the generated output has not been seen;
- current platform/model facts, prices, rules, dates, or external facts matter and have not been verified;
- two creative directions would lead to substantially different pieces and Liu has not signaled a preference.

Do not ask for tiny details that can be safely assumed. If uncertainty is low-risk, state the assumption briefly or keep it internal and continue. If uncertainty is high-impact, stop and ask 1-3 concise questions before producing the final prompt.

New Liu workflow extensions:

- Use `$mokeaigc-v9` as an upstream 9-still visual-world board when the user wants to展开世界, infer the world behind a reference image, or establish a coherent visual culture before story/video packaging.
- Use `$performance-scene-director` as the shared acting-performance base when actor emotion, micro-expression, and performance rhythm are the main value of the clip; choose exactly one emotion profile via `$anger-scene-director`, `$crying-scene-director`, `$sorrow-scene-director`, `$joy-scene-director`, or `$delight-scene-director` as a lightweight trigger.

## Organic Skill Linkage Protocol

When writing Liu's AI-video prompts, do not use specialist skills as separate checklist blocks that compete for control. Treat them as a staged pipeline with one owner per layer:

Conflict guardrail: if two skills could control the same sentence, choose one owner and demote the other to a constraint note. Never paste two specialist styles, two camera plans, two action plans, or two platform packaging formats into the same final prompt.

For recurring projects or high-risk production decisions, read `$director-workflow-70`'s bridge file at `director-workflow-70/references/capability-map.md`. Use its North Star, Bible, entity, invariant, constraint, selection, audit, and Agent-governance methods as upstream decision layers only when they change the route. When a project or inspected external production package exposes stable project controls plus shot-specific prompts, also read `references/project-prompt-inheritance.md` and compile project invariants -> shot binding -> shot delta. Never paste governance documents, a whole screenplay/bible, or an imported mega-prompt into the model-ready prompt.

0. **intent owner**: this skill's Phase 0 reads the real creative desire, hidden taste pressure, best-fit direction, and what to avoid before selecting the stack.
1. **segment objective owner**: `$video-structure-design` defines the one main event for the 15-second segment and whether the segment is story, PV, chase, fight, transformation, reveal, or usable insert material.
2. **reference / continuity owner**: `$character-continuity-bible` and SD2 reference-role rules lock who, what prop/monster, which environment, and what previous story state is active.
3. **audiovisual owner**: `$cinematic-audiovisual-language` defines shot function, first visible state, screen direction, geography, camera tracking owner, and cut/transition reasons.
4. **aesthetic owner**: `$visual-style-aesthetic-direction`, `$cinema-language-atlas`, or `$creative-anchor-director` defines medium, style family, named anchors, color ownership, and presentation bias.
5. **action owner**: `$action-choreography-reference` defines movement grammar, power relation, contact/near-miss, receiver response, route/topology, and end state. For Seedance/Higgsfield fight prompts, use `$seedance-fight-director` as the fused application layer after the physical action basis is clear; it combines choreography, rhythm, camera contract, material/reference locks, and retry notes into one paste-ready fight prompt.
6. **rhythm owner**: `$action-rhythm-editing` defines setup/build/turn/impact/recovery emphasis, but does not force unsupported micro-timings.
6A. **reference-audio timing owner**: before delivering a final video prompt, `$seedance-audio` runs its prompt-time Reference Audio Gate. When the clip benefits from audio conditioning, it turns the approved beat map into a local SFX/music/hybrid control WAV and returns the real path/hash/cue map together with the prompt. The workbench button is only a manual editor/fallback; Liu should not have to build the track separately.
7. **material owner**: `$ai-material-realism` adds only the material, light, optical, motion-blur, and anti-artifact controls needed for the current surfaces.
7A. **VFX owner**: `$cinematic-vfx-director` converts approved action, state, threat, transformation, or destruction into a medium-aware effect card: function, primary read, source/owner, path, collision, receiver/environment response, motion-effect family, intensity grade, light integration, decay, and sound sync. `$vfx-effect-construction-engine` then resolves the visible lifecycle and a small set of job-assigned effect atoms when needed. For Seedance, `$seedance-vfx` compiles the approved construction; it does not invent a second effect design.
8. **platform / positive-stability owner**: `$jimeng-sd2-prompting` packages the final prompt in Liu's copyable order and owns video-specific positive stability locks: positive visible locks only in the paste-ready block, with risk/exclusion notes kept backstage and no old-project contamination.
9. **risk owner**: `$ai-video-prompt-preflight` removes contradictions, overload, missing reference roles, vague camera language, generic exclusion spam, and unsupported exact timing.
10. **generation archive owner**: when an image or video is actually generated, `$generation-asset-pipeline` creates the ticket before submission and binds the exact final prompt, model/settings, output file, SHA-256, adjacent prompt/meta sidecars, and project ledger after completion. It never changes the creative prompt or replaces `$creative-production-ledger`; bridge both through one attempt/ticket identity.

## Stack Size Rules

Use only the minimum useful stack:

- **Simple final prompt**: director + mandatory film baseline (audiovisual grammar, internal beat/shot plan, material, positive video stability locks) + platform packaging + preflight.
- **Emotion-led clip**: structure + `performance-scene-director` + one emotion wrapper + audiovisual + platform.
- **Fight/action clip**: structure + choreography basis + `cinematic-vfx-director` only when effects carry force/state/destruction + `vfx-effect-construction-engine` only when lifecycle or vocabulary construction is unresolved + `seedance-fight-director` when final target is Seedance/Higgsfield + material + platform.
- **World/style-heavy clip**: worldbuilding/reference + audiovisual + one style owner + material + platform.
- **After failed generation**: output review + one diagnosis layer + iteration doctor + platform retry. Do not change action, style, camera, character, and material all at once.

If the stack exceeds six active skills, write a one-line route map first and drop any layer that does not change the final decision.

Before final wording, run an integration pass:

- If two skills both try to control the same thing, choose one owner and demote the other to a short support phrase.
- If a 15-second prompt contains more than one main event, split it or reduce to a looser素材段.
- If the prompt is meant to generate剪辑素材, optimize for 2-4 strong usable shots rather than a complete finished mini-film.
- If the prompt is a video prompt, do not stop at fixed compositions or shot-size labels. Each major beat must define camera tracking owner, camera path, movement motivation, and the visible state change the move reveals.
- Keep `镜头语言总控` as the owner of the default camera identity, but instantiate every output-critical coverage change inside `事件节拍`. If a close-up, insert, wide proof shot, POV, or scale jump is necessary for the event to read, write a concise local `切镜触发 + 新景别/机位 + 证明任务 + 连续性承接`; a master-only promise such as `穿插特写`, `多景别`, or `快速切镜` is not enough.
- If storyboards were used only for ideation, transfer 2-3 selected mechanisms or frames, not the whole board.
- If the user's recent feedback rejects a workflow choice such as storyboards, do not force a visible/full storyboard; keep only minimal internal beat logic or skip it for tiny non-storyboard rewrites unless they ask again.
- When VFX is active, integrate it into Liu's existing six-part prompt instead of creating a seventh generic effects section: medium/color/light hierarchy in `视觉材质总控`, camera/effect coupling in `镜头语言总控`, lifecycle in `事件节拍`, sync in `声音`, and current-shot positive identity/ownership locks in `正向稳定约束`.

## User-Calibrated Reference Routing

Read `references/user-calibrated-ai-video-lessons.md` when the user asks to summarize past AI-video work, update or optimize the skill suite, create a new prompt in the user's recurring workflow, compare generated outputs, or diagnose repeated failures in action, character PV, camera, aesthetics, material quality, timing, prompt contamination, or copyable SD2/Seedance packaging.

Read it together with `references/orchestration-playbook.md` for substantial AI-video prompt work. The playbook gives the generic pipeline; the user-calibrated lessons give the current working taste, failure patterns, and output contract.

For any substantial film / AI-video / storyboard / action / prompt / review task, route through `$director-workflow-70` and the canonical mandatory film stack at `director-workflow-70/references/mandatory-stack.md` before finalizing the stack. This makes the baseline layers non-optional: audiovisual grammar, professional storyboard/shot planning, material realism, positive video stability locks, preflight, and the relevant action/sound/continuity/evidence layers.

## User Workflow Defaults

- Keep Sophia mode and lightweight director-mode posture globally active: do not ask the user to "turn on director mode"; perform the intent read and route silently. Load this full skill only for creative/video/prompt work.
- Default to 即梦 SD2 / Seedance-ready packaging when the user asks for a final video prompt and no target model is named.
- When the target is specifically Seedance 2.0, route the final packaging, continuation/extend logic, reference-role transfer, platform/API facts, safety rewrites, and failed-output repair through `$seedance-20` after the director-mode creative stack has set structure, world, camera, action, sound, and material controls.
- When Liu gives a world seed, place, culture, creature ecology, or reference image and wants a coherent visual world, route through `$mokeaigc-v9` before production design; distill its nine stills into stable visual laws instead of pasting all prompts into a video prompt.
- For a recurring multi-shot project, or when Liu provides a public production package with project-wide style/constraint blocks and per-shot prompts, use `references/project-prompt-inheritance.md`: retain approved project invariants, bind the current shot's entities/references, add only the shot delta, then compile into Liu's six-part positive-only format.
- When the prompt is emotion-led, route through `$performance-scene-director` first, then choose one profile wrapper: `$anger-scene-director` for anger, `$crying-scene-director` for visible tears/release, `$sorrow-scene-director` for restrained sadness, `$joy-scene-director` for inner joy/surprise, or `$delight-scene-director` for playful external fun.
- Separate planning order from final prompt order. Plan structure and causality first, but place the global visual master block near the beginning of the final generation prompt, before detailed shots. Treat medium, aesthetic family, palette ownership, shape/line language, material-light system, rendering hierarchy, and forbidden drift as upstream controls that every later shot must inherit.
- For high-speed combat, chases, giant/mecha action, aggressive POV, extreme shot-scale contrast, or unconventional camera requests, use `$kinetic-action-visual-master` to turn the aesthetic direction into a bounded whole-film kinetic envelope. Break framing conventions without breaking axis, geography, target relation, or action causality.
- Separate segment timing from individual shot timing. Exact segment ranges can improve generation by allocating screen time among setup, build, turn, climax, and recovery when those ranges are supported by a reviewed reference, previous successful output, animatic/edit map, or a credible physical action budget. Keep the internal shots inside each segment flexible unless a specific shot must synchronize to music, dialogue, first/last frames, or an edit point.
- For substantial video prompts, define the complete whole-film camera identity in `镜头语言总控`: named style anchors, perspective system, lens family, distortion, movement energy, framing/edit rhythm, transition language, and reveal logic. Example: `扳机社动画美学 + 极端透视与高能构图；金田透视法 + 近大远小的夸张纵深；FPV超广角 + 贴近动作路线的高速穿行；强桶形畸变 + 边缘外弯的速度压力`. `事件节拍` inherits that master and normally writes action, state change, contact, consequence, and handoff only. Add a local camera clause only for a genuine special-camera need, with its action/impact/occlusion trigger and concrete visible result; keep it compatible with the master.
- Use a timing-confidence gate: high confidence -> write exact segment ranges; medium confidence -> use approximate ranges or broad proportions; low confidence -> omit segment times and use causal order only. Never invent precise seconds merely to make the prompt look directed.
- For pure weapon action, armor-function, transformation, movement-system, or character-ability showcases with no required opponent, route through `$action-showcase-direction` after the macro duration structure and before detailed shot, physics, rhythm, effects, and model packaging.
- For action-led clips, do not default to opening with characters standing still, facing off, posing, or slowly preparing. Unless the user wants a ritual standoff, open in motion, pressure, aftermath, near-contact, chase-in, or environmental consequence so the first second already carries force.
- When providing a paste-ready prompt, append positive stability locks inside the same prompt block after the positive instructions so the user can copy it once.
- Liu's default copyable AI-video prompt budget is flexible up to roughly 3000 Chinese characters. Do not force a substantial prompt toward 1000 characters unless Liu explicitly requests a short test. Let event complexity determine length; preserve the six-part control structure, minimum world identity, action path, coverage-critical cuts, material/light behavior, sound intent, and current-risk stability locks. Compression removes repetition and low-value wording, not necessary control layers. Do not pad a simple prompt merely to approach the limit.
- When the user supplies video exclusions or an avoid list, use `$jimeng-sd2-prompting` plus `$ai-video-prompt-preflight` to translate each valid current risk into a positive present-state lock. Keep exclusion wording, correction language, and old-project failure terms outside Liu's paste-ready block. Do not load the image-generation cleanup series for video work; that series is for AI image, IM2/GPT Image 2, keyframe, or reference-still generation.
- For Liu's current paste-ready format, use `{{Image 1}}`, `{{Video 1}}`, and `{{Audio 1}}` as asset handles. On first mention, immediately add the assigned role in Chinese parentheses, e.g. `{{Image 1}}（角色身份、外观、服装与武器参考）`, `{{Video 1}}（动作、节奏与运镜参考）`, or `{{Audio 1}}（音乐节拍与声音参考）`. Do not replace these handles with `参考图1`, `图1`, `第一张图`, bare `image1`, `@Image1`, `@Video1`, `@material[...]`, or pseudo-layer tags in the final prompt. Platform docs may mention @-style handles, but Liu's deliverable format is the exact `{{...}}` format.
- When a whitebox/previs/mocap render is supplied as `{{Video 1}}`, treat it as motion and camera evidence only: transfer action rhythm, body weight, camera distance, shot-scale changes, cut triggers, and continuity logic; do not transfer capsule/body material, grey viewport look, grid floor, labels, debug markers, preview lighting, or placeholder scene design.
- For reference-video prompts based on a whitebox or mocap preview, route through `$mocap-action-previs` to respect the source motion evidence and `$action-rhythm-editing` when timing, impact, cut rhythm, or continuity between action beats matters. Then package through `$jimeng-sd2-prompting` and check with `$ai-video-prompt-preflight`.
- If the answer includes planning, asset maps, or preflight notes, keep them outside the paste target. Put only the model-ready prompt in one standalone `完整可复制提示词` code block, with positive stability locks inside that same block.
- For clean-slate new concepts or tests, do not mention old project-specific characters, locations, props, enemies, palettes, or failure cases in the new prompt or positive stability locks. Carry forward only reusable positive rules, such as stable subject count, localized color ownership, readable contact, and active camera-coupled motion.
- Before writing a new prompt, choose the clip mode explicitly: character PV, pure action showcase, fight/duel, story beat, product/prop reveal, or image-only character design. The mode controls the ratio of identity, expression, action density, camera, and final hold. Do not let a character PV collapse into continuous action, and do not let an action showcase collapse into portrait posing.
- Run a prompt-contamination check for new concepts: remove old project-specific props, motion modes, locations, colors, enemies, powers, and negative examples unless the user deliberately reuses them. Preserve only general controls such as single-subject lock, no weapon morph, no early terminal pose, readable contact, and no extra characters.
- When the user says they want to test action, reduce worldbuilding and lore to the minimum needed for staging. Put most prompt weight on action grammar, start state, movement path, contact/near-miss, reaction, displacement, recovery, camera readability, and the one variable being tested. `Minimum` still requires a world-identity packet when no environment reference carries the approved location: world scale/function, palette and light state, 2-4 silhouette/architecture invariants, density/atmosphere state, and the project's distinctive anomaly or environmental signature. Do not compress an approved original world into a generic noun such as `夜城`, `古城屋顶`, `森林`, or `大殿`.
- For substantive new creative prompts, run `$creative-research-first` before ideation and prompt assembly. Inspect supplied assets first, then browse unresolved domain, reference, and current-platform questions. Skip only for tiny rewrites, complete user-supplied transformations, explicit no-browse requests, or unavailable internet.
- For original characters, costumes, weapons, creatures, factions, worlds, visual masters, action systems, and character PV/action prompts, include a cultural/design sedimentation pass by default. Research culture, craft, object lineage, material process, profession/social use, movement source, and aesthetic precedent, then translate only the useful mechanisms into design and prompt controls. Do not deliver a merely pretty but culturally thin prompt, and do not paste surface symbols as a shortcut.
- When the user supplies reference videos/links or says "拉片", "整个都看", "你看看这个", first route through `$reference-hunting-board` and `$cinematic-audiovisual-language` to classify the whole reference: aesthetic system, scene design, camera grammar, action grammar, editing rhythm, transitions/VFX, sound, prompt structure, transferable mechanisms, and non-transferable risks. Do not jump directly to a new prompt from a few attractive moments.
- When a project has repeated failures in action, camera, or aesthetic quality, pause full-prompt rewriting until `$ai-video-output-review`, `$ai-video-iteration-doctor`, and the relevant reference/aesthetic/action skills identify an evidence-backed next variable. Do not answer repeated failure with more adjectives.
- Treat user-supplied director, studio, film, cinematography, martial-art, dance, stunt, weapon, design, music, and sound names as a starting set, not a complete set. Use `$creative-anchor-director` to audit missing reference functions, then route candidates through the relevant domain skills.
- When the user says "直接", "来吧", "整", "生成", or similar, make reasonable assumptions and output a paste-ready prompt instead of asking follow-up questions.
- For character/team design, keep series-level style unity while deliberately varying silhouette, height impression, body type, expression, posture, weapon scale, and personal rhythm. Do not reuse one body/personality template across every member unless the user asks for uniformity.
- For the user's SD2 全能参考 workflow, declare reference roles in Liu's local asset format, such as `{{Image 1}}（角色身份与服装参考）`, `{{Image 2}}（载具与道具参考）`, `{{Image 3}}（世界色彩与地点参考）`, `{{Image 4}}（场景布局参考）`, `{{Image 5}}（道具细节参考）`, and `{{Video 1}}（动作与运镜参考）`. Do not let style/layout/motion references override identity unless the user asks.
- Treat every clip as standalone unless prior frames are actually supplied. For paste-ready SD2 / Seedance prompts, encode the visible starting state inside the opening event beat, e.g. `开场：第一帧就是...`, not as a detached first-frame-state block unless the user is preparing a first-frame asset note.
- For story-driven or emotion-driven clips, use a temporal hinge before writing shots: what just happened, what is happening now, and what is about to happen. Prefer "刚刚...正在...即将..." to naked emotion labels, so behavior and expression evolve naturally.
- If the user asks for "保持这个画风但更真实/三渲二", preserve stylized anime character design while adding realistic lighting, material response, depth, and camera physics. Avoid drifting into flat cartoon.
- If the user asks for opposite-color backgrounds, assign color ownership: character colors, vehicle colors, environment colors, danger/authority colors, and forbidden palette drift.
- Treat `$cinematic-audiovisual-language` as the structural foundation for video prompts. Shot function, spatial path, axis/screen direction, staging, and cut logic must be clear before style, tension, material, or SD2 packaging.
- Treat `$professional-storyboard-director` as the professional storyboard / beat-planning layer for substantial film-video prompts, and as the full output owner when the user asks for 分镜, 剧本转分镜, 15S beat, 短剧分镜, 漫剧分镜, storyboard, shot list, 镜头表, 高张力分镜, 动作分镜, 情绪分镜, 广告分镜, or wants a scene translated into a shot-by-shot board. It should sit after macro structure and before final prompt packaging, combining normal storyboard discipline, imported script-to-AI-video board logic, and high-tension bias when appropriate.
- Treat `$visual-style-aesthetic-direction` as the aesthetic foundation when the user asks for style, 画风, 高级感, 通用审美, or when a result feels generic/cheap. Choose the medium domain, relevant industry control vocabulary, and style rules before adding render terms or effects.
- Treat `$ai-material-realism` as a mandatory baseline for every visual prompt, not an optional polish step. Apply it after the audiovisual scaffold exists: every image/video prompt should include material surfaces, light direction, contact shadows, reflection/roughness/texture response, optical behavior, and fake-look avoidance before final packaging.
- Treat `$action-choreography-reference` as the physical foundation for meaningful action: define actor/load relation, support and center path, weapon mass distribution, force chain, contact response, braking, and recovery before action rhythm or spectacle.
- Before writing action nodes, use `$action-choreography-reference` to assign each principal performer a primary movement/martial basis and visible action grammar: stance, body level, path geometry, support changes, rhythm, and recovery signature. Action verbs alone are not choreography.
- When game/render-engine vocabulary helps, use it deliberately: AO/contact shadows for grounding, PBR/roughness/metallic/specular for material behavior, anisotropic highlights for brushed metal/hair/satin, GI/bounce light for scene integration, volumetrics for air/water/fog, and NPR/cel-shading controls for 三渲二 or stylized CG.
- When a prompt belongs to a specific industry, use its control vocabulary deliberately: fashion terms for garment construction, architecture terms for space and circulation, product/industrial terms for seams and ergonomics, photography/cinema terms for lens/light/color, print/typography terms for layout, UI/data terms for hierarchy, food/craft terms for material truth.
- For one-scene clips, lock fixed-stage blocking before ordered beats: same 16:9 frame, same left/right/foreground/background relationships, and same action path. Camera changes are allowed; use master wide shots to reveal position and close-up/insert/occlusion shots to hide micro-position drift.
- When possible, assign a reference as `layout/blocking reference only` to control subject placement, scale, and camera framing without overriding identity or style.
- For strict position control, use an abstract color-board/CAD layout reference rather than a pretty scene reference. The board should map color blocks to subjects/objects/set pieces and encode object footprint, front/back layer, long-axis orientation, facing/gaze direction, action path, and target points. Keep a clean no-text version for model upload and a labeled version only for human checking.
- When a layout/blocking problem needs 3D proof, camera-path proof, animatic/previs layout, whitebox staging, or Blender-controlled reference renders, route through `$blender-mcp-previs` before final SD2 packaging. Use it to produce functional blockout references, not decorative finished art.
- When a Blender/previs problem is specifically character action motion quality, route through `$mocap-action-previs` before hand-keying. Use sourced mocap, BVH/FBX, or premade animation evidence when prior procedural or hand-keyed motion looks slow, silly, static, off-rig, or has bad limb/leg motion.

## 15-Second Prompt Contract

### Cross-Layer Locomotion Packaging

When full-body terrestrial locomotion is a primary proof task, coordinate the specialist outputs instead of pasting a physics paragraph into every section:

- `【视觉材质总控】`: light- and surface-specific contact occlusion, sole/surface response, and visible garment/hair material lag;
- `【镜头语言总控】`: camera-subject average velocity coupling, parallax, relative drift function, and motion-blur ownership;
- `【事件节拍】`: support phase, center-of-mass transfer, terrain adaptation, acceleration/braking, and changed position;
- `【声音】`: load-acceptance footfall, surface transient, cloth/gear lag, and perspective-consistent distance;
- `【正向稳定约束】`: at most one concise current-shot grounding lock when the risk is proven.

Spend fidelity only where the framing can show it. Close-ups, flight, suspended motion, and stylized abstraction do not inherit terrestrial foot/IK language by default. Technical terms such as RTAO, IK, collision mesh, or velocity matching remain backstage unless a compact term genuinely improves a visible result.

For 15-second AI video prompts, avoid the weak default of 3 broad shots unless the user explicitly wants a simple three-shot plan.

Use one of these structures:

- **5-beat micro-story**: hook -> orientation -> decision -> consequence -> payoff.
- **6-peak action showcase**: launch -> dodge/turn -> scale reveal -> near miss -> hero peak -> exit/loop.
- **continuous scene with panel cuts**: one spatial path, but 5-7 manga/comic panel-like camera changes with clear screen direction.

Each beat must change at least two of:

- shot function
- shot size
- camera height/angle
- camera movement path and tracking owner
- motion vector
- subject action verb
- information revealed
- foreground/background relationship

For every major beat, write camera motion as a motivated relationship, not a decorative move:

```text
名词风格锚点：[director / cinematographer / film / studio / work]风格 + [concrete visible camera result]
镜头跟随对象：[subject / vehicle / weapon / ground line / threat / receiver]
运镜路径：[push / pull / side-track / chase / arc / descend / rise / whip / drift / recoil / handoff]
运镜动机：[speed pulls camera / obstacle forces camera upward / contact freezes camera / scale requires pullback / foreground wipe hides cut]
证明的信息：[scale / route / friction / contact / danger / state change / consequence]
交接/终点：[next tracking owner / impact consequence / final camera state]
```

Treat the owner/path/trigger/proof/handoff contract above as backstage shot planning. In the final paste-ready prompt, compile the default camera relationship into `镜头语言总控` once. Ordinary `事件节拍` lines inherit it. Add local camera wording only for a genuine special device—such as FPV dive, extreme-perspective rupture, weapon-to-lens pass, impact lock, distortion surge, overhead reveal, POV switch, or transition—and state its trigger plus visible result. Do not repeat the master style names or routine camera contract in every beat.

Locked-off shots are allowed only when the stillness itself creates tension; otherwise, do not let a 15-second prompt become a set of static compositions.

Do not repeat "side tracking shot of the character moving through city" across multiple beats. If the subject travels, vary the information: scale, obstacle, viewpoint, route, threat, or emotional state.

The beat map becomes literal prompt syntax only when its segment allocation is high-confidence. A good hybrid is exact large segments plus flexible internal editing: `0-3秒突进与截击；3-8秒连续攀攻；8-10秒核心暴露与蓄势；10-12秒终结；12-15秒收势`，while avoiding timestamps for every cut inside those segments.

For emotion-led 15-second prompts, define the time state before the shot list:

```text
刚刚: visible residue from the previous event.
正在: present action in the scene.
即将: incoming interruption, threat, reveal, or reversal.
最终: irreversible image or emotional consequence.
```

Activation keywords:

- **导演模式**: primary keyword for the full AI-video prompt workflow.
- **片场模式**: casual alias.
- **SD2导演模式**: explicit alias when the user wants 即梦 SD2 / Seedance output.

## Specialist Stack

Use the skills in this order when relevant:

1. `$creative-research-first`: inspect supplied assets and research unresolved domain mechanics, references, current platform behavior, and professional vocabulary before creative synthesis.
2. `$creative-anchor-director`: preserve known names, audit missing creative-reference functions, research candidates, assign each anchor a role, and build a compact compatible stack.
3. `$video-structure-design`: define hook, first-frame promise, retention curve, temporal hinge, duration map, segment order, turn, payoff, loop/CTA, and platform/use-case structure.
4. `$screenwriting-story-craft`: define protagonist, desire, obstacle, stakes, temporal hinge, choice, consequence, dialogue/subtext, and scene purpose when the clip needs drama.
5. `$production-design-worldbuilding`: define world rules, art direction, color ownership, location logic, material systems, props, costumes, vehicles, and environmental storytelling.
6. `$visual-style-aesthetic-direction`: choose the medium domain, aesthetic family, industry control vocabulary, style rules, color ownership, rendering hierarchy, and anti-cheapness constraints when style or 高级审美 matters.
7. `$kinetic-action-visual-master`: for high-energy action, convert the chosen aesthetic into a whole-film camera, composition, shot-scale, animation-exaggeration, physics, and coherence envelope before detailed shots.
8. `$cinematic-audiovisual-language`: foundational shot grammar. Convert structure/story/world/style beats into shot functions, spatial path, axis/screen direction, staging, continuity editing, rhythm, and sound-image logic before adding spectacle or render polish.
9. `$professional-storyboard-director`: baseline beat/shot-planning layer for substantial film/video prompts; full owner for 分镜, 剧本转分镜, 15S beat, 短剧/漫剧分镜, AI-video-ready shot boards, and prompt-ready clip splitting.
10. `$cinematic-music-sound-design`: design spotting, cue boundaries, motifs, rhythm, harmony, orchestration, ambience, foley, effects, silence, sound perspective, mix hierarchy, and AI music prompts.
11. `$ai-material-realism`: mandatory render baseline for every visual prompt. Once the shot grammar exists, define physical material surfaces, light direction, render vocabulary such as AO/PBR/GI/anisotropic highlights when useful, reflection/roughness/texture response, contact shadows, optical behavior, motion blur, and fake-look avoidance before final shot packaging.
12. `$reference-hunting-board`: build a reference search board when the user lacks examples or needs real film/action/material references.
13. `$character-continuity-bible`: lock character, costume, prop, weapon, scene, and world continuity before multi-shot or identity-sensitive work.
14. `$mechanical-transformation-design`: design believable folding, unfolding, telescoping, locking, linkage, cam/pulley, TF-style vehicle-to-robot restructuring, mecha transformation boards, and weapon-transformation mechanics.
15. `$visual-reference-vocabulary`: find camera, composition, lighting, director, anime-impact, and style-reference terms when the user wants feeling but lacks vocabulary.
16. `$blender-mcp-previs`: when 3D spatial proof is useful, create whitebox/blockout previs, camera-path, action-beat, or layout reference renders before SD2 packaging.
17. `$mocap-action-previs`: when Blender action previs needs believable body motion, use sourced mocap, BVH/FBX, rigged models, or premade animation projects before rendering or hand-keying.
18. `$action-choreography-reference`: design martial basis, actor/weapon physical profile, center of mass, support, mass distribution, force chain, contact response, braking, and recovery when the shot contains action.
19. `$action-rhythm-editing`: scale timing, impact beats, recoil, follow-through, braking, slow motion, music sync, and 3s/5s/8s/15s structure to the action's mass and inertia.
20. `$seedance-fight-director`: for Seedance/Higgsfield fight outputs, especially 起始态/终止态, A/B/C/D action anchoring, HEAVY/RUSH/CHASE hit-marking, and action reference binding.
20A. `$cinematic-vfx-director`: when effects carry force, speed, magic, transformation, destruction, threat, or environmental consequence, design the primary read, medium-aware motion family, source/path/collision/response/decay, grading, and compositing/sound integration; let `$vfx-effect-construction-engine` resolve lifecycle and vocabulary when needed, then let `$seedance-vfx` compress it for Seedance.
21. `$jimeng-sd2-prompting`: package the final idea into 即梦 SD2 / Seedance-ready prompt structure, including mode, reference roles, camera, consistency locks, audio cues, and positive stability locks.
22. `$seedance-20`: when the target is Seedance 2.0, compile the director-mode plan into Seedance-specific standalone, sequence, continuation, first/last-frame, edit, extend, reference-to-video, source-gated platform, safety, or troubleshooting guidance.
23. `$ai-video-prompt-preflight`: check the final prompt for conflicts, feasibility, reference roles, timing overload, continuity gaps, audio/material-light completeness, split strategy, and likely failure modes before generation.
24. `$think-one-step-further`: final handoff check. Confirm the prompt solves the real intent, is directly usable, names any missing reference/action, extracts reusable structure, and adds one guardrail for the next likely failure.
25. `$creative-production-ledger`: before generation, bind the exact prompt, reference roles, model/mode/settings, and later outputs under one immutable attempt ID.
26. `$ai-video-output-review`: after generation, probe the video, extract timestamped frames/contact sheets, compare the result with the prompt and references, and identify evidence-backed acceptance failures.
27. `$ai-video-iteration-doctor`: diagnose a failed result and write the next precise retry patch.
28. `$creative-casebook`: after the user confirms a result, or when an inspectable open-production project exposes output plus prompts/references/settings/iterations, separate facts, observations, claims, and inference; extract the successful/failed layer, isolated controls, model/mode condition, and the right case/skill/template destination.
29. `$capsule-engine`: promote sufficiently evidenced case lessons into scoped reusable capabilities, track applications and counterexamples, and propagate only active controls into relevant skills.

Read `references/orchestration-playbook.md` before handling substantial AI-video prompt work.

## Routing Rules

- If the user says "没思路", "给我几个方向", "要更电影感", "要张力", use `$creative-anchor-director` to choose the relevant lanes, then route visual terms to `$visual-reference-vocabulary`.
- If the user knows only some names, asks "还有什么参考", "帮我补足名称锚点", "举一反三", or supplies partial references without covering style/world/camera/action/audio needs, start with `$creative-anchor-director` and research unfamiliar lanes before finalizing.
- For substantial prompt creation, use `$creative-research-first` before the specialist stack. Search current official platform documentation when model behavior matters, and search credible craft/reference sources for unfamiliar domains.
- If the user asks for 视频结构, 片子结构, 开头怎么抓人, 留存, 起承转合, 预告片结构, 广告片结构, MV结构, 15/30/60秒结构, or says the video has shots but no structure, start with `$video-structure-design`.
- If the user says 镜头没信息点, 主体不突出, 只剩氛围/光影, 镜头重复, 同一张脸反复推近或换景别, 不知道下一镜为什么接, 运镜没有理由, or tools/effects have become a 缝合怪, use `$shot-information-progression` before storyboard and camera polish. It owns shot-level viewer-knowledge delta, visible-behavior versus implied-meaning separation, redundancy removal, and the causal handoff skeleton; `$professional-storyboard-director` and `$cinematic-audiovisual-language` still own the complete board and camera grammar.
- If the user says 主镜, 从画面推机位, 先想到了关键画面但前后接不上, 多人轴线/阵营关系混乱, 景别或机位高度只凭公式, or the scene has clear information but still looks like average coverage, use `$master-shot-camera-planning` after any needed `$shot-information-progression` pass and before the full storyboard. It owns indispensable master-image selection and reverse-derived blocking, relationship axes, camera zones, shot-size/view-height reasoning, attention path, and connector constraints; `$professional-storyboard-director` still owns the complete board and `$cinematic-audiovisual-language` owns the general camera/continuity grammar.
- If the user supplies an existing song or `Audio1` and asks for the complete MV picture to be cut to it, especially dance/performance, performer-image identity, timecoded formation changes, insert clusters, or a final button, use `$reference-track-mv-director` as the fixed-track MV owner. It receives macro structure from `$video-structure-design`, cue evidence from `$cinematic-music-sound-design`, identity locks from `$character-continuity-bible`, physical phrasing from `$action-rhythm-editing`, and hands platform audio binding to `$seedance-audio` rather than creating competing music.
- If the user asks for 剧本, 故事, 人物动机, 冲突, 反转, 对白, 潜台词, 场景目标, 时间词, 情绪推进, or emotional hook, use `$screenwriting-story-craft`.
- If the user asks for 世界观, 美术设定, 场景设定, 城市设计, 视觉系统, 颜色体系, 反差背景, 道具/载具/服装设计, or says the world feels random or pasted together, use `$production-design-worldbuilding`.
- If the user asks to 展开一个世界, 做一组世界观图, 9张世界观静帧, 视觉文化板, infer a world from a reference image, or build a coherent imagined world before video/story, use `$mokeaigc-v9` before `$production-design-worldbuilding`; keep it responsible for still-image world evidence and visual laws.
- If the user mentions 怒戏/愤怒/暴怒/对峙, use `$performance-scene-director` with `$anger-scene-director`; 哭戏/眼泪/情绪爆发, pair it with `$crying-scene-director`; 哀伤/惆怅/孤独/不哭的悲伤, pair it with `$sorrow-scene-director`; 喜戏/惊喜/欣喜, pair it with `$joy-scene-director`; 乐戏/嬉闹/玩乐/戏谑, pair it with `$delight-scene-director`. Pick one primary emotion profile unless the user requests a deliberate mixed arc.
- If the user asks for 风格化, 审美, 画风, 高级感, 视觉风格, 通用审美, or says the result is cheap/generic/aesthetically weak, use `$visual-style-aesthetic-direction` before material/render polish.
- If the user asks for 视听语言, 镜头设计, 轴线, 场面调度, 镜头组接, 景别, or says the camera design is weak, repetitive, or incoherent, use `$cinematic-audiovisual-language`.
- If the user asks for 分镜, 剧本转分镜, 15S beat分镜, 短剧分镜, 漫剧分镜, 专业分镜师, storyboard, shot list, 镜头表, 漫画式分镜, 高张力分镜, 动作分镜, 情绪分镜, 广告分镜, 角色PV分镜, or wants a scene turned into a shot-by-shot board, use `$professional-storyboard-director` as the visible output owner; for substantial film/video prompts, use it at least as an internal beat/shot-plan baseline before packaging. For AI-video-ready boards, use its imported script-to-storyboard reference, then pair it with `$cinematic-audiovisual-language` for continuity and `$jimeng-sd2-prompting` for final packaging.
- If the user asks for 高速战斗视觉母版, 激烈运镜, POV动作, 非常规构图, 多景别高速切换, 大画幅真人质感与动画夸张融合, giant/mecha combat, or a forceful opening style paragraph for an action prompt, use `$kinetic-action-visual-master` after aesthetic selection and before detailed shot design.
- For any final video prompt, run `$cinematic-audiovisual-language` before material, tension, and model-packaging layers. Do not let rich texture or style language substitute for shot function, blocking, axis, screen direction, or cut logic.
- If the user asks "找参考", "我不了解", "有什么现实参考", "给我搜/找例子", start with `$reference-hunting-board`.
- If the user supplies video links, Bilibili/B23 links, local video files, or prior successful clips and asks to 看看/拉片/整个都看/归类, start with `$reference-hunting-board` plus `$cinematic-audiovisual-language`; inspect the whole-work grammar or state access limits before transferring only selected pieces.
- If the user is building a recurring character, weapon, scene, short drama, series, or complains about drift, use `$character-continuity-bible`.
- If the user asks to control layout, blocking, color-board references, CAD references, front/back relationship, object footprint, long-axis direction, standing point, facing direction, or position drift, use `$character-continuity-bible` plus `$jimeng-sd2-prompting`; use `$cinematic-audiovisual-language` when translating the board into shots.
- If the user asks for Blender, 3D预演, previs, whitebox, blockout, camera path, animatic layout, or viewport reference renders for AI video planning, use `$blender-mcp-previs`; keep the output functional for staging/camera/reference control rather than polished art.
- If the user asks for 动作预演, mocap, BVH/FBX, Blender action preview, game-style / martial-arts / boxing / melee / weapon / stunt action previews, or says a previous Blender/procedural motion looked slow, silly, static, off-rig, or had bad limbs/legs, use `$mocap-action-previs`; keep it responsible for sourced body motion evidence and preview validation.
- If the user mentions mechanical transformation, 机械变形, TF, 变形机甲, 载具变机器人, mecha transformation, 武器变形, 弓变形, folding/unfolding, telescoping, hinge, linkage, cam, pulley, lock, or deployable parts, use `$mechanical-transformation-design`; for vehicle-to-robot or mecha combat boards, use its imported TF mecha reference.
- If the user mentions fight, weapon, chase, slash, kick, throw, bow, staff, sword, chain, body motion, or "动作参考", use `$action-choreography-reference`.
- If the user specifically wants a Seedance/Higgsfield 打斗/格斗/武打/动漫战斗 prompt, or asks to fuse 动作、节奏、运镜、打击感 into one output, route to `$seedance-fight-director` as the direct fight-output skill; use its imported action systems for 起始态/终止态, A/B/C/D 动作分类, HEAVY/RUSH/CHASE 打点, or reference-material binding. Call `$action-choreography-reference`, `$action-rhythm-editing`, or `$seedance-camera` separately only when deeper diagnosis or reference extraction is needed.
- If the user mentions weapon weight, center of mass, balance, leverage, inertia, momentum, traction, recoil, braking, heavy weapons, strength differences, or says all martial arts look the same, route to `$action-choreography-reference` before rhythm and model packaging.
- If the user mentions rhythm, timing, beat, music, slow motion, impact frame, 卡点, 打击感, 起势/爆发/收势, use `$action-rhythm-editing`.
- If the user mentions 特效, VFX, 粒子, 光效, 魔法, 能量, 冲击波, 爆炸, 火焰, 烟雾, 水体, 破坏, 碎片, 武器轨迹, 拖影, 速度线, 变身生长, 特效廉价, 特效遮动作, or effects must carry force/state/transition, use `$cinematic-vfx-director` after the action/state and medium are clear. Use `$vfx-effect-construction-engine` for lifecycle, particle/energy/ritual grammar, source-to-endpoint construction, and precise term retrieval. For Seedance, then use `$seedance-vfx` only as the compact platform compiler.
- Before delivering any final video prompt, run `$seedance-audio`'s prompt-time Reference Audio Gate. If the clip needs selective action/impact/transition peaks, music-led section changes, exact-duration visual structure, or text-only timing has already proved soft, generate the reference WAV in the same response without waiting for Liu to ask separately. `$seedance-audio` owns the sparse cue track, local SFX/music adapter, audio-reference role, one-variable A/B, and leakage fallback; `$action-rhythm-editing` still owns physical timing and `$cinematic-music-sound-design` owns the final score/mix. Skip the WAV when the shot has no material timing problem or the platform cannot accept audio reference.
- If the user mentions 配乐, BGM, 音乐, 主题动机, BPM, 配器, 和声, 音效, 声音设计, 声画关系, 环境音, 拟音, 静默, Suno, Udio, or the clip needs an audio plan, use `$cinematic-music-sound-design`.
- Use `$ai-material-realism` for every visual prompt as a baseline, even when the user does not mention material, lighting, or realism. If the user says "AI味", "塑料感", "质感", "真实", "商业质感", "光影", "打光", "反射", "逆光", "轮廓光", "渲染", "游戏渲染", "PBR", "AO", "环境光遮蔽", "各向异性高光", "全局光照", "运动模糊", "速度模糊", "motion blur", or the scene features skin/metal/fabric/wet ground/glass/vehicles/high-speed motion, make that layer more explicit and detailed.
- For vehicle, chase, impact, or fast camera prompts, combine `$cinematic-audiovisual-language` for shot logic with `$ai-material-realism` for readable layer-based blur, light direction, reflections, contact shadows, and material response.
- If the user asks for 即梦, SD2, 图生视频, 文生视频, 首帧/尾帧, or final generation prompt, use `$jimeng-sd2-prompting`; if the user specifically names Seedance 2.0 or needs Seedance continuation, first/last frame, reference-to-video, edit/extend, platform/API facts, safety rewrite, or failed-output repair, also use `$seedance-20`.
- If the user asks for 生成前检查, 提示词质检, prompt QA, 哪里会崩, 怎么拆段, 稳定性, or final safety check before generation, use `$ai-video-prompt-preflight`.
- If the work will be generated, reviewed, compared, or retried as a project, use `$creative-production-ledger` to bind the final prompt, reference roles, model/mode/settings, outputs, review evidence, and retry delta.
- If Codex/imagegen or TapNow will actually generate or download an output, use `$generation-asset-pipeline`: create its ticket before generation, attach/archive the completed original result before review, and keep the exact submitted prompt beside the media.
- If the user asks for 举一反三, 多想一步, 整体优化, 这个处理对不对, 还要不要做什么, or asks to optimize the whole workflow/skill/prompt system, use `$think-one-step-further` as the final reasoning and propagation layer.
- If the user says retry, not right, 崩了, 乱了, 人脸变了, 武器变了, 动作软, use `$ai-video-iteration-doctor`.
- If the user supplies a rendered video and says 看看, 检查, 验片, 逐帧, 抽帧, 穿帮, 两个主角, 站位漂移, 音画不同步, or asks what actually failed, use `$ai-video-output-review` before retry diagnosis.
- If the user says 这个效果好, 这次可以, 记住这个, 复盘, 沉淀, 做成案例, 下次沿用, 开源提示词, 完整工程, production breakdown, or a repeated failure reveals a stable mechanism, use `$creative-casebook`. For external cases, inspect the finished output and authoritative project package before promoting any rule.
- If a case lesson has clear evidence, conditions, failure boundaries, and future reuse value, use `$capsule-engine`; do not promote an ambiguous single generation.
- For durable evidence, route narrowly: exact generation attempt -> `$creative-production-ledger`; one inspected success/failure -> `$creative-casebook`; repeated or user-approved reusable rule -> `$capsule-engine`; stable preference/commitment/global operating policy -> Sophia memory / session state.
- For normal action-video prompt creation, use continuity + audiovisual shot grammar + visual/action/rhythm + material + SD2 packaging, but keep output concise.
- For weight-sensitive action, insert an explicit action-physics block between audiovisual grammar and rhythm: actor/load relation -> support/center path -> mass distribution -> contact response -> braking/recovery.
- For any action-led clip, insert an action-grammar block before the event chain: primary basis -> visible signature -> recurring support/level/vector pattern -> recovery signature -> fantasy amplification.
- For character PV and action-showcase prompts, audit the ending before delivery: the strongest action or reveal should not resolve into a static hero pose before the last 1-1.5 seconds unless portrait/fashion stillness is the explicit goal. If the final pose starts too early, add or move a mid-late action/state-change beat instead of extending the beauty hold.

## Output Shape

For exploration:

```text
意图判断：
推荐路线：
1. 联网研究：
2. 视频结构：
3. 剧作/人物：
4. 美术世界：
5. 视听语言：
6. 音乐与声音：
7. 参考方向：
8. 连续性锁定：
9. 动作/节奏：
10. 材质真实感：

可选方向：
...
```

For final prompt, the visible planning notes may stay brief, but the standalone copyable prompt block must use Liu's six-part order: 角色/资产锁定 -> 视觉材质总控 -> 镜头语言总控 -> 事件节拍 -> 声音 -> 正向稳定约束. If one section has little content, keep the heading and write one current positive lock inside the copyable block. `镜头语言总控` must carry the complete whole-film camera style as compact style-result phrases. `事件节拍` inherits this master; write local camera direction only for a special beat whose trigger and visible result differ from the default.

For final prompt:

```text
意图判断：
需要你确认：（只有关键不确定时出现）
创意判断：
联网研究：
调用层：
视频结构：
剧作核心：
时间铰链：
美术世界：
视听语言：
音乐与声音：
参考板：
连续性锁定：
机械变形：
视觉参考：
素材准备：
动作参考：
节奏设计：
材质控制：
生成前质检：

参考音频：（仅在 Reference Audio Gate 触发时出现）
- 文件：<真实本地 WAV 路径>
- 目标片长：<秒>
- 节奏点：<简洁 cue 表>
- 上传角色：{{Audio N}}（画面节奏控制参考；最终混音另行处理）

【完整可复制提示词】（独立代码块，只放模型提示词）
【角色/资产锁定】
{{Image N}}（...参考）：...  # replace N with the real supplied number
【视觉材质总控】
...
【镜头语言总控】
[complete whole-film camera style: named aesthetic anchors + perspective + lens family + distortion + movement energy + framing/edit rhythm + reveal logic]
【事件节拍】
[action/state/contact/consequence beats; add a trigger + visible-result camera clause only for a genuine special-camera beat]
【声音】
...
【正向稳定约束】
...

下一轮只建议调：
...
```

For short answers, output only the final prompt plus the most important reference choices. If the Reference Audio Gate triggered, the reference WAV path and compact cue map are mandatory even in the short answer.

## Quality Bar

- Every substantial director-mode response starts from Phase 0 intent reading, even if the visible answer only shows one concise `意图判断` sentence or uses the inference silently.
- Apply the Non-Self-Deception Gate: never invent unseen references, fake inspection, fake current facts, fake prior context, exact timing, model behavior, or user taste evidence. Ask Liu when the missing information changes the core result.
- The final prompt must read like a director describing one shootable clip.
- The first substantive creative block of the final prompt must establish the global visual master. Detailed shots may vary scale and angle but must not reopen the medium, palette, material, or rendering decision.
- Treat masters as high-level invariants, not as long paragraphs. Keep one compact visual/material master and one compact camera master; later beats inherit them and describe only temporal change. Precision is decision density, not word count.
- Before packaging specialist outputs, choose one primary fidelity spend and one secondary spend. Compress or omit every layer that does not change the visible result; never concatenate every specialist recommendation into the final prompt.
- Under a hard character budget, preserve identity, world-identity packet, event path, coverage-critical cuts, and end state before decorative adjectives, repeated render synonyms, broad stability boilerplate, lore explanation, secondary flourishes, or unsupported weapon actions. If a supplied environment reference already carries the world, replace the text packet with one explicit reference-role lock rather than duplicating it.
- For I2V/R2V, let inspected references carry spatial appearance and layout. Use text mainly for motion, timing, camera path, sound, and endpoint instead of re-describing the image.
- For aggressive action, the visual master must bound camera behavior: every move or cut has an action, occlusion, gaze, impact, or spatial trigger; unconventional framing never licenses random rotation, axis loss, or unreadable geography.
- Research must alter at least one meaningful creative or feasibility decision for substantive prompts; do not add sources as decoration.
- Original designs must show sedimentation: the viewer should be able to infer some culture/craft/material/professional/social/action lineage from silhouette, costume construction, weapon function, location rules, palette ownership, and positive stability locks.
- Preserve deliberate director, studio, film, genre, cinematography, martial-art, dance, sport, and movement-system names as compact semantic anchors. Add minimal visible camera/body/material language only to disambiguate intent or prevent a known failure; do not replace one useful term with a diluted paragraph.
- Do not make the user supply the complete reference vocabulary. State what their anchors cover, supplement the missing high-value roles, and keep the final set compact and compatible.
- Avoid name salad. Keep at most 2-4 named references per shot unless the user is brainstorming a library.
- Keep one main action per 5-second clip; split longer action into beats.
- For weighted action, retain the named technique or movement basis and bind it to the required physical profile. The name supplies movement identity; support, mass distribution, contact response, and recovery keep it physically credible.
- For aesthetic action, every event chain must inherit a movement grammar; “run, climb, attack, block, slash” alone does not pass the quality gate.
- Lock identity/weapon/scene before adding heavy action or camera movement.
- Define the macro video structure before writing shots; shots should serve hook, orientation, build, turn, payoff, or loop.
- For story-driven clips, define want, obstacle, choice, and consequence before shot language.
- For emotion-driven clips, define the temporal hinge before shot language: past residue -> present action -> incoming pressure -> final consequence.
- For emotion-driven clips where acting is the main value, let `$performance-scene-director` own the shared acting arc, and let exactly one emotion profile wrapper own the intensity ceiling and micro-action flavor; camera and sound should support that playable arc.
- For world-driven clips, define color ownership, material rules, location function, and forbidden drift before shot language.
- For world-first development, use `$mokeaigc-v9` to create/inspect the 9-still world board, then carry forward only stable visual laws into video packaging.
- For multi-shot clips, run audiovisual continuity before adding tension effects.
- Audiovisual grammar is the first visual quality gate: each beat needs function, shot size, camera position, camera movement path, tracking owner, screen direction, continuity bridge, and cut reason before material, tension, or SD2 packaging is added.
- For video prompts, reject “good storyboard but no motion” outputs: if the sequence could be generated as still frames with hard cuts, add motivated camera movement, action-camera coupling, or a deliberate lock-off rationale.
- Run an anti-repetition pass: adjacent shots cannot share the same shot size, camera height, action verb, and motion direction unless the repetition is the intended concept.
- Every beat should have this internal shape: function -> visible image -> camera behavior -> motion/transition -> continuity lock. A major segment may have a high-confidence time range; an individual cut gets an exact timestamp only when synchronization or edit control requires it.
- Audit duration at four levels: total clip duration, segment allocation, structural peak placement, and physical action-phase timing. Convert high-confidence segment allocation into prompt ranges when useful; keep micro-shot duration flexible by default.
- When audio matters, every major beat should identify its sound focus, cue change, or intentional silence; do not synchronize every cut mechanically.
- Run preflight before final delivery when the prompt is long, multi-shot, action-heavy, reference-heavy, or intended for immediate generation.
- For reference-based generation, state which assets already exist, which are required, which are optional, and the exact role of each asset before presenting the final prompt.
- For high-speed shots, do not leave motion blur as a generic adjective. Specify what stays readable and what blurs: hero subject, vehicle silhouette, background streaks, foreground wipe blur, wheel rotation blur, light trails, and shutter feel.
- For transformation shots, every new part must have a visible source: hinge, rail, nested segment, linkage, cable, cam, or latch.
- Put consistency locks and positive video stability locks at the end through `$jimeng-sd2-prompting`, then check them with `$ai-video-prompt-preflight`.
- When uncertain, give 2-3 route options instead of pretending one path is objectively best.


## High-Speed Flight Reference Rule
For extreme high-speed flight, ascent, dive, dash, or fall prompts, never describe only the subject. Add visible spatial references: ground shrinking away, treetops whipping past, cloud layers being pierced, debris lagging behind, foreground objects crossing frame, and a clear wide/close rhythm. Use ultra-wide shots for scale and extreme close-ups for speed pressure. Transformation details should occur during motion unless the user requests a display; reserve the readable full form for the final hover or impact pose.

## Negative-Hygiene Preflight For Motion Prompts
Before adding positive stability locks, remove positive phrases that can summon the wrong result. For vertical ascent/dive, avoid camera wording that implies parallel horizontal pursuit, such as following behind/side-behind through trees. Replace with visible vertical references: ground rapidly shrinking below, tree crowns becoming a flat texture, cloud hole opening above, vertical parallax, falling debris lagging behind, ultra-wide distance proof, and close-up motion-blur inserts. Negatives cannot override a stronger wrong positive camera instruction.
