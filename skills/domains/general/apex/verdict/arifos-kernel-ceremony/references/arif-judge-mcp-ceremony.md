# arif_judge / arif_seal via MCP — getting a REAL verdict

Every failure mode below is **silent**: the call returns a well-formed envelope with
the wrong verdict, not an error. Read the `reasons` string — the hard gates name
themselves exactly.

## 1. Latency class decides whether deliberation happens at all

`arif_judge` maps `action_tier` to a hard latency budget. The default is a trap:

| action_tier | class | budget | on timeout |
|---|---|---|---|
| omitted / `standard` | C2_STANDARD | 200 ms | degrades to **SABAR** |
| `elevated` | C3_DEEP | 1000 ms | degrades to HOLD |
| `sovereign` / `c4` / `c5` | C4_SOVEREIGN | unbounded | — |

Real deliberation on a non-trivial candidate takes **seconds**. At the default tier the
judge is killed at 200 ms before it reasons and returns a valid-looking
`verdict: "SABAR"` whose only reason is `LATENCY_TIMEOUT`. That SABAR is a clock
reading, not a judgment.

- For any seal / irreversible / multi-step candidate: pass `action_tier="sovereign"`.
- Tell-tale: `meta.within_budget == false`, `meta.latency_ms == meta.budget_max_ms`
  exactly (killed at the deadline), `meta.timeout_enforcement == "preventive"`.
- A HOLD/SABAR you did not ask for is **not a floor decision** until you have re-run
  unbounded at least once. Escalating to the unbounded class is the kernel's own
  documented remedy — the degradation message itself says so.
- Payload size is **not** the cause. A leaner evidence dict changes nothing; only the
  class does.

## 2. Evidence schema: the hard gates reject shape, not substance

### F2 TRUTH grounding

For `action_tier in (sovereign, c4, c5, T2, T3)` or
`reversibility in (IRREVERSIBLE, MUTATE)`, the `evidence` dict MUST contain at least
one of:

```
observed_state  receipt  source  records  telemetry
 diff           metrics  grounding  observation  findings
```

None present → `VOID / F2_TRUTH_VIOLATION: Substantive mutation requires structured
observation/receipt grounding.` Free-form prose keys do not count.

### causal_cascade

Required for L3+/irreversible mutation:

```json
{"causal_cascade": {
  "steps": [
    {"phase": "immediate", "effect": "...", "affected_party": "..."},
    {"phase": "secondary", "effect": "...", "affected_party": "..."},
    {"phase": "tertiary",  "effect": "...", "affected_party": "..."}
  ],
  "recovery_path": "...",
  "reversibility": "...",
  "omission_consequence": "..."
}}
```

- `steps` needs **≥3** entries.
- Each step needs `effect` **or** `description`, AND `affected_party` **or**
  `affected_parties`. A step carrying only prose in an unread key fails.
- `omission_consequence` must be non-empty — the judge asks "what if we do nothing?".
- Absent → `HOLD / Missing causal_cascade for L3+/irreversible mutation`.

### candidate must be a string

Passing a dict where the candidate is parsed yields
`meta.parse_warning: ["candidate JSON unparseable — verification state not extracted"]`
and the verification state silently drops out of the judgment. Put structure in
`evidence`, prose in `candidate`.

## 3. Reading the verdict

The scored envelope sits under `result.reason` (keys `L01`…`L10`) when the judge
reasons fully. The ones that hold a seal:

- `L02` Truth Score — threshold **≥ 0.99**
- `L03` W4 Consensus — threshold **≥ 0.85**, reported as `(H, A, E, V)`

W4 is a geometric mean, so the **lowest channel dominates** — a high AI score cannot
rescue a weak human or external channel. When a delegated seal is held, identify which
channel is short before proposing anything. A low `H` means no human witnessed it, and
that is the constitution working, not an obstacle to route around. Tell the sovereign
which channel is short; never manufacture the missing number.

Also read `meta.latency_ms` / `within_budget` before trusting the verdict at all (see
§1), and `judge_postcondition.verdict_channel_integrity`.

## 4. Reaching F13 SOVEREIGN (the only path to seal)

Seal needs `seal_allowed: true`, which needs `authority_band: FULL`/`SOVEREIGN`.
**String-matching the actor id is not authentication** — a claim-only init binds the
session at limited authority, and the response will still self-attest verification it
did not perform. Trust `effective_state`, not the top-level attestation.

1. `arif_init(mode="challenge", actor_id=...)` → `nonce` + `signature_payload`
   (form `<ACTOR>:<nonce>`), single-use, ~120 s TTL.
2. Sign `signature_payload` **exactly** — Ed25519, sovereign private key.
3. `arif_init(mode="init", actor_signature=<b64>, nonce=<nonce>)`.
4. Confirm `authority_band: FULL`, `seal_allowed: true`.

Key-id interoperability:

```
ed25519:sha256:<first 16 hex chars of sha256(RAW public key bytes)>
```

RAW public-key bytes — **not** DER and **not** PEM. Verify the key in hand against a
registered id *before* signing; checking the wrong encoding looks like a key mismatch
when the key is correct.

### Delegation provenance

When an agent signs on the sovereign's behalf, record `caller_actor_id=<sovereign>`,
`executor_actor_id=<agent>`, `delegation_mode="delegated"`. Without them the ledger
claims a verification that did not physically occur — the exact breach the schema
exists to prevent. Say plainly which hand signed, and offer the sovereign the choice
between signing personally, delegating, and leaving the work unsealed.

**Unsealed ≠ broken.** Work that runs correctly but is not attested is a weaker
*record*, not a safety defect. Say so rather than manufacturing urgency.

## 5. Confirming a seal actually landed

Use `arif_seal(mode="verify")` — do not hunt the filesystem for the chain file.

- Compare `result.ledger_size` **before and after**. Unchanged means nothing was
  written; report "chain unchanged at N" rather than implying a partial write.
- `result.canonical_audit` reports `entries` / `head_hash` / `gap_count` for the
  verified canonical scope.
- `result.integrity` may read `GAPS_FOUND` while `canonical_chain_verified` is true,
  because `ledger_size` counts entries beyond the canonical chain. Two different
  scopes — report both and name the scope rather than calling it corruption.

A judge HOLD writes **no** seal. No new entry after a HOLD is the correct outcome; do
not retry the seal or route around the judge to force one.
