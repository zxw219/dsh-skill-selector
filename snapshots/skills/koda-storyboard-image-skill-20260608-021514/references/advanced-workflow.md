# Advanced Koda Storyboard Workflow

Read this only for Project Batch Mode, full Koda workflow, Seedance handoff, asset-grounded continuity planning, complex choreography, procedural assembly, character identity boards, or detailed prompt-only deliverables.

## Full Workflow

1. **Reference prep**: inspect supplied characters, props, environments, shot notes, scripts, and current scene settings. Use inventory helpers for large or unclear asset folders.
2. **Action inventory**: build a complete beat chain before image prompting.
3. **Continuity locks**: define identity, wardrobe, hero props, geography, first/final state, screen direction, and allowed changes.
4. **Storyboard sheet**: create one annotated rough-sketch 16:9 control sheet with masthead, sequential panels, in-panel annotations, and bottom director tracks.
5. **Video handoff**: write a Seedance/video prompt that treats the storyboard as motion/control reference and explicitly excludes sheet graphics from the final render.

For multi-sheet storyboard generation, finish all reading and planning before the first image call, write compact per-sheet dispatch prompts, then call `image_gen` one sheet at a time. After a dispatch prompt is read, the next tool call must be the real image-generation route; do not use shell/status/no-op commands as placeholders. Do not locate, copy, move, preview, inspect, or summarize generated images between image calls. File handling waits until all requested image calls complete, except for a minimal `batch_progress.json` checkpoint after each returned `savedPath`.

Useful helpers:

```bash
python <skill_dir>/scripts/inventory_assets.py <asset_root> --md-out work/asset_inventory.md --json-out work/asset_inventory.json --ignore outputs --ignore output --ignore work
python <skill_dir>/scripts/prepare_project_batch.py <project_root> --out work/koda_batch --json-out work/asset_inventory.json --md-out work/asset_inventory.md --global-assets-per-scene 30
python <skill_dir>/scripts/make_asset_contact_sheet.py <project_root> --manifest work/koda_batch/scene_manifest.json --scene SC01 --out work/SC01_contact.jpg --max-images 24
python <skill_dir>/scripts/validate_project_batch.py work/koda_batch --mark-ready --write-dispatch-prompts
```

Contact sheets are secondary reference overviews, not storyboard deliverables.

## Project Batch Mode

Use Project Batch Mode when scripts, shot lists, and assets are stored in a shared project folder or when the user asks to generate storyboards by scene. The goal is to make the mixed project deterministic before image generation.

Recommended project shape:

```text
project_root/
  00_script/
  01_shotlist/
  02_assets/
    characters/
    environments/
    props/
    style_refs/
  work/koda_batch/
  outputs/storyboards/
```

If the user's folder is flat or mixed, do not require them to reorganize it before helping. Instead, create a batch scaffold in `work/koda_batch/` and record uncertainty.

### Batch Artifacts

Create or update these files before any image call for the requested batch:

- `scene_manifest.json`: canonical scene order, `scene_id`, title, source files, shot range, sheet count, status, and notes.
- `continuity_bible.md`: global locks for character identity, wardrobe, props, locations, time-of-day, weather/light, and cross-scene state changes.
- `scene_packets/SCxx.md`: per-scene source of truth with referenced script lines, shot list rows, required assets, uncertain assets, first/final state, and continuity locks.
- `prompt_plan.jsonl`: one JSON object per storyboard sheet with planned prompt data and deterministic `output_name`.
- `dispatch_prompts/SCxx_sheet_nn.txt`: one compact, ready-to-send prompt per storyboard sheet.
- `batch_progress.json`: resume ledger with `pending`, `running`, `done`, `failed`, returned paths, failure notes, and scene packet status.

Do not rely only on chat memory for paths or progress.
Use `validate_project_batch.py --mark-ready --write-dispatch-prompts` as the explicit gate from preflight to generation. If it fails, finish the listed TODO/scaffold/prompt-plan items before any image call.
After this gate passes, do not announce that generation will start and then continue planning. Read only the next pending sheet's dispatch prompt and immediately call `image_gen` for that sheet. If `image_gen` is unavailable or blocked after the prompt is read, report one blocker and stop; do not loop.

### Scene Parsing Rules

- Prefer explicit scene ids from filenames, headings, shot-list rows, or user notes: `SC01`, `Scene 01`, `场次01`, `第1场`, `S01`.
- `prepare_project_batch.py` scans both filenames/paths and source text scene headings. It reads text formats directly and attempts best-effort extraction for `.docx`, `.xlsx`, and `.pdf`; if extraction fails, fall back to filenames and mark the scene `needs_review`.
- The shorthand `S01` scene pattern is intentionally conservative: require at least two digits and a separator/start boundary to avoid matching paths such as `version_S1_final`.
- Keep script parsing conservative. Extract scene heading, location, time, characters, visible action, dialogue cues only when useful for action, and final state.
- Keep shot-list parsing conservative. Preserve shot numbers, shot size, camera movement, duration, action, characters, props, and notes.
- Never invent missing scenes to make a sequence feel complete.

### Scene-To-Asset Mapping

- Prefer explicit maps from scene packets, manifests, filenames, folder names, or user notes.
- Treat `characters`, `角色`, `人物`, `environments`, `场景`, `locations`, `props`, `道具`, `style`, and `reference` folders as strong hints.
- For each scene packet, list `confirmed_assets` and `uncertain_assets` separately.
- Ask before generation if an uncertain asset affects identity, location, wardrobe, or hero props.
- Contact sheets should be per scene or per category. Prefer `make_asset_contact_sheet.py --manifest <scene_manifest.json> --scene <SCxx>` for scene-level sheets. Increase `--max-images` only when the resulting sheet remains readable. Adjust `--global-assets-per-scene` when a project has many unassigned shared assets.

### Whole-Project Continuity

Maintain continuity across scene packets:

- Character: face/body silhouette, age, hair, wardrobe, accessories, injury/dirt/wetness, emotional baseline.
- Props: ownership, handoff state, damage, open/closed state, carried/not carried.
- Environment: geography, doors/windows, light source, weather, fire/smoke/wind, set dressing.
- Screen direction: travel direction, axis side, entrances/exits, camera side.
- Timeline: time of day, elapsed story time, state at the start/end of every scene.

If a later scene contradicts the continuity bible, update the bible only when the source material proves the change. Otherwise flag the contradiction.

### Batch Size And Resume

- Prefer generating one scene or a small scene range per batch.
- `prepare_project_batch.py` estimates sheet count from shot-count hints: 1 sheet for 1-3 shots, 2 sheets for 4-9 shots, and 3+ for longer scenes. Review and adjust `expected_sheet_count` before marking ready.
- For large projects, first create all batch artifacts, then generate only the requested scene range.
- To resume after a reconnect or stall, skip preflight if the batch still validates. Read `batch_progress.json`, choose the next `pending` or `failed` sheet, read its dispatch prompt once, and call `image_gen` directly. If the prior turn returned a `savedPath` but the ledger still says `pending` or `failed`, update the ledger first and do not reselect that sheet.
- After each returned `savedPath`, update or remember the completed sheet before selecting the next one. Prefer `update_batch_progress.py` for the checkpoint. After all image calls in a batch finish, copy/organize outputs and report failed or uncertain sheets.
- If generation fails, stop the current batch, mark the failed sheet, preserve completed paths in `batch_progress.json`, and resume later from pending/failed entries only.
- Re-running `prepare_project_batch.py` preserves existing `batch_progress.json` entries by default. Use `--reset-progress` only when intentionally discarding prior progress. Use `--overwrite-packets` only when replacing hand-filled packet content.
- When a packet is preserved, `packet_write_status` is recorded in `scene_manifest.json` and `batch_progress.json`; compare the manifest's updated `story_excerpt/source_spans` with preserved packets if source files changed.

## Full Action Inventory

```text
Existing shot setting:
[Summarize only the provided scene, shot, script, or visible references.]

Reference priority:
- Character identity source:
- Environment/geography source:
- Prop/effect source:
- Storyboard controls:

Storyboard mode:
- Commercial/product ad, performance/dance/kata, combat/chase/sports, procedural assembly/handwork, hidden-cut long-take illusion, horror/reveal, or custom:
- Mode-specific must-haves:
- Panel count and complexity budget:

Motion sufficiency:
- Shot class:
- Visible motion seeds:
- Missing action risk:
- Panel count decision:
- Forbidden filler:

Characters:
- [Name/role]: visible identity, movement/action language, start position, end position, body orientation, gaze, hand/foot action, emotional state.

Scene layout:
- Key anchors: doors, windows, table, seats, stove, stairs, corridor, props, foreground/background zones.
- Screen direction and axes:

Staging and blocking:
- Playable geography:
- Character lanes and zones:
- Entrances, exits, occluders, reaction positions:
- Prop handoff/contact positions:

Action chain:
P01: [initial state]
P02: [first micro-action]
P03+: [continue until motion is decomposed]
Final: [final state]

Panel purpose map:
Each panel must answer: what changed, why it matters, and what visual anchor carries continuity.

Camera plan:
- Shot size, lens/feel, camera height, movement, and function per beat.

State changes:
- Props, doors/windows, fire/smoke/wind/light, character posture, object position, room condition.
```

## Staging And Camera Grammar

- Establish playable geography before close-ups.
- Anchor the screen direction and camera side. If crossing the axis, bridge it with an overhead, master, or motivated turn.
- Move characters through named lanes/zones, not vague space.
- Track each important character's start, end, body orientation, gaze target, contact point, and exit/final hold.
- Assign camera function per beat: geography, travel, threat reveal, tactical path, hand/prop insert, reaction, contact, reversal, or payoff.
- Cut on carried motion: gaze, hand, object transfer, body lean, camera push, light trail, wind, crowd gap, or prop state.
- Show cause before effect. Every changed prop, open door, grabbed wrist, stolen object, or changed position needs setup/contact/reaction.
- For hidden-cut long-take illusions, name the wipe source: body occlusion, prop crossing lens, smoke burst, dust, wall impact, whip pan, darkness, etc.

## Mode Notes

- **Commercial/product**: setup, tension/problem, product reveal, interaction, transformation/impact, clean hero finish.
- **Performance/dance/kata**: prioritize body mechanics, foot plants, turns, drops, gestures, fabric/ribbon/fan trails.
- **Combat/chase/sports**: avoid dead-air poses; track attack line, defense line, contact, impact, recoil, recovery, next vector.
- **Continuous chase/FPV/parkour**: panels are beat divisions; preserve route and screen direction; use physical cues and occlusion.
- **Procedural assembly/handwork**: show every part placement, hand contact, tool use, component state, and final activation.
- **Horror/reveal**: track viewer knowledge, character knowledge, occluders, offscreen threat direction, reveal timing, final changed state.

## Character Identity Board

Create or request a character identity board only when identity needs locking and no stable sheet exists. If the user already has a useful character reference, use it directly.

Prompt shape:

```text
Create an artistic 16:9 CHARACTER IDENTITY BOARD.
Show the same character identity across hero pose, front/side/three-quarter view, expression range, outfit/silhouette lock, accessories, material, color, hair, face, body proportion, and style notes.
Use a pure white or soft off-white background.
All views must clearly be the same person. Do not redesign face, outfit, body type, hairstyle, age, or role.
This is a reference board for later storyboard and video generation, not a poster or final scene.
```

## Full Storyboard Prompt Additions

Use the lightweight prompt from `SKILL.md`, then add only the relevant advanced sections:

```text
[REFERENCE PRIORITY]
角色参考 locks face, body, wardrobe, proportions, silhouette, hero props.
环境参考 locks location style, geography, lighting family, spatial anchors.
故事板控制 locks staging, motion, camera progression, rhythm, state changes, panel purity.

[CONTINUITY LOCKS]
Lock identity, wardrobe, hero prop, environment geography, screen direction, first-frame state, final state, and allowed changes.

[STYLE / EFFECT / ENVIRONMENT LOCKS]
Separate rough storyboard style from final video style. State allowed effects and what they cannot change.

[SPATIAL CONTINUITY LOCK]
Name recurring anchors, route, camera side, screen direction, and allowed changes.

[EMOTIONAL ARC]
Describe visible posture/reaction progression.
```

## Video Handoff Template

```text
INTENT:
[One concise sentence describing the sequence purpose.]

STYLE:
[Final render style, more polished than the rough storyboard.]

WORLD / ENVIRONMENT:
[Location, mood, lighting, geography, and state transition.]

REFERENCES:
Use @[character sheet] as the authoritative character identity reference.
Use @[environment ref] as the environment/style reference when available.
Use @[storyboard control sheet] as the director-approved storyboard blueprint, shot guide, camera guide, pacing map, choreography reference, action-path map, blocking map, and scene-state map.

Do not render the storyboard control sheet itself.
Exclude all panel borders, text, labels, headers, swatches, director-strip graphics, masthead graphics, arrows, guide marks, path lines, axes, and page layout elements from the final video.

Treat each storyboard panel as one sequential cinematic shot or motion beat. Do not treat the sheet as one single image.
Follow the storyboard panel order and director strip. Translate rough panels into the intended final style.
Interpolate natural motion between panels while preserving prop states, effect states, screen direction, and continuity.
Do not invent alternative coverage, new characters, unrelated props, changed wardrobe, changed identity, different locations, new major actions, or alternate camera setups.

VISUAL APPROACH:
[Readability, screen direction, continuity, shot scale, staging, effects, materials, lighting shifts, motion motifs.]

SEQUENCE BEHAVIOR:
[Panel-by-panel action, blocking, camera progression, action path, rhythm track, state changes, emotional arc.]

CONTINUITY LOCKS:
[Identity, costume, hero prop, geography, screen direction, motion path, final state.]
```

## Advanced Preflight

- Existing shot setting is source of truth.
- Motion sufficiency is classified and panel count is justified.
- Character sanitization removes invisible psychology and keeps visible identity/action language.
- Playable geography, lanes, entries/exits, occluders, camera side, and screen direction are clear.
- Every panel has an in-panel action/camera/blocking mark.
- Bottom tracks summarize purpose, continuity anchor, beat, camera path, action path, rhythm, state, and style.
- Project batches have scene packets, global continuity locks, scene-to-asset mapping, deterministic output names, and resume status before image generation.
- Video handoff excludes storyboard page graphics and translates rough marks into final video style.
