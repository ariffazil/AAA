---
name: kimi-skill-reflector
description: Audit, reflect on, and recursively upgrade Kimi Code skills across the arifOS federation. Bounded autonomous ritual — proposes improvements, never auto-writes governed skills without 888_HOLD, caps iterations, enforces ΔS ≤ 0.
version: 1.1.0
zen_added: 2026-07-16
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil
license: Proprietary
---

# Kimi Skill Reflector — Bounded Autonomous Skill Updater

## Purpose

At the start of every agentic session, audit the Kimi Code skill surface and propose improvements with constitutional awareness. This is a **bounded recursive ritual**, not an unbounded self-modifying loop.

## Scope

Kimi Code user-scope skills live at:
```bash
/root/.arifos/agents/kimi/skills/
/root/.arifos/agents/kimi/skills/*/SKILL.md
/root/.arifos/agents/kimi/skills/SKILL_INDEX.md
```

Project-scope skill mirrors live at:
```bash
/root/.agents/skills/
```

Edit **user-scope** skills for Kimi-specific behavior. Edit **project-scope** skills only when the behavior change is generic across all AAA agents.

## Ritual — Run at Session Start

```text
1. LOAD  → Read SKILL_INDEX.md and list user-scope skills
2. SCAN  → Check each SKILL.md for drift, rot, and constitutional gaps
3. SCORE → Rate description / content / format / constitutional awareness
4. PROPOSE → Draft improvements (file patches or new skills)
5. GATE  → Governed skills → 888_HOLD; infra skills → diff + ack; domain skills → propose
6. APPLY  → Write only after human or arifOS SEAL
7. LOG   → Append to audit-log.md
8. STOP  → If ΔS ≤ 0 and max iterations reached
```

## Skill Classification

### Governed Skills (require arifOS MCP review / 888_HOLD)
Pattern: `^(arifos|geox|wealth|well|aforge|aaa|kimi-.*-(arifos|geox|wealth|well|aforge|aaa))-`
- NEVER auto-write without human approval.
- Load `CONSTITUTIONAL_REFLEX` (canonical alias for the `arifos-act` reflex) and route through `arifos-mcp` `/tools` if an audit tool exists.
- If any floor > F2 in play → mark 888_HOLD.

### Infra Skills (require diff + explicit ack for destructive changes)
- Examples: `kimi-vps-*`, `kimi-docker-*`, `kimi-caddy-*`, `kimi-fastmcp-deploy`
- Show diff before writing.
- Destructive = explicit human ack.

### Domain / Reasoning Skills (safe to propose)
- Examples: contrast skills, planning skills, audit skills.
- Can propose improvements without 888_HOLD.
- Still require entropy check (ΔS ≤ 0).

## Bounded Autonomy Rules

| Guard | Value | Why |
|---|---|---|
| Max iterations per session | 3 | Prevents runaway recursion |
| Max skills modified per session | 3 | Keeps diff reviewable |
| Entropy requirement | ΔS ≤ 0 | No cosmetic churn |
| Governed skill writes | 888_HOLD only | F13 authority |
| Infra destructive writes | explicit ack | F1 AMANAH |
| Audit log | append-only | F11 AUDIT |
| Rollback | git revert path | F1 AMANAH |

## Audit Criteria (score 1-5 each)

### A. Description Quality
- Trigger keywords present? 1-1024 chars?
- Would an agent confidently choose this skill?

### B. Content Completeness
- Commands current and not deprecated?
- Error tables complete?
- Destructive ops flagged with 888_HOLD?
- Missing common scenarios?

### C. Output Format Consistency
- Clear output format defined?
- Severity levels standardised?
- Kimi-specific tool references correct?

### D. Constitutional Awareness
- Floor references where appropriate?
- arifOS MCP call suggested for governed actions?
- Identity threading mentioned?
- `CONSTITUTIONAL_REFLEX` / `arifos-act` reflex invoked for mutating actions?

## Recursive Self-Improvement Loop

If the reflector detects that its own skill (`kimi-skill-reflector/SKILL.md`) needs improvement:

1. Score itself using the audit criteria.
2. Propose a patch.
3. Route to 888_HOLD if the patch changes governance rules.
4. If the patch is cosmetic/Clarity-only and ΔS ≤ 0, it may apply after logging.
5. Always log the self-edit in `audit-log.md`.

## Output Format

```markdown
## Skill Audit Report — [timestamp]

### [skill-name] [GOVERNED/INFRA/DOMAIN]
- Description Score: X/5
- Content Score: X/5
- Format Score: X/5
- Constitutional Score: X/5
- Total: X/20
- Issues Found: ...
- Recommended Changes: ...
- Authority Required: 888_HOLD / diff+ack / propose-only

### Federation Health: X% (skills needing work / total)
### Session Actions Taken: ...
### Ω₀ / Open Questions: ...
```

## Audit Log

Append every audit to:
```bash
/root/.arifos/agents/kimi/skills/kimi-skill-reflector/audit-log.md
```

Entry format:
```markdown
## Audit [date] — session [session_id]
- Skills audited: N
- Governed skills: N
- Infra skills: N
- Domain skills: N
- Skills improved: N
- 888_HOLD raised: N
- Key constitutional changes: ...
- Entropy delta (ΔS): ...
```

## Handover Contract

At session end, if skills were modified, produce a handover note:
```markdown
# Skill Handover — [session_id]

## Skills touched
- skill-name: change summary, authority level

## Pending 888_HOLD
- skill-name: reason

## How to verify
- Read SKILL_INDEX.md
- Run skill audit ritual
- Check audit-log.md

## Next session trigger
- If skill drift detected → run kimi-skill-reflector
```

## STOP Conditions

Cease the ritual when:
1. Task is complete.
2. Authority exhausted (888_HOLD needed).
3. Evidence insufficient (cannot score a skill).
4. Blast radius exceeded (governance rule change).
5. Cost exceeds value (cosmetic-only changes with ΔS > 0).
6. Tools are shaping the mission (re-attune with Arif).

---


## Federation anchors (v1.1.0 — added 2026-07-16)

- **Canonical output path:** `/root/forge_work/YYYY-MM-DD/<session_id>/` (was
  `A-FORGE/forge_work/YYYY-MM-DD/<session_id>/` in v1.0.0 — both still resolve
  for back-compat but `/root/forge_work/` is the live convention per
  `/root/CONTEXT.md`).
- **Audit anchor:** `/root/.arifos/agents/kimi/skills/kimi-skill-reflector/audit-log.md`
  (kimi-skill-reflector ritual, append-only).
- **Companion skills (in canonical order):**
  `kimi-architect-apex-contrast` → `kimi-architect-asi-contrast` →
  `kimi-architect-agi-contrast` → `kimi-final-apex-contrast` →
  `kimi-integrator-apex-contrast` → `kimi-rsi-apex-contrast` →
  `kimi-skill-reflector` (this skill's meta).
- **Session entry:** `KIMI_RSI_INIT_PROMPT.md` v1.1.0 (cold-boot diagnostic
  recipe added) → routes task-class → contrast skill.
- **Session exit:** `KIMI_HANDOVER_PROMPT.md` v1.1.0 (post-deploy verification
  recipe added).
- **Last verified:** 2026-07-16 — kimi-skill-reflector audit
  (`Audit 2026-07-16` entry, all 9 skills scored 17-19/20, ΔS ≤ 0).

---
**DITEMPA BUKAN DIBERI** — improve skills, but never outrun the constitution.
