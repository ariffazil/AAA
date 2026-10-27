---
title: "What a Receipt Proves"
description: "Disambiguation of receipt semantics across command success, governance verdicts, execution results, world outcomes, and human acceptance."
type: concept
tags: [receipts, semantics, verification, evidence]
confidence: high
---

# What a Receipt Proves

> **The Law of Receipts:** A receipt proves only what its evidence field can independently support.

In complex autonomous systems, there is a dangerous tendency to collapse multiple distinct layers of reality into a single boolean `status: success`. arifOS formally separates five distinct levels of verification.

---

## 1. The Five Levels of Reality

```text
[ Level 1: Command Success ]      Did the process exit with code 0?
             ↓
[ Level 2: Governance Verdict ]    Did internal rules/floors pass?
             ↓
[ Level 3: Execution Result ]      Were the bytes actually written to disk?
             ↓
[ Level 4: World Outcome ]         Did the state of the physical world change?
             ↓
[ Level 5: Human Acceptance ]      Did the affected humans agree to the consequence?
```

### 1. `COMMAND_SUCCESS`
- **Definition:** A script, tool, or API request returned without crashing (e.g., HTTP 200, shell exit code 0).
- **What it proves:** The execution syntax was valid and the host completed the routine.
- **What it does NOT prove:** It does not prove the logic was sound, the file was populated, or external reality matches the output.

### 2. `GOVERNANCE_VERDICT`
- **Definition:** An internal evaluator (such as `888_JUDGE` or `F1–F13` floor producer) verified that declared constraints were satisfied and issued a `SEAL` or `PASS`.
- **What it proves:** The proposed action conformed to the system's internal rules.
- **What it does NOT prove:** It does not verify external truth, factual accuracy of claims, or absence of unforeseen consequences.

### 3. `EXECUTION_RESULT`
- **Definition:** Measurable, durable mutation on local physical media (e.g., non-zero file written, database row inserted, container deployed).
- **What it proves:** State delta occurred on the host machine.
- **What it does NOT prove:** It does not prove the mutation achieved its intended external purpose.

### 4. `WORLD_OUTCOME`
- **Definition:** The observed state of external reality independently confirmed by external sensors or independent witnesses.
- **What it proves:** The external environment responded as intended.
- **What it does NOT prove:** It does not prove human consequence-bearers are satisfied with that outcome.

### 5. `HUMAN_ACCEPTANCE`
- **Definition:** Affirmative, uncoerced consent and acceptance by the human beings who bear the material burden of the decision.
- **What it proves:** Legitimate human agreement.
- **What it does NOT prove:** It does not prove the system is infallible or that all future consequences are known.

---

## 2. Why One Boolean Cannot Represent All Five

A command can succeed (Level 1) while writing a 0-byte file (Level 3 failure).  
An internal governance rule can issue a SEAL (Level 2) while external database replication is 64 days stale (Level 4 failure).  
A system can achieve a world outcome (Level 4) while causing severe harm to an unconsenting human (Level 5 failure).

Treating `SEAL` as equivalent to `VERIFIED` or `ACCEPTED` is an epistemic category error. 

---

## 3. Receipt Semantics Standard

Every verifiable public record on arifOS must explicitly separate these dimensions:

| Field | Allowed States | Meaning |
|---|---|---|
| `claim_status` | `CLAIM_RECORDED`, `UNCHECKED`, `REFUTED` | The epistemic status of the statement itself. |
| `event_status` | `SEALED`, `HELD`, `REJECTED` | The internal governance determination. |
| `verification_status` | `VERIFIED`, `NOT_VERIFIED`, `GAPS_DETECTED`, `UNKNOWN` | Independent confirmation against reality. |
| `execution_status` | `SUCCESS`, `PARTIAL`, `FAILED` | Physical mutation on media. |
| `world_outcome` | `OBSERVED`, `UNCONFIRMED`, `UNKNOWN` | Real-world state delta. |
| `human_acceptance` | `ACCEPTED`, `REFUSED`, `PENDING_DEMONSTRATION` | Human consequence-bearer standing. |

Missing measurements must always be rendered as `UNKNOWN` or `NOT_MEASURED`, never as numerical zero (`0`, `0.0`) or boolean `false`.
