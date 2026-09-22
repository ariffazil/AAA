---
id: temporal-intelligence
name: temporal-intelligence
description: "Seal and read human temporal state across sessions."
version: 1.0.0
owner: curator
risk_tier: low
floor_scope: [F1, F2, F4]
autonomy_tier: T1
forged: 2026-09-20
forged_by: "hermes (F13 directive: solve carry_forward blind spot for Telegram DM sessions)"
trigger_when:
  - "session starts or /new typed"
  - "making time-based claims about the human (tidur, pagi, malam)"
  - "carry_forward.json has no human state"
  - "temporal awareness needed"
  - "when did the human last sleep/wake"
tags: [temporal, carry-forward, session, telegram, human-state, chron]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Temporal Intelligence Bridge

## Why this skill exists

When Telegram DM sessions end (user closes app, types /new, or goes idle), carry_forward.json
gets NO human temporal state. Next session starts blind — agent doesn't know when the human
last slept, woke up, or was active. This leads to temporal grounding failures (e.g., saying
"tidur" when it's afternoon).

## Architecture

Two scripts, event-driven, zero background overhead:

### Seal direction: `/root/HERMES/scripts/session-temporal-seal.py`
- Reads state.db (read-only) for Arif's DM sessions (chat_id 1042200555)
- Extracts: last message timestamp, message count, duration, snippet
- Writes ONE anchor to carry_forward.json via `carry_forward.py anchor`
- Idempotent: tracks sealed session_ids in `/root/.hermes/experience/temporal-seal-state.json`
- Handles BOTH anchor formats: direct (`state.session_id`) and wrapped (`state.human_state.session_id`)

**When it runs:**
1. On `session:start` hook (fires from `/root/HERMES/hooks/temporal-seal/handler.py`)
2. Manually: `python3 /root/HERMES/scripts/session-temporal-seal.py`
3. On session start of NEXT session (seals the previous one)

**Flags:**
- `--new-session <id>` — seal previous, exclude current session
- `--session <id>` — seal specific session
- `--briefing` — print temporal briefing only, no seal
- `--idle-detect` — seal active sessions idle >30min
- `--dry-run` — show what would be sealed

### Read direction: `/root/HERMES/scripts/session-temporal-read.py`
- Reads carry_forward.json, finds most recent session/close anchor
- Outputs one-line temporal briefing
- Handles both direct and wrapped anchor formats

**When it runs:**
1. At session init (30-second checklist)
2. Manually: `python3 /root/HERMES/scripts/session-temporal-read.py`

**Output formats:**
- Default: `[temporal] Last session: 3h ago (2h15m) ended 11:48 PM MYT, was active. Last: "..."`
- JSON: `--json` flag

## Pitfalls


- **Schema mismatch between seal and read scripts.** The seal script writes session data
  directly (session_id, ended_at, duration_min at top level). The read script must accept
  BOTH this direct format AND the wrapped format (inside `human_state` key). Always test
  both formats when modifying either script.

- **Idempotency: check BOTH anchor formats.** Old anchors use direct format (session_id at
  top level). New anchors use wrapped format (inside human_state). The `read_cf_anchors()`
  function in the seal script must extract session_ids from BOTH locations to prevent
  duplicate seals.

- **Don't assume the most recent anchor is the CURRENT session.** carry_forward.json accumulates
  anchors over time. The read script uses `reversed()` to find the latest, but an old anchor
  with wrapped format may appear AFTER newer direct-format anchors. Always check `ended_at`
  timestamp, not just array position.

- **state.db access from inside gateway process is BLOCKED.** SQLite read-only connections
  via `?mode=ro` work, but direct `sqlite3.connect()` from within the gateway process gets
  SIGTERM. Always use: `sqlite3.connect("file:/root/.hermes/state.db?mode=ro", uri=True, timeout=5)`

- **Carry forward is NOT populated automatically.** The `carry_forward.py` script only writes
  when explicitly called. Telegram DM sessions do NOT trigger session/close anchors by
  default. The temporal-seal hook fills this gap.

## Hook integration

`/root/HERMES/hooks/temporal-seal/` — fires on `session:start` event.
- HOOK.yaml declares event type
- handler.py calls seal script with `--new-session <current_session_id>`
- Only fires for Arif's DM (chat_id 1042200555)
- Fail-soft: errors logged, never block pipeline

## Verification

```bash
# Test seal (dry run)
python3 /root/HERMES/scripts/session-temporal-seal.py --dry-run

# Test read
python3 /root/HERMES/scripts/session-temporal-read.py
python3 /root/HERMES/scripts/session-temporal-read.py --json

# Check anchors
python3 /root/scripts/carry_forward.py show --anchors

# Check seal state
cat /root/.hermes/experience/temporal-seal-state.json
```

## Connection to carry_forward

This skill extends the carry_forward system (schema v3) with human temporal state.
carry_forward.py itself is NOT modified — the seal script uses it as a CLI tool.
Anchor name: `session/close:<session_id>` with state containing session metadata.