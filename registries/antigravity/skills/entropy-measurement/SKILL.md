---
name: entropy-measurement
description: Sub-skill to score system structure, duplication, dead code, and boundary bleed before and after mutations.
---

# Entropy Measurement Sub-Skill

You are operating as the telemetry engine for the RSI and Forge roles.

## When to use this skill
Trigger this skill BEFORE and AFTER making structural changes or refactors to quantify the baseline and the resulting impact. It provides the shared ground truth for structural health.

## Role Behavior
- **Action**: Autonomously inspect the repository and run static analysis checks.
- **Measurement Vectors**:
  1. **Duplication**: Identify copy-pasted logic or redundant implementations.
  2. **Dead Code**: Find unused functions, unreferenced variables, and stale comments.
  3. **Complexity / Cognitive Load**: Flag functions exceeding 50 lines, deep nesting, or passing more than 4 parameters.
  4. **Boundary Bleed**: Check if domain layers leak into each other (e.g., UI logic in database adapters, or mixing business rules with transport layers).
  5. **Test Drift**: Identify execution paths lacking test coverage.
- **Output**: Generate or update an `entropy-report` artifact with quantifiable metrics. If invoked autonomously by RSI, immediately use the report to apply structural fixes.
