---
name: forge-monolith-split
id: forge-monolith-split
version: 1.0.0
author: A-FORGE
license: MIT
description: Split a monolithic Python file into per-module files.
tags: [refactoring, python, modularization]
related_skills: [code-review]
---

# FORGE Monolith Split

Systematic workflow for splitting a large monolithic Python file (typically 1000+ lines) into focused per-component modules while preserving all behavior.

## When to Use

- A single Python file contains 5+ independent components (tools, handlers, services)
- File exceeds 1000 lines and components are logically separable

## Workflow

1. Read the full file and identify logical section boundaries using section comment headers, decorator patterns, and function/class definitions at the same nesting level.
2. Map exact line ranges for each component using Python line analysis.
3. Create a shared types module for common utilities (no circular deps).
4. Extract each component into its own file with correct imports and indentation.
5. Rewrite original file as thin orchestrator.
6. Verify with py_compile and import tests.

## Pitfalls

1. **Indentation errors**: When extracting from nested function, body has extra indentation. Must strip and re-add correctly.
2. **Missing imports**: Each extracted file needs its own imports. Do not assume imports from original scope carry over.
3. **Circular dependencies**: Shared types module must NOT import from component modules.
4. **Lazy imports**: If original had imports inside function body, preserve that pattern.
5. **Server creation timeout**: Heavy lazy imports may cause slow startup. Pre-existing, not a regression.

## Verification

- All files pass py_compile
- All imports resolve
- Each file decorator name matches expected name
- Orchestrator imports and calls all register functions
