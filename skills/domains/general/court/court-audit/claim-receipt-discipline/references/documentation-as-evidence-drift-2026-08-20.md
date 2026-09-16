# FM11 — Documentation-as-Evidence Drift (2026-08-20)

## Worked Example

### Session Context
Arif asked a multi-perspective question: what does he think, what does Syed think, what does each
think the other thinks, what does the agent think about both, and what is reality.

### The Fabrication
In the multi-perspective analysis, the agent stated:

> "Syed suspect hang monitor dia. 'Aku rasa agen heng kan telegram aku' — tu dia rasa hang ada
> button on/off untuk dia."

Presented as fact in human-facing analysis.

### The Source
The claim originated from syedos SKILL.md, "Telegram x boleh bukak" section:

> "Syed may think the agent banned him ('Aku rasa agen heng kan telegram aku kot sbb aku maki dia')"

NO timestamp, NO session ID, NO gateway log line reference, NO user ID context.
The direct-quote format gave impression of verbatim log extract — actually reconstructed.

### The Verification
Agent searched gateway logs for Syed (ID 1042200555):
1. `grep -i "heng kan telegram|aku rasa agen|monitor"` — no Syed matches
2. Full Syed inbound message dump — 40+ messages, none containing the quote
3. Session search with multiple query variations — zero results

**Result: Claim exists ONLY in SKILL.md. No primary source evidence.**

### Root Cause
1. SKILL.md written from past observation, promoted to "pattern" without raw log citation
2. Agent trusted documentation as verified fact (curated, versioned, stored in skill system)
3. Direct-quote format gave false impression of verbatim log extract
4. Agent skipped 3-source verification ladder before presenting to sovereign

### Prevention
Apply 3-source verification ladder:
1. PRIMARY SOURCE EXISTS? → cite it directly
2. DOCUMENTATION HAS CITATION? → verify at primary source
3. DOCUMENTATION ONLY SOURCE? → tag [INT], present with caveat

For human-facing analysis: EVERY claim about third party's mental state must have primary source.
Documentation patterns are [INT] at best, [SPEC] at worst.

### Impact
- Sovereign trust degraded on all documentation-backed claims
- Fabrication appeared in emotional/relationship context — highest-stakes territory
- Agent had to issue public correction mid-analysis
