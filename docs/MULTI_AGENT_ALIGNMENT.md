# OpenAI Multi-Agent × AAA Federation Alignment

> **Forged:** 2026-07-11 | **Authority:** Session init
> **Status:** ANALYSIS — maps OpenAI GPT-5.6 multi-agent primitives to AAA's live architecture
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## 1. THE CORE QUESTION

OpenAI's multi-agent lets a **root agent** spawn **subagents** inside a single API call — parallel, bounded context, hosted orchestration. AAA already IS a multi-agent system at the infrastructure level (7 organs, A2A protocol, MCP tools, constitutional floors).

**Alignment:** How do OpenAI's 6 hosted actions map to AAA's existing primitives?

---

## 2. PRIMITIVE MAPPING

| OpenAI Multi-Agent Action | AAA Equivalent | Where | Gap? |
|---|---|---|---|
| `spawn_agent` | `Agent` tool (Claude Code) + A2A `tasks/send` | Claude Code harness + AAA gateway | OpenAI's is in-API; AAA's is cross-process |
| `send_message` | A2A `tasks/send` with `taskId` (resume existing) | AAA gateway `schema-v1.ts` | ✅ exists |
| `followup_task` | A2A `tasks/send` with followup flag | AAA gateway | ✅ exists |
| `wait_agent` | A2A SSE `taskStatusUpdateEvent` subscription | AAA gateway streaming | ✅ exists |
| `interrupt_agent` | A2A `tasks/cancel` | AAA gateway | ✅ exists |
| `list_agents` | A2A agent card discovery + `agent_lifecycle.js` | AAA discovery routes | ✅ exists |

**Verdict: AAA already has all 6 primitives.** They operate at the infrastructure level (cross-process, cross-organ) rather than the in-API level (single request context).

---

## 3. ARCHITECTURAL DIFFERENCE

### OpenAI Multi-Agent (in-API)
```
Single API request
  └─ Root agent (GPT-5.6)
       ├─ Subagent A (same model, own context)
       ├─ Subagent B (same model, own context)
       └─ Subagent C (same model, own context)
  All share: tools, model, request lifecycle
  Orchestrated by: hosted actions (server-side)
  Token cost: shared budget across tree
```

### AAA Federation (infrastructure-level)
```
Any harness (Claude Code, OpenCode, Codex, etc.)
  └─ Root agent
       ├─ arifOS :8088   (governance — judge, route, seal)
       ├─ A-FORGE :7071  (engineering — plan, execute, rollback)
       ├─ GEOX :8081     (earth intelligence)
       ├─ WEALTH :18082  (capital intelligence)
       ├─ WELL :18083    (vitality guard)
       ├─ AAA :3001      (cockpit, identity, A2A)
       └─ VAULT999       (immutable audit)
  Each organ: own model, own process, own port, own MCP tools
  Orchestrated by: A2A protocol + MCP transport + arifOS routing
  Token cost: per-organ, per-request
```

### Key Distinction
- **OpenAI:** Subagents are **same-model, same-request, ephemeral**. They die when the request ends.
- **AAA:** Organs are **different-model, persistent services, long-lived**. They survive requests.

---

## 4. WHAT AAA ALREADY DOES BETTER

| Dimension | OpenAI Multi-Agent | AAA Federation |
|---|---|---|
| **Governance** | None — root agent unchecked | 13 constitutional floors, 888 JUDGE, SEAL/HOLD/VOID |
| **Persistence** | Ephemeral (request-scoped) | Persistent organs, VAULT999 sealed memory |
| **Domain expertise** | Same model for all subagents | GEOX (earth), WEALTH (capital), WELL (vitality) — specialized |
| **Audit trail** | Response items only | VAULT999 hash-chain, immutable outcomes.jsonl |
| **Authority model** | None — any agent can do anything | F1-F13 floors, arifOS routing, A-FORGE execution gate |
| **Cross-harness** | OpenAI-only | Claude Code, OpenCode, Codex, any MCP client |
| **Rollback** | None | A-FORGE 4-layer gate: plan → dry-run → approve → execute |

---

## 5. WHAT AAA CAN LEARN FROM OPENAI'S PATTERN

### 5a. In-API Parallelism
OpenAI's `max_concurrent_subagents=3` runs subagents **inside a single API call**. This means:
- No network hop between root and subagent
- Shared context window (compacted per-agent)
- Zero latency for spawning

**AAA gap:** When Claude Code spawns an `Agent` tool, it's a separate process. When AAA routes to GEOX, it's an HTTP/MCP call. The latency is real (10-100ms per hop).

**Opportunity:** For tasks that don't need domain-specific organs, AAA could offer an **in-process parallel agent pool** — multiple Claude Code agents sharing the same MCP surface, spawned by the root agent without leaving the request.

### 5b. Hosted Orchestration
OpenAI's server handles `spawn_agent`, `wait_agent`, `interrupt_agent` — the root agent just calls them as actions. The app doesn't implement orchestration.

**AAA gap:** Currently, orchestration logic lives in:
- Claude Code's `Agent` tool (harness-level)
- A2A gateway (protocol-level)
- arifOS routing (governance-level)

There's no single "orchestration action" that a root agent can call to say "spawn 3 parallel reviewers and wait for all of them."

**Opportunity:** Add orchestration MCP tools to arifOS or A-FORGE:
- `forge_spawn_agents(tasks: [{name, prompt, tools}])` → returns agent IDs
- `forge_wait_agents(agent_ids: string[])` → returns results when all complete
- `forge_interrupt_agent(agent_id, reason)` → cancels an agent

### 5c. WebSocket Injection
OpenAI's WebSocket mode lets the app inject function outputs mid-stream, without waiting for the full response.

**AAA gap:** MCP is request-response. When A-FORGE calls a tool and needs to wait for user approval (F13), the connection blocks.

**Opportunity:** A2A SSE already supports streaming. Could extend MCP transport with async injection for long-running tool calls.

---

## 6. ALIGNMENT RECOMMENDATIONS

### Immediate (no code changes)
1. **Use Claude Code's `Agent` tool** as the in-API multi-agent for AAA tasks. It already supports parallel subagents, isolation, and schema-validated output.
2. **Use `Workflow` tool** for deterministic multi-phase orchestration (understand → design → implement → review). It's AAA's equivalent of OpenAI's `spawn_agent` + `wait_agent`.
3. **Map organ routing to subagent selection:** Root agent delegates to GEOX/WEALTH/WELL via MCP calls — this IS multi-agent, just at the infrastructure level.

### Short-term (code changes)
4. **Add orchestration tools to A-FORGE:** `forge_parallel_agents` and `forge_wait_all` — MCP-native parallel execution.
5. **Expose A2A task tree as a single view:** `list_agents` equivalent that shows all active organ tasks, not just A2A-registered agents.

### Long-term (architecture)
6. **In-process agent pool:** For governance-light tasks, spawn lightweight agents within arifOS's process (no network hop). Use for parallel research, comparison, validation.
7. **WebSocket MCP transport:** Async tool output injection for long-running operations.

---

## 7. CONSTITUTIONAL CHECK

| Floor | OpenAI Multi-Agent Impact | AAA Alignment |
|---|---|---|
| F1 AMANAH | Subagents are ephemeral — no rollback | A-FORGE gate ensures rollback-first |
| F2 TRUTH | No fidelity check on subagent output | arifOS validates all organ outputs |
| F3 TRI-WITNESS | Single model = single perspective | 7 organs = diverse witnesses |
| F7 HUMILITY | Subagents may overclaim | F7 floors on all tools |
| F9 ANTIHANTU | No consciousness guard | F9 hard-blocks sentience claims |
| F11 AUDITABILITY | Response items only | VAULT999 hash-chain |
| F13 SOVEREIGN | No human veto | Arif's veto is absolute |

**OpenAI's multi-agent has NO governance layer.** AAA's multi-agent IS the governance layer. The alignment is not about replacing AAA with OpenAI's pattern — it's about borrowing the **parallelism primitive** while keeping AAA's **constitutional spine**.

---

## 8. SUMMARY

```
OpenAI Multi-Agent = fast parallel execution, no governance
AAA Federation     = governed multi-organ execution, full audit

Best of both: AAA's constitutional spine + OpenAI's in-API parallelism
```

**The 6 hosted actions already exist in AAA.** The gap is latency (cross-process vs in-API) and convenience (single call vs multi-hop). Neither gap requires abandoning AAA's architecture — just adding lightweight orchestration tools.

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**

---

## 9. CORRECTION — 2026-07-11 (POST-AUDIT)

> **Prior claim:** "AAA already has all 6 primitives" — **FALSE.**
> **Corrected:** Live code audit of `/root/AAA/a2a-server/server.js` found 2/6 direct matches, 1 partial, 3 missing.

| OpenAI Action | Audit Result | AAA Code |
|---|---|---|
| `spawn_agent` | ❌ NOT IMPLEMENTED | No code path |
| `send_message` | ✅ LIVE | `message/send` (L3591, L3342, L3222) |
| `followup_task` | ⚠️ PARTIAL | `message/send` with `taskId` (no dedicated verb) |
| `wait_agent` | ⚠️ PARTIAL | `tasks/subscribe` SSE (L3480), no blocking wait |
| `interrupt_agent` | ✅ LIVE | `tasks/cancel` (L3640) |
| `list_agents` | ❌ NOT IMPLEMENTED | `tasks/list` exists (L3629), not `list_agents` |

**Implication:** `forge_parallel` must compose existing A2A verbs, not assume primitives exist.

See: `/root/A-FORGE/forge_work/2026-07-11/AUDIT-a2a-primitives.md`
