---
name: public-column-publishing
description: Use when writing a MakcikGPT/public column article.
---

# Public Column Publishing

Writing and shipping an opinion/analysis column for the user's public surface
(MakcikGPT series on arif-fazil.com/world/makcikgpt). Covers the two halves that
fail independently: the article body, and whether the published URL actually
serves it.

## 1. Write for a zero-context reader — always

Assume the reader has never heard of the dispute, the acronyms, the agencies,
or the people. A draft that opens mid-argument is the single most common
rejection: it reads as incoherent to anyone outside the conversation that
produced it. **The user will reject it and ask for a redo. Lead with context.**

Open with a short context block before any argument:

- What happened, in one paragraph, in plain language.
- Who the parties are and what role each plays.
- Any statute, scheme, or acronym expanded on first use, plus one clause saying
  what it does.
- The scale involved, in units a non-specialist reads.

Only then the argument. If a reader needs the previous conversation to follow
the piece, the piece is not finished.

## 2. Register and voice

- Conversational register: short sentences, direct address, rhetorical
  questions, repetition of a structural refrain, analogies drawn from ordinary
  household life rather than from the industry.
- A running refrain works when it is a claim, not a mood. It must still be true
  after the reader finishes the evidence.
- **Target conduct, decisions, and structures — not a person's dignity.**
  Institutional critique is the goal; personal defamation is not. The user holds
  this line himself and will enforce it.
- Satire is welcome and expected; invented facts are not. The register is
  licensed to be sharp, never to be inaccurate.

## 3. Honesty rails inside the piece

An accusatory column only survives if its own evidence does:

- **Quote you cannot verify** → paraphrase it, and say in the piece that the exact
  wording could not be confirmed. Never assert the quote.
- **One-off accounting item** → label it as such. Recognition of an accumulated
  prior-period amount is not a run-rate loss, and presenting it as one hands the
  reader a one-line rebuttal.
- **Third-party figure** (analyst estimate, consultant deck, recalled number) →
  name who said it and that it is an estimate, or cut it. One wrong figure
  discredits an otherwise sound argument.
- Close with a short verified / corrected / unverified note. It is what makes a
  sharp piece survive scrutiny instead of collapsing on the first check.

## 4. Compression ladder — expect to be asked, in this order

1. Full draft.
2. "Simplify this" / "simplify N lines" — a numbered list, one idea per line.
3. "One line I can forward" — a single standalone sentence.

The one-liner must carry the whole argument, work out of context in a chat app,
and contain no proper-noun dependency that breaks outside the article. When asked
for it, give the line and nothing else — no framing paragraph, no options list.
Producing a summary when a one-liner was requested is itself the failure.

## 5. Publishing is not done until the live URL renders the article

Source of truth is the typed article file in the site source tree. The route
manifest the app resolves against is **generated** from it. Registering a piece
means an entry in the typed index **and** in the generated manifest.

Do not trust `make verify-pages` as proof of reachability. It is a
**status-only** gate: a page that falls through to the SPA catch-all returns
HTTP 200 with the hub render, and the gate reports `ALL PAGES REACHABLE`.

Verify with content markers and a control page — full recipe and commands in
`references/reachability-verification.md`. Never tell the user a piece is
published until the live URL renders that piece's own text.

## 6. Pitfalls

- **Context assumed, not supplied.** The most likely reason for a redo. Lead with
  who/what/why before the argument.
- **Manifest staleness.** An entry can exist in the built output but not in the
  generated manifest, and therefore never resolve at runtime. Check the source
  manifest, not the dist copy.
- **A generator that cannot run.** If the manifest generator `require()`s a typed
  module, it fails on modern Node; a generator that never executes leaves the
  manifest frozen at its last good run and every later entry silently missing.
  Confirm the generator is wired into the build, not invocation-by-hand.
- **Trusting the green gate.** A PASS from a status-only checker is not evidence.
  The proof is the rendered text.
- **Rendering the argument as a person.** Keep the target structural.
- **Offering options instead of the compression asked for.** When asked for one
  line, deliver one line.

## References

- `references/reachability-verification.md` — proving a deployed page actually
  serves its own content: marker assertions, the control-page rule, outcome
  classification, and the registration-gate diagnosis.
