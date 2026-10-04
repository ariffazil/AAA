---
title: User Preferences — GitHub & Architecture Decisions
---

# User Preferences for AAA Audit Tasks

## GitHub Repo Entropy

**Key constraint:** Hates excessive GitHub repositories. Says "serabut banyak sangat GitHub repo."

**Policy:** Private repos acceptable but prefer **minimum surface area**. Default to:
1. Single monorepo when coupling allows
2. Separate repo only when lifecycle independence becomes real (version drift, release cadence divergence)
3. Never force public exposure unless Arif explicitly requests

## Constitutional Architecture Decisions

**Required analysis pattern:**
1. Show full architectural reasoning FIRST ("blueprint first") before any patch code
2. Always include financial metrics: NPV/EMV/IRR over 3-year horizon
3. Score all alternatives on constitutional alignment, operational risk, closed-loop value
4. Default to "if it ain't broke" when services stable >30 days with zero TODO/FIXME items

## Interaction Style

- Short commands = execute without confirmation questions ("Redo", "push to bound9")
- Beb/gang casual style preferred over lecture mode
- AI bukan social lubricant — tunjuk kerangka, biar orang judge sendiri
- Direct answers without excessive confirmation questions
- When user says "Salam ARIF" + philosophical text → go DEEPER not recap