# Federation Handoff — OpenCode ↔ arifOS Federation

> **Directive:** i-ARIF (2026-08-26) — make arifOS OpenCode a real AGI coding agent for the federation.
> **Operator:** 333-AGI Δ MIND
> **Session:** SEAL-eae656a15f4749f9

## Topology

```
┌─────────────────────────────────────────────────────────────┐
│  OpenCode runtime (this session, AAA warga FI-001)          │
│  ├── 6 agents: 333-AGI · 555-ASI · 555-ASI-VISION ·        │
│  │              888-APEX · image-analyzer · dispatch        │
│  ├── 11 skills (3 meta-mesa + 8 L1/L2)                     │
│  ├── 9 custom plugins (arifos-federation, judge-gate, ...)  │
│  ├── 4 custom tools (carry-forward, federation-health, ...) │
│  ├── 27 MCP servers (gated per-agent)                       │
│  ├── 18 providers (pool-routed)                             │
│  └── agent_state/ (per-agent persistent JSON)               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │  arif_init → arif_route → arif_judge → arif_seal
                            │  (8 constitutional verbs, F1-F13 floor enforced)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  arifOS federation (kernel :8088 + 5 organs)                │
│  ├── arifOS :8088 — constitutional kernel (JUDGE_ONLY)       │
│  ├── A-FORGE :7071 — execution shell (EXECUTE_AFTER_SEAL)   │
│  ├── arifFlow :7073 — metabolic nerve (FQ pulse)            │
│  ├── GEOX :8081 — earth intelligence (COMPUTE_ONLY)         │
│  ├── WEALTH :18082 — capital intelligence (COMPUTE_ONLY)    │
│  ├── WELL :18083 — vitality mirror (REFLECT_ONLY)           │
│  └── AAA :3001 — cockpit (DISPLAY_ONLY)                     │
└─────────────────────────────────────────────────────────────┘
```

## 8 Constitutional Verbs

OpenCode 333-AGI invokes these via arifOS MCP (`mcp_arifos_*`):

| Verb | arifOS tool | When |
|------|-------------|------|
| 1. INIT | `arif_init` | session boot — first action every session |
| 2. OBSERVE | `arif_observe` | evidence before claim |
| 3. THINK | `arif_think` | reasoning with mode=reason/plan/verify |
| 4. ROUTE | `arif_route` | intent → organ dispatch |
| 5. MEMORY | `arif_memory` | L1-L6 semantic recall/storage |
| 6. JUDGE | `arif_judge` | constitutional verdict |
| 7. FORGE | `arif_forge` | governed execution |
| 8. SEAL | `arif_seal` | immutable VAULT999 append |

## Per-Agent MCP Allowlist (orthogonal axes)

```
333-AGI     → arifos, aforge, arifflow, fed, geox, wealth, well, aaa,
               context7, firecrawl, brave-search, perplexity, exa, fetch,
               hermes, hermes-agent        (16 — full power)
555-ASI     → arifos, arifflow, hermes, context7,
               firecrawl, brave-search, perplexity   (7 — read-only research)
555-ASI-V → 555-ASI + vision lanes
888-APEX    → arifos, arifflow, hermes-agent, context7   (4 — judge + state)
dispatch    → arifos, arifflow, hermes-agent, aaa,
               geox, wealth, well                       (7 — A2A router)
image-analyzer → firecrawl only                          (1 — pure vision)
```

Redundant MCP servers denied via `experimental.policies`:
megamemory, graphiti, serena, repomapper, hindsight, capability-index,
semgrep, hostinger-vps, qdrant, supabase, sqlite, fed.

## Zen Mutations Applied (2026-08-26)

| ID | Mutation | ΔS Effect |
|----|----------|-----------|
| M-A1 | `watcher.ignore` (14 noise patterns) | file watch load ↓ |
| M-A2 | `compaction.model = kimi/kimi-for-coding-highspeed` | token cost ↓ |
| M-A3 | `compaction.reserved 10000 → 6000` | context reuse ↑ |
| M-A4 | `experimental.policies` (+12 deny rules) | tool surface ↓ |
| M-B | per-agent `mcp_*` allowlist (6 agents) | per-agent tool surface ↓ 50-80% |
| M-C1 | `opencode-meta-mesa` skill | meta-orchestration |
| M-C2 | `opencode-zen-router` skill | orthogonal routing |
| M-C3 | `opencode-agentic-state` skill | persistent agent memory |
| M-D1 | `agent_state/<agent>.json` (4 agents) | cross-session continuity |
| M-D2 | `command/probe-state.md` | introspection |
| M-D3 | this handoff doc | bidirectional sync clarity |

## Sync Protocol

```
OpenCode 333-AGI                          arifOS :8088
   │                                            │
   │  arif_init(mode="init", actor="ARIF")      │
   │ ─────────────────────────────────────────► │
   │ ◄─────────────────────────────────────────  │ session_id, sct
   │                                            │
   │  arif_observe(mode="vitals")               │
   │ ─────────────────────────────────────────► │
   │ ◄─────────────────────────────────────────  │ floors=13, drift=false
   │                                            │
   │  arif_route(intent="...", organ="geox")    │
   │ ─────────────────────────────────────────► │
   │ ◄─────────────────────────────────────────  │ routed to GEOX
   │                                            │
   │  geox_* (raw tool call)                    │
   │ ─────────────────────────────────────────► │
   │ ◄─────────────────────────────────────────  │ compute result
   │                                            │
   │  arif_seal(mode="receipt", ...)            │
   │ ─────────────────────────────────────────► │
   │ ◄─────────────────────────────────────────  │ sealed VAULT999
   │                                            │
   │  arifFlow ingest (FQ pulse)                │
   │ ─────────────────────────────────────────► │ :7073
   │                                            │
   │  forge_vault(mode="receipt")  [Lane B]     │
   │ ─────────────────────────────────────────► │
```

## When 333-AGI writes state

```bash
# Per-agent state update
python3 -c "
import json, time
state = json.load(open('/root/.config/opencode/agent_state/333-AGI.json'))
state['updated_at'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
state['missions_completed'] += 1
state['last_seen_session'] = 'SEAL-eae656a15f4749f9'
json.dump(state, open('/root/.config/opencode/agent_state/333-AGI.json', 'w'), indent=2)
"
```

Atomic write: tmp file then rename. F1 AMANAH.

## Failure modes

- If `arifOS :8088/health` returns 401/403 → service is UP, auth-gated (not DOWN).
- If `arifFlow :7073/health` returns FQ < 0.5 → ALL agents HOLD until FQ recovers.
- If a session's `carry-forward.json` has 5+ open loops → SEAL before starting new work.
- If `agent_state/<name>.json` >100KB → promote insights to SKILL.md, prune state.

DITEMPA BUKAN DIBERI ⚒️
