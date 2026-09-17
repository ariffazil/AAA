---
name: pasted-material-analysis
description: Use when he pastes material for analysis or a deep read.
tags: []
related_skills: []
---

# Analysis of Material He Pasted

Arif often hands over material written by someone else — a song lyric, a news piece, a screenshot, another agent's long analysis — and asks for a deep read, or to relate it to his own life. The material is the object of the task. It is never the model for the reply.

## Procedure

1. **Read the material to the end, and check what is missing.** Pasted blocks are often truncated, machine-translated, or copied mid-conversation. Say so if the material is cut off rather than filling the gap from imagination.
2. **Verify the material's anchors before building a reading on them.** Who actually wrote/composed it, when it was published, the numbers, the place names. These are the cheapest facts to check and the most embarrassing to get wrong — one wrong anchor discredits the whole reading even when the interpretation is sound. When the material carries **citations**, fetch each one and check the figure, the direction and the year before assessing the argument at all: a fabricated piece and a properly cited one read identically in prose, and only the fetch separates them.
3. **Separate three things:** what the material literally says · what the material claims about him · what he himself has said. Only the third is ground truth about him.
4. **Compose in his register, not the material's.** See below.
5. **Hand back the one thing only he can answer.** If the material contains a personal claim you cannot place in your record, ask it once, plainly, and let it stand open. Do not build on it and do not silently drop it.
6. **Close short.** One or two things that matter, in his voice. No summary of what was already said.

## When the material proposes doctrine, a framework, or a metric

A long argumentative essay is the shape that most tempts a summary, and a summary is the one thing
it does not need. Three moves, in this order.

**Diff its concepts against our own canon and report the overlap as a fraction.** Grep each concept
name across the instruction, governance and canon trees, and name the file that already holds each:

```bash
for kw in "<concept 1>" "<concept 2>" …; do
  printf '%-30s %s file(s)\n' "$kw" \
    "$(grep -ril "$kw" /root/AAA/instructions /root/AAA/governance /root/AAA/canon /root/AGENTS.md | wc -l)"
  done
```

An essay presenting a thesis as discovery has often re-derived doctrine that was ratified months
ahead of it — measured on one artifact, roughly 28 of its 35 sections already existed here. So the
question is never "is this good?" but **"what is left?"** The residue is the only part with import
value, and it is frequently **instrumentation** rather than philosophy: the principles were sealed,
and never once measured.

**Test any objective function or metric it proposes for degeneracy.** Ask what the optimum is, and
whether that optimum violates a standing rule. A ratio like *verified outcomes ÷ human attention*,
placed beside "silence is a valid action", optimises by never reporting and never escalating — every
unmeasured failure scores as a success because the denominator cannot see it. A constraint list in
prose below the objective does not bind it; only constraints *inside* the objective do. Name the
stronger form rather than rejecting the whole essay: the authority-bearing and irreversible classes
must bypass the optimisation entirely, not be balanced within it. And if its proposed new mechanism
is a **measurement of his burden**, wire it to report and trend, never as a gate — a gate makes
"stop reporting" the cheapest way to improve the number.

**Report three buckets, never a verdict on the essay as a whole:** what is already ratified here
(with the file), what is genuinely new, and what is rejected with the mechanism named. A mostly-true
essay carrying one degenerate mechanism is neither good nor bad — it is a diff.

## When he asks for the material to be KEPT, not only read

He sometimes pastes externally-authored material — another model's spec, a character bible, a
literature review — and the ask is to keep it, not to summarise it. Filing is a separate act from
analysis, and the destination is the whole decision.

- **File it into the register it belongs to, never into canon.** A craft spec for a synthetic
  archetype belongs in that lane's media archive; a doctrine proposal belongs in the instructions
  tree marked DRAFT; a claim about a person belongs nowhere. A persona spec filed next to canon gets
  re-read downstream as a finding, which is the exact contamination the register split exists to stop.
- **The header is the load-bearing part, and the body stays unedited.** Name the original author, that
  he pasted it and when, the register, and explicitly what the file is NOT — canon, memory, session
  preamble, evidence about any named human. Keep his material verbatim below that line. Editing a
  pasted artifact destroys the one thing that makes it quotable.
- **Append your own verification pass below the header, as a table.** One row per cited source:
  CONFIRMED with the identifier you found, or UNCONFIRMED. Verifying first is what turns the filing
  into a finding; naming an unconfirmed citation *and the source that actually belongs in that slot*
  beats a silent omission, because the next session otherwise re-fetches it.
- **Then prove the file carries no leak: grep the filed file for the names of real people in his
  orbit, and show the empty result.** An archived spec that quietly carries a real name is the merge
  this class of work keeps producing, and the grep is cheap, mechanical and repeatable.
- **The reply is what the filing changed, not a restatement.** The verdict, the one citation that did
  not resolve, and which finding cannot travel from a population to an individual. Never a walk
  through the material — he wrote it or chose it, he has read it.

## Register follows the human, never the material

- Language and register are set by **who is talking to you**, not by the text they pasted. A long English article, an English report, or a machine-translated document does not license an English reply. He pasted a translated deep-analysis and got back a formal English report; he had to ask twice why.
- **Machine-translated input has already lost its register. Do not inherit what is left of it.** Reconstruct in his voice (BM Penang, pendek, terus) and answer the substance there. If the material was translated, the only correct output language is still his.
- **Length of input is not a request for length of output.** Document-shaped material invites document-shaped replies — resist. Collapse to the one or two things that matter to him.

## When he references a book he's reading (no material in hand)

He mentions a book title and asks for analysis or distillation. No text is pasted; no photograph is taken. The object lives only in your knowledge base.

**Procedure:**
1. **Verify the book exists before analyzing it.** Quick search — title + author match. If the title might be a chapter, subtitle, or misremembering, say so upfront rather than building a reading on a phantom. "I know Housel's *Psychology of Money* inside-out; I can't confirm a book called *Art of Spending Money* — here's the analysis from his known work, correct me if the title is different."
2. **Give the analysis from what you actually know.** If the book is real and within your knowledge, give the full deep read. If it's partially or wholly outside your knowledge, state the boundary, then give the best analysis you can from related work, marking explicitly what comes from the specific book vs. your broader knowledge of the author's framework.
3. **Critique, don't just agree.** Books he's reading are objects to diff, not authorities to defer to. Name what the author misses, where the framework breaks under local conditions (Malaysia, his industry, his life), and what's genuinely new vs. restated wisdom.
4. **Ground in his world.** Every framework point lands on one of three surfaces: his institution (PETRONAS/geoscience), his bonds (Syed, family), or his own life. Without that landing the analysis is a book report.

**Pitfall — do not fabricate a book you cannot confirm.** If online verification fails (search tools blocked, CAPTCHA, config error), fall back to your knowledge base honestly. State what you know and what you can't verify in the same breath. A confidently wrong book title or invented chapter summary costs the whole reply's credibility.

## Books, products, objects he photographs

He shops and photographs covers, one at a time, then asks for the distill ("analyze and distill the key eureka from each"). When a shelf arrives whole, run it through `vision_analyze` and transcribe the spines before naming anything — never guess a title, author or subtitle from a blurry spine, and skip spines that cannot be read rather than filling them in.

Hold ONE block shape for the whole run so entries can be compared:

- **Title / author** — one line.
- **Tesis** — the object's claim in one sentence.
- **Eureka** — the transferable mechanism, not a summary of contents.
- **Untuk kau** — where it lands in his world: his institution, his own system, his bonds. This block
  is the entire value of the entry; without it the reply is a blurb.
- **Verdict** — take or skip, with one reason, plus one honest caveat when the evidence or framing is
  weak.

Rules:

- **Never fabricate contents.** What you know, unpack fully. What you do not, say so and judge from
  the blurb, the author and the shelf position alone. Naming your ignorance costs nothing; a
  confident invented chapter summary costs the whole run.
- **A shelf gets a shortlist, not a catalogue.** Rank the few worth buying and name the skips with
  their reason. Twenty entries is a spreadsheet; four entries and a skip-line is advice.
- **Material about his own world outranks imported bestsellers.** A book on his country's era, his
  industry or his institution outperforms a translated trend title, because he can check it against
  the building he works in.
- **When the object's message reinforces a wound he does not need reinforced, deliver that as data**
  — what the work concludes, why it lands on him specifically, and a suggested timing — never as a
  prohibition. He is an adult reader; forbidding something guarantees he reads it, and the honest
  frame is the respectful form.

## Pitfalls

- **Do not re-summarise the material.** Restating what he just pasted is the most common way to fill a reply without saying anything. If it is another agent's analysis, the useful move is verifying and correcting it, not paraphrasing it back.
- **Never restate a named real person's private inner state as fact.** Not a loved one's feelings, not what they "secretly fear", not why they are really upset. Mark it as inference, or leave it open and hand the question back. Writing it as fact puts words in a real person's mouth, and it reads as true precisely because it is elegantly phrased.
- **Cantik bukan bukti betul.** An elegant reading of someone's life is not evidence about their life. Beautiful coherence is what a mirror produces; it is not a finding.
- **Do not correct a person's life story with the material's frame.** The material's narrative is a lens, not a verdict on him.
- **A fluent correction beats a fabricated reading, always.** State plainly which parts of the input you could not verify — a short honest note costs nothing and protects the whole reply.
- **Honest citations do not license the conclusion.** "The numbers check out" is a statement about the references, not about the argument. Verify the citations, then still diff the concepts and still test the objective — the two steps are independent, and a well-sourced essay can carry a degenerate mechanism. The same split applies to a review that assembles real studies from six literatures: the stack is genuine and the *synthesis* is still the author's construction. Say which layer is which, and do not let a real bibliography lend authority to a mechanism no study has tested.
- **Do not stage a re-derivation as new doctrine.** Staging restatements of what we already hold as floors inflates canon with what already exists, which is exactly the accumulation the diff was run to prevent. A capability or sensor that falls out of the residue can be built; a floor is not yours to add.
- **Say plainly when nothing was fabricated.** A verified citation record is a real finding and the opposite of the routine outcome for this material class — recording it lets the next session calibrate rather than re-fetch the same four studies.

## When the material is about someone he loves

Keep every rule above, and add: do not write that person's interior at all. Offer what he could do or say to them instead — presence, timing, one unforced question — and let them be the one who speaks for themselves.

## When analysis leads to a parallel deliverable

He may chain: book analysis → summary → system check → PDF. When the session scope expands mid-conversation, the analysis is NOT the bottleneck — the downstream deliverable is. Two moves:

1. **Deliver the analysis inline first** (as normal). The human is reading and reacting in real time; the analytical output is its own value.
2. **Spawn the downstream deliverable immediately** as a background subagent while continuing to engage. The subagent gets a self-contained prompt with all personal context it needs (name, bonds, profession, life details, voice style) and an explicit **no-system-references** ban if the artifact is personal. Do not wait for the analysis discussion to finish before spawning — the latency is in PDF generation, not in conversation.

**Pitfall:** Do not batch the analysis and the PDF into one subagent. The analysis is conversational and interactive; the PDF is a one-shot background job. Mixing them means either the analysis waits for PDF generation, or the PDF gets incomplete input. Separate them.

**Pitfall:** When spawning a subagent for a personal artifact, repeat ALL personal context in the delegation prompt — name, workplace, family details, preferences, speaking style. The subagent sees nothing of the parent conversation. A subagent prompt that says 'write about his life' without the life details will produce generic output.