# A2A Linux Foundation Standard Comparison — arifOS AAA Sovereign Profile

**Date:** 2026-06-23  
**Context:** Exploration of Google → Linux Foundation Agent2Agent Protocol (A2A) vs sovereign AAA implementation.  
**Goal:** Interoperability while preserving constitutional floors F1-F13, principal_agent taxonomy, 888_HOLD, VAULT999, and MCP complementarity.  
**Forge:** Grounded in live machine state (/root/AAA/a2a-server/, public/a2a/, agent cards, arep-task-manager.js, grok-build card, MCP surfaces).

## Executive Summary

The Linux Foundation A2A (post-2025 donation) is the dominant open standard for agent discovery, task delegation, and collaboration. It defines:

- Agent Card (JSON at /.well-known/agent-card.json or equivalent)
- Task as stateful work unit (submitted → working → input-required → completed/failed/canceled)
- Message (turns with Parts: text/data/file)
- Artifact (outputs)

**AAA Status:** Already substantially aligned on core primitives (Agent Cards with skills/capabilities, Task lifecycle via AREP explicitly documented as "aligned with A2A v1.0", rich discovery). 

**Sovereign Advantage:** Deep extensions for governance that the base spec lacks (F floors, evidence, human veto, principal binding). Do not replace base — extend it.

**Recommendation for Grok Build + Federation:**
- Adopt base A2A fields for external interoperability.
- Keep arifOS extensions (principal_agent, floor_scope on skills, subAgentPolicy with 888_HOLD, mcp_servers list).
- Use A2A for agent-to-agent delegation (e.g., Grok Build delegates research synthesis to 333-AGI or organ witness).
- Keep MCP for tool surfaces (narrow mcp-repo-read, mcp-memory, etc. as previously forged).
- Hybrid: xAI multi-agent for breadth → A2A handoff to sovereign surfaces for depth + control.

## Detailed Field Comparison

### Agent Card

**Base LF A2A (from spec + public examples):**
- name, description, url, provider (organization, system)
- version, protocol_version
- capabilities: {streaming, push_notifications, ...}
- authentication: {schemes: ["bearer", "apiKey"], ...}
- default_input_modes, default_output_modes (e.g., ["text/plain", "application/json"])
- skills: array of {id, name, description, tags, examples, ...}
- (implied: endpoints, supported features)

**AAA Current (inspected):**
- Public gateway card (`/public/a2a/agent-card.json`): Matches closely — name, description, url, provider, version, protocol_version, capabilities (streaming), authentication, default modes, skills (with id/name/description/tags/examples).
- Per-citizen cards (e.g., grok-build.json in a2a-server/agent-cards/ and /agents/grok-build/agent-card.json): Use custom "$schema": "arifOS/agent-card/v2.0.0".
  - Heavy sovereign: principal_agent (string + binding object with source/sovereignty_tier/authority_notes), principal_accountability, governed_by (F1-F13 list), authority_boundary (T1/T2/T3), subAgentPolicy (maxParallel, registered types, capability_modes, isolation, 888_HOLD default), skills with extra fields (floor_scope[], riskClass, executionAllowed, approval_policy), mcp_servers list, strengths/weaknesses, preferred_tasks, constitutional_injection.
  - Transport, capabilities, version present but embedded.
- Discovery: Multiple locations (/.well-known/ implied in docs, /a2a/agent-card.json, per-agent, registries/AAA_AGENTS_REGISTRY.json, agent-card-registry.js auto-load).
- Task: arep-task-manager.js explicitly "manages task lifecycle aligned with A2A v1.0 (submitted → working → completed/failed)" + AREP reality layers + VAULT seals.

**Gaps / Opportunities:**
- grok-build card lacks top-level "skills" array in standard shape (has custom "skills" with floor_scope) and "authentication"/"default_modes" at root.
- No explicit "endpoints" or "url" in all per-agent cards (gateway has).
- State machine richer in AAA (UNBORN → ... → SEALED/DEAD) vs base A2A (focus on task states).
- No native "Parts" / "Artifacts" modeling in inspected code (but AREP + task manager produce artifacts/seals; messages via dialogue).

### Task / Message / Artifact

**LF A2A:**
- Task: id, contextId, status (state: submitted/working/...), metadata, artifacts[].
- Message: role, parts[] (Part: kind=text/data/file, content).
- Artifact: name, parts[], metadata.

**AAA:**
- AREP Task Manager + agent_lifecycle: task_id, context_id, status.state, metadata (routing, skill), seals to VAULT999 with task_id/context_id.
- Explicit alignment note in code.
- Messages handled in dialogue routes / federation_envelope.
- Artifacts via evidence bundles, receipts, vault payloads.

**Alignment:** Strong on intent. AREP adds "reality gating" (health probes, evidence progression, F floors) before A2A states advance.

## Sovereign A2A Profile (Proposed Extension)

**Rule:** Base fields for interoperability. All constitutional logic under "arifos" or "extensions" namespace.

Example structure for any card (e.g., grok-build):

```json
{
  // Base LF A2A (for external discovery)
  "name": "...",
  "description": "...",
  "url": "https://.../a2a",
  "provider": { "organization": "arifOS", "system": "AAA + Grok Build" },
  "protocol_version": "1.0.0",
  "capabilities": { "streaming": true, ... },
  "authentication": { ... },
  "default_input_modes": ["text/plain", "application/json"],
  "default_output_modes": ["application/json"],
  "skills": [  // Standard shape
    { "id": "plan-mode", "name": "...", "description": "...", "tags": ["plan"], "examples": [...] },
    // ... map from custom
  ],
  "endpoints": { "a2a": "...", "mcp": "..." },

  // Sovereign Extensions (arifOS profile)
  "arifos": {
    "$schema": "arifOS/agent-card/v2.0.0",
    "id": "grok-build",
    "principal_agent": "llm",
    "principal_binding": { ... },
    "governed_by": ["F1", ... "F13"],
    "authority_boundary": "... T3: 888_HOLD ...",
    "subAgentPolicy": { "default": "888_HOLD for irreversible", ... },
    "mcp_servers": [ ... ],  // From previous MCP forge work
    "skills": [  // Extended with constitutional
      { "id": "plan-mode", "floor_scope": ["F1","F4","F7"], "riskClass": "low", ... }
    ],
    "constitutional_injection": "...",
    "mcp_federation": "arifos-mcp-federation skill + narrow MCPs (repo-read, memory, write gated)"
  }
}
```

This allows:
- External agents (Google Cloud, Azure, etc.) to discover basic capabilities/skills.
- Sovereign agents to see full F floors, leases, MCP surfaces, 888 gates.

## MCP + A2A Complementarity (Reinforced)

From prior forge (narrow MCPs for Grok Build):
- MCP = tool plane (mcp-repo-read for code/ADR, mcp-memory for Cooling/Dream/governance, mcp-repo-write gated via leases).
- A2A = agent plane (delegate e.g. "use mcp-memory to ground this research, then A2A handoff to 555-ASI for critique").

In Grok Build card: Advertise both (mcp_servers + a2a delegation endpoints).

Example A2A skill for Grok Build:
{
  "id": "federation-mcp-delegate",
  "name": "Federation MCP + Organ Delegate",
  "description": "Route to narrow MCP surfaces or A2A to organs (GEOX etc.) under F floors.",
  "tags": ["mcp", "federation", "governance"]
}

## Task Lifecycle Mapping

AAA AREP already claims alignment:
- submitted → working → ...
- Adds: reality probe (F2 evidence), lease (A-FORGE), 888 if needed, seal to VAULT.

Recommendation: Expose standard A2A Task status in responses, while internal state is richer.

## Recommendations for Grok Build Integration

1. **Card Alignment:** Update grok-build/agent-card.json (and mirrored a2a-server copy) to include base fields above. Keep sovereign under "arifos".
2. **Discovery:** Ensure grok-build publishes at standard path or via AAA gateway registry.
3. **Delegation:** Grok Build (harness) uses A2A to delegate to persistent citizens (hermes-asi for memory, organs for evidence). Use previous narrow MCPs locally.
4. **Hybrid:** As sealed previously — multi-agent research → A2A structured task to sovereign surfaces.
5. **Governance:** All A2A interactions inject F1-F13 + principal binding. Use hooks/plugins from extension surface for policy.
6. **Next Forge:** Implement minimal A2A Task submit/response that maps to AREP + routes to MCP if needed.

## Forged Artifacts (This Exploration)

- This document.
- (See sibling forge: updated grok-build card with A2A base + arifos extensions if applied.)

**Entropy Reduction:** High. Clarifies path to external interoperability without diluting sovereignty.

**Sealed under previous 999_SEAL context + F11 auditability.**

All decisions respect: evidence before confidence, proposals before mutation, human veto absolute.

**DITEMPA BUKAN DIBERI.**