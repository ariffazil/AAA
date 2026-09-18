---
name: human-relationship-audit
description: "Use when auditing a real relationship from archives."
version: 1.0.0
tags: [evidence, audit, relationship, forensic, privacy, epistemic]
metadata:
  hermes:
    category: research
    tags: [evidence, audit, human, privacy]
---

# Human Relationship Audit

Grade every claim; never let fiction, population literature, or a gap become evidence.

For when the question is *"what is actually true between these two people?"* and a fiction, persona, or
population-literature layer about them already exists. The deliverable is a **graded evidence map** —
not a profile, not a diagnosis, not a sexuality classification, and never an optimisation for the more
interesting story.

Load this when:
- the user asks what a relationship *really* is, or asks you to audit one against chat logs, exports,
  message history, or agent records;
- the user pastes another model's analysis of the same records and asks you to adopt or refute it;
- one of the two people has a persona/archetype built around them elsewhere in the federation;
- the user asks to "resolve the unknowns" about a bond.

Parsing and attribution mechanics (chat exports, gateway logs, speaker resolution, corpus hygiene):
`references/archive-parsing-pitfalls.md` — read that before the first retrieval pass.

## Procedure

1. **Build the source graph first, including what does NOT exist.** List every corpus with span,
   volume, and provenance class (first-party both sides / first-party one side / second-order /
   synthesis / fiction). A *missing* lane is a finding, not a gap — if two people have no private
   channel and every recorded exchange happened with a third listener present, that shapes everything.
   Quarantine synthesis and fiction explicitly; they may generate hypotheses, never evidence.
2. **Layer every claim, exactly once.** `OBSERVED` (directly in the record) · `REPORTED` (a participant
   states their own internal state — self-report, not proof) · `INFERENCE` (must carry its causal bridge
   **and** at least one alternative explanation) · `UNKNOWN`. Use UNKNOWN aggressively; never repair it
   with narrative. Reprocessing a document is the moment claims drift from REPORTED to OBSERVED — check
   each tag against the source, not against the previous document.
3. **Write the negative-evidence section.** State what the records *fail* to show, and grade each
   absence: **strong** (the channel would have carried the behaviour and it is not there) vs **weak**
   (the channel does not carry it — anything visual, vocal, physical, internal). Never let a weak
   absence support a hypothesis; never let a strong absence be softened into "we don't know".
4. **Place each behaviour on a dated ladder.** Stop at the highest rung with evidence and never promote
   a rung because the story "sounds like" it belongs there:

   ```
   TOUCH      L1 tolerated -> L2 positively engaged -> L3 independently created another opportunity
              -> L4 initiated/requested -> L5 noticed absence and attempted restoration
   ADMIRATION L1 accepts -> L2 engages/jokes -> L3 displays for reaction -> L4 explicitly solicits
              -> L5 seeks this person specifically -> L6 notices it stopped and bids to restore
   ```

   Record the **window**, not just the rung: "L4 for fifteen months, L0 since" is a different finding
   from "L4". A withdrawn channel and a never-existing channel are indistinguishable without dates.
5. **Map power by domain, never globally.** Contact initiation, physical access, information, emotional
   expression, money, boundary-setting, and who can withdraw cheaply are separate axes and routinely
   point in opposite directions. Any single dominant/submissive verdict is wrong somewhere.
6. **Test the specific hypotheses the user cares about, one row each:** verdict / best evidence /
   counterevidence / alternative explanation / confidence. Do not let a coherent story raise a
   confidence score — coherence is the thing to distrust.
7. **Classify every remaining unknown into exactly one bucket:**
   - **Retrievable** — the evidence exists and this pass has not covered it. Go get it.
   - **Human-private** — the answer exists inside a person and has not been volunteered. Do not infer
     it; only they can answer.
   - **Uncreated** — no answer exists yet because the question was never put to anyone. No retrieval
     resolves this; only future human interaction creates it.

   Naming the third class is often the most valuable output: it converts a permanently failed search
   into a solvable problem.
8. **Ship a minimum model and a maximum-justified model**, then the distance between them. That
   distance is the honest measure of how much interpretation the evidence actually licenses.

## Standing rules

- **Never convert:** contact-seeking -> touch-seeking · return -> dependence · initiation -> attachment ·
  tolerance -> agreement · humour -> flirting · admiration -> attraction -> identity · practical care ->
  love · silence -> rejection · repetition -> importance · one-sided frequency -> one-sided feeling.
  Each step needs its own evidence, and "X's absence is salient to Y" licenses nothing beyond itself.
- **Uniqueness is usually untestable, not unknown.** "Does A value B's attention more than others'?"
  needs a comparison denominator (a second lane, third-party testimony, a matched corpus). If none
  exists, say **untestable from this archive** — do not report it as a gap more retrieval would close.
- **A private DM one person sent to a machine is not the other person's property**, even when the other
  person owns the infrastructure. Not-disclosable unless that person authorised sharing or the message
  was already in a shared channel. When such a corpus turns out to contain nothing about the
  relationship, say so — that is itself a finding, and the firewall then costs nothing.
- **Never use biometric material as relationship evidence.** Sovereign authority over one's own data is
  not subject consent for another adult's. If third-party face/voice material is found with no consent
  artefact, relocate it to a private 600-mode location, write a HOLD record, and escalate the
  delete/keep decision — never delete unilaterally, never analyse it for meaning.
- **Variant spellings before any absence claim** — a zero from one regex is a hypothesis, not a finding.
  See `references/archive-parsing-pitfalls.md`; a wrong negative propagates into every downstream
  document and an external reviewer may then build a theory on top of it.
- **An external model's report may be built on your own earlier bad output.** Check provenance before
  treating it as corroboration — if it cites numbers you produced, it is echo. Verify its figures
  against the raw file before adopting or rejecting any of it.
- **Preserve the boring answer.** If the records support only companionship, ship companionship. Do not
  optimise for romance, eroticism, drama, or closure — and do not optimise for cynicism either.
- **Append-only.** Corrections go in dated amendments; never rewrite the finding that misled, and never
  let a corrected number stand unamended in an older section.
- **Deliverable discipline:** one artefact; no narration of the rounds, retries, or search budget; the
  user experiences the finding, not the search. End with the smallest model that assumes least — then
  stop.

## Related

Sibling skills that cover the adjacent mechanics: the chat-export pipeline, per-person case files, and
relationship-ledger extraction live in the text-forensics and telegram-history skills; this skill owns
the *evidence grading* layer that sits on top of them.
