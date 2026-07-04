---
title: "SKILL: Adapter Sync — Wiki Canonical to Platform Adapters"
created: 2026-05-17
updated: 2026-05-17
version: 0.1.0
type: skill
tags: [adapter, sync, skills, platform, claude, openclaw, openai, mcp]
category: infra
risk_band: HIGH
floors: [F1, F8, F10]
evidence_required: true
sources: [wiki/concepts/AGENT_SKILLS.md]
confidence: low
status: stub
---

# SKILL: Adapter Sync

> **Skill ID:** `skill-adapter-sync`
> **Canonical location:** `AAA/wiki/skills/SKILL_ADAPTER.md`
> **Status:** STUB — requires full procedure development
> **When to use:** After updating a canonical wiki skill — must propagate to all platform adapters
> **Severity:** HIGH — drift between canonical and adapters causes inconsistent behavior

---

## Summary

When a canonical skill in `AAA/wiki/skills/` is updated, propagate the changes to all platform adapters in `AAA/skills/{skill-name}/{platform}/`. The canonical wiki page is the **source of truth**. Platform adapters are **derived**, not hand-maintained.

---

## TODO: Procedure (not yet written)

### Precondition Check
- [ ] Verify canonical skill has been updated (check `updated:` frontmatter date)
- [ ] Verify canonical skill passes schema validation (has required frontmatter)
- [ ] Run `wiki/LOG_MD.md` query to confirm this is a meaningful update vs. typo fix

### Identify Affected Adapters
- [ ] Read canonical skill's `Adapters` section
- [ ] List all platforms with existing adapters
- [ ] Identify missing adapters (marked 🚧 in index)

### Propagate Changes to Each Adapter

#### Claude Adapter (`AAA/skills/{name}/claude/SKILL.md`)
- [ ] Extract: name, version, description, trigger conditions, procedure steps
- [ ] Translate to Claude SKILL.md format
- [ ] Verify: links back to canonical wiki skill
- [ ] Verify: version matches canonical

#### OpenClaw Adapter (`AAA/skills/{name}/openclaw/SYSTEM_MD.md`)
- [ ] Extract: name, version, description, SPATIAL_LAW or equivalent text
- [ ] Translate to OpenClaw SYSTEM_MD.md override section format
- [ ] Verify: links back to canonical wiki skill
- [ ] Verify: version matches canonical

#### OpenAI Adapter (`AAA/skills/{name}/openai/`) — if applicable
- [ ] Extract: tool name, description, parameter schema
- [ ] Generate `tool.json` from canonical spec
- [ ] Verify: `name` field matches canonical `name`

#### MCP Adapter (`AAA/skills/{name}/mcp/`) — if applicable
- [ ] Extract: trigger conditions, risk_band, floors, verification
- [ ] Generate `manifest.json` from canonical spec
- [ ] Verify: links back to canonical wiki skill

### Log the Sync
- [ ] Append entry to `AAA/wiki/LOG_MD.md`:
  ```
  ## [YYYY-MM-DD] sync | adapter: {skill-name}
  - Canonical updated: {date}
  - Adapters synced: {list}
  - Verification: PASS
  ```
- [ ] Run VAULT999 outcome logging if skill is high-risk

---

## Preconditions

- Write access to `AAA/skills/{skill-name}/{platform}/` directories
- Canonical skill in `AAA/wiki/skills/` updated and schema-valid
- Platform adapter directories exist (may need to create from template)

---

## Expected Outputs

- All existing adapters updated to match canonical version
- New adapters created for missing platforms (if templates available)
- `AAA/wiki/LOG_MD.md` entry created
- VAULT999 outcome logged (if HIGH risk_band)

---

## Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Canonical not updated yet | Sync only after canonical is committed |
| Adapter directory missing | Create from template; do not block on missing platforms |
| Version mismatch after sync | Re-run sync; check for manual edits to adapter |
| Platform-specific limitation discovered | File issue in `AAA/wiki/queries/`; do not silently skip |

---

## The Derivation Principle

> **Wiki canonical is the source of truth. Platform adapters are generated from it, not hand-edited toward it.**

If an adapter requires a platform-specific change that cannot be expressed in the canonical:
1. File a query in `AAA/wiki/queries/`
2. Mark the platform adapter as `⚠ NOTE: platform-specific deviation` in the adapter file
3. Do not change the canonical to accommodate a single platform

---

## Related Pages

- [[agent-skills-architecture]] — the problem this skill solves (format fragmentation)
- [[skill-spatial-grounding]] — first skill with full adapter set
- [[concept-tools-and-embodiment]] — tools vs skills distinction

---

## Stub Author Notes

This skill is derived from the migration path in [[AGENT_SKILLS.md]], specifically the "Migration Path" section.

The key principle is: **canonical wiki → platform adapters** (not the other way around).

**Next step:** Write the step-by-step for one platform (Claude SKILL.md format) to establish the template, then generalize.

*DITEMPA BUKAN DIBERI — Canonical is truth. Adapters are derived.*
