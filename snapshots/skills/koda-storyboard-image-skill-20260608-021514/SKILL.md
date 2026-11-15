---
name: koda-storyboard-image
description: "Run Koda/@aimikoda-style storyboard-to-video and previs workflows. Use when Codex should split a shot into an annotated rough-sketch storyboard control sheet, create static or low-action continuity boards, prepare storyboard-to-video controls, generate Seedance handoff prompts, or batch storyboard scenes from a project folder containing scripts, shot lists, and visual assets. Default to Light Mode for single shots. Use Project Batch Preflight before multi-scene batches or mixed script/shotlist/asset folders. Storyboard image requests are image-generation requests: call image_gen directly when it is exposed after required preflight. Never downgrade to prompt-only unless the user asks for prompt-only or an actual image_gen call fails. Never produce a single cinematic frame, separate keyframes, polished shot cards, random filler panels, or detailed concept images as the storyboard."
---

# Koda Storyboard Image

## Default Mode

Use **Light Mode** by default for a single shot or one clearly prepared scene. A storyboard is a fast video-control artifact, not a full production bible. Optimize for speed and usability:

- Keep planning compact and mostly internal.
- Focus on action beats, scene layout, character blocking, camera path, continuity anchors, and state changes.
- Put scene layout, role movement, action direction, and camera motion inside the panels with concise arrows/labels.
- Use the bottom director strip as a summary, not as the only control layer.
- Do not write a Seedance/video handoff unless the user asks.
- Do not read advanced references unless the request explicitly needs them.

Read [references/advanced-workflow.md](references/advanced-workflow.md) only for Project Batch Mode, full Koda workflow, Seedance handoff, asset-grounded continuity plans, complex multi-character choreography, procedural assembly/handwork, character identity boards, or detailed prompt-only deliverables.

## Product Contract

For a storyboard image, generate one complete 16:9 Koda-style rough-sketch storyboard previs/control sheet:

- Top masthead.
- Sequential panel grid with headers.
- In-panel control annotations.
- Bottom director strip/control tracks aligned to panel columns.

Do not generate separate keyframes, a single shot card, a triptych, polished storyboard thumbnails, concept art, or a contact sheet. If the result reads that way, revise and regenerate.

If the user gives an existing shot or scene, preserve it as the source of truth: setting, axis, characters, props, first state, and final state. Do not invent new plot events, new props, new characters, or unrelated coverage.

## Light Workflow

1. Inspect only the user-provided shot text and essential reference assets. Skip folder inventory unless many assets or unclear identity make it necessary.
2. Run the Motion Sufficiency Gate.
3. Build the Compact Action Inventory.
4. Generate with the Lightweight Prompt Template through `image_gen`.
5. Return the generated storyboard. Keep the final response short.

Do not switch to prompt-file output for normal storyboard image requests. Save a prompt artifact only when the user explicitly asks for prompt-only output, or after an actual `image_gen` tool call fails and no image generation route remains. Do not fabricate SVG/HTML/vector placeholders unless the user asks for those formats.

## Project Batch Preflight

Use **Project Batch Preflight** before image generation when the request involves multiple scenes, a project folder, mixed scripts/shotlists/assets, "batch by scene", "all scenes", or unclear asset identity. Do not treat a mixed folder as a ready storyboard prompt.

Before the first image call:

- Read [references/advanced-workflow.md](references/advanced-workflow.md).
- Inventory and scaffold the project folder once when needed. Prefer `prepare_project_batch.py` with `--json-out/--md-out` so the folder is not scanned twice:

```bash
python <skill_dir>/scripts/prepare_project_batch.py <project_root> --out work/koda_batch --json-out work/asset_inventory.json --md-out work/asset_inventory.md --global-assets-per-scene 30
```

- Use `inventory_assets.py` separately only when no batch scaffold is needed:

```bash
python <skill_dir>/scripts/inventory_assets.py <project_root> --md-out work/asset_inventory.md --json-out work/asset_inventory.json --ignore outputs --ignore output --ignore work
```

- Build or verify these artifacts before generation:
  - `scene_manifest.json`: ordered scenes, scene ids, source files, expected sheet count, status.
  - `continuity_bible.md`: cross-scene character identity, wardrobe, hero props, environment state, time of day, screen direction, and allowed changes.
  - `scene_packets/SCxx.md`: one scene packet per scene with shot range, story action, characters, environment, props, asset paths, first/final state, and continuity locks.
  - `prompt_plan.jsonl`: one planned storyboard sheet per line with `scene_id`, `sheet_id`, `shot_range`, `output_name`, `asset_refs`, and compact prompt notes.
  - `dispatch_prompts/SCxx_sheet_nn.txt`: one compact prompt per sheet, written by validation for immediate `image_gen` dispatch.
  - `batch_progress.json`: pending/running/done/failed status and returned output paths after generation.
- Fill scene packets, the continuity bible, and every `prompt_plan.jsonl` row until no `[TODO...]`, `[fill...]`, `packet_status: scaffold`, `continuity_status: scaffold`, blank `shot_range`, blank `asset_refs`, or placeholder `prompt_notes` remain. Then validate readiness:

```bash
python <skill_dir>/scripts/validate_project_batch.py work/koda_batch --mark-ready --write-dispatch-prompts
```

- If scene-to-asset mapping is missing or ambiguous, infer only from clear filenames/folders and mark uncertain assets in the scene packet. Ask for clarification before generation if the ambiguity would change character identity, location, or hero props.
- The scaffold helper reads text formats directly and attempts best-effort extraction for `.docx`, `.xlsx`, and `.pdf`; if document extraction fails, fall back to filenames plus user-visible source notes.
- Prefer processing one scene or a small scene range per generation batch. For a whole project, prepare the manifest first, then generate scene batches incrementally so failed scenes can resume.
- Do not start `image_gen` until `validate_project_batch.py --mark-ready` passes for the requested batch, or the user explicitly asks to generate from a reviewed partial batch.
- Run inventory/scaffold/validation helpers at most once per dispatch attempt. If a helper times out or a turn reconnects, inspect the existing output files before rerunning it, and do not start duplicate scans or duplicate image-generation processes.

## Image Tool Availability Gate

Before reading any dispatch prompt for generation, choose one image route:

- If the built-in `image_gen` tool is exposed in the active tools, use that route.
- If no built-in image tool is exposed and a local image-generation CLI fallback is intentionally available, verify credentials once before dispatch and run exactly one foreground CLI generation for the selected sheet.
- If neither route is available, stop before reading dispatch prompts and report one concise blocker. Do not enter dispatch mode and do not create prompt-only output unless the user asked for prompt-only.
- Do all tool discovery or fallback checks before reading a dispatch prompt. Once the dispatch prompt is read, do not run `tool_search`, shell probes, or availability checks; call the chosen image route or stop with the blocker.

## Image Dispatch Gate

Use this gate for every Project Batch or multi-sheet run. It exists to avoid long "thinking" stalls between validation and the first image call.

- Validation must write `dispatch_prompts/<sheet_id>.txt` before generation. If the prompts are missing, run `validate_project_batch.py --mark-ready --write-dispatch-prompts` again after fixing the packet/plan blockers.
- After validation passes, select exactly one next pending sheet from `batch_progress.json`, normally the first `pending` or `failed` entry in requested order.
- Read only that sheet's compact dispatch prompt. Do not re-read the full project, re-open assets, re-summarize packets, or compose prompts for later sheets at this point.
- The next assistant action after reading the dispatch prompt must be the real `image_gen` tool call for that sheet. This is literal: do not send a prose-only "I will now generate" status message, do not run `shell_command`, and do not emit `Write-Output`/echo/no-op marker commands.
- For "generate all" or "batch" requests, repeat this one-sheet dispatch loop after each image returns: update/remember the completed path, pick the next pending sheet, read its dispatch prompt, call `image_gen`.
- If the turn reconnects, stalls, or resumes after validation, do not redo preflight. Resume from `batch_progress.json` and dispatch the next pending sheet directly.
- Keep each dispatch prompt compact. Use the prompt file as the source of truth and add only a short missing detail if the user explicitly supplied it after validation.

### Hard Dispatch Stop

After a dispatch prompt has been read, the only valid next tool call is `image_gen`.

- Do not use `shell_command`, `view_image`, `tool_search`, file reads, folder scans, path checks, or empty/status commands between reading the prompt and calling `image_gen`.
- Never use shell output such as "calling image_gen", "...", or "image_gen call follows" as a placeholder for the image tool.
- If `image_gen` is not exposed or the interface prevents the tool call, stop immediately with one concise blocker message. Do not loop, do not keep saying the call is starting, and leave `batch_progress.json` unchanged.
- If an image call returns a `savedPath` or visible generated image even while the wrapper status still says `generating`, treat that sheet as generated and move on to the next dispatch step.
- After a sheet returns a `savedPath`, mark or remember that exact sheet as complete before selecting the next sheet. A minimal `batch_progress.json` checkpoint update is allowed here; do not reselect the same sheet just because the old progress file still says `failed` or `pending`.
- Prefer the checkpoint helper for progress updates: `python <skill_dir>/scripts/update_batch_progress.py <batch_dir> --sheet-id <sheet_id> --status done --output-path <path> --print-next`.
- On resume after a stall, read at most `batch_progress.json` and the one next dispatch prompt once; the next action after that read is `image_gen` or a blocker message.

### Local CLI Fallback Safety

Use a local image-generation CLI only when the built-in `image_gen` route is unavailable and the user/session has a working local credential path.

- Run CLI generation in the foreground with a clear output path and a finite timeout. Do not use `Start-Process`, background jobs, or hidden long-running helpers for image generation.
- If the CLI command times out, check for a still-running process and for the expected output file once before retrying.
- Do not launch a second CLI generation for the same sheet while an earlier process is still alive.
- If credentials are missing, stop with that blocker; do not loop through retries or produce a prompt-only artifact unless the user asked for it.

## Batch Throughput

Use **Batch Mode** when the user asks for many sheets in one round, says batch/all/continue without stopping, or asks to group a scene into several storyboard sheets.

- Plan the exact sheet count first. Do not over-split. For a 9-shot scene grouped around 15 seconds, default to 2 sheets unless actual timing clearly requires 3.
- For 2-sheet scene work, use a natural split such as shots 1-4/5 and shots 5/6-9, based on story/action transition.
- For multi-scene projects, Batch Mode applies to the requested scene batch after Project Batch Preflight, not to an unprocessed mixed folder.
- In Batch Mode, call `image_gen` once per sheet, using the Image Dispatch Gate for every sheet.
- Before the first image call, finish all required reading, asset inspection, grouping, prompt planning, and dispatch-prompt writing. After validation passes, the batch is in one-sheet dispatch mode.
- Do not locate, copy, move, preview, view, open, inspect, or search generated files between image calls. Store returned paths mentally and continue to the next `image_gen` call.
- Do not run shell commands, file reads, folder scans, image previews, or path discovery between image calls unless an image call actually fails and the failure requires diagnosis.
- If you say "continue generating sheet 2" or similar, the next actions must be reading the sheet 2 dispatch prompt and calling `image_gen`, not file management, analysis, status narration, or shell markers.
- Do all file discovery/copying/saving only after every requested image call has completed.
- Keep batch prompts shorter than single-sheet prompts: fewer prose notes, 4-7 panels per sheet when possible, compact in-panel labels, and a short bottom strip.
- If one image call actually fails, stop the batch and report which sheet failed. Do not silently switch to prompt-only output.
- After a batch finishes or fails, update `batch_progress.json` and organize outputs by `outputs/storyboards/<scene_id>/<scene_id>_sheet_<nn>.<ext>` when file handling is allowed.

## Motion Sufficiency Gate

Classify the shot before prompt writing:

- **Actionful**: visible character/object/environment changes support 8-12 beats.
- **Low-action establishing**: mostly geography, mood, props, surveillance, or static tension; use 5-7 purposeful beats.
- **Static hold**: no meaningful visible motion beyond atmosphere/camera hold; use 3-5 beats or ask for one motion intention.

For low-action/static shots:

- Use only existing motion seeds: camera hold/push/pan/tilt, screen glow/flicker, window light, smoke/fire/wind/fabric movement, gaze/posture/hand shift, prop contact/state, or final hold.
- Give every panel a purpose: establish geography, confirm axis, reveal prop, show micro-action, show environment change, confirm state, or final hold.
- Carry a visible anchor from panel to panel: same desk edge, window/door axis, character silhouette, prop position, light source, or screen direction.
- Do not force 8-12 panels. Never pad weak action with random inserts, repeated room views, alternate angles, or filler.

Ask for one concise motion intention only before generation begins, and only when the user expects video but the shot has no usable motion seed. During Batch Mode, do not stop between sheets to ask; infer minimal camera/environment motion from the provided shot description.

## Compact Action Inventory

Use this compact form internally or as a short visible note when useful:

```text
Existing shot:
[one sentence]

Motion sufficiency:
[actionful / low-action establishing / static hold], [panel count], [motion seeds]

Action chain:
P01 [beat] -> P02 [beat] -> P03 [beat] -> ... -> Final [state]

Scene / blocking / camera:
[spatial anchors], [character lanes/start/end], [camera path], [screen direction]

Continuity anchors:
[identity/wardrobe], [key props], [room geography], [prop/effect state], [final state]
```

## Annotated Panel Rules

Default to annotated previs panels, not clean visual-only panels.

Inside each panel, draw concise production marks:

- Scene anchors: doors, windows, table, path, foreground/midground/background, occluders.
- Character blocking: start/end dots, lanes, body direction, gaze, hand/foot contact.
- Action controls: route arrows, action arrows, prop handoff/contact, state change marks.
- Camera controls: push/pan/tilt/track arrows, camera axis, entry/exit marks.

Keep in-panel labels short: `A`, `B`, `入口`, `桌`, `窗`, `遮挡`, `推`, `路线`, `手`, `视线`, `道具`, arrows, and simple path symbols. Put long notes in headers or the bottom strip.

The bottom director strip should summarize: `目的线`, `连续锚点`, `节拍线`, `镜头路径`, `动作路径`, `节奏转折`, `状态轨`. It must not be the only place where blocking/action/camera information appears.

Failed storyboard signs:

- The panel art has no in-panel scene/blocking/action/camera marks.
- Information exists only in the bottom table.
- Middle panels are unrelated coverage options rather than consecutive time.
- Inserts appear without setup/payoff.
- A panel has no visible change, inherited anchor, or purpose.
- The board cannot be translated into a continuous video plan.

## Lightweight Prompt Template

Use this template by default and keep it concise:

```text
Create one 16:9 Koda-style annotated rough-sketch Storyboard Previs Control Sheet.
This is a lightweight video-control storyboard, not polished keyframes, not a cinematic frame, not separate shot cards.

Layout:
- Top masthead: title, shot id, lens/camera note, continuity note.
- Middle grid: [PANEL_COUNT] sequential rough thumbnail panels with in-panel scene/blocking/action/camera annotations.
- Bottom director strip aligned to panel columns with rows: 目的线, 连续锚点, 节拍线, 镜头路径, 动作路径, 节奏转折, 状态轨. The strip summarizes the panel marks; it is not the only control layer.

Existing shot:
[Use only the supplied setting/references. Preserve geography, characters, props, screen direction, first state, final state.]

Motion sufficiency:
[actionful / low-action establishing / static hold]
Panel count: [count justified by real motion]
Motion seeds: [camera movement, character movement, prop/effect/environment state changes]
Forbidden filler: no random inserts, no repeated room views, no unrelated angle variety, no new props, no new plot events.

Action chain:
P01: [beat, purpose, continuity anchor]
P02: [beat, purpose, continuity anchor]
P03: [beat, purpose, continuity anchor]
P04+: [continue only real connected beats]
Final: [final visible state]

Scene layout and blocking:
[Key spatial anchors: doors/windows/table/paths/foreground/midground/background.]
[Character start/end zones, body direction, gaze/hand/foot action.]

Camera plan:
[Shot size, lens feel, camera height, fixed/push/pan/track/cut plan, screen direction.]

Panel rules:
Each panel is one time beat, not a new illustration.
Every panel must show what changes, why it matters for video, and which anchor continues from the previous panel.
Inside each panel, add concise production marks: scene anchors, character start/end dots, route arrows, action arrows, gaze/hand/prop contact marks, camera push/pan/track arrows, axis line, and entry/exit marks.
Headers stay outside panel art: `P01 / lens / short Chinese beat`.
Panel art stays low-detail monochrome rough sketch with simple blocking figures, props, spatial anchors, and readable state changes.

Style:
Clean off-white production board, sparse grayscale sketch thumbnails, simple silhouettes, readable geography, compact Simplified Chinese labels, no rich rendering, no cinematic lighting, no polished storyboard frames.
```

## Output Policy

- For storyboard-only image tasks, generate the storyboard image. Do not provide only a prompt artifact unless the user explicitly asks for prompt-only output or a real `image_gen` call fails.
- For project-folder or multi-scene requests, complete Project Batch Preflight before generation. Do not generate directly from a mixed folder without a scene manifest and scene-to-asset mapping.
- For multi-sheet requests, use Batch Mode when the user asks to generate them in one round. Plan the count, write dispatch prompts, then call `image_gen` once per sheet without doing file operations between calls.
- Prefer the minimum necessary sheet count. For a 9-shot scene at roughly 15-second grouping, target 2 storyboard sheets unless the shot table proves a longer duration.
- After the first image in a batch returns, continue to the next image dispatch immediately. Do not detour into locating filenames, copying outputs, previewing the image, or summarizing quality.
- If `image_gen` is exposed in the active tools, call it after required preflight. Do not claim image generation is unavailable without attempting the exposed tool.
- Do not simulate an image-generation call with `shell_command`, `Write-Output`, echo, empty commands, or status text. If the image tool cannot be called, report that blocker once and stop.
- If no image tool is exposed in the active tools, ask the user whether they want a prompt-only artifact; do not silently create one.
- Do not add a Seedance prompt, full reference plan, full Action Inventory, or long continuity report unless requested.
- For full workflow tasks, read [references/advanced-workflow.md](references/advanced-workflow.md), then return the requested artifacts.
- For video-only tasks with an existing storyboard, skip storyboard generation and produce the handoff prompt from the advanced reference.

## Quick Check

Before generation, verify:

- Light Mode is appropriate, or advanced workflow was explicitly requested.
- For project batches, the scene manifest, continuity bible, scene packets, prompt plan, output naming, and resume status file are ready before generation.
- For project batches, `dispatch_prompts/<sheet_id>.txt` exists for the next pending sheet before the first `image_gen` call.
- The shot class and panel count match real motion.
- The prompt includes action chain, scene layout, character blocking, camera path, continuity anchors, and annotated panel rules.
- For Batch Mode, every planned sheet has a compact dispatch prompt before the first `image_gen` call, and no file operations are scheduled between image calls.
- Scene layout, character movement, action direction, and camera motion appear inside panels, not only in the bottom director strip.
- The storyboard is rough-sketch previs/control, not a polished frame or keyframe sheet.
