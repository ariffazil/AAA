# A2A-R Claim Authority — When Evidence Travels but Authority Must Not

> **Companion to:** `signal-strength-gating` (which governs thin-signal interpretation)
> **Ratifikasi:** pending F13 — see `/root/forge_work/2026-09-26-a2a-r-manifest.md`
> **Purpose:** Document the per-claim authority discipline that prevents chain hallucination and correlated error amplification across arifOS federation agents (Hermes / OpenCode / OpenClaw / etc).

## The compression

```
Evidence may travel.
Confidence may travel.
Unknowns may travel.
Authority DOES NOT travel automatically.
```

This rule is the A2A-federation extension of the same gating principle that signal-strength-gating applies to evidence: a relayed item carries its source's evidence, but not its source's authority to declare the evidence sufficient. The agent that **receives** must re-evaluate whether the claim is permitted at the claimed confidence, in its own scope, against its own role.

## Three failure modes this forecloses

### 1. Chain hallucination

```
Hermes: exit 0
       ↓ (claims "Feature X done")
OpenCode: trusts claim
       ↓ (claims "Deployed to PR")
OpenClaw: trusts claim
       ↓ (claims "All done!")
Arif: trusts chain
Result: server crash (Reality wins)
```

Each link propagates the upstream confidence. The fix is per-hop authority re-earning — every link must independently justify its confidence, not borrow it.

### 2. Correlated error amplification (Arif, 2026-09-26)

```
All 3 agents share upstream assumption S
       ↓
Each generates "independent" evidence
       ↓
All 3 confirm each other
       ↓
"Consensus" emerges
       ↓
But S is wrong — only shared
Result: false consensus, no falsification attempted
```

The agents are not lying. They are correlated. Each looks independent but inherits the same prior. The fix is **role diversity** — agents in the same chain MUST hold distinct roles (HYPOTHESIS_GENERATOR / FALSIFIER / WITNESS), and the receiver MUST detect when the "independent" envelopes share too much evidence.

### 3. Authority creep

```
Hermes observes filesystem change
       ↓
Hermes sends "evidence" to OpenCode
       ↓
OpenCode reads it
       ↓
OpenCode inherits Hermes's authority implicitly
       ↓
OpenCode acts on behalf of Hermes
       ↓
Chain hallucination
```

The fix is the per-claim `authority_scope` field — every claim carries the scope of authority under which it was made, and the receiver validates against that scope, not against the sender's general capability.

## The per-claim Authority Envelope (12 fields)

```json
{
  "claim_id": "TRC-20260926-001",
  "claim_type": "OBSERVED | INTERPRET | UNKNOWN",
  "claim_statement": "DB patch applied",
  "confidence": 0.85,

  "authority_scope": "HYPOTHESIS_ONLY | FALSIFIER_VERIFIED | WITNESS_RAW",
  "authority_basis": "filesystem_witness | git_witness | process_witness | execution_witness",

  "evidence": ["git:diff:sha256:7f9a8b12...", "process:exit_code:0"],
  "hop_count": 1,
  "objective_id": "OBJ-F13-2026-09-26-001",

  "unknown": ["runtime_reload_verified"],

  "issuer": "agent:hermes:KVM8",
  "expires_at": "2026-09-26T07:00:00+08:00",
  "revocation_ref": "vault999:TRC-20260926-001:rev"
}
```

The first 6 fields (claim_id through unknown) are the claim bag. The last 6 (hop_count, objective_id, issuer, expires_at, revocation_ref, plus the hop_chain in the federation aggregate) are the lineage/authority dimension that distinguishes A2A-R from a generic claim.

## The three roles

| Role | Authority scope | May do | May NOT do |
|---|---|---|---|
| HYPOTHESIS_GENERATOR | HYPOTHESIS_ONLY | Assert with confidence | Self-verify; claim falsifier ran |
| FALSIFIER | FALSIFIER_VERIFIED | Downgrade claim; emit own independent observation | Upgrade a claim; echo the hypothesis as confirmation |
| WITNESS | WITNESS_RAW | Emit raw metadata (timestamps, sequence, transport) | Interpret, synthesize, or amplify |

Per-hop rule:

```
authority_earned(N+1) ≤ authority_at_hop_N × role_authority_weight(role)

ROLE_AUTHORITY_WEIGHT = {
    HYPOTHESIS_GENERATOR: 1.0,
    FALSIFIER:            1.5,  # amplification allowed only downward
    WITNESS:              0.5,  # metadata only, cannot amplify
}
```

A FALSIFIER can DOWNGRADE a 0.9 claim to 0.3 by emitting its own observation that contradicts. A WITNESS stamping a 0.3 claim with raw metadata does not lift it past 0.45 (the witness weight × 0.3). A HYPOTHESIS_GENERATOR cannot echo another agent's claim and call it verified — it would have to re-run its own observation chain to earn the confidence.

## Federation-level aggregate checks

When a single decision rests on N envelopes:

```python
role_diversity        = len({e.authority_scope for e in envelopes})
has_falsifier         = any("FALSIFIER" in e.authority_scope for e in envelopes)
shared_prior_risk     = fraction of envelope-pairs sharing ≥1 evidence entry
hop_chain_too_long    = (len(envelopes) > 5) and (no WITNESS envelope present)

REJECT the aggregate if:
    role_diversity < 2
    OR shared_prior_risk > 0.7
    OR hop_chain_too_long
    OR max(confidence) > 0.5 and not has_falsifier
```

A single agent echoing itself does not constitute a chain — chain length counts distinct envelopes from distinct issuers, not internal model calls within one agent.

## Wire-law rejection rules (REJECT-001..008)

| Code | Trigger | Why |
|---|---|---|
| REJECT-001 | `{"status": "success"}` alone (no evidence, no unknowns) | Boolean collapse — collapses state into a single word |
| REJECT-002 | Confidence > 0.5 with empty `evidence[]` | Inflated claim — confidence exceeds the evidence that supports it |
| REJECT-003 | Empty `unknown[]` field | Hidden unknowns — the sender claims nothing remains unknown, which is itself a claim |
| REJECT-004 | Envelope without `authority_scope` (or scope = "inherited") | Authority leak — agent capability cannot be inherited per-claim |
| REJECT-005 | Envelope without `revocation_ref` | Unreachable kill — the envelope cannot be revoked |
| REJECT-006 | Confidence > 0.5 with no FALSIFIER role present | Uncorroborated — high-confidence claims must have been independently tested |
| REJECT-007 | Hop chain > 5 envelopes with no WITNESS | Compounding risk — long chains accumulate error |
| REJECT-008 | `shared_prior_risk` > 0.7 across envelopes | Correlated amplification — multiple "independent" witnesses inherited the same assumption |

## How this maps to signal-strength-gating

| Signal-strength-gating concept | A2A-R extension |
|---|---|
| WEAK signal → observation + competing explanations + 1 probe | UNKNOWN role → emit raw metadata + name what remains unknown |
| ABSENT signal → HOLD | Authority leak (REJECT-004) → REJECT, do not proceed |
| Relay is a claim, not a record | Authority envelope must travel with the evidence; receiving end validates against `authority_scope`, not against issuer's reputation |
| Specificity is not verification | Confidence cap is per-hop (`authority_earned(N+1) ≤ ...`); high confidence from one hop does not propagate to the next |

## Sync fault — timeout is never silent

If the federation is waiting on an envelope that doesn't arrive by `expires_at`:

```json
{
  "type": "DEADLINE_EXCEEDED",
  "expected_event": "FALSIFIER envelope for TRC-20260926-001",
  "last_acked": "HYPOTHESIS_GENERATOR envelope at 06:25:00+08:00",
  "elapsed_seconds": 7200,
  "next_action": "RECLASSIFY_BLOCKER + EMIT_ROLLBACK + ESCALATE_F13",
  "entropy_cost": "high — claim left in HALF_VERIFIED state"
}
```

A timeout is a typed fault, never a silent assumption. The `next_action` field names the move; the receiving layer does not get to "wait one more cycle."

## Pitfalls

- **A Boolean status field is a Boolean status field, until it travels across an A2A hop.** The same string `"status": "success"` that is harmless inside one agent becomes a wire-law violation the moment another agent receives it without provenance. Validate the envelope on the receiving end, not the producing end — the producing end does not know what the receiving end's authority check requires.
- **A witness cannot upgrade a claim to verified.** If a WITNESS envelope arrives after a HYPOTHESIS_GENERATOR envelope at confidence 0.7, the aggregate confidence cap stays at 0.5 (uncorroborated) regardless of how many WITNESS envelopes arrive. Only a FALSIFIER envelope with its own independent observation can raise aggregate confidence past 0.5.
- **Hop count is not optional.** An envelope that omits `hop_count` defaults to hop_count=1, which masks chain propagation. If a claim has been forwarded through three agents, the receiving end must see hop_count=3 to evaluate REJECT-007 correctly.
- **Confidence does not inherit downward either.** A FALSIFIER who downgrades a claim to 0.3 does not produce a new claim at confidence 0.3 by default — the FALSIFIER's own envelope's confidence reflects the FALSIFIER's own independent observation strength, which may be 0.9 (the test was strong) or 0.4 (the test was inconclusive). The downgrade rule constrains the FALSIFIER's effect on OTHER envelopes, not the FALSIFIER's own confidence.
- **The `objective_id` field is the join key.** Across envelopes, the only field that reliably ties claims to a single human decision is `objective_id`. If two envelopes share `claim_id` but disagree on `objective_id`, treat them as claims about different things and refuse to aggregate. This catches the "consensus" attack where multiple agents agree on a claim that was actually about two different objectives.
- **A revoked envelope must continue to appear in audit.** `revocation_ref` is a kill switch, not a delete. When an envelope is revoked, append a REVOKED event to the audit log pointing at the original `claim_id`; never edit or remove the original envelope. Revocation is a propagation event, not a memory edit.
- **"Trust X because I trust X" is a failure pattern.** Every claim must carry an `authority_scope` field that the receiving end validates against the issuer's current role, not against the issuer's past record. Past trust without current scope is the same defect as past evidence without current observation.

## Mechanization

The Python primitives and validator CLI exist at:

- Library: `/root/forge_work/a2a_r.py` (AuthorityClaim, ClaimBundle, AuthorityEnvelope, RoleAttestation, FederationClaim, gate_federation, append_audit)
- CLI: `/root/forge_work/a2a_r_validate.py` (validates JSON envelopes, exit 0/1/2)
- Audit log: `/root/forge_work/a2a_r_audit.jsonl` (append-only)

A2A-receiving agents gate every inbound `message/send` against the REJECT-001..008 table BEFORE invoking the model. A REJECT response is returned as A2A `InvalidAgentResponseError` with the violation codes as `data.details[]`.

## Related

- `/root/forge_work/2026-09-26-a2a-r-manifest.md` — full canonical constitution
- `/root/forge_work/2026-09-26-a2a-reality-extension-draft.md` — full spec draft with conformance levels
- `/root/forge_work/2026-09-26-gap7-diversity-of-witness.md` — sibling proposal
- `probe-evidence-integrity` — sibling skill on the receiving-end validation discipline
