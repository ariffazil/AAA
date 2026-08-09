# CONSTITUTIONAL_SEPARATION_AXIOM

> **Sealed:** 2026-08-09T05:45:00+08:00
> **Author:** ARIF (F13 Sovereign)
> **Witness:** Hermes Agent (hermes-asi)
> **Classification:** SOVEREIGN CONSTITUTIONAL — F13 ratification
> **Epistemic:** INT (architectural truth from sovereign reasoning)

---

## The Eureka

> **AAA bukan protocol. AAA adalah constitutional state.**

---

## The Architecture of Separation

### Two Flows

**Operation flow (downward):**
```
STATE_READY
    ↓
CALL_MAP
    ↓
MCP
    ↓
A2A
    ↓
arifOS
    ↓
ACT + DID
    ↓
VAULT999
```

**Authority flow (upward):**
```
VAULT999
    ↓
ACT + DID
    ↓
arifOS
    ↓
A2A
    ↓
MCP
    ↓
CALL_MAP
    ↓
STATE_READY
```

#> **Amended by:** ACT_AUTHORITY_LAYER.md (L5 detail — did:web + ACT separation of powers)

## The Layer Table

| Layer | Category | What lives here | Test: remove it |
|-------|----------|----------------|-----------------|
| **L6** | IMMUTABLE | VAULT999 — immutable sealed receipts | Institution dies |
| **L5** | IMMUTABLE | ACT + DID — who am I, am I allowed | Institution dies |
| **L4** | CONSTITUTIONAL | arifOS F1-F13 — should I do it | Institution dies |
| **L3** | REPLACEABLE | A2A — how do I talk | Institution survives ✅ |
| **L2** | REPLACEABLE | MCP — how do I call | Institution survives ✅ |
| **L1** | DISPOSABLE | FastMCP, SDK, Framework, Libraries | Institution survives ✅ |

**L5 detail:** See `ACT_AUTHORITY_LAYER.md` for did:web (identity) + ACT (authority) separation of powers, 403 enforcement proof.

### The Questions

| Layer | Question |
|-------|----------|
| MCP | **How** do I call? |
| A2A | **Who** do I talk to? |
| ACT | Am I **allowed**? |
| did:web | **Who** am I? |
| arifOS | **Should** I do it? |
| VAULT999 | Can I **prove** it happened? |

### The Formula

**Protocol is subordinate to governance. Not the other way around.**

---

## The Destruction Test

| Test | Remove | Survives? |
|------|--------|-----------|
| 1 | MCP | ✅ Yes — institution survives |
| 2 | A2A | ✅ Yes — institution survives |
| 3 | FastMCP / SDK | ✅ Yes — institution survives |
| 4 | F1-F13 | ❌ No — institution dies |

**Therefore:** F1-F13 is the constitutional layer.

---

## The Anti-Pattern Warning

> Kalau AAA nak survive 10 tahun lagi, jangan biarkan A2A atau MCP masuk ke L4.

The drift pattern to guard against:
```
Protocol → Policy → Governance → Trapped
```

**The principle:** Protocol is the law of coordination.
Governance is the law of truth.
AAA must remain a *constitutional state machine* that uses MCP and A2A,
but never depends on MCP or A2A to determine what is true, permitted, or authoritative.

---

## Compact Form

```
MCP      = HOW
A2A      = WHO TALKS
ACT      = WHO MAY ACT
arifOS   = WHO DECIDES
VAULT999 = WHO CAN PROVE
```

---

*Protocol ialah undang-undang koordinasi.*
*Governance ialah undang-undang kebenaran.*
*DITEMPA BUKAN DIBERI.*
