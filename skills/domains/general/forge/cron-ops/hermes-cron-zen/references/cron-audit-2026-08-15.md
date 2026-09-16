# Cron Audit — 2026-08-15 Session

## Context
Arif flagged vault-data-refresh as spam (same 10 receipts every 15min, no change).
Full audit of all 21 cron jobs followed.

## Jobs removed permanently (2)
1. **vault-data-refresh** (2123bfc0a3bc) — every 15m, wrote same vault-data.json, delivered stdout to origin (spam)
2. **contradiction-scan** (8aa44381de86) — weekly LLM job, no script exists, local delivery only

## Jobs converted LLM to script-only (6)
| Old Job | New Script | Schedule | Deliver |
|---|---|---|---|
| seal-integrity-sweep (LLM) | seal_integrity_sweep.py | Sun 03:17 | local |
| artifact-drift-audit (LLM) | drift-alert.sh | daily 01:53 | local |
| syed-mak-dressing (LLM, ERROR) | syed-mak-dressing.sh | daily 08:00 | telegram:1042200555 |
| syed-gerd-log (LLM, ERROR) | syed-gerd-log.sh | daily 08:00 | telegram:1042200555 |
| syed-sambal-preorder (LLM, ERROR) | syed-sambal-preorder.sh | daily 06:30 | telegram:1042200555 |
| evening-zen-brief-v2 (LLM, ERROR) | zen/evening_zen_brief.sh | daily 20:00 | telegram:267378578 |

## Key finding: Syed delivery was NOT broken
- `curl getChat?chat_id=1042200555` returned ok: true (username: rico_ricaldo_33)
- Bot could reach Syed — error was LLM agent failure, not connectivity
- Root cause: LLM agent jobs with deliver=telegram:* fail when agent loop errors
- Fix: no_agent=True + script-only = no LLM, no agent loop, just stdout to delivery

## Scripts created
All at /root/.hermes/scripts/ (symlinked from /root/HERMES/scripts/):
- syed-mak-dressing.sh — outputs mak dressing reminder text
- syed-gerd-log.sh — outputs GERD tracker nudge text
- syed-sambal-preorder.sh — outputs sambal preorder reminder text

## Final inventory after audit
- Total: 18 jobs (was 21)
- LLM jobs: 7 (was 12, 42% cut)
- Script-only: 11

## Pending: vault-data.json stale
/var/www/html/arif/999/vault-data.json no longer updates (refresh job removed).
Needs change-detection script if public endpoint /999/vault is still live.
