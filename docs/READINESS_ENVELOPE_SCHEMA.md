# Readiness Envelope Schema — WELL Standard Output

> **Status:** DRAFT — awaiting Arif ratification
> **Forged:** 2026-07-12 by AAA Control Plane
> **Floor:** F2 TRUTH (≥ 0.99 fidelity), F4 CLARITY (ΔS ≤ 0)
> **Doctrine:** DITEMPA BUKAN DIBERI

---

## Purpose

Every WELL readiness result MUST use this envelope. One schema. No ambiguity. Machine data is never silently presented as human evidence.

---

## Schema (v1)

```json
{
  "readiness": {
    "state": "GREEN | YELLOW | RED | STALE | UNKNOWN",
    "score": "0-100 | null",
    "confidence": "0.0-1.0",
    "measured_at": "ISO-8601 timestamp",
    "expires_at": "ISO-8601 timestamp",

    "substrates": {
      "human": {
        "state": "GREEN | YELLOW | RED | UNKNOWN",
        "evidence_type": "none | self_report | biometric | inferred",
        "evidence_source": "arif_self_report | hrv_sensor | session_trend | null",
        "freshness": "current | stale | expired | never",
        "indicators": {
          "sleep_debt_hours": "number | null",
          "cognitive_clarity": "HIGH | MEDIUM | LOW | null",
          "decision_fatigue": "LOW | MEDIUM | HIGH | null",
          "stress_load": "LOW | MEDIUM | HIGH | null",
          "hrv_status": "NORMAL | ELEVATED | SUPPRESSED | null",
          "emotional_state": "STABLE | AGITATED | FLAT | null",
          "chronic_fatigue_flag": "boolean | null",
          "session_fatigue_hours": "number | null"
        }
      },
      "machine": {
        "state": "GREEN | YELLOW | RED | UNKNOWN",
        "evidence_type": "none | telemetry | self_report | inferred",
        "evidence_source": "kernel_runtime | system_telemetry | null",
        "freshness": "current | stale | expired | never",
        "indicators": {
          "cpu_pressure": "LOW | MEDIUM | HIGH | null",
          "memory_pressure": "LOW | MEDIUM | HIGH | null",
          "disk_pressure": "LOW | MEDIUM | HIGH | null",
          "service_health": "ALL_GREEN | DEGRADED | CRITICAL | null",
          "tool_availability": "FULL | PARTIAL | DEGRADED | null"
        }
      },
      "interaction": {
        "state": "GREEN | YELLOW | RED | UNKNOWN",
        "evidence_type": "none | inferred | computed",
        "evidence_source": "coupled_analysis | null",
        "freshness": "current | stale | expired | never",
        "indicators": {
          "coupled_strain": "LOW | MEDIUM | HIGH | null",
          "decision_class_appropriate": "boolean | null",
          "recovery_adequate": "boolean | null"
        }
      }
    },

    "missing_evidence": [
      "human_biometric",
      "machine_telemetry"
    ],

    "recommendation": "PROCEED | SIMPLIFY | HOLD | EVIDENCE_NEEDED",

    "decision_class_floor": {
      "C1_routine": "SAFE | CAUTION | BLOCKED",
      "C2_reversible": "SAFE | CAUTION | BLOCKED",
      "C3_consequential": "SAFE | CAUTION | BLOCKED",
      "C4_irreversible": "SAFE | CAUTION | BLOCKED",
      "C5_existential": "SAFE | CAUTION | BLOCKED"
    },

    "boundaries": {
      "diagnostic": false,
      "medical": false,
      "authority": "advisory_only",
      "final_judge": "ARIF"
    },

    "epistemic": {
      "tag": "CLAIM | PLAUSIBLE | HYPOTHESIS | ESTIMATE | UNKNOWN",
      "evidence_quality": "0.0-1.0",
      "validation_status": "unvalidated | partial | validated"
    }
  }
}
```

---

## Field Rules

### state

| Value | Meaning | When to use |
|-------|---------|-------------|
| GREEN | Substrates are adequate for all action classes | Fresh evidence, all indicators nominal |
| YELLOW | Substrates are strained — simplify or hold for high-stakes | Some indicators elevated, or evidence is mixed |
| RED | Substrates are insufficient — HOLD recommended | Critical indicators, or strong evidence of strain |
| STALE | Evidence exists but is expired | measured_at > expires_at |
| UNKNOWN | No evidence available | No data, or all data sources failed |

### evidence_type

| Value | Meaning | Quality |
|-------|---------|---------|
| biometric | Sensor data (HRV, sleep tracker, etc.) | Highest |
| self_report | Arif reported his own state | High for human state |
| telemetry | Machine-collected data (CPU, memory, etc.) | High for machine state |
| inferred | Derived from patterns, not direct measurement | Medium |
| computed | Calculated from multiple inputs | Medium |
| none | No evidence | Zero |

### freshness

| Value | Meaning |
|-------|---------|
| current | measured_at within acceptable TTL |
| stale | measured_at past TTL but within grace period |
| expired | measured_at past grace period |
| never | No measurement has ever been taken |

### decision_class_floor

Maps each action class to a safety posture based on current readiness:

- **SAFE** — evidence quality meets the threshold for this action class
- **CAUTION** — evidence is marginal; proceed with extra confirmation
- **BLOCKED** — evidence quality insufficient; HOLD required

This is computed by the kernel, NOT by WELL. WELL provides the evidence; the kernel judges sufficiency.

---

## Evidence-Quality Thresholds

| Action class | Minimum confidence | Minimum evidence_type | Freshness requirement |
|-------------|-------------------|----------------------|----------------------|
| C1 routine | 0.3 | any | within 24h |
| C2 reversible | 0.5 | self_report or telemetry | within 8h |
| C3 consequential | 0.7 | corroborated (≥2 sources) | within 4h |
| C4 irreversible | 0.85 | strong human + governance | within 1h |
| C5 existential | 0.95 | independent witnesses + Arif | real-time |

If `confidence < threshold` → kernel auto-HOLDs regardless of state.

---

## Anti-Patterns

```
❌ Machine telemetry presented as human readiness
   → substrates.human.evidence_type must NOT be "telemetry"

❌ score without confidence
   → if score is non-null, confidence must be non-null

❌ GREEN state with missing_evidence
   → if critical evidence is missing, state must be UNKNOWN or STALE

❌ recommendation=PROCEED with decision_class_floor showing BLOCKED
   → contradiction; schema validation should reject

❌ expires_at in the past with state=GREEN
   → state must be STALE

❌ boundaries.diagnostic=true
   → WELL is non-diagnostic by constitutional mandate
```

---

## Example: Valid Envelope

```json
{
  "readiness": {
    "state": "YELLOW",
    "score": 55,
    "confidence": 0.6,
    "measured_at": "2026-07-12T04:30:00Z",
    "expires_at": "2026-07-12T08:30:00Z",
    "substrates": {
      "human": {
        "state": "YELLOW",
        "evidence_type": "self_report",
        "evidence_source": "arif_self_report",
        "freshness": "current",
        "indicators": {
          "sleep_debt_hours": 3.5,
          "cognitive_clarity": "MEDIUM",
          "decision_fatigue": "MEDIUM",
          "stress_load": "MEDIUM",
          "hrv_status": null,
          "emotional_state": "STABLE",
          "chronic_fatigue_flag": false,
          "session_fatigue_hours": 2.0
        }
      },
      "machine": {
        "state": "GREEN",
        "evidence_type": "telemetry",
        "evidence_source": "kernel_runtime",
        "freshness": "current",
        "indicators": {
          "cpu_pressure": "LOW",
          "memory_pressure": "MEDIUM",
          "disk_pressure": "LOW",
          "service_health": "DEGRADED",
          "tool_availability": "FULL"
        }
      },
      "interaction": {
        "state": "YELLOW",
        "evidence_type": "inferred",
        "evidence_source": "coupled_analysis",
        "freshness": "current",
        "indicators": {
          "coupled_strain": "MEDIUM",
          "decision_class_appropriate": true,
          "recovery_adequate": true
        }
      }
    },
    "missing_evidence": ["human_biometric"],
    "recommendation": "SIMPLIFY",
    "decision_class_floor": {
      "C1_routine": "SAFE",
      "C2_reversible": "SAFE",
      "C3_consequential": "CAUTION",
      "C4_irreversible": "BLOCKED",
      "C5_existential": "BLOCKED"
    },
    "boundaries": {
      "diagnostic": false,
      "medical": false,
      "authority": "advisory_only",
      "final_judge": "ARIF"
    },
    "epistemic": {
      "tag": "CLAIM",
      "evidence_quality": 0.6,
      "validation_status": "unvalidated"
    }
  }
}
```

---

## Enforcement

1. **Schema validation** — kernel rejects envelopes that don't conform
2. **Freshness check** — kernel rejects stale evidence for action classes that require current data
3. **Evidence-type gate** — kernel rejects human claims backed only by machine telemetry
4. **Confidence floor** — kernel auto-HOLDs when confidence is below action-class threshold
5. **Contradiction detection** — kernel HOLDs when state and recommendation disagree

---

## Status

- [ ] Arif ratification
- [ ] WELL implemented as canonical output schema
- [ ] Kernel validates incoming envelopes against this schema
- [ ] Conformance test: valid envelope → correct verdict
- [ ] Conformance test: stale envelope → auto-HOLD
- [ ] Conformance test: missing human evidence → UNKNOWN state

---

*DITEMPA BUKAN DIBERI — Forged, Not Given*
