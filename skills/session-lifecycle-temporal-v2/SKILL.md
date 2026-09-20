---
id: session-lifecycle-temporal
name: session-lifecycle-temporal
version: 1.1.0
description: "Run at session start. Temporal awareness from carry-forward."
owner: F13 SOVEREIGN
autonomy_tier: T1
risk_tier: low
floor_scope: [F1, F6, F13]
forged: 2026-09-20
scar_origin: Missing temporal intelligence - Arif slept 6h, Hermes had no idea
---

# session-lifecycle-temporal

## Problem
Telegram DM sessions end via session_reset (user types /new). The gateway tracks sessions in state.db with started_at/ended_at/end_reason. But carry_forward.json never gets updated so the next session has zero temporal awareness.

## Solution (zero-cron, agent-triggered)

Two scripts. No daemon. No cron. Agent runs them at session start. Arif explicitly rejected cron jobs and daemons -- anything that runs in background wastes server resources under throttle.

### Step 1: Session Closer

```bash
python3 /root/scripts/session-closer.py
```

Reads state.db for ended sessions (end_reason='session_reset'). Checks carry_forward for existing anchors (dedup). Writes session/close anchor + event entry. Backs up to /root/.hermes/experience/session-closures/. Idempotent.

Flags: --dry-run, --session ID, --limit N

**Pitfall:** sqlite3.Row objects dont have .get() -- convert to dict first. The script now returns plain dicts from queries.
**Pitfall:** Arifs chat_id is 267378578 (not 8798431893). Verify chat_id before querying.

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
   gap > 4h + crossed sleep -> hang baru bangun (dont assume continuity)
   gap > 8h -> check open loops (something may be stale)
   gap < 30m -> normal continuation
4. NEVER assume what the human was doing. Use the actual timestamps.
```

**Pitfall (SCAR):** Temporal grounding failure is a recurring bug. The agent assumed a time without checking. Always compute from actual session timestamps, never infer from conversation flow.
**Pitfall:** When carry_forward has no anchors, check if session-closer has run yet. The anchors may exist in state.db but havent been bridged. Dont conclude no session history until session-closer has been executed.

### Paths
- Session closer: /root/scripts/session-closer.py
- Temporal briefing: /root/scripts/temporal-briefing.py
- Carry forward: /root/.local/share/arifos/carry_forward.json
- Carry script: /root/scripts/carry_forward.py
- Backup: /root/.hermes/experience/session-closures/
- State DB: ~/.hermes/state.db
- Arif chat_id: 267378578

### Anti-patterns
- Cron job (wastes CPU/RAM -- Arif explicit)
- Daemon process (kills VPS under throttle)
- Reading carry_forward without session-closer first (stale data)
- Guessing time gap with date command (use actual session timestamps)
- Assuming continuity when user returns after gap (always check)