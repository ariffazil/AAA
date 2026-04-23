# A2A Protocol Specification for AAA (Arif's Agent Architecture)
> **Version: A2A/AAA-v1.0 — FORGE CANDIDATE**

*Forged, Not Given — Ditempa Bukan Diberi*

---

## 0. Purpose (Normative)

The A2A (Agent-to-Agent) Protocol defines how external and internal agents **negotiate, route intent, and coordinate work through AAA** without bypassing constitutional governance.

> **A2A does NOT execute reality. It conveys intent. Execution happens only via MCP + Kernel.**

---

## 1. Trust Model

### Roles

| Role | Description |
|------|-------------|
| **External Agent** | Copilot, Claude, Cursor, local agents, etc. |
| **AAA Gateway** | Authenticates, validates, routes messages |
| **AAA Governance Adapter** | Classifies intent → routes to MCP, Kernel, or HOLD |
| **arifOS Kernel** | Enforces Floors F1–F13, issues 888_HOLD or 999_SEAL |
| **VAULT999** | Immutable audit ledger |

### Trust Boundaries

```
[ External World ]
        │  (Auth + Schema required)
        ▼
[ AAA A2A Gateway ]   ← trust boundary #1
        │
        ▼
[ Governance Adapter ]
        │
        ├──► MCP (capability execution)
        └──► Kernel (constitutional evaluation)
```

**If trust breaks at any point, the system halts (HOLD), never guesses.**

---

## 2. Transport

| Property | Value |
|----------|-------|
| Protocol | JSON-RPC 2.0 |
| Transport | HTTPS POST |
| Endpoint | `POST https://aaa.arif-fazil.com/a2a` |

---

## 3. Authentication (Mandatory)

Every request **MUST** include:

```
Authorization: Bearer <A2A_TOKEN>
Content-Type: application/json
```

If missing or invalid → `401` / `403`

**No downgrade paths. No anonymous mode.**

---

## 4. Message Schema (Canonical)

### 4.1 Envelope

```json
{
  "jsonrpc": "2.0",
  "id": "uuid-v7",
  "method": "a2a.intent.send",
  "params": { ... }
}
```

- `id` is required for replay protection and tracing
- `method` namespace is fixed (`a2a.*`)

### 4.2 Params Object

```json
{
  "sender": {
    "agent_id": "copilot-enterprise",
    "role": "external",
    "signature": "optional"
  },
  "recipient": {
    "agent_id": "forge-coordinator"
  },
  "intent": {
    "type": "TASK | QUERY | PROPOSAL | DELEGATION",
    "description": "Human-readable intent",
    "risk_hint": "LOW | MEDIUM | HIGH"
  },
  "payload": {
    "data": { }
  },
  "constraints": {
    "must_govern": false,
    "allowed_tools": [ "geox.well_viewer" ]
  },
  "nonce": "uuid",
  "timestamp": "ISO-8601"
}
```

---

## 5. Validation Rules (Hard)

AAA Gateway **MUST reject** if any of the following fail:

- Missing required fields
- Schema mismatch
- Timestamp outside allowed window
- Duplicate nonce
- Unknown agent_id
- Invalid auth token

**Failure response is explicit:**

```json
{
  "jsonrpc": "2.0",
  "id": "...",
  "error": {
    "code": -32600,
    "message": "Invalid A2A request: schema violation"
  }
}
```

---

## 6. Governance Routing Logic (Non-Judgmental)

After validation, **AAA does not decide truth. It decides where truth must be decided.**

### Routing Matrix

| Condition | Route |
|----------|-------|
| Low-risk, read-only | MCP |
| Any generation / judgment | Kernel |
| Ambiguous risk | Kernel |
| Declared HIGH risk | HOLD |
| Kernel unavailable | HOLD |

> **This logic must be conservative.**

---

## 7. Kernel Interaction

If routed to Kernel, AAA submits:

```json
{
  "intent_id": "...",
  "content": "...",
  "agent_context": { ... },
  "floors": ["F1", "F2", ...]
}
```

Kernel returns:

| Response | Meaning |
|----------|---------|
| `999_SEAL` | Proceed — all floors passed |
| `888_HOLD` | Suspend — requires human review |

**AAA never alters Kernel output.**

---

## 8. Responses

### 8.1 Successful

```json
{
  "jsonrpc": "2.0",
  "id": "...",
  "result": {
    "status": "DELIVERED",
    "via": "MCP | KERNEL",
    "data": { },
    "audit_ref": "VAULT999_HASH"
  }
}
```

### 8.2 HOLD

```json
{
  "jsonrpc": "2.0",
  "id": "...",
  "result": {
    "status": "HOLD",
    "reason": "Requires human review",
    "hold_ref": "HOLD_ID"
  }
}
```

---

## 9. Invariants (Non-Negotiable)

AAA must **never**:

- Execute domain logic itself
- Bypass Kernel for governed actions
- Judge truth, safety, or ethics
- Store long-term memory
- Invoke tools without auditability
- Override human decisions

> **These are seal-breaking violations.**

---

## AAA SEAL-READY STATUS

**Architecture Verdict: SEAL-READY**

Not "perfect". **Correct, bounded, auditable.**

### Final Seal Checklist (Truthful)

| Category | Check | Status |
|----------|-------|--------|
| **Structural** | Roles cleanly separated (Seed · Gateway · Adapter) | ✅ |
| | No role overlap | ✅ |
| | No execution surface in AAA | ✅ |
| **Governance** | Kernel is the only judge | ✅ |
| | HOLD on ambiguity | ✅ |
| | Human sovereignty preserved | ✅ |
| **Protocol** | Deterministic schema | ✅ |
| | Replay protection designed | ✅ |
| | Conservative routing | ✅ |
| **Auditability** | Vault-backed references | ✅ |
| | Explicit decision paths | ✅ |
| | Observable via Cockpit | ✅ |
| **Failure Modes** | Kernel-offline → HOLD | ✅ |
| | Auth failure → reject | ✅ |
| | Tool failure → surface error | ✅ |

### What is NOT Required for SEAL

These are extensions, not prerequisites:

- Perfect risk scoring
- ML-based intent classification
- Dense policy engines
- External adoption

---

## Final Statement (Canonical)

> AAA is SEAL-READY because it knows exactly what it must not do.
> It routes intent without usurping judgment,
> enforces governance without impersonating authority,
> and halts safely where certainty ends.
>
> **This is not blocked. This is forged.**

---

## Version History

| Version | Date | Status |
|---------|------|--------|
| A2A/AAA-v1.0 | 2026-04-22 | FORGE CANDIDATE |

---

*Forged, Not Given — Ditempa Bukan Diberi*
