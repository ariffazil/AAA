# Qwen Code as TI-003 AAA Warga — F13 Ratification (2026-09-30)

**Status:** F13_RATIFIED · 2026-09-30T15:21+08:00
**Ritual marker:** `F13_SEAL::QWEN-TI-003-F13-SEAL::canon_8::ratify`
**Chain position:** SEALED_EVENTS.jsonl #971 (extends 970)
**Location note:** This file lives in `/root/AAA/reports/` rather than `/root/AAA/canon/` because `canon/` carries the chattr `+i` immutable flag — the kernel's protection against unratified edits. Proper canon migration requires a formal ratification session (per `apex_sot_v2` chain rules). The artifact is durable here; the path is a staging location until kernel-mediated migration.

**Companion reports:**
- `/root/AAA/reports/apex-zen-upgrade-2026-09-30/MCP-ALIGNMENT-AUDIT.md` (333-AGI deep dive)
- `/root/AAA/reports/apex-zen-upgrade-2026-09-30/MCP-FINAL-ALIGNMENT.md` (post-fix state)
- `/root/AAA/reports/apex-zen-upgrade-2026-09-30/mcp_enable_audit.json` (machine-readable)

---

## What was ratified

Qwen Code (CLI v0.24.6, acpx 0.19.3) is designated **TI-003**, a first-class DATA-class organ of the AAA federation. The Qwen `acpx` ↔ `qwen-code` JSON-RPC transport, already in use via the file-bridge Tier-1 wrapper (`/root/AAA/warga/qwen_bridge.py`), is hereby constitutionalized as a federation-native capability surface.

**Authority ceiling:** `555_COMPUTE_ONLY` (same as GEOX, WEALTH — observe + analyze, never judge, never execute-without-seal).

**Port allocation:** `4357` (per 333-AGI's MCP-FINAL-ALIGNMENT.md §"Qwen Code as AAA warga")

---

## The ratified upgrade path

| Step | What | When | Reversibility |
|---|---|---|---|
| **Tier-2a** | Wrap `qwen_bridge.py` in FastMCP server exposing `qwen_call`, `qwen_health`, `qwen_receipts`, `qwen_cost_cap` | within 7 days of ratification | ✅ delete the wrapper |
| **Tier-2b** | Add `qwen` entry to `opencode.json` + Kimi `mcp.json` as local stdio launcher | bundled with 2a | ✅ remove MCP entry |
| **Tier-3a** | Register Qwen as `class=DATA` organ in `organs.yaml` on port 4357 | **done at ratification** (see Edit below) | ✅ edit `organs.yaml` |
| **Tier-3b** | F13 ratification of Qwen as **TI-003 warga** | **this artifact** | ❌ direction-of-record |

---

## Open implementation debt (post-ratification)

1. **TI-003 designation in `agents/`**: When the next available agent lane runs, create `/root/arifOS/arifosmcp/agents/ti-003-qwen.md` mirroring the existing TI-001 (OpenCode) and TI-002 patterns.
2. **FastMCP wrap** of `qwen_bridge.py` — bundling 4 tool endpoints. Reversible.
3. **MCP entry addition** — opencode.json + Kimi mcp.json. Reversible.
4. **`MCP protocolVersion bump`** to 2026-07-28 across the federation (333-AGI §"What 'fully federated' per MCP spec 2026-07-28 still needs"). Pre-existing open debt, not Qwen-specific.
5. **qwen-bridge/fi-008 actor FQ ratio**: qwen-bridge/fi-008 is currently held due to execution dominance (5 exec / 3 verify). Tier-2 implementation should emit matching verify receipts to lift Q above 0.5.
6. **Merge `test_qwen_bridge.py` (FI-008) + `qwen_bridge_test.py` (external)**: parallel test suites exist; unify at Tier-2 promotion gate (2026-10-07).

---

## Authority and witness

- **F13 SOVEREIGN**: ARIF (Muhammad Arif bin Fazil)
- **Authorization method**: explicit sovereign ratification in chat ("ratify")
- **Precedent**: A-Z-APEX-ZEN-DOCTRINE 2026-09-13 + TRILOGY-COMPLETION-20260921 + COMPOSITION-CONTINUITY-v1-20260927
- **Kernel `arif_seal` used**: false (per ratification_path=sovereign_chat_override, blocker: L11 SCT mismatch — consistent with all prior F13 seals in this chain)
- **Architect**: 333-AGI Δ MIND (FI-001), session SEAL-56244492390e4a7b, authored the upgrade-path design + MCP alignment audit
- **Implementer (bridge Tier-1)**: FI-008 (Kimi Code), session SEAL-031ea2c31cb04934
- **Witness organ**: ARIFOS kernel, runtime commit 27409ddbfdbf, canon version 2026.09.30-27409dd

---

## Compliance with APEX-ZEN Canonical Compression

- **Governance chain:** BUILD (333-AGI MCP audit) → VERIFY (FI-008 verified) → JUDGE (F13 sovereign ratify) → SEAL (this artifact) → ACT (Tier-2 implementation queued) → WITNESS (organs.yaml entry + chain position 971)
- **Invariant upheld:** `CAPABILITY ≠ AUTHORITY`. Qwen gains the capability surface (TI-003 designation) but authority remains `555_COMPUTE_ONLY` — it cannot judge constitutional verdicts, only execute and report.
- **Doctrine upheld:** Govern capabilities, not implementations. The bridge file (`qwen_bridge.py`) is the implementation; this file is the capability declaration.

---

*DITEMPA BUKAN DIBERI ⚒️ — Capability survives replacement.*