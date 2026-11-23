# SFX Editing Playbook

## 1. Layer Hierarchy

Build the soundtrack from causal layers:

1. dialogue, narration, breath, effort;
2. room tone and ambience;
3. body, cloth, footsteps, handled props;
4. hard source effects;
5. designed/subjective effects;
6. music;
7. intentional silence.

At each beat choose one foreground owner. More layers do not automatically create more weight.

## 2. Select By Physical Evidence

For each sound object specify:

```text
source + material + action + size/mass + speed + distance + direction
+ environment/reflections + transient + body/resonance + tail + realism/stylization
```

Match material before magnitude. A quiet correct metal contact is more credible than a loud generic boom.

## 3. Timing Grammar

- **prelap**: begin ambience/mechanism before the cut to pull the viewer forward;
- **exact sync**: use for visible contact, latch, click, landing, title/button;
- **delayed body**: transient first, low resonance 20–120 ms later for mass;
- **trail/bridge**: let tail cross the cut to connect space/time;
- **suck-back**: reverse motion into a cut, reveal, or disappearance;
- **silence pocket**: remove bed/music immediately before an important transient;
- **subjective smear**: widen/slow/filter after shock, memory, or loss of orientation.

Do not place every whoosh exactly on the cut. Align its energy peak to the moment of fastest motion or reveal.

## 4. Common Recipes

### Visual transition

```text
air/swish onset -> peak at movement/reveal -> short tonal or environmental tail
```

Use light whooshes for framing/camera motion; use heavy whooshes only when mass or scale is visible.

### Heavy impact

```text
preload detail -> sharp material transient -> low-mid body -> environment/debris -> reaction/settle
```

Offset layers slightly. Avoid stacking identical transients at sample-exact time.

### UI/product detail

```text
clean click/tick -> tonal confirmation -> optional tiny airy tail
```

Keep the sound proportional to the graphic. Premium does not mean louder or brighter.

### Tech/glitch

Use glitch to indicate a real state change, signal failure, data interruption, or viewpoint rupture. Avoid random glitch decoration on every cut.

### Foley

Footsteps follow weight transfer, surface, pace, footwear, distance, and camera perspective. Cloth precedes or follows body motion rather than landing on every limb movement.

### Ambience

Use a continuous bed plus selective foreground details. Crossfade room tones across cuts; do not insert absolute digital silence unless subjectivity demands it.

## 5. Perspective And Processing

- distance: reduce highs/transients, narrow stereo, add early reflections;
- close subjective: emphasize breath, cloth, contact detail, internal resonance;
- large exterior: separate transient from delayed environment response;
- behind glass/door/helmet: low-pass plus enclosure resonance;
- fast pass-by: level/pan motion plus changing spectrum; use Doppler only when speed/path justify it;
- slow motion: preserve one sharp proof transient or the result may feel weightless.

## 6. Bundled Library

The local CC0 library is under `assets/sfx/` and contains:

- `impacts`: generic, metal, glass, wood, soft, punch, plate, bell;
- `foley`: footsteps, cloth, doors, books, knives, coins, leather, props;
- `ui`: clicks, selects, confirmation, error, glitch, open/close, toggle;
- `digital`: lasers, phase motion, power-up, zaps, tonal tech cues;
- `whoosh`: light/heavy swishes and air movement;
- `ambience`: wind beds.

Search it before downloading new material:

```powershell
python scripts/search_sfx.py "重型金属撞击" --limit 6
python scripts/search_sfx.py "轻微转场呼啸" --category whoosh --plan-snippet
```

Read `references/sfx-catalog.json` for machine-readable metadata and `references/sfx-sources.json` for source/license provenance.

## 7. Placement And Mix Rules

- Start with conservative gains, usually -12 to -6 dB per one-shot before final context balancing.
- High-pass tiny UI/cloth sounds when low-frequency noise is irrelevant.
- Do not normalize every effect to the same peak; preserve scale relationships.
- Use short fades to prevent clicks, not to erase the transient.
- Use `sfx` entries in the mix plan; the renderer outputs `sfx-edit.wav` and includes it in `full-mix.wav`.
- Dialogue remains foreground unless the story intentionally masks it.
- Listen to SFX with music and production audio; solo quality is not mix quality.

## 8. Library Expansion Gate

Download a new sound only when the local library lacks the required source, material, scale, perspective, or tail. Prefer CC0. Record source page, direct file URL, license, retrieval date, and SHA-256; rebuild the catalog and audition the file before use.
