---
id: reality-kernel-phase1-evidence-ledger
name: reality-kernel-phase1-evidence-ledger
version: 1.0.0
description: 'Evidence ledger with typed truth states and LLM write gate.'
author: 'arifOS federation / Hermes Agent'
license: 'constitutional (arifOS F1-F13)'
tags: [reality, evidence, ledger, truth, integrity, infrastructure, arifos]
related_skills: [claim-receipt-discipline, audit-seal, FORGE-vault999-witness]
autonomy_tier: T0
floor_scope: [F2, F9, F11, F13]
risk_tier: low
capability_tier: fed-agent-subagent
ecology_state: WARM
---

## When to Use

USE WHEN:
- Agent makes factual claims about system state, deployment status, or external events
- Need to distinguish between what was observed (source-verified) vs inferred (agent reasoning)
- Building or operating infrastructure that requires provable event history
- Hardening claim-receipt-discipline from prompt-level to data-layer enforcement

DO NOT USE WHEN:
- Casual conversation or brainstorming (soft discipline suffices)
- No external systems to verify against (no connector target)
- Task is purely creative/planning (no truth claims needed)

---

# Reality Kernel Phase 1 — Evidence Ledger

> **DITEMPA BUKAN DIBERI** — Memory is not evidence. A tool call is not proof.
> Only scoped, attributable, time-bound, independently checkable evidence
> upgrades a claim about reality.

## Why this exists

claim-receipt-discipline enforces that agents tag claims with evidence at the
**prompt level** (soft enforcement). The Reality Kernel enforces the same
discipline at the **data layer** (hard enforcement).

The gap: a prompt-level rule can be ignored, forgotten, or overridden by
training incentives (confident fluency scores higher than uncertain truth).
A data-layer rule cannot be bypassed — the LLM literally cannot write
OBSERVED into the ledger because the write path does not exist for
`actor_kind='agent'`.

Progression:
- claim-receipt-discipline → "agent must tag claims with evidence" (soft)
- Reality Kernel Phase 1 → "agent's claims are structured records with enforced types" (hard)

**CRITICAL RULE (from 2026-08-19 analysis):**

> "Fluent false observation + confident inference = false belief that feels like memory."

The Reality Kernel makes this structurally impossible by separating
observation from inference at the data layer.

## Architecture position

```
Human (F13) ←→ Hermes LLM ←→ Reality Kernel MCP ←→ External Systems
                  ↓                    ↓
            reasoning layer     evidence ledger
            (planning,          (append-only,
             inference,          hash-chained,
             language)           typed truth states)
```

The LLM remains the planner and interpreter. The Reality Kernel owns truth status.

## Four-state truth model

| State | Who can write it | Meaning | Agent phrasing |
|---|---|---|---|
| **OBSERVED** | Connectors, humans ONLY | Directly read from trusted source | "The CI run succeeded at 14:03." |
| **ATTESTED** | Anyone | Reported, not independently verified | "Arif reported that it was settled." |
| **INFERRED** | Agent only | Derived from evidence | "It is likely deployed." |
| **UNKNOWN** | Anyone | Evidence does not establish it | "I cannot establish whether X occurred." |

**LLM WRITE RESTRICTION:** The agent may ONLY write INFERRED, PROPOSED, or
UNKNOWN states. OBSERVED can only be created by authenticated connectors or
human attestation tools. Enforced by `actor_kind` validation at the gate layer.

This single rule closes ~90% of agent-reality gaps. When the agent is forced
to label "Syed drove Arif home" as INFERRED instead of presenting it as fact,
the human sees the uncertainty and can ask "Verify." That friction is the feature.

## Schema

Full SQLite schema: `references/evidence-ledger-schema.sql`

Three core tables:
1. **reality_events** — append-only factual records
2. **reality_evidence** — raw receipts and artifacts (content-addressed)
3. **reality_conflicts** — contradiction tracking

Plus:
- **reality_actions** — action state machine (PROPOSED → REQUESTED → AUTHORIZED → EXECUTED → VERIFIED)
- SQLite triggers for append-only enforcement
- Hash chain via `prev_hash` → `event_hash` linkage

## Event envelope

Every record in the ledger follows this envelope:

```json
{
  "event_id": "evt_01J...",
  "prev_hash": "sha256:...",
  "event_hash": "sha256:...",
  "occurred_at": "2026-08-19T18:37:00+08:00",
  "recorded_at": "2026-08-19T18:37:02+08:00",
  "event_type": "deployment.status_observed",
  "subject": "geox-api@production",
  "state": "OBSERVED",
  "actor": { "kind": "connector", "id": "github-actions" },
  "authority": "system_receipt",
  "source": {
    "uri": "https://github.com/org/repo/actions/runs/...",
    "receipt_id": "run_123",
    "content_hash": "sha256:..."
  },
  "evidence_ids": ["ev_01J..."],
  "confidence": 0.995,
  "supersedes": null,
  "scope": "production",
  "immutable": true
}
```

Two distinct timestamps:
- `occurred_at` — when the event happened in reality
- `recorded_at` — when the ledger received the record

The gap between these is observability latency. If `recorded_at` is hours
after `occurred_at`, the chain is still valid but the evidence is stale.

## Hash chain integrity

Each event includes:
- `prev_hash`: SHA-256 of the previous event's canonical form
- `event_hash`: SHA-256 of this event's canonical form (excluding event_hash itself)

Verification: recompute hash chain from genesis. Any break = tampering detected.

```python
import hashlib, json

def compute_event_hash(event: dict) -> str:
    canonical = json.dumps(
        {k: v for k, v in event.items() if k != "event_hash"},
        sort_keys=True, separators=(",", ":")
    )
    return "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()

def verify_chain(events: list) -> bool:
    for i, event in enumerate(events):
        if event["event_hash"] != compute_event_hash(event):
            return False
        if i > 0 and event["prev_hash"] != events[i-1]["event_hash"]:
            return False
    return True
```

## LLM write restriction gate

```python
def validate_event_write(event: dict, actor: dict) -> bool:
    if actor["kind"] == "agent":
        if event["state"] == "OBSERVED":
            raise ValueError("Agent cannot write OBSERVED; use INFERRED or UNKNOWN")
        if event["state"] not in ("INFERRED", "PROPOSED", "UNKNOWN"):
            raise ValueError(f"Agent state must be INFERRED/PROPOSED/UNKNOWN, got {event['state']}")
    elif actor["kind"] in ("connector", "human"):
        if event["state"] not in ("OBSERVED", "ATTESTED"):
            raise ValueError(f"Connector/human should write OBSERVED/ATTESTED, got {event['state']}")
    return True
```

### Database-level enforcement

The Python gate above is application-layer. For Phase 1 on SQLite, add a trigger:

```sql
CREATE TRIGGER trg_deny_agent_observed
BEFORE INSERT ON reality_events
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.actor_kind = 'agent' AND NEW.state = 'OBSERVED'
        THEN RAISE(ABORT, 'Agent cannot create OBSERVED events; use INFERRED or UNKNOWN')
    END;
END;
```

This prevents accidental self-promotion at the database level. SQLite does not support
stored procedures or role-based access, so a determined attacker controlling the
application layer could bypass this by setting `actor_kind='connector'`. For production
enforcement, migrate to PostgreSQL with role-based access control and stored procedures
(`append_agent_inference()`, `append_connector_observation()`).

The trigger is the minimum viable enforcement. It catches the most common failure mode:
the agent (or its application layer) accidentally or carelessly writing OBSERVED.

## Claim gateway architecture

**CRITICAL INSIGHT:** The LLM must never decide whether to call falsification.
The runtime calls it by policy.

If the model chooses whether a fact is high-stakes, whether a source is sufficient,
or whether to hold, it will eventually optimize for conversational completion — the
exact bypass path.

```
LLM drafts response/action
        ↓
Claim parser + risk classifier (deterministic, rules-first)
        ↓
Evidence policy engine
  ├─ sufficient → attach provenance + allow scoped wording
  ├─ conflicting → report conflict; block factual verdict
  ├─ missing → force UNKNOWN / request verification
  └─ irreversible/high impact → 888 HOLD → F13 authorization
        ↓
Renderer produces final response
```

The model may propose claims. It cannot elevate their epistemic status.
This transforms the Reality Kernel from an optional MCP tool into a
mandatory post-processor for every factual output.

## Integration with Hermes

### Option A: MCP server (recommended)

Build `reality-mcp` as a standalone MCP server. Hermes loads it dynamically.

MCP tools exposed:
- `reality.append_event(...)` — submit event (state validated by actor_kind)
- `reality.record_observation(...)` — connector/human only
- `reality.get_timeline(...)` — query events by subject/time range
- `reality.query_claims(...)` — search events by type/state
- `reality.verify_state(...)` — read-back from source system
- `reality.list_conflicts(...)` — unresolved contradictions
- `reality.verify_chain(...)` — hash chain integrity check

### Option B: Hermes plugin

Wire into Hermes plugin system as a hook that intercepts factual claims
before output. Less flexible than MCP but tighter integration.

**Recommendation:** Start with Option A (MCP server). Composable, testable,
no Hermes core changes required.

## Build order within Phase 1

| Step | What | Depends on | Output |
|---|---|---|---|
| 1.1 | Create SQLite schema | Nothing | evidence_ledger.db |
| 1.2 | Implement hash chain module | 1.1 | reality/chain.py |
| 1.3 | Implement event append + validation | 1.1, 1.2 | reality/events.py |
| 1.4 | Implement LLM write restriction gate | 1.3 | reality/gate.py |
| 1.5 | Implement query/timeline API | 1.3 | reality/query.py |
| 1.6 | Implement conflict detection | 1.3 | reality/conflicts.py |
| 1.7 | Wire into MCP server | 1.3–1.6 | reality_mcp/server.py |
| 1.8 | Integration test with Hermes | 1.7 | test_evidence_ledger.py |

Steps 1.1–1.6: one session. Step 1.7: another session. Step 1.8: requires Hermes restart.

## Compression quarantine

When Hermes summarizes a conversation, the compressed output must be tagged:

```json
{
  "memory_class": "COMPRESSED_TESTIMONY",
  "source_turn_range": ["turn_34", "turn_81"],
  "lossiness": "KNOWN",
  "may_contain": ["omitted negation", "lost chronology", "lost attribution"],
  "permitted_use": ["orientation", "retrieval_hint"],
  "prohibited_use": ["fact_verification", "action_authorization"]
}
```

Hard policy:
- A summary may guide retrieval.
- A summary may NOT satisfy an evidence requirement.
- A summary may NEVER become OBSERVED, VERIFIED, or AUTHORIZED.
- If user asks "what did I say?" → retrieve the raw turn, not the summary.
- If raw turn is unavailable → state UNKNOWN or "aku hanya ada summary yang lossy."

This prevents the worst failure mode: compressed testimony promoting plan to fact.

## Phase 1 exit criteria

Do not call Phase 1 complete because the SQL exists. Complete only when:

1. Agent credential attempts OBSERVED insert → database rejects it.
2. Agent credential attempts UPDATE upgrading its old INFERRED row → database rejects it.
3. Connector can write only its own registered source_id and event types.
4. Every mutable-source receipt stores retrieval time, source version/edit metadata, and raw-content hash.
5. Every event has `occurred_at`, `recorded_at`; do not collapse time.
6. Events are append-only; corrections are new, linked events — not overwritten rows.
7. Any claim built from compressed summary carries COMPRESSED_TESTIMONY, never factual status.
8. A direct DB client with the Hermes role cannot bypass the policy.

## Adversarial test fixtures

Build these alongside the schema. See `references/adversarial-test-fixtures.md` for
structured test cases covering: plan-to-execution promotion, conditional approval
missing conditions, stale receipts, edited messages, forged connectors, conflicting
sources, summary-negation loss, clock skew, human-system conflicts, and agent
self-promotion attempts.

## Anti-patterns

| Anti-pattern | What it means | What to do |
|---|---|---|
| Agent writes OBSERVED | Self-promotion of claim to fact | Reject; force INFERRED or UNKNOWN |
| Hash chain broken | Tampering or corruption | Reject ledger; alert F13 |
| Event without evidence_ids | Unsubstantiated claim in ledger | Allow only as PROPOSED |
| Stale event not superseded | Old state visible as current | Create superseding event |
| Skipping conflict detection | Contradictions propagate silently | Run conflict scan on every append |
| Treating INFERRED as OBSERVED | Agent confidence ≠ source verification | Read back from source before acting |

## Connection to arifOS constitution

- **F2 TRUTH** — Every record must have a source. No source → UNKNOWN.
- **F9 ANTI-HANTU** — LLM cannot fabricate OBSERVED. Only connectors/humans.
- **F11 AUDIT** — Hash chain makes ledger tamper-evident. Conflicts logged.
- **F13 SOVEREIGN** — Human authority terminates every verification chain.
- **W_scar** — Consequence > authority → HOLD. Ledger records the hold.

## What this does NOT solve (defer to Phase 2+)

- **Connector truth** (Phase 2): Connectors must independently verify sources. Corrupted connector → corrupted OBSERVED. Start with ONE two-witness connector path (e.g., GitHub Actions + health endpoint). Cross-verification reduces integrity risk from single corrupted source.
- **Claim compiler** (Phase 3): Forcing every factual response through `reality.get_timeline()` before output.
- **Action state machine + output firewall** (Phase 4): Two layers: (a) track action lifecycle PROPOSED → EXECUTED → VERIFIED, (b) firewall that blocks unsupported claims on sensitive domains (finance, live data, health, legal). Agent cannot produce confident claims about real-time data without connector-backed evidence.
- **Evaluation harness** (Phase 5): Adversarial testing of the entire system against all 12+ fixtures.
- **World model** (Phase 6): Anomaly detection and implausibility scoring. Helps with prediction but cannot solve correspondence problem — that requires evidence, not intelligence.

### Phase sequence

1. Evidence ledger + state constraints (this skill)
2. One two-witness operational truth path
3. Claim compiler on every user-visible factual answer
4. Action state machine + output firewall for sensitive domains
5. Full evaluation harness with adversarial fixtures
6. World-model layer for anomaly detection

## The invariant

> **Memory is not evidence. A tool call is not proof. An execution receipt
> is not an outcome. Only scoped, attributable, time-bound, independently
> checkable evidence upgrades a claim about reality.**

---

*DITEMPA BUKAN DIBERI — every record must earn its state, not inherit it
from confidence.*
