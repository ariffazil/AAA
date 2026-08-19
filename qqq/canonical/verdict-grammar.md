# AAA 5-Verdict Grammar :: v1.0

> **Ratified**: 2026-08-10 by F13 SOVEREIGN (Arif)
> **Includes SABAR**: Non-terminal meta-state (anti-hallucination & anti-escalation)

## Non-Terminal States

```
UNKNOWN = State description. "I do not know."
SABAR   = Required action.  "I do not know yet, keep working."
```

## Terminal Verdicts

```
SEAL    = "Proceed."
PARTIAL = "Safe subset delivered."
HOLD    = "Authority required."
VOID    = "Forbidden."
```

## SABAR vs HOLD

| Ciri | SABAR | HOLD |
|------|-------|------|
| Tahu? | Belum cukup | Cukup |
| Punca | Evidence nipis | Authority/Risk/Ethics |
| Tindakan | Re-enter discovery | Stop, await sovereign |
| Visibility | Inner-only | Outer-visible |
| Terminal? | **Non-terminal** | **Terminal** |

## Inner Loop Placement

```
SENSE → DISCOVER → COMPOSE → CRITIQUE → SABAR? → JUDGE → EXECUTE → WITNESS
                       ▲                        │
                       └─── if evidence thin ──┘
```

## Anti-HARAM Protection

SABAR prevents two failure modes:
- **Dosa A**: Kurang evidence → terus SEAL = hallucination
- **Dosa B**: Kurang evidence → tanya ARIF = H1/H2/H10 violation

## Top-Level Settle (Outer Loop)

```
SEAL    = Proceed.
PARTIAL = Safe subset.
HOLD    = Await sovereign.
VOID    = Reject.
UNKNOWN = No claim yet.
SABAR   = Internal investigation (not outer-visible).
```
