---
name: seedance-2-5-prompting
description: Write prompts for Seedance 2.5 / Dreamina 2.5 video generation, editing, and extension. Use whenever the target model is Seedance 2.5, or when the task needs any 2.5-only capability — up to 50 reference materials with @Image N / @Video N / @Audio N role mapping, videos up to 30 seconds structured as stages with end states, video editing (subject swap, background replacement, audio edits), forward/backward video extension, multi-keyframe sequences, storyboard grids, blockout rendering, one-click video, and seamless transitions. Triggers on Seedance 2.5, Dreamina 2.5, 30-second video prompt, multi-reference video, video extension, video editing prompt, blockout reference, storyboard to video, one-click video, seamless transition, first and last frame video, keyframe sequence, locked look block, camera body and lens set choice, film stock look, film grade, camera operation. Not for Seedance 2.0, which uses a different reference syntax and per-second timecodes.
---

# Prompting Seedance 2.5 (Dreamina)

Source: ByteDance's official Dreamina Seedance 2.5 prompting guide. Everything in this file and in `references/` comes from that guide unless a section is explicitly marked as carried over from 2.0 practice. The Settings table comes from the hosts listed under Sources.

Scope: prompt construction only. Generation parameters (resolution, seed, model tier) are set on the generation page or via API, not in the prompt — never write them into the prompt text.

**Version check first.** If the user is targeting Seedance 2.0, say so and do not use this file as is. The two versions have incompatible reference syntax and incompatible sequencing models. Do not blend them.

**Tag format depends on the platform.** The official guide writes `@Image 1` with a space. Many platforms insert their own tag when you pick a file from the upload list (often `@image1`). Use whatever tag the user's platform inserts. What matters is that every tag gets its own role line.

## Settings (on the page, never in the prompt)

| Setting | Value |
|---|---|
| Length | up to 30 seconds in one pass |
| Resolution | 480p, 720p, up to 1080p. Some platforms cap at 720p, check the model card |
| Shapes | 1:1, 3:4, 4:3, 16:9, 21:9, 9:16 |
| References | up to 50: 30 images, 10 videos, 10 audio |
| Audio | generated in the same pass as the picture |

Build long pieces up in steps. Get 5 seconds right, then 10, then commit to 30. A wrong line in a 30 second prompt costs the whole generation.

## What changed from 2.0

| | 2.0 | 2.5 |
|---|---|---|
| Reference syntax | `@Image1` (no space) | `@Image 1`, `@Video 1`, `@Audio 1` (with space) |
| Material budget | 9 images / 3 videos / 3 audio | up to 50 total: 30 images (≤4K each), 10 videos (≤30s combined), 10 audio (≤30s combined) |
| Max duration | short clips | up to 30 seconds |
| Sequencing | per-second timecodes | **stages with end states**; timestamps only for critical beats |
| Reference roles | optional | **mandatory** — every material states what to use *and* what not to use |
| Modes | text-to-video, image-to-video | + video editing, forward/backward extension, one-click video, seamless transition, blockout rendering |

The single biggest behavioural change: 2.5 does not infer which reference maps to which subject. If it isn't written in the prompt, it is not bound.

## Core formula

```
Subject + Action or Event + Scene and Environment + Visual Style + Camera/Cut + Audio
```

Only Subject + Action is required. Drop any component that doesn't earn its place.

**Template**

```
<Subject> performs <primary action or event> in <scene and environment>.
The visuals feature <visual style>.
Use <shot size, camera angle, camera movement, or cuts>.
Audio includes <dialogue, ambience, sound effects, or music>.
```

**Example**

```
A ceramic artist finishes a pale blue cup in a studio at dawn, lifts it from the wheel,
and places it in the center of a wooden shelf.
Soft morning light enters through the window. The wet clay has a delicate sheen.
Begin with a medium shot of the wheel-throwing process, slowly push in toward the cup's
surface texture, then cut to a frontal view of the shelf.
Retain the low hum of the pottery wheel, the friction of clay, and subtle indoor ambience.
```

## Locked look block — the head of every multi-shot prompt

Anything with more than one shot opens with the capture format, stated once and inherited by every shot below. Without it the model re-rolls grain, contrast, depth of field and skin tone at each cut, and the shots stop reading as one piece of footage.

```
[LOOK — LOCKED, APPLIES TO EVERY SHOT]
<camera body / capture format>, <lens set>, <stock or sensor>, <optical format>, <T-stop>,
<depth of field>, <grain>, <highlight behaviour>, <black level>, <contrast>.
<Grade name>: <hero tone>, <secondary field>, <shadow bias>.
<Camera operation>. <Performance and audio baseline>.
```

Per-shot blocks then carry only what changes — shot size, focal length, camera move, blocking. Restating the look per shot invites re-interpretation.

**The rule the block lives or dies on: every named piece of gear is followed by its visible consequence.** Seedance does not simulate an Arricam. The name biases the output; the description controls it. `Cooke S4/i primes` on its own is decoration — `Cooke S4/i primes, warm skin rendering, creamy controlled bokeh, soft flare` is an instruction. Same pairing as the niche-camera-term rule further down, applied to bodies, glass, stocks and filtration.

Keep it to roughly three lines. Past that the model averages the adjectives instead of applying them, and contradictory descriptors (`lifted milky blacks` plus `deep rich blacks`) flatten to mid-grey.

Bodies, lens sets, stocks, grade labels, camera operations and six ready-made presets: `references/camera-and-look-lock.md`.

## Rule 1 — every material gets a role and an exclusion

The exclusion is not optional politeness. Reference images carry backgrounds, bystanders, and compositions that will leak into the output unless you ban them explicitly.

```
@Image 1 defines <subject>'s <appearance, clothing, structure, or material>. Do not use <what leaks>.
@Video 1 defines <motion, camera movement, or pacing>. Do not use <identity, clothing, or scene>.
@Audio 1 defines <character or sound type>'s <voice, dialogue, ambience, or music>.
```

**Wrong:** `@Images 1 through 4 define four characters respectively.`
Nothing here says which image is which character.

**Right:**
```
<Conservator> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.
<Registrar> corresponds to @Image 2. Use only the appearance, hairstyle, and clothing.
```

**Multiple views of one object** — say so, or you get duplicates:
```
@Image 1 defines the front view of the same folding desk lamp.
@Image 2 defines the left-side structure of the same folding desk lamp.
All images define one folding desk lamp. The output must contain only one lamp throughout.
```

**When a reference video already carries the motion**, state only which attributes to inherit. Re-describing the action in prose fights the reference and degrades it. Exception: a *blockout* video carries only motion and space, so the prompt must still supply subjects, scene, action, and style.

Do not rely on text labels burned into the reference images. Mappings live in the prompt text.

### Recommended material counts

Prefer 1–8 distinct subjects across subject images, 1–5 subjects and 5–10 seconds per subject video, and 1–5 reference images when editing a source video under 20 seconds. Higher counts work but stability drops. If more than five subjects each need several views, put each view in its own image — separate view images beat a collage.

## Rule 2 — long videos are stages, not timelines

For anything with multiple events, split into consecutive stages. **One primary state change per stage**, and state what is visibly true when the stage ends. The end state is what keeps the model from drifting.

```
[Generation Goal]
Generate a <video type>. The central subject is <subject>, and the primary event is <story summary>.

[Stage 1]
Initial state: <initial state of characters, props, and scene>.
Primary event: <one primary action or event>.
End state: <character positions, prop ownership, or visible scene state>.

[Stage 2]
Continue from the previous stage: <state that must remain unchanged>.
Primary event: <one primary action or event>.
End state: <observable state>.

[Stage 3]
Primary event: <closing event>.
End state: <final visible state>.

[Maintain Consistency]
Keep <character identity, number of characters, clothing, prop ownership, spatial direction,
and audio relationships> consistent.
```

Note the `Continue from the previous stage:` line — it re-anchors identity and prop ownership at every hand-off. Include it in every stage after the first.

### When to reach for timestamps

Default to stages. Use one-second precision only for a critical hand-off, an entrance or exit, a transition, or an explicit beat.

| Pattern | Example |
|---|---|
| Time range | `0-3 seconds… 3-7 seconds… 7-12 seconds…` |
| Exact point | `At 5 seconds, the camera whip-pans rapidly to the left and completes the transition.` |
| Relative | `Three seconds after the character presses the button, the room lights gradually turn off.` |

Ranges must be consecutive and non-overlapping. A range is a time *budget*, not an edit point — the action may land slightly early or late. Too little content in a range gives the model freedom it will use; too much causes over-cutting or dropped events. Never demand a frequency like "three actions in one second".

## Audio and text syntax

Natural language works throughout. Use the delimiters when you need the model to separate the layers cleanly.

| Content | Syntax | Example |
|---|---|---|
| Music | `()` | `(Soft, rhythmic piano music plays in the background)` |
| Sound effects | `<>` | `<A bell rings in the distance>` |
| Dialogue | `{}` | `{Hello, welcome back.}` |
| Subtitles | `【】` | `【Chapter One: Departure】` |

**Non-Chinese dialogue must declare its language before the line**, otherwise the model may speak English text with a Chinese delivery:

```
Dialogue language + regional variety or accent + delivery style + speaker + {line}

Dialogue language: American English. The girl says in natural, conversational American
English: {I thought you weren't coming.}
```

## Emotion — direct with observable cues

"Tense", "warm", "oppressive" set a direction but leave the performance open. Anchor them to things a camera can actually record: eye movement, brow tension, mouth movement, breathing, gaze direction, hand movement. Two to four cues is enough for one transition — do not inventory the whole face.

**Single transition:**
```
The overall emotion shifts from <starting emotion> to <ending emotion>.
After <triggering event>, <subject> first shows <immediate observable reaction>.
Then, <eyes, brows, mouth, breathing, gaze, or hand movement> gradually <changes>.
Finally, <subject> expresses <target emotion> through <restrained or explicit behavior>.
```

**Multi-stage:** drive each shift with its own triggering event rather than listing emotions in sequence.

## Camera language

Directly supported and safe to write plainly:

- **Shot size:** extreme wide, wide, medium, close-up, extreme close-up
- **Movement:** push in, pull out, pan, lateral move, follow shot, orbit, dive, dolly out, tilt up, handheld shake
- **Position:** low angle, overhead view, first-person view
- **Popular techniques:** one-take, dolly zoom, aerial view, FPV, bullet time, handheld, bounce speed ramp

With several subjects in frame, always name which subject the camera follows or orbits, where the move starts, and where it ends.

For a niche or ambiguous term, keep the term **and** translate it into a visible change:

```
Cinematography term + target subject + visual change + foreground/background relationship + direction or speed

Rack focus: shift focus smoothly from the leaves in the foreground to the person in the
background. The leaves gradually blur while the person's face changes from soft to sharp.
```

Aperture and focal length values are allowed, but the described visible result controls the output more reliably than a number.

## Mode router

Pick the reference file that matches the task and read it before writing the prompt.

| Task | Read |
|---|---|
| Locking capture format across shots; picking a camera body, lens set, stock, grade or camera operation; matching a named film look | `references/camera-and-look-lock.md` |
| Several characters/props/scenes across multiple scenes; subject profiles; per-scene material selection | `references/multi-reference-system.md` |
| First/last frame, multi-keyframe sequences, storyboard grids, coarse or fine blockouts | `references/keyframes-storyboards-blockouts.md` |
| Editing an existing video (subject swap, background replacement, audio changes); forward or backward extension; locked aspect ratio and duration rules | `references/editing-and-extension.md` |
| One-click video from a batch of images; seamless transition bridging two clips | `references/oneclick-and-transitions.md` |

Simple single-scene generation needs none of them — the core formula above is enough.

## Pre-flight checklist

Run this before handing a prompt over.

- Subject and primary action stated?
- Multi-shot: locked look block at the head, every named body/lens/stock paired with its visible consequence, no look descriptors repeated inside the per-shot blocks?
- Every material states what to use **and** what not to use?
- Every distinct character, product, and prop named and bound to a specific reference?
- References selected per scene rather than all forced into frame at once?
- Each stage carries exactly one primary change plus a clear end state?
- Character count, clothing, prop ownership, and spatial direction consistent across stages?
- Editing tasks: sole editing master, edit scope, target quantity, and content to preserve all defined?
- Abstract emotions and camera terms paired with visible or audible cues?
- First/last frames: one role per image, and the same aspect ratio on both?
- Storyboard or blockout: reading order stated, and coarse vs fine identified?
- Extension: boundary frame, motion trend, and audio continuity checked?
- No generation parameters written into the prompt body?

## Hard limits — set expectations honestly

Do not promise the user what the model cannot do:

- Timestamps allocate time to events; they are **not** frame-accurate edit points.
- Editing prompts raise the probability that events align with the source; they cannot guarantee frame-by-frame overlap.
- Multi-reference selects and combines the right materials — it does not put every material on screen at once.
- Boundary frames in extensions connect *visually*, not pixel-identically.
- Seamless transitions generate a bridge; they do not preserve both source clips pixel-for-pixel.
- Subtitles, formulas, signage, and product specs that must be exactly right need prepared reference materials plus post-production — not prompt wording.

## Carried over from 2.0 practice

Not in the official 2.5 guide, but held up across production work on 2.0. Treat as heuristics, and drop any that stop helping on 2.5:

- One primary camera movement per shot. Compound moves get described as beats, not stacked adjectives.
- Rhythm words (`slow`, `smooth`, `gradual`, `gentle`) control motion speed; unqualified `fast` produces jitter.
- State subject movement and camera movement in separate clauses.
- `cinematic` alone is noise — qualify it with a concrete lighting type or drop it.
- Layer 2–5 specific, onomatopoeic sounds per beat rather than one ambient bed for the whole video.
- Iterate one variable at a time so you can attribute the change.

## Sources

- ByteDance / BytePlus ModelArk, Dreamina Seedance 2.5 prompt guide: https://docs.byteplus.com/en/docs/ModelArk/2607689
- Dreamina, Seedance 2.5 prompt guide: https://dreamina.capcut.com/seedance/seedance-2-5-prompt
- OpenArt, Seedance 2.5 prompt guide: https://openart.ai/blog/seedance-2-5-prompt-guide/
- Hedra, Seedance 2.5 model specs: https://www.hedra.com/models/video/bytedance/seedance-25
- Apiframe, Seedance 2.5 complete guide: https://apiframe.ai/guides/seedance-2-5-guide

Made by promptcraft.shop. Checked 22 September 2026.
