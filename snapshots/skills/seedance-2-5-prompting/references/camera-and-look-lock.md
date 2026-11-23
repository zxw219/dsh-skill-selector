# Camera and look lock

The capture format written once at the head of the prompt and inherited by every shot below it. Without it, a multi-shot prompt re-rolls grain, contrast, depth of field and skin tone at each cut, and the sequence stops reading as one piece of footage.

## Placement

First block in the prompt, above cast, location and shots.

```
[LOOK — LOCKED, APPLIES TO EVERY SHOT]
<camera body / capture format>, <lens set>, <stock or sensor>, <optical format>, <T-stop>,
<depth of field>, <grain>, <highlight behaviour>, <black level>, <contrast>.
<Grade name>: <hero tone>, <secondary field>, <shadow bias>.
<Camera operation>. <Performance and audio baseline>.
```

Per-shot blocks then carry only what changes: shot size, focal length, camera move, blocking. Never restate the look — repeating it invites the model to re-interpret it.

## The one rule that makes it work

**Every named piece of gear is followed by its visible consequence.** Seedance does not simulate an Arricam. The name biases the output; the description controls it. Strip the descriptions and the block degrades into decorative noise.

| Weak | Working |
|---|---|
| `Arricam LT, Cooke S4/i primes, Kodak Vision3 500T` | `Arricam LT, Cooke S4/i primes, 35mm Kodak Vision3 500T — shallow depth of field, halation on highlights, fine organic grain, lifted milky blacks, low contrast` |
| `shot on anamorphic` | `anamorphic: oval bokeh, horizontal blue flare across highlights, soft frame edges` |
| `T2.8` | `T2.8 — background falls out of focus one metre behind the subject` |

This is the same pairing the main file requires for niche camera terms. It applies to bodies, glass, stocks and filtration equally.

## Camera bodies and capture formats

| Named format | Visible signature to write alongside it |
|---|---|
| Arricam LT / ARRI 435 (35mm film) | organic grain, halation on highlights, soft highlight roll-off, no digital edge sharpening |
| ARRI Alexa 35 | wide latitude, gentle highlight roll-off, natural skin, near-noiseless shadows |
| ARRI Alexa LF / Mini LF | large-format: wider field at the same framing, shallower focus fall-off, subject separation without long lenses |
| Sony Venice 2 | clean neutral base, deep retained shadow detail, slightly cooler bias |
| RED V-Raptor / Komodo | high acuity, crisp edge definition, punchier contrast |
| Panavision Millennium DXL2 | large-format softness in highlights, gentle skin rendering |
| 16mm (Aaton XTR, ARRI SR3) | coarse visible grain, softer resolution, texture over detail, documentary weight |
| Super 8 | heavy grain, gate weave, muted desaturated colour, soft corners |
| VHS camcorder | interlaced smear on motion, chroma bleed on reds, tracking noise, low resolution |
| Phone front camera | deep focus throughout, wide field, flat HDR contrast, digital sharpening, autofocus hunting |
| DSLR (5D-era) | shallow depth wide open, mild moiré, video-grade highlight clipping |

## Lens sets

| Named set | Visible signature |
|---|---|
| Cooke S4/i | warm skin rendering, creamy controlled bokeh, soft flare, gentle contrast |
| Zeiss Master Primes | clinical sharpness, high contrast, neutral colour, sharp corners |
| Zeiss Super Speeds | low contrast wide open, glow around highlights, warmer cast |
| Panavision C-series anamorphic | 2x squeeze, oval bokeh, horizontal blue flare, edge softness, focus breathing |
| Panavision E-series anamorphic | anamorphic separation with restrained flaring, cleaner edges |
| Lomo / Kowa anamorphic | pronounced distortion, strong streak flares, dreamy edge fall-off |
| Angénieux Optimo zoom | neutral rendering, holds contrast through the zoom range |
| Helios 44-2 / vintage Canon FD | swirling background blur, low contrast, strong veiling flare |
| Black Pro-Mist 1/4–1/2 (filtration) | bloom around highlights, lifted blacks, softened micro-contrast |

## Stocks and grade base

| Named stock | Visible signature |
|---|---|
| Kodak Vision3 500T | fast tungsten stock, visible grain, warm under practicals, cool-blue cast in uncorrected daylight |
| Kodak Vision3 250D | daylight balanced, fine grain, clean neutral colour |
| Kodak Vision3 50D | finest grain, dense saturation, needs strong light |
| CineStill 800T | red halation bloom around lights, night neon palette |
| Fuji Eterna | muted greens, low saturation, soft palette |
| Ektachrome / reversal | high contrast, saturated colour, deep blacks |
| Kodak Double-X 5222 | black and white, coarse grain, hard contrast |

Grade descriptors that behave predictably: lifted milky blacks, crushed contrast, bleach bypass (desaturated, silvery, high contrast), teal-orange separation, warm golden-hour bias, cool blue night bias, hazy sun bloom, chromatic blue shadows.

Naming a grade — `Riviera Gouache grade:`, `Bleach Bypass grade:` — then defining it in the same line gives the model a label to hold across shots. The label alone means nothing; the definition after the colon does the work.

## Camera operation

| Operation | Visible signature |
|---|---|
| Handheld with micro-drift, never locked off | constant small frame movement, no perfectly static frame |
| Shoulder-mount documentary | reactive reframing, slight overshoot at the end of pans |
| Steadicam | smooth floating glide, no footfall bounce |
| Gimbal | very smooth, faintly weightless motion |
| Dolly on track | constant mechanical speed, no drift |
| Locked-off tripod | static frame, movement comes only from the subject |

## Ready-made presets

**Sun-bleached Riviera**
```
Arricam LT, Cooke S4/i primes, 35mm Kodak Vision3 500T, spherical, T2.8, shallow depth of
field, halation on highlights, fine organic grain, lifted milky blacks, low contrast, no
sharpening. Riviera Gouache grade: terracotta-warm skin as the hero tone, aqua-teal sea and
sky field, cream sand, chromatic blue shadows, hazy sun bloom. Handheld with micro-drift,
never locked off. Naturalistic performance, real dialogue sync, no music.
```

**Clean commercial gloss**
```
ARRI Alexa 35, Zeiss Master Primes, T4, deep focus with controlled background separation,
no visible grain, gentle highlight roll-off, neutral colour, clean shadows. Product grade:
true whites, saturated brand colour, soft specular highlights on surfaces. Motion-control
dolly, constant speed. No handheld movement.
```

**Anamorphic night neon**
```
ARRI Alexa LF, Panavision C-series anamorphic, T2.0, oval bokeh, horizontal blue flare
across practicals, soft frame edges, red halation bloom around light sources, deep blue
shadows, wet reflective surfaces. Steadicam glide at walking pace.
```

**16mm documentary**
```
ARRI SR3, Zeiss Super Speeds, 16mm Kodak Vision3 500T, coarse visible grain, softer
resolution, low contrast wide open, glow around highlights, muted palette. Shoulder-mount
handheld with reactive reframing and slight overshoot on pans. Available light only.
```

**Phone UGC**
```
Phone front camera held at arm's length, wide field, deep focus throughout, flat HDR
contrast, digital sharpening, occasional autofocus hunting, mixed indoor colour
temperature. Handheld with natural arm sway. Direct-to-camera address, room-tone audio.
```

**Camcorder nostalgia**
```
Consumer VHS camcorder, interlaced smear on motion, chroma bleed on reds, tracking noise
at the frame edge, low resolution, blown-out window highlights, timestamp overlay in the
corner. Handheld, unsteady, frequent small reframes.
```

## What stays out of this block

- Shot size, camera moves, blocking — those belong in the per-shot blocks.
- Delivery aspect ratio. Optical format (`spherical`, `anamorphic`) describes the glass and belongs here; `9:16` or `1080p` are generation-page settings and must not appear in prompt text.
- Contradictory descriptors. `low contrast, lifted milky blacks` and `deep rich blacks` in the same block average into a flat mid-grey.
- Bare negatives. `no HDR, no sharpening` is weaker than the positive form: `soft highlight roll-off, unsharpened organic texture`. Where a ban matters, phrase it as substitution — not X, instead Y.
- More than roughly three lines. Past that the model starts averaging the adjectives rather than applying them.

## Checks

- Does every named body, lens, stock and filter have its visible consequence written next to it?
- Is the grade label defined in the same line where it is named?
- Is the camera operation stated once here rather than repeated per shot?
- Do any two descriptors in the block cancel each other out?
- Are per-shot blocks free of look descriptors?
