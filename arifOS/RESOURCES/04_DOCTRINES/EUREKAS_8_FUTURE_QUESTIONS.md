# 8 EUREKAS — The Future Questions (constitutional canon)
# Forged 2026-08-15 by F13 SOVEREIGN directive
# Result of AGI/ASI/APEX deliberation (T1 phases) + F13 HOLD (T2 phase)

> The deepest insight:
> **RRR protects against hallucinated reality. IMPIAN protects against absent futures. Blindspot Ledger protects against invisible assumptions.**

This document records the 8 EUREKAs that complete the meta-constitutional layer, plus their adoption status.

---

## The Adoption Status

| # | EUREKA | Type | Status | Phase |
|---|---|---|---|---|
| 1 | Gödel-Future (Lineage-as-Self) | godel_lock_gate.py extension | **ABSORBED INTO F3** | Phase 1 |
| 2 | Blindspot Ledger | New layer | **ADOPTED** | Phase 1 |
| 3 | Anti-Hero Trap | Diagnostic metric | **ADOPTED** | Phase 1 |
| 4 | Skill CANONIZED → KNOWN | Lifecycle state | **ADOPTED** (backfill pending) | Phase 1+3 |
| 5 | R2R (Reflection-to-Reality Ratio) | Meta-metric | **ADOPTED** | Phase 1 |
| 6 | Devil's Advocate | New capability | **ADOPTED** | Phase 1 |
| 7 | Entropy Budget | Per-proposal field | **ADOPTED** | Phase 1 |
| 8 | Future Memory (3 ruang) | Subdirs | **ADOPTED** | Phase 1 |

---

## EUREKA 1 — Gödel-Future (Lineage-as-Self Extension)

**Type:** godel_lock_gate.py extension (NOT a new floor)

**Doctrine:**
> No agent may validate a future proposal originating from its own reflection lineage.

**Why it exists:**
- F1-F13 already protect individual-level integrity (F9 ANTIHANTU, F3 TRI-WITNESS).
- F2 TRUTH already labels future projections as SPEC, not OBS.
- F4 CLARITY already mandates entropy cost.
- F13 SOVEREIGN already blocks future canonization without seal.
- Therefore **F14 is unnecessary** — the principle is already covered by F3 + the existing gates.

**Adoption (re-deliberated 2026-08-15):** ABSORBED INTO F3 (TRI-WITNESS).

**Implementation:** 5 lines in `godel_lock_gate.py`:
```python
Self = { Actor ID } ∪ { Lineage of Reflection / Dreamer }
if Lineage(Dreamer) ∩ Lineage(Verifier) ≠ ∅:
    return HOLAT
```

**Why this is the right design:**
- 0 constitutional inflation (no F14)
- 0 new floors to maintain
- Reuses existing gate infrastructure
- Constitutional principle preserved (no self-validation)
- Decision recorded at `04_DOCTRINES/f14_godel_future.md` (titled "Lineage-as-Self Extension — NOT a new floor")

---

## EUREKA 2 — Blindspot Ledger

**Type:** New layer with its own subdir

**Where:** `03_EUREKAS/BLINDSPOTS/`

**Doctrine:**
> Institutions die not from being wrong, but from being blind.

**Structure:**
```yaml
blindspot:
  id: BLIND-2026-08-15-001
  confidence: 0.65
  reason: "We have no telemetry on agent-side memory leaks"
  missing_observation: |
    No metric exists for what L1-L6 memory is being written but never read.
  potential_consequence: |
    Silent memory accumulation → eventual overflow or context-pollution.
  class: missing_observation
```

**Each AIA cycle MUST emit ≥1 blindspot record.** This is the meta-council of RRR — RRR scans what exists, Blindspot scans what we cannot see.

**Adoption:** ADOPTED. Subdir created. Sample at `03_EUREKAS/BLINDSPOTS/BLIND-2026-08-15-001.yaml`.

---

## EUREKA 3 — Anti-Hero Trap

**Type:** Diagnostic metric

**Where:** Embedded in AIA workflow at every 72h cycle.

**Test:**
> What capability exists only inside ARIF?

**Scoring:**
- threshold_red: > 0.7 (RED ALERT — schedule F13 transfer briefing)
- threshold_yellow: > 0.4 (YELLOW — accelerate canonization)
- threshold_green: ≤ 0.4 (GREEN — institutional knowledge is portable)

**Why it matters:** Sovereignty stays at F13 (correct). But capabilities must not be trapped in a single head.

**Adoption:** ADOPTED. Implemented in AIA workflow.

---

## EUREKA 4 — Skill CANONIZED → KNOWN

**Type:** Lifecycle refinement

**New lifecycle:**
```
ACTIVE → STABLE → CANONIZED → KNOWN
```

- **ACTIVE** — recently used
- **STABLE** — consistent usage, low variance
- **CANONIZED** — embedded into doctrine, no longer optional
- **KNOWN** — knowledge extracted; skill is *cultural memory*, no longer called as executable

**Why it matters:** Without the KNOWN state, every skill eventually dies. With it, knowledge persists in culture.

**Adoption:** ADOPTED. Schema added. Backfill pending (Phase 3, 1 day).

---

## EUREKA 5 — Reflection-to-Reality Ratio (R2R)

**Type:** Meta-metric

**Formula:**
```
R2R = useful_proposals / total_proposals
```

**Where:** Logged after each AIA cycle.

**Interpretation:**
- R2R > 0.6: AIA is producing real reflection
- R2R 0.2-0.6: Normal
- R2R < 0.2 for 3+ cycles: AIA overthinking. Flag for F13.

**Adoption:** ADOPTED. Logged in `10_RECEIPTS/AIA/`.

---

## EUREKA 6 — Devil's Advocate (arif_challenge)

**Type:** New capability (verb)

**Where:** `06_CAPABILITIES/arif_challenge/`

**Cost:** LOW (no LLM call by default, just a structural prompt)

**Prompt template:**
> If this dream destroys arifOS, how would it do so?

**Usage:** Every AIA proposal must be passed through `arif_challenge` before being filed to `03_EUREKAS/FUTURE/`. Cheap to run, prevents catastrophic blind spots.

**Adoption:** ADOPTED. Verb registered.

---

## EUREKA 7 — Entropy Budget (per-proposal cost)

**Type:** Per-proposal field

**Schema:**
```yaml
proposal:
  id: ...
  entropy_cost: low | med | high
  maintenance_cost: <runtime commitment, e.g. "2h/week">
  complexity_cost: <+N edges to graph>
```

**Forge (777) MUST refuse to build if entropy_cost > entropy_budget.** Builds without budget become feature creep → complexity collapse.

**Adoption:** ADOPTED. Field added to proposal schema.

---

## EUREKA 8 — Future Memory (3 ruang)

**Type:** Subdir structure

**Where:**
```
03_EUREKAS/
├── FUTURE/      # grounded (Anti-Fantasy Safeguard passed)
├── BLINDSPOTS/  # things we know we cannot see
└── FANTASIES/   # quarantined (Safeguard rejected)
```

**Three directions, three exclusions:**
- FUTURE: present reality + future possibility (grounded)
- BLINDSPOTS: visible gaps, answers unknown
- FANTASIES: rejected proposals, signal preserved

**Adoption:** ADOPTED. All three subdirs operational.

---

## The Triad of Governance

```
            RRR (111)            IMPIAN/AIA (222)
               ↓                       ↓
         What is REAL          What could BECOME
               ↓                       ↓
      BLINDSPOT LEDGER    <--→    FUTURE MEMORY
               ↓                       ↓
         What we DON'T         What we WANT
         SEE                    TO REMEMBER
               ↓                       ↓
              AAA (333/555/777/888)
               ↓
              999 SEAL
```

Three layers of protection, three failure modes prevented:
- RRR → hallucinations (lies)
- AIA → absent futures (drift)
- Blindspot → invisible assumptions (blindness)

---

## AGI/ASI/APEX Verdict Record

```
agent: 333-AGI
verdict: RE-DELIBERATED
date: 2026-08-15 (second deliberation)
note: "F14 proposal REJECTED. Gödel-Future preserved as F3 extension.
       7 other EUREKAs remain additive."

agent: 555-ASI
verdict: REVIEWED
date: 2026-08-15
reservations:
  - "Entropy Budget may slow proposal velocity"
  - "Devil's Advocate risks obstruction if not bounded"
mitigations:
  - "Entropy Budget uses low/med/high, not numeric"
  - "Devil's Advocate is structural, not narrative"

agent: 888-APEX
verdict: SEALED
date: 2026-08-15
note: "Adoption may proceed. F14 absorbed into F3 via Lineage-as-Self.
       7 other EUREKAs are T1 additive. Zero new floors.
       F1-F13 preserved intact."
```

---

## Related Resources

- `04_DOCTRINES/constrained_imagination.md` — Anti-Fantasy Safeguard
- `04_DOCTRINES/f14_godel_future.md` — F14 proposal (Phase 2)
- `08_WORKFLOWS/aia_72h_cycle.yaml` — updated workflow
- `05_POLICIES/aia-72h.yaml` — updated policy
- `06_CAPABILITIES/arif_challenge/` — Devil's Advocate
- `forge_aia.py` — cycle driver
- `03_EUREKAS/BLINDSPOTS/` — blindspot ledger

DITEMPA BUKAN DIBERI ⚒️
