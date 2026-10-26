# AAA operating model

Use this reference when the task asks what AAA is, how to make work less chaotic, or how abstraction, attestation, and abduction should cooperate.

## AAA definition

AAA is the governed control-plane discipline for agentic intelligence:

1. **Abstraction**: name the correct level of reality and interface.
2. **Attestation**: prove or label the claim state.
3. **Abduction**: choose the best explanation or route from incomplete evidence, then test it.

AAA lowers entropy by preventing layer collapse:

- UI is not authority.
- Routing is not judgment.
- Evidence is not decision.
- Execution is not permission.
- Inference is not verified fact.
- Simulation is not live state.

## Orthogonality rules

### Abstraction

Ask:

- What layer owns the request?
- What object is being changed or explained?
- What interface is involved: repo, MCP, A2A, UI, runtime, document, policy?
- What is explicitly out of scope?

Return:

```text
OWNER:
INTERFACE:
BOUNDARY:
SOURCE OF TRUTH:
DISCARDED:          # distinctions this abstraction removed (what can no longer be distinguished)
INVARIANT_UNDER:    # transformations where the answer MUST stay the same (e.g. display colour, harmless paraphrase, unit-preserving rewrite, alias-of-same-principal)
EQUIVARIANT_UNDER:  # structured transformations where the output must transform correspondingly (e.g. reference-frame change)
SENSITIVE_TO:       # transformations where the answer MUST change (e.g. negation, recipient, quantity, revoked permission, different principal)
INVALIDATION:       # observations that would falsify this abstraction's validity for its task
```

These five fields close the abstraction audit loop with explicit transformation semantics.
A representation is valid only while (a) the distinctions it dropped stay irrelevant
(INVARIANT_UNDER holds), and (b) the distinctions it kept still change the decision
when meaning changes (SENSITIVE_TO fires). Unit changes that preserve the physical
quantity are INVARIANT_UNDER; unit changes that alter it are SENSITIVE_TO. An alias
resolving to the same principal is INVARIANT_UNDER; a different principal is
SENSITIVE_TO. Identity semantics must be settled before classifying a mismatch as
a canonicalization defect (answer wrongly stable) or a sensitivity defect (answer
rightly changed).

### Attestation

Use these evidence labels:

| Label | Meaning |
|---|---|
| FACT | Directly supported by current evidence or user authority |
| OBSERVED | Seen in live output, logs, tests, or tool result |
| DERIVED | Computed from facts with visible method |
| INFERRED | Reasonable but not directly proven |
| HYPOTHESIS | Plausible route/explanation awaiting test |
| UNVERIFIED | Claimed but unsupported |
| SIMULATION | Non-authoritative rehearsal |

Never upgrade a label without evidence.

### Abduction

Use abduction when evidence is incomplete. It is not guessing; it is disciplined best-explanation reasoning.

Return:

```text
BEST EXPLANATION:
WHY THIS ROUTE:
MISSING EVIDENCE:
VALIDATION STEP:
FAIL-CLOSED CONDITION:
```

## Recursive governed loop

For complex tasks, repeat until entropy falls:

```text
observe -> abstract -> attest -> abduce -> route -> gate -> compose -> verify
```

Stop recursion when one of these is true:

- The owner organ is clear.
- The evidence class is clear.
- The risk tier is clear.
- The next action is reversible and minimal.
- Further recursion adds vocabulary but no decision value.

## Entropy smell list

Flag these as chaos indicators:

- One request asks for design, deployment, constitutional judgment, and capital decision in the same sentence.
- A repo owns both UI routing and final authority.
- A tool can mutate state but no approval path is named.
- An architecture diagram is treated as live runtime proof.
- A simulated verdict is phrased as a real SEAL.
- A domain organ computes and decides its own consequence.
