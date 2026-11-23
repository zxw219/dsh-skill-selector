# H3 interoperability guide

This community-authored guide defines the serializer used by this Skill. It records only the interface names and mode relationships needed to produce H3-compatible prompts. It does not reproduce MiniMax documentation or claim to replace the active product instructions.

Before a release, compare the identifiers below with the current H3 product surface. If the surface differs, update this guide as a compatibility patch and keep creative recipes in their own file.

## 1. Pick one input relationship

- `T2VA`: the prompt is the only source for the requested sequence.
- `I2VA`: one picture supplies the opening image at 0.00 seconds.
- `FL2VA`: two pictures supply the opening and closing images.
- `L2VA`: one picture supplies the closing image.
- `Ref2VA`: labeled pictures, videos, audio, or reusable visible subjects contribute references across the sequence.

Use one relationship only. The presence of a picture does not force `Ref2VA`: choose a frame mode when the picture's job is specifically the first or last frame.

## 2. Three-section serializer

For `T2VA`, `I2VA`, `FL2VA`, and `L2VA`, emit these interface keys in this order:

```text
integrated_multimodal_description: ...

overall_soundscape: ...

non_diegetic_music: ...
```

Use English for instructions. Keep spoken words, lyrics, and requested on-screen copy in their intended language.

Frame modes add one concise English alignment sentence before the three sections, then a blank line:

- `I2VA`: state that `Picture 1` fully defines `Shot 1` at `0.00s`.
- `FL2VA`: state that `Picture 1` defines `Shot 1` at `0.00s`, and `Picture 2` defines the final `Shot N` at `S.SSs`.
- `L2VA`: state that `Picture 1` defines the final `Shot N` at `S.SSs`.

Replace `N` and `S.SS` with real values. For first/last-frame work, describe a causal visual path between the aligned states rather than treating the images as general style references.

## 3. Full-reference serializer

For `Ref2VA`, emit these interface keys in this order:

```text
subject_definitions: ...

summary: ...

retention_analysis: ...

detailed_description: ...

overall_soundscape: ...

non_diegetic_music: ...
```

Number each label family independently and keep labels unchanged after definition:

- `<Subject N>` identifies reusable visible content or an attribute assembled from supplied assets.
- `<Picture N>` identifies a concrete frame, composition, edited still, or storyboard anchor.
- `<Video N>` identifies a temporal source for editing, continuation, motion, camera, or cut structure.
- `<Audio N>` identifies a source for sound content, voice character, delivery, beat, or texture.

If a still merely contributes an attribute to a subject, cite the picture inside that subject definition instead of inventing a second standalone frame role. A video's audio becomes `<Audio N>` only when the audio track has an explicit target job.

### Summary vocabulary

Begin `summary` with one bracketed combination of the needed task identifiers: `keyframe completion`, `reference generation`, `video editing`, `video continuation`, `audio reuse`, or `audio reference`. Join multiple identifiers with ` + `. The following sentence briefly states the intended sequence and already-defined reference relationships.

### Retention vocabulary

Give every defined label one line in `retention_analysis`. For visible labels, select the applicable machine token: `fully_preserved`, `partially_preserved`, `attribute_transfer`, or `weak_reference`. For audio labels, select `fully_copy`, `partially_copy`, `reference`, or `weak_reference`.

Judge retention only against the declared job. A subject can remain fully preserved while performing a new target action that was never assigned to the source.

## 4. Timeline grammar

- Start with `[Shot 1]`; later cuts use increasing `[Shot N]` numbers and explicit times inside the requested duration.
- A cut should reveal a new state, scale, viewpoint, spatial fact, or time step. Use camera movement rather than a cut for a small reframing.
- Keep stable speaker IDs such as `(S1)` for recurring vocal sources.
- Put exact speech or lyrics inside `<d>[Language] ...</d>`; keep voice direction outside the tag.
- Put requested visible copy in double quotation marks.
- Describe synchronized physical sound beside its owning visual event.

## 5. Layer ownership

- `integrated_multimodal_description` or `detailed_description`: playback-order image, action, edit, camera, visible text, speech, singing, and event-synchronous sound.
- `overall_soundscape`: ambience, physical effects, and non-verbal human sound, summarized without repeating spoken or sung wording.
- `non_diegetic_music`: score heard by the audience rather than produced inside the scene.

Use `N/A` only for a deliberately empty audio layer. Prefer relative mix language and event relationships to hard numeric loudness claims.

## 6. Release checks

A compiled prompt passes when:

1. one input relationship is selected;
2. its section set is complete and ordered;
3. frame alignment is included only for a frame mode;
4. every reference label is defined before reuse and has one compatible retention token;
5. cut times increase and remain inside the duration;
6. speakers, dialogue tags, visible copy, physical sound, ambience, and score are in their owning layers;
7. backstage planning notes, citations, and unresolved placeholders are absent from the copyable prompt.
