# SURFACE-SCHEMA VALIDATION REPORT — 2026-09-21

> **Forged:** FI-008 · 2026-09-21 ~02:40 MYT
> **Trigger:** T1-H auto-do · validate draft-*-surface.json against `/etc/arifos/federation/surface-schema.json`
> **Doctrine:** machine law #7 (never destroy evidence) — reports gaps, doesn't fix them silently

## Method

Per surface-schema.json `invariants` block, each draft is checked for:
1. `declared_eq_exported_eq_callable` — each tool in `canonical` must appear in live `/tools/list` AND be callable
2. `compat_lifecycle` — each compat entry carries `deprecation_since` + `remove_after`, with `remove_after >= deprecation_since + 30 days`
3. `unclassified_eq_zero` — `len(canonical) + len(compat) + len(private) + len(deprecated) == total registered count from /health.registry`
4. `reachability_zero` — every "use X instead" message references a tool in canonical or compat

## Results

| Organ | compat_lifecycle | declared_eq_exported_eq_callable | unclassified_eq_zero | reachability_zero |
|---|---|---|---|---|
| arifos | PASS (vacuously, compat=0) | TBD — needs live probe | counts: 8c+0k+0p+0d=8 | TBD — needs error-message audit |
| aforge | PASS (vacuously, compat=0) | TBD — needs live probe | counts: 121c+0k+0p+0d=121 | TBD |
| geox | PASS (vacuously, compat=0) | TBD — needs live probe | counts: 25c+0k+0p+0d=25 | TBD (known: catch-22 with geox_surface_status error message) |
| wealth | PASS (vacuously, compat=0) | TBD — needs live probe | counts: 14c+0k+0p+0d=14 | TBD |
| **well** | **FAIL** | TBD | counts: 10c+9k+19p+0d=38 | TBD |

## WELL compat_lifecycle FAIL — root cause

The draft `draft-well-surface.json` lists 9 compat entries:
```
well_log_intake, well_log_recovery_event, well_log_substance,
well_inject_biometric, well_observe_machine, well_observe_federation_thermal,
well_observe_scar_load, well_observe_drift_field, well_observe_evidence_backlog
```

These entries are **strings (names only)**. They do NOT carry the required metadata:
- `alias_for` — canonical tool this aliases
- `deprecation_since` — when the deprecation began
- `remove_after` — when the alias will be removed (must be ≥ deprecation_since + 30 days per MCP 2026-07-28 minimum deprecation window)

**Fix:** WELL lane must rewrite compat entries as objects with full lifecycle metadata:
```json
{
  "name": "well_observe_machine",
  "alias_for": "well_classify_machine_state",
  "deprecation_since": "2026-09-21",
  "remove_after": "2026-12-21",
  "description": "...",
  "input_schema_ref": "...",
  "output_schema_ref": "..."
}
```

This is honest reporting, not failure suppression.

## Other TBD items (require additional probes)

- `declared_eq_exported_eq_callable` needs live probe: cross-check draft's `canonical` list against `/tools/list` response for each organ
- `reachability_zero` needs error-message audit: pull all error strings from each organ and verify any "use X instead" suggestion targets a tool in the draft's canonical or compat

Both require organ team ratification — surface as F13 binary items not yet enumerated.

## Honest residue

- The drafts are starting points, not finished contracts.
- The compat_lifecycle FAIL on WELL is a real finding, not a bug — the draft was written quickly to capture tool names; the lifecycle metadata is the proper engineering work that follows.
- Until each draft gets organ team ratification AND the WELL compat entries get lifecycle metadata, NONE of the drafts are eligible to be promoted to canonical `/etc/arifos/<organ>/surface.json` paths.

⚒️ DITEMPA BUKAN DIBERI
