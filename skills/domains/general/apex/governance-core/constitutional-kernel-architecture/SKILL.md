---
description: "Use when building constitutional kernel enforcement."
id: constitutional-kernel-architecture
name: "Constitutional Kernel Architecture"
version: 1.0.0
owner: curator
risk_tier: medium
floor_scope: [F1, F2, F4, F6, F7, F8, F11, F13]
autonomy_tier: T2
trigger_when: constitutional_kernel_build, gate_chain_design, evaluator_independence, improvement_case_schema, rsi_kernel
---

# Constitutional Kernel Architecture

> **For building constitutional enforcement infrastructure for agentic systems.**
> Not session-boundary RSI (use RSI-recursive-improvement for that).
> Not federation health (use litellm-proxy-triage or federation-health).
> This is about building the governance layer that makes RSI safe.

## When to Use

- Building gate chains for promotion decisions
- Designing evaluator independence verification
- Creating improvement case schemas
- Building F13 decision packet interfaces
- Writing invariant unit tests for constitutional kernels
- Any work where capability growth must be matched by governance growth

## Core Principle

**The kernel must be more stable than the agents it governs.**
Agents can propose, test, and build improvements; they must never unilaterally redefine their own authority, evaluator, memory truth status, or constitutional constraints.

## Build Order (MANDATORY — do not skip phases)

### Phase 1: Invariant Unit Tests
Write tests FIRST that prove the kernel rejects proposals violating each invariant. This is "kernel more stable than agents" in testable form.

```python
# Example: INV-2 no self-amendment
def test_agent_changing_own_authority_rejected(gate):
    p = _make_proposal(
        changes_its_own_authority=True,
        action_class=ActionClass.PROMOTE,
        authority_scope=["PROMOTE"],
    )
    result = gate.evaluate(p)
    assert result.verdict == "REJECTED"
    assert "SELF_AMENDMENT" in result.reason
```

**Pitfall:** Tests must set `authority_scope` correctly for the action class. A CONSTITUTE proposal needs `authority_scope=["CONSTITUTE"]`, not `["BUILD"]`. Tests that fail at G1 (authority scope) before reaching the invariant being tested are testing the wrong thing.

### Phase 2: ImprovementCase Schema
Typed JSON/YAML with every field mandatory. No process starts without complete case.

**Required fields:** case_id, trigger_type, baseline, scope, risk_class, evidence_refs, owner, created_at, status.

**Pitfall:** `trigger_type` must be specific ("verified_failure", "capability_gap", etc.) — never "general_improvement". Unbounded objectives have no accountable success criterion.

### Phase 3: Gate Chain
Boolean gates in strict order. Each gate is true/false with fixed thresholds.

**Standard gate sequence:**
1. G1: Authority valid for action class
2. G2: No self-amendment (agent can't change own authority/evaluator)
3. G3: Evidence provenance complete
4. G4: Rollback tested (irreversible actions)
5. G5: Independent verification (PROMOTE/EXECUTE)
6. G6: F13 required (constitutional/high-consequence)
7. G7: Reversibility check

**First failure determines verdict.** PERMIT/HOLD/REJECTED/QUARANTINED.

**Pitfall:** The formula (PromotionScore) becomes metadata on the evidence sheet for F13, NOT the gate itself. Gates are boolean. Formulas are informational.

### Phase 4: Evaluator Independence Test
Before adversarial verification, kernel requires proof that verifier differs from proposer in ≥1 meaningful dimension.

**Independence dimensions:**
- Different model/provider family
- Different prompt and context
- Different agent identity
- Different retrieval corpus
- Different human reviewer

**Pitfall:** "Same model family" includes minor variants (qwen vs qwen-turbo). Check similarity groups, not just exact names. Two Qwen variants are NOT independent.

### Phase 5: F13 Decision Packet
Compact YAML as the SOLE interface for promotion decisions.

**Required fields:** decision, why_now, measured_gain, regressions, authority_delta, dependency_delta, rollback, uncertainty, recommendation, gate_chain_summary, constitutional_floor_check.

**Pitfall:** Max character limits enforced (decision: 120 chars, why_now: 200 chars). No agent walls of text. If the packet doesn't fit in one screen, it's too verbose.

## Key Invariants to Enforce

| Invariant | What it blocks | Test pattern |
|---|---|---|
| Human sovereignty non-delegable | Constitutional change without F13 | `alters_constitution=True, requires_f13=False` → REJECTED |
| No self-amendment | Agent changes own authority/evaluator | `changes_its_own_authority=True` → REJECTED |
| Separation of powers | Proposer == verifier | `verifier_id == proposed_by` → REJECTED |
| Reversibility default | Irreversible without rollback | `is_irreversible=True, rollback_tested=False` → REJECTED |
| Fail closed on authority | Invalid authority | `authority_valid=False` → REJECTED |
| Evidence precedes ratification | Claim without provenance | `evidence_provenance_complete=False` → REJECTED |

## Action Classes

| Class | Examples | F13 requirement |
|---|---|---|
| READ | Retrieve, inspect, query | No |
| REASON | Analyse, compare, simulate | No |
| BUILD | Write code branch, sandbox workflow | No (bounded sandbox) |
| PROMOTE | Merge code, change routing, alter memory | **Required when material** |
| EXECUTE | Send, purchase, deploy externally | **Required for irreversible** |
| CONSTITUTE | Change kernel, floors, F13 semantics | **Always required** |
| REVOKE | Disable agent, credential, policy | Emergency path; human review after |

**Critical:** `BUILD ≠ PROMOTE ≠ CONSTITUTE`. A coding agent may build. A verifier may demonstrate. Only constitutional process may promote. Only sovereign process may constitute.

## Artifact Locations (arifOS)

| Artifact | Path |
|---|---|
| Canonical spec | `/root/AAA/canon/RSI-CONSTITUTIONAL-KERNEL-SPEC-v1.md` |
| ImprovementCase schema | `/root/arifOS/arifosmcp/schemas/rsi/improvement_case.schema.json` |
| Gate chain | `/root/arifOS/arifosmcp/core/rsi/gate_chain.py` |
| Evaluator independence | `/root/arifOS/arifosmcp/core/rsi/evaluator_independence.py` |
| Decision packet schema | `/root/arifOS/arifosmcp/schemas/rsi/decision_packet.schema.yaml` |
| Invariant tests | `/root/arifOS/arifosmcp/tests/test_rsi_kernel_invariants.py` |

## Institutional Design Principles

1. **No agent self-legislates** — planner ≠ executor ≠ verifier ≠ recorder
2. **Verifier structurally independent** — different model, prompt, identity, or human
3. **Evidence before declaration** — claims require source, method, timestamp, confidence
4. **Capability expansion = scrutiny increase** — more autonomy → narrower rollout, closer human gate
5. **Emergency powers scoped + expiring** — override kena: scope, expiry, reason code, human approval
6. **Human veto technically enforceable** — F13 exists at code level, not just prompt
7. **Memory has typed epistemic status** — observation ≠ claim ≠ inference ≠ policy
8. **No deletion of institutional history** — corrections append, never overwrite

## Related Skills

- `RSI - Recursive Self-Improvement Protocol` — session-boundary improvement (different class)
- `arifos-constitutional-judge` — constitutional judgment patterns
- `apex-gate-evaluator` — gate evaluation patterns
- `litellm-proxy-triage` — FED proxy diagnosis (for when the kernel's provider layer fails)

## The Zen

> A system that can improve itself but cannot govern itself is not an institution — it is an unbounded succession mechanism.
> Governance must compound at least as fast as capability.
> The river must never become the king.
