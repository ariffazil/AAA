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
- **Don't use the future-self device if the person is in acute crisis.** It requires a baseline of hope to land. In acute distress, the present-tense letter alone is enough.
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
