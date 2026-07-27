# 001 MOTD RSI — Recursive Self-Improvement Cycle

**Domain:** arifOS Federation MOTD
**Owner:** arifOS Kernel (via `/root/AAA/governance/`)
**Update cycle:** As-needed (triggered by drift or performance regression)
**GOLDEN_HASH: d72ffaf9967ec419afcb857d371f40aa

## Purpose

The MOTD (Message of the Day) at `/etc/update-motd.d/05-arifos` is the **State-of-Truth surface** for every SSH login to the af-forge VPS. It must reflect live constitutional, operational, and epistemic reality — not stale caches.

This document defines the recursive improvement cycle: how the MOTD proposes its own improvements, and how sessions respond.

## The RSI Contract

```
┌─────────────────────────────────────────────┐
│  SSH Login → MOTD renders                    │
│     ↓                                        │
│  MOTD footer checks its own freshness:        │
│    • drift vs this reference document         │
│    • age since last modification              │
│    • render performance (from perf log)       │
│     ↓                                        │
│  If stale/drifted → SUGGEST improvement       │
│     ↓                                        │
│  Session (arif_init → arif_think) reads this  │
│  document and proposes patch to MOTD          │
│     ↓                                        │
│  Patch applied → MOTD updated                 │
│     ↓                                        │
│  Record update timestamp + diff in git        │
│     ↓                                        │
│  Next SSH login shows fresh MOTD             │
└─────────────────────────────────────────────┘
```

## Reference Version Tracking

The MOTD script at `/etc/update-motd.d/05-arifos` must be kept in sync with the intent defined here. The RSI footer in the MOTD computes `md5sum` of both files and flags drift.

| Artifact | Path | Role |
|----------|------|------|
| MOTD script | `/etc/update-motd.d/05-arifos` | Live renderable |
| Reference | `/root/AAA/governance/001_MOTD_RSI.md` | Intent spec |
| Perf log | `/var/run/motd_perf.log` | Render timing history |

## MOTD Improvement Drivers

### 1. Performance
Render time is logged to `/var/run/motd_perf.log`. If average render exceeds **2 seconds**, the MOTD should be profiled and slow probes (e.g., slow organs, Git SHA reads) should be:
- Cached with a TTL (e.g., `/tmp/motd_cache_*`)
- Moved to background refresh
- Removed if unimportant

### 2. Accuracy
If an organ endpoint changes its health path or response schema, the MOTD must be updated. Signals:
- An organ reports "healthy" but the MOTD shows unreachable
- A new organ joins the federation (new port)
- A repo is renamed or relocated

### 3. Completeness
At minimum, the MOTD MUST show:
- ASCII arifOS logo
- Constitutional state (SEALED/UNSEALED) from real kernel health
- All 6 organ statuses
- Git SHAs for all 6 governing repos
- Phone node count
- Session init prompt
- RSI footer (self-check)

### 4. Clarity
- Use ANSI colour codes only (no tput)
- Keep output under 60 lines
- Ensure timeout killer fires within 8s
- All external commands shielded with `2>/dev/null`

## Improvement Protocol

When a session identifies that the MOTD needs improvement:

1. **Diagnose**: Compare MOTD output vs this reference. Identify the gap.
2. **Propose**: Use `arif_think` to reason about the best fix.
3. **Forge**: If the fix requires file modification, use `arif_forge` with mode=engineer or mode=write.
4. **Verify**: Run `run-parts /etc/update-motd.d/` and capture output.
5. **Attest**: Update the `Last improved` timestamp below and record the diff.

## Changelog

| Date | Author | Change |
|------|--------|--------|
| 2026-07-27 | arifOS Agent | Initial RSI contract — v2 MOTD with real kernel SEAL/UNSEAL, 6-organ probes, init prompt, RSI footer |
