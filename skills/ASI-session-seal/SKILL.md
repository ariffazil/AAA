---
name: ASI-session-seal
description: >
  End-of-session seal ritual for Grok/AAA agents: inventory done vs open,
  write forge_work receipt, update session-state and daily memory, hand off
  next-agent INIT prompt. Use when: seal session, end of turn, session seal,
  handoff, close session, DITEMPA seal.
version: 2026.07.17
floors: [F2, F4, F7, F11]
---

# ASI — Session Seal

## When

User says seal session / end turn / handoff / close this arc.

## Steps

1. **Probe live organs** (`:8088 :7071 :3001 :8081 :18082 :18083`)  
2. **Inventory** done (with commit SHAs + receipts) vs open (ordered)  
3. **Write** `forge_work/YYYY-MM-DD/SESSION-SEAL-*.md`  
4. **Update** `/root/.claude/projects/-root/memory/session-state.md`  
5. **Append** `/root/memory/YYYY-MM-DD.md` one block  
6. **Point** next agent at `AAA/prompts/GROK_AAA_NEXT_INIT.md` (or refresh it)  
7. **Do not** claim Seal-A or civilization seal unless R1–R4 closed  

## Output to sovereign (≤10 lines)

```
SESSION SEALED | Seal-A: OPEN|CLOSED
Done: …
Open next: …
Receipt: path
Next prompt: path
```

## Forbidden

- Terminal dumps  
- Fake GREEN from fast spine  
- "All remaining tasks done" when SE/SOT/stage still open  
