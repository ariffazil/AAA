# PHASE0-2B-INSPECTION-PLAN.md — bounded, config/receipt-first, zero live probes
2026-10-30. Per directive: exact operations for N2/N4/N5, shared-resource + side-effect
check, partial-failure join semantics, route-lineage from EXISTING config, evidence
matrix for the 12 graph patterns. Configured vs observed explicitly separated.

## 1. Exact operations N2/N4/N5 (all read-only, all stdlib/local)

| id | exact operations | input | output | side effects |
|---|---|---|---|---|
| N2 | For each of 7 governance falsifier predictions: read claim+success_rule from already-retrieved CHRON data (in-session); grep matching repos (/root/arifOS, /root/AAA) for the named falsifier marker; record hit/miss/ambiguous per criterion terms | in-session CHRON records; local repo text | per-prediction evidence row: match_term, file:line, criterion-match assessment | none (filesystem reads only) |
| N4 | stat -L + ls -la on /root/VAULT999/wealth/receipts.jsonl; id of owning user; lsattr on file + parent dir; findmnt backing of /root/VAULT999 | filesystem | permission root-cause hypothesis with owner/mode/attr/mount facts | none (no chmod/chown) |
| N5 | sha256sum of /root/A-FORGE/dist/src/interfaces/mcp/cli.js + /proc/3403239/cmdline + /proc/<pid>/exe readlink; npm lockfile hash; service ExecStart cross-check | filesystem + /proc | artifact identity object: hash, path, cmdline, lockfile ref | none (reads; /proc read is safe) |

## 2. Data dependencies / shared resources

- N2 touches /root/arifOS + /root/AAA text. N4 touches /root/VAULT999 metadata.
  N5 touches /root/A-FORGE + /proc. ZERO overlapping stores. No rate limits (local FS).
  No session state shared. No snapshot-window requirement (all facts atemporal).
- Failure isolation: each branch writes its own evidence row; one timeout does not
  cancel others (allSettled semantics). Join = full set required for REPORT, not for
  truth: a failed branch is recorded as UNRESOLVED, never dropped, never substituted.

## 3. Partial-failure join semantics (per directive)

join(allSettled) -> {fulfilled rows recorded with evidence refs} + {rejected rows
recorded as branch_name: UNRESOLVED, reason}. Overall report status = MIXED if any
branch unresolved. No "pick the best-looking branch".

## 4. Route-lineage inventory (CONFIG-FIRST — done from litellm-config.yaml, no inference call)

MEASURED from /root/A-FORGE/litellm-config.yaml [PROBE this session, config read only]:

role primary chains (by underlying litellm_params.model, deduped):
- agi-333: MiniMax-M3, qwen3.8-max, glm-5.3-flash, qwen3.7-plus, deepseek-v4-pro, glm-5.3, gemini-2.5-flash
- asi-555: glm-5.3-flash, qwen3.8-max, mimo-v2.6-pro, qwen3.7-max, deepseek-v4-flash-0731, deepseek-v4.1-flash, gemini-2.5-flash
- apex-888: deepseek-flash, MiniMax-M3, glm-5.3-flash, deepseek-v4-pro, qwen3.8-max, qwen3.7-max, deepseek-v4.1-flash

router fallbacks block: EMPTY for all three roles (no per-role fallback config found
in router_settings.fallbacks). The "fallback collision" recorded 28/10
(333-fallback#2 == 888-primary MiniMax-M3; 555-head == 888-P4 glm-5.3-flash) is
therefore visible in config as ROLE CHAIN OVERLAP, not explicit fallback entries.

pairwise underlying-model overlap (full role chains):
- 333 ∩ 555: gemini-2.5-flash, glm-5.3-flash, qwen3.8-max (3 models)
- 333 ∩ 888: MiniMax-M3, deepseek-v4-pro, glm-5.3-flash, qwen3.8-max (4)
- 555 ∩ 888: glm-5.3-flash, qwen3.7-max, qwen3.8-max (3)

CONSEQUENCE (configured, not yet observed per-call): any "independent verification"
edge drawn between 333/555/888 lanes is structurally suspect — at minimum 3 of 7
underlying models are shared per lane pair. Verifier independence from the 28/10
addendum CANNOT be claimed at model level from this config. Independence currently
available: ACTOR level (different agents) and AUTHORITY level (human 888 gate).
configured-vs-observed caveat: config shows what MAY be served; per-call resolved
model still requires x-litellm-model-name receipt per call (not probed — no
inference permitted this step).

## 5. F6 scope statement (corrected per directive)

test: synthetic interruption AFTER ledger append (os.replace atomic rewrite path),
BEFORE projection re-read; assertions: replay deduped, corrupt tail quarantined,
clean records readable. NOT tested: interruption between validation and file write,
disk-full, concurrent writers, projection read during rewrite. F6 PASS is valid
WITHIN that single interruption point only.

## 6. Evidence matrix — 12 graph patterns (status labels, no blanket pass)

| # | pattern | status | reference | gap |
|---|---|---|---|---|
| 1 | Parallel by default | SUPPORTED_BY_INSPECTION | N2/N4/N5 zero-overlap resources (this doc §2) | parallel execution not yet exercised live |
| 2 | Node contracts | TESTED_WITHIN_FIXTURE_SCOPE | shadow_capture.ingest schema validation F5 | production nodes unexercised |
| 3 | Edges as data contracts | SUPPORTED_BY_INSPECTION | TEMPORAL-CONTRACT mapping table | adapter wiring pending |
| 4 | Four base shapes | DESIGN_INTENT_ONLY | N1 chain, N2/4/5 diamond candidate, approval router | shape not executed |
| 5 | Fan-out + deliberate join | DESIGN_INTENT_ONLY | this doc §3 semantics written | not run |
| 6 | Inspectable routing | NOT_ASSESSED | arif_route exists [tools/list]; routing table not inspected | one schema read needed |
| 7 | Verification on edge | PARTIAL | verifier ≠ generator at ACTOR level; model-level independence FAILED by config (§4) | chain-diff policy decision needed from 888 |
| 8 | Durable state | TESTED_WITHIN_FIXTURE_SCOPE | F6 (scope per §5), /dev/sda1 backing [findmnt] | production failure modes untested |
| 9 | Convergent cycles | SUPPORTED_BY_INSPECTION | probe-stop + per-proposal approval = hard stops | no loop currently running |
| 10 | Local failure | TESTED_WITHIN_FIXTURE_SCOPE | F5 quarantine, F6b corrupt-tail | concurrent-failure untested |
| 11 | Topology = cost | NOT_ASSESSED | Phase-0 probes cheap; Phase-1 cost model unwritten | metric design pending |
| 12 | Production research graph | NOT_ASSESSED | out of scope this phase | — |

Summary: 0 blanket passes. 4 tested-in-fixture, 4 supported-by-inspection,
2 design-intent-only, 1 partial (with a config-level FAIL on model independence),
3 not-assessed. Two nodes flagged POSSIBLY DELETABLE (not deleted): pattern-6 check
if arif_route routing table duplicates RSR router intent; pattern-12 explicitly
deferred to avoid over-architecture (F9).

## 7. Human-authorization vs independent-observation (separated per directive)

review:
  reviewer_identity: 888 = human Arif (authorization + veto authority)
  evidence_lineages: [litellm-config.yaml, CHRON in-session records, repo text]
  model_route_ref: hermes-default lane (single lane this session)
  independent_observation_performed: false  # same actor, same lane produced and checked
authorization:
  decision: not_requested
  authority_ref: null

No claim anywhere in this document equates human authorization with independent
observation, or different routes with independent evidence.

STOP: no live inference, no ledger writes, no permission changes, no restarts.
Next live actions (if approved) remain N1-P1 (with as-of derivation first) and the
diamond N2/N4/N5 — now with exact ops + join semantics above.
