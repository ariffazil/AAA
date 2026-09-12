title: Hermes A2H HOLD Capsule Spec v0 — Pure Presenter Contract
mode: read-only design / spec only
mutation: NONE performed
date: 2026-09-12 (Asia/Kuala_Lumpur)
authority: ARIF FAZIL (F13)

# 0. Status

This document specifies the **Hermes-side** of a federation
transaction in which a 888 HOLD ticket is rendered into a human
decision surface. It performs no mutation, no Telegram send, no
TTS synthesis, no capability provisioning.

What it produces today is a **pure skill/prompt rendering** that:
1. Receives a HoldTicket JSON (minted by AAA / arifOS),
2. Emits a BM-EN decision card for Arif,
3. Captures Arif's typed decision,
4. Submits it via `arif_route` to `arif_judge` (so AAA validates the
   payload hash + actor identity before any execution).

The arbitration and execution surfaces live in arifOS / AAA / A-FORGE
and are explicitly NOT re-implemented here.

# 1. Where this lives

Hermes owns it. Because Hermes is A2H (per
`/root/AAA/registry/capabilities.yaml`), this is a permitted place:
NO mutation authority, NO privileged credentials, NO outbound
delivery. Only format transformation + explicit human decision
capture + decision submission over the existing `arif_route`
boundary.

# 2. Inputs

## 2.1 HoldTicket

Source of truth: `AAA.get_hold` or the equivalent `arif_route` /
`arif_judge` response when called with the HOLD intent.

Required fields (all must be present before rendering; absence ⇒
HOLD = UNKNOWN):

| Field | Type | Description |
|---|---|---|
| `ticket_id` | ULID | unique per attempt |
| `trace_id` | ULID | ties to federation event spine |
| `capability_id` | string | e.g. `federation.test.echo`, or capability providing desired effect |
| `owner` | enum | "arifOS" | "AAA" | "A-FORGE" |
| `executor` | enum | "A-FORGE" | registered-actuator |
| `action_summary` | string | human-readable 1-line |
| `resolved_target` | object | the binding target descriptor |
| `canonical_parameters` | object | signed canonical params |
| `risk_class` | enum | read / reversible_write / irreversible_write / critical |
| `impact_summary` | string | human-readable consequence |
| `rollback_summary` | string? | null if none |
| `evidence_refs` | array | FRAME / organ receipts |
| `policy_version` | string | e.g. `AAA.888.v1` |
| `payload_hash` | string | `sha256:` prefixed |
| `issued_at` | ISO-8601 | when ticket minted |
| `expires_at` | ISO-8601 | when ticket becomes VOID |
| `actor_identity_requirement` | string | e.g. `arif_arifos_user_id#267378578` |
| `allowed_decision_set` | enum array | `["approve","deny","request_clarification"]` |
| `nonce` | string | replay protection |
| `signature` | string | AAA signed |

## 2.2 User input

Arif's typed/voice reply against this ticket.

# 3. Outputs

## 3.1 HoldCard (rendered to human)

Format: plain text message, BM-EN code-mixed per Arif's preference.
NEVER use yes/no or generic "Proceed?" language.

```text
⚠️ 888 HOLD — Your confirmation required

Ticket: <ticket_id>
Trace:  <trace_id>
Policy: <policy_version>
Expires: <expires_at>

— Requested outcome
<action_summary>

— Resolved target
<key=value list from resolved_target>

— Why the federation paused
<risk_class> action. <impact_summary short rationale>.

— Evidence before action
[<label>] <text>  — <reference/observed_at>

— Expected consequence
<impact_summary>

— Rollback if available
<rollback_summary> (omit section if null)

— Your choices
[Approve exact action]
[Deny]
[Ask a question]
[Show raw evidence]

— Submission binding
payload_hash = <payload_hash>
executor      = <executor>
owner         = <owner>
```

## 3.2 HumanDecision

Only emitted after Arif selects one of the options.

| Field | Type | Description |
|---|---|---|
| `ticket_id` | ULID | must match ticket |
| `actor` | "ARIF" | fixed |
| `decision` | enum | approve | deny | request_clarification |
| `approved_payload_hash` | string | exact value from `payload_hash` |
| `presented_at` | ISO-8601 | when card rendered |
| `decided_at` | ISO-8601 | when human replied |
| `human_note` | string? | optional |

No `command`, no `parameter overrides`, no `target edits` — those
fields must be exactly equal to ticket. If Arif asks to alter any
field, do NOT submit a HumanDecision; reply with a new HOLD because
payload hash will fail.

## 3.3 Outbound wire

`arif_route` with arguments:
- `intent`: `submit human decision on ticket <ticket_id>`
- `organ`: `arifOS`
- `organ_tool`: `arif_judge`
- `arguments` containing the HumanDecision, optionally `payload_hash`
- `actor_id`: arif
- `session_token`: arif's SCT (must be live; otherwise refuse to
  render at all — see §4.4)

# 4. Failure modes and rejection rules

## 4.1 Unknown payload_hash → REFUSE

If the ticket's payload_hash is empty or malformed, refuse to render:
emit `UNKNOWN: HOLD ticket missing payload_hash, refuse to render`
and request clarification.

## 4.2 Expired → REFUSE

If `now >= expires_at`, refuse to render. Emit `UNKNOWN: HOLD ticket
expired at <expires_at>`. Do NOT honour any decision because AAA
will reject anyway.

## 4.3 Identity mismatch → REFUSE

If `actor_identity_requirement` does not match the active session's
actor, refuse to render. Do not impersonate.

## 4.4 No SCT bound → REFUSE

If the live session is not bound to arifOS with a valid SCT, render
becomes moot because AAA will reject the decision anyway. Emit
`UNKNOWN: not bound to governed session; cannot submit HOLD decisions`.

## 4.5 Unsigned ticket → REFUSE

If `signature` is missing or empty, refuse. Emit `UNKNOWN: ticket
unsigned; arifOS policy requires AAA signature on HOLD`.

## 4.6 Payload-altered-in-human-reply → REFUSE & NEW HOLD

If Arif's reply implies a target / parameter / recipient change, do
NOT submit a HumanDecision. Emit a new HOLD card showing the
requested change and asking for a fresh approval through AAA — not
by us. Concretely: "The action you describe differs from the bound
ticket. Do not approve this card. The original HOLD expires at
<expires_at>. Ask the federation to issue a corrected ticket."

## 4.7 Decision set violated → REFUSE

If `decision` ∉ `allowed_decision_set`, refuse and emit
`UNKNOWN: decision set violation`.

# 5. State representation inside Hermes

This spec is a pure presenter. Hermes MUST NOT persist a
`hold_approved` flag in a way that implies authority. If human
memory persistence is desired it must be stored as:

```json
{
  "kind": "human_observation",
  "ticket_id": "...",
  "decision": "approve",
  "submitted_at": "...",
  "outcome": "submitted_for_judgement",
  "note": "do not infer execution; awaiting AAA verdict"
}
```

NOT as:
- "action approved by Arif"
- "execute at <target>"
- any state that would let the next session continue as if the
  external action had been authorized.

# 6. Test acceptance (what success looks like for this spec)

A reader of this spec should be able to confirm the following
without running anything:

1. The HOLD card content above can be hand-rendered from a sample
   ticket JSON and the same content appears in the rendered output.
2. The HumanDecision only ever references fields present in the
   ticket.
3. If a payload field is altered, the spec mandates a new HOLD, not
   a re-submission.
4. If the session is unbound, the spec mandates REFUSE.
5. No outbound voice/Telegram/SMTP/etc is mentioned or implied.
6. The only outbound wire is `arif_route(intent=submit human
   decision, organ_tool=arif_judge)`.

# 7. Where this spec does NOT cover

- AAA HOLD minting logic (owner's job).
- A-FORGE execution flow (owner's job).
- Multi-modal actuator selection (Hermes may RECOMMEND a modality
  preference, but rendering does not commit it).
- Telegram delivery of voice (A-FORGE actuator only).
- Long-term commitment table; this spec does not bind to "open
  loops" / "approval tokens". Those require AAA policy minting
  durable holds, which is the owner's job, not Hermes'.

# 8. Counterfactuals I owe

(Per F2: name one condition the spec would fail under.)

If AAA's ticket format changes (rename `payload_hash` → `binding_hash`,
or `executor` becomes a tool name not an organ, or evidence references
become opaque IDs without an accessible resolver), this renderer
becomes inert. Mitigations:
- prefer public resource URI `arifos://hold/schema/v1` if/when AAA
  publishes a JSON-Schema for HoldTicket
- request rerendering after schema updates via `arif_observe`

# 9. What is left out of spec, and why

- "Carry forward of HOLD across restart" — that requires durable
  storage binding in AAA/arifOS, not this A2H presenter.
- "Voice delivery of the HOLD card" — that is actuator work, not
  presenter work. The presenter renders text. Asking the presenter
  to speak it would cross the execution boundary.
- "Multi-card render (split across messages)" — out of scope for v0;
  one ticket = one card.

-- 999 SEAL ALIVE · DITEMPA BUKAN DIBERI
