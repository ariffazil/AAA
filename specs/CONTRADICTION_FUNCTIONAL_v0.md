# Contradiction Functional v0 — `C(path) → ℝ`

> ## ⚠ DEPRECATED 2026-08-27 — superseded by [`ROUTING_FIELD_v0.1.md`](./ROUTING_FIELD_v0.1.md)
>
> **Status:** DEPRECATED (kept as iteration history, not deleted)
> **Superseded by:** `ROUTING_FIELD_v0.1.md` — three-object pipeline (AUTH · FIELD · DEBT)
> **Reason for deprecation:**
> 1. Naming was GEOX-coloured — "contradiction" smuggled geological epistemology into arifOS
> 2. Topology was wrong — four signals of different cardinalities mashed into one scalar
> 3. v0 missed three live arifOS primitives (APEX P boundary, Law #5 Debt, FQ exec:verify)
>
> **This file is preserved** for traceability — the math in §3 holds but the framing in §0–2 is obsolete. Do not implement against v0. Read v0.1.

---

**LEGACY CONTENT BELOW — retained for history only**

> **Status (when live):** DRAFT (F13 SEAL pending, never issued)
> **Authority (when live):** ARIF F13 SOVEREIGN, ratified from musyawarah 2026-08-27
> **Scope (when live):** All capability routing in arifOS federation. Pre-dispatch gate.
> **Supersedes (when live):** implicit "minimum contradiction" hand-wave in CAPABILITY_GRAPH v0 (HELD)
> **Reversibility (when live):** Doc-only. No runtime mutation until v1.0 SEAL.
> **DITEMPA BUKAN DIBERI**

---

## 1. Why this spec exists

The Capability Graph (proposed L0–L5 ladder, 2026-08-27 dialogue) requires Level 4
(Thermodynamic Routing) to be a **router**, not a metaphor. The bare claim
"route by minimum contradiction" is unfalsifiable until `C(path) → ℝ` is a
concrete scalar with a unit and a computation.

This spec defines that scalar. It is the missing primitive that completes the
four-pillar stack:

```
Inventory (what exists)
    ↓
Capability Graph (what can happen)
    ↓
Governor (what is allowed)
    ↓
C(path) (what should happen next)         ← THIS SPEC
    ↓
Emergent Reality
```

`HERMES/plans/2026-08-06_1800-kernel-contradictions-recon.md` already enumerates
real contradictions C1–C6 in the kernel. None are quantified. This spec turns
enumeration into arithmetic.

---

## 2. Definitions

**path** — Ordered tuple of capability invocations:
`path = [step_1, step_2, …, step_n]`. Empty path = `[]`.

**step** — A single capability invocation:
`step = (capability_id, actor_id, evidence_refs, expected_artefact)`.

**C(path)** — contradiction score, dimensionless ∈ `[0, 1]`. Higher = more
contradiction. Lower = cleaner path.

| Score | Verdict | Gate (per gate-promotion.md) |
|-------|---------|------------------------------|
| `C < 0.20` | FLOW | TAMAT |
| `0.20 ≤ C < 0.50` | SEEK | PERHATI |
| `C ≥ 0.50` | HOLD | SABAR |

Thresholds reuse the same 0.20 / 0.50 boundaries as
`forge-vision-densify` ΔS gate — pattern, not coincidence.

---

## 3. Components

Four orthogonal signals, each ∈ `[0, 1]`. Sum of weights = 1.

### 3.1 F-conflict — Floor Conflict (weight `w_F = 0.40`)

> **Constitutional priority. Highest weight. Floor violation is hard.**

For each step, compute `floor_violation(step) ∈ [0, 1]`:
- `0.0` if step respects all F1–F13 floors
- `1.0` if step directly violates F1 (irreversible deletion) or F9 (consciousness claim)
- `0.5` if step violates F2 (truth), F4 (consent), F10 (ontology boundary)
- `0.3` if step violates F12 (evidence routing), F13 (sovereignty)
- `0.1` if step violates soft floors (F5–F8, F11)

```
F_conflict(path) = max over all steps of floor_violation(step)
```

**Rationale:** max-floor-wins. One F1 violation is enough to void a path;
summing dilutes the constitution. See OQ1 for alternative.

### 3.2 E-gap — Evidence Gap (weight `w_E = 0.25`)

For each step, compute `evidence_coverage(step) ∈ [0, 1]`:
- `1.0` if all declared `evidence_refs` resolve to live, recent, attributed sources
- `0.0` if any required evidence_ref is missing or unresolvable
- linear interpolation otherwise

```
E_gap(path) = 1 - mean over all steps of evidence_coverage(step)
```

### 3.3 A-gap — Authority Gap (weight `w_A = 0.20`)

For each step, compute `authority_match(step) ∈ {0, 1}`:
- `1` if actor's authority level ≥ required authority for capability
- `0` otherwise (no partial credit — authority is binary per session)

```
A_gap(path) = 1 - mean over all steps of authority_match(step)
```

### 3.4 T-drift — Temporal Drift (weight `w_T = 0.15`)

For each step, compute `freshness(step) ∈ [0, 1]`:
- `freshness = exp(-age_hours / 168)` (1-week half-life)
- `age_hours` = hours since capability surface was last verified live

```
T_drift(path) = 1 - mean over all steps of freshness(step)
```

This is the only soft signal. C4 (false-positive drift) from the recon is
absorbed here: `__pycache__` drift does not raise T_drift; runtime capability
drift does.

---

## 4. Formula

```
C(path) = w_F · F_conflict(path)
       + w_E · E_gap(path)
       + w_A · A_gap(path)
       + w_T · T_drift(path)

with weights: w_F = 0.40, w_E = 0.25, w_A = 0.20, w_T = 0.15
              sum = 1.00 ✓
```

**Default weights** are ARIF-ratified. Changing weights requires F13 seal.

---

## 5. Properties (must hold)

| # | Property | Justification |
|---|----------|---------------|
| P1 | Bounded: `0 ≤ C(path) ≤ 1` | All components bounded; convex combination |
| P2 | Monotonic: `path ⊆ path' ⇒ C(path) ≤ C(path')` | Adding a step can only add contradiction |
| P3 | Composable (sequential): `C(p1 ++ p2) = max(C(p1), C(p2))` | Sequential contradiction is worst-part-wins for hard signals; mean for soft. Spec uses max for compositional simplicity. |
| P4 | LLM-free computable | All inputs are structured fields. RRR-level purity: an engineer can recompute C(path) by hand from the inputs. |
| P5 | Constitutional priority | `w_F = max(w)` ensures floor violation dominates any single soft signal |

---

## 6. Falsification tests

v0.1 prototype passes if and only if all 8 tests pass on canonical inputs.

| # | Test | Pass condition |
|---|------|---------------|
| T1 | Identity | `C([]) = 0` |
| T2 | Hard floor | `C([F1-violating step]) ≥ 0.40` (F_conflict alone forces HOLD) |
| T3 | Evidence | `C(no-evidence path) > C(full-evidence path)` all else equal |
| T4 | Monotonicity | For any `path ⊆ path'`, `C(path) ≤ C(path')` |
| T5 | Live vs stale | `C(path using 14-day-old capability) > C(path using 1-hour-old capability)` |
| T6 | Bounded | `0 ≤ C(path) ≤ 1` for 1000 random paths |
| T7 | Composable | `C(p1 ++ p2) = max(C(p1), C(p2))` for 100 random path pairs |
| T8 | Authority | `C(path with wrong actor) > C(path with right actor)`, all else equal |

---

## 7. Why this closes Level 4

| Without C(path) | With C(path) |
|-----------------|--------------|
| "minimum contradiction" = metaphor | `argmin_p C(p)` = concrete objective |
| Constitution check is manual per step | Floor violation auto-HOLDs path |
| Drift is observed, not enforced | T-drift is a routable signal |
| Authority check is best-effort | A-gap forces seek-or-hold |
| Routing collapses to heuristic | Routing is convex optimization over `[0,1]^n` |

---

## 8. Implementation path (reversible, staged)

| Stage | Artifact | Reversibility |
|-------|----------|---------------|
| v0 | This spec | Doc-only. ARIF amends or VOIDs by overwriting. |
| v0.1 | `/root/arifOS/arifosmcp/contradiction.py` (~80 lines, LLM-free) | Add to git, not deployed to `/opt/arifos/` |
| v0.2 | `/root/arifOS/tests/test_contradiction_functional.py` (T1–T8) | Add to git, run via `pytest` |
| v0.3 | Wire into RRR output path (read-only shadow mode) | Reversible flag, log only |
| v1.0 | SEAL: shadow mode matches kernel verdict on 1000 live routes | F13 required |

---

## 9. Open questions for F13

| # | Question | Default if no answer |
|---|----------|----------------------|
| OQ1 | F-conflict: max-floor or sum-of-violations? | max (constitution is hard) |
| OQ2 | A-gap: should A2A delegation chain depth multiply `authority_match`? | No — binary match, depth checked separately |
| OQ3 | T-drift: exponential (`exp(-age/168)`) or step (>7d = stale)? | exponential (smooth, falsifiable) |
| OQ4 | Expose `C(path)` as MCP tool `forge_contradiction_score`? Or kernel-internal? | kernel-internal for v1; expose at v2 |

---

## 10. Anchors

- **Inventory:** `/root/AAA/governance/DEWAN_REGISTRY.yaml`, `/root/.config/federation-models.json`
- **Capability Graph (proposed):** `/root/AAA/governance/CAPABILITY_GRAPH_v0.1.md` (HELD pending this spec SEAL)
- **Governor:** `constitution.md` (F1–F13), `arif_judge` kernel, `gate-promotion.md`
- **Recon that motivated this:** `/root/HERMES/plans/2026-08-06_1800-kernel-contradictions-recon.md` (C1–C6)
- **Related spec:** `/root/AAA/specs/agi_kernel_regression_harness.yaml` (test methodology)

---

## 11. Reversibility note

v0 is a markdown file. To amend, edit and stamp version (`v0.1`, `v0.2`, …).
To VOID, replace with `CONTRADICTION_FUNCTIONAL_v0.VOID.md` containing a single
line: "VOID by F13 ARIF, YYYY-MM-DD, reason: …". No runtime mutation until
v1.0 SEAL.

DITEMPA BUKAN DIBERI.