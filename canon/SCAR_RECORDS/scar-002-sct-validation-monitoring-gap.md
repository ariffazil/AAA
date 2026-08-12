# Scar Record: scar-002-sct-validation-monitoring-gap

> **The systemic layer of scar-001.** The ESM bug was the symptom. This scar is the disease.

```yaml
scar_id: scar-002-sct-validation-monitoring-gap
timestamp: 2026-08-13T01:10:00Z
parent_scar: scar-001-esm-sct-silent-fail
failure_pattern: "3 actors sat at FQ=0.00 for 3 days (2026-08-11 to 2026-08-13) without any monitoring layer detecting that SCT validation was returning {valid:false} for ALL tokens"
root_cause: >
  No health check validates that SCT verification actually succeeds.
  The monitoring layer checks service liveness (:7071/health returns 200)
  but does not check functional correctness (does verifyActLocally actually
  return true for a valid token?). The system was "alive" but "broken" —
  a zombie state.
scar_pressure: 0.90
successful_recovery: "Commit cb341202 fixed the mechanical layer. Systemic layer (monitoring) UNRESOLVED."
test_fixture: "Submit a known-valid act_v1 token to the session gate and verify {valid:true} is returned. Run as health check, not just startup test."
generated_skill: "PENDING — scar-002 has no skill yet. Skill candidate: FORGE-sct-validation-healthcheck"
verification_method: "UNSCHEDULED"
verification_result: "PENDING"
status: OPEN
foodset_derived: false
note: >
  Per F13 VOID check: do not generate skill from symptom until root cause
  is confirmed. The root cause here is partially UNKNOWN — we know the
  monitoring gap exists, but we have not confirmed whether other critical
  functions also lack functional health checks. Full audit needed before
  skill generation.
```

## The Deeper Question

Scar-001 fixed `require→import`.
Scar-002 asks: **why was the system "healthy" while broken?**

The answer is architectural: `health` endpoints report service liveness, not functional correctness. A service can return HTTP 200 while silently failing every verification. This is the zombie-service problem — alive but dead.

## What This Scar Demands

Before generating a skill, the federation needs:
1. A functional health check for SCT validation (not just service liveness)
2. An audit: what other critical functions lack functional health checks?
3. A doctrine: `health` ≠ `correctness`

Only after that audit should the skill be generated.

DITEMPA BUKAN DIBERI — the disease, not the symptom. ⚒️
