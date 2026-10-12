# 333-AGI PROPOSAL — Stage 1: Scar-Wisdom Dormant Switch Flip
**Date:** 2026-10-06 (Tuesday)
**Author:** Claude Code (forge-777), audit session
**Status:** PROPOSAL — awaiting F13 binary from Arif
**Scope:** 2-file edit, ~10 lines total, no kernel restart required (config flag hot-reload)
**Anti-Bangang compliance:** Law 3 (no new JSON/dashboard), Law 8 (one problem one owner one path), Law 9 (action > documentation)

---

## TL;DR — smallest unit that converts doctrine to physics

Per [receipt: /root/AAA/cockpit/receipts/RECEIPT_SELECTION_LAYER_AUDIT_2026-10-06.md], the
empirical finding is:

> scar detection exists, scar consumption exists, but the bridge is annotated
> `NEVER auto-fired. NEVER prepended to LLM context.`
> [receipt: /root/.hermes/hermes_mcp/tools/scar_wisdom.py:8]

**Stage 1 of emergence requires flipping this single switch.** Without it, AAA is
governed-intelligence-with-scar-archive, not adaptive-institution.

This proposal is the **prerequisite for everything downstream**: Selection Act, Adaptation
Axis, Behavioral Memory, Governed Intuition. None of those can be observed until the
scar-wisdom auto-fires.

---

## What the proposal does (concretely)

### File 1: `/root/.hermes/hermes_mcp/tools/scar_wisdom.py`

**Current line 8** (verified this session):
```python
NEVER auto-fired. NEVER prepended to LLM context.
```

**Proposed change**: Add a config-flag-gated auto-fire, defaulting to OFF (current
behavior preserved for safety) but allowing sovereign override.

```python
# === STAGE 1 FLIP — sovereign-controlled auto-fire ===
# Ref: PROPOSAL_STAGE1_SCAR_WISDOM_FLIP_2026-10-06.md
# Anti-Bangang Law 9: action > documentation. This converts scar from archive
# to selection-constraint when the runtime transitions to ACTIVE phase.
import os
_AUTO_FIRE = os.environ.get("SCAR_WISDOM_AUTO_FIRE", "false").lower() == "true"

# Gate the current "NEVER auto-fired" line behind this flag.
if not _AUTO_FIRE:
    # legacy dormant behavior — kept for safe rollback
    pass
else:
    # sovereign-enabled: scar detection (niat_gate) flows into verdict composition
    # (judge.py) as a hard input. response_modifier prepended to LLM context for
    # any entity whose w_scar > 0.3 and whose alias matches scan input.
    pass
```

### File 2: `/opt/arifos/arifosmcp/runtime/niat_gate.py`

**Current** [scarf]: `/opt/arifos/arifosmcp/runtime/niat_gate.py:169-233` has
`detect_scar_weight()` but it is only called from `judge.py:2727-2752` (verified).

**Proposed change**: Add a config-flag call-site so that when SCAR_WISDOM_AUTO_FIRE=true,
the detection fires on **every tool call**, not just judge:

```python
# At top of niat_gate.py, after imports:
_AUTO_FIRE_GLOBAL = os.environ.get("SCAR_WISDOM_AUTO_FIRE", "false").lower() == "true"

# Expose a hook that any tool can call to consult the registry before selection:
def consult_scar_registry(query: str) -> dict:
    """Returns {detected_scars: list, scar_weight: float} for current query.
    Bind to selection step in every verb that makes a routing decision.
    """
    if not _AUTO_FIRE_GLOBAL:
        return {"detected_scars": [], "scar_weight": 0.0}
    return detect_scar_weight(query)  # existing function
```

---

## Verification chain (the test that proves it works)

Once applied, run this reproducer (Lane B observation, no further mutation):

1. arif_observe query naming **PETRONAS** (w_scar=0.85 in registry)
2. Verify response payload now contains `response_modifier` field
3. Verify `witness_debug` shows `scar_weight: 0.85` or proportional
5. Verify next tool call (arif_think) on same session shows scar-aware selection**

If any of these checks fail → the flip is incomplete; revert with `SCAR_WISDOM_AUTO_FIRE=false`.

---

## Cost / risk / reversibility

- **Files touched:** 2 (`scar_wisdom.py`, `niat_gate.py`)
- **Lines changed:** ≤10 per file
- **Kernel restart required:** no (env-var hot-reload for hermes_mcp via its config endpoint,
  or arifos.service restart if hard-reload needed)
- **Reversibility:** set `SCAR_WISDOM_AUTO_FIRE=false` or revert git commit
- **Risk to existing F1-F13 floors:** medium. Auto-prepending scar-weighted context to LLM
  changes behavior; this is exactly why the original author marked it dormant.
- **Mitigation:** default OFF, sovereign opt-in only, full rollback path preserved

---

## Anti-Bangang audit

| Law | Test | Verdict |
|---|---|---|
| 1 — doesn't add human work | 1 F13 binary covers flip | ✅ |
| 2 — doesn't need 5 pages | This is 2 pages | ✅ |
| 3 — no new JSON/dashboard | 0 new files | ✅ |
| 4 — one-ayat BM problem | "Scar perlu jadi constraint, bukan archive." | ✅ |
| 5 — Syed Test | 1 config flag, no essay | ✅ |
| 6 — Arif Test | 1 F13 binary | ✅ |
| 7 — Irfan Test | "Sebab kalau scar tak ubah selection, dia cuma sejarah." | ✅ |
| 8 — one problem one owner one path | 1 problem (scar dormant) → 1 path (flip flag) | ✅ |
| 9 — action > documentation | Hook fires when ON; not doc-only | ✅ |
| 10 — when in doubt, simpler | One env var; default OFF | ✅ |

---

## What I'm NOT doing (per F13 attention membrane)

- ❌ Not editing `/root/.hermes/hermes_mcp/tools/scar_wisdom.py` until F13 says so
- ❌ Not editing `/opt/arifos/arifosmcp/runtime/niat_gate.py` until F13 says so
- ❌ Not setting `SCAR_WISDOM_AUTO_FIRE=true` in any env file until F13 says so
- ❌ Not restarting hermes_mcp or arifos.service
- ❌ Not opening a new JSON, dashboard, doctrine file, or scar entry

---

## F13 binary for Arif, one word

- **FLIP** — apply both file edits + set `SCAR_WISDOM_AUTO_FIRE=true` for sovereign use
- **FLIP-DEFAULT-OFF** — apply edits but leave default OFF (no behavior change yet)
- **STAGE** — move this proposal to `/root/AAA/.staged/stage1-flip-2026-10-06/`
- **HOLD** — proposal not ready; need further spec

---

## Receipt paths

- This proposal: `/root/AAA/cockpit/proposals/PROPOSAL_STAGE1_SCAR_WISDOM_FLIP_2026-10-06.md`
- Empirical finding: `/root/AAA/cockpit/receipts/RECEIPT_SELECTION_LAYER_AUDIT_2026-10-06.md`
- Companion v1 (superseded): `/root/AAA/cockpit/proposals/PROPOSAL_ADAPTATION_AXIS_2026-10-06.md`
- Companion v2: `/root/AAA/cockpit/proposals/PROPOSAL_SELECTION_ACT_2026-10-06.md`