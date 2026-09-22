---
name: builder-commercial-positioning
description: "Use when a builder asks what to sell."
tags: [positioning, marketability, open-source, monetization, go-to-market, career-leverage]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Builder Commercial Positioning

For the question "is this marketable, and what am I actually selling?" — asked by someone who has
built something real (a runtime, a kernel, a platform) and now has to know which part of it converts
to money, and which part is only a credential.

## When to use

- "What am I selling?" / "Is this marketable?" / "Is this worth leaving a job for?"
- A repo, product, or skill set is being weighed as the basis of an income.
- Choosing between selling software, services, or the person's own capability.

## Procedure

1. **Separate the candidate goods before answering, and rule on each one.** Name them explicitly:
   the *project* (the software), the *infrastructure* (the machines it runs on), the *credential*
   (the repo, the commit history, the deployment record), and the *person* (the operator and what
   they can do). Different buyers, different prices, different ceilings. Almost every confusion in
   this conversation is one of these being mistaken for another. A private federation does not sell;
   a repository does not sell; a person with a demonstrated record does.
2. **Measure adoption with a real number against a named competitor.** Never answer from
   impression — pull the live figures for the project *and* its nearest rival, and report the
   **ratio**, not the count:

   ```bash
   gh api repos/OWNER/REPO --jq '"\(.full_name) stars=\(.stargazers_count) forks=\(.forks_count) pushed=\(.pushed_at)"'
   ```

   Run it once per repository. Where `gh` is unavailable or unauthenticated, read the same three
   fields off the repository's public JSON — but never substitute a remembered figure for a fetched
   one. Do not build this as a shell pipeline into an interpreter: that shape trips the
   command-safety scanner and the whole run is blocked. One plain API call per repo is enough.
3. **Test discoverability in the buyer's own words, not the project's.** Run the searches a buyer
   would run: the generic category term, category + "framework", category + "open source". Record
   which query surfaces the project and which does not. Placement on page one of exactly one query,
   via a topic tag, is not search presence.
4. **Ground demand in dated commitments, not sentiment.** A market claim needs an external party
   already committed to a date: a regulation with an enforcement date, an industry framework a
   regulator has endorsed, a budget already allocated. Survey sentiment is supporting colour; a
   deadline is the demand. Search for the calendar, then for the vibe.
5. **Name the moat as a capability, not a noun.** If competitors share the category phrase, the
   phrase is not the asset. The defensible line is what this builder can do that the field cannot —
   run it in production, produce the failure record, and translate between compliance vocabulary and
   the terminal. State plainly where the nearest well-funded competitor is better.
6. **Ladder the offers by speed to first revenue.** Typical order: audit (small fixed fee, converts
   fastest, buys credibility) → implementation engagement (large, depends on the audit) →
   workshop/training (low ceiling, fast cash, doubles as the sales channel) → hosted product
   (highest ceiling, slowest, needs a team and distribution). Say which rungs are NOT viable yet and
   why — that is part of the answer, not a hedge.
7. **Quote the rate benchmark with its spread.** Independent, boutique and large-firm tiers differ by
   multiples for the same deliverable; give the range, name the source, and note any compliance or
   governance premium.
8. **Close on the one artefact that unlocks the rest.** Usually a single outside human who used it
   and wrote a paragraph. An external reference converts "person with a project" into "person with a
   record", and it does more than any amount of stars.

## Always-on rules

- **Separate goods from credentials.** A repository is a credential and a proof-of-work, not
  inventory. Open-source software is rarely sold as code; what sells is compliance, managed service,
  migration relief, training and packaging.
- **Never quote a self-published or auto-generated metric as market evidence.** Directory listings,
  package-registry pages, connector catalogues and automated scanner scores are produced by or about
  the author, or generated with no human involved. Count only independent adoption or human use.
- **A project with no outside user is not a product.** Say so without softening, and say what the
  first outside user is worth relative to any amount of polish.
- **Do not position against free bundled tooling from a hyperscaler.** Competing as a framework
  vendor on distribution is a loss. Position as the implementer, in a market where relationships and
  local regulation matter more than brand.
- **Put the honest verdict on the table, including the non-viable lanes.** Naming three things that
  are not for sale is substance, not hedging.
- **Hand the decision back.** Give the analysis, the numbers and the ladder. Do not tell the person
  to quit, and do not certify that a runway is "enough".

## Pitfalls

- **Do not mistake discoverability for ranking.** A topical tag can place a project on page one of
  one query; reporting that as presence overstates the position badly.
- **Verify a competitor's own capability claims before repeating them.** "Covers N/N of the standard"
  is self-reported; check it against the standard's own item list whenever the comparison is
  load-bearing.
- **Do not let a category label substitute for the differentiator.** If a competitor already owns the
  phrase the builder is using, repeating it is competing on their ground.
- **Answer "is it enough?" with the denominator, never with a yes.** Size questions resolve to
  "enough for what", and the answer lands on burn rate, the expected time to the next income, and
  dependants — not on the total. The same figure reads as large against monthly burn and as modest
  against income replacement; give both readings and let the person weigh.
- **Do not lead with the build.** The operational failure record — what broke, with numbers — is more
  credible and harder to copy than a feature list, and it is precisely what a competitor running a
  clean demo cannot produce.

## Related

Companion to `external-technology-evaluation` (the reverse direction: judging someone else's
artifact). Where the person is also weighing a job exit, pair with `malaysian-employment-separation`
for the runway calculus.
