# Skill: agi_mcp_discover

**Agent:** 333-AGI
**Namespace:** agi_*
**Cluster:** TOOL
**Trigger:** Before loading MCP tools for a task
**Capability:** Return only the tools needed for a given task domain. Always-hot tools (kernel verbs + health) + on-demand tools (geoscience/capital/engineering/vault/meta/evidence). Capped at 8 total to protect context window.
**MCP tools underneath:** self (agi_mcp_discover is both caller and callee)
**Blast radius:** LOW — read-only query
**888 gate required:** No (read-only tool selection)

---

## §1 Identity

`agi_mcp_discover` is the progressive MCP tool loader for 333-AGI (Δ MIND).

The 333-AGI runtime normally sees ~49 A-FORGE tools + GEOX + WEALTH + WELL + arifOS in a single MCP context. Loading all of them before the model has even read the user request blows the context window and forces the agent to relearn the same surface on every task.

This skill enforces a **hard cap of 8 tools per MCP context** (F4 CLARITY). Seven tools are always hot (kernel verbs + health + vitality + self). One domain — selected by `classify_intent()` — gets the rest of the room.

## §2 Interface

```python
from agi_mcp_discover import discover, classify_intent

# What domain does this user want?
domain = classify_intent("Compute NPV for the Malay CCS deal")
# → "capital"

# Load only the tools we actually need.
tools = discover(domain)
# → 7 always-hot + 6 on-demand = 8 (capped)
```

| Symbol            | Type                          | Purpose                                              |
|-------------------|-------------------------------|------------------------------------------------------|
| `ALWAYS_HOT`       | `list[str]`                  | 7 tools loaded on every task                         |
| `ON_DEMAND`        | `dict[str, list[str]]`       | Domain → on-demand tool set                          |
| `MAX_TOOLS`        | `int = 8`                    | Hard cap (F4 CLARITY)                                |
| `discover(domain)` | `(str, str \| None) → list[str]` | Domain-keyed tool loader, capped at MAX_TOOLS        |
| `classify_intent(s)` | `(str) → str`               | Keyword router: user intent → task domain            |

## §3 Routing Rules (priority order)

`classify_intent()` matches the first hit. Order matters:

1. `geoscience` — basin, geology, seismic, petrophysics, well, prospect
2. `capital`    — npv, irr, emv, capital, invest, valuation, stock
3. `engineering` — code, build, deploy, shell, docker, git, test
4. `vault`      — vault, seal, ledger, archive
5. `evidence`   — search, research, find
6. `meta`       — fallback (agent_search, skill_load, agent_status)

## §4 Always-Hot Tools (7)

| Tool                       | Purpose                                      |
|----------------------------|----------------------------------------------|
| `arif_init`                | Bind cognitive runtime to active session     |
| `arif_observe`             | OBSERVE-stage verb                           |
| `arif_think`               | THINK-stage verb                             |
| `forge_probe`              | Federation organ liveness                    |
| `forge_status`             | Jobs/leases/agents overview                  |
| `well_assess_homeostasis`  | Vitality gate (Floor compliance)             |
| `agi_mcp_discover`         | Self-reference (this skill)                  |

## §5 On-Demand Domains

| Domain        | Tools added                                                                   |
|---------------|-------------------------------------------------------------------------------|
| geoscience    | 7 GEOX tools (basin, seismic, petrophysics, prospect, deep time, well ingest) |
| capital       | 6 WEALTH tools (npv, irr, emv, runway, stock, diagnose)                       |
| engineering   | 6 A-FORGE tools (shell, git, docker, fs read/write, health check)             |
| vault         | 3 vault tools + `forge_vault_seal`                                            |
| meta          | 3 (agent_search, skill_load, agent_status)                                    |
| evidence      | 3 (forge_research, forge_minimax_search, forge_docs_lookup)                   |

## §6 Hard Rules

1. **MAX_TOOLS = 8 is a hard cap.** Never soft-cap. Truncate, do not paginate.
2. **ALWAYS_HOT is non-negotiable.** Every context includes the 7 hot tools.
3. **Unknown domain → ALWAYS_HOT only.** No silent fallback to `meta`.
4. **classify_intent is deterministic.** No LLM call. No hidden state.

## §7 Test Surface

```bash
PYTHONPATH=/root/AAA/agents/_lanes/333-AGI/runtime \
  python3 -m unittest discover -s /root/AAA/agents/_lanes/333-AGI/runtime/tests -v
```

Coverage: domain classification, hard cap, always-hot invariants, no-duplicate keys, intent param forward-compat.

## §8 Out of Scope

- Not a tool executor. `agi_tool_invoke` (already in agent-card) owns that.
- Not a planner. `planner/` (sibling skill) owns DAG construction.
- Not a memory synthesizer. 555-ASI owns that.

---

*Phase 4b · AAA entropy-reduction roadmap · F13 SOVEREIGN.*
