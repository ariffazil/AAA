# APEX Path Selector v0.3 — P-split, EFE mapping, sovereignty axis

> **Status:** DRAFT (F13 SEAL pending)
> **Authority:** ARIF F13 SOVEREIGN, restructured 2026-08-27 (post-ARIF P-split critique + EFE anchor)
> **Supersedes:** `APEX_PATH_SELECTOR_v0.2.md` (DEPRECATED 2026-08-27)
> **SOT anchors:** Jauhari-Manikam APEX Doctrine (2026-08-20) + Active Inference / Expected Free Energy (Friston, Parr)
> **Reversibility:** Doc-only. No runtime mutation until v1.0 SEAL.
> **DITEMPA BUKAN DIBERI**

---

## 0. Iteration history

| Version | Frame | Mistake / Correction |
|---|---|---|
| v0 | Contradiction Functional C(path) | GEOX-flavoured naming |
| v0.1 | Routing Field (3-object pipeline) | Right structure, invented APEX-adjacent math |
| v0.2 | APEX Path Selector (single P as boundary) | Missed P-split (veto + legitimacy); missing EFE anchor |
| **v0.3** | **APEX Path Selector + P-split + EFE mapping + sovereignty axis** | Fail-closed geometric mean; Friston anchor; P has no physics analog |

---

## 1. Big picture — APEX is a ranking function over discrete paths

```
ART (Capability Graph)        →    APEX (ranking function)    →    ACT (EXECUTE)
       ↓                              ↓                              ↓
   morphology                    selection function            metabolism
   what can happen              what should happen             what does happen
```

APEX is not a node IN the graph. APEX is the ranking function over admissible paths. **"Field" metaphor is literal only when capability space is continuous** — today it is discrete, so APEX = ranking function (see §8).

Maps to arifOS canonical phases:

```
333 (propose)        →    555 (challenge)        →    888 (synthesize)        →    A-FORGE (execute)
   ↓                          ↓                          ↓                            ↓
  ART                        JUDGE                      SEAL                          ACT
```

---

## 2. The equation — geometric mean, with P-split

Per Jauhari-Manikam (2026-08-20) **and** Active Inference / Expected Free Energy (Friston):

```
P is BOTH a boundary condition (veto) AND a continuous factor (legitimacy).

P_veto(s)         ∈ {0, 1}                       — binary gate
P_legitimacy(s)   ∈ [0, 1]                       — continuous factor

AUTH(p) = PASS  iff every step P_veto = 1
        = BLOCK iff any step P_veto = 0

When AUTH = PASS:
  G(p) = ( mean_step(A) · mean_step(P_legitimacy) · mean_step(E) · mean_step(X) )^(1/4)
       ∈ [0, 1]
```

**Why P-split is mandatory (ARIF critique 2026-08-27):** Without it, geometric mean has a **fail-OPEN** hole. If only paths with low P_legitimacy remain admissible, `argmax G` still picks "least bad" — that's not fail-closed. Fix: veto role (binary, removes path from admissible set) **before** ranking; legitimacy role (continuous) enters the score.

**Log-space identity (free F13 wall, derived not patched):**

```
ln G = ¼(ln A + ln P_legitimacy + ln E + ln X)

If P_legitimacy → 0, ln P → -∞, so G → 0.
F13 veto wall is DERIVED from geometric mean — not added by hand.
```

ARIF: "Geometric mean kau memberi percuma dinding yang aku kena bina tangan dulu. Bentuk kau lebih elegan."

---

## 3. The canonical example — with P-split

Goal: **Deploy GEOX**

| Path | Steps | A | P_veto | P_legitimacy | E | X | G | Result |
|------|-------|---|----------|---------------|---|---|---|--------|
| A | Deploy | 0.4 | 1 | 0.4 | 0.3 | 0.9 | 0.45 | rejected |
| **B** | **Verify → Deploy** | **0.8** | **1** | **0.8** | **0.8** | **0.6** | **0.74** | **selected** |
| C | Verify → Test → Deploy | 0.9 | 1 | 0.7 | 0.95 | 0.1 | 0.42 | rejected |
| D | Deploy (no F13 seal) | 0.9 | **0** | — | 0.9 | 0.9 | — | **vetoed (AUTH=BLOCK)** |

Path B wins. **Path D never enters ranking** — P_veto = 0 fails AUTH. P-split works.

---

## 4. Active Inference mapping — APEX = EFE + Authority axis

APEX is **Active Inference + Authority axis**. Mapping:

| APEX dim | Friston / EFE term | Meaning |
|---|---|---|
| **A (AKAL)** | Risk / Pragmatic value | `E_Q[D_KL[Q(s|π) ‖ P(s)]]` — divergence from prior preferences |
| **E (ENTROPY)** | Ambiguity (negated → clarity) | `E = 1 − E_Q[H[P(o│s)]]/H_max` — clarity = inverse of expected observation entropy given states. High E = low ambiguity = certain. |
| **X (EXPLORATION)** | Epistemic value | information gain `I[O; S]` — expected reduction in state uncertainty from observations. Future-leaning. |
| **P_legitimacy** | — | **NO PHYSICS ANALOG** — sovereignty axis |
| **P_veto** | — | **NO PHYSICS ANALOG** — pre-filter |

```
EFE(π) = E_Q[D_KL[Q(s|π) ‖ P(s)]]  +  E_Q[H[P(o│s)]]
       = Risk                          +  Ambiguity
       = A                             +  (1 − E)   (in our mapping; E negated = clarity)
```

**E vs X — distinct:**
- E = present clarity = `1 − ambiguity` (state of knowledge now)
- X = future info-gain = `I[O; S]` (learning ahead)

Both relate to uncertainty but at different time orientations. E measures present certainty; X measures expected future learning.

Active Inference is the **3D subset (A, E, X) of APEX**. **P is the 4th axis — sovereignty — that has no Friston analog.** That makes APEX = Active Inference + Authority, not pure physics cosplay.

---

## 5. Implementation objects

### 5.0 P-split (NEW v0.3)

Two distinct P signals per step:
- `P_veto(s)` ∈ {0,1} — binary. From F1-F13 floor check + capability required_authority match.
- `P_legitimacy(s)` ∈ [0,1] — continuous. From authority freshness, consent, prior track record.

### 5.1 AUTH — P_veto gate (binary)

```
AUTH(p) = PASS  iff every step P_veto = 1
        = BLOCK iff any step P_veto = 0
```

BLOCK → path HELD. APEX ranking never reached.

### 5.2 FIELD — geometric mean with P_legitimacy

When AUTH = PASS:
```
FIELD(p) = G(p) = ( mean_step(A) · mean_step(P_legitimacy) · mean_step(E) · mean_step(X) )^(1/4)
                ∈ [0, 1]
```

| FIELD verdict | Effect |
|---|---|
| `G ≥ 0.50` | HOLD (SABAR) |
| `0.20 ≤ G < 0.50` | SEEK (PERHATI) |
| `G < 0.20` | PROCEED (TAMAT) |

### 5.3 DEBT — Law #5 reflection (unchanged)

```
Reality_Debt(p)    = Σ_24h Execute(p) − Σ_24h Verify(p)
Opportunity_Debt(p) = Σ_24h Verify(p)  − Σ_24h Execute(p)
```

### 5.4 SEAL — fail-closed gate (NEW v0.3)

For high blast-radius / irreversible actions, APEX-proposed path ≠ auto-execute.

```
SEAL(p) = PASS  iff DEBT = BALANCED  AND  reversibility_budget covers blast_radius(p)
        = PAUSE  iff irreversible — request F13 override
```

**"Should" is anchored in P (sovereign), not emergent.** APEX cadang, SEAL melupuskan, A-FORGE executes. Organism flows; sovereignty stays axiom.

---

## 6. Combined verdict

```
argmax_p G(p)   subject to:
  AUTH(p) = PASS                    (P_veto intact)
  DEBT(p) ∈ {BALANCED, OVER-VERIFY}
  SEAL(p) = PASS                    (reversibility intact)
```

For irreversible actions: PAUSE + F13 override required even when G is highest. Prevents "organism" from becoming "no accountability".

---

## 7. Path input schema (with P-split)

```json
{
  "path_id": "uuid",
  "actor_id": "fi003-qwen-code",
  "P_veto_min": 1,
  "reversibility_budget": "session",
  "steps": [
    {
      "step_id": "s1",
      "capability_id": "arif_judge",
      "A": {"value": 0.8, "evidence": ["step_clarity_score"]},
      "P_veto": {"value": 1, "evidence": ["f13_floor_check_pass"]},
      "P_legitimacy": {"value": 0.85, "evidence": ["sct:abc", "authority_age"]},
      "E": {"value": 0.85, "evidence": ["ref:doc1"]},
      "X": {"value": 0.6, "evidence": ["verified_at:2026-08-27"]}
    }
  ]
}
```

Structured inputs. **No LLM in the loop.** RRR-level purity.

---

## 8. "Field" is metaphorical today — when it becomes literal

| Today (discrete paths) | Tomorrow (continuous capability space) |
|---|---|
| APEX = ranking function | APEX = scalar potential G(x) |
| `argmax G` over candidates | Geodesic flow down `∇G` |
| Topological sort | Variational principle |
| Discrete ranking | Smooth manifold |

**Don't sell "field" before the space is continuous.** Today: ranking function. Tomorrow (if you smooth capability space): proper field with `∇G` driving geodesic flow.

---

## 9. Status — SEAL-able vs HOLD vs UNKNOWN

| Aspect | Status |
|---|---|
| ART → APEX → ACT architecture | ✅ SEAL-able |
| APEX = geometric mean over paths | ✅ SEAL-able |
| P-split (veto + legitimacy) | ✅ SEAL-able |
| Log-additive form (F13 wall derived, free) | ✅ SEAL-able |
| EFE mapping (A↔Pragmatic, E↔Ambiguity, X↔Epistemic) | ✅ SEAL-able |
| P has no physics analog (sovereignty axiom) | ✅ SEAL-able |
| SEAL gate for irreversible actions | ✅ SEAL-able |
| Exponents α,β,γ,δ = ¼ each (uniform) | ⏳ HOLD (assumption, not law) |
| Content of A (contradiction handling) | ⏳ HOLD |
| Content of X (exploration value) | � UNKNOWN (nested functional) |
| Capability space continuity | ⏳ FUTURE (today: discrete) |

---

## 10. Open questions for F13

| # | Question | Default |
|---|----------|---------|
| OQ1 | How is A (AKAL) computed per step? | UNDEFINED (load-bearing) |
| OQ2 | How is P_veto computed? | F1-F13 floor check + required_authority match |
| OQ3 | How is P_legitimacy derived? | freshness decay × consent × track record |
| OQ4 | How is X (exploration) computed? | UNDEFINED (UNKNOWN, nested functional) |
| OQ5 | SEAL gate blast-radius threshold? | reversibility_budget per session |
| OQ6 | Exponents α,β,γ,δ — uniform ¼ or calibrated? | uniform ¼ (assumption, F13 to override) |

---

## 11. Implementation path

| Stage | Artifact | Anchor |
|-------|----------|--------|
| v0.3 | This spec | — |
| v0.4 | `/root/arifOS/arifosmcp/apex_selector.py` (~180 lines, LLM-free) | capability dispatch |
| v0.5 | `/root/arifOS/tests/test_apex_selector.py` (T1–T7 falsification) | kernel harness |
| v0.6 | Wire AUTH (P_veto) against F13 + agency registry | governance kernel |
| v0.7 | Wire P_legitimacy derivation (freshness × consent) | session capability tokens |
| v0.8 | Wire DEBT live-stream from `:7073/ingest` | FQ stabilizer |
| v0.9 | Wire SEAL gate (reversibility budget check) | capability dispatch |
| v0.10 | Shadow mode: APEX shadow matches kernel verdicts | capability dispatch |
| v1.0 | SEAL: shadow matches kernel on 1000 live routes | F13 required |

---

## 12. Anchors

- **APEX (SOT):** `/root/.qwen/projects/-root/memory/project-jauhari-manikam-apex-doctrine.md`
- **EFE (Friston):** Friston 2010 "The free-energy principle"; Parr & Friston 2019 "Generalised free energy"
- **AGENCY_LEVELS (L0–L6):** `/root/AAA/governance/AGENCY_LEVELS.md`
- **Constitution (F1–F13):** `/root/AAA/instructions/constitution.md`
- **Gate Promotion (0.20/0.50):** `/root/AAA/instructions/gate-promotion.md`
- **FQ / Reality-Opportunity Debt:** `/root/.qwen/projects/-root/memory/project-ariflow-fq-dynamics.md`
- **K-2 asymmetric degradation:** `/root/.qwen/projects/-root/memory/project-kernel-eurekas-from-aforge-directives.md`
- **4-Layer Architecture (333/555/888/A-FORGE):** `/root/.qwen/projects/-root/memory/project-4layer-architecture.md`
- **Recon origin:** `/root/HERMES/plans/2026-08-06_1800-kernel-contradictions-recon.md`
- **v0.2 (DEPRECATED):** `/root/AAA/specs/APEX_PATH_SELECTOR_v0.2.md`
- **v0.1 (DEPRECATED):** `/root/AAA/specs/ROUTING_FIELD_v0.1.md`
- **v0 (DEPRECATED):** `/root/AAA/specs/CONTRADICTION_FUNCTIONAL_v0.md`

---

## 13. Reversibility

This is `v0.3`. Amend via version bump. VOID via `APEX_PATH_SELECTOR_v0.3.VOID.md`.

All predecessors preserved with deprecation banners. Iteration history is kept, not deleted.

DITEMPA BUKAN DIBERI.