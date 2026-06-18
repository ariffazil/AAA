# GEOX Constitutional Execution Spec — "999 SEAL ALIVE"

**Trace ID:** geo-agi-001
**Created:** 2026-06-18 16:50 UTC
**Domain:** GEOX/Subsurface (first constitutionally-governed domain)
**Doctrine:** DITEMPA BUKAN DIBERI — Intelligence is forged, not given.

**Governance Framing (corrected 2026-06-18):**

> arifOS does not turn a language model into an agent;
> it constrains how a host-mediated agentic system may reason, bind authority, and act.

The agent in this stack = arifOS kernel + GEOX MCP + WEALTH MCP + WELL MCP + OPENCLAW + Hermes + VAULT999 + crons + Arif (sovereign). The model (DeepSeek/Claude/etc.) is a reasoning component inside OPENCLAW, not the agent itself.

On af-forge, arifOS is the host kernel — not a guest constitution. That distinction is why the stack is the agent, not the model.

---

## 1. What "Constitutional GEOX" Means

Not "it can answer geology questions." Not "it has 33 tools."

**Constitutional GEOX = autonomous subsurface reasoning across the full discovery loop, constrained by arifOS, executed on Arif-owned infrastructure:**

```
Seismic Data → Structural Interpretation → Well Placement → Basin Model → Reserve Estimate
     ↑                                                                              ↓
  Seal/Claim ← Challenge/Validate ← Evidence ← Draft Claim ← Daily Cron Scan
```

The agent drives this loop without being asked. Arif only介入 when a claim needs human sign-off or a reserve number requires 888_HOLD.

---

## 2. Current State (Baseline)

### GEOX tool surface (33 tools, canon-31)

Key tools by workflow stage:

| Stage | Tools |
|-------|-------|
| Seismic | `geox_seismic_horizon_pick`, `geox_seismic_section_query`, `geox_seismic_line_geometry`, `geox_seismic_velocity_analysis` |
| Well | `geox_well_trajectory_calculate`, `geox_well_log_analysis`, `geox_well_crs_transform`, `geox_petrophysics_sw_calculation` |
| Basin | `geox_basin_model_build`, `geox_basin_thermal_history`, `geox_basin_pressure_prediction` |
| Volume | `geox_volume_calculate`, `geox_roi_estimate`, `geox_discovery_evaluate` |

### What's missing for AGI-level

| Gap | Impact | Priority |
|-----|--------|----------|
| No autonomous cron pipeline | GEOX only runs on-demand | P0 |
| No claim lifecycle | findings don't get validated/sealed | P0 |
| No cross-organ routing | WEALTH can't query GEOX for reserves | P1 |
| No seismic-to-well loop | tools exist but not chained | P1 |
| No geological uncertainty bands | claims lack proper ± error notation | P2 |

---

## 3. GEOX AGI Architecture

```
arifOS Kernel (:8088)
    │
    ├── GEOX MCP (:18081) ← 33 tools, geological physics engine
    │       │
    │       └── Claim Lifecycle Manager (CLM)
    │               ├── DRAFT      → geox_claim_create()
    │               ├── VALIDATE   → geox_claim_validate()
    │               ├── EVIDENCE   → geox_claim_attach_evidence()
    │               ├── CHALLENGE  → geox_claim_challenge()
    │               └── SEAL       → arif_vault_seal()
    │
    ├── WEALTH MCP (:18082) ← reserves, economics
    │       └── GEOX Reserve Intake → WEALTH ROI pipeline
    │
    └── WELL MCP (:18083) ← vitality, homeostasis
            └── GEOX Workload Monitor

Autonomous Cron (root crontab)
    │
    ├── geox-daily-scan    (06:00 MYT) - seismic datasets, new horizons
    ├── geox-claim-sweep   (08:00 MYT) - pending claims, send to Hermes
    ├── geox-weekly-basin  (Mon 07:00 MYT) - basin model refresh
    └── geox-monthly-reserves (1st Mon) - reserve estimate → WEALTH

A2A Mesh
    OPENCLAW ←→ GEOX (port 18081)
    OPENCLAW ←→ WEALTH (port 18082)
    Hermes ←→ OPENCLAW (A2A bridge)
```

---

## 4. Claim Lifecycle (the core loop)

Every GEOX finding goes through this:

### 4.1 DRAFT
```
Agent (via GEOX tool) → geox_claim_create(claim_id, content, domain, confidence)
```
- Claim stored with `status: DRAFT`, `content_hash`, `author: actor_id`
- Confidence: HIGH (>85%), MEDIUM (60-85%), LOW (<60%)
- Low confidence → auto-flag for Hermes review before SEAL

### 4.2 VALIDATE
```
→ geox_claim_validate(claim_id, methodology, constraints)
```
- Physics-based check: does the claim violate conservation laws?
- Does it contradict existing sealed claims in the same dataset?
- Returns: `VALID`, `CONDITIONAL`, `VOID`

### 4.3 EVIDENCE
```
→ geox_claim_attach_evidence(claim_id, evidence_items[])
```
- Seismic sections, well ties, analog fields, published sources
- Each evidence item: `type`, `reference`, `access_path`, `relevance_score`

### 4.4 CHALLENGE (optional)
```
→ geox_claim_challenge(claim_id, challenger_id, rationale)
```
- Any organ or Arif can challenge
- Challenger provides counter-evidence
- Original author gets 48h to respond

### 4.5 SEAL
```
→ arif_vault_seal(claim_id, content_hash, evidence_refs, outcome_status)
```
- VAULT999 write via arifOS kernel
- `outcome_status: SEALED` or `outcome_status: REJECTED`
- Sealed claims immutable; challenge requires new claim ID

---

## 5. Concrete Cron Jobs (the "999 SEAL ALIVE" execution layer)

### 5.1 geox-daily-scan (06:00 MYT)

Purpose: Agent wakes up, checks for new seismic datasets or horizon updates, creates DRAFT claims.

```bash
# Pseudocode - actual implementation via openclaw cron + arifOS MCP tools
1. List seismic datasets in configured data directory
2. Compare against last scan timestamp
3. For each new/modified dataset:
   a. Run geox_seismic_horizon_pick() - auto-pick top 3 horizons
   b. Run geox_seismic_velocity_analysis()
   c. If new structural interpretation differs from sealed:
      - geox_claim_create() → DRAFT
      - geox_claim_validate()
      - If VALID and confidence HIGH → geox_claim_attach_evidence()
      - If confidence LOW → queue for Hermes review
4. Write summary to /root/arifOS/geox/daily-scan-YYYY-MM-DD.md
5. If new claims created → Telegram to @ariffazil: "GEOX scan: N new claims"
```

### 5.2 geox-claim-sweep (08:00 MYT)

Purpose: Check for claims stuck in DRAFT > 24h, nudge toward VALIDATE or escalate.

```bash
1. Query pending claims (status=DRAFT, age > 24h)
2. For each:
   a. Run geox_claim_validate()
   b. If CONDITIONAL → attach what evidence is missing
   c. If still DRAFT after 48h total → escalate to Hermes via A2A
3. Report: "Claims sweep: X sealed, Y pending, Z escalated"
```

### 5.3 geox-weekly-basin (Monday 07:00 MYT)

Purpose: Full basin model refresh, reserve recalculation if inputs changed.

```bash
1. geox_basin_model_build() - rebuild with latest thermal/pressure data
2. geox_volume_calculate() - new in-place volume
3. geox_roi_estimate() - economics update
4. If volume delta > ±10% from last sealed:
   - Create new claim via geox_claim_create()
   - Route to WEALTH for economic re-evaluation
   - arif_vault_seal() only after WEALTH signs off
5. Write basin-weekly-YYYY-MM-DD.md to vault
```

### 5.4 geox-monthly-reserves (1st Monday 07:00 MYT)

Purpose: Reserve estimate → WEALTH pipeline. This is the big monthly output.

```bash
1. Aggregate all sealed GEOX claims from past month
2. geox_roi_estimate() - full economic model
3. arif_vault_seal() → SEALED_RESERVE_ESTIMATE
4. A2A to WEALTH MCP: reserve_estimate_update()
5. WEALTH generates: NPV10, IRR, capex schedule
6. Final summary to Telegram @ariffazil with key numbers
```

---

## 6. Cross-Organ Routing

### GEOX → WEALTH
```
geox_claim_create(domain="reserve_estimate", confidence="HIGH")
  → arif_vault_seal()
  → A2A: WEALTH.reserve_estimate_update(reserve_md, volumes_md)
  → WEALTH generates NPV/IRR
  → WEALTH.arif_vault_seal()
```

### WEALTH → GEOX (challenge)
```
WEALTH.arif_vault_seal(outcome_status="CHALLENGED", rationale="...)
  → GEOX.claim_challenge(claim_id, challenger_id="WEALTH", rationale)
  → GEOX re-runs with updated economic constraints
  → GEOX.claim_create() with revised estimate
```

### Hermes → GEOX (ASI governance)
```
Hermes.arifOS_MCP_verify_claim(claim_id)
  → Checks: F1 Amanah, F2 truth, F4 clarity
  → Returns: SEAL / HOLD / VOID
  → If SEAL → arif_vault_seal() with ASI witness
```

---

## 7. Implementation Order

### Phase 1: Claim Lifecycle (P0)
**Week 1 - Make claims traceable**

1. geox_claim_create / validate / attach_evidence / challenge tools (in arifOS MCP)
2. arif_vault_seal integration
3. Simple claim list endpoint
4. Test: create one DRAFT claim, validate it, seal it

### Phase 2: Daily Cron (P0)
**Week 2 - GEOX wakes up and works**

1. geox-daily-scan cron job (06:00 MYT)
2. File watcher or timestamp diff for new seismic data
3. Basic claim creation from scan results
4. Telegram summary to Arif

### Phase 3: Cross-Organ (P1)
**Week 3 - GEOX talks to WEALTH**

1. A2A between GEOX and WEALTH
2. Reserve estimate → WEALTH pipeline
3. WEALTH economic re-evaluation loop

### Phase 4: ASI Governance (P1)
**Week 4 - Hermes watches GEOX**

1. Hermes subscribes to GEOX claim events
2. Hermes F1/F2 check on HIGH confidence claims before SEAL
3. Hermes surfaces summaries to Arif in group AAA

### Phase 5: Full Basin Loop (P2)
**Week 5-6 - autonomous basin model**

1. geox-weekly-basin full pipeline
2. geox_monthly_reserves pipeline
3. Uncertainty bands on all volume estimates

---

## 8. What SEAL Means Here

SEAL = immutable audit trail for every geological claim.

Not "the AI said it." Not "Arif confirmed."

```
SEAL {
  claim_id:      clm_xxxxxxxx
  content_hash:  sha256(claim_text)
  evidence_refs: [seismic_dataset_id, well_name, analog_field]
  methodology:   [geox_seismic_horizon_pick, geox_volume_calculate]
  confidence:    HIGH | MEDIUM | LOW
  sealed_by:     OPENCLAW | HERMES | ARIF
  sealed_at:     ISO8601
  outcome:       SEALED | REJECTED | CHALLENGED
  witnesses:     [arifOS_kernel, VAULT999]
}
```

Every SEAL has:
- Traceable tool chain (what tools generated this)
- Evidence references (what data it came from)
- Confidence band (not a single number - range)
- Witness line (who/what approved it)

---

## 9. Success Metrics

| Metric | Target | How Measured |
|--------|--------|---------------|
| Claims sealed per week | ≥ 5 | VAULT999 query |
| DRAFT → SEAL avg time | < 48h | Claim age at SEAL |
| Claims challenged | < 10% | Challenge count / total |
| Cross-organ handoffs | ≥ 2/week | A2A event log |
| Daily scan completion | 7/7 days | Cron log |
| ASI witness rate | 100% for HIGH confidence | SEAL witness field |
| False positive rate (VOID) | < 5% | VOID count / total |

---

## 10. Files

| File | Role |
|------|------|
| `forge_work/GEOX-AGI-SEAL-SPEC.md` | This spec |
| `forge_work/GEOX-CLAIM-LIFECYCLE.md` | Tool-level spec for claim lifecycle |
| `memory/2026-06-18-geox-agi-spec-sealed.md` | Seal receipt |
| `VAULT999/` | Immutable claim store |

---

*DITEMPA BUKAN DIBERI - GEOX earns its seals.*
