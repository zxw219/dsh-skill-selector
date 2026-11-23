# H3 guided task recipes

Read only the primary task lane selected in the H3 Design Card. Also read section 10 when an audio file has a tracked reference role; it is a cross-cutting add-on rather than a competing visual lane. These are design presets, not model-facing templates. Upstream film owners still control story, camera, material, VFX, sound, and continuity. After planning, serialize the selected T2VA, I2VA, FL2VA, L2VA, or Ref2VA mode through [h3-interoperability-guide.md](h3-interoperability-guide.md).

## 1. Typography, titles, credits, animated posters

Guide toward:

- the exact short copy set and its reading order;
- one hierarchy system: primary title, secondary line, numeric/time code;
- one recurring carrier such as a line, beam, paper edge, route, cursor, slit, or aperture;
- one material family per major card and one fully exposed reading moment;
- an active final lockup rather than an early static poster.

Recommend independent cards or post-composited copy when order and spelling are delivery-critical. A multi-panel atlas may own style and layout vocabulary, but not a deterministic timeline.

Starting density for 15 seconds:

- 7–9 short isolated cards: normal high-density range;
- 10–11: deliberate stress range with one local job per card;
- rich character/material nodes: reduce to 7–8;
- long subordinate data, dialogue, UI logic, and exact credits reduce the count further.

Acceptance: correct glyphs, full unobstructed exposure, intended hierarchy, carrier continuity, and final motion are reviewed separately.

### Text-only PV specialization

Use this branch for activity teasers, manifesto/poster copy, lyric PVs, and beat-synced typography where readable text is the visual subject rather than a caption layer.

- lock a visible-text whitelist and its reading order before motion design;
- count distinct copy or meaning states separately from beat-level microshots: several short operations may elaborate the same phrase without creating a new information node, so budget the required copy states first and the motion beats inside each state second;
- when the requested taste is ultra-fast text flash, budget **perceived speed density** as a separate surface: long clean holds, empty-black gaps, repeated ease-in/ease-out landings, and an early final lockup can make an otherwise accurate sequence feel slow;
- preserve one clean exposure for each required phrase without turning every phrase into a settled card: interleave partial entries, cropped scale jumps, collision frames, split/reassembly phases, and cut-on-motion handoffs around the clean exposure, then reserve the final lockup for the shortest readable terminal window compatible with the brief;
- choose one typographic motion system, then give each beat one local operation such as scale, rotation, compression, collision, split, duplication, inversion, or reassembly;
- move important words or lines as intact units whenever spelling and reading order matter;
- keep the graphic vocabulary intentionally narrow: type, negative space, and at most one restrained accent family;
- separate on-screen lyric accuracy from vocal accuracy; supplied audio or post verification owns decision-critical sung wording.

Acceptance: authorized text only, exact glyphs, full-exposure moments, beat alignment, hierarchy, perceived speed density, final-lockup timing, and an active final state are checked independently. Requested microshot counts remain planning targets rather than guaranteed hard-cut counts.

## 2. Pure motion, VFX, material change, and transitions

Guide toward one attributable carrier through one chain of state changes. Choose whether the carrier's protected invariant is color, silhouette, direction, pulse, or material boundary; rank one as primary.

Blueprint:

```text
trigger -> state A -> causal handoff -> state B -> scale/material escalation -> resolved active state
```

Prefer a few strong material states over many simultaneous sub-effects. When exact material identity matters, give each state a visible boundary and compatible ending motion. Review visible state count, material fidelity, and editorial block count separately because H3 may fuse several planned nodes into one continuous transition.

### Motion Design / MG specialization

Treat `After Effects`, `AE`, and `TouchDesigner` as visual-language anchors, not as executable software guarantees. Translate them into visible primitives, transformation rules, and timing:

- derive the piece from two or three primitives such as a point, line, track, field, block, glyph, particle, or waveform;
- define one graphic DNA and let shapes, type, transitions, and the final lockup evolve from it;
- give every transformation a visible cause and inherited direction, scale, path, pulse, or topology;
- use audio-reactive or generative-field behavior only when the relevant beat, amplitude change, flow direction, or spatial response can be described visibly;
- keep requested resolution and frame rate as platform/output settings rather than assuming that prompt wording overrides the active H3 route.

When readable copy becomes the sole visual subject, hand the detailed design to the text-only PV branch in lane 1.

## 3. Product and e-commerce film

First decide which proof the film sells:

- industrial form/material;
- one or two functions;
- packaging/opening;
- macro structure;
- real-world application.

Recommended chain:

```text
identity -> material discovery -> function occurs -> optional macro breakdown -> intact hero -> use result
```

Use a product keyframe for exterior geometry and label copy. Use a CAD/exploded diagram or structure board when internal order and function are factual. Without structural reference, limit breakdown to three or four macro modules and avoid detailed engineering claims.

Industrial-design graphics work best when each line is anchored to a real edge, part, motion, or result and follows `appear -> prove -> retract`. Keep structure lines, active-function color, and naming text as separate hierarchy roles.

When moving from breakdown to application, first restore the complete closed product, establish it briefly, then let the intact exterior motivate a cut or occlusion into use. Judge product identity, label accuracy, callout semantics, assembly logic, application proof, and material response separately.

## 4. UI and interface motion

First ask or infer whether the user wants:

- a polished visual prototype; or
- a logically exact interaction demonstration.

For visual prototypes, H3 may own shared-element expansion, layout hierarchy, cards, cover art, parallax, and aesthetic transitions. For exact interaction, supply before/after states or a screen recording.

If one approved UI still is the actual opening frame, use I2VA. If separate images define several interface states or a screen recording owns interaction timing, use Ref2VA and label each asset only for its declared role.

Each beat follows:

```text
input gesture -> one state mutation -> visible confirmation -> next input
```

Keep mutually exclusive controls, cursor identity, counters, and active/inactive states reference-owned. Acceptance separates visual polish from functional correctness.

## 5. Character, game showcase, and menu package

MiniMax's official co-op game intro recipe uses a useful staged workflow: choose the style and identity anchors, generate one menu still for approval, wait for approval, then rebuild the characters, UI copy, and event timing for the video. Treat this as a task recipe rather than a universal H3 rule: <https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/co-op-game-intro-generator/SKILL.cn.md>.

When the approved still is the actual opening frame, compile the final video prompt as I2VA. Use Ref2VA instead only when additional images, video, or audio require persistent labeled roles beyond the first-frame anchor.

Choose one primary purpose:

- reveal identity;
- prove outfit/weapon/equipment;
- demonstrate one signature skill;
- finish on a selection or profile card.

Recommended 15-second structure uses 7–8 rich nodes:

```text
identity -> costume/material -> weapon -> selected equipment -> signature motion -> graphic transition -> final selection state
```

Use one recurring graphic carrier as divider, cursor, weapon energy, route, or frame edge. Keep short primary labels exact; treat dense stats as visual texture unless independently addressable. Preserve subtle motion in the final card.

### Attribute-card / action-proof character intro specialization

Use this candidate recipe when the purpose is to introduce one character through compact graphic labels and visible action evidence:

```text
identity ignition -> activation/status card -> controlled action proof -> ability card -> impact proof -> maximum-state card -> hero identity lockup
```

Keep one character, one compact action chain, and three to five short decision-critical labels. Alternate a bright graphic definition field with a darker action field so the labels define the character while nearby action beats demonstrate the corresponding state, behavior, or impact. The relationship may precede or follow the label; it must remain visually legible rather than becoming a literal one-label/one-move checklist.

Create density through editorial microshots, scale changes, layout recomposition, graphic silhouettes, impact inserts, and sound attacks while preserving only a few semantic states. Reuse one graphic system across both fields—for example condensed type, one accent-color pair, concentric rings, brush masks, or silhouette wipes—so the package feels continuous instead of becoming unrelated title cards and action footage.

Declare the complete readable-text whitelist. Keep the final character name and role card isolated long enough to inspect; supply decision-critical names, logos, or custom marks as artwork or verify them in post. When identity matters, give one character sheet or portrait board the identity role and keep costume, hair, face, and signature color stable across graphic and action fields. End on a readable hero lockup with subtle cloth, hair, light, or graphic motion.

The inspected external 15-second specimen that motivated this recipe is supporting evidence for the package structure only. Its post-production boundary is unknown, one final English role word appears misspelled, and its action vocabulary is limited to running, slashing, impact flashes, and motion blur. Do not use it to claim native complex-combat control, guaranteed typography accuracy, or that every visible MG element was generated inside H3.

### Fashion lookbook / editorial outfit-switch specialization

Use this candidate recipe for a non-narrative fashion package:

```text
locked identity and stage -> typography hook -> close-up identity proof -> beat-synced look/layout switches -> simplified hero lockup
```

Keep the performer near one stable composition anchor. For every look switch assign one outfit state, one pose state, one editorial layout family, and at most one dominant camera change. Budget outfit states, layout states, exact copy, and camera motion separately. A new outfit, pose, layout, headline, and camera move in the same short node already make it rich; reduce the look count before adding another mechanism.

Use one recurring editorial carrier—headline edge, cable afterimage, barcode, scan line, border, or grid—to inherit direction or shape into the next look. It may change form, but it remains the sole repeated transition system; hard cuts and one-off apertures may support it without becoming competing carriers. Keep short decision-critical headlines exact and quoted. Declare the complete readable-text whitelist and treat every other barcode, number string, coordinate, grid, or mark as abstract texture unless its exact value matters; supply exact logos or custom marks as artwork or add them in post.

For intentional editorial overload, keep the semantic chain small and increase presentation density with single-job proof inserts: face, garment material, accessory connection, pose, silhouette, or hero prop. Adjacent inserts should change crop, scale, angle, layout, or rhythmic function instead of repeating one continuous movement. A proof insert verifies an existing look or identity state; it does not create another outfit state.

When facial identity or garment design is decision-critical, assign identity and outfit boards as reference owners and choose I2VA or Ref2VA by their actual role. End on a hero lockup with subtle hair, fabric, light, or layout motion unless a true editorial freeze is required.

One uninspected external 15-second specimen uses seven changes at roughly 1–1.5-second intervals. Treat that cadence as a density candidate, not a default or reliability claim. A safer first test uses three or four clearly separated looks plus proof inserts; increase the look count only after inspecting identity, garment, copy, and layout fidelity from the returned output.

## 6. MV, trailer, TV opening, and film-title package

H3 is strongest here as packaging, not as a substitute for long performance choreography.

Choose:

- one protagonist/performer or one recurring object;
- one stable world or stage;
- one recurring graphic carrier;
- one live-action/graphic/material state chain;
- a small number of exact lyric/title/event cards.

For greater camera variety, distinguish **cut roles** from **in-shot travel**. Ask for a few meaningfully different shot functions and specify sustained travel only where it carries information. Exact sung words use supplied audio or post verification; on-screen lyric correctness does not prove vocal intelligibility.

## 7. Reference-driven multimodal edit or V2V

Treat this as officially supported but not yet validated by the documented local test set until a returned output is inspected.

Use Ref2VA for this lane. Distinguish `video editing`, `video continuation`, `reference generation`, `audio reuse`, and `audio reference` in the official `summary`; do not infer editing or audio reuse merely from the presence of a video file.

Allocate one owner per reference:

- source video: motion/action/camera/edit rhythm;
- identity image: character or product;
- style frame: palette/material/layout;
- audio: timing/voice/music.

Text states only the intended deltas and protected invariants. Do not make two references co-own the same property. After generation, verify which reference actually controlled motion, identity, style, and sound before promoting a rule.

## 8. Dense action or multi-actor combat

Recommend an action-first model. If H3 must be used, require a motion-reference video as action/rhythm owner and keep the H3 prompt to identity, environment, effect ownership, concise deltas, sound, and endpoint.

Do not trade the missing motion reference for more choreography prose. If the user still chooses prose-only H3, reduce the scene to one decisive action state change rather than a coupled exchange.

## 9. Local reality-to-hand-drawn rewrite

Use this lane when a drawing instrument progressively converts selected live-action objects while the surrounding world remains photographic. It is a localized causal transformation, not a whole-scene style transfer.

Choose the mode from the asset's real job: T2VA for a fully generated scene, I2VA when one still is the actual opening frame, and Ref2VA `video editing` when a supplied live-action clip owns motion, composition, and timing.

Give each beat one target and use this chain:

```text
real target established -> tip contacts the outline -> rough line grows from the tip
-> only the crossed region becomes paper/drawn -> interior color appears stroke by stroke
-> completed 2D drawing inherits the target's position, scale, and motion
```

Define the protected live-action layer explicitly: background, untargeted objects, camera continuity, and every untraced part remain in their current photographic state. Define the hand-drawn endpoint with observable properties such as irregular dark contours, occasional double lines, paper gaps, slight color overshoot, or boiling-line motion. Keep drawing sounds, location ambience, and music in their official audio fields.

Acceptance: the real object is visible before intervention; the line originates at the tip; the conversion frontier follows the drawn path; fill develops progressively; protected areas remain live action; and the completed drawing preserves the original track rather than jumping position or scale.

## 10. Cross-cutting audio reference and timbre transfer

Use Ref2VA whenever an audio file has a tracked role. Decide one primary role before writing:

- exact or partial audio reuse;
- voice timbre only;
- delivery, cadence, or emotion;
- beat/rhythm synchronization;
- ambience or sound texture.

Map the audio to a stable target speaker `(Sx)` when a visible person speaks or sings. Keep exact target words inside `<d>[Language] ...</d>`. A timbre-only reference transfers voice identity and the declared delivery qualities, not the source wording. Use `fully_copy`, `partially_copy`, `reference`, or `weak_reference` only according to the official retention contract.

For event timing, place the synchronized sound beside the owning action in `integrated_multimodal_description` or `detailed_description`, then restate the sound events in playback order inside `overall_soundscape`. Put audience-only music in `non_diegetic_music`, using event-relative entry, continuation, and exit cues plus a relative mix hierarchy rather than percentages or dB values.

Acceptance: speaker mapping, target words, timbre similarity, delivery, lip synchronization, event timing, ambience/physical sound separation, score separation, and final mix are reviewed independently. Treat official showcase success as capability evidence until a matching local output is inspected.
