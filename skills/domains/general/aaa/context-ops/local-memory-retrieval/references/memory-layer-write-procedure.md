# Memory Layer Write Procedure — recording what a session learned

Load when a session's output must survive it: a finding, a decision, a scar, or an open loop that a
later session has to inherit. The read side (where facts live, how to report them) is the parent
skill; this file is the *write* side.

Write the layer that owns the fact. Do not route everything through one store.

## 1. carry-forward — always first, the only layer with a sanctioned writer

```bash
python3 /root/scripts/carry_forward.py append --agent hermes --kind decision   --content "..." [--tags a,b]
python3 /root/scripts/carry_forward.py append --agent hermes --kind open_loop  --content "..."
python3 /root/scripts/carry_forward.py append --agent hermes --kind scar       --content "..."
python3 /root/scripts/carry_forward.py anchor --name "session/close" --agent hermes --state '{...}'
python3 /root/scripts/carry_forward.py show
```

- Kinds: `decision`, `scar`, `open_loop`, `eureka`, `directive`, `event`. Decisions, scars, eurekas
  and directives are permanent; events auto-prune after 7 days. Anything you want a later session
  to act on is an `open_loop`, not an `event`.
- **Never hand-edit the JSON.** The script holds the flock that keeps the two-writer race dead. It
  takes backups on every mutation, so a bad write is recoverable but a lost race is not obvious.
- Close the session with an `anchor`, carrying the artifacts produced, the open loops handed
  forward, and any skill you patched. The anchor is what the next session reads first.

## 2. eureka canon — stage it, because the ledger is sealed

```
/root/AAA/eurekas/<EUREKA-ID>.md      # header status: STAGED — PENDING CANON PROMOTION
```

The canon ledger carries a filesystem-level immutable attribute, as does most of the canon tree.
Do **not** attempt to clear it: a constitutional gate blocks the command, and the lock is not yours
to lift. Promotion runs through the kernel seal lane with sovereign authority.

Stage an individual `.md` carrying: the claim, its status header, the canon SOT path it targets,
the blocker, the audit provenance (what was verified, against what), and the open loops. Report
"staged, pending promotion" — never "sealed".

A sibling `eureka-entries.jsonl` inside the staging directory is frequently a **stray duplicate**
whose own README says append nothing. Honour that; stage files, do not append to it.

## 3. Vector store — embed, then upsert

```
POST http://<embed-host>:11434/api/embed   {"model":"bge-m3","input":text}  → 1024-d vector
PUT  http://<qdrant>:6333/collections/<col>/points?wait=true  {"points":[{id,vector,payload}]}
```

- **The upsert verb is `PUT`.** `POST .../points` is retrieve-by-id and answers a bad payload with
  "missing field `ids`" — which reads like a schema fault and is actually the wrong endpoint.
- Chunk by *claim class*, roughly 300–3000 chars: one chunk per distinct finding, not one chunk per
  document. Carry `category`, `source`, `epoch`, `organ` in the payload so the point stays
  attributable on retrieval — an unattributed vector is unusable as evidence later.
- Read the collection's current max id before upserting so you extend it rather than collide.
- **Never leave a probe point in a canon collection.** If a test vector was inserted to debug the
  upsert, delete it in the same session and re-count. A canon collection accumulating debug rows is
  contamination the agent authored.
- If the local embed host is not serving the model, check the federation before declaring the
  vector lane down: another node usually serves it. That is the general shape — probe for the
  capability before writing off the lane.

## 4. Reality graph — one edge per step, chained

```python
rec = {"receipt_id":  str(uuid.uuid4()),        # MUST be a UUID — a readable prefix is rejected
       "created_at":  utc(), "actor_id": "hermes", "session_id": SID,
       "step_type":   STEP,                     # closed enum, see below
       "step_number": 0, "cost_ns": 0, "epistemic_label": "Observation",
       "floor_verdict": "Pass", "cooling_decision": "None",
       "summary": summary, "routed_organ": "AAA", "entry_kind": "session"}
if parents:
    rec["parent_receipt_ids"] = parents[-1:]    # chain depth-first; do not fan out flat
POST http://127.0.0.1:7073/ingest
```

- **`step_type` is a closed enum:** `Execute`, `Verify`, `Cool`, `Seal`, `Barrier`, `Merge`,
  `Route`, `Abort`. An unknown value 400s *and returns the full variant list* — read it instead of
  guessing. Map intent on: analysis steps are `Execute`, audits `Verify`, consolidation `Merge`,
  decisions `Route`.
- Persist `{receipt_id} {jcs_body_hash}` to `/root/.local/share/arifflow/edges/<receipt_id>.last`,
  and read the previous `.last` to continue the chain when a call has to be retried.
- Retry a single failed step by reading the most recent `.last` for the parent id rather than
  re-running the whole chain — re-running duplicates edges that already landed.

## 5. Report the layers that did not write

A layer that refused connections, an organ reporting zero registered sources, a store with a char
budget already at its ceiling — all of these are part of the report. "Written" unqualified means
every layer you attempted succeeded. Name the ones that did not and why.

## The flow meter reports on you

After a chain is ingested, the service exposes a per-actor flow quotient over
`GET /health` — execute/verify counts, a ratio, and a verdict. A chain that is
**execution-dominated comes back throttled or `STUCK` even though every write succeeded.**

That is the meter describing the agent's own balance, and it is the same audit signal the
principal applies to the agent's numbers. Surface it as a finding about the session's work rather
than ignoring it: the honest close is "here is what I wrote, and here is what the meter says about
how I wrote it." An agent that logs eleven steps and verifies none of them has produced a record,
not a witness.
