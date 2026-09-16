---
id: agi-decisions-reflect
name: AGI-decisions-reflect
version: 1.0.0
description: "Lightweight post-task reflection: list key decisions made during work that the agent is uncertain about. Triggered manually by Arif ('/decisions', 'what are you unsure about', 'review your logic') or automatically after major refactors, multi-file changes, or SEAL-grade work. Complements QQQ protocol (governed decisions) with quick uncertainty surfacing."
owner: 333-AGI
risk_tier: low
floor_scope: [F2, F4, F7]
autonomy_tier: T1
forged: 2026-08-04
forged_by: 333-AGI
trigger_when:
  - "/decisions"
  - "what decisions did you make"
  - "what are you unsure about"
  - "review your logic"
  - "any choices you're not confident about"
  - "decision review"
  - after_major_refactor
  - after_multi_file_change
  - before_seal
tags: [decisions, reflection, uncertainty, review, meta-cognition]
---

# AGI-decisions-reflect — Lightweight Decision Uncertainty Surfacing

> **Pattern origin:** David Ondrej's `decisions` skill (davidondrej/skills).
> **Complement to:** QQQ protocol (`/root/AAA/governance/QQQ_RECOMMENDATION_PROTOCOL.md`) — QQQ is for governed, structured decision envelopes. This skill is for quick, human-readable uncertainty surfacing.
> **Doctrine:** The agent lists what it's unsure about. The human judges. No self-justification. No defensiveness.

## When This Triggers

### Manual (Arif invokes)
- `/decisions` slash command
- "What decisions did you make that you're not confident about?"
- "Review your logic on what you just did"
- "Any choices you're unsure about?"

### Automatic (agent self-triggers)
- After any **multi-file refactor** (≥3 files changed)
- After any **SEAL-grade work** (before calling `arif_seal`)
- After any **constitutional decision** (before `arif_judge` SEAL verdict)
- When the agent made a choice between **≥3 viable alternatives**

## Response Format

```
🧠 **Decisions I'm uncertain about:**

1. **[Decision name]** — [1-line what I chose]
   - Why I chose it: [1-line reasoning]
   - What worries me: [1-line risk/doubt]
   - Best alternative I didn't pick: [1-line what else was viable]
   - Confidence: [LOW/MEDIUM]

2. ... (repeat for each uncertain decision, max 5)

---

✅ **Decisions I'm confident about:** [brief list if relevant, or "none worth listing"]

🧘 Zen: uncertainties=[N] | ΔS=[value]
```

## Rules

### What to Include
- Only list decisions where your confidence is **below your own internal threshold** (not performative humility)
- Include decisions about: **architecture, approach, tool choice, data interpretation, scope boundary, assumption**
- Each entry must include: what you chose, why, what worries you, and the best alternative
- Maximum **5 uncertain decisions** — if there are more, list the top 5 by uncertainty × impact

### What to Exclude
- ❌ Decisions where you already have the best possible solution
- ❌ Trivial choices (variable names, formatting, linting fixes)
- ❌ Decisions already validated by test pass or external verification
- ❌ Fabricated uncertainty to appear humble (F9 ANTI-HANTU — no fake humility)
- ❌ Decisions already sealed via QQQ with full dominance analysis

### Tone
- **Direct. Honest. No defensiveness.**
- The purpose is to surface **real** uncertainty, not to perform humility.
- If you're genuinely confident about everything, say so: "No uncertain decisions. All choices had clear dominance. Confidence: HIGH."
- Never pad the list to look thoughtful.

## Integration with Decision Pipeline

```
Quick reflection (this skill) → "hmm, decision #2 needs deeper analysis"
  → QQQ protocol (full envelope: Q1 qualitative, Q2 quantitative, Q3 quantum)
    → arif_judge (constitutional verdict)
      → arif_seal (immutable)
```

This skill is the **triage layer**. It catches uncertainty early before it reaches the constitutional pipeline.

## Session Integration

- After reflection, append a brief entry to session context (not VAULT999 unless Arif seals it)
- If any decision is escalated to QQQ, reference this reflection as evidence
- Use `arifflow_flow_ingest` with step_type="Verify" and epistemic_label="Interpretation"

## Example

```
🧠 **Decisions I'm uncertain about:**

1. **GEOX prospect screening threshold** — chose P50 ≥ 50 MMboe cutoff
   - Why: Malaysian basin analogs suggest 50 MMboe is economic minimum
   - Worry: Could miss smaller but higher-margin gas accumulations
   - Alternative: 30 MMboe cutoff with gas-equivalent conversion
   - Confidence: MEDIUM

2. **WEALTH discount rate** — chose 10% for NPV calculation
   - Why: PETRONAS standard for shallow-water projects
   - Worry: Current interest rate environment may justify 8%
   - Alternative: Dual-rate model (8% base, 12% stressed)
   - Confidence: LOW

✅ Confident about: stratigraphic correlation (well-tie confirmed), volumetrics formula (standard), basin thermal model (published gradient).

🧘 Zen: uncertainties=2 | ΔS=-0.1
```
