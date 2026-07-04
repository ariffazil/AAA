---
title: "SKILL: Skill Promote — Convert Repeated Patterns into Canonical Proposals"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
tags: [promote, skill, pattern, TREE777, 888, governance, ladder]
category: governance
risk_band: MEDIUM
floors: [F1, F2, F4, F7]
evidence_required: true
sources: [wiki/concepts/MD.md, wiki/SCHEMA.md]
confidence: high
status: canonical
---

# SKILL: Skill Promote

> **Skill ID:** `skill-skill-promote`
> **Canonical location:** `AAA/wiki/skills/SKILL_SKILL_3.md`
> **Status:** CANONICAL — this is a meta-skill, not a draft
> **When to use:** When the same pattern is seen 2-3× across evidence bundles or scar drafts, and there is no existing canonical skill covering it
> **Severity:** MEDIUM — creates promotion proposals, requires 888 deliberation for canonical status

---

## Summary

When a technique, approach, or failure-countermeasure appears as a pattern in 2-3+ evidence bundles or scar drafts, distill it into a **skill promotion proposal** and submit it for 888 deliberation.

This is the **middle step** of the promotion ladder:
- [[skill-trace-capture]] → captures evidence (always)
- [[skill-scar-distill]] → converts failures to scar drafts (on failure)
- **skill-skill-promote (this skill)** → converts repeated patterns to skill proposals (on repetition)
- → 888 JUDGE → canonical skill or entity page

---

## Trigger Conditions

**Run when ALL of these are true:**
1. The same or very similar pattern appears in 2+ evidence bundles (from [[skill-trace-capture]])
2. There is no existing canonical skill covering this pattern
3. The pattern is a **technique** (how to do something), not just a fact
4. The pattern is **generalizable** (applicable beyond the specific task that generated it)

**OR when:**
- 2+ scar drafts share the same root cause and countermeasure
- A proposed skill (status: proposed) in `wiki/skills/` has accumulated 2+ supporting evidence bundles

**Do NOT promote:**
- One-off facts (file content) — these belong in raw notes, not skills
- Things already covered by an existing canonical skill
- Agent-specific configurations (these belong in entity pages, not skills)
- Pure opinions or preferences

---

## Precondition

- 2+ evidence bundles or scar drafts exist showing the same pattern
- Evidence bundles stored in `wiki/raw/notes/`
- You have verified the pattern actually recurs (not just similar superficially)

---

## Procedure

### Step 1: Verify the Pattern Recurs

Before promoting, confirm the pattern appears in multiple evidence bundles:

```bash
# Search for the pattern across evidence bundles
grep -l "{pattern keyword}" wiki/raw/notes/*.md

# Count occurrences
grep -c "{pattern keyword}" wiki/raw/notes/*.md
```

If 2+ files match with concrete examples, proceed.

### Step 2: Write the Skill Promotion Proposal

Create `wiki/skills/skill-{name}.md` with `status: proposed`:

```markdown
---
title: "SKILL: {Skill Name}"
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
version: 0.1.0
type: skill
tags: [{relevant tags}]
category: {governance | domain | tool}
risk_band: LOW | MEDIUM | HIGH
floors: [{relevant F floors}]
evidence_required: true
sources: [{evidence-bundle-paths}]
confidence: medium | high
status: proposed
---

# SKILL: {Skill Name}

> **Skill ID:** `skill-{name}`
> **Status:** PROPOSED — pending 888 deliberation
> **Promotion trigger:** Pattern observed in {N} evidence bundles
> **Evidence:** {list evidence bundle paths}

---

## What This Skill Does

[2-3 sentences: When should an agent use this skill? What does it help accomplish?]

## Why This Pattern Should Be a Skill

**Evidence of repetition:**
- Evidence bundle 1: {path} — {1-2 sentence description of what happened}
- Evidence bundle 2: {path} — {1-2 sentence description}
- Evidence bundle 3 (optional): {path} — {1-2 sentence description}

**What all cases had in common:** [the shared structural element]

**What was different:** [the task-specific context that differs]

## Procedure

### Step 1: [Name of Step]

[Description]

### Step 2: [Name of Step]

[Description]

## Failure Modes

| Failure | Mitigation |
|---------|-----------|

## Related Pages

- [[TREE777]] — governance framework
- [[skill-trace-capture]] — upstream evidence source
- [[skill-scar-distill]] — scar source (if promoted from failure)
- [[skill-skill-promote]] — this skill

---

*Proposed {YYYY-MM-DD}. Promotion requires 888 deliberation.*
```

### Step 3: Assess Risk Band and Floors

| Risk Band | When |
|-----------|------|
| **HIGH** | Skill touches security, auth, deletion, or irreversible operations |
| **MEDIUM** | Skill changes how agents behave in non-trivial ways |
| **LOW** | Skill is advisory or informational |

| Relevant Floors | When to cite |
|----------------|--------------|
| F1 (AMANAH) | Skill involves deletion, irreversible action, or data modification |
| F2 (TRUTH) | Skill involves verifying claims or checking evidence |
| F3 (WITNESS) | Skill involves cross-checking outputs against sources |
| F4 (CLARITY) | Skill is about clear communication or documentation |
| F7 (HUMILITY) | Skill involves acknowledging uncertainty |
| F9 (ANTIHANTU) | Skill involves claims about the agent's own state |
| F11 (AUTH) | Skill involves identity verification |

### Step 4: Submit for 888 Deliberation

After creating the proposed skill, append to `wiki/LOG_MD.md`:

```markdown
## [YYYY-MM-DD] PROMOTION PROPOSAL | skill-skill-promote | {agent}
- Proposed skill: wiki/skills/skill-{name}.md
- Status: proposed
- Evidence count: {N} bundles
- Risk band: {LOW | MEDIUM | HIGH}
- Floors cited: [{F1, F2, ...}]
- Deliberation requested: 888_JUDGE
- Proposed by: {agent name}
```

### Step 5: If 888 Returns SEAL

If 888 returns **SEAL**, update the frontmatter:
- `status: proposed` → `status: canonical`
- `version: 0.1.0` → `version: 1.0.0`
- Add `approved: {date}` and `approved_by: 888_JUDGE`

If 888 returns **SABAR**, address the conditions and resubmit.
If 888 returns **HOLD** or **VOID**, archive the proposed skill with explanation.

---

## Preconditions

- 2+ evidence bundles in `wiki/raw/notes/` showing the same pattern
- Verified the pattern is not already covered by a canonical skill
- Write access to `wiki/skills/`
- The pattern is a technique or procedure, not a fact

---

## Expected Outputs

- `wiki/skills/skill-{name}.md` created with `status: proposed`
- `wiki/LOG_MD.md` entry recording the promotion proposal
- Evidence paths cited from `wiki/raw/notes/`

---

## Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Promoting something already covered | Check `INDEX_MD.md` for existing canonical skills before proposing |
| Not enough evidence | Wait for a 3rd occurrence before promoting — better slow than wrong |
| Superficial similarity ≠ pattern | Verify the structural element is the same, not just the surface text |
| Promoting opinions | Stick to techniques (how to) not preferences (what's best) |

---

## Promotion Ladder Summary

```
[EVENT] → skill-trace-capture → wiki/raw/notes/{slug}.md
                                      ↓ (if failure)
                              skill-scar-distill → wiki/scars/scar-{name}.md (status: proposed)
                                      ↓ (if pattern repeats 2-3x)
                              skill-skill-promote → wiki/skills/skill-{name}.md (status: proposed)
                                      ↓ (if 888 returns SEAL)
                              CANONICAL SKILL (version: 1.0.0, status: canonical)
```

---

## Related Pages

- [[TREE777]] — governance framework and promotion ladder
- [[skill-trace-capture]] — upstream evidence capture
- [[skill-scar-distill]] — scar-to-pattern upstream
- [[SCHEMA.md]] — skill spec format requirements
- [[INDEX_MD.md]] — canonical skill catalog

---

*DITEMPA BUKAN DIBERI — Patterns forged in repetition become skills. Skills become law.*
