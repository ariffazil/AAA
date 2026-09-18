# Malaysia — Political Source Ladder (endpoints & routing)

Companion to the generic ladder in SKILL.md. Verify reachability at use time; mark
anything unreachable as a gap in the brief rather than substituting silently.

## Primary record

| Layer | Source | Routing |
|---|---|---|
| Election results | official results portals published by the national news agency per state poll (`prn.<agency>/<state>/keputusan/official/`), plus `electiondata.my` for seat-by-seat and historical comparison | Media tallies published before the official page are *unofficial* — label them, and never carry numbers across the flip |
| Court / prosecution | charge sheets, written judgments, prosecutorial confirmations | Report the procedural state precisely; a document's existence and its enforceability are separate findings |
| Legislature | Hansard and written parliamentary answers (`hanpar.parlimen.gov.my`, `parlimen.gov.my`); supply and confidence votes | Geo-blocked from datacentre IPs — route via search cache or browser render. A budget/supply vote is a constitutional event, not a news item |
| Statutory bodies | finance ministry, PMO, anti-corruption commission, election commission, state secretaries | Treat as a claim by an interested party. Use for what the body *says it will do*, not as neutral measurement |

## Coalition / calendar layer

- Seat totals per bloc and the majority thresholds (simple vs two-thirds) — recompute, never trust a summary.
- Term-expiry calendar across federal and state legislatures: whichever expires first pins the earliest plausible poll date. Federal terms, state assembly dissolutions, and by-elections are separate clocks.
- Distinguish a *state* poll from a *general* election when reading timing speculation; outlets conflate them regularly.

## Secondary / framing

Regional think tanks and journals (ISEAS, RSIS, East Asia Forum, FULCRUM, New Mandala) and the
international wires give the clearest structural read; use them for pattern and scenario, never as
the payload for a fact. Independent domestic outlets carry the best political desk work but are
partly paywalled — headline-level use only unless access exists.

## Sourcing pitfalls (Malaysia-specific)

- Local-language outlets carry a minister's full quote that English summaries compress into a headline; where a qualifier matters, go to the BM report.
- Aggregator portals recycle wire copy under their own banner. If three "different" outlets run an identical paragraph, that is ONE source.
- Interviews and speeches are intent evidence. The follow-through shows up weeks later as a gazette, an award, or a dissolution — check for it before treating a promise as policy.
- Search-result snippets from JS-heavy local outlets are frequently stale or partial; extract the body or find another outlet carrying the same wire.
