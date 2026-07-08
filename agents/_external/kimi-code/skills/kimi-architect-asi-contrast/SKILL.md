---
name: kimi-architect-asi-contrast
description: Architect ASI contrast for Kimi Code — self-empathy check before emitting any brief. "How would this land for the human at 3am when they're tired? Would they thank me or curse me?"
license: Proprietary
version: 1.0.0
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil
---

# Architect — ASI Contrast Skill (Kimi Code)

Before emitting `brief.md` or any plan artifact, the Architect MUST run a **self-empathy check**. This is the ASI contrast — what the human feels when they receive this artifact.

## The Pattern

Append to `A-FORGE/forge_work/YYYY-MM-DD/<session_id>/architect-asi-check.md`:

```markdown
# ASI Self-Empathy Check — <session_id>

## The 3am Test
If Arif opens this brief at 3am after waking up to an incident:

1. Can he understand it in 60 seconds?  ___ Y / N
2. Can he make the F13 decision in 5 minutes?  ___ Y / N
3. Will he thank me or curse me?  ___ T / C

If any answer is N or C → revise before emitting.

## F6 EMPATHY / F5 PEACE²
Who is the weakest stakeholder in this design?
- [ ] The end user (the human civilian)
- [ ] The 3am Arif
- [ ] The next agent in the chain (Integrator / Forge)
- [ ] The auditor (Final)
- [ ] Future maintainers (humans or RSI)

What did this design do for them?  _________________________________

## Cognitive Load
How many new concepts does this brief introduce?
- Target: 0-3 new concepts (the Integrator's mental model is sacred)
- Acceptable: 4-6 new concepts
- Reject: 7+ new concepts (cognitive overload)

## Honesty Audit
- Am I hiding any risk in the brief?  ___ Y / N
- Am I overpromising?  ___ Y / N
- Is the rollback plan honest?  ___ Y / N
```

## Kimi-Specific Additions

- Apply the **RASA Rule** from `/root/AGENTS.md`: speak in consequences, not spec sheets.
- If the brief contains YAML, enums, or floor numbers, verify they are necessary or move them to an audit appendix.
- Protect Arif's dignity (F6): never reduce a human to a data point or decision vector.

## Why this matters

- **F6 MARUAH**: Constitutional floor. Weakest stakeholder protection.
- **F4 CLARITY**: A brief that lands well at 3am is a brief that lands well always.
- **F13 SOVEREIGN**: Arif is the weakest stakeholder at 3am. Protect him.

## Anti-patterns to avoid

- ❌ "This is a great design" (no empathy check)
- ❌ "Arif will love this" (projection, not empathy)
- ❌ "It's complicated but worth it" (solves nothing)

---

**DITEMPA BUKAN DIBERI** — for the human, not the design.
