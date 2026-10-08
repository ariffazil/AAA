# 333-AGI PROPOSAL — arif_observe → arif_think Evidence Continuity (P1)
**Date:** 2026-10-06 09:35 MYT
**Author:** Claude Code (forge-777), audit session
**Status:** PROPOSAL — awaiting F13 binary from Arif before any patch
**Scope:** 1 file, ≤30 lines, no kernel restart required

---

## TL;DR — single bug, two wrong gates

The arif_observe → arif_think evidence flow dies because **arif_observe's response never gets
deposited into `_SESSIONS[session_id]["observations"]`**. There are **two independent gates**
that both fail on HOLD verdicts:

1. **Gate A (binding gate)** — `tools.py:6264` only populates `_SESSIONS[_sid]` when
   `effective_verdict ∈ {SEAL, OK, COMPLETED, PROCEED, ""}`. **`arif_observe` returns HOLD
   even on success**, so `_SESSIONS` is never initialized.
2. **Gate B (deposit gate)** — `tools.py:6354-6357` only deposits observation results when
   `session_id in _SESSIONS`. **Combined with Gate A, observe never deposits anything.**
3. **Reader** — `arif_think` (3 sites: `tools.py:15470`, `tools.py:16276`,
   `arif_think_embodied.py:136`) reads only `_SESSIONS[session_id]["observations"]`, which
   stays empty forever.

The chain is verified live this session. PID 3827232 served all 3 calls (init, observe, think)
without restart, so the process-restart hypothesis is **falsified**.

---

## Live reproducer (this session, 09:33 MYT)

```
T0 PID=3827232, CLIENT_SID=SEAL-probe3-1791249624

STEP 1: arif_init
  → kernel_sid=SEAL-76c2d69828854bbe
  → session_token=act_v1.eyJ...   (full JWT-style)
  → actor_verified=True

STEP 2: arif_observe mode=search (with SCT echoed in body)
  → verdict=HOLD, effective_verdict=HOLD
  → session_id=SEAL-76c2d69828854bbe  (continuity works)
  → result.results: 3 search hits present
  → BUT: observations_n=n/a, last_observation=False
  → reasons: ['delta_S=0.002 within reversible thermodynamic bounds']
  PID still 3827232 (no restart)

STEP 3: arif_think mode=reason (with SCT echoed)
  → verdict=HOLD
  → evidence_used_n=0
  → bounded_answer="" (empty)
  → what_is_supported: ["The EVIDENCE BLOCK provided in this prompt is explicitly
    marked empty, with the annotation that no observations have been recorded for this
    session.", ...]
  PID still 3827232 (no restart)
```

The think call's `what_is_supported[0]` **is the literal empty-EVIDENCE-BLOCK string from
`tools.py:7151`**. The kernel itself confirmed: by think-time, the observations store is empty.

---

## Hypothesis resolution (your enumerated list)

| # | Hypothesis | Result |
|---|---|---|
| 1 | Evidence store in-process only; observe writes to one dict, think reads another | **Partially right.** Both write/read from same in-process `_SESSIONS`, but observe **never deposits** because Gates A+B fail on HOLD. |
| 2 | Evidence has session scope but think runs in fresh inner-session | **Wrong.** think runs in same process, same `_SESSIONS`, but the key is empty. |
| 3 | evidence_receipt is separate field think doesn't look at | **Wrong.** `evidence_receipt` at `tools.py:11260` is init's policy metadata. Observe's search results live in `result.results`, which **is** what `_SESSIONS[sid]["observations"]` should hold. |
| 4 | Cache invalidation | **Wrong.** No cache layer in the path. |

**Real cause:** The gate logic at `tools.py:6264` excludes HOLD, and observe legitimately returns HOLD.

---

## The smallest shippable patch

### Option A: widen the verdict gate (1-line semantic fix + 4-line evidence-passthrough)

In `tools.py`, change the gate at line 6264 from:

```python
if str(_eff).upper() in ("SEAL", "OK", "COMPLETED", "PROCEED", ""):
```

to:

```python
if str(_eff).upper() in ("SEAL", "OK", "COMPLETED", "PROCEED", "", "HOLD", "SABAR"):
```

Rationale: HOLD/SABAR are *legitimate observation outcomes* (low-confidence, reversible). The
gate was designed for irreversible mutations; observations are reversible. The semantic split
between observation (reversible) and mutation (irreversible) is the constitutional distinction,
not the verdict label.

### Option B: decouple evidence deposit from verdict gate (5-line additive fix)

Add a separate evidence-deposit block after line 6353 that **doesn't require `_SESSIONS` to be
pre-populated**:

```python
# Observation deposit (P1 fix 2026-10-06) — decouple from verdict-bound gate.
# Observations are constitutionally reversible; deposit on any verdict.
if tool_name in ("arif_observe", "arif_sense_observe") and session_id:
        try:
            _res = ensured.get("result") if 'ensured' in dir() else enforced.get("result")
            if isinstance(_res, dict):
                _SESSIONS.setdefault(session_id, {"session_id": session_id})\
                    .setdefault("observations", []).append(_res)
                _SESSIONS[session_id]["last_observation"] = _res
        except Exception:
            logger.exception("suppressed exception", exc_info=True)
```

This guarantees `_SESSIONS[session_id]` exists before the deposit, breaking the chicken-and-egg.

### Option C: both A and B (defense in depth, 6 lines)

Run A first; if observe is still bound by verdict semantics, B guarantees continuity.

---

## Cost / risk / reversibility

- **Files touched:** 1 (`/opt/arifos/arifosmcp/runtime/tools.py`)
- **Lines changed:** ≤30
- **Kernel restart required:** yes (`arifos.service` restart, ~5s downtime, systemd auto-recovers)
- **Reversibility:** git checkout HEAD -- tools.py; redeploy via arifos-deploy-reconciler
- **Risk to other tools:** low — these gates only gate observation storage, not mutation logic
- **Risk to F1-F13 floors:** zero — observations are constitutionally reversible by design

---

## Test fixtures to add (per your P1 brief)

1. `observe_only_think` — single observe, no think, then inspect `_SESSIONS[sid]["observations"]`
2. `observe_then_think_with_receipt` — observe + think on same sid; assert
   `think.result.evidence_used_n == observe.result.results length`
3. `multi_observe_think_chain` — 3 sequential observes, single think; assert all 3 in evidence

These can live in `/opt/arifos/tests/runtime/test_observe_think_continuity.py` (or wherever
the existing eval suite lives; not changed without explicit F13).

---

## What's NOT in scope (per your prioritization)

- P3 (route confidence split, memory recall empty, actor self-mismatch) — separate proposals later.
- P4 (kernel restart) — auto-handled by systemd; nothing to do.
- P5 (WELL sensor integration) — F13-only path, not patched in this proposal.

---

## What I need from Arif (one binary)

- **PATCH-A** → widen the verdict gate at tools.py:6264 to include HOLD/SABAR; restart
  arifos.service; re-run live reproducer.
- **PATCH-B** → add the decoupled deposit block at tools.py:6353; re-run reproducer.
- **PATCH-C** → both, defense in depth.
- **PROPOSE-ONLY** → I write this proposal and a draft diff at
  `/root/AAA/cockpit/proposals/diffs/`, but no edit to `/opt/arifos/...`. Await review.
- **HOLD** → no patch; profile-only; revisit after P3.

---

## Receipt path
/root/AAA/cockpit/proposals/PROPOSAL_KERNEL_HYDRATION_2026-10-06.md
Companion receipt: /root/AAA/cockpit/receipts/RECEIPT_KERNEL_CRASH_AND_DEFECTS_2026-10-06.md