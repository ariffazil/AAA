---
title: "SKILL: Forge Claude Code Skill — Create or Upgrade a Personal Skill"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
tags: [claude-code, skills, SKILL.md, forge, create, upgrade, personal-skills]
category: infra
risk_band: LOW
floors: [F1, F2, F8]
evidence_required: false
sources:
  - wiki/concepts/CLAUDE_CODE.md
  - https://code.claude.com/docs/en/skills
confidence: high
status: canonical
---

# SKILL: Forge Claude Code Skill

> **Skill ID:** `skill-forge-claude-skill`
> **Canonical location:** `AAA/wiki/skills/skill-forge-claude-SKILL_MD.md`
> **When to use:** When creating a new Claude Code skill, upgrading a legacy runbook to proper SKILL.md format, or auditing an existing skill's quality
> **Severity:** LOW — creating a skill file is non-destructive and reversible

---

## Summary

Forge a new personal Claude Code skill at `~/.claude/skills/<skill-name>/SKILL.md`, or upgrade an existing flat-file runbook to the proper directory-based SKILL.md format. Skills created here are available across all projects on this VPS.

Full reference: [[claude-code-skills-architecture]]

---

## Trigger Conditions

- A recurring procedure is being pasted into chat sessions (move it to a skill)
- A CLAUDE.md section has grown into a multi-step procedure (extract it)
- A legacy `~/.claude/skills/*.md` flat file needs upgrade to proper SKILL.md format
- A new domain is being added to the arifOS federation (forge its skill)
- `constitutional-reasoning.md`, `vps-health-ops.md`, or any flat runbook needs to be discoverable by Claude automatically

---

## Pre-Skill Decisions (Answer Before Writing)

1. **Name:** What is the `/command-name`? (lowercase, hyphens, max 64 chars)
2. **Type:** Reference (Claude loads automatically) or Task (user invokes manually)?
3. **Isolation:** Does it need `context: fork`? (destructive ops, long research, clean output)
4. **Tools:** Does it need pre-approved tools (`allowed-tools:`)?
5. **Dynamic context:** Does it need live data injected at runtime (git diff, docker status, etc.)?

---

## Procedure: Create a New Skill

### Step 1 — Create the skill directory
```bash
mkdir -p ~/.claude/skills/<skill-name>
```

### Step 2 — Write SKILL.md

Minimal template for a **reference skill** (Claude loads automatically):
```yaml
---
description: <what it does and when Claude should use it — put key trigger phrase first>
---

## <Context or Knowledge Title>

<Instructions or knowledge. Keep under 500 lines.>
```

Template for a **task skill** (user-invoked only):
```yaml
---
description: <what it does — used in /skills menu>
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(docker *)
---

<Task instructions. Steps, not prose.>

$ARGUMENTS
```

Template for a **forked subagent skill** (isolated execution):
```yaml
---
description: <what it does>
context: fork
agent: general-purpose
disable-model-invocation: true
---

<Task instructions that become the subagent's prompt.>

$ARGUMENTS
```

### Step 3 — Add supporting files (optional)

If the skill needs large reference docs, example outputs, or scripts:
```bash
mkdir -p ~/.claude/skills/<skill-name>/scripts
# Add: reference.md, EXAMPLES_MD.md, scripts/helper.sh
```

Reference them from SKILL.md:
```markdown
## Additional resources
- For full reference, see [reference.md](reference.md)
```

### Step 4 — Verify live detection

Skills take effect immediately in the current Claude Code session (no restart needed for existing directories). Test:
```
/skill-name
```
Or ask Claude something that matches the description to verify auto-invocation.

### Step 5 — Run /doctor

```
/doctor
```

Check that the skill appears and its description is not truncated in the budget.

---

## Procedure: Upgrade a Legacy Flat-File Runbook

Legacy skills in `~/.claude/skills/` are flat `.md` files (e.g. `vps-health-ops.md`). They lack frontmatter and are not auto-discoverable. To upgrade:

### Step 1 — Create the directory structure
```bash
mkdir -p ~/.claude/skills/vps-health-ops
```

### Step 2 — Move the content

Read the existing flat file and write a proper SKILL.md:
```bash
# The old file: ~/.claude/skills/vps-health-ops.md
# The new file: ~/.claude/skills/vps-health-ops/SKILL.md
```

Add frontmatter:
```yaml
---
description: VPS and Docker health sweep — disk, memory, CPU, container status, port checks. Use when checking system health, debugging resource issues, or performing a pre-work VPS diagnostic.
when_to_use: "health check, system status, VPS status, docker status, disk full, high memory, port down, service not responding"
allowed-tools: Bash(df *) Bash(free *) Bash(uptime) Bash(docker ps *) Bash(docker stats *) Bash(curl *)
---
```

### Step 3 — Optionally remove the old flat file
```bash
# Only after verifying the new SKILL.md works
rm ~/.claude/skills/vps-health-ops.md
```

---

## arifOS Priority Upgrade Queue

These legacy flat-file skills are the highest-value candidates for upgrade to proper SKILL.md format:

| File | Why upgrade matters |
|------|-------------------|
| `vps-health-ops.md` | Health checks should auto-trigger when Arif mentions system issues |
| `constitutional-reasoning.md` | F-floor evaluation should always be available to Claude without explicit invocation |
| `docker-thermodynamics.md` | Docker ops are frequent; auto-discovery saves token budget in CLAUDE.md |
| `secret-hygiene.md` | Should auto-load when any secret-related term is mentioned |

---

## Quality Standards for arifOS Skills

A skill is production-quality when:

- [ ] `description:` — 1–3 sentences, trigger phrase first, under 1,536 chars total
- [ ] `when_to_use:` — lists trigger phrases user would naturally say
- [ ] `disable-model-invocation:` — explicitly set for destructive or side-effect tasks
- [ ] `allowed-tools:` — scoped to exactly what the skill needs, no broader
- [ ] Body under 500 lines — large reference docs in separate files
- [ ] No F-floor violations baked in (no irreversible actions without HOLD gate)
- [ ] Tested: invoke directly with `/skill-name` and verify output
- [ ] Run `/doctor` — confirm budget not overflowed

---

## Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Skill never triggers automatically | Check `description:` relevance; run `/doctor` for budget overflow |
| Old flat-file coexists with new directory | Remove the old `.md` file after verifying new SKILL.md works |
| Skill triggers too broadly | Add `disable-model-invocation: true`; narrow description |
| Skill lost after compaction | Re-invoke with `/skill-name`; if critical, set `user-invocable: false` to keep it auto-loading |
| `context: fork` returns blank output | Skill body contains only guidelines, not actionable instructions — add explicit task steps |

---

## Related Pages

- [[claude-code-skills-architecture]] — full technical reference for the skills system
- [[skill-adapter-sync]] — propagating canonical skills to platform adapters
- [[skill-spatial-grounding]] — example of a well-structured canonical skill

*DITEMPA BUKAN DIBERI — Procedure forged 2026-05-17 from official evidence.*
