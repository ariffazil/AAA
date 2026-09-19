---
name: relationship-evidence-audit
description: "Use when auditing a relationship story against the record."
version: 1.0.0
author: Hermes
license: arifOS
tags: [audit, evidence, relationships, chat-exports, epistemology]
metadata:
  hermes:
    category: audit
    tags: [audit, evidence, relationships, epistemology]
    related: [text-forensics, void-paradox-doctrine, claim-level-verification, governed-uncertainty, abang-sado-creative-lane]
triggers:
  - asks for an audit of a relationship against the record ("not a persona task", "an audit of what has actually happened")
  - asks whether a story about a person is actually supported by the messages
  - pastes an external model's analysis of a personal relationship and asks if it is true
  - asks what the record FAILS to show about a bond
  - asks for negative evidence, an UNKNOWN register, or a minimum true model
  - a bond has an AI-authored map/dossier/card about it that is being treated as fact
---

# Relationship Evidence Audit

Different deliverable from a chat profile. A profile answers *what is this person like*. An audit
answers **what does the record actually support, and where has the story outrun it**.

Load this when the framing is an AUDIT of a bond the requester is in — the tell is language like
"this is not a persona task", "evidence-grounded", "what has actually happened", "apply the register
law strictly". The output is allowed to be boring. It is not allowed to be unfalsifiable.

## Prime directive

Reconstruct first. Then infer. Then challenge the inference. Then report what remains.

Population literature, archetypes and plausibility are barred until the reconstruction is complete,
and even then they may appear only as optional comparison — never as diagnosis or causal proof about
an individual. A category is a coordinate for auditing a population; individual evidence decides
anything about a person.

## Procedure

### 1. Corpus inventory and SOURCE CLASS (before quoting anything)

Enumerate every corpus; record span, message volume, active-day count and per-sender split. Then
label each by class. This step is what makes the rest honest, and it is the step that gets skipped
when an audit goes wrong.

| Class | What it is | Weight |
|---|---|---|
| FIRST-PARTY | the two parties' own messages, in any channel | evidence |
| SECOND-ORDER | one party's own words to a third party, including to an agent | evidence of the speaker's STATE; only REPORTED about the other party |
| AI-SYNTHESIS | any map, card, dossier or summary a previous agent wrote about this relationship | **object of the audit, not a source for it** |
| MEDIA | generated voice / stills / video, registry entries | zero weight about any human |
| LAW | sealed care directives, behavioural rules | governs agent conduct; carries no behavioural fact |

**The AI-synthesis trap.** An earlier agent's map of a relationship reads like primary source because
it quotes primary source. It is not — it was written from the same messages now being audited, inside
a session that already believed a thesis. Audit its load-bearing claims (the "wound", the "flinch",
the "motive") against the messages first; that is where the gloss concentrates.

### 2. Count before you narrate

Narrative reading recovers the story the sources already contain. Counting is what falsifies it. Run
all of these first — `scripts/relationship_measures.py` emits them in one pass from a WhatsApp-style
export:

- **Initiation split.** Define an active day (both parties present, ≥2 messages); attribute the day to
  whoever sent the first message. A party who opens most days is not the one waiting.
- **Silence-gap and silence-break.** Largest gaps in EACH party's own posting, and who sent the first
  message in the whole thread after each gap. "Who broke it" is invisible to keyword search.
- **Directional token counts.** Count every contended token in BOTH directions and report both
  numbers. "A used the worship register 19 times; B used it once and that once was B quoting A back"
  is a finding. A one-sided count invites you to read your own hypothesis in.
- **Media counts** per sender, plus the completeness ceiling they create.
- **Absence greps.** Search for the words the hypothesis REQUIRES (an explicit request for the thing,
  an explicit declaration, an exclusivity claim) and report the zero. Zero across the full span is the
  strongest single result an audit can produce.

### 3. Label every claim

Exactly one label each: OBSERVED (behaviour present, with the message it came from) · REPORTED (a
party's own statement about their own internal state — still not independent proof) · INFERENCE (with
the causal bridge written out AND at least one alternative explanation) · UNKNOWN.

Use UNKNOWN aggressively; it is a successful output. Never repair a missing datum with narrative.

### 4. Hypothesis tests with calibrated confidence

State each hypothesis the way the persona or the literature would, then verdict it SUPPORTED /
PARTIALLY SUPPORTED / NOT SUPPORTED / UNKNOWN, with best evidence, counter-evidence, one alternative
explanation, and a number.

Calibration anchors — a hypothesis can be *plausible and untested* at the same time, and the number
must say so: **0.05–0.15** no trace in the record · **0.3–0.45** a few instances, every one with an
innocent reading · **0.6** supported as report, never observed · **0.8+** the archive directly shows
it. Never let coherence raise a number. **NOT SUPPORTED and UNKNOWN are successful audit results.**

**Expect an inversion and do not protect against finding one.** The most valuable result is that the
hypothesised behaviour belongs to the wrong party. Report it plainly, without softening and without
diagnosing — the record is not a compliment.

### 5. Power matrix, per domain

Never one global dominant/submissive verdict. Per-domain rows: initiation, volume, silence-breaking,
who supplies attention, who supplies money, who supplies presence, physical access control, emotional
access control, informational vulnerability, who escalates intimacy, who repairs after conflict.
Asymmetries routinely run in OPPOSITE directions across domains, and that opposition is itself the
finding.

### 6. Negative evidence, then the completeness caveat

Two separate lists. (a) What the records FAIL to show. (b) Where the absence is WEAK because the
archive is incomplete — gaps between corpora, attachments replaced by omission markers, a channel a
party deliberately kept agent-free. Absence in an incomplete archive is not absence in the world, and
the report must say which one it is.

### 7. Three-object firewall

Maintain to the end: **A. actual relationship** (what the corpora support) · **B. the requester's
model** (show the exact evidence gap where B exceeds A — neither treat his reading as projection nor
accept it as fact) · **C. fictional persona / craft artifact** (show overlap with B, usually the
vocabulary; with A, usually nothing). **C is never evidence for A**, and say so in the deliverable,
because the next session reads the same archive.

### 8. Audit the AI, including yourself

Table every place a previous agent transformed: possibility→probability · pattern→motive ·
population-literature→individual-claim · fiction→biography · admiration→sexuality ·
expectation→dependence · playful-dominance→possession. Correct each explicitly. **Include this
session's own errors** — an audit that exempts itself commits the defect it is auditing.

## Verifying a pasted external-model packet

Audit briefs often arrive with another model's research attached. Check each citation resolves (author
+ title, DOI/PMID); an unresolved citation is a FINDING to report — name the nearest real adjacent
source if you find one, and mark it UNCONFIRMED rather than calling the whole packet fabricated. Then
separate the citations from the synthesis: a packet can cite nine real papers and still be its own
argument. Quote the packet's own hedge back ("a synthesis rather than an established phenomenon") and
check that hedge survives downstream reading. File the packet in the register it belongs to — a craft
or media archive with the external author named in a provenance header, never canon, never memory,
never inside an evidence base about a person.

## Output shape

Executive compression (≤10 lines, no archetype labels) · chronology with a layer per row ·
behavioural inventory both directions (observed first, interpretation after) · reciprocity loop test
with N and confidence (N=1 is an episode, N=2 a possible recurrence — reserve "pattern" for genuine
repetition) · attention/admiration mechanics with a confidence per rung · power matrix · hypothesis
tests · where the requester's model exceeds the evidence · where the AI projected · negative evidence ·
UNKNOWN register · **minimum true model**: *"The archive establishes X, Y, Z. It suggests A with
confidence N because B. It does not establish C, D, E."* Then stop.

See `references/output-template.md` for the section skeleton to reproduce.

## Pitfalls

- **Don't start from the hypothesis.** Starting from the archetype guarantees you find its components
  in ordinary friendship behaviour. Reconstruct first.
- **Don't let the archive's confidence set yours.** A confident map in the archive is not a confident
  finding; it is a document with an author and a date.
- **Don't turn the audit into a vocabulary test.** One party's absence of affection-words is not
  absence of affection — compare it against what that party supplies behaviourally and report both.
- **Don't close on a story.** A coherent narrative ending is the failure mode. End on the minimum
  model plus the UNKNOWN list even when that reads as unfinished — it is finished.
- **Don't collapse stages of a construct.** Familiarity ≠ preference ≠ expectation ≠ selective
  seeking ≠ possessiveness ≠ dependence. Quote the stage you actually have evidence for.

DITEMPA BUKAN DIBERI.
