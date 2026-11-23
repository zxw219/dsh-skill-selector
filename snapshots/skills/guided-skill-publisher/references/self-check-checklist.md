# Skill self-check checklist

Use this checklist after deterministic validation. Report only evidence-backed findings.

## Identity and triggers

- The top-level name follows the active platform's schema and produces the intended slug.
- The description says what the Skill does and when it should activate.
- Display name, description, body, and bundled files describe the same capability.
- Version data is valid for the target and does not reuse a submitted version.

## Structure and references

- Exactly one authoritative `SKILL.md` exists in the delivery package.
- Every referenced file resolves inside the Skill and every bundled file has a purpose.
- Scripts, references, assets, and agent metadata use portable relative paths where required.
- The ZIP root does not contain an accidental outer project folder, cache, secret, backup, or dependency tree.

## Workflow quality

- Steps have a clear order, entry condition, success evidence, and stop condition.
- User questions are limited to decisions that cannot be safely discovered.
- Upload and final submission are separately authorized.
- Remote analysis is not confused with approval or publication.
- Retries first check whether the previous action already succeeded.

## Script and package checks

- Run deterministic validators and compile or syntax-check bundled scripts where applicable.
- Verify the final ZIP rather than only the source folder.
- Check archive size, expanded size, unsafe paths, duplicates, encryption, compression method, CRC, and suspicious ratios.
- Record the final path, byte size, file count, and SHA-256.

## Report quality

- Separate blockers, warnings, and optional improvements.
- Cite the exact file and section or line for each issue.
- Give the smallest concrete repair and a way to verify it.
- State which checks passed when no defect is reproduced.
