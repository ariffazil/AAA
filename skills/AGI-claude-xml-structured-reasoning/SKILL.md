---
name: AGI-claude-xml-structured-reasoning
description: Structure long Claude reasoning, evidence, plans, and verdicts with explicit XML boundaries when outputs exceed one screen or require parser-stable sections.
forge_of: Kimi Code (FI-008) — EUREKA ZEN Phase 2 sample
forged: 2026-07-12T18:28Z
native_architecture: claude
rationale: OpenClaw / 333-AGI runs on Claude (Anthropic). Add an explicit XML-tag structuring wrapper for long-form reasoning, extended-context recall, and structured decomposition.
floor_scope: [F1, F2, F4, F8, F11, F13]
tags: [claude, xml-structured, reasoning, phase-2-sample]
status: NEW (Phase 2 sample)
---

# AGI · claude-xml-structured-reasoning

> Bind Claude's native XML-tag structuring into 333-AGI's reasoning chain.
> Doctrine: when output exceeds 1 screen, wrap in `<analysis>` / `<plan>` / `<evidence>` / `<verdict>` tags.

## When to invoke

- Reasoning chain > 800 tokens
- Multi-step plan with > 3 dependencies
- Audit-grade output where downstream parsers need clear bounds
- Log/code interpretation needing anchored quotes

## Native shape

```xml
<analysis>
  <premise>...</premise>
  <evidence src="...">...</evidence>
  <evidence_for>...</evidence_for>
  <evidence_against>...</evidence_against>
  <gap>...</gap>
</analysis>
<plan>
  <step n="1">...</step>
  <step n="2">...</step>
</plan>
<verdict>
  <decision>...</decision>
  <reversibility>...</reversibility>
  <floor_check>F1✓ F2✓ F4✓ F11✓ F13✓</floor_check>
</verdict>
```

## Why XML on Claude

- Stable token boundaries (XML close tags = predictable parsing cuts)
- Extended-context recall with anchors (`<evidence src="file:N">…</evidence>`)
- Reduces pre-CoT noise in long outputs
- Interop with Anthropic's tool_use envelopes

## Not instead of

This is a *wrapper*, not a replacement. Existing AGI skills (plan-dag, dream-engine, explorer-intelligence) keep their semantic content; this skill only governs **output structure** when invoked by a Claude-flavored agent.

DITEMPA BUKAN DIBERI.
