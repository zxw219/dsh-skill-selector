---
name: blender-whitebox-action-previs
description: Blender白模动作预演工具：利用动捕、绑定动画或现成动画模型快速搭建干净的白模动作预演，检查站位、距离、碰撞、节奏和镜头。用于动作场面的三维预可视化。
version: 1.0.0
---

# Blender Whitebox Action Previs

## Scope

Use this skill only from action reference to Blender whitebox output. Do not design final characters, write AI video prompts, or make styled final videos unless the user asks for that separately.

The deliverable is usually:

- a `.blend` scene;
- an `.mp4` whitebox/clay action preview;
- a contact sheet or sampled frames for review;
- a short report with source, specs, and visible limitations.

## Core Rule

Use motion evidence before inventing motion. Prefer sourced mocap, rigged animation libraries, BVH/FBX/GLB clips, or premade animation projects over hand-keyed guessing. Hand-key only helper timing, camera, props, cuts, or simple corrective holds.

## Workflow

1. Define the target: action type, duration, FPS, resolution, camera style, and whether the user wants a complete combo or a single move.
2. Choose a motion source. Prefer complete combos with labels like `combo`, `heavy`, `regular`, `dash attack`, `finisher`, `melee`, `sword`, `boxing`, or `martial arts`. Verify license/readme before using downloaded sources.
3. Inspect the source before committing: action names, frame ranges, skeleton consistency, visible motion quality, root motion, prop attachments, and whether it is a full combo or a loop.
4. Import or load into Blender. If the importer produces a static pose, broken axis, wrong scale, or unusable skeleton, inspect the file and try another path rather than polishing a broken import.
5. Keep one stable acting body. Use one source rig/model for the whole preview or retarget clips onto one fixed rig. Do not let body proportions change between moves.
6. Build a clean whitebox look: clay material, simple lighting, floor grid, readable prop, and no decorative final materials. Hide or delete debug rods, tails, axes, helper empties, stray bones, and nonessential source meshes.
7. Preserve source speed unless the user requests slow motion. High FPS means smoother sampling, not stretching a short action into slow motion.
8. Direct a full-body safety camera first. Head, feet, hands, and full weapon extent must remain inside frame for the entire contact sheet. Add push-ins or impact framing only after the full action is readable.
9. Render a fast preview or contact sheet before the final export. Reject outputs with cropped bodies, unreadable strikes, broken legs, sliding feet, random prop drift, or slow/empty action beats.
10. Export the final whitebox preview. Default to 1280x720 MP4 when the user says 720. Save the `.blend`, video, contact sheet, and sampled frames in a clear output folder.
11. Probe the exported video for resolution, FPS, duration, frame count, and decode issues before calling the task done.

## Quality Gates

- The preview must show a complete action phrase when the user asks for a showcase: anticipation, attack beats, transition, finisher, and recovery.
- The action must read at contact-sheet size.
- The acting body must visibly shift weight through feet, hips, torso, and shoulders; arm-only motion is not enough.
- The feet must have plausible support or intentional airborne phases. Avoid unexplained skating, spinning legs, or root snapping.
- The weapon must look intentional and attached. A helper stick, debug marker, or bone cannot remain visible as an accidental tail or rod.
- The camera must keep the full performer and weapon visible unless the user explicitly requests close-ups.
- Do not fill duration by looping one short attack unless the user approves that design.
- If the source motion is weak, replace the source before tuning materials or camera.

## Coordination

- Use `mocap-action-previs` when sourcing, evaluating, retargeting, or composing mocap/game animation.
- Use `blender-mcp-previs` when direct Blender MCP control is required.
- Use `ai-video-output-review` or an equivalent local video probe when reviewing exported previews.

## Final Response

Report only the useful facts:

- source name and license status if known;
- output video path, `.blend` path, and contact sheet path;
- resolution, FPS, duration, and frame count;
- review verdict and any remaining visible issues.
