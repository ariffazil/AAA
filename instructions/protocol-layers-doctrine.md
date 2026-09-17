# Protocol Layers Doctrine — Three-Layer Federation Separation

> **Status:** F13_OBSERVED (2026-09-18) — forged from ChatGPT Deep Research contrast.
> **Binding:** All federation agents and organs.
> **Grounding:** CCC_DOCTRINE pipeline (ARIF→AAA→FED→CCC→A-FORGE→arifFlow→VAULT999) · A2A v1.0 spec · MCP 2026-07-28 · four-layer-separation.md.

## The Law

The federation uses three distinct, non-interchangeable interoperability layers:

| Layer | Protocol | Purpose | Authority |
|---|---|---|---|
| **Federation** | A2A v1.0 | Agent↔agent discovery, delegation, tasks, messages, artifacts | AAA registry decides who exists |
| **Capability** | MCP | Agent↔tool/data access | arifOS policy decides what's permitted |
| **Edge** | ACP / product SDK | Editor↔agent terminal binding | Local harness config |

## Invariants

1. **MCP is NOT the authority protocol.** An MCP call still needs arifOS policy when its consequence is meaningful. MCP provides capability; arifOS provides authority.
2. **A2A is NOT the tool protocol.** A2A handles agent discovery and task delegation. Tool access belongs to MCP.
3. **Edge protocols are local.** ACP, product SDKs, and harness-specific interfaces terminate at adapters. They never become the sovereign federation protocol.
4. **Each layer upgrades independently.** MCP protocol version changes do not affect A2A. A2A spec evolution does not affect tool access.

## Mapping to CCC Pipeline

```
ARIF (F13) ─── sovereign intent
  ↓
AAA ────────── A2A: agent discovery + task delegation
  ↓
FED ────────── A2A: model routing + capability matching
  ↓
CCC ────────── Edge: ACP/SDK harness binding
  ↓
A-FORGE ────── MCP: tool access + mutation execution
  ↓
arifFlow ───── MCP: receipt ingest + flow invariants
  ↓
VAULT999 ───── MCP: immutable append
```

DITEMPA BUKAN DIBERI ⚒️
