# A2A v1.0.0 Alignment — AAA Gateway
# ═══════════════════════════════════════
# Aligned: 2026-07-02 by FORGE (000Ω)
# Spec: https://a2a-protocol.org/latest/specification/
# Status: PHASE 2 COMPLETE — ~97% aligned

## Gap Analysis Summary

| Aspect | Official A2A v1.0 | AAA Current | Status |
|--------|-------------------|-------------|--------|
| Agent Card path | `/.well-known/agent-card.json` | ✅ Serves both `agent-card.json` + `agent.json` | ✅ OK |
| Agent Card schema | Standard fields + extensions | ✅ Official fields + `extensions[]` for governance | ✅ OK |
| JSON-RPC methods | `message/send`, `message/stream`, `tasks/get`, `tasks/list`, `tasks/cancel`, `tasks/subscribe` | ✅ All implemented | ✅ OK |
| Task states | `TASK_STATE_*` prefix | ✅ All states use `TASK_STATE_*` prefix | ✅ OK |
| HOLD → INPUT_REQUIRED | HOLD maps to INPUT_REQUIRED externally | ✅ `VERDICT_TO_A2A_STATE` mapping | ✅ OK |
| VOID → REJECTED | VOID maps to REJECTED externally | ✅ `STATE_TO_A2A_WIRE` mapping | ✅ OK |
| Part structure | `text`, `raw`, `url`, `data` | ⚠️ Phase 1: legacy `kind` kept for backward compat | ⚠️ Phase 3 |
| Extended Card | `supportsAuthenticatedExtendedCard: true` | ✅ Declared in capabilities | ✅ OK |
| Extended Card endpoint | `GET /.well-known/agent-card-extended.json` (auth) | ✅ Implemented | ✅ OK |
| Push notifications | `tasks/pushNotificationConfig/*` CRUD | ✅ 4 endpoints | ✅ OK |
| Streaming | `message/stream` → SSE | ✅ Implemented | ✅ OK |
| contextId | Server-generated grouping | ✅ + constitutional lineage mapping | ✅ OK |
| Multi-tenancy | `tenant` field in params | ✅ Supported, defaults to `personal` | ✅ OK |
| Security | Declared in Agent Card | ✅ Bearer + API key | ✅ OK |
| referenceTaskIds | Multi-turn refinement | ⚠️ Not yet implemented | ⚠️ Phase 3 |

## Architecture Insight (from Copilot analysis)

> **AAA = Constitutional Overlay, NOT A2A server.**
> Governance sits ABOVE transport, not replacing it.

```
A2A       → transports tasks
AAA       → transforms decisions
arifOS    → evaluates authority
A-FORGE   → executes
```

## Memory Federation (Zen Flow into AAA A2A State, 2026-07-05)

- Memory governed by kernel (arif_memory + L1-L6 + bands + provenance + canonical paths + no-bypass per FEDERATION_MEMORY.md + memory_store.py + AGENTIC_MEMORY_ROUTING.md).
- AAA observes + surfaces as federated AA state:
  - Redis: aaa:federation:memory:L1, L6, etc. (light snapshots)
  - GET /federation/memory on a2a-server (returns layers + flow + rule)
  - Updated AAA_FEDERATION_STATE.yaml with memory_layers + federated_memory_state
- Flow (zen): kernel → L1-L6 → AAA Redis + /federation/memory + YAML
- Bootstrap sets keys on start (after redis init).
- Exposed as A2A skill "federated-memory-query" in main agent card.
- Test: curl http://localhost:3001/federation/memory ; redis-cli KEYS 'aaa:federation:memory:*'
- All per "no over-engineer, kernel governs, AAA surfaces".

## Phase 2 Fixes (2026-07-02)

### 1. HOLD → INPUT_REQUIRED Wire Mapping
- Internal: `HOLD_888` (constitutional verdict)
- External: `TASK_STATE_INPUT_REQUIRED` (A2A wire format)
- Function: `VERDICT_TO_A2A_STATE` + `STATE_TO_A2A_WIRE`

### 2. VOID → REJECTED Wire Mapping
- Internal: `VOID` (constitutional violation)
- External: `TASK_STATE_REJECTED` (A2A wire format)

### 3. Agent Card — Official A2A v1.0
- Added `supportsAuthenticatedExtendedCard: true`
- Added `extensions[]` for constitution, federation, tenancy
- Added tenant extension with `supported_tenants` and `default_tenant`

### 4. contextId → Constitutional Lineage
- `contextLineage` Map tracks contextId → session_id + task_ids
- `registerContextLineage()` called on task creation
- Maps A2A contextId to arifOS session lineage

### 5. Multi-Tenancy Support
- `tenant` field accepted in `message/send` params
- Defaults to `personal`
- Stored in task metadata
- Filterable in `tasks/list`

### 6. Official Agent Card Wired
- Server loads `agent-card-official.json` first
- Falls back to legacy `agent-card.json` if not found

## Phase 3 Remaining (Future)
- Part structure migration (kind → direct text/raw/url/data)
- `referenceTaskIds` support in Message handling
- Test with official A2A Python SDK

## Constitutional Invariants Preserved

All 10 A2A invariants (I-1 through I-10) remain enforced.

## References

- Official A2A Spec v1.0.0: https://a2a-protocol.org/latest/specification/
- Agent Card spec: https://a2a-protocol.org/latest/specification/#8-agent-discovery-the-agent-card
- JSON-RPC binding: https://a2a-protocol.org/latest/specification/#9-json-rpc-protocol-binding

---

*DITEMPA BUKAN DIBERI — A2A is the civic layer between agents.*
