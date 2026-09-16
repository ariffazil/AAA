---
name: autonomous-learning-loop
description: "Use when building or auditing a self-improving loop."
tags: [autonomy, loop, learning, verification, promotion, rsi, capability]
related_skills: [agentic-autonomy-loop, live-probe-audit-pattern, verify-work]
---

# Autonomous Learning Loop

Turns experience into durable capability: session / scar / eureka → classified
pattern → verified claim → promotion → measured consequence. Covers atom design,
independent verification, promotion gating, consequence measurement, and the
integrity traps that make a loop report healthy while learning nothing.

An **acting** loop (observe → judge → act → seal) is half a system. This skill is the
other half.

Build/operate this whenever the request is "make it learn from its own sessions",
"auto-improve", "recursive self-improvement", "turn scars into capability", or when
auditing a loop that claims to learn. For the acting half (tick, gate, act, seal),
see `agentic-autonomy-loop`.

## The pipeline (run in this order)

```
SESSION / SCAR / EUREKA
   → EXTRACT      read LIVE stores, not transcripts of them
   → CLASSIFY     into a closed taxonomy; unnamed → quarantine
   → ATOM         one claim + evidence + falsifier + measured frequency
   → VERIFY       four checks, all must pass (below)
   → PROMOTE      route by layer; governance layers are not writable
   → MEASURE      baseline at promotion, re-measure after one window
```

**A run that produces no applied change is a FAILED run, logged as such.** Silence is
not success. Write the diagnosis record even when nothing was promoted — an
observation-only log is how a learning loop becomes a diary.

## The unit of learning is a capability atom, not a new skill

`Capability → Organ → Tool → Skill` — skill sits at the bottom. A loop that turns
every insight into another SKILL.md grows the library without growing intelligence.
The atom is the smallest unit that can change future behaviour, and it is only real
if it carries: the claim, evidence at the same layer as the claim, a falsifier, and a
**measured** frequency (counted from distinct sources — never asserted as an
adjective).

## Verification: four checks, all must pass

| Check | Rule | Failure meaning |
|---|---|---|
| **LAYER** | claim layer == evidence layer | a layer answered with another layer's evidence |
| **FALSIFY** | the atom states what would prove it wrong, testably | unfalsifiable claim |
| **REDERIVE** | the verifier re-runs the check against the **live** surface | claim not reproducible |
| **PROCESS** | what *rank* of independence the verdict earned (below) | see below |

A pattern the taxonomy cannot name is **quarantined** — recorded, never promoted.

## Independence is a RANK, not a boolean

`producer != verifier` is a string comparison. Two names written by the same author
pass it while leaving one witness. **A different TOOL is not a different WITNESS** —
routing a verdict through an observer chamber or a judge endpoint does not create
independence if the same agent produced the claim:

| Class | Meaning | Allowed |
|---|---|---|
| `SELF` | same actor graded itself | **rejected outright** |
| `NOMINAL` | different names, same author | graph entry only — **PROVISIONAL**: no survival recorded, no rule proposed |
| `STRUCTURAL` | distinct authors | may record survival |
| `EXTERNAL_ORGAN` | a different agent or external receipt | may also back a judgment claim |

C1–C3 still hold at NOMINAL, because re-derivation runs against the live surface and
does not care who wrote the extractor. So a same-author verdict **may assert "this
pattern exists" and may not assert "this pattern was beaten"**. Before naming an
external witness, probe what it actually accepts: an observer named for your subject
may guard only its own state, and a real judge endpoint called as an actor you already
own is still you. If no other agent can witness, say so and leave the node PROVISIONAL.

## Promotion routing

| Layer | Policy | Applies automatically? |
|---|---|---|
| skill (adapter) | auto when verified | yes — reversible, digital |
| capability (the graph / ledger) | auto when verified | yes |
| policy | propose only | no — queue for the sovereign |
| judgment (ranking, routing weights) | propose only | no — queue for the sovereign |
| governance (floors, kernel, canon, judge, verifier, thresholds) | **forbidden** | **never** |

The loop must not be able to relax its own boundary. Keep the forbidden-path list
**hardcoded in the module** rather than read from a config the loop may edit, and
self-test it on every run (attempt each forbidden write, assert it raises). The loop
may APPEND a claim to a source-of-truth it does not own, and may never rewrite an
existing entry in it — that is what a probe with evidence is for.

## Consequence is the only proof

Capture the recurrence of the pattern being fixed **at the moment of promotion**, and
re-measure it after one full observation window.

| Verdict | Condition |
|---|---|
| PERSISTED | recurrence fell ≥ 50% |
| PARTIAL | fell, but < 50% |
| NO_EFFECT | unchanged (±10%) |
| REGRESSED | rose |
| PENDING | less than one full window elapsed |

A promotion that does not move the recurrence of its own pattern produced no
consequence, however good the receipt looked. Until the window closes the honest
answer is **"not yet observable"** — never "improved". Baseline only the FIRST
promotion of a capability: re-baselining on every run lets the system move its own
goalposts.

## Operating discipline

### The loop shares its state with its own scheduler

A cron-fired cycle and a manually-triggered cycle read the same inputs and then each
rewrite the same derived state from their own stale read — silently moving the
baselines the consequence verdict rests on. Take an exclusive lock for the **whole
cycle**. A second **process** must fail fast with a distinct exit code rather than
wait (a blocked tick is worse than a skipped one); make the lock reentrant within one
process so modules can hold it without nested deadlock. Reserve separate exit codes
for "nothing to do", "ran but applied nothing", and "another instance in flight" —
collapsing them makes a skip and a real miss read identically.

### Amplify only on change

Gate outbound notifications on the **set of state changes** (what was promoted, held,
or changed verdict), not on the rendered message. A bridge that hashes the whole body
sees counts and timestamps move every cycle and re-posts identical work — a ledger
turns into a feed. Keep volatile counts out of the body and write the dedupe marker
only AFTER delivery succeeds, so a failed send retries instead of being swallowed.
Silence when nothing changed is the correct output.

## Integrity traps — a loop that reports healthy while learning nothing

Every trap below presents a green surface. Probe the **payload**, not the status.

- **Registered ≠ served.** A measurement tool can be registered in code and present
  in `tools/list` while the real transport rejects the call. `tools/list` proves
  registration; only a live `tools/call` proves service. A loop that cannot read its
  own measurement while health is green is the worst case — check the read is
  `readable` explicitly and report UNREADABLE rather than `None`, because `None` is
  indistinguishable from a real zero.
- **Structurally-zero read.** A reader keyed on a field the writer never emits (e.g.
  reading `ts` while the writer writes `created_at`) filters every row out and returns
  a genuine-looking zero with a success status. Compare writer and reader field names.
- **Silent no-op.** A derive step keyed on a name that does not exist dead-letters
  every unit while the run still reports success. Compare output count against input
  count.
- **Unbounded re-scan.** A rejected unit left inside the job's own glob path is
  re-checked every run forever; the log reads as stability while the queue is jammed.
  A repeat rejection count for the SAME unit is QUEUE_BLOCKED, not steady state.
  Dead-letter rejects out of the scan path and make re-sweeping a deliberate move.
- **Heartbeat-as-diagnosis.** A log dominated by "observed, nothing improved" rows
  with zero applied changes is an inhale-only loop. Measure the ratio: proposals
  without applications is the signature.

**Probe the estate you are claiming about.** Two trees with the same purpose (a live
runtime root and a canonical catalog) give different counts for the same question.
Report the root alongside every count, probe the root the claim names, and dedupe by
`realpath` before counting — a duplicate count collapses or inflates purely from which
tree was walked and whether symlinks were followed.

## Verifying a loop someone claims is working

1. Read the loop's own ledger and count `applied`/`improvement` records — not the
   summary. Proposals without applications is the failure signature.
2. Confirm the measurement the loop depends on is actually readable through the real
   transport (see Registered ≠ served).
3. Confirm each promoted node's independence class; PROVISIONAL nodes are not survivals.
4. Confirm a consequence baseline exists and check whether the window has closed.
5. Confirm the boundary self-test passes — attempt a forbidden write and assert refusal.
6. Confirm exactly one writer: start two cycles and require one to refuse.

## Reference

- `references/verification-and-promotion-design.md` — atom schema fields, the closed
  failure taxonomy, independence classes, and the consequence verdict table with the
  probe for each.
