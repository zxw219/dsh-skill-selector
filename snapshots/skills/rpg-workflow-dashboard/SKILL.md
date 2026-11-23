---
name: rpg-workflow-dashboard
description: RPG像素风工作流看板工具：为Codex多任务或多Agent工作建立右侧浏览器进度面板，展示项目状态、任务队列、线程进展和可视化反馈。用于需要可视化工作台和任务追踪时。
version: 1.0.0
---

# RPG Workflow Dashboard

## Purpose

Use this skill to give long Codex workflows a visible companion dashboard: progress bar, RPG map, worker/skill party, narration, event stream, artifacts, watchdog state, and a full-screen “mission clear” result page.

Default behavior:
- Active task: show map, progress, skill party, ETA, narration.
- New task starts: hide the previous completion page immediately.
- Current task completes: show a full-screen RPG completion/result page.
- Chinese text must be written through the bundled Python scripts, not raw PowerShell arguments, to avoid mojibake/`????`.

## Fast Workflow

1. Create a dashboard from the bundled template:

```powershell
python <skill>/scripts/create_dashboard.py --output <workspace>/outputs/workflow-dashboard --preset film --start
```

2. Open the printed local URL in the in-app browser or side browser.

3. Before every new task, start a fresh run. This hides any old completion page:

```powershell
python <skill>/scripts/update_dashboard.py --dashboard <dashboard_dir> start-run --title "任务标题" --subtitle "副标题"
```

4. During work, update steps/threads:

```powershell
python <skill>/scripts/update_dashboard.py --dashboard <dashboard_dir> step --id brief --status running --progress 35 --note "正在拆解需求"
python <skill>/scripts/update_dashboard.py --dashboard <dashboard_dir> thread --id t-style --status running --progress 60 --current "正在锁定视觉母版"
```

5. On completion, write the current-run conclusion. The overlay only appears if the conclusion `runId` matches the active `meta.runId`:

```powershell
python <skill>/scripts/update_dashboard.py --dashboard <dashboard_dir> complete --title "副本通关" --verdict "最终结论"
```

## Presets

- `film`: Liu's tested personal preset: pixel/RPG film workflow, skill party roles, watchdog, mission-clear screen.
- `generic`: neutral project/task workflow for sharing with others.

For schema and customization options, read `references/customization.md`.
For operating rules and failure prevention, read `references/workflow-protocol.md`.

## Customization Contract

When the user wants a different feel, edit the state/config rather than hardcoding CSS:

- `meta.theme`: CSS variable overrides, such as `cyan`, `green`, `amber`, `panel`, `line`, `cream`.
- `meta.labels`: visible headings, such as `mapTitle`, `partyTitle`, `narrationTitle`, `artifactTitle`, `clearRibbon`.
- `steps`: map nodes and workflow stages.
- `threads`: worker cards, skill labels, avatars, watchdog values.
- `finalConclusion`: completion overlay content.

Use `scripts/update_dashboard.py theme` or a JSON config file for non-trivial changes.

## Non-Negotiable Runtime Rule

Always call `start-run` before beginning a new visible workflow. If this is skipped, the browser may keep showing the previous completion overlay while new work is happening.

## Packaging For Others

To create a shareable skill zip from this folder:

```powershell
python <skill>/scripts/package_skill.py --output <workspace>/outputs
```

Share the produced `.zip`. The recipient can unzip it into their own `.codex/skills` folder.
