---
name: witness-independence-audit
description: Use when a ledger row is cited as witness to an event.
version: 1.0.0
author: Hermes
license: arifOS
tags: [audit, receipts, ledger, witness, self-attestation, evidence]
triggers:
  - a ledger, receipt or log is offered as proof that an event happened
  - does a receipt exist for this event
  - a system claims it witnessed, sealed or recorded its own action
  - a self-modifying runtime change should have left a trail
  - deciding whether a record is an independent witness or self-attestation
related_skills: [claim-receipt-discipline, probe-evidence-integrity]
---

# Witness Independence Audit

A record's existence is a claim, not a witness. This skill is the procedure for deciding whether a
ledger row can carry the claim placed on it — and for saying honestly which verdict you reached.

Scope: ledgers, seal chains, skill/agent mutation journals, audit logs, and any "the system lists this
as done" surface in a self-modifying runtime. Adjacent skills own probe mechanics and claim tagging;
this one owns **the independence question**.

## The law

> A record written by the actor that performed the mutation proves **ordering**, not **independence**.

Independence is a property of three things, never of the row's content: **who** wrote it, **when**
relative to the event, and whether an **outside actor** can read it. A hash chain authored by the
mutator satisfies none of them.

Corollary — self-audit is structurally incomplete: no system fully verifies its own compliance from
inside itself, so the missing item is always an outside witness. Name the witness that *would* close
the gap; do not treat a better record as that witness.

## Procedure

1. **Name the event and its artifact.** What changed, the hash that identifies the changed object, who
   or what performed the change (uid/actor), and the timestamp the change itself carries.
2. **Resolve the store from the writer's own declaration** — its path constant, config, or the file it
   opens. Never from the name that sounds right. An absence read against the wrong store manufactures
   a defect.
3. **Read one row and enumerate its fields:** actor, event `ts`, chain fields (`prev`, `hash`), and any
   retro labels (`kind: *BACKFILL`, `backfilled_at`, `imported_at`, `reconciled_at`).
4. **Judge authorship.** Actor == the mutator → `SELF_ATTESTED`. Independent actor or external
   substrate, recorded at event time → `WITNESSED`. A chain present but authored by the mutator is
   still `SELF_ATTESTED`; the chain buys tamper-evidence, nothing more.
5. **Judge timing.** Compare the row's event `ts` against the file's mtime and any backfill label.
   Rows whose `ts` are much earlier than the file's mtime, all carrying a backfill kind, mean the
   ledger was **minted after the fact** from some local journal — `BACKFILLED`: real data about real
   events, and not evidence that anything witnessed them.
6. **Check the container's perimeter with `stat -L`.** A directory that is a symlink always reports
   mode `777`; report the target's real owner/mode instead, plus the uid the writing process runs as.
   Say which layer is enforced and which is convention.
7. **Separate fixture rows from operational rows** before counting anything — temp-dir paths, names
   containing `selftest`/`test`/`fixture`, obviously synthetic actors. A probe must not write its test
   fixtures into the canonical ledger.
8. **Stamp the verdict with your probe time.** Absence is time-scoped: a store can be populated minutes
   later by the same actor, so "nothing there" is a fact about your timestamp. Re-probe before
   repeating an absence as a standing gap.

## Verdict vocabulary (state one, never a bare "verified")

| Verdict | Meaning |
|---|---|
| `WITNESSED` | Independent actor/substrate recorded the event at event time |
| `SELF_ATTESTED` | The mutating actor wrote its own record — usable as a source, not as a witness |
| `BACKFILLED` | Record created after the event, labelled or provable from ts-vs-mtime |
| `ABSENT_AT <time>` | Nothing found at probe time; carries no force about later states |

## Rules

- **Never mint a receipt for an unwitnessed mutation.** Writing the entry afterwards does not create
  the missing witness — it destroys the evidence that one was missing. Declare witness debt instead:
  the event, the actor, the artifact hash, and the fact that no independent record exists.
- **A local journal is a source, not a witness.** Keep it, cite it, label it as such — do not delete it
  and do not promote it.
- **Repair the record by relabelling, not by rewriting history.** If an old row overstates what it
  witnessed, classify it correctly going forward and leave the original row intact; append-only formats
  are the only ones still auditable later.
- **The smallest shippable slice of a lock is one path with one outside witness.** Prefer wiring a
  single mutation path to a receipt plus an independent reader over designing a framework.
- **A gate that has never been attacked is a claim, not a control.** Pair any enforcement claim with a
  negative test that exercises the path (a probe that *fails* when it should).
- **Distinguish blocked from impossible.** "The proof requirement cannot currently be met" is
  `BLOCKED_UNMET_PRECONDITION`; "this cannot be built" is a much stronger claim that needs its own
  warrant. State which one the evidence supports.

## Pitfalls

- **`stat` without `-L` on a symlinked ledger path reports `777` for the link** and becomes a confident,
  wrong "world-writable" security finding. Follow the link first.
- **A hash chain is not verification.** `prev`/`hash` continuity rules out silent editing of the middle;
  it says nothing about who authored the chain or whether anyone independent holds a copy.
- **Counting rows before filtering fixtures** inflates a ledger with the probe's own test writes.
- **A retroactively-created ledger reads as a populated one.** Check `kind`/`backfilled_at` and the file
  mtime against the row timestamps before citing coverage.
- **Independence has axes.** A second process, a different uid, a different host and an external service
  are different strengths of witness — say which axis you actually have.

## Probe recipe

```bash
grep -rl "<event-id>" <store> | head          # any record at all
stat -c '%y  %n' <store>/<ledger>.jsonl      # when the ledger was last written
ls -lat <store> | head -5                    # a store born after the event = backfill
stat -L -c '%a %U:%G %n' <store>             # right way; plain stat on a symlink always says 777
```

```python
import json, collections
rows = [json.loads(l) for l in open("<store>/<ledger>.jsonl") if l.strip()]
print("by actor:", collections.Counter(r.get("actor", "?") for r in rows))
print("kinds:",    collections.Counter(r.get("kind", "-") for r in rows))
print("ts range:", rows[0].get("ts"), "->", rows[-1].get("ts"))
print("chained:",  any(k in rows[-1] for k in ("prev", "prev_hash", "chain_hash", "signature")))
print("backfilled:", any(k in rows[-1] for k in ("backfilled_at", "imported_at")))
fixtures = [r for r in rows if "selftest" in json.dumps(r).lower() or "/tmp/" in json.dumps(r)]
print("fixture-shaped rows:", len(fixtures))
```

Absence template: `ABSENT_AT <HH:MM TZ>  store=<resolved path>  pattern="<subject>"  rows_searched=<n>`.

## Reporting shape

Event → store → row evidence (fields, ts, mtime) → verdict → what would make it `WITNESSED`.
Field names and numbers before the conclusion, and probe time with every absence.
