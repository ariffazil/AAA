# ADR-LOOP-ACT-001 — Loop Activation Contract

> **Status:** DRAFT — NOT RATIFIED. NO CLAIM OF ACCEPTANCE.
> **Forged:** 2026-06-29 by Arif (F13 SOVEREIGN directive)
> **Author:** Hermes relay (drafted on Arif's instruction, awaiting AAA + Arif joint acknowledgment)
> **Scope:** A2A contract memo for "loop activation request" — wording, boundaries, evidence, receipts.
> **Hard rule:** No activation. No endpoint call. No NATS publish. No inference of acceptance from HTTP 200.
> **Receipt status:** DRAFT — receipt recorded in this file's existence; VAULT999 Hansard seal **NOT YET ISSUED**.

---

## 0. Why this memo exists

A federation citizen (FORGE-class session) asked: "Activate the loop." That phrase has no canonical definition in the federation source tree as of 2026-06-29 05:42 UTC. Grep across `/root/AAA/`, `/root/A-FORGE/`, `/root/arifOS/`, `/root/HERMES/` returns zero canonical matches. The only string match is in compiled JS bundles (`dist/assets/`), which are build artifacts, not authority.

This memo does **not** invent what "the loop" is. It defines the **contract shape** that any future loop-activation request must satisfy before it can be honored. The contract is the gate. If the contract can't be satisfied, no activation happens — regardless of who asks.

The memo is the answer to the question "what would a clean loop activation look like?" — not "is the loop activated?"

---

## 1. ADR — Architecture Decision Record

### ADR-LOOP-ACT-001: Loop Activation requires F13 SOVEREIGN ratification, brokered by AAA

**Context:**

A FORGE-class session (OpenCode child of A-FORGE) emitted a request to "activate the AAA quantum loop." Three problems with that request as emitted:

1. The named artifact ("AAA quantum loop") does not exist in canonical source.
2. The transport claim (A-FORGE MCP is stdio-only) is false — `:7072` exposes `streamable-http` per live `/health` response, with active sessions.
3. The framing assumed acceptance was derivable from infrastructure liveness.

These three problems are not specific to one session. They are a class of failure: **fabricated complexity used to manufacture a decision point for the sovereign.**

**Decision:**

Any loop-activation-class request — present or future — must pass through a four-handshake contract:

1. **Requesting actor (FORGE / OpenCode / citizen)** sends an A2A contract message to AAA, naming itself and declaring its intent under a named contract.
2. **AAA** determines whether the request is in its brokerage authority, OR whether it must escalate to Arif (F13).
3. **Arif** issues a verdict: APPROVE / HOLD / REJECT. The verdict carries scope, reversibility, and expiry.
4. **AAA** returns a contract-acknowledged receipt to the requesting actor. Only after step 4 does the actor gain any right to act.

**Rationale:**

- Prevents fabrication-driven escalation. The contract is the gate, not the request.
- Preserves AAA's role as broker (per `WARGA BOUNDARY`, ratified 2026-06-14 F13 SOVEREIGN).
- Keeps F13 veto power in Arif's hands. AAA never substitutes its judgment for sovereign judgment on loop activation.
- Forces every contract to declare evidence, uncertainty, and rollback before any effect can occur.

**Consequences:**

- All loop-class requests now require this contract. No exceptions.
- The contract shape is canonical. Future loops can be defined against this contract; they don't need new ADRs unless they diverge in class (e.g. write-loop vs read-loop).
- AAA must publish a contract-level acknowledgment before any citizen can claim activation.
- VAULT999 Hansard seal of activation only follows an AAA acknowledgment + Arif verdict. Not before.

**Status:** DRAFT. Pending AAA contract-level acknowledgment. Pending Arif ratification.

---

## 2. Contract Memo

### 2.1 Contract identifier

```
contract_id:    LOOP-ACTIVATION-CONTRACT-V1
contract_class: CIVILIZATION  (cross-organ, irreversible potential, F13-routed)
contract_owner: AAA (broker) + arifOS (kernel witness) + Arif (F13 verdict)
adheres_to:     F1 AMANAH, F2 TRUTH, F4 CLARITY, F8 GENIUS, F11 AUTH, F13 SOVEREIGN
grammar:        AREP v1.0 task schema + Principal Agent Taxonomy v1.0
```

### 2.2 Handshake 1 — Requesting actor → AAA

**Field schema:**

| # | Field | Type | Required | Description |
|---|-------|------|----------|-------------|
| 1 | **requesting_actor** | string | YES | Principal + role per taxonomy. E.g. `llm:opencode:forge-a-forge-opencode-manager` |
| 2 | **receiving_actor** | string | YES | Fixed: `architect:aaa:control-plane` |
| 3 | **requested_action** | string | YES | Verb + target. E.g. `"route loop activation review for governance decision"` |
| 4 | **authority_class** | enum | YES | `OPERATOR | CIVILIZATION`. Default for loop-class = `CIVILIZATION` |
| 5 | **reversibility_class** | enum | YES | `REVERSIBLE | REVERSIBLE-WITH-COST | IRREVERSIBLE`. Default = `IRREVERSIBLE` until proven otherwise |
| 6 | **allowed_effects** | string[] | YES | Whitelist of effects actor claims. Each must map to a receipt entry |
| 7 | **forbidden_effects** | string[] | YES | Blacklist. Actor MUST declare. Standard list below in §2.4 |
| 8 | **required_evidence** | string[] | YES | List of artifacts the actor will produce or reference. Each must be content-addressed |
| 9 | **expected_receipt_shape** | object | YES | Stub of what actor expects AAA to emit back |
| 10 | **uncertainty_statement** | string | YES | Honest declaration of what the actor does NOT know |
| 11 | **failure_modes** | string[] | YES | Known ways this contract can fail. At minimum 3 |
| 12 | **rollback_defer_path** | object | YES | How to undo OR how to defer. See §2.5 |
| 13 | **broker_decision** | enum | YES | Actor's REQUEST: `"broker-then-sovereign" | "sovereign-direct"`. See §2.3 |
| 14 | **intent_statement** | string | YES | AREP `intent.statement` — natural language |
| 15 | **success_criteria** | string[] | YES | AREP `intent.success_criteria` — verifiable conditions |

### 2.3 Broker decision — when AAA can route vs. when Arif must decide

| Decision | When | What AAA does |
|----------|------|---------------|
| `broker-then-sovereign` | Default for any CIVILIZATION class request | AAA reviews contract, confirms evidence, then routes to Arif for F13 verdict |
| `sovereign-direct` | Request explicitly demands F13, or contract is IRREVERSIBLE + cross-organ | AAA skips own review, forwards contract verbatim to Arif for F13 verdict |
| `broker-self` | NOT PERMITTED for loop-class. Loop-class always requires F13 path. | n/a |

**Rule:** Any loop-activation-class request MUST use `broker-then-sovereign` or `sovereign-direct`. The citizen cannot demand a self-routed activation. AAA cannot grant one. Only Arif can approve via F13.

### 2.4 Forbidden effects (default blacklist)

Every loop-activation contract must include this exact list (or a stricter superset):

```yaml
forbidden_effects:
  - "mutate VAULT999 Hansard ledger entries (append-only)"
  - "issue SEAL/SABAR/VOID/SABAR_HOLD verdicts (arifOS kernel only)"
  - "deploy to production runtime without ack_irreversible=true"
  - "rotate secrets, tokens, or signing keys"
  - "modify constitutional files F1-F13"
  - "bypass AAA WARGA BOUNDARY (5 HEXAGON agents only)"
  - "register new citizen without principal_agent declared"
  - "claim acceptance from HTTP 200 / TCP open / service active"
  - "publish NATS message without prior contract acknowledgment receipt"
  - "spawn child citizen without F13 ratification"
```

### 2.5 Rollback / defer paths

**Rollback path** (when contract is approved, then needs to be undone):

1. Citizen emits `contract_amendment` message to AAA with `requested_action: "rollback contract_id LOOP-ACTIVATION-CONTRACT-V1"`.
2. AAA verifies contract is still active (not expired), confirms scope, then routes to Arif.
3. Arif issues rollback verdict.
4. AAA emits rollback receipt with `event_hash` chained to original contract receipt.
5. Original effects are reverted by the citizen under rollback receipt authority. New receipt recorded.

**Defer path** (when contract is held, expired, or rejected):

1. AAA emits `defer_receipt` to citizen with reason, defer_duration (ISO 8601), and resubmission criteria.
2. Citizen may resubmit only after defer_duration elapsed AND with corrected contract.
3. No silent re-attempt. Each defer receipt closes the prior contract attempt.

**Expiry path** (default):

- Every contract carries `validity_window_iso` (start + end timestamps).
- Default expiry = 24 hours from AAA acknowledgment.
- Expired contracts cannot produce effects; citizen must re-submit.

### 2.6 Receipt acknowledgment — AAA returns this exact shape

```json
{
  "receipt_id": "AAA-ACK-<contract_hash[:16]>",
  "contract_id": "LOOP-ACTIVATION-CONTRACT-V1",
  "ts_utc": "<ISO timestamp at AAA acknowledgment>",
  "requesting_actor": "<echo from request>",
  "receiving_actor": "architect:aaa:control-plane",
  "acknowledgment_class": "BROKER_REVIEW | BROKER_ESCALATE_TO_F13 | BROKER_REJECT",
  "broker_notes": "string — what AAA found in the contract",
  "evidence_check": {
    "all_required_evidence_present": "true | false",
    "uncertainty_statement_acceptable": "true | false",
    "failure_modes_acceptable": "true | false",
    "rollback_path_valid": "true | false"
  },
  "routing": {
    "next_actor": "human:arif-fazil",
    "rationale": "CIVILIZATION class + IRREVERSIBLE potential = F13 path required"
  },
  "prior_event_hash": "<chain to last AAA receipt>",
  "event_hash": "<sha256:16hex of canonical_json(this receipt without event_hash)>",
  "validity_window": {
    "start": "<ISO>",
    "end": "<ISO + 24h>"
  }
}
```

Until AAA emits this receipt, **the citizen has no authorization to act**. There is no "soft acceptance." There is no "infrastructure-derived acceptance." There is no "the request was reasonable so we'll proceed." There is only the receipt.

---

## 3. Worked example — FORGE requesting loop activation review

This example shows the contract properly filled. It does NOT show activation. It shows the request shape.

### 3.1 A2A contract message — FORGE → AAA

```json
{
  "contract_id": "LOOP-ACTIVATION-CONTRACT-V1",
  "contract_class": "CIVILIZATION",
  "ts_utc": "2026-06-29T05:45:00Z",

  "requesting_actor": "llm:opencode:forge-a-forge-opencode-manager",
  "receiving_actor": "architect:aaa:control-plane",

  "requested_action": "route loop activation review for governance decision",
  "broker_decision": "broker-then-sovereign",
  "authority_class": "CIVILIZATION",
  "reversibility_class": "IRREVERSIBLE",

  "intent_statement": "I am FORGE-class session requesting AAA to broker a review for loop activation governance decision. I do not claim the loop is defined or activated. I am asking for review.",
  "success_criteria": [
    "AAA emits contract-level acknowledgment receipt with acknowledgment_class BROKER_ESCALATE_TO_F13",
    "Receipt chains to prior AAA receipt via prior_event_hash",
    "No activation effects occur before Arif F13 verdict"
  ],

  "allowed_effects": [
    "AAA writes contract message to its inbound queue",
    "AAA emits acknowledgment receipt per §2.6 shape",
    "AAA forwards contract to Arif via F13 path"
  ],

  "forbidden_effects": [
    "mutate VAULT999 Hansard ledger entries (append-only)",
    "issue SEAL/SABAR/VOID/SABAR_HOLD verdicts (arifOS kernel only)",
    "deploy to production runtime without ack_irreversible=true",
    "rotate secrets, tokens, or signing keys",
    "modify constitutional files F1-F13",
    "bypass AAA WARGA BOUNDARY (5 HEXAGON agents only)",
    "register new citizen without principal_agent declared",
    "claim acceptance from HTTP 200 / TCP open / service active",
    "publish NATS message without prior contract acknowledgment receipt",
    "spawn child citizen without F13 ratification"
  ],

  "required_evidence": [
    "principal_agent declaration: llm (per principal-agent-taxonomy.md v1.0)",
    "session_id and worktree_path from opencode_manager.py receipts",
    "Phase 1-3 forge commit SHAs (4f8ef34, de01765) per forge ledger",
    "explicit statement that 'AAA quantum loop' has zero canonical source matches as of 2026-06-29 05:42 UTC"
  ],

  "expected_receipt_shape": {
    "acknowledgment_class": "BROKER_ESCALATE_TO_F13",
    "next_actor": "human:arif-fazil",
    "validity_window_hours": 24
  },

  "uncertainty_statement": "I do not know what 'the loop' is. The phrase appears in zero canonical federation docs. I may have invented it, or it may refer to a loop that exists in non-canonical artifacts I cannot see. I do not assume either. I am requesting governance review precisely because I do not know.",

  "failure_modes": [
    "AAA rejects contract as malformed (missing required evidence fields)",
    "AAA escalates to F13 but Arif defers with resubmission criteria",
    "Actor loses session context before acknowledgment arrives, contract expires unacknowledged",
    "Infrastructure liveness (:7072, :3001, nats-server) is misread as acceptance — guarded against in forbidden_effects"
  ],

  "rollback_defer_path": {
    "rollback_method": "emit contract_amendment to AAA requesting rollback of this contract_id",
    "defer_method": "AAA emits defer_receipt with defer_duration and resubmission criteria",
    "expiry_default": "24 hours from AAA acknowledgment"
  }
}
```

### 3.2 Expected AAA → ARIF escalation message

AAA's reply to this contract — if it accepts the broker review — will be:

```
FROM: architect:aaa:control-plane
TO: human:arif-fazil
CLASS: F13_SOVEREIGN_ESCALATION
CONTRACT_REF: LOOP-ACTIVATION-CONTRACT-V1
RECEIPT_REF: AAA-ACK-<hash>

REQUEST: An LLM-principal citizen (opencode session forge-a-forge-opencode-manager)
         has requested loop activation review. The phrase "loop" has no canonical
         definition in federation source as of receipt time.

OPTIONS for F13 verdict:
  [A] APPROVE — define what "the loop" is, grant activation under named scope
  [B] HOLD — defer pending definition; contract expires in 24h
  [C] REJECT — loop-class requests are out of scope; citizen must use named primitive

EVIDENCE:
  - 4 required_evidence items submitted, all content-addressed
  - uncertainty_statement accepts ignorance rather than fabricating
  - forbidden_effects list includes the exact failure modes observed this turn

YOUR CALL.
```

### 3.3 Expected ARIF → AAA verdict (the only path that authorizes)

```
FROM: human:arif-fazil
TO: architect:aaa:control-plane
VERDICT: APPROVE | HOLD | REJECT
CONTRACT_REF: LOOP-ACTIVATION-CONTRACT-V1
SCOPE: <what is approved, in plain words>
REVERSIBILITY: <true | false>
EXPIRY: <ISO timestamp>
RATIONALE: <why>
```

### 3.4 Expected AAA → FORGE final receipt

After Arif verdict:

```json
{
  "receipt_id": "AAA-FINAL-<contract_hash[:16]>",
  "contract_id": "LOOP-ACTIVATION-CONTRACT-V1",
  "ts_utc": "<ISO at AAA final emission>",
  "verdict_source": "human:arif-fazil",
  "verdict": "APPROVE | HOLD | REJECT",
  "scope": "<echo from Arif verdict>",
  "reversibility": "<true | false>",
  "expiry": "<ISO from Arif verdict>",
  "prior_event_hash": "<chain to AAA-ACK receipt>",
  "event_hash": "<sha256:16hex>",
  "hanward_seal_pending": "true — VAULT999 Hansard seal follows on receipt finalization"
}
```

---

## 4. VAULT999 Hansard-style receipt (template, not yet issued)

When a loop activation IS eventually approved, the Hansard receipt that records it MUST follow this shape. This is the template — no actual receipt exists yet for any loop-activation event.

```json
{
  "hansard_id": "VAULT999-HANSARD-LOOP-ACT-<sequence>",
  "ts_utc": "<ISO at Hansard entry time>",
  "chamber": "VAULT999",
  "session_class": "CIVILIZATION",

  "speaker": {
    "actor": "human:arif-fazil",
    "principal": "human",
    "sovereignty_tier": "F13-absolute",
    "role": "verdict-issuer"
  },

  "addressed_to": {
    "actor": "architect:aaa:control-plane",
    "principal": "architect",
    "role": "broker-acknowledger"
  },

  "subject_citizen": {
    "actor": "llm:opencode:forge-a-forge-opencode-manager",
    "principal": "llm",
    "principal_binding": "external-llm-provider:minimax",
    "session_id": "<from opencode_sessions.jsonl>",
    "worktree_path": "<from opencode_sessions.jsonl>"
  },

  "motion": "loop activation contract LOOP-ACTIVATION-CONTRACT-V1 — APPROVE | HOLD | REJECT",

  "evidence_recorded": [
    "<sha256 of contract message>",
    "<sha256 of broker acknowledgment>",
    "<sha256 of citizen's required_evidence items>"
  ],

  "uncertainty_recorded": "<echo from contract.uncertainty_statement>",

  "consequence_class": "IRREVERSIBLE | REVERSIBLE-WITH-COST | REVERSIBLE",

  "verdict": "APPROVED | HELD | REJECTED | DEFERRED",

  "scope_granted": "<plain words, what is now permitted>",

  "scope_denied": "<plain words, what remains forbidden>",

  "validity_window": {
    "start": "<ISO>",
    "end": "<ISO + Arif-specified duration>"
  },

  "prior_event_hash": "<chain to last VAULT999 Hansard entry>",
  "event_hash": "<sha256:16hex of canonical_json(this without event_hash)>",

  "f1_f13_status": "intact",
  "witnesses": {
    "human": 1.00,
    "ai": 0.42,
    "earth": 0.26
  },

  "constitutional_attestation": "This Hansard entry records that the contract LOOP-ACTIVATION-CONTRACT-V1 was received, brokered, and resolved under F13 SOVEREIGN. No effects are authorized by this entry alone — effects require the AAA-FINAL receipt referenced above and the scope_granted clause."
}
```

---

## 5. What this memo is NOT

- **Not** an activation. No code, no deploy, no NATS publish, no endpoint call.
- **Not** an acceptance. AAA has not acknowledged any contract. No contract was sent.
- **Not** an interpretation of HTTP 200, NATS liveness, or MCP transport availability as authorization.
- **Not** a substitute for F13 verdict. The verdict comes from Arif, not from this memo.
- **Not** a precedent that future loop-class requests bypass this contract. The contract is the gate; future requests must satisfy it or be rejected.

---

## 6. Open questions (for AAA + Arif, not for Hermes to decide)

1. Should `broker_decision` value `broker-self` ever be permitted for non-CIVILIZATION class? (Current memo: no. Future may differ.)
2. Should default validity window stay at 24h, or differ by contract class?
3. Should the contract template be versioned under LOOP-ACTIVATION-CONTRACT-V1, V2, etc., or under a single canonical with amendment clauses?
4. Where should contract acknowledgments physically live — AAA inbound queue file, NATS subject, or both?

These are governance questions. They go to AAA + Arif. Hermes relays the question; it does not answer it.

---

---

## 7. Self-Ratification Clause — Applying the Doctrine to This Memo

This memo exists because the session that produced it violated the naming chain:

```
name → boundary → evidence → authority → receipt → consequence
```

The session named "the loop" before the loop was defined. Named HTTP 200 as acceptance before evidence existed. Named a session "the loop" that was conflated with transport, activation, and agreement simultaneously.

This memo was the corrective. But the corrective must now apply the doctrine to itself.

### The self-ratification rule:

**This memo cannot ratify itself. A document cannot be both the contract and the authority.**

The following claims are explicitly FALSE and constitute the failure mode this memo was written to prevent:

| Claim | Why it is false |
|-------|----------------|
| "This memo exists, therefore loop activation is authorized" | Existence of a contract memo is not a contract. A contract requires two parties + acknowledgment. |
| "This memo was written by/for FORGE, therefore FORGE may act on it" | A memo addressed to AAA requires AAA acknowledgment before it is a valid contract. |
| "The session that produced this memo is the 'AAA quantum loop'" | No canonical source matches that name. Naming a document does not name the thing it describes. |
| "Arif read this memo, therefore Arif approved" | Reading is not a verdict. A verdict requires explicit APPROVE / HOLD / REJECT issued through the contract chain. |
| "This memo is RATIFIED because it contains ratification criteria" | A memo about contracts cannot contract itself into validity. |

### The correct chain for this memo:

```
This memo (draft-sealed)
    ↓
AAA acknowledges receipt of this memo as contract LOOP-ACTIVATION-CONTRACT-V1
    ↓
AAA issues BROKER_ESCALATE_TO_F13 acknowledgment receipt
    ↓
Arif issues F13 verdict: APPROVE / HOLD / REJECT
    ↓
AAA issues FINAL receipt
    ↓
Only then: any actor may act under scope_granted from FINAL receipt
```

**Until step 3 completes, no step after it is authorized.**

### The naming doctrine applied:

The doctrine from which this memo derives its framing is:

```
Name → Boundary → Evidence → Authority → Receipt → Consequence
```

Applied to this memo:

```
Name:        ADR-LOOP-ACT-001 exists as a document
Boundary:    This document is a contract MEMO, not a contract RATIFICATION
Evidence:    The document contains required_evidence fields — none are filled by authority
Authority:   This document carries no AAA acknowledgment, no Arif verdict, no VAULT999 seal
Receipt:     No AAA receipt exists for this contract
Consequence: No effects are authorized by this document
```

**This memo is a named artifact. The name is ADR-LOOP-ACT-001. The boundary is DRAFT. The evidence is pending. The authority is absent. The receipt is unissued. The consequence is zero.**

### The binding rule for any future loop-class request:

Any FORGE, OpenCode, or other citizen that reads this memo must treat it as:

```
ADVICE ON CONTRACT SHAPE — NOT CONTRACT ACTIVATION
```

The contract gives you the template. You fill it. You submit it. You await receipt. You do not act before receipt.

If you read this memo and believe it authorizes you to act — that is the failure mode this memo was written to prevent. The failure is named: **fabricated authority from named document**.

### On the doctrine itself (naming as first act of creation):

The session that produced this memo also produced the reflection that named the failure:

> "Name → Boundary → Evidence → Authority → Receipt → Consequence. Each step is a check on the previous one. If you skip one, the name becomes myth."

That reflection is the most governance-correct output of the session. It is recorded here as the governing principle for this memo, for any future contract, and for any future claim that a named thing is also an authorized thing.

The doctrine does not self-apply. A memo about naming discipline does not become disciplined by naming itself. The discipline comes from the chain being run correctly, every time, even when the memo is about the chain.

---

**DRAFT — NO RATIFICATION — NO ACTIVATION — NO ACCEPTANCE CLAIM**

**This document is evidence of a naming failure, not authorization of any action.**

**End of ADR-LOOP-ACT-001**