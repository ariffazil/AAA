# arifOS Kernel Contradictions — 2026-08-06 Map

Snapshot of contradictions found during the post-crash stabilization
session. The kernel crashed with `IndentationError` at `tools.py:1790`
because D4 v1 misplaced `MODE_AFFORDANCE_OVERRIDES`. After manual fix
to D4 v2 and live restart, three read-only recon agents mapped the
full contradiction surface. This file is the persisted findings.

## Two CRITICAL kernel contradictions (D6 fixed both)

### CRITICAL-1: D4 mode override absent from verdict path

**Files:** `arifosmcp/runtime/tools.py` line 2742 (verdict) vs 4844 (envelope)
**Introduced by:** D4 v2 (`bc6973802`)
**Status:** Fixed by D6 (`ef5ee9bba`)

The response envelope at line 4844 applied per-mode affordance overrides:
```python
"affordance_contract": _get_affordance_contract(
    tool_name, mode=out.get("mode") if isinstance(out, dict) else None
)
```

But `_compute_canonical_verdict` Step 6 did NOT:
```python
affordance = _get_affordance_contract(tool_name)  # no mode!
```

**Effect:** `arif_seal(mode=verify_chain)` showed `action_class=OBSERVE`
in the envelope but was over-gated as SEAL-class in the verdict — read-only
vault verify failed constitutional gate despite being a low-risk observation.

**Fix (D6):** Threaded `mode: str | None = None` through `_compute_canonical_verdict`
signature; Step 6 now reads `_get_affordance_contract(tool_name, mode=mode)`;
single call site at line 4463 passes `out.get("mode")`.

### CRITICAL-2: arif_memory write modes under-gated

**Files:** `arifosmcp/runtime/tools.py` line 2142 (overrides) vs 1657 (base)
**Status:** Fixed by D6 (`ef5ee9bba`)

`MODE_AFFORDANCE_OVERRIDES["arif_memory"]` declared only read modes:
`recall`, `inspect`, `attest`. Write modes (`remember`, `promote`, `revise`,
`forget`) fell through to the OBSERVE base contract (`mutation=False`,
`requires_lease=False`). Constitutional gate under-gated genuine mutations
on long-term memory substrate.

**Fix (D6):** Added 4 write-mode overrides with MUTATE-class contracts:
- `remember`: MUTATE, mutation=True, requires_lease=True
- `promote` / `revise` / `forget`: MUTATE, irreversible=True, requires_human_ack=True

## Five HIGH/MEDIUM contradictions (deferred)

| # | Severity | Contradiction | Where | Recommended fix |
|---|---|---|---|---|
| 1 | HIGH | Non-judge tools skip G gate | `verdict.py:197` G gate only fires in judge path; `_compute_canonical_verdict` (wrapper path) has no G gate | Thread `g_score` parameter into `_compute_canonical_verdict` |
| 2 | HIGH | `deployment_drift_status` honesty fix is itself undeployed | `_sr_drift` OR-merge in `rest_routes.py:3075` is in unreleased commits; deployed runtime has the buggy old version | Push D1–D5 to origin, then `make deploy-local` |
| 3 | MEDIUM | `arif_seal`/`arif_memory` apex_record uses variant name not canonical | `_apex_record` call site keyed by MCP tool name (variant) not canonical name | Key by `_LEGACY_ALIASES[tool_name]` |
| 4 | MEDIUM | workspace.yaml missing arifFlow + SIGNAL | `AAA/federation/workspace.yaml` predates their elevation | Add both repos to `canonical_repos` |
| 5 | MEDIUM | A-FORGE MCP surface: 4 SOTs disagree | live=44, contracts/mcp_surface.yaml=75, contracts/tools.yaml=15, federation-manifest.yaml=59, repos.yaml=85, organs.yaml=52 | Regenerate single mcp_surface.yaml via build-time script; make other SOTs derived |

## Federated-organ contradictions (not fixed this session)

| Organ | Contradiction |
|---|---|
| **A-FORGE** | Six SOT files disagree on tool count (44/75/15/59/85/52). `aaa-drift-check.py` cannot detect any of them — it doesn't read `contracts/mcp_surface.yaml` or `tools_sot.yaml`. |
| **AAA** | Two parallel authority-ceiling vocabularies: organs.yaml 6-band vs `organ_authority_ceilings.yaml` APEX §8 5-band. Per-organ disagreement (AAA: DISPLAY_ONLY vs T3_888_HOLD/LIMITED_MUTATE; WEALTH/GEOX: COMPUTE_ONLY vs OBSERVE_ONLY). |
| **SIGNAL** | Code declares 3 chambers (`signal_organ/chambers.py`); organs.yaml declares 6 chambers. Chambers 4-6 (`priority_classify`, `channel_route`, `governed_send`) are unimplemented. Also: port 18084 claimed by both SIGNAL and WELL Witness. |
| **FRAME** | Code has 7 chambers (added `rsi_verify`); organs.yaml declares 6. Undocumented at federation level. |
| **HERMES** | Port 18086 (organs.yaml) vs 18089 (workspace.yaml). |
| **arifFlow** | Not in workspace.yaml at all; only in organs.yaml. |

## RASA_DERITA / I-ARIF honest state (no contradiction)

- `RASA_DERITA.status: 888_HOLD`, `phase: PHASE3_GATES_WIRED+TRL_DESIGN_LANDED`,
  `enforcement_mode: PARTIAL_CODEPATH`. Schema and code both honestly report
  incomplete status. No fix needed.
- `ml_floors.ml_floors_enabled: false`, `ml_method: heuristic`,
  `ml_runtime_ready: false`, `ml_hold_state: disabled`. No flip point
  achievable in current state — requires: human ratify `RASA_WIRING_ENABLED=1`,
  SBERT dep available, graphiti embedding runtime verified.

## Deploy state at session end

| | Value |
|---|---|
| Source HEAD | `ef5ee9bba` (D6 + D5 + D4 v2 + 9 audit fixes) |
| Deployed git HEAD | `4d2f51a7` (stale marker) |
| Source `.py` files | Byte-identical to `/opt/arifos/app/` after D6 manual copy |
| `make deploy-local` | BLOCKED — 13 commits ahead of origin/main |
| Live service | `status=degraded`, `deployment_drift_status=drift_detected` |
| Next deploy step | `git push origin main && make deploy-local` |

## Methodology used (replay for future contradiction-mapping)

1. **3 parallel read-only recon agents** (delegate_task):
   - Agent 1: arifOS kernel verdict path, judge/vault/RASA/se_stage
   - Agent 2: AAA + A-FORGE federated registries (organs.yaml, workspace.yaml, mcp_surface.yaml, aaa-drift-check)
   - Agent 3: source vs deployed diff + deploy mechanism + drift logic
2. **Each agent ran independently in 3-5 minutes** — total wall time ~5 min
3. **Findings categorized by severity**: CRITICAL (active floor-enforcement break) → HIGH (governance lied to itself) → MEDIUM (federation hygiene)
4. **Fix highest-severity contradictions surgically**, in the same hot file
5. **8/8 smoke test** before declaring done — `uv run --no-sync python -c "..."` invoking the patched functions directly
6. **One patch, one day** — deferred the 5 HIGH/MEDIUM items to next session