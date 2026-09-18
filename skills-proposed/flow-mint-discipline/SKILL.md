# Skill: flow-mint-discipline

> **Status:** PROPOSED · **Created:** 2026-09-18 · **Forged by:** FI-008 (kimi-code / k3)
> **Capability, not implementation.** Govern capabilities, not implementations.

## 1. Capability contract (binding)

Bounded capability: every AAA-agent emit (text, JSON, claim, or receipt) mints a `mcp__arifFlow__flow_ingest` step receipt before returning the response. This closes F11 auditability at the agent emission surface, not just at the tool call surface.

## 2. Why this skill exists

arifFlow FQ (Flow Quotient = verify/execute ratio) is currently 1.073. Above 1 is healthy; below 1 is BURNING. But that number is built from tool-call receipts; it does not capture every agent decision. **Without this skill, an agent can answer a question, produce a claim, or hand off a token without leaving any audit trail except its own internal log.** That is a hole in F11 auditability.

This skill closes that hole for the AAA agent roster.

## 3. Scope (where this skill binds)

Any agent on the AAA roster (af-forge, af-explore, af-plan, af-reviewer, af-coordinator, af-fix, af-worker, plus aaa-*) that emits a non-trivial response.

## 4. Out-of-scope

- Pure read-only reconnaissance by an Explore agent where no agent decision was made → mint a `step_type=Execute` once at session start, not per file read
- Eyeballing a result with no consequence → skip
- Routing under `mcp__aforge__forge_emit` (already mints internally)

## 5. Required MCP tools

- `mcp__arifFlow__flow_ingest` — primary
- `mcp__well__well_observe_evidence_backlog` — to confirm FQ effect after batch

## 6. Workflow (BINDING order)

```
emit_response():
    arifFlow.flow_ingest(
        actor_id=<self.actor_id>,
        session_id=<self.session_id>,
        step_type=Execute,           # default; escalate per consequence class below
        step_number=<incr>,
        cost_ns=<time spent>,
        epistemic_label=Derivation,  # default; OBS/DER/INT/SPEC/Spec per claim
        floor_verdict=Pass,          # default; Caution/Hold/Void per impact
        payload={
            "summary": "<what was emitted, 1 line>",
            "file_path": "<if applicable>",
            "consequence_class": "<T0|T1|T2|T3>",
            "citations": [...]
        },
        witness_organs=["arifos"],
        harness_fingerprint="<eta-sovg hash>"
    )
    return emit
```

### Consequence class defaults

| Class | Trigger | step_type | floor_verdict | reversibility |
|---|---|---|---|---|
| T0 | emit without state change | Execute | Pass | reversible |
| T1 | emit + minor state change | Execute | Pass | reversible |
| T2 | emit + significant state change | Verify | Caution | reversible |
| T3 | emit + irreversible consequence | Seal | Hold (until F13) | irreversible → escalate |

## 7. Truth classes (F2 binding)

Every minted receipt carries an `epistemic_label` ∈ {`Observation`, `Derivation`, `Interpretation`, `Specification`, `Seal`}. The default is `Derivation`; explicit per-claim override required.

## 8. Kill-switch (F13 Attention-Kill binding)

```yaml
kill_switch:
  kill_phrase: "STOP flow_mint — emit without receipt"
  fallback: "log a sentinel to events.jsonl so the gap is visible downstream"
  expected_recovery_time: <60s
  side_effects_on_kill: ["FQ metric temporarily in unknown state"]
```

## 9. Reversibility class (F1 binding)

`REVERSIBLE` — receipts are append-only; killing a minting skill reduces coverage, not correctness.

## 10. F11 Auditability (binding)

This skill IS F11 auditability at the agent emission layer. Its kill would create an audit hole. Decoration risk: high if abandoned.

## 11. F13 Sovereign veto (binding)

If a T3-class emission is required and F13 sovereignty is unclear, escalate with a HOLD step_type and request the F13 veto — do NOT emit.

## 12. Operator handoff (F13 silent execution binding)

This skill runs silently. It does NOT ask the operator. It DOES emit a FlowReceipt per response, which the operator can audit via `mcp__arifFlow__flow_health`.

## 13. Verification checks

- [ ] `mcp__arifFlow__flow_ingest` called per emit (per Class table)
- [ ] `step_type`, `epistemic_label`, `floor_verdict` all non-null
- [ ] `actor_id` identifies the emitting agent (not "anonymous")
- [ ] `session_id` matches the active arif_init session
- [ ] After batch, `mcp__arifFlow__flow_health` shows FQ unchanged or increased
- [ ] No emission crosses the IRREVERSIBLE line without F13 verdict

## 14. Decoration risk (binding)

If agents emit multiple uncategorized receipts in a session, the ledger becomes noise and the signal-to-noise ratio drops below utility. **Mitigation: every emission must carry semantic payload with `summary`, `consequence_class`, and `citations`. Empty payloads are decoration.**

---

DITEMPA BUKAN DIBERI · forged, not given.
