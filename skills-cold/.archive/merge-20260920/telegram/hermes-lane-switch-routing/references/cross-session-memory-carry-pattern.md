# Cross-session memory carry — the pattern, generalised (2026-08-13)

The root cause behind "agent can't read back what was said earlier" is almost
never the observe pipeline. It is **session isolation**: sessions are per-chat
and split by idle gaps, so a fresh session starts from an empty thread. Two
agents in this federation hit the same wall:

- **Hermes lane_switch** — SADO group had 4+ sessions split by time gaps;
  Hooligan V6 exchange from an older session was invisible in the current one.
- **OpenClaw memory-core dreaming** — the 3am dreaming cron fires but REM/deep
  output says "No strong patterns surfaced" / "Promoted 0 candidate(s)" day
  after day. The infrastructure is configured but **starved of input**: no
  extract-signal→dreaming pipeline feeds candidate material in before the dream
  pass runs. "RAM kosong" — ceremony over an empty buffer.

## The fix pattern (both cases)

Don't fuse sessions (DB surgery, migration risk). **Carry recent context across
the session boundary** instead:

1. A persistent store already accumulates exchanges/notes (Hermes: lane MEMORY
   file via `post_llm_call`; OpenClaw: `memory/` + MEMORY.md).
2. On every turn (not just first turn), read the tail of that store and inject
   it as a "recent history" context block.
3. Graceful-degrade: if nothing is there, return "" and carry on.

## Why the "advisory" capability map is not enough

A prompt-text capability map ("you may SEARCH but not FORGE") is a suggestion
the model can ignore. Real enforcement needs a hard gate at the tool-call
boundary. On Hermes the adapter exposes a `pre_tool_call` hook whose return
`{"action": "block", "message": "..."}` aborts the call — the same pattern the
bundled `security-guidance` plugin uses. Wire it as:

- `pre_llm_call` records `session:<id> → lane` into the runtime state.
- `pre_tool_call` resolves the active lane from the session, and if the lane is
  group-scoped (no FULL capability), hard-blocks execution-class tools
  (`forge_*`, `aforge_*`, `mcp__aforge__*`, `delegate_task`, `cronjob`,
  `arif_forge/seal/init`). Intelligence tools (web_search, web_extract,
  session_search, memory, vision) pass.

Verified 12/12 on Hermes: BLOCK forge/delegate/cron/arif_forge for the scoped
`arif-sado` lane; ALLOW web tools; ALLOW FULL (arif DM) and WARGA lanes.

## Reusable diagnostic for any agent's memory

```bash
# "Is the memory machinery actually producing, or just configured?"
# 1. Find the memory store
ls -la <agent-home>/memory* 2>/dev/null
# 2. Check the most recent transformation output (dreaming/compile/consolidate)
cat <agent-home>/memory/dreaming/deep/$(date +%F).md 2>/dev/null
# If it says "0 candidates" / "no patterns" repeatedly → the feeder is missing,
# not the cron. Fix the extract→store pipeline, not the scheduled job.
```

## Improvement checklist OpenClaw (if Arif asks)

1. Extract-signal→dreaming pipeline (highest value — dreaming is starved).
2. Cross-session recent-context carry (same as Hermes Fix 1).
3. Wire OpenClaw scars ↔ A-FORGE SCAR LAW (two scar systems not talking).
4. Proprioception pattern register (largest, defer — new class).

#1 + #2 are T1-reversible and touch nothing already working.