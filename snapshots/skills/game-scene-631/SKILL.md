---
name: game-scene-631
description: Design, rewrite, generate, or critique game-environment and cinematic scene images with a flexible 6:3:1 hierarchy across composition, lighting, color, spatial layout, asset form, and information density. Use when focal clarity and visual prioritization matter; do not use for isolated subjects with no scene-design goal.
---

# Game Scene 631

Build scenes whose dominant, supporting, and accent information can be read in that order at a glance.

## Interpret 6:3:1 Correctly

- Treat 6:3:1 as a hierarchy target, not an exact pixel count or industry standard.
- Preserve the user's subject, story, references, platform, aspect ratio, style, exclusions, and exact counts before applying this framework.
- Prefer a clearly separated hierarchy such as 6:3:1 or 7:2:1. Do not force 6:3:1 when the user deliberately wants balanced opposition, symmetry, or another controlled exception.
- Never assume that repeating the words `6:3:1` is enough. Translate every applicable tier into visible objects, areas, light behavior, color relationships, and material treatment.

Read [references/631-rulebook.md](references/631-rulebook.md) when creating a scene prompt, generating an image, or diagnosing an existing scene.

## Workflow

1. Identify the scene's one-sentence narrative purpose and the first thing the viewer must notice.
2. Lock three hierarchy anchors:
   - **Dominant:** the large mass or quiet field that establishes the place and holds the frame together.
   - **Supporting:** the structures or directional lines that add variation and guide the eye.
   - **Accent:** one compact focal cluster with the strongest local contrast, saturation, light, or narrative importance.
3. Map the anchors across the six relevant dimensions: composition, lighting, color, spatial layout, asset form, and information density. Keep the same focal anchor coordinated across dimensions instead of creating a different focal point in each one.
4. Write observable image instructions. Name what occupies each tier, where it sits, how it leads the eye, and what remains quiet.
5. Add only the style, camera, lens, lighting, material, and rendering details that support the requested image. Do not let decorative detail dilute the hierarchy.
6. Apply the quality gate before delivery or generation.

## Prompt Delivery

When the user asks for a prompt, provide a complete `English Prompt` followed by a separate, semantically aligned `中文 Prompt`. Preserve all hard constraints in both versions. Add a negative prompt or exclusion line only when it materially protects the composition.

When the user asks to generate or edit the image, use the available image-generation workflow after constructing the scene hierarchy. Inspect the result rather than treating prompt delivery as proof that the visual rules were achieved.

When the user asks for critique or analysis, report the broken dimension, the hierarchy conflict, and the smallest corrective change. Do not rewrite or regenerate unless requested.

## Quality Gate

Require all applicable checks:

- **Thumbnail:** at small size, the dominant mass and one focal accent remain readable.
- **Blur:** broad value and color blocks survive; fragmented lines and props do not turn the frame into uniform noise.
- **Silhouette:** major architecture or hero assets remain recognizable without surface detail.
- **Light:** one source family determines time, weather, mood, and most shadow direction; ambient light preserves dark-area information; accent light marks the focal area.
- **Focus:** there is one primary focal cluster unless the brief explicitly calls for controlled duality.
- **Density:** quiet, medium, and dense regions are visibly distinct; detail and gloss are not spread uniformly.
- **Continuity:** reference identity, scene geography, and user-specified content have not been altered by the 6:3:1 pass.

If reviewing an actual generated image, explicitly note any failed check and revise only the affected layer. If delivering a prompt without an image result, state no claim that visual compliance has already been verified.
