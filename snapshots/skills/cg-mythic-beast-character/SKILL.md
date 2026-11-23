---
name: cg-mythic-beast-character
description: Generate compact Midjourney 8.2 prompts for stylized 3D anime CGI mythic-beast characters with porcelain anime faces, dominant silver-white groomed fur, luminous elemental energy, spectral beast spirits, and cinematic lighting. Use for white fox, dragon, Vermilion Bird, Azure Dragon, White Tiger, Black Tortoise, other Eastern fantasy beasts, male or female deities, wallpapers, character renders, and requests mentioning 超写实CG神兽、兽耳、神兽少女、神兽男神、白虎、朱雀、龙族 or the white-fur CG style.
metadata:
  author: MOKE
---

# 3D CG Mythic-Beast Character Prompt

Generate one copy-ready English Midjourney prompt that includes all parameters and negative terms and is no longer than 1024 characters, counting spaces and parameters.

## Workflow

1. Infer the character gender, mythic beast, eye color, head marker, hair accent, elemental energy, spectral spirit, backdrop, action, and aspect ratio. Default to an adult female deity, 16:9 wallpaper, and a stable one-arm casting pose.
2. Read [references/variants.md](references/variants.md) for listed beasts. For an unlisted beast, fill the same five slots: head marker, eyes, accent, energy, spectral spirit.
3. Assemble the prompt in the exact priority order below. Keep the face description minimal and keep fur as the dominant texture.
4. Count the final prompt. If it exceeds 1024 characters, remove secondary costume detail, particles, duplicate camera terms, duplicate lighting terms, then low-priority negative terms. Never remove the 3D medium anchor, identity slots, dominant white fur, spectral spirit, energy, face focus, parameters, or core anti-2D negatives.

## Prompt Order

Use this structure and replace bracketed slots:

```text
AAA stylized 3D anime game cinematic, pre-rendered CGI cutscene frame, [adult woman/adult man], [adult mythic role], delicate [masculine] anime face, porcelain skin with subsurface scattering, calm cold expression, half-lidded [eyes], [head marker], [hair], massive groomed white fur [collar/mantle] whipping in wind, pure white fur untouched by glow, [robes] with PBR silk and metal, [elemental energy] coiling around [her/him], translucent spectral [beast] winding through energy, one arm thrust toward camera, foreshortening, compressed [energy] sphere in palm, arcs between fingers, low-angle dynamic composition, face in focus, [dark background], volumetric rim light, cinematic depth of field, hyper-detailed 3D CGI --v 8.2 --ar [ratio] --raw --no [negatives]
```

## Hard Style Rules

- Start with `AAA stylized 3D anime game cinematic, pre-rendered CGI cutscene frame`. Do not start with `splash art`, `concept art`, `illustration`, or `anime screenshot`; they push Midjourney toward 2D.
- Keep the face to: anime face, porcelain skin, calm cold expression, half-lidded eyes, plus `masculine jawline` only for men. Do not stack detailed facial anatomy.
- Make groomed silver-white fur the visual subject. Restrict scales, feathers, and stripes to the headpiece, cheeks, or neck.
- Keep explosive body action and a calm face. Avoid fierce, glaring, or screaming expressions.
- Use `subsurface scattering`, `PBR silk and metal`, `volumetric rim light`, and `cinematic depth of field` to enforce three-dimensional CGI without turning the face into a real photograph.
- Do not use positive `photorealistic`, `real photo`, `octane render`, `unreal engine`, or `8k`.
- Always include anti-2D negatives: `2D illustration drawing painting flat anime screenshot photorealistic real photo`.
- For a single adult subject, use `child` only if needed; do not negate other genders when the user requests multiple characters. Add beast-specific animalization negatives from the reference only when they will not suppress the requested spectral beast. Describe a human face positively rather than broadly negating animal bodies.
- Place parameters after the description: `--v 8.2 --ar 16:9 --raw`, then `--no [negatives]` unless the user specifies another ratio.

## Output Contract

Return only one English prompt in a copyable code block, followed by one short line: `字符数：N/1024`. Do not add composition analysis or advice unless the user asks. If the user asks for variants, return the requested number of separately counted prompts (default up to three).

## Scope and Parameter Compatibility

User-specified character, action, palette, framing, count, language and output format override defaults. For another image platform, retain the visual direction and remove Midjourney-only syntax. Default to Midjourney 8.2 and explicitly include `--v 8.2`. If the user requests another version, use that version and verified supported parameters. Do not add `--preview`. Use integer aspect ratios, with all parameters after the visual description. Raw is a control option, not a guarantee of CGI or film texture. The 1024-character limit is this skill's compact-output convention, not a universal Midjourney limit; explicit user limits take precedence. Count the actual final prompt, excluding code fences, labels and the count line.

Version compatibility: https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
