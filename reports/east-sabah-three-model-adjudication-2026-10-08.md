# East Sabah / Dangerous Grounds — Three-Model Adjudication
**Date:** 2026-10-08 · **Session:** SEAL-7391bf016f624eba · **Actor:** FI-008 (kimi-code)
**Input:** F13 handoff `east_sabah_dangerous_grounds_models.json` (public-safe, self-declared WORKING MODEL — NOT SEALED)

## State achieved
- GEOX computed & contrasted: 3 models registered as claims, each with evidence envelope + sha256 receipt.
- arifOS judge lane: **BLOCKED** — L11 `TOKEN_INVALID` (SCT alias defect) on arif_think, arif_judge, and arif_init(resume). 3 attempts, tebus path exhausted. Matches documented defect `/root/AAA/reports/kernel-actor-mismatch-falsehold-2026-10-02.md` (slash-form actor alias missing; fix bundled for kernel review). **No machine verdict was rendered. Nothing was sealed.**

## Contrast result (grounded ONLY in registered GEOX claims)

| Model | GEOX claim | Truth class | Registered evidence verdict |
|---|---|---|---|
| A Extension-Ridge | `clm_1d43072344d54ec5` | SPECULATIVE | Tensed by 3 registered facts: DG = attenuated **continental** crust (dgr_clm_1, MED-HIGH); SCS spreading dead ≥16 Ma (sys_clm_4, HIGH) while Kinabalu magmatism is 7–14 Ma contested (sys_clm_6) ⇒ magmatism multi-generation, not one syn-extensional axis; volcanic-basement H3 weakest of four deep-crust hypotheses p50 0.18 (CLM-NWS-006). A's strong form (continuous ridge) fails crust truth; A's weak form collapses into C. |
| B Underthrust + Mud-Canopy | `clm_da9c21d8c3e54874` | DERIVED | Half-strong, half-open. Canopy documented (Morley 2023 ~1,900 km² ~50 centres; NSPW 8–9 km mobile shale = CLM-NWS-007 p50 0.32). Underthrust = registered UNTESTED hypothesis (sys_clm_3/dgr_clm_2, LOW, pending dip line); polarity/timing UNDER RESOLUTION — HOLD (sys_clm_5, do-not-average). |
| C Hybrid Inherited Corridor | `clm_bebd2c76b29049dd` | INTERPRETATION | **Only model contradicted by zero registered claims.** Inherited rift fabric (dgr_clm_1), forebulge (dgr_clm_4), loading-dominant overprint (two-oceanics 4.25×), BANGKIT late-Miocene rebalancing (sys_clm_6), two-surface-family geometry (sys_clm_8/9, F13-settled) all compatible. |

**Working posture (FI-008 analysis, not a kernel verdict): C preferred · A/B live falsifiable alternatives · none sealable** — open holds: `underthrust_continuation_untested`, `subduction_polarity HOLD`, `KT-7 BLOCKED` (CLM-NWS-008).

## Cheapest discriminating next test
Public magnetic/gravity reprocessing along Tepat–Layang-Layang–Pekaka (potential-field continuity) — already registered as near-zero-cost kill test (CLM-NWS-006, ~6 months). Continuous anomaly → revives A; discontinuous bodies → confirms C; no anomaly → B. Sequence BEFORE any OBS/seismic acquisition spend.

## Receipts
- GEOX claims: `clm_1d43072344d54ec5` (sha dd741fef…) · `clm_da9c21d8c3e54874` (sha a873aa8f…) · `clm_bebd2c76b29049dd` (sha fdd8ee64…)
- GEOX basin packet: `geox:SEAL-7391bf016f6:geox_basin:efc729cc130a` (sha 3932cc9f…)
- Blocked judge traces: trc-fad715d9ba10 (think) · trc-f96984a78352 (judge) · trc-fc5c860b45f4 (resume)
- Evidence base: `/root/GEOX/resources/basins/{dangerous_grounds,nw_borneo_collision_system,sabah_basin}/` + `sabah_two_oceanics.yaml`
