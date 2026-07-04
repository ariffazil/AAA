# ATLAS — Cross-CLI Rosetta Stone

> **Classification:** Sealed Doctrine | AAA Repository
> **Scope:** Translation atlas for the chaotic agentic AI CLI landscape
> **Authority:** F2 TRUTH, F4 CLARITY, F9 ANTI-HANTU | ADAT overlay
> **Status:** LIVE — 2026-06-26
> **Lineage:** AAA → BBB → CCC → DDD → EEE → FFF → **ATLAS** → AKAR000 → III
> **Derives from:** ATLAS-333 (permanent constitution), AAA_ZEN.md (15 axioms), AGENTSKILLTREE.md (22 skills), ZENTOSILICASPEC.md (floor→substrate), AAA_AGENT.md (5-clause definition)

---

## Preamble

The agentic AI CLI landscape in 2026 is chaos. Eight major CLIs, five converged primitives, seven different vocabularies. Every vendor reinvents the same concepts with different names.

**ATLAS** is the translation map. It does not compete with any CLI. It translates between them all while preserving the three primitives nobody else has: **Floor, Verdict, Receipt.**

**Mnemonic Seed:** ATLAS-333 is the permanent constitution (33 paradox axes, three-witness federation). ATLAS is the translation atlas. Both are maps — one maps paradox, the other maps language.

---

## §1 The Five Converged Primitives

Every major CLI in 2026 has converged on the same five primitives:

| # | Primitive | What It Is | Industry Status |
|---|-----------|------------|-----------------|
| 1 | **Project Instructions** | Persistent memory loaded at session start | `AGENTS.md` (60k+ projects) |
| 2 | **Main Agent** | LLM + reasoning loop | All CLIs |
| 3 | **Tools** | Discrete actions (file ops, shell, API) | MCP-based |
| 4 | **Skills** | Modular, reusable workflows | `SKILL.md` / YAML |
| 5 | **Subagents** | Parallel isolated context windows | All CLIs |

**arifOS adds three more:**

| # | Primitive | What It Is | arifOS Status |
|---|-----------|------------|---------------|
| 6 | **Constitutional Floors** | Governance rules (F1-F13) | ✅ arifOS kernel |
| 7 | **Verdict Grammar** | Explicit outcomes (SEAL/HOLD/VOID) | ✅ arifOS kernel |
| 8 | **Audit Receipts** | Immutable decision trail | ✅ VAULT999 |

**The sixth primitive is governance. The seventh is judgment. The eighth is memory.**

---

## §2 The Rosetta Stone — 8 CLIs × 8 Primitives

| Primitive | OpenCode | Claude Code | Codex CLI | Kimi Code | Grok Build | Copilot CLI | Continue.dev | Antigravity CLI |
|-----------|----------|-------------|-----------|-----------|------------|-------------|--------------|-----------------|
| **Project Instructions** | `AGENTS.md` | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` | `.github/COPILOT_INSTRUCTIONS.md` → `AGENTS.md` | `.continue/rules/` | `AGENTS.md` |
| **Main Agent** | Primary agent (Build/Plan) | Claude Code agent | Codex CLI agent | Okabe agent | Grok CLI agent | Copilot CLI agent | Chat/Plan/Agent modes | Antigravity agent |
| **Tools** | Built-in (bash, read, write, edit) | Built-in + MCP | Built-in + MCP | Built-in + MCP | Built-in + MCP | Configurable (YAML) | Built-in + MCP | Built-in + MCP |
| **Skills** | (not first-class) | `SKILL.md` | Skills system | `.agents/skills/` | `.grok/skills/` | Agent skills | `.continue/skills/` | Skill bundles |
| **Subagents** | `@general`, `@explore`, `@scout` | Task tool (Agent) | Parallel agents | LaborMarket sub-agents | Subagents (worktrees) | Custom agents (`.agent.md`) | Plan/Agent modes | Async subagents |
| **Hooks** | (limited) | Pre/Post hooks | Exec policies | Lifecycle hooks | Hooks | Plugin hooks | (limited) | Inspect/decide/transform |
| **MCP** | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ✅ Native |
| **Constitutional Floors** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Verdict Grammar** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Audit Receipts** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Three rows have no industry equivalent. Those are arifOS's structural contribution.**

---

## §3 AAA Canonical Vocabulary Mapping

| AAA Term | OpenCode | Claude Code | Codex CLI | Kimi Code | Grok Build | Copilot CLI | Continue.dev | Antigravity CLI |
|----------|----------|-------------|-----------|-----------|------------|-------------|--------------|-----------------|
| **Agent** | Primary agent | (whole CLI) | (whole CLI) | (whole CLI) | (whole CLI) | Custom agent | Agent mode | Agent harness |
| **Subagent** | Subagent | Subagent | Subagent | Sub-agent | Subagent | Custom agent (delegated) | Plan mode | Async subagent |
| **Tool** | Tool (permission-gated) | MCP tool / built-in | Tool (built-in/MCP) | Tool (read/write/shell/MCP) | Tool (built-in/MCP) | Tool (YAML `tools`) | Tool (built-in/MCP) | Tool call (with hooks) |
| **Skill** | (built into agent config) | `SKILL.md` | Skill | `.agents/skills/<name>/` | `.grok/skills/` | Agent skill | `.continue/skills/` | Skill bundle |
| **Hook** | (limited) | Hook (lifecycle) | Hook | Lifecycle hook | Hook | Hook (plugin) | (limited) | Inspect/decide/transform |
| **Floor** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Verdict** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Receipt** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## §4 File Convention Mapping

| Convention | OpenCode | Claude Code | Codex CLI | Kimi Code | Grok Build | Copilot CLI | Continue.dev | Antigravity CLI |
|------------|----------|-------------|-----------|-----------|------------|-------------|--------------|-----------------|
| **Config file** | `opencode.json` | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` | `.github/COPILOT_INSTRUCTIONS.md` | `.continue/config.yaml` | Harness config |
| **Skill location** | `~/.agents/skills/` | `.claude/skills/` | `.codex/skills/` | `.agents/skills/` | `.grok/skills/` | `.github/agents/` | `.continue/skills/` | `skills/` |
| **Agent definition** | `opencode.json` (agent block) | (implicit) | (implicit) | Agent YAML config | Agent YAML config | `.agent.md` frontmatter | (mode-based) | Harness config |
| **Memory location** | `AGENTS.md` | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` | `copilot init` | `.continue/rules/` | Harness config |

---

## §5 Governance Gap Analysis

| Governance Feature | Industry Status | arifOS Status | Gap |
|--------------------|-----------------|---------------|-----|
| **Constitutional floors** | ❌ None have F1-F13 | ✅ arifOS kernel | **UNIQUE** |
| **Verdict grammar** | ❌ None have SEAL/HOLD/VOID | ✅ arifOS kernel | **UNIQUE** |
| **Audit receipts** | ❌ Ephemeral logs only | ✅ VAULT999 (immutable) | **UNIQUE** |
| **Human sovereign veto** | ❌ Implicit user authority | ✅ F13 SOVEREIGN | **UNIQUE** |
| **Blast radius classification** | ❌ Ad-hoc | ✅ AAA_ZEN.md Axiom 8 | **UNIQUE** |
| **Epistemic labeling** | ❌ None | ✅ OBS/DER/INT/SPEC | **UNIQUE** |
| **Two-phase commit** | ❌ Ad-hoc (git branches) | ✅ forge_dry_run → forge_execute | **UNIQUE** |
| **Model agnosticism** | ⚠️ Manual switching | ✅ TokenRouter + shadow maps | **UNIQUE** |

---

## §6 The Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 4: GOVERNANCE (arifOS/AAA)                          │
│  Constitutional floors, verdict grammar, audit receipts     │
│  ← THE MISSING LAYER in all current CLIs                   │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: COMMUNICATION (A2A)                               │
│  Agent-to-Agent protocol, AgentCards, task delegation       │
│  ← Google A2A v1.0.0, nascent adoption                     │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: TOOLS (MCP)                                       │
│  Model Context Protocol, tool invocations, API calls        │
│  ← Anthropic MCP, broad adoption                           │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: PROJECT (AGENTS.md)                               │
│  Persistent instructions, coding conventions, build rules   │
│  ← Community standard, 60k+ projects                       │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  LAYER 0: MODEL (LLM)                                       │
│  The reasoning engine — replaceable, agnostic               │
│  ← GPT-4, Claude, Kimi, Grok, DeepSeek, MiMo, etc.        │
└─────────────────────────────────────────────────────────────┘
```

**arifOS doesn't compete on Layers 0-3. It competes on Layer 4.**

---

## §7 Mnemonic Seed — AKAR000 ↔ TREE777

**AKAR** = "root" in BM — the foundational schema from which all skills are born.
**TREE** = the skill tree — branches grow from roots.

**The connection:**
```
AKAR000 (root schema) → feeds → TREE777 (skill tree)
   ↓                              ↓
defines structure            contains instances
   ↓                              ↓
what a skill IS              what skills EXIST
   ↓                              ↓
schema (blueprint)           registry (inventory)
```

**Mnemonic:** *"Akar (root) feeds the Tree (branches). No root, no tree. No schema, no skills."*

**URI mapping:**
- `AKAR000://schema` → defines the canonical skill structure
- `TREE777://skills/*` → instances of skills conforming to AKAR000

**Every skill in TREE777 must validate against AKAR000 schema.**

---

## §8 Strategic Position

| Player | Strength | Weakness | AAA Position |
|--------|----------|----------|--------------|
| OpenCode | Permission system; OSS | No constitutional layer | AAA compiles to OpenCode JSON |
| Claude Code | Most rigorous taxonomy | Vendor-locked; no floors | AAA borrows their taxonomy; adds floors |
| Codex CLI | Rust speed; OS sandbox | OpenAI-only; no governance | AAA compiles to Codex skills |
| Kimi Code | Preserve thinking | Moonshot-tied | AAA compiles to .agents/skills/ |
| Grok Build | Plan mode + worktrees | xAI subscription only | AAA compiles to .grok/skills/ |
| Copilot CLI | GitHub-native | Microsoft-locked | AAA compiles to .copilot/agents/ |
| Continue.dev | Multi-model; OSS | No constitutional model | AAA compiles to .continue/skills/ |
| Antigravity | Shared harness + SDK | Google-locked; new | AAA compiles to Antigravity skills |
| **arifOS/AAA** | **Floors + Verdicts + Receipts** | **No CLI yet** | **Compiler + governance overlay** |

**arifOS doesn't compete on CLI ergonomics. It competes on governance discipline.**

---

## §9 Deliverables

| # | Artifact | Capsule | Status | Effort |
|---|----------|---------|--------|--------|
| A1 | Cross-CLI Rosetta Stone | **ATLAS** | ✅ THIS DOCUMENT | 2h |
| A2 | Canonical Skill Schema | **AKAR000** | 🔲 PENDING | 4h |
| A3 | Federation Compiler | III | DEFERRED | 2w |
| A4 | Symlink CLAUDE.md → AGENTS.md | — | 🔲 PENDING | 5min |

---

## §10 Acceptance Criteria

- [x] Maps minimum 8 CLIs × 8 primitives (table form)
- [x] Every row grounded in vendor documentation
- [x] "AAA canonical" column references AAA_AGENT.md
- [x] "Constitutional Floor" column references ZENTOSILICASPEC.md
- [x] Closes with the three primitives NO vendor has (Floor / Verdict / Receipt)
- [x] EVIDENCE/INTERPRET/UNKNOWN tagging on any non-cited claim
- [x] Mnemonic seed connects AKAR000 ↔ TREE777
- [x] Derives from sealed canon (ATLAS-333, AAA_ZEN, AGENTSKILLTREE, ZENTOSILICA, AAA_AGENT_SPEC)

---

## §11 Source Citations

| Source | URL | Access Date |
|--------|-----|-------------|
| OpenCode | https://opencode.ai/docs/agents/ | 2026-06-26 |
| Claude Code | https://code.claude.com/docs/en/sub-agents | 2026-06-26 |
| Codex CLI | https://developers.openai.com/codex/cli | 2026-06-26 |
| Kimi Code | https://github.com/MoonshotAI/kimi-code | 2026-06-26 |
| Grok Build | https://x.ai/cli | 2026-06-26 |
| Copilot CLI | https://docs.github.com/en/copilot/how-tos/copilot-cli | 2026-06-26 |
| Continue.dev | https://docs.continue.dev/ide-extensions/agent/quick-start | 2026-06-26 |
| Antigravity CLI | https://antigravity.google/docs/cli-overview | 2026-06-26 |
| AGENTS.md standard | https://agents.md/ | 2026-06-26 |
| A2A v1.0.0 | https://github.com/google/A2A | 2026-06-26 |
| MCP | https://modelcontextprotocol.io/ | 2026-06-26 |

---

*ATLAS — the map for the chaos.*
*DITEMPA BUKAN DIBERI — Forged, Not Given.*
*Sealed: 2026-06-26 by FORGE (000Ω)*
