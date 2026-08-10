---
name: openclaw-propose-seal
description: OpenClaw-native /propose-seal — proposes a sealed candidate to 888-APEX. NEVER self-seals. Pipeline: agent proposes → 888 judges → F13 authorizes → 999 executes (append to VAULT999).
tags: [constitutional, seal, propose, substrate-primitive, telegram-native, openclaw]
license: MIT
capability_tier: fed-agent-subagent
ecology_state: WARM
---
# OpenClaw /propose-seal — Substrate Primitive

When a user types `/propose-seal <description>` to the OpenClaw bot, OpenClaw compiles evidence and submits the candidate to 888-APEX for constitutional verdict.

**OpenClaw NEVER self-seals.** All sealing routes through 888-APEX.

## Output format

```
SEAL REQUEST ROUTED
────────────────────────────────────
Request:      <description of what is being sealed>
Proposer:     OpenClaw (333 THINK + 444 ORCHESTRATE)
Session:      <session_id>
Actor:        ariffazil (F13 SOVEREIGN)
────────────────────────────────────
Evidence compiled:
  1. SHA-256: <hash>  path: <file>
  2. Git ref: <commit>
  3. Live probe: <:PORT/health output>
  4. Epistemic tag: OBS | DER | INT | SPEC
  5. Ω₀ stated: <value>
────────────────────────────────────
Constitutional check (auto):
  F1  AMANAH      ✅
  F2  TRUTH       ✅
  F4  CLARITY     ✅
  F7  HUMILITY    ✅
  F11 AUDIT       ✅
  F13 SOVEREIGN   ⚠️ Awaits verdict
────────────────────────────────────
→ Routing to 888-APEX for constitutional verdict
→ 999-VAULT999 will record decision
→ Poll: /seal-status <request_id>

DITEMPA BUKAN DIBERI 🔥
```

## Evidence requirements (F2 TRUTH)

Before /propose-seal can be routed, these must be present:

| Evidence | Required | Check |
|---|---|---|
| SHA-256 of work product | ✅ | `sha256sum <file>` |
| Git commit reference | ✅ | `git log --oneline -1` |
| At least 1 live probe result | ✅ | `curl :PORT/health` or equivalent |
| Epistemic label (OBS/DER) | ✅ | Embedded in evidence chain |
| Ω₀ stated | ✅ | "Ω₀ = 0.XX" in request |

Without all 5, the proposal is **INADMISSIBLE-QQQ-INCOMPLETE**.

## Pipeline

```
/propose-seal <description>
   ↓
OpenClaw compiles evidence (auto-detect recent files, git refs, live probes)
   ↓
OpenClaw submits via `apex-judge --actor OPENCLAW` (or arif_init→arif_judge MCP).
   Never free-text "888-APEX JUDGMENT". Quote effective_verdict + call_hash.
   ↓
Kernel arif_judge returns SEAL | HOLD | VOID | SABAR
   ↓
If SEAL → OpenClaw appends correction receipt to VAULT999 via forge_vault(mode="receipt")
   ↓
OpenClaw replies with verdict receipt
```

## Verdict responses

| Verdict | What OpenClaw sees |
|---|---|
| **SEAL** | `✅ SEALED — {receipt_hash} added to VAULT999` |
| **SEAL-CONDITIONAL** | `⚠️ CONDITIONAL — {gaps} must resolve before final seal` |
| **HOLD** | `🛑 HOLD — {reason}, placed in open_loops_888_HOLD` |
| **VOID** | `❌ VOID — {reason}, work not sealed` |
| **SABAR** | `⏳ SABAR — {reason}, wait for next cycle` |

## Doctrine

- /propose-seal is the ONLY way an agent submits to VAULT999 via 888-APEX
- /seal is BLOCKED — no self-sealing
- 999 is witness, not authority — runs ONLY after 888 verdict
- F13 (Arif) is the final authority for T3 irreversible sealing

## ZEN

```
/propose-seal answers:  CAN THIS BE SEALED?
         → OpenClaw compiles evidence
         → 888 judges
         → 999 witnesses (if SEAL)

OpenClaw is the courier. Not the judge. Not the witness.
```