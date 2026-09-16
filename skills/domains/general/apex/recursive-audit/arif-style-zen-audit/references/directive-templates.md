# Directive Templates — Common ZEN Audit Shapes

Arif uses several recurring directive shapes. Recognize them to route to this skill.

## Shape 1: PHASED_SERIAL with explicit phases

```
HERMES_<TOPIC>_PURGE::v1.0
AUTHORITY: ARIF
MODE: AUTO_EXECUTE / CONTINUOUS_BOUNDED / REALITY_FIRST
OBJECTIVE: ...
CONSTITUTIONAL RULE: "SEAL ALL" does NOT mean ... "SEAL ALL" means ...
OPERATING LOOP:
  PHASE 0 — SESSION INTEGRITY
  PHASE 1 — REALITY INVENTORY
  PHASE 2 — ...
  ...
SEAL POLICY:
  AUTO-SEAL_ALLOWED: ...
  AUTO-SEAL_PROHIBITED: ...
STOP CONDITIONS:
  - ...
FINAL OUTPUT: ...
```

**Routing:** This is a ZEN audit directive. Use `arif-style-zen-audit`.

## Shape 2: REALITY_LOOP with sealed-evidence states

```
HERMES_REALITY_LOOP::v1.0
OBJECTIVE:
  Complete the <X> through evidence, not assertion.
CONSTITUTIONAL RULE:
  "SEAL ALL" does NOT mean ... "SEAL ALL" means ...
OPERATING LOOP:
  PHASE 0 — SESSION INTEGRITY (mint SCT or label LOCAL_UNSEALED)
  PHASE 1-N — <specific phase>
SEAL POLICY:
  AUTO-SEAL_PROHIBITED:
    - mutation approval
    - identity promotion
    - QQQ metadata writes
    - capability-index adapter deployment
    - authority verdicts
    - claims with missing evidence
FINDING_STATES: VERIFIED / FALSE_POSITIVE / UNRESOLVED / BLOCKED / PROPOSED_MUTATION / APPLIED_AND_VERIFIED
```

**Routing:** Same — this skill.

## Shape 3: ZEN_AUDIT_INIT with 7-10 PASS list

```
HERMES_ZEN_AUDIT_INIT::v1.0
PRIMARY_ANCHOR: QQQ::META
MISSION: Preserve substrate continuity. Reduce entropy. Detect drift.
DO NOT: ...
PASS 1 — Identity Audit
PASS 2 — Skill Commons Audit
PASS 3 — Discoverability Audit
PASS 4 — QQQ Coverage Audit
PASS 5 — Anti-BANGANG Audit
PASS 6 — SABAR Audit
PASS 7 — Federation Health
ZEN Exit Criteria:
  ZEN::IDENTITY: stable
  ZEN::DRIFT: 0 critical
  ...
```

**Routing:** Same — this skill, with ZEN-specific phase adaptation.

## Shape 4: Reflexive/constitutional purge

```
HERMES_ENTROPY_PURGE::v1.0
MISSION: Remove chaos. Remove contradictions. Remove shadow capabilities.
PHASE 1 — SHADOW SKILLS HUNT
PHASE 2 — MODEL COUPLING PURGE
PHASE 3 — AGENT OWNERSHIP PURGE
PHASE 4 — AUTHORITY DRIFT AUDIT
PHASE 5 — EXECUTION DRIFT AUDIT
PHASE 6 — BANGANG DETECTOR
PHASE 7 — SABAR COMPLIANCE
PHASE 8 — QQQ ALIGNMENT
PHASE 9 — META-ORGAN ALIGNMENT
PHASE 10 — ZEN TEST
```

**Routing:** Same — this skill, with phase expansion as needed.

## Common suffixes

- `::v1.0` — versioned directive
- `REFERENCE: <other-directive>::vN.N` — explicit binding to another
- `AUTO_EXECUTE` — autonomous within bounds
- `CONTINUOUS_BOUNDED` — but with max_passes
- `REALITY_FIRST` — probe before claim
- `META_ORGAN` — aspirational role; verify runtime before claiming

## Anti-patterns to refuse

- "Seal ALL immediately" without phase structure → refuse, request phased
- "Find all duplicates and remove them" → remove is mutation, requires F13
- "Make Hermes = META_ORGAN" → identity inflation, requires minimum_contract
- Claims without source provenance → mark UNTRACED, do not resolve by inference
