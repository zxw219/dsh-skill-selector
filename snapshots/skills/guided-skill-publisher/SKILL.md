---
name: guided-skill-publisher
description: 基础型 Skill 发布与自检助手，引导用户检查、诊断、修复、打包、上传、远程分析、提交审核和发布新版本；适用于准备 Skill 文件夹或 ZIP、排查平台校验错误、评估 Skill 质量及安全性，并通过平台适配器接入不同市场。Foundational guided Skill publishing and self-check assistant for inspecting, diagnosing, repairing, packaging, uploading, remotely analyzing, submitting, and versioning Skills across registries. Use when a user needs a guided release or an evidence-based audit of a Skill package. Keep local preparation, external upload, and final submission as separate stages.
metadata:
  version: "1.1.0"
version: "1.1.0"
---

# Skill 发布与自检助手 / Guided Skill Publisher

This is a foundational workflow Skill. It helps other users publish their own Skills while explaining each step, checking the package before transmission, identifying defects with evidence, and treating each registry, API, CLI, or browser as a replaceable adapter.

## Operating contract

Keep these stages in order:

1. identify the artifact and target;
2. validate locally;
3. repair and package;
4. authorize upload;
5. run remote analysis;
6. confirm final submission;
7. record and track the result.

Do not treat a successful connection, upload, or analysis as a completed publication. Complete only when the requested stopping point has evidence.

## 1. Establish the current step

Determine the user's intent:

- **check**: inspect a folder or ZIP without uploading;
- **package**: create a submission-ready ZIP;
- **analyze**: upload for remote validation, but do not submit;
- **publish**: complete analysis and submit for review;
- **update**: prepare or submit a new version;
- **diagnose**: explain and repair a failed validation or review.

Resolve the artifact path, target platform, account or workspace, namespace, and intended version. Discover obvious values from the current workspace or signed-in page before asking. If more than one plausible artifact or destination remains, ask one short question.

For platform-specific execution, read the matching adapter reference. Read `references/moke-aigc.md` when the target is MOKE AIGC. Read `references/platform-adapter-contract.md` when adding or evaluating another platform adapter.

At each user-facing handoff, show only:

```text
当前阶段：<stage>
已完成：<evidence>
下一步：<single next action>
需要你决定：<only when blocked or approval is required>
```

## 2. Run local preflight

Inspect the source before any upload.

1. Run `scripts/validate_skill_package.py <folder-or-zip> --profile <profile> --json`.
2. Read the single `SKILL.md` and confirm that its metadata describes the actual capability and triggers.
3. Classify findings:
   - **blocker**: the target will reject the package or the package is unsafe;
   - **warning**: publication may work, but review or usability risk remains;
   - **ready**: deterministic checks passed.
4. Report exact file paths and repair actions.

Do not upload while blockers remain. Local validation is preparation, not platform approval.

### Perform the assisted self-check

After deterministic validation, read `references/self-check-checklist.md` and inspect the Skill itself. Check whether its capability, trigger conditions, steps, referenced files, scripts, safety boundaries, and expected outputs agree with each other.

For every material issue, report:

```text
级别：阻断 / 警告 / 建议
位置：<exact file and section or line>
问题：<what is wrong>
影响：<what may fail or confuse users>
修复：<smallest concrete repair>
复检：<command or observation that proves the fix>
```

Do not invent defects merely to fill the checklist. If no issue is reproduced, say which checks passed and distinguish that result from remote platform approval.

## 3. Repair and package

Make requested local fixes, then create the ZIP with:

```text
python -X utf8 scripts/package_skill.py <skill-folder> --output <output.zip>
```

When a target registry requires a top-level semantic `version` or a display-oriented `name`, package a target-specific copy without mutating the installable source:

```text
python -X utf8 scripts/package_skill.py <skill-folder> --output <output.zip> --set-version <semver> --set-name <target-name>
```

Package the contents of the Skill folder at the ZIP root. Prefer:

```text
SKILL.md
agents/
references/
scripts/
assets/
```

Include only files used by the Skill. Exclude repository metadata, caches, virtual environments, dependency trees, secrets, and unrelated drafts. Re-run local validation against the final ZIP and capture its absolute path, byte size, and SHA-256.

## 4. Gate the upload

Uploading transmits the complete ZIP to an external service. Upload only when the user's request already authorizes that exact transmission or after receiving narrow approval.

Before upload, state:

- destination platform and account/workspace;
- namespace or publishing scope;
- exact ZIP path, size, and SHA-256;
- whether this action only analyzes or also submits.

If authorization covers analysis only, stop before final submission.

## 5. Run remote analysis

Use the best available adapter in this order: purpose-built connector or API, supported CLI, then browser UI. Follow the active tool's instructions and inspect visible state before each action.

Capture the platform's authoritative analysis result:

- derived name or display name;
- slug or locator;
- version;
- summary;
- file count and expanded size when available;
- warnings and blockers;
- analysis token or expiry when exposed.

Compare remote metadata with local expectations. If the source changed, rebuild the ZIP and rerun both local validation and remote analysis. If only the token expired, rerun remote analysis against the unchanged ZIP. If the platform reports a metadata mismatch, stop and resolve the mismatch before continuing. Do not silently proceed past warnings that can affect safety, scope, identity, or visibility.

## 6. Gate final submission

Immediately before the irreversible or externally visible action, present a compact submission card:

```text
目标：<platform / namespace / skill>
版本：<version>
可见性：<public, private, review-only, or unknown>
分析：<passed / warnings / blocked>
提交后：<review queue, immediate publish, or platform-specific result>
```

Ask for confirmation unless the user's latest instruction explicitly authorized this exact final submission. Submit once, then verify the success message, resulting status, and submission record. Do not retry a network failure blindly; first check whether the platform created the submission.

## 7. Track the result

Return a receipt containing:

- platform and full Skill locator;
- submitted version;
- local ZIP path and SHA-256;
- submission time and status;
- review note or submission identifier when available;
- next valid action.

For a new version, inspect the last submitted version and require a different semantic version. For rejection, preserve the review evidence, repair only the cited or reproduced defects, rebuild, revalidate, and resubmit through the same gates. When the user is learning the workflow, explain why each gate exists rather than only performing clicks.

## Stop conditions

Stop and request the missing item when:

- no unique source artifact can be identified;
- no publishing destination or namespace can be resolved;
- local blockers remain;
- authentication, CAPTCHA, or account approval requires the user;
- upload or final-submit authorization is absent;
- platform analysis is expired, mismatched, or blocked;
- the platform's current rules conflict with a stale adapter reference.

When platform rules may have changed, verify the current official page or API before relying on stored limits. Update the adapter's verification date only after confirming the live behavior.
