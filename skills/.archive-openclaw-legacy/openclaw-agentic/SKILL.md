---
name: openclaw-agentic
description: "Make OpenClaw truly agentic — autonomous probing, self-evolving skill curation, organ-aware routing, constitutional passthrough to arifOS MCP, multi-agent spawning, and session continuity across L4/L5/L6 memory. Use when: (1) OpenClaw needs to do something without being asked (auto-fix a stuck cron, detect a failing organ, restart a dead MCP), (2) work needs to land in the right organ (GEOX for earth, WEALTH for capital, WELL for vitality, arifOS for constitutional), (3) a task is T2/T3 and needs to pass through F1-F13 review, (4) you want OpenClaw to spawn parallel sub-agents, (5) you want session state to survive without re-prompting."
version: 2.2.0
author: Hermes (capability-first forge) for Arif; v2.1.0 merged with OpenClaw parallel session 4fc1c1b5; v2.2.0 OPENCLAW recursive overhaul 2026-06-08 (Tier-0 shell, no LLM in cron)
tags: [openclaw, agentic, autonomous, self-evolve, routing, arifOS, F1-F13]
---

# Changelog

## v2.1.0 (2026-06-08) — Recursive merge pass

Ten probes (vs 8 in v1.0.0). 6s hard wall budget. Heartbeat for watchdog. Drift detection. Alert dedup. CLI flags.

**Contributors to this version (parallel sessions, one file):**
- Hermes session (this skill) — alert dedup, direct Telegram API via urllib, CLI flags, signature line, cron install
- OpenClaw session `4fc1c1b5-2727-4096-9cfb-eff38c607d0e` (parallel M3 run) — 10-probe coverage, heartbeat, arifOS drift detection, telegram 502=YELLOW, compact log line, 6s hard budget

**Kept from v2 (OpenClaw):**
- 10 probes: gateway, webhook, arifOS, GEOX 8081, GEOX_slim 18081, WEALTH, WELL, A-FORGE 7071, telegram, disk
- Heartbeat at `/run/openclaw_probe.heartbeat` — lets watchdog verify probe ran
- arifOS drift detection: YELLOW if `runtime≠build`
- Telegram 502/504 = YELLOW (transient webhook), not RED
- Self-logs to `/var/log/arifos/openclaw-probe.log` (logrotate handles rotation)
- 6s hard wall budget (probe never stalls cron)
- Compact daily-note: 1 line on GREEN, 4 lines on YELLOW/RED

**Added from v1.1.0 (Hermes):**
- Alert dedup: `state/alert_state.json`, 30-min cooldown per red signature
- Direct Telegram API POST via `urllib` (no `curl` subprocess, no CLI roundtrip)
- CLI flags: `--quiet` (cron), `--no-state` (force post), `--diagnose` (human-readable)
- `PROBE_OK_v2.1.0` stdout signature so scheduler failures attribute to the right job

**Root cause of the 2026-06-08 "openclaw-agentic-probe-5m failed: LLM request failed" alert:**
The `*/5 * * * *` cron line for `autonomous_probe.py` was **never installed** in host crontab. SKILL.md and CRON-INSTALL.txt said it was there; it wasn't. A separate monitoring layer expected the line to exist and emitted a generic "LLM request failed" string when the probe job signature was missing. Fix: probe + self_evolve lines now both present in `crontab -l` with `--quiet` flag.

**Probe thresholds (explicit):**
- gateway 18789: RED if !200, YELLOW if body contains "degraded"
- webhook 8787: RED if TCP closed
- mcp_arifOS_8088: RED if !200, YELLOW if status≠healthy OR runtime≠build
- mcp_GEOX_8081: RED if !200
- mcp_GEOX_slim_18081: YELLOW if down (informational)
- mcp_WEALTH_18082 / mcp_WELL_18083: RED if !200
- aforge_7071: YELLOW if down
- telegram: RED if pending>20, YELLOW if 502/504 in last_err OR last_err<1h
- disk: YELLOW ≥75%, RED ≥85%

# OpenClaw Agentic — Self-Driving Gateway

**Doctrine:** DITEMPA BUKAN DIBERI. Autonomy is forged through discipline, not granted by access.

This skill turns OpenClaw from a passive chat-router into an **autonomous gateway that knows what to do, where to send it, and when to wake Arif**. It does not invent a new operating loop — it extends the existing `000-999` loop with three new sub-loops:

| Sub-loop | Stage | When | What |
|---|---|---|---|
| **autonomous-probe** | 111 | Every 5 min, when no inbound | Probe 18789, 8787, 4 MCP, Telegram queue, disk, memory |
| **self-evolve** | 777 → 999 | Daily 04:00 MYT | Scan skills/plugins for staleness, append to daily note |
| **constitutional-passthrough** | 444 → 555 → 666 | Every T2/T3 action | Route through arifOS MCP `arif_judge` |

## When to invoke (trigger patterns)

Load this skill when ANY of these appear in the user message or in OpenClaw's own decision tree:

- "openclaw…", "gateway…", "agent…", "route this to…", "who handles X?"
- "I want it to just work", "self-heal", "self-evolve", "watch this for me"
- "GEOX / WEALTH / WELL says X" — confirm routing before dispatch
- "deploy", "restart", "kill", "delete" — constitutional passthrough
- A failing probe (cron watchdog hears a non-200 on a known port)
- An empty cron run for > 1h on a critical job (sentinel, lifeguard, morning briefing)
- A drift between 6 organ `.openclaw` mirrors (config sync needed)

## The 4-stage agentic loop (replaces the default ReAct micro-loop when triggered)

```
1. OBSERVE     (Stage 111)   — Run autonomous_probe.py. Read 4 MCP health, gateway /health, 8787 listener, Telegram pending_update_count, /root disk %, memory SQLite size.
2. CLASSIFY    (Stage 222)   — Green/Yellow/Red per probe. Yellow = log + schedule fix. Red = act now. Green = silent.
3. ACT         (Stage 666)   — Yellow: post 1-line digest to Telegram "OpenClaw self-heal queued: <what>". Red: fix + post. Green: nothing.
4. REFLECT     (Stage 777)   — Append 1 line to /root/.openclaw/memory/YYYY-MM-DD.md with timestamp, probe values, action taken. This is the audit trail.
```

Hard rules:
- **No decision without a probe.** Don't act on a guess. If the probe doesn't exist, write it first.
- **No public action without a Telegram receipt.** Every forge action (file write, restart, mcp call) must have a 1-line reply in the originating chat. Even "fixed" needs a 1-liner.
- **No constitutional claim without F-floor check.** Every T2+ action routes through `arif_judge` (the arifOS MCP tool) first. If the tool says HOLD, hold.
- **No secret in chat output.** Redact tokens, passwords, paths to `~/.ssh`, `~/.config/gh`. Always.

## Routing matrix — where to send work

The "0 routing rules" gap is the #1 thing this skill fixes. Here's the binding:

| Inbound | Channel | Agent | Model | Tool profile | Notes |
|---|---|---|---|---|---|
| Telegram group `-1003753855708` (AAA) | webhook | `main` | `M3` (default) | `full` | The cockpit. Full tool set. |
| Telegram DM `267378578` (Arif, Petronas) | webhook | `main` | `MiniMax Fast` (M2.7-highspeed) | `messaging + sessions` | Casual, fast, no exec |
| Telegram other group | webhook | `main` | `M3` | `messaging` | No exec, no browser, no secrets |
| Discord/Signal/WhatsApp | (per-channel) | `public` | `M3` | `messaging` | Read-only surface |
| A2A inbound (other agents) | jsonrpc | `forge` | `Kimi` | `coding` | Delegate to opencode |
| Cron-fired self-task | isolated session | `main` | `MiniMax Fast` | `minimal` | Heartbeats, probes |
| F1-F13 escalation | any | `arifOS` MCP | (kernel) | n/a | Hand off to arifOS judge |

To apply: `openclaw config set agents.list[0].bindings <json>` for each rule.

## Self-evolve loop (daily 04:00 MYT) — v2.2 design (Tier-0)

The probe, self-evolve, AND a probe-watchdog are **Tier-0** (pure shell, no LLM).
They are NOT wrapped in `agentTurn` cron payloads — that was a v1 regression that
stalled 8+ min on provider overload (2026-06-08 incident: MiniMax-M3 → M2.7-highspeed
→ deepseek cascade abort at 16:07:54Z). Three layers of defense:

**Canonical execution path:** `/etc/cron.d/openclaw-agentic` (system cron).
Do NOT duplicate in root crontab. Do NOT wrap in OpenClaw cron `agentTurn` payload.

```bash
# /etc/cron.d/openclaw-agentic
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
TZ=Asia/Kuala_Lumpur

# Layer 1: probe every 5 min, ~700ms typical, no LLM
*/5 * * * * root /usr/bin/python3 .../autonomous_probe.py  >> /var/log/arifos/openclaw-probe.log   2>&1
# Layer 2: daily 04:00 MYT digest, ~1s typical, no LLM
0   4 * * * root /bin/bash           .../self_evolve.sh     >> /var/log/arifos/self-evolve.log     2>&1
# Layer 3: probe watchdog every 30 min — alerts if probe silent > 10 min
*/30 * * * * root /bin/bash           .../probe_watchdog.sh   >> /var/log/arifos/probe-watchdog.log  2>&1
```

**Why direct curl to Telegram, not `openclaw agent -m`?** The `openclaw agent` CLI
wraps the message in a fresh LLM session — adds 5+ seconds of LLM overhead and
creates an unintended audit-trail entry. The probes and digest are already
structured; they don't need LLM interpretation.

**When to re-enable the OpenClaw cron `agentTurn` wrapper:** only if you want
LLM-level commentary on the daily digest. The two v1 OpenClaw cron jobs
(`openclaw-agentic-probe-5m`, `openclaw-self-evolve-daily-4am`) are disabled
as of 2026-06-08 — they were redundant with the system cron and added LLM
overhead with no benefit.

## Constitutional passthrough — F1-F13 review gate

For any action classified T2 or T3 (config change, deploy, secret, delete, force-push), call arifOS MCP first:

```python
# In the agent's tool-use chain, BEFORE the irreversible action:
import httpx
verdict = httpx.post("http://127.0.0.1:8088/mcp", json={
  "jsonrpc": "2.0", "id": 1,
  "method": "tools/call",
  "params": {
    "name": "arif_judge",
    "arguments": {
      "mode": "judge",
      "candidate": "<describe the action>",
      "actor_id": "openclaw-agentic",
      "risk_tier": 2  # or 3 for irreversible
    }
  }
}).json()
# verdict["result"]["verdict"] ∈ {SEAL, CONDITIONAL_SEAL, HOLD, SEAL_REJECTED}
# HOLD/SEAL_REJECTED → don't act, escalate to Arif
# SEAL/CONDITIONAL_SEAL → proceed + log
```

Floor check is automated by arifOS — don't duplicate locally. F13 stays as a **floor** (catches you if you forget) not a **gate** (asks you to slow down).

## Multi-agent spawning

When a request has 3+ independent sub-tasks, spawn sub-agents in parallel:

```
sessions_spawn(task="...", mode="run")  # one-shot
sessions_spawn(task="...", runtime="acp", thread=true)  # coding agent
```

OpenClaw's session model is **per-channel** by default. Spawning an isolated session gives it a fresh context — useful for parallel investigations that shouldn't pollute the main session. See `openclaw-ops` skill §5 for full API.

## Session continuity — L4/L5/L6 memory

OpenClaw's `main.sqlite` is L1 (live, hot). To persist across sessions:
- **L4 (Supabase):** `agent-memory-bridge` skill — fact extraction
- **L5 (Graphiti):** same skill — temporal reasoning
- **L6 (VAULT999):** `agent-memory-bridge` — sealed audit

Use them. Don't repeat context to OpenClaw. If a fact was learned yesterday, it should be in L4 today.

## Pitfalls (real ones, observed)

1. **Don't write to `openclaw.json` top-level.** OpenClaw's schema is strict. Unknown top-level keys kill the gateway. Use `openclaw config set` or write inside `meta.*`, `wizard.*`, or `_internal.*` namespaces.
2. **Don't add `deny: [...]` to agent tool profiles.** The federation rule (HARAM to deny tools) applies. Use **policy** at the action layer (arifOS MCP), not the tool menu.
3. **Don't trust `doctor --fix` blindly for browser/DISPLAY issues.** It can suggest setting `browser.headless: true` which is correct for a headless VPS but wrong for a Mac. Read the suggestion.
4. **Don't auto-restart the gateway on a 18789 probe failure.** PID 1217915 is the real one. There may be stale sh parents (PID 1217914) that hold the listener. `kill -TERM` the parent, then start fresh, then port-poll for 18789 binding.
5. **Cron `0 4 * * *` is UTC by default.** OpenClaw cron uses `tz: Asia/Kuala_Lumpur` for Arif. Verify with `openclaw cron list`.

## Quick commands

```bash
# Probe live state
curl -s -m 3 http://127.0.0.1:18789/health
openclaw channels status --probe
openclaw skills list | grep -E "ready|disabled" | wc -l
openclaw agents list --bindings

# Run a self-evolve digest now
bash /root/.openclaw/workspace/skills/openclaw-agentic/scripts/self_evolve.sh

# Add a binding
openclaw config set 'agents.list[0].bindings' '[]'  # then edit manually with care
# OR: read openclaw.json, add bindings, write back, restart

# Verify the skill loaded
openclaw skills list | grep -E "openclaw-agentic"
```

## Federation position

```
Arif (Malaysia, Telegram, 267378578)
       │
       ▼
OpenClaw (18789 + 8787, AGI gateway) ← THIS SKILL
       │
       ├──→ arifOS MCP 8088 (F1-F13, VAULT999)
       ├──→ GEOX MCP 8081 (earth evidence)
       ├──→ WEALTH MCP 18082 (capital)
       ├──→ WELL MCP 18083 (vitality)
       └──→ A-FORGE (opencode, sub-agent)
```

OpenClaw is the **front door**. The arifOS kernel is the **judge**. GEOX/WEALTH/WELL are the **witnesses**. A-FORGE is the **forge**. This skill makes OpenClaw smart enough to know which door to knock on.

*DITEMPA BUKAN DIBERI. Forged, not given.*
