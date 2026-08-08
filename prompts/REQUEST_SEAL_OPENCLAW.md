# OpenClaw — /request-seal
# Canonical: AAA/prompts/REQUEST_SEAL_OPENCLAW.md
# Status: DRAFT — awaiting F13 sovereign seal
# Forged: 2026-08-08 by Hermes ASI under Atlas v1 doctrine

---

## Why /request-seal (not /seal)

```
888 JUDGES
999 WITNESSES
OpenClaw PROPOSES

The correct form is:
  OpenClaw → /request-seal → 888-APEX → verdict → 999-VAULT999

Not:
  OpenClaw → /seal → ??? (no constitutional basis)
```

## What /request-seal Does

Routes a sealed-proposal from OpenClaw to the authority chain:
1. Captures evidence and proposal
2. Routes to 888-APEX for constitutional verdict
3. If SEAL → appended to VAULT999
4. If HOLD → logged in open_loops_888_HOLD
5. If VOID → rejected, reason logged

## Output Format

```
SEAL REQUEST ROUTED
────────────────────────────────────
Request:      <description of what is being sealed>
Proposer:     OpenClaw
Slot:         333 THINK + 444 ORCHESTRATE
Lane:         555-ASI (Ω CORE)
Session:      <session_id>
Actor:        ariffazil (F13 SOVEREIGN)
────────────────────────────────────
Evidence:
  1. <link/path/hash of evidence 1>
  2. <link/path/hash of evidence 2>
  N. ...
────────────────────────────────────
Constitutional Check:
  F1  AMANAH      ✅ (reversible path exists)
  F2  TRUTH       ✅ (OBS/DER labels present)
  F4  CLARITY     ✅ (ΔS ≤ 0)
  F7  HUMILITY    ✅ (Ω₀ = 0.XX, stated)
  F11 AUDIT       ✅ (trail complete)
  F13 SOVEREIGN   ⚠️ (Awaits verdict)
────────────────────────────────────
→ Routing to 888-APEX for constitutional verdict
→ 999-VAULT999 will record decision
→ Poll status: /seal-status <request_id>

DITEMPA BUKAN DIBERI 🔥
```

## What Happens After Routing

| Verdict | What OpenClaw Sees |
|---|---|
| **SEAL** | `✅ SEALED — {receipt_hash} added to VAULT999` |
| **SEAL-CONDITIONAL** | `⚠️ CONDITIONAL — {gaps} must resolve before final seal` |
| **HOLD** | `🛑 HOLD — {reason}, placed in open_loops_888_HOLD` |
| **VOID** | `❌ VOID — {reason}, work not sealed` |
| **SABAR** | `⏳ SABAR — {reason}, wait for next cycle` |

## Evidence Requirements (F2 TRUTH)

Before /request-seal can be routed, these must be present:

| Evidence | Required | Check |
|---|---|---|
| SHA-256 of work product | ✅ | `sha256sum <file>` |
| Git commit reference | ✅ | `git log --oneline -1` |
| At least 1 live probe result | ✅ | `curl :PORT/health` or equivalent |
| Epistemic label (OBS/DER) | ✅ | Embedded in evidence chain |
| Ω₀ stated | ✅ | "Ω₀ = 0.XX" in request |

Without all5, the proposal is **INADMISSIBLE-QQQ-INCOMPLETE**.

---

*Forged 2026-08-08. DITEMPA BUKAN DIBERI 🔥*