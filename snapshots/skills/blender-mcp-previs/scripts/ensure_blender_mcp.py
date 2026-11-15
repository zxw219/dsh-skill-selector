import argparse
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path


DEFAULT_BLENDER_EXE = r"D:\steam\steamapps\common\Blender\blender.exe"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9876


def send_code(code: str, host: str, port: int) -> dict | None:
    request = json.dumps({"type": "execute", "code": code, "strict_json": False}).encode("utf-8") + b"\0"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3.0)
            sock.connect((host, port))
            sock.sendall(request)
            chunks = bytearray()
            while True:
                chunk = sock.recv(65536)
                if not chunk:
                    break
                chunks.extend(chunk)
                if b"\0" in chunks:
                    break
    except OSError:
        return None
    line, _sep, _rest = bytes(chunks).partition(b"\0")
    if not line:
        return None
    try:
        return json.loads(line.decode("utf-8"))
    except json.JSONDecodeError:
        return None


def ping(host: str, port: int) -> dict | None:
    return send_code(
        """
import bpy
result = {
    "version": bpy.app.version_string,
    "filepath": bpy.data.filepath,
    "object_count": len(bpy.data.objects),
    "online_access": bpy.app.online_access,
}
""",
        host,
        port,
    )


def launch_blender(args: argparse.Namespace) -> int:
    blender_exe = args.blender_exe or os.environ.get("BLENDER_EXE") or DEFAULT_BLENDER_EXE
    if not Path(blender_exe).exists():
        blender_exe = "blender"

    startup_script = Path(args.startup_script or Path(__file__).with_name("blender_start_bridge.py")).resolve()
    cmd = [blender_exe]
    if args.blend:
        cmd.append(str(Path(args.blend).resolve()))
    cmd.extend(["--online-mode", "--python", str(startup_script)])

    log_dir = Path(args.log_dir or tempfile.gettempdir())
    log_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = log_dir / "blender_mcp_stdout.log"
    stderr_path = log_dir / "blender_mcp_stderr.log"
    stdout = stdout_path.open("ab")
    stderr = stderr_path.open("ab")

    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

    proc = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, creationflags=creationflags)
    return proc.pid


def main() -> int:
    parser = argparse.ArgumentParser(description="Ensure Blender MCP socket bridge is reachable.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--blend", help="Optional .blend file to open when launching Blender.")
    parser.add_argument("--blender-exe", help="Path to blender.exe. Defaults to BLENDER_EXE or local Steam install.")
    parser.add_argument("--startup-script", help="Blender-side startup script. Defaults to bundled blender_start_bridge.py.")
    parser.add_argument("--wait", type=float, default=45.0)
    parser.add_argument("--no-launch", action="store_true")
    parser.add_argument("--log-dir", help="Directory for Blender stdout/stderr logs.")
    args = parser.parse_args()

    response = ping(args.host, args.port)
    if response and response.get("status") == "ok":
        print(json.dumps({"status": "ready", "launched": False, "response": response}, ensure_ascii=False, indent=2))
        return 0

    if args.no_launch:
        print(json.dumps({"status": "unreachable", "launched": False}, ensure_ascii=False, indent=2))
        return 2

    pid = launch_blender(args)
    deadline = time.time() + args.wait
    while time.time() < deadline:
        response = ping(args.host, args.port)
        if response and response.get("status") == "ok":
            print(
                json.dumps(
                    {"status": "ready", "launched": True, "pid": pid, "response": response},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0
        time.sleep(0.5)

    print(json.dumps({"status": "timeout", "launched": True, "pid": pid}, ensure_ascii=False, indent=2))
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
