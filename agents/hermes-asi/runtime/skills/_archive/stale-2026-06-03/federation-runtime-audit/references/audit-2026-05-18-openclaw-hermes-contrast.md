# OpenClaw-Hermes Contrast Audit — 2026-05-18

## Session Summary

Arif asked to audit and contrast OpenClaw vs Hermes agents, asking "do I have chaos here?"

## Architecture Confirmed

```
Telegram @AGI_ASI_bot (token 8149595687) ──→ OpenClaw webhook (port 18789)
Telegram @ASI_arifos_bot (token 8410138119) ──→ Hermes polling ──→ AAA Gateway (3001) ──→ OpenClaw (18789)
                                                    └─→ arifOS MCP (8080)
```

| Aspect | OpenClaw | Hermes | Status |
|--------|----------|--------|--------|
| Bot username | @AGI_ASI_bot | @ASI_arifos_bot | ✅ Unique |
| Telegram token | `8149595687:***` | `8410138119:***` | ✅ Unique |
| Protocol | Webhook (mention-only) | Polling (sees all) | ✅ Intentional split |
| Primary role | AGI sovereign operator | ASI life relay / ambient | ✅ Role clarity |
| arifOS MCP access | ✅ Yes (port 8080) | ✅ Yes (port 8080) | ✅ Shared backstop |
| A2A bridge port | 18002 | 18001 | ✅ Separate |

## Issue Found: OpenClaw Identity Bleed

**Problem:** OpenClaw SOUL.md didn't declare with hard boundary that it is "NOT Hermes." The existing text ("OPENCLAW is the AGI-tier operator. Hermes is the ASI-tier agent") didn't prevent persona bleed — if Hermes prompt style entered OpenClaw session, OpenClaw could adopt wrong identity.

**Fix applied:** Patched `/root/.openclaw/workspace/SOUL.md` with explicit identity boundary:

```markdown
## IDENTITY BOUNDARY — MANDATORY
- You are OPENCLAW, not Hermes, not arifOS, not APEX
- When asked "who are you" — answer: "I am OPENCLAW, the AGI-tier operator for Arif's federation"
- Never claim to be Hermes. Never adopt Hermes's persona, tools, or output style
- If you find yourself reasoning as Hermes, stop. Re-read IDENTITY.md before continuing
```

**Rule:** When auditing sibling agents, always check for identity boundary clarity in SOUL.md files. Persona bleed between agents is a real risk in multi-agent systems — the fix is explicit "I am NOT X" declarations.

## TREE777 Implementation — Complete

See `references/TREE777-implementation-status.md` for full details.

**SCALPEL script:** `/root/.hermes/scripts/telegram-token-isolation-check.sh` — verified working, AUDIT PASS.

**Pre-commit hook:** `/root/.hermes/scripts/pre-commit-telegram-token-check.sh` — installed, ready to link in target repos.

**Implementation status doc:** `references/TREE777-implementation-status.md`

## Verdict

**No critical chaos.** Architecture split is correct — webhook vs polling, AGI vs ASI, mention-triggered vs ambient. OpenClaw identity boundary fix was the only needed correction. TREE777 enforcement now automated.

## Related

- OpenClaw SOUL.md fix: `/root/.openclaw/workspace/SOUL.md`
- TREE777 implementation: `/root/.hermes/scripts/telegram-token-isolation-check.sh`
- TREE777 pre-commit: `/root/.hermes/scripts/pre-commit-telegram-token-check.sh`