# SCAR-002 — retired_alias_hard_fail
Class: availability · Severity: HIGH · Promoted 2026-09-22

**Pattern:** A provider retires a model name; compatibility aliases persist
"temporarily" with no expiry date. Hard-coded callers survive until the day
routing ends, then fail 400 simultaneously (fleet-wide cliff).

**First observed:** deepseek-v4-flash-0731 → HTTP 400 "supported API model
names are deepseek-flash, deepseek-v4-pro" (official, 2026-09-22), while
aliases for v4-flash/vision-exp still route.

**Immunity:** canonical names in SOT/routes/probes; alias inventory with
"temporary" marked expiring; failure events logged here (fed_health_set
auto-appends on 400-class evidence) to build the retirement watchlist.

**Floors:** F2_TRUTH · F8_LAW system_boundary
