<!--
SOT-MANIFEST
owner: Arif
last_verified: 2026-05-19
valid_from: 2026-05-19
valid_until: 2026-06-19
confidence: high
scope: /root/.openclaw/workspace
epistemic_status: CLAIM
-->

# Sovereign Interface v0 — Command Reference

**Status:** `SI v0` | **Effective:** 2026-05-19

This document lists the **operational commands** that agents and Arif use to interact with the 888_HOLD system and the A2A bridge.

---

## Agent → Arif (Notification)

When an agent creates an 888_HOLD:

```
🛑 888_HOLD #<id>
Request: <short description>
Reason: <why it was held>
File: AAA_HOLDS.md
Action required: /approve <id> or /reject <id>
```

## Arif → Agent (Decision)

Via Telegram or direct file edit:

| Command | Effect |
|---------|--------|
| `/holds` | List all active holds |
| `/approve <id>` | Approve hold `<id>`, agent executes on next read |
| `/reject <id>` | Reject hold `<id>`, agent discards |
| `/status` | Show federation health (G, ΔS, Ψ) |
| `/memory` | Query Ω-MEMORY L5 (when active) |

## Agent Internal (Auto)

| Trigger | Action |
|---------|--------|
| Task completion | Write observation to Ω-MEMORY L5 (when active) |
| Wake cycle | Read `AAA_HOLDS.md`, process approved/rejected holds |
| 6h cron | Run Insight Engine (when active) |
| Error / anomaly | Write 888_HOLD, notify Arif |

---

*Commands are forged in use. This list grows with operational need.*
