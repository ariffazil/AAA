# TEMPORAL-CONTRACT.md — RSR v0 delta (adopted from cross-audit 30/10)

Status: BERASAS (method) / PENDING (experiment records). No SEAL issued — agent verdicts not authority.
Source: cross-audit of pasted synthesis + Phase 0 REALITY_MAP.md (same dir). Experiment claims (Qwen/GPT-OSS time-machine probe) = USER-REPORTED, raw outputs unverified.

## Adopted rules (add to CHRON ledger + reality_graph schema)

1. FORECAST MODE (mandatory field): `mode: prospective | retrospective`
   - prospective: created_at < outcome_available_at. Enters calibration denominator.
   - retrospective: simulated_as_of != created_at date. Separate leaderboard. Never scored with prospective.
   - Example: Oct-2026 probe about mid-2026 = retrospective replay, not forecast.

2. FOUR TIMESTAMPS (all required):
   - forecast_created_at — when actually generated
   - simulated_as_of — historical boundary intended (null for prospective)
   - target_at — when outcome is evaluated
   - outcome_available_at — when outcome info first knowable

3. FORECAST OBJECTS (three, immutable chain):
   - F0 locked forecast: content_hash, resolution_policy_version, supersedes_forecast_id (null allowed)
   - Outcome record: status pending|provisional|final|disputed, event_at, first_available_at, evidence_refs, official_confirmation flag
   - Evaluation record: score, baseline_forecast_ref, scoring_policy_version, exclusions+reasons
   - Probability updates create F1 referencing F0; never edit 0.70 then score 0.85.

4. BASELINE PER FORECAST (required for scoring):
   - reference_class baseline mean_brier on same question class + horizon
   - "CEO continuity" style base-rate questions: model score reported AGAINST baseline, never alone.

5. BOUNDARY BLOCK (retrospective only):
   - requested_model, resolved_model (from route receipt / x-litellm-model-name), documented_training_cutoff: null if unknown
   - parametric_leakage_status: not_established (default) — "no observed leakage" ≠ "leakage impossible"

6. CAUSAL DISCIPLINE (tripwire 8):
   - forecast hit → dependencies marked `compatible_not_discriminated`, never `true`
   - causal promotion requires outcome more expected under H than under named alternatives

7. REGISTRY ELIGIBILITY (provisional only):
   - status: provisional, scope: this_probe_only, repeated_tests_required: true
   - no model becomes sole historical verifier or sole financial forecaster from one probe

## Rejected / flagged from source paste

- Agent-issued "SEAL" verdict: returned unopened. Method BERASAS; sealing is F13 only.
- One-probe model identities: superseded by paste's own correction (§8).
- arXiv citations [2512.23847, 2605.24564]: UNVERIFIED this session.

## Mapping to existing runtime (anti-duplicate)

| Contract element | Owner | Existing surface |
|---|---|---|
| Forecast ledger + hash | CHRON | predictions.jsonl append-only, :18102 |
| Resolve + Brier | CHRON | chron_record_verification, chron_calibration_state |
| Two-vault split | CHRON (extend) | lock-then-verify ordering exists; add retrieval_manifest_hash |
| State schema | AAA | lib/reality_graph.py (bitemporal, extend with 4 timestamps) |
| Route identity | A-FORGE/LiteLLM | x-litellm-model-name verification (fp precedent 28/10) |
| Loop execution spine | A-FORGE | forge_reality_loop (do NOT build second runner) |

— OBS 2026-10-30, KVM8. /root/forge_work/reality/RSR-2026-10-30/
