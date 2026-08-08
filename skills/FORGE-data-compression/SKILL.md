---
name: FORGE-data-compression
description: 'Context-window-aware data compression for long logs, code dumps, and
  multi-source evidence bundles. Compresses input to fit within model context limits
  while preserving semantic fidelity (F2 TRUTH ≥ 0.95). Supports streaming chunk-and-summarize
  pipelines. USE WHEN: "compress this log", "summarize before context window", "fit
  this in context".

  '
version: 1.0.0
tags:
- compression
- context-window
- summarization
- F2
- F4
floor_scope:
- F02
- F04
- F07
owner: A-FORGE
---
# FORGE-data-compression

## Purpose
Long logs, massive codebases, and multi-organ evidence bundles routinely exceed model context windows. This skill compresses input through a staged pipeline while maintaining ≥0.95 semantic fidelity.

## Pipeline
1. **Chunk** — Split input into semantic units (log blocks, code functions, evidence sections)
2. **Score** — Rank chunks by relevance to the query/task context
3. **Compress** — Apply lossy compression to low-relevance chunks, lossless to high-relevance
4. **Reconstruct** — Reassemble into compressed artifact with provenance markers
5. **Verify** — F2 TRUTH check: decompress sample and compare against original

## Compression Modes
- `log-compress`: Strip timestamps, deduplicate repeated lines, extract error/warn signals
- `code-compress`: Collapse boilerplate, preserve signatures + logic + comments
- `evidence-compress`: Rank by epistemic rung, compress low-confidence sections
- `streaming`: Chunk-summarize-recurse until target token count reached

## Floors
- F2 TRUTH: ≥ 0.95 fidelity. Compression must not fabricate or distort meaning.
- F4 CLARITY: Compressed output must be more readable than raw input.
- F7 HUMILITY: Report compression ratio and what was lost.
