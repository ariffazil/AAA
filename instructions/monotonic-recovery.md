# MONOTONIC_RECOVERY — Capability Recovery Under Uncertainty

**Forged:** 2026-09-10
**Source:** EUREKA::CAPABILITY_METABOLISM::v1
**Status:** DRAFT_AWAITING_F13

## Axiom

When certainty falls, capability access expands. Never shrink capability because confidence fell. Recover monotonically.

## Canonical Form

```
UNKNOWN → SABAR → Broaden surface → Proceed safely
```

Not:

```
UNKNOWN → BLOCK
```

## Implementation

The tool router implements this at the session level:
- If a pruned tool is needed later, add its owning toolset permanently
- Never re-prune a recovered toolset within the same session
- Capability, once formed, is never revoked

The experience metabolism implements this at the cross-session level:
- If a trace shows capability improvement, promote it permanently
- Never demote a proven capability without F13 SOVEREIGN approval
- Scar formation is monotonic: scars are never deleted

## Relationship to Existing Doctrine

- Operational form of SABAR principle
- Composes with Scar doctrine: scars are permanent recoveries
- Composes with Fail-Open: uncertainty triggers expansion, not restriction
- Inverse of Fail-Closed governance: fail-closed restricts ACTION, fail-open expands CAPABILITY
