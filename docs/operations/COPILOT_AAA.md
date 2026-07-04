# Copilot Agentic Intelligence Path Map (AAA State + arifOS Kernel)

Status: deploy-ready map
Date: 2026-06-09
Owner: AAA control plane

## 1) Direct Answer: Do You Need to Build an MCP Client?

Short answer: no for Copilot Studio, yes only for custom runtime surfaces.

- Copilot Studio already provides the MCP client.
- You only provide MCP server URL, auth config, and tool schema quality.
- You build a custom MCP client only if you want a non-Studio runtime (custom web app, custom orchestrator, etc.).

## 2) Surface Truth (Important)

Two separate surfaces exist today:

1. BizChat/Copilot chat surfaces:
- Strong user context and enterprise integration.
- MCP availability depends on product surface and tenant rollout.

2. Copilot Studio agent surface:
- Explicit MCP tool onboarding and control.
- Best place to enforce deterministic routing for contrast discovery.

Operational recommendation:
- Use Copilot Studio as the execution surface for MCP-governed retrieval.
- Keep AAA/arifOS governance as the policy spine.

## 3) Federation Endpoint Map (Public + Internal)

Source of truth file:
- AAA docs endpoint registry: `AAA/docs/MCP_ENDPOINT.md`

Current public MCP endpoints:
- arifOS kernel: `https://arifos.arif-fazil.com/mcp`
- GEOX: `https://geox.arif-fazil.com/mcp`
- WEALTH: `https://wealth.arif-fazil.com/mcp`
- WELL: `https://well.arif-fazil.com/mcp` (registry notes service may be offline)

Transport policy:
- Public transport standard: `streamable-http`
- Avoid new SSE-based flows.

## 4) File Path Map by L0-L5

### L0 Governance (AAA + arifOS constitutional controls)

- AAA governance runbook: `AAA/docs/operations/REPO_MCP.md`
- AAA MCP endpoint authority: `AAA/docs/MCP_ENDPOINT.md`
- AAA snapshot attestation: `AAA/docs/operations/COPILOT_SNAPSHOT.md`
- arifOS MCP surface contract: `arifos/contracts/mcp_surface.yaml`

### L1 Identity (agent identity and role cards)

- AAA primary agent card: `AAA/agent-card.json`
- AAA A2A cards: `AAA/a2a/agent-cards/`
- AAA public agent registry: `AAA/public/a2a/agents.json`

### L2 Memory (policy memory + governed context)

- arifOS memory/governance tooling: `arifos/arifosmcp/tools/memory.py`
- arifOS session tools: `arifos/arifosmcp/tools/session.py`
- arifOS vault events: `arifos/arifosmcp/VAULT999/SEALED_EVENTS.jsonl`

### L3 Enterprise Data (M365/Graph, tenant-scoped)

- No repo-local file is the authority for tenant Graph ranking.
- Treat Copilot Studio agent configuration and tenant policy as L3 control plane.
- For discovery use-cases, route to contrast tools instead of Graph-only ranking.

### L4 Tools (MCP servers, routing, execution)

AAA side:
- MCP contracts: `AAA/contracts/mcp_surface.yaml`
- MCP web bridge code: `AAA/src/webmcp.ts`

A-FORGE side:
- MCP server entry: `A-FORGE/src/mcp/server.ts`
- MCP core server: `A-FORGE/src/mcp/core.ts`
- MCP client lib: `A-FORGE/src/mcp/client.ts`
- MCP surface contract: `A-FORGE/contracts/mcp_surface.yaml`

arifOS side:
- HTTP transport: `arifos/arifosmcp/transport/http.py`
- STDIO transport: `arifos/arifosmcp/transport/stdio.py`
- Tool registry surface: `arifos/arifosmcp/tool_registry.json`
- Canonical tools package: `arifos/arifosmcp/tools/`

GEOX discovery governance specs:
- Contrast primitive spec: `geox/docs/GEOX_CONTRAST_PRIMITIVE_SEARCH_SPEC.md`
- Deterministic router spec: `geox/docs/ARIFOS_ROUTE_QUERY_SPEC_v1.md`

### L5 Model Layer

- Model is replaceable.
- Behavior quality is dominated by L0 routing policy + L4 tool contract quality.

## 5) Deterministic Query Path (Recommended)

For all knowledge queries inside Studio agent:

1. Agent receives user query.
2. Mandatory call: `arifos_route_query`.
3. Router returns mode:
- `exploit` -> Graph/known-item lane
- `explore` -> contrast/disconfirmation lane
- `hybrid` -> both lanes with fixed explore floor
4. Agent executes only allowed tools from router output.
5. Final response must include:
- supporting evidence
- contradicting evidence
- unknowns
- confidence band
6. If contradiction floor fails, response status = PARTIAL (not COMPLETE).

## 6) What Must Be Forged Next (Minimal)

1. Authentication boundary:
- Pilot: API key auth on MCP gateway.
- Production: delegated/OAuth path and per-user ACL filter if service principal is used.

2. Router enforcement:
- Implement `arifos_route_query` as mandatory pre-call.
- Add guard that blocks retrieval tools if router decision is missing.

3. Observability:
- Log mode, selected tools, reason_code, exploit/explore doc counts.

4. Evaluation:
- Baseline vs variant with KPIs:
  - Novelty@K
  - contradiction hit rate
  - noise rate
  - analyst utility

## 7) Tenant-Deploy Checklist

- [ ] `streamable-http` endpoint reachable at `/mcp`
- [ ] TLS certificate valid
- [ ] Auth policy configured (pilot or production mode)
- [ ] Copilot Studio agent includes MCP server URL
- [ ] System instructions enforce mandatory router call
- [ ] Retrieval guard blocks policy-bypass calls
- [ ] Audit telemetry enabled
- [ ] KPI dashboard defined

## 8) Final Operating Position

Bridge is easy.
Governed behavior is the hard part.

Use Copilot Studio as MCP execution surface, bind it to AAA state policy, and make arifOS routing mandatory so discovery behavior cannot silently collapse back into Graph-only exploitation.
