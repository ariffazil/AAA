# AAA for Humans — Plain Language Guide

> **Classification:** Reference | AAA Repository
> **Scope:** Human-readable explanation of the arifOS federation
> **Status:** LIVE — 2026-06-26
> **Audience:** Anyone who needs to understand what AAA is without reading 1000 lines of YAML

---

## What is AAA?

AAA is your control plane — the part of the arifOS federation that decides who can do what, using what tools, within what authority bounds.

It is not an AI model. It is the governance layer that sits between you and every AI model or agent you run, making sure nothing happens outside of what you approved.

---

## The Five Things You're Building

### 1. Tools

A tool is a single function an AI can call. Like a Python function. It does one thing:

- `forge_github_pr` — fetch a PR
- `forge_shell_dryrun` — run a command but only simulate it
- `forge_filesystem_read` — read a file

An AI model by itself is just a text predictor. Tools are how it touches the real world. Without tools it can only write text. With tools it can read files, call APIs, run code, write to databases.

In AAA you have: your own MCP servers exposing tools, A-FORGE's tool registry, and the arifOS kernel's 27 constitutional tools.

### 2. Skills

A skill is a governed playbook for a multi-step job. Not a single function call — a whole workflow.

Think of it like a Standard Operating Procedure (SOP). `github-pr-review` doesn't just fetch a PR — it runs a checklist: read the diff, check constitutional files, verify REPO= trailer, check CI status, produce a verdict. It's 8–15 tool calls orchestrated in sequence, with rules about what to do and what to refuse.

Skills are what separate an agent doing something useful from an agent doing something random.

You have 39 skills in AAA right now, covering: GitHub ops, MCP federation, incident escalation, geoscience grounding, agent onboarding, vault integrity, secret scanning, Docker ops, and more.

### 3. Agents

An agent is `loop(Model + Tools + State + Goal) → Actions → Verdict`.

A model alone generates text. An agent uses a model to decide which tool to call, calls it, reads the result, decides what to do next, repeats — until the goal is done or it hits a constitutional stop.

You defined this precisely in your `AAA_AGENT_SPECIFICATION_v1.0.md`:

- It must have a goal
- It loops with tools
- It terminates in a sealed constitutional verdict (SEAL / HOLD / VOID / SABAR)
- It produces a VAULT999 receipt

In AAA you have: the HEXAGON (5 constitutional agents), runtime coding agents (OpenCode, Claude Code, Kimi, Grok, Codex, Gemini, Antigravity, Qwen), role agents, and Hermes (the cross-model relay).

### 4. CLI

A CLI (Command Line Interface) is just an AI coding assistant you run from the terminal. Claude Code is one. OpenCode, Kimi Code, GitHub Copilot CLI, Codex, Grok Build — all the same thing: you type a task, the model runs a loop with tools in your repo.

The problem you were solving: every CLI has its own name for the same concept. Claude calls them "skills", Copilot calls them "agents", OpenCode calls them "context providers". Your ROSETTA STONE is the translation table.

What you built (`compile.py`) auto-generates the right file format for each CLI from one canonical `SKILL.md`. You write a skill once; the compiler makes it speak every vendor's dialect.

### 5. MCP (Model Context Protocol)

MCP is the protocol for connecting AI to external tools, invented by Anthropic and now adopted across the industry (OpenAI, Google, etc.).

Think of it like USB. Before USB, every device had its own connector. MCP is the universal connector for AI tool integrations. Instead of hardcoding every tool into every model, you expose tools as an MCP server, and any MCP-compatible model can discover and call those tools.

In your federation: arifOS runs an MCP server on port 8088, GEOX has its own MCP server with petrophysics tools, WEALTH has capital tools, WELL has vitality tools. Any agent can connect to any server and get access to that organ's capabilities.

### 6. A2A (Agent-to-Agent)

A2A is the protocol for agents talking to other agents — not agents talking to tools.

- MCP = agent calls a tool server.
- A2A = agent calls another agent and delegates a task.

You have a Hermes A2A server in `a2a-server/` — it's the relay node. When one agent (say, A-FORGE) needs a geoscience computation, it doesn't just call a tool — it sends a structured task to the GEOX agent via A2A, GEOX runs its own loop, returns a result with a receipt.

A2A is how a federation of agents coordinates without any single agent needing to know everything.

---

## What You Have That Most Labs Don't

- **Constitutional invariants (Floors F1–F13)** — hardcoded ethical/governance constraints that no agent can override, not even you on impulse. No major AI lab ships this with their CLI. They do model-level alignment, but there's no per-repo, per-action constitutional gate.

- **VAULT999 receipts** — immutable hash-chained audit trail on every consequential action. Most AI tools have no audit trail at all. You can reconstruct every decision.

- **SEAL/HOLD/VOID/SABAR verdicts** — agents don't just "succeed" or "fail". They produce constitutional verdicts. HOLD is "I need more information before I can proceed". SABAR is "wait, this is not the right moment". No CLI has this.

- **Federation organs** — you didn't build one AI assistant, you built 7 sovereign organs with hard boundaries between them (GEOX can't run capital math; A-FORGE can't issue verdicts). This prevents capability creep and makes each organ auditable.

---

## What's Missing or Still Stubs

- **No live skill invocation yet** — your 39 skills are defined and validated but there's no runtime that auto-routes "hey, a PR opened" → trigger `github-pr-review`. The plumbing between events and skills isn't wired yet.

- **Agent cards drifting from reality** — your `AGENT_REGISTRY.md` and `AAA_AGENTS_REGISTRY.json` disagree on 3 entries. The SCAR-13 note in the registry documents this but it's unresolved.

- **No unified evaluation harness** — `arifos-evals` is a stub skill. You have benchmarks directory but no actual eval runs. You can't currently measure whether your agents are getting better or worse.

- **Hermes A2A bridge is refactored but not battle-tested** — last commit was a 220-line refactor. No test coverage visible on the A2A server.

---

## What the AI Labs Are Missing vs You

Labs build models. You built governance over models. Labs like Anthropic and OpenAI ship alignment baked into weights — you can't inspect it, you can't override it per-repo, you can't audit it. What you're building is the constitutional layer above the model — the thing that should exist in every enterprise AI deployment but almost nobody has actually built. The industry calls this "AI governance" or "AI alignment in production" but almost no one has a real implementation at the repo level. You have one.

---

## The Short Version

You have an AI operating system with 39 governed workflows, a multi-vendor translation layer, an audit vault, a 5-agent constitutional architecture, and cross-agent federation protocol — all sitting on top of every major coding CLI. What's missing is the event wiring that makes skills trigger automatically, and a real eval loop.

---

*DITEMPA BUKAN DIBERI — Forged, Not Given.*
