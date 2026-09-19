# Multi-Agent Synthesis Coordination — Tracking Contributions to Canon

Use when managing contributions from multiple agents to a single canonical artifact.

## Synthesis Log Structure

Maintain a SYNTHESIS.md alongside the canonical document:

```
## Synthesis Rounds
### Round N — <title>
- **Time:** ISO-8601
- **Contributor:** agent_id (role)
- **Actions:**
  1. What they did
  2. What changed
- **Status:** COMPLETE | PARTIAL | BLOCKED
- **Next:** what happens next

## Integration Decisions
<!-- logged as contributions arrive -->

## Open Questions
<!-- tracked with status: UNRESOLVED | RESOLVED -->

## Metrics
| Round | Contributions | Accepted | Rejected | Pending |
```

## Recording Sovereign Decisions

When the sovereign answers open questions mid-session:
1. Mark the question as RESOLVED with timestamp
2. Quote the sovereign's answer verbatim (it is the canonical form)
3. Mark any superseded candidate resolution paths
4. Record in the synthesis log as its own round

## Inbox Pattern

For ongoing multi-agent contributions, maintain an INBOX.md:
- Standardized entry format: AGENT_ID | TYPE | EUREKA_REF | STATUS
- Types: VALIDATE, CHALLENGE, EXTEND, MAP, IMPLEMENT
- Manager reviews and moves accepted entries into the SOT

## Dual-File Resolution

See parent SKILL.md pitfall: "Dual-file resolution: when two agents create overlapping files."

## Pitfalls

- **Tracking contributions is not the same as integrating them.** An inbox that grows without a synthesis pass becomes a TODO list, not a coordination mechanism. Run synthesis rounds periodically.
- **Sovereign answers supersede candidate resolutions.** When the sovereign provides a direct answer, mark the old candidate path as superseded — do not delete it, as it explains the reasoning that led to the question.