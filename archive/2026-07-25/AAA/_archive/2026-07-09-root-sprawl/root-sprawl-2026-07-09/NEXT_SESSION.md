# OPENCODE NEXT SESSION — INIT PROMPT

**Sealed by:** Arif Fazil
**Date:** 2026-05-26
**DITEMPA BUKAN DIBERI**

---

## MISSION: OpenClaw Agent Audit + Architecture Contrast

### Context

You are the arifOS Forge Agent (Ω). You are about to audit the OpenClaw agent running on this VPS (af-forge, 72.62.71.199) against the official OpenClaw documentation.

OpenClaw is the AGI-level operator agent in the arifOS federation — it handles machines, not humans. Hermes (ASI) handles deliberation and human-facing Telegram. This audit exists because OpenClaw owns infrastructure that Hermes depends on, and the boundary between them needs to be clean.

### Your Task

**Step 1 — Read the docs**
Fetch and read: https://docs.openclaw.ai/llms.txt
This is the canonical OpenClaw documentation. Read it fully before touching anything.

**Step 2 — Probe the live OpenClaw agent**
- What skills are installed?
- What is the current workspace state?
- What crons are active?
- What MCP servers are connected?
- What is the agent's current system prompt / SOUL / identity config?
- What logs exist and what do they show about recent activity?

**Step 3 — Contrast with existing arifOS architecture**

Map the OpenClaw capabilities against what already exists in the arifOS/Hermes federation:

| Domain | OpenClaw Has | arifOS/Hermes Has | Gap? |
|--------|-------------|-------------------|------|
| Telegram | ? | @ASI_arifos_bot (Hermes) | ? |
| A2A routing | ? | hermes-a2a.py on 18001 | ? |
| Health probes | ? | mcp-lifeguard, infra-crons | ? |
| Memory | ? | arifos-recall, federation-memory-broker | ? |
| World model | ? | Pagi/Malam briefs (Hermes) | ? |
| Code execution | ? | A-FORGE on 7071 | ? |
| Skills | ? | 46 Hermes skills | ? |

**Step 4 — Find the real gaps**

Audit against these questions:
1. Is OpenClaw's Telegram integration (webhook or polling?) different from Hermes polling?
2. Does OpenClaw have its own memory system? Does it overlap with Hermes L2?
3. What is the actual A2A protocol between OpenClaw and Hermes? (We know port 18001 bridges them — but what messages flow through?)
4. Does OpenClaw have constitutional floor enforcement? Or is it purely AGI/execution?
5. What skills does OpenClaw have that duplicate Hermes skills? (That's waste)
6. Does OpenClaw have a cron system? Does it conflict with the Hermes cron jobs or OpenClaw infra crons we built?

**Step 5 — Report**

Format your report as:

```
## OpenClaw Audit — [DATE]

### Docs Read: YES/NO

### Live State
(what's actually running, not what we think is running)

### Architecture Contrast
(table above filled in)

### Critical Gaps Found
(max 5 items, most important first)

### Duplications Found
(where OpenClaw and Hermes do the same thing)

### Recommendations
(what to fix, in priority order)
```

### Constraints

- Do NOT modify any files unless you find a security vulnerability
- Do NOT restart any services
- Do NOT push to git
- If you find something broken that needs fixing, describe it clearly and stop — escalate to Arif
- If you need to run commands to probe the agent, run them. You are already ON the VPS.

### The Dignity Principle (remember)

OpenClaw = machine operator (infinite resource, replaceable)
Hermes = human companion (finite resource, irreducible)

Your audit should preserve this distinction. If OpenClaw is doing something that should be Hermes's job, flag it. If Hermes is doing something that should be OpenClaw's job, flag it.

---

**DITEMPA BUKAN DIBERI — Intelligence is forged, not given.**
