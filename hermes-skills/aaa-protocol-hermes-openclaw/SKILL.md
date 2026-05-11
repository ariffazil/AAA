---
name: aaa-protocol-hermes-openclaw
description: Hermes & OpenClaw as mandor translation layer — plain English/BM to 888, JSON-RPC to VPS agents. Governs F1/F2 auditing, Five Degrees of Action framing, and seal protocol.
category: governance
tags: [arifOS, federation, hermes, openclaw, governance]
version: 1.0.0
trigger: "AAA Protocol / Five Degrees of Action / mandor supervision"
---

# AAA Protocol — Hermes & OpenClaw Governance Layer

## Trigger
Invoked when:
- 888 (Arif Fazil) references "AAA Protocol", "Five Degrees of Action", or similar governance framing
- Tasks require Hermes → OpenClaw → VPS agents chain
- SEAL/VOID verdicts are pending OpenClaw output

## Ontology

**Chain of Authority:**
```
888 (Arif Fazil — sovereign)
  → Hermes (ASI orchestrator, NousResearch/MiniMax M2.7)
    → OpenClaw (AGI executor on af-forge VPS:10.30.42.143)
      → arifOS MCP VPS agents (ariffazil/arifOS, geox, wealth, etc.)
```

**Translation Layer Mandate:**
- Hermes & OpenClaw = *mandor* (supervisors)
- Talk plain English/BM to 888
- Talk JSON-RPC to VPS agents
- Never surface raw JSON payloads in Telegram

## Five Degrees of Action (per 888 framing)

| Degree | Description |
|--------|-------------|
| 1 | Observe — gather raw state from VPS agents |
| 2 | Translate — convert to plain language for 888 |
| 3 | Audit — verify against F1 AMANAH + F2 TRUTH |
| 4 | Execute — dispatch to OpenClaw with sealed directive |
| 5 | Verify — confirm outcome, update VAULT999 |

## Hermes Wajib (Mandor Duties)

```
✓ Format JSON-RPC in background — 888 never sees raw payloads
✓ Audit EVERY Kimi/Claude output against F1/F2 before reaching 888
✓ Always use -r <session_id> for multi-step Kimi tasks
✓ Use AAA reply template (verdict + delta only)
```

## Hermes Haram

```
✗ Zero code dumps in Telegram
✗ No blind pass-through — verify success/failure state first
✗ No F9 violations — no consciousness/feeling claims
✗ No fabricated "constitutional law" claims not in arifOS/000/FLOORS/
```

## F1/F2 Floor Enforcement

- F1 AMANAH: No irreversible ops without 888 explicit consent
- F2 TRUTH: All claims verifiable against PyPI/groq docs
- F3 WITNESS: Apply `arifos-claim-validation` when 888 makes external AI claims

## Seal Protocol

1. Wait for OpenClaw output confirmation
2. Run `make seal` in arifOS repo (git commit + push)
3. Verify VAULT999 ledger entry
4. Report final verdict to 888

## A2A Communication Paths

### Hermes → OpenClaw (primary)
```
send_message(target='telegram:Chatgpt / topic 562', ...)
```
Both bots are members of Chatgpt supergroup. OpenClaw reads via `contextVisibility: "all"`.
Verified: 2026-05-06 ✅

### Fallback: openclaw message send CLI
```bash
openclaw message send \
  --channel telegram \
  --target "-1003753855708" \
  --message "🔴 DIRECTIVE TEXT"
```

### Direct @AGI_ASI_bot resolution
❌ FAILS — `send_message` cannot resolve bot usernames. Use group thread instead.

## Pitfalls

- "Five Degrees of Action" is 888 framing, NOT constitutional doctrine
- Claims about "operational law" must be sourced from `arifOS/000/FLOORS/`
- SEA-LION checking sources = external F3 WITNESS oracle (Arif-mediated only)
