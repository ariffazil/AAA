# CODING AGENT FEDERATION — Unified Swarm Reference

> **Scope:** All coding agents on `af-forge` VPS  
> **Root agent config:** `ROOT_AGENT_CONFIG.yaml`
> **Canonical registry:** `AAA_AGENTS_REGISTRY.json`  
> **Capability index:** `registries/CAPABILITY_INDEX.json` (97 tools)  
> **Last updated:** 2026-06-05  
> **DITEMPA BUKAN DIBERI**

---

## The Swarm at a Glance

| Agent | Native MCP | Servers | Integration | Risk |
|-------|-----------|---------|-------------|------|
| **Kimi Code** | ✅ 9 servers | arifOS, WEALTH, WELL, minimax, github, brave-search, meyhem, **playwright-mcp**, **capability-index** | MCP native | YELLOW |
| **Claude Code** | ✅ 10 servers | arifOS, WEALTH, WELL, minimax-media, minimax-code, github, brave-search, meyhem, **playwright-mcp**, **capability-index** | MCP native | YELLOW |
| **Continue CLI** | ✅ 17 servers | Full federation + tavily, exa, chrome-devtools, **capability-index** | MCP native | YELLOW |
| **OpenCode** | ✅ 18 servers | arifOS, A-FORGE, GEOX, WEALTH, WELL, GitHub, Context7, Playwright, Docker, web/search/data MCPs | MCP native | YELLOW |
| **Copilot** | ✅ 8 servers | arifOS, WEALTH, WELL, github, brave-search, meyhem, playwright, **capability-index** | IDE MCP | GREEN |
| **Codex** | ⚠️ Ready | Configured for 8 servers (experimental) | MCP config ready | YELLOW |
| **Aider** | ❌ No | Python fallback | A-FORGE bridge | YELLOW |
| **Antigravity / Gemini** | ❌ No | Python fallback | A-FORGE bridge | YELLOW |

**Total swarm size:** 8 agents  
**Total unified tool surface:** 97 tools across 9 MCP servers  
**New scaffolds added today:** Capability Index, Playwright MCP, NATS Agent Bridge, Evals Harness

---

## Integration Modes

### MCP-Native (Kimi, Claude, Continue, OpenCode, Copilot)
These agents connect directly to MCP servers via stdio, SSE, or HTTP. They discover tools through the capability index and invoke them natively.

### MCP-Ready (Codex)
MCP config file created at `.codex/mcp.json`. Will activate automatically when Codex CLI adds MCP support.

### Bridge/Fallback (Aider, Antigravity)
No MCP support. Use Python subprocess or A-FORGE pattern detection to access federation tools.

**Example fallback:**
```bash
cd /root/arifOS && PYTHONPATH=core python3 -c "
from capability_index.store import CapabilityStore
for r in CapabilityStore().search('calculate zakat', 3):
    print(r.tool_name, r.server)
"
```

---

## Capability Access Patterns

| Pattern | MCP-Native Agents | Bridge Agents |
|---------|-------------------|---------------|
| **Discover tools** | `capability_search` / `capability_select` MCP tools | Python import `CapabilityStore.search()` |
| **Browse web** | `playwright-mcp` server | Python `playwright.sync_api` directly |
| **Publish telemetry** | `agent_bridge.publisher` Python module | Same Python module |
| **Run evals** | `pytest evals/` | `pytest evals/` |
| **Governance check** | `arif_judge_deliberate` MCP tool | `arif_judge_deliberate` via A-FORGE |

---

## Shared Invariants

1. **One Constitution:** All agents bound by F1-F13, adjudicated by arifOS 888_JUDGE
2. **One Audit Trail:** VAULT999 logs all significant actions, regardless of originating agent
3. **One Capability Space:** 97 tools indexed in Qdrant, searchable by all agents
4. **One Memory Bus:** NATS JetStream `agent.memory` — learnings shared across swarm
5. **No Self-Authorization:** No agent can SEAL or authorize destructive actions alone

---

## Router Recommendations (A-FORGE Phase 4)

| Task Type | Best Agent | Why |
|-----------|-----------|-----|
| Debug complex algorithm | **Kimi** | SOTA debugging, large context |
| Architecture / safety review | **Claude** | Constitutional awareness, long reasoning |
| Quick inline completion | **Copilot** | IDE-native, lowest latency |
| Python/data pipeline | **Codex** | OpenAI function calling, Python strength |
| Autonomous health audit | **Continue** | Headless, systemd, 17 tools |
| Skill-driven automation | **OpenCode** | 40+ skills, subagent delegation |
| Multi-file refactor with git | **Aider** | Git-integrated, diff review |
| Google ecosystem task | **Antigravity** | Gemini backend, rapid generation |

---

## Files Changed Today

| File | Change |
|------|--------|
| `agents/kimi-code/agent-card.json` | native_mcp: true, +2 servers |
| `agents/claude-code/agent-card.json` | +8 new federation servers |
| `agents/copilot/agent-card.json` | native_mcp: true, +6 servers |
| `agents/codex/agent-card.json` | mcp_ready: true, config path added |
| `agents/continue-cli/agent-card.json` | +1 server (capability-index) |
| `agents/opencode/agent-card.json` | +1 server (capability-index) |
| `agents/antigravity/agent-card.json` | fallback_commands added |
| `agents/aider/agent-card.json` | **NEW** |
| `agents/gemini/agent-card.json` | **NEW** |
| `registries/CAPABILITY_INDEX.json` | **NEW** — 97 tools |
| `schemas/capability-card.schema.json` | **NEW** |
| `schemas/task-envelope.schema.json` | **NEW** |
| `AGENT_BRIDGE_ACCESS.md` | **NEW** — universal access guide |
| `UNIFIED_AGENT_ARCHITECTURE.md` | **NEW** — master document |
