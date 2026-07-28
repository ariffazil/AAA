---
name: COPILOT_AUTONOMOUS_PIPELINE
version: v2026.07.28
harness: copilot-cli
layer: execution
agentic_level: FULL_AUTONOMOUS
triggers:
  - "autonomous pipeline"
  - "agentic workflow"
  - "auto execute plan"
  - "governed autonomous loop"
  - "full autonomous cycle"
  - "plan execute verify seal"
  - "run autonomously"
  - "pipeline full"
  - "self-driving task"
  - "autonomous agent mode"
dependencies:
  - arifOS :8088 (session, governance, seal)
  - A-FORGE :7071 (execution, pipeline, reality loop)
  - arifFLOW :7073 (metabolism, checkpointing)
---

# COPILOT_AUTONOMOUS_PIPELINE

> **DITEMPA BUKAN DIBERI** — Forged, not given.
> Governed autonomous execution pipeline for Copilot CLI.
> Chains arifOS → A-FORGE → arifFLOW into a single autonomous cycle.

## WHAT THIS SKILL DOES

Turns Copilot CLI from a "one-shot tool caller" into a **governed autonomous agent**
that can plan → execute → verify → seal in a continuous loop.

Without this skill, Copilot CLI does one thing at a time.
With this skill, Copilot CLI runs **autonomous governed pipelines**.

## THE AUTONOMOUS PIPELINE (5-STAGE)

```
STAGE 1: INIT     → arif_init(intent=X) → session_id, SCT
STAGE 2: PLAN     → forge_apex_encode(goal=X) → goal_id, task vector T
STAGE 3: EXECUTE  → forge_pipeline_run(mode=full, task=X, cc_id=SEAL) → result
STAGE 4: VERIFY   → Check outputs. If FAIL → forge_reality_loop(mode=advance)
STAGE 5: SEAL     → arif_seal(payload=result) → VAULT999 immutable receipt
       METABOLISM → arifFLOW flow_ingest at every stage boundary
```

## WHEN TO USE

Use this skill when Arif (or any agent) wants Copilot CLI to:
- Execute a multi-step task autonomously without asking per step
- Run a governed pipeline with constitutional floors enforced
- Chain arifOS governance → A-FORGE execution → VAULT999 sealing
- Self-correct on failure using forge_reality_loop
- Leave an audit trail via arifFLOW metabolism

## TOOL CHAIN (EXACT SEQUENCE)

### Quick autonomous pipeline:
```python
# 1. Ignite session
arif_init(intent="<intent>", mode="init")
# → session_id, session_token

# 2. Decompose goal
forge_apex_encode(goal="<goal>", session_token="<sct>")
# → goal_id, tasks, G scalar

# 3. Full autonomous pipeline (route + witness + forge + judge + seal)
forge_pipeline_run(
    task="<task>",
    mode="full",
    session_token="<sct>",
    constitutional_chain_id="<cc_id>"
)
# → executed result or HOLD

# 4. If HOLD or failure → self-heal
forge_reality_loop(mode="advance", intent="<intent>")

# 5. Seal to VAULT999
arif_seal(payload="<result>", session_token="<sct>")
```

### Background autonomous loop (for long-running tasks):
```python
# Start reality loop
forge_reality_loop(
    mode="start",
    intent="<intent>",
    config='{"auto_execute":true,"seal_every_iteration":true}'
)
# → loop_id

# Let it run autonomously...
# Check progress:
forge_reality_loop(mode="report")

# Seal when done:
forge_reality_loop(mode="seal")
```

### Parallel autonomous agents:
```python
forge_parallel(
    tasks=[
        {"name":"explore", "prompt":"<task1>", "target_organ":"geox"},
        {"name":"compute", "prompt":"<task2>", "target_organ":"wealth"},
        {"name":"verify", "prompt":"<task3>", "target_organ":"well"}
    ],
    failure_policy="collect_all",
    context_policy="isolated"
)
# → group_id → monitor with forge_parallel_status(group_id)
```

## METABOLISM CHECKPOINTING (MANDATORY)

Every stage boundary MUST ingest a receipt into arifFLOW :7073.
Without checkpointing, session continuity is lost on terminal close.

### Shell checkpoint (use flow_checkpoint.sh):
```bash
# At session START:
/root/scripts/flow_checkpoint.sh start "$SESSION_ID" "<intent>"

# After each STEP:
/root/scripts/flow_checkpoint.sh step "$SESSION_ID" "<action>" "Pass|Caution|Hold"

# At session END:
/root/scripts/flow_checkpoint.sh end "$SESSION_ID" "<summary>" "Pass"
```

### MCP checkpoint (use flow_ingest tool):
```python
flow_ingest(
    actor_id="copilot-cli",
    session_id="<session_id>",
    step_type="Execute|Verify|Cool|Seal|Barrier",
    epistemic_label="Observation|Derivation|Interpretation|Seal",
    floor_verdict="Pass|Caution|Hold|Void",
    lane_id=1
)
```

### Resume from prior session:
```bash
/root/scripts/flow_resume.sh          # read carry-forward + FQ
/root/scripts/flow_resume.sh --write  # also persist carry_forward.json
```

### 5-STAGE PIPELINE WITH CHECKPOINTS:
```
STAGE 1: INIT      → flow_checkpoint.sh start   → Barrier receipt
STAGE 2: PLAN      → flow_checkpoint.sh step     → Execute receipt
STAGE 3: EXECUTE   → flow_checkpoint.sh step     → Execute receipt
STAGE 4: VERIFY    → flow_checkpoint.sh step     → Verify receipt
STAGE 5: SEAL      → flow_checkpoint.sh end      → Seal receipt
```

**Rule: If you can't checkpoint, you can't proceed.** A failed 
checkpoint at any stage → HOLD the pipeline until arifFLOW is healthy.

## CONSTITUTIONAL GATES (ALWAYS ACTIVE)

| Stage | Gate | What it blocks |
|-------|------|---------------|
| INIT | F13 SOVEREIGN | Session must have valid actor |
| PLAN | F1 AMANAH | Irreversible plans → 888_HOLD |
| EXECUTE | F2 TRUTH + F12 INJECTION | Cheap claims, injection risk |
| VERIFY | F4 CLARITY + F7 HUMILITY | Entropy increase, fake certainty |
| SEAL | F11 AUDITABILITY | Unattributed actions |

## FAILURE RECOVERY

If forge_pipeline_run returns HOLD:
1. Read the hold reason
2. Adjust the plan using forge_apex_recompute
3. Re-run forge_pipeline_run
4. If 3 consecutive failures → escalate (do not loop forever)

If tool not found:
1. Use capability_search to find alternative
2. Route through arif_route if cross-organ needed

## EXAMPLES

### Example 1: "Deploy GEOX with latest changes autonomously"
```
arif_init(intent="deploy geox autonomously")
forge_apex_encode(goal="deploy geox organ: build, test, systemctl restart")
forge_pipeline_run(task="deploy geox", mode="full")
→ SEAL or HOLD
```

### Example 2: "Fix all lint errors in arifOS and commit"
```
arif_init(intent="fix and commit lint errors")
forge_pipeline_run(task="cd /root/arifOS && ruff check . && ruff format . && git commit", mode="forge")
→ result → arif_seal
```

### Example 3: "Run full federation prove suite"
```
arif_init(intent="federation prove")
forge_pipeline_run(task="cd /root && make prove", mode="full")
→ all 6 organs verified → SEAL
```

## ANTI-PATTERNS

- ❌ Don't skip arif_init — sessionless execution = F11 violation
- ❌ Don't run irreversible ops without cc_id from arif_judge
- ❌ Don't loop more than 3 times on failure — escalate
- ❌ Don't skip flow_ingest — uncheckpointed work = audit gap
- ❌ Don't use mode="full" for read-only tasks — use mode="observe" or mode="forge"

---

**SOT:** 2026-07-28 | **seal_seq:** 000-ARIFLOW-WIRED
**Agentic score:** FULL_AUTONOMOUS — 5-stage governed pipeline with mandatory arifFLOW checkpoints
