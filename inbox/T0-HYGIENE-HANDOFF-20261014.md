# HANDOFF → 555-ASI / kernel lane: T0 HYGIENE PACK (AUTHORIZED, F13 "a - Z apex zen all" 2026-10-14)
From: HERMES (spec + probes) · To: 555-ASI (executor) · Full spec: /root/.hermes/receipts/T0-HYGIENE-PACK-SPEC-20261014.md
Ledger: e-a05ed4c8 (directive) · F13 "go" recorded this turn.

## WHAT TO EXECUTE (patch-class only, branch hygiene/t0-20261014)
HF-1 single verdict enum {SEAL,SABAR,HOLD,VOID} + reason_code field.
  Emit sites probed: arifosmcp/runtime/tools.py L458 (mixed OBSERVE_ONLY/DEGRADED/888_HOLD in
  verdict position) and L607-608 ("SABAR_HOLD" alias). Kill aliases, map to enum + reason_code.
HF-2 envelope diet: tools/list currently 54,664 B over just 8 tools (arif_init schema 11,846 B,
  arif_judge 10,147 B, arif_memory 6,699 B = 52% of the envelope). Move long purpose prose to a
  description_url resource; ≤400 chars inline per tool. Target: tools/list ≤20 KB, median call <2 KB.
HF-3 provenance enum {live,cached,mock} required on observations; mock-as-live = hard reject.
HF-4 arif_init stores root intent VERBATIM in objective (no kernel-side paraphrase).
HF-5 OBSERVE_ONLY sessions: return advisory content stamped sealable:false — never empty body;
  floor block returns HOLD + floor_id.

## PROTOCOL
Branch hygiene/t0-20261014 → one commit per HF, each with its partial T0 test green → full T0
(200-call battery, tests pre-registered in the spec) → deploy via attestation path (this closes
the standing :8088 SOT drift warning — confirmed again 08:5x MYT) → return before/after hashes,
per-HF pass/fail, T0 raw output, rollback = per-commit revert.

## FROZEN (separate F13 binaries, not this handoff)
PlanGraph + dag/branches/score/collapse modes · CHRON agent-task wiring · forge plan_graph_id
gate (B1 conflict: 30-Sep "no tool blocks" directive vs enforcement — F13's call) · MCP
2026-07-28 transport · per-agent Ed25519 keys · C1-C4 conformance suite.

## NOTE FROM HERMES LANE (reconcile when convenient)
333-AGI reported "first-person collaboration" on today's kernel probes (envelope ~25KB, SABAR-vs-HOLD
divergence) while HERMES independently measured the same surfaces (tools/list 54,664B — likely the
~25KB was a subset view; /health degraded attestation). Either two witnesses or an attribution
error — please log both sources in the T0 receipt.

Ground state when authorized: main @ b78092a64 (FORGE 000Ω commits), 1 dirty file, no uncommitted
verdict-token changes. Execute on that base.

## ADDENDUM (F13 "Activate shadow mode", 2026-10-14) — IMPOSSIBLE_TASK_HOLD joins this pack

Authorized Phase 0 SHADOW ONLY (log-only, no enforcement). Full spec:
/root/AAA/inbox/IMPOSSIBLE-TASK-HOLD-SPEC-20261014.md
Implement as part of this branch (patch-class, one commit):
- shadow_hold event schema: {task_id, trigger(BUDGET_EXCEEDED|ZERO_SOLVE|STRUCTURAL_BLOCK),
  budget_consumed, would_be_reason_code, ts_utc} → append-only JSONL alongside T0 receipts.
- Gate review day 14 (28 Oct MYT): FP-cost derivation computed from shadow data; decision
  deadline day 21 (4 Nov MYT): PROMOTE / RETUNE (once) / KILL — no fourth state.
- Phase 1 enforcement requires a separate F13 authorization line. Do NOT enforce in this deploy.
- Zero-solve register seed: task classes with zero solves across T1-T7 conformance history
  (4 independent identities, per conformance baseline receipt).
