# Recurring Automation Setup

Use the Codex automation tool rather than editing live automation files directly.

## Recommended Configuration

- Kind: recurring local project automation.
- Cadence: twice weekly, preferably Tuesday and Friday morning.
- Status on first creation: paused until the target project and paths are verified.
- Execution environment: local.
- Reasoning effort: medium.
- Project: the workspace whose skill system should be governed.
- Prompt: load `assets/automation-prompt.txt` and replace the workspace-state placeholder.

## Creation Workflow

1. Locate the target Codex project id with the available project/thread tools.
2. Read `assets/automation-prompt.txt`.
3. Choose a writable state file inside the target workspace, for example:

```text
<workspace>/skill-evolution-work/rolling-state.md
```

4. Call the app's automation creation/update tool with the full configuration.
5. View the created automation and verify name, cadence, status, project, and prompt.
6. Run one manual audit before activating the recurring schedule.

## Update Rule

Prefer updating the existing automation id over creating a duplicate. Preserve its cadence and project unless the user explicitly requests a change.

## Safety Boundary

The automation may auto-apply only low-risk, reversible skill/reference/document edits that can be validated immediately. It must not install software, use credentials, publish externally, delete evidence, or make broad personality/value changes.
