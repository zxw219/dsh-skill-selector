---
name: seedance-vocab-en
description: Seedance英语词汇库：整理英语环境下常用的镜头、动作、表演、光线、材质、声音和风格表达。用于英文提示词编写、翻译和词汇选择。
version: 6.1.0
---

# seedance-vocab-en

English is the default prompting language and fails in two ways at once: slop (empty evaluation words that add tokens and no signal) and false positives (vague threat-adjacent wording that trips the heaviest moderation surface). The cure for both is the same: concrete production English. Preserve reference tags exactly: `[Image1]`, `[Video1]`, `[Audio1]` must never be reworded.

## Intent

English is where most users think, and where most prompts quietly rot. The soul of this vocabulary is precision as kindness: give people exact words so their excitement survives contact with the model, and so honest prompts stop being mistaken for dangerous ones.

## Usage Rule

If a camera, microphone, light meter, or stopwatch cannot detect it, rewrite it. Every sentence should name something visible, audible, or measurable: subject, visible action, camera, light source, sound, constraint.

| Function | English wording |
|---|---|
| Camera | `slow push-in`, `locked medium shot`, `stable lateral tracking`, `pull back to reveal`, `macro close-up` |
| Lighting | `soft backlight`, `warm practical light from the left`, `cool moonlight rim`, `wet asphalt reflecting neon` |
| Motion | `a slow head turn that stops`, `droplets merge and slide down`, `fabric settles after the gesture` |
| Audio | `quiet room tone`, `one clear spoken line in quotes`, `no music until after the line` |
| Constraints | `keep the logo, label, and shape unchanged`, `one action, one camera move`, `nothing else moves` |

## De-Slop Pass

Strip quality adjectives before adding anything: `cinematic`, `epic`, `stunning`, `masterpiece`, `8K`, `ultra-realistic`, `award-winning`, `hyper-detailed` all delete or convert to one observable detail each. A prompt that earns "epic" names the crowd size, the lens distance, or the structure height instead of the word.

## Filter-Aware Wording

English homonyms read as threats to filters: `shoot the scene`, `kill the lights`, `gun it`, `dead silence`, `blow up the image`. Use the production synonym (`film the take`, `cut the lights to black`, `accelerate hard`, `held silence`, `enlarge to full frame`). This is clarity for safe prompts only — never evasion. Anything genuinely risky (minors, real-person likeness, sexual or graphic content) routes to `[skill:seedance-filter]` for its boundary rule, not to a rewording.

## Compact Pattern

`[Image1] is the reference; keep identity, color, and shape unchanged. Only [motion/light/camera] changes. Camera: [one move]. Sound: [one cue]. Constraints: [lock].`

Load `../../references/vocab/en.md` for the full function-organized vocabulary, slop traps, and filter-trip repairs. Load `[ref:anti-slop-lexicon]` for the core replacement rule and `[ref:filter-vocab]` for the full false-positive repair table.

## Output Contract

Return the de-slopped English prompt, each replacement made (slop → observable detail), any filter-trip repair applied, and unchanged reference tags.
