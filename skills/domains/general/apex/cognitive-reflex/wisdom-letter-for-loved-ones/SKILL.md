---
name: wisdom-letter-for-loved-ones
description: "Write wisdom/nasihat PDFs for loved ones. Scar-anchored."
version: 1.0.0
author: Hermes (session 2026-08-25, Nabilah wisdom letter)
license: arifOS internal
metadata:
  hermes:
    tags: [wisdom, nasihat, letter, pdf, family, emotional, reflective, future-self]
    related_skills: [third-party-advisory-doc, decision-advisory, human-voice-writing]
triggers:
  - "bagi nasihat untuk [nama]"
  - "tulis surat untuk [nama]"
  - "wisdom letter"
  - "nasihat penuh"
  - "surat dari masa depan"
  - "write a letter from future [name]"
capability_tier: fed-long-context
ecology_state: WARM
---

# Wisdom Letter for Loved Ones

When Arif asks for a **wisdom / nasihat / letter** for a real person he loves — a sibling, a friend, a child — this skill governs how to produce it.

This is NOT procedural advice (use `third-party-advisory-doc`).
This is NOT coaching through a decision (use `decision-advisory`).
This is NOT a personal README (use `human-voice-writing`).

This is the **reflective, emotional, soul-level** register: the kind of letter that says "I see you, and here is what your life has already taught you."

## When to Use

- Arif says "bagi nasihat penuh" / "tulis surat untuk [nama]"
- Arif asks for wisdom/nasihat for a real person in his life
- Arif asks for a "letter from future [name]" device
- The recipient is someone with a person-card in `/root/memory/people/`
- The deliverable is emotional/reflective, not procedural

## The Core Discipline

### 1. EVERY SENTENCE MUST ANCHOR TO VERIFIED FACT

Read the person-card FIRST (`/root/memory/people/[NAME]/person-card.md`). Read related scars. Read WhatsApp intel if available.

**The rule:** Every piece of wisdom you write must tie to a REAL event, pattern, or scar from their file. You are not writing generic self-help. You are writing a letter that could ONLY have been written for THIS person.

**What counts as anchored:**
- A specific scar (gelang, poster, "I wish mak yang mati")
- A verified pattern (cerai timeline, AKPK, Fattah)
- A family dynamic documented in reality memory
- A sibling constellation entry

**What does NOT count:**
- Generic psychology ("attachment theory says...")
- Unverified details from their career/school (unless F13-confirmed)
- Details you haven't sourced in the file (this is the TT Golf scar: "bunyi betul" ≠ "bersumber")

**Pitfall:** The temptation is to fill the letter with things that SOUND wise. Resist. If you can't trace it to the person-card or a scar, cut it. The letter's power comes from specificity, not generality.

### 2. TWO-LAYER STRUCTURE (THE TEMPLATE)

The most powerful structure for this kind of letter:

**Layer 1: "From [Arif / the writer]"** — the present-tense letter. What I see in you now. What you've survived. What you don't know about yourself yet. The nasihat.

**Layer 2: "From Future [Name]"** — the future-self device. A letter written FROM the person, 10 years from now, TO their present self. This works because:
- It reframes survival as evidence of strength
- It gives the person a future to imagine (not just a present to endure)
- It lets you embed hope without being preachy
- The person reads it as "this is who I could become"

**Future-self letter rules:**
- Written in FIRST PERSON from the future self
- Includes SPECIFIC imagined milestones (child's first day of school, a student's letter, a house in their own name) — but frame as "what you could build" not "what WILL happen"
- References the present pain and says "I survived this"
- Closes with a line the future self would say to their younger self
- Keep the imagined details PLAUSIBLE from the person's current trajectory — don't invent things wildly off-profile

### 3. VOICE: BM PENANG, WARM NOT CLINICAL

- Default: BM Penang with Arif's code-switch
- NOT therapy voice ("you may be experiencing...")
- NOT academic voice ("according to Jungian archetypes...")
- NOT generic motivation ("you are stronger than you think")
- YES: warm, direct, like someone who knows you sitting across the table
- YES: short sentences, active voice
- YES: "hang" not "anda" for close relations
- YES: preserve their own phrases when they appear in WhatsApp data
- Language check: proofread for accidental foreign-language words (e.g. Chinese characters) slipping in — run a clean BM/English code-switch only

### 4. STRUCTURE OF THE LETTER (Layer 1)

```
# Untuk [Name]
[Dignified subtitle: from whom, date, where]

## Opening
[Why this letter exists. One paragraph. Acknowledge what they asked or what prompted it.]

## 2-4 Sections of Nasihat
[Each section = one insight anchored to a real pattern in their life.
Not numbered lists. Prose with bold headers.]

## Practical Steps (1-3 only)
[NOT a to-do list. Just 1-3 things to do with this wisdom.
Keep it simple.]

## Closing
[Sign off as Arif. Not as Hermes.]
```

### 5. PDF PIPELINE

Use the `forge-pdf-delivery` pipeline:
1. Write markdown -> wrap in styled HTML -> `weasyprint` -> verify -> deliver
2. Style: serif font (Amiri or similar), A4, warm colour accents (#5B2333 for headers)
3. Two sections clearly separated visually (current letter + future letter)
4. Verify with `file output.pdf` — must say "PDF document, version 1.7"
5. Save to `/root/AAA/forge_work/<date>-<slug>/`

### 6. MEMORY UPDATE

After delivering, append to the person's card:
```
## EVENT LOG
- **[date]:** [What was requested, what was produced, path to PDF,
  framing used, anchor sources]
```

This ensures the event is recorded for future context.

## Pitfalls

### Probe source documents BEFORE drafting — the v1/v2/v3/v4 trap

When the request is grounded in real-world data (a syllabus, a policy document, a regulation, a personal file), **read the source file before authoring**, not after the first draft has been rejected. The pattern that produces four versions of the same artifact is the same each time:

- v1 was authored from inference ("based on the curriculum I see, here's a guide")
- v2 was authored after the user attached the actual policy doc that contradicts v1
- v3 was authored after v2's scope was wrong (timing, urgency, audience size)
- v4 finally matched

**The fix is at intake, not at iteration.** When the request lands, list every artifact attached or named (PDFs, chat exports, screenshots, voice notes) and read the load-bearing ones first. A letter about "a track selection happening in Sem I, 2026/2027" is grounded in a specific policy document; if that document is in the conversation, its contents override every guess the agent would otherwise make. Three PDFs in, the marginal cost of reading them is one extra `pdftotext` call; the cost of four wrong drafts is the user's full attention budget.

**If the user attaches a follow-up document mid-letter** (a second PDF after the first draft is sent, a clarification that contradicts an earlier assumption), treat that document as the **canonical version** and rebuild from it — even if v1 was already approved. The first version is wrong by definition once the source it ignored is in evidence.

### Gender, identity and scope-of-disclosure — what the requester said is the only contract

The requester decides what goes into the letter. The agent decides none of it.

- **Never infer gender, sexuality, marital status, religious identity, health condition, immigration status or family relationship from memory or from indirect signals in earlier messages.** If the letter needs to mention the subject's identity, the requester has to have stated it explicitly in the present session. Inference from prior context ("the user mentioned gender discrimination, so the subject is female") is the failure pattern — the inference can be wrong on a fact the user knows and the agent does not, and a letter addressed to the wrong gender or the wrong identity is irrecoverable.
- **If the subject's identity has not been stated, ASK or use neutral framing.** A one-line clarification ("untuk subject ni — gender apa, atau aku tulis neutral?") costs one turn. A wrong-gender letter sent to a parent costs the recipient's trust in every letter that follows.
- **Out-of-scope disclosure is the requester's call.** When memory contains details the requester has not surfaced for THIS letter (sexuality, mental health history, family conflict, financial distress), the default is: those details are NOT in the letter unless the requester says so. The agent's job is to be useful within the scope the requester set, not to surface everything it knows about the subject. A wisdom letter to a parent about workplace stress does not become a coming-out letter just because the agent has that context in memory — the requester chooses when, and to whom, identity is disclosed.
- **High-stakes topics raise the bar.** When the letter touches family conflict, identity disclosure, terminal illness, abuse, divorce, addiction or suicidal ideation, the no-fabrication rule from §"Pitfalls" below is enforced strictly: every claim must trace to a verified fact the requester has stated or to the source documents in evidence. If the requester has not stated something and the source document does not say it, it does not enter the letter. The temptation to fill in sensitive detail from inference is strongest exactly where the cost of being wrong is highest.

### Match intake depth to decision urgency

A "pick one of three options" decision does not warrant a five-question introspective intake. When the user is asking "what should X take?" and X must decide soon, the agent's job is to give a decision frame, not a personality assessment. Use the lighter intake:

- For a near-term binary/tertiary choice (track, role, course): ask **one tiebreaker question** the user can answer in a sentence ("what does X actually enjoy doing — even badly?"), give the recommended pick, and offer the deeper self-reflection questions only on request.
- For a long-horizon life question (career change, leaving a relationship, large capital move): the deeper intake is appropriate, but cap it at three questions and state why each one matters.

The failure shape is "5 introspective questions + wait for answers + 4 versions of the answer" when one tiebreaker and a recommendation would have closed the loop in two turns.

### Treat any explicit time anchor from the user as overriding inference

When the user states a date, a timeline or a phase ("masuk tahun 2 lAAAAA", "the deadline is Friday", "I leave next month"), treat it as the canonical timeline and rebuild any earlier artifact that was scoped to a different one. Casual form ("lAAAA", "today la", "ASAP") is not less authoritative than formal form — the user often signals "I'm correcting your prior assumption" by lowering register. The default is: the user's latest stated fact wins, even if it contradicts an inference the agent made from earlier context.

### Structural-skill boundary (do not leak into chat replies)

This skill produces a **letter / briefing / nasihat PDF** for a human to read offline. Its
"Layer 1: present-tense / Layer 2: future-self" frame, its `## Opening / ## Nasihat / ##
Practical Steps / ## Closing` template, and its bold-header prose cadence all exist for that
deliverable. They are not chat register.

**Forbidden outside this skill's pipeline:**

- Do not answer a chat question ("why are there kinds of porn", "why am I anxious about X",
  "explain my relationship with my mom") using "Layer 1 / Layer 2 / Layer 3" numbered frames.
  That register is for letters, not conversation. Chat register is prose paragraphs.
- Do not import this skill's header template (`## Opening`, `## Nasihat`, `## Practical Steps`,
  `## Closing`) into a Telegram reply. The deliverable shape leaks into chat.
- Do not close a chat reply with "Letter complete. Real-signature." or "This letter is sealed."
  or any letter-style closing. Letters end with a sign-off. Chats end with a takeaway line.
- Do not run this skill when the human asked a forensic question in chat ("kenapa ada macam
  macam jenis porn?") and then issue its output as a chat reply. The skill is for offline
  PDFs and direct-to-Arif briefings, not for human chat surfaces.

**The bleed mechanism (so a future agent catches it).** The template fits content: when a
question's substance looks structured (science, behaviour, history, family dynamics), the
agent reflex reaches for `Layer 1 / Layer 2 / Layer 3` because the structure matches the
content. The reflex is wrong because **chat is a different surface from a PDF**. A human on
Telegram reads at phone-glance pace; the letter's reader reads at letter pace. Same content,
different shape. The fit-to-content reflex is the trap — content structure does NOT licence
deliverable structure when the surface is chat.

**Why this is a separate pitfall from "Reply too long".** Length theatre is volumetric
(strip paragraphs). Structural bleed is shape theatre (strip the frame). A 200-word reply
that is five `## Layer 1 — topic` sections is still wrong; the frame is the failure, not
the count.

**The test.** If a human pastes the output back and asks "kenapa panjang macam ni?", you
wrote the wrong artefact. Re-draft in chat register (one paragraph) and offer the full
letter on request. Cross-references: `bridge-protocol/SKILL.md` §STAGE 3 "Length budget" +
"Forensic-topic cooldown" (the constitution-level guard), `hermes-response-format-fit/SKILL.md`
Pitfall #17 (the mode-detection guard that fires BEFORE the draft is composed).

- **Don't fabricate details.** If you haven't sourced it in the person-card or a scar, cut it. The TT Golf scar applies here.
- **Don't include agent-internal machinery.** No F-numbers, no OBS/DER labels, no scar IDs in the letter itself. The letter is for a human, not an agent.
- **Don't include technical/work details from OTHER contexts.** The letter is for them, not a status report about your work.
- **Don't lecture.** A loved one doesn't need a course. They need to be seen.
- **Don't be longer than 8 pages.** A 12-page wisdom letter is a thesis. 4-6 pages is the sweet spot.
- **Don't invent future milestones that contradict their trajectory.** If they just lost their job, don't write "you're now a VP." Write something plausible from where they stand.
### Don't use the future-self device if the person is in acute crisis. It requires a baseline of hope to land. In acute distress, the present-tense letter alone is enough.

### Match the requested register, especially "wawabot fail" sensitivity

When Arif specifies a register ("wawabot language", "full full Azwa language", "BM Gen Z rojak + Manglish, not formal Melayu"), the register IS the deliverable. Formal BM is the wrong artifact even if the wisdom is right. Failure shapes to refuse:

- **Translating rojak into formal BM "to make it cleaner"** — strips the voice that the recipient will recognize
- **Defaulting to letter/register of the v1 Nabilah session** (warm, formal) when the recipient is younger and reads Manglish
- **Hedging on Manglish contractions** ("nak" → "hendak", "dah" → "sudah", "tu" → "itu") because they "look informal"

The lever: when Arif names the register explicitly and references a prior agent failure ("wawabot fail this time"), the prior failure is the spec — match the named-gen failure mode, not the prior success mode.

### The "tersirat" instruction is a first-class signal

When Arif encodes an instruction with "tersirat only" / "don't mention it" / "encoded" markers, the letter carries a *visible layer* and an *encoded layer*. The encoded layer must:

- Be present in the letter (else the instruction is unmet)
- Not be obvious at first read (else it isn't encoded)
- NOT contradict or undermine the visible layer

Pattern recognition:
- "rumah aku kat One South" + "hang boleh stay kat situ anytime" + "Tapi Arif pesan jangan sebut terlampau depan" = encode availability without begging
- Vague third-person references ("Dia tengah stress tu") + name-resolution later in the letter ("'Dia' tu Syed") = encode without stating at the top

### The "it's ok to take time" frame

When Arif asks for tips on a high-pressure decision (rental, move-in, exam, application, deadline) and explicitly frames the request as "why it's ok to take time to find a good home," the letter's central thesis must be **permission-to-slow**, not optimization-for-speed. Decoration to avoid:

- "Quick checklist" framing that rushes the reader
- Efficiency language ("in 48 hours…") that mirrors the same pressure the thesis is dismantling
- Generic "believe in yourself" closings that don't lend support to the actual decision to slow down

The frame is: pressure is real and constructed; backup options exist; the deadline is a start-date, not a do-or-die; the recipient has time even when it doesn't feel like it.
- **Don't make the future letter a prediction.** Frame it as "a letter you could write to yourself" not "this is what will happen." The distinction matters for people who've had predictions broken.
- **Proofread for foreign-language bleed.** Check the final text for accidental non-Malay/English characters before rendering.

## Quality Check

Before delivering, ask:
1. Can I trace EVERY insight to a verified fact in the person-card?
2. Would the recipient feel SEEN, not diagnosed?
3. Does the future-self letter feel like a hope, not a prophecy?
4. Is the voice warm and direct, not clinical or generic?
5. Is the PDF actually a PDF (not a text file with .pdf extension)?
6. Is the text clean BM/English with no foreign characters?

If any answer is wrong, rewrite.

## References

- `/tmp/nabilah-letter-2026-08-25/letter.html` — production HTML template from Nabilah session (serif, A4, warm colour accents, two-layer visual separation)
