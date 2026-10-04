# Session Findings: Layer Separation & Authority Layer Doctrine

## Context

Forged 2026-08-09 as part of the arifOS federation constitutional doctrine. Arif's Eureka was the distinction between communication protocols (MCP, A2A) and authority layers (ACT, did:web). This insight was canonized as two GENESIS documents.

## Key Documents Created

| Document | Path | Commit |
|----------|------|--------|
| Layer Separation Doctrine | `/root/arifOS/GENESIS/LAYER_SEPARATION_DOCTRINE.md` | `38cac609e` |
| Authority Layer Doctrine | `/root/arifOS/GENESIS/AUTHORITY_LAYER_DOCTRINE.md` | `b33d0a2d3` |
| STATE.md (unified SOT) | `/root/AAA/docs/STATE.md` | `1a046dc3` |

## Layer Separation Doctrine Summary

> **AAA bukan protocol. AAA adalah constitutional state.**
> Protocol is subordinate to governance. Not the other way around.

### Three Strata

| Stratum | Layers | Status |
|---------|--------|--------|
| **Immutable** | L6 VAULT999 · L5 ACT+DID · L4 arifOS F1–F13 | Constitutional — survives any protocol death |
| **Replaceable** | L3 A2A · L2 MCP | Coordination — swap today for tomorrow, F1–F13 unchanged |
| **Disposable** | SDK · Libraries · Frameworks | Plumbing — dies tomorrow, institution unchanged |

### The Test

| Remove | Survive? |
|--------|----------|
| MCP | ✅ CLI remains |
| A2A | ✅ CLI remains |
| FastMCP | ✅ |
| F1–F13 / arifOS | ❌ institution dies |
| ACT+DID | ❌ no trustworthy agency |
| VAULT999 | ❌ no proof |

## Authority Layer Doctrine Summary

**did:web** = "Who are you?" → identity (cryptographic)
**ACT** = "What office do you hold?" → capability binding
**F1-F13** = "Should that office be allowed?" → constitutional judgment
**VAULT999** = "Can we prove it later?" → evidence

### Separation of Powers

| Actor | Office | Allowed |
|-------|--------|---------|
| 333-AGI | Proposer | Propose |
| 555-ASI | Verifier | Verify |
| 888-APEX | Judge | Judge |
| A-FORGE | Executor | Execute |
| VAULT999 | Witness | Record |

### The 403 Proof

```
Hermes → AAA: "SEAL this action"

1 DID   Who?            → did:…:hermes     ✅
2 ACT   Office rights?  → OBSERVE/RESEARCH ✅
3 Req  SEAL
4 ACT   SEAL capability? → NO             ❌

Result: 403 / HOLD — AUTHORITY DENIED
```

**A2A valid · MCP valid · JSON-RPC valid — still DENY.**
Transport success is orthogonal to office rights.

## Integration with STATE.md

STATE.md §16 codifies this as the **docs entropy** section:

```
STATE.md = Constitution, not Library
1 Truth · N References · 0 Contradictions
```

The layer separation principle applies not just to protocols but also to documentation structure:
- STATE.md = Constitution (immutable authority)
- Satellite docs = Replaceable adapters (pointers, elaborations, procedures)
- Receipts = Proof (never merge)

## Related Skills

- `federation-provider-integration` — model provider routing
- `gemini-integration` — Gemini API specifics
- `aaa-docs-entropy-reduction` — document classification framework
