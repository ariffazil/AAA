---
name: geox-basin-claims-audit
description: Use when auditing GEOX basin claims or knowledge.
tags: [geox, audit, claims, provenance, sabah, malay-basin]
---

# GEOX Basin Claims & Audit

Two jobs: (a) register basin claims so later results land against records, (b) audit GEOX
artifacts without overclaiming. Both were done end-to-end on 2026-09-15; the traps below
were all hit live.

## 1. Where things live

- **Claim stores (file lane):** `/root/GEOX/resources/basins/<basin>/claims.json`
  (`sabah_basin`, `malay_basin`). This is the working write path.
- **Deploy split:** repo `/root/GEOX` vs live `/opt/geox` — `/opt/geox` is the
  `WorkingDirectory` of the live `geox-mcp.service`. **Verify both.** Resource files were
  byte-identical while `src/` had drifted (repo ahead of deploy). A defect can serve live
  while the repo diff looks clean, and vice versa.
- **Live surface:** `/health` on the MCP port self-reports `git_version`. Compare it to
  repo HEAD before claiming what is deployed.
- **Signing lane:** `127.0.0.1:18900` (`status ok`, `key_loaded true`) is the path to
  raising actor authority.

## 2. Registering a claim (file lane)

`geox_claim` (MCP) requires OPERATOR authority. An unverified actor gets
`AUTHORITY_GATE · HOLD` with `OBSERVE_ONLY` — **correct behaviour, not a blocker.** Report
it as such (constitution working) and use the file lane instead.

Match the existing file style. Core fields:

```json
{
  "claim_id": "CLM-XXX-00N",
  "claim": "one-paragraph statement",
  "claim_type": "observed|derived|interpreted|hypothesis|other",
  "confidence_prior": 0.45,
  "confidence": "LOW|MEDIUM|HIGH",
  "valid_until": "YYYY-MM-DD",
  "forbidden_uses": ["site_specific_drilling", "commercial_resource_estimate"],
  "evidence_refs": ["basin_profile.yaml"],
  "source": "Author Year | Author Year",
  "metadata": {
    "evidence_for": [],
    "evidence_against": [],
    "missing_tests": [],
    "uncertainty_band": {"p10": 0.0, "p50": 0.0, "p90": 0.0, "basis": "..."},
    "falsifier": "...",
    "registered_at": "YYYY-MM-DD",
    "registered_by": "..."
  }
}
```

Rules:

- **Append textually; never re-serialise the whole file.** Read the raw text, insert before
  the closing `]`, write back. A full `json.dump` reformats every existing entry and shows
  up as mass deletions.
- **Verify with `git diff --numstat`.** Expect `N 0`. Any deleted line other than the
  moved `]` is a reformat — revert and redo. Then parse the file and compare the original
  entries canonically (`json.dumps(..., sort_keys=True)`) to prove zero content loss.
- Every claim needs a **falsifier** and a **missing test**. A claim without one is prose.
- A decision test is itself registrable as a claim — include its blockers and an explicit
  `auto_upgrade_condition` so the record lifts itself when the input lands.
- **Flag a-priori brackets honestly.** If the source published no numeric value, write
  `"basis": "QUALITATIVE_ONLY — p50 is an a-priori bracket, not a derived estimate"`.
  Never dress a guess as a posterior.

## 3. Contradiction discipline (two traps, both hit)

Both looked like a "three-way contradiction" and neither was.

**Trap A — an orphan string is not a contradiction.** A number in exactly one free-text
note can look like a source disagreeing with three others. Grep the **whole repo** for the
disputed figure first. `10-13.7 Ma` appeared once, in a notes list, while a sibling module
in the same package used the correct `7.85 Ma`, and the ledger/dossier split
(melt onset 9.5 / emplacement 7.0) was internally coherent. The fix was one line, not a
modelling dispute. **Check sibling modules before escalating severity.**

**Trap B — confirm the figure exists inside the federation before blaming the federation.**
If an external document cites a value the federation contains nowhere (`grep` → zero hits),
that document is the outlier. The remedy is tagging the document, not repairing the organ.

Corollary: **two agreeing internal sources beat one loud external one.** When internal
sources agree with each other and disagree with a single external document, say so — the
fix has a different owner, and that changes what work is actually needed.

## 4. Auditing external artifacts

- **Verify citation metadata, not just existence.** A real paper with a wrong journal or
  wrong DOI still means the reference line was never checked. Shape ≠ witness.
- **Provenance labels:** `PROVENANCE_PARTIAL` when authorship is declared but no build
  source exists on the host; `PROVENANCE_ABSENT` when none. Hash the delivered file —
  repeat deliveries are often byte-identical, which is itself evidence.
- **Do not invent corrections.** A corrupted formation name stays flagged until a source
  supports the fix. Corrupt ≠ correctable-without-evidence.
- **Contested ages are disputes, not defects.** Register both values with sources; do not
  patch to one number — that manufactures false precision.
- **Check internal self-contradiction:** a field whose value contradicts its own comment,
  and capacity/units figures that disagree across a document's own sections.
- **Retract your own overclaim in writing.** When a later probe shows an earlier flag was
  wrong, say so plainly and state what changed the judgement. Silence here is drift.

## Pitfalls

- Declaring a tool missing because a protocol probe returned an empty list — an era or
  transport mismatch is not absence. Check the deployed source filesystem instead.
- Treating a "the code is written" claim as a runnable tool. Search for the executable.
  A dataclass with a `PENDING` slot is a placeholder, not a test.
- Editing a sealed ledger or an untraced code path. Sealed-refresh and deprecation are F13
  authority boundaries — produce apply-ready patches and HOLD.
- Deleting a superseded file to resolve two contradictory models. That destroys the audit
  trail proving the defect existed — mark DEPRECATED with a pointer instead.
- Assuming a findings bundle is the deliverable. The mutation footprint, the holds, and the
  decisions still owed to the sovereign are what close the work.
