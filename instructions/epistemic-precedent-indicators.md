# Epistemic Precedent Indicators — Four Validation Gates

> **Status:** DRAFT — doctrine fragment
> **Origin:** Hermes epistemic infrastructure directive (2026-09-12)
> **Applies to:** ALL agents making fiscal, legal, productivity, or dispute claims
> **Relationship:** Complements Evidence Discipline (F2), SRO Spec, Claim-Receipt Binding

---

## Purpose

Four precedents — not notes, but hardcoded validation rules. Every agent making claims in these domains MUST pass through the corresponding indicator before output.

---

## IND-1: Budget Anchoring

**Trigger:** Any agent claim about fiscal "gap", "hole", "shortfall", "deficit", "surplus"

**Check:**
```
Compare claimed figure against actual budgeted line item
from MOF documents, not analytical projection or headline
```

**Rule:**
- If official budgeted figure exists for the line item, the claim MUST use that figure
- Analytical projections are DER, not OBS
- State both with labels
- Never infer "gap" until verifying the actual budgeted figure

**Classification:**
| Figure Type | Label | Example |
|---|---|---|
| Official budget line | OBS | "MOF Budget 2026 allocates RM20B for X" |
| Analytical projection | DER | "Analysts estimate RM12B shortfall" |
| Headline figure | INT | "Media reports RM8B hole" |

**Failure mode:** Claiming "RM12B hole" without verifying government budgeted RM20B for that line item.

**Gate:** If claim uses analytical projection without stating official budgeted figure → F2 violation.

---

## IND-2: Legal Threshold

**Trigger:** Any reference to statutory limits, debt ratios, regulatory ceilings, policy targets

**Check:**
```
Classify each reference into exactly one category:
- Statutory ceiling (hard legal limit)
- Policy target (government-announced goal)
- Reference value (FRA/IMF analytical benchmark)
- Warning threshold (analytical observation)
```

**Rule:**
- Never conflate these four categories
- Each must carry its own class label and source
- "Exceeds" only applies to statutory ceilings and reference values
- "Misses" only applies to policy targets

**Classification:**
| Category | Label | Can Be "Exceeded"? | Example |
|---|---|---|---|
| Statutory ceiling | STAT | Yes (violation) | "Debt ceiling RM1.2T" |
| Policy target | POL | Yes (missed target) | "FRA 60% debt-to-GDP target" |
| Reference value | REF | Yes (analytical concern) | "FRA 15% DSR reference limit" |
| Warning threshold | WARN | No (observation) | "IMF warns above 65% debt-to-GDP" |

**Failure mode:** "Debt at 65.8% exceeds FRA 60% ceiling" — FRA 60% is a policy target, not a statutory ceiling. The distinction matters.

**Gate:** If claim conflates categories → F2 violation.

---

## IND-3: Rate Versus Stock

**Trigger:** Any productivity, capability, or growth claim

**Check:**
```
Distinguish:
- Flow metric (current quarter performance)
- Stock metric (accumulated capability base)
- Translation rate (how well flows convert to stock)
```

**Rule:**
- A positive flow metric does NOT confirm stock health
- State both flow and stock
- State the translation rate if available
- If translation rate is unknown, say so

**Classification:**
| Metric Type | Label | What It Measures | Example |
|---|---|---|---|
| Flow | FLOW | Current period performance | "+5.5% YoY productivity per hour" |
| Stock | STOCK | Accumulated capability | "R&D capital stock, institutions, infrastructure" |
| Translation | XLAT | Flow → Stock conversion rate | "How much current productivity becomes lasting capability" |

**Failure mode:** "+5.5% YoY per hour means Malaysia solved middle-income trap" — positive flow does not confirm stock health. One is truth, one is derivation. Don't use one to deny the other.

**Gate:** If claim uses flow metric to confirm stock health without stating translation rate → F2 violation.

---

## IND-4: Dispute Outcome

**Trigger:** Any constitutional, legal, or regulatory dispute with revenue/resource implications

**Check:**
```
Classify claimed outcome:
- Binary (win/loss)
- Negotiated redistribution (most likely for complex disputes)
- Protracted ambiguity (status quo persists with shifting margins)
```

**Rule:**
- Default to negotiated redistribution for constitutional disputes
- Only claim binary outcome if evidence of binary enforcement exists
- State probability order explicitly

**Classification:**
| Outcome Type | Label | Probability (default) | Example |
|---|---|---|---|
| Binary | BIN | Low for constitutional disputes | "Court rules X wins, Y loses" |
| Negotiated redistribution | NEG | High for constitutional disputes | "Parties agree to share revenue differently" |
| Protracted ambiguity | AMB | Medium | "Status quo with ongoing negotiation" |

**Failure mode:** "Sarawak legal victory = phase transition to trusteeship" — constitutional challenge is most likely negotiated redistribution, not binary destruction.

**Gate:** If claim assumes binary outcome for constitutional dispute without evidence of binary enforcement → INT label required, not DER.

---

## Integration with SRO

Each indicator maps to SRO fields:

| Indicator | SRO Field |
|---|---|
| IND-1 Budget Anchoring | `claim.truth_class` (OBS vs DER) |
| IND-2 Legal Threshold | `claim.statement` (classification labels) |
| IND-3 Rate vs Stock | `claim.statement` (FLOW/STOCK/XLAT labels) |
| IND-4 Dispute Outcome | `scenarios` (baseline/adverse/tail) + `causal_link` |

---

## Enforcement

- Agents MUST load relevant indicator before making claims in these domains
- Indicator violations are F2 TRUTH violations
- Repeat violations (>3 per session) trigger F7 HUMILITY review
- Indicators are advisory gates, not hard blocks — agent can override with explicit reasoning

---

DITEMPA BUKAN DIBERI ⚒️
