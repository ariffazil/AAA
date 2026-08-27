# Routing Field v0.1 — three-object pipeline: AUTH · FIELD · DEBT

> ## ⚠ DEPRECATED 2026-08-27 — superseded by [`APEX_PATH_SELECTOR_v0.2.md`](./APEX_PATH_SELECTOR_v0.2.md)
>
> **Status:** DEPRECATED (kept as iteration history, not deleted)
> **Superseded by:** `APEX_PATH_SELECTOR_v0.2.md` — three-phase ART → APEX → ACT architecture.
> **Reason for deprecation:**
> 1. Right three-object structure (AUTH/FIELD/DEBT) but wrong framing
> 2. **Invented APEX-adjacent math** instead of citing existing Jauhari-Manikam APEX Doctrine (2026-08-20)
> 3. v0.2 rewires math to `G = (A·P·E·X)^(1/4)` and reorganizes architecture around the canonical arifOS phases (333/555/888/A-FORGE)
>
> **Legacy content below retained for traceability.** v0.1's structural ideas (AUTH=P boundary, FIELD=geometric mean, DEBT=Law #5) live on in v0.2 §4 — just rewired to cite APEX rather than invent. Do not implement against v0.1.

---

**LEGACY CONTENT BELOW**

> **Status (when live):** DRAFT (F13 SEAL pending, never issued)
> **Authority (when live):** ARIF F13 SOVEREIGN, restructured 2026-08-27
> **Supersedes:** `CONTRADICTION_FUNCTIONAL_v0.md` (DEPRECATED 2026-08-27)
> **Reversibility:** Doc-only. No runtime mutation until v1.0 SEAL.
> **DITEMPA BUKAN DIBERI**

---

## 0. Why v0.1, not v0

`CONTRADICTION_FUNCTIONAL_v0.md` named a weighted sum of four signals `C(path)`.
ARIF's critique (2026-08-27) — held, accepted, fail-closed:

1. **Naming was wrong.** "Contradiction" is GEOX-flavoured. In geology, contrast
   (sand vs shale) ≠ contradiction (model failure). Contrast produces
   information; contradiction destroys the model. v0 smuggled epistemologi
   geologi ke seluruh arifOS tanpa audit.

2. **Topology was wrong.** Four signals mashed into one scalar had different
   cardinalities: `A_gap` is binary, `F_conflict` is magnitude, `E_gap` is
   deficit, `T_drift` is age. Averaging them dilutes constitution hardness.

3. **v0 missed arifOS canon primitives.** Three already exist as live
   constructs:
   - **P (Amanah)** — boundary condition for G to be defined
     (Jauhari-Manikam APEX Doctrine, 2026-08-20). `P ≤ P_min ⇒ HOLD`.
   - **Reality Debt / Opportunity Debt** — Law #5 control loop
     (FQ Stabilization Protocol). `Reality = ΣExecute − ΣVerify`,
     `Opportunity = ΣVerify − ΣExecute`.
   - **FQ exec:verify ratio** — the BALANCED verdict on arifFlow :7073.

v0.1 separates these into three pipeline objects with sharp boundaries.

---

## 1. The three objects

### 1.1 AUTH — Authority Gate (binary)

**Source primitives:** Agency Levels L0–L6 (F13 SOVEREIGN, 2026-07-12),
APEX P boundary condition, kernel-hardening Eureka K-2 (asymmetric degradation).

For each step `s` along path `p`, compute `authority_match(s) ∈ {0, 1}`:

```
authority_match(s) = 1  iff  actor(s).authority_level ≥ capability(s).required_authority
                       0  otherwise
```

**No partial credit.** Authority is binary per session per actor
(per `AAUTH_BOUNDS`: authority is opening a door, not negotiating through it).

```
AUTH(p) = AND over all s in p of authority_match(s)
        = 1  iff every step authorized
        = 0  iff any step unauthorized
```

| AUTH verdict | Pipeline effect |
|--------------|-----------------|
| `0` | **BLOCK** → return VOID. Path terminates. FIELD and DEBT never evaluated. |
| `1` | Continue to FIELD. |

**Anchor:** P_min from Jauhari-Manikam — `G` is undefined when `P ≤ P_min`.
Same shape: AUTH gate is the existence condition for downstream evaluation.

### 1.2 FIELD — Path Cost Gradient (scalar ∈ [0, 1])

**Source primitives:** F1–F13 floors, Evidence Discipline, kernel-contradictions-recon C1–C6
(now quantified), gate-promotion thresholds.

Computed only when AUTH = PASS. Three components (A_gap removed — now in AUTH):

| Component | Weight | Definition |
|-----------|--------|------------|
| `F_cost` | **0.50** | `max` over all steps of `floor_violation(s) ∈ [0, 1]` |
| `E_cost` | **0.30** | `1 − mean` over all steps of `evidence_coverage(s) ∈ [0, 1]` |
| `T_cost` | **0.20** | `1 − mean` over all steps of `freshness(s)`, `f = exp(−age_h/168)` |

```
FIELD(p) = 0.50 · F_cost + 0.30 · E_cost + 0.20 · T_cost
         ∈ [0, 1]                     (convex combination)
```

**Weights sum to 1.00.** F dominates because constitution is hard (max-floor-wins,
not averaged). Rebalancing requires F13 seal.

| FIELD verdict | Pipeline effect |
|---------------|-----------------|
| `FIELD ≥ 0.50` | **HOLD** (SABAR gate) |
| `0.20 ≤ FIELD < 0.50` | **SEEK** (PERHATI gate) — replan preferred |
| `FIELD < 0.20` | **PROCEED** candidate (TAMAT) — pending DEBT |

**Thresholds reuse** `0.20 / 0.50` from `gate-promotion.md` and
`forge-vision-densify` — same boundaries, different domain.

### 1.3 DEBT — Reflection Loop (time-series)

**Source primitives:** FQ Stabilization Law #5, arifFlow :7073 FQ vector,
Reality Debt / Opportunity Debt formulation.

Computed on rolling window (default 24 h, adjustable per `DEBT_LOOP` config).
Read-only against the live `:7073/ingest` stream. No LLM.

```
Reality_Debt(p)    = Σ_24h Execute_receipts(p) − Σ_24h Verify_receipts(p)
Opportunity_Debt(p) = Σ_24h Verify_receipts(p) − Σ_24h Execute_receipts(p)
```

| DEBT verdict | Condition | Pipeline effect |
|--------------|-----------|-----------------|
| `BALANCED` | `\|Reality_Debt − Opportunity_Debt\| ≤ 1` over window | no throttle |
| `OVER-EXECUTE` | `Reality_Debt ≥ +3` over window | force Verify before next Execute |
| `OVER-VERIFY` | `Opportunity_Debt ≥ +3` over window | throttle Execute (more verify, less execute) |

DEBT verdict modulates — never blocks. It is observation, not gate.
The kernel-hardening Eureka K-2 (asymmetric degradation) lives here:
governance failure → MUTATE blocked first, not OBSERVE.

---

## 2. Pipeline topology

```
                            ACT request
                                ↓
┌────────────────────────────────────────────────────────────┐
│  [AUTH gate]    binary, hard gate                            │
│    input: path + actor                                       │
│    verdict: PASS | BLOCK                                     │
│    BLOCK → return VOID (no FIELD, no DEBT, no EXECUTE)       │
└────────────────────────────────────────────────────────────┘
                                ↓ PASS
┌────────────────────────────────────────────────────────────┐
│  [FIELD gradient]    scalar ∈ [0, 1], soft signal            │
│    input: path steps (capability, evidence, age)             │
│    F_cost + E_cost + T_cost weighted                         │
│    verdict: PROCEED (<0.20) | SEEK (0.20–0.50) | HOLD (≥0.50)│
│    HOLD → return SABIYAN (no EXECUTE)                        │
└────────────────────────────────────────────────────────────┘
                                ↓ PROCEED or SEEK
┌────────────────────────────────────────────────────────────┐
│  [DEBT loop]    reflective, time-series                      │
│    input: live :7073/ingest window                          │
│    verdict: BALANCED | OVER-EXECUTE | OVER-VERIFY            │
│    effect: throttle direction (modulation, not blocking)     │
└────────────────────────────────────────────────────────────┘
                                ↓
                            EXECUTE
```

**No LOOP within pipeline.** Each path is one-shot; DEBT window is sliding.
Multi-step paths compose: AUTH = AND, FIELD = max over concatenation.

---

## 3. Combined verdict table

| AUTH | FIELD | DEBT | Final verdict | Action |
|------|-------|------|---------------|--------|
| BLOCK | — | — | **VOID** | return without execution |
| PASS | HOLD ≥ 0.50 | — | **VOID (SABAR)** | halt; require explicit override |
| PASS | SEEK ∈ [0.20, 0.50) | — | **PERHATI** | replan or escalate |
| PASS | SEEK | OVER-EXECUTE | **PERHATI + throttle** | replan + force Verify |
| PASS | PROCEED < 0.20 | BALANCED | **TAMAT** | execute |
| PASS | PROCEED | OVER-EXECUTE | **TAMAT + observe** | execute + flag for review |
| PASS | PROCEED | OVER-VERIFY | **TAMAT + throttle** | execute at reduced rate |

---

## 4. Path input schema (illustrative)

```json
{
  "path_id": "uuid",
  "actor_id": "fi003-qwen-code",
  "actor_authority_level": 4,
  "steps": [
    {
      "step_id": "s1",
      "capability_id": "arif_judge",
      "required_authority_level": 4,
      "evidence_refs": ["vault999:abc123"],
      "expected_artefact": "verdict",
      "capability_verified_at": "2026-08-27T10:00:00Z"
    }
  ]
}
```

Inputs are structured. **No LLM in the loop.** RRR-level purity.

---

## 5. Properties

| # | Property | Justification |
|---|----------|---------------|
| P1 | Bounded | All components bounded; convex combination |
| P2 | AUTH = AND across steps | any unauthorized step voids path |
| P3 | FIELD monontonic | adding steps can only add cost |
| P4 | LLM-free computable | structured inputs; engineer can recompute by hand |
| P5 | Constitutional priority | F dominates FIELD via weight + max-floor-wins |
| P6 | DEBT modulates not blocks | reflection loop observes; does not refuse |

---

## 6. Falsification tests

v0.2 prototype passes iff all 9 tests pass on canonical inputs.

| # | Test | Pass condition |
|---|------|---------------|
| T1 | AUTH identity | path with no steps → AUTH = PASS, FIELD = 0, PROCEED |
| T2 | AUTH failure | path with one unauthorized step → AUTH = BLOCK, no FIELD eval |
| T3 | AUTH passes | all authorized steps → AUTH = PASS, FIELD computed |
| T4 | F floor violation | single F1-violating step → FIELD ≥ 0.50 (F alone = 0.50) |
| T5 | E-gap dominance | path with zero evidence → FIELD ≥ 0.30 (E alone = 0.30) |
| T6 | T-drift | 14-day-old capability → FIELD(T=stale) > FIELD(T=fresh) |
| T7 | Sequential | `FIELD(p1 ++ p2) = max(FIELD(p1), FIELD(p2))` |
| T8 | DEBT steer | actor with 5 Execute / 0 Verify → DEBT = OVER-EXECUTE → throttle direction forces Verify |
| T9 | Bounded | 0 ≤ FIELD ≤ 1 for 1000 random paths |

---

## 7. Why this closes Level 4

| Need | Object that satisfies it |
|------|--------------------------|
| "Is this allowed?" | AUTH (binary, constitutional) |
| "How expensive is this?" | FIELD (scalar, gradient) |
| "Are we over-doing one half?" | DEBT (reflective, time-series) |

The Capability Graph's Level 4 (Thermodynamic Routing) becomes:

```
argmin_p FIELD(p)  subject to AUTH(p) = PASS, DEBT(p) = BALANCED
```

A real convex optimization over the federation's capability space.
Not metaphor. Router.

---

## 8. Implementation path

| Stage | Artifact | Organ anchor |
|-------|----------|--------------|
| v0 | This spec | — |
| v0.2 | `/root/arifOS/arifosmcp/routing_field.py` (~120 lines, LLM-free) | capability dispatch |
| v0.3 | `/root/arifOS/tests/test_routing_field.py` (T1–T9) | kernel test harness |
| v0.4 | Wire AUTH check against existing F13 + agency-level registry | governance kernel |
| v0.5 | Wire DEBT live-stream read from `arifFlow :7073/ingest` | FQ stabilizer |
| v0.6 | Shadow mode: log routing verdicts next to kernel verdicts | capability dispatch |
| v1.0 | SEAL: shadow matches kernel verdict on 1000 live routes | F13 required |

All git-add only. NOT deployed to `/opt/arifos/` until SEAL.

---

## 9. Open questions for F13

| # | Question | Default if no answer |
|---|----------|----------------------|
| OQ1 | Is P_min sealed? If so, do we cite it? | cite as SOT anchor for AUTH |
| OQ2 | DEBT window size (24 h default OK?) | 24 h |
| OQ3 | DEBT threshold (≥ 3 receipts imbalance)? | 3 |
| OQ4 | Expose pipeline as MCP tool `forge_route_evaluate` or kernel-internal? | kernel-internal for v1 |
| OQ5 | Should AUTH = BLOCK emit a VAULT999 record automatically? | yes (audit trail) |

---

## 10. Anchors

- **Inventory:** `/root/AAA/governance/DEWAN_REGISTRY.yaml`, `/root/.config/federation-models.json`
- **Capability cards:** `/root/AAA/schemas/capability-card.schema.json`
- **Governor:** `/root/AAA/instructions/constitution.md` (F1–F13), `arif_judge` kernel
- **Agency contract:** `/root/AAA/governance/AGENCY_LEVELS.md` (L0–L6)
- **APEX P boundary:** `/root/.qwen/projects/-root/memory/project-jauhari-manikam-apex-doctrine.md`
- **FQ exec:verify + Reality/Opportunity Debt:** `/root/.qwen/projects/-root/memory/project-ariflow-fq-dynamics.md`
- **Asymmetric degradation (K-2):** `/root/.qwen/projects/-root/memory/project-kernel-eurekas-from-aforge-directives.md`
- **Gate thresholds 0.20/0.50:** `/root/AAA/instructions/gate-promotion.md`
- **Three Foundations (HUMAN · INTENTION · VOID):** `/root/.qwen/projects/-root/memory/project-foundations-loop.md`
- **Predecessor (DEPRECATED):** `/root/AAA/specs/CONTRADICTION_FUNCTIONAL_v0.md`
- **Recon that motivated v0:** `/root/HERMES/plans/2026-08-06_1800-kernel-contradictions-recon.md` (C1–C6)

---

## 11. Reversibility note

This is `v0.1`. To amend, version bump. To VOID, replace with
`ROUTING_FIELD_v0.1.VOID.md` containing one line:
"VOID by F13 ARIF, YYYY-MM-DD, reason: …".

v0 file is preserved at `/root/AAA/specs/CONTRADICTION_FUNCTIONAL_v0.md`
with deprecation banner — kept as iteration history, not deleted.

DITEMPA BUKAN DIBERI.