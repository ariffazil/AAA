# OpenClaw Sleep-Time Manager — Prototype

This directory contains a reversible prototype for adding sleep-time compute to OpenClaw and, by extension, any AAA warga agent.

## Files

| File | Purpose |
|------|---------|
| `l3_shadow_schema.sql` | Postgres schema for the shadow partition (F1 reversibility) |
| `openclaw_sleep_manager.py` | Daemon prototype: state monitor → L2 ingress → metabolizer → shadow commit (deferred) |
| `morning_briefing_merge.py` | F1/F2 validation handshake: shadow → primary memory merge (deferred) |
| `systemd/arif-dream-phase2.service` | **Priority:** weekly counterfactual rehearsal service |
| `systemd/arif-dream-phase2.timer` | **Priority:** weekly timer (Sunday 02:00 MYT) |
| `systemd/arif-dream.service` | Optional migration of nightly cron to systemd |
| `systemd/arif-dream.timer` | Optional nightly systemd timer |
| `dream.py` (external) | User-provided minimal PoC using file-based shadow partition (deferred) |

## Priority Pivot

Per live telemetry, the existing nightly Stages 1-4 are stable. The immediate build target is **Phase 2 counterfactual rehearsal**, implemented as `/root/.hermes/skills/dream-engine/scripts/stage5_rehearse.py` with systemd timer `arif-dream-phase2.timer`.

The OpenClaw sleep-time manager and L3_shadow schema remain as reversible prototypes for later phases.

### 1. Install schema

```bash
psql -h 127.0.0.1 -U arifos_admin -d vault999 \
  -f /root/AAA/skills/agentic-dream-engine/prototype/l3_shadow_schema.sql
```

### 2. Dry-run the daemon

```bash
cd /root/AAA/skills/agentic-dream-engine/prototype
python3 openclaw_sleep_manager.py --dry-run
```

This prints what would be written to `l3_shadow` but makes **no writes**.

### 3. Shadow-write the daemon

```bash
python3 openclaw_sleep_manager.py --execute
```

Writes only to `l3_shadow` and `l3_shadow_audit`. Never touches `memory_records`.

### 4. Review and merge via morning briefing

```bash
# Dry-run review
python3 morning_briefing_merge.py --dry-run

# Execute merge (requires F1 snapshot + F2 witness to pass)
python3 morning_briefing_merge.py --execute
```

## Architecture

```
OpenClaw ACTIVE
       │
       ▼  (idle > 120 min OR nightly window)
 State Monitor
       │
       ▼
 L2 Ingress & Entropy Sorting  ──► read-only on primary stores
       │
       ▼
 Offline EMD Metabolizer        ──► 333-AGI gist extraction + anticipatory compute
       │
       ▼
 Shadow Commit & Seal           ──► write to l3_shadow only
       │
       ▼
 Morning Briefing Merge        ──► F1 snapshot + F2 witness → memory_records
```

## Comparison with `dream.py`

The user-provided `dream.py` is a minimal PoC using a file-based shadow partition (`/var/arifOS/memory/L3_shadow.json`). This prototype uses Postgres for:

- Concurrent access by multiple warga agents
- Built-in audit trail (`l3_shadow_audit`)
- Queryable pending review queue
- Atomic transactions

Both approaches respect the same constitutional rule: **shadow-first, primary-only-after-validation**.

## F1/F2 Checklist

| Floor | Mechanism |
|-------|-----------|
| F1 AMANAH | Snapshot before merge; single-command purge; additive writes only |
| F2 TRUTH | Counterfactual in gist; F2 witness before merge (stub → hermes_cross_verify) |
| F7 HUMILITY | `synthesis_score` threshold-locked at 0.65 |
| F8 LAW | Agent lease + session binding |
| F9 ANTIHANTU | Mechanical language only; no "I dreamed" |
| F11 AUTH | Every write to `l3_shadow_audit` and `memory_audit_log` |
| F13 SOVEREIGN | Threshold/cap/cadence changes require Arif ratification |

## Production Checklist

- [ ] arifOS + WEALTH health restored
- [ ] Real L2 trace source wired (OpenClaw session DB)
- [ ] Real LLM endpoint wired (MiniMax-M3 via OpenClaw gateway)
- [ ] F1 snapshot script implemented in dream-engine stage4
- [ ] F2 witness switched from stub to `hermes_cross_verify`
- [ ] Cron entry installed (Option A: nightly 03:00 MYT)
- [ ] 888_HOLD clearance obtained

## Risks

- **Hallucinated gist:** mitigated by shadow partition + F2 witness.
- **Daemon runs while user active:** mitigated by L1 mutex + signal handler.
- **Compute spike:** mitigated by fixed window + max LLM calls cap.

---

*Forged: 2026-06-16 by FORGE (000Ω) — DITEMPA BUKAN DIBERI*
