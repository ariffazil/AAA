# Kinabalu Well A/B — Discriminator Test Matrix

**Date:** 2026-09-29
**Discriminator set:** `geox://discriminators/north_sabah/diapir_thrust_miiec` (v1.0.0)
**Targets:** Well A (Stage IV gas + oil, Kinabalu closure), Well B (Stage IV post-MMU oil)
**Tool used:** `geox_seismic_alternative_interpret.v1` (3 hypotheses emitted, all HOLD)

---

## 1. Discriminator output (live, just executed)

All three hypothesis cards returned with `state: HOLD`, `claim_ceiling: HYPOTHESIS`, `evidence_class: ALTERNATIVE_INTERPRETATION`. Citation: Morley 2023 §6 + Figs 5–22.

---

## 2. Test Matrix — Required Observation × Well A/B Test

For each discriminator observation, the table below specifies:
- **Testable on Well A/B?** — YES / PARTIAL / NO
- **How** — the specific data source and metric
- **Decision** — what the test result means for each hypothesis

### Hypothesis A — Mobile-shale diapir

| Required observation | Testable? | How (Well A/B data) | Decision rule |
|---|---|---|---|
| Velocity LOW under highs | **YES** | Sonic log + VSP — compute interval velocity in Stage IV under the closure; compare to regional Vavg | V < Vavg × 0.92 → supports A |
| Continuous reflectors across sags | PARTIAL | Image-log dip across MD; check for consistent bedding dips between two picks separated by a "sag" | Consistent dips → supports A |
| Crestal graben above single-rising diapir | **NO** | Seismic-only feature | Cannot be tested from vertical well |
| DRU as single unfolded surface | **YES** | Dipmeter at DRU; check for repeated DRU picks | Single DRU → supports A |
| **Falsifier:** Vertical velocity normal → rejects A | | | |
| **Falsifier:** DRU appears folded → rejects A | | | |

### Hypothesis B — Thrust-cored anticline

| Required observation | Testable? | How (Well A/B data) | Decision rule |
|---|---|---|---|
| DRU folded, possibly thrust-repeated | **YES** | Dipmeter + image log at DRU level; cross-section from regional wells | Folded/repeated DRU → supports B |
| Reflectors offset across highs (folded-over) | **YES** | Image-log dip changes across MD; bed dip inversion | Offset dips → supports B |
| Velocity NORMAL under highs | **YES** | Same VSP/sonic as A | V ≈ Vavg → supports B (rejects A) |
| Thrust faults visible on flanks | **YES** | Image log + core (drag folds, cataclasite, mineralized slip surfaces) | Thrust fabrics in core → supports B |
| **Falsifier:** Vertical velocity low → rejects B | | | |
| **Falsifier:** Piercing structures (mud pipes) → rejects B | | | |

### Hypothesis C — Mud-volcano / MIEC feeder

| Required observation | Testable? | How (Well A/B data) | Decision rule |
|---|---|---|---|
| Transparent cores (seismic facies) | **NO** | Seismic facies only | Cannot be tested from vertical well |
| Vertical feeder pipes from below | PARTIAL | Image-log dip azimuth near IVC; vertical fabric (near-vertical dips) → supports C | Vertical fabric → supports C |
| IVC onlap onto edifice flanks | **NO** | Seismic geometric | Cannot be tested from vertical well |
| Gas chimneys above edifices | PARTIAL | Gas shows in logs above IVC (sonic low, resistivity high, neutron-density crossover) | Multiple stacked gas zones → supports C |
| **Falsifier:** DRU folded, not pierced → rejects C | | | |
| **Falsifier:** No vertical pipes AND no chimneys → rejects C | | | |

---

## 3. Decisive best-test per hypothesis (cheapest first)

| Hypothesis | Decisive test on Well A/B | Cost | Information yield |
|---|---|---|---|
| **A** | Compute interval velocity in Stage IV from sonic/VSP | LOW | HIGH — single value discriminates A from B |
| **B** | Dipmeter at DRU level + image-log dip profile | LOW | HIGH — single pass detects folding |
| **C** | Image-log dip azimuth near IVC + gas-show inventory | MEDIUM | MEDIUM — gas shows are ambiguous (could be source rock or migration) |

**Recommendation order:** run A's velocity test FIRST. If velocity is low → A wins (or C with gas). If velocity is normal → B likely. Then run dipmeter for B confirmation. Then C if both prior tests are inconclusive.

---

## 4. Decision tree (binary branching)

```
START: Well A/B Stage IV sonic+VSP+dipmeter+image-log+core
  │
  ├── Stage IV interval velocity < Vavg × 0.92 ?
  │     ├── YES → Support A (or C if gas shows)
  │     │         └── C gas shows present?
  │     │               ├── YES → Support C (with vertical fabric)
  │     │               └── NO  → Support A
  │     └── NO  → Support B (or reject A and C)
  │               └── DRU folded (dipmeter)?
  │                     ├── YES → Support B
  │                     └── NO  → INCONCLUSIVE (need seismic)
  │
  └── Seismic tie (if available):
        ├── Reflectors offset across closure crest → Support B
        ├── Reflectors continuous across crest → Support A
        └── Transparent core + vertical fabric → Support C
```

---

## 5. Required data from Well A/B (extract from PETRONAS internal — sovereign gate)

| Data | Source | Used in |
|---|---|---|
| Sonic log (DT or slowness) | Standard logging suite | Velocity test (A, B) |
| VSP / checkshots | If acquired | Velocity calibration (A, B) |
| Density log (RHOB) | Standard logging suite | Velocity + lithology |
| Image log (FMI/DSI/OBMI) | Specialized logging | Dip profile (A, B, C) |
| Dipmeter (if no image log) | Standard | Dip profile (A, B, C) |
| Core photographs + descriptions | Core analysis | Thrust fabrics (B), mud-pipe textures (C) |
| Gas-show inventory (mud log, RFT) | Drilling | Gas chimney detection (C) |

**Access path:** sovereign invokes F13 to open PETRONAS internal data; AA-hermes routes the request through the proper privacy lane per `00-EPISTEMIC-HEADER.md` 4-lane routing doctrine.

---

## 6. What this test matrix proves vs what it doesn't

### Proves

- **The discriminator logic is portable** to well data (not just seismic)
- **A single decisive test exists** per hypothesis (velocity for A, dipmeter for B, image-log for C)
- **Each hypothesis has ≥3 falsifiable observations** that can be checked on actual rock data
- **The discriminator resource** (`geox://discriminators/north_sabah/diapir_thrust_miiec`) is consumable programmatically via `geox_seismic_alternative_interpret.v1`

### Does NOT prove

- Whether A, B, or C is "right" for Kinabalu — that requires actual well data + sovereign authorization to access
- Whether the discriminator applies equally to onshore Kinabalu as to offshore Sabah Shelf (the analog is structural, not stratigraphic)
- Quantitative confidence — only binary (supports/rejects) per hypothesis
- Production implication (trap, seal, charge) — separate workflow

---

## 7. What I did NOT do

- ❌ Did NOT fabricate Well A/B core/log data (none in canon)
- ❌ Did NOT pick a winning hypothesis (all remain HOLD per Canon #0)
- ❌ Did NOT auto-seal any result (hermes witness only; F13 SEAL pending)
- ❌ Did NOT access any PETRONAS internal data (mode-600 sovereign gate)
- ❌ Did NOT propose modifying the discriminator resource

---

## 8. Canon compliance

- **F2 TRUTH:** every observation mapped to specific data source; no fabrication
- **F7 insider bias:** acknowledged — the user is a PETRONAS employee
- **APEX REALITY KERNEL:** Reality > Everything — output structured around "what would test it" not "what it probably is"
- **Canon #0:** every discriminator card is HOLD with concrete reason
- **Anti-Haram:** technical mapping, not institutional critique
- **Anti-Bangang LAW 4:** "Apa masalah yang diselesaikan?" → provides a runnable test, not more interpretation

---

## 9. Next step (one binary)

**A)** Sovereign invokes F13 to open Well A/B data access → I run the velocity test + dipmeter test → I update the hypothesis states (some HOLD → some ACTIVE).

**B)** Save this test matrix to `/root/AAA/instructions/kinabalu-discriminator-test-matrix.md` for project-team access → handover to the well-evaluation team.

**C)** Both — sovereign authorizes data + I save + hand off.

I lean **B** (smallest, no data movement, audit-trail preserved).

Pick A, B, or C.
