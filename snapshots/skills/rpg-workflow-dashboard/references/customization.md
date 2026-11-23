# Customization Reference

## Config Shape

Use a JSON config with any of these fields. Missing fields fall back to the selected preset.

```json
{
  "projectName": "My Workflow",
  "taskTitle": "Current task",
  "subtitle": "What this run is doing",
  "port": 17321,
  "theme": {
    "bg0": "#070a17",
    "bg1": "#0d1230",
    "panel": "#141b38",
    "line": "#31406f",
    "cream": "#f8e7bf",
    "muted": "#9fb0d0",
    "cyan": "#55d6ff",
    "green": "#73f59a",
    "amber": "#ffd166",
    "red": "#ff6b93",
    "violet": "#b996ff"
  },
  "labels": {
    "progress": "总进度",
    "phase": "当前阶段",
    "eta": "预计剩余",
    "mapEyebrow": "QUEST MAP",
    "mapTitle": "流程地图",
    "narrationEyebrow": "NARRATION",
    "narrationTitle": "旁白",
    "partyEyebrow": "SKILL PARTY",
    "partyTitle": "技能小队",
    "logTitle": "事件流",
    "artifactTitle": "产物槽",
    "clearRibbon": "MISSION CLEAR",
    "clearKicker": "工作流 · 通关结算"
  },
  "steps": [
    {"id":"brief","label":"需求理解","thread":"主控","estimateMinutes":4},
    {"id":"research","label":"调研分析","thread":"调研线程","estimateMinutes":8}
  ],
  "threads": [
    {"id":"t-research","title":"调研线程","role":"参考猎人","skill":"Skill：调研","avatar":"scout","location":"research"}
  ],
  "watchdog": {"timeoutSeconds":300,"retryLimit":1,"fallbackOnFinalTimeout":true}
}
```

## Theme Keys

`meta.theme` maps directly to CSS variables. Supported common keys:

- `bg0`, `bg1`: page background.
- `panel`, `line`, `shadow`: panel and pixel border colors.
- `cream`, `muted`: main text and secondary text.
- `cyan`, `green`, `amber`, `red`, `violet`: accent palette.
- `pixel`: border pixel size, e.g. `4px`.

Do not put untrusted CSS expressions in theme values. Keep them simple colors or pixel sizes.

## Label Keys

`meta.labels` lets users change the feel without editing HTML:

- `progress`, `phase`, `eta`
- `mapEyebrow`, `mapTitle`
- `narrationEyebrow`, `narrationTitle`
- `partyEyebrow`, `partyTitle`
- `logEyebrow`, `logTitle`
- `artifactEyebrow`, `artifactTitle`
- `clearRibbon`, `clearKicker`, `clearNext`

## Avatars

Bundled avatars:

- `scout`
- `alchemist`
- `smith`
- `knight`
- `mage`

Add custom PNGs to `assets/characters/` and set `thread.avatar` to the file stem.

## Completion Overlay

The completion overlay reads `finalConclusion`:

```json
{
  "runId": "must match meta.runId",
  "title": "副本通关",
  "subtitle": "任务完成",
  "verdict": "最终判定",
  "stats": [
    {"label":"总进度","value":"100%"}
  ],
  "sections": [
    {"title":"核心结论","text":"..."},
    {"title":"产物","items":["A","B"]}
  ]
}
```

If `runId` does not match, the overlay stays hidden. This prevents stale completion screens.

## Recommended Custom Styles

- `film`: dark blue/pixel/RPG, suited for creative and video workflows.
- `ops`: green/terminal style, suited for engineering tasks.
- `guild`: parchment/gold style, suited for writing/research.
- `arcade`: bright cyan/magenta style, suited for demos.

Create these by changing `theme` and `labels`; do not fork the app unless layout itself must change.
