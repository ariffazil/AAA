---
name: observability-completeness-audit
description: "Use when asked if observability coverage is complete."
tags: [observability, telemetry, tracing, coverage, audit, ledger, spans]
triggers:
  - "do we have full observability"
  - "is observability complete"
  - "observability coverage"
  - "full-stack observability"
  - "we have N million spans"
  - "do we have tracing"
  - "can we trace a request end to end"
  - "how much observability do we have"
  - "how many visitors do we have"
  - "do we have analytics"
  - "site traffic numbers"
  - "can we measure readership"
---

# Observability Completeness Audit

Answering "do we have full observability?" with liveness checks is the standard
failure. A pipeline can be perfectly healthy — worker active, consumer drained at
zero pending, rows arriving seconds ago — and still be a flat event log that nothing
reads. **Liveness and completeness are different questions.** This skill is the
second one.

High row counts are the most common false positive. "We have 200k observations"
is not a coverage claim; it is a row count. Coverage is per field, per layer, and
conditional on someone reading the result.

## Procedure

### Step 0 — find the live writer before reading any code

A service may execute a symlinked or module-invoked path that differs from the
worker/config file you find first. Read the unit's `ExecStart` and resolve
`readlink -f` on the deployed path. A stale twin will show you a bug the live code
already fixed, and the resulting false finding costs the whole audit its credibility.

### Step 1 — column census

`count(<col>)/count(*)` for every column in one query. Turns "we have N rows" into a
shape. See `references/coverage-census.md` for the full statement.

### Step 2 — the correlation test (the sharpest single measurement)

Compare `count(DISTINCT trace_id)` against the row count.

**Equal means every row is its own trace and nothing is correlated with anything** —
not parent to child, not request to retry, not agent to subagent. Combined with a
NULL `parent_span_id`, the store is a flat event log wearing trace-shaped column
names, not a trace store with missing links. No backfill creates the missing
hierarchy afterwards.

Related: **a column that is always NULL is a schema promise nobody kept.** Presence
of the column is not capability. Say what cannot be queried, not what exists.

### Step 3 — constant-field check

Group by any attribution field (`organ_id`, `service`, `tenant`). **A field that is
100% one value is a constant, not an attribution** — it looks populated in a census
and carries no information.

### Step 4 — grammar / vocabulary purity

For any field that is supposed to carry a closed vocabulary (a verdict, a status, an
enum), print the value distribution before quoting it in a statistic. When execution
status codes leak into a governance or semantic field, every aggregate over that
field is silently contaminated. **Count how many distinct tokens are valid members
of the declared vocabulary** and report that share.

### Step 5 — does the store have a health surface at all?

A telemetry plane with no health endpoint can die completely with the only symptom
being a stale `max(timestamp)` in the table. Check for a listener rather than
trusting a docstring or config value that declares a health port — declared is not
deployed. If the surface is missing, it is a blocker for any "monitor the monitoring"
work and it outranks schema improvements.

### Step 6 — THE GATE: find the consumer before proposing anything

Grep for readers of the table/store, excluding the writer:

```bash
grep -rl "<schema>.<table>" /root --include="*.py" --include="*.sql" --include="*.yaml"
```

If only the writer appears, it is a **write-only ledger**. Also check the visualiser:
a dashboard stack whose datasources are a metrics endpoint plus an unrelated status
source does not read this table, however healthy it looks.

**This finding outranks every coverage gap.** Compute and storage are being spent
producing a record nobody opens, and every downstream ambition is built on top of it.

Then quantify the stream — volume plus zero readers is the whole finding:

```bash
wc -l <the-stream>; tail -1 <the-stream>          # how much, and how recently
grep -rl "<stream-name>" /root --include="*.py" --include="*.sh" --include="*.service"
```

Two signals live inside a write-only stream and must be read before recommending anything
else:

- **An emitter that declares its own instrument broken.** A counter or detector whose last
  row carries a status like `BROKEN` / `DEAD_CONVENTION` is the loudest coverage defect there
  is: the oracle cannot see, it said so, and it said so into a channel nobody reads. Lead the
  report with it rather than filing it as a curiosity.
- **Exceptions with no triage.** Count exception/severity-class rows and check whether any was
  ever actioned — a fix, a closed incident, a change in the next row. A stream that has
  emitted for weeks without a single action is not monitoring; it is a log with a severity
  field.

**Apply the same gate to governance artifacts, not just tables.** A doctrine, invariant or
threshold that is named and ratified but resolves to no executor anywhere on disk is a
write-only ledger in prose: it costs context every session and changes no behaviour. Grep for
whatever mechanism its name implies — a script, a unit, a cron line, an import, a gate on the
write path — before describing it as "in place".

### Step 7 — report per layer, with the spread

Score coverage per observability layer (execution/ingest, causal trace, token &
cost economics, governance decisions, retrieval, agentic metabolism, outcome). State
the fields each layer was held to, and show any weighting.

**"Two layers carry the system and five are empty" is actionable; one averaged
percentage hides the thing worth fixing.** Equal weighting across layers is a
defensible default — say so, and show the weights so the reader can recompute.

## Ordering the remediation

When you are asked what to fix, this order beats severity-ranked lists:

1. **Consumer first.** Establish a reader, or a decision to stop writing.
2. **No-DDL structural fixes.** Trace-context propagation usually needs *no schema
   change* — the column already exists and the **producer** is what is broken (it
   mints a fresh trace per emit instead of propagating caller context).
3. **Additive, non-destructive splits.** A vocabulary fix is best expressed as a
   view mapping legacy values plus a write-side change, leaving history verbatim.
4. **New columns last.** Three more columns in an unread table is not progress.

## Pitfalls

- **Do not quote a row count from any document, including your own earlier report.**
  Re-measure. Ingest counters move by orders of magnitude within days.
- **NEW — 2026-09-18 scar (PETRONAS dossier audit): Audit must probe the live surface
  before claiming a defect exists in the artifact.** A textual/structural audit of a
  document can declare "missing" or "defective" while the live URL serves something
  completely different — a wrong-page 200, a `text/html` body behind a `.pdf` slug,
  a symlinked fallback that resolves to a sibling surface. The defect may be a
  *ghost URL* (page claims `seal: 999` but serves empty/HTML) rather than the
  vocabulary the artifact itself uses. Before naming any defect that touches a
  public surface, route the same probe that caught the ghost: live HEAD/GET on
  every slug the artifact names, then compare body, content-type, and byte-size
  against the artifact's own claims. A finding whose evidence is the artifact's
  internal text alone — without a live surface probe — is `PLAUSIBLE` at best,
  not `CLAIM`. This is the same discipline as Step 0 applied to a publication
  surface, not a worker.
- **A process that runs is not a process that works.** A daemon receiving nothing
  will still report healthy. Check its own traffic counters before concluding
  anything about the pipeline, and trace where data actually enters rather than
  assuming the declared receiver is the entry point.
- **An observer with an unscheduled write path is not observing.** If the only code
  that advances a series is an HTTP endpoint, nothing happens without a caller.
  Check for a timer before diagnosing a "writer failure" — the writer was never
  broken, it was never called. An irregular historical series (clustered, gappy) is
  the signature of manual invocation, not of a failing writer.
- **Distinguish `NULL` from JSON `null` in a census.** In JSON/JSONB columns these
  are different states and lumping them misreports coverage.
- **Beware name collisions between a telemetry plane and a notifier/alert endpoint
  sharing a name.** Confirm which one a caller means before wiring anything in.
- **Do not let the audit mutate.** A completeness audit is read-only. Producing
  graphs and receipts is the deliverable; schema work needs its own authorisation
  and its own reversibility plan.

## Reference

- `references/coverage-census.md` — the full SQL set (census, correlation, constants,
  vocabulary, liveness) and a worked report shape. Load it when running the audit.
- `references/web-readership-measurement.md` — the same audit applied to a **web surface**
  instead of a telemetry table: establishing visitor measurement from an origin access log
  behind a tunnel and a CDN, and the traps that make a count silently wrong. Load it when the
  question is traffic, readership, or "do we have analytics".

## A surface may have no instrument at all

Before scoring coverage on any layer, establish that a *sensor exists*. A whole surface can be
unmeasured — no logging directive, no beacon, no collector — and the honest finding is then
"there is no instrument", not "coverage is 0%". Establishing the instrument is the deliverable,
and it outranks any per-field analysis you would otherwise write.

The same gate applies across surfaces: web traffic, deployment state, human input. Ask what
observes the thing, and where that observation lands, before asking how complete it is.
