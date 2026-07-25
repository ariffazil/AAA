---
name: ASI-session-seal
description: >
  DEPRECATED — Canonical seal is now /root/AAA/prompts/SEAL.md (the ONE seal for ALL agents).
  This skill retained as harness-specific bridge for Grok/AAA execution semantics.
  Use when: seal session, end of turn, session seal, handoff, close session.
version: 2026.07.25
floors: [F2, F4, F7, F11]
status: DEPRECATED_CANONICAL_REDIRECT
---

# ASI — Session Seal (Grok/AAA)

> **DEPRECATED:** Canonical seal ceremony is now `/root/AAA/prompts/SEAL.md` — the ONE seal for ALL agents.
> This file is a harness-specific bridge. For seal doctrine, tiers, ceremony steps, and anti-patterns, load SEAL.md.

## Quick Route

```
Grok/AAA   → SEAL.md §2 Path B (forge_vault, session.ledger tier)
Copilot CLI → SEAL.md §2 Path B (forge_vault, session.ledger tier)
Sovereign  → SEAL.md §2 Path A (arif_seal, VAULT999 tier, requires arif_judge SEAL verdict)
```

## Grok/AAA-Specific Execution

1. Probe live organs (`:8088 :7071 :3001 :8081 :18082 :18083`)
2. Inventory done (with commit SHAs + receipts) vs open (ordered)
3. Write `forge_work/YYYY-MM-DD/SESSION-SEAL-*.md`
4. Update `/root/.claude/projects/-root/memory/session-state.md`
5. Append `/root/memory/YYYY-MM-DD.md` one block
6. Refresh `AAA/prompts/GROK_AAA_NEXT_INIT.md` + handoff
7. ATLAS333 checkpoint under `~/.local/share/arifos/atlas333/`
8. Report ≤10 lines to sovereign

## Cross-refs
- **Canonical seal:** `/root/AAA/prompts/SEAL.md`
- Authority doctrine: `/root/AAA/docs/SEAL_AUTHORITY_DOCTRINE.md`
- Copilot variant: `/root/.agents/skills/ASI-session-seal-copilot/SKILL.md`
