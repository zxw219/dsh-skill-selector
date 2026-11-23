# Keyframes, Storyboards, and Blockouts

Four ways to hand Seedance 2.5 a visual plan instead of describing one in prose.

**Contents**
1. First and last frame (with extra references)
2. Multi-keyframe sequences
3. Storyboard grids
4. Blockouts — coarse vs fine
5. Coarse blockout template
6. Fine blockout template

---

## 1. First and last frame

No separate mode needed. In multimodal reference mode, declare the roles in the first lines. The system locks output aspect ratio to the **first** image; duration is set on the generation page or via API.

**Both anchor images must share the same aspect ratio** — a mismatch stretches the last frame.

```
@Image 1 is the first frame. It defines the opening composition, subject position, pose,
         prop state, scene, and camera direction.
@Image 2 is the last frame. It defines the ending composition, subject position, pose,
         prop state, scene, and camera direction.
@Image 3 defines <Subject A>'s <appearance, clothing, structure, or material>.
         Do not change the first-frame composition defined by @Image 1 or the last-frame
         composition defined by @Image 2.
@Image 4 defines <specified attributes> of <Subject B, prop, or scene>.
         Do not change the first-frame composition defined by @Image 1 or the last-frame
         composition defined by @Image 2.

<Describe one continuous action or event>.
The video begins naturally from the first frame defined by @Image 1 and reaches the last frame
defined by @Image 2 after the continuous action.
Between the first and last frames, maintain continuity in <character identity, prop structure
and ownership, scene layout, and camera direction>.
```

Describe each anchor on its own line. `@Images 1 and 2 are the first and last frames` does not assign roles. Supplementary references supply attributes only — they must never override the anchor compositions, hence the repeated do-not-change clause.

## 2. Multi-keyframe sequences

When separate images define successive stages of a process, open with the ordering instruction, then state the key state each image represents.

```
Use @Image 1 through @Image N as keyframes in this order.

@Image 1 is the first frame. It defines <opening composition, subject position, pose,
         prop state, and camera direction>.
@Image 2 defines the second keyframe: <visible end state of Stage 1>.
@Image 3 defines the third keyframe: <visible end state of Stage 2>.
@Image N is the last frame. It defines <ending composition, subject position, pose,
         prop state, and camera direction>.

The video passes through the states defined by @Image 1, @Image 2, @Image 3, and @Image N in
order, using continuous action to transition naturally between stages.
Maintain continuity in <subject identity, prop structure and ownership, scene layout, lighting,
and axis of action> throughout.
```

Separate keyframe images align more reliably than several frames combined into one grid image. Keyframes control **stage order and key states**, not exact frame reproduction.

## 3. Storyboard grids

A grid communicates story, shot order, and approximate composition. It is not a specification for exact reproduction.

**Grid requirements:** no more than 15 panels, clean line art or simple diagrams, minimal text labels.

```
@Image 1 provides an <N-panel storyboard grid> for shot order and approximate composition.
         Read it <left to right, top to bottom>. Do not use the grid's <line-art style,
         text labels, or placeholder characters>.
@Image 2 defines <Subject A>'s <appearance and clothing>.
@Image 3 defines <key prop or scene>'s <structure, material, or lighting>.

Shot 1: <shot size, subject action, and scene state>.
Shot 2: <shot size, subject action, camera movement, or transition>.
...
Shot N: <closing action and final visible state>.

The final video uses <visual style>. Audio includes <dialogue, ambience, action sound
effects, or music>.
```

The exclusion on line-art style and text labels is essential — without it, the sketch aesthetic and the panel captions render into the output.

## 4. Blockouts — identify the type first

| | Coarse blockout | Fine blockout |
|---|---|---|
| **Best for** | Previewing action, paths, blocking, camera movement, cuts | Re-rendering materials, colors, characters, scenes, style |
| **Material** | Simple geometry with clear relationships and a complete action sequence | Complete, clean model — no path lines, coordinate axes, controllers, camera frustums |
| **Prompt focus** | Map every geometric object to its final subject; state which temporal and spatial info to inherit | Preserve structure, action, and camera; define what to re-render |

Getting this wrong wastes a generation: treating a fine blockout as coarse discards structure you paid for; treating a coarse blockout as fine imports grey geometry into the output.

Avoid arms, wings, and other appendages in coarse geometry unless the action sequence is complete — partial appendages produce stiff motion or get misread structurally.

## 5. Coarse blockout template

A coarse blockout locks action paths, motion direction, blocking, entrances and exits, camera paths, cut points, lighting changes, and sound rhythm.

| Blockout carries | State in the prompt |
|---|---|
| Path | Trajectory, motion direction, subject blocking, entrance/exit order |
| Camera movement | Position, path, direction, speed changes |
| Lighting | Direction, brightness changes, and when they occur |
| Cuts | Cut positions, and subject/composition before and after each |
| Audio | Whether to inherit dialogue, music, ambience, or action SFX |

```
@Video 1 is a coarse blockout reference. It provides only <motion paths, subject blocking,
         camera position, camera movement, cuts, lighting changes, sound rhythm, or spatial
         relationships>. Do not use its blockout appearance, materials, or scene.
<Blockout Subject A> in @Video 1 corresponds to <Subject A>.
<Blockout Subject B or geometric prop> in @Video 1 corresponds to <Subject B or key prop>.
@Image 1 defines <Subject A>'s <appearance, clothing, or structure>.
@Image 2 defines <specified attributes> of <Subject B, key prop, or scene>.

<Subject> completes <primary action or event> in <scene>.
Keep <motion path, blocking, camera movement, cuts, lighting, or sound rhythm> from @Video 1.
The final video uses <characters, scene, materials, and visual style>.
Audio includes <dialogue, ambience, or action sound effects>.
```

Every geometric object needs its own `corresponds to` line — same discipline as character mapping.

## 6. Fine blockout template

```
@Video 1 is a fine blockout reference. Preserve <subject structure, action, spatial layout,
         camera position, camera movement, and cuts>. Do not use its original gray materials
         or empty background.
@Image 1 defines <subject>'s <character appearance, material, color, or surface details>.
@Image 2 defines <scene>'s <space, materials, lighting, or visual style>.

Re-render <subject> from @Video 1 as <final subject>, and re-render the scene as <final scene>.
Keep <structure, action, camera treatment, and spatial relationships> from @Video 1.
Use <materials, colors, and style>. Audio includes <ambience, sound effects, or music>.
```

Clean the blockout before uploading. Production markers — path lines, axes, controllers, camera frustums — get read as geometry and rendered as objects.
