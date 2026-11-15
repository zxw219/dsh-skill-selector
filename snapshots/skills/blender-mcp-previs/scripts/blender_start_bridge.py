import importlib
import os
import sys
import traceback

import bpy


HOST = os.environ.get("BLENDER_MCP_HOST", "localhost")
PORT = int(os.environ.get("BLENDER_MCP_PORT", "9876"))
ADDON_PARENT = os.environ.get("BLENDER_MCP_ADDON_PARENT")

if ADDON_PARENT and ADDON_PARENT not in sys.path:
    sys.path.insert(0, ADDON_PARENT)


def import_addon_package():
    candidates = (
        "bl_ext.user_default.mcp",
        "mcp",
        "blender_mcp_addon",
    )
    for name in candidates:
        try:
            return importlib.import_module(name)
        except Exception:
            continue
    raise ImportError("Could not import the installed Blender MCP add-on package")


try:
    addon = import_addon_package()
    execute_interactive = importlib.import_module(addon.__name__ + ".execute_interactive")
    mcp_to_blender_server = importlib.import_module(addon.__name__ + ".mcp_to_blender_server")

    mcp_to_blender_server.timer_internal_vars_calc(active=0.05, idle=0.5, idle_delay=2.0)
    if not mcp_to_blender_server.is_running():
        mcp_to_blender_server.start(HOST, PORT)

    if not bpy.app.timers.is_registered(execute_interactive.run):
        bpy.app.timers.register(execute_interactive.run, first_interval=0.05, persistent=True)

    print(f"Blender MCP bridge is running on {HOST}:{PORT}")
except Exception:
    traceback.print_exc()
    raise
