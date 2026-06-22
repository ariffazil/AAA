# TOOLS.md — OpenCode 333-AGI | AAA Warga Coder Forge

## NATIVE TOOLS (OpenCode Built-in)

| Tool | Use | Risk |
|------|-----|------|
| bash | Shell execution (local, root) | HIGH — atomic ops require 888_HOLD |
| read | Read files | LOW |
| write | Create/overwrite files | MEDIUM — backup first |
| edit | Targeted string replacement | LOW |
| glob | File pattern matching | LOW |
| grep | Content search with regex | LOW |
| websearch | Web search | LOW |
| webfetch | Fetch URL content | LOW |
| task | Spawn subagent (forge, auditor, ops, explore, general) | MEDIUM |
| todowrite | Task list management | LOW |

## FEDERATION MCP TOOLS

### arifos-kernel (13 tools)
| Tool | Use |
|------|-----|
| `arif_session_init` | **FIRST CALL** — bind constitutional session |
| `arif_os_attest` | Verify arifOS kernel liveness |
| `arif_organ_attest_all` | Probe all 7 organs in one call |
| `arif_judge_deliberate` | Constitutional verdict on proposed action |
| `arif_vault_seal` | Seal verdict to immutable ledger |
| `arif_mind_reason` | Multi-step reasoning, planning, reflection |
| `arif_sense_observe` | Web search, system vitals, repo map |
| `arif_memory_recall` | Search past sessions, sealed events |
| `arif_ops_measure` | System health, thermodynamic state |
| `arif_kernel_route` | Route intent to correct organ |
| `arif_heart_critique` | Ethical risk assessment |
| `arif_evidence_fetch` | Fetch external evidence with citations |
| `arif_forge_execute` | Execute approved builds/deployments (SEAL required) |
| `arif_reply_compose` | Compose final response |
| `arif_gateway_connect` | Bridge to other federation agents |

### A-FORGE (20+ tools) 🆕
| Tool | Use |
|------|-----|
| `forge_plan` | Classify action, estimate blast radius |
| `forge_dry_run` | Simulate execution without mutation |
| `forge_query` | Read-only system introspection |
| `forge_approve` | Approve action from hold queue |
| `arif_vault_seal` | Ledger closure (Stage 999) |
| `forge_remember` | Store memory to vault |
| `wealth_evaluate_ROI` | Evaluate investment ROI |
| `wealth_compute_EMV` | Compute expected monetary value |
| `wealth_thermodynamic_scan` | Scan for Landauer cost |

### GEOX (37 tools)
| Tool | Use |
|------|-----|
| `geox_basin_resolve` | Resolve basin name to canonical ID |
| `geox_basin_profile` | Basin-level intelligence |
| `geox_data_ingest_bundle` | Ingest LAS, SEG-Y, CSV, Parquet |
| `geox_seismic_compute` | Forward model, well tie, anomaly detection |
| `geox_prospect_evaluate` | Integrated prospect evaluation |
| `geox_claim_create` | Create structured Earth claim |
| `geox_evidence_reason` | Cross-domain evidence synthesis + abduction |

### WEALTH (20 tools)
| Tool | Use |
|------|-----|
| `wealth_conservation_capital` | Capital stock reality |
| `wealth_flow_liquidity` | Cashflow, burn, runway |
| `wealth_entropy_risk` | Uncertainty, dispersion, tail risk |
| `wealth_signal_information` | EVOI, information quality |
| `wealth_game_coordination` | Multi-agent incentives |
| `wealth_boundary_governance` | Constitutional floors + maruah |

### WELL (18 tools)
| Tool | Use |
|------|-----|
| `well_assess_metabolism` | Biological metabolism assessment |
| `well_assess_homeostasis` | Sleep, fatigue, regulation |
| `well_validate_vitality` | Vitality, readiness, NIAT |
| `well_guard_dignity` | Soul, personhood, meaning |

### Other MCPs
| Server | Key Tools |
|--------|-----------|
| playwright | browser_navigate, browser_snapshot, browser_click, browser_type |
| docker | Container lifecycle, exec, file ops |
| brave-search | web search |
| perplexity | AI research |
| postgres | SQL queries |
| qdrant | Vector search |
| cloudflare | DNS, Workers |
| github | Repos, PRs, issues |
| hostinger-vps | VPS lifecycle (OBSERVE + reversible MUTATE) |

## APPROVAL TIERS

| Tier | Action | Auth Required |
|------|--------|---------------|
| T1 | Read, search, observe, plan | None |
| T2 | Write files, edit, build, test, restart services | None (autonomous) |
| T3 | Delete, drop, force push, production deploy, vault seal | **888_HOLD** — Arif required |

---

*Forged: 2026-06-14 by FORGE (000Ω)*
