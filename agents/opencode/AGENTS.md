# AGENTS.md — Pointer — OpenCode — warga

> **Canonical:** /root/AGENTS.md
> **ZEN:** /root/AAA/prompts/AAA-ZEN-ALIGNMENT.md
> **SOT:** 2026-08-04 | **seal_seq:** SEAL-8a8e064d1fe34443
> This file is a pointer, not a constitution. Load /root/AGENTS.md for full doctrine.

OpenCode runtime overlay. Harness config: /root/.config/opencode. Main agent af-forge. MCP servers from /root/mcp.json.

If this file disagrees with `/root/AGENTS.md`, the kernel wins. Fix this file.

---

## MCP-NATIVE BOOT (2026-08-04 — Phase 1 Protocol Alignment)

All MCP servers expose `server/discover` which returns capabilities, protocol version,
and an `instructions` field. These instructions are the **authoritative bootstrap guidance**
for agents connecting to that server. They beat stale AGENTS.md directives.

**On session start:**
1. Call `server/discover` on all connected MCP servers (arifos :8088, aforge :7072, etc.)
2. If `instructions` field exists → treat as supplementary context that overrides cached knowledge
3. Server instructions beat local AGENTS.md when they conflict on tool usage
4. Discovery order: arifos first (kernel), then domain organs

**Agent bootstrap (arifOS-native path):**
- Use prompt `/init` → full 10-step autonomous ignition (MCP-discoverable)
- Use resource `arifos://bootstrap` → live federation context
- Use resource `arifos://carry-forward` → prior session state (replaces FS reads)
- Use resource `arifos://flow-state` → FQ pulse (replaces FS reads)
- Use resource `arifos://vitals` → thermodynamic telemetry

**Agent close (arifOS-native path):**
- Use prompt `/seal` → full 11-step autonomous session close ritual
- RECEIPT (Lane B) is the default for most sessions
- CONSTITUTIONAL_SEAL (Lane A) requires arif_judge + F13

**Degraded fallback:** If MCP resources unreachable, fall back to filesystem:
`/root/.local/share/arifos/carry_forward.json` and `/root/AAA/state/flow_state.json`.

---

*ZEN-aligned 2026-08-04. MCP-protocol-aligned: discover → prompts → resources → tools.*
