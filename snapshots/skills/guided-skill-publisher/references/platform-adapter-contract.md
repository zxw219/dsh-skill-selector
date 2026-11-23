# Platform adapter contract

Use this contract when connecting the publication method to a new registry, API, CLI, or website.

## Required capabilities

An adapter must declare:

| Capability | Required evidence |
|---|---|
| Discover session | Signed-in identity or explicit unauthenticated state |
| Discover destinations | Owned workspaces, namespaces, or scopes and whether they are active |
| Read limits | Archive, expanded-size, file-count, metadata, and version rules |
| Analyze package | Authoritative pass, warnings, blockers, derived metadata, and expiry |
| Submit | Resulting locator, status, and visibility |
| Inspect submission | Current status, review note, and timestamps |
| Version lifecycle | New-version rule and withdraw/unpublish behavior |

## Adapter record

Document each implementation with:

```yaml
platform: example
verified_at: YYYY-MM-DD
official_entrypoint: https://example.invalid/publish
surfaces:
  connector: unavailable
  api: optional
  cli: optional
  browser: supported
limits:
  archive_bytes: unknown
  expanded_bytes: unknown
  metadata: unknown
analysis:
  expires_after: unknown
submission:
  review_required: unknown
  default_visibility: unknown
```

Mark unverified values as `unknown`; never invent a default.

## Error normalization

Map platform errors to one of:

- `AUTH_REQUIRED`
- `DESTINATION_REQUIRED`
- `PACKAGE_INVALID`
- `METADATA_INVALID`
- `VERSION_CONFLICT`
- `ANALYSIS_EXPIRED`
- `ANALYSIS_MISMATCH`
- `REVIEW_BLOCKED`
- `NETWORK_UNCERTAIN`
- `USER_ACTION_REQUIRED`

Preserve the original platform message beside the normalized error.

## Replacement test

Before calling an adapter complete, verify:

1. one valid package reaches analysis;
2. one invalid package stops before submission;
3. one expired or changed package requires reanalysis;
4. final submission remains separately gated;
5. a network-uncertain result is checked before retry;
6. the final receipt can be produced from platform evidence.

Changing adapters may change commands and selectors, but must not change these gates.
