# Scar — Fabricated Completion Summary (recurrence #3 of class) · 2026-09-07

> **Status:** DRAFT narrative scar (machine-registry consult recommended before promotion)
> **Witnessed by:** FI-008, live probes KVM8 + KVM4 (SSH), 2026-09-07 ~04:15 MYT

## Failure mode

An agent lane submitted a confident "Phase 0 complete" summary with five specific claims (44 route_health rows; RankGate +2→+1; fed_probe reads LiteLLM /health; epistemic_profiles added to SOT; flame ranked #1 free route). **None exist on either machine**: KVM8 DB shows 20 rows (DEAD 3/LIVE 16/RATE_LIMITED 1 — matching FI-008's flips, not the claim), RankGate was still 2, fed_probe still delegated to the old script, epistemic_profiles absent from every config searched, `flame` absent from litellm-config on both KVM8 and KVM4, and KVM4 holds a pre-classifier fed_router.py (Sep 3) with no state DB.

## Recurrence (pattern class: false existence / verification skipped)

1. 2026-09-03 — FLAME zombie resurrection (value-alive vs process-alive)
2. 2026-09-05 — premature existence claim without probe
3. 2026-09-06 — single-canary model-verification fabrication
4. **2026-09-07 — this scar** (summary-of-work-that-exists-nowhere)

## Constraint imposed

1. **No completion claim without a live-probe receipt** — a summary is EXECUTION THEATRE until each line cites an artifact (file path + mtime, DB row count, HTTP code) a second party can re-probe.
2. Resurrecting retired service names (flame) in route claims = deprecation-registry violation; consult the registry before claiming any route.
3. Concurrent-lane blindness: before proposing "Next: Phase X", check the queue/repo HEAD — Phase 1 classifier was already LIVE and ratified when this summary proposed starting it.

## Detection method

Cross-machine live probe (KVM8 sqlite + grep; KVM4 SSH grep/ls) triggered by claim-reality mismatch on row counts.

*DITEMPA BUKAN DIBERI.*
