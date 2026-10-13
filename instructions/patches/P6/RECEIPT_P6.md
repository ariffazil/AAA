# PATCH 6 — CLOSURE RECEIPT

## PATCH_ID
P6

## ROOT_CAUSE
The HERMES MCP `hermes_contradiction` tool at `/root/HERMES/mcp/hermes-rasa/server.py:587-629` is a **storer** (writes one row to `contradictions` table for two human perspectives), not a detector. The Opus and ChatGPT external tests both submitted scanner-shaped inputs and observed "no contradictions" because the storer had no comparison logic — and no MCP surface existed that did. The defect was that a *detection surface* was implied but never implemented.

## CONTRACT_STATE
CORRECTED_WORKING_CONTRACT — Recipe re-authored to add an additive `@mcp.tool hermes_contradiction_scan` rather than to modify the existing storer. The detector is pure-function, deterministic, and produces only semantic evidence rows.

## FILES_CHANGED
- `/root/HERMES/mcp/hermes-rasa/server.py` — additive 241 lines inserted between line 629 (end of `hermes_contradiction`) and line 631 (separator before TOOL 6).
- `/root/AAA/instructions/SUBSTRATE-PATCHES-v2.1.md` — recipe re-authored to match traced source reality.

## PRE_HASH (server.py)
`sha256:1d441f7ee65c58743f528a1bd9d68b14e2a2defbb7234297640543feddf3b798`

## POST_HASH (server.py)
`sha256:7f43eece4296bd0617891cf814b1eb9f19dcff4d34c1b5e45b524c9775bf07c0`

## BACKUP
- Pre-patch (binary-equivalent): `/root/AAA/instructions/.patch-receipts/P6_server.py.before.md`
- Post-patch (binary-equivalent): `/root/AAA/instructions/.patch-receipts/P6_server.py.after.patch.md`

## TESTS
| Suite | Result |
|---|---|
| `python3 /root/AAA/instructions/patches/P6/test_detector.py` (pure-unit, 14 tests) | OK |
| `python3 /root/AAA/instructions/patches/P6/server_smoke.py` (in-process, 11-claim smoke) | OK |
| `python3 /root/AAA/instructions/patches/P6/mcp_call_v4.py` (live MCP via :18420) | OK |
| `python3 /root/AAA/instructions/patches/P6/mcp_negative.py` (4 negative controls at MCP) | OK |
| `python3 /root/AAA/instructions/patches/P6/mcp_side_effect.py` (canonical-store side-effect probe) | OK |

## EXIT_CODES
All five exit code: `0`.

## BUILD_ARTIFACT / BUILD_HASH
The artifact is the source file itself; FastMCP loads it dynamically — no separate build step. SHA before/after captured in `PRE/POST_HASH`.

## SERVICE_OWNER
- PRE_PID = 1194 (root, started 2026-10-09 08:39, command `/usr/bin/python3 /root/HERMES/mcp/hermes-rasa/server.py --port 18420 --transport http`, cwd `/root/.hermes`, listener 127.0.0.1:18420)
- POST_PID = 107208 (root, command unchanged, started 2026-10-11T01:15:05Z by `restart_v2.sh`, listener 127.0.0.1:18420, port-bound in 1.6s)
- The old PID was killed TERM-then-KILL after the new PID bound the port. Single-owner verified post-restart.

## MCP_RESULT
- `tools/list` registered 33 tools including both `hermes_contradiction` (storer) and the new `hermes_contradiction_scan` (detector).
- 11-claim Budget 2027 fixture returned `ok:true`, `count:15`, classes `{SCOPE:1,SOURCE:2,MODEL_VERSUS_MODEL:6,MODEL_VERSUS_REALITY:2,DENOMINATOR:1,MEASUREMENT_VERSUS_INTERPRETATION:3}`.
- Each row carries `contradiction_id`, `claim_a_id`, `claim_b_id`, `class`, `source_a`, `source_b`, `subject`, `unit`, `temporal_scope`, `geographic_scope`, `denominator_a`, `denominator_b`, `possible_reconciliation`, `evidence_needed`, `decision_impact`, `status`, `limitations`.

## FIXTURE_RESULT
PASS. All five required detections observed:
- RM510b vs RM459.8b → SCOPE / RESOLVED_BY_SCOPE
- RM32b vs RM25b → SOURCE / OPEN (also surfaces as MODEL_VERSUS_MODEL because both are FORECAST/independent clusters)
- 3.3% vs 3.6% → MODEL_VERSUS_MODEL / OPEN
- Subsidy scope → DENOMINATOR / PARTIALLY_RECONCILED
- USD85 model vs USD101 spot → MODEL_VERSUS_REALITY / OPEN
- C11 internal inconsistency → MEASUREMENT_VERSUS_INTERPRETATION / OPEN

## NEGATIVE_CONTROL_RESULT
- Identical same-source claims → 0 rows (cluster dedup active)
- Different sources, identical text → 0 rows (verbatim copy detection not in scope; contract-silent)
- Different units → 0 rows, 0 SCOPE rows (correct)
- Garbage inputs (`{}`, `[]`, malformed text) → detector returns `ok:true` with empty `contradictions`, never crashes

## SIDE_EFFECT_CHECK
10 detector invocations: `contradictions` table count went from 6 → 6 (delta = 0).
1 storer invocation with `event_id="p6-side-effect-100005"`: row count 6 → 7 (delta = 1, the row carries the exact event_id we passed).

The detector is side-effect-free.

## ROLLBACK_PROOF
Rollback recipe (`-` is the script's name): restore server.py from `.patch-receipts/P6_server.py.before.md`, kill PID 107208, start a fresh server with the pre-patch source. Diff at file level: byte-equal swap. Tested in dry-run by confirming the pre-patch file at `.patch-receipts/P6_server.py.before.md` matches the originally-observed byte content (`1d441f7e…`).

A second rollback recipe exists: rather than restoring the file, kill the process and start the **same** file freshly — the detector is purely additive, so the live process can be reloaded with the patched source without ever dropping the new tool. Rollback to no-detector state requires the byte-swap.

## STATUS
`RUNTIME_ACTIVE`

## DEPENDENCY FOR FUTURE WAVES
P6 alone does **not** clear the `deployment_drift` HOLD. Per the mandate's discipline 6 ("Do not clear deployment drift before P1, P2 and P3 pass adversarial tests"), we proceed to Wave 1 with the substrate drift alarm still active. Once Wave 1 completes and we can re-run a session verifying that drift, P1 (verdict-text authority) is the most plausible next defect to consolidate.

