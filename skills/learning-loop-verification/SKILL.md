---
name: learning-loop-verification
description: "Use when auditing whether a learning loop closes."
version: 1.0.0
risk_tier: low
floor_scope: [F2, F4, F7, F11]
autonomy_tier: T1
triggers:
  - "does the learning loop actually close"
  - "can the agent improve its own skills"
  - "eureka / scar promotion audit"
  - "capability evolution audit"
  - "auto-update skills from sessions"
  - "is the system actually learning"
  - "the rule is ratified but nothing enforces it"
  - "doctrine exists with no executor"
---

# Learning Loop Verification

Method for answering "does this system actually learn from its own sessions, or does it
merely record them?" in a way that survives hostile audit. Every hop is proven with a
receipt. The question is never "does the pipeline exist" — it is "did an artifact
change, and can I show it".

## The Iron Rule (F2)

```
No hop is CLOSED until three things line up:
  the item was consumed → the ledger row was written → the text is visible in the artifact.
"The job ran" is evidence of none of them.
```

Report closure **per hop**, not as one verdict. A pipeline that is producer-open,
consumer-broken and measurement-blind is not "50% working" — it is three separate
findings with three separate owners.

## The hops

| # | Hop | Question | Receipt |
|---|-----|----------|---------|
| 1 | Producer | what is queued right now? | queue listing: pending vs consumed items |
| 2 | Scheduler | is the drain actually firing? | crontab / cron.d / systemd timer line + last-run log tail |
| 3 | Consumer | what does the job say about itself? | its own log, especially reject reasons |
| 4 | Landing | did the write reach the artifact? | grep the artifact for the payload AND the ledger for the row |
| 5 | Measurement | does the change alter later behaviour? | the live instrument's characterization fields |
| 6 | Backlog | what is waiting on a decision? | status histogram over the queue |

## Procedure

1. **Count pending vs consumed.** A queue holding only consumed items means producer or
   consumer is idle; a queue holding only pending items means the consumer is stuck.
2. **Find the scheduler line, not the job's reputation.** Check `crontab -l`, `/etc/cron.d/`
   and `systemctl list-timers` — jobs frequently live outside crontab.
3. **Read the consumer's own reject log before theorising.** It usually names the exact
   reason it refused. A reason repeating on every run IS the diagnosis.
4. **Prove landing by grep, not by trust.** Search the target artifact for the payload
   text and the ledger for the row. Both, not either.
5. **Call the instrument live.** Query the running tool, not the module on disk, and read
   its characterization fields rather than its status.
6. **Histogram the backlog** by status, to see whether the loop terminates in a decision
   or accumulates proposals.
7. **Separate structural from incidental.** Name which hop is broken and which is merely
   slow. Never present a partially-closed loop as a working one.
8. **Probe for receipts that already arrived.** Before reporting a loop as "not closed yet",
   scan the pending queue for items whose outcome is already determinable from a live instrument.
   "Waiting for its date" and "waiting for evidence" are different states, and only the second is
   legitimately open.

## Pitfalls

- **Volume is not learning.** Break any ledger down by event type and count only rows
  carrying a non-zero improvement/result field before citing it. Heartbeat/pulse rows
  outnumber real improvements by an order of magnitude, so a raw row count turns activity
  into a false claim of learning.
- **A responding instrument is not a measurement.** A tool returning success with an
  all-null payload, a false characterization flag, or a zero-sample window is *wired but
  uncharacterized*. Report the empty gauge as such — same class of error as inventing a
  timestamp.
- **An identified label is not an identified unit.** A numerator/denominator over N *names* is not
  evidence about N independent things: role lanes, agent seats and service names are routinely
  fallback **chains**, so several names can be served by one backend. Resolve every unit name to what
  actually served it before reading an agreement, consensus, or coverage figure, and record the
  serving unit per observation — an instrument that stores only the requested label cannot be
  falsified later, because two different worlds yield identical output. If the denominator cannot be
  resolved, the verdict is *metric real, denominator unverified*: neither pass nor fail. Full probe in
  `references/instrument-validity.md`.
- **Resolve every named organ to a path, unit or cron line before repeating it.** Labels
  arrive from other agents' briefs, reviews and pasted audits. If a named governor or
  sweep does not resolve on disk, report it as unresolved and name what IS live instead;
  repeating an unresolvable label launders someone else's guess into your own report.
- **A repeating identical reject is a resolver defect, not a bad item.** When a consumer
  refuses the same item every run with the same reason, suspect its own lookup (search
  roots, case sensitivity, path map) before the item. One item failing identically N times
  is a search-space bug — fix the resolver and re-run rather than deleting the item.
- **"Stops at PROPOSED" is usually a gate, not a failure.** Read the proposer's docstring.
  If it declares that it proposes only and execution requires human authority, the backlog
  is a gate mis-placed over reversible work — split proposals by reversibility and route
  the reversible ones to the agent lane instead of escalating the whole queue.
- **Count distinct signals, not files.** Check producer dedupe before reading queue volume
  as signal strength; a producer can emit the same item twice within minutes.
- **Skill count is not capability.** Learning that only ever appends artifacts grows the
  surface without changing behaviour. Ask what the *next* decision does differently; with
  no answer, the loop recorded experience without compressing it.
- **Check the closure ledger's own recency, not merely its existence.** Count the rows at
  each hop (decision → contract → mutation → observation) and take `max(timestamp)` per hop.
  An apparatus with rows whose newest is weeks old is a loop that stopped, and it is
  indistinguishable from a working one in any inventory that only asks whether the file is
  there. Report the newest row per hop, not the row count.
- **A proof field carrying a self-assertion is testimony, not observation.** When a mutation
  row's proof reads like an expectation (`SIMULATED_*`, `expected_*`, a bare `OK`), that hop
  never asked reality — precisely the defect the loop exists to prevent. The string IS the
  finding: the schema has a slot for the observation and the writer is filling it with the
  intent.
- **A date-gated verifier is blind to a receipt that arrives early.** When the loop wakes on
  `verify_at` rather than on the evidence, a prediction whose falsifier is already satisfied sits
  unscored until its calendar date — and the same defect hides a claim that has already resolved the
  other way. Probe it directly: load the prediction store, and for every row with no verdict, ask
  whether a live instrument already answers its threshold; report those rows as
  `FALSIFIER_ALREADY_SATISFIED` with the reading that satisfied them. Do **not** shortcut this by
  letting the verifier run early — a claim *about* a future date is not falsified by today's reading,
  and scoring it early is a transition lie (`SCHEDULED → FALSIFIED` skips the state). The correction
  is a new state, not a shorter clock: `SCHEDULED → FALSIFIER_ALREADY_SATISFIED → {FALSIFIED |
  RECOVERED}`.
- **A store holding two claims about one world is a contradiction you can compute.** When the same
  ledger carries a predicted band and a sibling organ already publishing the live value for that
  quantity, diff them on every read. Two mutually exclusive statements sitting unremarked is F2
  drift no per-hop check catches, because every hop is individually healthy.
- **A check that names a symbol or path which does not exist is measuring an older design.** A red
  result of the form `AttributeError: module has no attribute X`, or `FileNotFoundError` on a
  constant declared at the top of the check file, means the check still points at a shape the system
  has moved past — a helper that now lives in another language, a directory that was renamed or never
  existed. Resolve the symbol and the path against disk BEFORE touching production code. Rewriting a
  working component to satisfy a check written against an older shape is the expensive direction: it
  silences the check without restoring the property the check was protecting.
- **A check that witnesses a copy instead of the running artifact certifies the copy.** When one
  invariant is computed in two places (a builder in one language, a mirror of it in another), the
  mirror passes while the served path drifts — worse than no check, because it reports green. Test
  the artifact that actually runs, and recompute the invariant independently on the check side: a
  cross-language recomputation (one runtime produces the digest, another recomputes it from the same
  bytes) is a real witness; a re-implementation is not.
- **A ratified rule with no executor is a write-only ledger in prose.** Before describing a
  doctrine, invariant, or threshold as "in place", resolve it to the thing that enforces it —
  a script, a unit, a cron line, an import, a gate on the write path. Named-but-unenforced is
  the same defect class as a table nobody reads, and it is worse to leave unreported because
  it gets quoted as authority.

### A middleware organ that ran once and stalled

An organ can hold well-formed state files, be scheduled, and be `active` — while having completed
**one** cycle and then silently stopped. Its own records contain the proof; read them as a series,
not as evidence of existence.

Measured shape: six cycle records, each valid JSON with a correct schema. Read as a series:

```
cycle   phase     scars  repairs  baseline  participants
1       GOLD        6      6      present   {}
2       RED         7      0      null      {}
3       REBIRTH     0      0      null      {}
4       REBIRTH     0      0      null      {}
5       REBIRTH     0      0      null      {}
6       RED        10      0      null      {}
```

And the phase-completion map, which is the field that settles it:

```
cycle 1: {RED, BLUE, GOLD}    ← the only complete cycle
cycle 2: {RED}                ← stalled after the first phase
cycles 3-5: {}                ← opened and completed NOTHING
cycle 6: {RED}
```

Rules:

1. **Count completed cycles, not cycle files.** Read the per-cycle phase-completion map. A file
   that exists is not a cycle that ran — three of the six above produced no phase at all, and an
   inventory that asks only "is the file there" reports all six as healthy.
2. **The ratio that matters is observed-vs-repaired, summed since the last repair.** Six scars then
   `7 + 0 + 0 + 0 + 0 + 10 = 17` scars against **zero** repairs: an organ that sees and does not
   mend. Report the ratio, not the record count.
3. **Read the loop's own historical output for named recurring classes, and check each against the
   live system.** The successful cycle recorded a `recurring_scar_classes` list; one entry named a
   class that was **still open a month later** when probed directly. That converts "the feedback
   loop is missing" from theory into a dated prediction the loop failed to act on — the strongest
   available evidence that it is inert, and cheaper than any argument about design.
4. **A witness or participant field that is empty in EVERY record means attachment was never
   wired** — including in the cycle that otherwise succeeded. Do not read a completed cycle as a
   witnessed one; the emptiness is uniform across success and failure, which is the signature of a
   step that was never implemented rather than one that failed.
5. **`baseline: null` from cycle 2 onward means later cycles had nothing to measure against.** A
   survival or regression claim needs a stored baseline; without it the loop can still emit a
   verdict, and that verdict is about nothing.
6. **An instrument exported but never called is decoration.** Grep for CALL SITES, not definitions.
   A function built to compute the honest state — exported in the package `__init__` and documented
   as the honest path — had zero callers anywhere, while the dishonest constant-driven path was the
   one wired to a surface. Extends *a ratified rule with no executor* to the function level: an
   export list is not an enforcement point.
7. **Absence of a field in the organ's output propagates upward.** If the leaf organ that would
   produce a scalar emits no field for it at all, no consumer can measure it — and every surface
   claiming a value for that scalar is synthesising one. Trace the scalar to its leaf producer
   before auditing the consumers.

## Output contract

```
Verdict per hop: CLOSED | PRODUCER-OPEN | CONSUMER-STUCK | UNLANDED | EMPTY-GAUGE | GATED
Then: the receipt for each verdict, the single hop to fix first, and the boundary —
which changes are the agent's to execute and which require sovereign authority.
```

## Boundary

State explicitly which side of the line each finding sits on:

- **reversible + digital** → agent lane, execute now;
- **governance, canon, verifier, thresholds** → sovereign authority, HOLD.

A system whose evaluator can rewrite its own evaluator loses its anchor. Auto-evolve the
capability surface; leave governance under human sovereignty.

## Support

- `references/learning-pipeline-probes.md` — copy-pasteable probe bundle for the six hops,
  plus an observation→interpretation table.
- `references/instrument-validity.md` — hop 5 extended: resolving a metric's denominator to distinct
  real units before citing it, the unit-identity output contract, and batch-run safety (smoke-test,
  fail-fast on every dead-input class, incremental writes). Read before quoting any agreement,
  consensus, coverage, or drift figure.
