# agent-readiness-action — Scanner Endpoint

> **Default scanner:** https://isitagentready.com/api/scan

## Usage

```yaml
- uses: lingzhong/agent-readiness-action@v0.1
  with:
    url: https://example.com
    min-level: 2
```

## Inputs (canonical)

| Input | Required | Default | Purpose |
|---|---|---|---|
| `url` | yes | — | Target URL to scan |
| `min-level` | no | `2` | Fail if detected level is below this (0–5) |
| `wait-for-url` | no | `true` | Poll target until reachable before scanning |
| `wait-timeout` | no | `60` | Max seconds to wait for target |
| `wait-interval` | no | `3` | Seconds between polls |
| `scanner-endpoint` | no | `https://isitagentready.com/api/scan` | Override for self-hosted scanner |
| `scanner-retries` | no | `3` | Retries on scanner API call |
| `scanner-retry-delay` | no | `5` | Seconds between scanner retries |
| `fail-on-scanner-unavailable` | no | `false` | Hard-fail when scanner unreachable |
| `annotations` | no | `true` | Emit `::error::` / `::warning::` workflow commands |

## Outputs

| Output | Type | Meaning |
|---|---|---|
| `level` | integer or empty | Parsed level (0-5) |
| `passed` | `'true'` / `'false'` | Whether the gate passed |
| `response` | JSON string | Raw scanner response (truncated ~900 KB) |

## Failure semantics (one rule)

- Level regression → hard fail
- URL unreachable within `wait-timeout` → hard fail
- Scanner unavailable → `::warning::` + pass (default), or hard fail if `fail-on-scanner-unavailable: true`

## Self-host option

Response shape must match: `{"level": <int>, ...}`. The scanner at
`isitagentready.com` is the reference implementation.
