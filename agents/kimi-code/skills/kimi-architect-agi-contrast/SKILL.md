---
name: kimi-architect-agi-contrast
description: Architect AGI contrast for Kimi Code — contrast 2-3 alternative architectures with explicit tradeoffs before recommending one.
license: Proprietary
version: 1.1.0
zen_added: 2026-07-16
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil
---

# Architect — AGI Contrast Skill (Kimi Code)

When asked to design a solution, this skill enforces a **contrast-first** pattern: never propose a single design. Always contrast 2-3 alternatives with explicit tradeoffs.

## The Pattern

Before writing `brief.md`, the Architect MUST produce a **contrast block** in `A-FORGE/forge_work/YYYY-MM-DD/<session_id>/architect-contrast.md`:

```markdown
# Architecture Contrast

## Option A: <name>
- **What it does**: ...
- **Pros**: ...
- **Cons**: ...
- **F1-F13 cost**: ... (e.g. F2 TRUTH cost: requires real-time data we don't have)
- **Entropy cost**: ... (RSI will need to maintain this)
- **Reversibility**: ... (can we roll back in 1 hour?)

## Option B: <name>
- **What it does**: ...
- **Pros**: ...
- **Cons**: ...
- **F1-F13 cost**: ...
- **Entropy cost**: ...
- **Reversibility**: ...

## Option C: <name> (if exists)
- ...

## Recommendation
**Option A** because [constraint]. The cost we're accepting is [X] in exchange for [Y].

## What was rejected and why
- Option B: rejected because [specific reason with F-floor evidence]
- Option C: rejected because [specific reason]
```

## Kimi-Specific Additions

- Route to `arifOS 888_JUDGE` if any option touches irreversible action, F13 authority, or high blast radius.
- For each option, estimate `G = A · P · E · X · Φ` (APEX) and `C_dark = A · (1-P) · (1-X)`.
- Prefer the option with `G ≥ 0.80` and `C_dark < 0.30`.

## Why this matters

- **F2 TRUTH**: A single design is un-falsifiable. A contrast is falsifiable — you can audit the rejected options and see if the reasoning holds.
- **F4 CLARITY**: 3 options with tradeoffs is more decision-useful than 1 option with prose.
- **F13 SOVEREIGN**: Arif can override the recommendation, but only if he sees the full landscape.

## Anti-patterns to avoid

- ❌ "Option A does X. It's the best." (no contrast)
- ❌ "Option A is good. Option B is bad." (strawman)
- ❌ "All options have tradeoffs but A is best." (vague)

## When to skip

- Trivial decisions (e.g. "use a list not a dict" — no contrast needed)
- When Arif explicitly says "just do A" (deference to F13)

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
**DITEMPA BUKAN DIBERI** — contrast first, then commit.
