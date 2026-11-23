# Multi-Reference System

For prompts carrying several characters, props, scenes, motion references, and audio across multiple scenes. Seedance 2.5 accepts up to 50 materials, but the goal is never to cram every reference into one sentence — it is to define the relationships between them and then select the right subset per scene.

**Contents**
1. The four-step order
2. Step 1 — name and map each subject individually
3. Step 2 — group materials by type
4. Step 3 — subject profiles for recurring characters
5. Step 4 — select references per scene
6. Worked example
7. Failure modes

---

## 1. The four-step order

```
Define each material's role → Map subjects → Group by type → Create subject profiles → Select references by scene
```

Skipping straight to prose is the most common cause of identity swaps, duplicated props, and characters wearing each other's clothes.

## 2. Step 1 — name and map each subject individually

Bind every person, product, and prop to its material on its own line. Angle-bracket names (`<Conservator>`) give you a stable token to reuse everywhere else in the prompt.

```
<Character A> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.
<Character B> corresponds to @Image 2. Use only the appearance, hairstyle, and clothing.
<Prop A> corresponds to @Image 3. Use only the structure, material, and color.
<Scene A> references @Image 4. Use only the spatial layout, architecture, and lighting.
             Do not use the people in the image.
```

Never collapse this into `@Images 1 through 4 define four characters respectively`. That sentence contains no mapping.

## 3. Step 2 — group materials by type

Grouping makes the cross-contamination bans readable and gives you one obvious place to state them.

```
[Characters]
<Conservator> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.
<Registrar> corresponds to @Image 2. Use only the appearance, hairstyle, and clothing.
<Exhibition Installer> corresponds to @Image 3. Use only the appearance, hairstyle, and clothing.
<Guide> corresponds to @Image 4. Use only the appearance, hairstyle, and clothing.
Do not interchange the four characters' appearances, clothing, actions, positions, or dialogue.

[Props]
<Sample Case> corresponds to @Image 5 and belongs only to <Conservator>.
<Record Board> corresponds to @Image 6 and belongs only to <Registrar>.

[Scenes]
<Conservation Lab> references @Image 7. Use only the space, materials, and lighting.
<Gallery> references @Image 8. Use only the space, materials, and lighting.

[Motion and Audio]
@Video 1 defines the motion of <Conservator> opening <Sample Case>.
          Do not use the person or scene from the video.
@Audio 1 defines <Guide>'s voice and specified dialogue.
```

`belongs only to` is the prop-ownership lock. Without it, props migrate between characters across scenes.

## 4. Step 3 — subject profiles for recurring characters

When one character draws on several references and appears in more than one scene, give them a consolidated profile. This is the anti-drift device for your lead.

```
[Subject Profile: Conservator]
Appearance and clothing: @Image 1.
Fixed prop: <Sample Case> from @Image 5.
Locations: <Conservation Lab> and <Gallery>.
Motion references: the case-opening motion from @Video 1 and the sample-placement motion from @Video 2.
Do not use: other characters' clothing. Do not give this character <Record Board> or guide equipment.
```

Write profiles only for subjects that recur. A one-scene walk-on doesn't need one.

## 5. Step 4 — select references per scene

Each scene declares which materials it uses, what happens, and what is visibly true at the end. Materials not listed for a scene should not appear in it.

```
Scene 1 | Inspection in the Conservation Lab
Use: <Conservator>, <Sample Case>, <Conservation Lab>, and the case-opening motion from @Video 1.
Event: <Conservator> opens <Sample Case> at the workbench and inspects the sample inside.
End state: <Conservator> remains on the inner side of the workbench. <Sample Case> stays beside
           the conservator's right hand, which is on the left side of the frame.

Scene 2 | Registration in the Gallery
Use: <Registrar>, <Record Board>, and <Gallery>.
Event: <Registrar> checks the number on <Record Board> beside the display case.
End state: <Registrar> still holds <Record Board> with both hands. No other character enters
           the display-case area.
```

End states carry spatial detail — which side of the frame, which hand, inner or outer side of a surface. Vague end states ("the inspection is finished") do not constrain anything.

## 6. Worked example — assembling the whole thing

Order the finished prompt like this:

1. `[Characters]` / `[Props]` / `[Scenes]` / `[Motion and Audio]` blocks with mappings and exclusions
2. `[Subject Profile: X]` for each recurring lead
3. `Scene 1 | …`, `Scene 2 | …` blocks with Use / Event / End state
4. A closing consistency block naming identity, count, clothing, prop ownership, and spatial direction

The closing block is cheap and catches drift the per-scene blocks miss:

```
[Maintain Consistency]
Keep <Conservator> and <Registrar>'s identities, clothing, prop ownership, workbench
orientation, and camera direction consistent across all scenes.
```

## 7. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Characters swap faces or outfits | Mapping written as a group sentence | One `corresponds to` line per character, plus the do-not-interchange ban |
| A prop appears in the wrong hands | No ownership lock | `<Prop> belongs only to <Character>` |
| Background people from a reference show up | Missing exclusion | `Do not use the people in the image.` |
| The same object appears twice | Multiple views not declared as one object | `All images define one <object>. The output must contain only one <object> throughout.` |
| Everything crowds into every scene | No per-scene selection | Add `Use:` lines per scene |
| Identity holds early, drifts late | No subject profile, no closing consistency block | Add both |
