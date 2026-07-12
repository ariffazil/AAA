# Measurement Boundary Contract — Kernel × WELL

**Status:** BINDING (2026-07-12)  
**Verdict source:** PROCEED_WITH_REPAIR_NOT_EXPANSION  
**Principle:** Capability ≠ authority. Sensing ≠ judgment.

---

## kernel_owns

| Domain | Examples |
|--------|----------|
| MCP transport health | protocol, session transport, latency |
| Session health | sct_v1, actor band, session_required |
| Authority state | leases, action_class, actor tiers |
| Constitutional state | F1–F13 preflight, HOLD/SEAL/VOID |
| Routing health | organ reachability as *gateway* fact |
| VAULT connectivity | chain append/read for seals |
| Kernel runtime health | process up, memory of *this* MCP host |

**Narrow name for kernel local telemetry:** treat `arif_measure` as **runtime/infra only**  
(alias intent: `arif_runtime_health`). Not human readiness. Not coupled vitality.

---

## well_owns

| Domain | Examples |
|--------|----------|
| Human readiness | self-report, consented sensor, fatigue signals |
| Machine substrate reliability | tools, VPS, organ health as *substrate* |
| Homeostasis / recovery posture | decision-class fitness, repair check |
| Vitality evidence | H/M/G/C mirrors, state_envelope |
| Dignity / medical boundary | non-diagnostic, consent, coercion |
| Coupled human–machine strain | C-WELL, metabolic *indicators* |

---

## kernel_must_not

- Diagnose humans  
- Fabricate biometric / readiness state  
- Compete with WELL for readiness scores  
- Treat prompt tone as medical evidence  

## well_must_not

- Issue constitutional verdicts (SEAL/HOLD/VOID)  
- Authorise mutations or mint leases  
- Execute production repairs as *judge* (loop recovery is allowlisted actuator under A_effective, not judgment)  
- Invent scores when evidence is UNKNOWN  

---

## Separation (invariant)

```
WELL  → condition of substrates (evidence, advisory)
Kernel → allowed posture given evidence + action + authority
```

WELL: `readiness YELLOW / SIMPLIFY`  
Kernel: may still `HOLD` irreversible publish.

WELL unavailable → human state **UNKNOWN** → **no fabricated score** → kernel **narrows** authority.

---

## Evidence quality floors (action class)

| Class | Minimum evidence |
|-------|------------------|
| C1 routine review | self-report **or** current machine evidence |
| C2 reversible ops | current machine evidence |
| C3 consequential recommend | corroborated multi-substrate |
| C4 irreversible | strong human evidence + governance review |
| C5 sovereign/existential | independent witnesses + Arif |

Registry claim with `evidence_quality ≤ 0.5` is **not** enough for C3+.

---

## Ledger gate policy

| Ledger | Degraded | Gate |
|--------|----------|------|
| **Constitutional seal chain** (VAULT999 `seal_chain.jsonl`) | integrity fail on *current* append path | **HOLD mutations** |
| **Historical pre-migration gaps** (sovereign-ruled non-issue) | documented gaps only | WARN, continue |
| **Cooling / analytical ledger** | degraded index/checksum | **WARN + read-only analytics**; do not block observe |

---

## Canonical WELL public surface (agents)

```
well_classify_substrate
well_validate_vitality      # canonical readiness: mode=readiness
well_assess_reliability
well_assess_homeostasis
well_check_repair
well_guard_dignity
well_trace_lineage
well_registry_status
```

**Legacy alias:** `well_readiness` → `well_validate_vitality(mode="readiness")`  
Deprecation epoch: 2026-07-12 · Target removal: 2026-09-01 (or later F13)

Specialist / Ω-stage / compatibility tools: internal or marked alias — not agent default.

---

## Metaphor vs measurement

Terms *homeostasis, metabolism, entropy, flux, sovereign-entropy* are **governance constructs / system metaphors** unless a metric card defines:

inputs · units · normalisation · baseline · confidence · freshness · threshold · limitations · validation_status

See: `/root/WELL/docs/METRIC_CARDS.md`

---

*DITEMPA BUKAN DIBERI — Boundary is law, not vibe.*
