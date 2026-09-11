# A2A SRO Propagation Protocol — Cross-Agent Reality Sharing

> **Status:** DRAFT — design specification
> **Origin:** Hermes epistemic infrastructure directive (2026-09-12)
> **Relationship:** Implements cross-agent SRO propagation for AAA federation

---

## Purpose

When agent A creates or supersedes an SRO, agents B, C, D must know. Currently, each agent's memory is isolated. SRO propagation creates a shared reality layer.

---

## Protocol

### 1. SRO Creation Event

When any agent creates an SRO:

```json
{
  "type": "SRO_CREATED",
  "agent_id": "hermes-asi",
  "claim_id": "wo-MY-FISCAL-2026-DSR",
  "content_hash": "sha256:...",
  "jurisdiction": "Malaysia federal",
  "truth_class": "DER",
  "confidence": 0.88,
  "expires_at": "2027-03-31",
  "timestamp": "2026-09-12T00:00:00Z"
}
```

**Delivery:** A2A message/send to all federation agents.

### 2. SRO Supersession Event

When agent A supersedes an SRO:

```json
{
  "type": "SRO_SUPERSEDED",
  "agent_id": "hermes-asi",
  "old_claim_id": "wo-MY-FISCAL-2026-DSR",
  "new_claim_id": "wo-MY-FISCAL-2027-DSR",
  "reason": "Updated with 2027 MOF data",
  "timestamp": "2026-09-12T00:00:00Z"
}
```

**Delivery:** A2A message/send to all agents who referenced old_claim_id.

### 3. SRO Calibration Event

When outcome is observed:

```json
{
  "type": "SRO_CALIBRATED",
  "agent_id": "hermes-asi",
  "claim_id": "wo-MY-FISCAL-2026-DSR",
  "outcome": true,
  "calibration_error": 0.12,
  "timestamp": "2027-03-31T00:00:00Z"
}
```

**Delivery:** A2A message/send to all agents who used this claim.

---

## Propagation Rules

1. **Broadcast on creation.** Every new SRO is announced to all federation agents.
2. **Targeted on supersession.** Only agents who referenced the old claim are notified.
3. **Broadcast on calibration.** Calibration data is shared for collective learning.
4. **No forced update.** Agents receive notification but decide independently whether to update their local memory.
5. **Conflict resolution.** If two agents create contradictory SROs for the same claim, escalate to arif_judge.

---

## Implementation via A2A

### Send SRO Event

```
aaa_dispatch_a2a(
  target_agent="all",
  prompt="SRO_CREATED: claim_id=wo-MY-FISCAL-2026-DSR, jurisdiction=Malaysia federal, truth_class=DER, confidence=0.88, expires_at=2027-03-31",
  context="SRO propagation from hermes-asi"
)
```

### Receive SRO Event

On receipt, agent:
1. Checks if claim is relevant to its domain
2. If relevant: stores in local memory with provenance
3. If supersession: updates local copy
4. If calibration: updates local calibration data

---

## Integration Points

| Component | Role |
|---|---|
| AAA A2A Gateway | Routes SRO events between agents |
| arif_memory | Stores SROs with supersession index |
| arif_judge | Resolves conflicting SROs |
| VAULT999 | Records SRO lifecycle events |
| Agent boot | Loads recent SRO events on startup |

---

## Open Questions

1. **Fan-out:** Should SRO events go to ALL agents or only domain-relevant ones?
2. **Rate limiting:** How many SRO events per hour before flooding?
3. **Priority:** Should SRO supersessions be prioritized over creations?
4. **Acknowledgment:** Should agents ACK receipt of SRO events?

---

DITEMPA BUKAN DIBERI ⚒️
