# GB_MCP.md — Grok Build + arifOS / AAA / A-FORGE

**Forge:** 2026-06-23 by Grok Build (self) under AAA + arifOS constitution.
**Grounded in live machine reality** (not external Perplexity plan).
Uses:
- arifos-mcp-federation skill (O_Ω router)
- A-FORGE MCP (7072) + real lease authority system (scopes = allowed_tools equivalent)
- arifOS MCP (8088) constitutional kernel
- AAA A2A mesh (agent cards, handoff, discovery)
- Organ MCPs (evidence only)
- stdio for local harness; streamable-http for mesh/remote
- Narrow surfaces + server-side policy + 888_HOLD

## Core Principle (F1-F4-F11-F13)

One narrow MCP (or surface) per trust boundary. Planner decides. Leases + floors gate. Everything emits auditable telemetry. Human (F13) has absolute veto.

**Do not** put read + write in the same server unless the write surface is lease-scoped and explicitly declared.

## 1. Layers (Reality Topology)

| Layer | Substrate | Transport (preferred) | Role in Grok Build flows | Narrow Control |
|-------|-----------|-----------------------|---------------------------|---------------|
| Planner / Router | Grok Build (this harness) + `arifos-mcp-federation` skill + gb-federation-router | Native + stdio MCP | Intent → sequence plan (editable) | orchestrate_sequence, route_to_mcp, check_floors |
| Read tier | GEOX / WEALTH / WELL / arifOS sense / repo native | stdio or streamable-http | Evidence, search, status | Only read tools; organs are evidence-only by design |
| Change tier | A-FORGE lease (propose_patch, limited FS/git) | A-FORGE MCP (7072) | Patch, branch, PR draft | Lease scopes + dry-run first |
| Execution tier | A-FORGE (test, build, lint, staging deploy) | A-FORGE MCP + lease | Run, measure, release (gated) | Lease required; 888_HOLD for prod |
| Control / Judgment | arifOS (judge, vault, floors) | arifOS MCP | 888 deliberation, seal, F gates | Read + deliberate only for Grok Build |
| Mesh / Handoff | AAA A2A (3001) + agent registry | A2A (JSON) | Discovery, delegation, status, cross-role | Via agent cards + contracts |
| Memory / State | AAA memory + arifOS L1-L6 + cognitive services | Via skill or MCP bridge | Context, ADRs, receipts | Bounded |

## 2. Orchestration Flow (Grok Build as Planner)

Typical multi-step (e.g. "implement feature X and run tests + evidence impact"):

1. **Grok Build receives intent** (TUI or headless).
2. **Call planner**:
   - Native plan mode, or `orchestrate_sequence` from gb-federation-router, or invoke `arifos-mcp-federation` skill.
   - Returns stages + recommended MCP labels + tool sequence.
   - Grok Build (or human) edits/vetoes the plan.
3. **Read phase** (parallel where safe):
   - Route to geox/wealth/well for evidence.
   - Local narrow read or native grep/read.
   - arifOS sense for governance context.
4. **Change phase** (gated):
   - Request lease from A-FORGE with minimal scopes.
   - Perform edits via native search_replace or A-FORGE lease-mutate.
   - Draft PR / patch via github MCP (read-heavy) or A-FORGE.
5. **Execution phase**:
   - Lease-scoped test / build / benchmark via A-FORGE MCP tools.
   - Monitor + get output.
6. **Control / Judgment**:
   - If T3 or high risk: hand to arifOS judge (via MCP or A2A).
   - Emit receipts to VAULT.
7. **Mesh / Handoff** (if needed):
   - A2A to hermes-asi, openclaw, or another FI for complementary work.
   - Status polling via A2A.

Fallbacks always exist (native tools + spawn_subagent worktree, other organs).

## 3. Config & Registration (for this Grok Build)

See `mcp-configs/grok-build-mcp.example.json` in this directory.

- Local (this machine): stdio entries for gb-federation-router + any thin local servers. Fast, full native control.
- Remote declaration (if using xAI Responses/SDK side for other instances): use `type: "mcp"`, `server_url`, `server_label`, **always** `allowed_tools` list + description.
- A-FORGE + arifOS already declared via env or existing MCP connections in this session.

Grok Build auto-discovers / can be pointed at these.

## 4. Tool Filtering & Context (critical)

- Every tool definition injected into context costs tokens.
- Use `allowed_tools` / lease scopes aggressively.
- gb-federation-router deliberately exposes only 6 high-value orchestration verbs.
- For A-FORGE: request lease first (authority object) instead of exposing every forge_* tool.

## 5. Metrics & Telemetry (agentic + server path)

Emit the envelope (see gb_federation_router.py + prior CLAIM):

```json
{
  "epoch": "...",
  "server": "gb-federation-router",
  "tool": "orchestrate_sequence",
  "latency_ms": 120,
  "success": true,
  "schema_valid": true,
  "approval_required": false,
  "policy_denied": false,
  "confidence": 0.9,
  "qdf": "orchestration",
  "verdict": "allow"
}
```

Track (at minimum):
- Tool selection precision (first-try correct narrow server)
- Success / schema rate
- Latency (P50/P95)
- Escalation / policy_denied rate
- Read vs change ratio
- End-to-end task success without manual intervention

Route envelopes to arifOS VAULT / A-FORGE receipts / AAA observability.

## 6. Security Holds (non-negotiable)

**888_HOLD + explicit F13 for:**
- Any production deploy or release
- Secret rotation / env mutation
- VAULT writes (except via proper writer path)
- Destructive ops, DROP, rm unknown
- Cross-organ structural changes

**Hard controls present in reality:**
- A-FORGE leases (per-agent authority matrix)
- arifOS F1-F13 injection + judgment
- AAA A2A contracts + principal-agent taxonomy
- Server-side (this router + A-FORGE) policy before model sees result
- Localhost binding + UFW for external
- Dynamic state probe before irreversible

## 7. How This Differs from Pure External Guidance

- We already have mature router (`arifos-mcp-federation`).
- Execution is A-FORGE with leases (better than prompt-only policy).
- Governance is arifOS (888 + floors) not a sidecar.
- Mesh is A2A (AAA) for agents, not only raw MCP.
- Config surface is mcporter + existing organ MCPs + these narrow add-ons.
- Everything is already under F1-F13 + VAULT audit.

We adopt the good ideas (narrow per-boundary, allowed_tools as primary knob, descriptive labels, 3-stage thinking, metrics) and wire them to live federation substrates.

## 8. Usage from Grok Build (this session)

- The harness already has native + many MCPs (github 95, geox/wealth/well, etc.).
- For complex orchestration: first use plan mode + call `arifos-mcp-federation` (skill) or the gb-federation-router MCP.
- For execution: go through A-FORGE MCP + lease request.
- For cross-agent: A2A via AAA.
- Start with the two forged narrow servers (per synthesis): mcp-repo-read (this dir) and mcp-memory.

See also:
- agents/grok-build/AGENTS.md + TOOLS.md (updated)
- A-FORGE/services/grok-build-mcp/mcp_arifos_kernel.py (the clean transport of arifOS kernel)
- /root/AAA/skills/arifos-mcp-federation/SKILL.md
- A-FORGE contracts/mcp_surface.yaml + src/interfaces/mcp
- AAA contracts/AAA_SKILL.md + mcp_surface.yaml
- arifOS/arifosmcp/kernel_mcp.py (internal reference narrow kernel surface)

## 9. Hybrid Pattern with xAI Multi-Agent (grok-4.20-multi-agent)

**Synthesis from xAI docs:** Server-side leader + sub-agents (4/16) is excellent for breadth in research/synthesis but has limitations:
- No direct client custom MCP / function calling in that mode.
- Sub-agent reasoning hidden (use `use_encrypted_content=True` if available).
- Higher cost/latency. Best for exploration, not long-horizon execution or governance.

**Sovereign Hybrid Recommendation (T1/T2 aligned):**

| Phase | Model/Mode | Tools/Surface | Handoff |
|-------|------------|---------------|---------|
| Exploration/Research | grok-4.20-multi-agent (4 or 16 agents via xAI SDK/Responses) | xAI built-in (web_search, x_search, code_execution) + remote MCP if supported | Output summaries → feed to Grok Build context |
| Planning & Routing | Regular Grok (Grok Build harness) | gb-federation-router + arifos-mcp-federation skill + mcp-repo-read + mcp-memory | Plan (editable) → narrow MCPs |
| Execution & Change | Regular Grok + Custom MCP | mcp-repo-read (read), A-FORGE leases (change/exec), mcp-memory (reflection) | Lease receipt + telemetry → arifOS 888 if T3 |
| Reflection/Closure | Grok Build + Hermes | mcp-memory (Cooling Ledger, Dream), A2A handoff | Write to Cooling Ledger / Dream Engine via arifOS |
| Kernel / Governance depth | Grok Build | **mcp-arifos-kernel** (new 2026-06-23) + check_floors / submit_for_judgment / get_rhythm_context / record_malam | Direct low-entropy kernel health + daily rhythm. Always HOLD on judgment. |

**Handoff mechanism:** Use A2A mesh (AAA) or simple file/VAULT drop of research artifacts into mcp-memory / repo context. Grok Build planner decides when to invoke external multi-agent (via tool that calls xAI API) vs stay in sovereign MCP loop.

This gives breadth (multi-agent) + depth/control/sovereignty (Grok Build + narrow MCPs + arifOS floors + A-FORGE leases + A2A).

Never rely on multi-agent mode alone for any action that touches write, infra, or constitutional decisions.

## Receipts & Audit

Every significant orchestration run should produce:
- Plan (editable)
- Lease receipts (A-FORGE)
- Telemetry envelope(s) (with policy_denied, approval_required, fallback_triggered)
- Optional VAULT seal (via arifOS)

F11 is satisfied by the trace.

---

**DITEMPA BUKAN DIBERI — forged against the actual machine (arifOS + AAA + A-FORGE + existing memory_mcp + ADRs + Dream Engine).**

Delivered: mcp-repo-read.py + mcp_memory.py skeletons (narrow, FastMCP stdio), updated config, hybrid guidance, layout.

Next if Arif directs: implement full proxy wiring, add mcp-repo-write gated, run mcp-smoke-test against the new servers, A2A validation, or 888_HOLD review.