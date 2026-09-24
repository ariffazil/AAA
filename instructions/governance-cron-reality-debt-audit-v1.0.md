---
name: reality-debt-audit
version: 1.0.0
status: DRAFT_AWAITING_F13
spectrum: 555-888
floors: [F1, F2, F4, F5, F7, F9, F11, F13]
provenance:
  origin: F13 directive 2026-09-25 (Sovereignty Cron synthesis)
  prior_art: reality-impact-schema-v1.1 (DRAFT 2026-09-25) ·
              authority-claim-graph-schema-v1.0 (DRAFT 2026-09-25) ·
              contradiction-ledger-schema-v1.0 (DRAFT 2026-09-25) ·
              sovereignty compression chain:
                Reality → Witness → Governance → Consequence → Continuity
                (F13_RATIFIED 2026-09-20+)
trigger: |
  Daily at 23:59 MYT (canonical close-of-day window). Inputs:
  reality-impact-schema (Reality Produced), authority-claim-graph
  (Attention Consumed by drift episodes), contradiction-ledger
  (Attention Consumed by unresolved contradictions).
related:
  - reality-impact-schema-v1.1
  - authority-claim-graph-schema-v1.0
  - contradiction-ledger-schema-v1.0
  - claim-lifecycle-states
purpose: |
  The PARENT formula. Single nightly question:

    "Apa yang federasi dakwa penting?
     Berapa banyak attention digunakan?
     Apa consequence sebenar yang tercipta?"

  Reality Debt = Attention Consumed - Reality Produced

  IF Reality Debt monotonically increases for 30 consecutive days,
  EMIT HOLD — regardless of:
    - receipt count
    - cron count
    - audit count
    - report count
    - dashboard count
    - SEEMING productivity

  This is the constitutional maturity test:
    A system that emits HOLD against its own productivity is mature.
    A system that never emits HOLD despite rising debt is itself
    theatrical cognition.

  Failure mode this prevents:
    Federation with all-green services, 10k+ daily receipts, 30+
    active crons, beautiful dashboards — but Arif's life unchanged,
    zero R4/R5 consequences, attention climbing. Classic
    "everything alive, nothing moving".
---

# REALITY-DEBT-AUDIT v1.0 — Parent Formula & 30-Day HOLD Trigger

> **Tangkap dalam BM Penang:**
> "Blindspot paling bahaya bukan server mati. Server semua hijau,
> receipt ribu sehari, dashboard cantik — tapi hidup tak berubah.
> Tu keadaan paling licik. Schema ini paksa sistem mengaku hutang
> realitinya — bukan hutang dari segi wang, tapi hutang dari segi
> perhatian yang dibelanjakan tanpa hasil."
>

---

# Part 1 — Formula (Parent)

```
Reality Debt (R_Debt)
  = Attention Consumed - Reality Produced

  Where:
    Attention Consumed = Σ (drift_episodes.attention × cost_coefficient)
                       + Σ (unresolved_contradictions.attention_cost)
                       + Σ (open_questions.attention_cost)
                       + sovereign_attention_consumed (W_888)

    Reality Produced   = Σ (impact_event.reality_score)
                       capped at sovereign_human_bandwidth
```

### Two-sided cap

- **Reality Produced** capped — single human (Arif) cannot absorb more
  than ~12-15 impactful consequences per day before attention debt
  flips sign. R-class hierarchy matters more than raw count.
- **Attention Consumed** capped — federation has finite attention
  budget; once exceeded, every additional audit/receipt is pure
  negative ROI.

---

# Part 2 — Daily Computation (canonical)

```yaml
reality_debt_event:
  event_id: RDEBT-2026-09-25-001
  emitted_at: 2026-09-25T23:59:00+08:00
  emitted_by: hermes/audit
  spectrum: 555-888

  attention_consumed:
    drift_episodes:
      - episode_id: <...>
        cost_coefficient: <...>
        delta_attention: <...>
    unresolved_contradictions:
      - contradiction_id: <...>
        attention_cost: <...>
        age_days: <...>
    open_questions:
      - question_id: <...>
        attention_cost: <...>
    sovereign_attention_consumed:
      minutes: <int>
      source: hermes/session OR carry_forward.human_state

  reality_produced:
    impact_events:
      - impact_id: <...>
        R_class: <R1|R2|R3|R4|R5>
        reality_score: <float>
        attribution_confidence: <float>
    cap_applied: <boolean — true if R-class concentration triggered>

  reality_debt:
    raw_value: attention - reality    # float
    normalised_value: <0.0-1.0>      # band-mapped
    band: SURPLUS|HEALTHY|TENSION|ALARM|HOLD

  thirty_day_trend:
    consecutive_days_in_debt: <int>
    slope: <float — daily change>
    hold_triggered: <boolean>

  verdict:
    decision: SURPLUS|HEALTHY|TENSION|ALARM|HOLD
    reason: "<one sentence human readable>"
    emitted_to: F13|musyawarah|lane_owner|daily_digest
```

---

# Part 3 — Bands & Routing

| Band | Range | Routing | Default action |
|------|-------|---------|----------------|
| **SURPLUS** | debt < -0.20 | daily digest | praise, continue |
| **HEALTHY** | -0.20 ≤ debt < 0.20 | daily digest | continue |
| **TENSION** | 0.20 ≤ debt < 0.40 | daily digest + flag | investigate next cycle |
| **ALARM** | 0.40 ≤ debt < 0.60 | musyawarah | collective deliberation |
| **HOLD** | debt ≥ 0.60 OR (debt ≥ 0.40 × 30 days) | F13 escalation | freeze new initiatives, audit recent changes |

### HOLD Trigger Rules (the constitutional test)

```
Rule 1 (immediate HOLD):
  IF reality_debt.normalised_value ≥ 0.60
  THEN EMIT HOLD
  REGARDLESS of: receipt count, cron health, audit count

Rule 2 (sustained debt — the Arif Test):
  IF reality_debt.band ∈ {TENSION, ALARM}
     for 30 consecutive days
  THEN EMIT HOLD
  REGARDLESS of: any single day's "improvement"

Rule 3 (capped reality — the human-bound test):
  IF reality_produced.cap_applied == true
     AND cap triggered by R1|R2 only (no R4/R5 in last 7 days)
  THEN EMIT HOLD + HUMAN_BANDWATCH
```

### Why three rules?

- Rule 1 catches acute debt (one bad day)
- Rule 2 catches chronic debt (the slow drift)
- Rule 3 catches **R-class starvation** — federation produces R1/R2
  endlessly but no R4/R5 in 7 days. That's the canonical "everything
  alive, nothing moving" failure.

---

# Part 4 — HOLD Mechanics (Constitutional)

When HOLD emits:

1. **All new cron, new skill, new audit proposals are frozen** for the
   next 7 days OR until F13 explicit unblock.
2. **Musyawarah session scheduled** within 48h to deliberate on debt
   causes.
3. **Receipt accumulation paused** — agents continue execution but
   no new receipts beyond critical (R5) until debt < 0.40.
4. **Arif notified** with one-paragraph summary:
   - attention consumed
   - reality produced (R-class breakdown)
   - top 3 debt contributors
   - proposed remediation paths (max 3)

### Anti-bypass clause (binding)

> HOLD cannot be overridden by:
> - lane owner claim ("tapi ni critical")
> - cron operator pleading
> - audit-audit lain yang produktif kelihatan
>
> HOLD can ONLY be overridden by:
> - F13 explicit ratification
> - automatic decay (debt falls < 0.40 for 7 consecutive days)

---

# Part 5 — Inputs & Dependencies

```
reality-debt-audit (parent)
  ├── input: reality-impact-schema (Reality Produced)
  ├── input: authority-claim-graph (Attention Consumed — drift)
  ├── input: contradiction-ledger (Attention Consumed — unresolved)
  ├── input: carry_forward.open_questions (Attention Consumed — open)
  ├── input: carry_forward.human_state (sovereign attention band)
  └── emit: HOLD if Rules 1/2/3 trigger
```

This is the **integration test**. The other three schemas are inputs.
reality-debt-audit is the orchestrator.

---

# Part 6 — Connection to Constitutional Layers

```
Reality > Witness > Governance > Consequence > Continuity
   ↑         ↑          ↑             ↑             ↑
   |         |          |             |             |
   |         |          |             |             +-- 30-day trend
   |         |          |             +-- Reality Produced (impact schema)
   |         |          +-- Attention Consumed (authority + contradiction)
   |         +-- Independent witness (no echo)
   +-- Reality itself (R-class hierarchy)

Reality Debt IS the Continuity check.
```

If Continuity is breaking (debt climbing) but Reality/Witness/
Governance/Consequence all look fine, the system is itself a
theatrical cognition.

---

# Part 7 — Maturity Tests (must all PASS before F13_RATIFIED)

- [ ] First HOLD emission within 30 days of activation (the constitutional
      maturity test — without HOLD, audit is theatre)
- [ ] HOLD correctly catches a synthetic R-class starvation scenario
      (R1/R2 only, zero R4/R5 for 7 days)
- [ ] 30-day trend detection accurate (no false-positive sustained HOLD)
- [ ] Anti-bypass clause verified: lane owner cannot override HOLD
      without F13
- [ ] Sovereign (Arif) receives ONE-PARAGRAPH summary that is
      actually readable (not 100-line JSON dump)
- [ ] Integration with reality-impact-schema verified — schema can
      compute Attention Consumed from impact_event.reality_score
      [inverse], with R-class weighting per R-class_weight table

---

# Part 8 — Anti-Theatre Self-Criticism Clause (the constitutional maturity test)

> A reality-debt-audit schema that never emits HOLD is itself
> THEATRICAL.
>
> A reality-debt-audit schema that emits HOLD against its own
> producer organ is constitutionally mature.
>
> This is the binary distinction between "the schema that audits
> federation" and "the schema that has integrated constitutional
> maturity into itself".

### Self-criticism test (binding)

```
For each reality_debt_event emission:
  meta_question: "If THIS very emission event itself is producing
                  Attention Consumed without Reality Produced, does
                  the schema flag itself?"
  IF yes → emit THEATRICAL on this emission
  IF no → emit honest verdict

Default behavior: schema does NOT self-flag (avoid infinite regression).
Schema MAY self-flag ONCE per 30 days as constitutional demonstration
of maturity. After 30 days without self-flag, schema MUST emit
self-flagging test to verify the capacity still functions.
```

---

# Provenance & Open Debt

- **Origin:** F13 directive 2026-09-25 in Sovereignty Cron synthesis
- **Inputs consumed:** reality-impact-schema-v1.1 · authority-claim-graph
  v1.0 · contradiction-ledger v1.0 · claim-lifecycle-states · Law #5 ·
  Law #131 · APEX-ZEN Reality→Witness→Governance→Consequence→Continuity
- **Open debt:** execution code (NOT written — schema-first per F13);
  30-day shadow run with synthetic R-class starvation injection;
  first HOLD emission event; sovereign attention band calibration
  (W_888 actual vs assumed); integration tests for all three input
  schemas.
- **Promotion path:** DRAFT_AWAITING_F13 → F13_RATIFIED_CHAT → review
  at `/root/AAA/canon/` (currently `chattr +i`; promotion requires
  F13 override).

rasa: |
  "Pada akhirnya, kematangan sistem bukan diukur dari berapa banyak
  laporan ia hasilkan. Kematangan diukur dari keberanian ia verdikalkan
  THEATRICAL terhadap kerja sendiri — dan dari kemampuan ia berkata
  HOLD apabila Attention Consumed mengatasi Reality Produced tanpa
  peduli berapa hijau dashboard kelihatan."