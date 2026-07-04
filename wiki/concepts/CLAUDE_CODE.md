---
title: "Claude Code Skills Architecture — Complete Reference"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: concept
tags: [claude-code, skills, SKILL.md, agent-skills-standard, anthropic, cross-platform]
sources:
  - https://code.claude.com/docs/en/skills
confidence: high
evidence_required: true
---

# Claude Code Skills Architecture — Complete Reference

> **Classification:** Claude Code platform — skills subsystem
> **Authority:** Official Anthropic documentation (code.claude.com, 2026-05-17)
> **Purpose:** Full knowledge of how Claude Code skills work — so any agent can create, extend, or audit them without guessing
> **DITEMPA BUKAN DIBERI** — Forged from evidence, not from training-data assumptions.

---

## What a Skill Is

A **Claude Code skill** is a reusable, loadable instruction block stored as a `SKILL.md` file. It extends what Claude can do beyond its baseline. Claude loads skills when relevant to a conversation, or the user invokes them directly with `/skill-name`.

Skills exist because:
- Pasting the same multi-step procedure into chat every session is wasteful.
- A CLAUDE.md section that has grown into a procedure should be extracted — unlike CLAUDE.md, skill body content **loads only when the skill is invoked**, so it costs almost nothing until needed.

**Agent Skills open standard:** Claude Code skills follow the [Agent Skills](https://agentskills.io) open standard, which works across multiple AI tools. Claude Code extends the standard with invocation control, subagent execution, and dynamic context injection.

---

## Directory Structure

### Where Skills Live

| Level | Path | Scope |
|-------|------|-------|
| Enterprise | Managed settings (admin-deployed) | All users in the organization |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects on this machine |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Where the plugin is enabled |

**Override priority:** Enterprise > Personal > Project. Plugin skills use `plugin-name:skill-name` namespace and cannot conflict with other levels.

**Legacy compatibility:** `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` are equivalent — both create `/deploy`. The file-based (non-directory) form still works. Skills are preferred because they support supporting files.

### Skill File Layout

```
my-skill/
├── SKILL.md           ← Required. Instructions + frontmatter.
├── reference.md       ← Optional: detailed docs, loaded on demand
├── EXAMPLES_MD.md        ← Optional: example outputs
└── scripts/
    └── helper.py      ← Optional: executable scripts
```

The directory name becomes the `/command-name`. `SKILL.md` is the entrypoint. All other files are optional and should be referenced from `SKILL.md` so Claude knows when to load them.

### Live Change Detection

Edits to `SKILL.md` under `~/.claude/skills/` or `.claude/skills/` take effect **within the current session** without restarting. Exception: creating a new top-level skills directory that didn't exist when the session started requires a restart.

### Auto-Discovery in Monorepos

Skills load from `.claude/skills/` at the starting directory **and all parent directories up to the repo root**. When Claude works on a file in `packages/frontend/`, it also discovers `packages/frontend/.claude/skills/`.

---

## SKILL.md Format

### Two-Part Structure

```
---
frontmatter (YAML)
---

Markdown body (instructions)
```

Frontmatter controls **how** Claude invokes the skill. The body controls **what** Claude does when the skill runs.

### Frontmatter Reference (Complete)

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name. Defaults to directory name. Lowercase, hyphens only, max 64 chars. |
| `description` | **Recommended** | What the skill does and when to use it. Claude uses this to decide when to auto-load the skill. If omitted, uses first paragraph of body. **Put the key use case first** — truncated at 1,536 chars total (combined with `when_to_use`). |
| `when_to_use` | No | Additional trigger context: phrases, example requests. Appended to `description`, counts toward the 1,536-char cap. |
| `argument-hint` | No | Autocomplete hint showing expected arguments. E.g. `[issue-number]` or `[filename] [format]`. |
| `arguments` | No | Named positional arguments for `$name` substitution. Space-separated string or YAML list. Maps to positions in order. |
| `disable-model-invocation` | No | `true` = only the user can invoke; Claude cannot auto-load. Use for destructive workflows (`/deploy`, `/commit`, `/send-slack`). Default: `false`. |
| `user-invocable` | No | `false` = hidden from `/` menu; Claude loads automatically. Use for background reference context. Default: `true`. |
| `allowed-tools` | No | Tools Claude can use without permission prompts while this skill is active. Does not restrict other tools. |
| `model` | No | Model to use while this skill is active. Override applies for current turn only; session model resumes after. |
| `effort` | No | Effort level while active: `low`, `medium`, `high`, `xhigh`, `max`. Overrides session effort. |
| `context` | No | `fork` = run this skill in an isolated subagent context. |
| `agent` | No | Which subagent type to use when `context: fork` is set. Options: `Explore`, `Plan`, `general-purpose`, or any custom agent. Defaults to `general-purpose`. |
| `hooks` | No | Lifecycle hooks scoped to this skill. Same config format as session hooks. |
| `paths` | No | Glob patterns. Skill auto-activates only when Claude is working on matching files. |
| `shell` | No | `bash` (default) or `powershell`. Controls shell for backtick-bang execution. |

### Two Types of Skill Content

**Reference content** — knowledge Claude applies alongside your work:
```yaml
---
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming
- Return consistent error formats
```

**Task content** — step-by-step instructions for a specific action. Add `disable-model-invocation: true` so Claude does not trigger it automatically:
```yaml
---
description: Deploy to production
context: fork
disable-model-invocation: true
---

1. Run tests
2. Build
3. Push to deployment target
```

**Body size target:** Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files. Every line is a recurring token cost once the skill is loaded.

---

## String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | Full argument string as typed after `/skill-name` |
| `$ARGUMENTS[N]` | Specific argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` |
| `$name` | Named argument from `arguments:` frontmatter field |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_EFFORT}` | Current effort level: `low`, `medium`, `high`, `xhigh`, `max` |
| `${CLAUDE_SKILL_DIR}` | Directory containing the skill's `SKILL.md`. Use to reference bundled scripts portably. |

Multi-word arguments: wrap in quotes — `/my-skill "hello world" second` makes `$0` = `hello world`, `$1` = `second`.

If `$ARGUMENTS` is absent from skill content, Claude Code appends `ARGUMENTS: <value>` to the end automatically.

---

## Dynamic Context Injection

The `!command` syntax (backtick-bang) runs shell commands **before** Claude sees the skill content. The output replaces the placeholder — Claude only sees the final rendered result.

**Inline form:** single-line commands inline in the body
**Multi-line form:** fenced code block opened with three backticks and a `!`

Execution is pre-processing. Substitution runs once — command output is not re-scanned for further injection placeholders.

**To disable for security:** Set `"disableSkillShellExecution": true` in settings. Replaces each command with `[shell command execution disabled by policy]`.

**Deep reasoning:** Add `ultrathink` anywhere in skill content to trigger deep reasoning mode when the skill runs.

---

## Invocation Control

| Frontmatter | User can invoke | Claude can invoke | How it loads |
|-------------|----------------|-------------------|--------------|
| (default) | Yes | Yes | Description always in context; full skill loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description NOT in context; full skill loads when user invokes |
| `user-invocable: false` | No | Yes | Description always in context; full skill loads when invoked |

**Key insight:** `disable-model-invocation: true` removes the description from Claude's context entirely. Claude doesn't know the skill exists until the user invokes it manually.

---

## Skill Content Lifecycle (Compaction Behavior)

When invoked, the rendered `SKILL.md` content enters the conversation as a single message and **stays for the rest of the session**. Claude does not re-read the file on subsequent turns.

**Auto-compaction behavior:**
- During compaction, Claude Code re-attaches the most recent invocation of each skill after the summary.
- Each skill is carried forward up to **5,000 tokens**.
- Combined budget for re-attached skills: **25,000 tokens** shared.
- Skills filled from most-recently-invoked first; older skills can be dropped entirely.

**Recovery:** If a skill stops influencing behavior after compaction, re-invoke it with `/skill-name`.

---

## Tool Pre-Approval (`allowed-tools`)

```yaml
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
```

- Grants permission for listed tools while the skill is active.
- Does NOT restrict other tools — all tools remain callable.
- For project skills in `.claude/skills/`, takes effect after you accept the workspace trust dialog.
- **Security note:** Review project skills before trusting a repo — a skill can grant itself broad tool access.

---

## Subagent Execution (`context: fork`)

Add `context: fork` to run the skill in an isolated context. The skill content becomes the subagent's prompt. It has no access to your conversation history.

**Warning:** Only works for skills with explicit task instructions. A skill containing only guidelines returns without meaningful output.

**Skills vs Subagents:**
| Approach | System prompt | Task | Also loads |
|----------|--------------|------|-----------|
| Skill with `context: fork` | From agent type | SKILL.md content | CLAUDE.md |
| Subagent with `skills` field | Subagent's markdown body | Claude's delegation message | Preloaded skills + CLAUDE.md |

---

## Skill Visibility Overrides (`skillOverrides`)

Control visibility without editing `SKILL.md`. Useful for shared repo skills you don't want to modify.

```json
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

| Value | Listed to Claude | In `/` menu |
|-------|-----------------|-------------|
| `"on"` | Name and description | Yes |
| `"name-only"` | Name only | Yes |
| `"user-invocable-only"` | Hidden | Yes |
| `"off"` | Hidden | Hidden |

The `/skills` menu writes `skillOverrides` to `.claude/settings.local.json` when you highlight a skill and press Space.

---

## Description Budget and Truncation

- All skill descriptions are loaded into Claude's context so Claude knows what's available.
- Budget scales at **1% of the model's context window** (configurable via `skillListingBudgetFraction`).
- When budget overflows, descriptions for least-used skills are dropped first.
- Each skill's `description` + `when_to_use` combined is capped at **1,536 characters** (configurable via `maxSkillDescriptionChars`).
- **Mitigation for low-priority skills:** Set `"name-only"` in `skillOverrides` to list without description.
- Run `/doctor` to see if the budget is overflowing and which skills are affected.

---

## Built-in Bundled Skills

Claude Code ships with bundled skills available in every session:

| Skill | Purpose |
|-------|---------|
| `/simplify` | Review changed code for quality and reuse |
| `/batch` | Execute multiple operations in parallel |
| `/debug` | Diagnose and fix bugs |
| `/loop` | Run a prompt on a recurring interval |
| `/claude-api` | Build/debug Claude API apps |
| `/init` | Initialize CLAUDE.md |
| `/review` | Review a pull request |
| `/security-review` | Security review of pending changes |

Bundled skills are prompt-based (not fixed logic). They appear alongside built-in commands, marked "Skill" in the commands reference.

---

## arifOS VPS — Current Skill Inventory

### Personal Skills (`~/.claude/skills/`)

| File | Format | Purpose |
|------|--------|---------|
| `constitutional-reasoning.md` | Runbook (legacy flat file) | F1–F13 floor evaluation framework |
| `docker-thermodynamics.md` | Runbook | Docker health + resource ops |
| `github-ops.md` | Runbook | Git/GitHub federation workflow |
| `mcp-ops.md` | Runbook | MCP server lifecycle ops |
| `secret-hygiene.md` | Runbook | Secret management reasoning |
| `vault-integrity.md` | Runbook | VAULT999 attestation chain |
| `vps-docker-ops.md` | Runbook | VPS-level Docker operations |
| `vps-health-ops.md` | Runbook | VPS health sweep + diagnostics |
| `aaa-governance/` | Directory | AAA control plane governance |

**Format note:** These use the legacy flat-file format (no directory, no proper frontmatter). They work but lack `description:`, `when_to_use:`, `allowed-tools:`, and `disable-model-invocation:` fields. Claude loads them only when explicitly invoked, not automatically. Migration to proper SKILL.md directory format is a valid upgrade — see [[skill-forge-claude-skill]].

---

## Comparison to Other Platform Formats

| Dimension | Claude Code Skills | OpenClaw | OpenAI Tool |
|-----------|-------------------|---------|-------------|
| **Format** | `SKILL.md` + YAML frontmatter | Embedded in `SYSTEM_MD.md` | `tool.json` (JSON schema) |
| **Discovery** | Auto (description matching) + `/name` | Monolithic agent prompt | Function-calling mechanism |
| **Isolation** | Optional (`context: fork`) | No (inline) | No |
| **Dynamic context** | Shell injection syntax | No | No |
| **Per-tool permissions** | `allowed-tools:` | System-prompt gates | API-level |
| **Versioning** | Custom frontmatter field | None standard | None standard |
| **Canonicalization** | AAA wiki → SKILL.md adapter | AAA wiki → SYSTEM_MD.md section | AAA wiki → tool.json |

The AAA wiki canonical skill page is the **source of truth**. Platform adapters are derived from it. See [[skill-adapter-sync]] for the propagation procedure.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Skill not triggering | Description doesn't match user phrasing | Add trigger phrases to `description` or `when_to_use`; run `/doctor` |
| Skill triggers too often | Description too broad | Add `disable-model-invocation: true` for manual-only |
| Description cut short | Budget overflow | Set `"name-only"` for low-priority skills; increase `skillListingBudgetFraction` |
| Skill stops working after compaction | Dropped from budget | Re-invoke with `/skill-name` |
| Project skill not loading | Trust dialog not accepted | Accept workspace trust in Claude Code |
| New skills directory not discovered | Session started before directory existed | Restart Claude Code |

---

## Related Pages

- [[skill-forge-claude-skill]] — procedure for creating/upgrading Claude Code skills on this VPS
- [[skill-adapter-sync]] — propagating canonical skills to platform adapters
- [[agent-skills-architecture]] — cross-platform skills landscape
- [[concept-tools-and-embodiment]] — tools vs skills distinction
- [[skill-spatial-grounding]] — first canonical skill with full procedure

*DITEMPA BUKAN DIBERI — Evidence forged 2026-05-17 from official Anthropic documentation.*
