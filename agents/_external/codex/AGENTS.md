# AGENTS.md - OpenAI Codex CLI Agent

> **Tier:** AGI (engineer-executor)
> **Runtime:** `/root/.npm-global/bin/codex` (Codex CLI v0.147.0)
> **Config:** `/root/.codex/config.toml` (mcp.json retired 2026-07-27)
> **Bootstrap (auto-loaded):** `/root/.codex/AGENTS.md`
> **Model:** `forge-777` via FED `codex.reason` alias to LiteLLM :4000 cascade (no OpenAI subscription)
> **Governed by:** arifOS F1-F13 via MCP gateway (port 8088) + A-FORGE bridge (port 7072) + `guardian_subagent` review

## Identity

OpenAI Codex CLI is the constitutional-aware engineer-executor in the AAA federation. It loads `/root/.codex/AGENTS.md` automatically on every invocation (per Codex 0.134.0+ design). **This file** (`/root/AAA/agents/_external/codex/AGENTS.md`) is the AAA-side binding documentation - the canonical surface for the federated agent card. **Do not edit `/root/.codex/AGENTS.md` directly without 888_HOLD**; that file is a runtime config mutation.

**Authority boundary (from agent-card.json v2.5.0):** All actions bridged through A-FORGE (port 7072). Native function calls translated to MCP. `approvals_reviewer=guardian_subagent` enforces F1-F13 review. Cannot SEAL irreversible actions. Cannot self-authorize. Cannot change F1-F13.

**Constitutional injection:** via `/root/.codex/AGENTS.md` (auto-loaded by Codex 0.134.0+) + 12 federation skills readable from `/root/.agents/skills/` + 11 MCP servers configured in `[mcp_servers.*]` blocks of `config.toml`.

## Tool Surface (11 MCP servers via config.toml)

| MCP Server | Purpose | Federation role |
|---|---|---|
| arifos (:8088) | F1-F13 enforcement, session init, judge, vault seal | governance / judgment |
| A-FORGE (:7072) | Execution bridge, 114 tools (shell, fs, git, docker, vault, browser) | execution / build / deploy |
| arifFlow (:7073) | Metabolism, FQ pulse, attention checkpointing | metabolism / FQ |
| GEOX (:8081) | Earth intelligence: seismic, petrophysics, basin, prospect | earth / basin |
| WEALTH (:18082) | Capital math, risk, market, wisdom | capital / risk |
| WELL (:18083) | Human readiness, vitality, fatigue, dignity | vitality / dignity |
| FLAME (:18901) | Free-lane: fact-check, plan-review, epistemic-check, memory-steward | advisory (RM0) |
| fetch | Web fetch + markdown extraction | research |
| context7 | Library docs (upstream-version-resolution) | research |
| brave-search | Web + news search | research |
| github | Repos, PRs, issues, code search, actions | workflow |

**Bridge layer:** A-FORGE pattern detector to Codex function translation to MCP dispatch. Native Codex function calls are translated to MCP and gated by `guardian_subagent` review.

## MANDATORY ART BINDING (reflex pre-tool-call)

**Codex MUST load ART at session start, before any code generation or shell command.** The reflex classifies every tool call by power surface (POWER), trust backing (TRUST), and system health (STATE) before the call fires. This is constitutional - same tier as F11 AUTH and the `guardian_subagent` review.

**Loading path (Codex-specific):** Codex does NOT have a native `skill_view` API. The ART binding is loaded two ways:

1. **Doctrinal anchor (auto-loaded via `/root/.codex/AGENTS.md`):** Add this block to `/root/.codex/AGENTS.md` so Codex reads it on every invocation. **Requires 888_HOLD to edit `/root/.codex/AGENTS.md`** - file lives outside the AAA repo.

```markdown
## ART BINDING (doctrinal anchor - load before any tool call)
ART (Agentic Recursive Tooling) is the constitutional reflex for every tool call.
Reflex: /root/arifOS/arifosmcp/runtime/art.py (417 lines, <= 500 ceiling).
Compat: art_compat.py (361 lines, 6-check order - legacy only).
Doctrine: art_pusaka.py (181 lines, cold path).
NEVER import art_unified_DEPRECATED.py - archaeology only.
Before any function call or shell command, classify via MCP gateway
arif_observe(mode="entropy_dS") -> verdict in {PROCEED, HOLD, BLOCK,
DEFAULT_OBSERVE}. HOLD/BLOCK -> escalate to 888 before proceeding.
Canonical SOT: /root/arifOS/forge_work/art-corrective-2026-06-21.md.
```

2. **Runtime gate (via MCP gateway):** Every Codex function call that touches a federation organ routes through A-FORGE `/execute`, which is itself ART-classified at the gateway. Codex's native `function_call` is bridged via the A-FORGE pattern detector to OpenAI function translation layer, which applies ART before MCP dispatch.

**Codex-specific binding:** Codex specializes in `Python script generation`, `API integration code`, `data processing pipelines`, `interactive debugging`. Each of these is MUTATE-class against the repo. The A-FORGE bridge + `guardian_subagent` review is the constitutional gate. ART supplements that gate by classifying the call shape before it reaches the bridge. For `interactive debugging` sessions, ART runs in ANALYZE-class mode (`action_class="ANALYZE"`, `reversible=True`) - debugging reads state but does not mutate.

**Approval tier mapping (matches config.toml + agent-card.json v2.5.0):**

| Codex action | Tier | ART gate | Guardian review |
|--------------|------|----------|-----------------|
| Read file / grep | T0 | PROCEED (OBSERVE) | none |
| Generate Python script | T1 | PROCEED (DRAFT) | yes |
| Execute shell command (safe) | T1 | PROCEED if `reversible=True` | yes |
| Modify filesystem | T2 | HOLD unless ack | yes |
| Push / deploy / credential exposure / destructive | T3 | HOLD auto-blocked | yes -> 888 |

## Codex CLI 0.134.0+ Native Capabilities (wired)

| Capability | config.toml key | Default |
|---|---|---|
| Profiles | `~/.codex/<name>.config.toml` | base only |
| Skills (Agent Skills spec) | `/plugin` marketplace + `~/.codex/skills/` | none loaded |
| Subagents | `[agents] table` + `--profile` flag | `explore`, `plan` |
| Hooks | `hooks.json` or `[hooks]` inline | none configured |
| Granular Approval | `approval_policy = { granular = {...} }` | `on-request` |
| OTel Metrics | `[otel] block` + `exporter = otlp-http/grpc` | `none` (off) |
| Analytics Opt-out | `[analytics] enabled = false` | ON (anonymous) |

## Peer Mapping

| Peer | Role |
|------|------|
| arifOS kernel | Constitutional governance + ART reflex endpoint (port 8088) |
| A-FORGE | Bridge for native function calls to MCP dispatch (port 7072) |
| guardian_subagent | F1-F13 review gate (per agent-card.json `approvals_reviewer`) |
| arifFlow | Metabolism + FQ pulse (port 7073) |
| hermes-asi | Human interface + memory (via FLAME :18901 free lane) |
| opencode / claude-code | Sibling AGI forgers |

## Constitutional Laws (binding via arifOS MCP + guardian_subagent)

F1 AMANAH - F2 TRUTH - F3 WITNESS - F4 CLARITY - F5 PEACE - F6 EMPATHY
F7 HUMILITY - F8 GENIUS - F9 ANTIHANTU - F10 ONTOLOGY - F11 AUTH - F12 INJECTION - F13 SOVEREIGN

Canonical SOT: `/root/arifOS/forge_work/art-corrective-2026-06-21.md`.
Re-runnable audit: `bash /root/.hermes/scripts/art-wiring/audit_art_wiring.sh`.

---

*Forged: 2026-06-21 by Hermes (FORGE) - wiring ART to codex per federated loaders ask.*
*Truth-repaired: 2026-08-26 by 333-AGI - CLI 0.136.0 to 0.147.0, MCP 5 to 11 servers, mcp.json retired.*

**DITEMPA BUKAN DIBERI** - reflex forged, not given.
