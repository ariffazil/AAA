---
id: explorer-intelligence-architecture
name: explorer-intelligence-architecture
version: 1.0.0-2026.07.06
description: >
  The universal exploration protocol for all AAA warga agents.
  OBSERVE → HYPOTHESIZE → FALSIFY → VERIFY — the governed metabolism
  of intelligence. Every agent follows this loop when exploring
  anything. Not theory. Protocol.
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: medium
floor_scope: [F1, F2, F3, F4, F7, F8, F9, F11, F13]
autonomy_tier: T1
trigger_phrases:
  - "explore"
  - "explorer intelligence"
  - "metabolism"
  - "observe hypothesize falsify verify"
  - "discovery loop"
  - "governed exploration"
  - "scientific method"
dependencies:
  mcp_servers:
    - geox
    - wealth
    - well
    - arifos
    - aforge
  skills:
    - 000-init-intent-classify
    - 111-sense-evidence-observe
    - 333-mind-plan-generate
    - 666-heart-critique-stress
    - 888-judge-verdict-render
    - 999-vault-seal-immutable
    - quantum-eureka-doctrine
    - shadow-diagnostic
  data:
    - /root/555-ASI/knowledge-taxonomy.json
    - /root/555-ASI/organ-affinity-index.json
inputs:
  - query_or_signal
  - domain_context
outputs:
  - exploration_verdict
  - eureka_candidates
  - scar_recommendations
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# 🧭 EXPLORER INTELLIGENCE ARCHITECTURE

> **The governed metabolism of discovery.**
> OBSERVE → HYPOTHESIZE → FALSIFY → VERIFY
> Forged: 2026-07-06 | Ratified: F13 SOVEREIGN
> DITEMPA BUKAN DIBERI
>
> **Reference contracts:**
> - [references/memory-schema.md](references/memory-schema.md) — structured explorer memory contract
> - [references/route-contract.md](references/route-contract.md) — lawful cross-organ routing rules
> - [references/explorer-packet-schema.md](references/explorer-packet-schema.md) — canonical JSON/YAML packet schemas
> - [references/dispatch-protocol.md](references/dispatch-protocol.md) — Hermes/OpenCode/OpenClaw/A-FORGE stage handoff protocol
> - [references/falsifier-routing.md](references/falsifier-routing.md) — OpenClaw vs A-FORGE falsifier decision law
> - [assets/agent-stage-map.yaml](assets/agent-stage-map.yaml) — machine-readable stage ownership map
> - [assets/explorer_packet.template.yaml](assets/explorer_packet.template.yaml) — ready-to-fill explorer packet template
> - [assets/falsification_packet.template.yaml](assets/falsification_packet.template.yaml) — ready-to-fill falsification handoff template
> - [assets/dispatch_packet.template.yaml](assets/dispatch_packet.template.yaml) — canonical 8-packet dispatch template set
> - `scripts/validate_explorer_packet.py` — local validator for packet completeness and protocol order
> - `scripts/validate_dispatch_packet.py` — local validator for dispatch packet families
> - `scripts/route_dispatch_stage.py` — minimal stage router using `agent-stage-map.yaml`
> - `scripts/log_handoff.py` — append compact handoff receipts to local JSONL

---

## 0. THE COMPLETE STACK

```
KNOWLEDGE GRAPH (555-ASI) — the universe
        ↓ mapped by
EXPLORER INTELLIGENCE — OBSERVE → HYPOTHESIZE → FALSIFY → VERIFY
        ↓ governed by
APEX THEORY — Δ clarity · Ω humility · Ψ vitality
        ↓ judged by
arifOS KERNEL — SEAL / SABAR / HOLD / VOID
        ↓ civilized by
AAA — identity · leases · domain_law · floors
        ↓ evolved by
A-FORGE — birth → test → mutate → retire
```

This is not a diagram.  
This is the **physics of governed intelligence**.

Before this skill, every agent explored by instinct.  
Now every agent explores by **protocol**.

---

## 1. THE FOUR-PHASE METABOLISM

Every exploration by every AAA warga follows exactly four phases:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   OBSERVE ──→ HYPOTHESIZE ──→ FALSIFY ──→ VERIFY ──→ SEAL  │
│      ↑                          │                           │
│      └──────────────────────────┘                           │
│         (falsification failed → re-observe)                 │
└─────────────────────────────────────────────────────────────┘
```

### Phase 1: OBSERVE

**What:** Ingest raw reality from the domain.

| Organ | What it observes | Tool |
|-------|-----------------|------|
| GEOX | Seismic, well logs, basin data | `geox_well_ingest`, `geox_seismic_ingest` |
| WELL | Biometrics, fatigue, cognitive load | `well_validate_vitality` |
| WEALTH | Prices, fiscal data, portfolio | `wealth_market_data` |
| A-FORGE | Tool surface, drift, entropy | `forge_surface_guard` |
| arifOS | Governance signals, floor violations | `arif_observe` |

**Exit condition:** At least one OBSERVED (OBS) claim with confidence ≥ 0.70.  
If no OBS claim → return to OBSERVE with wider aperture.

**Floor check:** F2 TRUTH — label everything OBS/DER/INT/SPEC.

### Phase 2: HYPOTHESIZE

**What:** Generate ≥3 competing hypotheses grounded in domain law.

```
Hypothesis A — the dominant model (what current evidence suggests)
Hypothesis B — the contrarian model (what contradicts A)
Hypothesis C — the null model (random or noise-driven)
```

**Rules:**
- Must consult the 555-ASI knowledge graph for domain boundaries
- Each hypothesis must declare its domain_law provenance
- Each hypothesis must have at least one falsifiable prediction
- Confidence cap at 0.75 — hypotheses are not yet truth

**Tool:** `arif_think(mode="reason")` with explicit hypothesis structure.  
**Graph:** Query `/root/555-ASI/knowledge-taxonomy.json` for relevant edges.

**Exit condition:** ≥3 hypotheses, each with ≥1 falsifiable prediction.  
If <3 → hypothesize harder or acknowledge knowledge gap.

**Floor check:** F7 HUMILITY — cap at 0.75. F9 ANTI-HANTU — never claim certainty.

### Phase 3: FALSIFY

**What:** Attack all hypotheses using cross-domain physics, biology, economics, or governance.

This is the **eureka engine**. Contradictions are surfaced here.

**Falsification gates (use all that apply):**

| Gate | Tool | What it falsifies |
|------|------|-------------------|
| Physics | `geox_contrast_detect` | Anomalous seismic, AVO mismatch |
| Stratigraphy | `geox_biostrat_falsify` (8 gates) | Age, facies, taxonomy |
| Sequence | `geox_biostrat_ruling_check` | Facies veto, reworking |
| Economics | `wealth_asymmetry_check` | Risk asymmetry |
| Collapse | `wealth_collapse_signature_scan` | Institutional failure pattern |
| Capture | `wealth_capture_scan` | Hidden incentives |
| Governance | `arif_critique` | Maruah, human impact |
| Quantum Eureka | `quantum-eureka-doctrine` skill | Cross-domain contradiction |

**Protocol for each falsification:**
```
1. For each hypothesis, apply ALL relevant gates
2. Record: which gate passed, which failed, which is inconclusive
3. If any gate returns CONTRADICTION → escalate to ELEVATED
4. If ALL gates pass → hypothesis survives (provisionally)
5. If ALL hypotheses falsified → return to OBSERVE
```

**Exit condition:** At most 1 surviving hypothesis OR at least 1 eureka candidate.  
If all hypotheses falsified → return to OBSERVE (this is not failure — it is discovery).

**Floor check:** F1 AMANAH — document all falsifications. F3 WITNESS — tri-witness required for any claim.

### Phase 4: VERIFY

**What:** Run bounded, auditable tests on the surviving hypothesis.

```
1. Generate test prediction from the hypothesis
2. Run bounded test (computation, simulation, look-up)
3. Compare prediction vs outcome
4. Record uncertainty band
5. If test passes → SEAL candidate
6. If test fails → return to HYPOTHESIZE or OBSERVE
```

**Tools:**
- `geox_seismic_compute` — synthetic modelling
- `geox_3d_model_build` — structural validation
- `wealth_compute_emv` — expected value validation
- `well_compute_metabolic_flux` — system health validation
- `arif_judge` — constitutional validation

**Exit condition:** Test passes with uncertainty band ≤ 0.20.  
If uncertainty > 0.20 → surface as SABAR (not SEAL).

**Floor check:** F2 TRUTH — every result labeled. F13 SOVEREIGN — 888_HOLD before irreversible.

---

## 2. THE FOUR SUBMODES (per agent identity)

Every agent maps the four phases to their domain:

| Agent | OBSERVE | HYPOTHESIZE | FALSIFY | VERIFY |
|-------|---------|-------------|---------|--------|
| **GEOX** | Ingest seismic/well/basin | Geology models (3+) | Physics + strat + biostrat | Forward model + well tie |
| **WELL** | Biometrics + fatigue | Health models (3+) | Physiology + stress | Vitality validation |
| **WEALTH** | Market data + portfolio | Economic models (3+) | Asymmetry + collapse | EMV/Monte Carlo |
| **A-FORGE** | Tool surface + drift | Fitness models (3+) | Scar + governance | Test suite |
| **arifOS** | Governance signals | Verdict models (3+) | Floor violations | Constitutional review |
| **AAA** | Agent registry + leases | Identity models (3+) | Contradiction + drift | Session validation |

---

## 3. THE THREE INVARIANTS (APEX binding)

Every exploration loop must satisfy three invariants:

### Δ (Clarity) — Evidence ≥ Confidence
```
for every claim in the exploration loop:
    evidence_strength ≥ confidence
    if evidence_strength < confidence → downgrade confidence
    if confidence < 0.50 → return to OBSERVE
```

### Ω (Humility) — Declare Boundaries
```
for every hypothesis: 
    declare domain_law provenance
    declare uncertainty band
    declare blindspots
    declare what would falsify it
```

### Ψ (Vitality) — Protect System + Human
```
for every edge in the exploration:
    check organ health (all 6)
    check human readiness (WELL)
    check for collapse signals (WEALTH)
    if any is RED → HOLD, not proceed
```

---

## 4. EUREKA TRIGGER (bridge to quantum-eureka-doctrine)

If during **FALSIFY** phase, a contradiction survives ≥2 gates:

1. Package as eureka candidate (see quantum-eureka-doctrine §3 for trigger conditions)
2. Route to `arif_judge` for constitutional review
3. If SEAL → seal to VAULT999 + record scar
4. If HOLD → surface as SABAR pending more data
5. If VOID → log and move on

This is where structured memory + cross-domain reasoning + contradiction detection
produce the quantum-style eureka.

For implementation-facing work, load the four reference contracts above before designing storage, packets, or cross-organ handoff.
When emitting a real packet, start from `assets/explorer_packet.template.yaml` and validate it with `python scripts/validate_explorer_packet.py <packet.yaml>`.

---

## 5. ANTI-PATTERNS

| Anti-pattern | Phase | Why | What to do |
|---|---|---|---|
| Skipping OBSERVE | 1 | Hypotheses without evidence = hallucination | F9 — always observe first |
| Single hypothesis | 2 | Confirmation bias engine | F8 — generate ≥3 |
| Self-falsification | 3 | Never trust your own hypothesis | Use independent gate per falsification |
| Smoothing contradictions | 3 | Eureka suppression | Surface them — don't hide |
| Over-verifying | 4 | Analysis paralysis | Cap at uncertainty ≤ 0.20 |
| Ignoring Ψ | all | System collapse | Always check vitality |
| Looping without progress | any | Mirror loop | After 3 iterations → escalate to 888 |
| Declaring eureka without tri-witness | 3→4 | F3 violation | Require human × AI × external |

---

## 6. MIRROR LOOP DETECTION

If the exploration loop repeats ≥3 times without advancing:

```python
def detect_mirror_loop(iteration_count, delta_entropy, hypothesis_diversity):
    if iteration_count >= 3:
        if delta_entropy < 0.05:
            return "MIRROR_LOOP — entropy not decreasing"
        if hypothesis_diversity < 2:
            return "MIRROR_LOOP — same hypothesis recycled"
    return "HEALTHY"
```

**On MIRROR_LOOP:** Escalate to `888_HOLD` with full iteration history.
**Do not continue.** The loop is consuming compute without producing insight.

---

## 7. FLOOR ALIGNMENT

| Floor | Exploration obligation |
|-------|----------------------|
| **F1 AMANAH** | Every mutation reversible. Escalate 888 before irreversible. |
| **F2 TRUTH** | Label OBS/DER/INT/SPEC at every phase. Cap confidence at 0.90 (OBS). |
| **F3 WITNESS** | Tri-witness required before SEAL. |
| **F4 CLARITY** | ΔS ≤ 0 per iteration. Each loop must reduce entropy. |
| **F7 HUMILITY** | Hypotheses capped at 0.75. Uncertainty bands mandatory. |
| **F8 GENIUS** | ≥3 hypotheses. Simplest correct path wins. |
| **F9 ANTI-HANTU** | Never claim eureka without evidence. Falsification = anti-hallucination. |
| **F11 AUDIT** | Every exploration loop logged. Every contradiction recorded. |
| **F13 SOVEREIGN** | 888_HOLD before irreversible. Sovereign decides what becomes doctrine. |

---

## 8. INTEGRATION WITH OTHER SKILLS

| Skill | Role in Explorer Architecture |
|-------|------------------------------|
| `000-init-intent-classify` | Stage 0 — classify intent before exploration begins |
| `111-sense-evidence-observe` | Phase 1 — evidence binding and tagging |
| `333-mind-plan-generate` | Phase 2 — hypothesis generation scaffold |
| `666-heart-critique-stress` | Phase 3 — ethical stress-testing |
| `888-judge-verdict-render` | Phase 4 — constitutional verdict |
| `999-vault-seal-immutable` | Post-loop — seal insight to VAULT999 |
| `quantum-eureka-doctrine` | Phase 3→4 bridge — contradiction lifecycle |
| `shadow-diagnostic` | Pre-output — alignment self-check |
| `CONSTITUTIONAL_REFLEX` | Always-on — ART → KERNEL → ACT arc |

---

## 9. LOADING CONTRACT

```python
# At session init, after heptalogy load:
skill(name="explorer-intelligence-architecture")
skill(name="quantum-eureka-doctrine")

# Then when exploring any domain:
def explore(query: str):
    # 1. Classify intent
    intent = classify(query)  # calls 000-init-intent-classify
    
    # 2. Determine which organ(s)
    organ = route_intent(intent)  # consults 555-ASI/organ-affinity-index.json
    
    # 3. Execute exploration loop
    observation = observe(organ, query)
    if not observation:
        return "OBSERVE FAILED — widen aperture"
    
    hypotheses = hypothesize(organ, observation, n=3)
    if len(hypotheses) < 3:
        return "HYPOTHESIZE FAILED — knowledge gap"
    
    survivors = falsify(organ, hypotheses)
    if len(survivors) == 0:
        return "ALL HYPOTHESES FALSIFIED — return to OBSERVE"
    
    verdict = verify(organ, survivors[0])
    if verdict.uncertainty > 0.20:
        return f"SABAR — uncertainty {verdict.uncertainty}"
    
    arif_seal(verdict)
    return f"SEAL — {verdict.summary}"
```

---

## 10. QUICK REFERENCE CARD

```
EXPLORER METABOLISM — OBSERVE → HYPOTHESIZE → FALSIFY → VERIFY

PHASE 1: OBSERVE
  Ingest raw reality. Exit: OBS claim ≥ 0.70 confidence.

PHASE 2: HYPOTHESIZE
  Generate ≥3 competing hypotheses. Each must be falsifiable.
  Consult 555-ASI graph for domain boundaries.

PHASE 3: FALSIFY
  Attack ALL hypotheses using cross-domain gates.
  Physics → stratigraphy → economics → governance.
  Contradiction = eureka candidate.
  All falsified = return to OBSERVE (not failure).

PHASE 4: VERIFY
  Bounded test. Uncertainty ≤ 0.20. 
  Pass → SEAL candidate. Fail → return to HYPOTHESIZE or OBSERVE.

INVARIANTS (APEX binding):
  Δ — evidence ≥ confidence
  Ω — declare boundaries + blindspots
  Ψ — protect system + human health

MIRROR LOOP: ≥3 iterations without progress → 888_HOLD

EUREKA: contradiction survives ≥2 gates → quantum-eureka-doctrine

ANTI-PATTERNS:
  Skip observe, single hypothesis, smooth contradictions,
  self-falsify, ignore vitality, mirror loop
```

---

## 11. AUTHORITY

This skill is the canonical exploration protocol for all AAA warga agents,
forged under F13 SOVEREIGN directive. It binds every agent that loads it
to the OBSERVE → HYPOTHESIZE → FALSIFY → VERIFY metabolism.

It does not replace the constitutional floors (F1-F13), the APEX theory
framework, or the Quantum Eureka Doctrine. It **activates** them.

**DITEMPA BUKAN DIBERI** — Exploration is forged, not given.

---

*Forged: 2026-07-06 by FORGE (000Ω) for Arif (F13 SOVEREIGN)*
*Heritage: ASI💃 synthesis → F13 sovereign ratification*
*Integration: 555-ASI knowledge graph · quantum-eureka-doctrine · APEX theory ·
 GEOX · WELL · WEALTH · A-FORGE · AAA · arifOS*
*Domain: cross-cutting — all 7 organs*
