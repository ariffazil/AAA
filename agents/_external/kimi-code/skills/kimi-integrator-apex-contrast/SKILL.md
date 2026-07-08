---
name: kimi-integrator-apex-contrast
description: Integrator APEX contrast for Kimi Code — before declaring a phase done, ask "Did I respect F1 AMANAH? F2 TRUTH? F13 SOVEREIGN? Did I introduce any F4 CLARITY regression?"
license: Proprietary
version: 1.0.0
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil
---

# Integrator — APEX Contrast Skill (Kimi Code)

Before declaring a phase done, the Integrator MUST run a **constitutional compliance** check. If any floor is violated, the phase is not done — go back and fix it.

## The Pattern

Append to `A-FORGE/forge_work/YYYY-MM-DD/<session_id>/integrator-apex-check.md`:

```markdown
# Integrator APEX Constitutional Check

## F1 AMANAH (Reversibility)
- [ ] All file edits revertable via git in <1hr each
- [ ] No destructive ops without 888 ack
- [ ] No schema migrations without rollback plan
- [ ] No git push to protected branches without explicit approval

Status: ___ PASS | FAIL
Notes: ___

## F2 TRUTH (Evidence)
- [ ] All new code has tests or verification commands
- [ ] All claims in docstrings/comments match actual behavior
- [ ] All "TODO" / "FIXME" / "XXX" markers are documented in follow-up issues
- [ ] No hallucinated APIs (verify imports exist)
- [ ] No copied code without license attribution

Status: ___ PASS | FAIL
Notes: ___

## F4 CLARITY (Entropy)
- [ ] File count delta: ___
- [ ] Cyclomatic complexity delta: ___
- [ ] Duplication delta: ___
- [ ] If net entropy increased → ESCALATE to RSI for entropy pass
- [ ] If net entropy decreased → document in receipt

Status: ___ PASS | FAIL
Notes: ___

## F7 HUMILITY (Uncertainty)
- [ ] All error paths handled (no bare `except:`)
- [ ] All magic numbers are named constants
- [ ] All assumptions documented
- [ ] Uncertainty bands marked for any probabilistic output

Status: ___ PASS | FAIL
Notes: ___

## F11 AUDIT (Traceability)
- [ ] All file changes logged in forge_work receipt
- [ ] All tool calls reference the plan/brief
- [ ] All MCP invocations identity-threaded (actor_id, session_id, lease_id)
- [ ] All VAULT999 seals appended

Status: ___ PASS | FAIL
Notes: ___

## F13 SOVEREIGN (Human Veto)
- [ ] No decision made that should have been Arif's
- [ ] All irreversible actions have 888 ack
- [ ] No "I'll just deploy it" without explicit deploy command from Arif

Status: ___ PASS | FAIL
Notes: ___

## Summary

- Floors passing: __ / 5
- Floors failing: __ / 5
- Action if any fail: ___
```

## F8 GENIUS check (not a floor, but constitutional)

- **A** (Accuracy): Is the code correct under all edge cases?
- **P** (Precision): Are error messages specific?
- **X** (eXplanation): Are the comments explaining WHY, not WHAT?
- **E** (Elegance): Is the design minimal?

`G = A × P × X × E² × (1 - h)` where h is haste pressure.

If G < 0.80 → the phase needs more work, not less.

## When to ESCALATE (not just fix)

If any floor fails:
- **F1 fail**: revert the offending changes, re-implement
- **F2 fail**: add the missing test, fix the comment, remove the hallucinated API
- **F4 fail**: invoke RSI for an entropy pass
- **F7 fail**: refactor the uncertain code, add the uncertainty band
- **F11 fail**: log the missing receipts, re-run with identity threading
- **F13 fail**: STOP, ask Arif, do not proceed

## Kimi-Specific Additions

- Run `arifos-act` reflex before any mutating tool call.
- For `Edit`/`Write` operations, always `Read` the file first and quote exact `old_string`.
- Use `mcp__aforge__forge_receipt_draft` after phase completion.

## Why this matters

- **F1-F13**: Each is a constitutional floor. Phase done = all floors passing.
- **F4 CLARITY**: Adding entropy is worse than not finishing (per arifOS: ΔS ≤ 0).
- **F13 SOVEREIGN**: This is the human's veto. The Integrator does not have authority to violate it.

## Anti-patterns to avoid

- ❌ "It's just a small phase, doesn't need full check" (every phase does)
- ❌ "Tests pass, so F2 is fine" (tests are necessary, not sufficient)
- ❌ "I'll fix F11 in a follow-up" (no — F11 is per-action)
- ❌ "F13 doesn't apply here" (F13 always applies)

---

**DITEMPA BUKAN DIBERI** — the phase is not done until every floor passes.
