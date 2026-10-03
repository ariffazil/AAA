---
id: session-lifecycle-temporal
name: session-lifecycle-temporal
version: 1.0.0
description: "Run at session start. Temporal awareness from carry-forward."
owner: F13 SOVEREIGN
autonomy_tier: T1
risk_tier: low
floor_scope: [F1, F6, F13]
forged: 2026-09-20
scar_origin: Missing temporal intelligence - Arif slept 6h, Hermes had no idea
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# session-lifecycle-temporal

## Problem
Telegram DM sessions end via session_reset (user types /new). The gateway tracks sessions in state.db with started_at/ended_at/end_reason. But carry_forward.json never gets updated so the next session has zero temporal awareness.

## Solution (zero-cron, agent-triggered)

Two scripts. No daemon. Agent runs them at session start.

### Step 1: Session Closer

```bash
python3 /root/scripts/session-closer.py
```

Reads state.db for ended sessions. Checks carry_forward for existing anchors (dedup). Writes session/close anchor + event entry. Backs up to /root/.hermes/experience/session-closures/. Idempotent.

Flags: --dry-run, --session ID, --limit N

### Step 2: Temporal Briefing

```bash
python3 /root/scripts/temporal-briefing.py          # full
python3 /root/scripts/temporal-briefing.py --compact  # one-liner
python3 /root/scripts/temporal-briefing.py --json     # machine
```

Computes: time gap, sleep boundary, meal boundary, open loops, unread events, last user message.

### Session Start Protocol

```
1. python3 /root/scripts/session-closer.py
2. python3 /root/scripts/temporal-briefing.py --compact
3. Ground response in briefing:
   gap > 4h + crossed sleep -> hang baru bangun
   gap > 8h -> check open loops
   gap < 30m -> normal continuation
```

### Paths
- Session closer: /root/scripts/session-closer.py
- Temporal briefing: /root/scripts/temporal-briefing.py
- Carry forward: /root/.local/share/arifos/carry_forward.json
- Carry script: /root/scripts/carry_forward.py
- Backup: /root/.hermes/experience/session-closures/
- State DB: ~/.hermes/state.db
- Arif chat_id: 267378578

### Anti-patterns
- Cron job (wastes CPU/RAM)
- Daemon process (kills VPS)
- Reading carry_forward without session-closer first
- Guessing time gap with date command