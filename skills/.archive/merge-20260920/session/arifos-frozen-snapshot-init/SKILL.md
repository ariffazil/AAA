---
name: arifos-frozen-snapshot-init
version: 1.1.0
description: "Session init: human-first grounding, carry forward, snapshot, boot before reply."
trigger:
  - "session init"
  - "carry_forward"
  - "frozen snapshot"
  - "session start"
  - "init protocol"
  - "ur message not carry fwd"
  - "init sucks"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Frozen Snapshot Injection — Session Init Protocol

> **Principle:** The first human-facing message must be preceded by a compact state summary. The agent enters the conversation already knowing.
> **Source:** Anthropic context engineering, MindStudio frozen snapshot pattern, OpenAI context personalization cookbook.
> **Full protocol:** `/root/AAA/instructions/base.md` (Session Init Protocol section)
> **Canonical:** `/root/AAA/canon/GODEL-LOCK-V2-2026-09-20.md`, `/root/AAA/canon/FLOORS/MASTER-COMPRESSION.md`

## Step 0 — Human-First Grounding (MANDATORY, pre-tool, pre-everything)

Before ANY tool invocation, before ANY technical check:

1. **READ THE HUMAN FIRST** — what are they carrying right now?
   - What time is it for THEM? (not server time — their time)
   - What did they just send? (images, voice, text, files)
   - What mood/energy/state signal is present?
   - What was the last thing they said about themselves?
2. **THEN:** `date '+%H:%M %Z %z'` — MANDAAT TEMPORAL
3. **THEN:** carry_forward entries (top 20) — open loops
4. **THEN:** federation health — technical state

**PITFALL: Technical-first init is a bridge failure.** If you check carry_forward, health endpoints, and dirty repos BEFORE reading the human's message, you'll ground in filesystem instead of in the person. The human sent something — an image, a question, a correction. THAT is the first signal. Everything else is secondary.

If no carry_forward or last entry >24h stale: flag WITNESS_DEMAND_UNKNOWN, proceed minimally.

## Step 0b — Temporal Continuity (the human's last known state)

`carry_forward.json` (v3) tracks **federation** state — `entries[]` are decisions, scars,
open_loops, eurekas, directives. It does **not** natively carry a `human_state`, and `anchors[]`
sits empty unless something writes it. So "was the human asleep? awake? how long ago did they last
speak?" is normally **UNKNOWN at session start**, and guessing it from conversational context is
the failure you are trying to avoid.

A bridge exists. Event-driven, no background process:

```bash
python3 /root/HERMES/scripts/session-temporal-read.py          # one-line briefing
python3 /root/HERMES/scripts/session-temporal-read.py --json   # machine-readable
python3 /root/HERMES/scripts/session-temporal-seal.py --dry-run # what would be sealed
python3 /root/HERMES/scripts/session-temporal-seal.py --new-session <session_id>  # seal previous, exclude current
```

- **Seal direction** reads `~/.hermes/state.db` (READ-ONLY) and writes one
  `session/close` anchor into carry_forward via `carry_forward.py anchor`.
- **Read direction** returns: gap since last activity, session duration, MYT end time, inferred
  state, and the last human message snippet.
- Hook at `/root/HERMES/hooks/temporal-seal/` fires on `session:start`; **no cron job** — the
  human explicitly rejected background schedulers for this ("I don't want cron yang makan server").
  Event-driven only.
- Idempotent: sealed session ids are tracked in `~/.hermes/experience/temporal-seal-state.json`.
  Re-running is safe and prints `SKIP ... (already sealed)`.

**Anchor shape gotcha:** older anchors carry the session fields at the top level of `state`
(`session_id`, `ended_at`, `duration_min`, `last_user_msg`); newer ones wrap them in
`state.human_state`. Both the seal and read scripts must accept **both** shapes — if you touch
either script, keep the dual-format accept or you silently drop every previously sealed session.
Name matching must be a **prefix** test (`session/close:*`), not equality.

**state.db access pattern (gateway-safe):**
```python
sqlite3.connect("file:/root/.hermes/state.db?mode=ro", uri=True, timeout=10)
```
Tables that matter: `sessions` (`id`, `session_key`, `chat_id`, `started_at`, `ended_at`,
`last_activity_at`), `messages` (`session_id`, `role`, `content`, `timestamp`). Read-only, always.
Some shell invocations against the gateway's own state DB are blocked from inside the gateway
process — prefer a script file over a long inline command.

**PITFALL: never make a temporal claim without reading the clock.** The system-prompt date goes
stale after the first turn, and carry_forward may hold no human state at all. Before saying
morning / night / late / "tidur" / "bangun" — check: `date '+%H:%M %Z %z'`, or the temporal
briefing above. Elaborate framing built on an unverified "now" ("it's late, go to sleep") reads as
insight and lands as an insult when the human has been awake for hours. If no source can confirm
the time or the human's state, say you don't know — do not infer it from the conversation's mood.

**PITFALL: seal the most recent unsealed session, not history.** Sealing every closed session on
first run produces a wall of anchors nobody reads and dates the bridge to a backfill. Seal one
forward from now; leave the backlog.

## Step 1 — Snapshot Assembly (before first human-facing message)

Internal only, never shown to human:
```
SESSION SNAPSHOT:
- Time: [HH:MM MYT] ([Day])
- Human state: [known/unknown — from Step 0 reading]
- Open loops: [count + top 3 by urgency]
- Federation: [KVM8 status, carry_forward age, dirty count]
- Pending F13: [pending decisions]
- Last topic: [from carry_forward]
- What they just sent: [image/text/file description]
```

## Step 2 — Boot Sequence

```
source /root/.secrets/kunci-root.env
Read /root/AGENTS.md + /root/CLAUDE.md
Boot: MCP '/init' prompt (arifos-kernel)
```

## Step 3 — Federation State (parallel reads)

```
now                           # Time + surfaces + FRAME drift
Dirty repos check
Deprecation registry check
```

## Step 4 — Ready

First message: grounded in their context, not your uncertainty.

**PITFALL: Never announce your init.** Don't say "let me check" or "loading context." The human doesn't care about your bootstrap. They care about being met where they are. Check silently. Respond from knowledge.

## Pitfalls

- **Never skip step 0.** Human state MUST precede every capability invocation.
- **Never fumble.** Check silently. Don't announce "let me check."
- **Carry forward = source of truth** for open loops. Don't guess.
- **Snapshot is internal.** Don't dump it to the human.
- **Time check is mandatory** (MANDAAT TEMPORAL). Never guess the time.
- **Anti-collapse:** Never collapse unfinished work back to the human. If info + authority + capability exist, execute.
- **Technical-first = bridge failure.** Files before human = wrong order. Always.

## References

- `/root/AAA/instructions/base.md` — Full init protocol
- `/root/AAA/canon/FLOORS/MASTER-COMPRESSION.md` — 13 floors = 13 defenses of reality
- `/root/.local/share/arifos/carry_forward.json` — Carry forward (v3 schema)
