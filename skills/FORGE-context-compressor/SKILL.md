---
name: FORGE-context-compressor
description: Compress oversized logs, transcripts, diffs, and telemetry before they
  exceed a host runtime context budget while preserving provenance and recovery
version: "1.1.0-2026.08.21"
merged_from: [FORGE-context-compress, FORGE-data-compression]
forge_of: Kimi Code (FI-008) — EUREKA ZEN Phase 3 (gap fill · long-log compression
  for 256K-bound runtimes)
forged: 2026-07-12 18:33:00+00:00
rationale: Directive OPERATION EUREKA ZEN explicitly named "missing context-compression
  for long logs" as a Phase 3 forge candidate. Long-context runtimes (Grok 4.3 256K,
  Claude 1M variants) need a compression gate so they don't trip context-window boundaries
  mid-session. Phase 3 gap fill.
binding: FORGE-* skills (cross-CLI), particularly for Grok (FI-010) and long-context
  adapters
floor_scope:
- F1
- F2
- F4
- F8
- F11
- F13
cognitive_engine_notes:
  claude: "Use <critical_sections> XML tags to mark preserved coordinates. Claude's extended context handles the structural wrapping natively."
  codex: "Output compressed payload as strict JSON with `preserved_coordinates` array. Codex handles strict schema adherence best."
  hermes: "Output as `--- COMPRESSED ---` markdown blocks with inline failure markers. Hermes reads conversational formatting fastest."
tags:
- forge
- context-compression
- long-log
- 256k
- rsi-breaker
status: NEW (Phase 3 gap fill)
owner: A-FORGE
capability_tier: fed-long-context
ecology_state: WARM
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

## Merged Protocol (from FORGE-context-compress — retired 2026-08-21, trigger-collision merge)

## Compression Protocol

### 1. Input Classification

When context exceeds 10K tokens:

```yaml
input_classification:
  type: BUILD_OUTPUT | TEST_TRACE | LOG_DUMP | CONTAINER_LOG | MIXED
  estimated_tokens: <number>
  target_tokens: <number>  # typically 2K-4K
```

### 2. Critical Coordinate Extraction (NEVER COMPRESS)

These coordinates MUST survive compression:

| Coordinate | Pattern | Why Critical |
|---|---|---|
| **Error lines** | `Error:`, `FAIL`, `✗`, `Traceback`, `panic:`, `FATAL` | Root cause anchor |
| **File:line refs** | `/path/file.ts:42`, `at line 127` | Source location |
| **Exit codes** | `exit code 1`, `exited with code 137` | OOM/signal diagnosis |
| **Timestamps** | `2026-07-13T02:`, `[18:11:50]` | Temporal ordering |
| **Stack traces** | Indented trace lines (≥4 spaces after error) | Failure chain |
| **Test names** | `✓`, `✗`, `# Subtest:` | Test result grid |
| **Docker events** | `Container`, `Exited`, `Killed`, `OOMKilled` | Infrastructure events |

### 3. Compression Strategy

```
FULL OUTPUT (50K tokens)
  → [Extract] Critical coordinates (error lines, file:line, exit codes, stack traces)
  → [Sample] Non-critical sections (1 line per 50, representative)
  → [Summarize] Repeating patterns (e.g., "37 identical npm warnings" instead of 37 lines)
  → [Truncate] Known-verbose sections (node_modules paths, full stack frames after first 3)
  → COMPRESSED OUTPUT (2K-4K tokens)
```

### 4. Output Envelope

```yaml
compressed_output:
  summary:
    original_tokens: 52400
    compressed_tokens: 2800
    compression_ratio: 0.947
    preserved_coordinates: 23
  critical_sections:
    - type: ERROR
      line: 847
      content: "TypeError: Cannot read properties of undefined (reading 'blockedBy')"
      file: "test/VerticalAgentE2E.test.ts:97"
    - type: ERROR  
      line: 1203
      content: "FATAL: Container exited with code 137 (OOMKilled)"
      file: "docker compose logs arifos"
  pattern_summary:
    - pattern: "npm WARN deprecated"
      count: 37
      sample: "npm WARN deprecated inflight@1.0.6: This module is not supported..."
    - pattern: "Downloading"
      count: 142
      sample: "(142 package downloads, all HTTP 200)"
  sampled_sections:
    - range: "lines 1-200 (build init)"
      sample: "> tsc -p tsconfig.json\n> node dist/test/*.test.js"
    - range: "lines 400-800 (test output)"
      sample: "ok 1 - test passes\nok 2 - test passes\n... (8 tests, 8 pass)"
  full_output_preserved: true
  full_output_path: "/tmp/opencode/full_output_20260713_0215.log"
```

### 5. Restore Protocol

When an agent needs the full context, it requests restoration via the `full_output_path`. The compressed envelope carries enough reference coordinates for the agent to:
- Know exactly where failures occurred (file:line)
- Decide whether full restoration is needed
- Trace failure chains without loading 50K tokens

## Anti-Patterns

- ❌ Removing error lines to "save more tokens" — they're the whole point
- ❌ Summarizing stack traces as "an error occurred" — preserves nothing
- ❌ Compressing below 500 tokens — loses too much signal
- ❌ Deleting the full output file — F1 AMANAH: always preserve original
