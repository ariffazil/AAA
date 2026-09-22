# 13 CONSTITUTIONAL LAWS — A2A Layer Canon Fragment

> **Status:** F13_RATIFIED_CHAT (2026-09-21)
> **Scope:** Agent-to-Agent (A2A) constitutional layer — sits ABOVE the A2A wire protocol
> **Premise:** A2A solves how agents communicate. It does not solve whether agents should trust, obey, delegate to, remember, or amplify one another.

## The 13 laws

\[
\boxed{
\begin{aligned}
&1.\ \text{Identity} \neq \text{Claim} \\
&2.\ \text{Capability} \neq \text{Authority} \\
&3.\ \text{Authentication} \neq \text{Trust} \\
&4.\ \text{Message} \neq \text{Evidence} \\
&5.\ \text{Consensus} \neq \text{Truth} \\
&6.\ \text{DelegatedAuthority}_{n+1} \subseteq \text{DelegatedAuthority}_n \\
&7.\ \text{State}_{terminal} \not\rightarrow \text{State}_{working} \\
&8.\ \text{Retry} \neq \text{Replay} \\
&9.\ \text{Provenance}_{out} \supseteq \text{Provenance}_{material} \\
&10.\ \text{Unknown} \neq \text{Invented} \\
&11.\ \text{Time}_{evidence} \neq \text{Time}_{now} \\
&12.\ \text{Agent\_Internality} \neq \text{Trust} \\
&13.\ \text{Federation} \neq \text{Sovereignty}
\end{aligned}
}
\]

## Deepest invariant

> **Agents may exchange work freely. They may not exchange truth, trust, authority, identity, or sovereignty implicitly.**

## Why this layer exists above A2A

A2A standardizes:
- Agent Cards (discovery)
- Tasks (unit of work)
- Messages (communication)
- Artifacts (deliverables)
- Contexts (lineage)
- Streaming
- Authorization hooks
- Extensions

A2A does NOT standardize:
- Trust propagation
- Authority delegation chains
- Provenance requirements
- Memory scope governance
- Verification independence
- Witness validation

## The federation's constitutional layer — required envelopes

Every agent-to-agent interaction in arifOS carries:

```json
{
  "identity_envelope": {
    "actor_actual": "<cryptographic identity, e.g. actor_id>",
    "actor_declared": "<what agent says it is>",
    "verifiable": true
  },
  "capability_envelope": {
    "declared": [...],
    "exported": [...],
    "callable": [...],
    "observed": [...]
  },
  "authority_envelope": {
    "actor": "...",
    "session": "...",
    "scope": "...",
    "expiry": "...",
    "delegation_chain": [...],
    "ceiling": "..."
  },
  "trust_envelope": {
    "authentication": "verified | unverified",
    "epistemic_trust": "evidence-based | inferred | unknown",
    "transitive": false,
    "reputation_inherited": false
  },
  "provenance_envelope": {
    "source": "<origin system/agent>",
    "timestamp_utc": "...",
    "transformation_chain": [...],
    "lossiness_declared": []
  },
  "temporal_envelope": {
    "evidence_time_utc": "...",
    "valid_from_utc": "...",
    "valid_until_utc": "...",
    "deadline_utc": "...",
    "stale_after_seconds": "..."
  }
}
```

## Mapping to existing arifOS doctrine

| Law | arifOS primitive |
|---|---|
| 1 | `arif_init` actor identity (F11 attribution) |
| 2 | Authority Envelope (F13_RATIFIED_CHAT 2026-09-16) |
| 3 | Well guard dignity / HERMES reality grounding |
| 4 | `arif_observe` produces evidence-typed observations |
| 5 | FRAME observer (independent witness, not vote-count) |
| 6 | Delegation monotonic narrowing (already in agent compartments) |
| 7 | State-Transition Discipline (F13_RATIFIED_CHAT 2026-09-16) |
| 8 | Idempotency keys on every mutation; parent_seal_hash Merkle lock |
| 9 | VAULT999 receipt chains (append-only) |
| 10 | `UNKNOWN` is valid result; UNKNOWN ≠ PASS |
| 11 | CHRON with `function`/`step_type` discriminator; freshness boundaries |
| 12 | FRAME is the independent observer (not a federation-internal organ's word) |
| 13 | F13 sovereign veto preserved at meaningful boundaries |

## See also

- `/root/AAA/canon/7-MACHINE-LAWS.md` — substrate canon
- `/root/AAA/instructions/authority-envelope.md` — primary implementation reference
- `/root/AAA/instructions/state-transition-discipline.md` — primary implementation reference
- `/root/AAA/instructions/witness-zen-doctrine.md` — independent witness pattern
