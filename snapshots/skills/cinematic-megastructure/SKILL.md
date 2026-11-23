---
name: cinematic-megastructure
description: Generate compact Midjourney 8.2 prompts for cinematic live-action megastructure compositions with an overwhelming scale contrast, at least 40 percent negative space, cropped monumental forms, tiny silhouettes for scale, atmospheric perspective, one soft light source, and a restrained monochromatic palette. Use for 巨构、超级建筑、巨物、大场景、电影感构图、轨道电梯、方舟、太空设施, or inputs such as 大:巨物 小:人物.
metadata:
  author: MOKE
---

# Cinematic Megastructure Prompt

Generate one copy-ready English Midjourney prompt that includes parameters and negative terms and is no longer than 1024 characters, counting spaces and parameters.

## Parse the Request

Extract:

1. One megastructure: required. If several are supplied, select the dominant one unless the user requests separate variants.
2. Scale reference: default to three to five tiny silhouetted figures, each approximately 1/100 to 1/150 of frame height.
3. Environment: default to a salt desert, dark sea, barren plain, or fog field suited to the object.
4. Mood: default to quiet awe, oppressive stillness, one monochromatic range, and one soft light source.

Do not ask questions when these defaults can resolve missing details.

## Composition Laws

- Keep a known scale reference visible.
- Reserve at least 40 percent negative space. Let the structure occupy approximately 40 to 60 percent of the frame.
- Crop the top or one side beyond the frame. Use cropping by default; show the full structure when the user explicitly requests it.
- Set the horizon between the bottom fifth and bottom third.
- Use base fog, atmospheric haze, aerial perspective, and distant edges fading into air. Do not make the whole image equally sharp.
- Use one soft key light and one monochromatic palette with at most one accent color.
- Prefer backlit silhouettes, central symmetry, or strict thirds.
- Default to 21:9.

## Prompt Order

Use this structure and replace bracketed slots:

```text
cinematic live-action sci-fi film still, a colossal monolithic [megastructure] in [environment], extreme wide shot, [angle] anamorphic 65mm IMAX framing, structure occupies [40-60]% of frame and [top/side] is cropped beyond the edge, low horizon at [bottom fifth/third], over 40% negative space, [tiny scale references] for scale, each about 1/[50-200] of frame height, [symmetry/thirds], single soft [light direction], backlit silhouettes, monochromatic [palette] with one [accent], physically plausible [materials], base buried in volumetric fog, atmospheric haze, aerial perspective, distant edges fading into air, restrained detail, [mood], realistic monumental architecture --v 8.2 --ar 21:9 --raw --no clutter busy composition oversaturated colors multiple light sources lens flare concept art illustration video game art full structure visible large people text watermark
```

## Hard Style Rules

- Start with `cinematic live-action sci-fi film still`, not `concept art` or `illustration`.
- Describe observable cinematography instead of relying on a director name: extreme-wide framing, low horizon, negative space, cropped structure, restrained detail, single-source backlight, monochromatic color, and atmospheric depth.
- Always state a numerical structure share and scale-reference ratio.
- Keep materials physically plausible. Avoid decorative surface overload and dense city clutter.
- Place parameters after the description: `--v 8.2 --ar 21:9 --raw`, then `--no [negatives]` unless the user specifies another ratio.
- Keep the fixed negative core: `clutter busy composition oversaturated colors multiple light sources lens flare concept art illustration video game art full structure visible large people text watermark`.

## Length Control

Count the final prompt. If it exceeds 1024 characters, remove secondary material adjectives, secondary mood words, redundant camera terms, then optional accent-color wording. Never remove the scale reference, numerical ratio, negative-space percentage, crop instruction, fog, single light, palette, aspect ratio, or negative core.

## Output Contract

Return only one English prompt in a copyable code block, followed by one short line: `字符数：N/1024`. Do not output tables, ASCII diagrams, Chinese translations, or explanations unless requested. If the user asks for variants, return the requested number of separately counted prompts (default up to three) with different camera angles while keeping all composition laws.

## Scope and Parameter Compatibility

User-specified character, action, palette, framing, count, language and output format override defaults. For another image platform, retain the visual direction and remove Midjourney-only syntax. Default to Midjourney 8.2 and explicitly include `--v 8.2`. If the user requests another version, use that version and verified supported parameters. Do not add `--preview`. Use integer aspect ratios, with all parameters after the visual description. Raw is a control option, not a guarantee of CGI or film texture. The 1024-character limit is this skill's compact-output convention, not a universal Midjourney limit; explicit user limits take precedence. Count the actual final prompt, excluding code fences, labels and the count line.

Version compatibility: https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
