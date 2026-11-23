---
name: seedance-continuation
description: Seedance续写工具：根据已有视频的最后状态延续角色、动作、镜头、空间、光线和节奏，减少跳变与重复。用于视频续写、扩展镜头和连续片段生成。
version: 6.1.0
---

# seedance-continuation

Use this for seamless continuation, intentional next shots, bridge clips, tail repair, and re-anchoring after drift. A continuation prompt must be grounded in accepted footage, not only in the old plan.

Load `[ref:continuation-handoff]`, `[ref:sequence-project-state]`, `[ref:prompt-compiler]`, `[ref:reference-transfer-contract]`, and `[ref:continuity-qc]`. Load `[ref:failure-atlas]` when the continuation failed or drift is visible. Load `[ref:directing-engine]` so the next clip inherits the project's directorial voice and its position on the long-form spine; the look never re-rolls between clips.

## Required Input Gate

Before writing any continuation prompt, require:

- `project_id`;
- current `clip_id`;
- valid `parent_clip_id`;
- full-story objective;
- final story outcome;
- next planned narrative job;
- accepted previous clip or accepted final frame;
- `observed_end_state`;
- continuity locks;
- inherited directorial voice and arc position;
- exact reference registry;
- active surface or conservative surface profile.

If the source is unavailable, say: "I have the story plan, but I do not have the actual ending of the previous generation. Upload the clip or its final frame, or describe exactly what is visible at the end. I should not invent the continuation state."

Do not hide this uncertainty by writing a speculative prompt.

## Continuation Types

`seamless_continuation`: same shot, same geography, same open motion, same or motivated camera continuation, and accepted previous footage as the source.

`intentional_next_shot`: an editorial cut is appropriate. Story continuity matters, but exact frame continuity is not promised. Do not call it seamless.

`bridge_between_known_states`: a defined start state and end state must be connected, often with first/last-frame generation when the active surface supports it.

`repair_tail`: the previous final seconds failed. Repair, edit, or regenerate the tail before continuing because continuing from a failed tail amplifies the error.

`reanchor_after_drift`: identity, detail, geography, motion, audio, or world continuity degraded. Return to canonical identity, the strongest accepted final frame, a stable source clip, or a new intentional shot using canonical references.

## Canon Rule

Accepted observed footage overrides planned state. If the plan says the subject reached the car door but the accepted clip ends two steps away, the next prompt begins two steps away. It does not replay the terminal exit, and it does not assume the subject is inside the car.

Rejected footage never updates canon and never becomes a parent source.

Track `extension_depth`. At depth 2 or greater, warn that repeated extension can increase continuity risk. When visible drift has begun, recommend re-anchoring instead of blindly extending again.

## Output Contract

Return:

1. Continuation type.
2. Source evidence used.
3. Observed end state.
4. Next clip contract.
5. Continuity locks and allowed changes.
6. Completed beats to exclude.
7. Reserved future beats to exclude.
8. Final natural-language Seedance prompt for the current clip only.
9. Updated Project State Capsule or a request for missing source evidence.
