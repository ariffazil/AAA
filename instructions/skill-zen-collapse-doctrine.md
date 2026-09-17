# Skill Zen — Collapse Doctrine (many names → one owner + few modes)

> **Status:** DRAFT_AWAITING_F13 (2026-09-16, sovereign directive: "your 412 skills should
> become ~60–100 real owners; the rest become aliases, modes, examples, references").
> **Mesh fact (measured 2026-09-16):** 522 canonical skills in `/root/.agents/skills`
> (mirror views: `.claude`, `.opencode` → 1597 SKILL.md files; 477 names multi-root).
> **Mechanics SOT:** `AAA/skills/OWNERSHIP_MAP.yaml` · Precedent: `.archive/2026-09-16-media-skill-dedup/`.

## The Zen move

```
many names  →  one owner skill  +  few modes
```

Collapse **by responsibility, not by folder.** Never delete: **freeze to `/root/AAA/skills/.frozen/<date>-<reason>/`
and leave an alias stub** (F1-reversible; loaders get a redirect, history survives).

> ⚠️ **INCIDENT LESSON (2026-09-16):** do NOT freeze inside `/root/.agents|.opencode|.claude/skills/.archive/` —
> the mesh sync prunes removals across ALL views and can destroy the frozen copy
> (sovereign-recognize vanished from the synced `.archive` within minutes; recovered from the
> AAA-tree copy). **`.frozen` lives only in the AAA tree, outside the mirror roots.**

## The one-box rule

> Same owner + same inputs + same authority + same kill conditions ⇒ **one skill.**

Keep separate only when one of these differs **materially**:
authority boundary · input modality · safety/consent boundary · side effects ·
output contract · failure semantics · runtime dependency.

If only the prompt wording differs → collapse. If only the domain label differs → collapse.
If only the tone/persona differs → definitely collapse. If the authority boundary differs → keep.

## The anti-bloat law

> Before creating or preserving any skill, **find the existing owner.** If an owner exists,
> patch the owner. New skill only when authority, side effects, or runtime contract are
> genuinely different.

This is the single law that prevents the RASA/human-paradox layer from becoming another
20-skill ontology explosion.

## The three chains

| Domain | Collapse to |
|---|---|
| Human alignment | **RASA Doctrine → Perspective/Privacy → Reflect/Audit → Human Clarification** (4 owners) |
| Verification | **VERIFY → WITNESS → SEAL** (3 owners; everything else routes through) |
| MCP tooling | **MCP Build + MCP Verify + MCP Operate** (3 owners) |
| Research | **search → evidence → synthesis** (3 owners) |

## The human-alignment quartet (P1 — done 2026-09-16)

| # | Owner | Path | Owns | Absorbed |
|---|---|---|---|---|
| 1 | hermes-rasa-doctrine | apex/governance-core/ | human-state epistemology: O/S/R/I/F/P/C, forbidden promotions, qualia boundary, UNCREATED, CHANNEL_EXHAUSTED | (canon SOT) |
| 2 | audience-scoped-disclosure | human-interface/ | information flow: who may know/use/disclose; principal recognition; channel scope; privacy fiduciary | sovereign-recognize (frozen) |
| 3 | APEX-humility-godel | apex/recursive-audit/ | self-correction: falsification, ≥3 alternatives, agent-shadow, narrative gravity, overclaim, Ḧ≠H | AGI-decisions-reflect (frozen) |
| 4 | disclosure-advisory | counseling/ | return to humans: how to ask, when NOT to ask, consent, non-manipulative clarification | (mode patch queued P1.5) |

## Alias stub format

```markdown
---
name: <old-name>
description: "ALIAS → <owner>. <one-line capability>. Collapsed <date> per Skill Zen."
---
# ALIAS — COLLAPSED INTO OWNER n
**Owner:** <path> — load that skill. Survives as Mode: <NAME>.
Original (frozen): .agents/skills/.archive/<date>-<reason>/<name>/
```

## Kill condition (this doctrine)

If after 90 days the alias-stub pattern has zero redirect hits and zero collapses beyond P1,
this doctrine is decoration — demote to note. Tracked in OWNERSHIP_MAP.yaml `phase_log`.
