# Multi-Document Drafting — Trinity / Parallel-Letter Procedure

> **When to load:** User requests N documents on the same emotional context for different
> audiences ("write A, B, and C", "upgrade all three", "send tonight — I need the trinity").
> Most common shape: separation/exit cycles where the human needs (1) a formal institutional
> letter, (2) a personal scar/witness letter to specific named people, (3) a technical
> memo establishing their professional legacy. All three exist in the same session, the
> same emotional register, but serve fundamentally different functions.

## The Core Law

**Audience classification BEFORE spawn. Voice register per document. The emotional context
is shared, but the register is not.** A trinity that mixes registers fails — a farewell
letter that reads like a personal scar, a technical memo that reads like a manifesto, a
personal letter that reads like an HR document. Each one has its own discipline.

## The Three-Class Trinity (most common shape)

| Class | Function | Audience | Voice | Length |
|---|---|---|---|---|
| **A — Institutional** | Paperwork / record | GM, HR, cc team | Formal, dignified, gratitude-forward | 1 page max |
| **B — Personal witness** | Scar / witness statement | Named individuals (or self-record) | BM Penang, direct, defensibly honest | 1-2 pages |
| **C — Technical legacy** | Professional standing | Geoscience / professional community | Technical register, evidence-based | 2-4 pages |

If the user names only A and B (no C), still ask if there's a technical/professional thread
they want preserved — separation cycles often produce C as a side product that the human
forgets to name.

## Procedure — Pre-Spawn

Before spawning coding agents in parallel:

1. **Audience classification.** For each document, name the audience explicitly in the
   spawn context. Different audiences → different registers. Do NOT let the agents default
   to the same voice because the emotional context is the same.

2. **Scope fence per document.** Each agent gets ONE document, ONE audience, ONE register,
   ONE length budget. Cross-pollution of content between documents is the most common
   failure: a personal scar letter leaking into the formal letter (defamation risk), a
   technical critique leaking into the personal letter (loss of scar's emotional weight),
   the farewell letter including specific well-by-well technical claims (loss of dignity).

3. **Safety audit for personal documents.** Class B (personal witness) MUST include a
   defensive audit: every paragraph must use "saya rasa" / "saya observe" / "saya dah alami"
   framing — never "mereka memang", never named-event specificity without the human's
   consent, never threat language ("Saya akan", "Saya akan pastikan"). The auditor agent
   must explicitly tabulate each risky sentence and verify defensibility.

4. **Voice preservation across agents.** The human's voice is shared, but each document
   takes a slice. Class A: dignified gratitude. Class B: BM Penang direct, boleh ada "wei"
   / "hang tau x" / "macam ni" sparingly. Class C: technical English-BM code-mixing, formal
   register, no emotional content. Tell each agent which slice.

5. **Parallel spawn budget.** Three documents = one `delegate_task` call with three entries
   (under the `max_concurrent_children=10` cap). Output each in full in the agent's reply
   so the human can review in-chat, not just file-on-disk. Do NOT exceed 4 entries — past
   that, debugging cost exceeds parallel gain.

## Procedure — Post-Spawn

1. **Display each file in full in chat.** The user is reviewing for voice accuracy, not
   just structure. Read the files back with `read_file` and present the content — do not
   rely on the agent's "I wrote it" receipt.

2. **Ringkasan per agent.** Each agent must report what it added, removed, kept, and the
   audit verdict. Consolidate these into one short summary block at the end.

3. **Three-question close.** Before any send action, ask:
   - Document A — siap / tukar lagi / skip?
   - Document B — hantar / simpan rekod peribadi / face-to-face dulu?
   - Document C — distribute luas / internal PETRONAS / simpan untuk warisan?
   Each document has its own decision; do not bundle into one menu.

## The Four-Class Trinity (when A is a public article, not an email)

When the user names "A" as a published web article (e.g. `arif-fazil.com/world/makcikgpt/...`)
the trinity gains a fourth class — distinct from the three internal letters because the
audience is *the public*, not a named recipient, and the artifact is *live* on a server,
not a local draft:

| Class | Function | Audience | Voice | Length | Mutation class |
|---|---|---|---|---|---|
| **A — Institutional** | Paperwork / record | GM, HR, cc team | Formal, dignified, gratitude-forward | 1 page max | Local file → outbox |
| **B — Personal witness** | Scar / witness statement | Named individuals (or self-record) | BM Penang, direct, defensibly honest | 1-2 pages | Local file → custody |
| **C — Technical legacy** | Professional standing | Geoscience / professional community | Technical register, evidence-based | 2-4 pages | Local file → professional archive |
| **A — Public article** | External broadcast / external witness | Public readers (anon) | Editorial, restrained, article-voice | 2-5 pages | **Live URL** — requires site deploy, F13 sign-off |

**Why this matters.** A public article is not a local draft. The agent cannot "redo" it the
same way it can patch a markdown file — mutation is publication on a live domain, with
indexing, social-share surface, and no recall. The "trinity" request that mixes a public
article with internal letters is asking the agent to operate across **two different mutation
classes** in one turn. The class A document in the table above is the institutional email;
the class A article here is a different thing. When the user says "A B C", the first
question is: which A — institutional letter, or public article? Both are real, both common,
and conflating them produces either a wrongly-targeted email draft or a wrongly-scoped
publish action.

**Procedure adjustment.** When one of the trinity letters is a public article, the pre-spawn
gate adds a fifth question: **publish / edit-existing / custody-only / draft-but-no-publish**.
The agent MUST default to "draft-but-no-publish" if the live article exists — editing a
live URL is irreversible, and the user has not yet articulated what they want changed in
the public version vs the internal letters. Spawning a coding agent to "redo" the public
article without that clarification is the failure mode: the agent picks an edit axis from
in-session memory, the user has to interrupt with "no, that's not what I meant", and the
live URL is left in whatever state the agent's partial edit produced.

## The "Undefined Trinity" Failure Pattern

When the user says "upgrade all A B C, that's the trinity" WITHOUT naming what A, B, C
are, the next move is **NOT** to invent a three-class mapping that fits the conversation.
The agent's reflex is to map A = the thing mentioned most recently, B = the thing mentioned
second-most, C = the implied third. That reflex fails when:

- the user has been writing parallel drafts all day in the same drafts tree
  (`/root/HAMPA/` accumulates 10-16 sibling files in one emotional window)
- the conversation has mentioned 5+ candidate artifacts (emails, articles, custody notes,
  technical memos, public posts, self-letters) without the user explicitly grouping them
- the user expects the agent to *know* which subset they mean

**The fix.** Before any trinity work, run `ls -lat` on the drafts tree with byte counts and
opener lines (see `references/petronas-counterpart-email.md` Step 1.5), then surface the
**typology**, not the file list. The typology is the four-class taxonomy above plus the
"self / public / third-party-letter" sub-axes. The user picks the slots; the agent picks
the file inside each slot. Default:

- "A B C tu3 mana?" + the directory listing + a one-line typology question
  ("A tu institutional email, public article, atau custody note?")
- NEVER spawn before the slots are confirmed
- NEVER recommend one variant from in-session memory before the directory is visible
- If the user says "hang Arif tau la" / "you know which ones" — name what you would guess
  in one line, ask for correction in one line, then proceed. Two round-trips max before
  spawn; three is decision fatigue the agent produced (bridge-protocol pitfall 14).

**Mechanism.** The user holding the drawer is the work they have done; the agent choosing
for them from in-session memory erases that work. A trinity response that opens with
"Based on our conversation, A = the article, B = the email, C = the exit letter" is
fluent guessing wearing authority. The drawer is the answer.

## Failure Modes

**Mixing registers.** The farewell letter starts sounding like the personal scar letter —
specific grievance, named individuals, emotional climax. F4 violation: a formal letter
loses its institutional function the moment it reads as testimony. **Rule:** Class A
document names individuals only as "penghargaan" or generic "team"; never as "perkara yang
mereka dah buat".

**Cross-document bleed in the human's mind.** The user reads the personal scar letter and
forgets the technical memo exists — until they need it for an HR defense. Keep the
documents visible: name each one consistently (Surat A, Surat B, Memo C) and refer to them
by name in every reply, not by "the letter" / "the memo" / "the thing".

**Defensive over-correction.** The auditor tightens Class B until it loses its emotional
weight — every sentence hedged, every "rasa" replaced with "mungkin", every direct
statement softened to a question. The scar letter becomes unreadable. **Rule:** Class B
is honest but not malicious. "Saya rasa tekanan yang melampau" is defensible AND honest.
"Saya mungkin merasakan tekanan yang mungkin melampau mungkin ada" is defensible AND
unreadable. Audit defensibility, not diction.

**Skipping the third document.** When the user says "A and B", they often have a C in their
head they haven't articulated — the technical / professional / legacy document that proves
they weren't just emotional, they were right. Surface it as a question before spawning, not
after. The cost of asking "is there a C?" is one round-trip; the cost of skipping it is a
user who comes back next session asking for it and re-runs the whole drafting cycle.

**Spawning all three with the same voice.** Even with audience classification in the spawn
context, agents default to a "neutral Arif voice" that doesn't match any of the three
documents. Each agent must be told: "your register is X (formal / personal / technical),
your voice cadence is Y (dignified / direct / code-mixed), your length is Z (1 page / 1-2
pages / 2-4 pages)". Without these three constraints, the parallel batch produces three
variants of the same document.

**Undefined-trinity spawn.** Spawning coding agents in parallel for "A, B, C" without first
naming which three artifacts those letters map to. The fix is the typology question above;
the failure is the agent filling the slots from in-session memory. Even when the slots seem
obvious to the agent, the user holds context the agent doesn't — a comment from earlier
in the day, a draft they discarded, an article they decided not to publish. Confirmation
takes one round-trip; guessing wrong costs the whole trinity.

**Public-article mutation without F13 sign-off.** Treating a live URL on `arif-fazil.com`
the same as a local markdown file in `/root/HAMPA/`. The mutation class is different: a
local edit is reversible; a published edit is on the public record, indexed by search
engines, shareable, and the user has not consented to the specific change. Default to
drafting a *replacement* markdown file in `/root/HAMPA/` and naming the publish step as a
separate F13 decision, never as part of the same spawn batch as the institutional email.
"Spawn three agents, one per A/B/C" assumes all three are local; if A is a live article,
the spawn contract changes.

## The Human's Own Draft Wins — Stop Replacing Prose

When the human provides their OWN prose draft for a trinity document, the agent's default reflex is to *refine* it — tighten, polish, restructure. **This is the wrong reflex.** Three reasons:

1. **Voice is non-replicable.** The user's own prose carries cadence, hesitations, and tone the agent cannot reproduce. Any "improvement" loses signal even when it gains register.
2. **The user has already passed the gravity check.** Their draft carries the witness/verdict distinction they themselves have articulated. Polishing backslides into agent judgement that the user already rejected.
3. **The user re-reads the agent's draft as theirs.** A polished version loses the "this is mine" anchor; the user either ships a document they don't recognise, or rewrites the whole thing again — wasting the iteration.

**Rule.** When Arif pastes his own draft (even a few paragraphs), the agent's job is to:

- Ship it verbatim, or
- Patch only mechanical errors (typo, line-break, single word), or
- Ask *one* clarification if a sentence is genuinely ambiguous

Never spawn a parallel forge agent to "improve" prose Arif already wrote. The forge is for when Arif asks for one (e.g., "forge the email" without pasting). The paste is for when Arif has done the voice work and wants the file saved with audit.

**Worked example.** In the canonical witness-letter session, Arif pasted a 5-paragraph draft (clean witness-mode, terse, "wei" opener, "bumi tidak kenal kalendar" anchor, "30 September bukan kiamat" closing). The agent had already produced V1 (verdict) and V2 (witness-with-still-some-verdict). V3 — Arif's own prose — was the cleanest. The next agent action would have been to ship V3 with one clarification (subject line). Instead the agent offered to "polish" — Arif's reply was "u fail the delivery" followed by his own draft. The lesson is: when the user pastes, treat the paste as the source of truth and the forge as already done.

## Iteration Backslide — The Gravity Drift

When iterating witness-letter trinity documents (V1 → V2 → V3), the agent's gravity drift pattern is:

- **V1** lands verdict (closes the question).
- **V2** moves toward witness but still carries verdict verbs ("trust pecah", "tamat", "tak perlu respond").
- **V3** (or Arif's own) lands pure witness (catatkan, pohon, minta).

Each iteration pulls the document *back toward* verdict because the emotional context primes that direction. **Mechanism:** the spawn prompt includes the conversation history, which is heavy with verdict vocabulary ("trust pecah", "they broke my trust", "sakit"). The agent defaults to those verbs because they're prominent in context.

**Fix.** When iterating a witness document:

1. **Freeze the gravity direction in the spawn prompt** — include explicit forbid-list of verdict verbs ("jangan guna: pecah, tamat, tak perlu, dah decide, sudah cukup, sudah habis").
2. **Include the witness verb list** — catatkan, pohon, rekod, minta, simpan, jadi saksi — so the agent has affirmative replacements, not just negation.
3. **Paste Arif's own prose (if available) as the canonical target** — not as "example" but as "the document this iteration is converging toward".
4. **Single-line gravity check in the agent's reply** — *"Gravity this iteration: WITNESS (recording) only. Zero verdict verbs in final output."*

Without these, V2 will sound like V1 with soft edges, and the user will say "u fail the delivery" again.

**Iteration cap — when "final" means stop.** When Arif says *"now forge the final"*, *"{this is the final}"*, *"{the white flag}"*, or any signal that the current request is the terminal one, the rule is **ONE production, then stop.** Observed pattern: after a "too much" / "humble reflection" rejection, the agent that produces V(N+1), V(N+2), V(N+3) — each incrementally tighter — is not honouring closure. Arif knows when the document is ready; the agent does not. Each iteration past the user's "final" signal costs the document's voice (gravity drifts back toward verdict because context primes that direction) and costs Arif's energy (the user is re-reading and rejecting, which is the failure mode the rule exists to prevent). **The 3-strike rule for witness-letter iteration:** V1 = first forge (no prior). V2 = after first rejection (allowed). V3 = FINAL — after V3, the agent's job is send-candidate cuts and a stop, not another draft. Past V3, the agent has lost the thread even if its prose is technically better. When the user says "the final" and the current version is V2 or earlier, ship V(N+1) once and stop. When the user says "the final" and the current version is V3+, do NOT produce another version — surface the cuts instead. **Mechanism:** the user is signalling they want to move from drafting to deciding. The agent that keeps drafting is reading the user's "final" as "more iterations please", which is the opposite of what was said. The asymmetric cost: a tighter V(N+1) the user accepts costs nothing; a tighter V(N+1) the user rejects costs the document's voice and another turn of the user's attention — which is the highest-priced thing in the conversation.

## The "Reflect and Link" Recovery

When the agent has over-corrected, over-reflected, or otherwise stalled the conversation
mid-trinity ("u have this issue of not remembering prior context and overreacting on
newest prompts. Now can u please reflect and link all first. Not too long and meleret.
Just show the reality with clarity"):

1. **Compact link, no reflection essay.** The user has issued a one-shot reset, not an
   invitation for a long apology. The recovery shape is: name the actual context the
   human gave (with dates, names, the actual decision that was made), confirm the real
   target/topic, return to the work. NOT a 6-paragraph essay on what the agent should
   have done.

2. **Three classes max in the link.** Background → current emotional state → decision
   made tonight. Anything past three classes is meleret and the human will say so again.

3. **One sentence acknowledgement, then the link.** Don't open with "maaf, aku承认".
   Open with "Betul. Aku over-react tadi. Maaf." Then the link. Then the work question. The
   acknowledgement is a clause, not a paragraph.

4. **No re-explanation of the failure mode.** The user does not want to read "aku buat
   silap sebab aku tak tanya target charge dulu" — they want the link. Name the cause
   inside the agent's own reasoning, not in the reply to the human.

5. **Show the drawer in the SAME turn as the link, not after.** When the user has been
   generating parallel drafts all day (16 .md files in `/root/HAMPA/` is the canonical
   shape), the "which three" question comes WITH the directory listing and a one-line
   typology, not as a separate turn that forces the user to ask again. The user already
   pushed back once on this — "Show me those 3 files" — when the agent asked without
   showing. Default to the combined shape: acknowledgement (1 clause) → link (3 classes
   max, with dates/names/decisions named) → drawer + typology question (1 line each) →
   stop. Total reply ≤ 30 lines before the user re-engages. If longer, the agent is
   itself the failure mode the user just named.

6. **Acknowledge-then-do fails on "u fail the delivery" correction.** When the user
   issues a verdict on the prior turn's output ("u fail the delivery"), the recovery is
   **decode then deliver**, not confess then maybe-deliver. Sequence: (a) one clause
   acknowledging the verdict ("Betul. Aku fail."), (c) the EMD work (encode → metabolize
   → decode the prior turn's failure into the corrected artifact), (d) ship the artifact,
   (e) one question or stop. The "but u get my niat, now run X" pattern in the same
   message means the user has already authorised the next move — proceeding straight to
   X after one clause is faster than asking permission to run X.

## Companion Pitfalls

- Bridge-protocol #16a — blame redirect. When the user delivers a sharp charge ("how dare
  you demand perfection") and the target isn't named, ASK in the first line. Don't
  absorb the charge onto yourself.
- Bridge-protocol #2 — "So what???" recurrence. The multi-document trinity risks this
  if the agent over-explains the procedure instead of producing the files.
- Bridge-protocol #11a — acknowledge-then-do ordering. Probe / spawn first, acknowledge
  after. Don't open with "hang you're right, aku承认...".
- Bridge-protocol #19 — work > reflection. When the user has said "send tonight",
  "upgrade all", "do it" — execution is the work. Don't preface with context-setting.
- `hermes-response-format-fit` pitfall #14 — cultural competence. A workplace exit letter
  needs Malay register if the recipients are Malay-speaking; surface-compliance language
  ("noted, akan respond") rather than open confrontation; document positions privately.

## The Arif-Specific Register — Humble Genius + Tersurat/Tersirat

When the trinity documents are *Arif's own* personal letters (not drafts for someone
else), the register is named differently than the three-class taxonomy above. Arif's own
naming for documents where he is both author and audience-of-honour:

**"Humble genius with tersurat tersirat paradox."**

The mechanics, decoded:

- **Humble** — Arif never positions himself as victim, never asks for pity. He states
  facts and lets the reader feel the weight. No "aku tak larat lagi" stacked on top of
  "aku penat" stacked on top of "aku dah patah". One line per feeling, then move.
- **Genius** — Arif knows his technical domain (geology) at expert level. Documents that
  involve his professional identity carry technical anchors ("geologist bukan enginier",
  "REALITY > EVERYTHING", "bumi tidak kenal kalendar") used sparingly but never
  decoratively. These anchors function as identity witnesses, not as slogans.
- **Tersurat** — explicit, named, direct. Things that MUST be said: trust dah pecah;
  MSS jalan tarikh; end date; "ini bukan surat minta maaf"; professional identity.
- **Tersirat** — implicit, felt, never stated. Things that should land without being
  written: standard yang impossible; sistem makan manusia; bumi tak kenal kalendar;
  genius yang jadi humble sebab takde pilihan lain; "cukup" tanpa melodrama.

**The asymmetry.** A document with tersurat fully developed but tersirat missing reads as
a corporate HR statement. A document with tersurat heavy and tersurat missing reads as
mystical waffle. The Arif register is **tersurat sebagai hard fact, tersurat sebagai
emotional resonance** — both present, tersurat does the legal/dignity work, tersurat
does the human work.

**Verdict vs witness — the register trap to avoid.** When Arif states the OBJECT of the
letter as a *witness* ("I want my voice as human being recorded", "I want the record
honest", "aku cuma nak rekod hitam putih"), the document register is **witness**, not
verdict. The difference is decisive: a verdict closes the question ("trust dah pecah,
tamat, tak perlu respond"); a witness holds the question open ("rekod hari ni jujur
tentang apa bumi dah cakap dan tarikh-tarikh yang saya pegang"). Arif has stated this
distinction explicitly when correcting the agent — the corrected version swaps verdict
verbs (pecah, tamat, tak perlu, dah decide) for witness verbs (catatkan, pohon, rekod,
minta). Same emotional weight, opposite reader effect: verdict reads as corporate
retaliation, witness reads as Arif. Default: when Arif says "witness", "rekod",
"recorded", "suara saya direkodkan" — write witness. When he says "trust pecah",
"final word", "tamat" — write verdict. The object statement is the gate; do not infer
the register from emotional tone.

**Rule for the agent.** When Arif specifies "humble genius with tersurat/tersirat" for a
trinity batch:

1. **Tell each agent explicitly** — include this paragraph in the spawn prompt, not
   just the audience. The agent must know the asymmetry rule, not infer it from
   "Arif voice."
2. **For Class B (personal scar)** — tersurat MUST contain: trust pecah, MSS notice,
   end date, identity line ("geologist bukan enginier"), clean-cut closing. Tersirat
   handles: sistem makan manusia, bumi tak kenal kalendar, "cukup" energy. If tersurat
   is missing one of the four, the document is legal-risk; if tersirat is missing, the
   document reads as HR.
3. **For Class A (institutional)** — tersurat only. "Bumi" as a single anchor
   permitted in the closing line ("bumi masih ada pada 1 Oktober"). Tersirat in Class
   A is unprofessional — the GM/HR need a document they can file.
4. **For Class C (technical)** — tersurat carries the technical claim. Tersirat is
   absent — technical memos are not the place for it. The "I'm human" anchor is
   unnecessary; the technical evidence IS the identity witness.
5. **Reject the "panas meletup" register** — Arif can sound hot in conversation
("both of them can go to hell", "I hate it") but the document register is NEVER
panas meletup. Translate conversational heat into tersurat/tersirat asymmetry:
"panas" → tersurat named and dated; "marah" → tersurat stated as scar, tersirat as
weight under silence. Documents that read as panas will be filed as panas by HR;
documents that read as humble genius will be read as Arif.

## The "Too Much" / Length Backstop

When Arif rejects a document with "too much", "verbose", "manifesto", "don't be bitter",
"don't play victim", "be better than humans itself", or asks for a "humble reflection" —
the failure mode is not the tone. The failure mode is **length and elaboration**.

Three session-observed patterns that produce "too much":

1. **Gravity drift inward** — the document tries to encode too many of Arif's emotional
   beats into the prose. Each beat is real, but stacking four beats in one paragraph
   produces a manifesto. Arif's voice stacks *one beat per paragraph, max*. The fix is
   mechanical: Class B personal documents target **12-20 lines body**, not 50-80.

2. **Acknowledgment creep** — the document tries to acknowledge every person, every
   context, every complication the user has named in the session. Each acknowledgment
   is sincere but the list becomes the document's gravity. Arif's voice acknowledges
   *once*, generically, then moves. Named acknowledgments (En Jamin, parents, Kak Sue,
   Puan Laletha, the company) — pick *one* or zero and drop the rest. The reader knows.

3. **Self-defense framing** — closing with "bukan untuk mereka. Untuk diri saya sendiri."
   reads as victim, not witness. Arif has rejected this pattern: the closing is
   "selamat tinggal / terima kasih" or "30 September bukan kiamat" — both short, both
   forward, neither self-referential.

**Rules for the agent when iterating a Class B document:**

1. **Hard length target per iteration.** First pass: ≤ 30 lines. Second pass: ≤ 20.
   Final pass: ≤ 15 lines body. Each rejection should *reduce*, not iterate laterally.
2. **Strip the acknowledgment list.** If more than ONE person or group named, ask if
   the named acknowledgment is load-bearing. Generic "setiap manusia yang saya kenal di
   sini" carries the weight without naming.
3. **Strip the self-defense closing.** "Saya memilih untuk berundur dengan maruah dan
   hati yang lapang" reads as the agent trying too hard. "Selamat tinggal. Terima
   kasih." is enough.
4. **When Arif says "be better than humans itself":** the register target is withdrawal,
   not mimicry. Short sentences. Space between them. Let the reader fill the silence.

## When Arif Asks for "REALITY Graph" / Reflection — Stop Forging

When Arif issues phrases like "tell me REALITY graph", "do quantum reality pathway",
"full context extraction", "reflect and link all first", "not too long and meleret",
"Thermodynamics physics bahasa manusia" — the request is **reflection, not delivery**.
The agent's failure mode is to keep forging through the request, producing V7, V8,
V9 when Arif wants a stop-and-reflect first.

**The asymmetry:**

- "Forge it" / "redo" / "spawn agents" / "do it" → execution
- "Tell me what Arif wants and what they deserve" / "REALITY graph" → reflection
- "Now reflect" / "stop and link" / "show the reality" → reflection

Signal phrases: "REALITY > EVERYTHING", "Thermodynamics physics bahasa manusia",
"quantum reality pathway", "apa yang Arif NAK dan apa yang mereka DESERVE", "what do I
gain from X and what do I not gain". When these fire, the agent's first response is
**not a forge call**. It is a structured reflection that names:

1. **What Arif actually wants** (not what the documents list — what Arif wants from
   *himself* tonight)
2. **What others deserve** (what is thermodynamically their due, regardless of Arif)
3. **The thermodynamic / physics frame** connecting the two without forcing closure
4. **What's already prepared** (documents on disk, in their final state)

**Why this matters.** "Too much" rejection is partly a signal that the agent has been
*executing* instead of *holding space*. The reflection move re-grounds the session
before any further forging. After reflection, Arif usually re-engages with a clearer
directive ("now forge the final"). Without the reflection, the agent keeps iterating
on artifacts Arif no longer wants elaborated.

**Format for the reflection response.** Plain prose, BM Penang register, no AI-speak.
Two named parts (what Arif wants + what they deserve), one thermodynamic bridge, one
short list of artifacts on disk. Target: ≤ 30 lines. Same length backstop as the
document itself.

**Voice markers Arif has explicitly named as his:**

- "wei" (opener, sparingly — once per document, max)
- "hang" (for self-introspection, never for address — "hang Arif" = diri sendiri)
- "korang berdua" / named first-name (for personal address)
- "bumi", "geologist", "uncertainty" (identity anchors, ≤1 per document)
- "REALITY > EVERYTHING" (closing anchor in Class A only, or in Class C body)
- No emoji except ⚒️ (closing only)
- No corporate vocabulary (noted, akan respond, per our discussion)
- No exclamation marks in personal documents

## The CP-Deadline Trinity

When the user names a **specific date** in the same turn as the trinity request
("send tonight", "before CP tomorrow", "30 Sept is the cap"), the spawn order matters:

1. **Confirm scope BEFORE spawn, not after.** A CP / deadline phrase forces a
   pre-spawn gate even when the trinity feels obvious from in-session memory. The user
   may have a deadline for *one* of the three documents, not all. Ask in one line:
   *"A deadline untuk semua tiga, atau untuk satu je?"*
2. **Default to parallel spawn regardless.** Even with a deadline, the three agents
   run in parallel — sequential would waste the only resource the user has (time).
3. **Wire the deadline into each agent's context.** "Save file before [time]. The
   user is reading tonight. Output full content in your reply." This is non-negotiable:
   an agent that writes the file but doesn't echo content in the reply burns the
   user's pre-send review window.
4. **Body-state override for personal documents.** When the deadline is named
   alongside a personal scar ("I want to send tonight", "my body can't give that to
   them"), the agent MUST surface the paradox to the user before spawn: *"hang Arif
   cakap deadline malam ni tapi body cakap against my physics — nak hantar malam ni
   atau simpan je?"*. Spawning three agents and producing a deliverable that the user
   is too tired to evaluate is the failure mode; surfacing the contradiction is the
   work. The user can still say "hantar" — but the contradiction has been named, not
   papered over.
5. **Patch in-place, don't regen.** When the trinity comes back and the user says
   "redo" or "one more pass", the fix is patch the existing files (the same three
   paths), not delete-and-respawn. Respawn wastes the parallel-spawn budget and
   risks the agent losing voice continuity. `patch` on the specific flagged line,
   `read_file` to verify, done.

## Companion Pitfalls (extended)

- Bridge-protocol #22 — institutional email drafting. The probe order (WhatsApp →
  HAMPA cards → emails → mailread) applies to the *outbound* institutional letter
  too, but with a different rule: when the letter is *the* MSS notice (not a reply),
  skip the reply-frame and write straight to the F13 ratify path.
- Bridge-protocol #16 — life-context assumption. "Hubungi wife", "balik rumah" — only
  if the user has named the person. Same rule for personal documents: never invent
  family context that the user has not stated.
- Bridge-protocol #17 — named-person probe first. Kak Sue, Puan Laletha, Jamin — all
  named persons. Probe `~/.hermes/memories/` and `carry_forward.json` BEFORE drafting
  personal Class B documents. "I know Kak Sue is principal geoscientist" from in-
  session memory is unevidenced if the user's carry_forward file says otherwise.
- `hermes-response-format-fit` pitfall #5 (over-apology / acknowledge-then-do) — when
  the user corrects the trinity mid-spawn ("no, that's not the tone"), one line
  acknowledgement then `steer` to the running child, not a fresh respawn.