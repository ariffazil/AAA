# 🌐 PROTOCOL_MAP — arifOS Federation Protocol Alignment

> **Forged:** 2026-07-19 by FORGE (000Ω) · **Doctrine:** DITEMPA BUKAN DIBERI
> **Scope:** All 9 federation repos · **Status:** LIVING — update with every protocol change

---

## 1. Protocol Inventory (15 protocols)

| # | Protocol | Class | TRINITY-33 | Spec | Used By |
|---|----------|-------|------------|------|---------|
| 1 | **MCP** (Model Context Protocol) | PROTOCOL SPEC | K1 | [spec](https://modelcontextprotocol.io/llms.txt) | arifOS, GEOX, WEALTH, WELL, A-FORGE, HERMES |
| 2 | **FastMCP** | Framework | — | [docs](https://gofastmcp.com/llms.txt) | GEOX, WELL |
| 3 | **JSON-RPC 2.0** | Transport | — | [spec](https://www.jsonrpc.org/specification) | All MCP servers |
| 4 | **SSE** (Server-Sent Events) | Transport | — | [whatwg](https://html.spec.whatwg.org/multipage/server-sent-events.html) | arifOS, GEOX, A-FORGE |
| 5 | **Streamable HTTP** | Transport | — | MCP 2025-06-18 | arifOS, GEOX |
| 6 | **A2A** (Agent-to-Agent) | PROTOCOL SPEC | C1 | [spec](https://github.com/a2aproject/A2A) | AAA, A-FORGE |
| 7 | **XMCP** (Extended MCP) | Extension | — | [docs](https://xmcp.dev/) | GEOX (MCP Apps), A-FORGE |
| 8 | **SEP-2127** (Server Card) | Discovery | — | MCP docs-agent | GEOX, arifOS |
| 9 | **RFC 8615** (Well-Known URIs) | Discovery | IETF | [rfc8615](https://datatracker.ietf.org/doc/html/rfc8615) | arifOS, GEOX, ARIF-SITES |
| 10 | **NATS** | Message Fabric | C2 | [docs](https://docs.nats.io/) | arifOS, AAA, A-FORGE |
| 11 | **CloudEvents** | Event Envelope | C9 | [spec](https://github.com/cloudevents/spec) | arifOS ✅ (v2026.07.19) |
| 12 | **DID:WEB** | Identity | — | [w3c](https://w3c-ccg.github.io/did-method-web/) | A-FORGE |
| 13 | **OpenTelemetry** | Observability | K7 | [spec](https://opentelemetry.io/docs/specs/otel/) | AAA (observability stack) |
| 14 | **SLSA + Sigstore** | Supply Chain | F8 + K4 | [slsa](https://slsa.dev/) [sigstore](https://sigstore.dev/) | arifOS ✅ (provenance module) |
| 15 | **gRPC** | RPC | C10 | [spec](https://grpc.io/) | Infrastructure layer |

---

## 2. Per-Repo Protocol Matrix

### L0 — CANON (Identity)
| Repo | MCP | A2A | XMCP | Well-Known | Other |
|------|-----|-----|------|------------|-------|
| **ariffazil** | Consumer only | — | — | ✅ (GitHub Pages) | — |

### L1 — ROOT (Constitutional)
| Repo | MCP Server | FastMCP | JSON-RPC | SSE | Streamable HTTP | A2A | NATS | CloudEvents | Well-Known | SEP-2127 |
|------|-----------|---------|----------|-----|-----------------|-----|------|-------------|------------|----------|
| **arifOS** | ✅ (8 tools) | — | ✅ | ✅ | ✅ | Gateway | ✅ | ❌ Planned | ✅ | ✅ |
| **AAA** | Consumer | — | Consumer | Consumer | Consumer | ✅ Server | ✅ | — | — | — |

### L2 — EXECUTIVE (Agentic)
| Repo | MCP Server | MCP Client | A2A Agent | XMCP Apps | DID:WEB | SLSA | NATS | Well-Known |
|------|-----------|-----------|-----------|-----------|---------|------|------|------------|
| **A-FORGE** | ✅ (100+ tools) | ✅ | ✅ | ✅ Planned | ✅ | ✅ Planned | ✅ | ✅ |

### L3 — DOMAIN (Organs)
| Repo | MCP Server | FastMCP | JSON-RPC | SSE | Streamable HTTP | SEP-2127 | Well-Known | A2A Consumer |
|------|-----------|---------|----------|-----|-----------------|----------|------------|--------------|
| **GEOX** | ✅ (24 tools) | ✅ 3.4.2 | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| **WEALTH** | ✅ (8 tools) | — | ✅ | ✅ | ✅ | ❌ | ✅ | — |
| **WELL** | ✅ (8 tools) | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | — |
| **HERMES** | ✅ Bridge | — | ✅ | ✅ | ✅ | ❌ | ❌ | — |

### L4 — PUBLIC (Surface)
| Repo | MCP Apps | XMCP | Well-Known | SSE Consumer |
|------|----------|------|------------|--------------|
| **arif-sites** | ✅ Consumer | ✅ Consumer | ✅ | ✅ |

---

## 3. Conformance Status Summary

| Protocol | Repos Implemented | Repos Missing | Gap Severity |
|----------|-------------------|---------------|--------------|
| MCP Server | 5/5 (arifOS, GEOX, WEALTH, WELL, A-FORGE) | 0 | ✅ FULL |
| FastMCP | 2/2 (GEOX, WELL) | 0 | ✅ FULL |
| JSON-RPC 2.0 | 5/5 | 0 | ✅ FULL |
| SSE | 4/5 | HERMES (unverified) | 🟡 LOW |
| Streamable HTTP | 4/5 | HERMES | 🟡 LOW |
| A2A | 2/3 | A-FORGE (agent cards incomplete) | 🟠 MEDIUM |
| XMCP | 2/4 | A-FORGE (planned), WEALTH, WELL | 🟡 LOW |
| SEP-2127 | 2/5 | WEALTH, WELL, HERMES | 🟠 MEDIUM |
| Well-Known | 5/7 | A-FORGE (partial), HERMES | 🟡 LOW |
| NATS | 3/3 | 0 | ✅ FULL |
| CloudEvents | 0/3 | arifOS, AAA, A-FORGE | 🔴 HIGH |
| DID:WEB | 1/5 | arifOS, AAA, GEOX, others | 🟡 LOW |
| OpenTelemetry | 1/5 | AAA only (Prometheus/Grafana) | 🟠 MEDIUM |
| SLSA + Sigstore | 0/4 | All repos | 🔴 HIGH |
| gRPC | Infra only | Not required at app layer | 🟢 N/A |

---

## 4. Priority Fixes

| Priority | Protocol | Action |
|----------|----------|--------|
| 🔴 P0 | CloudEvents | Wire event envelope for inter-organ propagation (arifOS→NATS→AAA) |
| 🔴 P0 | SLSA + Sigstore | Add provenance generation to all CI pipelines |
| 🟠 P1 | A2A Agent Cards | Complete A-FORGE agent card schemas per A2A spec |
| 🟠 P1 | SEP-2127 | Add server cards to WEALTH, WELL, HERMES |
| 🟠 P1 | OpenTelemetry | Wire OTel SDK into arifOS + A-FORGE (traces + metrics) |
| 🟡 P2 | DID:WEB | Publish did:web documents for all organs |
| 🟡 P2 | XMCP Apps | Register MCP Apps in WEALTH + WELL |

---

*DITEMPA BUKAN DIBERI — Protocol alignment is the skeleton of federation.*
