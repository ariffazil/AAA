---
name: entity-position-dossier
description: "Use when asked what an entity holds in a province."
version: 1.0.0
tags: [intelligence, upstream, portfolio, asset-map, epistemic-tags, public-sources]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Entity Position Dossier

Builds an evidence-tagged **position dossier** — asset table, capital-flow reading, unpublished-facts
register — from public sources only.

Load when the request is a **position**, not a period: what does this operator hold off X, what is it
actually doing there, and what does the record not say. Counterparty block inventories, competitor asset
bases, an operator's footprint in a basin, state or country.

Not for: current-events briefings, single-disclosure analysis, or anything touching non-public material.
Public sources only, and nothing in the output is a resource estimate.

## Procedure

1. **Fix scope and source class before drafting.** Name the entity, the province and the horizon. Put
   `public sources only` on the cover. If part of the question can only be answered from inside, say so
   in the first paragraph rather than filling the gap.
2. **Work the primary-source ladder** (`references/upstream-source-ladder.md`). Start with the entity's
   own releases *and* its project schedule or annual filing — the schedule is usually the only place the
   project-by-project table appears. Trade press comes after, never first.
3. **Build the asset table before writing any prose.** Asset · phase · interest · partners · key facts.
   Every later claim cites a row.
4. **Reconcile interests field by field.** Never average a block; confirm each percentage against a
   second source where one exists.
5. **Reconstruct the timeline** — award, acquisition, first production, partner change — with a
   *significance* column on every row.
6. **Split the deep dives:** the flagship (how it earns) and the frontier position (what is committed,
   and by when) written separately. They are read for different reasons.
7. **Assemble the unpublished-facts register before the reading**, so the reading is written against the
   known gaps rather than around them.
8. **Tag every claim** OBS / DER / INT / SPEC with a confidence, keep the legend on the first page, and
   close with the epistemic map plus a scope note.
9. **Name the transfer.** Compare the province where the entity earns with the province receiving its
   development and exploration capital.

## Rules that carry

- **Split interests by field; never average a block.** One PSC routinely carries a different share for
  the flagship field than for the rest of the block — an operator premium on the discovery field. A
  single averaged percentage is wrong for every figure built on it. Write `42% general / 56% at <field>`.
- **Obligation is not conviction.** A programme described in the language of a *minimum work commitment*
  is a compliance floor, and obligation wells are drilled to the cheapest compliant standard. Read as
  strategic intent it inverts the finding. Name which one you are looking at.
- **Positions are usually inherited, not built.** Check the acquisition history before reading a
  portfolio as strategy. A block bought wholesale and held for years reads differently from acreage won
  at a bid round and worked. Mark inherited positions in the summary.
- **Compare where it earns with where it spends.** Producing province and receiving province are often
  different places, and naming the transfer is frequently the whole finding. It is inferred from
  disclosed schedules — tag it INT with a confidence and state what it is inferred from, never OBS.
- **Give absent facts their own table.** Question · status · why it matters, status values *not published*
  / *no public evidence* / *partial*. Never estimate the missing number and never drop the row — gaps
  that are invisible make an incomplete dossier read as complete.
- **`No public evidence` is not `does not hold`.** Absence in a disclosed portfolio is not proof of
  absence. Say which you mean, with a confidence and the qualifier.
- **A regional reading is not the operator's thesis.** Placing an asset inside a geological or commercial
  framework the operator has never published is legitimate work — tag it INT at moderate confidence and
  say in the text that it is your reading. A plausible story must not borrow the operator's authority.
- **Tag claims where they appear, legend on page one.** Untagged prose reads authoritative while being
  uncheckable — exactly the failure the dossier exists to prevent.
- **Keep a range as a range.** Where the source gives a value band (`USD 50–250 million`), do not collapse
  it to a midpoint; the band is the disclosure.

## Verification before delivery

- [ ] Every interest split by field wherever the source splits it — no averaged block figure anywhere
- [ ] Every figure carries its period and its source
- [ ] Every obligation programme labelled as such; no obligation well narrated as strategy
- [ ] Every inference tagged INT with a confidence and a stated basis
- [ ] Unpublished-facts register present; no gap filled with an estimate
- [ ] No proprietary, licence, well or reservoir data in the rendered text
- [ ] Scope note states plainly that nothing is a resource estimate
- [ ] Page count and per-page ink share checked on the built artifact before delivery

## Note

A news brief decomposes by beat (politics / economics / social). A position dossier decomposes by asset
and by disclosure gap. Running the news skeleton on a position question produces a document with no
asset table — the one section the reader came for.

Depth: `references/upstream-source-ladder.md`.
