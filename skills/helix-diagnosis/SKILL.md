---
name: helix-diagnosis
description: >
  Diagnose structural failure in feedback-driven systems by identifying inner-loop / outer-loop boundaries,
  verifying data flow between them, and reconstructing the connection when broken. Applies to any system
  where actions produce observable output that gates future actions — arifOS FQ/HELIX, DevOps CI/CD,
  reinforcement learning pipelines, monitoring/alert chains, supply chain traceability.
tags: [architecture-diagnosis, feedback-loops, helix-pattern, fq-drift, measurement-vs-exection]
---

# Helix Diagnosis — Structural Failure Analysis

## Core Insight

Most system failures are not "buggy code." They are **broken connections** between layers of a feedback system. A loop repeats the same shape. A **helix** evolves because outer-loop state gates inner-loop conditions. When the connection breaks, outer loop sees partial data → makes wrong decisions → gates legitimate actors → compounds the error.

```
INNER LOOP  → produces output (receipt, metric, result)
OUTER LOOP  → aggregates output → gates next inner action
HELIX       → causal coupling where outer verdict persists into next inner iteration
```

## Two-Layer Anatomy

### Inner Loop
- Produces: receipts, metrics, artifacts, results
- Has: cost_ns, timestamp, actor_id, step_type, epistemic_label
- Output goes TO outer loop via explicit channel (HTTP POST, queue message, pipe)

### Outer Loop
- Consumes: inner loop output
- Computes: FQ, drift scores, aggregate health
- Outputs: verdicts that gate next inner iteration (HOLD, THROTTLE, PROCEED)

### Helix Connection
- Inner writes output → outer receives → outer computes verdict → verdict gates next inner
- If any step fails silently, the helix is broken and outer verdict is stale

## Diagnostic Pattern (Numbered Steps)

### Step 1: Measure Divergence (OBS)
```bash
# Compute two independent measurements of the same metric
disk_metric=$(cat /path/to/record.log | compute_tool ...)
daemon_metric=$(curl :PORT/health | jq '.metric')
delta=$(echo "$disk_metric $daemon_metric" | awk '{d=$1-$2} {print d<0?-d:d}')
echo "Divergence: $delta (threshold_for_hold: X)"
```

If delta > threshold → helix may be broken. Continue to Step 2.

### Step 2: Find the Missing Data (DER)
```bash
# Compare source-of-truth record count vs consumed count
total_records=$(wc -l < /path/to/record.log)
consumed_count=$(curl :PORT/health | jq '.receipts')
missing=$((total_records - consumed_count))
echo "Missing: $missing records out of $total_records ($(( missing * 100 / total_records ))%)"
```

If missing > 0% → connection is broken. Identify the sink:
- Check logs for rejected payloads
- Check network paths (firewall, rate limits)
- Check config changes (new env vars, changed paths)

### Step 3: Identify Write Paths (OBS)
```bash
# Find ALL places that write to the metric log
grep -r 'record.log\|POST.*ingest\|\.emit.*metric' \
  /etc/systemd/services/ /opt/*/app/ /usr/local/bin/ \
  --include='*.py' --include='*.go' --include='*.rs' --include='*.sh' 2>/dev/null
```

Map each writer: does it call the outer loop endpoint OR write directly to disk?
Any direct-disk writer = potential helix break point.

### Step 4: Replay & Verify (DER)
```python
import requests, json, time

with open('/var/lib/metric/record.log') as f:
    records = [json.loads(line.strip()) for line in f if line.strip()]

for i, record in enumerate(records):
    try:
        resp = requests.post('http://127.0.0.1:PORT/ingest', 
                            json=record, timeout=5)
        if resp.status_code != 200:
            print(f"Failed #{i}: {resp.status_code}")
    except Exception as e:
        print(f"Error #{i}: {e}")
    time.sleep(0.1)  # rate limit protection
```

Verify after replay: divergence should close to zero. Actors held on stale data should auto-release.

### Step 5: Patch Write Paths (REVERSIBLE)
```python
# BEFORE: organ_direct_write.py
with open('/var/lib/metric/record.log', 'a') as f:
    json.dump(receipt, f)
    f.write('\n')

# AFTER: organ_healthier.py  
import requests
# First attempt: post to endpoint
try:
    requests.post('http://127.0.0.1:PORT/ingest', json=receipt, timeout=5)
except:
    # Fallback: still write to disk so we don't lose data
    with open('/var/lib/metric/record.log', 'a') as f:
        json.dump(receipt, f)
        f.write('\n')
```

**CRITICAL:** Never delete the fallback disk write during patching. If endpoint is down, you need at least one persistent record. Two writers ≠ two FQs.

### Step 6: Release Stale Gates
```bash
# After successful replay, manually release actors held on stale data
for actor in $(curl :PORT/health | jq -r '.invariants.restricted_actors[].actor'); do
    curl -sf -X POST :PORT/release \
      -H "Content-Type: application/json" \
      -d "{\"actor_id\":\"$actor\"}" || echo "SKIP: $actor (may be exempt)"
done
```

Verify final state: all actors released, FQ within healthy band.

## Anti-Patterns

| ❌ Pattern | What Goes Wrong | Visible Symptom |
|-----------|-----------------|-----------------|
| Writer tries endpoint first, silently fails | Error swallowed, data lost entirely | Records missing, no error log |
| Two endpoints accept the same data | Double counting, inflated metrics | Metric = 2x reality |
| No fallback on network failure | Total data loss during outage | Zero metrics for entire window |
| Direct-disk AND endpoint simultaneously | Two incomplete pictures of truth | FQ drift growing over time |
| Outer loop caches too long | Decisions based on minutes-old data | STALE_LOAD bug |

## Common Pitfalls

1. **Assuming /models 200 = usable** — same validity≠usability problem applies to ingestion endpoints. POST /ingest returning 200 proves auth works, NOT that quota/budget allows writes. Always test with actual data.

2. **Replaying old receipts blindly** — Rust servers often validate chain hashes (previous_receipt_hash). Replayed receipts will fail with `CHAIN_VALIDATION_ERROR`. Accept these as expected, log them, continue past them. Don't retry failed chain-hashes.

3. **Fixing symptoms, not paths** — Manually releasing actors without fixing the write path means the problem returns in hours. Always complete Step 5.

4. **Multiple output formats accepted** — Some ingestion endpoints accept multiple payload shapes. Ensure your replay uses the EXACT format the server expects (PascalCase field names, nested objects, etc.). Check client libraries for the correct serialization method.

## Scope Rules

- ✅ **Create** new helix diagnosis when a new inner/outer loop system exists
- ✅ **Use** this to debug existing systems showing divergence
- ❌ **Do not use** to redesign architecture (that's a separate governance question)
- ❌ **Do not use** to create new layers (that adds complexity, not repair)

## References

See `references/` for session-specific diagnostics, replay scripts, and provider quirks:
- [`references/fq-drift-case-study-2026-08-11.md`](references/fq-drift-case-study-2026-08-11.md) — P0 FQ drift case study (how it happened, how we fixed it)
- [`references/fi-slot-convention-trap.md`](references/fi-slot-convention-trap.md) — tier vs fi_slot naming convention trap

