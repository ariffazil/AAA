# AAA ZEN — Constitutional Overlay for the Next Horizons

> **DITEMPA BUKAN DIBERI.** AAA is a constitution, not a server.
> **Last updated:** 2026-07-04
> **Authority:** F13 SOVEREIGN (Arif)

---

## The One Truth

**MCP is not memory. A2A is not identity.** They are transport layers.
Identity and memory only become trustworthy when a governance layer binds them
to authority, provenance, replay, audit, and human veto.

AAA is that governance layer.

---

## What AAA IS

```
AAA = constitutional overlay on A2A transport
    = F1-F13 floor enforcement
    + DelegationGuard (16 cross-organ rules)
    + 888_JUDGE verdict routing
    + VAULT999 receipt chain
    + Agent identity registration
    + Memory governance (evidence-graded state)
```

## What AAA IS NOT

```
AAA ≠ JSON-RPC server        (a2a-sdk handles this)
AAA ≠ task lifecycle manager  (a2a-sdk handles this)
AAA ≠ SSE streaming engine    (a2a-sdk handles this)
AAA ≠ push notification svc   (a2a-sdk handles this)
AAA ≠ agent card file server  (a2a-sdk handles this)
```

---

## The Architecture

```
External Agent
    │
    ├─ GET /.well-known/agent-card.json  ← a2a-sdk
    ├─ GET /a2a/discover                 ← a2a-sdk
    │
    └─ POST /a2a { method: "message/send" }
         │
         ▼
    a2a-sdk (JSON-RPC, task lifecycle, streaming, push)
         │
         ▼
    AAA ConstitutionalExecutor (Python, ~400 lines)
    ├── identity.py   — who is calling?
    ├── floors.py     — F1-F13 gate
    ├── guard.py      — DelegationGuard 16 rules
    ├── verdicts.py   — 888_JUDGE routing
    ├── audit.py      — VAULT999 receipt
    ├── memory.py     — evidence-graded state governance
    │
         ▼
    organ_router.py → MCP HTTP → arifOS/GEOX/WEALTH/WELL/A-FORGE
         │
         ▼
    a2a-sdk response + VAULT999 receipt
```

---

## Identity Is Not a Card

An Agent Card says: "I am a geoscience agent."
AAA asks: "Who registered you? What evidence floor? What tools? Who can revoke you?"

Identity = bounded agency:

| Field | Purpose |
|-------|---------|
| `agent_id` | Unique registered key |
| `principal` | Who it serves (Arif, federation, external) |
| `role` | What it may do |
| `authority_band` | observe / reason / draft / execute / mutate / seal |
| `memory_scope` | What it may remember |
| `tool_scope` | What MCP tools it may call |
| `audit_scope` | What must be logged |
| `revocation_path` | How authority is removed |
| `human_veto` | Where F13 interrupts |

Without this, "agent identity" is theatre.

---

## Memory Is Not Storage

LLM memory = helpful context.
Governed memory = admissible evidence with authority, provenance, and replay.

| Grade | Meaning | Example |
|-------|---------|---------|
| **L1 Ground Truth** | Sealed, ratified, immutable | VAULT999 receipt |
| **L2 Verified State** | Live tool/source checked | arifOS health probe |
| **L3 Cached State** | Previously known, may be stale | Agent card from disk |
| **L4 Inferred** | Reasoning only, not truth | LLM output |

Memory without governance = hantu memory — appears to know, cannot prove standing.

---

## The Five Permanent Rules

1. No memory becomes truth without evidence.
2. No identity becomes authority without registration.
3. No delegation becomes permission without policy.
4. No tool result becomes judgment without audit.
5. No AI output becomes SEAL without sovereign ratification.

---

## What Survives the Next Horizon

| Component | Survival Strategy |
|-----------|-------------------|
| **Transport** | Delegate to a2a-sdk. Never re-implement. |
| **Constitutional overlay** | Python middleware. Thin, testable, portable. |
| **Identity** | Registered, scoped, revocable. Not cosmetic. |
| **Memory** | Evidence-graded. L1-L4. Auditable. |
| **Governance** | F1-F13 floors + DelegationGuard + 888_JUDGE. |
| **Audit** | VAULT999 receipts. Every completion. No exceptions. |

---

## The Migration Path

```
Today:    Express server (3,862 lines) + 200 lines of governance
Phase 1:  Python scaffold + ConstitutionalMiddleware
Phase 2:  SDK integration + governance overlay
Phase 3:  Express deprecated, Python AAA on port 3001
Future:   AAA grows governance, not transport. Always.
```

The Express server stays running until Python reaches parity.
Arif decides the cutover. Not the agents.

---

*DITEMPA BUKAN DIBERI — AAA is a constitution, not a server.*
