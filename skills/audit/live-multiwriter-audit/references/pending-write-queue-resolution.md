# Resolving a Pending Write Queue

Trigger: a write-approval gate is set and records are staged on disk (for example
`<hermes-home>/pending/memory/<id>.json`), with a human applying them by id.

## Shape of a record

```json
{"id": "...", "subsystem": "memory", "action": "batch", "origin": "background_review",
 "payload": {"action": "batch", "target": "memory",
   "operations": [{"action": "replace|remove|add", "old_text": "...", "content": "..."}]}}
```

Read every payload **in full from disk**. The one-line `summary` is truncated and names only the
first operation, so a summary-based review misses most of the batch.

## Recipe

1. Snapshot the live store: split the file on its entry delimiter and hold the entry list in
   memory, with the total character count and the configured limit.
2. **Dry-run every op against the live list before applying anything.**
   - `add` → is the content already present?
   - `replace` / `remove` → does `old_text` match *exactly one* live entry?
   Zero matches means the batch was built against a stale snapshot and cannot apply as written;
   multiple matches means it is ambiguous and must be made specific.
3. **Decide per batch, never for the queue.** Batches staged at different times target the same
   entries with different replacement text. Applying the whole queue in order means the newest
   silently clobbers the rest — the earlier work is erased and the result looks clean.
4. **Move, do not delete.** Copy the record files into `pending/.../processed-<label>/` and write a
   receipt beside them naming the restore step (moving them back re-stages them as pending).
5. Record entry count and final character count before and after. That is the evidence the
   resolution did something.

## Rejection classes that recur

- **Fabricated fact** — an inferred value (a birth year derived from a stated age) asserted as
  fact. Keep `UNKNOWN` as `UNKNOWN`; do not manufacture precision the principal never gave.
- **Stale anchor** — `old_text` matching no live entry. This is diagnostic: it dates the payload
  against an old snapshot.
- **Third-party identifiers** — a real name, employer, or handle for someone other than the
  principal. An active memory file renders into every session, including shared rooms; route such
  facts to the vault and refer to the person generically in active layers.
- **Psychological modelling of a person** — diagnosis, attachment analysis, or motive claims about
  someone the principal knows. Standing doctrine forbids it: a model may hold a behaviour pattern,
  not a mind. The one defensible clause in such a batch is usually already covered by an existing
  conduct rule; check before adding.
- **Compression that drops a fact** — a tightened entry that loses the principal's own phrasing or
  a real deployed path is a loss, not a saving. Diff old against new field by field and restore
  anything that vanished.

## Gate state

Half-on is the only setting that accumulates: approval enabled with nothing draining the queue, or
approval disabled while writes are still being staged. Either enable it and consume it, or disable
staging entirely. Report which of the two you recommend and why.
