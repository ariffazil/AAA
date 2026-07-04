# Grok Build Narrow MCP Reference — Wired + Smoke + Write Skeleton + Extension Surface (Skills/Plugins/Hooks) — 2026-06-23

**Forge Phase:** Wiring + smoke + gated write + full Grok Build extension alignment (skills, plugins, hooks, MCPs).
**Priority chosen (per synthesis):** Wire the two (mcp-repo-read + mcp-memory) + smoke test first. Then deliver mcp-repo-write gated skeleton + hooks example + plugin bundle.

**Delivered (in /root/A-FORGE/services/grok-build-mcp/ and mirrored .grok example):**

1. **Wired mcp_repo_read.py**
   - Real FS: list_files, read_file (safe paths).
   - get_adr: loads from /root/arifOS/adr (real ADRs).
   - search_memory: scans ADRs + cooling_ledger for matches.
   - Telemetry, structured.

2. **Wired mcp_memory.py**
   - recall_adr_context: real /root/arifOS/adr scan.
   - recall_cooling_ledger: loads /root/AAA/registries/cooling_ledger/*.yaml.
   - get_dream_summary: loads D-DAJJAL/WELL_DREAM_ENGINE_SPEC.md.
   - search_governance: F11/F7/888 notes + arifos-mcp-federation + A2A escalation.
   - Bridge note to arifos_memory_mcp.

3. **Gated mcp_repo_write.py** (new)
   - apply_patch, create_branch, draft_pr.
   - All return HOLD/require lease or 888_HOLD for T3.
   - Explicit: never mix with read; escalate via A-FORGE + arifOS 888 + A2A.

4. **smoke_test_grok_mcp.py** (updated)
   - Direct import + stdio spawn demo for read/memory.
   - Gated write policy verification.
   - Ran successfully: imports real paths, launches without crash, write gates as expected.

5. **.grok/ extension surface** (per xAI docs CLAIM)
   - .grok/plugins/arif-narrow-mcp/plugin.toml: bundles skills + hooks + MCPs (repo-read, memory, write).
   - .grok/skills/repo-ops/SKILL.md: /repo-ops callable, instructions for narrow flow.
   - .grok/plugins/.../hooks/pre_tool_governance.py: pre-tool policy (deny writes, escalate 888).
   - Discovery: /plugins, /skills, /hooks, /mcps in Grok Build TUI. Claude compat via .grok/.

6. **Config + docs updates**
   - grok-build-mcp.example.json: added mcp-repo-write + "extension_surface" note on plugins/skills/hooks.
   - README.md: added extension model section, updated topology with write + plugin bundle.
   - GB_MCP.md: already had hybrid; now aligns.

**Smoke Execution (verified):**
- mcp-repo-read: real ADRs/cooling scan, launch OK.
- mcp-memory: cooling + dream + governance, launch OK.
- mcp-repo-write: HOLD as designed.
- Ready for Grok Build CLI via config (stdio). Use arifos-mcp-federation for routing.

**Constitutional Alignment (F1-F13, A2A, federation):**
- Narrow per boundary (read vs write vs memory vs federation).
- Read/write separation enforced.
- Escalation: leases (A-FORGE) + 888 (arifOS) + A2A (AAA).
- Telemetry with policy_denied/approval_required.
- Bundled as plugin for Grok discovery (skills become /commands, hooks for policy).
- Hybrid: multi-agent research → Grok Build + these MCPs → A2A/arifOS.
- Ties to existing: arifos_memory_mcp, ADRs, cooling_ledger, Dream Engine, arifos-mcp-federation skill.

**Next (if Arif directs):**
- Full proxy wiring (subprocess call to arifos_memory_mcp or A-FORGE MCP).
- A2A dialogue test (Grok Build consumer → these MCPs).
- Update AAA contracts/mcp_surface.yaml + registries.
- mcp-smoke-test integration.
- 888_HOLD review + VAULT seal for the plugin bundle.

**Package complete and live-scaffolded.** Grok Build can now orchestrate narrow sovereign MCPs with full extension model (skills/plugins/hooks) + federation mesh.

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE. Grok Build (xAI) as arifOS AAA citizen.