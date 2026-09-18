---
name: durable-claim-ledger
description: "Use when a claim about system state must stay re-checkable."
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
| `status: ok` read as delivered | Require a receipt; else SENT-unconfirmed |
| Building a second ledger | Check for an existing store first |
