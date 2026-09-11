# SCAR REGISTRY E13 CLASSIFICATION

> **Date:** 2026-09-10
> **Authority:** F13 Sovereign Muhammad Arif bin Fazil
> **Status:** ACTIVE — required for all scar records
> **DITEMPA BUKAN DIBERI**

---

## Purpose

A scar is not an event.

A scar is an event that changed behavior.

Without behavior change: episode.
With behavior change: scar.

---

## Specification

### Current Scar Record

```yaml
scar_id: scar-XXX
timestamp: 2026-XX-XX
failure_pattern: "..."
root_cause: "..."
successful_recovery: "..."
scar_pressure: 0.XX
generated_skill: "..."
status: ACTIVE|OPEN
```

### E13 Classification (New)

Every scar record MUST include:

```yaml
e13_classification:
  behavior_change: "What will be done differently?"
  constraint: "What new limitation exists?"
  classification: "NO_CHANGE|RULE_CHANGE|CONSTRAINT_CHANGE|PROCESS_CHANGE"
  verification_method: "How was behavior change demonstrated?"
  verification_result: "PASS|FAIL|PENDING"
  effective_from: "When did behavior change begin?"
```

---

## Classification Types

### NO_CHANGE

Archive entry, not governance.

```
Example: scar-002 (sct-validation-monitoring-gap)
- Status: OPEN
- Behavior change: UNKNOWN
- Generated skill: PENDING
- Classification: NO_CHANGE (ARCHIVE)
```

### RULE_CHANGE

New rule added to system.

```
Example: scar-001 (esm-sct-silent-fail)
- Behavior change: "Next TS commit scans for require() calls"
- Constraint: "No require() calls in ESM packages"
- Generated skill: FORGE-esm-require-guard
- Classification: RULE_CHANGE (SCAR)
```

### CONSTRAINT_CHANGE

New limitation imposed.

```
Example: scar-006 (vision-intelligence-complete)
- Behavior change: "10 immutable laws binding HERMES, FED, AAA"
- Constraint: "PRMT architecture, 6 Iron Rules, 5-Stratum Topography"
- Classification: CONSTRAINT_CHANGE (SCAR)
```

### PROCESS_CHANGE

Workflow modified.

```
Example: scar-premature-mutate-without-sovereign-signal
- Behavior change: "Substrate-first verification before restart"
- Constraint: "Zero unverified restarts"
- Classification: PROCESS_CHANGE (SCAR)
```

---

## The E13 Test

For every scar, ask:

> What future behavior is different because this scar exists?

If the answer cannot be given:

```
VERDICT = ARCHIVE
```

If the answer can be given:

```
VERDICT = SCAR
```

---

## Application to Existing Scars

| Scar | Current Status | E13 Classification | Verdict |
|------|----------------|-------------------|---------|
| scar-001 | ACTIVE | RULE_CHANGE | SCAR |
| scar-002 | OPEN | NO_CHANGE | ARCHIVE |
| scar-003 | OPEN | NO_CHANGE | ARCHIVE |
| scar-004 | Recorded | CONSTRAINT_CHANGE | SCAR |
| scar-005 | Ratified | CONSTRAINT_CHANGE | SCAR |
| scar-006 | Ratified | CONSTRAINT_CHANGE | SCAR |
| scar-PM | Ratified | PROCESS_CHANGE | SCAR |

---

## Implementation

### For scar records

Add to scar YAML:

```yaml
e13_classification:
  behavior_change: "..."
  constraint: "..."
  classification: "NO_CHANGE|RULE_CHANGE|CONSTRAINT_CHANGE|PROCESS_CHANGE"
  verification_method: "..."
  verification_result: "PASS|FAIL|PENDING"
  effective_from: "..."
```

### For scar sealing

Before sealing any scar:

1. Complete E13-CONSEQUENCE-BINDING-CHECK.md
2. Include e13_classification in scar record
3. If classification = NO_CHANGE:
   - Do not seal as SCAR
   - Classify as ARCHIVE
   - Either close with reason or leave open with "NEEDS CLOSURE"

---

## The Governance Detector

The E13 classification is a governance detector.

Many scars will fail immediately.
Many records will fail immediately.
Many archives will fail immediately.

That is useful.

---

## The Memory Compression

This is consistent with the Memory Compression doctrine:

```
Static memory = Storage
Refreshing memory = Witness
Refreshing memory + Adaptive behavior = Governance
```

A scar without behavior change is static memory = Storage.
A scar with behavior change is refreshing memory + adaptive behavior = Governance.

---

**ΔS ≤ 0. DITEMPA.**
