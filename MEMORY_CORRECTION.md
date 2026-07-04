# MEMORY CORRECTION — 2026-05-25T15:30Z

## What I got wrong

| Claim | Was | Should be |
|-------|-----|-----------|
| GEOX MCP on 18081 has 15 tools, petrophysics/stratigraphy | FALSE | 11 arifOS kernel tools only |
| WEALTH MCP has 15 tools | FALSE | 33 tools |
| arifos MCP has 13 tools | FALSE | 23 tools |

## Verified LIVE state (2026-05-25)

| Port | Service | Tool count | Tool names |
|------|---------|-----------|-----------|
| 8088 | arifos.service | 23 | Full arifOS kernel + organ_consensus + drift_check |
| 18081 | arifosd.py (ARCHIVE) | 11 | arifOS kernel stub (session/sense/judge/vault/run/exec/sudo/systemctl/apex/floor) |
| 18082 | wealth-organ.service | 33 | wealth_* tools |
| 18083 | well.service | 73 | well_* tools |

## What this means

- GEOX Earth tools (petrophysics, stratigraphy, geometry) are NOT registered on any live MCP
- The "GEOX MCP" claim in memory was based on a stale schema, not live probe
- WEALTH and WELL are properly federated
- arifOS MCP (8088) is the primary kernel surface
- arifosd (18081) is a lightweight kernel stub, not a separate organ
