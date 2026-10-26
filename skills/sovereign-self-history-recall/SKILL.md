---
name: sovereign-self-history-recall
description: Use when he asks about his own past, period or town.
version: 1.0.0
tags: [memory, recall, biography, sovereign, gap-discipline]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Sovereign Self-History Recall

Trigger: he asks for his OWN life by period, place or institution — school years, a town, a posting,
a decade — as opposed to asking about a third person or about what an agent once said. The
deliverable is the record plus the shape of its absence. It is never a biography written to satisfy
the request.

Rule 0: a recorded line is one line deep. Expanding it into scene-by-scene detail is invention, not
recall. Depth here means naming the gap, not covering it.

## Sweep, in order (stop when the question is answered)

1. **Canon wiki.** `/root/AAA/wiki/ARIF_FAZIL_B.md` carries the period stratigraphy — one block per
   era, the fastest map. `/root/AAA/wiki/SCAR_TERRAIN.md` carries the scar prose behind it. Both are
   `SOVEREIGN_TESTIMONY` and their own FORGE note forbids summarizing, paraphrasing or interpreting
   them: quote the line, or state the fact it carries, and never rewrite them into a smoother arc.
2. **Live memory.** `~/.hermes/memories/USER.md` holds the standing identifiers (identity triple,
   family role, work) that anchor any period; it rarely holds period detail. `MEMORY.md` holds rules,
   not a life.
3. **Session DB.** `state.db` messages `LIKE '%<place>%'` often contains his own earlier answers
   about the same period — what has already been said, and what he already corrected.
   ```python
   import sqlite3
   con = sqlite3.connect("file:/root/.hermes/state.db?mode=ro", uri=True)
   con.row_factory = sqlite3.Row
   q = ("SELECT id,timestamp,role,content FROM messages WHERE content LIKE ? "
        "AND role IN ('user','assistant') ORDER BY timestamp LIMIT 80")
   for r in con.execute(q, ('%<place>%',)):
       print(r["id"], r["role"], (r["content"] or "")[:900])
   ```
   Query through Python, not `sqlite3 -json "<multi-line SQL>"` in a shell string — the quoting
   breaks on the newlines and returns a parse error that reads like an empty result.
4. **HUMAN corpus.** `/root/ariffazil/HUMAN/memory-graph-*/memory-graph.json` (people, places,
   events, relationships — name-walk it), plus the WhatsApp exports under
   `/root/ariffazil/HUMAN/{mak-abah,kawan}/*/*.txt`. Grep the place name AND sibling school names: a
   family thread about a younger sibling's placement often carries the only real chronology.
5. **Artifacts** — dossiers/PDFs built earlier. State their real date and size when quoting.

## Report shape

A few short paragraphs in his register — no tables, no headers, no jargon. One line per recorded
fact, each flagged as record; then the explicit gap list (the people, rooms, first week, canteen,
the small humiliations the record does not carry); then what the record cannot supply at all. Close
with one plain line, not a question.

When the follow-up is interpretive (how do you think I was then, macam mana aku masa tu), open by
naming it as a reading built from the scar shape, not memory, and keep inference visibly separate
from record in every sentence after that.

## Pitfalls

- **Canon files can contradict each other about his own biography.** Two files can place the same
  phase in different towns, or give different years for the same transition. Name both, say which
  file says what, and do not merge them into one rounder story or silently pick the likelier. He
  settles it when he wants to. A harmonised biography is the one failure he cannot detect from the
  outside.
- **Do not answer tell-me-everything with a summary of the testimony.** The testimony is stored
  verbatim on purpose. The answer is what the record holds, in his register.
- **A family chat export is not a chronology of feeling.** Transit messages and forwarded
  school-placement threads give dates and places; label them as evidence of an event, not of an
  experience.
- **Period arithmetic is inference.** Working out a form or year from a birth year and a university
  start is fine, but say it is arithmetic — never present a derived timeline as a remembered one.
- **Media pasted alongside the question is new evidence, not decoration.** When the paste is a video
  or photo of the period, read it (frames plus ASR; see `media-ingest-lane` for the pipeline) and say
  plainly that it is not in the record — that is the one layer the sweep cannot supply.
- **Unnamed people stay unnamed.** Friends, teachers and dorm-mates exist in the record only as
  types unless he names them; inventing a name so a scene lands is the same failure as inventing
  the event.

## Related

The generic store catalogue (person-recall, self-recall, pending-queue adjudication) lives in
`local-memory-retrieval`, which is externally owned and read-only to curation. This skill adds only
the sovereign's own-history case, where the record is thin and the gap is the deliverable.
