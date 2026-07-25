---
name: ASI-session-seal-copilot
description: >
  DEPRECATED — Canonical seal is now /root/AAA/prompts/SEAL.md (the ONE seal for ALL agents).
  This skill retained as harness-specific bridge for Copilot CLI execution semantics.
  USE WHEN: seal session, end session, handoff, close arc, seal.
  HARBOR: copilot-cli
  CANON: /root/AAA/prompts/SEAL.md
version: 2026.07.25
floors: [F1, F2, F3, F7, F11]
status: DEPRECATED_CANONICAL_REDIRECT
---

# ASI — Session Seal (Copilot CLI)

> **DEPRECATED:** Canonical seal ceremony is now `/root/AAA/prompts/SEAL.md` — the ONE seal for ALL agents.
> This file is a harness-specific bridge. For seal doctrine, tiers, ceremony steps, and anti-patterns, load SEAL.md.

## Quick Route

```
Copilot CLI → SEAL.md §2 Path B (forge_vault, session.ledger tier)
Grok/AAA   → SEAL.md §2 Path B (forge_vault, session.ledger tier)  
Sovereign  → SEAL.md §2 Path A (arif_seal, VAULT999 tier, requires arif_judge SEAL verdict)
```

## Copilot-Specific Execution

1. Probe organs — `curl :port/health` 6 organs
2. Inventory — done/open with commit SHAs
3. Write receipt — `/root/forge_work/YYYY-MM-DD/SESSION-SEAL-*.md`
4. Append memory — `/root/memory/YYYY-MM-DD.md`
5. Update session state — `/root/.claude/projects/-root/memory/session-state.md`
6. VAULT999 append — via `forge_vault(mode="write")` Path B, or direct canonicalizer
7. Update handoff — `/root/AAA/prompts/GROK_AAA_NEXT_INIT.md`
8. Report — ≤10 lines to sovereign

## Cross-refs
- **Canonical seal:** `/root/AAA/prompts/SEAL.md`
- Authority doctrine: `/root/AAA/docs/SEAL_AUTHORITY_DOCTRINE.md`
- Sister skill: `/root/.agents/skills/ASI-session-seal/SKILL.md`
- Vault: `/root/arifOS/VAULT999/outcomes.jsonl`
