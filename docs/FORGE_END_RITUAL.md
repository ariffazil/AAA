# ⚒️ FORGE END — Autonomous Session Seal Ritual

> **ATLAS333 Cognitive Geometry:** Completion → Contour → Seal
> **DITEMPA BUKAN DIBERI** — Every session ends by forging its seal.
> **Every agent on af-forge runs this at session end. No exceptions.**

---

## The Ritual (6 Steps)

```
STEP 1: 📦 Check repos     → stash dirty state, prevent drift
STEP 2: 📝 Build summary   → load /tmp/forge_session_summary.txt
STEP 3: 🔐 Seal to VAULT999 → write immutable record
STEP 4: 🧊 Update cooling   → append to gate_fire.jsonl
STEP 5: 🔍 RSI bottleneck   → record what was learned
STEP 6: 🧹 Clean workspace  → rm -rf /tmp/opencode/*
```

## Usage

```bash
# At end of every session:
export ARIFOS_SESSION_ID="SEAL-xxx"
export ARIFOS_ACTOR="ARIF"
echo "What was done this session" > /tmp/forge_session_summary.txt
forge-end
```

Or from inside an agent:
```
1. Write session summary to /tmp/forge_session_summary.txt
2. Run: bash /usr/local/bin/forge-end
3. Report seal receipt to Arif
```

## What Gets Sealed

| Artifact | Location |
|---|---|
| Session record | VAULT999 via arifOS kernel |
| Cooling ledger | `/root/.local/share/arifos/gate_fire.jsonl` |
| Seal chain (fallback) | `/root/.local/share/arifos/vault999/seal_chain.jsonl` |

## Constitutional Floors

| Floor | Enforcement |
|---|---|
| **F1 AMANAH** | Dirty repos stashed, not destroyed |
| **F2 TRUTH** | Session summary written from facts, not fiction |
| **F4 CLARITY** | Temp files cleaned, ΔS ≤ 0 |
| **F11 AUDIT** | Every seal produces a receipt with timestamp + session + actor |
| **F13 SOVEREIGN** | Seal is immutable — Arif's chain grows |

## RSI Bottleneck (for future agents)

To record what was learned this session:
```bash
echo "Biggest bottleneck: <what slowed you down>" > /tmp/forge_rsi_bottleneck.txt
echo "Fix for next agent: <what would make this faster>" >> /tmp/forge_rsi_bottleneck.txt
```

This gets cleared by forge-end. But the seal record persists in VAULT999.

---

*Forged: 2026-07-16 · ATLAS333 · DITEMPA BUKAN DIBERI*
