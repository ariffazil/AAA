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

### A cycle record carries delta AND state

Logging only what this run changed makes a healthy quiet cycle indistinguishable
from a broken one: **both write zeros.** An observer who did not run the job cannot
tell "nothing was due" from "every step failed silently".

Every cycle record carries four things:

- `delta` — what this run changed
- `state` — what is true now (a post-run snapshot of the store)
- `errors` — the failed steps, named, each with its message
- `status` — three-way: `ACTIVE` (something changed) / `QUIET` (nothing due, no
  errors, and `state` shows the store populated) / `DEGRADED` (a step failed)

Collapsing those three into a boolean is what lets an organ report "all zeros" for
weeks while holding live data.

Corollary — never wrap a loop step in `except: pass`. That is how `DEGRADED`
becomes indistinguishable from `QUIET`. Capture the exception as data, keep the
other steps running, and put the failure in the record.

Corollary — a `dry_run` flag must reach every mutating step. One step that ignores
it means a "dry" cycle still writes. Prove it by hashing every store file around a
dry pass, never by reading the flag.

Corollary — extraction jobs that append every cycle duplicate their own output.
Fingerprint the artefact by its defining fields (not its timestamp) and skip ones
already held, or N cycles produce N copies and inflate every downstream count.

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
- **deliver to `origin`, not to a hardcoded chat id.** `origin` resolves at fire time and follows
  the session; a hardcoded numeric id is a routing claim that is routinely wrong (a bot's own DM id
  and a human's user id are different numbers) and it cannot follow a chat that moves. Use an
explicit id only for a channel the creating session is not in.
- **confirm every skill the job names actually resolves**, with `skill_view(name=...)` rather than a
  filesystem search. A cited skill that does not resolve fails silently: the run starts, the skill is
  absent, and the agent improvises a procedure it believes it loaded. A job created in the same
  session as its own skill is the exact case that breaks, and it breaks at the first unattended fire.
- **check the other producers before you retire this one.** A loop is frequently the *second* producer
  of an artifact, and the first lives in another session's job store. Two jobs, same schedule, same
  artifact, same human is one defect — but retiring both is a worse one.

### Zero-slack cadence — a phase window must never equal the period

A state machine that advances by **elapsed wall-clock time**, driven by a job on that same period,
has no margin at all. When window width equals the interval every run lands on the boundary and the
arithmetic decides the phase:

```bash
# cron 0 3 * * *  → every 24 h.  Phase window: 24 h wide.  ZERO SLACK.
compute_phase() { h=$(( (now - start) / 3600 ))
  [ $h -lt 24 ] && echo RED; [ $h -lt 48 ] && echo BLUE; [ $h -lt 72 ] && echo GOLD; }
```

One second of scheduler jitter moves `h` from 23 to 48 — an increment of 25, not 24 — stepping clean
over the entire BLUE window. Bash integer division truncates toward zero, so a run a fraction early
floors to the previous band and a run exactly on time jumps past it.

Measured: across six cycles one phase was skipped **every time**; the cycle then HOLDs on its unmet
prerequisite, burns its remaining hours, seals **empty**, and ignites a successor carrying the same
defect. Seventeen scars collected, zero repairs, for a month — while from outside the organ looked
healthy throughout: cron fires, logs appear, state advances, cycles seal.

Rules:

1. **Advance the phase by WORK COMPLETED, not by clock.** The *gate* almost always already reads the
   completed-state record; if the *selector* reads the clock instead, two mechanisms disagree and the
   wrong one wins. Point both at one source:
   ```bash
   compute_phase() {
     [ -z "$(phase_done RED)"  ] && { echo RED;   return; }
     [ -z "$(phase_done BLUE)" ] && { echo BLUE;  return; }
     [ -z "$(phase_done GOLD)" ] && { echo GOLD;  return; }
     echo REBIRTH; }
   ```
   A missed run then self-heals on the next fire instead of skipping a phase.
2. **Enforce cycle length separately** once the selector is state-driven, or a stalled phase retries
   forever. Retrying is correct here — but make it visible rather than silent.
3. **Give the window margin.** If the phase must stay clock-derived, make the width strictly greater
   than the period (period + slack) and assert the computed band is the one you intended.
4. **A cycle that seals EMPTY is a defect, not a quiet cycle.** Count completed phases at seal time
   and fail loudly on zero — the empty seal is precisely what hides this class, because it makes a
   dead cycle record exactly like a finished one.

**Provisioning is not the loop.** A manual sovereign-run cycle completed all three phases and did
real repairs; every unattended cycle since skipped one. When a loop has ever worked *only* under
supervision, the defect is in the scheduler, not the design — check that first.

### Two writers on one scheduler — the failure is ZERO, not a conflict

Several sessions editing the same job store concurrently is the normal condition in a federation, not
an edge case. They read the same file, spot the same duplicate, and **each retires the other's
producer.** Measured: two lanes building the same daily artifact both judged the other redundant;
each pause applied cleanly and reported success, and the net result was no artifact at all. Nothing
errored, and each mutation was correct in isolation.

```
After ANY scheduler mutation:
  1. re-read the job store FROM DISK (a tool's return value reports what you wrote,
     not what the store now holds — a concurrent writer may have moved it)
  2. enumerate every ENABLED job whose product overlaps yours
  3. assert the overlap set is exactly ONE, and that it is enabled: true
  4. assert the total is not zero before you stop
```

Decide the survivor on **evidence** — test coverage, verified output, a seal that re-hashes — never on
which session authored it, and never on which looks tidier. Record the survivor and the reversal in
the pause reason, so the next reader knows which lane is authoritative without re-deriving it. Pause
the redundant job; **do not delete the implementation.** Its code tree, schema and archived output
stay on disk, still readable, so the logic can be revived or ported later.

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
- **A measurement of the human's burden is report-only, and must never acquire a gate.**
  A metric whose subject is human attention, interruption, effort or cost has a degenerate
  optimum: placed beside a doctrine of *"silence is a valid successful action"*, the cheapest
  way to improve it is to stop reporting, stop escalating, stop asking, and let unobserved
  failures score as successes. Emit such numbers at `INFO`, trend them over time, and say in
  the module itself why no scored objective may be added there. The authority-bearing and
  irreversible classes must bypass any such optimisation entirely — they are not a term an
  optimiser is allowed to trade away — because a constraint list in prose below an objective
  does not bind it. Same test for any external metric proposal: ask what its optimum is, and
  whether that optimum violates a standing rule.
- **Extract the classification into a pure function, then wire its suite into the periodic
  sweep.** A decision buried inside a scan loop cannot be shown to fail, and a loop's own
  "is it healthy" logic is the last place worth trusting unverified. A branch table that
  resolves every input to a benign state is decoration wearing a verdict — enumerate the
  inputs that take each branch and require the failing one to be reachable. A test that is
  not wired to run every cycle is prose in a file, so it will be the edit that softens the
  check that goes unnoticed. After any change, plant one wrong assertion, confirm the sweep
  returns a failing verdict with a non-zero exit, then restore: a suite that cannot be made
  red is not evidence of anything.

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
❌ Gating a human-burden metric              → its optimum is to stop reporting.
❌ Classifier logic inline in a scan loop    → cannot be shown to fail; untestable.
❌ Phase window width == cadence period     → sub-second jitter skips a phase; loop deadlocks.
❌ Selector keyed on clock, gate on state   → two mechanisms disagree; the clock wins.
❌ A cycle that seals empty and ignites one → the defect propagates to every future cycle.
❌ Phase derived from elapsed time alone     → a missed run skips the work instead of retrying it.
❌ Retiring a duplicate without checking     → two writers each retire the other; net zero.
❌ Trusting your own write as final state   → a concurrent writer moved it after you looked.
❌ Hardcoded chat id instead of origin       → routing claim that cannot follow the session.
❌ Citing a skill the job depends on unproven → silent improvise at the first unattended fire.
❌ A regression suite never wired to a sweep → it will not run on the edit that matters.
❌ A branch that absorbs every input         → decoration wearing a verdict.
❌ Deltas only, no state snapshot           → quiet cycle and dead cycle are identical.
❌ `except: pass` around a loop step         → DEGRADED silently reported as QUIET.
❌ A dry_run flag some step ignores          → rehearsal mutates what it meant to protect.
❌ Appending the same extraction each cycle  → N runs, N copies, inflated counts.
```

---

## §11. REFERENCE

- `references/autonomous-loop-runtime.md` — concrete lock implementation, cron entry
  shape, notification gate wiring, baseline schema, ledger record shape, and the
  race / double-run tests used to verify each of them.

---

*DITEMPA BUKAN DIBERI*
