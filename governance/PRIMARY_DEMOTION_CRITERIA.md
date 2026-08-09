# PRIMARY Harness Demotion Criteria

> **Status:** DRAFT v0.1 · Design only · No implementation
> **Forged:** 2026-08-09 by 333-AGI under F13 directive
> **Carry-forward:** PRIMARY-DEMOTION-CRITERIA → IN_DESIGN

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

## Edge Cases

- **What if all harnesses are degraded?** → F13 HOLD. Human decides.
- **What if no harness matches at all?** → Route back to F13 with capability gap report.
- **What if the FED router itself fails?** → Fallback to static PRIMARY. Demotion evaluation pauses until FED recovers.
