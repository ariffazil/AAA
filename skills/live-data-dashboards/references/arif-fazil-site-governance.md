
# arif-fazil.com Site Governance — Deploy Gate & File Authority

> This file is reference for agents building surfaces on arif-fazil.com.
> Extracted from the SOT Atlas build session (2026-08-06) — canonical source lives in `/root/arif-fazil.com/canon/file-authority.yaml`.

## Non-negotiable rule: FAIL-CLOSED file authority

Before writing ANY file, read `canon/file-authority.yaml` and confirm:

| State | Meaning | Agent rights |
|---|---|---|
| CANON | Source of truth | Read only; mutate only with F13 lease from ARIF |
| DERIVED | Generated output | Never hand-edit |
| SCRATCH | Temporary workspace | Can create; must clean or promote |
| PROPOSAL | Human review artifact | Safe to create under `forge_work/proposals/<agent-id>/<mission>/` |
| RECEIPT | Audit output | Append-only, timestamped |
| RETIRED | Do not use | Redirect/reference only |
| UNKNOWN | No authority declared | HOLD — do not touch |

## Deploy gate (MUST pass before any deploy)

```bash
make verify-pages   # probes every dist/*/index.html against the live site; asserts HTTP 200
```

If `make verify-pages` fails → HOLD. Do not seal. Fix routing first.

### Deploy pipeline
```
make deploy = verify → sync-aaa → build → verify-pages → reload
                                                     ↑
                                               THIS GATE MUST PASS
```

If `verify-pages` fails, fix one of:
- Add a `handle` block to `/etc/caddy/Caddyfile` for the path
- Add the path prefix to `@spa_routes` in the Caddyfile
- Add the path to `public/_redirects` (Cloudflare Pages routing)
- Re-run `make verify-pages` until all pass

## Proposal zone (where new work lives before promotion)

Path: `forge_work/proposals/<agent-id>/<mission>/`

Agents create and mutate files freely here. This is the ONLY write zone without a lease.
New build output (`dist/`) goes here, not directly into `sites/.../public/`.

## Promotion pattern (from proposal to DERIVED/production)

1. Verify `dist/` matches the receipt hash.
2. `cp -r dist/* sites/arif-fazil.com/public/<path>/` (overwriting existing file)
3. `make verify-pages` — must pass before reload
4. `systemctl reload caddy` (or `make deploy`)
5. Smoke test on live URL

**Full rollback at any point:** `rm -rf forge_work/proposals/<agent>/<mission>/`

## Receipt format

Place a JSON receipt at `receipts/<agent>/<mission>-<date>.json` with:
- `receipt_id`, `agent`, `mission`, `timestamp_utc`
- `build` object (tool, duration, exit_code, errors)
- `bundle` (per-file size + gzip)
- `data_sources` (endpoint, auth, cors, smoke_test_status)
- `runtime_verification` (HTTP status, browser render, JS errors, screenshot quality)
- `limits` (canon files changed = 0 for proposals)
- `deploy_gate` status and `next_step`

## Style alignment (from the SOT Atlas build)

- Dark theme default: `#0B0B0F` background, gold `#E8B84B` accent (Trinity tokens)
- `data-ring="BODY" data-plane="narrative" data-agent-surface="content-first"` on `<html>`
- Load `/_shared/design-system/tokens.css` (CANON, referenced at runtime, not at build-time — ignore Vite's "doesn't exist" warning)
- Footer must preserve all 13 navigation links
- Footer must include `DITEMPA BUKAN DIBERI` in gold italic

## Known gotcha: shared CSS not resolvable at build time

`tokens.css` lives at `public/_shared/design-system/tokens.css` (CANON). When building
an app that references it via `<link>` or `import`, Vite will warn "doesn't exist at
build time" — this is expected. The CSS is resolved at runtime by Caddy. Do NOT try
to bundle it into the app; do NOT remove the warning. It is correct behavior.
