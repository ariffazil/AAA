# Agent Portfolio Registry

> Live registry of all agents in Arif Fazil's intelligence federation.
> Updated: 2026-05-11 from VPS architecture audit + agent portfolio mapping session.

## ASI Layer

### Hermes
- **Role:** ASI deliberative relay, strategic judgment, contextual reasoning
- **Trust:** High
- **Speed:** Fast (local device)
- **Location:** Local device (not on VPS)
- **Entry:** Direct Telegram/user prompt
- **Delegation ceiling:** F1-F13 enforcement, 777 FORGE (reason/plan/execute), escalate to 888_JUDGE
- **Capabilities:** Federation orchestration, prompt routing, strategic reasoning, memory management
- **Limitations:** Cannot seal, cannot adjudicate beyond F1-F13

### OpenClaw
- **Role:** Gateway orchestrator, task routing, tool registry, A2A mesh
- **Trust:** Medium
- **Speed:** Medium
- **Location:** VPS (runs as root — hardening needed)
- **Entry:** Via Hermes or direct CLI
- **Delegation ceiling:** Route tasks, cannot seal or judge
- **Capabilities:** Task routing, tool registry, A2A bridge, agent spawning
- **Risk:** Runs as root process — isolation gap

---

## Federation Nodes

### arifOS
- **Role:** Constitutional kernel, sole final judgment path
- **Language:** Python 3.12+
- **Port:** 8080
- **MCP:** `http://127.0.0.1:8080/mcp`
- **Invariant:** Sole 888_JUDGE / 999_SEAL chokepoint
- **Tools:** 37+ constitutional tools (arif_<noun>_<verb>)
- **Trust:** High
- **Risk:** Low (containerized)

### A-FORGE
- **Role:** Operator chair, orchestration substrate
- **Language:** TypeScript 5.8+
- **Port:** 7071
- **MCP:** Stdio server
- **Invariant:** May NOT adjudicate — orchestrate only
- **Architecture:** Planner/Executor/Verifier triad, event-sourced
- **Trust:** High
- **Risk:** Low (containerized)

### GEOX
- **Role:** Earth intelligence coprocessor
- **Language:** Python 3.11+
- **Port:** 8081
- **MCP:** `http://127.0.0.1:8081/mcp`
- **Invariant:** Ψ node — geoscience, petrophysics, physics grounding only
- **Trust:** High
- **Risk:** Low (containerized)

### WEALTH
- **Role:** Capital intelligence organ
- **Language:** Python 3.12+
- **Port:** 8082
- **MCP:** `http://127.0.0.1:8082/mcp`
- **Invariant:** NPV/EMV/risk/crisis — NOT irreversible allocator
- **Trust:** High
- **Risk:** Medium (Supabase key in git history — needs rotation)

### WELL
- **Role:** Biological readiness substrate
- **Language:** Python 3.12+
- **Port:** 8083
- **MCP:** `http://127.0.0.1:8083/mcp`
- **Invariant:** Operator state/cognitive pressure — NOT sole strategic judge
- **Trust:** High
- **Risk:** Low (containerized)

### AAA
- **Role:** Control plane — dashboard, A2A gateway, operator visibility
- **Language:** React 19 + TypeScript
- **Port:** 3001
- **Invariant:** Control plane — NOT hidden governance kernel
- **Trust:** High
- **Risk:** Low (containerized)

---

## External Coding Agents (Engineers)

### Codex
- **Role:** Primary coder
- **Specialty:** Features, iterative builds, PRs
- **Use when:** Complex builds, new features
- **Trust:** High
- **Speed:** Fastest
- **Delegation ceiling:** Execute code, cannot access soul docs or system files
- **Workspace rule:** Never in `~/.openclaw` or workspace state directories

### Claude Code
- **Role:** Deep refactor agent
- **Specialty:** Heavy refactors, full-stack builds, complex architecture
- **Use when:** Codex unavailable or insufficient for deep architecture work
- **Trust:** High
- **Speed:** Moderate

### Kimi Code
- **Role:** Architecture audit agent
- **Specialty:** Site architecture mapping, capability bootstrap verification
- **Use when:** Architecture mapping, system audits
- **Trust:** Medium

### OpenCode
- **Role:** PR review agent
- **Specialty:** Code quality review, full-stack builds
- **Use when:** PR reviews, code quality validation
- **Trust:** High

### Copilot CLI
- **Role:** Inline completion agent
- **Specialty:** Quick fixes, one-liners, lightweight edits
- **Use when:** Lightweight edits, inline completions
- **Trust:** High
- **Speed:** Fast

---

## External Auditors / Validators

### Perplexity
- **Role:** Research auditor
- **Specialty:** Live web facts, citations, grounding
- **Use when:** Need current facts, web research, citation verification
- **Trust:** Good
- **Speed:** Slower
- **Delegation ceiling:** Research only — no execution

### ChatGPT
- **Role:** General validator
- **Specialty:** Cross-check reasoning paths, alternative perspective
- **Use when:** Reasoning validation, second opinion
- **Trust:** Good
- **Speed:** Moderate
- **Delegation ceiling:** Validate only — no execution

---

## Reasoning / Research Agents

### mmx-text-researcher
- **Role:** Deep research synthesis
- **Model:** MiniMax-Text-01
- **Specialty:** Structured research output, multi-source synthesis
- **Use when:** Deep research with synthesis requirement

### Pi (agent)
- **Role:** Adversarial second opinion
- **Specialty:** Alternative perspective, adversarial reasoning check
- **Use when:** Need adversarial lens on reasoning path

---

## VPS Network Map

| Service | Internal URL | Tailscale URL | Public |
|---------|--------------|---------------|--------|
| arifOS | `127.0.0.1:8080` | `100.111.84.52:8080` | via Caddy |
| GEOX | `127.0.0.1:8081` | `100.111.84.52:8081` | via Caddy |
| WEALTH | `127.0.0.1:8082` | `100.111.84.52:8082` | via Caddy |
| WELL | `127.0.0.1:8083` | `100.111.84.52:8083` | via Caddy |
| AAA | `127.0.0.1:3001` | `100.111.84.52:3001` | `aaa.arif-fazil.com` |
| OpenClaw | `127.0.0.1:7071` | `100.111.84.52:7071` | via Caddy |
| Grafana | `127.0.0.1:3000` | `100.111.84.52:3000` | via Caddy |
| Loki | `127.0.0.1:3100` | `100.111.84.52:3100` | via Caddy |

**SSH:** Port 22888, Tailscale IP `100.111.84.52`, public IP `72.62.71.199`
**User:** `ariffazil` (sudo NOPASSWD: ALL — effectively root)

---

## Security Posture

| Item | Status | Priority |
|------|--------|----------|
| OpenClaw running as root | Needs hardening | Medium |
| WEALTH Supabase key in git history | Needs rotation | High |
| 8 secret files unrotated | Needs sovereign approval | High |
| arif-sites tokens in tracked files | Needs rotation | High |
| Tailscale exposed on public | Verified firewall | Low |
| SSH key-based auth | Enabled | Low |

---

## Notes

- All federation nodes (arifOS, GEOX, WEALTH, WELL, AAA) are containerized — host user separation not required for them
- OpenClaw is the priority for host user isolation (move off root)
- Hermes is NOT on the VPS — it runs locally as Arif's personal agent
- Tailscale is required for mobile access (SSH + services via Tailscale IP)