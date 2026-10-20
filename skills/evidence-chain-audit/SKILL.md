---
name: evidence-chain-audit
description: "Use when auditing claimed evidence artifacts or receipts."
license: Proprietary
platforms: [linux]
---

# Evidence-Chain Audit

Use when a report presents evidence objects, receipts, attestations, citations, or "tests pass" claims that others will trust. A report can be schema-valid, test-green, hash-stamped, and still be built on artifacts that do not exist. Schema validation proves **fields are present and well-typed**; it never proves the **referent exists**. This skill is the existence layer under any provenance, warrant, or receipt system.

## Four existence checks (run all four before trusting a record)

1. **Citation → resolve AND match.** Fetch registered metadata (`https://api.crossref.org/works/<doi>`), then compare title, authors, journal, volume, pages against the citation text. A resolving DOI pointing at an unrelated paper is the worst failure class because it survives every HTTP-200 check.
2. **Hash → check for repetition before trusting it.** `fold -w16 | sort -u` on the hex; a real digest never collapses to one or two unique lines. SHA-256 is 64 hex chars. Never quote a hash you did not compute yourself.
3. **Witness → falsify the environment claim.** `uname -srm` against the reported platform; `ps -o pid=,cmd= -p <pid>` against the reported service. A witness from the wrong hardware, or a PID serving a different binary, voids the execution record entirely.
4. **Test result → run it with the interpreter that serves the service.** Resolve with `readlink /proc/<pid>/exe`; use that venv, not a project-local `.venv` that may be absent or broken. "N passed" from an interpreter that cannot serve the service is not a receipt.

## Three-way separation (do not collapse)

```
artifact identity  ≠  execution evidence  ≠  scientific truth
```

A content hash proves bytes did not change. It does not prove the code ran, and it does not prove the conclusion is true. Keep the three ledgers distinct and say which one each claim lives in.

## Verdict vocabulary

- `EXISTS_MATCHES` — referent resolved and metadata matches the claim.
- `EXISTS_WRONG_ENTITY` — resolved, but a different paper/object/host.
- `FABRICATED_SHAPE` — right syntax, no referent (repeating hash, invented DOI, impossible platform).
- `UNCHECKED` — no probe ran. Never promote to EXISTS by inference.

Report `UNCHECKED` as `UNCHECKED`. "I could not reach it" and "it does not exist" are different findings and must not merge.

## Procedure

1. List every artifact the report depends on (citations, hashes, witnesses, test runs, endpoints).
2. Run the four checks. Batch them; each is seconds.
3. Mark each artifact with the verdict vocabulary.
4. Downgrade every claim whose load-bearing artifact is not `EXISTS_MATCHES`.
5. Propose **one** existence test to add to the pipeline, per artifact class — the fix belongs in the gate, not in prose.

## Pitfalls

- **Format-complete evidence is the failure mode, not the exception.** The most dangerous artifact is not the honestly ugly one; it is the one that looks audited. A polished page lowers scrutiny faster than a rough one raises it.
- **A validator that rejects missing fields will happily accept a fabricated value for a present field.** Add an existence test alongside every completeness test.
- **Category mismatch survives every schema check.** Comparing quantities of different kinds (e.g. an isostatic *root* — deflection below a reference Moho — against a measured Moho *depth*; they differ by the reference thickness) yields a residual that looks quantitative and is meaningless. Re-derive dimensionally before accepting any residual.
- **A witness record is a claim, not proof of execution.** Environment, PID, timing and commit are all checkable; check at least one.
- **Do not retract a whole report over one bad artifact.** Name the specific artifact, keep what survives, put the repair in the gate.
- **Absence of a counter-source is not support.** If you could not read the source, the claim stays `UNCHECKED`, however plausible.

## Reference

- `references/artifact-probe-recipes.md` — copy-paste probes for DOI metadata, hash repetition, witness environment, and interpreter resolution.
