# Blender MCP Local Setup

Use this reference only when troubleshooting setup.

Current known-good state:

- Blender version: 5.1.2
- Blender executable: `D:\steam\steamapps\common\Blender\blender.exe`
- Official Blender Lab add-on package: `bl_ext.user_default.mcp`
- Socket bridge: `localhost:9876`
- Blender preference `system.use_online_access`: `True`

Codex config contains:

```toml
[mcp_servers.blender]
command = 'uv'
args = ['run', '--directory', 'C:\Users\liu1\Documents\Codex\2026-06-29\ban\work\blender_mcp_official\mcp', 'blender-mcp']
startup_timeout_sec = 120
tool_timeout_sec = 300
enabled = true

[mcp_servers.blender.env]
BLENDER_MCP_HOST = 'localhost'
BLENDER_MCP_PORT = '9876'
```

If Codex has not loaded the `blender` MCP namespace in the current turn, continue with the bundled socket scripts instead of stopping.
