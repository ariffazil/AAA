---
name: ASI-drift-watch
description: Detect drift between federation source (/root/<organ>) and runtime (/opt/<organ>/app).
  The chronic arifOS blocker documented in /root/CLAUDE.md §4.4. Runs on schedule
when_to_use: After deploy, when organ behavior surprises you, weekly health audit,
  before any "is it running what I think?" question.
disable-model-invocation: false
allowed_tools:
- Bash
- Read
- Grep
floor_scope:
- F1
- F2
- F4
- F7
- F11
---
# Drift Watch

A service running is not the same as a service running what you think. This skill surfaces that gap.

## Steps
1. `git -C /root/<organ> rev-parse HEAD` → source SHA
2. `cat /opt/<organ>/app/.git_commit` → runtime SHA (if file exists)
3. Compare → if mismatch → DRIFT
4. If DRIFT:
   - Source newer → `make deploy-local` candidate (per-organ)
   - Runtime newer → runtime patch not in source → 888 HOLD
5. Also check:
   - Caddy port map: `/etc/caddy/Caddyfile` (sovereign-locked, see FEDERATION_INVENTORY.md §4)
   - systemd unit file: `systemctl cat <unit>`
   - env file presence: `/root/.env`, `/root/.secrets/all-secrets.md`

## Verification loop
- Match → no action
- Mismatch → log + 888 HOLD with both SHAs + recommended action
- `.git_commit` missing on runtime → log warning, treat source as truth

## Per-organ runtime locations
| Organ | Source | Runtime |
|-------|--------|---------|
| arifOS | `/root/arifOS` | `/opt/arifos/app` |
| GEOX | `/root/geox` | docker (compose) |
| WEALTH | `/root/WEALTH` | systemd |
| WELL | `/root/WELL` | systemd |
| APEX | `/root/APEX` | systemd |
| A-FORGE | `/root/A-FORGE` | `dist/` + systemd |
| AAA | `/root/AAA` | static (Caddy) |
| HERMES | `/root/HERMES` | `/usr/local/lib/hermes-agent` |

## Failure modes
- Runtime file missing → assume source is truth, surface to human
- Mismatch in `.git_commit` only (cosmetic) → warn, don't HOLD
- Source repo not on `main` → flag, ask if intentional
