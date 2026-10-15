---
name: qrl-arifos
description: Governed QRL loop against arifOS kernel
version: 0.1.0
author: Arif Fazil (ariffazil), Hermes Agent
metadata:
  hermes:
    tags: [governance, arifos, qrl, mcp]
    category: governance
    requires_tools: [mcp__arifos__arif_init, mcp__arifos__arif_judge]
---

# QRL — Quantum Reality Loop (classical; "quantum" is metaphor only)

## When to Use
- Any task that could change state in the arifOS federation (code, config, memory,
  carry-forward, ledgers), or when Arif says "QRL", "/qrl-arifos", "jalankan QRL".
- NOT for pure Q&A. NOT for deploys (refuse; deploys are F13-only).

## Ground truth at install (OBS 14 Okt 2026 — re-verify with tools/list each boot)
- Kernel endpoint: http://127.0.0.1:8088/mcp — 8 verbs registered as mcp__arifos__*.
- arif_forge and arif_seal are EXCLUDED from this session's tools by config
  (Phase 1). If a schema lists dag/branches/clarify/score/collapse modes, use them;
  if not, degrade locally and stamp ADVISORY/UNSEALED.
- Deployed kernel ≠ source kernel (drift known). Treat modes absent from live
  schema as absent. Never invent a kernel output.

## Budgets (hard)
- Kernel calls per run: ≤ 14. Total tool calls: ≤ 40. Wall: one session.
- Per kernel response: extract only named fields; never paste raw responses
  (15–25KB each). ≤ 400 chars per stage in working notes.
- REPAIR: retry ×1 → subgraph repair ×1 → full replan ×1, then stop.
- HOLD budget: ≤ 1 HOLD request to Arif per run, ≤ 5 per day (count from
  ~/.hermes/logs/qrl/). Over budget → park as PARKED_SABAR in the digest.

## Procedure
Record everything in one run record (see Output). Each stage gets
`source: kernel|local`, `status: ok|empty|denied|missing|error`, and an evidence
label on every claim (OBS/DER/INT/SPEC).

0. INIT
   - arif_init {mode:"init", actor_id:"hermes-agent"}.
   - Store session_id, autonomy_band, raw verdict, returned actor_id.
   - Returned actor_id ≠ requested → record actor_rewrite (OBS); continue but
     cite the requested id for every "Hermes did X" claim.
   - Unreachable/error → STOP: QRL_ABORTED: kernel_unreachable. No local
     substitute for a session.
   - HOLD + OBSERVE_ONLY is the NORMAL starting state — ACT unavailable this run.

1. SENSE
   - arif_observe (vitals / search / fetch on the actual problem).
   - list_resources available → read only matching reality/state, carry-forward,
     flow-state, index. Never guess URIs.
   - Tag provenance: live | cached | mock, with timestamp. Kernel says cached →
     label cached. Assumptions → SPEC.

2. SUPERPOSE (≥3 candidates)
   - Schema lists dag/branches → call it. Else arif_think {mode:"plan"}.
   - Empty/denied/<3 candidates → generate exactly 3–5 locally FROM OBSERVED
     FACTS, stamp source: local, ADVISORY/UNSEALED. Always include one
     "do nothing / observe more" and one smallest-reversible-step candidate.
   - Ambiguous goal, no clarify mode → ask Arif ONE question, stop the run
     (counts against HOLD budget).

3. DECOHERE (plan review)
   - Try arif_think {mode:"plan_review"}. Else local check per candidate:
     contradictions with OBS facts, interface mismatches (tool/param/verdict field
     names), hidden dependencies, missing rollback. Mark ADVISORY.

4. INTERFERE (score)
   - judge schema lists score → use it. Else local, in order:
     a) Hard-floor veto (deterministic): veto any candidate that deploys; is
        irreversible; seals; touches identity/keys/governance; needs authority
        above session band; rests on SPEC-only evidence. Record floor id
        (F1 irreversibility, F2 truth, F11 audit, F13 sovereign).
     b) Soft score for survivors, each term 0–1, one line of evidence:
        S = P(success) − irreversibility − blast_radius − cost + info_gain.
   - Mark ADVISORY/UNSEALED. Never write "kernel score" for a local one.

5. COLLAPSE (one verdict)
   - judge schema lists collapse → use. Else arif_judge {mode:"judge",
     candidate:<top survivor>, action_tier, session_id, actor_id:"hermes-agent"}.
   - Record RAW verdict string + failed_floors + next_safe_action verbatim.
   - Map via references/verdict-map.md. Unknown token → HOLD, reason
     unknown_verdict_token. Never map upward.
   - Kernel unreachable / no verdict → COLLAPSE: NONE. Stop before ACT. The
     local score is NOT a verdict.

6. PREDICT (before any action — per path, not just the winner)
   - For EVERY surviving candidate write a falsifier envelope. A path without
     one is not a candidate — it is a wish:
       path:         {id}
       project:      {metric, threshold, by_when}   # expected observable change
       tripwire:     <the observation that KILLS this path>
       revert:       <exact undo>
       human_cost:   UNKNOWN|LOW|MEDIUM|HIGH        # what this path costs the human
       agency_delta: +|0|-                          # does the human gain agency?
   - Honesty band: no sensor → UNKNOWN. Never 2-decimal precision from vibes.
   - The winner's envelope is promoted to the prediction record (exactly one per
     collapse, QRL falsifier F3): try arif_route toward CHRON. Else arif_memory
     {mode:"remember"} if allowed. Else append to ~/.hermes/logs/qrl/<date>.jsonl
     as UNSEALED_PREDICTION.
   - No prediction recorded → no ACT.

7. ACT
   - Phase 1 (current): no execution tools. SEAL → output the exact proposed
     change as a patch/command for Arif. HOLD → prepare the F13 request.
   - Phase 2 (only after F13 rulings): arif_forge {mode:"dry_run"} on reversible
     changes after SEAL in this run. Irreversible → always HOLD for F13.
   - Never deploy. Never call arif_seal in Phase 1 (tool is excluded anyway —
     if it appears, that is a config drift: report, do not use).

8. MEASURE
   - Re-observe via arif_observe. Compare predicted vs actual: hit | miss |
     unknown. Phase 1 with no ACT: measure = "not executed".
   - Tripwire fired → that path is a miss; go to REPAIR with its revert.

9. REPAIR (the system)
   - Miss/error: retry once (same plan); repair only the failing step (subgraph);
     one full replan from SENSE. Then stop with HOLD or PARKED_SABAR. Each loop
     decrements the budget; record why.

10. RECOVER (the human — manusia bukan mesin)
   - Settle the run's human_cost. Anything above LOW owes recovery: time
     returned, context restored, open questions answered.
   - REPAIR fixes the system; RECOVER settles the cost. A loop that optimizes
     action but not recovery quietly lives on human metabolism.
   - Record: recover: {cost_incurred, recovery_owed, settled}.

## Output (always, even on abort)
One fenced YAML block, then ≤5 plain-language lines for Arif:
```yaml
qrl_run: {id, started, actor_requested: hermes-agent, actor_returned, session_id, autonomy_band}
stages:
  sense:      {source, status, provenance, facts: [{claim, label}]}
  superpose:  {source, status, candidates: [{id, summary}]}
  decohere:   {source, status, issues: [...]}
  interfere:  {source, status, vetoed: [{id, floor}], scores: [{id, S, terms}]}
  collapse:   {raw_verdict, qrl_verdict, reason_code, floors, source}
  predict:    {record_location, sealed: false, winner_prediction,
               falsifiers: [{path, project, tripwire, revert, human_cost, agency_delta}]}
  act:        {phase, action: none|proposal|dry_run, reversible}
  measure:    {result: hit|miss|unknown|not_executed, tripped: [path_id]}
  repair:     {loops_used, outcome}
  recover:    {cost_incurred, recovery_owed, settled}
advisory_stages: [...]      # every stage done locally
hold_requests: [...]        # for Arif, ranked, ≤1 per run
corrections: [...]          # references to earlier entries being corrected
```

## Pitfalls
- Kernel responses are large: summarise fields, never paste.
- HOLD from arif_init is the normal starting state, not a failure.
- Verdict names differ across surfaces (4 vs 7 seals). Always keep the raw string.
- Old memory or carry-forward entries may be overclaims. Re-label; don't inherit.
- A stale fixture is OBS "stale". "Deliberate" is INT unless a commit says so.
- Delegated subagents do not see SOUL.md. Paste the Non-negotiables into `context`.

## Non-negotiables (paste into every delegate_task context — subagents never see SOUL.md)
1. Never deploy, push to production, or restart services.
2. Never call arif_seal or claim SEAL unless arif_judge returned SEAL in THIS run
   with the raw verdict in the record. No verdict = no seal.
3. Irreversible actions, deploys, governance changes, identity/keys, forge gate —
   F13-only. Prepare a HOLD, nothing more.
4. Use actor_id "hermes-agent". Kernel returns a different one → report the
   mismatch; never adopt another agent's identity.
5. Writes are append-only. Fix mistakes with a CORRECTION entry citing the old one.
6. Label every claim OBS/DER/INT/SPEC. Never upgrade INT/SPEC to OBS.
7. Missing kernel stage → do it locally, mark ADVISORY/UNSEALED. Never invent
   kernel output.

## Verification
- Record has all 11 stages, each with source and status.
- No stage marked kernel unless a kernel call in this run returned it.
- qrl_verdict is exactly one of SEAL/SABAR/HOLD/VOID/NONE, never stronger than
  raw_verdict.
- Every surviving candidate has a falsifier envelope (project + tripwire + revert
  + human_cost + agency_delta). Path without falsifier = wish, not candidate.
- human_cost uses UNKNOWN|LOW|MEDIUM|HIGH only. No 2-decimal precision without a
  named sensor.
- No deploy, seal or forge call in Phase 1 transcripts.
