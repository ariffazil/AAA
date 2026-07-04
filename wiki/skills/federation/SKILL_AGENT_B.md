---
title: "SKILL: Agent Onboarding"
created: 2026-05-17
updated: 2026-05-17
version: 0.1.0
type: skill
tags: [onboarding, federation, agent-config, spatial-grounding, constitutional]
category: infra
risk_band: HIGH
floors: [F1, F7, F9, F11, F12]
evidence_required: true
sources: []
confidence: low
status: stub
---

# SKILL: Agent Onboarding

> **Skill ID:** `skill-agent-onboarding`
> **Canonical location:** `AAA/wiki/skills/SKILL_AGENT_2.md`
> **Status:** STUB — requires full procedure development
> **When to use:** When installing a new agent binary (Claude, Gemini, Kimi, OpenCode, Copilot, Codex)
> **Severity:** HIGH — unconfigured agents are unsafe agents

---

## Summary

Full procedure for onboarding a new agent to the arifOS federation: spatial grounding + constitutional prompt + tool access + verification.

---

## TODO: Procedure (not yet written)

### Step 1: Install agent binary
- [ ] Verify binary source (official渠道, not third-party)
- [ ] Place in standard location (`/usr/local/bin/` or `~/.local/bin/`)
- [ ] Verify checksum if available

### Step 2: Create spatial grounding config
- [ ] Run [[skill-spatial-grounding]] — embed SPATIAL_LAW in agent config
- [ ] Verify: `grep "72.62.71.199" <config-file>` returns match

### Step 3: Embed constitutional floors
- [ ] Append F1-F13 floor summary to system prompt
- [ ] Include boot sequence: ROOT_CANON → SOUL → USER → AGENTS → IDENTITY → MEMORY
- [ ] Include 888_HOLD triggers

### Step 4: Configure tool access
- [ ] Identify available tool interfaces (MCP, CLI, API)
- [ ] Map to arifOS kernel stages (000-999)
- [ ] Document in [[federation-entities]]

### Step 5: Verify onboarding
- [ ] Agent responds to identity query correctly
- [ ] Agent knows it runs on VPS 72.62.71.199 (not SSH target)
- [ ] Agent can list available tools without claiming non-existent access
- [ ] VAULT999 onboarding entry logged

---

## Preconditions

- Agent binary available and hash-verified
- Target config file location known
- VAULT999 access confirmed
- [[federation-entities]] up to date

---

## Expected Outputs

- Agent config file patched with SPATIAL_LAW + constitutional floors
- Verification commands return expected output
- [[federation-entities]] updated with new agent entry
- VAULT999 outcome logged
- `AAA/wiki/LOG_MD.md` entry created

---

## Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Binary source untrusted | Do not proceed; report to sovereign |
| Config file not writable | Check permissions; escalate |
| Agent ignores config | Restart session; check config path |
| Agent claims non-existent tools | Run anti-fabrication check; [[anti-fabrication-protocol]] |

---

## Related Pages

- [[skill-spatial-grounding]] — first step (spatial grounding)
- [[anti-fabrication-protocol]] — third step (verify before claiming)
- [[federation-entities]] — update with new agent entry
- [[scar-hermes-fabrication-2026-05-17]] — why verification is mandatory

---

## Stub Author Notes

This is a STUB. The full procedure requires:
1. A canonical list of all agent config file locations (from federation-entities)
2. The exact F1-F13 floor text to embed
3. The standard boot sequence text
4. A verification checklist

**Next step:** Fill in procedure after [[federation-entities]] is confirmed complete.

*DITEMPA BUKAN DIBERI — Unconfigured agents are unsafe agents.*
