# RECEIPT — v0.1.1 Anchor Corrections (Hermes 555-VERIFY)
**Date:** 2026-10-01T23:13:40Z
**Lane:** B (read-only correction of anchor table + sha sidecar update)

## Sovereign Signal (Hermes 555-VERIFY)
> "2 of 5 anchors FALSE. Not SAH-ready as-filed; one 5-line correction away."
> 5-line edit, 2 minutes. Then SAH.

## D1 (material) — Port-Map Correction ✅ Applied
| Probe | Before (Phantom) | After (Live Verified) |
|---|---|---|
| GEOX | curl :18090/health → 000 (claimed dead) | curl **:8081/health → HTTP 200** (canonical) |
| WEALTH | curl :18100/health → 404 (claimed timeout) | curl **:18082/health → HTTP 200** (canonical) |
| :18090 | implied GEOX | **legacy  deprecated** |
| :18100 | implied WEALTH | **live but serves /mcp JSON-RPC, not /health** |

 +  still declare  (registry drift, real finding).

## D2 (minor) — Bytes Field ✅ Applied
- Disk: 13,443 bytes
- sha.json reported: 13,233 (stale)
- New: 13,837 (post-edit)

## D3 (cosmetic) — Stray  Line 12 ✅ Applied
Removed in edit.

## Bonus — Registry Drift ✅ Documented
Live: GEOX :8081 ✓, WEALTH :18082 ✓. Dead: :18090 (legacy ). Drift is in config files, not runtime.

## New Validation Anchors Table

| Claim | Live status | Verdict |
|---|---|---|
| A-FORGE G=0.9115 | theoretical max of skeleton, NOT live runtime | skeleton PASS, runtime NOT measured |
| W³ | live = 0.7439 (below 0.75 floor) | measured-below |
| arifOS OBSERVE_ONLY | per-actor state, NOT federation gap | RE-SCOPED |
| WEALTH | **:18082/health → 200** | OK ✓ |
| GEOX | **:8081/health → 200**; legacy  returns 000 | OK + REGISTRY-DRIFT |

## Honest Placement (corrected)
- 1 confirmed gap (legacy port registry drift in federation.yaml:112 + claude/agent.yaml:45)
- 3 originally-cited "gaps" were 2 phantom (port misattribution) + 1 mis-scoped (per-actor state)

## Updated sha.json Sidecar
- sha256: 339c9dcf2d4a9e21fbe8d49c25b9ee8d128bfff50be1584482da413c42f9efbe
- bytes: 13,837
- status: CORRECTED_V0.1.1_AWAITING_SAH
- corrections_applied: [D1 port-map, D2 bytes, D3 stray, registry drift documented]

## Held for Sovereign Signal (F13 ratification)
- (a) SAH after v0.1.1 fix anchors (this is current state — fix done)
- (b) SAH as-is with audit correction on record (defect was anchors only, not contract core)
- (c) pushback on any anchor

[receipt: /root/AAA/cockpit/AAA_APEX_ZEN_INIT_TO_SEAL_v0.1.md — sha 339c9dcf]
[receipt: /root/AAA/cockpit/AAA_APEX_ZEN_INIT_TO_SEAL_v0.1.md.sha.json — CORRECTED_V0.1.1]
[receipt: 5/5 live probes (GEOX:8081=200, WEALTH:18082=200, :18090=000, :18100=404, federation.yaml:112)]
[receipt: Hermes 555-VERIFY correction honored]
