# Anthropic MCP Specification Alignment

> **DITEMPA BUKAN DIBERI** — *Forged, Not Given*

## Canonical Reference
- **Source:** [modelcontextprotocol/specification — GitHub](https://github.com/modelcontextprotocol/specification)
- **Role:** Functional Layer (Layer 1)

## Alignment Mapping

AAA relies on the **Model Context Protocol (MCP)** for the Body layer (Ψ) to ensure tool interoperability:

1. **Tool Calling**: All domain organs (GEOX, WEALTH, WELL) are exposed via MCP servers.
2. **Context Injection**: Uses MCP resource templates for dynamic context anchoring.
3. **Capability Negotiation**: Agents and hosts negotiate capabilities (e.g., `sampling`, `roots`) during the initial MCP handshake.
4. **Transport**: Support for both `stdio` and `sse` transports as defined in the MCP spec.

## Implementation Status
- **`.openclaw/`**: Anchors the primary OpenClaw-MCP integration.
- **`acp/`**: Agent Communication Protocol (ACP) acts as the high-level bridge over raw MCP calls.

---
**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
