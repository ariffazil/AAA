---
name: political-intelligence-briefing
description: Use when asked for a political intelligence read.
tags: [politics, intelligence, briefing, research, provenance]
triggers:
  - "wow me"
  - "political intelligence"
  - "what's brewing"
  - "catch me up on politics"
  - "what's going on in politics"
  - "who's winning"
  - "so what does this mean"
---

# Political Intelligence Briefing

Deliver a political read that is grounded, legible, and lands on consequence.
Politics is the domain where sourcing discipline decays fastest — everything is
someone's framing — so the ladder below is the skill's core, not an appendix.

## Procedure

1. **Fan out 4–6 narrow queries in one turn, then extract.** Theme them as
   institution × topic (election body, court, legislature, regulator, coalition,
   wire desk). One wide "what's happening in politics today" query returns
   listicles and misses the official record.
2. **Climb the ladder for each claim before it enters the brief** (see below).
   Note the rung you actually reached; do not promote a lower rung in the prose.
3. **Do the arithmetic yourself.** Seats per bloc, who holds a plain majority,
   separately who holds two-thirds, and which chamber or assembly's term expires
   next. Coalition survival is usually a counting problem, not a mood.
4. **Find the clock.** Name the next scheduled, unavoidable event that forces a
   decision, and who owns it. A political read without a deadline is a digest.
5. **Write it chat-first** (see output contract). Only escalate to a designed PDF
   when the user asks for a document.

## The Verification Ladder

```
primary record  → official result page · charge sheet or written judgment ·
                  gazette/statutory instrument · confirmation by the issuing body ·
                  legislature division/confidence-vote record
statutory body  → ministry / commission / central-bank statement
                  (still an interested party, not a measurement)
party claim     → speech, assembly resolution, floor challenge, press conference
                  = INTENT evidence only, never outcome evidence
analyst desk    → think-tank notes, wire explainers, regional forums
                  = framing and scenarios, never the payload for a fact
```

Rules that follow from the ladder:

- **Allegation ≠ finding.** An investigative report, an NGO demand, an opposition
  claim and a bloc talking point are all allegations. Name the alleger and carry the
  accused's response in the same breath. Never let the loudest party's framing become
  the narrative voice of the brief.
- **"Charged" ≠ "convicted"; "the document exists" ≠ "the document is enforceable."**
  Procedural state is the fact; outcome is a separate rung.
- **Separation-of-power check.** Courts, monarchies, election commissions and pardon
  boards are institutions, not coalition players. Quote their own instrument and state
  whether the act was advisory, deferred, or refused. Folding them into the horse-race
  is a category error.
- **Contested figure:** two credible sources, one number, different values → report
  both with source tags and call the range unresolved. Never average into a false middle.
- **Forecast vs schedule:** timing set by an expiring term or a mandated deadline is
  scheduled reality; timing set by "the leader will decide" is speculation. Label them
  differently in the same sentence if you have to.
- **Test a pact against the ballot paper, not the press conference.** An alliance is visible
  where nominations were filed: who contested whom, and who stood aside. Two states won by
  the same bloc is not two states won by the same pact — read each state's nomination list
  before generalising the arrangement to a national one. ("Bloc A won State X outright, and
  Bloc A+B won State Y together" ≠ "the pact has now won twice".)
- **Where the actor is a component party, name the party, not the coalition.** "The coalition
  cut ties" when one dominant component party did it overstates unanimity and misattributes
  the act — and the coalition's own chair may contradict it within days. Attribute the act to
  the body that performed it.
- **A contested exit is a state, not an outcome.** When one leader declares a member out
  under a coalition clause and the coalition chair says the member remains, the finding is the
  dispute and the body that will settle it (registrar, court). Carry it as CONTESTED — see
  `synthesis-verification-gate`.

## Pre-send figure ledger (mechanical — four questions per number)

Run this on the draft before it leaves. Any "no" is an edit, not a hedge.

1. **Document and period** — can I name the release each figure came from (body, title,
   date)? A figure whose provenance is "reports" is not audit-ready.
2. **Said or computed?** — if I computed it (delta, share, per-capita, or a *level*
   back-solved from a published percentage), is the derivation shown and the figure labelled
   as mine? Never hand a source's name to a figure the source did not publish.
3. **Right metric name?** — a value can be correct while its label is wrong: volume vs value,
   production vs exports, national vs state, nominal vs real, stock vs flow.
4. **Right digit and right rounding?** — a drifted decimal in a brief whose authority is
   precision reads as invention. Re-open the source for every number you intend to make
   load-bearing.

Then: the figures that fail (1) or (2) come out of the sentence, or carry the label inside
it. Do not park them behind a closing "figures from public reports" line — that sentence
grants provenance to every number in the brief, including the ones without any.

## Standing protocol (F13, locked 2026-09-18)

Two checks run by DEFAULT on every intel read, not on request. They are the two failure modes that
survive an otherwise disciplined brief, because both produce a result that *looks* verified.

**1 · Anti-thesis query.** Before synthesis, run at least one live query shaped to REFUTE the core
thesis, and record what it returned. A thesis that has only ever been searched *for* is a preference
with citations. Log it either way — `ANTI_THESIS_RUN: <query> → <result>`. **A counter-query that
returned nothing is a result and must be logged as such**; silently dropping it is how confirmation
bias launders itself. If the counter-query contradicts the thesis, the thesis becomes CONTESTED —
never "mostly true".

*Worked example, 2026-09-18:* a brief asserted that state-election losses created the leverage that
produced recent Borneo concessions. The counter-query surfaced the concession timeline — RM300m→RM600m
(Sept 2024), Petros aggregator recognition (Feb 2025), joint declaration (May 2025) — every item
predating the July/August 2026 losses. The thesis died. What survived was smaller and defensible:
electoral arithmetic explains the *timing and staging*, not the content.

**2 · Chronological lock.** Two events may be joined in a cause→effect sentence only if both carry
absolute timestamps and `t_A < t_B`. Check the mechanism was even *available* at the earlier date — an
actor cannot respond to a thing that had not yet happened. `LOCK: A(YYYY-MM-DD) < B(YYYY-MM-DD) →
ORDERED` or `→ UNESTABLISHED`.

**Contested is a state, not a hedge.** Aim it only where two NAMED parties of standing contradict each
other on the same status and a third body owns resolution. Widen it carelessly and everything becomes
"it's complicated", which is its own failure — the mirror of premature closure. Related machinery:
`synthesis-verification-gate` (Phase 2.5 — source independence + chronological lock) and
`APEX-humility-godel` (reflex 6 — anti-thesis query).

## Output Contract (chat delivery)

1. **Tension first.** Open with the contradiction the events sit inside — not a summary
   of events. That sentence is the thesis; everything after it is evidence.
2. **Three burning items, maximum.** Each carries a concrete artifact — figure, ruling,
   seat count, named instrument — never adjectives or atmosphere.
3. **The clock.** See Procedure step 4.
4. **SO WHAT — two consequences, maximum.** One for the country/policy, one for the
   user's own working reality. Never close on a recap, a table, or a menu of options.
5. **State the wall in one line.** If a figure could not be verified this session, say so
   plainly and move on. Naming the gap reads as rigour; padding it reads as noise, and
   inventing it is disqualifying.
6. **Register follows the user.** For this principal: BM Penang, short sentences,
   "hang/aku", no headers or tables unless the content is genuinely tabular. Collapse the
   search noise — the human sees one clean read, not the research.

## Pitfalls

- **`web_search` can return a W_SCAR-style HOLD** when the query names a
  money/legal/trading variable directly (subsidy cost, court bid, dividend, budget figure).
  It is a query-shape guard, not an outage. Retry the same intent with the variable named
  indirectly — the actor, body or scheme instead of the price or amount — and the rephrase
  passes. Do not abandon the enquiry, and never report the hold as a capability limit.
- **Extract the article body, not the search snippet.** Snippets truncate mid-clause and
  have inverted meaning (a deferred decision read as granted). When extraction hits a JS
  wall or paywall, switch to another outlet carrying the same wire story — never fill the
  gap from the snippet.
- **Quote the wire, not a rewording of the wire.** Outlet summaries of a statement drop the
  qualifier that carries the meaning ("conditionally", "in return for", "deferred").
- **Cross-check the date.** Political pages resurface old analysis; a piece about an
  election or a court stage from an earlier cycle reads identically to today's. Confirm the
  publication date before it enters the brief.
- **Do not stack analyst predictions as facts.** Where several desks agree, say "the
  consensus read is" and mark it as interpretation.

## Scar anchors

| Date | Incident | Lesson |
|---|---|---|
| 2026-09-18 | A coalition-exit status was briefed as settled (member "automatically out") while the coalition chairman publicly said the member remained and the dispute had gone to the registrar; the same brief attributed a component party's decision to the coalition as a body | Carry contested status as CONTESTED with the resolving owner; attribute acts to the actor |
| 2026-09-18 | Two states won by the same bloc were narrated as two wins for one electoral pact, though nomination lists showed both blocs fought each other in one of them | Read nomination lists per state; a bloc's shared ally is not a pact |
| 2026-09-18 | Real-wage levels were presented as a World Bank finding; the Bank published a percentage growth figure — the levels were consistent with back-solving it | Derived figures carry the derivation; a source's name is not available to a number it did not publish |

## Related skills (read, do not edit)

- `news-research-briefing` and `executive-intelligence-briefing` — the heavy document
  variants (sectioned briefings, designed PDFs, tersurat/tersirat layers). These are
  user-owned; propose changes to the user rather than editing.
- `Malaysia Reality Stack — Primary-Source Routing` — macro/fiscal/energy/corporate
  primary-source routing for Malaysia. Also user-owned.

## Depth

- `references/malaysia-political-sources.md` — verified Malaysia political endpoints
  (official result pages, courts, parliament, statutory bodies) and extraction routing.
