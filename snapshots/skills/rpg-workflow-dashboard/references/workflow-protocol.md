# Workflow Protocol

## Required Lifecycle

1. `start-run`: create a new `runId`, set `runStatus=running`, clear old `finalConclusion`, hide completion overlay.
2. `step` and `thread`: update visible progress while work runs.
3. `heartbeat`: refresh active worker status and watchdog deadline.
4. `complete`: attach a `finalConclusion` with the current `runId`, set `runStatus=done`, show completion overlay.

## Why start-run is mandatory

The completion overlay is intentionally full-screen. If a new task starts without `start-run`, users may keep seeing the old completion page while new work runs. Always start the visible run first, even if the actual work is not yet dispatched.

## Watchdog Defaults

- Timeout: 300 seconds.
- Retry limit: 1.
- After final timeout: allow fallback so the main thread can continue.

Use longer timeouts for slow creative/research subthreads.

## UTF-8 Rule

Avoid passing Chinese status text through raw PowerShell arguments. Use `scripts/update_dashboard.py` or JSON files; the scripts write UTF-8 safely.

## Suggested Status Values

- `waiting`: queued.
- `running`: active.
- `done`: completed.
- `confirm`: needs retry/decision.
- `fallback`: main controller has filled in a temporary result.
- `blocked`: cannot continue without intervention.

## Main Thread Behavior

If the user wants the main thread to stay quiet:

- Say only that the board has started.
- Keep details on the dashboard.
- Interrupt only for real confirmation/blockers.
- Report final answer after completion.
