# Batch Pending-List Judgment via apex-judge FED route (2026-08-12)

## Pattern

When F13 sovereign issues "execute all this" with a multi-item task list, the correct pattern is **verify each item independently first**, then **route through apex-judge for tier classification**, then **execute within authority**.

Do NOT execute the full list based on the sovereign's blanket approval alone. The sovereign may have received the list from a source with known false-positive rates (sibling audit, subagent report).

## Recipe

1. **Verify each item independently** (T0 read-only probes — grep, curl, diff)
2. **Build evidence package** (JSON with per-item claims, evidence, reversibility, blast radius)
3. **Route to apex-judge FED** (`execute_code` → `http://127.0.0.1:4000/v1/chat/completions` with `model: apex-888`)
4. **Receive per-item verdicts**: EXECUTE_AUTONOMOUSLY / ROUTE_TO_AFORGE / SKIP_ALREADY_RESOLVED / HOLD_FOR_F13
5. **Re-check apex verdict against reality** — apex judge can only judge what the evidence package contains; if the evidence was wrong, the verdict is wrong
6. **Execute or route per verdict**

## Example evidence package

```json
{
  "doer": "HERMES (Edge Sentinel, session ...)",
  "context": "Arif issued 'execute all this' for a 6-item pending list. Independent audit found 62.5% false/misleading.",
  "pending_items": [
    {
      "id": "Gap B",
      "severity": "RED",
      "description": "Wire metabolizer loop in server.js (3 lines)",
      "evidence": "metabolizer_loop.js exists but not imported at server.js:4508",
      "reversibility": "HIGH — additive code, no existing modified",
      "blast_radius": "1 file (server.js), 3 lines, restart required"
    }
  ],
  "f13_context": "Sovereign directive was 'execute all this'. Hermes needs judgment on which to execute, route, or skip."
}
```

## Pitfall: incomplete evidence packages

The apex judge can only evaluate what's in the evidence package. If the evidence is incomplete or wrong, the verdict will be wrong. In this session:

- Evidence package said "2 commits ahead" for arifOS drift
- Reality: 95+ commits behind deployed version, full redeploy needed
- Apex verdict (T1 EXECUTE_AUTONOMOUSLY) was wrong because the evidence undercounted the scope

**Lesson:** apex-judge verdicts are only as good as the evidence package. Always re-check the verdict against live state before executing.

## Pitfall: sovereign "execute all" ≠ blanket authority

F13 sovereign authority means final veto, not that all items in a list are safe. The HITL taxonomy applies:
- Items within T1/T2 authority → execute autonomously
- Items at T3 (kernel restart, deployment) → still need 888_HOLD even if sovereign said "all"
- Items already resolved → SKIP (don't waste compute)

The sovereign's intent is "get this done safely," not "skip all checks."

## Pitfall: subagent discovers already-implemented code

Files can change between reads. In this session:
- Subagent read `server.js` and found metabolizer_loop already imported at line 73
- Hermes read the same file earlier and it was at line 4508 without the import
- The file was modified between reads (by another session or process)

**Lesson:** when delegating verification to subagents, warn them that files may have changed since the parent's read. Always re-read critical files before applying patches.
