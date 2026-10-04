# When CLI/MCP unavailable — the honest doctrine

## When this applies

If `apex_judge.py` (Option 1 in main SKILL.md) and FED `:4000` (Option 2) are both unreachable — e.g., Telegram session, edge agent, isolated environment — the proper doctrine is **NOT to fake an apex verdict**. The Gödel Lock is binding: doer ≠ judge is enforced at the conversation AND model level.

## Mandatory workflow when isolated

1. **Build the evidence package** — content, claims, sources, F1-F13 concerns, action class/tier/reversibility. Write to `/tmp/apex-evidence-<name>.json` for auditability.
2. **Acknowledge the constraint** to the user — say plainly: "I cannot route apex-888 from this session. I will run the review myself with epistemic labels, but it is NOT a substitute for the apex verdict."
3. **Run your own F1-F13 self-review with epistemic labels** — but label it as "operator review, NOT apex verdict." Use `[OBS]`, `[DER]`, `[INT]`, `[SPEC]` on every claim.
4. **Flag for F13 escalation** if any floor returns FAIL or HOLD — the sovereign decides whether to proceed.
5. **Defer irreversible actions** until apex-888 routing is available OR the sovereign explicitly authorizes.

## What NOT to do

- ❌ Use `delegate_task` to spawn a subagent with the SAME model and label it "888-APEX" — `STRANGE_LOOP_VOID`. Per `delegate_task` defaults, subagents inherit the parent's model; same model + same conversation lineage = same observer.
- ❌ Write "888-APEX JUDGMENT" or "888-APEX VERDICT: SEAL" as your own output — F9 ANTIHANTU violation.
- ❌ Mark a verdict as "SEAL" without a `call_hash` from `apex_receipts/SEAL-*` SHA-256.
- ❌ Cite the operator review as the apex verdict downstream.

## Subagent fallback (model MUST differ)

If `delegate_task` is available AND the subagent is pinned to a non-parent model (e.g., via `delegation.model` config override), this becomes a valid `ACTOR_SEPARATED` fallback. But the default subagent inherits the parent's model — without explicit override, it fails Gödel separation. Do not silently hope.

## The honest move in isolated sessions

> "Apex-888 routing not available from this session. Evidence package at `/tmp/apex-evidence-<name>.json`. I will run an operator review with epistemic labels, but it is NOT a substitute for the apex verdict. If a real apex verdict is required, escalate to a session with FED access (`:4000`) or run `apex-judge isolate` from a federated runtime."

This is the Boring Path. It is also the only path that satisfies the Gödel Lock under isolation.

## Verified incident (2026-08-11, syaitan-ingat-dirinya-malaikat review)

Hermes delegated apex review via `delegate_task` to an OpenClaw persona with the apex-judge skill instruction in the goal. The subagent's independence was conversation-level (isolated context) but model-level depended on configuration — `ACTOR_SEPARATED` if model pinned to non-hermes provider, otherwise `STRANGE_LOOP_VOID`. The proper move was to acknowledge this constraint to Arif BEFORE the review — and either proceed with operator review + F13 escalation, or defer the publish until apex-888 is available.
