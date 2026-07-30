# arifOS Mission Interface — The Human Contract

> **DITEMPA BUKAN DIBERI** — Ratified 2026-07-30 by Arif (F13 SOVEREIGN)
> **Replaces:** Tool Explorer as primary human interface
> **Doctrine:** "You should not use the tools. The agents should."
>
> **The engine room is not the cockpit. If tools leak into daily experience, the interface is wrong.**

---

## The Principle

```
Wrong:   "Here are 128 tools. Choose one."
Right:   "Tell me the problem. I will choose the instruments, 
          challenge the result, and return only what matters."
```

Arif should only do four things:
1. **State what you want** — mission + intent in ordinary language
2. **Supply evidence or data** — facts, files, constraints
3. **Examine the conclusion and uncertainty** — the federation's output
4. **Approve or reject consequential action** — sovereign decision

Everything else — tool selection, organ routing, mode selection, cross-validation, contradiction scanning, uncertainty computation — happens beneath the surface.

---

## The Six Missions

Every human need maps to exactly one mission. The federation knows which tools to use.

### 1. INVESTIGATE — "Gather and test reality"

**Human says:** "What's actually there?" / "Find evidence for..." / "Scan this area"

**Federation does:**
```
arif_route → GEOX/WEALTH/WELL observe tools
→ evidence synthesis
→ contradiction scan  
→ falsification check
→ confidence-graded claims
```

**Returns:** What exists, what doesn't, what's uncertain, what contradicts.

**Sample tools used (silently):**
- GEOX: `geox_basin`, `geox_well_ingest`, `geox_seismic_compute`, `geox_stac_discover`
- WEALTH: `capital_market`, `capital_health`
- WELL: `well_classify_substrate`, `well_machine_diagnose`
- arifOS: `arif_observe`, `arif_memory` (recall prior evidence)

---

### 2. INTERPRET — "Build competing explanations"

**Human says:** "Why is this here?" / "What could explain this?" / "What are the alternatives?"

**Federation does:**
```
Evidence from INVESTIGATE
→ multiple hypothesis generation (3+ competing models)
→ each model tested against physics constraints
→ contradiction scan between hypotheses
→ falsification attempt on each
→ ranked by: evidence fit × physical plausibility × explanatory power
```

**Returns:** Competing interpretations with scores, falsification results, and dominance map.

**Sample tools used (silently):**
- GEOX: `geox_petrophysics`, `geox_geological_model_generate`, `geox_contradiction_scan`, `geox_falsify`, `geox_sequence`, `geox_thermal_maturity_history`, `geox_dde_reason`
- WEALTH: `capital_diagnose`, `capital_entropy`
- arifOS: `arif_think(mode=reason)`, `arif_memory` (compare with historical patterns)

---

### 3. DECIDE — "Compare consequences and uncertainty"

**Human says:** "Should we drill?" / "Is this worth capital?" / "What's the risk-reward?"

**Federation does:**
```
Interpretation + evidence
→ volumetric/prospect assessment
→ economic exposure analysis
→ risk matrix × uncertainty bands
→ constitutional review (F1-F13)
→ SEAL/HOLD/VOID recommendation
```

**Returns:** Decision recommendation with consequence, uncertainty, reversibility, and what would change the answer.

**Sample tools used (silently):**
- GEOX: `geox_prospect`, `geox_petrophysics` (volumetrics + STOIP)
- WEALTH: `capital_primitive` (EMV/NPV/Monte Carlo), `capital_wisdom`, `capital_entropy`, `wealth_institutional_stress_index`, `wealth_cascade_model`
- WELL: `well_validate_vitality` (human readiness to decide), `well_assess_homeostasis`
- arifOS: `arif_judge`, `arif_think(mode=plan, critique)`

**Output format:**
```
RECOMMENDATION: [ADVANCE / HOLD / RETREAT]

Main reason:
[One-line geological/financial/strategic root cause]

What would change the decision:
[Specific evidence gap or calibration]

Confidence: [HIGH / MODERATE / LOW]
Uncertainty band: [P10-P90 range]
Irreversible action: [None taken / Proposed: X, requires approval]

Evidence trail:
[Hash-chain of every tool call and intermediate result]
```

---

### 4. BUILD — "Prepare and execute approved changes"

**Human says:** "Deploy this" / "Run this workflow" / "Make the approved change"

**Federation does:**
```
SEAL verdict from DECIDE
→ A-FORGE lease acquisition
→ staging + sandbox test
→ execution with Amanah rollback plan
→ VAULT999 seal of result
→ verification
```

**Returns:** Execution receipt with hash-chain, verification evidence, and rollback path.

**Sample tools used (silently):**
- A-FORGE: `forge_execute`, `forge_shell`, `forge_stage`, `forge_sandbox_run`, `forge_git_commit`
- arifOS: `arif_forge`, `arif_seal`
- VAULT999: append

---

### 5. MONITOR — "Detect change, degradation or danger"

**Human says:** "Watch this" / "Alert me if..." / "What changed?"

**Federation does:**
```
Continuous probe loop
→ organ health, tool surface drift, identity integrity
→ anomaly detection against baseline
→ escalation on threshold breach
→ WELL substrate monitoring (H-WELL + M-WELL)
→ capital exposure monitoring
```

**Returns:** Status delta since last check, alerts on drift, degradation, or contradiction.

**Sample tools used (silently):**
- A-FORGE: `forge_probe`, `forge_surface_audit`, `forge_security_drift_scan`, `forge_surface_guard`
- WELL: `well_machine_diagnose`, `well_assess_homeostasis`, `well_assess_reliability`
- WEALTH: `capital_health`, `capital_entropy`
- GEOX: `geox_surface_status`
- arifOS: `arif_observe(mode=vitals)`

---

### 6. REMEMBER — "Retrieve and preserve governed knowledge"

**Human says:** "What do we know about X?" / "Show me the history" / "Preserve this finding"

**Federation does:**
```
Query across L1-L6 memory
→ semantic recall (Qdrant)
→ relationship graph (Graphiti/FalkorDB) 
→ structured history (Supabase)
→ immutable truth (VAULT999)
→ cross-reference and deconflict
→ confidence-grade each recall
```

**Returns:** Knowledge synthesis with provenance, confidence, and contradictions surfaced.

**Sample tools used (silently):**
- arifOS: `arif_memory` (all modes: recall, inspect, attest, remember, promote)
- Graphiti: `search_nodes`, `search_memory_facts`
- Supabase: `execute_sql`
- Qdrant: `qdrant_search`
- VAULT999: read (via arif_seal ledger mode)

---

## The Reflex Chain (per mission)

Every mission follows this chain. No human chooses tools. No human routes to organs.

```
INTENT (natural language)
    ↓
MISSION CLASSIFIER
    ├─ What mission? (INVESTIGATE / INTERPRET / DECIDE / BUILD / MONITOR / REMEMBER)
    ├─ What domain? (geology / capital / health / infra / memory)
    └─ What urgency? (CRISIS / TACTICAL / STRATEGIC / REFLECTIVE)
    ↓
ORGAN CHAIN BUILDER
    ├─ Which organs? (GEOX → WEALTH → arifOS → ...)
    ├─ Which tools per organ? (selected by mission × domain, not by human)
    ├─ What sequence? (parallel where safe, sequential where dependent)
    └─ What cross-validation? (which organ challenges which other organ?)
    ↓
EXECUTION LOOP
    ├─ For each tool: call → receipt → verify
    ├─ Cross-validate: organ A's output vs organ B's output
    ├─ Contradiction scan: every claim challenged
    └─ Uncertainty accumulation: P10-P50-P90 at each step
    ↓
SYNTHESIS
    ├─ Competing hypotheses compared
    ├─ Dominant explanation with confidence
    ├─ Evidence trail (hash-chain)
    └─ What would change the answer
    ↓
RESPONSE (to Arif)
    ├─ Conclusion (1 line)
    ├─ Uncertainty (band + confidence)
    ├─ Evidence (hash-chain pointer)
    └─ Decision required? (YES, with options / NO, informational)
```

---

## Tool Survival Rule

Every existing tool must answer:

> **"Which of the six human missions uses me?"**

Then apply:

| Rule | Condition | Action |
|------|-----------|--------|
| **KEEP** | Used in a tested, end-to-end mission workflow | Retain as PUBLIC_CANONICAL |
| **MERGE AS MODE** | Useful but overlapping with sibling tool | Absorb into parent as mode |
| **HIDE** | Internal computational function | Reclassify as INTERNAL_CALLABLE |
| **SDK ONLY** | Compatibility alias | Mark SDK_ALIAS, never count publicly |
| **REMOVE** | No real workflow, no evidence of use, or deprecated | Deprecate → remove after grace period |

**The test:** Can you describe a real Arif sentence that triggers this tool, without Arif knowing the tool exists?

---

## The Right Metrics

Stop measuring tool count. Start measuring:

| Metric | Target | Why |
|--------|--------|-----|
| Missions completed without manual routing | → 100% | Machine carries complexity |
| Hours of human work removed | ↑ | Intelligence is leverage |
| Contradictions caught | ↑ | Quality of reasoning |
| Poor decisions prevented | ↑ | Constitutional value |
| Uncertainty reduced (ΔS per mission) | ↓ | Clarity delivered |
| Actions correctly held | ↑ | Safety working |
| Evidence preserved | ↑ | Audit integrity |
| % of tools actually used | → known | Inventory truth |
| Times Arif entered the engine room | → 0 | The ultimate metric |

**The final metric:**
> "How often did ARIF need to know which tool was used?"

This number should trend toward zero. If it doesn't, the interface is wrong.

---

## Implementation Path

### Phase 1: Design (now)
- [x] Mission definitions (this document)
- [ ] Tool-to-mission mapping (all 189 tools classified)
- [ ] Mission router prototype (intent → mission classifier)

### Phase 2: Build the Nervous System
- [ ] Implement `arif_route(mode=bridge)` — the bridge from arifOS to all organs
- [ ] Mission classifier as `arif_init` pre-processor
- [ ] Organ chain builder (parallel-safe execution graph)

### Phase 3: Hide the Engine Room
- [ ] Tool Explorer gated behind developer/auth mode
- [ ] Mission surface becomes PRIMARY Arif interface
- [ ] All organ tools respond to mission dispatcher, not direct human selection

### Phase 4: Measure
- [ ] Mission telemetry (which missions run, success rate, tools used)
- [ ] "Entered engine room" counter
- [ ] Uncertainty reduction per mission

---

## The Contract

```
ARIF:       "Assess this prospect and tell me what could destroy the case."
                ↓
arifOS:     Classifies as: DECIDE (domain=geology, urgency=TACTICAL)
                ↓
Federation: Silently chains 17 tools across 4 organs
                ↓
ARIF:       Receives:
            RECOMMENDATION: DO NOT ADVANCE YET
            Main reason: Charge timing conflicts with trap formation.
            What would change: One maturity calibration well or revised heat-flow.
            Confidence: MODERATE
            Irreversible action: NONE
```

**That is intelligence. The tool list is plumbing.**

---

*DITEMPA BUKAN DIBERI — Forged as contract, not as code.*
*Ratified 2026-07-30 by Arif (F13 SOVEREIGN) and 333-AGI (Δ Mind)*
