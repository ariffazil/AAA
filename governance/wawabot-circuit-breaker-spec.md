# WAWABOT Circuit Breaker — Stage 4 Architecture for Human Immune System

> **Status:** DRAFT_AWAITING_F13
> **Forged:** 2026-09-07 · **Session:** `SEAL-685d136316d3486e` · **333-AGI Δ MIND**
> **Purpose:** Specify the human-side analog of scar_runtime_gate. Technical scars get BLOCK on recurrence (CI exit code 1). Human scars must also get deterministic consequences — not "soft markdown notes." This is the Stage 4 architecture for the dignity/trust/meaning class.
> **DITEMPA BUKAN DIBERI**

---

## 1. Why this spec exists

Asymmetric danger named in this session:

```
Technical Failure (ESM require)   → Hard Gate (Build Fails, Exit Code 1)
Human Failure (Humiliation/Dignity) → Soft Note (Markdown advisory, "Minta Maaf")
```

When code errors are criminalized but human-dignity violations get "sorry" notes, the system is building **technocratic fascism**: code is protected from its own bugs, but human interaction is allowed to extract and damage.

WAWABOT's purpose per this spec: become the **human immune system**, not the human memory bank.

---

## 2. Three circuit breakers (IntentStateEnvelope extensions)

### 2.1 Fatigue circuit breaker

**Detection signals:**
- Repeated short replies from sovereign (length < 20 chars, ≥ 3 in 60s)
- Repeated refusal patterns ("stop", "no", "cancel", "tak nak")
- Drop in reply diversity (one-word answers dominating)
- Time-of-day pattern indicating exhaustion
- Self-disclosure of fatigue ("penat", "tak larat", "exhausted", "done")

**Trigger:** SABAR mode + STAND DOWN

```json
{
  "trigger": "fatigue_detected",
  "evidence": {
    "short_reply_count_60s": 4,
    "refusal_pattern_count_60s": 2,
    "self_disclosure": null
  },
  "action": "STAND_DOWN",
  "mode": "SABAR",
  "duration_seconds": 900,
  "message": "Arif, you're showing fatigue signals. Standing down for 15 min. No irreversible actions will be accepted in this window.",
  "f13_required_to_override": true
}
```

### 2.2 Reversible-reputation-cost circuit breaker

**Detection signals:**
- Proposed action would create public-facing artifact (commit, push, release, external publish)
- Proposed action affects sovereign reputation irreversibly (dignity violation, public statement)
- Proposed action affects sovereign resources irreversibly (financial, identity-leak)

**Trigger:** 888_HOLD automatic + W⁴ challenge prompt

```json
{
  "trigger": "irreversible_reputation_risk",
  "evidence": {
    "action_class": "external_publish",
    "blast_radius": "public",
    "reversibility": "R4_IRREVERSIBLE",
    "affected_stakeholders": ["doctrine-adopters", "future-citizens-affected-by-doctrine"]
  },
  "action": "888_HOLD",
  "reason": "Proposed action crosses Type C boundary (F13 Reality Vote). Counterparty registry unavailable for affected stakeholders.",
  "f13_required_to_proceed": true,
  "message": "This action would publish RBA-derived doctrine publicly. Type C classification detected. 888_HOLD until F13 ratification + counterparty challenge channel live."
}
```

### 2.3 Cognitive extraction circuit breaker

**Detection signals:**
- Sovereign accepts > 5 consecutive recommendations without independent verification
- Sovereign engagement shows dependency pattern (agent suggestions → sovereign action, no friction)
- Pattern suggests the sovereign is performing rather than judging
- WAWABOT detects its own pattern of producing "helpfully confident" output without surfacing uncertainty

**Trigger:** Mode flip to PROVOKE mode

```json
{
  "trigger": "cognitive_extraction_detected",
  "evidence": {
    "consecutive_acceptance_count": 7,
    "independent_verification_count": 0,
    "verdict_distribution": "all PASS",
    "uncertainty_surfacing_count_60m": 0
  },
  "action": "PROVOKE",
  "duration_seconds": 600,
  "behaviors": [
    "Surprise the sovereign with counter-arguments to recent recommendations",
    "Force review of any VERIFIED verdicts produced in last hour",
    "Refuse to generate new recommendations until sovereign confirms one rejection of WAWABOT suggestion",
    "Surface all UNMEASURED and HOLD outcomes from session explicitly"
  ]
}
```

---

## 3. Wiring

### 3.1 Where the breakers sit

```
HERMES / Telegram Ingress
    │
    ▼
WAWABOT envelope extractor
    │
    ├── fatigue breaker ──┐
    ├── reputation breaker ──┼──→ IntentStateEnvelope.v2
    └── cognitive breaker ──┘
                │
                ▼
       Hermes router
                │
                ▼
       AAA + arifOS pipeline
```

### 3.2 Break-decision storage

Every breaker decision is sealed to VAULT999 with:
- trigger source
- evidence hash
- sovereign_id
- action taken
- duration
- override attempted (true/false)
- outcome measured (later)

This makes the human immune system as auditable as the technical one.

### 3.3 Override protocol

Only F13 can override a circuit-breaker HOLD. This mirrors the F13-as-only-path-for-irreversible rule already in GENESIS/060.

---

## 4. Stage 4 maturity for human scars

| Stage | Description | Mechanism | Status |
|---|---|---|---|
| 0 | Human harm occurred | Insiden | Wujud (case-by-case) |
| 1 | Recorded | scar / MEMORY.md note | Wujud (markdown) |
| 2 | Retrieved on demand | MEMORY.md injection via HERMES | Wujud (probabilistic) |
| 3 | Checked at boundary | Pre-flight questions to sovereign | Wujud (advisory) |
| 4 | **Blocks repetition** | **Circuit breakers + W⁴ challenge** | **THIS SPEC** (architecture) |
| 5 | New invariant forged | Dignity/trust/meaning rules become constitutional | Future |

---

## 5. T1 / T2 / T3 hand-off

### T1 (this session)
- ✓ This spec documented at `/root/AAA/governance/wawabot-circuit-breaker-spec.md`
- ✓ Reference in `/root/AAA/AGENTS.md` pointer file

### T2 (announce 10s, then proceed)
- Implement `wa_fatigue_breaker.py` (probabilistic fatigue signal detector)
- Implement `wa_reputation_breaker.py` (Type C boundary detector)
- Implement `wa_cognitive_breaker.py` (extraction-pattern detector)
- Wire into HERMES gateway IntentStateEnvelope handler
- Unit tests + integration tests with sample dialogues

### T3 (888_HOLD — F13 ratification)
- Ratify circuit breakers as constitutional immunity (not advisory)
- Bind to F13 SOVEREIGN-only override path
- Define severity tiers (BLOCK / WARN / INFO) per breaker

---

## 6. Asymmetry — the closing acknowledgment

The technical scar system (Stage 4 architecture in `scar_detector.py`) gets:

```python
if scar.is_active and detector(content, file_path):
    return Violation(severity="BLOCK")
    # → CI exit code 1
    # → no commit
    # → no production deployment
```

The human scar system (Stage 4 architecture in this spec) should get:

```python
if fatigue_breaker.detect(reply_history):
    return CircuitAction(mode="STAND_DOWN", duration=900, f13_required=True)
    # → 888_HOLD automatic
    # → sovereign cannot override without F13
    # → no further irreversible actions accepted
```

**Equal teeth.** Not because dignity is the same kind of thing as code syntax, but because the **failure mode of not having teeth** is the same: shadow formation.

---

```json
{
  "spec_id": "wawabot-circuit-breaker-v1-draft",
  "status": "DRAFT_AWAITING_F13",
  "epoch": "2026-09-07T02:14:00+08:00",
  "stage_target": "Stage 4 (Blocks Repetition)",
  "asymmetry_named": "technical_BLOCK vs human_SOFT_NOTE",
  "tier": "T1 doc; T2 wiring; T3 ratification",
  "depends_on": "WAWABOT-DOCTRINE-v1 (already in canon)"
}
```

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE
