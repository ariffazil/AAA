# SPEC: <name> v0.1

## What you are building

<One paragraph: what it is, what it's for, and one governance line
(e.g. "read-only, advisory only, never acts").>

## Working directory

Build EVERYTHING inside the current working directory. Do not touch any
other directory. Do not modify the source data.

## Input data (READ-ONLY — never write to these files)

<Exact absolute paths + schema/table notes the builder needs.>

## Deliverables

1. <numbered file list with purpose; add size caps, e.g. "every module
   <= 250 lines, split if it grows">
2. <executable shim if CLI>
3. <tests — with an explicit list of edge cases they must cover>
4. <README with usage + governance note>

## Constraints

- Python 3.10+ stdlib only for the package (pytest allowed in tests).
- No network calls. No writes anywhere except inside the working dir.
- Deterministic output.
- Handle: <edge cases — empty input, unicode, zero-match cases>. No
  exceptions on real data.

## Definition of done (verify before you finish)

1. `pytest tests/ -q` passes, covering the edge cases above.
2. `<main CLI command>` runs against the real data without error.
3. `<secondary command>` produces human-readable output.
Run all checks yourself and paste their actual output in your final answer.
