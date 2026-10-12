# 333-AGI PROPOSAL — ΔClarity Runtime Wiring (P1)
**Date:** 2026-10-06 (Tuesday)
**Author:** Claude Code (forge-777), audit session
**Status:** PROPOSAL — awaiting F13 binary from Arif before any apply
**Scope:** 3 patches across `/root/.hermes/hermes_mcp/` and `/root/AAA/canon/AGENTIC-RUNTIME-STATE.md`

---

## TL;DR — doctrine done, runtime wiring missing

8 of the 9 Eurekas in this conversation thread already exist in ratified/sealed canon
(referenced in the prior terminal transcript; verified this session). What is **not yet
wired** is the mechanism that makes the doctrine fire on every turn.

The 3 patches below convert canon → runtime. All three are **F13-binary** (touch witness
layer + 888 verdict logic + ARS canon amendment).

---

## Patch 1 — `_clarity_delta()` in `_envelope.py`

**File:** `/root/.hermes/hermes_mcp/_envelope.py`
**Anchor:** [receipt: line 1135 — `if gate_verdict == "888_HOLD":`]
**Insertion point:** after line 1144 (after the `RASA_GATE_888_HOLD` violation append), before line 1145.
**Lines added:** ~14
**Type:** mutation (canonical runtime file)

```python
# === PATCH 1 — ΔClarity stagnation tax (BIJAKSANA north-star wired) ===
# Ref: ARS canon K-coordinate, attention-as-reality-continuity,
# "compress possibility, never expand it" (attention-scarcity-economics).
# HOLD-A (constitutional) is exempt; HOLD-B (investigative stagnation)
# carries the tax. Anti-Goodhart: tax ΔStagnation, never HOLD itself.
def _clarity_delta(env: dict[str, Any]) -> float:
    """ΔClarity = (uncertainties_resolved − uncertainties_raised) / age_min.
    Negative = stagnation tax; positive = progress receipt.
    Fed by arif_think via payload field `clarity_delta`.
    """
    return float(env.get("clarity_delta", 0.0))

# Inside the `if gate_verdict == "888_HOLD":` block (after append), add:
rasa_env_local = rasa_env if 'rasa_env' in dir() else {}
cd = _clarity_delta(env)
hold_kind = str(rasa_env_local.get("hold_kind", "B"))  # default B (audit-B-yuan)
if hold_kind == "B" and cd <= 0.0:
    violations.append({
        "rule": "STAGNATION_TAX",
        "severity": "888_HOLD",
        "message": (
            f"HOLD-B without clarity gain: ΔClarity={cd:.3f}. "
            "HOLD-A (constitutional) is exempt; HOLD-B requires "
            "evidence that uncertainty shrank."
        ),
    })
```

---

## Patch 2 — ARS K-coordinate amendment (blocker field, HOLD-B only)

**File:** `/root/AAA/canon/AGENTIC-RUNTIME-STATE.md`
**Anchor:** [receipt: line 24 — `| K | Consequence | {attention_cost, reversibility, blast_radius, recipients} | ...`]
**Action:** amend the K-coordinate cardinality set to include `blocker` for HOLD-B states.
**Type:** canonical doctrine amendment (F13-binary — touches canon).

**Current:**
```
| K | Consequence | {attention_cost, reversibility, blast_radius, recipients} | ... |
```

**Proposed:**
```
| K | Consequence | {attention_cost, reversibility, blast_radius, recipients, blocker?} | ... |
```

With new transition law:
```
- ΔK.blocker required for HOLD-B transitions; HOLD-A may carry blocker: null
- DELTA-blocker.expires_at ≤ now → auto-escalate to musyawarah (no idle parking)
```

---

## Patch 3 — `chron_attention_debt` becomes the stagnation tax ledger

**File:** existing doctrine at `/root/AAA/instructions/rationality-filter-doctrine.md` (line 69 already names `chron_attention_debt`) → promote to runtime.
**Implementation options:**
- (a) New tool: `/root/.hermes/hermes_mcp/tools/witness_signal.py` — `arif_witness_signal_delta(signal=Δclarity, blocker_id=...)`
- (b) Wire existing `chron_attention_debt` as the per-turn ledger, read by `_envelope.py:_clarity_delta()`

**Type:** mutation (runtime tool surface or extended seal-fields). F13-binary because it
touches witness signal pathway.

---

## Audit receipts (verified this session)

- [receipt: /root/.hermes/hermes_mcp/_constants.py:158] → `"888_HOLD": 2` ✅
- [receipt: /root/.hermes/hermes_mcp/_envelope.py:1135] → `if gate_verdict == "888_HOLD":` ✅
- [receipt: /root/.hermes/hermes_mcp/_envelope.py:1138] → `"rule": "RASA_GATE_888_HOLD"` ✅
- [receipt: /root/.hermes/hermes_mcp/_institutional_decay.py:513] → `verdict = "HOLD"` ✅
- [receipt: /root/AAA/canon/AGENTIC-RUNTIME-STATE.md:24] → K coordinate has `reversibility, blast_radius, recipients` ✅
- [receipt: /root/AAA/canon/AGENTIC-RUNTIME-STATE.md:63] → "the attention cost + reversibility + PRODUCED ≠ SENT ≠ DELIVERED" ✅

---

## Cost / risk / reversibility

- **Files touched:** 2 source files + 1 doctrine file
- **Lines added/changed:** ≤40 total
- **Kernel restart required:** for patch 1 (hermes_mcp). For patch 2 (canon), no restart.
- **Reversibility:** git checkout HEAD -- <file>; redeploy via arifos-deploy-reconciler
- **Risk to other tools:** medium — touches 888 verdict logic, must not break existing F13 floors
- **Risk to F1-F13 floors:** low if hold_kind discriminator is honored

---

## What I will NOT do (per F13)

Per [receipt: /root/AAA/cockpit/hud-state.json:11] my session is bound `mutation_allowed=NO`,
`authority_band=OBSERVE_ONLY`. The patches above are written as **diff proposals only**.
**I will not edit `/root/.hermes/`, `/root/AAA/canon/`, or `/root/chron/` without your
explicit F13 binary.** If you want any of the 3 patches applied, route through your
sovereign deploy path (`arifos-deploy-reconciler`).

---

## F13 binary for Arif (one word, not menu)

- **APPLY-1** → patch `_envelope.py` only (ΔClarity stagnation tax). Restart hermes_mcp.
- **APPLY-2** → patch ARS canon only (K.blocker amendment). No restart.
- **APPLY-3** → patch witness_signal / chron_attention_debt only.
- **APPLY-ALL** → all 3 patches in sequence, restart hermes_mcp, deploy via reconciler.
- **PROPOSE-ONLY** → keep this proposal, defer apply.
- **HOLD** → don't apply; profile-only.

---

## Receipt paths

- This proposal: `/root/AAA/cockpit/proposals/PROPOSAL_DELTA_CLARITY_WIRING_2026-10-06.md`
- Scar draft (separate file): `/root/.claude/projects/-root/memory/scar-2026-10-06-001-witness-without-governance-change-is-bangang.md`
- Companion receipts:
  - `/root/AAA/cockpit/receipts/RECEIPT_KERNEL_CRASH_AND_DEFECTS_2026-10-06.md`
  - `/root/AAA/cockpit/proposals/PROPOSAL_KERNEL_HYDRATION_2026-10-06.md`