---
name: blender-mcp-previs
description: Blender MCP预演工具：通过Blender MCP连接Blender 5.1及以上版本，创建、编辑、检查、渲染或导出白模与动作预演场景。用于AI视频镜头规划、空间验证和动作预可视化。
version: 1.0.0
---

# Blender MCP Previs

## Core Workflow

Use this skill to operate a live Blender scene through the official Blender MCP socket bridge.

1. Check for native Blender MCP tools first. Search for tools like `execute_blender_code`, `get_objects_summary`, `render_viewport_to_path`, or a `blender` MCP namespace. Use them when available.
2. If native tools are not exposed in the current Codex turn, use the bundled scripts:
   - `scripts/ensure_blender_mcp.py` to confirm Blender is reachable or launch it.
   - `scripts/blender_mcp_send.py` to execute Python code in Blender.
   - `scripts/blender_start_bridge.py` only as the Blender-side startup script used by `ensure_blender_mcp.py`.
3. Confirm the bridge before modeling by executing a small ping that returns `bpy.app.version_string`, `bpy.data.filepath`, and object count.
4. Build or modify the scene with Python sent to Blender. Always return a JSON-serializable `result` dict.
5. Verify with a scene summary and at least one rendered preview image for visual tasks.

## Local Setup Defaults

The current machine has Blender 5.1.2 installed at:

```text
D:\steam\steamapps\common\Blender\blender.exe
```

The official Blender Lab MCP add-on is installed and enabled in Blender's `user_default` extension repository as `bl_ext.user_default.mcp`.

The bridge listens on:

```text
localhost:9876
```

Codex config has an MCP server named `blender` using the official `blender-mcp` package from:

```text
C:\Users\liu1\Documents\Codex\2026-06-29\ban\work\blender_mcp_official\mcp
```

If a future workspace moves this repo, prefer native MCP tools when available, or use the bundled socket scripts which only require Blender's installed add-on.

## Script Usage

Check or launch Blender:

```powershell
python C:\Users\liu1\.codex\skills\blender-mcp-previs\scripts\ensure_blender_mcp.py --blend C:\path\to\scene.blend
```

Execute code in Blender from stdin:

```powershell
@'
import bpy
result = {"version": bpy.app.version_string, "objects": len(bpy.data.objects)}
'@ | python C:\Users\liu1\.codex\skills\blender-mcp-previs\scripts\blender_mcp_send.py
```

Execute code from a file:

```powershell
python C:\Users\liu1\.codex\skills\blender-mcp-previs\scripts\blender_mcp_send.py C:\path\to\script.py
```

## Whitebox Previs Guidance

For AI video previs, prefer readable blockout scenes over decorative detail:

- Use simple cubes, planes, curves, empties, cameras, lights, and text labels.
- Name objects semantically: `WB_subject_A_start`, `Beat_02_crossing_line`, `MCP_Previs_Camera_Dolly`.
- Add floor grids, scale markers, shot labels, camera path curves, and frame-range metadata.
- Animate key camera or subject positions when timing matters.
- Save `.blend` files and preview renders into the user-facing `outputs` directory when working in a Codex projectless workspace.
- Use neutral clay/gray materials unless color conveys functional meaning such as action beats, camera path, or occluders.

## Verification Checklist

Before finishing a Blender task:

- Confirm Blender responded through MCP after the final edit.
- Return object count, active camera, frame range, and saved file paths.
- Render or capture a preview for visual inspection.
- Open/view the generated preview image when possible and mention if it is blank, misframed, or visually incorrect.

## Troubleshooting

- If `ConnectionRefusedError` occurs, run `ensure_blender_mcp.py`.
- If Blender opens but port `9876` stays closed, launch with `--online-mode` or run the bundled startup script through `ensure_blender_mcp.py`.
- If code fails on Blender API differences, fix for Blender 5.1+ and retry. Common compatibility checks: find shader nodes by `node.type`, and prefer `BLENDER_EEVEE` for the render engine.
- If native MCP tools do not appear after editing Codex config, restart Codex; use `blender_mcp_send.py` in the current turn.
