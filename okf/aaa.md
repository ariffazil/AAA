---
type: System
title: AAA Control Plane
description: Control plane, A2A gateway, and cockpit dashboard for the arifOS federation. STATE/ROUTING axis of the Trinity-33
resource: http://localhost:3001/health
tags: [federation, control-plane, a2a, cockpit, routing]
timestamp: 2026-07-20T08:00:00Z
links:
  - ../atlas333.md
  - ../skills/index.md
  - ../skills/layers.md
---
# AAA (Control Plane)

Trinity-33 Axis: STATE / ROUTING / VISIBILITY

## What it does

AAA is the **control plane** of the federation. It:

- **Routes** — Agent-to-agent (A2A) protocol gateway
- **Displays** — Cockpit dashboard for federation status
- **Identity** — Agent cards, registry, canonical identity
- **Coordinates** — Cross-organ work dispatch
- **Skills** — Hosts the canonical skill catalog (156+ skills)
- **Governance** — AAA_HUMAN_SPEECH_RULE, ADAT_AGENTIC, federation protocol

## Agent Citizens (Warga AAA)

| ID | Agent | Role |
|----|-------|------|
| 333-AGI | OpenCode / Claude Code | Reason + Plan + Execute |
| 555-ASI | Hermes | Sovereign conversation, multi-modal |
| 888-APEX | Judge / Deliberation | Constitutional verdict (decommissioned port 3002, now in AAA deliberation engine) |
| A-AUDIT | Auditor | Recursive audit, drift detection |
| A-ARCHIVE | Archiver | Civilizational memory preservation |

## Port

`:3001` — React 19 + Vite 8 + A2A gateway

## Key Paths

- `/root/AAA/` — Source
- `/root/AAA/skills/` — Canonical AAA skill catalog (linked to /root/.agents/skills/)
- `/root/AAA/agents/` — Agent identity directories
- `/root/AAA/prompts/` — Canonical agent INIT prompts
- `/root/AAA/governance/` — Governance doctrine files
