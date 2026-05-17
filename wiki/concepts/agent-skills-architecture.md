---
title: "Agent Skills Architecture — Cross-Platform Landscape"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: concept
tags: [skills, architecture, cross-platform, claude, openclaw, openai, copilot, codex, federation]
---

# Agent Skills Architecture — Cross-Platform Landscape

> **Classification:** Cross-platform skills interoperability
> **Problem:** Claude Agent Skills, OpenClaw system prompts, OpenAI tool defs use different formats
> **Solution:** AAA wiki as canonical skill spec → per-platform adapters

---

## Landscape: How Platforms Model Skills

### Claude Agent Skills (Anthropic / Hermes)

**Format:** Folder-based packages with `SKILL.md`
```
~/.hermes/skills/{skill-name}/
├── SKILL.md              ← REQUIRED (metadata + instructions)
├── DESCRIPTION.md        ← one-line summary for discovery
├── references/          ← supporting docs
├── scripts/             ← optional executable code
└── assets/             ← images, data files
```

**SKILL.md frontmatter:**
```yaml
---
name: claude-code
description: "Delegate coding to Claude Code CLI"
version: 2.2.0
author: Hermes Agent + Teknium
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Claude, Anthropic]
    related_skills: [codex, opencode]
---
```

Body: Markdown instructions with trigger conditions, numbered steps, pitfalls section, verification steps.

**Discovery flow:** Read DESCRIPTION.md → if relevant, load SKILL.md → execute.

**Sub-directory pattern for nested skills:**
```
skills/autonomous-ai-agents/claude-code/SKILL.md
skills/autonomous-ai-agents/codex/SKILL.md
```

---

### OpenClaw Skills

**Format:** Agent directory with `system.md` + `agent.json`
```
~/.openclaw/agents/{agent-name}/
├── system.md            ← constitutional prompt + F1-F13 floors
├── agent.json           ← agent configuration (optional)
├── sessions/           ← conversation history
└── registry.sqlite     ← flows and state
```

**system.md structure:**
- Constitutional prompt with F1-F13 floors
- Session boot sequence (ROOT_CANON → SOUL → USER → AGENTS → IDENTITY → MEMORY)
- Reply template (To/From/CC/Title/Context/Verdict/Way Forward/Seal)
- 888_HOLD triggers
- Operator identity (Arif)

**Key difference from Claude:** No standardized SKILL.md. Skills embedded directly in agent system prompt. No nested folder structure for skill variants — monolithic agent definition.

---

### OpenAI / Codex / Agents SDK

**Format:** JSON tool definitions + SDK config
```
tools/
├── tool.json           ← function schema (JSON Schema)
├── tool definitions    ← code-level function specs
└── agent config        ← agents SDK registry
```

**Tool definition (JSON Schema):**
```json
{
  "type": "function",
  "function": {
    "name": "delegate_coding",
    "description": "Delegate coding to Claude Code CLI",
    "parameters": {
      "type": "object",
      "properties": {
        "task": { "type": "string" },
        "allowedTools": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

**Key difference:** Skills as tool bundles. No folder-based packages. Skills declared in code/SDK config. Function-level granularity rather than procedure-level.

---

## The Fragmentation Problem

| Dimension | Claude | OpenClaw | OpenAI/Codex |
|-----------|--------|----------|--------------|
| **Format** | SKILL.md folder | system.md + agent.json | JSON tool def |
| **Path** | `~/.hermes/skills/name/` | `~/.openclaw/agents/name/` | `tools/` dir |
| **Discovery** | Read DESCRIPTION.md | Query registry.sqlite | SDK config load |
| **Granularity** | Folder packages | Single agent files | Function-level |
| **Safety** | Skill tags + metadata | Constitutional F-floors | Tool permissions |
| **Nesting** | Sub-directory per variant | Flat agent list | Flat tool list |

**Result:** Same skill duplicated 3x with drift between versions. No single source of truth.

---

## Solution: AAA Wiki as Canonical Skill Spec

### Core Principle

> **Describe each skill once in AAA/wiki/skills/ using platform-neutral format. Generate per-platform adapters from the canonical spec.**

### Canonical Skill Spec Fields

| Field | Purpose |
|-------|---------|
| `name` | Canonical identifier (e.g. `spatial-grounding`) |
| `version` | Semantic versioning (e.g. `1.0.0`) |
| `summary` | One-line description |
| `category` | Domain: geo, wealth, infra, governance |
| `risk_band` | Aligned to F1-F13 floors |
| `trigger_conditions` | When to activate this skill |
| `procedure` | Numbered steps in human-readable format |
| `preconditions` | Required tools, data, auth |
| `expected_outputs` | What the skill produces |
| `failure_modes` | What can go wrong + mitigations |
| `verification` | How to confirm the skill worked |
| `sources` | Raw evidence references |
| `scars` | Incidents where this skill failed |

### Adapter Structure

```
AAA/skills/{skill-name}/
├── SKILL.md              ← canonical (platform-neutral, in wiki/)
├── claude/SKILL.md       ← Claude Agent Skills format
├── openclaw/system.md    ← OpenClaw agent format
├── openai/tool.json      ← OpenAI agents SDK tool def
└── mcp/manifest.json     ← MCP tool manifest (if applicable)
```

---

## How AAA Solves Each Problem

| Problem | Without AAA | With AAA |
|---------|-------------|----------|
| Skill format drift | Each platform version differs | Canonical spec → all adapters derived |
| Reuse across agents | Copy-paste skills per agent | One wiki page → all platform adapters |
| Scar propagation | Bug fixes only in one agent | Fix wiki → regenerate all adapters |
| Discovery | Unclear what skills exist | AAA/wiki/index.md shows all skills |
| Governance | F-floors only on OpenClaw | F-floors embedded in canonical spec |

---

## First Canonical Skill Example

See [[skill-spatial-grounding]] — this is the first skill documented in both:
- Canonical wiki format (AAA/wiki/skills/skill-spatial-grounding.md)
- Claude adapter format (AAA/skills/spatial-grounding/claude/SKILL.md)

---

## Migration Path

1. **Define first canonical skill** in `AAA/wiki/skills/skill-spatial-grounding.md` ✅ (done)
2. **Create Claude adapter** in `AAA/skills/spatial-grounding/claude/SKILL.md` (pending)
3. **Create OpenClaw adapter** in `AAA/skills/spatial-grounding/openclaw/system.md` (pending)
4. **Log the mapping** in `AAA/wiki/log.md`
5. **Repeat** for next skill (skill-arif-workflow, skill-domain-ingest, etc.)

Over time, platform adapters are regenerated from wiki canonical — not hand-maintained.

---

## Related Pages

- [[skill-spatial-grounding]] — first canonical skill with real examples
- [[anti-fabrication-protocol]] — why verification before claim matters
- [[scar-hermes-fabrication-2026-05-17]] — the incident that exposed skill fragmentation

---

*DITEMPA BUKAN DIBERI — Skills are forged, not copied.*
*999 SEAL ALIVE*