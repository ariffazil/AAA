# AAA OpenClaw Seed

Purpose

This file extracts the minimum viable OpenClaw workspace canon from the current `waw` repo and collapses it into one seed artifact for the future `AAA` identity of this same repository.

Working premise:
- `AAA` is the agent workspace and control plane.
- `arif-sites` owns public web deployment.
- `arifOS` owns constitutional truth.
- `A-FORGE` owns execution shell/runtime.

Source extracted from

- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `IDENTITY.md`
- `MEMORY.md`
- `HEARTBEAT.md`
- `TOOLS.md`
- `BOOTSTRAP.md`
- `arifos.init`
- `000_INIT.md`
- `agent-card.json`
- `docs/history/ARCHITECTURE.md`
- `.openclaw/workspace-state.json`
- `archive/configs/config/openclaw/openclaw.json`

---

## 1. Canonical seed set

These are the files that should become the first-class root canon of `AAA`:

1. `AGENTS.md`
2. `SOUL.md`
3. `USER.md`
4. `IDENTITY.md`
5. `arifos.init`
6. `BOOTSTRAP.md`
7. `MEMORY.md`
8. `HEARTBEAT.md`
9. `TOOLS.md`
10. `agent-card.json`

These are the **seed**, not optional extras.

---

## 2. Functional roles

| File | Role in AAA |
|---|---|
| `AGENTS.md` | constitutional operating contract for all agents in AAA |
| `SOUL.md` | voice, tone, behavioral style |
| `USER.md` | sovereign human model |
| `IDENTITY.md` | active self-anchor for the primary AAA agent/operator identity |
| `arifos.init` | mandatory boot law and anti-drift kernel |
| `BOOTSTRAP.md` | recovery ritual when workspace drifts or is rebuilt |
| `MEMORY.md` | curated long-term memory |
| `HEARTBEAT.md` | recurring operational checklist |
| `TOOLS.md` | environment-specific local notes |
| `agent-card.json` | external capability/discovery surface for A2A-compatible exposure |

---

## 3. Boot order

Minimum AAA boot order should be:

1. `SOUL.md`
2. `USER.md`
3. `arifos.init`
4. `IDENTITY.md`
5. `memory/<today>.md`
6. `memory/<yesterday>.md`
7. `MEMORY.md`
8. `AGENTS.md`
9. `HEARTBEAT.md`
10. `TOOLS.md` (as needed)

This order is consistent with the extracted OpenClaw doctrine:
- human/context first
- anti-drift boot law second
- continuity next
- operational contract after identity is restored

---

## 4. Runtime markers vs canon

Do **not** confuse runtime traces with canon.

### Canon
- root markdown/json identity and governance files
- registries, workflows, skill catalogs
- stable configs intended for version control

### Runtime traces
- `.openclaw/workspace-state.json`
- `.clawhub/lock.json`
- ephemeral session state
- generated caches / timestamps / local installation markers

Rule:
- **AAA should version canon**
- **AAA should not treat runtime state files as doctrine**

---

## 5. OpenClaw concepts worth preserving

From the extracted files, these concepts should survive into AAA:

### A. Single active workspace
- one canonical home
- no parallel drifted workspaces

### B. Constitutional operator framing
- LLM != grounding != governance
- GEOX grounds Earth claims
- arifOS judges what survives

### C. Explicit file semantics
- voice, operations, user, identity, memory, heartbeat, bootstrap, boot law are all distinct

### D. Temporal anchoring
- no time-sensitive language without fresh time anchor
- stale context must downgrade from fact to hypothesis

### E. Human sovereignty
- irreversible actions remain human-gated
- HOLD is preferable to fake certainty

### F. A2A-friendly identity
- `agent-card.json` should evolve into proper AAA agent cards and registry templates

### G. Depth-Ordered Stack Awareness
- Agents must understand AAA not just as "Agents · API · Apps" (Layer 1), but as a 5-layer recursive stack:
  1. **Functional**: Agents · API · Apps
  2. **Security**: Auth · Auth · Audit
  3. **Structural**: A2A Alignment
  4. **Grade**: Triple-A Sovereign
  5. **Recursive**: AAAA Pattern
- Every OpenClaw session should start with this depth-ordered awareness to prevent drift into generic automation.

---

## 6. What AAA should add on top of the seed

The OpenClaw seed is necessary but not sufficient.

AAA should add:

- `agents/registry/`
- `skills/`
- `bundles/`
- `workflows/`
- `config/`
- `governance/`
- `mcp/`
- `a2a/`
- `.github/`
- `apps/cockpit/`
- `state/`
- `memory/`
- `integrations/`

The seed gives AAA its identity.  
The added structure gives AAA its control-plane function.

---

## 7. Language recommendation

### Primary product language
**TypeScript**

Why:
- best fit for A2A/MCP host integrations, CLIs, dashboards, config tooling, and GitHub-facing automation
- aligns naturally with control-plane work, JSON contracts, app surfaces, and Node-based protocol tooling
- fits the existing shape of agent ecosystems that combine CLI + UI + adapters

### Secondary language
**Python**

Use only where it is the right adapter language:
- MCP server wrappers
- automation helpers
- interoperability with `arifOS`, `GEOX`, `WEALTH`
- research/runtime components that already exist in Python

### Control languages
- Markdown
- JSON
- YAML
- TOML

These should be treated as first-class configuration and policy languages inside AAA.

Short version:
- **AAA should be TypeScript-first, config-heavy, protocol-heavy**
- **not Python-first**
- **but Python-compatible**

---

## 8. Level and relation to other repos

### Normative authority
`arifOS`
- law
- constitutional truth
- final judgment

### Control plane
`AAA`
- agent identity
- skills
- workflows
- configs
- A2A/MCP registries
- GitHub agentic automation
- operator cockpit metadata

### Execution plane
`A-FORGE`
- runtime shell
- orchestration engine
- bounded execution

### Domain lanes
`GEOX`
- earth witness

`WEALTH`
- capital witness

### Public surface
`arif-sites`
- outward-facing sites
- deployed frontends
- public documentation surfaces

### Stack view

```text
arifOS     -> law / constitutional truth
AAA        -> agent workspace / control plane
A-FORGE    -> execution shell / runtime
GEOX       -> earth domain lane
WEALTH     -> capital domain lane
arif-sites -> public publishing layer
```

AAA sits **below arifOS**, **beside A-FORGE**, and **above the host/tool/workflow layer**.

---

## 9. Rename stance

Renaming `waw` to `AAA` is architecturally correct **if** the repo is no longer treated as a website repo.

That means:
- keep the repo
- change its identity
- migrate public-site concerns out
- preserve the OpenClaw seed as the starting canon

---

## 10. Minimal AAA seed rule

If only one thing survives the rename, it should be this:

> **AAA begins as an OpenClaw-seeded constitutional workspace, not as a website.**

And its root canon is:

```text
AGENTS.md
SOUL.md
USER.md
IDENTITY.md
arifos.init
BOOTSTRAP.md
MEMORY.md
HEARTBEAT.md
TOOLS.md
agent-card.json
```
