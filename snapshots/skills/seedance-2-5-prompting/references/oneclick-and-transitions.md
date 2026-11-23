# One-Click Video and Seamless Transitions

Two assembly modes: turning a batch of images into a finished edit, and generating bridge content between two clips.

**Contents**
1. One-click video — the six-part order
2. One-click template
3. One-click worked example
4. Seamless transitions — the seven-part order
5. Transition methods
6. Transition template and example

---

## 1. One-click video — the six-part order

Designed to organise multiple images (optionally plus a style-reference video) into a complete video with consistent pacing and packaging.

```
Material Roles → Image Order → Motion Amount → Editing Style → Visual Treatment → Audio
```

`Turn these materials into a video` is not a prompt. Without stated roles and order, the model picks both, and character identities mix.

## 2. Template

```
[Material Roles]
@Image 1 is used for <character, product, scene, or opening image>.
@Image 2 is used for <character, product, scene, or process image>.
@Image 3 is used for <character, product, scene, or ending image>.
@Video 1 is used only for <editing rhythm, transitions, subtitle treatment, or music style>.
         Do not use its character identities or scene. (optional)

[Arrangement]
Show the images in <upload order, a specified order, or a model-selected thematic order>.
<State the character, product, location, and event relationships that must remain consistent>.

[Image Motion]
Apply <subtle live motion, parallax, push-in/pull-out, lateral movement, or local action>
to each image.
Keep <subject appearance, product structure, text, or background relationships> stable.

[Final Style]
Use <editing rhythm, transition style, subtitle or graphic treatment, and color style>.

[Audio]
Include <dialogue, ambience, sound effects, or music>.
```

If order matters, state the exact sequence. If the model may arrange freely, say it may organise by theme — but say which. With several characters or products present, keep naming and binding each one separately, exactly as in the multi-reference system.

## 3. Worked example

```
[Material Roles]
@Image 1 is used for the night-market entrance and opening environment.
@Image 2 is used for <Traveler> walking along the street.
@Image 3 is used for the lantern stall and craft details.
@Image 4 is used for three friends eating together.
@Image 5 is used for the riverside night view and reflections.
@Image 6 is used for the final group photo by the bridge.
@Video 1 is used only for light editing rhythm, hand-drawn stickers, and transition style.
         Do not use its character identities or locations.

[Arrangement]
Show @Image 1 through @Image 6 in order to form a complete sequence: arrival, street
exploration, dinner, riverside walk, and group photo.
Keep the three friends' appearances and clothing consistent. Do not mix their identities.

[Image Motion]
Use slow push-ins and subtle parallax for environment images. Add only natural blinking, head
turns, glass-raising, and slight clothing movement to character images.
Keep stall structure, table position, and bridge railing stable.

[Final Style]
Use an upbeat travel-video rhythm. Connect scenes with natural occlusion and similar colors.
Keep hand-drawn stickers at the frame edges.

[Audio]
Retain night-market chatter, light dish sounds, and riverside wind, with upbeat but
unobtrusive instrumental music.
```

Note how motion is specified differently for environment images (camera-driven) and character images (small local actions). Applying one motion instruction to all images flattens the result.

## 4. Seamless transitions — the seven-part order

Generates continuous bridge content between two videos.

```
Before Video → After Video → Trigger Action → Camera Movement → Visual Transformation → Arrival State → Audio
```

## 5. Transition methods

| Method | What to specify |
|---|---|
| Dive or reverse movement | Camera direction, speed change, when the next scene begins |
| Character rotation | Pose, rotation direction, how clothing or background changes continuously |
| Foreground occlusion | When the foreground object fills the frame, and the composition that follows |
| Object morph | Corresponding shapes, materials, the transformation process |
| Push/pull or focus change | Camera movement, focus target, continuous spatial relationship |

Object morph is the strongest when the two clips share a shape — a circular umbrella edge becoming a circular skylight ring, for instance. Look for the rhyme before choosing the method.

## 6. Template and example

```
@Video 1 is the before-transition clip. Use its <ending subject, action, composition, camera
         direction, and audio>.
@Video 2 is the after-transition clip. Use its <opening subject, composition, camera direction,
         and audio>.
Keep <character identity, product structure, scene, and primary action> stable in the original
portions of @Video 1 and @Video 2.

At the end of @Video 1, <subject or foreground object> triggers the transition through <action>.
The camera <movement direction and speed change>, while <shape, material, light, or space>
gradually transforms into <corresponding element> at the start of @Video 2.
The transition ends naturally at @Video 2's opening composition, preserving continuity in
<subject position, camera direction, and motion trend>.
Audio transitions smoothly from <before audio> to <after audio>.
```

**Example:**

```
@Video 1 is the before-transition clip. Use its rainy night street, red umbrella, slow push-in,
         and rain sound.
@Video 2 is the after-transition clip. Use its circular gallery skylight, upward camera
         movement, and quiet interior reverberation.
Keep the people, street, gallery structure, and primary actions in the two original videos stable.

At the end of @Video 1, the red umbrella approaches the camera and gradually fills the entire
frame, triggering the transition.
The camera continues moving forward. The umbrella's circular edge gradually becomes the
skylight's metal ring, and the red fabric transitions into white daylight passing through the
skylight.
The transition ends naturally at @Video 2's upward-looking opening composition, with the camera
movement changing smoothly from forward motion to an upward rise.
The rain gradually fades into footsteps reverberating inside the gallery.
```

The camera move is described as *continuous through* the transition — forward motion resolving into an upward rise. A transition that stops one movement and starts another reads as a cut, not a bridge.

The goal is visual and audio continuity. The generated bridge is not a pixel-identical edit splice of the two sources.
