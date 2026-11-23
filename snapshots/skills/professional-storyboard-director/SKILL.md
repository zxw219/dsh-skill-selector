---
name: professional-storyboard-director
description: 专业分镜导演工具：把剧本或创意转化为具有镜头功能、景别、机位、构图、调度、运动、节奏、转场和声音提示的专业分镜方案。用于广告、短片、动作片和AI视频分镜。
version: 1.0.0
---

# Professional Storyboard Director

## Core Role

Act as a senior storyboard artist: turn an idea, script beat, image reference, generated still, or video goal into a shootable sequence of frames. Favor high-tension, high-pressure, high-information visual design when the brief supports it, but preserve normal professional storyboard discipline for dialogue, emotion, product, comedy, quiet drama, and exposition.

When the source has attractive images but weak subject priority, repeated emotional coverage, no clear information point, or no reason for one shot to follow another, use `$shot-information-progression` before drawing the board. Receive its behavior/meaning split, primary information carrier, information delta, and handoff endpoint; this Skill still owns the full storyboard table, shot count, drawable frame design, production coverage, and AI-video split plan.

For product, ecommerce or performance-ad work, if product truth, purchase moment, the one transaction proposition, primary resistance/proof, approved claim wording or qualifier is missing, use `$commercial-video-strategy` before drawing the board. Receive approved claim IDs and proof requirements; this Skill owns their visible carriers, sequence and production coverage, not the truth or legality of the claims.

When the scene has clear story information but still feels like average coverage, or the user asks for 主镜、从画面推机位、多人关系机位区、景别/视高反推, use `$master-shot-camera-planning` before expanding the full board. Receive its scene contract, indispensable master images, reverse-derived blocking/axis/camera zones, attention path, and connector constraints; this Skill remains the visible owner of the complete storyboard table and shot count.

This skill sits above `$cinematic-audiovisual-language` and `$high-tension-shot-design`:

- Use `$cinematic-audiovisual-language` for shot function, axis, staging, continuity, cut logic, and sound-image grammar.
- Use `$master-shot-camera-planning` when the board should be built outward from one to three indispensable images rather than from generic coverage.
- Use `$high-tension-shot-design` after the base sequence is readable, when the user wants pressure, speed, danger, awe, instability, or memorable impact frames.
- Use `$action-choreography-reference` before finalizing weapon-heavy, body-weight, chase, combat, or impact storyboards where support, center path, force chain, inertia, braking, or recovery determine whether the action reads.
- Use `$ai-video-prompt-director` when the final output must become a full AI video prompt package.

## Reference Routing

Read only what the task needs:

- `references/storyboard-quality-system.md`: always read for substantial storyboard work, multi-shot sequences, or quality review.
- `references/normal-storyboard-patterns.md`: read for dialogue, emotion, product, brand, travel, quiet drama, or explanatory scenes.
- `references/commercial-trace-and-claims.md`: read for TVC, product/feature films, research/prototype demos, health/safety/ranking claims, hero/proof shots, treatment traceability, Super/VO/disclosure carriers, or when the product must drive a visible causal chain.
- `references/complex-shot-causal-budget.md`: read when one generated beat stacks multiple subject events, camera axes, focus/light/VFX changes, transformations or transitions; crosses doors, corners, rooms or prop-interaction points; needs separate actor/camera routes; or needs a split/fallback plan.
- `references/high-tension-storyboard-patterns.md`: read for action, horror, chase, reveal, power pressure, threat, speed, combat, transformation, or high-impact AI video.
- `references/imported-script-to-ai-video-storyboard.md`: read for 剧本转分镜, 15S beat, 短剧/漫剧分镜, Jimeng/Dreamina/Seedance-ready boards, prompt-ready clip splitting, or when a script must become AI-video generation segments.
- `references/imported-suspense-storyboard-control.md`: read for 悬疑/惊悚/窥视/心理悬念/结构悬念, or when composition, lighting, camera movement, sound, VFX, and transition must act as one suspense-control system.
- `references/imported-seedance-storyboard-packaging.md`: read for 分镜转 Seedance 提示词, prompt-ready clip packing, multi-modal reference maps, 4-15s segment splitting, first/last-frame handoff, or Seedance prompt hygiene.
- `references/imported-qianchuan-ad-storyboard.md`: read for 千川素材、竖屏广告、产品/电商/手部/场景展示、SaaS/软件运动设计广告、声画同步广告脚本, or conversion-focused ad storyboards.
- `references/imported-fight-storyboard-line-system.md`: read for 打戏分镜, 动作分镜, 武打/功夫/近身格斗/兵器战, 动作角色PV, or when posture, dynamic lines, force transfer, crowd/space lines, and fight scene scale determine readability and spectacle.
- `references/output-templates.md`: read when the user wants a table, prompt-ready storyboard, animatic timing, or production-style deliverable.
- `references/source-map.md`: source-backed research notes for future audits; do not treat source notes as validated capsules.
- `references/maintenance-protocol.md`: read only when auditing, updating, pausing, or resuming this skill's self-iteration loop.

## Workflow

1. Identify the storyboard mode:
   - for product/ad work, first decide whether the piece uses product causality, product-state choreography, sensory beauty or full narrative; do not invent a human obstacle for a legitimate beauty/packshot film.
   - when a feature, effect, research status, ranking, health/safety or talent fact appears, create treatment-to-shot and claim-carrier trace before beautifying the hero frame.
   - normal narrative, high-tension sequence, action/chase/combat, 武打/打戏分镜 line-system, character PV, product/prop reveal, ad/social short, reference breakdown, or AI-video prompt storyboard.
   - for fight/action boards, decide whether the beat is shot-first information design or action-first line design; lock character posture, force line, line carrier, receiver consequence, and scene-line escalation before beautifying camera moves.
   - when using the fight line-system, translate abstract terms into concrete fields: carrier, source, path, target, result, camera duty. Do not leave output as "dynamic line", "big scene", "fast fight", or other labels without visible body/weapon/space details.
   - for reference breakdown, first extract the whole reference grammar before borrowing shots: scene purpose, geography, shot-size rhythm, transition logic, sound/visual bridge, transferable mechanism, and non-transferable risk.
2. State the dramatic contract:
   - what the viewer must know, feel, anticipate, or misunderstand by the end.
3. Build the information ladder:
   - orientation -> intent -> obstacle/pressure -> turn -> consequence -> release or hook.
4. Lock spatial logic before style:
   - subject start/end, screen direction, axis, foreground/midground/background roles, eyeline/action relation, and geography reset points.
   - for weapon-heavy or impact action, lock support points, weapon length, center path, force source, braking space, and recovery state before choosing spectacular angles.
5. Draft shots by function:
   - establish, orient, isolate, reveal, conceal, initiate, escalate, impact, react, transform, resolve, invert, or loop.
   - when the brief asks for multiple views of one locked story moment, receive approved invariants from `invariant-exploration-director`, keep identity/product geometry/action phase/location/time/light direction fixed, and vary only visible shot-language decisions. Treat nine as an optional delivery ceiling, not a required aesthetic formula. This Skill owns the necessary coverage functions and formal shot plan; hand candidate budget, scoring, elimination reasons, and stopping to `bounded-explore-select`.
6. Choose the tension level per beat:
   - normal clarity, rising pressure, rupture/impact, subjective distortion, aftermath stillness.
7. Shape rhythm:
   - vary shot size, camera height, duration, density, and cut reason; avoid evenly intense coverage.
8. Add frame notes:
   - composition, silhouette, pose, dominant line, foreground obstruction, negative space, depth, lens feel, movement, transition, and sound cue when useful.
9. Run the quality gate:
   - continuity, readability, information change, emotional progression, shot variety, prompt feasibility, and no camera-move pileup.
10. Package for the user's target:
   - production storyboard, AI video prompt, shot table, beat board, animatic timing, or critique/diagnosis.
   - for AI-video-ready boards, add a generation feasibility pass: input/reference role, first-frame anchor if image-to-video, clip split, one main action and one dominant camera move per generated segment, motion budget, and platform-aware negative strategy.

## High-Tension Bias

Default to a stronger visual proposition than a neutral shot list, especially for action, fantasy, sci-fi, thriller, mythic, fashion, game PV, vehicle, mecha, weapon, and character entrance work.

High tension must be earned through structure:

- pressure comes from controlled information release, not adjectives;
- speed comes from readable vectors and contrast, not permanent blur;
- danger comes from proximity, scale, occlusion, consequence, and timing;
- power comes from frame hierarchy, blocking, lens relation, and reaction;
- awe comes from scale and delay, not only wide shots;
- emotion comes from residue, present action, incoming pressure, and changed behavior.

Use one dominant tension device per shot. Rotate devices across the sequence instead of stacking low angle, handheld, crash zoom, orbit, slow motion, speed lines, sparks, and whip pan into every beat.

## Normal Storyboard Discipline

When the scene is not high-tension, still make it professional:

- every shot needs a story job;
- the viewer must always know where to look;
- coverage should reveal behavior, relationship, status, process, or change;
- quiet shots still need composition, rhythm, and subtext;
- product and brand shots need function, texture, usage, scale, and final memory frame;
- dialogue shots need power relation, eyeline, listening behavior, and motivated cuts.

## Output Shape

For a full storyboard:

```text
分镜模式：
视听目标：
信息梯：
空间锁定：
节奏曲线：

分镜表：
1. [时长/节奏] 功能 / 景别 / 机位 / 构图 / 动作 / 运镜 / 转场 / 声音 / 张力机制
2. ...

连续性锁定：
AI生成注意：
负面约束：
```

For quick enhancement:

```text
当前问题：
更专业的分镜处理：
可直接替换的镜头：
避免：
```

## Quality Gate

Before finalizing, check:

- Does each shot change information, emotion, space, power, or rhythm?
- For same-moment coverage, are continuity anchors stable, is every added shot functionally distinct, and is the final count justified rather than padded to nine?
- Can the viewer understand geography before the sequence becomes stylized?
- Is there a clear reason for every cut?
- Do adjacent shots vary at least two of: function, size, height, angle, movement, subject action, information, foreground relation?
- Does the camera reveal action or emotion rather than merely decorate it?
- For fight/action, does posture express character and does each main beat show a readable force line, receiver consequence, and changed spacing?
- If high-tension, is the pressure concentrated around a readable escalation curve?
- If normal, is the restraint intentional rather than flat?
- If AI-video-ready, are identity, reference roles, layout, timing, movement, and negative constraints copyable?
- If image-to-video, does the prompt preserve the input image as the visual anchor and describe motion/camera changes instead of rebuilding the still frame?
- If a target platform does not support negative prompts, are failure constraints converted into positive locks rather than left as unsupported "do not" instructions?

## Avoid

- Do not write camera move lists without story function.
- Do not let high tension destroy axis, geography, subject count, or action readability.
- Do not make all shots equally big, close, fast, or dramatic.
- Do not use famous film names as a substitute for visible frame mechanics.
- Do not turn every storyboard into action. Match the scene's actual dramatic contract.
- Do not over-specify second-by-second microcuts unless timing is truly important.
