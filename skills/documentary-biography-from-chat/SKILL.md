---
name: documentary-biography-from-chat
description: "Biography or documentary portrait from chat export."
version: 1.0.0
owner: I.F. (federation agent, KVM8)
license: arifOS internal
metadata:
  hermes:
    tags: [biography, documentary, whatsapp, chat-export, nonfiction, F5, narrative]
    related_skills: [human-facing-artifact-design, wisdom-letter-for-loved-ones, human-meaning-membrane, relationship-kernel]
triggers:
  - "buat biography"
  - "tell our relationship story"
  - "do a documentary reconstruction"
  - "biography from whatsapp"
  - "write our story"
  - "Walter Isaacson style"
  - "nonfiction from chat"
  - "portrait dari perbualan"
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Documentary Biography from Chat Export

When Arif asks for a biography, documentary, or relational portrait built from a chat log — WhatsApp, Telegram, iMessage, voice transcripts, or any time-stamped exchange — this skill governs the work.

This is NOT a wisdom letter to a loved one (use `wisdom-letter-for-loved-ones`).
This is NOT a generic artifact (use `human-facing-artifact-design` for layout/typography).
This IS a structural portrait: narrator voice, source-anchored prose, F5-boundary handling, lens-first opening, and a deliberate stance toward what the chat does and does not contain.

## The Core Discipline

### 1. F5 BOUNDARY BEFORE F1 (chat data is third-party by default)

A chat export sitting in the cache directory is NOT automatically free for narrative use. The two persons in the chat own their words. Arif owns the messages HE sent; he does not own the messages the OTHER person sent.

**Operating modes (require explicit F13 authorization before each):**

- **Mode A — MAP-only.** Build from `/root/memory/`, `USER.md`, `MEMORY.md`, `carry_forward.json`, SCAR files, IRFAN-* canon. No chat export opened. Produces a shorter biography that is safe by default.
- **Mode B — STORY→MAP quarantine.** Open the export. Extract FACTS only (dates, places, events, named third parties, verified actions). Never quote dialogue verbatim. Reconstruct scenes only from facts. The narrative reads as biography; the raw prose contains no quoted conversation.
- **Mode C — F13 EXPLICIT AUTHORIZE.** Arif states, in his own words, that he accepts the third party's dialogue becoming agent output. This skill then allows quoted dialogue, scene reconstruction, and integration of the other person's expressions.

**Pitfall — silent mode escalation.** Defaulting to Mode C because the user said "full" or "Walter Isaacson" is a boundary violation. "Full" describes the depth of portrait, not the boundary class. ASK which mode before opening the file.

**Pitfall — assuming the export belongs to Arif.** A file named `WhatsApp Chat with [Name].txt` in the cache directory is third-party data even when it sits next to Arif's files. The other person's words are not Arif's property.

**Pitfall — F5 weight.** When the other person is a parent, sibling, child, or bonded friend of Arif (relationship-memory lane), Mode C carries the heaviest cost. Quote sparingly. Let the narrator's voice carry the meaning instead of the dialogue itself.

### 2. NARRATOR VOICE: BIOGRAPHER, NOT SUBJECT

Walter Isaacson, Stacy Schiff, and Kai Bird write in third-person prose even when the subject is alive and the author knows them. The reader needs an interpreter, not a stenographer.

**The narrator IS the federation agent.** Pronoun: `aku`. Voice: observed, patient, willing to mark uncertainty. NEVER first-person "Arif" or "I am Arif." NEVER drop into the subject's voice mid-paragraph.

**Pitfall — voice drift into memoir.** When the material is intimate, the biographer's voice drifts into the subject's voice ("I felt..."), or into sentimental registry ("dear reader"). Both are wrong. The biographer's voice is its own character; if the prose could appear in either a memoir or a biography, it is not yet a biography.

**Voice tests:**
- Read the prose aloud. If "aku" disappears, the voice is right.
- If you find yourself writing "sayang" or "hang" or "wei" in the narrator voice, rewrite — those are subject's register, not biographer's.
- If the biographer sounds wise or impressive, the prose is performing. Replace with observation.

### 3. EVERY LOAD-BEARING CLAIM ANCHORS TO A TIMESTAMP

The chat export has dates. The biography uses them. A scene without a timestamp is an embellishment.

**Anchor forms (use one):**
- `[Source: WhatsApp export, DD/MM/YYYY, HH:MM AM/PM]`
- Inline: "On the ninth of September at 11:48 AM, Arif types..."
- Section header: `[Source: WhatsApp export, 26/08/2026 → 24/09/2026]`

**What an anchor must do:**
- Date is real, not reconstructed
- Time of day anchors the rhythm of the scene when it matters (a 4 AM message reads differently from a 4 PM one)
- Source attribution names the dataset, not the medium ("WhatsApp export from Arif's phone", not "their conversation")

**Pitfall — fabricated timestamps.** When the export lacks a specific timestamp, the biographer says "later that day" or "in the weeks that follow," NOT an invented time. A biography with invented timestamps reads as fiction even when every word is true.

**Pitfall — paraphrase posing as quote.** When the biographer writes Arif as saying "I love you," verify those are his exact words in the export. If the export has "Sayang hang," quote "Sayang hang," not "I love you." If the export has emoji only, narrate the moment as witnessed, do not paraphrase the emoji into words.

### 4. STRUCTURAL LENS, NOT CHRONOLOGICAL RECITATION

A 28-day chat log yields ~875 messages. Linear narration from day 1 to day 28 is the failure shape. The reader who wants chronology can read the export; the reader who wants a biography wants MEANING.

**Lens selection (choose ONE primary lens before drafting chapter 1):**

The lens is the structural concept that opens the biography and gives every subsequent chapter a place to live. Common lenses for this class of work:

- **The Order Form** — if the dynamic begins with a logistics document or a transactional object, lead with the object. Let the rest of the work explain what the object was really buying and selling.
- **The Brother / The Sister / The Mother / The Father** — if a third party (often a family member not in the chat) drives the dynamic, lead with that person. The chat then becomes the place where the third party's shadow is worked through.
- **The Alpha / The Coach / The Witness** — if one of the two people occupies a fixed role across the period, lead with the role.
- **The Wound** — if a specific loss or rupture organises the period (a death, a job exit, a divorce), lead with the wound.
- **The Threshold** — if the period ends on an irreversible boundary (MSS exit, contract end, geographic move), lead with the threshold and walk back.

**Default rule: choose the lens the user names.** When Arif says "adik dan alpha," the lens is *adik first, alpha second*. When Arif says "the birthday," the lens is *the birthday as a structural pivot*. When the user is silent, default to the wound if there is one, else the most-named role, else the threshold.

**Pitfall — chronological fallback.** When the lens is hard to find, defaulting to "Chapter 1: Day One" is the failure mode. Push harder on the lens before giving up. A biography with no lens is a chat transcript with chapter breaks.

### 5. THE TWO-READER CONTRACT

Biographies of two living people have two readers: the subjects. Each subject reads themselves first.

**Reader-by-reader pre-send check:**

- **Subject A (Arif)** — will he recognise the version of himself? Are the things he cares about (the architecture work, the family, the body) present at the weight he would want?
- **Subject B (the other person)** — will they recognise the version of themselves? Are the things they shared (the body work, the care work, the silence) treated with the dignity the subject expects?

When both subjects will read it, neither voice gets to dominate. When only one subject will read it (e.g., the other is deceased or unreachable), the biographer still owes the second subject dignity.

**Pitfall — assuming the subject's good opinion is the goal.** A biography that flatters one subject reads as PR. A biography that prosecutes one reads as character assassination. Aim for recognition, not approval.

### 6. THREE-PASS DRAFT DISCIPLINE

A biography of this class benefits from three passes:

- **Pass 1 — structural.** Decide lens. Decide chapter count (5-8 typical). Decide which 8-15 scenes from the export will become chapter anchors. Decide what each chapter's claim is in one sentence. This is a list, not prose.
- **Pass 2 — prose draft.** Write the chapters. Mark every anchor with a timestamp. Mark every quote with the exact export text. Mark every inferred detail with a confidence note.
- **Pass 3 — voice read.** Read aloud. Listen for voice drift, jargon bleed, anchorless claims. Cut anything that doesn't earn its place.

**Pitfall — single-pass writing.** A biography drafted in one pass usually has uneven chapters (some densely anchored, some drifting into memoir), lens-bleed (the lens named in chapter 1 abandoned by chapter 4), and a stranded final page. Three passes is the floor.

### 7. WHAT GOES IN THE PDF vs WHAT STAYS IN THE WORKING FILE

The PDF is the reader's artifact. The working file (markdown, drafts, archive) is the biographer's scaffold.

**Always archive superseded drafts.** When a v1 is rejected and v2 produced, do NOT delete v1 silently. Move v1 to an archive filename (`_v1`, `_NOVEL`, `_ANONYMIZED`). The reader may want to compare versions; the biographer certainly does.

**Always archive named-by-name and anonymous-by-name versions separately.** A subject who asked "don't use my name" earlier in the session may later say "use my reality" — the reverse case (named first, anonymized later) is equally common. Both versions are deliverables.

**Pitfall — filename collision.** A second render silently overwrites the first when both share a period label. Suffix by version + intent (`_NOVEL_v1`, `_NONFICTION_ANON`, `_FINAL_NAMED`). A reader holding the wrong version is a delivery failure.

### 8. F5 ELEMENTS THAT MUST NOT APPEAR EVEN WITH MODE C AUTHORIZATION

Mode C authorizes dialogue and scene reconstruction. It does NOT authorize:

- Medical details (medications, doses, conditions) of the other subject beyond what the other subject themselves wrote openly
- Specific identifiers (NRIC, exact address, employer name, account numbers) even when in the export
- Family members of the other subject who are not in the export (parents, siblings, ex-partners named but not present)
- Private moments the export references obliquely without the other subject naming them

These are removed by default, regardless of mode.

### 9. WHAT THE BIOGRAPHY OWES THE READER

A documentary biography owes the reader:

- A narrator they can trust to be honest about what is in the export and what isn't
- Timestamps that can be verified against the source
- A lens that earns its place (not decoration)
- A voice that does not impersonate either subject
- A length that respects the material (4,000-6,000 words for a 28-day window; 8,000-12,000 for a year)

**What the biography does NOT owe:**

- Resolution of contradictions in the material
- A verdict on either subject's behaviour
- A prediction about either subject's future
- The biographer's moral approval or disapproval

## Pitfalls (Consolidated)

### Structural-voice bleed

This skill's narrator voice is its own. The Penang `hang/aku/wei` register belongs to Arif, not to the biographer. If the prose starts reading like a chat ("wei hang, macam ni..."), the biographer has slipped into subject register. Rewrite in observer voice.

### F5 weight (chat quotes are the heaviest material)

The most powerful sentences in a biography are direct quotes. They are also the most legally and ethically weighty. When in doubt, paraphrase. When paraphrasing is inadequate, Mode C authorization is the gate, not an assumption.

### Filename discipline

Always suffix by version + intent. A biography can have: `_v1_NOVEL`, `_v2_NONFICTION_ANON`, `_FINAL_NAMED`. The user may want any of them. Keeping them all is cheap; losing them is unrecoverable.

### Source citation drift

A chapter that opens with `[Source: ...]` and ends without one has lost its anchor somewhere in the middle. Verify each chapter ends on a cited scene, not an inference.

### Page count vs material density

A 4,000-word biography should be 8-12 pages depending on chapter count and density. A 1,200-word biography on 8 pages is sparse. Match the page count to the material.

### Aesthetic drift into literary memoir

The temptation to write beautiful sentences is real. The biography's job is recognition, not beauty. A plainer sentence that nails the scene beats a beautiful sentence that floats. Cut the metaphor when the metaphor replaces the fact.

## Quality Check (before send)

```
[ ] F13 mode authorization recorded (A / B / C) and respected throughout
[ ] F5 elements absent even in Mode C (medical, identifiers, third parties not in export)
[ ] Lens named before drafting; chapter order follows lens, not chronology
[ ] Every chapter opens with [Source: ...] or equivalent anchor
[ ] Every load-bearing quote is verbatim from the export
[ ] Voice stays in biographer register (aku) — no slip into subject register
[ ] Two-reader check passed (each subject will recognise their own weight)
[ ] Superseded drafts archived with intent suffix, not deleted
[ ] PDF actually opens, page count matches material density
[ ] Final page not stranded (no <50-char near-empty trailing page)
```