# D2 Reclassification Rules — organ_id backfill (DRAFT, awaiting F13)

## Root cause
`organ_id` was written with the KERNEL's identity (which tool-family ran: arif_*), not the CALLER's organ. Attribution lives in `actor_id`.

## actor_id → organ mapping (derived from live distribution)

| actor_id | rows | proposed organ_id | basis |
|---|---|---|---|
| f006-edge-probe | 81,300 | aaa | AAA edge probe surface |
| 333-AGI | 38,418 | opencode | 333-AGI runs in OpenCode (EDGE) |
| openclaw-anon | 25,074 | openclaw | OpenClaw anonymous edge |
| ariffazil | 10,583 | i-arif | sovereign identity |
| opencode-e2e-probe | 9,704 | opencode | OpenCode e2e |
| openclaw / OPENCLAW | 5,374 | openclaw | OpenClaw edge (case variants) |
| ARIF / arif | 7,383 | i-arif | sovereign identity (case variants) |
| qwen-code | 3,101 | opencode | FI-003 harness (OpenCode family) [PROPOSED — review] |
| agi-gate-010-cycle | 2,720 | aaa | AAA gate cycle |
| kimi-code/FI-008 | 2,267 | opencode | FI-008 harness [PROPOSED — review] |
| wealth-mcp | 1,180 | wealth | WEALTH organ MCP |
| opencode | 805 | opencode | direct |
| anonymous | 716 | unknown | unattributable |
| (any unmatched) | — | unknown | default, fail-visible |

## Invariants
1. Kernel-tool identity stays in `tool_name` (arif_init etc.) — unchanged.
2. `organ_id` becomes CALLER attribution going forward; writers must resolve from actor map, not default 'arifOS'.
3. Backfill = single transaction with full-table snapshot rollback point; run ONLY after Arif ratifies.
4. Unknown actors default to 'unknown' (fail-visible per witness-first), never silently 'arifOS'.

## Backfill sketch (NOT for execution — post-ratification)
BEGIN;
CREATE TABLE observability.observations_pre_d2 AS SELECT id, organ_id FROM observability.observations;
UPDATE observability.observations SET organ_id = CASE ... (per mapping above) ... ELSE 'unknown' END;
-- verify counts, then COMMIT; or ROLLBACK;
