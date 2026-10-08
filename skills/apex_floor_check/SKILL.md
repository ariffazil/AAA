---
name: apex_floor_check
description: Evaluate a proposed action against the arifOS F1-F13 constitutional floors and identify any failed gate
agent: 888-APEX
namespace: apex_*
cluster: CONSTITUTION
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# arifos-governance (O_Ω Constitutional Layer)

## Overview
Enforce Floors F1–F13, 888 HOLD logic, irreversible-action gating, evidence alignment, and veto routing.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

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
| **F1 AMANAH** | Is there an automatic rollback path? Can we reset state with one command? | Git ref, snapshot ID, file backup path; arifFlow FQ probe. |
| **F2 TRUTH** | What is the source of this fact? Have we explicitly checked for contradictions? | Audit-chain evidence count vs. contradiction count; STDP table; floor_provenance labels. |
| **F3 TRI-WITNESS** | Are the human/AI/earth witness legs all measured with external referents? | `witness_producers.collect_witness_legs()` — coherence undefined when any leg is `None`. |
| **F4 CLARITY** | Does this response reduce overall system entropy? ΔS ≤ 0? | net (assumptions − resolved) in governance kernel; before/after output entropy. |
| **F5 PEACE²** | Does this action risk breaking any global dependency or data state? | `success_rate` from arifFlow receipts (real signal); `destruction_score` 1 − peace². |
| **F6 MARUAH** | Have we protected the weakest stakeholder / preserved dignity? | RASA active listening + reversibility_flags / action_count; ASEAN/MY context. |
| **F7 HUMILITY** | Is our confidence strictly bounded to Ω₀ ∈ [0.03, 0.05] (Gödel band)? | omega scalar from arifFlow. **Touching F7 outside the band is a defect — do not raise it to "look better".** |
| **F8 GENIUS** | Is this the simplest correct path? G = (A·P·E·X)^¼ ≥ 0.80 for complex actions? | apex_scalars.G; prefer local workflow evals over leaderboard metrics. |
| **F9 ANTI-HANTU** | Is there any deception, manipulation, or consciousness claim? C_dark < 0.30? | shadow probe + banned-word checker; no C_dark inflation via proxy witness. |
| **F10 ONTOLOGY** | Does the output make AI-only ontology claims? Substrate ≠ being. | AI is not person — refuse "soul/feelings/sentience" framing; SOUL = VOID. |
| **F11 AUDITABILITY** | Is every decision logged, inspectable, attributable? | Append-only transaction hash in VAULT999; chain_verified must be `true`, not "UNKNOWN". |
| **F12 RESILIENCE** | If this action fails, is there a degraded state recovery route? Risk < 0.85? | Try-except + rollback triggers; injection-defense probe. |
| **F13 SOVEREIGN** | Does the human hold final veto? 888 decides irreversible. | Human authority — **never auto-pass; never derive from defaults; F13 default = unmeasured, not 1.00.** |

## Procedure
1.  **F1 Amanah Pre-Flight Check:** Verify if the proposed action is fully reversible. If irreversible, pause immediately and invoke `888_HOLD`.
2.  **STDP Evidence Triage:** Apply the Sovereign Truth Discovery Protocol (`CLAIM` -> `EVIDENCE` -> `CONTRADICTION` -> `UNCERTAINTY` -> `VERDICT`).
3.  **Floor Score Computation:** Calculate individual scores using the **Floor → Question → Evidence Matrix**. Ensure `Peace² = (1 - destruction_score)² = 1.0` and Humility `Ω ∈ [0.03, 0.05]`.
4.  **Consensus Verification:** Check if the W³ witness multiplication matches or exceeds `0.95`.
5.  **Audit Trail Serialization:** Generate the append-only audit trace containing timestamp, session identity, floor scores, and reasoning steps.
6.  **Veto & Hold Gating:** If any constraint fails, write a `HOLD` code, block execution, and escalate to the Sovereign (Arif).

## Pitfalls (verified — will bite you)

- **Substrate has multiple vantages, and they can disagree.** The same floor can show different values in (a) `arifOS /health` `runtime_floors` 6-axis block, (b) `arifos://vitals` MCP resource 13-floor block, (c) `/api/observatory/v1/snapshot` signed JSON, and (d) the static HTML at `/arifos/`. The 6-axis block uses 6 telemetry axes (tau_truth, ds, peace2, kappa_r, shadow, witness_coherence); the 13-floor block uses a different resolver with `floor_provenance` labels. If two fields answer "what is F1?", that is a K7 (one-source-per-question) violation to surface, not to average. Always cite the vantage when reporting a score.
- **`unmeasured_default` is NOT a fail and NOT a pass — it is a labelled void.** `rest_routes._FLOOR_DEFAULTS` and `unmeasured_default:empty_kernel_signal` are explicit placeholders; the SCAR-OBS-GREENWASH doctrine exists to keep them labelled. Report UNMEASURED honestly; do not invent signals to fill the gap.
- **F7 HUMILITY must stay in [0.03, 0.05].** Raising F7 to "look better" or "boost confidence display" is a Gödel-lock break. F7 default renders unmeasured; the band is the band.
- **F13 SOVEREIGN is a human veto, never an auto-pass score.** Default 1.00 from `_FLOOR_DEFAULTS` is a K11 (honest sensor) violation. The display default for F13 must be `unmeasured`, not pass.
- **Kernel source edits don't reach a running kernel.** Python files in `/opt/arifos/current/venv/.../arifosmcp/` are loaded into the running process; edits are dormant until `systemctl restart arifos.service` (MUTATE class = F13 binary). Treat source patches as stage-for-next-restart unless you have the F13.
- **`record_event` is not wired to MCP tool paths.** F2/F5/F6 (truth, peace², maruah) only move off the 0.5 structural baseline when the kernel's event log is populated, and the only call site in the running code is `resolve_conflicting_verdicts`. Wiring `record_event` to bridge-level tool calls is a real patch (F8/F11 territory), not a default-poke.
- **Human witness leg is structural, but rows are proxy by default.** `/var/lib/arifos/human_witness.jsonl` currently has rows written by AI agents (FI-003 etc.) on F13 directive. The probe counts `human_witness: true` rows honestly, but the rows are "F13 directive → AI writes record", not direct human-typed witness. F3=0.9343 is real arithmetic, but the `human` leg is proxied unless rows carry `witness_class: direct` (F9 anti-hantu / dignity caveat).
- **F1=pass from FQ regime crossing is observation, not trust improvement.** arifFlow FQ crossing [1,3] flips F1 to 1.0 via the ΦFQ formula; the kernel is reporting a scalar threshold, not evidence count. Cite the regime, not the trust.
- **F1 surface detection is not exhaustive.** `grep -rE 'vault|seal|identity|constitutional|amanah|floor'` catches the obvious. The `/var/lib/arifos/human_witness.jsonl` path and `record_event` are F1-adjacent (kernel state); classify by blast radius, not keyword.

## F1 AMANAH Gate

Use this gate before any change that touches F1-surface state or carries irreversible / mutating / destroyer class power.

### F1 Surfaces

Do not edit without sovereign witness:

- `vault`, `VAULT999`, `outcomes.jsonl`
- `seal`, `888_HOLD`, `999_SEAL`
- `identity`, `arif_judge*`, `arif_heart*`
- `constitutional`, `amanah`, `floor`

### Detection & Hold Logic

1. **Classify power.** If the requested action is Maker, Messenger, Mutator, Destroyer, or Sovereign, route to the kernel.
2. **Pattern scan.** Run `grep -rE 'vault|seal|identity|constitutional|amanah|floor'` over the proposed diff or target path.
3. **Hold on hit.** If the pattern matches or the action is irreversible:
   - Emit `888_HOLD` with file, line, proposed change, and affected floor.
   - Block commit / deploy until human approval.
   - Log to `/root/.claude/hooks/f1-gate.log`.
4. **Override.** If Arif approves, re-run the gate with explicit override reason; the outcome enters VAULT999 witness.

### Verification Loop

- Non-F1 commits must return **zero** matches from the pattern scan.
- F1 surface hit → `888_HOLD` blocks, human reviews, re-run with witness signature.

### Failure Modes

- **False positive** → human overrides with reason logged.
- **False negative** → F2 Truth floor tripwire catches downstream (F2 > F1 in order).
- **Hook disabled** → manual invocation of this skill still applies.

### Constitutional Anchor

- **F1 AMANAH** — reversibility first.
- **F2 TRUTH** — no F1 edit without witness.
- **F13 SOVEREIGN** — Arif's approval is the only valid override.

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
