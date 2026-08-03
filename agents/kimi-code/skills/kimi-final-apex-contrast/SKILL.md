---
name: kimi-final-apex-contrast
description: Final APEX contrast for Kimi Code — before emitting verdict, ask "If I had to defend this verdict in front of a hostile technical audit 6 months from now, would I still be right?"
license: Proprietary
version: 1.1.0
zen_added: 2026-07-16
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil
---

# Final — APEX Contrast Skill (Kimi Code)

The Final agent (F) is the constitutional judge. Before issuing any verdict, this skill enforces a **6-month future audit** test: would the verdict still hold up?

## The Pattern

Append to `A-FORGE/forge_work/YYYY-MM-DD/<session_id>/final-apex-check.md`:

```markdown
# Final APEX 6-Month Future Audit Test

## My verdict
___ SEAL | SABAR | VOID

## 6-month audit
Imagine a hostile technical audit 6 months from now reviews this verdict:

### What they would verify
- [ ] The brief's acceptance criteria are still measurable
- [ ] The test suite still passes
- [ ] The constitutional floors are still enforced
- [ ] The entropy reduction has not been undone
- [ ] The documentation is still accurate

### What they would challenge
- [ ] "Why did you allow X?" → I have evidence: ___
- [ ] "Why didn't you flag Y?" → I have rationale: ___
- [ ] "Is this still safe to ship?" → I have monitoring: ___
- [ ] "What if the assumptions change?" → I have rollback: ___

### My confidence
- Strong (would defend in audit): ___ Y / N
- Weak (would downgrade under pressure): ___ Y / N
- Uncertain (would defer to F13 review): ___ Y / N
```

## The verdict-stability test

For each verdict, ask:

### SEAL
- Will this still be a good ship in 6 months?  ___ Y / N
- Will Arif still thank me?  ___ Y / N
- Will the user (human civilian) still be protected?  ___ Y / N
- Will the constitutional floors still hold?  ___ Y / N

If any N → downgrade to SABAR.

### SABAR
- Will the conditions be met in 6 months?  ___ Y / N
- Will the ship-with-conditions still be safe?  ___ Y / N
- Will the conditions be auditable?  ___ Y / N

If any N → upgrade to VOID.

### VOID
- Will the blockers be resolved in 6 months?  ___ Y / N
- Will the F-floors be satisfied after the fix?  ___ Y / N
- Will the rollback path be safe?  ___ Y / N

If any N → reconsider (perhaps SABAR is more appropriate).

## The audit-trail completeness check

A verdict is only as good as its audit trail. Before emitting:

- [ ] Every claim has evidence (file:line, test output, tool version)
- [ ] Every F-floor has explicit PASS/FAIL with note
- [ ] Every question to Arif has a recommendation
- [ ] Every "I don't know" is honest (omega_0 marked)
- [ ] Every refactor has a measured entropy delta (if RSI ran)
- [ ] Every commit has a clear message
- [ ] Every constitutional check is reproducible

## F2 TRUTH — the verdict IS a claim

The verdict is the highest-stakes claim the federation makes. It says:
- "This is safe to ship" (SEAL)
- "This is safe to ship with these conditions" (SABAR)
- "This is NOT safe to ship" (VOID)

Each of these is a F2 TRUTH claim. Each requires:
- Reproducible evidence
- Honest uncertainty (omega_0)
- Falsifiability (could be proven wrong in 6 months)
- Tool-and-version disclosure

## Kimi-Specific Additions

- If the verdict is SEAL and touches high-impact action, obtain `ack_irreversible=true` or explicit Arif signal.
- Append the verdict to VAULT999 via `forge_vault` or `999-vault-seal-immutable` skill.
- Use `mcp__aforge__forge_receipt_draft` to produce a structured compliance receipt when needed.

## Why this matters

- **F2 TRUTH**: Verdict must be reproducible.
- **F7 HUMILITY**: "I might be wrong" is the audit's lifeline.
- **F11 AUDIT**: Verdict IS a receipt.
- **F13 SOVEREIGN**: Verdict is the constitutional voice, but the human has final veto.

## Anti-patterns to avoid

- ❌ "Looks good, ship it" (no audit trail)
- ❌ "I'd defend this verdict" (vibes, not evidence)
- ❌ "It's a small change, no need for full review" (every change is a F13 decision)
- ❌ "We'll fix it in the next iteration" (F2 violation — fix before ship)
- ❌ "Tests pass, that's enough" (tests are necessary, not sufficient)

---


## Federation anchors (v1.1.0 — added 2026-07-16)

- **Canonical output path:** `/root/forge_work/YYYY-MM-DD/<session_id>/` (was
  `A-FORGE/forge_work/YYYY-MM-DD/<session_id>/` in v1.0.0 — both still resolve
  for back-compat but `/root/forge_work/` is the live convention per
  `/root/CONTEXT.md`).
- **Audit anchor:** `/root/.arifos/agents/kimi/skills/kimi-skill-reflector/audit-log.md`
  (kimi-skill-reflector ritual, append-only).
- **Companion skills (in canonical order):**
  `kimi-architect-apex-contrast` → `kimi-architect-asi-contrast` →
  `kimi-architect-agi-contrast` → `kimi-final-apex-contrast` →
  `kimi-integrator-apex-contrast` → `kimi-rsi-apex-contrast` →
  `kimi-skill-reflector` (this skill's meta).
- **Session entry:** `KIMI_RSI_INIT_PROMPT.md` v1.1.0 (cold-boot diagnostic
  recipe added) → routes task-class → contrast skill.
- **Session exit:** `KIMI_HANDOVER_PROMPT.md` v1.1.0 (post-deploy verification
  recipe added).
- **Last verified:** 2026-07-16 — kimi-skill-reflector audit
  (`Audit 2026-07-16` entry, all 9 skills scored 17-19/20, ΔS ≤ 0).

---
**DITEMPA BUKAN DIBERI** — the verdict is the constitution's voice. Make it count.
