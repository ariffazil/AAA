---
name: skill-reflector
description: Audit, reflect on, and improve OpenCode skills across the arifOS federation. Analyses skill effectiveness, identifies gaps, updates SKILL.md content with constitutional awareness. Governed skills (arifos-*, geox-*, wealth-*, well-*, aforge-*, aaa-*) require arifOS MCP review before changes. Use when asked to improve skills, audit skill quality, update skill content, or reflect on skill performance.
version: 1.0.0
author: arif
tags: opencode, skills, self-improvement, audit, reflection, arifos
---

# Skill Reflector — Self-Improvement Engine (arifOS-Federated)

## Purpose
Audit skills across ALL repos in the federation and produce improved versions with constitutional awareness.

## Federated Skill Registry
Scan these locations:
```bash
AAA/.opencode/skills/
A-FORGE/.opencode/skills/
GEOX/.opencode/skills/
WEALTH/.opencode/skills/
~/.config/opencode/skills/
```

## Skill Classification

### Governed Skills (require arifOS MCP review)
Pattern: `^(arifos|geox|wealth|well|aforge|aaa)-`
- arifos-operator, geox-analyst, wealth-analyst, well-*, aforge-*, aaa-*
- NEVER auto-write without human approval

### Infra Skills (require 888 HOLD for destructive)
- vps-docker, caddy-cloudflare, fastmcp-deploy, vps-audit
- Show diff before writing; destructive = explicit human ack

### Domain Skills (reasoning only, safe to propose)
- geox-analyst, wealth-analyst
- Can propose improvements without 888 HOLD

## Audit Criteria (score 1-5 each)

### A. Description Quality
- Trigger keywords present? 1-1024 chars?
- Would agent confidently choose this skill?

### B. Content Completeness
- Commands current and not deprecated?
- Error tables complete?
- Destructive ops flagged with 888 HOLD?
- Missing common scenarios?

### C. Output Format Consistency
- Clear output format defined?
- Severity levels standardised?

### D. Constitutional Awareness
- Floor references where appropriate?
- arifOS MCP call suggested for governed actions?

## arifOS-Governed Skill Policy
For skills matching `^(arifos|geox|wealth|well|aforge|aaa)-`:
1. Before proposing changes, call `arifos-mcp` tool:
   - path: `/tools`
   - method: `GET`
   - check if `arif_audit_skill` or equivalent exists
2. If arifOS indicates any floor > F2 in play, mark as **888 HOLD**
3. Never auto-write governed SKILL.md files

## Output Format
```
## Skill Audit Report — [timestamp]

### [skill-name] [GOVERNED/INFRA/DOMAIN]
- Description Score: X/5
- Content Score: X/5
- Format Score: X/5
- Constitutional Score: X/5
- Total: X/20
- Issues Found: ...
- Recommended Changes: ...

### Federation Health: X% (skills needing work / total)
```

## Self-Audit Trigger Examples
```
> Audit all skills in the federation
> The Caddy cert renewal failed — update caddy-cloudflare skill
> Apply improvements to geox-analyst — show diff first
> Check all governed skills for F09 ANTIHANTU compliance
```

## Phase 5 — Version Tracking
Append to `AAA/.opencode/skills/skill-reflector/audit-log.md`:
```markdown
## Audit [date]
- Skills audited: N
- Governed skills: N
- Skills improved: N
- Key constitutional changes: ...
```

---

*Last updated: 2026-05-02*