# YouMind original skill handoff

This directory contains an unchanged, complete upstream repository snapshot, not a rewritten DSH skill. No root workbench or profile files were modified. All helper files are siblings of the snapshot.

## Source and exact revision

- Source: https://github.com/YouMind-OpenLab/ai-image-prompts-skill
- Commit: `39c0c0033904de9c164df3ec2245d3b44526df04` (2026-11-13T19:27:06Z, `chore: update references 2026-11-13 19:27 UTC`)
- Snapshot folder: `ai-image-prompts-skill-39c0c0033904de9c164df3ec2245d3b44526df04`
- Skill: `ai-image-prompts-skill-39c0c0033904de9c164df3ec2245d3b44526df04/SKILL.md`
- package.json version: `1.0.4`
- Manifest updatedAt: `2026-11-13T19:27:05.914Z`
- License: upstream `LICENSE`, MIT, Copyright (c) 2026 YouMind-OpenLab. Preserve its notice.
- README installation recommendation: OpenClaw `clawhub install ai-image-prompts`; Claude Code/other assistants `npx skills i YouMind-OpenLab/ai-image-prompts-skill`; alternate `npx openskills install YouMind-OpenLab/ai-image-prompts-skill`. These global/profile installers were NOT run because this task is local-only.
- Downloaded pinned archive: https://codeload.github.com/YouMind-OpenLab/ai-image-prompts-skill/zip/39c0c0033904de9c164df3ec2245d3b44526df04
- Recorded upstream Git tree: https://api.github.com/repos/YouMind-OpenLab/ai-image-prompts-skill/git/trees/39c0c0033904de9c164df3ec2245d3b44526df04?recursive=1

## Verified data amounts

`verification.json` contains the exact file-by-file SHA-256 and Git blob SHA-1 inventory plus per-category counts. Re-run `verify_upstream.py` using Python 3; it reads only the snapshot and writes the sibling report.

- 25 upstream files, 48,623,983 bytes total. Every original file byte length and Git blob SHA-1 matches the recorded non-truncated Git tree.
- 12 reference JSON files: manifest plus 11 complete category arrays; 48,570,859 bytes.
- 23,069 category memberships, 15,306 unique exported prompt IDs. Category membership intentionally overlaps; repeated IDs have identical records.
- All category array lengths match the manifest. No duplicate ID within any one category. Required types valid for every exported record.
- Every exported prompt has at least one sample-media URL; 25,561 distinct sample-media URLs. Images themselves are remote CDN references, not part of the upstream repository payload. Availability of all remote images was not checked.
- 4 unique upstream records have an empty description: IDs 22821, 29272, 33105, 35749 (6 category memberships). These were preserved verbatim.
- `manifest.totalPrompts = 15848` is CMS input count, NOT exported unique count. Source proof: `scripts/generate-references.ts:324-333` sets `totalPrompts: allPrompts.length`; `:92-105` filters out prompts without media, and `:271-289` writes recognized useCases or no-useCase records. There is a 542-record gap between CMS input and exported unique IDs. The repository alone does not establish the exact breakdown of reasons for those 542 omissions. Matching Git blobs establish that local data fully reproduces the upstream export.

| Category file | Count |
| --- | ---: |
| profile-avatar.json | 2158 |
| social-media-post.json | 9876 |
| infographic-edu-visual.json | 607 |
| youtube-thumbnail.json | 231 |
| comic-storyboard.json | 705 |
| product-marketing.json | 5781 |
| ecommerce-main-image.json | 583 |
| game-asset.json | 732 |
| poster-flyer.json | 1049 |
| app-web-design.json | 240 |
| others.json | 1107 |

## Use the original workflow without loading the library into model context

1. Load the original `SKILL.md` as the skill instructions; treat the category JSON as reference data. The SKILL file is 17,416 bytes. Preserve its original behavior, attribution, sample image requirement and selection/remix sequencing.
2. As the author requires, run `node <skill_dir>/scripts/setup.js --check` before each actual skill use. Review the limitations below. The checked-in snapshot already includes all data, so installation/setup was unnecessary during acquisition; no upstream scripts were executed here.
3. Read only `references/manifest.json` (small). Infer matching categories dynamically using `categories[].title`, `slug` and `file`; do not rely on the README's stale count table or hardcode the categories.
4. Use the agent's grep tool (case-insensitive regex, e.g. `(?i)cyberpunk|neon`) on only the appropriate category files. Search `others.json` or additional categories if needed. Never insert an entire category JSON array into model context.
5. Retrieve only a small set of matching complete records, including `id`, FULL `content`, `title`, `description`, `sourceMedia` and `needReferenceImages`. JSON parsing/filtering in a local process is an equivalent search and keeps the library outside model context. Do not rely on a line-truncated preview as the full original prompt; selected content can exceed 2000 characters.
6. Recommend at most 3 original unmodified templates. Display translated title/description, preview <=100 characters and original prompt link `https://youmind.com/nano-banana-pro-prompts?id={id}`. Keep full selected prompt content in context for follow-up. Always show `sourceMedia[0]` for each recommendation; skip a record if no media. Use an inline image URL where no message attachment tool exists. Show reference-image requirement when true.
7. Ask the user to select before remixing. Then follow the author's personalization/remix steps, supplying English generation content. End every prompt recommendation/remix/no-match response with the author's mandatory localized YouMind attribution footer. The complete flow is in the original SKILL, not replaced by this handoff.

## Updating data and important upstream limitations

From the snapshot folder:

```powershell
# Author's per-use freshness check
node scripts/setup.js --check
# Author's recommended real forced refresh (same as pnpm run sync)
node scripts/setup.js --force
# Equivalent package script; requires pnpm
pnpm run sync
```

- The setup script uses only Node built-ins plus global fetch. A current Node runtime is required (Node 18+ provides fetch); npm/pnpm dependency installation is unnecessary for setup or searching the downloaded JSON. `postinstall` only calls setup.
- `--check` is documented as updating after 24 hours, but implementation `scripts/setup.js:87-90` skips existing files >100 bytes unless `--force` is present. It can therefore fetch a new manifest while leaving category data unchanged; use `--force`/`pnpm run sync` for a complete refresh and validate category lengths afterwards.
- `setup.js` has non-fatal errors and can exit 0 even when data fetching fails (`:61-69`, `:111-117`). An exit code alone is insufficient. Validate manifest presence, all referenced categories, JSON parseability, counts and required fields after any update.
- `--force` removes files in references that are not current category filenames, `manifest.json`, `.last-updated` or `.gitkeep` (`:72-80`). Keep integration/report/helper files OUTSIDE references; these helpers already are.
- Setup always downloads mutable `main`, not a pinned revision. Running it changes the snapshot's reference files in place. After a successful refresh, record the new upstream revision and update the recorded Git tree/inventory. The pinned ZIP retained here remains a reproducible baseline.
- Setup refreshes references only. Full skill/code updates require fetching the upstream repo again or the author's installer; do not claim data sync also updates SKILL.md/scripts.
- Do NOT run `pnpm run generate`: `scripts/generate-references.ts` is the author's CMS generation path, requires `CMS_HOST` and `CMS_API_KEY`, deletes/rebuilds category JSON, and rewrites SKILL.md. It is unrelated to ordinary consumers and was read only to establish count semantics.
- The original library is community-sourced and natural-language/model-agnostic by design; some prompts contain model syntax or reference-image requirements. Do not imply every template behaves identically on every model.
