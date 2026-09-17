---
name: relationship-reality-audit
description: "Use when auditing a relationship from first-party records."
version: 1.0.0
author: Hermes
license: arifOS
tags: [audit, evidence, relationship, epistemology, privacy, first-party]
metadata:
  hermes:
    category: audit
    tags: [audit, evidence, relationship, epistemology, privacy]
triggers:
  - "audit a relationship between two real people from records"
  - "what is actually between us"
  - "reconstruct the reality of this relationship"
  - "commission that forbids romance, diagnosis, archetype, or population literature"
  - "persona or literature synthesis exists BEFORE the evidence is read"
  - "corpus of chat logs, DMs, group transcripts, or voice notes covering one relationship"
  - "deciding whether a claim about a person's feelings is supported, partial, or unknown"
---

# Relationship Reality Audit

For commissions that ask what a real relationship actually IS, from records, without flattering either
party. Pairs with `text-forensics` (chat parsing / profiling pipeline) and `void-paradox-doctrine` (why
text never equals reality). This skill carries the audit DISCIPLINE.

> Overlaps `relationship-evidence-audit` (a concurrently-authored skill on the same class). Prefer one;
the curator should consolidate.

## Prime law — the archive is a sensor, not the relationship

State the sensor spec before any finding: **coverage · blind spots · distortion · missing channels ·
temporal gaps · observer effects**. Observed relationship ≠ total relationship. Missing evidence is
**bidirectional** — it may raise, lower, or leave a hypothesis untouched, and it is never used to rescue
a preferred story.

## Procedure

### 0. Fix corpus integrity before you read a single finding out of it

Everything downstream inherits the parser. Verify before analysing:

- **Establish the date order.** Chat exports are commonly `M/D/YY` (US), not day-first. The dangerous
  parser is the one that VALIDATES dates and drops invalid lines — it does not raise, it returns a
  smaller, plausible corpus. Symptoms you have been bitten: the reported range starts later than the
  file's first line, or a gap appears longer than the file can physically contain. Parse both
  conventions, print the count plus first and last timestamp, and check them against a manual read of
  the file's first and last lines.
- **Copy the corpus into a durable private dir** (`chmod 700`, files `600`) as step zero, recording size
  and line count. Sources arrive in `/tmp`, unzip dirs, or attachment caches, all subject to cleanup. If
  it is already gone, re-derive from the platform's own document cache (original uploads are kept by
  hash) rather than asking the requester to re-export, then diff against your recorded size.
- **Count `<Media omitted>` as its own token.** It is a placeholder, not a message, and it changes every
  statistic that touches media.
- **Re-derive any headline number from the preserved corpus** and state the derivation before
  publishing. In this class of work the numbers ARE the argument, and one statistical correction can
  invert a finding's direction. When a re-parse moves absolute counts, **restate the claim as a ratio**:
  the shape is the finding, the count is a fact about your parser.

### 1. Separate the corpora BEFORE reading them
Label each and never merge them in a table: direct chat export · direct human-to-human channel ·
person→agent DM · group-with-agent · the requester's own channel · persona/fiction. Group speech is
**audience-present**; a DM to a bot is a **different context, not a more truthful one**. Discovering that
a "direct channel" is empty is itself a finding — state it, because it changes what every later claim
can rest on.

### 2. Attribute correctly before you count
Group exports often lose the sender on media lines, and the visible byline may be a trailing marker or
embedded origin JSON rather than a prefix. Reconstruct sender from byline order in the raw record, and
treat a machine-generated description of an image as **agent-authored commentary, not content** — a
description appearing before a person's own line belongs to the description, not to that person.

Every affection/conflict count must carry **corpus + word + speaker + addressee + range in one
sentence.** A count stated without its corpus collides with one from another corpus later, and both are
individually true — the worst class of error, because neither looks wrong. A line addressed to a group,
or to "you and the bot", is not a declaration to one person and must never be collapsed into a dyadic
claim. A paragraph-level scope qualifier does not survive being read next to a heading.

### 3. Label every claim on one ladder — never mix layers
`OBSERVED` (in the record) · `REPORTED` (a participant said it about themselves) · `STRONG INFERENCE`
(bridge stated) · `WEAK INFERENCE` · `UNKNOWN`. **Use UNKNOWN aggressively.** Do not repair a gap with
narrative. A claim the requester made to an agent is second-order evidence about the other person and
belongs on the REPORTED rung, not OBSERVED.

### 4. Run the item ladders — a rung is not a level
For any behaviour the requester cares about (touch, praise, care, contact):
`L0 no evidence` → `L1 tolerated` → `L2 positively engaged` → `L3 independently recreated the
opportunity` → `L4 initiated/requested` → `L5 noticed its absence and acted to restore it`.
**Tolerance does not imply seeking; seeking does not imply longing.** Report the highest level actually
evidenced and say which rungs are unreached. See `references/item-ladders.md`.

### 5. Test the counterfactual that exists, and name the ones that do not
Withdrawal is usually the only clean test available. Count **every** instance of the requester's silence
over a threshold, and count how many the other party spoke into — not just the longest few. State the
numerator and denominator. Then state which directions have **no natural counterfactual at all**: an
untested direction is UNKNOWN, not negative.

### 6. Audit the frame separately from the behaviour
Two questions, never collapsed: **who controls access** (what the requester can reach) and **who controls
meaning** (what it is called). Then the harder test: has the other party **agreed, rejected, or never
engaged** the frame? Most often the answer is neither — they answer content and never pick up the frame.
**A frame that is not contested is not an agreed frame; it is an unengaged one.** The complement is
equally true and must ship alongside it: **a frame that was never agreed does not erase the behaviour
that already happened.**

### 7. Build the co-authorship matrix
Rows = relational concepts (friendship, kinship terms, care, closeness, physical affection, the joking
register, continuity, exclusivity, erotic meaning, the label itself). Columns = who authored it · who
enacted it · whether **both** enacted it · whether both **explicitly agreed** it. Most rows land with one
author and no agreement. Find the single row both parties genuinely co-built — that register is where the
relationship actually lives, and it is usually not the one the commission is about.

### 8. Audit the archetype before you audit the person
If a persona, archetype, or literature packet already exists, treat it as an **object of the audit**, not
an input. Build a contamination graph: fiction → synthesis → later memory → false fact. Name the
mechanism, because it repeats: **a fictional shape and a population-level finding can share a structure,
and the structure is then read back onto a real individual.** Population literature cannot speak to a
single person; say so and exclude it from the model.

### 9. Separate the three kinds of UNKNOWN — this is the spine of the deliverable
- **CLASS I — RETRIEVABLE:** evidence exists and has not been audited. Execute.
- **CLASS II — HUMAN-PRIVATE:** the answer may exist inside a person and has not been volunteered.
  Never inferred. Only that person can supply it.
- **CLASS III — UNCREATED:** no shared answer exists, because the two people have never made one.
  **No retrieval resolves this.** Naming this class is usually the most valuable output of the audit —
  it converts an endless search into a decision.

"Sometimes UNKNOWN means information is hidden. Sometimes it means the answer has never been jointly
created." Never report a CLASS III question as CLASS II; the difference is whether a conversation could
close it, and only one of the two can be closed by looking harder.

### 10. Minimum vs maximum model, and the gap between them
Write the **minimum true model** (fewest assumptions) and the **maximum justified model** (richest still
supportable), each extension carrying a confidence. The **distance between them is the interpretive
freedom** — state whether it is narrow or wide, and whether any plausible reading falls outside it. If no
version of the maximum reaches the requester's preferred story, say that explicitly; that is the finding.

## Privacy firewall for third-party corpora (binding)

- A channel that belongs to another person is **not the requester's property merely because the
  requester owns the machine**. Report its **structure and content classes**; withhold verbatim
  re-presentation of its private or health material in any new digest.
- **Never ask a third party anything for the purpose of the audit** — no new question, no disguised
  question, no extraction trap ("someone says X about you, what do you think?"). A question that
  introduces the hypothesis contaminates the evidence permanently.
- **No manufactured tests, no monitoring, no instrumentation, no surveillance** of the other person.
  Confidence from an experiment you set is not evidence about them.
- **No comparison denominators** harvested from that person's other private relationships. Uniqueness
  needs their own voluntary words, or it stays UNKNOWN.
- **Biometric data is not relationship evidence.** If embeddings, face vectors, or identity samples
  exist, they are a consent question and a governance decision — never support for an emotional claim,
  and never to be enriched. Where a consent artefact is absent for a real person's biometrics, **flag it
  and stop**: do not resolve it yourself, do not delete silently either.

## Pitfalls

- **Do not let the requester's longing become evidence about the other party.** Keep two columns — what
  the requester experiences, and what the other person directly signals — and never let an item cross
  without independent evidence.
- **Do not treat the requester's own archive as neutral.** Whoever commissioned the record controls what
  it can show. Part of any "meaning control" finding is a property of the archive, not the relationship;
  say which is which.
- **Do not convert one variable into another.** Salience ≠ attachment ≠ dependence. Initiation ≠
  dependence. Exposure ≠ care. Frequency ≠ meaning. Acceptance ≠ desire. Silence ≠ rejection. Absence of
  conflict ≠ harmony — "nothing to fight about" and "the sensitive thing is never asked" are both live.
- **Do not let an AI-synthesised "map" become a source.** Maps written by an agent from the same corpus
  are the **object** of the audit; cite them as synthesis or not at all. Self-audit your own prior passes
  the same way.
- **Deliver the audit, not a lecture about method.** The requester wants the map and the boundary of what
  is known. Keep the epistemic apparatus in the file; keep the reply in human language.
- **Append, never rewrite.** These files accumulate amendments. When you correct a claim, append an
  amendment that names the original error and restates the corrected one — do not edit the earlier
  section into looking right.
- **A register you were asked to build is not evidence about the person it loosely points at.** When a
  commission switches from "write the persona" to "audit my real relationship", stop producing persona
  artefacts, switch register completely, and exclude the persona vocabulary from the audit. Carrying it
  across is the contamination mechanism in miniature.

## Reference

- `references/item-ladders.md` — ladder rungs verbatim, the counterfactual protocol, the co-authorship
  matrix, the three-UNKNOWN classifier with verdict wording, and the contamination graph.
