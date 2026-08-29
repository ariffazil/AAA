# PRIMARY Harness Demotion Criteria

> **Status:** v1.0 · IMPLEMENTED (T3 partially live via RSI ledger; T1/T2 require infrastructure)
> **Forged:** 2026-08-09 by 333-AGI under F13 directive
> **Carry-forward:** PRIMARY-DEMOTION-CRITERIA → IMPLEMENTED (gaps documented)

## Context

OpenCode (FI-001) is designated PRIMARY coding harness per F13 SOVEREIGN directive (2026-08-08). All coding missions route through OpenCode first; vendor harnesses (Kimi, Codex, Claude Code, Grok) are secondary fallback.

No criteria exist for when OpenCode should lose this designation.

## Trigger Conditions (any one fires demotion review)

### T1: Capability Miss Rate
- **Condition:** OpenCode fails to match capability signature for ≥3 consecutive coding missions that other harnesses can handle
- **Measurement:** Dispatch router logs — `capability_match: false` count
- **Window:** Rolling 10 missions
- **Threshold:** ≥3 capability misses

### T2: Latency Drift
- **Condition:** OpenCode median latency exceeds 2× the median of the fastest secondary harness for the same mission class
- **Measurement:** FED route latency table (`fed_report_latency`)
- **Window:** Rolling 20 missions
- **Threshold:** 2× multiplier sustained for ≥5 missions

### T3: Error Rate
- **Condition:** OpenCode produces errors (build failures, test failures, incorrect output) at >2× the rate of the best secondary harness
- **Measurement:** RSI ledger error classifications + scar ledger
- **Window:** Rolling 20 missions
- **Threshold:** 2× error multiplier sustained for ≥5 missions

## Demotion Process

1. **Detect:** 555-ASI monitors T1-T3 triggers continuously
2. **Flag:** Any trigger fires → 555-ASI flags to 888-APEX with evidence package
3. **Judge:** 888-APEX evaluates (isolate mode — cannot be OpenCode judging itself)
4. **Verdict:** 
   - SEAL: demotion confirmed. PRIMARY shifts to next-best harness.
   - SABAR: evidence insufficient. Continue monitoring.
   - HOLD: escalation to F13 required.
5. **Announce:** Demotion announced via Hermes to F13
6. **Grace:** 24-hour grace period before routing changes take effect

## Re-Promotion Criteria

A demoted harness can regain PRIMARY if:
1. The trigger condition that caused demotion has been resolved
2. 10 consecutive missions pass without triggering any T1-T3
3. 888-APEX re-evaluates and returns SEAL

## F13 Override

F13 SOVEREIGN can at any time:
- Override any demotion
- Designate a new PRIMARY
- Freeze the PRIMARY designation (no auto-demotion)
- Change any threshold or window

The automation DETECTS and PROPOSES. It never DECIDES alone. Arif holds F13.

## Implementation (v1.0 — 2026-08-10)

### Signal Source Assessment

| Trigger | Required Signal | Status | Current Data |
|---------|----------------|--------|--------------|
| T1: Capability Miss Rate | Dispatch router logs (`capability_match: false`) | ❌ GAP | No dispatch router logs exist |
| T2: Latency Drift | FED route latency table (`fed_report_latency`) | ❌ GAP | FED alive (:7074) but no latency data API |
| T3: Error Rate | RSI ledger error classifications + scar ledger | ⚠️ PARTIAL | RSI ledger (265 entries, 57 unique bottleneck patterns) |

### T3 Error Rate Analysis (from RSI ledger)

Top error patterns (all harnesses, not harness-specific):

| Pattern | Count | % of Errors |
|---------|-------|-------------|
| EVIDENCE_GAP | 10 | 18% |
| TOOL_DRIFT | 9 | 16% |
| ENTROPY_GAIN | 2 | 4% |
| 54 other patterns | 1 each | 2% each |

**Note:** RSI ledger does not distinguish by harness. To implement T3 properly, we need harness-tagged error logs (which harness produced each error). Currently all errors are attributed to the session, not the harness.

### Infrastructure Gaps

**T1 — Capability Miss Rate:**
- Required: Dispatch router that logs `capability_match: true/false` per mission
- Missing: No dispatch router exists. FED (`:7074`) is advisory-only, not a dispatch router.
- Recommendation: Build a thin dispatch layer that logs capability match decisions to `/root/.local/share/arifos/dispatch-log.jsonl`

**T2 — Latency Drift:**
- Required: FED route latency table with per-harness timing data
- Missing: FED has `fed_route` tool but no latency reporting API
- Recommendation: Instrument FED to log route decisions with latency to `/root/.local/share/arifos/fed-latency-log.jsonl`

**T3 — Error Rate (harness-specific):**
- Required: Harness-tagged error classifications in RSI ledger
- Missing: RSI ledger entries don't include `harness_id` field
- Recommendation: Add `harness_id` field to RSI ledger entries. Auto-populate from session context.

### What CAN Be Measured Now

Without new infrastructure, we can still detect:
1. **Overall error rate trends** (RSI ledger bottleneck patterns over time)
2. **Remediation effectiveness** (W5 from FRAME — already live)
3. **Session-level failure patterns** (carry_forward open loops)

The demotion criteria are sound. The infrastructure to automate detection is partially missing. Manual monitoring is possible but not sustainable at scale.

## Edge Cases

- **What if all harnesses are degraded?** → F13 HOLD. Human decides.
- **What if no harness matches at all?** → Route back to F13 with capability gap report.
- **What if the FED router itself fails?** → Fallback to static PRIMARY. Demotion evaluation pauses until FED recovers.
