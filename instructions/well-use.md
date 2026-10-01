# WELL — Substrate Readiness Organ

> **Status:** F13_PROPOSED (2026-10-01)  
> **Role:** Canonical federation instruction for WELL organ interaction  
> **Principle:** SENSE SUBSTRATE → COMPRESS RISK → EMIT READINESS SIGNAL  

```text
WELL observes fitness.
AAA allocates attention.
arifOS decides authority.
A-FORGE executes.
FRAME witnesses.
CHRON remembers change through time.
```

## THE FIVE INVARIANTS

- **W1:** WELL senses fitness; it does not create authority.
- **W2:** Silence is the default when no action is required.
- **W3:** One limiting signal outranks a hundred telemetry facts.
- **W4:** No stale or contradictory evidence may masquerade as readiness.
- **W5:** Every emitted attention signal must change what happens next.

## USE WHEN

- Consequential execution is about to begin.
- Repeated failure suggests substrate degradation.
- Monitoring reports a meaningful health delta.
- Post-action recovery must be verified.

## DO NOT

- DO NOT call WELL on every turn (default = no WELL).
- DO NOT use WELL as constitutional judge or authority gate.
- DO NOT interpret WELL signals as constitutional verdicts (HOLD / SEAL).
- DO NOT expose raw telemetry unless active investigation requires it.
- DO NOT chain multiple WELL tools when the readiness entrypoint suffices.

## THE READINESS REFLEX

Before meaningful action, ask: **"Is the ground fit?"**

```json
{
  "readiness": "READY | DEGRADED | NOT_READY | UNKNOWN",
  "confidence": 0.85,
  "freshness": "FRESH",
  "limiting_plane": "NONE | H_WELL | M_WELL | G_WELL | C_WELL",
  "signal": "STABLE",
  "recommended_load": "NORMAL | REDUCED | MINIMAL",
  "why_now": "short explanation",
  "recheck_after": "20m",
  "authority": "ADVISORY_ONLY",
  "next_organ": "arifOS"
}
```

1. Request readiness for the proposed workload (`well_readiness` or `well_human mode=readiness`).
2. Read `limiting_plane` + `signal`.
3. If `READY` → continue normal governance path.
4. If `DEGRADED` → reduce workload or consult arifOS.
5. If `NOT_READY` / `UNKNOWN` → escalate to arifOS.
6. Never invent `HOLD` / `SEAL` from WELL output.
