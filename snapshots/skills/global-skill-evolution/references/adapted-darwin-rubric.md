# Adapted Darwin Rubric

Use this rubric to judge meaningful skill changes. Prefer an evaluator other than the author of the edit.

Total: 100

## 1. Trigger Clarity - 20

- Does the description clearly say what the skill does?
- Does it clearly say when to use it?
- Would similar requests trigger it reliably?

## 2. Workflow Coherence - 20

- Does the skill own one coherent job?
- Are steps in a usable order?
- Are references routed clearly?

## 3. Executionability - 20

- Could another Codex instance act from this skill alone?
- Are required files, scripts, or decisions explicit?

## 4. Honesty And Boundaries - 15

- Are uncertainty, limits, and dependency conditions stated?
- Does the skill avoid pretending thread-local context is durable?

## 5. Anti-Bloat - 15

- Did the change remove noise or at least avoid adding it?
- Is each added section operational?

## 6. Runtime Neutrality - 10

- Does the skill avoid hidden dependence on unavailable memory, tools, or environment?
- If special context is required, is that dependency named?

## Keep / Revert Rule

- `85+`: keep unless a focused regression appears.
- `70-84`: usable, but tighten weak sections.
- `55-69`: revise before routine use.
- `<55`: revert or rewrite.

## Regression Questions

- Did the new version become broader but less precise?
- Did it hide assumptions that the old version made explicit?
- Did it add policy without evidence?
- Did it move a local fix into a global rule too early?
