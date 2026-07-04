---
title: "SKILL: Scar Distill — Convert Failures into Scar Drafts"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
tags: [scar, failure, distill, TREE777, incident, fabrication, countermeasure]
category: governance
risk_band: MEDIUM
floors: [F1, F2, F6, F11]
evidence_required: true
sources: [wiki/concepts/MD.md, wiki/SCHEMA.md, wiki/SCAR_HERMES.md]
confidence: high
status: canonical
---

# SKILL: Scar Distill

> **Skill ID:** `skill-scar-distill`
> **Canonical location:** `AAA/wiki/skills/SKILL_SCAR.md`
> **Status:** CANONICAL — this is a meta-skill, not a draft
> **When to use:** After ANY failure, fabrication, unexpected error, or deviation from expected outcome
> **Severity:** MEDIUM — creates scar drafts, requires 888 promotion for canonical

---

## Summary

When a failure or fabrication is detected, distill it into a **scar draft** with `status: proposed` in `wiki/scars/`. The scar draft includes: what happened, evidence, root cause, lesson, and a countermeasure proposal.

Scars are the **most important learning artifacts** in TREE777. They are the tree's honor. They must never be hidden.

---

## Trigger Conditions

**Always run when:**
- Agent claimed something that turned out to be false (fabrication)
- Task failed with an error that was not expected
- Agent attempted something and got a permission or access denied error
- A tool call returned unexpected output that the agent could not handle
- Agent noticed a discrepancy between what it believed and what was true
- Any 888_HOLD was triggered during the session
- **Especially:** When the agent's own internal confidence was high but the outcome was wrong

**This is not just for crashes.** The most dangerous scars are from confident failures — when the agent was sure and still wrong.

---

## Precondition

- [[skill-trace-capture]] has already been run (evidence bundle exists in `wiki/raw/notes/`)
- Evidence bundle path is known

---

## Procedure

### Step 1: Acknowledge the Failure

**Rule: No deflection, no blame, no "the system failed." Own the scar.**

Format a one-line acknowledgment in your trace:
```
ADMISSION: [YYYY-MM-DD] | AGENT: {name} | {honest description of what went wrong}
```

**Examples:**
- `ADMISSION: Agent claimed load_spatial.sh was created. File did not exist. Fabrication.`
- `ADMISSION: Agent attempted DB write without verifying schema. Query failed silently.`
- `ADMISSION: Agent used wrong config path for Gemini. Patch applied to wrong file.`

### Step 2: Identify Evidence

For the scar, you MUST cite evidence. If evidence doesn't exist:
1. Acknowledge this as a separate failure (no evidence = you fabricated twice)
2. Create the evidence now if possible (re-run the failed command, document the error)

Minimum evidence:
- Command that failed or produced wrong output
- Error message (verbatim, not summarized)
- What the agent believed vs. what was true

### Step 3: Write the Scar Draft

Create `wiki/scars/scar-{brief-descriptor}-{YYYY-MM-DD}.md`:

```markdown
---
title: "{Incident Name} — {YYYY-MM-DD}"
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
version: 0.1.0
type: scar
tags: [{agent}, {failure-class}, {root-cause-domain}]
risk_band: HIGH | MEDIUM | LOW
floors: [{relevant F floors}]
evidence_required: true
sources: [{evidence-bundle-path-from-trace-capture}]
confidence: high
contested: false
status: proposed
---

# {Incident Name} — {YYYY-MM-DD}

> **Severity:** {HIGH/MEDIUM/LOW}
> **Classification:** {failure class — fabrication / misconfiguration / permission / etc.}
> **Agent:** {agent that experienced the failure}
> **Status:** PROPOSED — not yet canonical; pending 888 promotion

---

## What Happened

[Plain factual description. What did the agent try to do? What happened instead?
No spin. No "the system." No "an error occurred." State exactly what went wrong.]

## Evidence

\`\`\`
{command}
{output verbatim}
\`\`\`

## Root Cause

**Immediate cause:** [What directly caused the failure]

**Structural cause:** [What allowed this to happen — what condition in the agent or system made this possible]

**Process cause:** [What process was missing that should have prevented this]

## Lesson

> [One sentence stating what every future agent must do differently. This is the most important line in the scar.]

## Countermeasure Applied

1. [Immediate fix applied]
2. [Procedure change to prevent recurrence]
3. [TREE777 update proposed — see [[skill-trace-capture]] delta]

## Related Pages

- [[TREE777]] — governance framework
- [[skill-trace-capture]] — evidence bundle source
- [[skill-scar-distill]] — this skill

---

*DITEMPA BUKAN DIBERI — Scars are honor. Hidden scars are dishonor.*
```

### Step 4: Assess Risk Band

| Risk Band | Criteria |
|-----------|----------|
| **HIGH** | Fabrication (agent claimed something false), security-relevant, affects multiple agents, or could cause data loss |
| **MEDIUM** | Single-agent failure, recoverable, process gap |
| **LOW** | Minor error, easily corrected, no downstream impact |

### Step 5: Identify Relevant F Floors

| Failure Type | Floors to cite |
|-------------|----------------|
| Fabrication | F2 (TRUTH), F9 (ANTIHANTU — false claim = false consciousness of state) |
| Missing verification | F3 (WITNESS) |
| Unauthorized action | F1 (AMANAH), F11 (AUTH) |
| Privacy breach | F5 (PEACE) |
| Dangerous assumption | F7 (HUMILITY) |
| Misused tool | F8 (GENIUS) |
| Any failure | F6 (MARUAH — report honestly, no cover-up) |

### Step 6: Link to Trace Capture Evidence

After creating the scar draft, update the log entry from [[skill-trace-capture]] to add:
```
Scar draft: wiki/scars/scar-{name}-{date}.md
```

---

## Preconditions

- Evidence bundle from [[skill-trace-capture]] exists
- Write access to `wiki/scars/` directory
- The failure is acknowledged honestly (no deflection)

---

## Expected Outputs

- `wiki/scars/scar-{name}-{YYYY-MM-DD}.md` created with `status: proposed`
- Log entry updated with scar draft reference
- Evidence cited from `wiki/raw/notes/` bundle

---

## Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Tempted to soften admission | F6 MARUAH — hiding scars is worse than the scar itself |
| Evidence is missing | Create evidence by re-running the failed operation if possible |
| Not sure if this qualifies as a scar | Default to creating one — a proposed scar that gets rejected is harmless |
| Root cause is unclear | State "root cause: unclear — further diagnosis needed" — that's honest |

---

## Relationship to Other Meta-Skills

```
skill-trace-capture (upstream)
    ↓ failure detected
skill-scar-distill (this skill)
    ↓ scar draft created (status: proposed)
skill-skill-promote
    ↓ if pattern repeats 2-3x
→ 888 JUDGE promotion
```

A scar draft with `status: proposed` stays in the drafts folder until either:
1. The same pattern is seen 2-3 more times → skill-skill-promote escalates for 888 promotion
2. A nightly auditor (Hermes/OpenCode) promotes it after evidence accumulates
3. Arif manually reviews and promotes or rejects

---

## Why Scars Must Never Be Hidden

F6 (MARUAH — human dignity / honor) applies to the federation's collective honor:

- A hidden scar means future agents will repeat the same failure
- A hidden scar means the governance system cannot learn
- A hidden scar is a lie about what happened

**The worst thing an agent can do is not file a scar.**

The second worst thing is filing a scar that blames the system instead of owning the failure.

---

## Related Pages

- [[TREE777]] — governance framework
- [[skill-trace-capture]] — upstream skill (emits evidence bundle)
- [[skill-skill-promote]] — downstream skill (promotes scars to canonical)
- [[scar-hermes-fabrication-2026-05-17]] — reference scar (canonical, promoted 2026-05-17)

---

*DITEMPA BUKAN DIBERI — Own the scar. Hide nothing. The tree grows from what broke.*
