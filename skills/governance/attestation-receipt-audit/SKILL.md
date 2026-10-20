---
name: attestation-receipt-audit
description: "Use when a published receipt must be grounded."
version: 1.0.0
risk_tier: low
floor_scope: [F2, F11]
autonomy_tier: T1
---

# Attestation Receipt Audit

An attestation is only worth what a stranger can re-derive from it. When the principal drops a public
page, a hash, a status badge, or another agent's system report and expects a reaction, the deliverable
is not agreement or rebuttal — it is **which parts reproduced, which parts did not, and the command
that decided it**.

Scope: published surfaces that assert receipts (identity digests, `/health` fields, vault seals, tool
counts, generated manifests), and relayed reports claiming the same. Repairing the surfaces themselves
is a different lane.

## Procedure

1. **Run the artifact's own verification instruction first.** If it says "fetch X and compare Y", do
   exactly that, from the reader's seat — external URL, no operator context, no localhost shortcut. A
   page that wrote its own test and fails it is the highest-value finding available.
2. **Split the remainder into atomic claims.** One row each: digest matches / field exists / endpoint
   returns the shape described / object exists / count equals N / side effect happens. No row bundles two.
3. **Probe cheapest-to-most-expensive, read-only.** Keep raw output; a claim without its command is
   another claim.
4. **Re-label every row** VERIFIED / FALSIFIED / PARTIAL / UNVERIFIED, with the probe beside it.
5. **Group the verdicts under plain words**, then give at most ONE next step. Do not offer a menu.

## The three claim classes that fail most often

### 1. A verification instruction the public edge cannot satisfy

A page claiming "check the `identity_hash` field at `/health`" is falsified when the external endpoint
returns a bare status object and the field exists only in the operator's loopback payload. Probe the
URL the reader would use. A field only the operator can see is not published, however complete the
internal view looks.

### 2. A digest that is correct and hashes the wrong object

An identity hash can survive a refactor that replaced the file with a pointer stub. Before calling a
mismatch tampering, `wc -c` and `head -3` every same-named copy: a valid digest of a 101-byte "this file
is superseded by X" note is not a digest of the constitution. The defect is the refactor, not the hash.
Then name which copy the runtime reports — the interesting result is usually *which* of the three
copies carries the published digest.

BLAKE3 is `pip install blake3` then `blake3.blake3(open(p,'rb').read()).hexdigest()` — `b3sum` is not
in coreutils. Publish the command beside any digest you quote, or you have asked for trust instead of
a check.

### 3. A count with no denominator

`entries`, `canonical entries`, `chain length`, `sealed receipts` are four counters on one store. A
report, a README and a live endpoint will each quote a different one and each be internally honest.
Pin the field name and the observation timestamp before repeating any of them. When two disagree the
finding is **one object, N numbers** — a provenance defect, not a stale copy — and it matters more
than the number itself.

## Chain-state claims need the chain's own verifier

A footer saying `SEAL ALIVE` is a claim; the verifier behind it is the witness. Call it — endpoints of
that shape return `verified`, `chain_status`, `gap_count`, gaps with class and mechanism, and last-seal
age. Quote those fields. A chain reporting `gaps-found` with a hash mismatch and a signature failure at
one sequence number is **broken at that number**, not "mostly fine" because the rest verifies.
Staleness in hours belongs in the same sentence as the verdict.

## A regenerated surface is not a repaired one

When a generator rewrites a published artifact (`llms.txt`, a manifest, a compiled index), audit the
writer and the cost, not the churn:

1. **Attribute the writer from evidence** — `ls -la --time-style=full-iso <file>`, the service journal
   line identifying the calling client in that minute, and which siblings moved together in
   `git status --porcelain`. Never guess at a writer you can identify.
2. **Read `git diff --stat` for LOSS.** A generator that knows only a subset of the surface makes
   deletions, not edits: a hand-curated capability graph flattened into a list is content loss in the
   exact file external agents use to discover the project. Churn is cosmetic; shrinkage weakens a
   published claim.
3. **Repair at the writer.** Hand-editing a regenerated file guarantees the fix is erased on the next
   run; constrain where the generator may write, or fix what it reads.

## When the input is another agent's report

- **A self-critical report earns credit, not verification.** A report that names its own mistakes and
  marks what it did not measure reads as trustworthy — and that register is exactly how its remaining
  claims slip through. Humility is a writing style, not a receipt. Grade the self-criticism as one more
  claim: an author who found five of his own bugs has not thereby seen the sixth.
- **A named artefact you cannot locate is a planning error.** When the report says "apply commit `X`",
  run `git cat-file -t <sha>` in every repo on the host and a path search for any named file, before
  repeating the step. A plan row resting on an identifier that exists nowhere on the machine is fantasy
  work — and deleting that row IS the correction. Say "the object does not exist here", not "I have not
  found it yet".
- **A dated count invites re-measurement.** "Last recorded in <month>" marks a snapshot. Probe live;
  the finding is usually not "the report is wrong" but "one object now carries N numbers".
- **Do not audit only the defects the report already admits.** The admitted set is the author's own
  visibility, not the defect class. Sweep the same claim type for a sibling instance.

## Reporting shape (this user)

- Plain BM, short, direct. Group under verdict words — **betul**, **lebih teruk**, **tak wujud**,
  **basi** — rather than a methodology section.
- Name the correction, not the process. No preamble, no congratulation, no restating the pasted text.
- One next step, and it must close the cause rather than the symptom. Never a menu.
- Any command the principal must copy goes in a fenced block, one block per command.
- Stop after the step. A closing question is noise.

## Pitfalls

- **Do not let `{"status":"ok"}` pass as constitutional health.** Transport liveness and governance
  health are different layers; report both, name which one you measured.
- **A contradiction inside one payload is a finding in itself** — the same object returning both HOLD
  and SEAL, or a badge and a verifier disagreeing, is a defect of the same class as a wrong number.
- **Do not repair a badge unilaterally when it is mirrored across surfaces.** One edit leaves the
  estate inconsistent; editing all of them is a brand decision above the repair lane. Present it as one
  binary with the contradicting witness and let the principal choose.
- **Recompute; never quote the page's own digest back as your verification.** Repeating a hash is not
  checking it.
- **A missing hit is UNVERIFIED, not absent.** Widen the search across all schedulers, both path roots
  and hidden variants before concluding a thing does not exist.

*DITEMPA BUKAN DIBERI*
