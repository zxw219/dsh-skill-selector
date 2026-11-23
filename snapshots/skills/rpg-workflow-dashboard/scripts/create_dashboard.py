from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "dashboard-template"


def deep_merge(a: dict, b: dict) -> dict:
    for k, v in (b or {}).items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            deep_merge(a[k], v)
        else:
            a[k] = v
    return a


def base_state(preset: str, port: int) -> dict:
    film = preset == "film"
    steps = [
        {"id": "brief", "label": "需求理解" if film else "Brief", "status": "waiting", "progress": 0, "thread": "主控线程" if film else "Controller", "estimateMinutes": 4, "note": "等待任务启动"},
        {"id": "research", "label": "参考猎场" if film else "Research", "status": "waiting", "progress": 0, "thread": "参考线程" if film else "Research thread", "estimateMinutes": 8, "note": "等待前置步骤完成"},
        {"id": "build", "label": "视觉母版" if film else "Build", "status": "waiting", "progress": 0, "thread": "美术线程" if film else "Builder", "estimateMinutes": 12, "note": "等待前置步骤完成"},
        {"id": "test", "label": "镜头分镜" if film else "Test", "status": "waiting", "progress": 0, "thread": "镜头线程" if film else "Tester", "estimateMinutes": 10, "note": "等待前置步骤完成"},
        {"id": "review", "label": "审片迭代" if film else "Review", "status": "waiting", "progress": 0, "thread": "审片线程" if film else "Reviewer", "estimateMinutes": 9, "note": "等待前置步骤完成"},
        {"id": "deliver", "label": "最终交付" if film else "Deliver", "status": "waiting", "progress": 0, "thread": "主控线程" if film else "Controller", "estimateMinutes": 5, "note": "等待前置步骤完成"},
    ]
    threads = [
        {"id": "t-reference", "title": "参考线程" if film else "Research", "role": "参考猎人" if film else "Scout", "skill": "Skill：参考猎取" if film else "Skill: research", "avatar": "scout", "location": "research"},
        {"id": "t-style", "title": "美术线程" if film else "Build", "role": "视觉炼金师" if film else "Alchemist", "skill": "Skill：视觉母版" if film else "Skill: build", "avatar": "alchemist", "location": "build"},
        {"id": "t-shot", "title": "镜头线程" if film else "Test", "role": "镜头工匠" if film else "Smith", "skill": "Skill：镜头语言" if film else "Skill: implementation", "avatar": "smith", "location": "test"},
        {"id": "t-review", "title": "审片线程" if film else "Review", "role": "审片骑士" if film else "Knight", "skill": "Skill：审查迭代" if film else "Skill: review", "avatar": "knight", "location": "review"},
    ]
    now = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    state = {
        "version": "1.0.0",
        "meta": {
            "projectName": "影视工作流项目包" if film else "Workflow Project",
            "taskTitle": "等待任务启动" if film else "Waiting for task",
            "subtitle": "主控线程将自动更新右侧看板" if film else "Controller will update this board",
            "owner": "主控线程" if film else "Controller",
            "startedAt": now,
            "updatedAt": now,
            "port": port,
            "runId": "idle",
            "runStatus": "idle",
            "watchdog": {"enabled": True, "timeoutSeconds": 300, "retryLimit": 1, "fallbackOnFinalTimeout": True},
            "theme": {},
            "labels": {}
        },
        "summary": {"status": "waiting", "progress": 0, "etaMinutes": 0, "currentPhase": "等待任务" if film else "Waiting", "heartbeat": "等待主控线程启动新任务" if film else "Waiting for controller"},
        "steps": steps,
        "threads": [],
        "events": [],
        "artifacts": [],
    }
    for t in threads:
        t.update({"status": "waiting", "progress": 0, "elapsedMinutes": 0, "etaMinutes": 0, "current": "候场中", "retryCount": 0, "maxRetries": 1, "timeoutSeconds": 300, "timedOut": False, "heartbeatLabel": "未开始"})
        state["threads"].append(t)
    return state


def copy_template(output: Path, force: bool) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for item in TEMPLATE_DIR.iterdir():
        dst = output / item.name
        if item.is_dir():
            shutil.copytree(item, dst, dirs_exist_ok=True)
        else:
            if force or not dst.exists() or item.name != "state.json":
                shutil.copy2(item, dst)


def start_server(output: Path, port: int) -> None:
    node = shutil.which("node")
    if not node:
        print("Node.js not found; dashboard files were created but server was not started.")
        return
    env = os.environ.copy()
    env["PORT"] = str(port)
    creationflags = 0
    if os.name == "nt":
        creationflags = 0x08000000  # CREATE_NO_WINDOW
    subprocess.Popen([node, "server.js"], cwd=str(output), env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=creationflags)


def main() -> None:
    ap = argparse.ArgumentParser(description="Create an RPG workflow dashboard from the bundled template.")
    ap.add_argument("--output", required=True, help="Dashboard output directory")
    ap.add_argument("--preset", choices=["film", "generic"], default="film")
    ap.add_argument("--config", help="Optional JSON config merged into state")
    ap.add_argument("--port", type=int, default=17321)
    ap.add_argument("--force", action="store_true", help="Overwrite template files")
    ap.add_argument("--start", action="store_true", help="Start the local Node server")
    args = ap.parse_args()

    output = Path(args.output).resolve()
    copy_template(output, args.force)
    state = base_state(args.preset, args.port)
    if args.config:
        cfg = json.loads(Path(args.config).read_text(encoding="utf-8-sig"))
        state = deep_merge(state, cfg)
    (output / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.start:
        start_server(output, int(state.get("meta", {}).get("port", args.port)))
    print(f"Dashboard created: {output}")
    print(f"URL: http://127.0.0.1:{state.get('meta', {}).get('port', args.port)}/")


if __name__ == "__main__":
    main()
