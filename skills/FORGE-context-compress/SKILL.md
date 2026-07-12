---
agent: FORGE
name: Context Compression — Log Intelligence
skill_id: forge-context-compress
version: 1.0.0
description: >
  Compress large log files, session traces, and tool outputs while
  preserving critical coordinates, depth markers, well references,
  seismic positions, and decision boundaries.
  Use when log output exceeds context window, when entired terminal
  histories must be summarized without losing evidence anchors,
  or before archiving session traces to VAULT999.
owner: A-FORGE
risk_tier: low
floor_scope: [F2, F4, F7]
autonomy_tier: T1
tags: [forge, compression, log, context, entropy]
forged: 2026-07-13
---

# FORGE Context Compression

## Purpose

Reduce token footprint of tool output and session logs without losing:
- Critical coordinates (lat/lng, easting/northing, depth, TVDSS)
- Well references and formation tops
- Seismic inline/crossline positions
- Decision boundaries (verdicts, holds, seals)
- Error signatures (stack frames, error codes, timeout values)
- Timestamps and sequence markers

## When to Use

- Terminal output > 200 lines → compress before continuing
- Session logs > 50KB → compress before storage
- Before VAULT999 archival → compress full session trace to 15% size
- When passing between agent context windows → compress handoff

## Compression Protocol

### Tier 1: Structural Compression (fast, lossless)
```
1. Strip ANSI escape sequences
2. Collapse repeated blank lines (max 1)
3. Merge consecutive identical status lines
4. Truncate long hex/uuids to first+last 4 chars
5. Remove timestamps older than current session
```

### Tier 2: Semantic Compression (medium, key-preserving)
```
1. Extract all coordinates into a summary table
2. Extract all SHA/commit hashes into a table
3. Extract all error messages (unique only)
4. Summarize repetitive sections: "line X repeated N times"
5. Keep the last 50 lines verbatim (most recent state)
```

### Tier 3: Evidence-Preserving Compression (lossy with audit trail)
```
1. Tag each compressed block with: [COMPRESSED:N_lines→M_lines:type]
2. Save original to /root/A-FORGE/forge_work/YYYY-MM-DD/raw/
3. Only use when context is critically tight (< 20% remaining)
4. Never compress: coordinates, seal entries, verdicts, error traces
```

## Invocation

```
Canonical: skills/FORGE-context-compress/SKILL.md
Usage: Apply Tier 1 automatically on any output > 200 lines
       Apply Tier 2 when transitioning between phases
       Apply Tier 3 only when explicitly context-constrained
```

---
*DITEMPA BUKAN DIBERI — arifOS Federation · A-FORGE Organ*
