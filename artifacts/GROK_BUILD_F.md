# Grok Build Narrow MCP + Hybrid Multi-Agent Synthesis Forge — 2026-06-23

**Mode:** Synthesis + Concrete Sovereign Reference Implementation
**Inputs:** xAI Grok Build MCP docs (narrow per trust boundary, allowed_tools, hybrid stdio/remote) + xAI grok-4.20-multi-agent analysis (server-side research augmentation vs client-controlled execution).
**Grounding:** Live arifOS federation (AAA A2A, A-FORGE leases/MCP 7072, arifOS MCP 8088, arifos-mcp-federation skill, existing arifos_memory_mcp, ADRs, Dream Engine/Cooling Ledger, principal_agent taxonomy).
**Boundary:** T1/T2. No irreversible execution. All respects F floors, 888_HOLD for change, read/write separation.

## Delivered Package (Minimal but Complete)

1. **mcp-repo-read** (`/root/A-FORGE/services/grok-build-mcp/mcp_repo_read.py`)
   - FastMCP stdio (or --http).
   - Tight tools: list_files, read_file (bounded), search_symbols, get_adr (arifOS/adr), search_memory (bridge).
   - No writes. F1/F2/F4/F11 native.
   - Configurable REPO_ROOT.

2. **mcp-memory** (`/root/A-FORGE/services/grok-build-mcp/mcp_memory.py`)
   - FastMCP stdio.
   - Narrow: recall_adr_context, recall_cooling_ledger, get_dream_summary, search_governance (F-floors, 888 notes).
   - Explicit escalation note: mutations via arifOS 888 + A2A.
   - Bridges to existing arifos_memory_mcp and Cooling/Dream artifacts.

3. **Config** (updated `mcp-configs/grok-build-mcp.example.json`)
   - Added entries for mcp-repo-read and mcp-memory (stdio).
   - Retains gb-federation-router + core federation MCPs (arifos, aforge, organs) with labels/descriptions.
   - Notes on narrow, leases, 888, hybrid handoff.

4. **Orchestration Layout** (extended `GB_MCP.md`)
   - Full table with new narrow servers + hybrid row for multi-agent.
   - Updated topology incorporating prior gb-federation-router.
   - New section 9: Hybrid Pattern with xAI Multi-Agent.
     - When to use each.
     - Handoff via A2A / memory drop / VAULT.
     - Limitations of multi-agent mode (no direct custom MCP, hidden state) respected.

5. **Self-docs** already carried prior forge; this extends with the two starters + hybrid.

## Alignment to Both Syntheses

- Narrow per trust boundary: delivered (mcp-repo-read read-only; mcp-memory governance read).
- allowed_tools / leases: wired (recommend in config + A-FORGE leases for any change).
- Router: gb-federation-router + arifos-mcp-federation skill.
- Metrics: telemetry in skeletons (policy_denied, approval_required, fallback).
- Governance overlay for ops-change: explicit arifOS 888 + A2A.
- Hybrid: documented (multi-agent for research breadth; sovereign MCP/Grok Build for execution depth + control).
- One server per boundary: mcp-repo-read (code read), mcp-memory (memory/gov), separate from exec (A-FORGE).

## Constitutional Mapping

- F1: reads only in these two.
- F2/F4/F7/F9/F11: explicit in tools + telemetry + ADR/governance recall.
- F13/888: escalation paths in memory and layout for any mutation.
- A2A mesh: for handoff and multi-agent result integration.
- Existing memory_mcp + ADRs + Dream: directly referenced, not reinvented.

## Hybrid Orchestration Guidance (Summary)

- **Research/Exploration**: xAI multi-agent (external API call from Grok Build tool if needed). Gather diverse views.
- **Plan/Route/Execute**: Grok Build harness + narrow MCPs (mcp-repo-read first, then mcp-memory for context, A-FORGE leases for change).
- **Handoff**: A2A task submit or memory drop of research artifacts. Grok Build planner owns routing.
- Never execute side-effects from multi-agent outputs without sovereign gates.

## Verification

- Skeletons use FastMCP patterns matching A-FORGE services and arifos_memory_mcp.
- Narrow (5-6 tools max per server).
- Stdio primary for Grok Build CLI.
- References real paths (/arifOS/adr, cooling_ledger, DREAM_ENGINE_SPEC).
- Updated config and layout include both syntheses.

**Next (Arif directive):**
- Wire the routers to actually proxy a couple calls (e.g. to arifos_memory_mcp or A-FORGE).
- Add mcp-repo-write (lease-gated skeleton).
- mcp-smoke-test the new servers.
- A2A dialogue test (Grok Build as consumer of mcp-memory).
- 888 review of surfaces + update toolbench/registry.

All per DITEMPA BUKAN DIBERI. 999 SEAL path ready.

**Package complete.** Ready for use in Grok Build orchestration within the federation.