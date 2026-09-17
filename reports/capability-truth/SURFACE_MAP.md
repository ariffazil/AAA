# SURFACE MAP — APEX-777 Phase 3 · STEP 0 (333-AGI, 2026-09-18)

> Measured live 2026-09-17T20:03Z / 2026-09-18 04:03 MYT. Read-only. No seal.

## Canonical declaration
- **arifOS canonical surface = the systemd-managed local kernel** `127.0.0.1:8088` (truth node KVM8). Public `mcp.arif-fazil.com/mcp` is a Caddy route to the **same** backend — proven by tool-list parity below.
- **HERMES canonical surface = `hermes-mcp-server.service` `127.0.0.1:18087`**. Public `mcp.arif-fazil.com/hermes/mcp` routes to the same backend.
- Both public doors reach the same processes; parity is at tool-name level (8=8, 10=10). Deeper parity (schemas, enums, auth) = STEP 1b.

## Table

| | arifOS | HERMES |
|---|---|---|
| process | Main PID 2353611 (`python`) | hermes-mcp (`python3 -m hermes_mcp`) |
| systemd unit | `arifos.service` | `hermes-mcp-server.service` |
| port | `127.0.0.1:8088` | `127.0.0.1:18087` |
| import root | `/opt/arifos/current/venv/lib/python3.13/site-packages/arifosmcp` | `/root/HERMES` (WorkingDirectory) |
| entry | `from arifosmcp.runtime.__main__ import main; main()` | `/usr/bin/python3 -m hermes_mcp` |
| repo / commit | `/root/arifOS` @ `6491a4ab0` | `/root/HERMES` @ `41aa124` |
| version | dist-info `arifos-1!2026.9.6` | `2026.09.17.1` |
| tools (advertised) | **8** = KERNEL_ABI_8, missing=0 | **10** |
| handlers (dispatch) | 62 (CANONICAL_TOOL_HANDLERS) | — |
| public route | `mcp.arif-fazil.com/mcp` → `127.0.0.1:8088` (Caddy `handle /mcp*`; also `/sse*`) | `mcp.arif-fazil.com/hermes/*` → `127.0.0.1:18087` (strip_prefix `/hermes`) |
| public tool count | 8 (parity ✓) | 10 (parity ✓) |
| legacy aliases | 12/12 resolve (ghost set, hidden from discovery) | n/a |

## Tool lists (live)
- arifOS (both surfaces): `arif_forge, arif_init, arif_judge, arif_memory, arif_observe, arif_route, arif_seal, arif_think`
- HERMES (both surfaces): `hermes_claim_validate, hermes_contradiction_scan, hermes_counterstory_test, hermes_handoff_package, hermes_makcik_render, hermes_perspective_scope, hermes_qualia_boundary, hermes_registry_status, hermes_retrieve, hermes_uncreated_classify`

## Known divergences (measurement, not verdict)
1. **Stage ontology split-brain (arifOS):** `arif_judge` description says `KERNEL 666`; its own structured `meta.stage_code` says `888 JUDGE`; `constitutional_map.py` says 666 everywhere; `prompts/list` spine = `666 ⚖ DIGNITY · 888 🔒 JUDGE`. Same object, two ontologies. **888 HOLD — reconciliation is canonical-surface semantics.**
2. **Version string drift:** public GET card hardcodes `1!2026.8.2`; installed package = `1!2026.9.6`.
3. **Deployed-commit marker:** `/opt/arifos/releases/deployed-commit` = `eff8a59e` (lags HEAD by one — the ghost-alias commit; marker refreshes on next restart).
4. Enum-level (mode) truth = `NOT_MEASURED_V01` — capability_truth.py v0.2 must enumerate advertised mode enums vs handler dispatch.
