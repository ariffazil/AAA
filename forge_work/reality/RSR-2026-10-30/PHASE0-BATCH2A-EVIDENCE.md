# PHASE0-BATCH2A-EVIDENCE.md — inspection only, zero writes to ledgers/forecasts
2026-10-30 ~09:15-09:25 MYT, KVM8. All items fresh probes this session unless labeled PRIOR/DOC.
Purpose: reconcile C1-C4 + prior report vs paste claims. Read-only except this file tree.

## R1 — C1 authorization path (paste claimed arif_seal not_found; probe says otherwise)

- RSR-OBS-2A1: tools/list :8088 fresh probe — arif_seal IS present, one of 9 tools.
  ADVERTISED with 6 modes (seal/verify/ledger/changelog/audit/session_close).
  Paste claim "not_found" = WRONG FOR THIS SURFACE (different scope: paste probed a
  connector catalog, we probed the live MCP endpoint; different-scope, both recorded).
- RSR-OBS-2A2: arif_seal mode=ledger (read-only) as UNBOUND actor -> verdict HOLD,
  actor anonymous, authority OBSERVE_ONLY, call_hash sha256:ad5e09... — callable,
  refused at authority layer, no crash.
- RSR-OBS-2A3: arif_judge mode=validate as UNBOUND actor -> verdict HOLD,
  call_hash sha256:c37915... Contract from schema: judge returns "binding verdict ...
  Approval verdict is required prior to calling arif_forge. Outputs: evaluation
  verdict and authorization receipt." seal requires ack_irreversible=true.
- Semantics established (scoped to unbound path): verdict != authorization grant;
  authorization receipt is produced by arif_judge on approval; seal is separate
  append action gated by session+ack. authorization_grant_id as a FIELD NAME: not
  observed — binding/call_hash/session_id are the observed identifiers. UNKNOWN:
  bound-session approval path end-to-end (requires bound actor = separate governed test).
- C1 status: NOT_ESTABLISHED for bound path; NOT_MISSING as tool. No alias needed.

## R2 — C2 A-FORGE source/build/deploy reconciliation (object per directive)

- aforge_reconciliation (MEASURED 09:20):
  intended_source_commit: 22348c55 (2026-10-30 01:15 +0800, branch repair/aforge-f3-f8-2026-10-25)
  parent_build_commit:    5b46c8bf (2026-10-29 22:36 +0800)
  dirty_files: 1 (untracked data-active/ runtime state dir — NOT code)
  working_tree_code_diff: 0 files (git diff HEAD empty for code)
  deployed_artifact: /root/A-FORGE/dist/src/interfaces/mcp/cli.js mtime 2026-10-29 22:36:56 +0800
  service: a-forge-mcp.service, node pid started 2026-10-29 19:58 (older than dist!)
  interpretation (INFER, flagged): running process predates the dist file on disk;
  dist file equals build of 5b46c8bf; HEAD 22348c55 (checkpoint commit, 01:15) is
  NEWER than dist -> source is one checkpoint ahead of build. NO uncommitted code.
  drift scope: ONE checkpoint commit, labeled "checkpoint ... in-flight lane work".
- C2 status: BASELINE_RECONCILIATION_REQUIRED, narrow scope: dist built at 5b46c8bf,
  running process even older than that build (restart needed to pick up even 5b46c8bf).
  Rebuild = separate governed mission (2B), NOT executed.

## R3 — C3 CHRON closure debt: 10 due inspected, ZERO closed (no write calls made)

Due set read via chron_predictions_due (fresh probe). Composition:
- 5x APEX/QRL/IRFAN governance falsifier events (pred-387b, 2792d, e9e75, 8b835, da1bd,
  b1c05, f843a): criteria are internal-federation events, evidence search = repo/receipt
  inspection, resolvable by offline inspection.
- pred-7229f: EROI audit /opt find >=5 dead services by 2026-10-21 — measurable offline.
- pred-9b8ad: verified predictions >= 40 by 2026-10-22, success_rule includes exact
  command `python3 -m chron status` — directly measurable NOW (observed 54 verified
  in Phase 0) -> strong candidate RESOLVED_TRUE proposal.
- pred-a955a: named-person khalwat identity prediction (Nik Nazmi) — EXTERNAL event,
  requires news evidence; resolution proposal needs source, not memory.
- All 10: proposals DRAFTED ONLY. No chron_record_verification / resolve_unverifiable
  called. 2B requires approval per directive.
- C3 status: CLOSURE_DEBT_CONFIRMED (10), inspection complete, zero writes.

## R4 — C4 metrics scope

- Global cohort n=47: allowed as REPORTED_AGGREGATE with policy version from
  calibration.json (chron-observation-level-rule-v1). Per-source/per-model claims:
  FORBIDDEN (single source=chron_events dominates; effective per-source n small).
- Brier 0.1735 (calibration.json) vs 0.1780 (recomputed from records): unreconciled
  delta ~0.005, flagged; hypothesis = snapshot timing (calibration.json updated_at
  2026-10-26 vs new verifications after). NOT yet established.
- C4 status: REPORTED_AGGREGATE; COHORT_REVIEW_REQUIRED before any skill claim.

## R5 — FED DEAD/LIVE (paste claim; this session could not reproduce)

- FED :7074 health fresh probe: status healthy; provider chain NOT exposed in /health
  payload; /providers /models /chain /status endpoints = Not Found.
- Paste claim of same-response DEAD+LIVE: NOT REPRODUCED this session; no probe of the
  fed_route tool path made (avoided write-ish routing calls). Status: UNREPRODUCED,
  scope-unknown. Needs the caller-context (fed_route tool output) to reconcile.

## R6 — GEOX/WEALTH/WELL read-only probes (batch 2A-6)

- WELL :18083 well_registry_status -> ok:true, REGISTRY_PASS, 10/10 tools registered,
  0 phantom. NOTE: registry self-check passes while /health still drift:true + degraded.
  Both true simultaneously: registry integrity != deployment freshness.
- WEALTH :18082 capital_registry(mode=list) -> tool RAN but receipt persist FAILED:
  "[Errno 1] Operation not permitted: /root/VAULT999/wealth/receipts.jsonl",
  call_status FAIL in _meta.wealth_receipt. NEW DEFECT: WEALTH cannot persist receipts
  to VAULT999 path (permission). Data answer itself not fully inspected (page cut).
- GEOX :8081 geox_surface_status -> status healthy (surface), 27 public tools,
  conformance QUALIFIED. /health still kernel_verdict HOLD + degraded — surface tool
  works; kernel-level health separate.

## Contradiction ledger (prior report vs paste vs fresh probe)

| item | prior report (RSR Phase0 rev2) | paste batch-2 text | fresh probe 2A |
|---|---|---|---|
| arif_seal | present in tools/list | not_found | PRESENT (R1) |
| A-FORGE drift | repo != deployed commit | dirty tree, repair branch | 1 untracked dir only, dist=5b46c8bf, HEAD one checkpoint ahead (R2) |
| overdue forecasts | 10 awaiting evidence | 10 overdue | 10 due, composition mapped (R3) |
| FED DEAD/LIVE | not observed | claimed | UNREPRODUCED (R5) |
| GEOX/WEALTH/WELL | transport-deployed, mostly uncalled | UNKNOWN | probed read-only: WELL pass, WEALTH receipt-persist FAIL, GEOX surface ok (R6) |
| CHRON n | 47 effective | n<8 per source | single-source dominated; per-source FORBIDDEN claims (R4) |

## Unknowns remaining
1. Bound-actor approval path end-to-end (needs governed session test — 2B+).
2. WEALTH receipts permission fix (root cause: chattr? ownership? — needs inspection with write intent).
3. Brier delta reconciliation.
4. FED provider chain visibility (no public endpoint).
5. Running node process vs dist: restart gap quantified but restart itself = 2B write-ish action, not done.

STOP: per directive — no forecasts closed, no events created, no rebuilds, no gate changes.
