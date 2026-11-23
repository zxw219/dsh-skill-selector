---
name: score-and-mix-picture
description: 看画配乐与混音工具：分析锁定画面，制作带时间码的音乐与音效点位，编写AI音乐提示词，选择本地音效并完成声画同步剪辑与混音。用于成片配乐、音效设计和最终混音。
version: 1.0.0
---

# Score And Mix Picture

## Core Contract

Turn locked picture into a repeatable two-pass audio workflow:

```text
picture evidence -> music/SFX spotting map -> score strategy -> generation prompt
returned music + licensed SFX -> edit map -> dialogue-safe mix -> verified audio masters
```

Treat music as narrative structure, not wallpaper. Preserve useful silence, source sound, dialogue, and sound effects. Do not promise a finished mix until the rendered files have been probed and checked against picture duration.

## Runtime Requirements

- Python 3.10 or newer; bundled scripts use only the standard library.
- FFmpeg and FFprobe available on `PATH` for probing, editing, loudness measurement, and WAV rendering.
- A host capability that can inspect video frames and audio/transcript semantics. If the host cannot watch video, require a timecoded shot list/transcript and state that semantic picture analysis is limited.
- No external Skill or MCP server is mandatory. Optional host video-understanding, music-generation, and NLE tools may improve execution.

## Route The Request

1. **Picture only**: analyze it and deliver a timecoded music/SFX spotting plan, 1 primary music direction, up to 2 materially different alternatives, and paste-ready music-generation prompts.
2. **Picture plus returned music**: inspect both, select only evidence-backed local SFX when useful, create a concrete mix plan, render, verify, and deliver the audio masters.
3. **End-to-end with a connected music generator**: complete the analysis first, submit the approved or clearly inferred prompt, wait for the audio result, then continue through the mix phase.
4. **No generator is available**: stop after the prompt package and tell the user exactly which audio file or stems to return. Do not pretend generation occurred.
5. **Editable NLE project requested**: use the available editor adapter for timeline placement and keep the music editable. Use the bundled renderer only for audio masters or when no editor is requested.

## Phase 1 — Inspect Locked Picture

1. Confirm the target video path or active editor timeline. Treat the current cut as timing truth.
2. Run the technical probe:

```powershell
python scripts/probe_media.py "<picture>" --output "<work>/picture-report.json"
```

3. Watch the complete video with time awareness. Use the host's video-understanding capability; if an optional `$watch` Skill is installed it may serve this role. Inspect frames, original audio, transcript/dialogue, action, scene changes, transitions, and the ending. A scene-cut list alone is not semantic analysis.
4. Record evidence in chronological order:
   - story/communication purpose;
   - point of view and emotional turn;
   - dialogue and source-sound priority;
   - major visual beats, reveals, impacts, transitions, and final button;
   - no-music zones and deliberate silence;
   - uncertainty caused by missing/inaudible material.
5. Read [references/spotting-and-prompt-contract.md](references/spotting-and-prompt-contract.md) and [references/scoring-knowledge-base.md](references/scoring-knowledge-base.md) before writing the cue map or prompts.

## Phase 2 — Design The Score

Use the bundled scoring knowledge and spotting contract as the musical judgment layer. If an optional `$cinematic-music-sound-design` Skill is installed, use it as an additional specialist reference rather than a dependency.

1. State the score's dramatic job in one sentence.
2. Decide whether the picture needs one evolving cue, several cues, source music, sound-design-led rhythm, or intentional silence.
3. Attach changes to story beats rather than every cut.
4. Define only the controls that matter: duration, structure, BPM or tempo behavior, meter, tonal center/mode, harmonic tension, motif, instrumentation, register, texture, dynamics, production space, ending behavior, and stems.
5. Protect dialogue and important effects by controlling density, register, transients, and reverb—not only by lowering overall volume.
6. Provide:
   - a timecoded spotting table;
   - the primary direction and alternatives with tradeoffs;
   - a full prompt and a compact prompt;
   - exclusions/avoidances in a separate field;
   - requested delivery format: preferably WAV, 48 kHz, 24-bit; request stems when the cue has dialogue-heavy passages or major structural changes.

Do not cite composer names as the whole solution. Translate every reference into audible mechanics.

## Phase 2A — Design And Select Sound Effects

Read [references/sfx-editing-playbook.md](references/sfx-editing-playbook.md).

1. Determine whether the existing production audio is final. Do not duplicate finished footsteps, impacts, ambience, or transitions.
2. Build an SFX spotting list from visible/audible evidence: exact timecode, source/material/action, scale, perspective, foreground owner, and intended tail.
3. Search the bundled CC0 library before downloading anything new:

```powershell
python scripts/search_sfx.py "<Chinese or English description>" --limit 8
```

4. Audition candidates against picture. Filenames and tags are only search aids.
5. Prefer physical specificity over generic magnitude. Use silence and source sound before adding decorative whooshes/booms.
6. Record each selected effect as an `sfx` entry in the mix plan. Keep new downloads provenance-complete and rebuild the catalog with `scripts/build_sfx_catalog.py`.

## Phase 3 — Accept And Inspect Returned Music

1. Reuse the original picture from the same task when its identity is certain; otherwise request the exact picture.
2. Probe every returned audio file. Check duration, channels, sample rate, clipping risk, leading/trailing silence, audible artifacts, usable sections, and whether the intended ending exists.
3. Audition against the picture. Mark:
   - source-in/source-out for each usable passage;
   - timeline start and intended duration;
   - musical bar/phrase boundaries;
   - hit points, transitions, ramps, drops, pauses, and tail;
   - gain, fades, overlaps, and dialogue-sensitive zones.
   - which existing production effects must remain foreground and which bundled SFX may support them.
4. Prefer musical phrase edits, repeated cells, stems, or generated alternates over arbitrary mid-note cuts. Do not time-stretch beyond roughly ±5% without a clear reason; prefer re-editing or regenerating when the music's form fundamentally misses the picture.
5. If the returned track is unusable, explain the exact structural failure and issue a corrected prompt instead of forcing a bad mix.

## Phase 4 — Build And Render The Mix

Create a JSON plan from [references/mix-plan.example.json](references/mix-plan.example.json). Paths may be absolute or relative to the plan file.

```powershell
python scripts/render_picture_mix.py "<mix-plan.json>" --output-dir "<deliverables>"
```

The renderer creates:

- `music-edit.wav`: score only, exactly aligned to picture duration;
- `sfx-edit.wav`: optional sound-effect stem, exactly aligned to picture duration;
- `full-mix.wav`: original picture audio plus dialogue-aware ducked music;
- `mix-report.json`: inputs, decisions, probes, loudness pass data, durations, and SHA-256 hashes.

When `sfx` entries exist, `full-mix.wav` includes original audio, ducked music, and the SFX stem.

Use multiple `music` entries for separate cues or alternate sections from one file. Use `loop: true` only for genuinely loopable material. Keep headroom through editing; normalization happens on the music bus and final mix.

If a timeline editor is active, reproduce the same edit map with editable clips/fades/levels, then export the requested masters. Do not replace an explicitly requested editable timeline with only a flattened local render.

## Phase 5 — Verify Before Delivery

1. Confirm both masters open and contain audio.
2. Confirm duration differs from picture by no more than 20 ms.
3. Check the opening, every cue/SFX boundary, every major hit point, dialogue-dense passages, and the ending.
4. Check for clicks, clipped words, pumpy ducking, phase problems, abrupt tails, unintended silence, and loudness jumps.
5. Compare `music-edit.wav`, optional `sfx-edit.wav`, and `full-mix.wav`; dialogue and important source effects must remain intelligible.
6. Deliver the files and summarize only the consequential creative decisions and any unresolved limitation.

## Adapter Boundary

Keep musical method independent from tools. Read [references/tool-adapters.md](references/tool-adapters.md) when selecting or replacing video inspection, music generation, SFX library, editor, or render tools. Use [references/compatibility-results.json](references/compatibility-results.json) as the current adapter regression baseline and [references/research-sources.md](references/research-sources.md) when auditing the knowledge/measurement sources. A successful tool call is not evidence that the score works.

## Failure Boundaries

- Do not infer semantic story beats from metadata alone.
- Do not generate wall-to-wall music by default.
- Do not decorate every cut with a whoosh, riser, glitch, or boom.
- Do not force music to every visual cut.
- Do not overwrite source media.
- Do not mix from a lossy preview when a WAV master or stems are available.
- Do not claim dialogue ducking if the picture has no original audio or the user supplied only a silent picture.
- Do not finalize from prompts alone; the music-return phase is a separate execution stage.
