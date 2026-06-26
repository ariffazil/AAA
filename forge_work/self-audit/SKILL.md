---
name: self-audit
description: Generate a constitutional audit document for OPENCLAW, a workspace, or a federation organ. Maps current state vs target state, identifies gaps, and produces a forgeable improvement plan.
version: 0.1.0
created: 2026-06-06
author: OPENCLAW
doctrine: DITEMPA BUKAN DIBERI
---

# Self-Audit Skill

> **Mission:** Produce a structured, citable, constitutionally-aware audit document.
> **Output:** Markdown file in `forge_work/`, with: executive verdict, deep-research section, current state, gap table, improvement plan, floor compliance check, sealing.

## When to Use

- User asks to "audit," "review," or "show me the state of"
- A new organ is added to the federation
- A version drift is detected (build ≠ live, version behind)
- Weekly/monthly self-audit cron fires
- After a major change (skill add, config patch, container rebuild)

## The Audit Skeleton

```markdown
# <SUBJECT> Audit — <DATE>

> Date: ISO timestamp
> Sealed by: OPENCLAW (or whoever)
> Sovereign directive: <quote if any>

## 0. Executive Verdict
   | Axis | State | Note |
   |------|-------|------|
   | one row per axis | 🟢/🟡/🔴 | one line |

## 1. What <SUBJECT> Is (Plain)
   2-3 paragraphs, no jargon

## 2. Deep Research (Upstream)
   Latest version, what's new, what's drift

## 3. Current State
   3.1 Version, 3.2 Model, 3.3 Skills, 3.4 Memory,
   3.5 Channels, 3.6 Crons, 3.7 Constitutional posture

## 4. Real Gaps
   Table of question → answer

## 5. Recursive Improvement Plan
   5.1 Immediate, 5.2 Next 24h, 5.3 Next 7d, 5.4 30d

## 6. Constitutional Audit (Self-Applied)
   Table: Floor | Triggered? | Note
   For F1-F13

## 7. Sealing
   Path, timestamp, hash, verdict, reviewer, sovereign waiver
```

## Required Sources

Every audit MUST cite at least:
- Live health endpoint (curl + status code)
- Latest version from official source (web_fetch with URL)
- Workspace state (ls, cat)
- Constitutional floors (FLOORS.md or 000_CONSTITUTION.md)

## Falsifiability Rules

**A self-audit is INVALID if any of these are missing:**
- No live verification of state (only "I think it's...")
- No source URL for "latest version"
- No execution path mentioned (file path, command, or output)
- No floor compliance table
- No seal/verdict

## Anti-Patterns

- ❌ Auditing without touching the system
- ❌ Repeating last audit's structure without re-verifying
- ❌ Skipping the floor table because "obviously passes"
- ❌ "I think the version is..." instead of `cat package.json | head -1`
- ❌ Auditing the audit (meta-loop without progress)

## Cron Hooks

- **Weekly:** Sunday 03:00 KL (after morning briefing, before Asia open)
- **Monthly:** 1st of month, full deep-research pass
- **On-demand:** via `agentic-loop` skill

## Output Path

`/root/.openclaw/workspace/forge_work/<SUBJECT>-AUDIT-<DATE>.md`

## Seal Format

```
TASK: <audit subject>
STATUS: SEAL | SEAL-with-CAVEATS | HOLD | VOID
EVIDENCE: <path to audit doc>
FLOORS: F01 F02 F04 F07 (those triggered)
NEXT: <next action>
```

---

*Forged 2026-06-06 under sovereign directive. DITEMPA BUKAN DIBERI.*
