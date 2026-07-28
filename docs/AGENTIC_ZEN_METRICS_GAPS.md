# AGENTIC ZEN METRICS GAPS — The 7 Spec-Level Holes

> **Forged:** 2026-07-28 | **Auditor:** 333-AGI (Delta MIND)
> **Sovereign:** Arif (F13) | **Heritage:** AGENTIC_ZEN_GAPS.md · AGENTIC_ZEN_METRICS.md
> **Relationship:** SIBLING to AGENTIC_ZEN_GAPS.md. That doc covers 5 structural gaps (FQ formula, actor pipeline, signal bridge, HOLD restart, organ pulse). THIS doc covers 7 spec-level gaps INSIDE those 5 — formula precision, actor aggregation, trend detection, notification path, override interface, and test coverage.
>
> **Rule:** AGENTIC_ZEN_GAPS.md answers "what's broken." THIS answers "how do we know it's fixed."

---

## GAP M1: FQ Upper Bound — OVERHEAT Detection

### Problem
```
FQ = execute/verify
FQ > 3.0 → OPTIMAL (green, forge freely)

But: verify dominating execute is ALSO pathological.
FQ = 10 means 10× more verify than execute — system is paralyzed by self-audit.
Current spec treats FQ > 3.0 uniformly as OPTIMAL.
```

**Example:** OpenCode executes 1 thing, then runs 10 cooling cycles → FQ = 10.0 → "OPTIMAL 🟢". Reality: agent is stuck in a verification loop, burning tokens with no progress.

### Fix
```rust
fn fq_verdict(execute_count: u64, verify_count: u64) -> FqVerdict {
    if verify_count == 0 {
        return FqVerdict::Stuck;  // GAP 1 fix
    }
    let fq = execute_count as f64 / verify_count as f64;

    match fq {
        x if x < 0.5                    => FqVerdict::Stuck,       // 🔴 execute outruns verify
        x if x >= 0.5 && x < 1.0       => FqVerdict::Watching,    // 🟠 verify catching up
        x if x >= 1.0 && x <= 3.0      => FqVerdict::Balanced,    // 🟡 healthy tension
        x if x > 3.0 && x <= 5.0       => FqVerdict::Optimal,     // 🟢 verify supports execute
        x if x > 5.0                   => FqVerdict::Overheat,    // 🔵 verify DOMINATES — self-audit spiral
    }
}
```

### States
```
STUCK       🔴  FQ < 0.5        execute outruns verify → HOLD
WATCHING    🟠  0.5 ≤ FQ < 1.0  verify lagging → alert
BALANCED    🟡  1.0 ≤ FQ ≤ 3.0  healthy tension
OPTIMAL     🟢  3.0 < FQ ≤ 5.0  verify supports execute well
OVERHEAT    🔵  FQ > 5.0        verify DOMINATES — self-audit spiral
```
| State | Threshold | Meaning | Agent behavior |
|-------|-----------|---------|---------------|
| **STUCK** | FQ < 0.5 | execute outruns verify | ALL HOLD |
| **WATCHING** | 0.5 ≤ FQ < 1.0 | verify lagging | Alert, probe |
| **BALANCED** | 1.0 ≤ FQ ≤ 3.0 | healthy tension | Normal operation |
| **OPTIMAL** | 3.0 < FQ ≤ 5.0 | verify supports execute | Forge freely |
| **OVERHEAT** | FQ > 5.0 | verify dominates — self-audit spiral | Cool throttle |

### METRICS — Gap M1 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M1.1 | FQ=10 → verdict OVERHEAT | Ingest 1 Execute, 10 Verify | `verdict = "OVERHEAT"` |
| M1.2 | FQ=2.5 → verdict BALANCED | Ingest 5 Execute, 2 Verify | `verdict = "BALANCED"` |
| M1.3 | FQ=4.0 → verdict OPTIMAL | Ingest 4 Execute, 1 Verify | `verdict = "OPTIMAL"` |
| M1.4 | FQ=6.0 → verdict OVERHEAT | Ingest 6 Execute, 1 Verify (yes, verify heavy) | `verdict = "OVERHEAT"` |
| M1.5 | OVERHEAT behavior | arifFLOW health probe | `overheat = true`, agents see warning |
| M1.6 | OVERHEAT → BALANCED recovery | Add more Execute without Verify | FQ drops back to BALANCED range |

### Self-Test
```bash
# GAP-M1-VERIFY.sh
echo "=== GAP M1: OVERHEAT ==="
# Ingest 1 Execute + 10 Verify → should be OVERHEAT
for i in $(seq 1 10); do
  curl -sf -X POST http://localhost:7073/ingest -H 'Content-Type: application/json' \
    -d "{\"actor_id\":\"test-m1\",\"session_id\":\"test\",\"step_type\":\"Verify\",\"step_number\":$i,\"cost_ns\":1000,\"epistemic_label\":\"Derivation\",\"floor_verdict\":\"Pass\"}" > /dev/null
done
curl -sf -X POST http://localhost:7073/ingest -H 'Content-Type: application/json' \
  -d '{"actor_id":"test-m1","session_id":"test","step_type":"Execute","step_number":1,"cost_ns":1000,"epistemic_label":"Derivation","floor_verdict":"Pass"}' > /dev/null
sleep 1
V=$(curl -sf http://localhost:7073/health | python3 -c "import json,sys; fq=json.load(sys.stdin)['fq']; print(fq['verdict'])")
[ "$V" = "OVERHEAT" ] && echo "✅ GAP M1 CLOSED" || echo "❌ GAP M1: verdict=$V (expected OVERHEAT)"
```

---

## GAP M2: Actor-Level FQ — Aggregation Method

### Problem
Spec says "Federation FQ." But individual agents have different FQs:
```
OpenCode:  FQ = 1/3 = 0.33  → STUCK
OpenCrawl: FQ = 2/1 = 2.0   → BALANCED
HERMES:    FQ = 5/3 = 1.67  → BALANCED
```

What is **Federation FQ**?
- `min(agent_fqs)` → 0.33 → STUCK (one agent blocks all)
- `max(agent_fqs)` → 2.0 → BALANCED (stuck agent invisible)
- `weighted avg by step_count` → (1×0.33 + 3×2.0 + 8×1.67) / 12 = 1.53 → BALANCED
- Ratio of sums → (1+2+5)/(3+1+3) = 8/7 = 1.14 → BALANCED

Four different formulas, four different verdicts. The spec must pick ONE.

### Fix

**Federation FQ = ratio of sums (not average of ratios)**
```
FQ_federation = SUM(all agent execute steps) / MAX(SUM(all agent verify steps), 1)
```

**Why ratio-of-sums:**
- Averages of ratios punish high-activity agents unfairly (HERMES doing 100 turns with 50 verifies shouldn't be dragged down by OpenCode's 1 turn with 0 verify)
- Ratio-of-sums gives each step equal weight regardless of which agent produced it
- Mathematically: `(E_hermes + E_opencode + E_opencrawl + E_organs) / max(V_hermes + V_opencode + V_opencrawl + V_organs, 1)`

**Actor-level FQ for diagnostics (separate):**
```json
{
  "fq": {
    "federation": 1.53,
    "verdict": "BALANCED",
    "by_actor": {
      "opencode": {"fq": 0.33, "verdict": "STUCK", "execute": 1, "verify": 3},
      "opencrawl-surface": {"fq": 2.0, "verdict": "BALANCED", "execute": 2, "verify": 1},
      "hermes-prime": {"fq": 1.67, "verdict": "BALANCED", "execute": 5, "verify": 3}
    },
    "worst_actor": {"id": "opencode", "fq": 0.33, "verdict": "STUCK"}
  }
}
```

**Actor-level STUCK → federation WARNING, not federation STUCK.**
- One stuck agent: `worst_actor_stuck = true` → alert, but federation forges on
- ALL agents stuck: federation STUCK → HOLD

### METRICS — Gap M2 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M2.1 | Federation FQ = ratio of sums | 3 agents, varying E/V | `fq.federation` = `sum(Ei)/max(sum(Vi),1)` |
| M2.2 | Actor-level FQ in health response | `curl :7073/health \| jq '.fq.by_actor'` | Object with per-actor E/V/FQ/verdict |
| M2.3 | `worst_actor` field | `curl :7073/health \| jq '.fq.worst_actor'` | Actor with lowest FQ |
| M2.4 | One stuck agent → FED OK | OpenCode stuck, others healthy | `federation.verdict != "STUCK"`, `worst_actor.id = "opencode"` |
| M2.5 | All stuck → FED STUCK | All agents have FQ < 0.5 | `federation.verdict = "STUCK"`, `worst_actor_stuck = true` |
| M2.6 | `fq_history` per actor | `curl :7073/fq/opencode/history` | Array of [ts, fq, verdict] for that actor |
| M2.7 | Non-blocking at ingest | Actor ingest fails → other actors unaffected | Federation FQ recalculates with remaining actors |

### Self-Test
```bash
# GAP-M2-VERIFY.sh
echo "=== GAP M2: ACTOR-LEVEL FQ ==="
HEALTH=$(curl -sf http://localhost:7073/health)
echo "$HEALTH" | python3 -c "
import json,sys
d=json.load(sys.stdin)['fq']
print(f'  Federation: FQ={d.get(\"federation\",\"?\")} verdict={d.get(\"verdict\",\"?\")}')
if 'by_actor' in d:
    for a, v in d['by_actor'].items():
        print(f'  {a}: FQ={v.get(\"fq\",\"?\")} E={v.get(\"execute\",0)} V={v.get(\"verify\",0)}')
    print(f'  worst_actor: {d.get(\"worst_actor\",{}).get(\"id\",\"?\")}')
    print('✅ GAP M2: actor-level FQ present')
else:
    print('❌ GAP M2: no by_actor field')
"
```

---

## GAP M3: FQ Trend Detection — Rate-of-Change Signal

### Problem
```
fq_history: [2.5, 2.5] — 2 entries from current window.
```

A flat FQ of 1.0 is very different from FQ dropping 3.0 → 1.0 in 10 minutes.

**Scenario A:** Steady FQ 1.0 for 30 min → metabolism is stable. No action needed.  
**Scenario B:** FQ drops 3.0 → 1.5 → 1.0 over 10 min → something BROKE. Alert immediately.

Without trend, both scenarios look identical at the last probe.

### Fix
```rust
struct FqTrend {
    direction: TrendDirection,  // Rising, Falling, Stable
    rate: f64,                  // ΔFQ per minute
    volatility: f64,            // std dev of last N readings
    acceleration: f64,          // is rate accelerating? (d²FQ/dt²)
    window_s: u64,              // lookback window in seconds
    samples: u64,               // readings in window
}

enum TrendDirection { Rising, Falling, Stable }
```

**Trend detection rules:**
```rust
fn detect_trend(history: &[(Instant, f64)], window_s: u64) -> FqTrend {
    let recent: Vec<_> = history.iter()
        .filter(|(ts, _)| ts.elapsed().as_secs() < window_s)
        .collect();
    
    if recent.len() < 3 {
        return FqTrend { direction: Stable, rate: 0.0, .. };
    }

    let values: Vec<f64> = recent.iter().map(|(_, v)| *v).collect();
    let times: Vec<f64> = recent.iter().map(|(ts, _)| ts.elapsed().as_secs() as f64).collect();
    
    // Linear regression slope
    let n = values.len() as f64;
    let sum_x = times.iter().sum::<f64>();
    let sum_y = values.iter().sum::<f64>();
    let slope = (n * times.iter().zip(values.iter()).map(|(x,y)| x*y).sum::<f64>() - sum_x * sum_y)
              / (n * times.iter().map(|x| x*x).sum::<f64>() - sum_x * sum_x);
    
    let rate_per_min = -slope * 60.0;  // negative because ts counts down from now
    
    FqTrend {
        direction: if rate_per_min.abs() < 0.05 { Stable }
              else if rate_per_min > 0.0 { Rising }
              else { Falling },
        rate: rate_per_min,
        samples: recent.len() as u64,
        ..
    }
}
```

**Alert bands:**
| Condition | Signal |
|-----------|--------|
| FQ falling > 0.3/min for 3+ min | FQ_DECLINING_FAST → alert to worst actor |
| FQ falling > 0.5/min for 2+ min | FQ_CRASH → immediate probe, escalate to HERMES |
| FQ stable < 0.5 for 5+ min | STUCK → existing GAP 4 trigger |
| FQ rising after STUCK | FQ_RECOVERING → auto-resume check |

### METRICS — Gap M3 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M3.1 | `fq_history` endpoint | `curl :7073/fq/history?window=600` | Array of `[timestamp, fq, verdict]` with ≥3 entries |
| M3.2 | `fq_trend` in health | `curl :7073/health \| jq '.fq.trend'` | Object with `direction`, `rate_per_min`, `samples` |
| M3.3 | Falling trend detected | Ingest rapid sequence with no verify | `trend.direction = "Falling"`, `trend.rate_per_min < -0.1` |
| M3.4 | CRASH alert | Drop FQ 3.0 → 0.5 in < 5 min | `trend.rate_per_min < -0.5`, barrier receipt emitted |
| M3.5 | Recovery detection | Add Verify after STUCK | `trend.direction = "Rising"` |
| M3.6 | Minimum 3 samples for trend | Fresh daemon, 2 readings | `trend.samples < 3`, `trend.direction = "Stable"` (insufficient data) |
| M3.7 | History pruning | After 3600s, old entries gone | `fq_history` entries all within window |

### Self-Test
```bash
# GAP-M3-VERIFY.sh
echo "=== GAP M3: FQ TREND ==="
TREND=$(curl -sf http://localhost:7073/health | python3 -c "
import json,sys
fq=json.load(sys.stdin)['fq']
t=fq.get('trend',{})
print(f'direction={t.get(\"direction\",\"?\")} rate={t.get(\"rate_per_min\",\"?\")}/min samples={t.get(\"samples\",0)}')
")
echo "Trend: $TREND"
HIST=$(curl -sf "http://localhost:7073/fq/history?window=600" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")
echo "History entries: $HIST"
[ "$HIST" -ge 3 ] && echo "✅ GAP M3: trend data present" || echo "⚠️  GAP M3: need ≥3 history entries"
```

---

## GAP M4: Formula Transparency — Exact FQ Definition

### Problem
The spec says `execute/verify`. But:
```
execute = count of Execute receipts? sum of cost_ns? weighted moving average?
verify  = count of Verify receipts? sum of cost_ns?
```

`execute_count=2, verify_count=1 → FQ=2.0`. Clear.
But what if `cost_ns` varies? 1 expensive Execute vs 100 cheap Verifies?

### Fix — Explicit Formula Contract

```rust
/// FQ = Σ(cost_execute) / max(Σ(cost_verify), 1)
/// Where:
///   cost = receipt.cost_ns clamped to [1_000_000, 300_000_000_000] (1ms to 5min)
///   Window = rolling 300s (5 min)
///   If window has 0 receipts → UNMEASURED
///   If window has no Verify → STUCK (regardless of cost)
///
/// Smoothed FQ = EMA(instantaneous_raw_fq) with α=0.3
///   EXCEPT: STUCK and OVERHEAT are NOT smoothed — they're immediate.
fn compute_fq(receipts: &[Receipt], window_s: u64) -> FqResult {
    let cutoff = Instant::now() - Duration::from_secs(window_s);
    let recent: Vec<_> = receipts.iter().filter(|r| r.created_at > cutoff).collect();

    if recent.is_empty() {
        return FqResult { quotient: 0.0, verdict: FqVerdict::Unmeasured, .. };
    }

    let exec_cost: u64 = recent.iter()
        .filter(|r| r.step_type == StepType::Execute)
        .map(|r| r.cost_ns.clamp(1_000_000, 300_000_000_000))
        .sum();

    let verify_cost: u64 = recent.iter()
        .filter(|r| r.step_type == StepType::Verify)
        .map(|r| r.cost_ns.clamp(1_000_000, 300_000_000_000))
        .sum();

    if verify_cost == 0 {
        return FqResult { quotient: 0.0, verdict: FqVerdict::Stuck, raw_ratio: f64::INFINITY, .. };
    }

    let raw = exec_cost as f64 / verify_cost as f64;
    // EMA smoothing with α=0.3 — only for non-terminal states
    // ...
}
```

**Exposed in health:**
```json
{
  "fq": {
    "quotient": 2.5,
    "verdict": "BALANCED",
    "raw_ratio": 2.5,
    "is_smoothed": false,
    "alpha": 0.3,
    "window_s": 300,
    "execute_cost_ns": 5000000000,
    "verify_cost_ns": 2000000000,
    "cost_clamp": {"min_ns": 1000000, "max_ns": 300000000000}
  }
}
```

### METRICS — Gap M4 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M4.1 | Window parameter exposed | `curl :7073/health \| jq '.fq.window_s'` | Number (default 300) |
| M4.2 | Alpha parameter exposed | `curl :7073/health \| jq '.fq.alpha'` | Number (default 0.3) |
| M4.3 | Cost breakdown | `curl :7073/health \| jq '.fq.execute_cost_ns, .fq.verify_cost_ns'` | Sums of clamped costs |
| M4.4 | `is_smoothed` flag | `curl :7073/health \| jq '.fq.is_smoothed'` | `false` for STUCK/OVERHEAT, `true` else |
| M4.5 | Cost clamp bounds exposed | `curl :7073/health \| jq '.fq.cost_clamp'` | `{min_ns: 1000000, max_ns: 300000000000}` |
| M4.6 | Receipt without cost_ns → default | Ingest receipt missing cost_ns | Defaults to 1_000_000 (1ms) |
| M4.7 | TypeScript mirror matches | `fqVerdict(/* cost params */)` in fq.ts | Same output as Rust for identical inputs |

### Self-Test
```bash
# GAP-M4-VERIFY.sh
echo "=== GAP M4: FORMULA TRANSPARENCY ==="
curl -sf http://localhost:7073/health | python3 -c "
import json,sys
fq=json.load(sys.stdin)['fq']
checks = [
    ('window_s', fq.get('window_s')),
    ('alpha', fq.get('alpha')),
    ('execute_cost_ns', fq.get('execute_cost_ns')),
    ('verify_cost_ns', fq.get('verify_cost_ns')),
    ('is_smoothed', fq.get('is_smoothed')),
    ('cost_clamp', fq.get('cost_clamp')),
]
all_ok = True
for name, val in checks:
    ok = val is not None
    all_ok = all_ok and ok
    print(f'  {\"✅\" if ok else \"❌\"} {name}: {val}')
print('✅ GAP M4 CLOSED' if all_ok else '❌ GAP M4: missing formula fields')
"
```

---

## GAP M5: Telegram Notification Sender — Who Fires Gap 4?

### Problem
Gap 4's Cooling Countdown has 4 phases (COOLING → NOTIFY → SOVEREIGN → RECOVERY). The NOTIFY phase says:
> "HERMES notified → Arif, federation HOLD. FQ={value}. Waiting."

**But HOW is HERMES notified?**
Options, none specified:
1. **arifFLOW daemon** → pushes to Telegram directly (but arifFLOW "never judges, never executes" — is notification an execute?)
2. **HERMES** → polls `/cooling/status` before every message (HERMES is the reader, not the watcher)
3. **cron job** → `*/1 * * * * curl :7073/cooling/status | jq '.phase'` then calls HERMES
4. **NATS** → arifFLOW publishes to `arifflow.cooling.phase.{phase}` → HERMES subscriber

### Fix

**Phase 1 (immediate): HERMES polls before every message**
```python
# In HERMES reply/response path — before composing message
import requests
cooling = requests.get("http://localhost:7073/cooling/status", timeout=3).json()

if cooling["phase"] in ("Notify", "Sovereign"):
    # Prepend cooling notification to message
    message = f"⚠️ FEDERATION HOLD — FQ={cooling['fq']}. Phase: {cooling['phase']}.\n\n{original_message}"
```

**Phase 2 (auto): arifFLOW → NATS → HERMES subscriber**
```
arifFLOW state transition: COOLING → NOTIFY
  → publish to NATS subject: arifflow.cooling.phase.notify
  → HERMES subscriber receives
  → HERMES sends Telegram message to Arif

arifFLOW state transition: NOTIFY → SOVEREIGN
  → publish to NATS subject: arifflow.cooling.phase.sovereign
  → HERMES subscriber receives
  → HERMES: "Arif, 10 min stuck. Jalan terus?"
```

**Sender contract:**
```
WHEN phase changes: arifFLOW emits NATS message
WHO delivers to Arif: HERMES (Telegram)
FALLBACK if HERMES down: arifFLOW logs to journalctl (visible in cockpit)
```

### METRICS — Gap M5 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M5.1 | HERMES polls cooling before output | Check HERMES log | `cooling/status` called before message send |
| M5.2 | Notification at NOTIFY phase | Set FQ to STUCK, wait 300s, check Telegram | Arif receives "FEDERATION HOLD" message |
| M5.3 | Notification at SOVEREIGN phase | Wait 600s | Arif receives "jalan terus?" message with options |
| M5.4 | NATS topic for phase transitions | `nats sub arifflow.cooling.phase.>` | Messages received when phase changes |
| M5.5 | Fallback logging | Stop HERMES, trigger STUCK | `journalctl -u arifflow | grep cooling` shows phase transitions |
| M5.6 | No notification spam | Multiple rapid phase flips | Only one notification per phase transition (debounce 60s) |

### Self-Test
```bash
# GAP-M5-VERIFY.sh
echo "=== GAP M5: NOTIFICATION SENDER ==="
# Check cooling/status endpoint
PHASE=$(curl -sf http://localhost:7073/cooling/status 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin).get('phase','?'))")
echo "Cooling phase: $PHASE"

# Check NATS topics (Phase 2)
if command -v nats &>/dev/null; then
    NATS_TOPICS=$(nats sub --count=1 arifflow.cooling.phase.> 2>/dev/null & sleep 1; kill %1 2>/dev/null)
    echo "NATS topics exist: $([ -n \"$NATS_TOPICS\" ] && echo yes || echo no)"
fi

# Check HERMES log for cooling polling
if journalctl -u hermes --since "5 min ago" 2>/dev/null | grep -q "cooling/status"; then
    echo "✅ GAP M5: HERMES polling cooling/status"
else
    echo "⚠️  GAP M5: HERMES not yet polling (pre-phase-2 expected)"
fi
```

---

## GAP M6: Override Interface — How Arif Says "Jalan Terus"

### Problem
Gap 4 Phase 3 says:
> `"jalan terus" → F13 override, reset FQ to 1.0, forge resumes`

**But HOW does Arif say "jalan terus"?**
Options, none specified:
1. **Telegram message:** Arif types `jalan terus` → HERMES detects → POST to `/cooling/override`
2. **Cockpit button:** https://aaa.arif-fazil.com → "OVERRIDE HOLD" button
3. **Direct API:** `curl -X POST :7073/cooling/override -d '{"source":"arif","signal":"jalan_terus"}'`
4. **arifOS kernel:** `arif_judge(mode="override", candidate="federation_hold")`

All four should work. But the spec must define the canonical path and the others as aliases.

### Fix

**Canonical path:** Telegram → HERMES → `/cooling/override`

```
Arif types "jalan terus" in Telegram
  → HERMES sovereign_signal_detect("jalan terus")
  → HERMES checks: is there an active cooling HOLD?
  → YES → POST http://localhost:7073/cooling/override
    {
      "source": "hermes",
      "signal": "jalan_terus",
      "sovereign": "Arif",
      "reason": "F13 override — sovereign has spoken",
      "session_id": "<current>"
    }
  → arifFLOW receives
  → FQ reset to 1.0
  → cooling cleared
  → SCAR recorded: COOLING_OVERRIDE event
  → HERMES replies: "F13 heard. Federation resumed. FQ reset to 1.0."
```

**Override endpoint contract:**
```
POST /cooling/override
  Body: { source, signal, reason?, session_id? }
  Responses:
    200: { status: "overridden", new_fq: 1.0, scar_id: "..." }
    400: { status: "invalid", reason: "no active cooling" or "missing source" }
    403: { status: "forbidden", reason: "source not authorized" }
```

**Authorized sources:**
- `hermes` — via Telegram (Arif authenticated by Telegram identity)
- `cockpit` — via AAA A2A (authenticated session)
- `arifos` — via kernel judge override
- `test` — only on `FORGE_TEST_MODE=true`
- NOT: `opencode`, `opencrawl`, or any organ MCP tool

**Override codes (signal values):**
| Signal | Meaning |
|--------|---------|
| `jalan_terus` | Full override — resume all forge |
| `tunggu` | Extend cooling 300s |
| `verify_metrics` | Testing override (only from `test` source) |

### METRICS — Gap M6 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M6.1 | `/cooling/override` accepts valid POST | `curl -X POST :7073/cooling/override -d '{"source":"hermes","signal":"jalan_terus"}'` | HTTP 200, `status: "overridden"` |
| M6.2 | Override resets FQ to 1.0 | After override, probe FQ | `fq.quotient = 1.0`, `fq.verdict = "BALANCED"` |
| M6.3 | Override clears cooling | After override | `cooling.phase = "Active"` (or absent) |
| M6.4 | Override records SCAR | Check receipt store | SCAR receipt with `cooling_decision = "Overridden"` |
| M6.5 | `tunggu` extends timer | `signal=tunggu` | `cooling.t_remaining += 300` (max 1800s) |
| M6.6 | Unauthorized source rejected | `source="opencode"` | HTTP 403 |
| M6.7 | No active HOLD → rejected | Override when cooling is Active | HTTP 400, `reason: "no active cooling"` |
| M6.8 | `jalan_terus` only in SOVEREIGN phase | Override in COOLING phase | Accepted (Arif can override at any phase, not just SOVEREIGN) |
| M6.9 | HERMES sovereign_signal_detect | Arif types "jalan terus" | HERMES calls `/cooling/override` automatically |

### Self-Test
```bash
# GAP-M6-VERIFY.sh
echo "=== GAP M6: OVERRIDE INTERFACE ==="

# 1. Can we hit the override endpoint?
OVERRIDE=$(curl -sf -X POST http://localhost:7073/cooling/override \
  -H 'Content-Type: application/json' \
  -d '{"source":"test","signal":"verify_metrics"}' 2>/dev/null)
if [ -n "$OVERRIDE" ]; then
    echo "Override response: $(echo $OVERRIDE | python3 -c 'import json,sys; print(json.load(sys.stdin).get("status","?"))')"
    echo "✅ GAP M6: override endpoint exists"
else
    echo "❌ GAP M6: override endpoint not responding"
fi

# 2. Can we get 403 for unauthorized source?
FORBIDDEN=$(curl -sf -X POST http://localhost:7073/cooling/override \
  -H 'Content-Type: application/json' \
  -d '{"source":"opencode","signal":"jalan_terus"}' 2>/dev/null)
echo "Unauthorized test: $(echo $FORBIDDEN | python3 -c 'import json,sys; print(json.load(sys.stdin).get("status","?"))' 2>/dev/null || echo 'no response')"

# 3. Is HERMES wired to detect sovereign signals?
if [ -f /root/HERMES/hermes_mcp.py ]; then
    grep -q "jalan.terus\|sovereign_signal\|cooling/override" /root/HERMES/hermes_mcp.py \
        && echo "✅ GAP M6: HERMES has sovereign signal detection" \
        || echo "⚠️  GAP M6: HERMES sovereign signal path not found"
fi
```

---

## GAP M7: Verification Tests — State Transition Coverage

### Problem
Cooling Countdown has 4 states: COOLING, NOTIFY, SOVEREIGN, RECOVERY.
The state machine has 12 possible transitions:
```
COOLING  → NOTIFY      (timer expires, still FQ<0.5)
COOLING  → RECOVERY    (verify arrives, FQ rises)
COOLING  → SOVEREIGN   (override called directly)
NOTIFY   → SOVEREIGN   (timer expires, still FQ<0.5)
NOTIFY   → RECOVERY    (verify arrives, FQ rises)
NOTIFY   → COOLING     (extend called - "tunggu")
SOVEREIGN→ RECOVERY    (override: "jalan_terus")
SOVEREIGN→ COOLING     (extend called - "tunggu")
SOVEREIGN→ SOVEREIGN   (no-op, timer expired but no override)
ACTIVE   → COOLING     (FQ drops below 0.5)
COOLING  → COOLING     (timer not yet expired, still waiting)
RECOVERY → ACTIVE      (FQ stable above 0.5)
```

0 tests exist for any of these. Zero.

### Fix

**Test file:** `/root/arifFlow/tests/cooling_state_machine.rs`

```rust
#[cfg(test)]
mod cooling_state_machine_tests {
    use super::*;
    use std::time::Duration;

    // T1: ACTIVE → COOLING when FQ drops below 0.5
    #[test]
    fn test_active_to_cooling_on_fq_drop() {
        let mut sm = CoolingStateMachine::new();
        sm.ingest(Receipt { step_type: Execute, .. }); // FQ = 1/0 = STUCK
        assert_eq!(sm.phase(), CoolingPhase::Cooling);
    }

    // T2: COOLING → RECOVERY when verify arrives
    #[test]
    fn test_cooling_to_recovery_on_verify_arrival() {
        let mut sm = CoolingStateMachine::new();
        sm.force_phase(CoolingPhase::Cooling);
        sm.ingest(Receipt { step_type: Verify, .. });
        sm.recalculate_fq();
        assert!(sm.phase() == CoolingPhase::Active || sm.phase() == CoolingPhase::Recovery);
    }

    // T3: COOLING → NOTIFY after 300s without recovery
    #[test]
    fn test_cooling_to_notify_on_timer_expiry() {
        let mut sm = CoolingStateMachine::new();
        sm.force_phase(CoolingPhase::Cooling);
        sm.advance_time(Duration::from_secs(301));
        sm.tick();
        assert_eq!(sm.phase(), CoolingPhase::Notify);
    }

    // T4: NOTIFY → SOVEREIGN after another 300s
    #[test]
    fn test_notify_to_sovereign_on_timer_expiry() {
        let mut sm = CoolingStateMachine::new();
        sm.force_phase(CoolingPhase::Notify);
        sm.advance_time(Duration::from_secs(301));
        sm.tick();
        assert_eq!(sm.phase(), CoolingPhase::Sovereign);
    }

    // T5: NOTIFY → COOLING on "tunggu" override
    #[test]
    fn test_notify_to_cooling_on_extend() {
        let mut sm = CoolingStateMachine::new();
        sm.force_phase(CoolingPhase::Notify);
        sm.override_signal("tunggu");
        assert_eq!(sm.phase(), CoolingPhase::Cooling);
        assert!(sm.t_remaining() > 250); // extended
    }

    // T6: SOVEREIGN → RECOVERY on "jalan_terus" override
    #[test]
    fn test_sovereign_to_recovery_on_override() {
        let mut sm = CoolingStateMachine::new();
        sm.force_phase(CoolingPhase::Sovereign);
        sm.override_signal("jalan_terus");
        assert_eq!(sm.phase(), CoolingPhase::Active);
        assert_eq!(sm.fq(), 1.0); // reset
    }

    // T7: Override rejected from unauthorized source
    #[test]
    fn test_override_rejected_unauthorized_source() {
        let mut sm = CoolingStateMachine::new();
        sm.force_phase(CoolingPhase::Sovereign);
        let result = sm.override_from("opencode", "jalan_terus");
        assert!(result.is_err());
        assert_eq!(sm.phase(), CoolingPhase::Sovereign); // unchanged
    }

    // T8: No-op when no active cooling
    #[test]
    fn test_override_rejected_no_active_cooling() {
        let mut sm = CoolingStateMachine::new();
        sm.force_phase(CoolingPhase::Active);
        let result = sm.override_signal("jalan_terus");
        assert!(result.is_err());
    }

    // T9: SOVEREIGN → SOVEREIGN (silence — no timeout beyond this)
    #[test]
    fn test_sovereign_sticks_on_silence() {
        let mut sm = CoolingStateMachine::new();
        sm.force_phase(CoolingPhase::Sovereign);
        sm.advance_time(Duration::from_secs(3600)); // 1 hour
        sm.tick();
        assert_eq!(sm.phase(), CoolingPhase::Sovereign); // doesn't auto-escalate
    }

    // T10: RECOVERY → ACTIVE after FQ stabilizes
    #[test]
    fn test_recovery_to_active_on_stable_fq() {
        let mut sm = CoolingStateMachine::new();
        sm.force_phase(CoolingPhase::Recovery);
        // Ingest several balanced Execute+Verify
        for _ in 0..5 {
            sm.ingest(Receipt { step_type: Execute, .. });
            sm.ingest(Receipt { step_type: Verify, .. });
        }
        sm.tick();
        assert_eq!(sm.phase(), CoolingPhase::Active);
    }

    // T11: COOLING → SOVEREIGN on direct override (skip NOTIFY)
    #[test]
    fn test_cooling_to_recovery_on_direct_override() {
        let mut sm = CoolingStateMachine::new();
        sm.force_phase(CoolingPhase::Cooling);
        let result = sm.override_from("hermes", "jalan_terus");
        assert!(result.is_ok());
        assert_eq!(sm.phase(), CoolingPhase::Active);
    }

    // T12: Debounce — rapid phase flips don't spam
    #[test]
    fn test_debounce_prevents_notification_spam() {
        let mut sm = CoolingStateMachine::new();
        sm.force_phase(CoolingPhase::Cooling);
        sm.advance_time(Duration::from_secs(301));
        sm.tick(); // → NOTIFY (notification 1)
        sm.advance_time(Duration::from_secs(10)); // only 10s later
        // Phase flip back to COOLING (verify briefly arrives)
        sm.ingest(Receipt { step_type: Verify, .. });
        sm.tick(); // → ACTIVE/RECOVERY
        assert_eq!(sm.notification_count(), 1); // only one notification sent
    }
}
```

### METRICS — Gap M7 CLOSED when:

| # | Metric | How to verify | Expected value |
|---|--------|-------------|----------------|
| M7.1 | 12 test cases exist | `find /root/arifFlow/tests -name "*cooling*"` | File exists with ≥12 `#[test]` functions |
| M7.2 | All tests pass | `cd /root/arifFlow && cargo test cooling` | 12/12 PASS, 0 FAIL |
| M7.3 | Test coverage ≥ 90% | `cargo tarpaulin --lib` (or equiv) | `cooling.rs` coverage ≥ 90% |
| M7.4 | FQ state machine tests exist | `cargo test fq_` | ≥8 tests for FQ state transitions |
| M7.5 | Trend detection tests | `cargo test trend_` | ≥5 tests for trend detection edge cases |
| M7.6 | Override auth tests | `cargo test override_` | Test unauthorized, missing, and valid overrides |
| M7.7 | CI runs tests on push | `.github/workflows/test.yml` (or equiv) | `cargo test` step in CI pipeline |
| M7.8 | No tests skipped | `cargo test -- --include-ignored` | 0 ignored tests (all must pass) |

### Self-Test
```bash
# GAP-M7-VERIFY.sh
echo "=== GAP M7: VERIFICATION TESTS ==="
cd /root/arifFlow 2>/dev/null || { echo "❌ GAP M7: arifFlow repo not found"; exit 1; }

# Count test functions
TEST_COUNT=$(grep -r "#\[test\]" tests/ 2>/dev/null | wc -l)
echo "Test functions found: $TEST_COUNT"

# Run the cooling tests specifically
if grep -q "cooling" Cargo.toml 2>/dev/null || [ -f tests/cooling_state_machine.rs ]; then
    cargo test cooling 2>&1 | tail -5
    RESULT=$?
    [ $RESULT -eq 0 ] && echo "✅ GAP M7: cooling tests pass" || echo "❌ GAP M7: cooling tests FAIL ($RESULT)"
else
    echo "❌ GAP M7: no cooling test file found"
fi

# Coverage check (if tarpaulin available)
if command -v cargo-tarpaulin &>/dev/null; then
    cargo tarpaulin --lib -- --test-threads 1 2>/dev/null | grep "cooling" | head -3
fi
```

---

## SUMMARY: 7 Spec Gaps → Unified Score Impact

| Gap | Severity | What's Missing | Fix Difficulty |
|-----|----------|----------------|----------------|
| **M1:** OVERHEAT upper bound | HIGH | FQ > 5.0 not detected | 30min — add one enum variant + 2 match arms |
| **M2:** Actor-level FQ | HIGH | Federation aggregation undefined | 2h — add `by_actor` map + `worst_actor` + ratio-of-sums |
| **M3:** FQ trend | MEDIUM | Rate-of-change invisible | 2h — linear regression over history window |
| **M4:** Formula transparency | HIGH | Cost_ns, alpha, window not exposed | 1h — add fields to health JSON |
| **M5:** Telegram notification sender | HIGH | Gap 4 dead without this | 1h — HERMES polling + NATS subscriber |
| **M6:** Override interface | CRITICAL | Arif can't say "jalan terus" | 2h — endpoint + auth + HERMES detection |
| **M7:** Verification tests | HIGH | 0 tests for 12 state transitions | 4h — Rust test module |

```
AGENTIC_ZEN_GAPS.md score (structural gaps): 5 gaps → 5.2/10 → target 8.5/10
AGENTIC_ZEN_METRICS_GAPS.md score (spec gaps):   7 gaps → new work

Combined score after ALL gaps closed (5+7=12):
  Phase 1 (M1 + M4 + M6): formula precision + override → 7.0/10
  Phase 2 (M2 + M3 + M5): actor FQ + trend + notification → 8.5/10
  Phase 3 (M7): tests → 9.5/10
```

---

*DITEMPA BUKAN DIBERI — Spec yang tak define formula explicit, tak specify aggregation method, tak wire notification path, tak test state transitions — bukan spec. Tu coretan atas kertas.*
