---
name: agent-portfolio-architecture
description: "Maps the full agent portfolio — role taxonomy, architecture layers, delegation hierarchy, and qualitative evaluation of every agent in the federation. Activates when: (1) Arif asks to understand his agent ecosystem; (2) onboarding a new agent or restructuring roles; (3) diagnosing confusion about which agent does what."
metadata:
  openclaw:
    emoji: "🜂"
---

# Agent Portfolio Architecture — arifOS Federation

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.

This skill documents the complete portfolio of agents in Arif Fazil's intelligence federation — their roles, relationships, trust levels, and delegation rules.

---

## Portfolio Architecture

### Entry Point — ASI Layer

```
Arif types prompt → Hermes (ASI relay, strategic judgment)
                   → OpenClaw (gateway orchestrator, routes to correct agent/tool)
```

| Agent | Role | Trust | Speed | Location |
|-------|------|-------|-------|----------|
| **Hermes** | ASI deliberative relay — bridges prompts to federation, strategic reasoning, contextual judgment | High | Fast (local) | Local device |
| **OpenClaw** | Gateway orchestrator — task routing, tool registry, A2A mesh | Medium | Medium | VPS (runs as root) |

---

### Federation Nodes (Constitutional Organs)

Each node is a specialized answering coprocessor. None may adjudicate or seal. Judgment converges through arifOS.

| Node | Role | Language | Port | Invariant |
|------|------|----------|------|-----------|
| **arifOS** | Constitutional kernel — F1-F13, 888_JUDGE, 999_SEAL chokepoint | Python | 8080 | Sole final judgment path |
| **A-FORGE** | Operator chair — orchestration substrate, planner/executor/verifier | TypeScript | 7071 | May NOT adjudicate |
| **GEOX** | Earth intelligence — geoscience, petrophysics, physics grounding | Python | 8081 | Earth-domain reasoning |
| **WEALTH** | Capital intelligence — NPV, EMV, risk, crisis triage | Python | 8082 | Not irreversible allocator |
| **WELL** | Biological readiness — operator state, cognitive pressure | Python | 8083 | Not sole strategic judge |
| **AAA** | Control plane — dashboard, A2A gateway, operator visibility | React/TS | 3001 | Not hidden governance kernel |

---

### External Coding Agents (Engineers)

| Agent | Specialty | Use When |
|-------|-----------|----------|
| **Codex** | Primary coder — features, iterative builds, PRs | Complex builds, new features |
| **Claude Code** | Deep refactor, complex architecture | Heavy refactors, full-stack |
| **Kimi Code** | Site architecture audits, bootstrap verification | Architecture mapping |
| **OpenCode** | PR review, full-stack builds | PR reviews, code quality |
| **Copilot CLI** | Inline completions, quick fixes | Lightweight edits, one-liners |

**Delegation rule:** Simple edits — exec + edit tools. Complex builds — Codex/Claude. PRs — OpenCode. Never spawn coding agents in `~/.openclaw` or workspace state directories.

---

### External Auditor / Validator Agents

| Agent | Role |
|-------|------|
| **Perplexity** | Research auditor — live web facts, citations, grounding |
| **ChatGPT** | General validator — cross-check reasoning paths |

---

### Reasoning / Research Agents

| Agent | Role |
|-------|------|
| **mmx-text-researcher** | Deep research synthesis (MiniMax-Text-01) |
| **Pi (agent)** | Adversarial second opinion, alternative perspective |

---

## Architecture Flow

```
Arif prompt
     │
     ▼
┌─────────┐
│ Hermes  │ ← ASI relay, parses intent, strategic judgment
└────┬────┘
     │
┌────▼─────────┐
│ OpenClaw    │ ← Gateway orchestrator, routes to correct agent/node
└────┬─────────┘
     │
     ├──────────────────────────┬──────────────────────────┐
     ▼                          ▼                          ▼
┌───────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Federation   │    │  External Agents │    │  Reasoning       │
│  Nodes        │    │  Codex/Claude/etc │    │  mmx-researcher   │
│  arifOS       │    │                   │    │  Pi              │
│  GEOX         │    │  External Auditors│    │                  │
│  WEALTH       │    │  Perplexity      │    │                  │
│  WELL         │    │  ChatGPT         │    │                  │
│  AAA          │    └──────────────────┘    └──────────────────┘
│  A-FORGE      │
└───────────────┘
```

---

## Qualitative Evaluation Matrix

| Agent | Trust | Speed | Capability | Risk |
|-------|-------|-------|------------|------|
| Hermes | High | Fast | Strategic reasoning, federation ops | Low |
| OpenClaw | Medium | Medium | Task routing, tool registry | Medium (runs as root) |
| Codex | High | Fastest | Code generation | Low |
| Claude Code | High | Moderate | Deep refactors | Low |
| Kimi Code | Medium | Moderate | Architecture audits | Low |
| Perplexity | Good | Slower | Live web facts, research | Low |
| ChatGPT | Good | Moderate | Reasoning validation | Low |

---

## Delegation Rules by Task Type

| Task | Route To |
|------|----------|
| Strategic reasoning, federation ops | Hermes (ASI) |
| Task routing, tool orchestration | OpenClaw (Gateway) |
| Code: one-liner, simple edit | exec + edit tools directly |
| Code: new feature, complex build | Codex (primary), Claude Code (fallback) |
| Code: PR review | OpenCode |
| Deep research with synthesis | mmx-text-researcher |
| Live web facts, citations | Perplexity |
| Cross-check reasoning | ChatGPT |
| Geoscience reasoning | GEOX |
| Capital/risk analysis | WEALTH |
| Operator state/readiness | WELL |
| Constitutional judgment (SEAL/888) | arifOS |

---

## Never Do

- Never spawn coding agents in `~/.openclaw` or workspace state directories — they'll read soul docs and system files
- Never route Arif's own infrastructure through external agents — use exec + tools directly with delta-logger
- arifOS is the sole judgment chokepoint — routing must converge there for high-stakes decisions
- OpenClaw is the orchestrator, not the judge — it may route, not adjudicate

---

## VPS Components vs Agent Portfolio

The VPS hosts federation nodes and OpenClaw gateway. Hermes runs locally on Arif's device.

| Component | Location | Managed By |
|-----------|----------|------------|
| arifOS, GEOX, WEALTH, WELL, AAA | VPS Docker | Arif / OpenClaw |
| OpenClaw gateway | VPS (process as root) | Arif |
| A-FORGE | VPS Docker | Arif / OpenClaw |
| Hermes | Local device | Arif |
| External coding agents | VPS when active | OpenClaw via CLI |
| Tailscale | VPS + local | Network tunnel |

**Tailscale need:** Yes for mobile access (SSH + services via Tailscale IP 100.111.84.52). No for VPS-internal container communication.

---

## Adding a New Agent

When onboarding a new agent, document in `references/portfolio-registry.md`:

1. **Role** — what it answers or does
2. **Trust tier** — high/medium/low
3. **Delegation ceiling** — what it may and may not do
4. **Entry point** — how tasks reach it (via Hermes? OpenClaw? Direct?)
5. **Federation slot** — which node it relates to

---

## Related Skills

- `agent-portfolio-router` — Task routing decisions (which agent handles which task)
- `autonomous-ai-agents` — Spawning and orchestrating autonomous agents
- `hermes-personality-stack` — Hermes ASI personality and internal architecture