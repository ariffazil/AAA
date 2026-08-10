---
name: FORGE-context-compress
version: "1.0.0-2026.07.13"
description: "Context window compression for massive log/output payloads"
domain: forge
cognitive_engine_notes:
  claude: "Use <critical_sections> XML tags to mark preserved coordinates. Claude's extended context handles the structural wrapping natively."
  codex: "Output compressed payload as strict JSON with `preserved_coordinates` array. Codex handles strict schema adherence best."
  hermes: "Output as `--- COMPRESSED ---` markdown blocks with inline failure markers. Hermes reads conversational formatting fastest."
---

# FORGE Context Compression

## Prime Law

**Compress, never lose. Reduce tokens, preserve meaning.**

Massive output signals (build logs, test traces, docker output) saturate agent context windows. This skill defines the compression protocol: reduce content by 80–95% while preserving every failure coordinate needed for root cause analysis.

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

## Floor Alignment

| F | Obligation |
|---|-----------|
| F1 AMANAH | Full output always preserved at `full_output_path` |
| F2 TRUTH | Critical coordinates preserved with exact line numbers |
| F4 CLARITY | Structured envelope, never free-form prose |
| F8 GENIUS | Simplest compression that preserves all failure information |

---

*Forged: 2026-07-13 by FORGE (000Ω) under F13 SOVEREIGN directive*
*DITEMPA BUKAN DIBERI*
