# arifOS Capability Architecture — The Seven Primitives

> **DITEMPA BUKAN DIBERI** — Ratified 2026-07-30 by Arif (F13 SOVEREIGN)
> **Doctrine:** "AGI doesn't need 128 tools. It needs 7 capabilities. Everything else is a specialised attachment or an ephemeral tool."
>
> **Architectural principle:** `Agent creates capability. arifOS governs authority. Never the reverse.`

---

## The Seven Capabilities

Every tool in the federation maps to exactly one capability primitive. Not 128 categories. Seven.

| # | Capability | What it does | arifOS verb | Organ owners |
|---|-----------|-------------|------------|-------------|
| 1 | **SENSE / READ** | Read web, files, databases, APIs, sensors, time, system state | `arif_observe` | GEOX, WEALTH, WELL, A-FORGE |
| 2 | **COMPUTE** | Calculate, run Python/shell, process data, simulate options | `arif_forge(compute)` | A-FORGE, GEOX, WEALTH |
| 3 | **MEMORY** | Remember, retrieve, correct, forget with provenance | `arif_memory` | arifOS, VAULT999, Supabase, Qdrant, Graphiti |
| 4 | **RESOLVE / ROUTE** | Determine which organ or tool is needed | `arif_route` | arifOS |
| 5 | **COMMUNICATE** | Interact with humans, agents, and external systems | `arif_forge(send)` | Hermes, A-FORGE |
| 6 | **ACT / FORGE** | Write files, call APIs, build code, mutate systems | `arif_forge` | A-FORGE |
| 7 | **VERIFY / GOVERN** | Test results, enforce permissions, rollback, audit, halt danger | `arif_judge`, `arif_seal` | arifOS, A-FORGE |

---

## Capability vs Tool Mapping

All 189 tools collapse into 7 capabilities:

### 1. SENSE / READ (62 tools)
```
arifOS:    arif_observe (all modes)
GEOX:      geox_basin, geox_deep_time_state, geox_stac_discover,
           geox_well_ingest, geox_well_view, geox_seismic_ingest,
           geox_map_layers_list, geox_map_scene_plan, geox_surface_status
WEALTH:    capital_market, capital_health, capital_registry, capital_ledger
WELL:      well_classify_substrate, well_machine_diagnose, well_trace_lineage
A-FORGE:   forge_search, forge_fetch (all variants), forge_probe,
           forge_filesystem_read/stat/search/tree, forge_journalctl,
           forge_netdata_*, forge_browser_*, forge_document_ingest,
           forge_vps_ports/services/cron, forge_registry/registry_status,
           forge_surface_audit/guard, forge_security_drift_scan
```

### 2. COMPUTE (31 tools)
```
GEOX:      geox_petrophysics, geox_seismic_compute, geox_geomechanics,
           geox_geological_model_generate, geox_gempy_implicit_3d,
           geox_subsurface_model, geox_thermal_maturity_history,
           geox_basin_backstrip, geox_lem_predict, geox_h3_spatial_index
WEALTH:    capital_primitive, capital_entropy, capital_diagnose,
           wealth_institutional_stress_index, wealth_cascade_model,
           wealth_governance_capacity, wealth_external_exploitation_detect,
           wealth_bid_surface
A-FORGE:   forge_chart, forge_shell_dryrun, forge_evaluate, forge_witness,
           forge_entropy_sweep, forge_predict, forge_verify_timeline
```

### 3. MEMORY (16 tools)
```
arifOS:    arif_memory (all 8 modes), arif_seal(mode=verify,ledger,audit)
A-FORGE:   forge_memory, forge_vault, forge_skillstore_read/write,
           forge_shell_ledger, forge_scar, forge_cool_drift/pattern
WELL:      well_trace_lineage
```

### 4. RESOLVE / ROUTE (4 tools)
```
arifOS:    arif_route, arif_think(mode=plan,plan_review)
A-FORGE:   forge_judge_proxy, forge_kernel
```

### 5. COMMUNICATE (6 tools)
```
A-FORGE:   forge_send_confirm, forge_transfer_confirm,
           forge_github_create_issue/pr, forge_browser_type
```

### 6. ACT / FORGE (48 tools — gated behind SEAL)
```
arifOS:    arif_forge
A-FORGE:   forge_execute, forge_execute_sealed, forge_shell,
           forge_filesystem_write/patch/move/delete,
           forge_git_commit, forge_stage, forge_synthesize,
           forge_sandbox_run/pause/resume, forge_docker,
           forge_skill, forge_register, forge_canonize,
           forge_vault(write), forge_seal, forge_tier_bind
```

### 7. VERIFY / GOVERN (22 tools)
```
arifOS:    arif_judge, arif_seal
A-FORGE:   forge_check_governance, forge_heart_critique, forge_approve,
           forge_scan, forge_fingerprint_check, forge_isomorphism_check,
           forge_runtime_verify, forge_visual_qa, forge_visual_seal,
           forge_wm_gaps/quality/stats, forge_lock, forge_policy
GEOX:      geox_falsify, geox_contradiction_scan
WELL:      well_validate_vitality, well_guard_dignity, well_check_repair
```

---

## The Eighth Capability: EPHEMERAL TOOL GENESIS

The seven primitives are the permanent substrate. But AGI needs one more thing:

> **The ability to create temporary tools on demand.**

This is not a new permanent verb. It's a set of modes under `arif_forge`:

```
arif_forge(mode=inspect_gap)       — Detect what capability is missing
arif_forge(mode=generate_ephemeral) — Create temporary tool in sandbox
arif_forge(mode=sandbox_test)      — Test tool against sample data
arif_forge(mode=invoke_ephemeral)  — Run tool with production data
arif_forge(mode=verify_output)     — Independently verify results
arif_forge(mode=propose_promotion) — Request permanent registration
arif_forge(mode=retire)            — Destroy temporary tool, clean sandbox
```

**Full contract:** `/root/AAA/contracts/EPHEMERAL_TOOL_GENESIS.md`

---

## The Tool Genesis Loop

```
1. DETECT gap        → "No existing tool can parse this format"
2. SEARCH existing   → arif_route: "does anything handle .xyz?"
3. REUSE if suitable → "Found partial — adapt or extend"
4. GENERATE ephemeral → arif_forge(mode=generate_ephemeral)
5. TEST in sandbox   → arif_forge(mode=sandbox_test)
6. GRANT minimum     → "Only needs: read /tmp/input, write /tmp/output"
7. EXECUTE           → arif_forge(mode=invoke_ephemeral)
8. VERIFY independent → arif_forge(mode=verify_output)
9. DESTROY temporary → arif_forge(mode=retire)
10. PROMOTE if worthy → Only if used 3+ times AND human-approved
```

**Key constraint:** `Agent creates capability. Agent never creates authority.`

---

## Autonomy Tiers for Ephemeral Tools

| Tier | Scope | Examples | Auto? |
|------|-------|----------|-------|
| **GREEN** | Sandboxed, reversible, no network | Parser, calculator, transformer, chart generator | AUTO |
| **YELLOW** | Read-only external, allowlist packages, scoped credentials | API adapter (no secret), format converter, local index | AUTO + LOG |
| **ORANGE** | Mutating, network access, persistent artifacts | Database migration script, deployment helper | ASK |
| **RED** | Authority amplification, credential creation, production mutation | API key generation, privilege escalation, kernel mutation | BLOCK |

---

## What This Architecture Eliminates

```
BEFORE                                  AFTER
──────                                  ─────
189 tools in flat catalog               7 capabilities + ephemeral forge
"Which tool do I use?"                  "Which capability do I need?"
GEOX: 33 overlapping endpoints          GEOX: SENSE + COMPUTE attachments
WEALTH: namespace drift                  WEALTH: SENSE + COMPUTE attachments
A-FORGE: 124 tools, no taxonomy         A-FORGE: ACT + ephemeral GENESIS
New format → wait for permanent tool    New format → agent builds parser now
```

---

*DITEMPA BUKAN DIBERI — Seven primitives. Infinite tools. Governed authority.*
*Ratified 2026-07-30 by Arif (F13 SOVEREIGN)*
