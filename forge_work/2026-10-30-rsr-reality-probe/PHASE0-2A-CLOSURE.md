# PHASE0-2A-CLOSURE.md — inspection complete within stated scope
2026-10-30, KVM8. Closes batch 2A. Five returns per review directive.
Provenance tags: [PROBE] = my own tool call with timestamp in-session; [RELAYED] =
Hermes-lane report pasted by Arif, not independently reproduced; [DOC] = schema/canon read.

## 1. OBSERVATIONS

| id | claim | provenance | scope limit |
|---|---|---|---|
| O1 | arif_seal present in MCP tools/list :8088, 6 modes | [PROBE 09:0x] | advertised; not executed in write mode |
| O2 | arif_seal(ledger) unbound -> HOLD, OBSERVE_ONLY, call_hash ad5e09… | [PROBE] | one request shape |
| O3 | arif_judge(validate) unbound -> HOLD, call_hash c37915… | [PROBE] | one request shape |
| O4 | arif_seal on REST wire /tools/arif_seal; canary empty request as OBSERVE for IRREVERSIBLE-class tool -> VOID/HOLD refusal citing F1_AMANAH "classification forgery" | [RELAYED] | refusal for that malformed/miss-classified request only |
| O5 | GEOX geox_claim refused: requires OPERATOR, session OBSERVE_ONLY | [RELAYED] + consistent with my probe showing kernel_verdict HOLD on :8081 health | claim-engine content UNKNOWN without OPERATOR session |
| O6 | WELL: INSUFFICIENT_DATA, test_fixture_detected, freshness EXPIRED, "no calibrated evidence-quality model implemented", HIGH_RISK label, no routing/vault action taken | [RELAYED] | one response; all-path boundary compliance NOT established |
| O7 | WEALTH capital_claims schema has vault-write side effect -> deliberately not called; capital_registry ran but receipt persist FAILED (Errno 1, /root/VAULT999/wealth/receipts.jsonl) | [PROBE for registry], [DOC for schema] | root cause of permission failure unknown |
| O8 | FED DEAD vs LIVE: 27 days apart, different probe methods (model-level sweep vs provider-level api_probe) | [RELAYED] | COMPARABILITY_UNRESOLVED; not reproduced by me; FED /health does not expose provider chain; /providers /models /chain /status all Not Found [PROBE] |
| O9 | A-FORGE: HEAD 22348c55 (branch repair/aforge-f3-f8-2026-10-25), 0 uncommitted code files, 1 untracked runtime dir data-active/, dist mtime 2026-10-29 22:36 (= build of parent 5b46c8bf), node process started 2026-10-29 19:58 (predates dist on disk) | [PROBE] | mtime != artifact identity; running binary may predate even 5b46c8bf build |
| O10 | CHRON: 10 predictions due, composition mapped (7 internal governance falsifiers, 1 measurable-now pred-9b8ad "verified>=40" vs observed 54, 1 EROI audit, 1 external news event) | [PROBE] | read-only; zero closures |
| O11 | Kernel 401 Unauthorized response class on REST contract | [RELAYED as OpenAPI doc] | DOCUMENTED contract, NOT observed HTTP enforcement |

## 2. RECONCILIATION (old claim -> new claim -> reason -> residual uncertainty)

1. "arif_seal not_found" (first paste) -> PRESENT on both MCP [PROBE O1] and REST [RELAYED O4].
   Reason: first paste probed a connector catalog, not the live endpoint. Residual: why the
   Hermes MCP surface in that lane did not project it (projection_difference: intended
   policy unknown; remediation undetermined; NO authorization to change projection).
2. "HOLD means gate enforces" (my rev-1 phrasing) -> one canary = one negative case
   observed. Residual: bound-actor approval path UNTESTED; test matrix proposed
   (malformed / wrong-class / no-identity / insufficient-scope / stale-binding), each
   row a separate governed decision; no irreversible call without approval.
3. "WELL boundary 100% compliant" -> one inspected response maintained uncertainty and
   showed no routing/vault action. Residual: all-path compliance NOT established;
   persistence side effects undetermined from a response alone.
4. "FED contradiction" -> two non-equivalent observations (different time + method).
   Status CONTESTED with recorded falsifier: simultaneous same-key dual-endpoint canary.
   That canary = inference call with cost/log side effects -> separate approval, not
   read-only batch.
5. "sifar mutation" -> precise scope: no rebuild, deploy, gate change, projection change,
   or CHRON closure. Local evidence files written (this tree). Probe persistence effects
   (kernel call_hash audit rows) expected organ behavior, not exhaustively audited.
6. Brier 0.1735 vs 0.1780 -> UNRECONCILED; hypothesis snapshot-timing only.

## 3. AUTHORITY CONTRACT (documented vs observed, kept separate)

Documented [DOC]:
- arif_judge outputs "binding verdict ... required prior to calling arif_forge",
  returns evaluation verdict + authorization receipt; modes judge/intercept/validate/
  hold/escalate.
- arif_seal appends immutable ledger, requires ack_irreversible=true; class IRREVERSIBLE.
- Verdict lattice 5: VOID > HOLD > SABAR > PARTIAL > SEAL (models/verdicts.py).
Observed [PROBE/O4 RELAYED]:
- Unbound actors get HOLD/OBSERVE_ONLY on judge+seal-read; empty mis-classified seal
  request gets VOID refusal citing F1_AMANAH.
- No authorization_grant_id FIELD observed anywhere; observed identifiers are
  session_id, actor_id, call_hash, trace_id. Whether a receipt object issued on an
  APPROVED verdict carries a grant identifier: UNKNOWN (requires governed bound test).
- Documented semantics != observed enforcement; equivalence established only for
  refusal paths probed.

## 4. CHRON RESOLUTION PROPOSALS (drafted, NOT submitted; exact write args pending approval)

| pred | criterion (abridged) | evidence status | proposed result |
|---|---|---|---|
| pred-9b8ad | verified >= 40 by 2026-10-22, success_rule = chron status command | MEASURED in-session: 54 verified (Phase 0 + today) | correct=true (subject to verifying the counter as-of 22 Oct vs now — snapshot timing question) |
| pred-b1c05, f843a (IRFAN F-A/F-B) | internal falsifier events, evidence = repo/receipt inspection | NOT searched yet | UNDECIDED — needs evidence pass first |
| pred-da1bd (QRL inc 1) | internal falsifier set | NOT searched yet | UNDECIDED |
| pred-387b, 2792d, e9e75, 8b835 (APEX AX-0/Lane B/C/D) | internal falsifier events, repo/test evidence | NOT searched yet; note APEX audit memory 30/10 says G=(A·P·E·X)^1/4 implemented+deployed — bears on Lane B/D | UNDECIDED |
| pred-7229f (EROI /opt >=5 dead services by 21 Oct) | filesystem audit | NOT run (would be a fresh probe; cheap, read-only — can run in 2B with approval) | UNDECIDED |
| pred-a955a (Nik Nazmi khalwat identity) | EXTERNAL news event, verify_at 23 Oct | requires news probe with sources; memory alone insufficient | UNDECIDED — needs sourced evidence, else UNVERIFIABLE per policy |

Proposed batch 2B write order (each individually approved): 9b8ad first (evidence
in-hand), then evidence passes for internals, news probe for a955a. correct semantics:
record prediction correctness under ORIGINAL criterion, never event-occurrence alone.

## 5. PROPOSED NEXT ACTIONS (each: purpose / side effects / approval / stop condition)

| # | action | side effects | approval needed | stop condition |
|---|---|---|---|---|
| N1 | Close pred-9b8ad via chron_record_verification | one ledger append | 888 yes/no | receipt persisted + chron shows verified |
| N2 | Evidence pass (read-only) for 7 internal falsifiers | none beyond reads | within inspection scope | each -> proposed resolution row |
| N3 | News probe for pred-a955a | external queries | yes (external surface) | sourced verdict or UNVERIFIABLE |
| N4 | WEALTH receipt permission inspection (stat/ls -la, no chmod) | none | none (read) | root cause named; fix = separate write |
| N5 | A-FORGE artifact hash + process cmdline capture | none | none (read) | provenance object complete (hash, path, build ref) |
| N6 | FED dual-endpoint simultaneous canary | inference call: cost + logs | yes, separate | DEAD/LIVE reconciled or CONTESTED stands |
| N7 | Projection-difference review (arif_seal absent from Hermes MCP lane) | config change if pursued | 888 decision: intended separation vs config lapse | recorded decision; NO unilateral expose |
| N8 | Bound-actor authority test matrix | governed session + harmless candidates | yes, per-row | each row's refusal/grant observed and recorded |

Open UNKNOWNs carried forward: bound approval path; grant identifier shape; projection
policy intent; FED provider chain visibility; Brier delta; WEALTH permission root cause;
A-FORGE artifact-hash provenance (N5 closes).

CLOSE: Batch 2A inspection complete within stated scope. Not claimed: full boundary
proof, gate universality, or authorization-path success. Awaiting 888 on N1-N8.
