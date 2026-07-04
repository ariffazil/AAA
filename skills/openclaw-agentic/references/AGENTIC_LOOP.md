# The 4-Stage Agentic Loop

This is the canonical sub-loop for any agentic task that should not require a human
to keep prompting. It sits **inside** the existing 000-999 governance loop (specifically
in Stage 666 Forge), as a disciplined re-implementation of the ReAct micro-loop.

## Stage 1: OBSERVE (5 min, every cron tick)

Run `scripts/autonomous_probe.py`. Get a JSON snapshot of 8 probes:
1. Gateway 18789 /health
2. Webhook listener 8787
3. arifOS MCP 8088 /health
4. GEOX MCP 8081 /health
5. WEALTH MCP 18082 /health
6. WELL MCP 18083 /health
7. Telegram pending_update_count
8. /root disk %

## Stage 2: CLASSIFY (instant, no I/O)

For each probe: GREEN / YELLOW / RED.

- **GREEN** = silent. No log, no post. Probe is healthy.
- **YELLOW** = log to daily note. Schedule a fix. Don't act now.
- **RED** = act. Fix or escalate.

Hard rules:
- 1 RED + MYT business hours (07:00–23:00) → post 1-line digest to Telegram
- 1 RED + MYT quiet hours (23:00–07:00) → log to daily note, post only if RED persists 2 ticks in a row
- 2+ REDs in the same tick → escalate to Arif directly (DM, not group)
- Disk RED (≥85%) → log + post, but **don't auto-prune** — that's irreversible

## Stage 3: ACT (only for RED)

For each RED, the right action depends on the probe:

| Probe | RED action |
|---|---|
| gateway 18789 | Try `kill -TERM <pid>` on parent sh, then `openclaw gateway restart`. Poll for bind. If still down after 60s, escalate. |
| webhook 8787 | Same as gateway — usually restarts together. Check `ss -tlnp \| grep 8787` after. |
| arifOS MCP 8088 | `systemctl status arifos` (Tier 1). If dead: `sudo systemctl restart arifos.service` (Tier 1 per AGENTS.md). If still dead: HOLD. |
| GEOX/WEALTH/WELL | Same pattern — `systemctl status`, `restart`, then HOLD. |
| Telegram pending > 20 | Don't drop pending. Check `getWebhookInfo` last_error_message. If 502, restart gateway (the Caddy route is per-Caddy rules; usually a config drift). |
| Disk ≥ 85% | Find the offender (`du -sh /root/.openclaw/* \| sort -h \| tail`). Default action: log + post. **Never auto-delete.** |

After every action, re-probe in the same tick. If still RED, escalate.

## Stage 4: REFLECT (1 line, append to daily note)

Format:
```
## openclaw autonomous_probe — 2026-06-06T09:35:12Z
  - gateway_18789         GREEN  {"ok":true,"status":"live"}
  - webhook_8787          GREEN  open
  - mcp_arifOS_8088       GREEN  ...
  - mcp_GEOX_8081         GREEN  ...
  - mcp_WEALTH_18082      GREEN  ...
  - mcp_WELL_18083        GREEN  ...
  - telegram              GREEN  pending=0 last_err=ok
  - disk                  GREEN  42% on /root
  --- red=0 yellow=0
```

This is the audit trail. Every decision is named, every action is traceable. F2 TRUTH in practice.

## What this is NOT

- Not a replacement for the 000-999 loop. The 000-999 is the governance layer (constitutional). This is the operational layer (heartbeats).
- Not a license to skip human review on irreversible actions. F1 AMANAH still wins.
- Not a place to invent constitutional judgments. arifOS MCP `arif_judge_deliberate` is the only judge.
- Not a no-op during quiet hours. YELLOWs still log.

## Federation position

```
This skill (autonomous probe + self-evolve + constitutional passthrough)
       │
       ▼
OpenClaw gateway (18789)
       │
       ├──→ arifOS MCP 8088 (judge)
       ├──→ GEOX/WEALTH/WELL MCP (witness)
       └──→ A-FORGE (forge)
```

The agentic loop is the **heartbeat** of the gateway. Without it, OpenClaw is a passive router. With it, OpenClaw is a self-driving gateway that knows when to act and when to wait.
