# Receipt — OpenClaw RSI Verification

**Sovereign:** Muhammad Arif bin Fazil (F13)
**Agent:** FORGE (000Ω)
**Time:** 2026-06-16T17:15:00+08:00
**Authority:** T1 verification of Hermes-RSI-Auditor findings. No config changes, no restarts.
**Verdict:** 5/7 CONFIRMED, 2/7 INCORRECT

## Verified Findings

| RSI ID | Finding | My Verification | Status |
|--------|---------|-----------------|--------|
| RSI-001 | /health is 23 chars | `{"ok":true,"status":"live"}` — 30 chars, still minimal vs arifOS 4KB | CONFIRMED |
| RSI-002 | Duplicate mimo in fallback | Primary `mimo-v2.5-pro` + fallback[1] `mimo-v2.5-pro` | CONFIRMED |
| RSI-003 | Kimi 401 on every probe | Returns 404 (endpoint doesn't exist, worse than 401) | CONFIRMED |
| RSI-006 | /v1/models returns HTML | `<!doctype html>` — not JSON | CONFIRMED |
| RSI-007 | Kimi alias + 401 | `kimi/kimi-for-coding` alias "Kimi" in fallback, returning 404 | CONFIRMED |

## Incorrect Findings

| RSI ID | Finding | My Verification | Status |
|--------|---------|-----------------|--------|
| RSI-004 | OpenClaw NOT a systemd unit | `openclaw-gateway.service` is active, running 1 day 2h | INCORRECT |
| RSI-005 | VAULT999 has 104 entries | Only 24 SEAL files in /root/VAULT999/ | INCORRECT (count wrong) |

## Critical Finding: Model-Default Drift

Four files disagree on the default model:

| Source | Default Model |
|--------|---------------|
| OpenClaw openclaw.json | `xiaomi-coding/mimo-v2.5-pro` |
| Federation registry | `deepseek` |
| arifOS /health | `sea_lion` |
| OpenCode config | `tokenplan-mimo/mimo-v2.5-pro` |

F2 TRUTH gap is critical. Same model, different names. Different providers, same name.

## Zone A Actions (operator required)

1. **Remove duplicate mimo** from OpenClaw fallback chain (position 1 = primary, position 3 = duplicate)
2. **Remove or fix Kimi** from fallback chain (returning 404, not 401)
3. **Enhance /health** with structured fields (operator code change)

## Zone C Actions (888 HOLD)

1. **Install openclaw-gateway.service** — RSI-004 was wrong, service exists and is running. No action needed.
2. **Add /v1/models JSON endpoint** — currently returns HTML
3. **Rotate or remove Kimi key** — returning 404 on all probes

## Evidence

- `curl http://localhost:18789/health` → `{"ok":true,"status":"live"}`
- `curl http://localhost:18789/v1/models` → `<!doctype html>`
- `systemctl status openclaw-gateway.service` → active (running)
- `/root/.openclaw/openclaw.json` → fallback chain with duplicate mimo

DITEMPA BUKAN DIBERI.
