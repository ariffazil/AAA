# AGENTIC ZEN METRICS — What "Done" Looks Like

> **Forged:** 2026-07-28 | **Author:** 333-AGI (Delta MIND)
> **Sovereign:** Arif (F13) | **Heritage:** AGENTIC_ZEN_GAPS.md · HITV v0.1
> **Role:** Agent-facing verification contract. Not a spec. Not a plan. The TARGET.
>
> Every agent that forges these gaps reads this file FIRST.
> If the live probe doesn't match this, the gap is NOT closed.

---

## 0. THE ONE RULE

```
FORGE = Execute + Verify + Cool + Seal.
A gap is closed ONLY when the metric changes AND stays changed.
"Done" = live probe confirms the metric at T₁ AND T₁+5min.
```

---

## 0.5. PASS/FAIL — Single Command

```bash
# EVERY gap verification runs through this:
curl -s http://localhost:7073/health | python3 -c "
import json,sys
d=json.load(sys.stdin)
fq=d['fq']
print(f'FQ={fq[\"quotient\"]} V={fq[\"verdict\"]} E={fq[\"execute_count\"]} Vc={fq[\"verify_count\"]}')
# If V='STUCK' and verify_count==0 → GAP 1 CLOSED
# If verify_count > 0 → GAP 2 MAKING PROGRESS
# Check cooling for GAP 4
if d.get('cooling'):
    c=d['cooling']
    print(f'COOLING: phase={c[\"phase\"]} stuck_since={c.get(\"stuck_since\",\"none\")}')
"
```

---

## GAP 1: FQ Formula — verify=0 → STUCK

### Before (broken)
```json
{
  "fq": 2.5,
  "execute_count": 2,
  "verify_count": 0,
  "verdict": "BALANCED"
}
```
**Observation:** FQ reports BALANCED while verify is completely absent.
Federation can operate in STUCK state while reporting healthy.

### After (fixed)
```json
{
  "fq": 0.0,
  "execute_count": 2,
  "verify_count": 0,
  "verdict": "STUCK"
}
```
**Observation:** verify=0 forces STUCK regardless of EMA, smoothing, or history.
FQ never reports BALANCED/OPTIMAL/WATCHING when verify is absent.

### METRICS — Gap 1 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M1.1 | `verify=0` → verdict | `curl :7073/health \| jq '.fq.verdict'` | `"STUCK"` |
| M1.2 | `verify=0` → quotient | `curl :7073/health \| jq '.fq.quotient'` | `0.0` (NOT 999, NOT 2.5) |
| M1.3 | `verify>0` → normal | Ingest 1 Execute + 1 Verify, then probe | verdict: OPTIMAL/BALANCED/WATCHING per formula |
| M1.4 | No regression | Ingest 0 Verify after having Verify before | Must STAY in last known verdict (not crash) |
| M1.5 | Zero-zero case | Fresh daemon, zero receipts | `fq.verdict` = `"UNMEASURED"` or `"STUCK"` with quotient=0 |
| M1.6 | Rust tests pass | `cd /root/arifFlow && cargo test` | 0 failures (update test_flow_quotient_no_verification) |
| M1.7 | TypeScript mirror | `fqVerdict(999, 2, 0)` in TS | returns `"STUCK"` |
| M1.8 | flow_state.json | `cat /root/AAA/state/flow_state.json` | `status: "STUCK"` when verify=0 |

### SELF-TEST script (agent runs after forge)
```bash
#!/bin/bash
# GAP1-VERIFY.sh
echo "=== GAP 1 VERIFICATION ==="

# 1. Current state
FQ=$(curl -sf http://localhost:7073/health | python3 -c "import json,sys; d=json.load(sys.stdin)['fq']; print(json.dumps(d))")
echo "Current FQ: $FQ"

# 2. Force scenario: ingest 2 Execute, 0 Verify
for i in 1 2; do
  curl -sf -X POST http://localhost:7073/ingest \
    -H 'Content-Type: application/json' \
    -d "{\"receipt_id\":\"test-gap1-$i\",\"actor_id\":\"test\",\"session_id\":\"test\",\"step_type\":\"Execute\",\"cost_ns\":1000,\"epistemic_label\":\"Derivation\",\"floor_verdict\":\"Pass\",\"created_at\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"step_number\":$i,\"cooling_decision\":\"None\"}" > /dev/null
done
sleep 1

# 3. Verify
RESULT=$(curl -sf http://localhost:7073/health | python3 -c "
import json,sys
fq=json.load(sys.stdin)['fq']
v=fq['verdict']
q=fq['quotient']
print('PASS' if v=='STUCK' and q==0.0 else f'FAIL: verdict={v} quotient={q}')
")
echo "Result: $RESULT"

[ "$RESULT" = "PASS" ] && echo "✅ GAP 1 CLOSED" || echo "❌ GAP 1 STILL OPEN"
```

---

## GAP 2: Three Agents, One FQ Pipeline

### Before (broken)
```
arifFLOW receipts:
  actor_id=opencode: 2 receipts (both Execute)
  actor_id=hermes-prime: 0
  actor_id=opencrawl-surface: 0
  actor_id=geox-*: 0
  actor_id=wealth-*: 0
  actor_id=well-*: 0
```

### After (fixed)
```
arifFLOW receipts (rolling window of 20):
  actor_id=opencode: Execute + Verify receipts
  actor_id=hermes-prime: Execute (conversation turns) + Verify (Arif replies)
  actor_id=opencrawl-surface: Execute (health probes) + Verify (consistency)
  actor_id=geox-falsify: Execute + Verify
  actor_id=wealth-compute: Execute + Verify
  actor_id=well-check: Execute + Verify
```

### METRICS — Gap 2 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M2.1 | HERMES produces Execute receipts | Send a message, then probe | ≥1 receipt with `actor_id=hermes-prime`, `step_type=Execute` |
| M2.2 | HERMES produces Verify receipts | Arif replies affirmatively, then probe | ≥1 receipt with `actor_id=hermes-prime`, `step_type=Verify` |
| M2.3 | OpenCode produces Verify receipts | Run `make prove` green, then probe | ≥1 receipt with `actor_id=opencode`, `step_type=Verify` |
| M2.4 | Verify count > 0 after normal session | `curl :7073/health \| jq '.fq.verify_count'` | `> 0` after 1+ full agent cycles |
| M2.5 | FQ reflects all agents | Ingest 5 Execute (various actors), 3 Verify (various actors) | FQ ≈ 5/3 = 1.67, verdict BALANCED |
| M2.6 | Non-OpenCode actors in receipt store | `cat /var/lib/arifflow/receipts.jsonl \| python3 -c "import json,sys; actors=set(); [actors.add(json.loads(l)['actor_id']) for l in sys.stdin]; print(len(actors), sorted(actors))"` | `≥3` unique actors |
| M2.7 | FQ drops when verify missing from ALL agents | Only Execute from all agents, no Verify from any | verdict = STUCK |
| M2.8 | Best-effort resilience | Stop arifFLOW, call HERMES tool | HERMES tool still works (ingest fails silently, doesn't block) |

### SELF-TEST script
```bash
#!/bin/bash
# GAP2-VERIFY.sh
echo "=== GAP 2 VERIFICATION ==="

# Count unique actors in receipt store
ACTORS=$(tail -50 /var/lib/arifflow/receipts.jsonl 2>/dev/null | python3 -c "
import json,sys
actors={}
for l in sys.stdin:
    try:
        r=json.loads(l)
        a=r.get('actor_id','?')
        s=r.get('step_type','?')
        actors[a]=actors.get(a,{})
        actors[a][s]=actors[a].get(s,0)+1
    except: pass
for a,steps in sorted(actors.items()):
    print(f'  {a}: exec={steps.get(\"Execute\",0)} verify={steps.get(\"Verify\",0)} barrier={steps.get(\"Barrier\",0)}')
print(f'TOTAL_ACTORS={len(actors)}')
")
echo "$ACTORS"

ACTOR_COUNT=$(echo "$ACTORS" | grep TOTAL_ACTORS | cut -d= -f2)
if [ "$ACTOR_COUNT" -ge 3 ]; then
    echo "✅ GAP 2 MINIMUM MET (≥3 actors)"
else
    echo "⚠️  GAP 2: Only $ACTOR_COUNT actors. Need ≥3. (OpenCode + HERMES + OpenCrawl/organ)"
fi
```

---

## GAP 3: HERMES ↔ OpenCrawl Signal Bridge

### Before (broken)
```
HERMES detects drift → writes to Telegram → Arif sees it → Arif tells OpenCode → OpenCode acts
                                   ↑ MANUAL RELAY ↑
Latency: hours. Arif is the bus.
```

### After (fixed)
```
HERMES detects drift
  → POST /ingest (step_type=Barrier, anomaly=surface_drift)
  → arifFLOW stores barrier receipt
  → flow_state.json writer detects barrier → drops FQ signal
  → OpenCode reads flow_state.json → sees FQ drop + barrier
  → OpenCode auto-triggers forge_surface_audit
  → OpenCode POST /ingest (step_type=Verify, surface_drift=false)
  → FQ rises
  → Loop closed. Latency: seconds.
```

### METRICS — Gap 3 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M3.1 | Barrier receipts accepted | `curl -X POST :7073/ingest -d '{"step_type":"Barrier",...}'` | HTTP 200 |
| M3.2 | Barrier receipts queryable | `curl :7073/barriers` | returns list of barrier receipts |
| M3.3 | Barrier affects FQ | Ingest Barrier, then probe FQ | FQ should reflect pending barrier (at minimum, visible in receipt count) |
| M3.4 | HERMES detects anomaly → Barrier | Trigger hermes_system_status on a down organ | Barrier receipt appears in store |
| M3.5 | OpenCode reads flow_state.json | Script reads flow_state.json, detects barrier | Returns barrier type + affected organ |
| M3.6 | End-to-end latency | Timestamp: anomaly detection → barrier receipt → agent reaction | < 10 seconds |
| M3.7 | No Arif relay required | End-to-end test without Arif touching keyboard | Signal propagates autonomously |
| M3.8 | NATS topics exist (Phase 2) | `nats sub arifflow.barrier.surface_drift` | Messages received when drift detected |

### SELF-TEST script
```bash
#!/bin/bash
# GAP3-VERIFY.sh
echo "=== GAP 3 VERIFICATION ==="

# 1. Can we post a barrier?
BARRIER_RESULT=$(curl -sf -X POST http://localhost:7073/ingest \
  -H 'Content-Type: application/json' \
  -d '{"receipt_id":"test-barrier-1","actor_id":"hermes-prime","session_id":"test","step_type":"Barrier","cost_ns":1000,"epistemic_label":"Observation","floor_verdict":"Pass","created_at":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","step_number":1,"cooling_decision":"None","payload":{"anomaly":"surface_drift","affected_organ":"test"}}')
echo "Barrier ingest: $(echo $BARRIER_RESULT | python3 -c 'import json,sys; print(json.load(sys.stdin).get("status","FAIL"))')"

# 2. Can we query barriers?
BARRIERS=$(curl -sf http://localhost:7073/barriers 2>/dev/null | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")
echo "Barriers in store: $BARRIERS"

if [ "$BARRIERS" -gt 0 ]; then
    echo "✅ GAP 3 BARRIER PATH WORKS"
else
    echo "⚠️  GAP 3: Barrier endpoint may not be wired yet"
fi
```

---

## GAP 4: Federation HOLD Restart Protocol

### Before (broken)
```
FQ < 0.5 → HOLD → ... (nothing) ...
System stays in HOLD forever. No timer. No notification. No exit.
Arif must manually notice and intervene.
```

### After (fixed)
```
T=0s:   FQ < 0.5 → COOLING phase
        All agents: Class 2+ blocked, Class 0 (observe) allowed
        arifFLOW: monitoring verify arrivals
        flow_state.json: cooling=true, phase=cooling, t_remaining=300

T=300s: NOTIFY phase (if still STUCK)
        flow_state.json: cooling=true, phase=notify
        HERMES reads flow_state.json before next output
        HERMES: "Arif, federation HOLD for 5 min. FQ=0.0. Verify missing."

T=600s: SOVEREIGN phase (if still STUCK)
        flow_state.json: cooling=true, phase=sovereign
        HERMES: "Arif, federation stuck for 10 min. Jalan terus?"
        Options: "jalan terus" → override → FQ reset → resume
                 "tunggu" → extend 300s
                 (silence) → remain HOLD

T=any:  If verify arrives → FQ recalculated
        If FQ ≥ 0.5 → auto-resume
        Cooling cleared
```

### METRICS — Gap 4 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M4.1 | FQ<0.5 triggers cooling | Ingest only Execute, no Verify, then probe | `cooling.phase != "Active"` |
| M4.2 | cooling/status endpoint | `curl :7073/cooling/status` | Returns `phase`, `stuck_since`, `t_remaining` |
| M4.3 | Phase transition: COOLING → NOTIFY | Wait 300s after STUCK | `cooling.phase = "Notify"` (if still stuck) |
| M4.4 | Phase transition: NOTIFY → SOVEREIGN | Wait 600s after STUCK | `cooling.phase = "Sovereign"` (if still stuck) |
| M4.5 | Auto-resume on verify arrival | Ingest Verify while in COOLING | `cooling.phase = "Active"`, FQ recalculated |
| M4.6 | Override endpoint | `curl -X POST :7073/cooling/override -d '{"source":"hermes","signal":"jalan_terus"}'` | HTTP 200, `cooling.phase = "Active"`, FQ reset to 1.0 |
| M4.7 | SCAR recorded after override | Check receipt store for Cool+Seal after override | SCAR receipt with `cooling_decision="Hold"` and resolution |
| M4.8 | flow_state.json reflects cooling | `cat /root/AAA/state/flow_state.json` | Contains `cooling` object with phase |
| M4.9 | HERMES notified at NOTIFY phase | Check HERMES output (or log) | Contains "federation HOLD" message |
| M4.10 | HERMES offers options at SOVEREIGN | Check HERMES output at 600s | Contains "jalan terus" / "tunggu" options |

### SELF-TEST script
```bash
#!/bin/bash
# GAP4-VERIFY.sh
echo "=== GAP 4 VERIFICATION ==="

# 1. Check cooling status endpoint exists
COOLING=$(curl -sf http://localhost:7073/cooling/status 2>/dev/null)
if [ -n "$COOLING" ]; then
    echo "Cooling status: $(echo $COOLING | python3 -c 'import json,sys; d=json.load(sys.stdin); print(f\'phase={d.get(\"phase\",\"?\")} t_remaining={d.get(\"t_remaining_s\",\"?\")}s\')')"
    echo "✅ GAP 4: cooling/status endpoint LIVE"
else
    echo "❌ GAP 4: cooling/status endpoint NOT FOUND"
fi

# 2. Check override endpoint
OVERRIDE=$(curl -sf -X POST http://localhost:7073/cooling/override \
  -H 'Content-Type: application/json' \
  -d '{"source":"test","signal":"verify_metrics"}' 2>/dev/null)
if [ -n "$OVERRIDE" ]; then
    echo "Override result: $(echo $OVERRIDE | python3 -c 'import json,sys; print(json.load(sys.stdin).get("status","?"))')"
    echo "✅ GAP 4: cooling/override endpoint LIVE"
else
    echo "⚠️  GAP 4: cooling/override endpoint NOT FOUND (may be HOLD-only)"
fi

# 3. Check flow_state.json has cooling field
if [ -f /root/AAA/state/flow_state.json ]; then
    HAS_COOLING=$(python3 -c "import json; d=json.load(open('/root/AAA/state/flow_state.json')); print('yes' if 'cooling' in d else 'no')")
    if [ "$HAS_COOLING" = "yes" ]; then
        echo "✅ GAP 4: flow_state.json has cooling field"
    else
        echo "⚠️  GAP 4: flow_state.json missing cooling field"
    fi
fi
```

---

## GAP 5: Organ Pulse Measurement

### Before (broken)
```
GEOX, WEALTH, WELL process requests. Zero arifFLOW visibility.
To arifFLOW, these organs don't exist.
```

### After (fixed)
```
Every organ tool invocation produces Execute + Verify receipts.
Failed falsification → Verify receipt with kills=X.
Successful compute → Verify receipt with result summary.
FQ is truly federation-wide — every organ's metabolic load is measured.
```

### METRICS — Gap 5 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M5.1 | GEOX produces Execute receipts | Call `geox_falsify`, then check receipts | ≥1 receipt with `actor_id=geox-falsify`, `step_type=Execute` |
| M5.2 | GEOX produces Verify receipts | After falsify completes, check receipts | ≥1 receipt with `actor_id=geox-falsify`, `step_type=Verify` |
| M5.3 | WEALTH produces Execute receipts | Call `capital_primitive`, then check | ≥1 receipt with `actor_id=wealth-compute`, `step_type=Execute` |
| M5.4 | WEALTH produces Verify receipts | After compute, check | ≥1 receipt with `actor_id=wealth-compute`, `step_type=Verify` |
| M5.5 | WELL produces receipts | Call `well_assess_homeostasis`, then check | ≥1 receipt with `actor_id=well-check` |
| M5.6 | Organ pulse is best-effort | Stop arifFLOW, call geox_falsify | GEOX returns result normally (ingest fails, doesn't block) |
| M5.7 | Payload contains tool info | Check receipt payload | Contains `tool` name and summary result |
| M5.8 | Verified domains in receipt store | `cat /var/lib/arifflow/receipts.jsonl \| python3 -c "..."` | `geox`, `wealth`, `well` all present |

### SELF-TEST script
```bash
#!/bin/bash
# GAP5-VERIFY.sh
echo "=== GAP 5 VERIFICATION ==="

# Count organ actors in receipt store
ORGAN_PULSE=$(tail -100 /var/lib/arifflow/receipts.jsonl 2>/dev/null | python3 -c "
import json,sys
organ_actors={'geox':0,'wealth':0,'well':0}
for l in sys.stdin:
    try:
        r=json.loads(l)
        a=r.get('actor_id','')
        for o in organ_actors:
            if o in a: organ_actors[o]+=1
    except: pass
for o,c in organ_actors.items(): print(f'  {o}: {c} receipts')
missing=[o for o,c in organ_actors.items() if c==0]
print(f'MISSING={len(missing)}')
")
echo "$ORGAN_PULSE"

MISSING=$(echo "$ORGAN_PULSE" | grep MISSING | cut -d= -f2)
if [ "$MISSING" = "0" ]; then
    echo "✅ GAP 5: All 3 organs have pulse receipts"
else
    echo "⚠️  GAP 5: $MISSING organs still invisible to arifFLOW"
fi
```

---

## 2. AGGREGATE SCORECARD — The Eight Metrics Arif Checks

After all gaps closed, this is what Arif should see:

```
╔══════════════════════════════════════════════════════════════════╗
║           AGENTIC ZEN — LIVE METRICS DASHBOARD                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  FQ PULSE                                                        ║
║  ──────────────────────────────────────────────────────────      ║
║  FQ:        2.88        (raw verify/execute ratio)               ║
║  Verdict:   BALANCED    (verify present, ratio healthy)          ║
║  Execute:   8           (across all 6 actors)                    ║
║  Verify:    5           (across all 6 actors)                    ║
║  Stuck-Safe: ACTIVE     (verify=0 → immediate STUCK)             ║
║                                                                  ║
║  COOLING                                                         ║
║  ──────────────────────────────────────────────────────────      ║
║  Phase:     Active      (no HOLD in progress)                    ║
║  Last HOLD: 2026-07-28T18:45:00Z  (resolved in 2.3 min)         ║
║  HOLD Resolution: auto  (verify arrived, FQ auto-resumed)        ║
║                                                                  ║
║  ACTOR PULSE                                                     ║
║  ──────────────────────────────────────────────────────────      ║
║  opencode         ████████░░  E:5 V:3                            ║
║  hermes-prime     ████░░░░░░  E:2 V:1                            ║
║  opencrawl        ██░░░░░░░░  E:1 V:1                            ║
║  geox-falsify     ██░░░░░░░░  E:1 V:0 PENDING                    ║
║  wealth-compute   ██░░░░░░░░  E:1 V:0 PENDING                    ║
║  well-check       ██░░░░░░░░  E:1 V:1                            ║
║                                                                  ║
║  TOTAL ACTORS:    6/6 PULSING    ✅                              ║
║  VERIFY COVERAGE: 5/8 = 62%      🟡 (below 100% — organs pending) ║
║                                                                  ║
║  AGENTIC ZEN SCORE:  8.5/10                                      ║
║  ──────────────────────────────────────────────────────────      ║
║  GAP 1: ✅ CLOSED  (verify=0 → STUCK)                            ║
║  GAP 2: ✅ CLOSED  (≥3 actors pulsing)                           ║
║  GAP 3: ✅ CLOSED  (barrier path wired)                          ║
║  GAP 4: ✅ CLOSED  (cooling countdown active)                    ║
║  GAP 5: ✅ CLOSED  (all organs pulsing)                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 3. THE EIGHT LIVE CHECKS (Arif runs one command)

```bash
curl -s http://localhost:7073/health && echo "---" && cat /root/AAA/state/flow_state.json
```

He should see:
1. **`fq.verdict`** is not BALANCED when verify=0
2. **`cooling`** object exists with phase
3. **`flow_state.json`** has cooling field
4. **`receipts`** count growing over time
5. **Multiple actor_ids** in receipt store

---

## 4. WHAT AGENTS CHECK BEFORE CLAIMING "DONE"

```
BEFORE SEALING ANY GAP:
  □ Run the SELF-TEST script for that gap
  □ Probe :7073/health — verify metric changed
  □ Wait 60 seconds — probe again — metric STILL changed
  □ Check 0 test failures in relevant organ
  □ Ingest a forge_work/ receipt documenting the change
  □ Update AGENTIC_ZEN_GAPS.md status from 🔴 to ✅

NEVER SEAL A GAP ON:
  □ "I changed the code" without test pass
  □ "It should work now" without live probe
  □ Metric changed at T₀ but drifted back at T₁
```

---

## 5. THE FINAL VERDICT (what Arif says)

```
"Gap closed" = Arif runs `make prove`, sees all 8 metrics green, says nothing.
"Gap still open" = any metric red → agent auto-detects and flags.
```

> **DITEMPA BUKAN DIBERI** — Zen is not a destination. Zen is tension sustained by honest measurement. This file is the measurement. Forge against it.

---

*Forged: 2026-07-28 by 333-AGI under F13 directive "tell me what I should expect"*
*Reference: AGENTIC_ZEN_GAPS.md · receipt.rs · fq.ts · hermes_mcp.py · flow_state.json*
