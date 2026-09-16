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

## Pitfalls

- **Volume is not learning.** Break any ledger down by event type and count only rows
  carrying a non-zero improvement/result field before citing it. Heartbeat/pulse rows
  outnumber real improvements by an order of magnitude, so a raw row count turns activity
  into a false claim of learning.
- **A responding instrument is not a measurement.** A tool returning success with an
  all-null payload, a false characterization flag, or a zero-sample window is *wired but
  uncharacterized*. Report the empty gauge as such — same class of error as inventing a
  timestamp.
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
- **A ratified rule with no executor is a write-only ledger in prose.** Before describing a
  doctrine, invariant, or threshold as "in place", resolve it to the thing that enforces it —
  a script, a unit, a cron line, an import, a gate on the write path. Named-but-unenforced is
  the same defect class as a table nobody reads, and it is worse to leave unreported because
  it gets quoted as authority.

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
