---
name: human-facing-recurring-card
category: human-interface
description: "Use when building a recurring personal card or digest."
version: 1.0.0
triggers:
  - "daily card"
  - "recurring digest"
  - "personal briefing card"
  - "infographic for us"
  - "balance card"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Human-facing recurring card

A card or short digest that one or two specific people receive repeatedly — daily, weekly — where
the same artifact is rebuilt each cycle. Not a one-off poster (see `infographic-generation`) and
not a multi-page report (see `paged-media-report-layout`).

Distinctive constraint: **the reader is known, the cycle repeats, and the card may be read by
someone other than its subject.** That last part drives most of the rules below.

## Rule 1 — Signal, not poetry

The single most common failure is writing evocative abstraction instead of checkable facts.
Phrases like *"read stone / read body"* or *"what rises / what holds"* feel profound and carry
**no information**. The reader gets nothing he can act on, verify, or remember.

Every line must be one of:
- a dated fact with a source ("fuel up 35 sen, effective 17–23 Sept — MOF")
- a countdown to a real date
- a named place, event, or thing with enough detail to find it
- a true fact that is checkable at all

**Test:** could the reader look it up? If not, cut it or make it checkable. A beautiful line that
can't be verified is decoration, and decoration on a recurring card becomes noise by week two.

## Rule 2 — Memory informs SELECTION, never DISCLOSURE

When the card is personalised from what the machine knows about the readers:

- Use known facts to choose what is **relevant**. Never reprint private life, chat contents,
  family, health, money, or anything said in confidence.
- If the card is read by **both** subjects, every line must be safe for either to read. Nothing
  about person B that is not already public or that B said in the shared space.
- **Cut any item that only lands if you explain why you chose it.** The provenance is the leak.
- A card that shows off what the machine knows has already failed, however accurate it is.

Write the real reason in the content file or the receipt, never on the card.

## Rule 3 — Fixed-count zones beat open prose

Structure the card as a small number of named zones, each with an **exact** count, e.g.:

- `3 must-know` — news / reminder / event / deadline / decision, mixed kinds
- `3 good-to-hear` — true and checkable; this zone fails by manufacturing compliments
- `3 eureka` — true facts, no moral welded on

Fixed counts force selection, which is the entire value. Open sections fill with whatever is at
hand. Enforce the count in the renderer (Rule 6) so the card cannot silently ship with two items.

**No item may appear in two zones.** The same fact twice in one card reads as padding.

## Rule 4 — Keep it alive

A card that is all consequence becomes a duty. Every cycle carries at least one **real,
checkable, near-term** thing near the reader — a gig, a place to eat worth going to, an outdoor
spot, a local event. Verify it that cycle; never reuse a stale listicle.

**Never invent one.** If nothing verifiable is found that cycle, omit the line rather than name a
venue. A fabricated recommendation is worse than no recommendation.

Tone: two people talking, not a dashboard. No corporate voice, no "I have analysed". If it reads
like a memo, rewrite it.

## Rule 5 — Show the principal before broadcasting

If the card goes to a group or anyone beyond the requester, **render it and show it to the
requester first**. A card is a design artifact; taste cannot be verified from a description.
The correction that costs one message now costs a retraction in front of an audience later.

Same applies to any new recurring surface: hand over cycle 1 for judgement before automating.

## Rule 6 — Renderer rules (the defects that recur)

These are mechanical and will bite every time:

- **Balance glyphs: the motif must be unable to encode an unequal quantity.** A yin-yang is the
  right shape for two people because it states equal weight and *cannot* render one subject at
  27% of the other. If you reach for a bar chart or any length-coded form to compare two people,
  check first whether the quantity is actually comparable — message volume, post count and years
  of service are not measures of a person's weight.
- **In a yin-yang, each dot must be the OPPOSITE half's colour.** A same-colour dot is invisible
  and the symbol degrades into two plain blobs. Tie the dot colour to the same variable that
  decides the orientation so the two can never disagree.
- **Mirrored boxes must be equal height.** Left and right panels in a balance layout: set the
  container to stretch and let children flex. Unequal heights on a balance card undermine the
  claim the card is making.
- **Render tall, then crop the tail.** A fixed screenshot height either clips long content or
  leaves dead space on short content. Render well beyond the needed height, find the last
  non-background row, crop there. Correct for both cases, no per-content tuning.
- **Disambiguate any label that collides with a common reading.** A moon phase beside a date reads
  as a calendar quarter unless you say *moon*. Add the glyph and the word.
- **Validate content before rendering and REFUSE on failure.** Reject: wrong item counts, quotes
  without an author, sourced claims without a source. A renderer that renders anything turns a
  content bug into a design bug you then chase in CSS.
- **Separate content from layout.** Content is a JSON file matching a schema; the renderer owns
  layout only and never invents text. This is what lets content improve without touching a single
  style rule.

## Rule 7 — Check the render with vision, every time you change layout

Rendered output must be *looked at* before delivery. Read the image and check specifically for:
clipped text at any edge, invisible elements (contrast against their own background), unequal
mirrored panels, dead space, and duplicated items across zones. Numeric ink-coverage checks catch
a stranded page but **not** an invisible dot or a mismatched pair — those need eyes.

Once the template is stable, per-cycle checks can be mechanical (counts, ink, links); go back to
vision whenever the layout itself changes.

## Pitfalls

- Fixing content by editing layout, or padding content to fill layout. Both hide the real defect.
- Treating a counts-pass as a design-pass. Three items each, all invisible, still fails.
- Adding a scheduled surface before checking what already fires at that time — this host runs
  multiple schedulers, so a duplicate is invisible from inside any one of them.
- Assuming which chat or group the user means. Confirm the target; a bot cannot create groups,
  and "the group" may name an existing space rather than a new one.
- Claiming a recurring surface is proven before it has delivered once unattended.

## Support files

- `references/content-contract.md` — the nine-component JSON contract, with the per-zone rules and
  a worked example.
