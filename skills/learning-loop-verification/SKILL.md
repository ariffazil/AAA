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
capability_tier: fed-long-context
ecology_state: WARM
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

## Conservation accounting — the count that must balance (F2)

Every hop is a filter: `X → Y`. It must account for the whole of its input.

```
N_input = N_accepted + Σ N_rejected(named reason) + N_deferred(future condition)
```

If the two sides disagree, the difference is not "no signal" — it is unaccounted state. And it is
the one defect no liveness check can see, because the mechanism reports success either way.

1. **Instrument the live module, never a re-implementation.** Load the production file by path
   (`importlib.util.spec_from_file_location`) and call its own predicates and constants
   (`MAX_PICKS`, `STALE_DAYS`, `_is_sovereign`, `_is_stale`). A hand-rolled copy of the filter tests
   your reading of the code, not the code. Do not call the module's `write_*` path — record the
   selection only, and leave the store untouched.
2. **Replay the exact branch order** and attach a named reason to every rejection, broken down to
   the individual guard that fired (`sovereign_pattern:DELIBERATE NEXT SESSION`,
   `not_stale:too_young(0.43d<3d)`). An aggregate `rejected: 128` is not auditable; the per-guard
   histogram is what proves the filter is specific rather than blunt.
3. **Separate DEFERRED from REJECTED.** Items that passed every guard and were cut only by a
   capacity cap (`[:MAX_PICKS]`) are next run's work, not refusals. Folding them into "rejected"
   hides the throughput ceiling — and that is exactly how a pure throughput problem gets misreported
   as a broken filter.
4. **Run it twice: live, and reconstructed at the historical run time.** The observed pass uses the
   real clock; the reconstructed pass filters entries by their own timestamp to the run under audit.
   Reconstructing by timestamp is not a backup read — say so, because an absent backup means you are
   approximating the input state, not recovering it.
5. **Expect to be wrong; this is a falsifier, not a confirmation.** If it balances, the filter is
   innocent and you retract, in writing, with the arithmetic. A probe built to confirm the
   hypothesis you already published is not a probe.

Balancing at one hop proves nothing about the next. Apply it at *every* hop — producer, filter,
judgment, write-back — and the defect usually surfaces where you were not looking.

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
- **Count distinct OBSERVATIONS, not scored rows.** Dedupe of *inputs* does not protect the
  *outcome* count. Two opposing claims about one quantity — a long hypothesis and a short one, both
  settled by the same closing price — are two rows and one fact. A routine that scores each row
  independently therefore reports `decisive: 2` from a single market event, and any hit-rate over that
  pair is an artefact of the duplication rather than a measurement. Before quoting an accuracy, a
  Brier score, or a calibration bucket, group the settled rows by the observation that decided them
  and count groups: `N_rows > N_observations` means the rate is inflated, and a complementary pair
  (one up, one down) will pin it near 50% on construction. Prefer one scored claim per falsifier; if
  the store permits opposite hypotheses, the accuracy meter must dedupe by falsifier, not by row id.
- **Two derived reports over one ledger that disagree means one is stale.** When a hand-computed
  summary and the instrument's own report carry different values for the same quantity over the same
  rows, that is not a range or a rounding difference — it is two writers, and at least one is reading
  a different window or an unsuperseded predecessor. Resolve which file is the source before citing
  either; do not average them, and do not report whichever one flatters the system.
- **Two status surfaces over one system may carry opposite verdicts and never reconcile.** A health
  surface reading `OPTIMAL` while a reconciliation surface over the same machine reports `CRITICAL`
  is not ambiguity to be narrated away — it is a defect with a specific repair: name which surface the
  downstream consumer reads, and make the other derive from it or cite it. Independent observers must
  be *independent*, not unreconciled; when they disagree, nothing that reads only one of them can be
  trusted to notice.
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

- **Every completed verification needs a terminal explanation.** A record that has reached the
  verified state must resolve to `LESSON_CREATED` *or* to an evidence-backed `NO_LESSON_REASON`
  (`NO_MEANINGFUL_SURPRISE`, `BELOW_LEARNING_THRESHOLD`, `MISSING_REQUIRED_FIELDS`,
  `EXTRACTOR_NOT_INVOKED`, `POLICY_INTENTIONALLY_SUPPRESSED`, `OTHER_MEASURED_CAUSE`). Verified
  outcomes sitting beside zero lessons is an unexplained gap, not evidence the loop is young — "not
  mature yet" stops being a reason the moment a record is verified. The invariant to enforce is
  `VERIFIED → {LESSON_CREATED | NO_LESSON_REASON}`, and it is what makes the loop auditable instead
  of merely productive.
  The same obligation binds every *non*-completion, which is where it is most often skipped: a
  `HOLD`, `DEFER`, `SKIP` or `VOID` that persists its verdict token but not the reason it chose it
  is a decision-shaped object with no decision inside. Test it as a rate, not a spot check —
  `verdicts_persisted / executions` beside `reasons_persisted / executions` over the consumer's own
  log. A verdict rate of 100% sitting next to a reason rate of 0% reads as a healthy, decisive
  mechanism, and it will loop forever because nothing downstream can act on a refusal whose cause
  was never written down.
- **A lesson whose error class is a placeholder is noise, not closure.** Count the lesson only after
  checking what class the producer resolved. A classifier that cannot determine the real error class
  usually writes its own sentinel (`UNKNOWN`, `OTHER`, `None`, `""`) into the record — and the lesson
  extractor then emits a lesson *about the sentinel*: `Unknown error type 'UNKNOWN' seen 1 times.`
  That increments `lessons_total` while carrying zero information, so it satisfies the
  `VERIFIED → LESSON_CREATED` invariant on paper and fails it in substance. Read one produced lesson
  end to end before crediting the arrow as closed; a placeholder class is a finding about the
  classifier, and it is *worse* than an honest zero, because the count now looks healthy.
  The inverse also holds: a guard that skips correct predictions compares against a string sentinel
  (`if error_type == "NONE"`) while the producer may write a language null (`None`) — a mismatch that
  silently routes "no error" down the unknown-error branch. Resolve the sentinel in the data before
  deciding which branch a record takes.
- **You can obtain the terminal reason by invoking the producer's own extractor once — but declare the
  store mutation you cause.** When the arrow is unproven because nothing has run since the last
  verification, running the organ's extractor by hand converts a guessed reason into a measured one.
  It also writes to the organ's store. Say so in the report: the byte delta, that it is idempotent
  and deduped by fingerprint, and that the scheduled run would have done the same. An undeclared
  write to a store you are auditing is indistinguishable from the contamination you are looking for.
- **Separate `NO_LESSON_BECAUSE_SCHEDULED_AFTER_THE_OUTCOME` from a broken arrow.** Compare the
  verification timestamp against the extractor's last invocation. A record verified *after* the last
  run is `EXTRACTOR_NOT_INVOKED_SINCE_VERIFICATION` — the machinery is intact and simply has not been
  asked yet. Reporting that as a consumer failure sends someone to rebuild a working stage.
- **Low lesson count can be correct; an unexplained zero cannot.** Do not optimise for more lessons.
  If outcomes matched expectations, no lesson is the right answer and manufacturing one is drift.
  What is unacceptable is zero lessons with no terminal reason recorded against any verified item.
- **Measure the conversion funnel before prescribing a build.** Count each arrow separately —
  `OBSERVE→PREDICT`, `PREDICT→DUE`, `DUE→VERIFIED`, `VERIFIED→LESSON_CANDIDATE`,
  `LESSON_CANDIDATE→LESSON` — with a median age per stage. A very large first stage and a near-zero
  last stage localises the fault to one arrow. A proposal that cannot name *which* arrow is broken
  will usually prescribe rebuilding machinery that already runs, so always check for existing
  schedulers, timers and loop scripts before accepting "the mechanism is missing".
- **A scheduler exit status is not an outcome.** A verifier timer reporting `success` with
  `due_count=0` is `SCHEDULER_SUCCESS`, not `VERIFICATION_SUCCESS`. Keep the two states separate in
  every report: a healthy timer over an empty work list certifies nothing about the arrow it was
  built to close. The same applies to a loop-closer that runs cleanly every cycle because nothing
  ever reaches a closable state.
- **Check whether the domain record is even parseable before auditing rates over it.** If the store
  returns one constant kind/type for every row, you are reading a field the writer never populated —
  the fine-grained breakdown you were handed came from the organ's internal counters, not from the
  data. Say which numbers you could re-derive and which you are inheriting; never present an
  an inherited breakdown as your own measurement.
- **An empty output is not evidence of no work — read the consumer's log before concluding.** An
  empty queue or artifact file is a *post-consumption* state at least as often as a never-produced
  one. The trace of a produced-then-drained item lives in bucket files, journals and the consumer's
  own execution log; the producer's empty artifact is the one place it does not. Concluding "produced
  nothing" from an empty file is the same class of error as reading a null payload as a measured
  zero — and worse in an audit, because it manufactures a defect the consumer's log would have
  disproved in a single read. Look for the consumer's execution log and its `DONE: N <items>` line
  before you name the producer.
- **A dedupe key held in the queue the consumer drains causes permanent re-examination.** When a
  consumer rewrites the queue to hold only the *remaining* items, the record of what it already
  examined leaves with the item — so the producer re-selects the identical work next cycle, forever.
  Measure it as repetition: count executions grouped by item id, then group those counts. Three ids
  cycling while the rest advance is the signature. The fix is structural and is not a larger cap:
  the memory of "already examined" belongs in a durable ledger *outside* the transport, keyed by item
  id and carrying the verdict. A queue is transport; a ledger is memory. A producer whose dedupe
  reads the queue's current contents has no memory at all.

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
- `references/conservation-accounting.md` — the per-hop balance test in full: the importlib probe
  pattern, the per-guard rejection histogram, the deferred-vs-rejected split, and the worked
  refutation that shows what a balanced result looks like.
