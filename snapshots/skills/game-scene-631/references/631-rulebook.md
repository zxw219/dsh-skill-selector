# 6:3:1 Scene Rulebook

Use this reference to translate a scene brief into visible hierarchy or to diagnose a generated scene.

## Source Status

These principles are adapted from the user-provided PDF *游戏美术中的 631 法则*, credited in that document to Douyin author 耿嘉辉, article ID 7680871898594512166. The source itself describes 6:3:1 as a practical experience ratio, not an industry standard or research-backed law. The exact numbers are therefore adjustable; the invariant is a clearly separated dominant, supporting, and accent order.

The first table below summarizes source-derived ideas. The later sections are operational adaptations for image-generation prompts and reviews.

## Source-Derived Six-Dimension Map

| Dimension | Dominant - about 60% | Supporting - about 30% | Accent - about 10% |
| --- | --- | --- | --- |
| Composition | planes and large masses: facade, ground, sky, broad shadow | lines and extensions: road, railing, cables, pipes, light shafts | compact high-contrast point: person, lamp, sign, doorway |
| Lighting | main light establishes time, weather, mood, and most shadow shape | skylight and bounce keep shadow information, depth, and color bias | small practical or emissive source creates an eye landing point |
| Color | dominant environmental palette, usually restrained or low saturation | secondary local colors on architecture and large props | small high-saturation accent; saturation may rise as area falls |
| Spatial layout | terrain, architecture, and large blockers make routes and boundaries legible | linear elements guide the eye and imply movement | sparse lived-in traces or small props provide evidence of use |
| Asset form | primary volume and readable silhouette | roofs, balconies, overhangs, attachments, and other secondary structures | handles, rivets, drains, trim, and other microdetail |
| Information density | quiet wall, ground, sky, fog, or shadow with little information | medium-density transition zone | dense focal cluster where attention should settle |

## Operational Adaptation for Image Generation

### 1. Composition

- Establish one dominant plane or mass before introducing linework and focal props.
- Use supporting lines to point toward, frame, or reveal the focal cluster. Avoid unrelated crossings that form a visual tangle.
- Keep the accent scarce. Several small lights, signs, or figures competing at equal contrast cease to function as an accent.
- Describe placement and scale in spatial terms: foreground frame, midground route, background landmark, upper-left light, lower-center subject, and so on.

### 2. Lighting

- Give the main light a motivated source and a coherent direction. It should define most large shadow shapes.
- Use sky fill, bounce, haze, or reflected color to preserve readable shadow information without flattening the image.
- Let practicals, windows, fire, neon, or screens identify the focal area rather than light the entire scene.
- Make the accent light meaningfully warmer or cooler than the main source when color contrast supports the brief.
- Avoid equal brightness everywhere, crushed black shadow with no structure, and many unrelated emissive colors.

### 3. Color

- Name a dominant environmental color family, a secondary structural family, and one accent family.
- Reserve the strongest saturation for a small area. Large saturated fields should appear only when explicitly required by the art direction.
- For game-navigation scenes, the accent color may consistently mark climbable, collectible, interactive, or route-critical elements. Do not invent gameplay coding when the user only wants a non-game cinematic image.
- Coordinate the color accent with the focal light and focal object when possible.

### 4. Spatial Layout and Set Dressing

- Make large terrain and architectural masses explain walkable space, walls, openings, and route direction before adding clutter.
- Use roads, walls, tree rows, pipes, railings, vehicles, or shadows as supporting eye-guides.
- Use litter, stains, posters, boxes, debris, and small traces of life sparingly. They imply history; they do not establish the composition.
- If the large spatial read is weak, remove or defer small props instead of adding more.

### 5. Asset Form

- Define the hero building or prop first as a simple readable primitive or silhouette.
- Add secondary structures to break monotony and clarify function.
- Concentrate microdetail where the viewer looks or where scale and use need explanation.
- If the silhouette fails, revise primary volumes before refining textures or ornaments.

### 6. Information Density and Materials

- Protect broad quiet regions so the focal cluster has room to register.
- Use medium detail as a transition from the dominant field toward the focus.
- Place the densest texture, edge contrast, story clues, and small forms near the focal area.
- Apply the same hierarchy to roughness: mostly rough or diffuse surfaces, fewer semi-gloss surfaces, and rare mirror-like highlights unless the brief requires another material logic.

## Prompt Construction Pattern

Use prose rather than a mechanical list when the target generator benefits from natural language, but preserve these functions:

1. Scene identity, story moment, and viewpoint.
2. Dominant large mass or quiet field.
3. Supporting route, structures, or directional lines.
4. One accent focal cluster and its location.
5. Main, ambient, and accent light relationship.
6. Dominant, supporting, and accent color relationship.
7. Detail-density and material hierarchy.
8. Camera, lens, depth, rendering style, aspect ratio, and user exclusions.

Prefer relational phrases such as `broad`, `secondary`, `sparse`, `isolated`, `dominant`, and `concentrated near the focal point`. Include `60/30/10` when it helps communicate intent, but do not rely on percentages alone.

## Failure Diagnosis

| Symptom | Likely cause | Smallest useful correction |
| --- | --- | --- |
| The eye has nowhere to land | too many accents or no contrast peak | keep one focal cluster and suppress competing lights, signs, or saturated props |
| The frame feels shredded | excessive ungrouped lines and microdetail | simplify into large masses, group lines, and restore quiet areas |
| Everything is bright but flat | main, ambient, and accent lights have equal strength | choose one dominant source, lower fill, and localize the accent |
| The image feels cheap or empty in shadow | ambient support is absent or shadows are crushed | add restrained bounce, color bias, haze, or reflected detail |
| The palette is tiring | saturated color covers too much area | desaturate the dominant field and confine strong color to the focal area |
| The space is hard to understand | clutter was designed before large layout | re-establish ground, walls, openings, and route lines; remove nonessential props |
| Assets are detailed but generic | primary silhouette and secondary structure are weak | redesign the large form before surface detail |
| Everything looks equally busy or glossy | density and roughness are uniform | enlarge quiet matte regions and localize dense or reflective material |

## Controlled Exceptions

Allow 8:1:1, 7:2:1, deliberate symmetry, or two equal opposing masses when the story or art direction benefits. State what hierarchy is being changed and preserve another clear organizing principle such as value separation, central symmetry, mirrored color, or opposing silhouettes. Do not call an accidental 5:3:2 conflict an intentional exception.
