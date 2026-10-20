---
name: context-budget-forensics
description: "Use when auditing compaction or the prompt token budget."
version: 1.0.0
floors: [F2]
triggers:
  - "is compaction working"
  - "context too big"
  - "why is the session slow"
  - "token budget"
  - "prompt size"
  - "memory is full"
---

# Context Budget Forensics

Auditing whether an agent harness is actually folding its history, and which budget is really full. The
config states intent; only the store shows behaviour. Report numbers, never "looks fine".

## When to Use

- The principal asks whether compaction exists, why a session got slow, or what a context/token setting does.
- After a model switch, before trusting any threshold tuned on the previous model.
- Before proposing anything for history size — check which budget is actually saturating first.

## 1. Three budgets, three mechanisms — never merge them

| Budget | Mechanism when full | Evidence |
|---|---|---|
| Conversation history | **compacted** (old turns replaced by a summary) | `compression:` config + `state.db` |
| System prompt / tool schemas | rebuilt each turn, only trim-able at source | prompt builder, skills index, MCP list |
| Memory / profile files | **evicted on write**, never summarised — no summariser exists on that path | per-file character budget |

A history problem is not a memory problem. Offering to "compress memory" as part of a history fix is
wrong: that path evicts, so the fix is consolidation. Check memory saturation first — it fails instantly
on write, while history degrades gradually.

## 2. Did compaction fire — three readings

Never answer from config. Each reading fails independently:

```python
import sqlite3
con = sqlite3.connect("file:/root/.hermes/state.db?mode=ro", uri=True)   # ro: keep the write lock free

# 1. generation counter == compaction count for that lane
print(list(con.execute("SELECT source, session_key, generation FROM conversation_generations "
                       "ORDER BY generation DESC LIMIT 20")))

# 2. per-session failure columns
print(list(con.execute("""SELECT id, substr(session_key,1,40), message_count, api_call_count,
       compression_ineffective_count, compression_fallback_streak, compression_overload_streak,
       compression_failure_cooldown_until, substr(coalesce(compression_failure_error,''),1,80)
       FROM sessions ORDER BY last_activity_at DESC LIMIT 8""")))

# 3. locks
print(list(con.execute("SELECT session_id, holder, acquired_at, expires_at FROM compression_locks")))
```

| Column non-zero | Meaning |
|---|---|
| `compression_ineffective_count` | the pass ran and reclaimed nothing (incompressible tool schemas are the usual cause) |
| `compression_fallback_streak` | the summariser failed and the code fell back; read the error string for the stage |
| `compression_failure_cooldown_until` in the future | hard backoff — compaction is not even attempted until it passes |
| `compression_overload_streak` | the store or provider is rejecting the pass under load |

A long live session at generation 0 has never compacted. A long session at a high generation is working
normally — say it with the number.

## 3. A lock's TTL is the finding, not the row

A lock is only as bounded as its holder made it. Measured on a live store: sessions held with a
**365-day** expiry, every one of those sessions already closed (`end_reason` set) weeks earlier — so they
could never be compacted again, and nothing in config, health or logs said so.

- Read `expires_at - acquired_at` before assuming the lock is live. Day-scale TTLs are a design defect.
- Read the lock's **session** before deleting the lock (`SELECT end_reason FROM sessions WHERE id=?`):
  a non-null `end_reason` means the session is closed and the lock protects nothing.
- Never touch a live session's lock — that is the mutual exclusion it exists for.
- Delete only the dead rows, re-read the table, run `PRAGMA quick_check`, and report the count removed.
- `holder` names the agent. Orphaned locks mean two agents share the store, which is a coordination
  finding, not housekeeping.

## 4. The estimator is calibrated to a tokenizer generation, not to the model

Rough estimators count UTF-8 bytes ÷ 4 for non-CJK text and ~1 token per CJK codepoint. That calibration
was tuned against an older tokenizer family; newer families cost roughly 30% more tokens for identical
text. Consequences:

- A ratio threshold (`0.5` of the window) tuned on the old calibration fires **late** on a new model. The
  estimate is self-consistent, so nothing disagrees with it until the provider rejects the request size.
- After a model switch, recount a representative prompt against the actual model. Do not reuse a count
  measured on the previous one.

State the provenance of every occupancy figure: provider-reported usage outranks the local estimate; a
local estimate outranks nothing.

## 5. Window errors propagate into compaction

Compaction triggers on a fraction of a *declared* window. If that window is larger than the binding minimum
(harness config vs proxy clamp vs upstream model), the trigger is never reached: no compaction, no log
line, and the proxy truncates older turns instead. Fix the window before tuning any threshold —
compression you can read beats truncation you cannot.

## 6. Config knobs and their failure modes

| Key (`compression.*`) | Effect | Failure when wrong |
|---|---|---|
| `threshold` | fraction of the window that triggers a pass | too high → provider ceiling reached first |
| `target_ratio` | size the summary aims for | too low → the thread between turns is lost |
| `protect_last_n` | tail messages kept verbatim | too low → the active task drops out of the verbatim window |
| `tail_mode` | `lean` clamps the verbatim tail; `legacy` restores the ratio tail | `legacy` costs more context per turn |
| `max_attempts` | retry rounds before a session is declared uncompactable | schema-heavy sessions legitimately need >3 |
| `idle_compact_after_seconds` | compact on resume after N idle seconds | 0 = disabled |
| `proactive_prune_tokens` | prune oversized tool results before the main pass | 0 = disabled |
| `model_thresholds` | substring-matched per-model overrides | a stale key silently applies to the wrong model |

## 7. Pitfalls

- **The runtime-audit skill owns the window contract; this skill owns what happens after it is right.**
  When the finding is about the *declared* window, read the runtime audit first rather than tuning the
  compressor.
- **Do not quote the config the wrong process resolved.** Profiles and install environments each carry a
  copy; quote what the running service loaded, and mark it UNKNOWN if you did not check.
- **A null sensor is not a measurement.** A counter absent rather than zero is UNMEASURED.
- **Retry patterns are not findings.** One summariser call that succeeded on retry is noise; a fallback
  streak persisting across sessions is the finding.
- **Never `SELECT *` on a session or message table while auditing.** One row can hold a whole transcript
  and end the session you are diagnosing.
