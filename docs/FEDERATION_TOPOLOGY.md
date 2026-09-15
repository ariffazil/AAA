# Federation Topology — auto-generated map

> **AUTO-GENERATED — do not hand-edit.** Regenerate with
> `/opt/arifos/venv/bin/python /root/scripts/federation_topology_gen.py`.
> Everything below is read from live `/health` probes and live MCP
> handshakes at generation time. An organ that is down appears as down.

Generated: **2026-09-15T15:16:52+00:00** (UTC) · Status: DRAFT (evidence map, not canon)

## Live surfaces

| Port | Organ | Declared state | Authority | MCP tools | Identity | Wired: Hermes / 1mcp |
|---|---|---|---|---|---|---|
| 8088 | arifOS kernel | healthy | SOVEREIGN | 8 | ARIFOS MCP | arifos / arifos |
| 7072 | A-FORGE MCP | healthy | 777_FORGE | 126 | A-FORGE-MCP | — / — |
| 7074 | FED | healthy | — | 7 | FED | fed / — |
| 8081 | GEOX | healthy | 555_COMPUTE_ONLY | 31 | geox-unified | geox / geox |
| 18082 | WEALTH | healthy | 555_COMPUTE_ONLY | 11 | 4c31dad39a2ce9a4fcb3baa14c5f | wealth / wealth |
| 18083 | WELL | degraded | REFLECT_ONLY | 31 | well-mcp | well / well |
| 18085 | FRAME | ok | — | 0 | frame | — / — |
| 18090 | minimax-media bridge | no /health | — | 0 | — | — / minimax-media |
| 18091 | minimax-code | no /health | — | 0 | — | — / minimax-code |
| 3001 | AAA daemon | healthy | DISPLAY_ONLY | 0 | f909eab007954d345edd20ecad73 | — / — |
| 4000 | Langfuse | no /health | — | 0 | — | — / — |
| 8083 | kabarkan? | pass | — | 0 | — | — / — |

## Tool inventory (measured, not assumed)

- **:8088 arifOS kernel** — 8 tools
  - `arif_init, arif_observe, arif_think, arif_route, arif_memory, arif_judge, arif_forge, arif_seal`
- **:7072 A-FORGE MCP** — 126 tools
  - `forge_session_init, forge_health_check, forge_heart_critique, forge_check_governance, forge_execute, forge_judge_proxy, forge_transfer_confirm, forge_send_confirm, forge_vault, forge_wealth, forge_docsgpt, forge_journalctl` …
- **:7074 FED** — 7 tools
  - `fed_route, fed_status, fed_probe, fed_contrast, fed_health, fed_classify, fed_report_latency`
- **:8081 GEOX** — 31 tools
  - `geox_geomechanics, geox_glof_cascade_initialize, geox_glof_cascade_step, geox_glof_cascade_phase, geox_glof_cascade_inverse, geox_glof_cascade_metabolize, geox_glof_cascade_mcmc_inverse, geox_glof_cascade_propagate, geox_paleobiodb_query, geox_well_ingest, geox_well_qc, geox_petrophysics` …
- **:18082 WEALTH** — 11 tools
  - `capital_primitive, capital_health, capital_diagnose, capital_market, capital_ledger, capital_registry, capital_entropy, wealth_judge_handoff, capital_indicator, capital_backtest, capital_entry_plan`
- **:18083 WELL** — 31 tools
  - `well_log_intake, well_log_recovery_event, well_log_substance, well_inject_biometric, well_observe_machine, well_observe_federation_thermal, well_observe_scar_load, well_observe_drift_field, well_observe_evidence_backlog, well_classify_machine_state, well_attest_to_kernel, well_handoff_dignity_to_arifos` …
- **:18085 FRAME** — no MCP tool list (ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception))
- **:18090 minimax-media bridge** — no MCP tool list (ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception))
- **:18091 minimax-code** — no MCP tool list (ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception))
- **:3001 AAA daemon** — no MCP tool list (ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception))
- **:4000 Langfuse** — no MCP tool list (ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception))
- **:8083 kabarkan?** — no MCP tool list (ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception))

## Wiring gaps

- In 1mcp but **not** wired to Hermes (11): docker, github, hermes, hostinger-vps, meyhem, minimax-code, minimax-media, perplexity, qdrant, sequential-thinking, supabase
- In Hermes but **not** in 1mcp (8): datadog, fed, firecrawl, hermes-social, hugging_face, zai_reader, zai_search, zai_vision

## Known blind spots of this generator

- A port that is not in the candidate list above is invisible here.
- stdio-only MCP servers (no HTTP port) cannot be probed this way;
  their truth lives in the wiring configs only.
- `declared_state` is what the organ says about itself. It is not a verdict.

<!-- sha256 of companion json: computed after write -->
