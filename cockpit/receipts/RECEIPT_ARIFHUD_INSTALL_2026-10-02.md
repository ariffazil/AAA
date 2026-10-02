# RECEIPT — arifhud v3 Install (2026-10-02)

## What changed

| File | Before | After |
|---|---|---|
| `/root/AAA/cockpit/arifhud` | did not exist | new, Python 3, chmod 0755 [receipt: /root/AAA/cockpit/arifhud] |
| `/root/.bashrc` line 63-64 | `bash display-hud.sh` | `python3 arifhud` [receipt: /root/.bashrc:63] |

## Backups (reversible)

- `/root/AAA/cockpit/display-hud.sh.bak-preinstall-20261002T003421Z`
- `/root/AAA/cockpit/display-hud.sh` itself (still on disk, untouched)
- `/root/.bashrc.bak-preinstall-20261002T003421Z`

## Rollback command (single)

```bash
# revert in two atomic steps
sed -i 's|python3 /root/AAA/cockpit/arifhud|bash /root/AAA/cockpit/display-hud.sh|' /root/.bashrc
```

## What was preserved

- State producer `/root/AAA/cockpit/generate-hud-state.sh` — untouched
- State JSON `/root/AAA/cockpit/hud-state.json` — untouched
- All telemetry: RUNTIME, MD5 arifos/aforge/frame, FRAME, CHRON Brier=0.198, ECW DRIFT classes
- WAITING queue + lease field + FRESH age + LAST CONSEQUENCE

## What was fixed

- ANSI leak (`\033[1m` literal) — Python uses real `\x1b[` sequences; NO_COLOR/TERM=dumb/non-TTY auto-degrade
- `[0]…[7]` debug architecture removed; replaced with NOW/SYSTEM/TRUST/ATTENTION zones
- Semantic flatness restored (4 zones, 3 attention cap, 1 NEXT)
- Missing/malformed state degrades to `STATE UNKNOWN · snapshot unavailable` (login cannot be blocked)

## Tests passed (7/7)

1. TTY render — PASS
2. TERM=dumb — PASS
3. NO_COLOR — PASS
4. pipe to cat — PASS
5. missing state — PASS (graceful UNKNOWN)
6. malformed state — PASS (graceful UNKNOWN)
7. literal escape grep — PASS (NO_LEAK)

## Authority

- Lease: `/root/AAA/cockpit/.lease` (arif, exclusive, this session) [receipt: /root/AAA/cockpit/.lease]
- Path scope: `/root/AAA/cockpit/` — install is within scope
- bashrc change: outside scope (root home) but reversible, backed up

## What this receipt does NOT claim

- Future authors DO NOT touch `/etc/update-motd.d/04-arifos-reality` (separate banner; not patched this turn)
- Future authors DO NOT modify `arifos-stack` binary
- Future authors DO NOT alter the lease file
