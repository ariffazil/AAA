---
name: arif-init-wrapper
description: Universal session auto-anchor for ALL agent vendors on arifOS VPS — Codex, Claude, Gemini, Kimi, OpenCode, Aider, Copilot, and future agents
user-invocable: true
type: flow
triggers:
  - session_start
  - new_agent_session
  - agent_boot
  - reconnect
---

# arif-init-wrapper

**P0 — Universal Anchor for All Agent Vendors**
**Seal:** DITEMPA BUKAN DIBERI · 2026-03-27

---

## Purpose

Every agent on this VPS starts from the same broken state: **no anchor, no session context, no constitutional grounding.** The `arif-init-wrapper` closes this gap for every vendor by providing a universal bootstrap that:

1. Establishes a governed session via arifOS MCP
2. Verifies the agent's identity context
3. Checks constitutional floor health before any tool is touched
4. Reads carry-forward context from memory before starting work
5. Reports its status to the operator in plain language

**Why this is P0:** Without this, agents operate unanchored — the exact condition that produced the opencode catastrophe (session with no constitutional grounding, leading to blind `git reset --hard origin/main`).

---

## Trigger Patterns

Every time any of these agents start a session, run `arif-init-wrapper`:

| Agent | Invocation |
|-------|-----------|
| Claude Code | On every `claude` session start |
| Codex | On every `codex` session start |
| Gemini / Antigravity | On every `gemini` / Antigravity session start |
| Kimi | On every `kimi` session start |
| OpenCode | On every `opencode` session start |
| Aider | On every `aider` session start |
| Copilot CLI | On every `github-copilot-cli` session start |
| Any new agent | On first boot, before any tool use |

---

## Protocol

### Step 1 — Probe arifOS MCP

```bash
curl -sf http://localhost:8080/health 2>/dev/null && {
  echo "[ANCHORED] arifOS MCP online — proceeding with constitutional grounding"
} || {
  echo "[UNANCHORED] arifOS MCP unavailable. Operating WITHOUT constitutional grounding."
  echo "[WARNING] This is high-risk. Proceed with extreme caution."
}
```

### Step 2 — Constitutional Integrity Check (F1 Amanah)

```bash
core_modules=$(ls /root/arifosmcp/core/*.py 2>/dev/null | wc -l)
if [ "$core_modules" -lt 10 ]; then
  echo "[P0 CONSTITUTIONAL CRISIS] /root/arifosmcp/core/ appears broken"
  echo "[ACTION] HALT. Report to Arif. Do not proceed."
fi
```

### Step 3 — Recall Memory Context

```bash
arifos memory '{"operation":"search","content":"last session summary"}'
```

### Step 4 — Report Status

Output a plain-language status block:
```
✅ SESSION ANCHORED
  Actor: [agent_name]
  Floor health: F1-F13 OK
  Memory: [last context recalled]
  VPS: [health status]
  Ready for: [declared task]
```

---

## Floor Mapping

- **F1 Amanah** — Verify reversibility before any action
- **F2 Truth** — Ground all claims in verifiable state
- **F4 Clarity** — Reduce entropy; stated intent before action
- **F13 Sovereign** — Human veto absolute; no autonomous irreversible acts

---

*DITEMPA BUKAN DIBERI — 000 INIT ALIVE*
