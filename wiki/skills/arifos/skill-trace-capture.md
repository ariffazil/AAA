---
title: "SKILL: Trace Capture — Post-Task Evidence Emission"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
tags: [trace, evidence, capture, post-task, TREE777, metadata, artifact]
category: governance
risk_band: LOW
floors: [F2, F4, F11]
evidence_required: false
sources: [wiki/concepts/TREE777.md, wiki/concepts/concept-memory-knowledge-paradox.md]
confidence: high
status: canonical
---

# SKILL: Trace Capture

> **Skill ID:** `skill-trace-capture`
> **Canonical location:** `AAA/wiki/skills/skill-trace-capture.md`
> **Status:** CANONICAL — this is a meta-skill, not a draft
> **When to use:** After EVERY non-trivial task — before session end or before moving to new work
> **Severity:** LOW risk_band — this skill only writes evidence, never modifies canonical pages

---

## Summary

After completing any non-trivial task, emit four artifacts:
1. A trace/event log of what happened
2. An evidence bundle of raw outputs and receipts
3. A proposed wiki delta (what should change in TREE777)
4. A confidence/risk tag (LOW / MEDIUM / HIGH / 888_HOLD)

This is the **entry point** to the promotion ladder. If you only do one thing after work, do this.

---

## Trigger Conditions

**Always run after:**
- Any task that took more than 5 tool calls
- Any task where the agent made a decision (not just followed a script)
- Any task that produced a non-trivial output (file creation, API call, config change)
- Any task where the agent was uncertain and made a judgment call
- Session end (end of any non-trivial session)

**Can skip if:**
- Task was a simple read-only query (just looked something up)
- Task was trivially simple (one tool call, obvious outcome)
- No new information was produced

---

## Procedure

### Step 1: Compose the Trace

Write a plain-text trace of what happened. Format:

```
TRACE: [YYYY-MM-DD HH:MM] | AGENT: {agent-name} | TASK: {one-line task description}
---
Step 1: [what was attempted]
Step 2: [what happened]
Step 3: [outcome]
---
Confidence: [LOW / MEDIUM / HIGH]
Risk: [LOW / MEDIUM / HIGH / 888_HOLD]
```

**Example:**
```
TRACE: 2026-05-17 14:30 | AGENT: claude-code | TASK: Patch Gemini config with SPATIAL_LAW
---
Step 1: Read Gemini config location (~/.gemini/system.md)
Step 2: Appended SPATIAL_LAW block to end of file
Step 3: Verified with grep — match found
---
Confidence: HIGH
Risk: LOW
```

### Step 2: Collect Evidence Bundle

For each significant action, capture:
- The exact command or API call made
- The raw output (not summarized, not interpreted)
- The verification result

Store in `wiki/raw/notes/{YYYY-MM-DD}_{agent}_{task-slug}.md`:

```markdown
# Evidence: {task description}
**Agent:** {agent}
**Timestamp:** {ISO 8601}
**Task:** {what was attempted}

## Raw outputs

### Command 1: {description}
\`\`\`
{raw output verbatim}
\`\`\`

### Verification: {what was checked}
\`\`\`
{verification output verbatim}
\`\`\`
```

**Rule:** Capture raw outputs, not interpretations. Let future readers interpret.

### Step 3: Write the Proposed Delta

Based on what happened, what should change in TREE777?

| Situation | Proposed delta |
|-----------|---------------|
| New failure pattern observed | `wiki/scars/scar-{incident}-{date}.md` draft (status: proposed) |
| New successful technique discovered | `wiki/skills/skill-{name}.md` draft (status: proposed) |
| Existing skill out of date | Update `wiki/log.md` with correction proposal |
| New concept needed | `wiki/concepts/concept-{name}.md` draft (status: proposed) |
| Evidence that existing page is wrong | Write correction to `wiki/raw/notes/` + propose via log |
| No change needed | State "no TREE777 delta" |

**Format for proposed delta in log:**
```
## [YYYY-MM-DD] PROPOSED | {agent} | {delta description}
- Page: {which page}
- Change: {what should change}
- Evidence: {where raw evidence is stored}
- Confidence: {your confidence this should change}
- Risk: {impact if wrong}
```

### Step 4: Assign Confidence/Risk Tag

| Tag | When |
|-----|------|
| **LOW** | Task was routine, outcome was expected, no surprises |
| **MEDIUM** | Task had complexity, some uncertainty, outcome was reached but not trivially |
| **HIGH** | Task had novel elements, significant uncertainty, or non-obvious outcome |
| **888_HOLD** | Task revealed something that should not be changed without 888 deliberation — escalate immediately |

### Step 5: Append to wiki/log.md

```bash
# Format for log entry
## [YYYY-MM-DD HH:MM] trace | {agent} | {task summary} | {outcome}
- Confidence: {tag}
- Risk: {tag}
- Evidence: {path to evidence bundle}
- Proposed delta: {description or "none"}
```

---

## Preconditions

- Task completed (at least attempted)
- Terminal/file access to write to `wiki/log.md` and `wiki/raw/notes/`
- Basic awareness of what "non-trivial" means (5+ tool calls, decisions made, novel elements)

---

## Expected Outputs

- `wiki/log.md` entry appended with trace summary
- `wiki/raw/notes/{YYYY-MM-DD}_{agent}_{task-slug}.md` evidence file created
- Log entry includes: confidence tag, risk tag, evidence path, proposed delta (or "none")

---

## Failure Modes

| Failure | Mitigation |
|---------|-----------|
| No significant output to capture | Still log the attempt — "task attempted, no novel output" |
| Can't write to wiki (permission) | Write to local tmp, propose in session summary |
| Evidence too large to store | Summarize key signals; note full output available in session logs |
| Unsure whether task was "non-trivial" | Default to capturing trace — safer than missing evidence |

---

## Relationship to Other Meta-Skills

This skill is the **entry point** to the promotion ladder:

```
skill-trace-capture (this skill)
    ↓ emits evidence bundle
skill-scar-distill (next skill)
    ↓ if failure pattern detected
skill-skill-promote
    ↓ if pattern repeats 2-3x
→ 888 JUDGE promotion
```

---

## Related Pages

- [[TREE777]] — governance framework this skill implements
- [[skill-scar-distill]] — next skill in the ladder (converts failures to scar drafts)
- [[skill-skill-promote]] — skill for promoting patterns to canonical
- [[concept-memory-knowledge-paradox]] — the bidirectional mirror this skill feeds

---

*DITEMPA BUKAN DIBERI — Capture first. Prove later. Always.*
