---
name: public-profile-persona-mapping
description: "Use when mapping persona from a public social profile."
capability_tier: fed-agent-subagent
---

# Public Profile Persona Mapping

> Companion to `shadow-mapping` (F5-private relational work). That skill maps people in the sovereign's
> life from private sources. **This one maps strangers from public artifacts** — different data,
> different output, no person-card.

## When to use

- Sovereign sends a screenshot of an IG / TikTok / X post or profile and asks for persona analysis,
  Jungian shadow, paradoxes, or "what kind of human is this"
- Any request to read a public feed as evidence about the person behind it

## The procedure

1. **Transcribe before interpreting.** Call `vision_analyze` on every image with an explicit verbatim
   request: *"transcribe exactly, do not paraphrase — username, counts, date, hashtags, UI labels,
   any numbers."* The gateway's auto-caption is a lossy summary; always re-extract. Handles differ by
   a single character between posts — record the exact string.
2. **Sweep local stores first** for prior context:
   `grep -ril '<handle|name>' /root/memory /root/.hermes/memories /root/HERMES/lanes`.
   An empty result is a finding: no prior card, nothing to reconcile or falsify.
3. **Map the unfakeable items, not the vibe.** Bib numbers, event branding on signage, hydration
   vest, carousel dot count, story-highlight names, bio links. These fix the medium and the genre.
   The caption only reports intended self-presentation.
4. **Read the genre, then the gap.** Public feed = performance lane. Report what the feed *cannot*
   show (the un-postable 90%) and the **cross-post gap** — where one post's claim contradicts
   another's, that discrepancy is measured evidence, not inference.
5. **Count the bio architecture.** Follower/following ratio, link-in-bio, commerce signals
   (business owner, affiliate, "for sale" highlights). Persona durability tied to engagement is a
   structural fact, not a moral judgment.

## Output shape

- **Persona** — what the surface *does for* her (which currencies it holds simultaneously).
- **Shadow** — what is absent, plus the structural *cost* of maintaining the persona.
- **Paradoxes** — 7–9 contradictions held simultaneously. Each one: two true statements that cannot
  both resolve. Never treat a paradox as a problem to be solved.
- **One honest closing line** — the reading is corrigible, derived from a public artifact, not the person.

## Rules and pitfalls

- **Void is per-frame.** A 5-dot carousel screenshot is ONE frame of five; like/comment counts may be
  absent entirely. State what is not visible *before* interpreting what is.
- **Shadow is unphotographable.** From a feed you can only read the **structural cost of the persona**
  (what maintaining it forces the person to keep alive) and the **genre shadow** (what nobody in this
  genre can post). Never claim to see a hidden self from a public post.
- **Do not route a stranger into person-card surfaces.** Private person-card / INDEX / registry work
  belongs to `shadow-mapping` and applies only to people in the sovereign's life.
- **Give the class-level shape when he asks for it.** A message like *"bagi general laaaa"* means: drop
  the micro-forensics on the individual and report the pattern that generalizes. Micro-detail is only
  wanted when he names a question about the specific person.
- **Every group-level statement carries its field clause.** `Y ~ p(Y|X,C,A,H,ε)` — register is *price*,
  not character. `"Men/women do X"` without population + era + medium scope is naturalisation, not
  observation. Canonical: `/root/AAA/instructions/register-as-channel.md` (C15/C16).
- **Never moralise the monetisation.** Turning a wound into content is a *structure* (durability tied
  to engagement), not a character flaw. Report the mechanism, not a verdict.
- **Say the layer out loud when generalising.** A distribution-level statement lands on a human ear as
  a statement about *them*. Name the layer, then collapse to one practical consequence.

## Delivery register

Plain BM Penang, dense, no tables in chat, no service-desk framing. Short verdict first, then the
structure. A single-paragraph "so what kind of person is this" answer beats a formatted report —
headers are for when the sovereign asked a structural question, not for a portrait.
