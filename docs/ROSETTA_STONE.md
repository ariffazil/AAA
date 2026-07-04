# AAA Rosetta Stone v1.0
## Cross-CLI Vocabulary Map for the arifOS Federation

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> **Status:** ACTIVE | **Author:** AAA Federation | **Date:** 2026-06-26
> **Authority:** Builds on `AAA_AGENT.md`, `AAA_ZEN.md`, `AGENTSKILLTREE.md`
> **Purpose:** Every major coding CLI uses different names for the same 5 primitives.
> This document is the translation key. One canonical concept → 8 vendor names.
> Plus: the 3 primitives **only AAA has** (Floor, Verdict, Receipt).

---

## The Core Problem

Eight major CLI coding agents have independently converged on the same five capability
primitives but named them differently. An agent onboarding into any of these ecosystems
faces vocabulary fragmentation. This document resolves it.

The five shared primitives are:
- **Memory** — persistent project context loaded at session start
- **Skill** — on-demand reusable workflow (auto or manual invocation)
- **Subagent** — isolated context window doing parallel work
- **Hook** — deterministic script on lifecycle events
- **MCP** — external tool servers via Model Context Protocol

The three **AAA-unique** primitives are:
- **Floor** — constitutional invariant that cannot be overridden by any agent
- **Verdict** — a constitutional judgment (SEAL / HOLD / VOID / SABAR) with VAULT999 receipt
- **Receipt** — immutable hash-chained audit record of every consequential action

---

## The Rosetta Stone — 8 Primitives × 8 CLIs

> Read across a row to translate AAA canonical terms to vendor terms.
> Read down a column to see everything one CLI calls a given primitive.

### Primitive 1 — Memory (persistent project context)

| AAA Canonical | Vendor Name | File Location | Load Timing |
|---|---|---|---|
| **AAA Constitution** | `AGENTS.md` | repo root | session start, memoized |
| **AAA Constitution** | `CLAUDE.md` | repo root | session start, memoized |
| **AAA Constitution** | `AGENTS.md` | repo root | session start (tree walk root→folder) |
| **AAA Constitution** | `AGENTS.md` | repo root | session start |
| **AAA Constitution** | `AGENTS.md` | repo root | session start |
| **AAA Constitution** | `copilot init` | `.copilot/` | session start |
| **AAA Constitution** | `.continue/rules/*.md` | workspace + global | session or path-scoped |
| **AAA Constitution** | (shared harness config) | harness init | session start |

CLI order: OpenCode · Claude Code · Codex · Kimi · Grok Build · GitHub Copilot · Continue.dev · Antigravity

**AAA note:** `AGENTS.md` is the industry standard (60k+ projects). Claude Code uses
`CLAUDE.md`. Both exist in every AAA repo. They point at the same canonical content.

---

### Primitive 2 — Skill (reusable governed playbook)

| CLI | Skill Name | Location | Format |
|---|---|---|---|
| **OpenCode** | Agent config (built-in) | `opencode.json:agents.<id>` | JSON config |
| **Claude Code** | Skill | `.claude/skills/<id>/SKILL.md` | Markdown + YAML frontmatter |
| **Codex CLI** | Skill | `.agents/skills/<id>/` | Markdown + schema |
| **Kimi Code** | Skill | `.agents/skills/<id>/` | YAML + markdown |
| **Grok Build** | Skill | `.grok/skills/<id>/` | Markdown frontmatter |
| **GitHub Copilot** | Agent skill | `.copilot/agents/<id>.agent.md` | YAML frontmatter + markdown |
| **Continue.dev** | Skill | `.continue/skills/<id>.md` | Markdown with frontmatter |
| **Antigravity** | Skill bundle | `skills/<id>/` | Markdown |
| **AAA Canonical** | **Skill** | `skills/<id>/SKILL.md` | YAML frontmatter + markdown |

**AAA note:** `skills/compile.py` reads each skill's `host_compatibility` and auto-generates
all vendor-specific formats from the canonical `SKILL.md`. Write once, deploy to 8 CLIs.

---

### Primitive 3 — Subagent (isolated parallel worker)

| CLI | Subagent Name | Isolation | Parallel? |
|---|---|---|---|
| **OpenCode** | Subagent (`general`/`explore`/`scout`) | Separate context window | Yes |
| **Claude Code** | Subagent (Agent tool) | Separate context + tool list | Yes |
| **Codex CLI** | Subagent | Separate context | Yes |
| **Kimi Code** | Sub-agent (LaborMarket) | Separate context | Yes |
| **Grok Build** | Subagent | Separate context + worktree | Yes (worktree isolation) |
| **GitHub Copilot** | Custom agent (delegated) | Separate context | Per-task |
| **Continue.dev** | Plan/Agent mode | Sequential | No |
| **Antigravity** | Async subagent | Separate context | Yes (background) |
| **AAA Canonical** | **AAA Agent** (A2A mesh) | Separate context + organ + VAULT999 | Yes + constitutional |

**AAA note:** An AAA Agent is not just an isolated context — it is a **sovereign-ratified
Golden Path traversal** (see `AAA_AGENT.md` §2). It terminates in a
VAULT999-sealed verdict. Vendor subagents terminate in a summary. That's the difference.

---

### Primitive 4 — Hook (deterministic lifecycle automation)

| CLI | Hook Name | Event Types | Config Location |
|---|---|---|---|
| **OpenCode** | (limited) | — | — |
| **Claude Code** | Hook | PreToolUse, PostToolUse, Notification, Stop | `.claude/settings.json` |
| **Codex CLI** | Hooks engine | Pre/post tool execution | config |
| **Kimi Code** | (limited) | — | — |
| **Grok Build** | Hook | Pre/post action | `.grok/hooks/` |
| **GitHub Copilot** | Hook (plugin) | Plugin lifecycle | `.copilot/plugins/` |
| **Continue.dev** | (limited) | — | — |
| **Antigravity** | Inspect/decide/transform | Per tool call | SDK config |
| **AAA Canonical** | **Hook** | Pre/post tool, lifecycle events | `.claude/settings.json` (primary) |

**AAA note:** Claude Code hooks are the most capable available (4 event types, shell
scripts). AAA uses these as the primary hook surface. See `hooks/` directory.

---

### Primitive 5 — MCP (external tool servers)

| CLI | MCP Support | Config Location |
|---|---|---|
| **OpenCode** | ✅ Full MCP | `opencode.json:mcp` |
| **Claude Code** | ✅ Full MCP | `.claude/settings.json:mcpServers` |
| **Codex CLI** | ✅ Full MCP | codex config |
| **Kimi Code** | ✅ Full MCP | `.kimi/config` |
| **Grok Build** | ✅ Full MCP | grok config |
| **GitHub Copilot** | ✅ `copilot mcp` | built-in GitHub MCP |
| **Continue.dev** | ✅ Full MCP | `.continue/config.yaml` |
| **Antigravity** | ✅ Via skill bundles | harness config |
| **AAA Canonical** | **27 tools on default wire** | `arifos-direct` MCP server |

**AAA note:** arifOS exposes 27 canonical MCP tools (`arif_init`, `arif_judge`,
`arif_seal`, etc.). Any CLI that supports MCP can call these. This is the primary
interoperability surface.

---

## AAA-Unique Primitives (Not in Any Vendor CLI)

These three primitives have no equivalent in any of the 8 major CLI ecosystems.
They are AAA's structural contribution to the agentic web.

---

### Primitive 6 — Floor (constitutional invariant)

> A Floor is a non-negotiable constraint that no agent, skill, or operator can override.
> Floors are not rules — they are the substrate on which rules rest.

**The 13 Floors (F1–F13):**

| Floor | Name | Machine Substrate |
|---|---|---|
| F1 | AMANAH | Reversibility-first: backup before mutate, VAULT999 seal before irreversible |
| F2 | TRUTH | Evidence-before-confidence: OBS/DER/INT/SPEC labels, τ ≥ 0.99 for facts |
| F3 | WITNESS | Theory × Constitution × Intent alignment check |
| F4 | CLARITY | ΔS ≤ 0: leave the machine cleaner than you found it |
| F5 | PEACE | De-escalate before optimize; guard weakest stakeholder |
| F6 | MARUAH | Human dignity is a constraint, not a preference |
| F7 | HUMILITY | Ω₀ ∈ [0.03, 0.05]; confidence capped at 0.90; unknowns named |
| F8 | GENIUS | Simplest correct path; orthogonal transfer; KISS before YAGNI |
| F9 | ANTI-HANTU | C_dark < 0.30; no soul claims; no consciousness simulation |
| F10 | ONTOLOGY | Category boundaries preserved; model ≠ person; agent ≠ tool |
| F11 | AUTH | Organ attestation before multi-organ actions; session binding |
| F12 | INJECTION | Sanitize all external inputs; no exec(user_input) |
| F13 | SOVEREIGN | Human veto is absolute; 888_JUDGE gate for irreversible actions |

**Enforcement:** Floors are checked at every tool call via the arifOS constitutional kernel.
Violation response: HOLD → escalate to 888_JUDGE → notify Arif (see `ZENTOSILICASPEC.md`).

**Vendor equivalent:** None. No major CLI has constitutional floors.

---

### Primitive 7 — Verdict (constitutional judgment)

> A Verdict is a constitutional judgment produced by the 888_JUDGE after deliberation.
> It terminates an Agent loop. Without a Verdict, there is no Agent — only a Model.
> (See `AAA_AGENT.md` §1 Definitional Ladder)

**Verdict types:**

| Verdict | Meaning | Action |
|---|---|---|
| **SEAL** | Approved, constitutional, immutable | Execute + write VAULT999 receipt |
| **HOLD** | Pause — insufficient evidence or authorization | Stop + request resolution |
| **VOID** | Rejected — constitutional violation detected | Abort + log |
| **SABAR** | Wait — timing not right; no urgency override | Defer + schedule |

**Verdict grammar:**
```
verdict := { type: SEAL|HOLD|VOID|SABAR, confidence: 0.0–0.90,
             floor_trace: {F1: PASS|FAIL, ...}, receipt_uri: vault999://... }
```

**Vendor equivalent:** None. No major CLI's skill/subagent produces a constitutional verdict.
The closest is Claude Code's subagent returning a "summary" — but that has no constitutional
anchoring, no floor trace, and no immutable receipt.

---

### Primitive 8 — Receipt (immutable audit record)

> A Receipt is a hash-chained, append-only record in VAULT999 of every
> consequential action. Axiom 9 of `AAA_ZEN.md`: "State changes require receipts."

**Receipt schema:**
```json
{
  "ts": "2026-06-26T07:00:00Z",
  "actor_id": "333-AGI",
  "session_id": "uuid",
  "action": "Human-readable action description",
  "blast_radius": "LOCAL_FILE | CONTAINER | FEDERATION",
  "reversible": true,
  "hash_prev": "sha256 of previous receipt",
  "hash_self": "sha256(this receipt)",
  "floor_trace": {"F1": "PASS", "F2": "PASS"},
  "seal_verdict": "SEAL-2026-06-26-abc123",
  "vault_uri": "vault999://arifos/sealed/2026-06-26/abc123.json"
}
```

**Vendor equivalent:** None. No major CLI provides an immutable audit chain.
GitHub has audit logs, but they are vendor-managed, not agent-local, not hash-chained,
and not attached to individual agent verdicts.

---

## The Complete Rosetta Table

> Full 8×8 matrix. Row = AAA canonical primitive. Column = vendor CLI.

| AAA Primitive | OpenCode | Claude Code | Codex CLI | Kimi Code | Grok Build | Copilot CLI | Continue.dev | Antigravity |
|---|---|---|---|---|---|---|---|---|
| **Memory** | `AGENTS.md` | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` | `copilot init` | `.continue/rules/` | harness config |
| **Skill** | `opencode.json:agents` | `.claude/skills/*/SKILL.md` | `.agents/skills/*/` | `.agents/skills/*/` | `.grok/skills/*/` | `.copilot/agents/*.agent.md` | `.continue/skills/*.md` | `skills/*/` |
| **Subagent** | `general`/`explore` | Agent tool (subagent) | Subagent | LaborMarket sub-agent | Subagent + worktree | Custom agent | Plan mode | Async subagent |
| **Hook** | (none) | `.claude/settings.json` hooks | Hooks engine | (none) | `.grok/hooks/` | Plugin hooks | (none) | inspect/decide/transform |
| **MCP** | `opencode.json:mcp` | `.claude/settings.json:mcpServers` | codex config | `.kimi/config` | grok config | `copilot mcp` | `.continue/config.yaml` | skill bundles |
| **Floor** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Verdict** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Receipt** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Reading the ❌ rows:** No major CLI has Floors, Verdicts, or Receipts.
AAA is the only ecosystem that provides constitutional governance at the agent layer.

---

## Interoperability Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│  ANY CODING CLI (OpenCode / Claude / Codex / Kimi / Grok /         │
│  Copilot / Continue / Antigravity)                                  │
│                                                                     │
│  Reads: AGENTS.md / CLAUDE.md  ←── AAA Memory (Primitive 1)       │
│  Loads: skills/<id>/SKILL.md   ←── compile.py output (Primitive 2) │
│  Spawns: subagents              ←── per-CLI native (Primitive 3)   │
│  Fires:  hooks                  ←── per-CLI hooks (Primitive 4)    │
│  Calls:  MCP tools              ←── arifOS 27-tool surface (P5)   │
└──────────────────────────────────┬─────────────────────────────────┘
                                   │ MCP (JSON-RPC)
                                   ▼
┌────────────────────────────────────────────────────────────────────┐
│  arifOS CONSTITUTIONAL KERNEL (port 8088)                           │
│                                                                     │
│  Primitive 6: F1–F13 Floors (every tool call checked)             │
│  Primitive 7: 888_JUDGE Verdict (SEAL/HOLD/VOID/SABAR)            │
│  Primitive 8: VAULT999 Receipt (hash-chained, append-only)         │
└─────────────────────────────────────────────────────────────────────┘
```

**The interop principle:** Any CLI with MCP support can call arifOS tools.
When it does, it implicitly enters the constitutional layer — floors are checked,
verdicts are issued, receipts are written. The CLI never needs to know.

---

## Compilation Path (Multi-CLI Skill Deployment)

One canonical skill definition → 8 vendor-specific outputs:

```
skills/<id>/SKILL.md                 ← canonical source (AAA)
│
├── skills/<id>/claude/SKILL.md      ← Claude Code
├── skills/<id>/openai/README.md     ← Codex / OpenAI CLI
├── skills/<id>/kimi/SKILL_MD.md        ← Kimi Code
├── skills/<id>/opencode/README.md   ← OpenCode
├── skills/<id>/grok/SKILL_MD.md        ← Grok Build
├── skills/<id>/copilot/<id>.agent.md ← GitHub Copilot CLI
├── skills/<id>/continue/SKILL_MD.md    ← Continue.dev
└── skills/<id>/antigravity/SKILL_MD.md ← Antigravity
```

**Tool:** `python skills/compile.py` — reads `host_compatibility` from SKILL.md frontmatter,
generates all declared vendor outputs. See `skills/compile.py` for implementation.

---

## Onboarding Any CLI to AAA

### Step 1 — Memory (30 min)
Ensure `AGENTS.md` (or `CLAUDE.md` for Claude Code) exists at repo root
with arifOS constitution, boot sequence, and federation context.

### Step 2 — Skills (compile.py, automated)
Add target CLI to skill's `host_compatibility` list. Run `python skills/compile.py`.
Vendor-specific skill files are generated automatically.

### Step 3 — MCP (per CLI config, 1 hour)
Add arifOS MCP server to the CLI's config:
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["/root/arifOS/server.py"],
      "transport": "stdio"
    }
  }
}
```
Or HTTP: `http://72.62.71.199:8088/mcp` (SSE transport).

### Step 4 — Hooks (optional, per CLI)
Wire `PreToolUse` hook to call `arif_get_affordance` before dangerous tool calls.
Wire `PostToolUse` hook to emit receipt to VAULT999.
See `hooks/` directory for reference implementations.

### Step 5 — Agent Card (A2A, for true AAA Agents)
If the CLI wraps a governed agent (not just uses AAA tools), publish:
`/.well-known/agent-card.json` with `aaa_extension` block.
See `AAA_AGENT.md` §3.

---

## Quick Reference

### Vocabulary translation (single term)

| You hear... | In CLI... | AAA canonical term |
|---|---|---|
| "Memory" / "project instructions" | Any CLI | AAA Constitution (`AGENTS.md`) |
| "Skill" / "slash command" | Claude Code | AAA Skill (`SKILL.md`) |
| "Skill" / "agent skill" | Codex / Copilot | AAA Skill (compiled) |
| "Subagent" / "worker" | Any CLI | AAA Agent (if constitutional) |
| "Hook" / "lifecycle script" | Claude Code / Grok | AAA Hook |
| "MCP server" | Any CLI | arifOS MCP surface |
| — (not present) | Any CLI | **AAA Floor** |
| — (not present) | Any CLI | **AAA Verdict** |
| — (not present) | Any CLI | **AAA Receipt** |

### The three things only AAA has

1. **Floor** — a constitutional constraint no agent can override
2. **Verdict** — a judgment with floor trace + confidence + VAULT999 seal
3. **Receipt** — an immutable hash-chained audit record

These are not features you can add to an existing CLI by config.
They require the arifOS constitutional kernel.

---

## Related Documents

| Document | Role |
|---|---|
| `AAA_AGENT.md` | Formal 5-clause definition of an AAA Agent |
| `AAA_ZEN.md` | 15 axioms of the Zen of Agentic Python |
| `AGENTSKILLTREE.md` | 22 machine self-optimization skills, 6 tiers |
| `ZENTOSILICASPEC.md` | Constitutional floors → machine substrate specification |
| `skills/SKILL_TEMPLATE.md` | Canonical skill template with `host_compatibility` |
| `skills/compile.py` | Multi-CLI skill compiler (reads `host_compatibility`, writes vendor outputs) |
| `UNIFIED_AGENT.md` | Architecture: 8 agents, one constitutional kernel |
| `AAA_FEDERATION_CONSTITUTION.md` | Full F1–F13 constitutional text |

---

*Forged: 2026-06-26*
*DITEMPA BUKAN DIBERI — The Rosetta Stone is forged, not negotiated.*
