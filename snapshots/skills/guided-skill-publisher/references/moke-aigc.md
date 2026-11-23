# MOKE AIGC adapter

Verified against the live website on **2026-08-15**.

## Entry points

- Publish: `https://www.mokeaigc.com/account.html#publish`
- Submissions: `https://www.mokeaigc.com/account.html#submissions`
- Public SkillHub: `https://www.mokeaigc.com/skill.html`

Use the current signed-in session. Discover the active creator identity and namespace from the page; never hard-code a user's account or namespace.

## Eligibility

Require:

- an active account;
- an approved creator identity;
- an owned, active namespace;
- permission to submit Skills.

If any requirement is missing, guide the user through that prerequisite and stop before upload.

## Current package rules

- ZIP upload only.
- Archive size: at most 5 MB.
- Expanded size: at most 50 MB.
- Exactly one readable `SKILL.md` in the ZIP.
- Reject damaged central or local ZIP structures.
- Reject unsafe or duplicate paths.
- Reject encrypted ZIPs and unsupported compression.
- Reject abnormal compression ratios.
- `name`: 2–100 characters and must produce a valid slug.
- `version`: a top-level `SKILL.md` field in semantic version format. If an installable source keeps release information under `metadata.version`, create the MOKE upload copy with `scripts/package_skill.py --set-version <semver>`.
- `description`: required and at most 1000 characters.
- Do not reuse the same Skill version in the same namespace.

MOKE derives the public locator from the packaged top-level `name`. When changing a display-oriented name for a new version, analyze the package and confirm that the returned slug still points to the intended existing Skill before submitting.

The server also enforces a file-count rule, but the live client does not expose the exact threshold. Treat an unusually large file count as a warning and let remote analysis remain authoritative.

## Guided flow

1. Open **Personal workspace → Publish Skill**.
2. Select an active namespace.
3. Select a ZIP no larger than 5 MB.
4. Click **Analyze package**.
5. Read the returned display name, slug, version, summary, file count, expanded bytes, and warnings.
6. Treat the analysis as valid for 15 minutes. Reanalyze after changing the ZIP or after expiry.
7. Present the submission card and obtain final confirmation.
8. Click **Confirm submission for review** once.
9. Verify the success message and open **My submissions**.

Analysis uses a server-issued token tied to the package. A missing, expired, or mismatched token requires a new analysis.

## Visibility and lifecycle

- Before approval, a submission is visible only to the uploader and reviewers.
- After approval and publication, it enters the public SkillHub.
- The submissions page exposes status, review notes, version, and publication time.
- Depending on status, the UI may allow withdrawal, unpublishing, or publishing a new version.

Do not promise a review time or approval outcome; the live page does not specify either.

## Browser interaction gates

Uploading sends the full ZIP to MOKE AIGC. Obtain upload authorization when it is not already explicit. After analysis, obtain separate final-submit confirmation unless the latest user instruction clearly authorizes that exact submission.

If the browser shows CAPTCHA, sign-in, permission prompts, or an account-approval requirement, hand that step to the user and preserve the current page for continuation.
