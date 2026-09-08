# Musyawawah Runtime Gate — Kernel Integration Proposal (Path B1)

> **Status:** Path B1 — proposal awaiting F13 governance review (B2)
> **Date:** 2026-09-08
> **Author:** FI-003 under F13 APEX Verdict (DUAL_GO → SEAL)
> **Path:** A (complete) → B1 (this proposal) → B2 (governance review) → B3 (runtime)
> **DITEMPA BUKAN DIBERI**

## 0. Origin pathway

Per F13's `scar-science-origin-pathway`:
```
Human → Consequence → Institution → System → Code
```

This proposal starts with **Consequence**, not Code.

## 1. Consequence (why this matters)

**Observed:** T2/T3 mutations in arifFlow ledger lack `payload.musyawawah_reference` field. 7+ post-grace violations detected (per Phase 2 sentinel). The musyawawah deliberation law has fired exactly ONCE (at its own birth, 2026-08-11) in 28+ days.

**Risk:** A T2/T3 mutation (irreversible or blast-radius-bearing) commits without the deliberation law ever running. The federation constitutional floor (F2 Truth, F11 Audit) is satisfied mechanically but **deliberately bypassed**.

**Failure mode:** Purpose dies but everything still works. (F13's question from `scar-science-origin-pathway`.)

## 2. Institutional layer (which doctrine serves)

| Doctrine | Citation | Service |
|---|---|---|
| Musyawawah law | `/root/AAA/instructions/musyawawah.md` §1 §6 | T2/T3 mutations require deliberation |
| Gate Promotion | `/root/AAA/instructions/gate-promotion.md` | OBSERVE_ONLY → GATE tier |
| F2 TRUTH | arifOS constitution | Verifiable claims required |
| F11 AUDIT | arifOS constitution | All actions witnessed |
| F13 SOVEREIGN | arifOS constitution | Sovereign override preserved |

## 3. System boundary (where the change lands)

**Kernel chokepoint:** `/root/arifOS/arifosmcp/runtime/pre_execution_gate.py`

**Insertion point:** Line ~589 (after ART computes `act_req`, before ACT processes at line 606).

**Rationale:** ART 2.0 has already classified the action's risk profile. Musyawawah check fires on the classified action. If ACT would otherwise PROCEED, musyawawah is the last constitutional filter.

**NOT inserted before ART (line ~280):** ART needs full action context to compute blast_radius, trust_level, etc. Pre-ART check would have less information.

**NOT inserted after ACT (line ~613):** ACT has already made its verdict. Musyawawah as a post-hoc check would be too late for T2/T3 actions where ACT says PROCEED.

## 4. Code change (minimal)

### 4.1 New module

Reuse existing reference implementation at `/root/AAA/scripts/musyawawah_runtime_gate.py`. For Path B, symlink to arifOS importable path:

```
/root/AAA/scripts/musyawawah_runtime_gate.py
  → /root/arifOS/arifosmcp/runtime/musyawawah_runtime_gate.py (symlink, AAA SOT)
```

(Per `feedback/systemd-protecthome-blocks-root-symlink`: ensure kernel module can read the symlink target. `/root/AAA/` is readable to root processes — kernel runs as root.)

### 4.2 pre_execution_gate.py change

Add between ART (line ~589) and ACT (line 606):

```python
# ── MUSYAWARAH NO-GATE (E-3 Path B, F13-ratified 2026-09-08) ──
# Per docs: specs/musyawawah_kernel_integration_proposal.md
# Reversibility: MUSYAWARAH_BYPASS_KERNEL=1 env disables (fail-open sentinel)
import os
if os.environ.get("MUSYAWARAH_BYPASS_KERNEL", "0") != "1":
    _musyawawah_action_class = art_req.action_class  # set by ART
    if _musyawawah_action_class in ("EXECUTE_HIGH_IMPACT", "SEAL"):
        try:
            from arifosmcp.runtime.musyawawah_runtime_gate import (
                check_with_log, InvocationContext as _MusCtx,
                ActionClass as _MusAC, Verdict as _MusV,
            )
            _payload = envelope.kernel.payload if hasattr(envelope, "kernel") and envelope.kernel else {}
            _musyawawah_ref = getattr(_payload, "musyawawah_reference", None) if _payload else None
            _ack_override = getattr(_payload, "ack_irreversible", False) if _payload else False
            _ctx = _MusCtx(
                action_class=_MusAC(_musyawawah_action_class),
                musyawawah_reference=_musyawawah_ref,
                ack_irreversible=_ack_override,
                tool_name=manifest_entry.tool_name if manifest_entry else None,
            )
            _verdict, _reason = check_with_log(_ctx)
            if _verdict == _MusV.DENY:
                logger.warning(f"MUSYAWARAH GATE DENY: {_reason}")
                return GateResult(
                    verdict=GateVerdict.HOLD,
                    reasons=[f"MUSYAWARAH GATE: {_reason}"],
                )
            elif _verdict == _MusV.ALLOW_BYPASS:
                logger.warning(f"MUSYAWARAH GATE BYPASS (F13): {_reason}")
        except ImportError:
            pass  # Reference impl not importable — fall open per gate-promotion doctrine (sentinel still runs)
```

### 4.3 Path B integration tests (separate from reference tests)

Re-run the 12-scenario falsification suite against the kernel-level integration (not just the standalone reference). Add to arifOS test suite.

## 5. Reversibility

| Env var | Effect |
|---|---|
| `MUSYAWARAH_BYPASS_KERNEL=1` | Kernel check disabled (fail-open). Sentinel (Phase 2) continues to log. |
| unset | Default behavior — musyawawah check active. |

**Rollback procedure:**
1. Set `MUSYAWARAH_BYPASS_KERNEL=1` in kernel systemd unit
2. Restart `arifos.service`
3. Verify sentinel still emits BLOCK lines
4. Plan re-instatement with F13 ratification

## 6. Backward compatibility (the migration problem)

**Current state:** 35K+ arifFlow receipts lack `musyawawah_reference`. Phase 2 sentinel flags 7+ post-grace violations. Once kernel enforcement activates, ALL of these would be DENIED.

**Migration options:**

| Option | Duration | Reversibility |
|---|---|---|
| A — 7-day grace period (no DENY during grace) | 7 days | Easy revert |
| B — Whitelist legacy receipts (by receipt_id range) | Permanent | Manual |
| C — Auto-promote legacy receipts (backfill `musyawawah_reference`) | Permanent | One-time |

**Recommendation: A.** 7-day grace matches the gate-promotion doctrine's "reversible via named rollback" criterion. After grace, kernel enforces strictly.

## 7. Performance impact (estimate, not measured)

| Component | Estimated overhead |
|---|---|
| Regex match | <1ms |
| Dataclass instantiation | <1ms |
| Reference import (cached after first call) | <1ms (one-time) |
| Total per-call overhead | ~1-2ms |

**Acceptable** for T2/T3 actions (which are infrequent). T0/T1 (baseline) is unaffected.

## 8. Risk matrix

| Risk | Severity | Mitigation |
|---|---|---|
| Existing T2/T3 actions denied | HIGH | 7-day grace period |
| VAULT999 lookup unavailable | MEDIUM | Sentinel continues; kernel fails open (per gate-promotion doctrine, fail-open for observation) |
| Performance regression | LOW | <2ms per call acceptable |
| Unicode lookalike in path | LOW | F5 finding — canonicalize spelling first |
| Reference implementation drift | MEDIUM | Symlink ensures AAA SOT |

## 9. Path B sequence (per F13 strategic judgment)

```
B1 (this proposal)         → AWAITING F13 RATIFICATION
B2 (governance review)     → HOLD pending F13 review
B3 (kernel integration)    → DEFERRED until B2 signed off
```

Per F13: "Observe before mutate. Prove before enforce. Preserve before prune."

## 10. Open questions for F13

1. **Migration grace:** 7 days OK? Or longer / different mechanism?
2. **Override frequency:** Should `ack_irreversible=True` have a rate limit? Per F5 spec, sentinel surfaces; but kernel could enforce.
3. **Audit log destination:** `/root/VAULT999/musyawawah/overrides/YYYY-MM-DD.jsonl` per spec §4. Confirm path.
4. **Symlink vs copy:** Reference impl at `/root/AAA/scripts/` — symlink to arifOS, or copy on each release? Symlink risks AAA SOT drift; copy risks AAA SOT divergence.
5. **VAULT999 lookup semantics:** Phase A uses regex only. Phase B should integrate with real VAULT999 (verify reference file exists). What is the failure mode if VAULT999 is temporarily unavailable — fail-open (allow, log) or fail-closed (deny)?
