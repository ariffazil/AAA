# PROBE::P0-1_DUAL_TRUTH_DEFECT — POSITION FILE

**Date:** 2026-09-21T21:10Z
**Author:** 333-AGI Δ MIND (read-only probe)
**Membrane status:** REVERSIBLE — `rm /root/AAA/eurekas/probes-2026-09-21/P0-1_dual_truth_defect_position.md`
**F13 status:** HOLD — mechanical enforcement pending Arif ratification

---

## 1. DEFECT CLAIM (from EUREKA-NAMING-CREATION-2026-09-21)

> **mutation_allowed=true ∧ session_state=OBSERVE_ONLY in the same response. Dual-truth violation.**
> **Hard-rule:** when session_state is OBSERVE_ONLY, mutation_allowed MUST be false. Make this mechanically enforced, not informational.

---

## 2. PATH-OF-EVIDENCE

### The dual-truth site (CONFIRMED REAL)

**File:** `/root/arifOS/arifosmcp/server.py`
**Function:** `kernel_identity_verify` (decorator at line 3801)
**Critical lines:** **3911–3912**

```python
# Line 3908
actor_class = "SOVEREIGN_VERIFIED" if verified else "UNVERIFIED"
# Constitutional boundary: SOVEREIGN authority_band ≠ agent becomes F13 human.
# Session may hold SOVEREIGN *band* when Arif's key signed the actor claim.

# Lines 3911-3912 — THE DEFECT SITE
mutation_allowed = bool(verified)         # ← only depends on signature
seal_allowed   = bool(verified)           # ← only depends on signature
```

**Diagnosis:** The two fields depend **only on `verified`** — the Ed25519 signature check. There is **no consultation of `session_state`** (which is set elsewhere in the session lifecycle). This means:

- A caller who submits a valid signature but is operating inside an OBSERVE_ONLY session can receive `mutation_allowed: True` in the response, while the underlying session remains OBSERVE_ONLY.
- This is exactly the dual-truth defect: `mutation_allowed` says "yes you can mutate", but `session_state` says "this session can only observe".

### Cross-reference (RECEIPTS — NOT YET VERIFIED LIVE)

From the EUREKA prompt: *"today's arif_init returned mutation_allowed:true while session_notice.session_state: OBSERVE_ONLY"*.

**Verification status:** I have not re-run `arif_init` in this session. The defect site at lines 3911-3912 is structural — independent of whether a particular call happened to demonstrate it. **The defect is real at code level.**

---

## 3. THE MECHANICAL FIX (proposed, NOT applied)

### Option A — Localized cross-check (least invasive)

Add a session_state consultation at line 3911-3912:

```python
# Fetch current session_state
session_state = sess.get("session_state", "ACTIVE") if sess else "ACTIVE"

# Hard rule: OBSERVE_ONLY ∧ any session_state that forbids mutation ⇒ mutation_allowed=false
if session_state in ("OBSERVE_ONLY", "FROZEN", "RETIRED"):
    mutation_allowed = False
    seal_allowed = False
else:
    mutation_allowed = bool(verified)
    seal_allowed = bool(verified)
```

### Option B — Centralize the rule (preferred — single source of truth)

Create a single function:

```python
def compute_mutation_allowed(verified: bool, session_state: str) -> bool:
    """F13-blessed single source of truth. Hard rule:
    OBSERVE_ONLY ⇒ False, regardless of signature."""
    if session_state in ("OBSERVE_ONLY", "FROZEN", "RETIRED"):
        return False
    return bool(verified)
```

Then call this from **every** site that currently does `mutation_allowed = bool(verified)`. Sites found via `grep "mutation_allowed" /root/arifOS/arifosmcp/`:

- `/root/arifOS/arifosmcp/router.py:91, 708, 727, 741, 764, 769, 791, 798, 841`
- `/root/arifOS/arifosmcp/server.py:3809, 3843, 3911, 3922`
- `/root/arifOS/arifosmcp/runtime/governance_identity.py:625, 647, 671, 681, 692`

(Approx **20 sites** to refactor.)

---

## 4. RISK & REVERSIBILITY

| Aspect | Status |
|---|---|
| Reversibility | **Fully reversible** — Option A is a 4-line addition; Option B is a refactor |
| Side effects | None in option A; option B may change behavior of other 19 sites if their `session_state` is unexpectedly restrictive |
| F13-bound | **YES** — touching `mutation_allowed` is touching the authority spine |
| Surface impact | None (no public-facing API change) |

**Recommendation:** Option B (centralized rule) — applied per-site via musyawarah before F13 ratification.

---

## 5. NEXT STEP (awaiting Arif)

Per membrane doctrine, ONE binary choice:

> **(a)** Apply Option A locally at server.py:3911 — minimal, reversible, fast.
> **(b)** Apply Option B centrally — stronger, slower, requires musyawarah across 20 sites.
> **(c)** Hold for further evidence — re-run arif_init to capture a live dual-truth response.

The probe itself is complete; the decision is sovereign.
