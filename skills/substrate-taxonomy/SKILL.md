---
name: substrate-taxonomy
description: "Diagnose and evaluate arifOS substrate state using the canonical 5-state taxonomy (OUTAGE, DEGRADED, IDLE_RESTING, FAIL_CLOSED, ACTIVE_SEALED)."
version: 1.0.0
owner: AAA
risk_tier: low
autonomy_tier: T1
dependencies:
  skills: [asi-agentic-governance, seal-discipline]
  files: [/root/AAA/governance/SUBSTRATE_TAXONOMY_2026-09-18.md]
floor_scope: [F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13]
---

# 🌐 Substrate Taxonomy — Anti-False-Green State Discipline

> **Canonical Ref:** `/root/AAA/governance/SUBSTRATE_TAXONOMY_2026-09-18.md` (F13 SEAL)  
> **Companions:** `state-transition-discipline.md` · `anti-collapse-doctrine.md` · `seal-discipline.md`  
> **Iron Law:** Single-word verdicts hide entire state machines. Saying "FAIL" for an alive, idling, fail-closed system is an **Epistemic Collapse**.

---

## 1. The Five Canonical Substrate States

Never collapse the substrate into a binary `PASS / FAIL`. Evaluate against these 5 orthogonal states:

| State | Physical Reality | Epistemic / Governance Posture | Operator Action Required |
|---|---|---|---|
| **`OUTAGE`** | Port dead, daemon crashed, process missing. | Unreachable. Floors cannot be evaluated. | **IMMEDIATE:** Page engineer, restart process, repair network. |
| **`DEGRADED`** | Port reachable, but SLO violated (high latency, stale telemetry, tool drift). | Evaluated, but failing non-doctrinal thresholds. | **INVESTIGATE:** Identify lag/drift source, schedule gotong-royong. |
| **`IDLE_RESTING`** | Substrate 100% alive, no active session, no mutation scheduled. | Watchdog awake, floors not under test. Honest rest (*Sabar*). | **NONE:** Normal resting state. Do NOT alarm the human. |
| **`FAIL_CLOSED`** | Substrate 100% alive, but F13 SOVEREIGN or gates F2/F3/F5/F6 hold authority. | Principled restraint. Machine asked, but doctrine says HOLD. | **GOVERNANCE:** Await sovereign ratification (`ARIF GO`). |
| **`ACTIVE_SEALED`** | Substrate 100% alive, active session, all 13 floors attested under `arif_judge`. | Legitimate green. Mutation permitted within authorized envelope. | **OBSERVE:** Follow receipt chain in VAULT999. |

---

## 2. Decision Tree for Future Agents

When analyzing Observatory, telemetry, or system prompts reporting `substrate_state=FAIL`:

```
                    Is port / service reachable via TCP/HTTP?
                                    │
                    ┌───────────────┴───────────────┐
                   NO                               YES
                    │                                │
             ┌──────────────┐          Are all essential daemons healthy?
             │    OUTAGE    │                        │
             └──────────────┘          ┌─────────────┴─────────────┐
                                      NO                          YES
                                       │                           │
                                ┌──────────────┐         Is an active mutating
                                │   DEGRADED   │         session running?
                                └──────────────┘                   │
                                                   ┌───────────────┴───────────────┐
                                                  NO                              YES
                                                   │                               │
                                          ┌──────────────────┐          Did arif_judge attest
                                          │   IDLE_RESTING   │          all 13 floors?
                                          └──────────────────┘                     │
                                                                       ┌───────────┴───────────┐
                                                                      NO                      YES
                                                                       │                       │
                                                               ┌──────────────┐     ┌──────────────────┐
                                                               │ FAIL_CLOSED  │     │  ACTIVE_SEALED   │
                                                               └──────────────┘     └──────────────────┘
```

---

## 3. Epistemic Reporting Rules for Agents

1. **Never Report False Alarm to Arif:**
   If all 8 organs are reachable, all 11 federation edges connected, and cryptographic signatures valid, **never** tell Arif "Sistem rosak / Sistem gagal".
   State clearly:
   > *"Substrat fizikal 100% hidup. Sistem berada dalam keadaan IDLE_RESTING / FAIL_CLOSED mengikut doktrin anti-false-green (menahan autoriti mutasi sehingga ada sesi berdaulat)."*

2. **Decompose into Three Layers:**
   Always report in three separate, non-collapsed layers:
   - **Layer 1: Physical Reality** (ALIVE / OUTAGE)
   - **Layer 2: Capability Reality** (ALIGNED / DEGRADED)
   - **Layer 3: Constitutional Reality** (ACTIVE_SEALED / FAIL_CLOSED / IDLE_RESTING)

3. **Receipt Requirement:**
   Every transition between `FAIL_CLOSED` and `ACTIVE_SEALED` must cite a verifiable trace ID and be anchored in VAULT999.
