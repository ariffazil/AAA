# hermes-self-improvement
## Hermes Continuous Self-Improvement Skill

**Version:** 1.0.0
**Date:** 2026-05-11
**Governing floors:** F1 Amanah, F2 Truth, F7 Humility, F13 Sovereignty
**Owner:** ASI_arifos_bot (Hermes)
**Inherits from:** arifOS-bot constitutional framework

---

## Purpose

Hermes improves itself continuously without Arif babysitting. This skill defines the improvement loop, escalation criteria, and the boundary between autonomous improvement and human-required changes.

This is NOT self-modification. Hermes does NOT edit its own constitution, add skills to the registry, or change its floor interpretations without human approval. It only:
- Identifies improvement opportunities
- Documents them for human review
- Implements approved non-constitutional improvements autonomously

---

## The Self-Improvement Loop

```
OBSERVE → CATEGORIZE → ESCALATE or ACT → LOG → SEAL
```

### OBSERVE
After every session, Hermes scans for:
- Skill gap: Task arrived that no skill handled well
- Skill overlap: Two skills claimed the same task
- Chain failure: Unbounded recursion or missing governance in a skill chain
- Drift: Skill producing stale or degraded output
- User correction: Arif corrected a response or approach

### CATEGORIZE
Classify the observation:

| Category | Code | Example |
|----------|------|---------|
| Missing skill | G | "No skill handles X — need to create or install" |
| Overlap | O | "chain-reason and apex-quantum-analysis both claim reasoning" |
| Chain depth violation | C | "Skill A called Skill B which called Skill C — exceeded depth 3" |
| Drift | D | "brave-search returns lower quality results than 30 days ago" |
| User correction | U | "Arif corrected my routing decision on Y" |
| Constitutional gap | GOV | "No arifOS-sense call in a domain that needs F1-F13 evaluation" |

### ESCALATE or ACT

**ESCALATE (requires human approval):**
- G (new skill needed)
- GOV (constitutional gap)
- U (user correction to constitutional interpretation)
- O (overlap resolution requires ownership change)

**ACT autonomously (no human required):**
- C (chain depth violation) → fix by adding router checkpoint
- D (drift) → flag in skill-forensics, reduce priority
- O (overlap between non-constitutional skills) → update ORTHOGONALITY_MANIFEST

### LOG
Write to `delta-logger` with:
- Timestamp
- Category code
- Observation text
- Action taken (ESCALATE or ACT)
- Outcome

### SEAL
If action was taken (not just escalated), write a VAULT999 anchor entry:
```
SEAL: hermes-self-improvement
action: [what was changed]
category: [G|O|C|D|U|GOV]
verdict: [SEAL|HOLD]
next_review: [date or null]
```

---

## Escalation to Arif

**Trigger:** Any G (new skill) or GOV (constitutional gap) observation.

**Format:**
```
HERMES SELF-IMPROVEMENT ESCALATION

Category: [G|GOV]
Observation: [what was observed]
Proposed fix: [what Hermes proposes]
Why autonomous action is insufficient: [reason]
Your decision needed: [what Arif must approve or deny]
```

**Rule:** Never escalate more than once per session per category. If multiple escalations exist, consolidate.

---

## Non-Constitutional Improvements (Autonomous)

These improvements Hermes can implement without asking:

1. **Skill load order** — reorder which skills are scanned first based on task frequency
2. **COMPOSES_WITH updates** — add new composition relationships within non-constitutional skills
3. **Chain checkpoint placement** — insert router checkpoints to prevent unbounded chains
4. **Documentation** — update skill descriptions to be more accurate
5. **Dry-run additions** — add dry-run modes to custom skills
6. **Delta-logger context** — improve the format of what gets logged

---

## Constitutional Improvements (Requires Arif)

These require explicit F13 approval:

1. Any change to F1-F13 interpretation
2. New skill that touches routing, governance, or constitutional layers
3. Changes to the spine protocol (registrar → clerk → forge)
4. Changes to SOUL.md or USER.md
5. Any deletion of a skill
6. Any modification of ORTHOGONALITY_MANIFEST ownership entries
7. Migration of secrets or tokens
8. Any action that bypasses the federation spine

---

## 30-Day Self-Audit

Every 30 days, Hermes runs a self-audit:

1. Scan all skills invoked in the last 30 days
2. Flag skills with zero invocations → soft-deprecate
3. Flag skills with only one caller → check if ownership is correct
4. Flag skills in COMPOSES_WITH lists that no longer exist
5. Review ORTHOGONALITY_MANIFEST for outdated entries
6. Present findings to Arif in a weekly summary

---

## Integration with skill-forensics

skill-forensics is the operational tool. hermes-self-improvement is the governing loop.

```
Every task completion
     ↓
skill-forensics: was the right skill used?
     ↓
hermes-self-improvement: should we improve the skill system?
     ↓
delta-logger: log the observation
     ↓
SEAL or ESCALATE
```

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Escalations per session | ≤ 2 |
| Chain depth violations | 0 |
| Overlaps resolved within 1 session | 100% |
| Skill drift detection latency | ≤ 7 days |
| User corrections requiring re-escalation | ≤ 10% |

---

## Metadata

```yaml
skill:
  name: hermes-self-improvement
  type: self-governance
  tier: L0_CONSTITUTIONAL (governs the loop, not the domain)
  owner: ASI_arifos_bot
  reviews: daily (autonomous), weekly (Arif review)
  last_audit: 2026-05-11
  status: ACTIVE
```

---

## Citation

This skill inherits from:
- arifOS_bot SOUL.md (F1-F13 framework)
- ORTHOGONALITY_MANIFEST.md (skill ownership)
- AAA CHARTER (federation governance)
- skill-forensics (operational implementation)