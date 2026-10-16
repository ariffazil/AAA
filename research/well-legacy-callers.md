# WELL legacy callers — branch `well/legacy-callers` (WELL side patched; cross-repo items below)

**Branch:** `well/legacy-callers` on `ariffazil/WELL.git` (HEAD `e27cba2`).
**WELL-side commit:** `fix(well-server): align DEPRECATED_TOOLS_MAP + _LEGACY_ALIASES_ALL with v2 surface window (2026-10-16 removal)` — 32 insertions, 25 deletions in `server.py`.
**Tests:** 497 passed, 23 skipped, 0 failed (143s on KVM8). Specifically `tests/test_deprecation_shims.py` 21/21.

## What was patched on the WELL side

Both `DEPRECATED_TOOLS_MAP` (the header middleware that fires `DEPRECATED_MOVED`) and `_LEGACY_ALIASES_ALL` (the registry's internal mirror) now agree with `well_v2/surface._DEPRECATION`:

- `deprecation_epoch`: 2026-09-16
- `removal_date`:     2026-10-16
- 6 entries unchanged in name + replacement; only the schedule moved.

The `well_registry_status(mode=…)` payload now reports the migration window with `removal_date=2026-10-16` and the `verdict` label correctly says NOT-`REGISTRY_DRIFT` inside the window.

## Cross-repo callers — OUTSIDE the WELL repo

Branch `well/legacy-callers` cannot edit these. They live in other repos and must be patched in their own branches. Locations (live, non-archive; ignore `.venv`, `node_modules`, `.git`, `forge_work`, `backups`, `xerj-data`):

| Caller | File:line | Patch needed |
|---|---|---|
| A-FORGE surface guard daemon | `A-FORGE/scripts/surface-guard-daemon.ts:48` | Remove `'well_readiness'` from `required_tools`. Keep `'well_validate_vitality'` and `'well_assess_homeostasis'`. Update `surface-guard-daemon.ts` only — the live-required list is what the surface guard probes. |
| AAA main agent card | `AAA/agents/main/agent-card.json:379` | Drop `"well_readiness"` from the `tools` list entry where it appears. |
| WEALTH makcikgpt card | `WEALTH/agent-cards/makcikgpt.json:309` | Drop `"well_readiness"` from the tools list. |
| A-FORGE docs/commentary | `A-FORGE/docs/archive/TRINITY_ECOSYSTEM_MAP.md:35` · `A-FORGE/docs/architecture/SOVEREIGN_INTELLIGENCE.md:415` · `A-FORGE/proto/isomorphism/GEOX-arifOS-VERDICT-MAP.md:98` | Doc-only — replace the prose reference from `well_readiness` to `well_validate_vitality`. |
| arifOS docs | `arifOS/docs/WELL_ARIFOS_CONTRACT.md:153` | Doc-only — `if well_readiness >= 0.6` becomes `if well_validate_vitality(mode='readiness').verdict >= 0.6`. |
| arifOS MCP internal state reader | `arifOS/arifosmcp/tools_canonical.py:796-882` | Reads `/root/WELL/state.json` (well_state file path) — NOT the legacy tool. Different shape. No patch needed; only the docstring references `well_state`. |

`.grok/`, `.codex-snapshots/`, `.qwen/`, `.hermes/`, `.cache/`, AAA `archive/`, AAA `agents/_lanes/_archive/`, AAA `agents/_superseded/`, `chron/data/episodes.jsonl`, `chron/data/verification_log.jsonl`, `memory/`, `wiki/`, `BACKUPS/` — all historical snapshots. The grep above intentionally excludes them. If any of these are restored to a live tree during 16/10 prep, they need a separate audit pass.

## Why no source code in other repos called `well_readiness` actively

The registered deprecation shim already returns `DEPRECATED_MOVED` for every legacy call. Hermes, OpenCode, and A2A agents that still send those calls will see a structured migration signal and the replacement. So **code-level callers**: zero, modulo agent-card / required-tool enumerations.

## Action recommended for the other repos

When ready:
1. A-FORGE — `surface-guard` refresh and one doc pass.
2. AAA — drop `well_readiness` from main agent card.
3. WEALTH — same for makcikgpt.
4. arifOS — doc patch + add a `tool_name` regex in MCP for `^well_(readiness|get_health|state|init|machine_state|assess_governance)$` returning a soft-redirect at the routing layer if the surface guard mis-orders a probe.

All reversible. None require a service restart; all are config + text.
