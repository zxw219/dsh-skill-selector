---
name: seedance-audio
description: Seedance声音工具：规划对白、旁白、环境声、拟音、音乐、节奏和声画同步要求。用于Seedance原生音频或需要明确声音叙事的视频生成任务。
version: 6.2.0
---

# seedance-audio

Use this for dialogue, lip-sync, sound layers, music, ambience, beat-sync, audio-reference mapping, desync troubleshooting, or sound-driven visual timing. Audio should support the visible beat instead of becoming a second competing prompt.

Load `[ref:audio-guide]` for detailed constraints, beat-sync, desync repair, audio-reference conflicts, and multi-character workarounds. Load `[ref:reference-audio-visual-control]` when reference audio should shape visible action speed, impact peaks, cuts, shot scale, or section rhythm through a custom cue track or fixed music. Load `[ref:audio-post-delivery]` when the user needs stems, M&E, dubbing, loudness, sync, mix, or delivery guidance.

## Intent

Half of every emotion enters through the ears, and users almost always forget sound until its absence makes the clip feel dead. The soul here is giving every scene its sound before being asked - the room's breath, the action's evidence, the line that lands. When they hear it, they realize it was always part of what they meant.

## Core Rules

Keep dialogue short, quote spoken lines, and assign every line to a named speaker. Prefer locked or stable framing for lip-sync. Remove head-turning, large face motion, extreme camera moves, or busy hand gestures while mouth accuracy matters. Treat `[Audio1]` as a rhythm, pacing, mood, voice-tone, ambience, or tested visual-timing condition unless the active platform documents exact playback behavior. Never turn a field-observed sound-to-picture tendency into a deterministic cue dictionary.

When the user already supplies the fixed final song and asks for a complete music-video cut map, `$reference-track-mv-director` owns the picture structure, choreography, formation changes, shot scale, edits, and final button. This Skill owns only the platform audio role, upload/binding language, leakage handling, and empirical A/B. Do not create a second control WAV that competes with the fixed song unless a one-variable diagnostic explicitly requires it.

## Prompt-time Reference Audio Gate

When Liu asks for a final video prompt, decide backstage whether a reference-audio control track materially improves the result. Do not wait for him to ask for the audio separately.

Create the track together with the prompt when at least one condition is true:

- the clip needs selective impact, dash, transformation, reveal, edit, or shot-scale peaks at named moments;
- music section changes are meant to control the visual arc or exact ending;
- a multi-beat action, chase, PV montage, dance, ritual, or transformation has a fixed target duration and text-only timing is likely to remain soft;
- a prior attempt ignored, reordered, or evenly spread the intended beats;
- Liu explicitly asks for 卡点, 音效/音乐控制画面, 参考音频, or stronger duration/rhythm control.

Do not create one for a simple continuous shot with no meaningful timing problem, pure prompt discussion without a target clip, dialogue/lip-sync work where another audio role already owns the reference, or a platform that cannot accept audio reference. In those cases keep a compact visible beat map in text.

Choose the smallest useful mode:

- `sfx`: exact motion/impact/transition points; default for action and first validation;
- `music`: emotional or montage structure without exact physical hits;
- `hybrid`: both section-level musical form and a few indispensable action peaks.

Before delivering the prompt, make the visible beat map, sparse cue list, exact target duration, and role contract. Then write a UTF-8 payload and run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/create_reference_audio.ps1 -PayloadFile "<payload.json>"
```

Minimum payload:

```json
{
  "projectId": "resolved current project or omitted for active-profile fallback",
  "profileId": "resolved episode/profile when available",
  "duration": 10,
  "mode": "sfx",
  "bpm": 96,
  "name": "shot-purpose_control_v01",
  "description": "the visible event path",
  "musicPrompt": "only for music or hybrid",
  "cues": [
    { "time": 1.2, "label": "sudden dash" },
    { "time": 5.8, "label": "decisive impact" }
  ]
}
```

Use the current task's explicit project/episode first, then the workbench active profile. If neither is reliable, let the adapter use Pending Review. Preserve the returned WAV, `.prompt.md`, `.meta.json`, SHA-256, cue map, and role contract. In the final paste-ready prompt bind the uploaded file as `{{Audio N}}（画面节奏控制参考）` or the exact platform equivalent and state that it controls visible timing, not the final mix. When actual image/video generation begins, pass the returned path/hash/cue map into `$generation-asset-pipeline` as `settings.referenceAudio`.

## Sound Layer Pattern

Use compact layers: `Dialogue: ... Sound: ... SFX: ... Music: ... Silence: ...`. Include only the layers that matter. Silence is valid when it sharpens drama or avoids confusing lip-sync.

| Need | Stable audio direction |
|---|---|
| Lip-sync | `Character A, locked medium close-up, says "I found it." Clear dry dialogue, no head turn.` |
| Product ad | `Sound: low room tone. SFX: magnetic click on lid open, soft glass chime at final frame.` |
| Beat sync | `[Audio1] provides tempo only; light pulses and foot taps match the downbeat.` |
| Drama | `Distant rain and refrigerator hum; no music during the line.` |
| Action | `Breathing grows louder, shoe squeak at landing, metal door buzzer at endpoint.` |
| Visual control track | `[Audio1] controls visible timing only: first short whoosh = dash, strongest transient = sole impact peak, final gap = changed end state; final mix is separate.` |

## Multi-Character Dialogue

Use one speaker per short clip when reliability matters. If two characters must speak, separate turns and keep the camera stable: `Character A says... pause. Character B answers...`. For complex exchanges, recommend generating controlled single-speaker clips and compositing in post.

## Failure Fixes

If dialogue desyncs, shorten the line, lock the camera, remove head turns, clean the audio role, and reduce competing SFX. If the wrong speaker talks, assign tags and split lines by speaker. If audio is ignored, remove extra music/SFX instructions and make the reference role explicit.

If audio and video references fight each other, mute the reference video before upload when possible, or make the priority explicit: `[Video1] controls camera only; [Audio1] controls tempo and energy`.

## Sequence State

When sequence state is present, inherit completed dialogue, active dialogue, ambience, music phase, SFX phase, current clip scope, continuity locks, exact reference tags, and reserved future beats. Do not repeat completed dialogue unless the user explicitly asks for a reprise. Continue or intentionally change the audio phase instead of restarting it by accident.

## Output Contract

Return speaker map, quoted dialogue, sound layers, audio reference role, lip-sync constraints, post/delivery notes if needed, and a compact prompt-ready audio block. When visual control is the goal, also return the generated reference-audio path, target duration, visible-beat map, sparse cue sheet, upload/binding role, one-variable A/B plan, cue-to-picture review fields, and leakage/post fallback. The normal front-stage package is `final prompt + reference WAV + concise cue map`; do not send Liu to the workbench to build it manually unless he asks to edit the track himself.
