# Cross-Platform Agent Skills Formats — Reference

> **Type:** Research notes / Knowledge capture
> **Source:** Session 2026-05-17 — deep research on agent skills interoperability
> **For:** `llm-wiki` skill, federation wiki extension

---

## Format Landscape

### Claude Agent Skills (Anthropic / Hermes convention)

**Path:** `~/.hermes/skills/{skill-name}/SKILL.md`
**Discovery:** `DESCRIPTION.md` (one-line) → full `SKILL.md`
**Structure:**
```
skills/
└── {skill-name}/
    ├── SKILL.md          # REQUIRED — YAML frontmatter + markdown body
    ├── DESCRIPTION.md    # one-line for discovery
    ├── references/       # supporting docs
    ├── scripts/          # optional executable code
    └── assets/           # images, data files
```

**Frontmatter schema:**
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

**Sub-directory nesting pattern** (for skill families):
```
skills/autonomous-ai-agents/
├── SKILL.md              # category-level overview
├── claude-code/
│   └── SKILL.md          # specific tool skill
├── codex/
│   └── SKILL.md
├── opencode/
│   └── SKILL.md
└── hermes-agent/
    └── SKILL.md
```

**Body sections** (per actual skill files):
- Trigger conditions
- Numbered procedure steps
- Pitfalls section
- Verification commands
- Failure modes + mitigations

---

### OpenClaw Agents

**Path:** `~/.openclaw/agents/{agent-name}/`
**Structure:**
```
agents/
└── {agent-name}/
    ├── system.md         # constitutional prompt + F1-F13 floors
    ├── agent.json        # agent configuration (optional)
    ├── sessions/         # conversation history
    └── registry.sqlite   # flows and state (binary)
```

**system.md structure** (per actual file at `/root/.openclaw/agents/main/system.md`):
- Constitutional prompt header
- Session boot sequence (ROOT_CANON → SOUL → USER → AGENTS → IDENTITY → MEMORY)
- F-floors (F1-F13)
- 888_HOLD triggers
- Reply template (To/From/CC/Title/Context/Verdict/Way Forward/Seal)
- Operator identity

**Key difference from Claude:** No standardized SKILL.md. Skills embedded directly in agent system prompt. No nested folder structure. Monolithic agent definition per agent.

**Skills storage:** No separate skill folder — each OpenClaw agent is self-contained. Skills are not portable between OpenClaw agents without copying system.md content.

---

### OpenAI / Codex / Agents SDK

**Format:** JSON tool definitions + SDK config
**Path:** `tools/` directory or SDK registry

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

**Key difference:** Function-level granularity. Skills as tool bundles. No folder-based packages. Skills declared in code/SDK config — not standalone markdown files.

---

## Fragmentation Matrix

| Dimension | Claude Agent Skills | OpenClaw | OpenAI/Codex |
|-----------|---------------------|----------|---------------|
| **Format** | SKILL.md folder | system.md + agent.json | JSON tool def |
| **Path** | `~/.hermes/skills/name/` | `~/.openclaw/agents/name/` | `tools/` dir |
| **Discovery** | Read DESCRIPTION.md | Query registry.sqlite | SDK config load |
| **Granularity** | Folder packages | Single agent files | Function-level |
| **Safety** | Skill tags + metadata | Constitutional F-floors | Tool permissions |
| **Nesting** | Sub-directory per variant | Flat agent list | Flat tool list |
| **Skill portability** | Copy folder → works | Copy system.md | Copy tool def |
| **Config update** | Edit SKILL.md | Edit system.md | Edit JSON + code |

---

## Canonical Skill Spec (AAA Pattern)

When the wiki serves as the single source of truth for skills, the canonical spec fields are:

| Field | Purpose |
|-------|---------|
| `name` | Canonical identifier |
| `version` | Semantic versioning |
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

---

## Adapter Generation Pattern

**File structure:**
```
AAA/skills/{skill-name}/
├── SKILL.md              ← canonical (in wiki/skills/)
├── claude/SKILL.md       ← Claude Agent Skills format
├── openclaw/system.md    ← OpenClaw agent format
├── openai/tool.json      ← OpenAI agents SDK tool def
└── mcp/manifest.json     ← MCP tool manifest (if applicable)
```

**Generation flow:**
1. Define canonical skill in `AAA/wiki/skills/{skill-name}.md`
2. Generate Claude adapter: extract name, description, procedure, pitfalls → SKILL.md format
3. Generate OpenClaw adapter: embed SPATIAL_LAW + F-floors into system.md section
4. Generate OpenAI adapter: map procedure steps to function definitions
5. Log each adapter creation in `AAA/wiki/log.md`

**Current adapters implemented:**
- `AAA/skills/spatial-grounding/claude/SKILL.md` ✅
- `AAA/skills/spatial-grounding/openclaw/system.md` ✅
- `AAA/skills/spatial-grounding/openai/tool.json` — pending

---

## Key Lessons from Session

1. **Three formats, one problem:** Claude (folder+SKILL.md), OpenClaw (system.md+agent.json), OpenAI (JSON tool def) all represent "skill = metadata + instructions" but with incompatible schemas.

2. **AAA solution:** Wiki as canonical spec. Describe once, generate adapters.

3. **Adapter location:** `/root/AAA/skills/{name}/{platform}/` — not in the wiki itself (wiki is canonical, adapters are derived artifacts).

4. **First canonical skill:** `skill-spatial-grounding` — demonstrates full pattern including two platform adapters.

5. **Naming pattern:** Skill names at class level: `skill-spatial-grounding`, `skill-arif-workflow` — not task-specific names.

---

*For context, see: `AAA/wiki/concepts/agent-skills-architecture.md`*
*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*