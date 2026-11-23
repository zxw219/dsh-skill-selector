from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

ACTIVE = {"blocked", "confirm", "running", "building", "waiting", "fallback"}
DONE = {"done", "ready", "fallback", "abandoned"}


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def now_hhmm() -> str:
    return time.strftime("%H:%M")


def load_state(dashboard: Path) -> dict:
    return json.loads((dashboard / "state.json").read_text(encoding="utf-8-sig"))


def save_state(dashboard: Path, state: dict) -> None:
    state.setdefault("meta", {})["updatedAt"] = now_iso()
    (dashboard / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def add_event(state: dict, type_: str, text: str) -> None:
    state.setdefault("events", []).append({"time": now_hhmm(), "type": type_, "text": text})
    state["events"] = state["events"][-60:]


def recompute(state: dict) -> None:
    steps = state.get("steps", [])
    total = round(sum(float(s.get("progress", 0) or 0) for s in steps) / len(steps)) if steps else 0
    active = next((s for status in ["blocked", "confirm", "running", "building", "waiting", "fallback"] for s in steps if s.get("status") == status), None)
    eta = 0
    for s in steps:
        if s.get("status") not in DONE:
            est = float(s.get("estimateMinutes", 0) or 0)
            prog = max(0, min(100, float(s.get("progress", 0) or 0)))
            eta += int((est * (100 - prog) + 99) // 100)
    state["summary"] = state.get("summary", {})
    state["summary"]["progress"] = total
    state["summary"]["etaMinutes"] = eta
    state["summary"]["currentPhase"] = active.get("label") if active else state["summary"].get("currentPhase", "最终交付")
    state["summary"]["status"] = ("running" if active and active.get("status") == "waiting" else active.get("status")) if active else "done"
    if active:
        state["summary"]["heartbeat"] = f"{active.get('thread','主控线程')}：{active.get('note') or active.get('status')}"
        state.setdefault("meta", {})["runStatus"] = "running"


def find_by_id(items: list[dict], id_: str) -> dict:
    for x in items:
        if id_ in {x.get("id"), x.get("title"), x.get("role"), x.get("threadId")}:
            return x
    raise SystemExit(f"Not found: {id_}")


def start_run(state: dict, title: str, subtitle: str, phase: str, note: str) -> None:
    run_id = f"run-{int(time.time() * 1000)}"
    meta = state.setdefault("meta", {})
    meta["runId"] = run_id
    meta["runStatus"] = "running"
    meta["taskTitle"] = title or meta.get("taskTitle", "新任务")
    meta["subtitle"] = subtitle or meta.get("subtitle", "主控线程正在派发任务")
    state.pop("finalConclusion", None)
    for i, step in enumerate(state.get("steps", [])):
        if i == 0:
            step.update({"status": "running", "progress": 8, "note": note or "新任务已启动，正在同步子线程"})
        else:
            step.update({"status": "waiting", "progress": 0, "note": "等待前置步骤完成"})
    for thread in state.get("threads", []):
        thread.update({"status": "waiting", "progress": 0, "current": "候场中，等待主控派发", "retryCount": 0, "timedOut": False, "timeoutReason": "", "heartbeatLabel": "刚刚", "lastHeartbeatAt": now_iso()})
    state["summary"] = {"status": "running", "progress": 8, "etaMinutes": 8, "currentPhase": phase or "任务启动", "heartbeat": note or "新任务已启动，通关页已收起，地图正在更新。"}
    state["events"] = []
    state["artifacts"] = []
    add_event(state, "start", f"新任务启动：{meta['taskTitle']}")


def complete(state: dict, title: str, subtitle: str, verdict: str, sections: list[str]) -> None:
    meta = state.setdefault("meta", {})
    run_id = meta.get("runId") or f"run-{int(time.time() * 1000)}"
    meta["runId"] = run_id
    meta["runStatus"] = "done"
    for step in state.get("steps", []):
        step["status"] = "done"
        step["progress"] = 100
    for thread in state.get("threads", []):
        if thread.get("status") not in {"fallback", "abandoned"}:
            thread["status"] = "done"
            thread["progress"] = 100
            thread["heartbeatLabel"] = "已完成"
    cards = []
    for raw in sections:
        if "=" in raw:
            t, body = raw.split("=", 1)
            cards.append({"title": t, "text": body})
    state["finalConclusion"] = {
        "runId": run_id,
        "title": title or "副本通关",
        "subtitle": subtitle or meta.get("subtitle", "任务完成"),
        "verdict": verdict or "任务已完成，可以进入下一步。",
        "stats": [
            {"label": "总进度", "value": "100%"},
            {"label": "步骤", "value": f"{len(state.get('steps', []))}/{len(state.get('steps', []))}"},
            {"label": "线程", "value": f"{len(state.get('threads', []))}/{len(state.get('threads', []))}"},
            {"label": "状态", "value": "完成"},
        ],
        "sections": cards or [{"title": "最终结论", "text": verdict or "任务已完成。"}],
    }
    state["summary"] = {"status": "done", "progress": 100, "etaMinutes": 0, "currentPhase": title or "最终交付", "heartbeat": verdict or "所有步骤已完成。"}
    add_event(state, "done", title or "任务完成")


def main() -> None:
    base = argparse.ArgumentParser()
    base.add_argument("--dashboard", required=True)
    sub = base.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("start-run")
    p.add_argument("--title", default="新任务")
    p.add_argument("--subtitle", default="主控线程正在派发任务")
    p.add_argument("--phase", default="任务启动")
    p.add_argument("--note", default="新任务已启动，通关页已收起，地图正在更新。")

    p = sub.add_parser("step")
    p.add_argument("--id", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--progress", type=float, default=0)
    p.add_argument("--note", default="")

    p = sub.add_parser("thread")
    p.add_argument("--id", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--progress", type=float, default=0)
    p.add_argument("--current", default="")

    p = sub.add_parser("complete")
    p.add_argument("--title", default="副本通关")
    p.add_argument("--subtitle", default="任务完成")
    p.add_argument("--verdict", default="任务已完成，可以进入下一步。")
    p.add_argument("--section", action="append", default=[], help="title=text, can repeat")

    p = sub.add_parser("theme")
    p.add_argument("--json", required=True, help="JSON file with theme and/or labels")

    args = base.parse_args()
    dashboard = Path(args.dashboard).resolve()
    state = load_state(dashboard)

    if args.cmd == "start-run":
        start_run(state, args.title, args.subtitle, args.phase, args.note)
    elif args.cmd == "step":
        s = find_by_id(state.get("steps", []), args.id)
        s.update({"status": args.status, "progress": args.progress})
        if args.note:
            s["note"] = args.note
        if args.status in ACTIVE:
            state.setdefault("meta", {})["runStatus"] = "running"
        add_event(state, args.status, f"{s.get('label', args.id)}：{s.get('note', args.status)}")
        recompute(state)
    elif args.cmd == "thread":
        t = find_by_id(state.get("threads", []), args.id)
        t.update({"status": args.status, "progress": args.progress})
        if args.current:
            t["current"] = args.current
        if args.status in ACTIVE:
            state.setdefault("meta", {})["runStatus"] = "running"
            state.pop("finalConclusion", None)
        add_event(state, args.status, f"{t.get('role') or t.get('title')}：{t.get('current', args.status)}")
        recompute(state)
    elif args.cmd == "complete":
        complete(state, args.title, args.subtitle, args.verdict, args.section)
    elif args.cmd == "theme":
        cfg = json.loads(Path(args.json).read_text(encoding="utf-8-sig"))
        state.setdefault("meta", {}).setdefault("theme", {}).update(cfg.get("theme", {}))
        state.setdefault("meta", {}).setdefault("labels", {}).update(cfg.get("labels", {}))
        add_event(state, "running", "主题/文案配置已更新")
    save_state(dashboard, state)
    print("OK")


if __name__ == "__main__":
    main()
