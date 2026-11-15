import argparse
import json
import socket
import sys
from pathlib import Path


def send_code(code: str, host: str, port: int, strict_json: bool) -> dict:
    request = json.dumps(
        {
            "type": "execute",
            "code": code,
            "strict_json": strict_json,
        }
    ).encode("utf-8") + b"\0"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(300.0)
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

    line, _sep, _rest = bytes(chunks).partition(b"\0")
    if not line:
        raise RuntimeError("Empty response from Blender MCP bridge")
    return json.loads(line.decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute Python code through the Blender MCP socket bridge.")
    parser.add_argument("code_file", nargs="?", help="Python file to execute. Reads stdin when omitted.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9876)
    parser.add_argument("--strict-json", action="store_true")
    args = parser.parse_args()

    if args.code_file:
        code = Path(args.code_file).read_text(encoding="utf-8")
    else:
        code = sys.stdin.read()

    response = send_code(code, args.host, args.port, args.strict_json)
    print(json.dumps(response, ensure_ascii=False, indent=2))
    return 0 if response.get("status") == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
