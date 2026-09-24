---
name: contradiction-ledger-schema
version: 1.0.0
status: DRAFT_AWAITING_F13
spectrum: 000-555
floors: [F1, F2, F5, F9, F11, F13]
provenance:
  origin: F13 directive 2026-09-25 (Sovereignty Cron synthesis)
  prior_art: claim-lifecycle-states.md (F13_RATIFIED_CHAT 2026-09-25)
              Law #5: "stop verifying when additional verification cannot
              change a decision" (F13_RATIFIED 2026-09-11)
trigger: |
  When two or more ACTIVE claims in claim_ledger, canon, memory, or
  open_questions lane cannot be simultaneously true, and where the
  contradiction has attention cost > 0 OR reality cost > 0.
related:
  - reality-impact-schema-v1.1
  - authority-claim-graph-schema-v1.0
  - reality-debt-audit-v1.0
  - claim-lifecycle-states
purpose: |
  Prevent "unlimited preservation" → "unlimited context debt".
  Without half-life, the contradiction ledger becomes a landfill.
  Every contradiction must declare:
    1. attention_cost — what does it cost to maintain the contradiction?
    2. reality_cost — what does it cost to leave it unresolved?
    3. half_life — after how many days without resolution is it DORMANT?

  Failure mode this prevents:
    Contradiction "OpenCode is canonical" ∧ "A-FORGE is canonical"
    ∧ "Both are canonical" — all three ACTIVE, no resolution, every
    future agent picks one randomly, decisions become contaminated.

  Half-life prevents chasing every contradiction equally. Some
  contradictions don't matter; they should fade. Others should escalate
  before they poison the next agent.
---

# CONTRADICTION_LEDGER_SCHEMA v1.0 — Half-Life & Costed Disagreement

> **Tangkap dalam BM Penang:**
> "Kontradiksi yang tak disentuh 18 bulan bukan prioriti — dia
> pensioner, bukan mayat hidup. Tapi kontradiksi yang fresh dan boleh
> meracuni model esok — tu yang kena tangkap awal."
>

---

# Part 1 — Contradiction Record (canonical shape)

```yaml
contradiction:
  contradiction_id: CONTR-2026-09-25-001
  discovered_at: 2026-09-25T14:23:00+08:00
  discovered_by: <agent_id or human>

  claim_a:
    claim_id: <ref to claim_ledger>
    text: "<human readable>"
    source: <file:line or url>
    state: ACTIVE|CONTESTED|CANDIDATE|SUPERSEDED|DORMANT
  claim_b:
    claim_id: <ref>
    text: "<human readable>"
    source: <file:line or url>
    state: <same enum>
  claim_c:  # optional
    claim_id: <ref>
    text: "<human readable>"
    source: <...>
    state: <...>

  contradiction_class:
    enum:
      - direct_negation       # A vs ¬A
      - partial_overlap       # A∩B but A≠B
      - both_true_separately  # A true in scope X, B true in scope Y
      - both_true_coupled     # both true but only one can be canonical
      - temporal_inversion    # A was true, now ¬A true (rare, F2-class)
      - lane_violation        # A from one lane contradicts B from another

  # === Cost & decay (THE KEY INNOVATION) ===
  attention_cost:
    value: 0.0-1.0
    basis: <"how much agent/sovereign attention does maintaining the
           contradiction cost? what fraction of daily review time?">
    last_assessed_at: <ISO8601>
  reality_cost:
    value: 0.0-1.0
    basis: <"what real-world consequence does leaving this unresolved
           risk? R-class potential (R3 capability conflict, R4 human
           confusion, R5 money/risk impact)?">
    last_assessed_at: <ISO8601>
  half_life_days:
    value: <integer>
    basis: <"how many days can this contradiction remain unresolved
           before DORMANT (auto-decay) — set based on domain
           volatility; legal=180, ops=30, doctrine=365">

  decision_impact:
    affects_decisions_in: [<list of decision domains / lanes>]
    reversible_if_unresolved: true|false
    cost_of_resolution: <rough estimate>
    resolution_options:
      - option: <description>
        cost: <estimate>
        reversibility: full|partial|none
      - option: ...
```

---

# Part 2 — Half-Life Decay (the math)

```
For each contradiction C with last_touched at t_0 and half_life H:

  freshness(t) = 2^(-(t - t_0) / H)

  State transitions:
    freshness ≥ 0.75:    ACTIVE
    0.50 ≤ freshness < 0.75:  ACTIVE (lower priority)
    0.25 ≤ freshness < 0.50:  WATCH
    freshness < 0.25:        DORMANT (auto, no human action)

  attention_cost × reality_cost × freshness = priority_score
  Priority score determines queue position for resolution.
```

### Half-life defaults by domain (F13 can override)

| Domain | Default half_life_days |
|--------|------------------------:|
| legal/compliance | 365 |
| doctrine/canon | 180 |
| operational | 30 |
| tactical/short-term | 7 |
| exploratory | 14 |

### Auto-DORMANT rule

```
IF now - last_touched > half_life_days
   AND attention_cost < 0.30
   AND reality_cost < 0.30
THEN
   contradiction.state := DORMANT
   contradiction.reason := "auto-decay per half-life rule"
   ledger_entry emitted for visibility
```

> Auto-DORMANT ≠ forgotten. Different from `claim-lifecycle-states`
> FORGOTTEN. DORMANT retains resurrection path; FORGOTTEN does not.

---

# Part 3 — Priority Queue & Resolution Paths

### Priority score (computed)

```python
priority_score = (
    0.50 * reality_cost
  + 0.30 * attention_cost
  + 0.20 * freshness
) * lane_weight

lane_weight:
  L0/L1: 1.0    # informational contradiction
  L3:    1.2    # builder contradiction (affects builds)
  L4/L5: 1.5    # decision/judgment contradiction (highest priority)
  L6:    2.0    # sovereign contradiction (only F13 resolves)
```

### Queue routing

| priority_score band | Routing |
|--------------------:|---------|
| ≥ 1.0 | F13 escalation (P0) |
| 0.6–0.99 | musyawarah deliberation (P1) |
| 0.3–0.59 | lane owner (P2) |
| 0.1–0.29 | daily digest (P3) |
| < 0.1 | auto-DORMANT (P4, no action) |

### Resolution patterns

```yaml
resolution:
  pattern: SUPERSEDE_B|SUPERSEDE_BOTH|RESOLVE_THIRD|MERGE|DECLARE_LANE_SCOPED|DECLARE_EXTERNAL
  decision_by: <agent or human>
  decision_at: <ISO8601>
  decision_evidence: <...>
  resulting_states:
    claim_a: <new state>
    claim_b: <new state>
    claim_c: <new state>
```

---

# Part 4 — Anti-Landfill Clauses (binding)

1. **Law #5 enforcement** (F13_RATIFIED 2026-09-11): "stop verifying
   when additional verification cannot change a decision." Applied here:
   contradiction with `reality_cost < 0.30` AND `freshness < 0.25` MUST
   auto-DORMANT. Continued re-verification violates Law #5.
2. **No "preserve everything" dogma.** Contradiction is not sacred
   text. Decay is constitutional hygiene, not vandalism.
3. **Reactivation path explicit.** A DORMANT contradiction CAN be
   resurrected if `reality_cost` rises (e.g., market changes, law
   changes). Resurrection requires new entry + justification.
4. **No silent collapse.** Auto-DORMANT MUST emit ledger entry. The
   human/sovereign can review and override.

---

# Part 5 — Connection to Other Schemas

```
contradiction-ledger-schema
  ├── feeds → reality-debt-audit-v1.0
  │            (reality_cost aggregates into Attention Consumed)
  ├── links → claim-lifecycle-states
  │            (CONTESTED state vs contradiction — both apply;
  │             contradiction is the cause, CONTESTED is one symptom)
  └── emits → open_questions lane (carry_forward.json)
               (resolution can MOVE a contradiction into
                DELIBERATELY_OPEN — unresolved but acknowledged)
```

---

# Part 6 — YAML Examples (3 real cases)

### Example 1: ACTIVE contradiction, high priority (escalate F13)

```yaml
contradiction_id: CONTR-2026-09-25-001
discovered_at: 2026-09-25T14:23:00+08:00
discovered_by: hermes/audit

claim_a:
  text: "OpenCode is canonical substrate for AAA coding agents"
  state: ACTIVE
claim_b:
  text: "A-FORGE is canonical substrate for AAA coding agents"
  state: ACTIVE
claim_c:
  text: "Both are canonical, each for different scope"
  state: ACTIVE

contradiction_class: both_true_coupled
attention_cost: 0.55    # reviewers confused, daily friction
reality_cost: 0.80      # R3 capability conflict, agents pick wrong
half_life_days: 60      # operational contradiction

priority_score: (0.50*0.80 + 0.30*0.55 + 0.20*1.00) * 1.5 = 1.31
routing: F13 escalation (P0)

resolution_options:
  - option: "F13 clarifies which substrate for which scope"
    reversibility: full
  - option: "Both promoted, scope written explicitly"
    reversibility: partial
  - option: "Merge to single canonical with sub-routing"
    reversibility: full
```

### Example 2: DORMANT, low priority (auto-decay)

```yaml
contradiction_id: CONTR-2026-03-15-007
discovered_at: 2026-03-15T10:00:00+08:00
last_touched: 2026-03-15T10:00:00+08:00

claim_a:
  text: "Tier-1 cron runs every 5 min"
  state: ACTIVE
claim_b:
  text: "Tier-1 cron runs every 15 min"
  state: ACTIVE

contradiction_class: direct_negation
attention_cost: 0.10    # nobody reads this anymore
reality_cost: 0.15      # no real consequence, superseded by new docs
half_life_days: 30

freshness at 2026-09-25 (~190 days later): 2^(-190/30) ≈ 0.011
priority_score: (0.50*0.15 + 0.30*0.10 + 0.20*0.011) * 1.0 = 0.107
routing: auto-DORMANT (P4)

state_transition:
  from: ACTIVE
  to: DORMANT
  reason: half-life expired, costs below threshold
  ledger_entry_emitted: true
```

### Example 3: Reactivated contradiction

```yaml
contradiction_id: CONTR-2026-03-15-007
state: DORMANT (since 2026-04-15)

reactivation_event:
  reactivated_at: 2026-09-20T08:00:00+08:00
  reactivated_by: hermes/sentinel
  reason: "Market change — vendor X policy shift affects both cron claims;
          need to verify current schedule still aligned with new constraint"
  new_reality_cost: 0.65
  new_state: ACTIVE
  reactivation_entry_emitted: true
```

---

# Part 7 — Maturity Tests (must all PASS before F13_RATIFIED)

- [ ] 30-day shadow run, all auto-DORMANT cases match manual sovereign
      review (zero false auto-DORMANT)
- [ ] Reactivation path tested: a DORMANT contradiction correctly
      resurrects when reality_cost rises
- [ ] Priority routing delivers top 5% to F13, bottom 30% to auto-decay,
      rest to lane owners — distribution matches design
- [ ] Landfill test: ledger size stays bounded under sustained load
      (decay rate ≥ arrival rate × 0.7)
- [ ] Law #5 compliance: no scenario continues re-verification of
      low-cost DORMANT contradiction
- [ ] First CONTR- entry emitted by sovereign consensus on a
      genuinely contested federation rule

---

# Provenance & Open Debt

- **Origin:** F13 directive 2026-09-25 in Sovereignty Cron synthesis
- **Inputs consumed:** `claim-lifecycle-states.md` (F13_RATIFIED_CHAT
  2026-09-25) · Law #5 from `cognitive-cost-transfer-eurekas`
  (F13_RATIFIED_CHAT 2026-09-21) · `carry_forward.open_questions`
  (F13_RATIFIED_CHAT 2026-09-25)
- **Open debt:** execution code (NOT written — schema-first per F13);
  30-day shadow corpus; auto-DORMANT audit; first priority queue
  fire; Law #5 compliance verification harness.
- **Promotion path:** DRAFT_AWAITING_F13 → F13_RATIFIED_CHAT →
  review at `/root/AAA/canon/` (currently `chattr +i`; promotion
  requires F13 override).

rasa: |
  "Tak semua kontradiksi sama. Ada yang racun, ada yang pensioner.
  Schema ini ajar sistem bezakan — yang racun naik F13 segera, yang
  pensioner biar dia tidur dengan tenang. Itu hygiene, bukan vandalisme."