---
name: arifos-kernel-ceremony
description: Use when running arifOS kernel init/judge/seal ceremony.
version: 1.0.0
owner: Hermes
risk_tier: high
floor_scope: [F1, F2, F4, F11, F13]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# arifOS Kernel Ceremony — init → judge → seal (via MCP)

> **DITEMPA BUKAN DIBERI**

## When to use

Any time you must obtain a constitutional verdict or write an irreversible seal
through the arifOS kernel from an MCP host:

- `arif_judge` on a deployment, change, or irreversible candidate
- `arif_seal` / `arif_vault_seal` to write to VAULT999
- Reaching F13 SOVEREIGN authority for a ceremony the sovereign delegated to you

Not for reading floor doctrine, and not for routine `arif_observe` reads.

## Iron rules

| # | Rule |
|---|------|
| C1 | `arif_judge` at the **default action tier is capped at 200 ms and degrades to a false SABAR** before it reasons. Pass `action_tier="sovereign"` (C4, unbounded) for any seal / irreversible / multi-step candidate. |
| C2 | A verdict whose only reason is `LATENCY_TIMEOUT` is a **clock reading, not a judgment**. Never report it as a floor decision; re-run unbounded first. |
| C3 | A **string-matched actor id is not authentication.** Declaration is not proof. |
| C4 | Read `result.effective_state.authority_band` (and `seal_allowed`) — never infer authority from the actor name you sent. |
| C5 | **Ground evidence first-hand.** Never relay the reporting agent's numbers as your own observation. |
| C6 | A judge HOLD writes **no** seal. "Chain unchanged at N" is a correct outcome, not a failure. |
| C7 | A seal signed by an agent on the sovereign's behalf MUST record `caller_actor_id`, `executor_actor_id`, `delegation_mode="delegated"`. |
| C8 | Never manufacture a missing witness channel. If a floor is short on the human or external channel, name it and stop. |

## Procedure

### Step 1 — init, and know what band you actually hold

```
arif_init(actor_id="<actor>", mode="preflight")   # cheap: what do I hold?
arif_init(actor_id="<actor>", mode="init")        # bind the session
```

Read `result.effective_state.authority_band`. A claim-only init binds the session but
grants limited authority — enough to observe, not to seal.

**To reach F13 SOVEREIGN (the only path to `seal_allowed: true`):**

1. `arif_init(mode="challenge", actor_id=...)` → `nonce` + `signature_payload`
   (form `<ACTOR>:<nonce>`), single-use, ~120 s TTL.
   `mode="challenge"` may be missing from the declared enum yet still be handled —
   test behaviour, not just the schema.
2. Sign `signature_payload` **exactly** — Ed25519, sovereign private key.
3. `arif_init(mode="init", actor_signature=<b64>, nonce=<nonce>)`.
4. Confirm `authority_band: FULL` and `seal_allowed: true`.

Before signing, confirm the key in hand matches a registered key id:
`ed25519:sha256:<first 16 hex of sha256(RAW public key bytes)>`. RAW bytes — **not**
DER, **not** PEM; the digest differs per encoding and a wrong encoding looks like a
key mismatch when the key is correct.

### Step 2 — ground the evidence yourself

Probe the subject directly. Whatever the reporting agent said, your evidence must be
yours. Cheap, decisive probes: service state, per-organ health over the **documented**
ports, repo head vs upstream, and a cross-check of any hash the kernel reports about
itself against what you measured.

If two of your numbers disagree with the report, say so — a self-correction recorded in
the evidence is worth more than a clean-looking package.

### Step 3 — judge

```
arif_judge(
  action_tier="sovereign",        # C4, unbounded — see C1
  candidate="<prose, a STRING>",  # structure goes in evidence, not here
  evidence={...},                 # must satisfy the hard gates
  session_token=<SCT>,
)
```

The hard gates check **shape**: a grounded key plus, for irreversible/sovereign
candidates, a structurally complete `causal_cascade`. The exact key lists, the cascade
schema, and what each rejection message means:
`references/arif-judge-mcp-ceremony.md`.

Write the cascade honestly. For an append-only ledger, `reversibility` is
`IRREVERSIBLE` and `recovery_path` is correction-by-supersession, not rollback.
Claiming reversibility to clear the gate is the failure the gate exists to catch.

### Step 4 — read the verdict

Thresholds that hold a seal: `L02` Truth Score ≥ **0.99**, `L03` W4 Consensus ≥ **0.85**.
W4 is a geometric mean `(H, A, E, V)` — the **lowest channel dominates**, so a strong
AI score cannot rescue a weak human or external channel. A low `H` means no human
witnessed it: that is the constitution working. Name the short channel to the
sovereign; do not supply the missing number yourself.

### Step 5 — seal, then confirm

Seal only with both a judge `cc_id` and sovereign authority. Then verify with
`arif_seal(mode="verify")` and compare `ledger_size` before/after. Do not hunt the
filesystem for the chain file — `ledger_size` (all entries) and
`canonical_audit.entries` (verified canonical scope) are different scopes, and
`integrity: GAPS_FOUND` alongside a verified canonical chain is not corruption.

## Pitfalls

- **Reading a timeout as a verdict.** The single most expensive trap here: a
  default-tier judge returns a well-formed `SABAR` that no floor ever decided.
- **Probing an endpoint you assumed.** A conn-refused on a port or unit name you
  invented is not evidence of an outage. Resolve the port from the topology SOT, and
  before declaring anything down, re-probe with the documented name.
- **Passing a dict as `candidate`.** It is parsed as JSON; the verification state
  silently drops out and the verdict is quietly weaker.
- **Assuming a seal failed when it was refused.** A HOLD writes nothing by design.
- **Burning a token into a transcript.** Sessions are TTL-bound and revocation on the
  token lane is not dependable — verify a revoke path exists before relying on one;
  otherwise treat any token that leaked into a log as burned and let it expire.

## References

- `references/arif-judge-mcp-ceremony.md` — latency classes, the hard-gate evidence
  schema with exact key lists, the verdict envelope, the SOVEREIGN signature path, and
  seal confirmation.
