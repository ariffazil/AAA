---
name: concept-arifOS-loop-architecture
version: 1.0.0-2026.06.25
title: "arifOS Loop Architecture — Canonical Operational Loops"
type: concept
tags: [loop, architecture, cron, watchdog, metabolic, hermes, forge, wealth, federation, operational]
author: FORGE (000Ω)
date: 2026-06-25
status: canonical
related_concepts:
  - intelligence-tree
  - concept-memory-knowledge-loop
  - concept-agent-skills-architecture
loops_references:
  - LOOP-001: Metabolic session loop
  - LOOP-002: Hermes pagi brief
  - LOOP-003: Hermes evening digest
  - LOOP-004: Federation health watchdog
  - LOOP-005: WEALTH daily compute
  - LOOP-006: WEALTH RSI scaffold
  - LOOP-007: Suriname FID watch
  - LOOP-008: Petronas lingkup watch
  - LOOP-009: Skill audit cycle
  - LOOP-010: A-FORGE build pipeline
  - LOOP-011: AAA agent onboarding
---

# arifOS Loop Architecture

> **Part of:** [[intelligence-tree]] — the operational loop layer
> **Supersedes:** ad-hoc cron + undocumented automation
> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.

## One-Line Definition

A **loop** in arifOS is a recurring, governed, reversible sequence of skills
that transforms reality under constitutional floors, with explicit writer/auditor
separation, a defined frequency or trigger, and a VAULT999 receipt.

## The Five Loop Classes

| Class | Trigger | Writer | Auditor | Example |
|-------|---------|--------|---------|---------|
| **METABOLIC** | Every session | Agent | AUDITOR/kernel | 000→999 session |
| **CRON** | Time-based | Hermes/Forge | AUDITOR | Pagi brief, watchdog |
| **EVENT** | MCP signal | Organ | arifOS kernel | arif_seal, arif_judge |
| **DEMAND** | Human request | Any agent | AUDITOR | Forge task |
| **WATCHDOG** | Threshold breach | OPS/organ | AUDITOR | Disk >80%, organ DOWN |

## The Key Insight

**Loop engineering (external) = engineering recurrence.**
**arifOS reality engineering = engineering reality constraints.**

Loops automate motion. Reality engineering governs the laws that motion must obey.
arifOS loop architecture is a constitutional superset of loop engineering.

## The arifOS Loop Primitives

Every loop is defined by:

| Primitive | Description | Example |
|-----------|-------------|---------|
| `TRIGGER` | What wakes the loop | `cron: 0 8 * * 1-5` |
| `PIPELINE` | Ordered steps | `SENSE → REASON → CRITIQUE → SEAL` |
| `GUARDS` | Constitutional floors active | `F1, F2, F6, F9` |
| `WRITER` | Agent responsible | `Hermes`, `FORGE` |
| `AUDITOR` | Agent that reviews | `AUDITOR`, `arifOS kernel` |
| `COST` | Token cost per run | `~$0.10–0.30` |
| `TOKEN_BUDGET` | Max context | `8K context` |
| `TERMINATION` | How loop ends | `VAULT999 + Telegram` |
| `RECEIPT` | Where outcome is recorded | `VAULT999 outcomes` |

## The 11 Canonical Loops

### LOOP-001: METABOLIC SESSION LOOP
```
TRIGGER:  New conversation or session_init
WRITER:   Agent (OpenCode, Kimi, Claude Code)
AUDITOR:  AUDITOR (Ψ) or arifOS kernel
GUARDS:   F1, F2, F11
PIPELINE: 000_INIT → 111_SENSE → 333_REASON → 555_JUDGE → 666_CRITIQUE → 777_FORGE → 999_SEAL
COST:     ~$0.50–2.00 per session
RECEIPT:  VAULT999 outcomes entry
```

### LOOP-002: HERMES PAGI BRIEF
```
TRIGGER:  cron: 30 07 * * 1-5 (Mon-Fri 07:30 MYT)
WRITER:   Hermes
AUDITOR:  AUDITOR (cultural gap — RSI-LOOP-01)
GUARDS:   F2, F5, F6, F9
PIPELINE: SENSE → REASON → CRITIQUE → COMPOSE → DELIVER → SEAL
COST:     ~$0.10–0.30 per run
RECEIPT:  VAULT999 outcomes
```

### LOOP-003: HERMES EVENING DIGEST
```
TRIGGER:  cron: 0 19 * * * (daily 19:00 MYT)
WRITER:   Hermes
AUDITOR:  AUDITOR (gap — RSI-LOOP-01)
PIPELINE: SENSE → COMPOSE → DELIVER → SEAL
COST:     ~$0.05–0.15 per run
```

### LOOP-004: FEDERATION HEALTH WATCHDOG
```
TRIGGER:  cron: */5 * * * * (every 5 minutes)
WRITER:   OPS (🌐) or Hermes
AUDITOR:  AUDITOR
GUARDS:   F2 (liveness only, no mutation)
PIPELINE: for each organ → curl health → alert if ❌ → SEAL
COST:     ~$0.01 per run
```

### LOOP-005: WEALTH DAILY COMPUTE
```
TRIGGER:  cron: 0 8 * * 1-5 (daily 08:00 MYT)
WRITER:   WEALTH organ
AUDITOR:  arifOS kernel
GUARDS:   F1 (read-only), F2, F13
PIPELINE: market_data → cache → SEAL
COST:     ~$0.05–0.20 per run
```

### LOOP-006: WEALTH RSI SCAFFOLD RUN
```
TRIGGER:  Post-FORGE session or weekly
WRITER:   FORGE (000Ω)
AUDITOR:  AUDITOR (Ψ)
GUARDS:   F1, F2, F4, F11
PIPELINE: git log → pytest → ruff → identify RSI → write scaffold → SEAL
COST:     ~$0.30–0.80 per run
```

### LOOP-007: SURINAME FID WATCH
```
TRIGGER:  cron: 0 9 1 * * (monthly) + event
WRITER:   Hermes
AUDITOR:  arifOS kernel
GUARDS:   F2, F9
PIPELINE: SENSE (3 indicators) → flag → alert if triggered → SEAL
COST:     ~$0.05–0.20 per run
NOTE:     RSI-04 — not yet active
```

### LOOP-008: PETRONAS LINGKUP WATCH
```
TRIGGER:  cron: 0 9 1 */3 * (quarterly) + event
WRITER:   WEALTH organ + FORGE
AUDITOR:  AUDITOR + arifOS kernel
GUARDS:   F2, F6 (MARUAH — no individuals named), F9
PIPELINE: SENSE → collapse_scan (PDVSA priors) → quarterly brief → SEAL
COST:     ~$0.50–1.50 per run
NOTE:     RSI-05 — not yet active
```

### LOOP-009: SKILL AUDIT CYCLE
```
TRIGGER:  cron: 0 2 1 * * (monthly 1st)
WRITER:   AUDITOR (Ψ)
AUDITOR:  FORGE (000Ω)
GUARDS:   F1 (read-only), F2, F4, F11
PIPELINE: audit skills/*.md → validate frontmatter → detect drift → SEAL
COST:     ~$0.20–0.60 per run
```

### LOOP-010: A-FORGE BUILD PIPELINE
```
TRIGGER:  GitHub PR merge OR manual forge_dry_run
WRITER:   FORGE (000Ω)
AUDITOR:  arifOS kernel (arif_judge)
GUARDS:   F1 (backup), F2 (evidence), F13 (irreversible = HOLD)
PIPELINE: dry_run → arif_judge → HOLD or proceed → pytest/ruff → deploy → SEAL
COST:     ~$1.00–5.00 per production deploy
```

### LOOP-011: AAA AGENT ONBOARDING
```
TRIGGER:  Skill load of agentic-builder or federation-router
WRITER:   FORGE (000Ω) + AAA
AUDITOR:  arifOS kernel
GUARDS:   F1, F2, F6, F9, F11, F13
PIPELINE: create agent → bind organ → constitutional tether → first ignition → SEAL
COST:     ~$2.00–10.00 per new agent
```

## Write/Audit Separation (Critical Gap)

Per Addy Osmani: *"The model that wrote the code is way too nice grading its own homework."*

| Loop | Writer | Auditor | Status |
|------|--------|---------|--------|
| METABOLIC SESSION | Agent | AUDITOR/kernel | ✅ Structural |
| HERMES PAGI BRIEF | Hermes | — | ❌ RSI-LOOP-01 |
| HERMES EVENING | Hermes | — | ❌ RSI-LOOP-01 |
| FEDERATION HEALTH | OPS/Hermes | AUDITOR | ✅ |
| WEALTH COMPUTE | WEALTH | kernel | ✅ |
| WEALTH LINGKUP | WEALTH+FORGE | AUDITOR+kernel | ✅ |
| A-FORGE BUILD | FORGE | kernel (arif_judge) | ✅ |
| SKILL AUDIT | AUDITOR | FORGE | ✅ Cross |

## Cost Tiers

| Tier | Cost | Approval |
|------|------|----------|
| T1: Probe/Sense | $0.01–0.05 | None |
| T2: Compose/Audit | $0.10–0.50 | None |
| T3: Build | $0.50–2.00 | ANNOUNCE (10s) |
| T4: Production Deploy | $1.00–5.00 | arifOS judgment |
| T5: Irreversible | — | F13 SOVEREIGN ack |

## RSI Items

| # | Gap | Severity |
|---|-----|----------|
| RSI-LOOP-01 | Hermes loops need explicit auditor | HIGH |
| RSI-LOOP-02 | No unified loop manifest | MEDIUM — this doc |
| RSI-LOOP-03 | No per-loop cost tracking in VAULT999 | MEDIUM |
| RSI-LOOP-04 | Suriname watch not active | MEDIUM |
| RSI-LOOP-05 | Petronas lingkup quarterly not active | MEDIUM |
| RSI-LOOP-06 | No `/goal`-equivalent | LOW |
| RSI-LOOP-07 | Skills not tagged `loop_class` | LOW |

## Quick Reference: LOOP_MAP

```
METABOLIC
└── LOOP-001: Session loop (000→999) — every session

CRON (time-based)
├── LOOP-002: Hermes pagi brief — daily 07:30 MYT
├── LOOP-003: Hermes evening digest — daily 19:00 MYT
├── LOOP-004: Federation health watchdog — every 5 min
├── LOOP-005: WEALTH daily compute — daily 08:00 MYT
├── LOOP-007: Suriname watch — monthly + event
├── LOOP-008: Petronas lingkup watch — quarterly
├── LOOP-009: Skill audit cycle — monthly
└── LOOP-011: Agent onboarding — on-demand

EVENT (signal-based)
├── arif_seal → VAULT999 write
├── arif_judge → constitutional verdict
└── organ_failure → watchdog alert

DEMAND (human request)
└── LOOP-010: A-FORGE build pipeline — on PR merge
```

## Related Pages

- [[intelligence-tree]] — 7-layer tree (where loops live)
- [[concept-memory-knowledge-loop]] — cognitive loop (memory↔knowledge)
- [[concept-agent-skills-architecture]] — skills as first-class citizens
- [[anti-fabrication-protocol]] — the skill that came from a scar

---

*Source: `/root/forge_work/loop-engineering-audit-2026-06-25/arifOS_LOOP_ARCHITECTURE.md`*
*DITEMPA BUKAN DIBERI — Forged, Not Given.*
*999 SEAL ALIVE — Reality is forged, not given.*
