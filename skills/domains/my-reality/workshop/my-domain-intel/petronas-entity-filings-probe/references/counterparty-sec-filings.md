# Counterparty SEC Filings — the Foreign Listed Party's Own Record

Use when a deal involves a **foreign listed** counterparty (Eni, TotalEnergies, Shell, ExxonMobil,
BP, any JV partner). That party's mandatory filings are primary record: dated, signed, and carrying
structure the host country never publishes.

## Why this lane exists

A host government is under no obligation to publish deal terms. A listed counterparty is. So when a
national oil company moves assets into a vehicle with a foreign major, the numbers — asset counts,
regional splits, production rates, financing, accounting treatment — appear in the counterparty's
filing first, and in the host's own release only as adjectives.

Search engines index these poorly: block codes and deal terms return unrelated results. Go straight
to EDGAR.

## Procedure

1. **Full-text search.** A declared User-Agent with a contact address is required; a browser UA is
   served an "undeclared automated tool" page instead of results.
   ```bash
   UA="<Org>-Research <contact@example.com>"
   curl -s -A "$UA" "https://efts.sec.gov/LATEST/search-index?q=%22<deal-or-entity-name>%22"
   ```
2. **Pull the exhibit, not the cover.** A 6-K is a wrapper; the substance is in the numbered
   exhibit referenced inside it.
   ```bash
   curl -s -A "$UA" --compressed "<exhibit .htm URL>" -o filing.htm
   ```
3. **Strip markup before searching the text.** A term can be split across tags in the raw HTML.
   Extract, collapse whitespace, then read a generous window around each hit rather than printing
   bare matches. Carry a **control term whose count must not move**, so a zero cannot be a parse
   artefact.
4. **Read the accounting commentary, not only the operations narrative.** The acquirer's
   balance-sheet notes are where transfer value shows.

## What this lane yields that host sources do not

| Finding | Where it sits | Why it matters |
|---|---|---|
| Asset count + regional split | operations narrative | no host release carries the split |
| Current rate + target rate | operations narrative | separates today's base from the ambition |
| Financing and investment envelope | corporate news exhibit | sets the vehicle's real scale |
| **Gain on contribution** | balance-sheet commentary | explicit that the investment was recognised above the book value of what was contributed — i.e. the assets changed hands below worth |
| "Immediately accretive" framing | CEO/CFO commentary | the acquirer's own statement of value captured |
| Entity domicile / governing law | registration detail | decides which courts and regulator govern |

## Ownership vs operatorship — do not collapse these

One transaction can move two different things at two layers. Counterparties describe their own layer
only. When the acquirer says the assets "retain their current operating set-up" while the host wire
reports the entity "assumed operatorship" on a stated date, both can be true: equity moved at
completion, operations moved on a handover date, and the two dates differ.

Record both, each with its own source and date. The operatorship line is usually the finding that
matters, because it moves **skill**, not just equity — a national company that has handed over
operatorship has lost the capability even while the reserves still sit on its books.

## Worked example shape — the Searah JV

One counterparty 6-K exhibit supplied, in a single document: 50:50 ownership; 19 gas-producing and
development assets, 14 Indonesia / 5 in Malaysia; ~300 kboe/d rising to a >500 kboe/d target; a
USD 6bn revolving credit facility; >USD 20bn planned over five years; >3bn boe of discovered
resources; and a statement that the investment was recognised **exceeding the book values of the
assets contributed**.

The host country's wire carried the operatorship handover date and the region descriptor. Neither
source alone gave the picture; together they did.

## Tooling — and why this lane is sometimes the only unblocked one

The lane is reachable two ways and both were exercised:

- **Harness MCP tools:** `filings_edgar_search` (full-text query, returns `document_url` per hit) and
  `filings_edgar_document` (extract one filing by that URL; returns text plus sha256 and provenance).
  Call them **one per `tool_call`** — local MCP tools cannot be batched, and a mixed batch is rejected
  outright with an error that costs a turn.
- **Raw curl** against `efts.sec.gov` with the declared User-Agent, when you want the underlying JSON.

Two backend behaviours to know before concluding "not found":

- **A compound query can 500.** A quoted multi-term descriptive query carrying boolean operators
  returned `upstream_non_200` / HTTP 500 from the search backend, while a **single distinctive proper
  noun in quotes** returned clean, complete results. Sequence: shortest unique term first, widen only
  if it under-returns.
- **The name the parties invented beats description.** Block codes, asset descriptors and industry
  phrasing pull unrelated filings. The JV or vehicle name is usually the one term that resolves — and
  it is the term the host country's wires and dead links will never give you.

**Route selection, not just tooling:** the W_SCAR gate holds a general web search on a money / health /
legal claim and directs you to an evidence source first. That is not a dead end — it is the gate saying
this lane is the sanctioned route for that class of claim. Reach for the counterparty's filings *before*
the search engine and the blocked search never needs to be attempted at all. When host-side sources are
thin (dead links, unpublished terms) and the general search is held, the filings lane is frequently the
only path that resolves — which is the opposite of the intuition that the gate has blocked you.

## Pitfalls

- **A partner's press release is not the filing.** Quote the exhibit, with form type and date.
- **Do not treat one filing as current.** The next periodic restates relationships and sometimes
  reclassifies them.
- **Entity names drift.** Confirm registered name and number from the counterparty's own letterhead
  before asserting a domicile.
- **An internal anchor figure for the same deal is not corroboration** unless it resolves to an
  instance. A class-level citation beside it is decoration.
- **Disclosure is not wrongdoing.** Structuring assets into a lower-cost vehicle is ordinary
  portfolio management. Report the mechanics and the value asymmetry; do not narrate motive the
  filing does not state.
