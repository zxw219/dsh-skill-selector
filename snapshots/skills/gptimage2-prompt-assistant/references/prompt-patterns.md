# GPT Image 2 Prompt Patterns

## Quick Rewrite Template

```text
Goal:
[What the final image should be used for and what it should show.]

Inputs:
- Image 1: [base scene / person / product / style reference]
- Image 2: [optional role]

Required changes:
- [Only the things that should change.]

Must preserve:
- [Identity, product details, composition, background, labels, lighting, perspective.]

Visual direction:
- Medium/style: [photorealistic / watercolor / 3D render / editorial / UI mockup / comic]
- Composition: [framing, angle, crop, focal point]
- Lighting/color: [time of day, mood, color temperature]

Text, if any:
- EXACT text: "[copy]"
- Placement: [where]
- Do not add any other readable text.

Negative constraints:
- No watermark, no extra logos, no extra limbs/fingers, no unrelated objects, no layout drift.
```

## Style Transfer

```text
Use the visual style of the input image as the style reference: color palette, texture, brushwork, line quality, lighting mood, and level of detail.
Generate [new subject/scene].
Do not copy the original subject unless requested.
Keep the style recognizable while making the new scene coherent and complete.
```

## Virtual Try-On

```text
Dress the person in Image 1 using the clothing from Image 2.
Preserve the person's identity, face, facial features, skin tone, body shape, pose, hair, expression, and age.
Change only the clothing.
Fit the garment naturally to the body with realistic drape, folds, seams, occlusion, lighting, and shadows.
Preserve the original background, camera angle, and photo realism.
Do not alter the face, body proportions, pose, or environment.
```

## Sketch To Render

```text
Turn this sketch into a photorealistic image.
Preserve the exact layout, proportions, perspective, object placement, and overall design intent.
Choose realistic materials, textures, lighting, and environmental details consistent with the sketch.
Do not add major new objects or change the composition.
```

## Product White Background

```text
Extract the product from the input image and place it centered on a plain white opaque background.
Preserve product shape, proportions, packaging geometry, colors, logo placement, and label text.
Keep a crisp silhouette with clean edges, no halos, no fringing, and no missing details.
Add only a subtle natural contact shadow if it improves realism.
Do not rewrite, blur, or invent label text.
```

## Marketing Creative With Text

```text
Create a [billboard/social ad/poster] featuring the product from the input image.
Scene: [environment].
Product: preserve the exact product design, label, proportions, and colors.
Text EXACT, verbatim, no extra characters: "[copy]"
Typography: [font feel, color, size hierarchy].
Placement: [specific location].
Make the design look polished and commercially usable.
Do not add any other readable text, watermark, fake logo, or unrelated product.
```

## Weather Or Lighting Change

```text
Change the scene to [weather/time of day].
Change only environmental conditions: lighting, shadows, atmosphere, precipitation, sky, reflections, and ground wetness.
Preserve the original camera angle, perspective, object placement, subject identity, architecture, and composition.
Make the new lighting and shadows physically consistent.
```

## Object Removal

```text
Remove [object/person] from the input image.
Fill the removed area naturally using the surrounding background, texture, lighting, and perspective.
Preserve everything else exactly, including camera angle, subject identity, pose, background, shadows, and color.
Do not crop, reframe, or introduce new objects.
```

## Person Into Scene

```text
Use Image 1 as the person's identity reference.
Create a photorealistic scene where [person] is [action] in [environment].
Preserve the person's face, identity, hair, age, body type, and recognizable features.
Match the person to the scene with realistic scale, lighting, shadows, motion, and perspective.
Do not make the person look pasted in or stylized unless requested.
```

## Multi-Image Subject Into Base Scene

```text
Use Image 1 as the base scene.
Use Image 2 as the subject/object reference.
Place the subject from Image 2 [specific location] in Image 1.
Match lighting, perspective, scale, lens feel, shadows, and edge detail.
Preserve the base scene's background, camera angle, composition, and existing objects.
Preserve the subject's identity, shape, colors, markings, and key details.
```

## Character Consistency For Story Images

```text
Continue the story using the same character from the reference image.
Preserve the character's face, proportions, outfit, color palette, hairstyle, age, and illustration style.
New scene/action: [scene].
Composition: [framing].
Mood/lighting: [tone].
Do not redesign the character, change the outfit, change age, or shift art style.
```
