---
name: inherited-claim-audit
description: "Use when repeating a claim from a prior pass or review."
version: 1.0.0
license: arifOS
triggers:
  - "a number or verdict quoted from an earlier audit or session"
  - "user pastes another AI's review and asks me to check it"
  - "build on the previous pass / update the audit"
  - "zero occurrences / never / no evidence of X"
  - "count comparison between two parties or two corpora"
  - "an audit uncovers data about a third party"
metadata:
  hermes:
    tags: [epistemic, verification, audit, provenance, third-party-data]
    related_skills: [claim-receipt-discipline, synthesis-verification-gate, text-forensics, relationship-memory-isolation]
capability_tier: fed-long-context
ecology_state: WARM
---

# Inherited-Claim Audit

A claim that arrives pre-packaged — from an earlier session's artefact, a sibling agent's audit, a
freshly-pasted external review, or an earlier turn of this same conversation — is **not evidence**.
It is someone else's computation, and it may be stale, measured on a different unit, or simply wrong.

> A number you did not compute this session is a rumour with a citation.

The failure this skill prevents is quiet: the inherited number gets repeated, other claims are built on
it, and by the time someone re-queries the source the wrong figure is load-bearing in three artefacts.

---

## 1. The core rule

**Re-derive it, or attribute it — never restate it bare.**

Before repeating any number, verdict, or finding that you did not produce in this session:

1. **Did I compute this now?** If no, either re-run the query (preferred) or carry it with explicit
   attribution: *"per the earlier pass, not re-derived here."*
2. **Is it load-bearing?** If a conclusion rests on it, re-derivation is mandatory. Context-only facts
   (a filename, a date) may be inherited with attribution.
3. **Does it contradict anything I did compute?** A single mismatch means the inherited figure is
   wrong, or was measured on a different unit. Either way it cannot ship unexplained.

A reviewer's **method** can be excellent while their **arithmetic** is inherited and stale. Split them
in the reply: adopt the method, re-derive the numbers, and say which is which.

## 2. Zero-claims and counts need three things

A published zero is a claim about your query before it is a claim about the world.

- **Variant search.** Before writing "zero occurrences", run the word's variant family plus one
  phonetic neighbour, and state the pattern. Chat and dialect writers spell the same concept several
  ways across years — a single substituted letter turns a multi-instance history into an apparent
  blank, and that blank then gets written up as *"he never asked"*, *"no evidence of X"*, and carries
  a whole analysis on top of it. Corpus coverage first, then the verdict.
- **Denominator.** Every zero/percentage claim states the exact denominator in the same sentence:
  *"0 in N-item sample; corpus of M unverified."* Sample findings are not population findings.
- **Unit.** Every count carries its threshold in the same sentence — e.g. *"active day = ≥2
  messages."* Three defensible definitions of the same unit yield three different totals from one
  corpus, and a ratio computed on one cannot be compared with a ratio computed on another. When you
  correct a figure, name the definition you corrected it **to**.
- **Scope.** When two methods give different counts of the "same" corpus, do not silently pick one:
  document the delta, classify where the extra items live, and report both with their inclusion rules.

## 3. Corrections land in the artefact, not just the reply

When a re-derivation contradicts a figure already written into an audit, brief, card, or canon file:

- **Append a dated amendment** to that artefact. Never silently rewrite, never leave the old number
  standing as if it were still current.
- State the defect, the re-verified replacement, and what the correction changes downstream.
- A correction that exists only in chat guarantees the next session inherits the wrong number again —
  which is the exact loop this skill exists to break.

## 4. Claims about people — the firewall

Assembling a picture of a human from records invites a specific class of overreach. Keep these pairs
separate, and never let an item cross without independent evidence from the other side:

| Evidence | Is NOT |
|---|---|
| exposed in the record | caring more |
| initiates more | depends more |
| silent | rejecting |
| seeks contact | seeks touch |
| admires a body | is attracted to a person |
| attracted to a person | an identity label |
| practical care | love |
| tolerance / acceptance | desire |
| repeated choosing | dependence |
| missing evidence | hidden evidence |

Two rules sit under the table:

- **State the rung, and the window.** For any *"does A want X"* question, place the evidence at the
  highest level actually shown — tolerated → positively engaged → independently created another
  opportunity → independently initiated or requested → noticed its absence and tried to restore it →
  sought it *from this person* over others — and report the **period** alongside the rung. Recurrence-
  seeking begins at the third rung; "longing" needs the fifth; the sixth needs a comparison baseline or
  it stays UNKNOWN. A rung with a window is a claim about behaviour; a rung without one is a claim about
  a person.
- **Prefer the natural counterfactual.** The strongest evidence about wanting something is what happens
  when it stops *without anyone deciding to test*. A withdrawal you engineered, announced, or routed
  through an agent is not a counterfactual — it is a probe, and its output is about the probe.

Missing evidence is **bidirectional**: it may raise, lower, or leave untouched any hypothesis. Never use
absence to rescue a preferred story, and never let a missing channel read as confirmation.

## 5. Contamination quarantine

Before delivering, trace each claim to its origin. Anything downstream of an AI synthesis, a persona or
fiction artefact, or population literature is **quarantined** and may never be cited as biography — the
vocabulary in particular: a word coined in one lane does not become neutral description just because it
was repeated in another. If the subject's own words exist in the record, quote them; if the only naming
attempts came from one side, say so rather than adopting their framing.

Also hold this: an *undefined* relationship is not an unresolved retrieval. High behavioural
reciprocity with low semantic reciprocity is a common, real configuration — sometimes the answer was
never created, and no amount of additional record will find it. Distinguish **hidden information** from
**an answer that does not exist yet**, and do not convert the second into either "it was nothing" or
"it was secretly everything."

## 6. When the audit surfaces third-party data without consent

Audits about a person routinely turn up artefacts about *another* person — a message export, a face or
voice template, a medical record. Standing response:

1. **Count the consent files.** The registry unit is one file per human; the operator's own file alone
   means no third party has granted anything.
2. **Read the organ's declared scope** rather than assuming it. A spec line stating an implementation
   is single-subject is a hard boundary a later helper script can silently cross.
3. **Search the scratch path** (`/tmp` and friends) — staged vectors and exports hide there and are
   usually world-readable.
4. **Take custody, then stop.** Move the artefact to a private `0600` HOLD location with a written
   record of what/why/who-decides. Do not delete on your own initiative — revocation is the
   principal's call — and do not leave it readable either.
5. **Never forge a consent entry**, never re-seed from the artefact, and never cite it as evidence about
   a relationship. A biometric proves a reading occurred; it says nothing about anyone's feelings.

**A populated vault is not consent.** A stored vector records that a reading once happened, not a
standing permission. Enrolment ≠ consent, and the operator's authority does not extend to another
adult, however close.

## 7. Deliverable shape

- Evidence base first: what corpora exist, their spans and classes, and what is **absent**.
- Findings with provenance per claim (first-party quote, this session's computation, inherited-with-
  attribution, or quarantined).
- Corrections stated as corrections, in the artefact as well as the reply.
- A void register — what the sensor cannot see — with each void's effect on the open hypotheses given
  symmetrically.
- UNKNOWN as a successful result. *"Reality has not resolved this variable"* is a finding, and it
  removes the need to tell a comforting story in either direction.

See `references/first-party-relationship-audit.md` for the relationship-specific probing shape.

---

## Siblings

- `claim-receipt-discipline` — tags and receipts for claims about file/system state.
- `synthesis-verification-gate` — claim taxonomy before a synthesis output.
- `text-forensics` — parsing and profiling chat exports (the source-side of this work).
- `relationship-memory-isolation` — where private-person data belongs and at what permissions.

*DITEMPA BUKAN DIBERI.*
