---
name: durable-claim-ledger
description: "Use when a claim about system state must stay re-checkable."
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Durable Claim Ledger

> A representation must never outrank the mechanism it describes.

Use this when you are about to write down something about system state that someone will
rely on LATER — a delivery route, a seal, a hash, a capability, a count. Prose and commit
messages decay into folklore because they cannot be re-checked. Bind the claim to a record
to a hashed artifact instead.

Sibling disciplines (user-owned; do not duplicate their content here):
`claim-receipt-discipline` carries tag/receipt discipline and the probe-to-claim matching
table; `assertion-window-discipline` carries scope-widening before a negative claim. This
skill covers the MECHANISM they both assume.

## The four steps

1. **Register the artifact.** Hash the file ON DISK at registration, so
   `claim → artifact → sha256` is a real foreign key rather than a string that looks like one.
2. **Record the claim** against that artifact id, with `claim_type` (OBS / DER / INT / SPEC /
   VOID), `observed_at`, `confidence`, plus `source_quote` and a `locator` (`file:line`).
3. **Verify by RE-HASHING.** A verdict that only stores "someone said CONFIRMED" is a second
   opinion, not evidence. The verification must re-hash the artifact on disk and report the
   live digest, so *verified* means the source still exists and still matches.
4. **Correct by superseding.** A new claim sets `supersedes_claim_id`; the original row is
   never mutated. Corrections are additive, so both the wrong belief and the fix stay readable.

In this federation the mechanism is the `claim_ledger` MCP: `claim_artifact_register`,
`claim_record`, `claim_verify` (with `recheck_artifact=true`), `claim_ledger_stats`,
`claim_list`.

**Check for an existing ledger before inventing a store.** A second store duplicating a
working one is the same defect class as a second clock — it manufactures two truths and
neither side can see the other.

**Know which store owns which record class before reading a negative out of it.** A zero from the
wrong store is an *empty search space*, not an absence. Measured: a search for commit-receipt ids in
the events ledger returned 0 hits for all seven organs and read as "the seals are missing"; the
records live in a different ledger, and all seven were present the whole time. Before reporting a
record missing, name the store that owns that record class and confirm it is the one you searched —
the path that is adjacent, older, or named for the same subsystem is exactly the wrong one. Report a
near-miss as one clause, never as a finding: a phantom defect spends attention and discounts the
findings that are real.

## A dedup guard over an append-only store must read the WHOLE store

An append-only ledger's writer usually carries a guard — "skip if this id is already present". Scope
that guard to a **window** (`f.readlines()[-1000:]`) and it stops being a guard: the store outgrows
the window, every older id falls outside it, and the writer re-appends records that are already
there. Measured on a ~93k-line ledger: **837 of 1,015 ids (82.5%) were invisible to a 1,000-line
window**, 73 ids duplicated, 103 excess rows — while the script's own docstring promised
"idempotent: re-running on the same commit produces no duplicate".

**The consequence is unrecoverable by design.** In an append-only store a duplicate cannot be
deleted, only superseded, so a dedup defect permanently corrupts the ledger's counts and its
readers' confidence. The immutability that makes the store trustworthy is exactly what makes the
writer's bug permanent. So a writer's dedup guard is a *durability* control, not a convenience —
scope it whole-store, or give it an index, and never let it read a window.

Two tells that a guard is windowed rather than whole:

- **Duplicates arrive in contiguous runs across independent subjects.** A run covering every organ
  in a single pass is a retroactive re-seal of the whole set, not one writer misfiring repeatedly —
  and it dates the moment the ids first drifted out of reach.
- **The defect is invisible while the store is young.** It cannot exist until the window stops
  reaching the oldest live id, so no amount of testing against a fresh ledger will catch it, and the
  guard's source reads as correct in review.

Falsify by counting, never by reading the guard's source:

```bash
grep -o '<id-pattern>' <store> | sort | uniq -c | awk '$1>1'      # duplicated ids and multiplicity
```

Then confirm the mechanism: check that each duplicate's **last** occurrence falls outside the
guard's window. That is what separates "the guard is scoped wrong" from "two writers raced". Fix
the scope, then re-run the writer expecting **zero appends** when every subject is already recorded.
A guard fix not proven by a no-op run is untested.

## VOID is a claim, not a silence

`UNKNOWN` must be RECORDED, not omitted. An unwritten unknown cannot be superseded later:
the record just has a hole, and a later reader cannot distinguish "nobody measured this"
from "this was fine."

Record it as a first-class claim with `confidence: 0.0` and a note naming what would resolve
it. When the observation arrives, the unknown is superseded by an OBS — and the history of
not-knowing survives, which is the only thing that makes the later confidence mean anything.

Stating a boundary as a finding is the failure mode: **an unmeasured system is not a healthy
one, and "no data" is not "all clear."**

## A seal over a mutable file describes a MOMENT, not a state

Sealing records a hash at write time. If the target is source code, a config, or any file
someone may edit, the seal is accurate for an instant and then silently stale — while still
reading as authoritative.

When a seal's hash no longer matches the working tree:

1. **Establish WHICH state each hash belonged to BEFORE calling anything wrong.** A hash
   matching the committed blob and a hash of the dirty working tree are different facts, not
   a contradiction. Two or three hashes can all be honest at once.
2. **Do not rewrite the seal.** Append a correction so history stays readable:

```
ORIGINAL        : what was recorded
COUNTEREVIDENCE : the measurement that disagrees, with observed_at
CORRECTION      : which state each value belongs to; mark the old one SUPERSEDED
```

3. **Move the live truth into the ledger** with the re-hash above, so the durable record is
   re-checkable instead of frozen.

Prefer content-addressing (`name-<hash8>.ext`) for anything a ledger points at, so the target
of a past claim never moves. Where a delivery contract demands a stable path, keep the stable
name as a COPY and point the ledger at the addressed one — a fixed path means every run
overwrites the file the previous row hashed, and a ledger whose target is mutable records
events rather than claims.

**A receipt over a git HEAD does not cover the working tree.** "Commit X is sealed" attests the
commit object and nothing else. Content the author has written but not committed sits outside every
seal built on HEAD while the receipt reads as complete coverage. Measured: six governance documents
Authored the same day were all **untracked** in a repo whose HEAD was sealed on a schedule — the
sealed object contained none of them, and nothing anywhere reported a gap. When a seal's claim is
"this work is recorded", the check is `git status --porcelain` measured against what the seal covers,
not the presence of a receipt. Say which of the two you verified: *the commit is sealed* and *the
work is sealed* are different claims, and only the first is automatic.

## An integrity manifest must not pin what is meant to grow

The section above covers a seal over a *mutable* file — honest for an instant, then stale. The
converse is worse, because it fails **by construction**: a whole-file digest recorded over an
append-only store can only ever report FAILED.

Classify the artifact before choosing the evidence.

| Artifact class | Correct integrity evidence | Wrong evidence |
|---|---|---|
| immutable (release, sealed deliverable, one-shot export) | whole-file sha256 | — |
| append-only (ledger, event log, seal chain) | hash-chain linkage (`prev_hash`), monotonic sequence, entry count + head digest | whole-file sha256 |
| live (rolling log, in-place state file) | freshness or rotation assertion, last-write timestamp | whole-file sha256 |

Measured: a public integrity manifest pinned the sha256 of a ledger appended to on every seal, plus
a live log and the generator script itself. Three of ~63 entries failed on every verification — the
ledger because it had *grown*, the log because it is *live*, the generator because it was *edited*
after the pin. Nothing was tampered with; the manifest was demanding that growing objects hold
still.

**Why the wrong one is worse than none:** a check that is red by construction is a check that gets
ignored, and it spends the signal that would have caught a real break. Three expected failures train
the reader to skip the fourth.

For an append-only store the honest check is over a **committed prefix**: record
`(entry_count, chain_head_digest)` at a declared point, then verify that prefix still matches while
permitting the tail to grow. That catches the two things a whole-file hash was reaching for —
retroactive edit and truncation — and it can actually pass.

When you find a manifest failing this way, classify each mismatch before naming a cause: grown,
edited and live are three different facts, and only one of them is a security event. Report the class
of each failed entry rather than a single verdict over the manifest.

## Routing is a chain, not a field

```
INTENT → CONFIG → RESOLVED → DELIVERED
```

Four independent steps, each able to fail alone. `last_status: ok` proves the process exited;
it does not prove a human received anything — a green status is an exit code wearing a
friendlier name. Only a delivery receipt, naming the destination AND the provider's message
id, closes the chain. Without one, the honest label is **SENT-unconfirmed**, not DELIVERED.

See `references/routing-evidence.md` for the host-layer enumeration and the id-resolution traps.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| Claim in prose/commit only | Register artifact, record claim, re-hash on verify |
| "Verified" with no re-hash | `recheck_artifact=true`; report the live digest |
| Editing a claim to fix it | New claim with `supersedes_claim_id` |
| Omitting what you do not know | Record it as VOID with confidence 0.0 |
| Rewriting a stale seal | Append ORIGINAL / COUNTEREVIDENCE / CORRECTION |
| Sealing a mutable file as final | Content-address it, or re-seal after the change |
| Whole-file hash pinned over a growing ledger | Pin the chain invariant or a committed prefix |
| `status: ok` read as delivered | Require a receipt; else SENT-unconfirmed |
| Building a second ledger | Check for an existing store first |
