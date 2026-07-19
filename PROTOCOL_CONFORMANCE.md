# PROTOCOL_CONFORMANCE.md — AAA Control Plane

> Layer: L1 · Role: Cockpit dashboard, A2A gateway, agent identity, federation display · Repo: ariffazil/AAA

## MCP Conformance
| Requirement | Status | Evidence |
|------------|--------|----------|
| llms.txt | ✅ | `/root/AAA/public/llms.txt` — React 19 cockpit + A2A mesh gateway summary |
| tools/list | ⚠️ | No MCP server — AAA serves the React cockpit UI and A2A gateway, not MCP tools |
| health endpoint | ✅ | `:3001/health` — returns status, identity_hash, apex_scalars |
| MCP protocol | N/A | AAA is not an MCP server; it is the federation display and A2A routing layer |

## FastMCP Conformance
| Requirement | Status | Evidence |
|------------|--------|----------|
| FastMCP server | ❌ | Not applicable — React 19 + Vite 8 + TypeScript. AAA is not a Python MCP organ |
| Resource discovery | ❌ | No MCP resources — AAA serves UI assets and A2A routes, not MCP resources |

## A2A Conformance
| Requirement | Status | Evidence |
|------------|--------|----------|
| Agent card | ✅ | `/.well-known/agent-card.json` — full schema with capabilities, skills, signatures. Additional agent cards for openclaw, opencode, hermes-asi, makcikgpt, prospect-maturation |
| A2A gateway | ✅ | `:3001` — A2A mesh gateway routing across all 7 organs |
| Task schema | ✅ | A2A task operations via `dist/a2a/agent-card.json` (13,939 bytes) |
| Streaming | ✅ | SSE support via A2A gateway |
| Routing policy | ✅ | `/.well-known/a2a-routing-policy.json` |
| Agent discovery | ✅ | `/.well-known/agent.json` for agent identity |

## XMCP Conformance
| Requirement | Status | Evidence |
|------------|--------|----------|
| App schema | ❌ | No webmcp.json — AAA is a control plane, not an MCP app host |
| Resource schema | ❌ | No MCP resources — AAA serves React SPA assets |
| AI plugin | ✅ | `/.well-known/ai-plugin.json` |
| Federation manifest | ✅ | `/.well-known/arifos.json` — federation identity |

## Gaps
| Gap | Priority | Detail |
|-----|----------|--------|
| MCP tools/list | P3 | Not a gap — AAA's role is display + A2A routing, not MCP tool serving. By design |
| FastMCP | — | Not applicable — TypeScript organ, not Python |
| webmcp.json | P3 | Not needed — AAA serves cockpit UI, not MCP apps |

## Required Compliance
- L1 Protocol: A2A (mandatory — gateway role) + MCP (not applicable) + FastMCP (not applicable)
- AAA is the A2A hub of the federation — its protocol compliance is measured by A2A conformance, not MCP
- Next milestone: Maintain zero gaps in A2A protocol compliance

---
Generated: 2026-07-19 · Authority: AAA Control Plane
DITEMPA BUKAN DIBERI
