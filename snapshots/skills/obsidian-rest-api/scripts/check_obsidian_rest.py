import argparse
import json
import os
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


PLUGIN_ID = "obsidian-local-rest-api"
SETTINGS_RELATIVE_PATH = Path(".obsidian/plugins/obsidian-local-rest-api/data.json")


def find_vault(start: Path) -> Path | None:
    candidate = start.expanduser().resolve()
    if candidate.is_file():
        candidate = candidate.parent
    for path in (candidate, *candidate.parents):
        if (path / ".obsidian").is_dir():
            return path
    return None


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def plugin_enabled(vault: Path) -> bool | None:
    enabled_path = vault / ".obsidian/community-plugins.json"
    if not enabled_path.exists():
        return None
    try:
        enabled = load_json(enabled_path)
        return isinstance(enabled, list) and PLUGIN_ID in enabled
    except (OSError, json.JSONDecodeError):
        return None


def obsidian_running() -> bool | None:
    try:
        if os.name == "nt":
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq Obsidian.exe"],
                capture_output=True,
                text=True,
                errors="replace",
                timeout=5,
                check=False,
            )
            return "obsidian.exe" in result.stdout.lower()
        result = subprocess.run(
            ["pgrep", "-f", "Obsidian"],
            capture_output=True,
            timeout=5,
            check=False,
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return None


def choose_endpoint(settings: dict[str, Any]) -> tuple[str, int]:
    secure_enabled = bool(settings.get("enableSecureServer", True))
    insecure_enabled = bool(settings.get("enableInsecureServer", False))
    if secure_enabled:
        return "https", int(settings.get("port", 27124))
    if insecure_enabled:
        return "http", int(settings.get("insecurePort", 27123))
    raise ValueError("Local REST API 的 HTTPS 和 HTTP 服务都未启用")


def request_status(
    base_url: str,
    path: str,
    api_key: str,
    timeout: float,
) -> tuple[int | None, str | None]:
    request = urllib.request.Request(
        base_url + path,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json,text/markdown;q=0.9,*/*;q=0.1",
        },
        method="GET",
    )
    context = ssl._create_unverified_context() if base_url.startswith("https://127.0.0.1") else None
    try:
        with urllib.request.urlopen(request, context=context, timeout=timeout) as response:
            response.read(1)
            return response.status, None
    except urllib.error.HTTPError as exc:
        return exc.code, f"HTTP {exc.code}"
    except Exception as exc:
        safe_message = str(exc).replace(api_key, "[REDACTED]")
        return None, f"{type(exc).__name__}: {safe_message}"


def markdown_files(vault: Path) -> list[Path]:
    files: list[Path] = []
    try:
        for path in vault.rglob("*.md"):
            try:
                relative = path.relative_to(vault)
            except ValueError:
                continue
            if ".obsidian" not in relative.parts and path.is_file():
                files.append(path)
    except OSError:
        pass
    return files


def yes_no_unknown(value: bool | None) -> str:
    if value is True:
        return "是"
    if value is False:
        return "否"
    return "未知"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="只读检查 Obsidian Local REST API 连接")
    parser.add_argument("--vault", type=Path, help="Obsidian 库路径；默认从当前目录向上查找")
    parser.add_argument("--skip-note-read", action="store_true", help="不测试读取具体笔记")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--timeout", type=float, default=8.0, help="每个请求的超时秒数，默认 8")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    start = args.vault if args.vault else Path.cwd()
    vault = find_vault(start)
    if vault is None:
        message = {"result": "failed", "error": "未找到包含 .obsidian 的 Obsidian 库", "start": str(start)}
        print(json.dumps(message, ensure_ascii=False, indent=2) if args.json else f"结果：连接失败\n原因：{message['error']}\n检查路径：{start}")
        return 2

    plugin_dir = vault / ".obsidian/plugins" / PLUGIN_ID
    settings_path = vault / SETTINGS_RELATIVE_PATH
    installed = plugin_dir.is_dir() and settings_path.is_file()
    enabled = plugin_enabled(vault)
    running = obsidian_running()

    if not installed:
        result = {
            "result": "failed",
            "vault": str(vault),
            "plugin_installed": False,
            "plugin_enabled": enabled,
            "obsidian_running": running,
            "error": f"缺少插件配置：{settings_path}",
        }
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("结果：连接失败")
            print(f"Obsidian 库：{vault}")
            print("插件已安装：否")
            print(f"插件已启用：{yes_no_unknown(enabled)}")
            print(f"原因：{result['error']}")
        return 2

    try:
        settings = load_json(settings_path)
        if not isinstance(settings, dict):
            raise ValueError("插件配置不是 JSON 对象")
        api_key = str(settings.get("apiKey", ""))
        if not api_key:
            raise ValueError("插件配置中的 API Key 为空")
        scheme, port = choose_endpoint(settings)
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        safe_error = str(exc)
        result = {
            "result": "failed",
            "vault": str(vault),
            "plugin_installed": True,
            "plugin_enabled": enabled,
            "obsidian_running": running,
            "error": safe_error,
        }
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("结果：连接失败")
            print(f"Obsidian 库：{vault}")
            print(f"插件已启用：{yes_no_unknown(enabled)}")
            print(f"原因：{safe_error}")
        return 2

    base_url = f"{scheme}://127.0.0.1:{port}"
    root_status, root_error = request_status(base_url, "/", api_key, args.timeout)
    commands_status, commands_error = request_status(base_url, "/commands/", api_key, args.timeout)
    connected = root_status is not None and 200 <= root_status < 300
    authenticated = commands_status is not None and 200 <= commands_status < 300

    notes = markdown_files(vault)
    note_status: int | None = None
    note_relative: str | None = None
    note_error: str | None = None
    if notes and connected and authenticated and not args.skip_note_read:
        note_relative = notes[0].relative_to(vault).as_posix()
        encoded_path = urllib.parse.quote(note_relative, safe="/")
        note_status, note_error = request_status(base_url, f"/vault/{encoded_path}", api_key, args.timeout)

    success = connected and authenticated
    if args.skip_note_read:
        note_result = "skipped"
    elif not notes:
        note_result = "not_tested_no_markdown"
    elif note_status is not None and 200 <= note_status < 300:
        note_result = "success"
    else:
        note_result = "failed"

    result = {
        "result": "connected" if success else "failed",
        "read_only": True,
        "vault": str(vault),
        "plugin_installed": installed,
        "plugin_enabled": enabled,
        "obsidian_running": running,
        "api_url": base_url + "/",
        "root_status": root_status,
        "root_error": root_error,
        "authentication_status": commands_status,
        "authentication_error": commands_error,
        "markdown_count": len(notes),
        "note_read_result": note_result,
        "sample_note": note_relative,
        "sample_note_status": note_status,
        "sample_note_error": note_error,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"结果：{'Obsidian 已通过 Local REST API 连接' if success else '连接失败'}")
        print(f"Obsidian 库：{vault}")
        print(f"插件已安装：{yes_no_unknown(installed)}")
        print(f"插件已启用：{yes_no_unknown(enabled)}")
        print(f"Obsidian 正在运行：{yes_no_unknown(running)}")
        print(f"API 地址：{base_url}/")
        print(f"服务状态：{root_status if root_status is not None else root_error}")
        print(f"API 认证：{'有效' if authenticated else (commands_status if commands_status is not None else commands_error)}")
        print(f"Markdown 笔记数量：{len(notes)}")
        if note_result == "success":
            print(f"笔记读取：成功（{note_relative}，未输出正文）")
        elif note_result == "not_tested_no_markdown":
            print("笔记读取：库中没有 Markdown 笔记，未测试")
        elif note_result == "skipped":
            print("笔记读取：按参数跳过")
        else:
            detail = note_status if note_status is not None else note_error
            print(f"笔记读取：失败（{note_relative}，{detail}）")
        print("本次操作：只读；未修改笔记、插件设置或 Codex 配置")

    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
