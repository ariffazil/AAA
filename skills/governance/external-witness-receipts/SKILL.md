---
name: external-witness-receipts
description: "Use when a mutation path needs a witness receipt."
version: 1.0.0
author: Hermes
license: arifOS
metadata:
  hermes:
    category: governance
    tags: [witness, receipts, hash-chain, tamper-evidence, self-modification, audit]
    related_skills: [self-improvement-lock, chokepoint-enforcement-audit, durable-claim-ledger, sealed-deliverable-provenance]
triggers:
  - a skill, prompt, doctrine or policy file changed and nobody signed it
  - make this mutation path witnessed / receipted / auditable
  - an audit log lives inside the system it audits
  - wire a control so a later reader can prove what changed, when, and by whom
  - prove this chain/log has not been edited
---

# External Witness Receipts

How to give a mutation path a receipt that survives the system producing it. Design of the lock itself
(what to constrain, which layers, red-teaming) lives in `self-improvement-lock`; the enforcement-boundary
audit lives in `chokepoint-enforcement-audit`. This skill owns the RECEIPT: the seam, the chain, the
off-host mirror, and the four checks that prove it works.

## 1. The defect

An audit ledger written by the same process, in the same tree, compacted by the same code that performs
the mutations is a **diary**. It answers nothing when the question is "did the system change itself and
hide it?". A receipt is only a witness when it is (a) chained, (b) copied somewhere the mutator does not
run, and (c) verifiable by a third party with one command.

## 2. Build, in this order

1. **Find the single writer.** Grep for the writer of the existing audit file. One function that every
   mutation funnels through is the seam; per-call-site hooks are not.
2. **Emitter runs OUT-OF-PROCESS.** The host package gets a three-line call (subprocess to a script you
   own); chain layout, storage paths and verification stay in a reviewable, independently versioned file.
   Vendor updates then cost the hook, not the logic.
3. **Hash-chain the rows.** `hash = sha256(prev + canonical_json(payload))` with `prev` carried in each
   row. Canonicalise (sorted keys, tight separators) or the chain will not reproduce. Keep volatile or
   self-referential fields OUT of the hashed body.
4. **Mirror off-host** — a witness node the audited system does not run on. One row per mutation, sent on
   write.
5. **Mirror status goes in a sidecar, never in the row.** See the pitfall below.
6. **Fail-soft.** The receipt emitter must never break the mutation it observes: catch, log, continue.
   Say plainly in the report that receipts are best-effort telemetry, not a gate — a witness that can
   halt production gets removed the first time it misbehaves.

## 3. Verify in four moves (each one caught a real defect)

1. **Exercise the real path in a fresh interpreter**, then read the chain. Drive the seam with a throwaway
   state dir (`STATE_DIR=/tmp/probe-home …`) so probe rows never land in the production ledger.
2. **Chain verify** — recompute every row; report `CHAIN_OK` / `TAMPERED(row, why)`. Exit non-zero on
   tamper so it can gate CI.
3. **Tamper test on a COPY, never the live chain**: edit one field, expect a content-hash mismatch at
   that row. A verifier that has never failed on known-bad input has not been shown to measure anything.
4. **Byte parity against the mirror** — md5 both sides right after a mirror write and again after any
   backfill. A mirror that silently differs is worse than no mirror: it looks like evidence.

```bash
python3 <emitter>.py emit < entry.json     # one row; also mirrors
python3 <emitter>.py verify                # CHAIN_OK | TAMPERED(row, why)
python3 <emitter>.py backfill              # history -> chain, labelled
python3 <emitter>.py resync                # push whole chain to witness node + report parity
```

## 4. Backfill honestly

Receipting history that predates the chain is fine **if** the rows are labelled as backfill and keep
their ORIGINAL ids and timestamps. Strip those and a backfilled row becomes indistinguishable from a live
receipt. Finish by reconciling local against mirror and reporting the parity result, not a claim.

## 5. Pitfalls (all cost real time)

- **Never rewrite a chain row to record its own state.** The mirror result is unknown when the row is
  written; putting it in the row means re-writing an append-only log — a tamper-shaped write. Sidecar.
- **Append with a terminating newline, and check parity by hash, not `wc -l`.** A mirrored row written
  without the newline merges with the next append: line and byte counts disagree and the mirror has
  quietly become a different file.
- **Shell overrides leak between commands.** An exported test-only state-dir variable stays set for the
  next command, so a later run silently operates on the throwaway target (this read as "nothing to
  backfill" against a 4,000-row ledger). Use inline `VAR=value cmd`, or `unset` in the same command.
- **Wired is not live.** A hook added to a long-running process does nothing until that process restarts.
  Report the path as wired-but-not-live, name the single switch that makes it live, and do not claim
  witnessing until a live mutation has actually produced a row.
- **Test the seam's failure mode, not just its success:** stop the mirror (unreachable host) and confirm
  the row still lands and the sidecar records `local-only(...)`. Silent degradation is the failure to
  catch early.

## 6. Limits to state, never to hide

- **Same-uid privileged processes can still rewrite the chain.** The chain is tamper-EVIDENT, not
  tamper-PROOF; the off-host copy is what makes deletion detectable, and only a parity re-check makes it
  visible.
- Mirror health is pull-verified, not push-guaranteed: nobody is paged when the witness node is down.
  Name that as the next gap rather than implying coverage.
- File permissions are not a lock against a privileged process. The durable fix is a non-root citizen for
  the mutating process, or off-box custody — say which one the current setup lacks.

## 7. Reporting shape

Evidence first: rows produced, chain verdict, parity result, tamper-test result, backfill count — then
what was deliberately left untouched (the working pipeline, the canonical registry: propose, do not
write), then the open gaps with the single switch that closes each. Numbers and verdicts, never
"witnessed" as a bare adjective.
