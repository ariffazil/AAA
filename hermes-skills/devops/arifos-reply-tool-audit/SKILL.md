---
name: arifos-reply-tool-audit
description: Audit the arifOS reply_compose tool (arif_reply_compose) — trace the full call chain, find manifest drift, and map kernel vs agent layer separation. Activate when auditing or updating arifOS reply tools.
---

# arifOS Reply Tool Audit

## Purpose
Audit the `arif_reply_compose` tool (444r_REPLY) and related reply composition infrastructure in arifOS. This skill captures the specific file-tracing approach used to audit the tool and its relationship to the Hermes/AAA agent reply layer.

## Audit Chain (File Tracing Order)

When auditing arifOS reply tools, follow this chain:

```
1. server.py                          → MCP server entry point, FastMCP registration
2. arifosmcp/runtime/tools.py          → CANONICAL_TOOL_HANDLERS, _arif_reply_compose_tool
3. arifosmcp/runtime/reply_compose.py  → LLM-powered text composer (444r)
4. arifosmcp/tools/manifests/tool_manifest.json  → safe_modes, dangerous_modes, metadata
5. arifosmcp/runtime/output_formatter.py  → format_output(), platform dispatch
6. arifosmcp/runtime/rest_routes.py    → REST endpoint aliases
7. arifosmcp/runtime/public_registry.py  → public tool registry
8. arifosmcp/runtime/floor.py         → RequestType.REASON, floor enforcement
```

## The arifOS Reply Composition Architecture

### Two-Layer Model (Critical)

```
┌─────────────────────────────────────┐
│  Hermes/AAA Agent Layer             │
│  - Reply structurer                 │
│  - To/CC/Title/Verdict routing     │
│  - 9 modes: HEALTH..META           │
│  - ✅ SEAL / ⚠️ SABAR / 🛑 VOID    │
└──────────────┬──────────────────────┘
               │ calls arif_reply_compose
               │ with mode="compose"
               ▼
┌─────────────────────────────────────┐
│  arifOS Kernel Layer                │
│  - Text composer (444r_REPLY)       │
│  - Applies F02/F04/F06/F07         │
│  - 6 modes: compose/style/cite/... │
│  - SEAL / HOLD / VOID              │
│  - RESPONSE_SCHEMA output          │
└─────────────────────────────────────┘
```

**Never conflate these layers.** The kernel is a text engine. The agent layer is a communication router.

## Verdict Bridge (Kernel → Agent)

| arifOS Kernel | Agent Layer | Meaning |
|---------------|-------------|---------|
| SEAL | ✅ SEAL | Approved, proceeding |
| HOLD | ⚠️ SABAR | Wait, uncertainty, not ready |
| VOID | 🛑 VOID | Denied, blocked, cannot do |

**Note:** `SABAR` is an agent-layer concept only. The kernel does not know SABAR.

## File Audit Checklist

When auditing `arif_reply_compose`:

- [ ] Read `server.py` — how is tool registered with FastMCP?
- [ ] Read `arifosmcp/runtime/tools.py` — how does `_arif_reply_compose_tool` route modes?
- [ ] Read `arifosmcp/runtime/reply_compose.py` — what are the actual valid modes?
- [ ] Read `tool_manifest.json` — do safe_modes match the code?
- [ ] Check `arifosmcp/runtime/output_formatter.py` — how is platform dispatch done?
- [ ] Check `arifosmcp/runtime/rest_routes.py` — what REST aliases exist?
- [ ] Check `arifosmcp/runtime/floor.py` — what RequestType is assigned?

## Known Audit Findings (2026.05.03)

### Finding 1 — Manifest Drift (BUG)
**File:** `tool_manifest.json`
**Issue:** `arif_reply_compose` safe_modes = `["compose"]` but code has 6 modes
**Code modes:** compose, style, cite, summary, format, nudge
**Fix:** Update manifest to include all 6 modes

### Finding 2 — Verdict Terminology Gap
**Issue:** Kernel returns SEAL/HOLD/VOID; agent layer uses ✅/⚠️/🛑
**Fix:** Agent layer must translate — this is by design, not a bug. Document the bridge.

### Finding 3 — Output Schema Gap
**File:** `reply_compose.py` RESPONSE_SCHEMA
**Issue:** Schema has no To/CC/Title/Seal fields — these belong at agent layer
**Fix:** None needed — correct by design

## Mode Comparison: Kernel vs Agent Layer

| Aspect | arifOS Kernel | Hermes/AAA Agent |
|--------|--------------|-----------------|
| Modes | compose, style, cite, summary, format, nudge | HEALTH, INCIDENT, PROPOSAL, ESCALATE, AUDIT, PLAN, EXPLAIN, DENY, META |
| Purpose | Text transformation | Communication intent |
| Floors | F02, F04, F06, F07 | All 13 floors |
| Output | `composed`, `tone`, `delta_S`, scores | Full To:/CC:/Title:/Verdict:/Seal: reply |

## Quick Audit Commands

```bash
# Check what modes are in the code
grep "_MODE_PROMPTS" /root/arifOS/arifosmcp/runtime/reply_compose.py

# Check what modes are in the manifest
grep -A5 '"arif_reply_compose"' /root/arifOS/arifosmcp/tools/manifests/tool_manifest.json

# Check tool registration in server.py
grep "reply_compose\|arif_reply" /root/arifOS/server.py

# Check floor enforcement
grep "arif_reply_compose" /root/arifOS/arifosmcp/runtime/floor.py

# Check REST aliases
grep "arif_reply_compose" /root/arifOS/arifosmcp/runtime/rest_routes.py
```

## Trigger
Use this skill when:
- Auditing or updating arifOS reply composition tools
- Investigating mismatches between tool manifests and actual code
- Understanding the relationship between arifOS kernel and Hermes/AAA agent layers
- Fixing arifOS reply tool bugs or adding new modes
