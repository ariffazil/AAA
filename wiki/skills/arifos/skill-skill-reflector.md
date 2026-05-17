---
title: "SKILL: Skill Reflector"
type: skill
version: 1.0.0
category: meta
risk_band: LOW
floors: []
evidence_required: false
sources: [/root/.opencode/skills/skill-reflector/SKILL.md]
confidence: high
---

# SKILL: Skill Reflector

> **DITEMPA BUKAN DIBERI — Skills audit skills.**
> **Source:** `/root/.opencode/skills/skill-reflector/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Auditing skills across federation
- Improving skill quality and content
- Skill performance measurement
- Constitutional awareness review
- Trigger: skill audit, improve skills, skill quality

---

## Federated Skill Registry

All skills centralized at:
```bash
/root/.opencode/skills/           # Master skill directory (30 skills)
/root/.opencode/skills/*/SKILL.md  # Each skill's canonical definition
```

---

## Skill Classification

### Governed Skills (require arifOS MCP review)
Pattern: `^(arifos|geox|wealth|well|aforge|aaa)-`
- arifos-operator, geox-analyst, wealth-analyst, well-*, aforge-*, aaa-*
- **NEVER auto-write without human approval**

### Infra Skills (require 888_HOLD for destructive)
- vps-docker, caddy-cloudflare, fastmcp-deploy, vps-audit
- Show diff before writing; destructive = explicit human ack

### Domain Skills (reasoning only, safe to propose)
- geox-analyst, wealth-analyst
- Can propose improvements without 888_HOLD

---

## Audit Criteria (Score 1-5 Each)

| Dimension | What to Check |
|-----------|---------------|
| **A. Description Quality** | Trigger keywords present? 1-1024 chars? Would agent confidently choose this skill? |
| **B. Content Completeness** | Commands current? Error tables complete? Destructive ops flagged? Missing scenarios? |
| **C. Output Format Consistency** | Clear output format defined? Severity levels standardized? |
| **D. Constitutional Awareness** | Floor references where appropriate? arifOS MCP suggested for governed actions? |

---

## arifOS-Governed Skill Policy

For skills matching `^(arifos|geox|wealth|well|aforge|aaa)-`:

```
1. Before proposing changes, call arifOS MCP:
   - path: /tools
   - method: GET
   - check if arif_audit_skill or equivalent exists

2. If arifOS indicates floor > F2 in play → mark as 888_HOLD

3. NEVER auto-write governed SKILL.md files
```

---

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

---

## Related Pages

- [[skill-skill-creator]] — creating new skills
- [[concept-tools-and-embodiment]] — skills as capabilities
- [[intelligence-tree]] — skills as tree layer
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Skills reflected. Quality audited.*
