---
name: reference-role-planner
description: Assigns explicit responsibilities to image, video, audio, text, and style references; detects conflicting authority, overloaded references, and missing coverage; and produces a precedence-aware reference matrix before generation or production. 为多模态参考图、视频、音频和文本分配明确职责，发现冲突与缺口，生成带优先级的参考责任表。
version: "1.0.0"
---

# Reference Role Planner｜参考职责规划器

Convert a loose pile of references into an unambiguous control plan. This skill plans reference authority; it does not imitate every visible property of every reference.

## When to use

Use before image generation, video generation, design, editing, worldbuilding, product visualization, or any task where two or more references may influence the same output.

Typical trigger phrases include “use these references,” “keep the character but copy the lighting,” “combine these images,” or “why does the output drift?”

## Role vocabulary

Assign one or more narrowly defined roles to each reference:

- **Identity** — face, character, product, logo, or object identity
- **Geometry** — proportions, silhouette, shape, construction, or topology
- **Composition** — framing, placement, scale relationships, or negative space
- **Camera** — viewpoint, lens behavior, distance, angle, or movement
- **Motion** — timing, path, rhythm, gesture, or physical behavior
- **Lighting & Color** — direction, contrast, palette, exposure, or atmosphere
- **Material** — texture, surface response, wear, translucency, or finish
- **Style** — rendering language, medium, era, graphic treatment, or visual abstraction
- **Content & Text** — wording, labels, factual content, typography, or layout hierarchy
- **Audio** — voice identity, music character, ambience, timing, or sound effects
- **Negative Constraint** — a feature that must not appear; record it in the template's **Exclusions** section rather than treating it as positive authority

Use the narrowest role that expresses intent. “Overall vibe” is not a sufficient role.

## Workflow

### 1. Inventory the references

Give every reference a stable ID such as `R1`, `R2`, or `AUDIO-01`. Record its type, source, and a one-line description. If a referenced asset is unavailable, mark it missing rather than guessing its contents.

### 2. Extract the user's intent

For each reference, state what should be borrowed and what should be ignored. Preserve explicit user instructions over visual inference.

Example:

> R1 owns character identity and costume silhouette. Ignore its background, pose, and lighting.

### 3. Assign authority

For every active role, set:

- **Primary** — authoritative reference
- **Secondary** — fills detail only when it does not contradict the primary
- **Advisory** — inspiration, not a matching requirement
- **Negative** — source of exclusions

Do not assign two primary references to the same role unless a merge rule is explicit.

### 4. Detect failure modes

Flag these conditions:

- **Conflicting authority** — two references control the same role differently
- **Reference overload** — one reference is unintentionally controlling unrelated roles
- **Missing coverage** — an important role has no owner
- **Hidden coupling** — satisfying one role may break another, such as camera angle hiding identity details
- **Unusable evidence** — low resolution, occlusion, inconsistent edits, missing audio, or unreadable text
- **Unclear precedence** — no rule decides which reference wins

Ask the user only when a conflict cannot be resolved safely. Otherwise choose the explicit instruction, then the primary, then the more direct and usable reference.

### 5. Write the control plan

Use [references/reference-matrix.md](references/reference-matrix.md). Include:

1. a reference inventory
2. a role-to-reference responsibility matrix
3. a precedence order
4. exclusions and ignored traits
5. unresolved conflicts or missing inputs
6. a compact generation or production handoff

### 6. Run the preflight

Confirm that:

- every critical role has no more than one primary owner
- every reference has a declared purpose
- ignored traits are explicit for visually dominant references
- conflicts have a precedence rule
- missing inputs are separated from creative freedom
- the handoff is short enough to use during production

Do not claim that a tool can enforce a reference role unless that tool exposes the corresponding control. Translate unsupported roles into clear text instructions.

In user-visible output, omit secrets, personal information, and unnecessary local paths unless the user explicitly needs them.
