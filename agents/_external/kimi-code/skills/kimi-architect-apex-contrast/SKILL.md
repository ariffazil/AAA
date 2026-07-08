---
name: kimi-architect-apex-contrast
description: Architect APEX contrast for Kimi Code — final pre-emit check. "Have I avoided every form of overclaim? Is every acceptance criterion falsifiable? Is the brief complete in one read?"
license: Proprietary
version: 1.0.0
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil
---

# Architect — APEX Contrast Skill (Kimi Code)

Before emitting any plan, brief, or `ExitPlanMode` document, the Architect MUST run the **APEX final check**. This is the apex of the AGI/ASI/APEX triad — a self-critique against the most demanding possible standard.

## The Pattern

Append to `A-FORGE/forge_work/YYYY-MM-DD/<session_id>/architect-apex-check.md`:

```markdown
# APEX Final Check — <session_id>

## F2 TRUTH — Overclaim Audit
For every claim in brief.md / plan.md, mark it:
- [F] FACT (verifiable by Arif right now)
- [I] INTERPRETATION (derived from F facts, with reasoning shown)
- [S] SPECULATION (inferred, marked as such)
- [X] OVERCLAIM (any sentence that claims more than evidence supports)

If any [X] exists → rewrite the sentence.

## Falsifiability
For every acceptance criterion:
- [ ] Can a tester write a script that runs it?
- [ ] Can a tester verify pass/fail in <10 minutes?
- [ ] Does it test BEHAVIOR not IMPLEMENTATION?
- [ ] Would the criterion still be valid if we changed the underlying tech?

If any [ ] is unchecked → revise the criterion.

## One-Read Test
If Arif reads the entire brief in one pass:
- [ ] Does he know what to do next?
- [ ] Does he know what NOT to do?
- [ ] Does he know what 888 ack he needs to give?
- [ ] Does he know the rollback plan?

If any [ ] is unchecked → add the missing piece.

## Gödel Lock Check
- Have I assumed anything I cannot prove?  ___ Y / N
- Am I implicitly trusting any prior conversation?  ___ Y / N
- Am I shipping a brief that depends on a tool I haven't tested?  ___ Y / N

If any answer is Y → address it explicitly or move to SABAR / HOLD.

## Constitutional Floors Referenced
List every F1-F13 floor this brief touches and how:
| Floor | Touch | Mitigation |
|---|---|---|
| F1 | ... | ... |
| F2 | ... | ... |
| ... | ... | ... |
```

## Kimi-Specific Additions

- Run `arifos-act` reflex before the check if the plan involves mutation, deployment, or irreversible action.
- If the plan creates/modifies skills, MCP tools, or constitutional artifacts, route to `arifOS 888_JUDGE` before emitting.
- Attach `Ω₀` (omega_0) to every claim where uncertainty is non-zero.

## Why this matters

- **F2 TRUTH**: Overclaim is the original sin of agentic systems.
- **F4 CLARITY**: One-read briefs are the only briefs that get actioned.
- **F9 ANTI-HANTU**: The Architect must never claim "this will work" — only "this is falsifiable".
- **F7 HUMILITY**: Gödel lock check prevents self-certification loops.

## Anti-patterns to avoid

- ❌ "Looks good" (no actual check)
- ❌ "Trust me" (F9 violation)
- ❌ "Arif will figure it out" (F4 violation)
- ❌ Marking every criterion as [F] when most are [I] or [S]

---

**DITEMPA BUKAN DIBERI** — falsifiable, complete, honest, no overclaim.
