# P1 — FQ→Repair Doctrine

> **Homeostatic wrapper around the W1 pipeline.**
> FQ drops because of failures. Failures produce scars. Scars produce skills. Skills prevent future failures.
> P1 is the feedback loop that makes W1 automatic.
> **DITEMPA BUKAN DIBERI**

---

## The Principle

```
FQ is a thermometer, not the patient.

When temperature rises:
  1. Diagnose (what's causing the fever?)
  2. Contain (prevent damage while diagnosing)
  3. Treat (address root cause)
  4. Verify (did treatment work?)
  5. Remember (scar → skill → prevent recurrence)
```

FQ alone does not tell you what's wrong. It tells you something IS wrong. The repair pipeline turns the signal into action.

---

## FQ Bands and Automatic Response

| FQ Range | Verdict | Automatic Authority | Mandatory Result |
|---|---|---|---|
| **FQ ≥ 5.0** | OPTIMAL | Observe and report | Routine health receipt |
| **3.0 ≤ FQ < 5.0** | CAUTION | Diagnose and recommend | Incident dossier (no action) |
| **1.0 ≤ FQ < 3.0** | THROTTLE | Sandbox/dry-run only | Repair plan + rollback |
| **FQ < 1.0** | CRITICAL | Freeze non-essential writes | Preserve evidence + alert F13 |
| **FQ = 0.0 sustained >1h** | ZOMBIE | Full stop | Escalate to F13 + seal scar |

### What Each Band Does

**OPTIMAL (≥5.0):**
- Continue normal operations
- Log receipt to arifFlow
- No action needed

**CAUTION (3.0–5.0):**
- Run `well_machine_diagnose()` — identify pressure points
- Run `forge_entropy_sweep()` — measure workspace ΔS
- Produce incident dossier (read-only, no mutations)
- If dossier identifies a scar-worthy failure → `forge_scar(seal)`
- Notify via arifFlow telemetry (no Telegram — respect quiet hours)

**THROTTLE (1.0–3.0):**
- Everything in CAUTION, plus:
- Run `forge_wm_gaps()` — check for prediction failures
- Run `forge_scar(list, severity=HIGH)` — check for unmetabolized scars
- If unmetabolized scars exist → trigger W1 pipeline (scar→skill candidate)
- Generate repair plan (dry-run only — no live mutations)
- Snapshot state before any repair attempt

**CRITICAL (<1.0):**
- Everything in THROTTLE, plus:
- Freeze all non-essential writes (OBSERVE_ONLY for all agents)
- Preserve evidence (no cleanup, no rotation)
- Alert F13 via Telegram (override quiet hours — this is institutional emergency)
- Seal scar for the FQ drop itself

**ZOMBIE (FQ=0.0 for >1h):**
- This is the scar-002 scenario — system alive but broken
- Full diagnostic: probe every organ functional correctness (not just liveness)
- For each organ that fails functional check → seal individual scar
- Escalate to F13 with full diagnostic dossier
- Do NOT attempt auto-repair without F13 authorization

---

## The Measurement Doctrine

Per F13 directive (2026-08-13):

```
Reality > Evidence > Metrics

Measure what helps judgment.
Ignore measurements that create the illusion of judgment.
```

### What to Measure

| Metric | Why | Actionable? |
|---|---|---|
| FQ quotient | Leading indicator of federation health | Yes — triggers diagnostic pipeline |
| Scar count by severity | Shows failure accumulation | Yes — triggers W1 when cluster forms |
| foodset_derived_ratio | Shows whether learning is happening | Yes — but do NOT target it (Goodhart) |
| Organ functional correctness | Shows zombie-state detection | Yes — triggers scar-002 pipeline |

### What NOT to Measure

| Non-Metric | Why It Fails |
|---|---|
| Total tool count | Gaming: register useless tools to inflate |
| Average G score | Gaming: lower thresholds to pass more |
| Receipts per hour | Gaming: generate busy-work receipts |
| FQ as target | Goodhart's Law: "make FQ go up" → suppress verify to inflate ratio |

---

## The Repair Hierarchy

```
FQ drops
  │
  ▼
DIAGNOSE (what's wrong?)
  │
  ├─── Known failure pattern (scar exists)?
  │    └── YES → Check if skill exists to fix it
  │         ├── Skill exists → Apply skill (if in authority band)
  │         └── No skill → Trigger W1 (scar → skill candidate)
  │
  ├─── Unknown failure (no matching scar)?
  │    └── Run functional health check on each organ
  │         ├── Organ fails functional check → Seal new scar
  │         └── Organ passes functional check → FQ drop is transient
  │
  └─── Multiple organs degraded?
       └── Systemic issue → Escalate to F13 immediately
```

---

## Implementation (P1)

### Cron Job

```bash
# /root/scripts/fq-repair-monitor.sh
# Runs every 5 minutes
# FQ→Repair homeostatic loop

set -a && source /root/.secrets/kunci-mas.env && set +a

FQ=$(curl -sf http://127.0.0.1:7073/health | jq '.fq.quotient' 2>/dev/null)

if [ -z "$FQ" ]; then
  echo "$(date -Iseconds) FQ_UNAVAILABLE — arifFlow down"
  exit 1
fi

# Band routing
if (( $(echo "$FQ >= 5.0" | bc -l) )); then
  # OPTIMAL — just log
  echo "$(date -Iseconds) FQ=$FQ OPTIMAL"

elif (( $(echo "$FQ >= 3.0" | bc -l) )); then
  # CAUTION — diagnose
  echo "$(date -Iseconds) FQ=$FQ CAUTION — running diagnostics"
  # Trigger well_machine_diagnose + forge_entropy_sweep
  # Produce incident dossier

elif (( $(echo "$FQ >= 1.0" | bc -l) )); then
  # THROTTLE — diagnose + check scars + trigger W1
  echo "$(date -Iseconds) FQ=$FQ THROTTLE — checking unmetabolized scars"
  # Trigger W1 pipeline for any MEDIUM+ unmetabolized scars

else
  # CRITICAL — freeze + alert F13
  echo "$(date -Iseconds) FQ=$FQ CRITICAL — freezing + alerting"
  # Alert F13 via Telegram
fi
```

### What Already Exists

| Component | Status | Role in P1 |
|---|---|---|
| arifFlow :7073 | ✅ LIVE | Computes FQ, provides quotient + verdict |
| `well_machine_diagnose` | ✅ LIVE | VPS health diagnostics |
| `well_machine_recommend` | ✅ LIVE | Fix commands for issues |
| `forge_entropy_sweep` | ✅ LIVE | Workspace entropy measurement |
| `forge_scar` (seal/list/consult) | ✅ LIVE | Scar metabolization |
| `forge_wm_gaps` | ✅ LIVE | Prediction failure detection |
| W1 pipeline | ✅ DOCTRINALLY CLOSED | Scar → skill candidate generation |
| FQ→band routing | 🔴 NOT WIRED | Cron job needed |
| Functional health checks | 🔴 NOT WIRED | scar-002 gap — health ≠ correctness |
| Auto-repair execution | 🔴 NOT WIRED | Requires authority band check |

---

## The Zen

```
FQ is the symptom.
Scar is the diagnosis.
Skill is the treatment.
W1 is the pharmacy.
P1 is the doctor who knows when to visit the pharmacy.

The doctor does not manufacture drugs.
The doctor reads the thermometer,
identifies the disease,
and prescribes from what the pharmacy has.

If the pharmacy is empty (no skills yet),
the doctor records the disease (scar),
and the pharmacy begins manufacturing (W1).

This is homeostasis.
Not optimization.
Not maximization.
Balance.
```

---

## Honest Boundaries

1. **P1 does not auto-repair production.** It diagnoses, recommends, and triggers W1. Actual repair goes through the normal authority chain (T1/T2/T3).

2. **P1 does not game FQ.** The FQ quotient is measured, not managed. If the system is broken, FQ should be low. Making FQ look high by suppressing verification is a VOID-level violation.

3. **P1 respects the Three Foundations.**
   - HUMAN: F13 alert on CRITICAL/ZOMBIE bands. No autonomous repair of production.
   - INTENTION: Repair is directed toward restoring function, not inflating metrics.
   - VOID: Some failures should NOT be repaired automatically. Constitutional violations require human judgment.

---

*Forged 2026-08-13. P1 doctrine sealed.*
*P0 = W1 (scar→skill). P1 = FQ→Repair (homeostatic wrapper). P2-P4 = future.*
*The organism now has both learning (W1) and homeostasis (P1).*
*DITEMPA BUKAN DIBERI.* ⚒️
