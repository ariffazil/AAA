# RECEIPT — HUD ↔ FRAME Integration
**Date:** 2026-10-01T21:35:11Z
**Lane:** B (autonomous, reversible)
**Doctrine:** hud-observability-doctrine-v3 + organs.yaml FRAME spec
**Prior:** [receipt: /root/AAA/cockpit/receipts/RECEIPT_HUD_DEPLOY_2026-10-02.md]

## Change
- HUD panel [4] JUDGMENT now includes FRAME behavioral drift data
- Source: /root/AAA/cockpit/shadow-matrix/drift-latest.txt (FRAME advisory output)
- Authority: FRAME = ADVISORY_ONLY per organs.yaml (does not judge, does not seal)

## Live data (verified, not narrative)
- FRAME organ: active (PID 1501746, 1d 19h uptime)
- Last FRAME probe: 2026-09-24T04:00:02Z (7.7 days stale — flag for sovereign)
- 5 signals: 🔴2 alerts, 🟡2 warnings, 🟢1 ok
- Red flags: verbosity_drift (+175 chars/response), receipt_output_ratio (3.33)
- Yellow flags: question_back_rate (0.5), shadow_activation_rate (0.3)

## Path-of-evidence
- State file: /root/AAA/cockpit/hud-state.json (sha256=a768062542c0e83b2921b6213aa0b26ce9129afb0b736ffe8a2c7a23f266ba6e)
- Modified files:
  - /root/AAA/cockpit/generate-hud-state.sh (added FRAME probe block)
  - /root/AAA/cockpit/display-hud.sh (added FRAME row to JUDGMENT panel)
- Bashrc hook: unchanged (still triggers display-hud.sh)

## Reversibility (F1)
- Same as prior receipt: remove bashrc lines + delete /root/AAA/cockpit/*.{sh,json}
- This change is additive — no infra mutation

## Held (sovereign lane, F13)
- Re-verify why FRAME last probe = 8 days stale (could be cron drift or organ drift)
- Cron-tie FRAME probe to HUD regeneration (mutual freshness guarantee)
- Surface FRAME signals in web HUD at arif-fazil.com

[receipt: /root/AAA/cockpit/hud-state.json]
[receipt: /root/AAA/cockpit/receipts/RECEIPT_FRAME_HUD_INTEGRATION_2026-10-02.md]
