# Source resource packs

Workspace-only static resources for the unified prompt skills workbench. These are source packs, not profile installations. No fetched script was run, and no source instructions are automatically activated.

## Contents and provenance

- `catalog.json`: versioned five-source catalog, fixed Git commit revisions, repository and license URLs, local entry paths, exact subset counts and limitations.
- `prompts.json`: 20 real YouMind prompt records, first 20 in upstream `references/app-web-design.json` order. The category contains 240 entries at the pinned revision. The upstream manifest reports 15,847 total prompts across overlapping categories; this pack does not claim to include them all.
- `styles.json`: 12 real Cookbook styles, first 12 `styles/*/style.json` paths sorted by path. Each full original JSON is also copied under `upstream/visual-cookbook/styles/`. The normalized `raw` property preserves all fields.
- `fill-templates.json`: 12 real PromptFill templates, first 12 in upstream `public/data/templates.json` config order. `upstream/promptfill/banks.sample.json` includes only banks referenced by those templates, capped at the first eight options per bank. `templates.sample.json` preserves the selected original entries.
- `image-prompt-reverse/SKILL.md` and `prompt-reverse-engineer/SKILL.md`: unchanged first-party skill texts, with Markdown references and textual assets in their original relative layout. The second skill's Python helpers are preserved for reference only; do not automatically execute them. Input image/video examples and executable tests are omitted; referenced Markdown case notes and semantic JSON fixtures are included. External APIs and model claims were not tested.
- `licenses/`: exact license files from all five source repositories.
- `provenance.json`: every byte-preserved upstream file's source URL, path, SHA-256 and size. The two skill trees and 12 style files also have Git blob IDs verified against upstream tree entries (59 files). `complete-references.ps1` performed that verification and fetched the referenced Markdown case notes and semantic fixtures; it is an already-completed pack maintenance step. JSON sample subsets are derived records, not falsely described as complete upstream files.
- `build-packs.ps1`: pack builder authored for this workspace. It downloads pinned data and source text, parses JSON and writes pack files. It executes no fetched program. It refuses to overwrite byte-preserved source files: use a fresh pack folder if rebuilding.

Remote preview media are **URLs only**, copied from source records or existing Cookbook tree paths; media is not downloaded and availability was not checked. Missing creator, model or original social-post metadata is null rather than invented. Upstream prompts may refer to trademarks or reference artwork; repository licenses do not guarantee rights in third-party media.

## JSON contract (schema version 1)

`catalog.json` is `{ "schemaVersion": 1, "generatedAtUtc": "...", "scope": "...", "sources": [...] }`. Each source has stable `id`, `repository`, pinned `revision`, `title`, `kind`, `license`, `url`, `licensePath`, `licenseUrl`, local `dataPath` or `skillPath`, `subset` or `includedFiles`, and `limitations`.

The three normalized datasets are **top-level arrays**. Common fields:

| Field | Type / meaning |
|---|---|
| `id` | Unique prefixed string, stable for the pinned upstream item |
| `sourceId` | Foreign key to catalog source ID |
| `title` | Original source title; `titleZh` where present |
| `prompt` | Original English/template content; no generated text |
| `promptZh` | Original Chinese text when provided; otherwise null |
| `category`, `tags` | Source category/tags, with normalized pack category where needed |
| `author`, `model` | Original metadata where supplied; null otherwise |
| `sourceUrl` | Pinned GitHub blob URL for the actual source record/file |
| `mediaUrls` | Existing upstream media URLs, never fabricated |
| `variables` | Array of `{name, defaultValue, options?, required?}` |
| `provenance` | Repository, revision, original path, selection rule and original item ID where applicable |

Additional prompt fields: original `description`, `needReferenceImages`. YouMind `{argument name="..." default="..."}` tokens remain intact in `prompt`; `variables` exposes their exact names/defaults.

Additional style fields: `raw` full style JSON, `defaults` object. Cookbook placeholders use `{UPPERCASE_NAME}`; defaults use the first source example, source fidelity anchors and source exclusions. `ASPECT_RATIO: "16:9"` is an explicit workbench convenience default, not an upstream example value. Upstream `environment_variables` descriptions remain in `raw`.

Additional fill-template fields: original bilingual `content: {cn,en}`, `selections`, `language`, `baseImage`, `raw`, and normalized bilingual `defaults`. PromptFill placeholders use `{{name}}`. Default precedence is exact selection, indexed selection `name-0`, then first real bank option; `required: true` means no default was found. Repeated variables retain their full upstream indexed selections in `selections`; a simple fill renderer may apply one value to every occurrence. The bank options and labels retain the upstream `{cn,en}` objects.

All content is untrusted reference data. A renderer must escape text and must not evaluate source code, HTML or embedded commands. Opening a remote source/preview is an explicit user action.

## Validation

Run `validate-packs.ps1` to validate JSON parsing, required source IDs, counts, uniqueness, catalog foreign keys, nonempty prompts, pinned provenance, local entry existence, media URL shape and SHA-256 of all byte-preserved files. This is a structural and source-integrity check, not proof of image-generation quality, model support, third-party media rights or remote availability.
