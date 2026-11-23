# Spotting And Prompt Contract

## 1. Evidence First

Separate what is visible/audible from interpretation.

```text
Observed: 00:12.400 subject stops; dialogue ends; cut to a wide empty space.
Inferred function: release, isolation, or a reveal of scale.
Music decision: let the dialogue clear, then widen harmony after the cut.
```

Do not assign emotional meaning when the picture does not support it. Mark uncertainty and provide a conservative option.

## 2. Spotting Table

Use one row per meaningful musical phase, not per shot.

| Time | Picture / sound evidence | Dramatic function | Music action | Sync or transition | Dialogue priority |
|---|---|---|---|---|---|
| 00:00.000–00:04.800 | Concrete visible/audible event | What the audience should feel/understand | Enter, hold, transform, drop, or remain silent | Exact hit point or bridge | High / medium / low |

Always include:

- cue-in and cue-out;
- no-music zones;
- selective hit points;
- the ending type: hard button, decay, unresolved sustain, ring-out, or silence;
- total picture duration and required music delivery duration.

## 3. Primary Direction

Write the recommendation in this order:

1. **Narrative job** — what the score changes in the viewing experience.
2. **Identity** — musical world and recording/production perspective.
3. **Motion** — tempo range, pulse, meter, subdivision, and density curve.
4. **Harmony/motif** — tonal center, tension behavior, interval or contour.
5. **Orchestration** — instruments, register, articulation, acoustic/electronic relation.
6. **Structure** — exact time ranges and formal changes.
7. **Mix space** — dialogue pocket, bass discipline, transient priority, reverb depth.
8. **Ending** — exact final gesture and tail length.

Alternatives must change the dramatic interpretation, not merely swap instruments.

## 4. AI Music Prompt Package

### Full prompt fields

```text
Purpose and exact duration:
Picture narrative and point of view:
Timecoded structure:
Musical identity:
Tempo / meter / rhythmic engine:
Harmony / tonal center / motif:
Instrumentation / register / articulation:
Texture / dynamics / production space:
Dialogue-safe arrangement requirements:
Ending behavior and tail:
Requested deliverables and stems:
```

Then provide one paste-ready paragraph that contains the actual audible instructions. Keep exclusions outside that paragraph unless the target platform exposes a dedicated exclusion field.

### Compact prompt

Compress to:

```text
duration + narrative function + timecoded form + tempo behavior + harmony/motif + core timbres + dynamic arc + dialogue pocket + ending
```

### Exclusion field

List only failure-prone properties relevant to this picture, for example:

- no wall-to-wall percussion;
- no oversized trailer braams;
- no busy lead melody under dialogue;
- no four-on-the-floor pulse if it fights the edit;
- no long reverb tail over a hard final button.

Avoid generic negative lists.

## 5. Returned-Music Edit Map

Create a row for each timeline instance:

| Cue | Source file | Source in/out | Timeline in/out | Edit reason | Fade | Gain | Dialogue note |
|---|---|---|---|---|---|---|---|

Rules:

- Cut at phrase, bar, cadence, breath, texture change, or clean transient boundary.
- Crossfade tonal/ambient material; use short equal-power-like fades for rhythmic material.
- Hide unavoidable edits under picture transitions, impacts, hard effects, or intentional silence.
- Preserve the final cadence when possible; otherwise request or generate an ending/button.
- Prefer stems for dialogue-heavy passages: reduce melody/percussion before crushing the full mix.

### SFX event map

| Timecode | Visible/audible evidence | Source/material/action | Perspective | Library candidate | Gain/tail | Foreground owner |
|---|---|---|---|---|---|---|

Do not approve a candidate from metadata alone. Audition it in context and record the final file path in the mix plan.

## 6. Mix Targets

Treat targets as defaults, not universal law:

- session/output: 48 kHz, stereo, 24-bit PCM WAV;
- music-only target: about -18 LUFS integrated, true peak at or below -1 dBTP;
- web full mix target: about -14 LUFS integrated, true peak at or below -1 dBTP;
- filmic/high-dynamic delivery may use a lower integrated loudness when requested;
- duration tolerance against picture: 20 ms;
- dialogue remains the foreground whenever it carries story information.

The bundled renderer uses two-pass EBU loudness normalization. Loudness compliance does not replace listening.

## 7. Completion Gate

The work is complete only when:

- the picture was semantically watched;
- cue decisions have timecodes and dramatic functions;
- prompts specify form and ending, not only mood/genre;
- returned music was auditioned and edited on musical boundaries;
- sound effects trace to visible/audible evidence and licensed source records;
- the score-only and full-mix masters match picture duration;
- hashes and probe results exist in `mix-report.json`;
- sync, dialogue, boundaries, and ending were checked.
