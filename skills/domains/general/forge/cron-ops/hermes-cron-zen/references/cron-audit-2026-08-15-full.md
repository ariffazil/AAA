# Cron Audit Trail — 2026-08-15 (Full Session)

## Context
Arif asked for a full cron audit after receiving repeated spam from vault-data-refresh.
Session covered: Hermes cron audit → zen optimization → reflection → OpenClaw audit → forge-weekly diagnosis.

## Jobs removed (from Hermes cron)
1. **vault-data-refresh** — wrote same 10 receipts every 15min, deliver=origin spammed terminal
2. **syed-mak-dressing** (LLM) — ERROR, converted to script-only
3. **syed-gerd-log** (LLM) — ERROR, converted to script-only
4. **syed-sambal-preorder** (LLM) — ERROR, converted to script-only
5. **evening-zen-brief-v2** (LLM) — ERROR, converted to script-only
6. **seal-integrity-sweep** (LLM) — converted to script-only (existing python script)
7. **contradiction-scan** (LLM) — killed, no script exists
8. **artifact-drift-audit** (LLM) — converted to script-only (existing bash script)

## Jobs added (script-only, zero token cost)
1. syed-mak-dressing — daily 08:00 → telegram:1042200555 (bash, echo text)
2. syed-gerd-log — daily 08:00 → telegram:1042200555 (bash, echo text)
3. syed-sambal-preorder — daily 06:30 → telegram:1042200555 (bash, echo text)
4. evening-zen-brief — daily 20:00 → telegram:267378578 (bash, existing script)
5. seal-integrity-sweep-script — weekly Sun 03:17 → local (python)
6. artifact-drift-audit-script — daily 01:53 → local (bash)

## Key findings

### Delivery diagnosis (Syed jobs)
Bot COULD reach Syed's chat (getChat returns ok: true, username rico_ricaldo_33).
Error was LLM agent failure, NOT delivery. Converting to no_agent=True script-only fixed it.
Test delivery before killing: curl -s "https://api.telegram.org/bot${TOKEN}/getChat?chat_id=ID"

### Token savings
LLM jobs: 12 → 7 (42% reduction). Script-only jobs: 0 → 11.
6 jobs converted from LLM to script-only.

### The no_agent=True + deliver interaction
When no_agent=True:
- Script stdout IS the delivered message
- Script should output plain text, NOT use curl (double delivery risk)
- deliver field controls where stdout goes
- First version of Syed scripts had curl IN the script + deliver=telegram — double messages. Fixed.

### Three-system duplication
- institution-mae-pulse (/etc/cron.d/) = institution-metrics-pulse (Hermes cron) — both publish metrics
- /etc/cron.d/ has 25+ entries, many infra, zero governance receipts
- OpenClaw cron system is dead (migrated files only)

### Forge-weekly false governance signal
forge-weekly.sh produced "0/7 days" for all metrics. Looked clean. Was dead — upstream
producers (steel.sh, silica.sh, intel.sh) never scheduled. Receipts directory empty.
Zero ≠ clean. Zero can mean dead pipeline.

## Architectural principle
Hermes = human edge bridge (SOUL.md contract). All infra cron should be OpenClaw.
Jobs with deliver=local + no_agent=True + infra task = candidate for migration.
