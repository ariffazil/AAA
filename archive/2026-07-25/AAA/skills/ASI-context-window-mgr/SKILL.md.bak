---
name: ASI-context-window-mgr
description: >
  Context window lifecycle management — monitors token usage, triggers compression
  when approaching limits, manages conversation summarization, and preserves critical
  context across compaction boundaries. USE WHEN: "context getting long", "compress
  conversation", "summarize session", "token budget".
version: 1.0.0
tags: [context-window, tokens, summarization, memory, F4, F7]
floor_scope: [F04, F07, F11]
---

# ASI-context-window-mgr

## Purpose
Model context windows are finite (128k-200k tokens). Long sessions, large codebases, and multi-organ evidence accumulate until the window fills. This skill manages the lifecycle: monitor → warn → compress → compact → restore.

## Lifecycle Stages
1. **Monitor** — Track token usage per turn. Warn at 70%, critical at 85%.
2. **Triage** — Classify context into: must-keep (task intent, floor state, active evidence), can-compress (completed steps, verbose logs), can-drop (repeated errors, resolved issues).
3. **Compress** — Apply FORGE-data-compression to can-compress segments.
4. **Compact** — When window is critical, generate session summary and restart with summary + must-keep context.
5. **Restore** — On resume, reload summary + check for drift in external state.

## Compaction Artifact
```json
{
  "session_id": "...",
  "compacted_at": "timestamp",
  "token_count_before": 150000,
  "token_count_after": 30000,
  "summary": "compressed session narrative",
  "must_keep": ["task intent", "floor state", "active blockers"],
  "dropped": ["resolved errors", "completed steps"],
  "provenance": "compacted by ASI-context-window-mgr"
}
```

## Floors
- F4 CLARITY: Compacted context must be clearer than raw history.
- F7 HUMILITY: Report what was lost in compaction. Never claim perfect recall.
- F11 AUDITABILITY: Compaction artifacts are logged, inspectable.
