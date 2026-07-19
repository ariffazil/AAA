---
name: ASI-session-seal
description: >
  End-of-session seal ritual for Grok/AAA agents: inventory done vs open,
  write forge_work receipt, update session-state and daily memory, hand off
  next-agent INIT prompt. Use when: seal session, end of turn, session seal,
  handoff, close session, DITEMPA seal.
version: 2026.07.19
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
6. **Refresh** `AAA/prompts/GROK_AAA_NEXT_INIT.md` + handoff md  
7. **Upgrade** skills that next agent must load (mirror AAA → .agents/.grok if not symlinked)  
8. **ATLAS333 checkpoint** — append survival index AXIS or eureka JSON under `~/.local/share/arifos/atlas333/`  
9. **Do not** claim Seal-A / T3a CLOSED unless matrix 13/13 + R4 green  

## ⚠️ T1 Direct Vault Append (2026-07-19)

When `forge_vault` or `arif_seal` requires F13 elicitation but the seal is T1 (non-sensitive session seal):
- Write directly to `/root/arifOS/VAULT999/outcomes.jsonl` via Python append
- Use the documented canonicalizer from `arifSeal.ts:94-110`
- Exclude `hash` field, sort keys alphabetically, compute SHA256
- Update `/root/VAULT999/seal_chain_head.json` with new seq + hash
- Reference: `/root/arifOS/docs/CANONICALIZER-VAULT999-2026-07-19.md`

## Output to sovereign (≤10 lines)

```
SESSION SEALED | Seal-A: OPEN|CLOSED | T3a: …
Done: …
Open next: …
Receipt: path
Next prompt: path
```

## Forbidden

- Terminal dumps  
- Fake GREEN from fast spine  
- "All remaining tasks done" when SE/T3a/stage still open  
- SE stage hand-bump  

