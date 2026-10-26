---
name: session-corpus-abstraction
description: "Use when deriving doctrine from chat session logs."
version: 1.0.0
risk_tier: low
floor_scope: [F1, F2, F6, F9]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
owned_by: curator
authority_of: AAA
---

# Session Corpus Abstraction

For the order *"do abstraction / generalisation on this chat logs session"* — the deliverable is a
doctrine, not a summary. The failure mode is a doctrine whose sections were remembered rather than
measured: it quotes themes the agent found vivid in its own context window instead of themes the
principal actually spent his turns on.

**Rule one: the shape of the abstraction is decided by a count, not by the last five messages.**

## Procedure

### 1. Measure the lane read-only, before drafting

Never write the doctrine first and look for support afterwards. Open the live session store read-only
(`file:/root/.hermes/state.db?mode=ro`, `uri=True`) and take five numbers:

- sessions in the window and their `message_count` sum;
- user turns only (`role='user'`) — assistant and tool rows inflate the count and belong to the agent,
  not to the principal;
- total characters of those user turns (a doctrine's depth is bounded by how much he actually wrote);
- a keyword bucket count per theme (regex per bucket over lower-cased bodies);
- short-message ratio (`len(strip) <= 40`) — the share spent steering rather than writing.

Schema anchors: `sessions(chat_id, started_at float epoch, message_count)` and
`messages(session_id, role, content)`. Filter by **`chat_id`**, never by a single `session_id` — one
lane spans many session resets, and a single-session sample produces a confident wrong shape.

Print the denominator with every figure. A share without a denominator is not a measurement.

### 2. Dedupe before quoting any bucket

Live stores re-quote earlier turns, tool output and quoted blocks, so a raw regex count over them is
inflated and manufactures themes that were never spoken. Collapse identical bodies per session and
report both figures (`raw 641 → 604 deduped`). If the difference exceeds a few percent, the buckets
are contaminated and must be re-run, not footnoted.

### 3. Let the distribution choose the sections

A bucket carrying a third of his turns is a chapter. Under one tenth is a paragraph. Under five
percent is a sentence — and if it cannot be placed, cut it rather than decorate the doctrine with it.
This is what stops the artifact from being the agent's own interests with his name on top.

### 4. Name the single question underneath the themes

Counts show *what* he kept returning to; the doctrine needs *why that set*. Look for the question that
generates all the buckets at once — the one whose removal would make the other topics incoherent. If
no such question exists, say the corpus is plural and deliver the distribution honestly instead of
forcing a thesis.

That single question is the abstraction. Everything else in the document is its unpacking.

### 5. State what the corpus cannot answer, in the document

A corpus reaches enacted behaviour, vocabulary, timing, volume and silence gaps. It does not reach
motive, interior or shared meaning. Put that limit in the artifact, not only in the chat reply — the
artifact is what survives.

### 6. Ship it in his delivery format

Reading material goes as a **PDF in chat** (Typst), not a `/tmp` path and not a wall of prose in the
message. Chat reply: the abstraction, three or four load-bearing findings, then the file. Verify the
PDF (`pdftotext` head and tail; rasterize page 1 and check layout) before emitting `MEDIA:`.

## Pitfalls

| Pitfall | Rule |
|---|---|
| Recency bias dressed as synthesis | The last session is not the corpus; bucket-count every theme in the window |
| Counting assistant/tool rows | Filter `role='user'`; the agent's own output is not his testimony |
| One session id sampled | Sweep the lane by `chat_id`; resets fragment one conversation into dozens of rows |
| Raw regex counts | Re-quoted text inflates buckets; dedupe per session and print the funnel |
| A share with no denominator | Never say "most of his time"; say "218 of 641 user turns" |
| Doctrine built to a thesis he did not state | If the buckets do not converge, deliver a plural distribution and say so |
| Motive smuggled in as finding | The corpus shows behaviour, not interior; keep the two tiers apart in the artifact |
| Doctrine delivered as chat prose | PDF artifact for reading, short chat summary, no `/tmp` paths |

## Relationship to other skills

- `corpus-claim-discipline` owns **claims about a person** drawn from a corpus (dedupe funnel,
  attribution, tiers, base rate). Load it whenever the abstraction makes a statement about a named
  human rather than about the principal's own themes.
- `doctrine-forging` owns the dialogue register once the abstraction becomes doctrine.
- `governed-uncertainty` owns the boundary between what the corpus can carry and what stays human-private.
