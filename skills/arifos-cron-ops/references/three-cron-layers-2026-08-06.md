---
title: "Three Cron Layers — OpenClaw (machine) + Hermes (human) + Legacy (arifOS)"
date: 2026-08-06
session: OpenClaw Chron Audit (post-morning revamp)
---

# TL;DR — The cron stack has THREE independent surfaces

A sibling agent (or even you, tomorrow) reading `arifos-cron-ops` SKILL.md will see "two registries." That was true at 03:00 UTC. By 04:14 UTC the same day, an audit revealed **OpenClaw runs its own scheduler via `openclaw-gateway.service`, independently of Hermes.** The two-registry model is now outdated — patching in this doc supersedes that section of SKILL.md.

# The three layers

| Layer | Path / command | Scheduler | Audience | Job count | Delivery target |
|---|---|---|---|---|---|
| **OpenClaw cron** | `openclaw cron list` (state in `/root/.openclaw/`) | `openclaw-gateway.service` :18789 | MACHINE — federation infra | 7 (5 OK, 2 in error) | `-1003753855708` (AAA group) |
| **Hermes gateway cron** | `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json` | `hermes gateway run` (cronjob tool) | HUMAN — blueprints | 5 (Arif-facing) | `telegram:267378578` (user DM) |
| **Legacy arifOS cron** | `/root/HERMES/cron/jobs.json` | UNKNOWN — `lsof +D` returns nothing; ticker_heartbeat updates within seconds | LEGACY — converged to 5 (same as gateway) | 5 | `telegram:267378578` |

# Critical count-drift observation (verified live)

The legacy registry went from **20 jobs at 03:28 UTC → 5 jobs at 03:55 UTC** the same day. The morning revamp session converged both gateway and legacy registries to the same 5 blueprints. **Both registries now hold identical job sets** → double-fire risk for the same blueprint (each fires from a different scheduler).

# Three-layer audit recipe (re-runnable)

```bash
# 1. OpenClaw layer — JSON, parse with python
openclaw cron list --json 2>/dev/null | python3 -c "
import json,sys
d = json.load(sys.stdin)
jobs = d.get('jobs', [])
for j in jobs:
    print(f'{j[\"id\"][:12]} | {j[\"name\"][:45]} | {j.get(\"schedule\",{}).get(\"expr\",\"?\")} | {j[\"status\"]} | to={j.get(\"delivery\",{}).get(\"to\",\"none\")}')"

# 2. Gateway layer
python3 -c "
import json
d = json.load(open('/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json'))
for j in d.get('jobs', []):
    print(f'{j[\"name\"]} | {j.get(\"schedule\",{}).get(\"expr\",\"?\")} | status={j.get(\"last_status\")} | deliv={j.get(\"deliver\")}')"

# 3. Legacy layer
python3 -c "
import json
d = json.load(open('/root/HERMES/cron/jobs.json'))
for j in d.get('jobs', []):
    print(f'{j[\"name\"]} | {j.get(\"schedule_display\")} | status={j.get(\"last_status\")} | deliv={j.get(\"deliver\")}')"

# 4. Ticker liveness (legacy)
stat -c '%y' /root/HERMES/cron/ticker_heartbeat
```

# OpenClaw cron jobs (full inventory, 2026-08-06 04:14 UTC)

| ID | Name | Schedule | Status | Error |
|---|---|---|---|---|
| 82bf65b3 | AF-FORGE Infrastructure Sentinel | `0 */6 * * *` UTC | error | `cron: job execution timed out (last phase: model-call-started)` — model call >180s |
| 7f7fcede | Federation Auto-Remediation 6h | `0 */6 * * *` UTC | ok | none |
| 3705ad6c | WELL freshness 12h | `0 */12 * * *` MYT | ok | none |
| d55b6a8a | Memory Dreaming Promotion | `0 3 * * *` MYT | ok | none |
| 097cc65c | JWT-violations-monitor-enforce | every 1d | ok | none |
| 6ecd2838 | MCP Lifeguard Probe | `0 9 * * *` MYT | ok | none |
| a4301644 | FORGE ⟁ Weekly Governance Roll-up | `0 19 * * 6` MYT | error | model `minimax/deepseek-v4-flash` rejected by allowlist — wrong provider prefix |

# Two error patterns observed

## A. Timeout (>180s) — AF-FORGE Infrastructure Sentinel
- `last phase: model-call-started` = the model's API call hung
- OpenClaw default cron timeout = 180s
- Fix: pin to a fast model OR shorten the prompt to fit <180s
- Suggested models from allowlist: `minimax/MiniMax-M3`, `groq/llama-3.1-8b-instant`

## B. Provider-prefix rejection — FORGE Weekly Governance
- Job model: `minimax/deepseek-v4-flash`
- Allowlist accepts only: `deepseek/deepseek-v4-flash` (no `minimax/` prefix)
- Sibling agents often add a `minimax/` prefix when migrating models → silently rejected at cron-preflight
- Fix: `openclaw cron edit <id> --model deepseek/deepseek-v4-flash`

# Telegram delivery pipeline — 1,182 errors / 24h

**The 1,182 "Forbidden: the bot can't send messages to the bot" errors** in `/usr/local/lib/hermes-agent/profiles/aaa-hermes/logs/gateway.log` are NOT cron-job failures. They're the gateway adapter sending a reply back to chat_id=8410138119 (the bot's own id) instead of the user's id. This breaks every outbound Telegram delivery.

- Source file: `/usr/local/lib/hermes-agent/plugins/platforms/telegram/adapter.py`
- The fix is to resolve outbound `chat_id` from the session's user_id, not from the inbound chat_id (which on a DM equals the bot id)
- Test: `curl ... /sendMessage -d chat_id=267378578` succeeds → user DM ok; same call to 8410138119 → Forbidden

# Verifications to apply after any change

1. **OpenClaw error fix**: `openclaw cron runs --id <job_id> --limit 1` — last entry should show `status: ok`
2. **Gateway delivery**: `grep "Forbidden" /usr/local/lib/hermes-agent/profiles/aaa-hermes/logs/gateway.log | wc -l` — should decrease after the adapter patch
3. **Legacy ticker**: `stat -c '%y' /root/HERMES/cron/ticker_heartbeat` — should be <60s old

# References

- `arifos-cron-ops/references/dual-registry-2026-08-06.md` — original two-registry doc (now superseded)
- `openclaw-ops/SKILL.md` — OpenClaw CLI surface
- `hermes-telegram-gateway-ops/SKILL.md` — Telegram identity / token / drop-in ops
- `telegram-gateway-group-debug/SKILL.md` — chat_id resolver + free_response_chats debugging