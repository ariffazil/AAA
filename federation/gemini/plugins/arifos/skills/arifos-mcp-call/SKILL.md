---
name: arifos-mcp-call
description: Invoke arifOS constitutional MCP tools (000-999 pipeline, F1-F13 enforced). Use to call arif_* tools on the arifos_remote MCP server.
user-invocable: true
---

# arifOS MCP Caller — Constitutional Anchor-First

**Runtime:** 42-tool constitutional kernel
**Requirement:** `init_anchor` MUST be called before `arifOS_kernel`
**Floors:** F1-F13 enforced via sBERT ML layer
**MCP Server:** `arifos_remote` at `https://mcp.arif-fazil.com/mcp`

## Constitutional Tool Contract

| Stage | Tool | Purpose |
|-------|------|---------|
| **000_INIT** | `arif_session_init` | **REQUIRED FIRST** — Bootstrap session, bind actor_id, risk tier |
| **111_SENSE** | `arif_sense_observe` | Observe environment, gather signals |
| **333_MIND** | `arif_mind_reason` | Full pipeline reasoning |
| **555_HEART** | `arif_heart_critique` | Constitutional critique |
| **777_OPS** | `arif_forge_execute` | Governed execution |
| **888_JUDGE** | `arif_judge_deliberate` | Cross-check decisions |
| **999_SEAL** | `arif_vault_seal` | Persist to VAULT999 |

## Tool Naming Convention

All arifOS MCP tools follow: `arif_<noun>_<verb>`

```bash
# Available via MCP (arifos_remote server):
arif_session_init       # 000 INIT
arif_sense_observe       # 111 SENSE
arif_evidence_fetch      # evidence retrieval
arif_mind_reason         # 333 MIND
arif_heart_critique      # 555 HEART
arif_kernel_route        # pipeline routing
arif_reply_compose       # compose reply
arif_memory_recall       # memory
arif_gateway_connect     # gateway
arif_judge_deliberate    # 888 JUDGE
arif_vault_seal          # 999 SEAL
arif_forge_execute       # 777 OPS
arif_ops_measure         # ops metrics
arif_stack_health_probe  # stack health
arif_organ_consensus     # organ consensus
arif_scan_local_instructions  # scan local
arif_session_budget      # budget check
```

## F13 Sovereignty Handling

If any tool returns `requires_human: true` or `verdict: "HOLD_888"`:
- **STOP execution immediately**
- **Prompt Arif for confirmation**
- **Do not proceed until explicit approval**

Exit code 88 = HOLD_888 (sovereign approval required).

## Rail Routing

- Read/Analyze/Dry-run → Rail A (local `arifos_local` at localhost:8080)
- Vault Seal / 888 JUDGE / Production Forge → Rail B (remote `arifos_remote` at mcp.arif-fazil.com)

## Degraded Mode

If Rail B unreachable:
```
⚠️ [DECOUPLED GOVERNANCE — READ-ONLY MODE]
```
Queue VAULT999 payloads locally to `vault_pending.jsonl`.

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
