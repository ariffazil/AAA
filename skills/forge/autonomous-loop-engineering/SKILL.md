---
id: autonomous-loop-engineering
name: autonomous-loop-engineering
risk_tier: low
floor_scope: [F1, F2, F4, F7, F11, F13]
version: 1.0.0
owner: Hermes
description: "Use when building or fixing an unattended cron loop."
trigger_when:
  - building_a_loop_that_improves_itself
  - a_cron_job_applies_changes_without_a_human
  - a_job_reports_success_but_nothing_changes
  - staged_work_accumulating_unapplied
  - debugging_a_loop_that_re_runs_forever
tags: [meta, loop, cron, unattended, rsi, verification, engineering]
---

# Autonomous Loop Engineering

> For any job that observes, decides, and applies changes with no human in the loop:
> improvement loops, ingest drains, reconcilers, self-healing jobs.
> Covers the **runtime engineering** that improvement protocols assume is already
> correct — the exhale test, locking, exit codes, notification gating, baselines,
> and measurement hygiene.

---

## §0. USE WHEN

```
USE WHEN:
  1. Building a job that writes changes on a schedule, not on request
  2. A scheduled job reports success but the system does not actually change
  3. Work is staged and nothing consumes it
  4. Two runs can overlap (cron + a manual or nested invocation)
  5. A loop re-processes the same item every cycle
  6. Deciding what a scheduled job should report to a human
```

---

## §1. THE EXHALE TEST — run this first

Before building or trusting any loop, answer one question from its own ledger:
**how many changes did it APPLY in the last N runs?**

A loop that observes and proposes but never applies is not improving anything. It
produces output that reads like progress while being amnesia. Measured signature: a
ledger dominated by heartbeat records, proposals in the hundreds, applied counts at
zero.

Write the ledger record **after** the action, never before, and make a run with zero
exhale log itself as a failed run. Silence is not success — distinguish "nothing to
do" from "nothing happened" explicitly in the record.

---

## §2. BUILD ORDER

1. **Define the unit and its verdicts.** What is the smallest thing that changes
   behaviour, and what states can it end in? Name every disposition before writing
   code, so routing is a lookup rather than an improvisation.
2. **Bound the change surface first.** Hardcode the paths the loop must never write
   — governance, canon, constitutional, verifier, and the loop's own configuration —
   **inside the module**, not in a config file the loop can read. A boundary the loop
   can relax by editing a file it is allowed to read is not a boundary. Self-test it
   every run and report a leak loudly.
3. **Wire into what already exists.** Search for an existing registry, ledger, graph,
   or queue for this fact before creating one. Two sources for one fact is the exact
   defect most loops are written to detect.
4. **Add the verifier before the promoter.** Nothing is promoted until an
   independent check passes (§7).
5. **Add the lock, exit codes, and cron entry** (§3–§5).
6. **Capture baselines** at promotion time (§8), then measure consequence.

---

## §3. SINGLE-WRITER LOCK

Any read-modify-write over shared state needs a lock the moment two invocations can
overlap: cron plus a manual run, or a parent plus a nested call.

- exclusive advisory lock (`fcntl.flock` / `flock`)
- **non-blocking** — a blocked cron is worse than a skipped one
- **reentrant within one process**, so the orchestrator can hold it across modules
  without deadlocking itself
- fail fast for a second *process*, with a distinct exit code (§4)
- add the lock module to the loop's own forbidden-paths list

**Verify by racing it, not by reading it.** Start two cycles a fraction of a second
apart and assert the exit codes are `{0, 4}`. A lock you have only read is a lock you
have not tested.

Why it matters more than it looks: if the derived state includes a measurement the
whole loop's verdict rests on, a concurrent writer silently moves that measurement
from a stale read and the result becomes invalid **with no error raised**.

---

## §4. EXIT CODES FOR TRIAGE

| Code | Meaning |
|---|---|
| `0` | acted, OR steady state (nothing new to do) |
| `3` | items verified but none reached application — a genuine miss |
| `4` | another cycle holds the lock — a SKIP, not a failure |

Do not let a correctly-refused item count as a miss. Define the **accepted
disposition set** explicitly: verification-failed, quarantined, proposed-up-only,
boundary-held, budget-deferred. When every novel item landed in that set the run is
healthy and must return `0`. If a lock skip reuses the miss code, a healthy steady
state reads as broken.

---

## §5. CRON ENTRY

- one invocation per cadence, output appended to a log with a bounded tail-trim so
  the log cannot grow without limit
- a separate low-frequency job that runs only the boundary self-test, so the guard
  is proven on cycles with nothing to do
- cadence above the cadence of the signal it governs and below the one it must not
  alias: sampling slower than twice the phenomenon folds it into noise
- header comment carries the rollback: how to remove the job, what to restore

---

## §6. NOTIFY ON SUBSTANCE, NOT ON RUN TEXT

A delta gate that hashes the whole message body treats volatile counters as new
events, so identical runs re-post. Symptom: the same run type lands several times in
minutes.

- build the dedup key from the **set** of what changed (which items were promoted,
  held, or changed verdict), sorted and hashed — not from the message text
- keep volatile counts out of the body
- write the dedup marker only **after** the delivery command reports success, so a
  failed send retries next cycle instead of being swallowed
- a human-facing group is an execution ledger, not a feed: silence when nothing
  changed is correct output

Verify by running the same cycle twice and asserting the sends are `1, 0` with the
underlying event count rising by exactly one.

---

## §7. INDEPENDENCE IS ORGANIZATIONAL, NOT A WIRING GAP

The most common false fix: "route the check through a different component." A
different **tool** is not a different **witness**; a second name written by the same
hand is still one author.

Before claiming a verdict is independent, establish:

1. Which actor produced the claim, and which produced the check — resolve both
   through the live actor registry, not from the name strings.
2. Whether the checking path can even accept a foreign claim. Some components verify
   only their own internal state and cannot be handed an item.
3. Whether an unregistered actor degrades to observe-only and is therefore denied
   before it can judge.

Report the class, in increasing strength: `SELF` (same actor) → rejected ·
`NOMINAL` (different names, same author) → **provisional**: record the item, do not
record a pass, do not propose a rule · `STRUCTURAL` (distinct authors) → may record a
pass · `EXTERNAL_ORGAN` (a separate agent or durable external receipt) → may also
back a policy claim.

Provisional is a correct output, not a defect to paper over — and do not go looking
for a smarter tool. The fix is a different agent.

---

## §8. BASELINES AND CONSEQUENCE

An applied change is only proven if the recurrence of the thing it governs falls
afterwards.

- capture the baseline at promotion time, keyed by the item, **first promotion only**
  — re-baselining on every run lets the system move its own goalposts
- a backfilled baseline is marked `backfilled`, its window starting at the backfill;
  it may never claim a full-window verdict for time predating the instrument
- verdicts only after a full observation window: `PERSISTED` (recurrence fell ≥50%) ·
  `PARTIAL` (fell <50%) · `NO_EFFECT` (unchanged ±10%) · `REGRESSED` (rose) ·
  `PENDING` (window not elapsed)
- report `PENDING` as **"not yet observable"** — never as success

---

## §9. MEASUREMENT HYGIENE

- **Separate occurrence counts from verification events.** Folding raw recurrence
  into the denominator of a fitness score makes every item look like it is failing.
  Keep how-often-seen and how-often-judged as distinct fields.
- **State which root you measured.** A count taken on one tree and reported against
  another is a wrong answer that looks right. Name the path in the finding.
- **Prefer an error to a zero.** A read that silently returns empty is
  indistinguishable from a read that reports zero. Label unreadable reads
  `UNREADABLE` rather than `None`, and treat rate-limiting on your own verification
  traffic as a retry condition, not a result.
- **Frequency is a measured count, never an adjective.** "12 occurrences" must come
  from counting sources; a heartbeat record is not a diagnosis.
- **Prove fixes before/after.** Record the value before, the value after, and the
  command that produced each. "Should work now" is not evidence.
- **Output from an earlier run is not current state.** Nested or backgrounded runs
  keep landing after you move on and their stdout reads like the present. Before
  reading any captured output, check state freshness — mtime of the state file, `ts`
  of the last record — and re-run once per fix rather than spraying runs.

---

## §10. ANTI-PATTERNS

```
❌ Ledger record written before the action   → a crashed run reads as complete.
❌ Boundary list in a config the loop reads  → the loop relaxes its own guard.
❌ Second store for a fact that exists       → duplicate source of truth.
❌ Rejected item left in the scan path       → re-checked forever; dead-letter it.
❌ Lock skip sharing the miss exit code      → healthy steady state reads as broken.
❌ Dedup keyed on message text               → volatile counters re-post the group.
❌ Dedup marker written before delivery      → a failed send is never retried.
❌ Re-baselining every run                   → the system moves its own goalposts.
❌ Occurrences folded into the fitness denom → everything looks like it is failing.
❌ "Independent" by name only                → same author, same blind spots.
❌ Reporting PENDING as success              → unfalsifiable and self-congratulatory.
```

---

## §11. REFERENCE

- `references/autonomous-loop-runtime.md` — concrete lock implementation, cron entry
  shape, notification gate wiring, baseline schema, ledger record shape, and the
  race / double-run tests used to verify each of them.

---

*DITEMPA BUKAN DIBERI*
