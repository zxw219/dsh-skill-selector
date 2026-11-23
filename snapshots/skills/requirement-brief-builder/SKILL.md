---
name: requirement-brief-builder
description: Guided bilingual requirement intake that turns a rough request into an executable brief with confirmed facts, assumptions, open questions, constraints, non-goals, risks, deliverables, and acceptance criteria. Use when a request is vague, stakeholders are misaligned, a task needs scoping before execution, or another agent needs a clean handoff. 引导式双语需求澄清与简报构建，把模糊想法整理成可执行、可验收、可交接的任务说明。
version: "1.0.0"
---

# Requirement Brief Builder｜需求简报构建器

Turn an incomplete request into a decision-ready brief without burying the user in a questionnaire.

## Operating principles

- Ask only questions whose answers can materially change scope, method, cost, risk, or acceptance.
- Prefer one high-impact question at a time. Group at most three tightly related questions when doing so saves a round trip.
- Reuse facts already provided. Never ask the user to repeat information.
- Label every material statement as **Confirmed**, **Assumed**, or **Open**.
- Make a reversible assumption when progress is safe; ask before making an assumption that could cause expensive or irreversible work.
- Separate desired outcomes from proposed implementation. Do not lock the solution too early.
- Keep the finished brief concise enough for another person or agent to act on immediately.

## Workflow

### 1. Capture the request

Extract what is already known:

- objective and reason it matters
- target audience or user
- inputs, references, and existing assets
- requested deliverables and format
- deadline, budget, platform, tooling, policy, or technical constraints
- named stakeholders and decision owner
- examples of success or failure

Do not interrupt merely because a low-impact field is blank.

### 2. Find the critical gaps

Check for gaps in this order:

1. outcome — what change or decision should the work produce?
2. deliverable — what must exist at the end?
3. acceptance — how will completion be judged?
4. constraints — what must not be violated?
5. inputs — what evidence or assets are required?
6. ownership — who decides when tradeoffs appear?

Ask only about gaps that block or materially redirect execution.

### 3. Build the brief progressively

Maintain a visible working summary after each important answer. When useful, say:

> 当前已确认 / Confirmed: …  
> 暂定假设 / Assumed: …  
> 仍需确认 / Open: …

If the user says “you decide,” select the safest reversible default and record it as an assumption.

### 4. Add acceptance criteria

Write criteria that can be observed or checked. Prefer statements such as:

- output contains the required sections and file formats
- named facts are sourced and dated
- specified platforms, dimensions, duration, or compatibility targets are met
- prohibited elements are absent
- reviewer can make the intended decision from the deliverable

Avoid empty criteria such as “high quality,” “professional,” or “looks good” unless translated into concrete signals.

### 5. Run the readiness gate

Before handing off, verify:

- the objective and deliverable do not contradict each other
- constraints and non-goals are explicit
- assumptions are visible rather than disguised as facts
- every acceptance criterion maps to a deliverable
- unresolved items have an owner or a safe fallback
- the next action is named

If a blocker remains, present the smallest decision needed from the user. Otherwise, produce the brief and proceed or hand it off.

## Output

Use the structure in [references/brief-template.md](references/brief-template.md). Omit empty sections that add no value, but always keep **Objective**, **Deliverables**, **Acceptance Criteria**, **Status of Information**, and **Next Action**.

When the user wants execution rather than documentation, show a compact brief for confirmation only when a high-impact assumption remains. Otherwise use it internally and begin the work.

In user-visible output, omit secrets, personal information, and unnecessary local paths unless the user explicitly needs them.
