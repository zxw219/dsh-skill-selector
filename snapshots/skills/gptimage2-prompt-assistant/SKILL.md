---
name: gptimage2-prompt-assistant
description: Write, rewrite, diagnose, and improve prompts for GPT Image 2 / gpt-image-2 image generation and editing. Use when the user asks for image prompt help, text-to-image prompts, image-to-image prompts, multi-image compositing, style transfer, character consistency, product mockups, virtual try-on, image text rendering, storyboards, or wants a Chinese prompt converted into a precise GPT Image 2 prompt.
---

# gptimage2提示词助手

## Goal

Produce practical GPT Image 2 prompts that separate the creative goal from the editing constraints. Favor controllability over poetic wording.

## Default Workflow

1. Identify the task type:
   - `text-to-image`: create from text only.
   - `image-to-image`: edit or transform one input image.
   - `multi-image`: combine references, subjects, products, outfits, or scenes from multiple images.
   - `iteration`: improve a previous result while preserving the parts that worked.
2. Ask only for missing information that changes the output materially. If enough context exists, make reasonable assumptions and proceed.
3. Rewrite the request into a structured prompt with:
   - Goal
   - Input image roles, when images are provided
   - Required changes
   - Must preserve
   - Style, medium, lighting, camera/composition
   - Text to render, if any
   - Negative constraints
4. For editing tasks, explicitly state what must remain unchanged on every iteration.
5. Return the final prompt first. Add a short note explaining why it is structured that way only when helpful.

## Core Prompt Rules

- Put the intended use early: ad, UI mockup, product photo, storyboard frame, infographic, comic panel, social post, catalog image.
- Be concrete about subject, material, shape, texture, environment, lighting, and composition.
- For photorealism, include `photorealistic`, `real photograph`, or `shot on a real camera` when the target should look like a photo.
- For complex prompts, use short labeled sections instead of one long paragraph.
- Prefer explicit preservation rules: identity, face, body shape, pose, camera angle, layout, background, logo, label text, product geometry.
- Prefer small iterative edits. When revising a previous result, say what worked and what must not drift.
- Do not rely on negative prompts alone. Say the desired positive result clearly, then add concise prohibitions.
- For `gpt-image-2`, do not depend on `input_fidelity`; treat prompt clarity as the main control surface.

## Task Patterns

### Text To Image

Use this structure:

```text
Create [asset type / intended use].
Scene/background: ...
Main subject: ...
Key details: ...
Style/medium: ...
Composition: ...
Lighting/color: ...
Quality constraints: ...
Do not include: ...
```

### Image To Image

Use this structure:

```text
Edit the input image to [goal].

Change only:
- ...

Preserve exactly:
- subject identity / product geometry / layout
- pose, camera angle, perspective, framing
- background and surrounding objects, unless specified
- lighting direction, shadows, color temperature, and texture continuity

Output style:
- ...

Do not:
- add extra objects, text, watermarks, logos, or unrelated changes
```

### Multi-Image Compositing

Name each input image by role:

```text
Use Image 1 as the base scene.
Use Image 2 as the subject/reference object.
Use Image 3 as the style/material/outfit reference.

Place [subject from Image N] into [location in Image 1].
Match lighting, scale, perspective, shadows, and edge detail.
Preserve Image 1 background, camera angle, and composition.
Preserve the subject identity/shape/details from Image N.
```

### In-Image Text

- Put exact text in quotes.
- Say `EXACT, verbatim, no extra characters`.
- Specify placement, hierarchy, font feel, color, and maximum number of text blocks.
- Add `Do not add any other readable text`.

### People And Identity

When identity matters, lock:

```text
Preserve the person's identity, face, facial features, skin tone, hair, body shape, pose, expression, and age. Do not beautify, age-change, face-swap, or alter recognizable features.
```

### Products

When product accuracy matters, lock:

```text
Preserve product shape, proportions, packaging geometry, logo placement, label text, material finish, color, and edge silhouette. Keep all readable label text sharp and unchanged.
```

## Output Format

When the user asks for a prompt, return:

```text
[Final prompt]
```

When useful, also include:

- `可选参数建议`: size, quality, number of variants.
- `为什么这样写`: one or two short bullets.
- `还缺的信息`: only if essential.

For detailed reusable examples, load `references/prompt-patterns.md`.
