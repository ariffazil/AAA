---
name: FORGE-context-compressor
description: Compress oversized logs, transcripts, diffs, and telemetry before they exceed a host runtime context budget while preserving provenance and recovery pointers.
forge_of: Kimi Code (FI-008) — EUREKA ZEN Phase 3 (gap fill · long-log compression for 256K-bound runtimes)
forged: 2026-07-12T18:33:00Z
rationale: Directive OPERATION EUREKA ZEN explicitly named "missing context-compression for long logs" as a Phase 3 forge candidate. Long-context runtimes (Grok 4.3 256K, Claude 1M variants) need a compression gate so they don't trip context-window boundaries mid-session. Phase 3 gap fill.
binding: FORGE-* skills (cross-CLI), particularly for Grok (FI-010) and long-context adapters
floor_scope: [F1, F2, F4, F8, F11, F13]
tags: [forge, context-compression, long-log, 256k, rsi-breaker]
status: NEW (Phase 3 gap fill)
---

# FORGE · context-compressor

> Cross-runtime compression gate for FORGE-* tools and AGI-* long-log producers.
> Used when raw input would exceed the host runtime's context budget.

## When to invoke

- Raw log / transcript / diff > 80% of host runtime's context budget
- Multi-file audit where side-effects are dense
- Telemetry / observability feeds ingested in-session
- Pre-compaction: before `forge_execute_sealed` if chain is dense

## Compression contract

```yaml
compress:
  - strategy: rolling_window | semantic_chunks | bsdiff | paged_attention
    chunk_size: tokens | lines | bytes
    overlap_pct: number (0..50)
    retention: verbatim | summary | pointer
    provenance:
      original_sha256: 12-char-prefix
      compressor: <which>
      captured_at: ISO-8601
```

## Strategy selector

| Strategy | When |
|---|---|
| `rolling_window` | conversation stream — keep last N tokens verbatim, drop the rest to pointers |
| `semantic_chunks` | narrative + structured — chunk on discourse markers, embed each |
| `bsdiff` | code diffs — keep delta fields, drop noise (whitespace-only hunks) |
| `paged_attention` | mixed modal — paginate by scene/section, keep anchors |

## RSI-breaker connection

If the compressor's output raises ΔS on re-decode:
1. Drop to a more aggressive strategy (semantic_chunks → rolling_window)
2. Emit `rsi_reason: "context_compression_too_aggressive"` + flag in next agent
3. Cap at 3 compressions per session — fail open to human after that

## Grok 256K boundary

Grok Build 4.3 (FI-010) has 256K context. Pre-flight:
- Read raw ingest size via `forge_filesystem_stat`.
- If > 240K tokens (≈960KB text), enter compression gate.
- If > 256K tokens, emit `rsi_reason: "would_exceed_context"` and HOLD.

## Not instead of

Distinct from `AGI-emd-encode` (intake contract, witness readiness) and `AGI-emd-metabolize` (memory promotion). Compressor operates between observation and encode — it shrinks the substrate so encode can attach witnesses without exceeding context.

DITEMPA BUKAN DIBERI.
