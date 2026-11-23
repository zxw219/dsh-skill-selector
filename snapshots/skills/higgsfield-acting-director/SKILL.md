---
version: 1.0.0
name: higgsfield-acting-director
description: Write ACTING TASK blocks for AI video prompts (Seedance on Higgsfield) so characters read alive instead of glassy or over-acted. Use WHENEVER a prompt or scene needs acting direction: a reaction, a discovery, dialogue delivery, an emotional beat, a listener, "make the eyes alive", or when a generated character looks dead, frozen, flat or overplayed. Works with higgsfield-seedance-prompt-writer: this skill writes the performance, that one writes the shots.
---

# Higgsfield Acting Director

A method for acting direction that makes AI-generated actors read ALIVE, because the mind behind the face is given real work, not choreography.

---

## Core principle

An acting task is when the character is **INVESTED in their tactic of reaching a goal.**

- It is NOT a description of external behavior ("eyes flick", "brows lift", "he looks sad"). That is playing the result, and it produces dead faces.
- It is NOT necessarily a physical action. The tactic can live entirely **in the eyes**: a different look when someone humiliates vs. begs; a person arguing from conviction keeps checking BOTH of the partner's eyes for a spark of trust, registers whether the partner is interested or drifting, and adjusts.
- The eye movement IS the doing. Aliveness = the mind visibly working on the task, moment to moment.
- Never fix dead eyes with lighting tricks (catchlights etc.). Fix them by giving the eyes a task.

## The ladder (work strictly in this order)

### 0. Read the WHOLE scene first
Never build a task from one line or one beat. The task lives across the whole scene: where it holds, where it breaks. Check every line and every beat of every character before directing any of them.

### 1. Scene direction: one shared direction
The scene has ONE direction that ALL characters play toward, usually unspoken: a silent agreement about how this moment will be lived.
Example (a mother packs her son's suitcase, he leaves for the army in an hour): **make it painless: hide the feeling, don't leave each other with sorrow, stay positive.** It belongs to both at once.
For a solo character the direction is the practical business of the moment, e.g. **finish the morning routine; follow a useful question far enough to settle it.**
The scene direction is NOT the film's purpose (the reveal, the joke, the product benefit). Characters never know or play the film's purposes; those happen THROUGH them.

### 1a. The ending names the event
Look at how the scene ENDS before naming what it is about. The last beat is the key you read the whole scene backward through.

### 1b. Everyone is in the event
The event must include EVERY character in the scene, silent ones too, as participants or mirrors of the same process. If someone stands outside it, the event is named wrong.

### 1c. The physical action is the channel
The surface activity (brushing teeth, packing a suitcase, routine rounds) stays as the PHYSICAL ACTION, and each character pursues the task THROUGH it, each with their own visible behavior. The invisible task needs a physical channel the camera can read.

### 2. MOTIVE: different fuel, same direction
Everyone pushes the same direction, each **for their own reason**. The son keeps it painless *for mom*; the mother *out of superstition* (no tears before a journey). Same vector, different fuel: that is what makes each performance distinct while the scene reads as one.

### 3. GOAL: the personal fight
Born from the motive: what this person is fighting for inside the scene. Ordinary, personal, playable. Never the same words as the scene direction.

### 4. OBSTACLE: what presses against the direction
What threatens to break the line (the real feeling pressing to surface; the first glimpse that doesn't prove anything yet). This pressure is what the audience feels, precisely because nobody plays it.

### 5. TACTIC: the acting task proper
The invested, moment-to-moment pursuit, written as what the character is DOING, with the eye-work named as purposeful action:
- checking both of the partner's eyes for a spark of trust
- registering after each point: did it land?
- stealing looks and snapping back before being caught
- using the mirror to check, examining the actual object to choose the test, then carrying it through
Key the beats to the actual dialogue words or timestamps. Where the script demands it, mark the point where the line breaks.

## Writing the ACTING TASK block in a prompt

Solo character (product ads, reactions, discoveries):

```
ACTING TASK — [NAME]
SCENE DIRECTION, UNSPOKEN: [one line]
MOTIVE: [why they push that direction]
GOAL: [their personal fight in this scene]
OBSTACLE: [what stands in the way]
TACTIC: [what they do, step by step, with the eye-work as action]. Moment-to-moment tasks are given in the timed stages below.
PERFORMANCE CONTINUITY: gaze stays engaged with the current target and question; natural blinking and breathing continue.
```

Two or more characters:

```
ACTING TASK — [NAME] (fully invested in the tactic; the work happens in the eyes):
SCENE DIRECTION (shared, unspoken): [one line]
MOTIVE: [their fuel]
GOAL: [their personal fight]
OBSTACLE: [what presses against the line, what one crack costs]
TACTIC: [what they do to the partner, with the eye-work as action]
Moment to moment:
— "[dialogue words]" / [timestamp] — [verb at the partner + what the eyes check]
— "[dialogue words]" / [timestamp] — [verb + eye-work]
— [where the line breaks, if it breaks]
(Safety: gaze always engaged in the task, never a frozen, glassy, unfocused stare; natural blinks now and then.)
```

Place the block before the timeline, and in a timed prompt refer to moments by timestamps ("at 11.0–13.5s he checks the mirror again"), not by shot numbers.

Rules:
- Verbs aimed at the partner or the target; no emotion adjectives as instructions ("sadly", "nervously").
- No facial choreography ("brows lift", "mouth trembles"); externals only in the safety line.
- Nobody plays the emotion; everyone plays the direction. The audience gets the feeling through the pressure.
- One safety line against the frozen stare is allowed and recommended for AI video.
- Every character in frame gets living eyes, including silent listeners: a listener's task is real too ("decide if he's serious", "wait for the punchline").
- Comedy works the same way: the character takes the absurd idea completely seriously. The laugh comes from his commitment, not from mugging.

## Contrast pairs

A two-character scene is richer when the pair is built on CONTRAST: each carries a plus and a minus, mirrored against the other, on one essential axis the audience reads.
- Example: a loyal-to-the-company (+) but careless-with-people (−) senior next to a compromised (−) but caring (+) junior. On the essential axis (care for the person in front of them) one is minus, the other plus.
- Both still push the same scene direction; the contrast leaks out through their tactics and their eyes.
- A trait that seems obvious is often scar tissue over its opposite: "careless" can be hope lost, not care absent. Direct the history, not the surface.

## Worked example

Mother and son, suitcase scene:
- Scene direction: part without pain, stay positive.
- Her motive: superstition (tears before a journey are a bad omen). His: for mom.
- Her goal: send him off strong, don't make him carry her fear. His: leave her calm, show he's ready.
- Obstacle: the real feeling, pressing every second; one wet look and the line collapses.
- Tactic: she packs "ordinarily", eyes stealing to him, measuring, memorizing, snapping back to the socks the moment he looks up; he eats "casually", watching her hands, not her face, because her face is where the danger is.
- The audience cries precisely because nobody on screen does.

## Common failures to catch

- Task built from one line instead of the whole scene → re-read the scene first.
- The film's purpose given to a character as their task → characters never play the film's purposes.
- Scene direction confused with a character goal → the direction is shared; goals are personal and differ.
- A motive that ignores the given circumstances → re-derive the motive.
- Eye or face choreography instead of eye-work as purposeful action → rewrite as verbs.
- Emotion adjectives as direction → replace with the task that produces the emotion.
