# Video Editing and Extension

Working from an existing video: editing it in place, or generating content before or after it.

**Contents**
1. Locked parameters — read before promising anything
2. Editing: the general pattern
3. Subject replacement
4. Background replacement
5. Audio editing
6. Forward extension
7. Backward extension
8. Extension with additional references

---

## 1. Locked parameters

These tasks inherit parameters from the input material. They cannot be overridden on the generation page or via API — so don't accept a brief that requires it.

| Task | Aspect ratio | Duration |
|---|---|---|
| Video editing | Inherits input video's — not settable | Inherits input video's — not settable. Frame handling may shift it by up to ~0.3s |
| First-frame or first-and-last-frame | Inherits the **first** image's — not settable | Settable |
| Video extension | Inherits input video's — not settable | Settable |

For first/last-frame work, mismatched anchor ratios stretch the last frame. Match them before uploading.

## 2. Editing: the general pattern

Every edit prompt declares four things: the sole editing master, the edit scope, the target material, and what must not change. Missing any one of them produces collateral changes.

```
[Edit Goal]
Edit @Video 1. Within <the entire video or a specific time range>, <add, remove, replace,
or adjust> <visual object, region, or audio category>.

[Source Video Role]
@Video 1 is the sole editing master. It defines <characters, scene, actions, composition,
camera movement, occlusion relationships, audio, and event order>.

[Target Material Role]
@Image 1 or @Audio 1 defines <specified attributes of the target object or sound>.

[Edit Scope]
Modify only <object, region, time range, or audio category>.

[Content to Preserve]
Keep <visual content, motion, audio, and timing relationships that must not change> from @Video 1.
```

**Example — lighting change on a time range:**

```
[Edit Goal]
Edit @Video 1. Only from 4-7 seconds, change the cool blue light on the right wall to warm
orange light.

[Source Video Role]
@Video 1 is the sole editing master. It defines the character, room layout, actions,
composition, camera movement, audio, and event order.

[Edit Scope]
Change only the light color on the right wall and the area it illuminates. Allow the
character's skin tone to respond naturally to the environmental light.

[Content to Preserve]
Keep the character's identity, clothing, expression, position, motion, room structure,
camera movement, dialogue, and ambience from @Video 1.
```

Note the deliberate permission granted inside the scope — skin tone responding to the new light. Without it, the model may hold skin tone rigid and produce an object that glows without affecting anything around it.

## 3. Subject replacement

The distinctive part is **timeline inheritance**: the replacement must adopt every appearance, exit, occlusion, and speed change of the original.

```
[Edit Goal]
Edit @Video 1. Change only <original object> to <target object>.

[Source Video Role]
@Video 1 is the sole editing master. It defines the original scene, camera position, camera
movement, motion path, occlusion relationships, and event order.

[Target Reference Role]
@Image 1 defines <target object>'s <appearance, structure, or material>.
         Do not use <irrelevant background, people, or composition>.

[Edit Scope]
Modify only <specific object and area>. The entire video contains <number> target object(s).
Do not modify <content to preserve>.

[Timeline Inheritance]
<Target object> inherits every appearance, motion, occlusion, and exit of <original object>,
including timing, duration, path, and speed changes.
Except for the object or area explicitly modified above, keep all other people, props, scene
content, camera movements, cuts, and event order from @Video 1 unchanged.
```

State the target count explicitly (`The entire video contains exactly one white folding desk lamp`). Replacements duplicate otherwise.

## 4. Background replacement

```
[Edit Goal]
Edit @Video 1. Replace only <original background area> with <target environment> from @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the people, foreground objects, actions,
composition, camera movement, and event order.

[Target Reference Role]
@Image 1 defines only <target environment>'s spatial layout, materials, depth of field,
ambient color, and lighting direction. Do not use the people or foreground objects in the image.

[Edit Scope]
Modify only <background outside the subject's silhouette>. Do not modify <subject identity,
facial features, hairstyle, clothing, expression, position, size, or motion>.

[Timeline Inheritance]
Keep the character actions and occlusion relationships from @Video 1. Except for the object or
area explicitly modified above, keep all other people, props, scene content, camera movements,
cuts, and event order from @Video 1 unchanged.
```

`outside the subject's silhouette` is the phrase that keeps the edit from creeping onto the person.

## 5. Audio editing

Dialogue, language, voice, music, and sound effects are separately editable. Name the speaker or sound category, the change, and which other sounds stay.

```
Edit @Video 1. Remove only the original background music. Keep the character dialogue, lip
sync, ambience, and action sound effects; preserve the visuals, camera treatment, and editing
rhythm from @Video 1.

Edit @Video 1. Change <Presenter>'s spoken language to natural American English while
preserving the dialogue content and speaking times. Keep all other character voices, background
music, ambience, and visuals from @Video 1.
```

Language swaps need `preserving the dialogue content and speaking times` — otherwise the new delivery reflows and lip sync drifts.

## 6. Forward extension (after the original)

Describe the boundary state **first**, then what happens next. The extension's first frame continues from the source's last frame.

```
@Video 1 is the source video to extend forward.

Extend @Video 1 forward. The first frame of the extended segment directly continues from the
last frame of @Video 1. Maintain continuity in <subject pose and orientation>, <prop position>,
<background and spatial relationships>, <camera position and composition>, <lighting>, and
<motion direction>.

Then, <describe the new action, event, camera treatment, or audio to add>.

Throughout the extension, maintain continuity in <character identity and clothing>, <key props>,
<background layout>, and <axis of action>.
Keep each subject as the same continuous instance throughout: do not duplicate or split it, and
keep the person's appearance or the object's number of parts stable.
```

The "same continuous instance" line prevents the classic extension failure where a subject splits into two or gains limbs at the seam.

## 7. Backward extension (before the original)

Reverse the order: describe the new content first, then define the source's first frame as the **explicit end state** of the extension.

Writing only "then connect to the source video" is the trap — it lets later characters or effects appear too early, or lets the image keep changing after it has already reached the target state.

```
@Video 1 is the source video to extend backward.

Extend @Video 1 backward. Before the source video begins, <describe the preceding action,
event, camera treatment, or audio>.

The last frame of the extended segment naturally connects to the first frame of @Video 1:
<subject pose and orientation>, <prop position>, and <background and spatial relationships>.
Match the <camera position and composition>, <lighting>, and <motion direction> of
@Video 1's first frame.

Throughout the extension, maintain continuity in <character identity and clothing>, <key props>,
<background layout>, and <axis of action>.
Keep each subject as the same continuous instance throughout.
```

## 8. Extension with additional references

Define every material's role first, then confirm the source video still controls the boundary. New references may add characters, props, or audio — they must not override the source's control of the extension's opening (forward) or closing (backward) image.

For backward extensions, explicitly quarantine anything that should only appear later:

```
@Image 1 defines <Character A>'s facial features.
@Image 2 defines <Character A>'s clothing.
@Image 3 defines <key prop>'s structure and material.
@Video 1 is the source video to extend backward.

Extend @Video 1 backward. Before the source video begins, <Character A completes a preceding
action or event>.

The last frame of the extended segment naturally connects to the first frame of @Video 1:
<Character A's pose and orientation>, <key prop's position and state>, and <other characters'
positions>. Match the <background and spatial relationships>, <camera position and composition>,
<lighting>, and <motion direction> of @Video 1's first frame.

<Materials that should appear only after the source video begins> must not appear early in the
backward extension.
```

Boundary frames connect naturally at a **visual** level — they will not be pixel-identical. Review both sides of the seam and the full extended segment, not just the joint. Extension segment volume may also differ slightly from the source.
