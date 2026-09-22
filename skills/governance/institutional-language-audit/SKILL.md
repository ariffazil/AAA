---
name: institutional-language-audit
description: "Use when auditing how an institution talks about itself."
version: 1.0.0
owner: AAA
category: governance
tags: [language, governance, forensics, audit, corporate-speak, rhetoric]
floors: [F2, F7, F9]
autonomy_tier: T1
capability_tier: fed-long-context
ecology_state: WARM
---

# Institutional Language Audit

**Trigger:** someone asks what an institution *really* means by its public statements; asks for a
"deep analysis" of corporate / government / agency language; or wants to show that official
language systematically leaves something out.

**Scope:** measuring the language of an institution's OWN published words. This is not fact-checking
(whether the claims are true) and not motive-reading (why the author wrote it). It measures
distribution and omission — which are countable, and which survive the reply "that's just your
opinion."

## The governing idea

Well-drafted institutional language almost never lies. Every figure in it is usually accurate.
What it does is **choose which truths get the first sentence and which go to the appendix** — and
then report outcomes as though nobody made a decision.

You cannot demonstrate that by quoting. Every quote is true and stands on its own. You demonstrate
it by counting: praise words against human-impact words, sentences that name an actor against
sentences that don't, and above all the words that **never appear at all**. The count turns
"this feels evasive" into an asymmetry the reader can verify.

## Procedure

1. **Assemble the corpus — verbatim, public only.**
   - Take the institution's own releases (primary source), plus at least one independent report of a
     press conference, where executives speak outside the drafted release. The unscripted register is
     where the drafted one shows contrast.
   - Save every document to disk. Write a `SOURCE_VERIFICATION` file recording each URL and its HTTP
     status at capture time. Every figure in the final artifact must trace to one of these.
   - **Verbatim only.** Never paraphrase into the corpus — if you paraphrase, you are measuring your
     own paraphrase, not theirs.
2. **Run the three tests.** `scripts/measure_institutional_language.py <corpus-dir>`.
3. **Write the zeros before the ratios.** The absent words are the finding; the counts are support.
4. **Separate measurement from interpretation**, and label the interpretation as interpretation.
5. **Deliver the corpus and the script with the conclusion**, so any reader can re-run it.

## The three tests

### 1. Actor test — does the text have a subject?

For every sentence over ~45 characters, ask: does it name who did the thing?

- `"Resilient performance was delivered against a backdrop of volatility"` — nobody delivered it, and
the difficulty is weather. Passive construction, agentless cause.
- `"Structural cost optimisation"` — a noun phrase with no verb at all. It becomes a *condition that
exists*, not a decision anyone made.

A high share of agentless sentences (85%+ is common in results releases) means praise has an owner and
failure does not. State that as a contrast: **find the sentences where the institution does claim the
credit, and show what changed when the news was bad.**

### 2. Distance test — praise against people

Count two families over the whole corpus:

- **honour words** — deliver, sustainable, value, strategic, resilient, committed, growth, solutions,
  transition, portfolio, disciplined, prudent
- **human-impact words** — employee, staff, worker, colleague, workforce, retrench, layoff, job loss,
  redundancy, unemployment, accident, injury, fatality, death, safety incident

Report the ratio. Then check the *context* of the survivors: a corpus that says "people" only when
meaning national population has not named anyone.

### 3. Absence test — the strongest result

Count the words you would **expect** given the subject matter, and report the ones at zero.

An institution writing about removing 10% of its workforce while never once writing *employee*,
*staff* or *worker* is not being imprecise. It has selected an abstraction — usually `workforce`
(a size), `headcount` (a number), or `enablers` / `work that is not necessary` (a cost). The zero is
the evidence, and it is very hard to argue with.

Something like `retrench` at zero alongside a five-figure separation programme, or `accident` at zero
in a release that reports a *rise* in injury rate, is the single most quotable line in the analysis.

## Explaining without excusing

Do not stop at exposure. The analysis is more credible — and more useful to someone inside the
institution — when it also says **why the language is structural rather than personal**:

- Many large institutions carry two mandates that conflict (e.g. commercial viability and serving as a
  state revenue source). When they conflict, the institution **cannot say so out loud**.
- So the language routes around the conflict: external forces (`volatility`, `headwinds`, `market
  conditions`) do the work that a decision would otherwise have to admit to.
- The officer drafting it is usually not lying; they are writing the only sentence that will clear
  review. **Understanding that is not the same as excusing it** — the language still produces its
  effect, which is that the thing people most need to know becomes the thing that is most abstract.

Say both. The "why" is what makes an internal audience able to use the artifact rather than merely
feel accused.

## Audience and delivery

- **Ask who the artifact is for, and let that set the framing.** An internal audience does not need
  outsider-facing disclaimers; adding them insults the reader and weakens the piece. Keep the
  public-sources-only discipline either way — it is what makes the artifact defensible.
- **Match the platform the audience actually uses.** If the requester says the readers live on
  WhatsApp, deliver a PDF, not a chat-formatted block or a Telegram-native artifact.
- Keep the artifact shareable without the agent attached: findings, method, source list and the
  script all inside the document.

## Pitfalls

- **Quoting true statements as if quoting proved deceit.** Every line in a well-drafted release is
  accurate. The finding is in the distribution and the absences, never in a single quote.
- **Reading motive instead of measuring distribution.** "They want to hide the layoffs" is
  unfalsifiable and gives the reader an easy exit. "`employee` appears zero times in 47,000
  characters" is not.
- **Paraphrasing into the corpus.** Also: silently excluding a document because it fits the thesis
  less well. The corpus is chosen by subject and type, before the counts are known.
- **Rounding or approximating the counts.** Report exact integers and the word list used; a reader who
  cannot reproduce a number will discount the rest.
- **A table column that does not sum to its own stated total.** Verify the arithmetic in any table
  you publish — one bad subtotal discredits every other figure in the document.
- **Treating a single release as a pattern.** One document is an anecdote. Compare across time and
  across registers (drafted release vs unscripted press conference) before claiming a register.
- **Framing it as a scandal piece.** The analysis lands harder as measurement plus structural
  explanation than as outrage; outrage is easy to dismiss and hard to act on.

## Provenance

Every figure in the artifact traces to a public URL verified at capture time, listed in the document
itself. No internal, non-public or leaked material — that constraint is what keeps the artifact
publishable and its author unexposed.

**Support file:** `scripts/measure_institutional_language.py` — the counter for all three tests
(`--selftest` to verify it works before use).
