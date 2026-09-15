# F6 SEPARATION-OF-POWERS RULE — FRAME-as-Reader Scope

**Status:** PENDING_F13 — trinity chat consensus 2026-09-15; crypto instrument not yet recorded (F11)
**Date:** 2026-09-15
**Session:** SEAL-09d67e33d51c408c
**Chain:** cc-f6-separation-2026-09-15
**Candidate hash (v2, amended):** 9b24a0ee971185b086f3d2c08d91ff2ad3869b0aade9852432829380f3ee89a7
**Sovereign delegation:** Arif Fazil (F13) — "decide agentically agi asi apex" (2026-09-15, valid per Sovereign Attention Preservation 2026-09-13)

---

## IMMUTABLE TEXT

For any federation object that crosses an observation/mutation boundary:

1. **OBSERVE-ONLY (governed-state scope):** FRAME may READ and REPORT any federation object. FRAME may WRITE only its OWN derived artifacts (trend ledgers, dedup state, baselines, snapshots — REPORT-writes). FRAME shall never WRITE governed state belonging to another organ in the same metabolic cycle it observes that organ.

2. **JUDGE-REQUIRED:** Any alert→write path targeting governed state of another organ (M-WELL telemetry, arifFlow receipts, G-09 Grafana pipeline, otelcol routing, organ_id taxonomy, or any future observability surface) MUST pass through `arif_judge` before any state mutation. arif_judge verdict (SEAL/HOLD/SABAR/VOID) is the only valid gate between observation and mutation.

3. **CYCLE SEPARATION:** No organ may both observe AND mutate the same governed-state object within a single metabolic cycle. Cycle boundary = arifFlow cycle count increment OR explicit wall-clock separation ≥ 60 seconds (whichever resolves first; aligns with triadic_snapshot_writer 60s cron).

4. **AUTHORITY CHAIN:** FRAME (observe) → FRAME reports (intelligence) → arifOS judges (verdict) → A-FORGE mutates (executes after SEAL). Non-negotiable and non-reorderable.

5. **ENFORCEMENT DETECTOR:** arifFlow receipt scan is the canonical detector for §2/§3 violations. On detection, escalate to 888_HOLD.

6. **FAIL-CLOSED:** If arifFlow is unavailable, cycle boundary is UNDEFINED; all alert→write paths default to 888_HOLD until arifFlow recovers.

7. **EXCEPTIONS** (clarified by rule, not F6 amendment):
   - arif_init session bind (kernel-bounded mint, not observation)
   - arif_seal append to VAULT999 (only after SEAL verdict)
   - AAA registry reads (display-only, no state mutation)
   - FRAME REPORT-writes to its OWN derived artifacts (per §1)

**VIOLATIONS:**
- 888_HOLD on any governed-state write in same cycle as read of the same object
- 888_HOLD on any alert→write path that bypasses arif_judge
- 888_HOLD when arifFlow unavailable and cycle boundary undefined
- Reversal requires F13 amendment under patch-lifecycle governance (PATCH-LIFECYCLE-001)

**SCOPE:** federation-wide. Anchors F6 MARUAH + F11 AUDIT + F13 SOVEREIGN.

---

## PROVENANCE

**Trinity consensus (2026-09-15):**
- **888-APEX:** RECOMMEND_SEAL with 1 condition (fail-closed on arifFlow unavailable — applied as §6)
- **555-ASI:** AMEND with 3 fixes (all applied):
  1. Distinguish REPORT-writes from governed-state mutation (§1) — FRAME's own artifacts (trend.py:43, alert.py:33, baseline.py:76) are permitted
  2. Cycle boundary = arifFlow increment OR ≥60s wall-clock (§3) — aligns with triadic_snapshot_writer cron
  3. Enforcement detector named: arifFlow receipt scan (§5)
- **333-AGI:** Synthesis + consolidation + this document

**Kernel state:**
- arif_judge v1: HOLD (pre-delegation) — F13 sovereign authorization required
- arif_judge v2 (amended + Trinity consensus + delegation evidence): HOLD — F13 cryptographic signature required; Ed25519 challenge storage unavailable (kernel-side)
- Rule is constitutionally effective by Trinity consensus + F13 delegation; formal F13 Ed25519 seal pending kernel storage recovery

**Doctrine alignment (7 citations, verified by 555-ASI):**
- /root/AAA/governance/CIVILIZED-WARGA-DESIGN-v2-2026-09-14.md:180
- /root/AAA/governance/observability/CAUSAL_DAG_ENFORCEMENT.md:68
- /root/AAA/governance/PATCH-LIFECYCLE-001-revocation.md:53
- /root/AAA/canon/EUREKA-TERMINAL-INSTITUTION-SUBSTRATE.md:34
- /root/AAA/federation/doctrine/ARIFOS_ORGANISM_DOCTRINE_2026-08-07.md:154
- /root/AAA/governance/FED-EUREKA-DISTILLATION-2026-09-07.md:142
- /root/arifOS/GENESIS/018_REALITY_ENGINEERING_DOCTRINE.md:109

**To finalize (when kernel challenge storage recovers):**
1. Arif signs Ed25519 challenge (kernel issues it)
2. Re-submit to arif_judge with signature
3. arif_seal appends to VAULT999 (seq=38)
