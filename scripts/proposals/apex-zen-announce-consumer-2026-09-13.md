# APEX-ZEN ANNOUNCE-Tier Consumer — Interface Spec (proposal)

**Status:** DRAFT · **Author:** 333-AGI · **Date:** 2026-09-13
**Depends on:** calibration v1 rules R1–R4 (`apex-zen-calibration-2026-09-13.md`)

## 1. Purpose

Move from OBSERVE_ONLY (no consumer) to ANNOUNCE: emit restrictions to a log surface
without blocking anything. GATE (blocking) is a later promotion and is NOT in scope here.

## 2. Input contract (live preflight, verified 22:05)

`/root/VAULT999/apex-zen-preflight.json` = actor map (24 entries), each:

| field | present? | use |
|---|---|---|
| `worst_severity` | ✅ | verdict (COMPLIANT/WATCH/WARNING/DOWNGRADE/VIOLATION/UNKNOWN) |
| `per_metric_severity` | ✅ | which metric produced the verdict |
| `metrics_missing` | ✅ | unmeasurable metrics (must not rank) |
| `timestamp` | ✅ | cycle id |
| `CD` `DD` `IAR` `DCR` | ✅ | raw values |
| `restriction` | ❌ (only when flagged) | proposed restriction string |
| `cd_basis` | ❌ **MISSING** | R1: which signal inputs backed CD |
| `consecutive_flags` | ❌ **MISSING** | R4: sustained vs spike |

## 3. Output contract (new surface only)

`/root/VAULT999/apex-zen-announce.jsonl`, one record per (actor, worst_severity, preflight.timestamp):

```json
{"announce_id":"sha256(actor|severity|cycle_ts)[:16]","cycle_ts":"...","actor":"arifFlow:x",
 "severity":"VIOLATION","per_metric_severity":{...},"metrics_missing":[...],
 "restriction":"tier0_restricted_5_turns","tier":"ANNOUNCE","action":"log_only"}
```

Idempotent by `announce_id`. No blocking. No mutation. No writes outside this file.

## 4. Readiness gates (halt conditions)

- **HALT if** any actor is missing `worst_severity`, or `worst_severity` not in enum.
- **HALT if** R1/R4 fields absent AND any VIOLATION actor is one of the known artifacts
  (CD=1.0 ×37 class: `arif`, `333-AGI/agentic-web`, `333-AGI/dynamic-gate`,
  `grok-build/FI-007`, `codex`, `codex-startup`) — announcing those = false alarms.
- **PROCEED** only when readiness validator reports READY.

## 5. Integration point (choose one at promotion)

1. A2A bridge preflight read (was the retired gate's home) — highest leverage, most coupling.
2. `route_task.py` dispatch hook — per-task announce.
3. Hermes gateway hook on `agent:start` — per-turn announce.
Recommended: **(1)** with the bridge ONLY reading the announce stream (never blocking) at ANNOUNCE tier.

## 6. Promotion criteria

| Tier | Enter when |
|---|---|
| OBSERVE_ONLY (now) | — |
| ANNOUNCE | R1–R4 land; readiness validator READY; 12 consecutive cycles with 0 artifact flags |
| GATE | ANNOUNCE shows 0 false positives over 7 days and ≥1 genuine catch |

## 7. Failure modes / rollback

- Announce writer fails → no writes, no side effects (fail-soft, log-only).
- False precision risk → mitigated by R1/R4 dependency declared above.
- Rollback: delete announce file + remove consumer wiring; zero effect on other surfaces.

---

## 8. UPDATE 22:14 — contract v2 (FI-008's real field) + READY

- **Live contract uses `severity_reliable = not metrics_missing`** (router line 135), added by FI-008 22:06 (`02af0c5a9`). It supersedes the hypothesised `cd_basis` field.
- **All 6 artifact actors carry `severity_reliable: false`** → automatically excluded from announcements. Artifact risk: **0**.
- **Validator v2 result: READY (ANNOUNCE tier)** — 24/24 verdict + reliability; announce set = 15; `consecutive_flags` absent (now scoped to GATE tier only).
- **Consumer built + tested** (`apex-zen-announce-consumer.py`):
  - preview: 15 flagged+reliable, restrictions visible (`tier0_restricted_5_turns` / `observe_only` / `f13_advisory`)
  - idempotency: emit 15 → second run emit 0 (skipped 15) ✓
- **Wiring on handoff (one line, do NOT add while FI-008 is mid-wave):**
  `python3 /root/AAA/scripts/proposals/apex-zen-announce-consumer.py --emit` after the router phase in `apex-zen-run-loop.sh` — or the bridge reads the announce stream (log-only, never blocking).
