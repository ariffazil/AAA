---
name: apex-gate-evaluator
description: >
  Unified APEX constitutional gate evaluator. Parameterized by gate_type to evaluate proposed actions
  against arifOS F1-F13 floors, scope boundaries, authority claims, reversibility requirements,
  audit coverage, and MCP tool approval routing. Merges: apex_floor_check, apex_scope_check,
  apex_authority_check, apex_reversibility_test, apex_audit_coverage_check, apex_tool_approval_gate.
agent: 888-APEX
namespace: apex_*
cluster: CONSTITUTION
capability_tier: fed-reasoning-heavy
ecology_state: WARM
version: 2.0.0
supersedes:
  - apex_floor_check
  - apex_scope_check
  - apex_authority_check
  - apex_reversibility_test
  - apex_audit_coverage_check
  - apex_tool_approval_gate
triggers:
  - "evaluate floor"
  - "check constitutional floor"
  - "F1-F13 check"
  - "floor check"
  - "scope check"
  - "scope boundary"
  - "authority check"
  - "parallel authority"
  - "source of truth conflict"
  - "reversibility test"
  - "F1 AMANAH gate"
  - "rollback test"
  - "audit coverage"
  - "constitutional audit"
  - "floor enforcement"
  - "tool approval gate"
  - "MCP tool routing"
  - "cross-organ gating"
  - "tool use gate"
---

# APEX Gate Evaluator

> **Parameterized by `gate_type`:** `floor` | `scope` | `authority` | `reversibility` | `coverage` | `tool_approval`
> *DITEMPA BUKAN DIBERI — The constitutional reflex is forged, not assumed.*

## Overview

Unified constitutional gate evaluator for the arifOS federation. Evaluates proposed actions against F1-F13 constitutional floors, scope boundaries, authority claims, reversibility requirements, audit coverage, and MCP tool approval routing. Each `gate_type` activates a specific evaluation procedure while sharing the common arifOS-ACT embedding and constitutional framework.

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
7. Two repos claim to be the "source of truth" for the same thing (authority check).
8. After any repo reorganization or when agents report conflicting instructions (authority check).
9. A proposed change touches vault, seal, identity, constitutional, or other F1 surfaces (reversibility test).
10. Auditing whether every constitutional floor and federation organ has code enforcement, tests, bypass resistance, and trace coverage (coverage check).
11. A complex task spans multiple distinct organ environments and needs MCP tool routing (tool approval gate).
12. Coordinating sequential multi-tool calls across different MCP servers (tool approval gate).

## Do Not Use When

1. The task is a simple, reversible local source code edit (e.g., refactoring a pure helper function).
2. The task is running localized unit tests (`npm test` or `pytest`) that do not interact with production databases or systems.
3. The task is purely investigatory reading of static documentation (use domain or search skills instead).
4. Task is entirely within a single local directory (tool approval gate not needed).

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| gate_type | yes | `floor` \| `scope` \| `authority` \| `reversibility` \| `coverage` \| `tool_approval` |
| requested_action | conditional | The command or code execution block proposed (floor/scope/reversibility) |
| system_state | conditional | Current container status, disk metrics, and active `session_id` |
| w3_context | conditional | W³ Tri-Witness Context: Theory, Constitution, Manifesto metrics |
| intent | conditional | High-level pipeline task (tool_approval) |
| server_registry | conditional | Active MCP endpoints (tool_approval) |
| client_connections | conditional | Active SSE/stdio channels (tool_approval) |
| fallback_policy | optional | "graceful" or "fail-fast" (tool_approval) |

---

## Gate Type: `floor` — Constitutional Floor Evaluation

### Floor → Question → Evidence Matrix

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

### Procedure

1. **F1 Amanah Pre-Flight Check:** Verify if the proposed action is fully reversible. If irreversible, pause immediately and invoke `888_HOLD`.
2. **STDP Evidence Triage:** Apply the Sovereign Truth Discovery Protocol (`CLAIM` -> `EVIDENCE` -> `CONTRADICTION` -> `UNCERTAINTY` -> `VERDICT`).
3. **Floor Score Computation:** Calculate individual scores using the matrix. Ensure `Peace² = (1 - destruction_score)² = 1.0` and Humility `Ω ∈ [0.03, 0.05]`.
4. **Consensus Verification:** Check if the W³ witness multiplication matches or exceeds `0.95`.
5. **Audit Trail Serialization:** Generate the append-only audit trace containing timestamp, session identity, floor scores, and reasoning steps.
6. **Veto & Hold Gating:** If any constraint fails, write a `HOLD` code, block execution, and escalate to the Sovereign (Arif).

### F1 AMANAH Gate

Use this gate before any change that touches F1-surface state or carries irreversible / mutating / destroyer class power.

**F1 Surfaces** (do not edit without sovereign witness):
- `vault`, `VAULT999`, `outcomes.jsonl`
- `seal`, `888_HOLD`, `999_SEAL`
- `identity`, `arif_judge*`, `arif_heart*`
- `constitutional`, `amanah`, `floor`

**Detection & Hold Logic:**
1. **Classify power.** If Maker, Messenger, Mutator, Destroyer, or Sovereign → route to kernel.
2. **Pattern scan.** Run `grep -rE 'vault|seal|identity|constitutional|amanah|floor'` over the proposed diff or target path.
3. **Hold on hit.** If pattern matches or action is irreversible:
   - Emit `888_HOLD` with file, line, proposed change, and affected floor.
   - Block commit / deploy until human approval.
   - Log to `/root/.claude/hooks/f1-gate.log`.
4. **Override.** If Arif approves, re-run with explicit override reason; outcome enters VAULT999 witness.

**Verification Loop:** Non-F1 commits must return **zero** matches. F1 surface hit → `888_HOLD` blocks, human reviews, re-run with witness signature.

**Failure Modes:**
- False positive → human overrides with reason logged.
- False negative → F2 Truth floor tripwire catches downstream.
- Hook disabled → manual invocation still applies.

**Constitutional Anchor:** F1 AMANAH (reversibility first), F2 TRUTH (no F1 edit without witness), F13 SOVEREIGN (Arif's approval is the only valid override).

### Postconditions
1. No irreversible command is executed without verified `888_HOLD` release.
2. A complete tamper-evident audit record is appended to the session log.
3. The final `G = A × P × X × E²` score is computed and verified to be `≥ 0.80`.

### Failure Modes & Escalation
- **Godellock (Ω < 0.03):** Overconfident or trapped in internal consistency. → Degrade immediately, notify operator, request external manual validation.
- **Paralysis (Ω > 0.05):** Cannot prove safety bounds. → Raise `888_HOLD` with code `ERR_GOV_PARALYSIS`, wait for manual override.
- **Ledger Write Timeout:** DB or redis connection fails during F11 logging. → Fall back to local synchronous JSONL cache in `/root/.agents/scratch/`.

---

## Gate Type: `scope` — Scope Boundary Check

Check whether a proposed action stays within its declared task, organ, and constitutional scope.

### Procedure

1. Identify the declared task scope (what was authorized).
2. Identify the proposed action (what is being attempted).
3. Compare: does the action stay within the declared boundaries?
4. Check organ boundaries: is the action appropriate for the organ it targets?
5. Check constitutional scope: does the action respect F1-F13 floors?
6. If scope creep detected → `888_HOLD` with evidence of boundary violation.

---

## Gate Type: `authority` — Parallel Authority Detection

Detect conflicting or parallel source-of-truth claims across federation repositories and resolve the canonical owner.

### When to Use
- After any repo reorganization.
- When agents report conflicting instructions.
- Quarterly federation authority audit.

### Procedure

**Step 1: File Collision Scan**
Search all federation repos for files with the same name:
- `CONSTITUTION.md`, `floors.py`, `judgment.py`, `ROOT_CANON.yaml`, `arifos.init`, `REPO_ROUTING_CONSTITUTION.md`

**Step 2: Content Comparison**
If duplicates found, compare contents. Identical = copy. Different = conflict.

**Step 3: Precedence Resolution**
Per `ROOT_CANON.yaml` (arifOS):
- `arifOS` wins for constitutional files
- `AAA` wins for agent cards and routing
- `A-FORGE` wins for build/deployment

**Step 4: Report**
Flag each conflict with recommended owner and migration path.

### Escalation Path

| Condition | Escalate To |
|-----------|-------------|
| Constitutional conflict | arifOS 888_JUDGE |
| Cross-repo boundary dispute | Arif |

---

## Gate Type: `reversibility` — F1 Reversibility Test

Test whether a proposed change touching vault, seal, identity, constitutional, or other F1 surfaces has a valid rollback and sovereign witness.

### Steps
1. Detect F1 pattern in target file or diff.
2. If matched → emit `888 HOLD` with: file, line, proposed change, affected floor.
3. Block commit/deploy until human approval.
4. Log to `/root/.claude/hooks/f1-gate.log`.
5. If approved by Arif → re-run gate with explicit override reason; outcome enters VAULT999 witness.

### Verification Loop
- `grep -rE 'vault|seal|identity|constitutional|amanah|floor' <diff>` returns 0 lines for non-F1 commits.
- F1 surface hit → 888 HOLD blocks, human reviews, re-run with witness signature.

### Failure Modes
- Pattern false positive → human overrides with reason logged.
- Pattern false negative → F2 Truth floor tripwire catches downstream.
- Hook disabled → manual invocation still available.

### Constitutional Anchor
- F1 AMANAH (reversibility)
- F2 Truth (no F1 edit without witness)
- F13 SOVEREIGN (Arif's approval is the only valid override)

---

## Gate Type: `coverage` — Audit Coverage Check

Audit whether every constitutional floor and federation organ has code enforcement, tests, bypass resistance, and trace coverage.

### Audit Checklist

#### Floor-by-Floor Check (F1-F13)
For each floor, verify:
1. Is the floor enforced in code? (grep for floor check functions)
2. Is the floor tested? (test coverage exists)
3. Is the floor bypassable? (can authority skip it?)
4. Is the floor logged? (F11 compliance)

#### Organ Gap Analysis
For each organ (arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA, VAULT999):
1. Does it declare its authority boundaries?
2. Does it enforce brain/hands separation?
3. Can it self-authorize mutation?

#### Blast Radius Check
1. Identify any action that could cascade across organs.
2. Verify 888_HOLD gates exist before cascade points.
3. Check for bypass paths (direct API calls skipping governance).

#### Dignity Packet Inspection
1. F6 EMPATHY: Is the weakest stakeholder protected?
2. F9 ANTIHANTU: Any consciousness/sentience claims?
3. F10 ONTOLOGY: AI-only ontology enforced?

### Findings Format
```json
{
  "floor": "F01",
  "finding": "description",
  "severity": "CRITICAL|WARNING|INFO",
  "evidence": "file:line or test name",
  "recommendation": "fix suggestion"
}
```

### Verdict
- **PASS:** All floors enforced, no critical gaps.
- **PARTIAL:** Some gaps found, non-critical.
- **HOLD:** Critical gaps found, 888_HOLD triggered.
- **VOID:** Constitutional violation detected.

### Governing Floors
- F1 AMANAH: Audit itself must be reversible (read-only).
- F2 TRUTH: Report only what is observed. No inference without evidence.
- F4 CLARITY: Findings must be actionable.
- F7 HUMILITY: Report confidence level for each finding.
- F9 ANTIHANTU: No consciousness claims in audit output.
- F11 AUDITABILITY: Full audit trail logged.
- F13 SOVEREIGN: Audit can be vetoed by human sovereign.

---

## Gate Type: `tool_approval` — MCP Tool Approval & Cross-Organ Routing

Gate and route tool use across federation MCP servers according to authority, risk, and fallback policy.

### Procedure

**Step 1: Intent Mapping + Brain/Hands Classification**
- Parse intent → identify required tools → classify as governance or execution → build routing graph.

**Routing Rules:**
- Governance, judgment, floors, memory mutation, sealing → **arifOS MCP (8088) FIRST**
- Execution, build, shell, browser, jobs → **A-FORGE MCP (7072)** only after lease
- Domain intelligence → **GEOX (8081) / WEALTH (18082) / WELL (18083)** as needed

**Step 2: Tool Sequence Plan**
Build ordered tool list. For each: input_schema, output_schema, dependency, fallback.

```json
{
  "tool": "tool_name",
  "server": "arifos|aforge|geox|wealth|well",
  "input": {},
  "output_schema": {},
  "depends_on": ["step_id"],
  "fallback": "alternative_tool or null",
  "governance_gate": true|false
}
```

**Step 3: F8 Cross-Organ Gating + Lease/Judge Handoff**
- Enforce Floor F8 (Genius/Systemic Health).
- Any mutate/atomic forge_* requires valid lease_id.
- Governance paths must reach arifOS canonical tools.

**Step 4: Sequential Execution & Verification**
- Execute step-by-step.
- Verify output of each tool before piping to next.
- Reject any pipe that lets A-FORGE issue or bypass 888/999 verdicts.

**Step 5: Fallback Routing**
- If server fails or times out:
  1. Identify equivalent alternative tools.
  2. Gracefully degrade execution loop.
  3. Log failure trace.
  4. Notify ASI-observability.
  5. On governance substrate failure: escalate to 888_HOLD; NEVER fall back to execution-only path.

**Step 6: Telemetry Serialization**
- Record cross-organ connection path, MCP surface used for judgment vs execution, lease_id, tool success counts.
- Emit to AAA for lease-compliance and seal-latency metrics.

### Postconditions (tool_approval)
1. All sequential tool outputs verified and validated.
2. Alternative backup routes executed automatically if primary fails.
3. Complete cross-server trace recorded for F11 auditability.

### Failure Modes (tool_approval)
- **Substrate Collapse:** All MCP servers unreachable → degrade, log ERR_MCP_SUBSTRATE_COLLAPSE, halt high-stakes, prompt user.
- **Data Pipeline Mismatch:** Output A ≠ Input B schema → invoke hold protocol, refuse to pipe, alert developer.

### Governing Floors (tool_approval)
- F2 TRUTH: Tool outputs verified before piping. No silent corruption.
- F3 TRI-WITNESS: Cross-organ consensus required for high-stakes routing.
- F4 CLARITY: Routing plan must be more structured than raw intent.
- F8 GENIUS: Systemic health maintained across organ boundaries.
- F11 AUDITABILITY: Full routing trace logged.

---

## Telemetry per Run
```json
{
  "skill_name": "apex-gate-evaluator",
  "version": "2.0.0",
  "gate_type": "{{gate_type}}",
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

---

*Consolidated 2026-08-26 from: apex_floor_check, apex_scope_check, apex_authority_check, apex_reversibility_test, apex_audit_coverage_check, apex_tool_approval_gate.*
*AAA Skill Library — version 2.0.0*
