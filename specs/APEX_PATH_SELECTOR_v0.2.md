# APEX Path Selector v0.2 — three-phase: ART → APEX → ACT

> ## ⚠ DEPRECATED 2026-08-27 — superseded by [`APEX_PATH_SELECTOR_v0.3.md`](./APEX_PATH_SELECTOR_v0.3.md)
>
> **Status:** DEPRECATED (kept as iteration history, not deleted)
> **Superseded by:** `APEX_PATH_SELECTOR_v0.3.md` — adds P-split + EFE mapping + sovereignty axis.
> **Reason for deprecation:**
> 1. Treated P as a single boundary — missed that P has TWO roles (veto + legitimacy). Pure geometric mean with single-P boundary has a fail-OPEN hole.
> 2. No formal anchor to Active Inference / Expected Free Energy — math looked invented rather than derived.
> 3. Did not formalize that P has no physics analog — sovereignty is arifOS-specific, not cosplay.
>
> **Legacy content below retained for traceability.** v0.2's core insight (geometric mean + ART/APEX/ACT) lives on in v0.3 §1–3. Do not implement against v0.2.

---

**LEGACY CONTENT BELOW**

> **Status (when live):** DRAFT (F13 SEAL pending, never issued)
> **Authority (when live):** ARIF F13 SOVEREIGN, restructured 2026-08-27
> **Supersedes (when live):** `ROUTING_FIELD_v0.1.md` (DEPRECATED 2026-08-27)
> **SOT anchor:** Jauhari-Manikam APEX Doctrine (2026-08-20) — `G = (A·P·E·X)^(1/4)`
> **Reversibility:** Doc-only. No runtime mutation until v1.0 SEAL.
> **DITEMPA BUKAN DIBERI**

---

## 0. Iteration history (honest archaeology)

| Version | Frame | Mistake |
|---|---|---|
| v0 | Contradiction Functional C(path) | GEOX-flavoured name; topology wrong (conflated binary + magnitude) |
| v0.1 | Routing Field (AUTH/FIELD/DEBT pipeline) | Right three-object structure, but **invented APEX-adjacent math** instead of citing existing doctrine |
| **v0.2** | **APEX Path Selector (ART → APEX → ACT)** | Cites Jauhari-Manikam. Topology = arifOS layers. No new equation invented. |

The primitive we were searching for was already ratified 2026-08-20 as `G = (A·P·E·X)^(1/4)`. v0.2 integrates it as the Capability Graph Level 4 router.

---

## 1. Big picture — APEX is a field, not a node

```
ART (Capability Graph)         →    APEX (selection field)    →    ACT (EXECUTE)
       ↓                                ↓                              ↓
   morphology                      evaluation field               metabolism
   what can happen                what should happen              what does happen
```

**APEX is not a node IN the graph.** APEX is the field that bends the graph. River isn't terrain — river flows *because of* terrain. Capability flow occurs because of APEX.

**Maps to arifOS phases:**

```
333 (propose)   →   555 (challenge)   →   888 (synthesize)   →   A-FORGE (execute)
   ↓                   ↓                      ↓                       ↓
  ART                 JUDGE                  SEAL                     ACT
 generate           evaluate              confirm                    execute
```

---

## 2. The canonical example

Goal: **Deploy GEOX**

| Path | Steps | A | P | E | X | G | Result |
|------|-------|---|---|---|---|---|--------|
| A | Deploy | 0.4 | 1.0 | 0.3 | 0.9 | 0.47 | rejected |
| **B** | **Verify → Deploy** | **0.8** | **1.0** | **0.8** | **0.6** | **0.79** | **selected** |
| C | Verify → Test → Deploy | 0.9 | 1.0 | 0.95 | 0.1 | 0.45 | rejected |

Path B wins. **Not** contradiction-min (A has lower F-cost), **not** auth-max (all P=1.0), but **APEX optimum** — best balance of coherence (A), evidence (E), and exploration (X).

---

## 3. The equation — cite APEX, don't reinvent

Per Jauhari-Manikam (2026-08-20):

```
P is a boundary condition. G is defined only when P > P_min.

G(path) = ( mean_step(A) · mean_step(E) · mean_step(X) )^(1/3)    if every step P_i > P_min
        = HOLD                                                     otherwise
```

Each dimension ∈ [0, 1] bounded. Geometric mean chosen over weighted sum because constitutional routing demands **multiplicative zero** — one missing dimension ≠ "0.30 cost", it = HOLD.

---

## 4. Implementation — three faces of APEX

A, P, E, X evaluations produced by three runtime objects (the same three objects v0.1 named, now re-derived from APEX dimensions):

### 4.1 AUTH — P boundary (binary)

```
AUTH(p) = PASS  iff every step P_i > P_min
        = BLOCK iff any step P_i ≤ P_min
```

BLOCK → path HELD. APEX evaluation never reached.

### 4.2 FIELD — geometric mean (scalar ∈ [0, 1])

When AUTH = PASS, compute `FIELD(p) = G(p)`.

| FIELD verdict | Pipeline effect |
|---|---|
| `G ≥ 0.50` | HOLD (SABAR) |
| `0.20 ≤ G < 0.50` | SEEK (PERHATI) |
| `G < 0.20` | PROCEED (TAMAT) |

Thresholds inherited from `gate-promotion.md`.

### 4.3 DEBT — Law #5 reflection loop

```
Reality_Debt(p)    = Σ_24h Execute(p) − Σ_24h Verify(p)
Opportunity_Debt(p) = Σ_24h Verify(p)  − Σ_24h Execute(p)
```

DEBT verdict: BALANCED | OVER-EXECUTE | OVER-VERIFY. Modulates, never blocks. Live read on `:7073/ingest`.

---

## 5. Combined verdict

```
argmax_p G(p)   subject to:
  AUTH(p) = PASS                                   (P boundary intact)
  DEBT(p) ∈ {BALANCED, OVER-VERIFY}               (don't execute during OVER-EXECUTE)
```

Tied paths break by recency (newest evidence preferred).

---

## 6. Path input schema

```json
{
  "path_id": "uuid",
  "actor_id": "fi003-qwen-code",
  "P_min": 0.5,
  "steps": [
    {
      "step_id": "s1",
      "capability_id": "arif_judge",
      "A": {"value": 0.8, "evidence": ["step_clarity_score"]},
      "P": {"value": 1.0, "evidence": ["sct:abc"]},
      "E": {"value": 0.85, "evidence": ["ref:doc1"]},
      "X": {"value": 0.6, "evidence": ["verified_at:2026-08-27"]}
    }
  ]
}
```

Structured inputs. **No LLM in the loop.** RRR-level purity.

---

## 7. Properties

| # | Property | Justification |
|---|----------|---------------|
| P1 | Bounded | Geometric mean of [0,1] inputs ∈ [0,1] |
| P2 | APEX-monotonic | Tightening any dimension can only lower G(p) or hold |
| P3 | Constitutional | P_min gate enforces floor violations as boundary |
| P4 | LLM-free | Structured inputs; recomputable by hand |
| P5 | Doctrine-anchored | Cites Jauhari-Manikam as SOT, no new equation |
| P6 | DEBT modulates | Reflection loop observes; does not refuse |
| P7 | Multiplicative zero | One dim = 0 ⇒ G(p) = 0, no partial credit |

---

## 8. Open questions for F13

| # | Question | Default if no answer |
|---|----------|----------------------|
| **OQ1** | **How is A (AKAL) computed per step?** | **UNDEFINED — load-bearing** |
| OQ2 | Is P_min global or per-capability? | per-capability (card carries P_min) |
| OQ3 | DEBT window size? | 24 h |
| OQ4 | Path tiebreaker? | recency |
| OQ5 | Expose APEX router as MCP tool `apex_score_path` or kernel-internal? | kernel-internal for v1 |

**OQ1 is the load-bearing question.** A (AKAL) has no canonical implementation. Until OQ1 closes, `G(p)` can be computed but its `A` term is hand-waved.

---

## 9. Implementation path

| Stage | Artifact | Anchored to |
|-------|----------|-------------|
| v0.2 | This spec | — |
| v0.3 | `/root/arifOS/arifosmcp/apex_selector.py` (~150 lines, LLM-free) | capability dispatch |
| v0.4 | `/root/arifOS/tests/test_apex_selector.py` (T1–T6 falsification) | kernel test harness |
| v0.5 | Wire AUTH check against F13 + agency-level registry | governance kernel |
| v0.6 | Wire DEBT live-stream from `:7073/ingest` | FQ stabilizer |
| v0.7 | Shadow mode: APEX shadow matches kernel verdicts | capability dispatch |
| v1.0 | SEAL: shadow matches kernel on 1000 live routes | F13 required |

All git-add only. NOT to `/opt/arifos/` until SEAL.

---

## 10. Anchors

- **APEX (SOT):** `/root/.qwen/projects/-root/memory/project-jauhari-manikam-apex-doctrine.md`
- **AGENCY_LEVELS (L0–L6):** `/root/AAA/governance/AGENCY_LEVELS.md`
- **Constitution (F1–F13):** `/root/AAA/instructions/constitution.md`
- **Gate promotion (0.20/0.50):** `/root/AAA/instructions/gate-promotion.md`
- **FQ / Reality-Opportunity Debt:** `/root/.qwen/projects/-root/memory/project-ariflow-fq-dynamics.md`
- **K-2 asymmetric degradation:** `/root/.qwen/projects/-root/memory/project-kernel-eurekas-from-aforge-directives.md`
- **4-Layer Architecture (333/555/888/A-FORGE):** `/root/.qwen/projects/-root/memory/project-4layer-architecture.md`
- **Recon that started the arc:** `/root/HERMES/plans/2026-08-06_1800-kernel-contradictions-recon.md`
- **v0.1 (DEPRECATED):** `/root/AAA/specs/ROUTING_FIELD_v0.1.md`
- **v0 (DEPRECATED):** `/root/AAA/specs/CONTRADICTION_FUNCTIONAL_v0.md`

---

## 11. Reversibility

This is `v0.2`. Amend via version bump. VOID via `APEX_PATH_SELECTOR_v0.2.VOID.md`.

All predecessors preserved with deprecation banners. Iteration history is kept, not deleted.

DITEMPA BUKAN DIBERI.