---
name: federation-ledger-ingest
description: "Use when filing a durable event in the federation ledger."
version: 1.0.0
author: Hermes
license: F13-Sovereign
tags: [ledger, receipts, provenance, arifflow, memory, witness, consequence]
capability_tier: fed-long-context
ecology_state: WARM
---

# Federation Ledger Ingest

Filing a durable event: something happened in the world that a later session must be able to prove —
an email sent, a form submitted, a decision taken, an instruction given, an artifact produced and
handed over. The job is a two-part receipt: a durable, hashed artifact on disk, and a governed entry
in the federation's consequence ledger.

Companion skills: what a document should *say* belongs to the submission/drafting skills; rendering
belongs to `forge-pdf-delivery`; the human-facts register (`people.yaml`) takes person facts under its
own admission rules, not this procedure.

## Trigger

- "Store this as reality", "record this", "file this", "keep this on the record".
- The user hands over an artifact, message, form submission, or decision and expects it to survive the
  session.
- Any event whose value is that it can be **re-verified later** rather than re-remembered.

## Procedure

### 1. Durable artifact first — the ledger entry is not the storage

Write the verbatim source to a stable path outside any cache, with a provenance header carrying:
`record_type`, `source`, `channel_in`, `what`, `when`, `classification`, `content_handling` (verbatim
vs excerpted), and an `integrity` line naming the hash of the verbatim block. The header is metadata;
the block beneath it is the evidence.

Hash the **verbatim block**, not the whole file. A whole-file hash breaks the moment anyone corrects a
typo in the header, and the point of the hash is that the *evidence* is unchanged.

Write a `manifest.json` in the working directory carrying the artifact paths, the hashes, the byte
size, the recipient and message id of any delivery, and the ledger receipt id. One file that answers
"what was sent, to whom, when, and what was its hash" without re-deriving anything.

### 2. Mint the ledger receipt — parenthood is mandatory

The daemon **rejects a top-level step** with `PARENT_REQUIRED: pass parent_receipt_ids OR set
top_level_intent=true with reason`.

**The MCP tool schema does not expose `top_level_intent`.** Its parameter list is closed
(`additionalProperties: false`), so passing that key fails argument validation *before the call reaches
the daemon* — the call is never invoked, and it looks like a schema problem when the real requirement
is causality. Do not respond by adding fields.

Parent the receipt instead. The parent-edge store is `/root/.local/share/arifflow/edges/`, holding
small files named `<receipt-id>.last` — `session-<timestamp>.last`, `<actor>-<date>-<slug>.last` — each
containing:

```
<receipt_uuid> <jcs_body_hash>
```

Read the newest relevant one and pass **both halves**:

- `parent_receipt_ids: ["<receipt_uuid>"]`
- `parent_receipt_hashes: ["<jcs_body_hash>"]`

The daemon recomputes the parent's content hash and rejects a mismatch. That check is the
tamper-evidence — it binds the edge to the parent's *content*, not merely to its id, so a guess or a
stale hash fails rather than silently inventing a causality that never existed.

### 3. Fill the step fields honestly

| Field | What belongs there |
|---|---|
| `actor_id` | who performed the step, in the federation's own naming |
| `session_id` | a stable string identifying the chain this belongs to — reuse it for every step of the same event so the chain is readable |
| `step_type` | `Execute` for an act, `Verify` for a check, `Seal` for a closure |
| `epistemic_label` | `Observation` for something witnessed in the world, `Derivation` for something computed |
| `floor_verdict` | `Pass` when nothing is being hidden or exceeded |
| `payload` | the substance: what happened, the paths, the hashes, the stated intent, and the unwitnessed list |
| `witness_organs` | which organs can attest to this step |

Set `jcs_body_hash` only if you are content for it to be ignored — the daemon recomputes and stamps it
server-side and never trusts a client value. Do not compute it yourself.

### 4. Validate the response, then record the receipt

Success returns HTTP 200 with `receipt_id`, `jcs_body_hash`, `status: ingested`. Put `receipt_id` and
`jcs_body_hash` into the manifest alongside the parent you passed. HTTP 400 is the daemon speaking
plainly — read the `error` and `remediation` keys rather than retrying the same call.

## The honest-record law — what makes an entry worth having

1. **Mark every unwitnessed field explicitly, in the record itself.** When the agent did not observe
the act — a form the user submitted alone, a radio value selected, a dropdown pick, the final text
after a third party edited it — the entry says so and names the read-back path that would settle it.
   A record that silently omits the gap is worth less than no record, because it will be trusted.
2. **A user's word is evidence of the claim, not of the fact.** "I sent it" is `REPORTED`; the
   platform's own confirmation or response page is the verification. File the claim as reported and
   point at where it becomes verified.
3. **Record the obligation the event creates.** An event that asks something of someone — a
   conversation requested within a stated window, a reply promised by a date — becomes a due date. A
   future session reads the ledger to know what falls due, and when silence itself becomes the answer.
4. **Supersede; never edit in place.** When a value in an existing entry is later corrected, file the
   correction as a new receipt parented to the old one and mark the old value superseded. The ledger's
   value is that it cannot be quietly rewritten.
5. **Chain the steps of one event in order.** An artifact and its later submission are two steps of
   one causal chain, not two unrelated facts — parent the second to the first so the ledger reads as
   cause, not coincidence.

## Pitfalls

- **Don't satisfy a rejected call by adding parameters.** The wrapper validates the argument set before
  dispatch; extra keys are rejected, not forwarded. When the detail you need is absent from the schema,
  the working route is the one the daemon's own error names — here, parenthood.
- **Don't invent a parent hash.** It must be read from the edge store; the daemon's recompute is
  designed precisely to catch a plausible-looking fabrication.
- **Don't hash the manifest.** Hash the evidence block; the manifest is derived and will legitimately
  change as versions are added.
- **Don't collapse a chain of events into one entry.** Two moments with different witnesses and
  different certainty are two entries with an edge between them.
- **Don't treat a ledger entry as the storage.** If the durable artifact is missing, the receipt proves
  that something happened while leaving nothing to inspect — file the artifact first.
- **Retire the churn.** A file per event is expected; a ledger entry per *revision* of the same event
  is not. File the state that was decided, not every draft that preceded it.
