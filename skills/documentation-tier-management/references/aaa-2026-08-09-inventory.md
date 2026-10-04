# AAA Docs Entropy Reduction — 2026-08-09

## Context

User asked to map all MD canon files in `/root/AAA/docs/` that should be federated and zen'd to reduce entropy. STATE.md exists at 341L as working SOT (commit `1a046dc3`, then updated to `6641d936` with §16).

## Inventory

| Metric | Count |
|--------|-------|
| Total non-archive `.md` files in `/root/AAA/docs/` | 340 |
| Already tagged (Tier B/C) | 43 |
| Untagged candidates | 297 |
| Tagged for removal | 233 |
| Kept alive | ~107 |

## Classification Applied

**Tier B (FEDERATED → STATE.md):** 22 files stamped
- Philosophy/, doctrine/, canon/ dirs (canon-level truth)

**Tier C (OPERATIONAL):** 21 files stamped
- operations/, contracts/, transport/, geox/, github-canon, agents, human-interface (procedure only)

**Tier D (PROOF):** Untouched
- sessions/, audit-2026-06-06/, receipts/ (session receipts, evidence)

**architecture/:** Left as legacy history (no mass archive)

## Key Eureka Insights Extracted to SURVIVAL_INSIGHTS.md

### E1 — GOVERNED-L3
arifOS is NOT an instance of L3 Evolver. It IS the constitutional answer to the L3 governance gap: a sovereign-braked evolver with rollback (VAULT999), audit (F11), veto (F13) as first-class primitives. Per Chu et al. arXiv 2604.22748.

### E2 — VALIDATOR IS HACKABLE; ONLY THE SOVEREIGN ESCAPES
Putting a judge in the loop makes the judge the new optimization target. The ONLY component escaping gradient hacking is what's outside the gradient: the human sovereign (F13). This proves F13-over-APEX topology is correct by argument, not fiat.

### E3 — TWO-AXIS ROUTING GATE v2
Route to smallest capability whose *per-step error does not compound* beyond acceptable levels over task step count. Axis 1: Capability Boundary (HARD). Axis 2: Error-Accumulation Boundary (SOFT).

### E4 — 80/20 SOVEREIGN INVARIANT
The law layer is 2% of codebase but determines 80% of outcomes. Arif is 1% of commits but decides everything. The constitution IS the Pareto optimization.

### E5 — T-000 SEAM 4 HOLD
Energy double-counting defect in APEX calculus: Seam 4 treats Energy appearing twice in GM vs once in derivative chain. Engineering debt, not resolved.

## What User Vetoed

- **Merging 329 files into STATE.md** — too large, loses separation of powers
- **Mass archiving architecture/** — optional later, not urgent
- **Bulk deleting without extracting** — insights survive in SURVIVAL_INSIGHTS.md

## Commit Chain

| Commit | Message |
|--------|---------|
| 1a046dc3 | STATE.md unified (365L, §16 added) |
| 6641d936 | 4-tier docs entropy classification |
| 8c9e29c7 | 233 files tagged + SURVIVAL_INSIGHTS.md extracted |
