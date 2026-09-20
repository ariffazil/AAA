# Pending-Queue Adjudication — turning a staged-memory queue into applied memory

Load when a background review has staged memory writes and somebody has to decide what lands.
The queue is not a to-do list to apply; it is a set of *proposals from an unsupervised writer*,
and the reason approval exists is that some of them are wrong, some duplicate each other, and
some quietly delete facts while claiming to consolidate them.

## Why the queue is inert, and why inert is not safe

The write gate is a config switch (`memory.write_approval`). With it **off**, proposals still
stage; they simply never apply. That produces a queue that is harmless this week and dangerous
later, because it is still readable and it looks like approved-but-unsent work. A later session
that finds it will "just apply it". Adjudicate it or clear it — do not leave it standing.

```python
import sys; sys.path.insert(0, "/usr/local/lib/hermes-agent")
from tools import write_approval as wa
wa.write_approval_enabled(wa.MEMORY)   # is the gate live?
wa.list_pending(wa.MEMORY)             # the queue
wa.discard_pending(wa.MEMORY, pid)     # the ONLY correct way to clear one
```

Never delete a pending file by hand. The API is what keeps the queue and its bookkeeping
consistent; the files are the implementation.

Each record carries `id`, `created_at`, `origin`, `summary`, and a `payload` holding
`target` + `operations[]`, where each op is `{action, old_text, new_text|content}`.

## The stages, in order

### 0. Triage — measure the queue against the store it would land in, BEFORE adjudicating

Do this first, because it can end the job. Item-by-item adjudication of a structurally inadmissible
queue is wasted work, and the finding is the *accumulation mechanism*, not the individual proposals.

**Volume against the ceiling.** Sum the proposed text and compare it to the store's hard limit. A
queue whose proposed text is a multiple of the entire live store cannot be applied as a batch under
any ordering of its items — the store improves by **replacement**, never by addition, so most of it
is re-statement. Measured: proposed **63,738** chars against a live store of **3,519** (with a
2,200-char cap on the larger file) — **18x the store**, at which point the per-proposal verdict is
the wrong instrument.

**Does the loader actually forget?** Check how the consumer discovers records before trusting any
prior cleanup. A recursive glob (`rglob("*.json")`) reads every subdirectory, so moving records into
a `processed-<date>/` archive hides them from a human listing while changing nothing the consumer
sees. Measured: four such archive directories, and the loader counted all of them — cleanups had
already been attempted several times and the queue came back unchanged. That is the signature: not
stubborn proposals, an unchanged population.

```bash
find <queue-dir> -name '*.json' | wc -l                # what a recursive loader sees
find <queue-dir> -maxdepth 1 -name '*.json' | wc -l    # what a human listing shows
```

**Does any record carry a terminal state?** If every record's status is absent (all `None`), nothing
anywhere records applied / rejected / superseded. The queue then has no floor: a decided proposal is
indistinguishable from a fresh one, so it regenerates indefinitely and the same work is
re-adjudicated every generation. A verdict vocabulary is for the *adjudicator*; the *data* needs the
terminal states too, or the queue is unbounded by construction.

**Count anchors, not records, when reporting size.** An anchor re-queued with competing text N times
is not N independent proposals — the newest supersedes the rest. Measured: **147 distinct anchors
across 173 records, 57 queued more than once, one anchor carrying seven competing versions in three
days.** That is the queue's own dedupe failure, and it is why the byte count overstates the content.

### 1. Measure entity overlap against prior archives

The queue is frequently a **re-generation** of one already adjudicated and archived. Test it —
but test on the right unit.

Phrase shingles under-report badly, because the second generation rewrites the wording.
Entity shingles — quoted strings, numbers with units, handles, ALLCAPS tokens, ids — survive
rewording and catch it:

```python
ENT = re.compile(r'"[^"]{6,60}"|\'[^\']{6,60}\'|[A-Za-z_][A-Za-z0-9_]{2,}@[A-Za-z0-9_]+'
                 r'|[0-9][0-9.,]{2,}(?:tok|k|B|%|boepd|mmboe)?|-[0-9]{9,}|[A-Z]{4,}')
```

Measured on one queue: phrase shingles reported **1 of 14** ops as already-archived; entity
shingles reported **11 of 14**. Same data, opposite conclusion. A wording-sensitive test on a
re-worded artifact is a test that cannot fire.

### 2. Group by `old_text` to find collisions

Two proposals replacing the **same** `old_text` with **different** `new_text` cannot both apply —
the second silently overwrites the first, and nothing errors. Group the ops, and when a group has
more than one claimant, adjudicate them *together*; the surviving text has to carry whatever the
loser got right.

### 3. Grep every `old_text` against the live file

A `replace` whose target does not exist is not a style problem — it means the entry was already
removed, and the proposal is a rework of a generation that was already rejected. Grep it:

```bash
grep -c 'AUDIT INSIGHT' ~/.hermes/memories/MEMORY.md    # 0 => target absent
```

Report it as `TARGET ABSENT` and name where the text actually lives (the archive ledger), rather
than applying a replace that no-ops or, worse, appends.

### 4. Diff each proposal against the entry it claims to replace, and list the LOSSES

This is the stage that earns the whole procedure. A proposal that says "compress" routinely
deletes named humans, live decision states, and precedent pointers — the same defect class as a
merge that loses its source.

For every `replace`: take the entities present in the **current** entry and absent from the
**proposed** entry. That difference is the loss list. Then decide, per entity, keep or drop —
never accept the proposal's own framing of itself.

Measured: a proposal adding a genuine new constraint also dropped a named person's remark and a
live decision state; another dropped a precedent file path and a claim-state qualifier. Both
called themselves consolidations.

### 5. Budget before writing — draft, measure, trim, repeat

Never write and then discover the ceiling. Build the full target text in a scratch script, count
it, and compare to the limit:

```python
SEP = 3   # the separator between entries
size = sum(len(v) for v in TARGET.values()) + SEP * (len(TARGET) - 1)
print("FITS" if size <= LIMIT else "OVERFLOWS by %d" % (size - LIMIT))
```

A store near its ceiling cannot be improved by **addition**, only by **replacement**. Each
accepted fact must be paid for by compressing an entry that already exists. Three measured
passes: **+683 → +190 → +107**, fitting only after the third.

An overflow is not a formatting problem to squeeze. It is the arithmetic telling you the queue's
real content is smaller than its byte count, and that most of it is re-statement.

### 6. Rank by blast radius, not by salience

For each candidate: *what goes wrong in a future session if this fact is absent?* Rank that, not
how interesting the fact is.

- **In:** constraints on the user's own livelihood, a mechanism that prevents a wrong action,
  a claim-state qualifier that prevents an unverified number being repeated as fact, a correction
  the user made twice.
- **Out:** identity garnish about a third party, ids and paths already discoverable in live
  config, procedure that a skill already owns, anything already homed in two other places.

### 7. Archive verbatim BEFORE discarding

The standing rule: a failed gate means compress to a ledger, never delete. Write one ledger
carrying:

```json
{"generated": "<iso>", "why": "<the standing rule being applied>",
 "measured": {"before": 0, "limit": 0, "target_after": 0, "draft_overflows": []},
 "collisions": [{"old_text": "", "claimants": [], "note": ""}],
 "verdicts": {"<pid>": {"verdict": "", "reason": ""}},
 "proposals": [{"id": "", "payload_verbatim": {}, "verdict": ""}]}
```

Then discard each id through the API. Verify `pending after: 0` — do not infer it.

### 8. Witness — read back and grep every fact the adjudication claims to have kept

**The adjudication is a claim about an artifact that did not exist when you wrote it.** Write its
preservation claims from a read-back, not from intent.

```bash
for s in '<fact 1>' '<fact 2>' '<dropped thing>'; do
  printf '%-30s %s\n' "$s" "$(grep -c "$s" ~/.hermes/memories/MEMORY.md)"
done
grep -c '<anything you rejected>' ~/.hermes/memories/MEMORY.md   # must be 0
```

Measured: the first write-back showed **two** preservation claims were false — the text asserted
"both kept" for content that was not in the applied entry. One was repairable within budget; one
was not. The unrepairable one was **named in the ledger as deliberately unapplied**, not left
silent. Repair what fits; name what does not.

## Verdict vocabulary

Use a closed set so a later reader can audit the decisions without re-reading the payloads:

| Verdict | Means |
|---|---|
| `ACCEPT` | lands as proposed |
| `COMPRESS` | lands, shortened |
| `MERGE` | lands combined with an existing entry; losses listed |
| `ACCEPT_WITH_LOSS_REPAIRED` | the proposal dropped content it claimed to keep; restored before landing |
| `PARTIAL` | some ops land, some do not; name which |
| `TARGET_ABSENT` | the `old_text` is not in the live store |
| `COLLIDES` | shares a target with another pending; adjudicated together |
| `REJECT_FALSIFIED` | the fact is wrong against evidence obtained in the same session |

## Pitfalls

- **Never adopt a fact the same session falsified.** If a proposal prescribes a mechanism that was
disproved by reading the code an hour earlier, applying it re-injects a superstition and directly
contradicts the skill that was just corrected. Reject it, and record *why* in the ledger so the
rejection survives the next generation of the same proposal.
- **A queue with two wordings of one idea is one proposal, not two.** Duplicate re-work inflates
the queue and makes it look like more evidence than it is.
- **Third-party detail is bounded by the relationship kernel.** Curation of memory about a person
the user cares about is not licence to accumulate a profile: gym, dietary and competition detail
is identity garnish, not decision-relevant, and building it is the dossier behaviour the kernel
forbids. When budget forces a cut, that is the correct thing to cut — and say so.
- **The queue's own summary lines are not evidence.** Each summary restates the proposal's
intent. Read the payload.
- **Report the trade, not just the result.** "Applied 9 operations" hides that two facts were
dropped to fit. State what left and why, in the reply.
- **An inert gate does not postpone the decision.** Clearing the queue while the gate is off is
  correct precisely because the gate being off is what makes it dangerous later.
- **Re-probe every live-state claim in the queue before adjudicating it.** An unsupervised writer
  carries assertions about running systems, and those move under it: measured, a proposal asserted a
  subsystem was broken (`CALIBRATION BROKEN, 0 verified, accuracy 0.0`) while a live probe in the
  same session read `2 verified, accuracy 0.5`. Grep the payloads for state claims and probe each
  one. A stale claim that reaches live memory installs a retracted fact permanently — and the check
  is cheap, because the probe is one call.
- **A queue larger than the store's capacity cannot be adjudicated item-by-item.** See stage 0:
  report the mechanism and the triage numbers instead. "N of M proposals re-state content the store
  already carries" is the honest summary of a queue that is many times the store.
- **The queue's content is not its byte count.** Volume at this scale is mostly the same sentences
  rewritten; measure distinct anchors and distinct entities before describing the queue as "a large
  amount of new information".
