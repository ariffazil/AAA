# Arrow-Wiring Recipe — Metabolize VAULT999 → Precedent + Evidence + KG

Execution companion to SKILL.md's "Prove-one-before-bulk" rule. After the audit
identifies broken arrows (`VAULT999=963 events`, `arifos_precedent=0`,
`arif_evidence=0`), this is how to actually wire ONE event through before automating.

## Step 0 — find an event with REAL substance, not template noise
Do NOT pick the first record. Filter.
- 251 `888_JUDGE_EXECUTION` records with identical metrics + clustered timestamps
  = benchmark/template noise, NOT distinct institutional decisions.
- The truly substantive record in the 963 was a `RESOLUTION` type carrying
  `root_cause`/`fix`/`scars`/`delta_s`/`f11_attestation` — that is the
  `Failure → Scar → Lesson → Skill` epitome worth turning into a precedent.
- Extract by searching whole file for a class with narrative fields, never by
  fixed index (file index ≠ scan index).

## CRITICAL GOTCHA — Qdrant collections have DIFFERENT vector dims
Probe per-collection config BEFORE writing; never assume one embedding size.
```python
for c in ("arif_evidence","arifos_precedent"):
    # GET /collections/{c} → result.config.params.vectors.size
```
Real baseline (2026-08-13): `arif_evidence` = **768**-dim, `arifos_precedent` = **1024**-dim,
both Cosine. Feeding one vector to both → the mismatched one returns **HTTP 400
Bad Request**, silently leaving that arrow at 0 while the other succeeds.
Fix: build a `make_vec(dim)` that hashes tokens into the target width.

## Qdrant upsert (PUT, wait=true)
```python
url=f"http://localhost:6333/collections/{coll}/points?wait=true"
body={"points":[{"id":pid,"vector":vec,"payload":payload}]}   # method=PUT
```
200 + `"status":"completed"` = written. Verify by re-reading `points_count`.

## FalkorDB relationship write (returncode 0 = ok)
```python
redis-cli -p 6380 GRAPH.QUERY arif_l5_knowledge \
  "CREATE (:Event {id:'evt_x',type:'RESOLUTION_SEAL'})"
redis-cli -p 6380 GRAPH.QUERY arif_l5_knowledge \
  "MATCH (e:Event {id:'evt_x'}) CREATE (e)-[:ROOT_CAUSED_BY]->(:Fact {...})"
redis-cli -p 6380 GRAPH.QUERY arif_l5_knowledge \
  "MATCH (e:Event {id:'evt_x'}) CREATE (e)-[:SEALED_BY]->(:Actor {name:'...'})"
```

## The institutional unit (schema family, shared + class-specific)
Shared: `id, event_class, intent, actor, ts, claim, decision, chain_proof`.
For a RESOLUTION: `root_cause, fix, scars[], delta_s, verified` are the payload's
signature fields — preserve them; they are the provenance that F2/F11 need.

## Prove retrievability, not just existence
0→1 points is necessary but NOT sufficient. Prove a judge can actually retrieve it:
search with a semantically-close query and show it returns the payload.
```python
# POST /collections/{coll}/points/search with {"vector":vec,"limit":1,"with_payload":true}
```
Expected ~0.5 cosine score for a hashed bag-of-tokens vector; the point is the
payload (id/claim/decision/scars/chain_proof) comes back whole and each field is
present — the record is traceable to actor+ts+chain(proof), not a dead row.

## Bulk-noise warning (why NOT to ingest 963 blindly)
If you bulk-ingest all 963, you print template-noise as precedent → "import sampah →
memory sampah → precedent sampah". Before any bulk run, TAG records by class
(substantive has root_cause/claim/query genuine vs template has uniform metrics).
Ingest substantive classes only. One-event proof is the gold-standard reference for
the automated path.

## POST_ZEN_OPERATION_AUDIT — verify the arrows are living
Measure LIVING ARROWS, not counts or storage growth. Output:
```
ALIVE           arrows proven retrievable+traceable
DEAD            arrows still disconnected
FALSE MEMORY    records that exist but are never queried
LEARNING SCORE  /5 based on evidence past action influences future judgment
VERDICT         more coherent, or just more records?
```
Real result (2026-08-13, event `oc-key-fix-20260812`): 3/3 write-arrows ALIVE,
retrieval PROVEN (score 0.51, payload whole), 3.5/5 learning score. The remaining
half-arrow `precedent → arif_judge automatic call` belongs to the kernel, not to a
storage function — wire it there.