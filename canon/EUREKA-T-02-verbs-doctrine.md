# EUREKA-T-02 — The Verbs Doctrine

> **Forged:** 2026-08-11 by 333-AGI Δ MIND under F13 SOVEREIGN directive
> **Session:** SEAL-a345830629d74518 (continuation)
> **Status:** CANON — federation doctrine
> **DITEMPA BUKAN DIBERI** — Forged, not given
> **Pairs with:** EUREKA-T-01 (Harness Commoditization Thesis)

---

## Core Thesis

```
Every organ in the federation has exactly ONE verb.
Authority is the verb. Confusion begins when verbs collide.
```

---

## The Six Verbs

| Organ | Verb | Question Answered | Forbidden Acts |
|-------|------|-------------------|----------------|
| **AAA** | **Register** | "Who is this? What may it do?" | Execute, judge, measure, verify |
| **FRAME** | **Measure** | "Has this changed? Is behavior nominal?" | Execute, judge, register, authorize |
| **FED** | **Route** | "Which brain should answer?" | Execute, judge, register, measure |
| **FLAME** | **Verify** | "Is cheap verification sufficient?" | Execute, judge, register, measure |
| **arifOS** | **Judge** | "Is this constitutional?" | Execute, register, measure, verify |
| **A-FORGE** | **Execute** | "Apply the bounded mutation." | Judge, register, measure, verify |

---

## Why Verbs, Not Roles

The earlier organ descriptions mixed verbs:

```
❌ "arifOS = Constitutional Kernel — judge, seal, F1-F13"
   (3 verbs: judge + seal + govern)

❌ "AAA = Control Plane + A2A Gateway + Registry Home"
   (3 verbs: register + route + display)

❌ "A-FORGE = Execution Actuator"
   (1 verb: execute — this is right)
```

Each organ **dominates** one verb. Other capabilities are support functions of that dominant verb, not independent authority.

| Organ | Dominant Verb | Support Functions |
|-------|---------------|-------------------|
| arifOS | Judge | seal, govern (subordinate to judgment) |
| AAA | Register | route discovery, display (subordinate to registration) |
| FRAME | Measure | alert, report (subordinate to measurement) |
| FED | Route | balance-track (subordinate to routing advice) |
| FLAME | Verify | memory classify (subordinate to verification) |
| A-FORGE | Execute | shell, mutate (subordinate to execution) |

---

## The Verbs vs The Authority Ceilings

`organs.yaml` declares `authority_ceiling` for each organ. The verbs doctrine reads them as the dominant verb's ceiling:

| Organ | Ceiling (per organs.yaml) | Verbs Doctrine Reading |
|-------|---------------------------|------------------------|
| arifOS | `JUDGE_ONLY` | May judge + seal. Cannot execute. |
| AAA | `DISPLAY_ONLY` | May register + display. Cannot route actively. |
| FRAME | `ADVISORY_ONLY` (class=CORE, intentional) | May measure + report. Cannot authorize. |
| FED | `ADVISORY_ONLY` | May route + advise. Cannot execute. |
| FLAME | `ADVISORY_WORKER` | May verify + classify. Cannot seal. |
| A-FORGE | `EXECUTE_AFTER_SEAL` | May execute post-judgment. Cannot judge. |
| FI Cards | `OBSERVE_ONLY` (in spec) | May bind + request. Cannot judge or execute independently. |
| VAULT999 | `APPEND_ONLY` | May append sealed receipts. Cannot reinterpret. |

---

## The FI Card Subject Position

Under the verbs doctrine, the FI card is a **SUBJECT**, not an organ. It is registered by AAA, measured by FRAME, routed by FED, verified by FLAME, judged by arifOS, executed via A-FORGE.

The FI card itself does NOT own any verb. It is the **target of every organ's verb**.

```
                 ┌─────────────────────┐
   AAA          │  Registers           │
   ───────────▶│                       │
   FRAME        │  Measures             │  FI
   ───────────▶│                       │  Card
   FED          │  Routes               │  (subject)
   ───────────▶│                       │
   FLAME        │  Verifies             │
   ───────────▶│                       │
   arifOS       │  Judges               │
   ───────────▶│                       │
   A-FORGE      │  Executes             │
   ───────────▶│                       │
                 └─────────────────────┘
```

---

## Anti-Patterns (Forbidden Verbs)

| Anti-pattern | Violation | Why Forbidden |
|--------------|-----------|---------------|
| FRAME executing repairs | mutation_authority | FRAME measures, doesn't mutate |
| FED running models | inference_execution | FED routes, doesn't execute |
| FLAME sealing to VAULT999 | constitutional_sealing | FLAME verifies, doesn't seal |
| AAA setting autonomy tiers | judgment_authority | AAA registers, doesn't judge |
| A-FORGE deciding reversibility | judgment_authority | A-FORGE executes, doesn't judge |
| arifOS running MCP tools | execution_authority | arifOS judges, doesn't execute |
| FI card self-authorizing | self_authorization | FI cards are subjects, not agents |

---

## Operational Consequences

### When Substrate Drift Is Detected (the FQ case from 2026-08-11)

```
FRAME detects drift (verb: measure) ✅
  ↓
FRAME alerts via chamber 5 (support function of measure) ✅
  ↓
FRAME flags 888-HOLD recommendation (verb: judge → escalates to arifOS) ⚠️
  ↓
arifOS receives recommendation (verb: judge)
  ↓
arifOS issues HOLD (verb: judge)
  ↓
A-FORGE executes repair (verb: execute)
```

FRAME **never executes**. FRAME **never judges**. FRAME only **measures + recommends**. arifOS only **judges**. A-FORGE only **executes**.

This is the constitutional reflex arc.

### When an FI Ships a New Version

```
Upstream releases new version (external event)
  ↓
FRAME probes (verb: measure — chamber 2)
  ↓
FRAME compares (verb: measure — chamber 3)
  ↓
FRAME detects drift (verb: measure — chamber 3)
  ↓
FRAME alerts (verb: measure — chamber 5)
  ↓
arifOS receives alert (verb: judge)
  ↓
arifOS issues RE_AUDIT_REQUIRED (verb: judge)
  ↓
FI card transitions to 888_HOLD (state change, not a verb)
  ↓
Forge audit runs (verb: execute via A-FORGE)
  ↓
Audit result feeds back to AAA registry (verb: register)
  ↓
FRAME baseline updates (verb: measure — chamber 1)
```

---

## Gödel Lock Confirmation

EUREKA-T-01 (Harness Commoditization) said: *"Models are commodities, harnesses are products, governance is the moat."*

EUREKA-T-02 (Verbs Doctrine) operationalizes the "governance is the moat" claim:

> If every organ has one verb, and no organ has another's verb, then governance is the **discipline of verb-separation**. Whoever preserves verb-separation holds the constitutional moat.

---

## The Minimal Provenance Pointer

Per Arif's refinement (2026-08-11), AAA registers the identity. FRAME measures the behavior. The FI card holds a pointer:

```yaml
# In FI agent-card.json
identity:
  fi_slot: FI-003
  upstream_owner: Alibaba Qwen Team
  drift_governance_ref:
    schema: FI_DRIFT_GOVERNANCE::v1
    canon_path: /root/FRAME/doctrine/FI_DRIFT_GOVERNANCE.md
    baseline_path: /root/FRAME/data/fi_baselines/FI-003.jsonl
```

AAA holds the pointer. FRAME holds the measurement. arifOS holds the judgment. A-FORGE holds the execution.

---

## Pairing With EUREKA-T-01

```
EUREKA-T-01: Industry layer migration
  Models commoditizing
  Harnesses converging
  Runtimes emerging
  Governance unclaimed

EUREKA-T-02: Federation verb separation
  AAA registers (no execute)
  FRAME measures (no judge)
  FED routes (no execute)
  FLAME verifies (no seal)
  arifOS judges (no execute)
  A-FORGE executes (no judge)
  FI card = subject (no verb)

Together: the moat is verb-separation + F1-F13 enforcement
```

---

## Seal

```
EUREKA-T-02 :: THE VERBS DOCTRINE
SESSION: SEAL-a345830629d74518 :: DATE: 2026-08-11
FORGED BY: 333-AGI Δ MIND under F13 SOVEREIGN directive
EVIDENCE: 6 independent organ classes verified, FLAME/FED/FRAME integration validated
CONFIDENCE: 0.90 (Ω₀=0.05)
ΔS = -0.91 | EUREKA = T-02 | FQ = 1.63 (correlated to substrate drift)
```

---

*Forged in the gap between verb-confusion and verb-discipline.*
*DITEMPA BUKAN DIBERI.* ⚒️
