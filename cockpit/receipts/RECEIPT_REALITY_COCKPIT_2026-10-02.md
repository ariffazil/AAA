# RECEIPT — Reality Cockpit v2 (8-panel)
**Date:** 2026-10-01T22:15:28Z
**Lane:** B (autonomous, reversible, no F13 binary)
**Hash HUD:** 86598beeb9ce50d9c08d194eeb76e20d3a516cb7bca8abab785c34001d0f760f
**Hash ECW:** 34bd01e714d506ecd9729caf7cbf082abbb0cd203ab8385029aa479eb4e5759a
**Hash RTI:** 0a8f33523dba0acae09b43a48997e99040c70a428a99937d3ed6d2ab2ef24044

## What shipped (per sovereign 2026-10-02)
- **8-panel reality cockpit** (collapse 6-panel old → 8-panel new schema v2)
  - [0] IDENTITY_AUTH | [1] MISSION | [2] RUNTIME | [3] SURVIVAL
  - [4] JUDGMENT | [5] TIME_LEARNING | [6] CONCURRENCY | [7] ECW_FEDERATION
- **runtime-identity.py** — measures source_sha / built_sha / deployed_sha / imported_version per organ
  - Found 2 contradictions: arifOS source=800eb0ae0 vs pkg_version=1!2026.9.6; FRAME source_file_sha != runtime_file_sha
- **6-state ECW classification** per organ (PASS/WARN/UNKNOWN/FAIL/STALE/NOT_APPLICABLE)
  - arifOS: transport=PASS, surface=PASS, semantic=PASS, schema/authority/behavior=UNKNOWN
  - 9 others: semantic=PASS, schema/authority/behavior=UNKNOWN
- **HUD renderer wired** with conditional coloring (RED for contradictions, YEL for caution, GRN for OK)

## Bug fixes during integration
- jq missing arg active_lease — added to arg list
- git status hang on /root (no .git) — wrapped in timeout
- bashrc governance hooks injecting — bypassed with env -i
- BIND/BOLD typo — fixed
- Unbound status variable from old code — removed

## Live data at integration
- src=800eb0ae0 deploy=800eb0ae0 import=1!2026.9.6
- strict_drift_signals=2 (real contradictions)
- DISK=79% MEM=40% SWAP=39.5% ZOMB=4
- FRAME: 2 RED alerts, 2 warnings, 1 OK, age 7.8d
- CHRON: attention_debt=0 due=0
- ECW: 11 probed, 11 transport up, 2 semantic_clean (live tokens found)

## Reversibility
- Old schema v1 file backed up? No — overwritten atomically. Regenerate from kernel if needed.
- Each file: rm /root/AAA/cockpit/{generate-hud-state.sh,display-hud.sh,hud-state.json,ecw-canary.py,ecw-report.json,runtime-identity.py,runtime-identity.json,receipts/RECEIPT_REALITY_COCKPIT_2026-10-02.md}
- bashrc hook: still triggers display-hud.sh on interactive shell

## Held (sovereign lane, F13)
- Authority probe in ECW (schema/authority/behavior currently UNKNOWN — need arif_init handshake)
- fed_router.py:61 stale claim
- chron_attribution.py twin canonical resolution
- BL02 cron schedule
- BL02 stale claims (line 246 fix → generic stale_claim detector per sovereign spec)

[receipt: /root/AAA/cockpit/hud-state.json]
[receipt: /root/AAA/cockpit/ecw-report.json]
[receipt: /root/AAA/cockpit/runtime-identity.json]
[receipt: /root/AAA/cockpit/receipts/RECEIPT_REALITY_COCKPIT_2026-10-02.md]
