# Collection adapter contract

Keep collection tools replaceable. The method requires normalized evidence, not a specific vendor.

## Input

- directions with weights;
- language and region preferences;
- time window;
- exclusions;
- maximum candidate count.

## Output item

| Field | Required | Meaning |
|---|---:|---|
| `platform` | yes | Independent platform or editorial origin |
| `title` | yes | Headline as published |
| `semantic_title` | for mixed languages | Pivot-language event restatement; preserve entities, action, object, model/version |
| `url` | yes | Direct original URL |
| `published_at` | preferred | ISO-8601 timestamp |
| `direction` | preferred | Matched user direction |
| `summary` | no | Short factual summary |
| `rank` | no | Zero-based prominence on the source; null/malformed values fall back to unknown rank |

## Capability declaration

An adapter must state whether it supports live search, date filters, language filters, direct-page opening, and pagination. Do not silently simulate unsupported filters.

## Errors and retries

- `unavailable`: try the next adapter.
- `rate_limited`: retry once after a bounded delay, then continue.
- `malformed`: discard the item and record the count.
- `auth_required`: use another public adapter unless the user explicitly selected the private source.

## Independence rules

- Derive `platform` from editorial origin, not the feed reader or aggregator.
- Canonicalize URLs by removing fragments and tracking parameters.
- The same canonical article appearing in several feeds counts once.
- Syndicated copies with materially identical text count as one origin unless independently reported.

## Acceptance

The adapter passes when a sample yields parseable normalized items, preserves direct links, respects the time window when supported, and degrades without blocking other sources.
