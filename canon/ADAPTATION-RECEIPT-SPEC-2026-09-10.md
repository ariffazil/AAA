# ADAPTATION RECEIPT SPECIFICATION

> **Date:** 2026-09-10
> **Authority:** F13 Sovereign Muhammad Arif bin Fazil
> **Status:** ACTIVE — required for all verify receipts
> **DITEMPA BUKAN DIBERI**

---

## Purpose

Current receipts answer: "What happened?"

Adaptation receipts answer: "What will be different now?"

This is the distinction between ARCHIVE and GOVERNANCE.

---

## Specification

### Current Verify Receipt

```
step_type: Verify
epistemic_label: Observation|Derivation|Interpretation|Specification
floor_verdict: Pass|Caution|Hold|Void
```

### Adaptation Receipt (New)

Every verify receipt MUST include these additional fields:

```yaml
adaptation_receipt:
  observation: "What was witnessed?"
  constraint: "What new limitation exists?"
  behavior_change: "What will be done differently?"
  effective_from: "When does behavior change begin?"
  classification: "NO_CHANGE|RULE_CHANGE|CONSTRAINT_CHANGE|PROCESS_CHANGE"
```

---

## Fields

### observation (required)

What was witnessed? This is the reality signal.

```
Example: "a-forge executed 80 times without verify"
Example: "scar-002 has no behavior change demonstrated"
Example: "hermes-asi FQ=0.30, execution dominates verification"
```

### constraint (required)

What new limitation exists? This is the scar.

```
Example: "MAX_EXEC_STREAK = 5 for BURNING actors"
Example: "Every execute must be followed by verify"
Example: "No new execution until verify is called"
```

### behavior_change (required)

What will be done differently? This is the adaptation.

```
Example: "After every forge_execute, call arifflow_flow_ingest(step_type='Verify')"
Example: "Before sealing any scar, complete E13-CONSEQUENCE-BINDING-CHECK.md"
Example: "Reduce hermes-asi execute:verify ratio from 3.3:1 to 1:1"
```

### effective_from (required)

When does behavior change begin? This is the commitment.

```
Example: "2026-09-10T04:30:00+08:00"
Example: "Immediately"
Example: "Next session"
```

### classification (required)

What type of adaptation? This is the scar type.

```
NO_CHANGE — Archive entry, not governance
RULE_CHANGE — New rule added to system
CONSTRAINT_CHANGE — New limitation imposed
PROCESS_CHANGE — Workflow modified
```

---

## Enforcement

### Without adaptation fields:

```
classification = ARCHIVE
```

### With adaptation fields:

```
classification = GOVERNANCE
```

---

## The E13 Connection

This specification enforces the E13 Consequence Binding Test:

> A witness becomes a scar only when reality extracts a cost.

The adaptation receipt is the proof that behavior changed. Without it, the verification is just a record, not a scar.

---

## The Mandatory Question

Every adaptation receipt must answer:

> What future behavior is different because this witness now exists?

If the answer cannot be given:

```
VERDICT = ARCHIVE
```

---

## Implementation

### For arifFlow

Add to FlowReceipt schema:

```typescript
interface AdaptationReceipt {
  observation: string;      // What was witnessed?
  constraint: string;       // What new limitation exists?
  behavior_change: string;  // What will be done differently?
  effective_from: string;   // When does behavior change begin?
  classification: 'NO_CHANGE' | 'RULE_CHANGE' | 'CONSTRAINT_CHANGE' | 'PROCESS_CHANGE';
}
```

### For scar records

Add to scar YAML:

```yaml
adaptation:
  observation: "..."
  constraint: "..."
  behavior_change: "..."
  effective_from: "..."
  classification: "..."
```

---

## The Governance Detector

The adaptation receipt is a governance detector.

Many reports will fail immediately.
Many audits will fail immediately.
Many receipts will fail immediately.

That is useful.

---

**ΔS ≤ 0. DITEMPA.**
