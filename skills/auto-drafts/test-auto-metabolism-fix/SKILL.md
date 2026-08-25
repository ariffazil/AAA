---
name: test-auto-metabolism-fix
description: Fix memory amnesia by wiring auto-metabolism hooks
reuse_count: 2
status: DRAFT
---

# test-auto-metabolism-fix

> **Problem Solved:** Fix memory amnesia by wiring auto-metabolism hooks

## Trigger
When session ends or memory needs consolidation

## Verified Workflow Steps
1. Run memory_classifier.py
2. Consolidate to carry_forward.json
3. Emit receipt
