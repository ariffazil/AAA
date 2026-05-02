# AAA Charter

> **DITEMPA BUKAN DIBERI** — *Forged, Not Given*

## Purpose

`AAA` is the **agent workspace and control plane** of the arif organism.

It exists to:

- define agent identity
- register capabilities, skills, bundles, workflows, tools, and hosts
- enforce policy, approvals, and invariants
- route work across agents, runtimes, and organism repos
- preserve auditability through append-only events and explicit epistemic status

`AAA` is **not** the constitutional law source, **not** the execution runtime, and **not** the public website layer.

---

## The Five-Layer Definition

In arifOS, "AAA" is not a flat label. It is a **depth-ordered stack** where each layer adds a new architectural meaning:

| # | Layer | Expansion | Core Principle |
|---|---|---|---|
| 1 | **Functional** | Agents · API · Apps | How the machine interacts with you and the world |
| 2 | **Security** | Auth · Auth · Audit | Identity, mandate, and accountability via F11/F13 |
| 3 | **Structural** | Agent-to-Agent Alignment | A2A mesh glue — constitutional coherence across federation |
| 4 | **Grade** | Triple-A Sovereign | Highest governance quality — sovereign-grade, not hallucination-grade |
| 5 | **Recursive (AAAA)** | Arif's Autonomous Agent Architecture | The full pattern: SOUL + loop + tool-capable units + Trinity layout |

---

## Canonical boundary

| Repo / system | Canonical role |
|---|---|
| `arifOS` | constitutional truth, judgment, doctrine, vault contracts |
| `AAA` | identity, control plane, registries, workflows, policy, host adapters |
| `A-FORGE` | execution shell, orchestration runtime, bounded execution |
| `GEOX` | Earth witness and grounded physical-domain truth |
| `WEALTH` | capital witness and economic-domain truth |
| `WELL` | human substrate witness and readiness telemetry |
| `arif-sites` | public sites, rendered surfaces, outward-facing documentation |

Rule:

- `AAA` may **coordinate** these systems
- `AAA` may **read** their declared contracts
- `AAA` must **not absorb** their canonical truth domains

---

## What AAA owns

`AAA` owns the control-plane layer:

- agent registry
- skill registry
- bundle registry
- workflow registry
- tool and server catalogs
- host contracts
- approvals and HOLD gates
- integration contracts
- observability/event schemas
- operator cockpit data model
- GitHub-native agent automation

---

## What AAA does not own

`AAA` must not become:

- a replacement for `arifOS`
- a dumping ground for random notes
- the only runtime or compute layer
- the source of public website implementation
- the owner of GEOX / WEALTH / WELL truth

If a concern belongs to law, runtime, domain truth, or public rendering, it stays outside AAA.

---

## Root canon

These files form the minimum root canon of AAA:

1. `AGENTS.md`
2. `SOUL.md`
3. `USER.md`
4. `IDENTITY.md`
5. `BOOTSTRAP.md`
6. `arifos.init`
7. `MEMORY.md`
8. `HEARTBEAT.md`
9. `TOOLS.md`
10. `agent-card.json`

These files define identity and boot law. They are not optional.

---

## Internal architecture

```text
AAA
├─ root canon
├─ governance/         # policies, approvals, HOLD gates, invariants
├─ agents/             # agent records and cards
├─ registries/         # YAML-authored canonical registries
├─ schemas/            # JSON schemas for all contracts
├─ openclaw/           # OpenClaw-specific source contracts and exports
├─ skills/             # capability units
├─ bundles/            # role/task-specific skill packs
├─ workflows/          # durable execution contracts
├─ mcp/                # tool/resource catalogs and transports
├─ a2a/                # agent discovery and delegation contracts
├─ hosts/              # host adapters and permission profiles
├─ integrations/       # contracts to arifOS, A-FORGE, GEOX, WEALTH, WELL, GitHub
├─ observability/      # traces, runs, audit events, failures, feedback
├─ apps/               # cockpit, approvals, registry, run viewer
└─ .github/            # repo-native automation and policy enforcement
```

---

## Contract model

AAA is authored and consumed in two layers:

- **YAML** for human-authored source contracts
- **JSON** for canonical generated artifacts consumed by tooling

Rule:

- source-of-truth files live in YAML
- CI validates and exports canonical JSON
- runtime consumers read JSON, not raw YAML

This keeps contracts readable for humans and deterministic for machines.

---

## Gödel-lock invariants

AAA is locked by enforced invariants, not vibes.

### 1. Authority invariant
- no agent may exceed its declared role, tier, host contract, or approval policy

### 2. Truth-boundary invariant
- `AAA` may coordinate claims, but final constitutional truth remains with `arifOS`

### 3. Witness invariant
- domain-sensitive actions must reference the correct witness:
  - `GEOX` for Earth
  - `WEALTH` for capital
  - `WELL` for human substrate

### 4. Epistemic invariant
- claims must carry an epistemic status
- no upgrade from plausible to claim without new evidence or approval

### 5. Pipeline invariant
- high-risk work may not jump to `999` without `888` audit

### 6. Audit invariant
- every material action must emit an append-only event record

### 7. Separation-of-duties invariant
- the same role should not both propose and approve high-risk changes

---

## Roles

AAA starts with these canonical roles:

- `architect`
- `engineer`
- `auditor`
- `validator`
- `operator`
- `domain-specialist`

Each role must declare:

- authority level
- allowed tools
- allowed servers
- host binding
- risk tier
- escalation rules

Higher authority means stronger checks, not looser boundaries.

---

## Relationship to A2A and MCP

AAA treats these as complementary layers:

- **MCP** = tool, resource, prompt, and transport surface
- **A2A** = agent identity, discovery, delegation, collaboration

AAA must model both explicitly.

Rule:

- tools and servers are not agents
- agents and cards are not tools
- hosts are not protocols

Keep those layers separate in contracts.

---

## OpenClaw-first operating model

OpenClaw is the primary agentic runtime.

AAA therefore acts as the **authoring monorepo** for OpenClaw behavior:

- AAA owns source contracts
- AAA exports runtime artifacts
- OpenClaw consumes generated state
- runtime drift must be compared back against AAA desired state

If OpenClaw can run it, AAA must be able to describe it.

---

## Execution order

AAA should be forged in this order:

1. charter
2. root canon normalization
3. schemas
4. registries
5. export pipeline
6. invariant validator
7. host contracts
8. A2A and MCP contracts
9. skill packaging
10. workflow contracts
11. integration contracts
12. GitHub plane
13. observability model
14. cockpit model and apps

---

## Current migration stance

This repository began as the legacy `waw` repo, but its canonical identity is now `AAA`.

The charter freezes the intended future:

- website concerns move toward `arif-sites`
- agent-native concerns consolidate here
- public rendering is downstream, not primary

Until rename/cutover is complete, this charter is the architectural source of truth for the repository direction.

---

## One-line verdict

**AAA is the governed control plane of the organism: identity, contracts, coordination, approvals, and auditability — not doctrine, not runtime, not public surface.**
