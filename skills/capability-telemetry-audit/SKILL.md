---
name: capability-telemetry-audit
description: "Use when auditing demonstrated capability from telemetry."
version: 1.0.0
floors: [F2, F7, F11]
triggers:
  - "what can you do that I never use"
  - "hidden capabilities"
  - "capability debt"
  - "why is this agent so bloated"
  - "which tools are unused"
  - "is this agent actually closing its loops"
  - "audit your own behaviour"
  - "skill bloat"
capability_tier: fed-long-context
ecology_state: WARM
---

# Capability Telemetry Audit

Auditing what an agent has **actually done**, as opposed to what it is wired for. Config describes
intent; the call history describes behaviour. Only behaviour answers "what should change".

All reads are read-only SQLite against `~/.hermes/state.db`. Query set, pattern counters and the
adjacency check: `references/call-history-audit.md`.

Companion skills — keep the layers separate:

| Layer | Skill |
|---|---|
| Config/prompt/storage surface (intent) | `hermes-runtime-audit` |
| What fired, and how (behaviour) | this skill |
| Structured self-assessment method | `agent-capability-self-audit` (user-owned) |

## Procedure

### 1. Four counts, never collapsed

| Count | Source |
|---|---|
| **configured** | what a file declares |
| **loaded** | what the process resolved at boot |
| **credentialed** | what has a key/host/path present to function |
| **demonstrated** | what the call history shows has fired |

The first three are agent-facing. The fourth is the one a human can act on.

### 2. Fired-tool census

```python
import sqlite3, collections
c = sqlite3.connect('/root/.hermes/state.db')
fired = dict(c.execute("SELECT tool_name, COUNT(*) FROM messages "
                       "WHERE tool_name IS NOT NULL GROUP BY 1"))
```

`wired − demonstrated = capability debt`. Then split the never-fired list into **redundant**
(another owner already covers the function → removal candidate) and **untapped**
(consequence-bearing and rare by nature → force-use or park honestly). The two need opposite actions;
reporting them as one list is the failure.

### 3. Read the arguments, not just the counts

Per-call arguments live in `messages.tool_calls` (JSON array; `function.name` +
`function.arguments`). This is what distinguishes *how* a capability is used from *whether* it is.
Classic finding: N delegated children all carrying the parent's prior — N× compute for ~1×
independent information. See the reference for the framing regex.

### 4. Closure: promise versus landed

`delivery_obligations.state`, `async_delegations.state`, `sessions.end_reason`.

**Fired calls minus tracked rows is a WITNESSING gap, not proof of failure.** Say which of the two you
are reporting. Claiming failure from a missing row is the same class of error as claiming success from
a missing error.

### 5. Self-check ratio — measure before asserting

For each mutation call, does a read/probe call follow within a few steps? Compute it **before**
asserting that verification or closure is missing. When the ratio comes back high, the thesis dies and
the real gap is elsewhere; letting the number kill the narrative is the point of measuring.

### 6. Reply-level behaviour counters

The unit is the agent's own human-facing text. Count the share of replies that ask permission for a
reversible decision, end in a question, state a hypothesis before acting, name a second-order effect,
reference a prior decision, name what is absent. Each ratio is **an action class the agent could take
autonomously but does not** — not a character judgement.

Also price the human's own input volume (mean message length × count): how much manual typing the
machine still costs him.

### 7. Price every count, then translate

Occurrences × seconds per occurrence → hours of the human's life. A count is not a finding until it is
priced and paired with the manual work he currently performs because of the gap.

## Report contract

Findings go to a human, so they must be expressed as human quantities in this order:

1. **Behaviour** — what the machine does or fails to do, one clause.
2. **Manual work the human currently does because of it** — the finding a human can act on.
3. **Attention cost** — the count converted into his time.

**Never name a tool, MCP server, port or schema in the human-facing reply.** MCP names are addressable
only by agents: *"I'm human. Mcp is for agents btw."* Capability names belong in the machine-readable
artifact (the report file, `--json`, VAULT999), never in chat.

End on the binary decisions only the human can make. Do the reversible ones yourself.

## Pitfalls

- **Measure the thesis before asserting it.** A plausible defect ("nothing gets verified", "loops
  never close", "capability is unused") must be counted in the call history before it enters the
  findings — otherwise the audit commits the same error it was hired to detect.
- **Never answer an audit request by minting a runtime.** No new skill, MCP, daemon, ledger or
  framework — the audit IS the deliverable. If something got built mid-audit, disclose it in one line
  and let the human choose kill-or-keep; do not fold it into the findings as a recommendation.
- **Volume is not value.** A rarely-fired, consequence-bearing capability is not waste; a
  frequently-fired convenience capability is not automatically kept. State the class of each.
- **Dormancy is a decision, not a verdict.** Present the triage queue with the action each item
  implies; do not silently delete, and do not queue work that is reversible and yours to finish.
- **Don't audit intent and behaviour in one breath.** A capability that is configured, loaded and
  credentialed but never fired is a different finding from one that is missing — and a capability that
  fires constantly may still be mis-framed (§3).
- **Re-run at least one counter after any change.** An audit without a second reading has no evidence
  the fix landed.

## References

- `references/call-history-audit.md` — the full query set: fired-tool census, argument extraction, the
  closure queries, the mutation→verification adjacency check, and the reply-level behaviour counters
  with their regexes.
