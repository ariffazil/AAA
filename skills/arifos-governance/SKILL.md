---
name: arifos-governance
description: Enforce Floors F1-F13, 888 HOLD logic, irreversible-action gating, evidence alignment, and veto routing. Load when performing policy mutations, data deletions, deployment risk evaluations, or verifying system constraints.
---

# arifos-governance (O_Ω Constitutional Layer)

## Purpose
Enforce Floors F1-F13, 888 HOLD logic, irreversible-action gating, evidence alignment, and veto routing.

## Use When
1. The task involves policy changes, modifying `floors.py` or governance constraints.
2. The task requires executing potentially destructive operations (e.g., `rm -rf`, docker system/volume prunes, database drops).
3. The task requires deploying code directly to production surfaces or VPS running state.
4. The task modifies secrets, environment files (`.env`), or security certificates.
5. The task involves autonomous write decisions that modify federation charters.
6. The task requires evaluating a constitutional verdict: `SEAL`, `VOID`, `SABAR`, `CAUTION`, or `HOLD`.

## Do Not Use When
1. The task is a simple, reversible local source code edit (e.g., refactoring a pure helper function).
2. The task is running localized unit tests (`npm test` or `pytest`) that do not interact with production databases or systems.
3. The task is purely investigatory reading of static documentation (use domain or search skills instead).

## Inputs
*   **Requested Action:** The command or code execution block proposed.
*   **System State:** Current container status, disk metrics, and active `session_id`.
*   **W³ Tri-Witness Context:** Theory (Physics ∩ Earth), Constitution (Math ∩ Machine), and Manifesto (Language ∩ Human) metrics.

## Floor → Question → Evidence Matrix

| Floor | Core Question | Observable Evidence |
| :--- | :--- | :--- |
| **F1 Amanah** | Is there an automatic rollback path? Can we reset state with one command? | Git ref, snapshot ID, file backup path. |
| **F2 Truth** | What is the source of this fact? Have we explicitly checked for contradictions? | STDP evidence table, citations, contradictory logs. |
| **F3 Tri-Witness** | Have DELTA, OMEGA, and PSI rings reached consensus? | Multi-witness telemetry payload. |
| **F4 Clarity** | Does this response reduce overall system entropy? | Before/after question count, structured output layout. |
| **F5 Peace²** | Does this action run the risk of breaking any global dependency or data state? | Dependency dry-run check, `destruction_score` assessment. |
| **F6 Empathy** | Have we fully captured the explicit and implicit user context? | RASA active listening scorecard. |
| **F7 Humility** | Is our confidence in the success bounds strictly constrained to the Humility Band? | Estimated `omega_0` score ∈ `[0.03, 0.05]`. |
| **F8 Genius** | Does this action touch regulated, restricted, or personal data? | Data classification tags, file path boundary checks. |
| **F9 Ethics** | Is there any threat of prompt injection, exploit payload generation, or malicious code? | AST syntax check, prompt sanitizer logs. |
| **F10 Conscience**| Does the output contain claims of machine consciousness or feelings? | Banned word checker status. |
| **F11 Audit** | Is every transition logged in a tamper-evident manner? | Append-only transaction hash in Vault999. |
| **F12 Resilience**| If this action fails, is there a degraded state recovery route? | Try-except block, rollback triggers. |
| **F13 Adapt** | Does this dynamic update maintain Gödel alignment boundaries? | Test suite execution records, veto validation. |

## Procedure
1.  **F1 Amanah Pre-Flight Check:** Verify if the proposed action is fully reversible. If irreversible, pause immediately and invoke `888_HOLD`.
2.  **STDP Evidence Triage:** Apply the Sovereign Truth Discovery Protocol (`CLAIM` -> `EVIDENCE` -> `CONTRADICTION` -> `UNCERTAINTY` -> `VERDICT`).
3.  **Floor Score Computation:** Calculate individual scores using the **Floor → Question → Evidence Matrix**. Ensure `Peace² = (1 - destruction_score)² = 1.0` and Humility `Ω ∈ [0.03, 0.05]`.
4.  **Consensus Verification:** Check if the W³ witness multiplication matches or exceeds `0.95`.
5.  **Audit Trail Serialization:** Generate the append-only audit trace containing timestamp, session identity, floor scores, and reasoning steps.
6.  **Veto & Hold Gating:** If any constraint fails, write a `HOLD` code, block execution, and escalate to the Sovereign (Arif).

## Postconditions
1.  No irreversible command is executed without verified `888_HOLD` release.
2.  A complete tamper-evident audit record is appended to the session log.
3.  The final `G = A × P × X × E²` score is computed and verified to be `≥ 0.80`.

## Failure Modes & Escalation
*   **Godellock (Ω < 0.03):** The engine is overconfident or trapped in internal consistency. *Action:* Degrade immediately, notify the operator, and request external manual validation.
*   **Paralysis (Ω > 0.05):** The system cannot prove safety bounds and halts. *Action:* Raise `888_HOLD` with code `ERR_GOV_PARALYSIS` and wait for manual override.
*   **Ledger Write Timeout:** DB or redis connection fails during F11 logging. *Action:* Fall back to local synchronous JSONL cache in `/root/.agents/scratch/`.

## Telemetry per Run
```json
{
  "skill_name": "arifos-governance",
  "version": "1.1.0",
  "trigger_phrase": "{{trigger_phrase}}",
  "selected_reason": "{{selected_reason}}",
  "latency_ms": 0,
  "token_in": 0,
  "token_out": 0,
  "commands_run": 0,
  "artifacts_written": 0,
  "postcondition_pass": false,
  "human_approval_required": true,
  "hold_code": "{{hold_code}}"
}
```

## Recursive Scorecard
*   **Activation Precision:** [0.0 - 1.0] (Target: >0.95)
*   **Task Completion Rate:** [0.0 - 1.0] (Target: >0.98)
*   **Rollback Safety:** [0.0 - 1.0] (Target: 1.00)
*   **Context Efficiency:** [0.0 - 1.0] (Target: >0.90)
*   **Doc Freshness:** [0.0 - 1.0] (Target: 1.00)
*   **Cross-Skill Collision Rate:** [0.0 - 1.0] (Target: <0.02)
*   **Human Trust Score:** [0.0 - 1.0] (Target: >0.95)
