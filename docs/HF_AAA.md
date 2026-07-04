# HF AAA — Card Expansion: Six Doctrine-Required Gates

> **Forged 2026-06-02 18:41 UTC under F13 SOVEREIGN ratification.**
> This is a documentation-only deliverable. It expands the existing HF AAA dataset card (`huggingface.co/datasets/ariffazil/AAA`) with the six gates that the doctrine we just ratified requires but the current A-RIF gate list does not cover.
> **To apply:** either (a) edit the HF dataset card directly on huggingface.co, or (b) add these gates to `AAA-hf-staging/` before triggering the GitHub workflow `/.github/workflows/push-to-huggingface.yml` (which requires typing `DITEMPA` to confirm).

---

## Current gate set (six — all floor-compliant)

Per the existing HF AAA dataset card, A-RIF already has:

| Gate | Floor served | Status |
|---|---|---|
| Truth verification | F2 Truth | ✅ |
| Context budget | F1 AMANAH (anti-cascade) | ✅ |
| Injection scanning | F1 AMANAH (security) | ✅ |
| Drift monitoring | F1 AMANAH (anti-cascade) | ✅ |
| Provenance binding | F2 Truth + receipts | ✅ |
| Regression testing | F7 Epistemic + F1 | ✅ |

These six are correct and required. Keep them.

---

## The six doctrine-required gates (missing)

The doctrine we just ratified — `arifOS/docs/CORE_INVARIANTS.md`, `AUTHORITY_MODEL.md`, `VERDICT_SEMANTICS.md` — exposes six more gates that the HF AAA dataset card must disclose. Without them, the canon is structurally incomplete and the A-RIF substrate can overclaim in ways the doctrine forbids.

### Gate 7 — Namespaced-seal check

**Purpose:** Reject any retrieved canon clause that uses bare `SEAL`, "verified", "authorized", "approved", or "healthy" without the namespaced context the doctrine requires.

**Why it matters:** Per `VERDICT_SEMANTICS.md`, "SEAL" must be one of: `KERNEL_SEAL_AWARENESS`, `DOMAIN_SEAL_VALIDITY`, `JUDGE_SEAL_AUTHORIZATION`, `VAULT999_SEAL_RECORD`, `PUBLIC_SEAL_READINESS`. A canon clause that says "this canon proves X is SEAL" is overclaim. The check rejects such clauses at retrieval time.

**Implementation hook:** a pre-filter on the BGE-M3 retrieval output, before the clause is passed to the agent's context window.

**Failure mode:** if a clause is rejected, the agent sees: *"Clause `c_xxx` rejected at gate 7: uses bare 'SEAL' without namespaced context. See VERDICT_SEMANTICS.md."* — never the rejected clause itself.

### Gate 8 — Receipt existence check

**Purpose:** Every canon record in `theory/canons.jsonl` (the 186 records) must carry a receipt. The receipt is the provenance: author, version, hash, review trail, ingestion timestamp.

**Why it matters:** Per `CORE_INVARIANTS.md` Invariant 5: "No component may claim more certainty than its evidence receipt." A canon clause without a receipt cannot ground a `KERNEL_SEAL_AWARENESS` claim. The check ensures every record has a receipt OR is explicitly marked `receipt_pending: true` with a target date.

**Implementation hook:** a validation pass on dataset load. Records without receipts are quarantined, not exposed to retrieval.

**Failure mode:** if 5 of 186 records lack receipts, the agent's view is restricted to 181 clauses and the system logs: *"5 canon records quarantined at gate 8: missing receipts. See `quarantine/g8_2026_06_02.jsonl`."*

### Gate 9 — Non-overclaim scan

**Purpose:** Reject canon clauses whose phrasing overclaims. The scan checks for patterns like:
- "This proves X" (overclaim — change to "this is the standard against which X is evaluated")
- "X is verified" (overclaim — change to "X is documented" or "X has receipts")
- "X is true" (overclaim — change to "X is canon" or "X is the federation's position")
- "X is approved" (overclaim — change to "X is admissible for judge")

**Why it matters:** the canon is the law the kernel reads. If the law itself overclaims, the kernel overclaims. This gate keeps the canon honest at the phrasal level.

**Implementation hook:** a regex + curated-pattern scan on dataset load. Overclaim patterns and their replacements are versioned in `arifOS/docs/seals/overclaim_patterns.yaml`.

**Failure mode:** flagged clauses are auto-suggested for rewording. The agent does not see the original phrasing; it sees: *"Clause `c_xxx` flagged at gate 9: overclaim pattern. Suggested rewrite: '...'. Author review required."*

### Gate 10 — Reversibility-of-action classifier

**Purpose:** When a canon clause is used to **justify an action** (not just inform a view), the action's reversibility must be checked against the clause's authority scope.

| Clause authority scope | Acceptable action reversibility |
|---|---|
| `advisory` | any |
| `decision_support` | ≥ 0.70 (reversible) |
| `execution_authorization` | ≥ 0.85 (highly reversible) — *but execution authorization canon clauses are themselves an anti-pattern* |
| `apex_only` | any reversibility, but the action MUST have APEX approval |

**Why it matters:** a canon clause is reference material. It does not, by itself, authorize action. When a clause is being *used* to justify an action, the gate ensures the action's reversibility matches the clause's authority scope. An "advisory" canon clause cannot ground an irreversible deploy.

**Implementation hook:** a check at the moment an agent proposes an action that references a canon clause. The clause's authority scope is in the record metadata.

**Failure mode:** if a clause is misused, the action is held: *"Action `a_xxx` references canon clause `c_yyy` of scope 'advisory' but proposes an irreversible deploy. Gate 10 hold. Reframe: either choose a more authoritative clause or increase action reversibility."*

### Gate 11 — APEX-tier gate

**Purpose:** A subset of canon clauses are marked `requires_apex: true`. Retrieval of these clauses does not trigger free use — it triggers a HOLD notification.

**Why it matters:** some clauses touch APEX-anchored territory (F13 SOVEREIGN, identity, override authority, data sovereignty). An agent reading these clauses is reading law that requires human authority to apply. The gate surfaces that.

**Implementation hook:** an attribute on the canon record. Retrieval of an APEX-tier clause emits a HOLD to the AAA approval queue, with the clause attached.

**Failure mode:** the agent sees: *"Clause `c_xxx` is APEX-tier. This clause is read-only in this context. To apply, raise a HOLD with APEX. (Gate 11 active.)"*

### Gate 12 — VAULT999 lineage check

**Purpose:** A canon clause that has been amended must show its lineage — what it replaced, when, by whom, with what review trail.

**Why it matters:** without lineage, an agent cannot know whether a canon clause is current. A clause replaced in 2026-05-27 but still in the dataset is misleading. The gate enforces visible lineage.

**Implementation hook:** every canon record carries a `lineage` field: `{ replaces: ["c_xxx"], replaced_by: null, amendments: [{ date, author, summary, review_trail_hash }] }`. A clause with `replaced_by` set is excluded from retrieval.

**Failure mode:** superseded clauses are not retrieved. The lineage is queryable for audit.

---

## Updated gate table (6 + 6 = 12)

| # | Gate | Floor | Doctrine status |
|---|---|---|---|
| 1 | Truth verification | F2 | ✅ existing |
| 2 | Context budget | F1 | ✅ existing |
| 3 | Injection scanning | F1 | ✅ existing |
| 4 | Drift monitoring | F1 | ✅ existing |
| 5 | Provenance binding | F2 | ✅ existing |
| 6 | Regression testing | F7, F1 | ✅ existing |
| 7 | Namespaced-seal check | VERDICT_SEMANTICS | 🆕 required |
| 8 | Receipt existence check | Invariant 5 | 🆕 required |
| 9 | Non-overclaim scan | Invariant 1, 2, 5 | 🆕 required |
| 10 | Reversibility-of-action classifier | AUTHORITY_MODEL | 🆕 required |
| 11 | APEX-tier gate | AUTHORITY_MODEL | 🆕 required |
| 12 | VAULT999 lineage check | Invariant 4, VAULT | 🆕 required |

---

## Suggested dataset card addition

Add a new section to the HF AAA dataset card titled **"Doctrine-Required Gates (12 total)"** with the table above and the following summary:

> The A-RIF substrate is gated by twelve rules. Six cover retrieval integrity (truth, context, injection, drift, provenance, regression). Six cover constitutional compliance (namespaced-seal, receipt, non-overclaim, reversibility, APEX-tier, VAULT999-lineage). All twelve are required for any canon clause to be admissible as evidence in an arifOS deliberation. A clause that fails any gate is quarantined; the agent never sees it as authoritative.

---

## How to apply this expansion

Two paths:

**Path A — Direct edit on huggingface.co:** open the dataset page for `ariffazil/AAA`, edit the README, paste the new section. Commit. Done.

**Path B — Via the GitHub workflow:** add the new gate documentation to `AAA-hf-staging/` (e.g., as `docs/GATES.md`), then trigger `.github/workflows/push-to-huggingface.yml` from the GitHub Actions tab. The workflow requires typing `DITEMPA` to confirm. The 11 files get pushed as one commit.

Either path is acceptable. Path B is preferable because it keeps the gates versioned alongside the data.

---

**DITEMPA BUKAN DIBERI — Forged, Not Given.**
