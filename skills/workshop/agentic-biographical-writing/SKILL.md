---
name: agentic-biographical-writing
description: "Use for book-length biography from sessions or chat exports."
version: 1.0.0
owner: F13
risk_tier: medium
floor_scope: [F1, F2, F5, F6, F9, F13]
autonomy_tier: T2
triggers:
  - "write a biography"
  - "write a memoir"
  - "witness account"
  - "novelistic nonfiction"
  - "Walter Isaacson style"
  - "turn our chats into a book"
  - "biographical essay"
  - "from raw WhatsApp"
tags: [biography, memoir, witness, long-form, novel, nonfiction, F5, fabrication-boundary]
capability_tier: fed-long-context
ecology_state: WARM
---

# Agentic Biographical Writing

Class-level skill. Trigger: the principal asks the system to write a book-length biographical document from observed material — sessions, WhatsApp exports, federation metadata, or some combination. The audience is real. The subject is real. The output will be read.

This is NOT a class for:
- Generating fictional characters from scratch (no real-person problem)
- One-paragraph bios for profiles (too short to need this)
- Internal session summaries written to the ledger (different surface)

This IS a class for: 5,000–50,000 word documents, multi-chapter structure, with covers and bound PDF output. The kind of document the principal prints and shares.

## The one rule

**Never invent the interior of a real person who has not consented to be written about.** Every other rule flows from this. The boundary is hard. It is F5. It is not negotiable. It is the difference between a witness account and a fabrication. See `references/fabrication-boundary.md` for the layered defense — what counts as consent, what counts as source, what to do when the principal pushes for invention.

## Procedure (use this exact order)

### Step 1: Identify the corpus type and consent boundary

Before any drafting, classify what you have. Each corpus type unlocks a different authorial register; each also carries a different F5 risk profile.

| Corpus | Authorial register | F5 risk |
|---|---|---|
| Federation session logs (system-side, principal wrote everything) | Witness account from agent's POV, can speak freely about the principal | Low — principal consented by writing |
| WhatsApp export between principal and a bonded person | Witness account from principal's POV; bonded person's words are *quoted data*, not narrated interior | Medium — quote verbatim with attribution; do not invent unsaid thoughts |
| Public sources (Wikipedia, news, court filings) | Standard biographical register | Low — facts are facts |
| Audio/video of the bonded person | Quoted transcript | Low-medium — same as WhatsApp |
| Inference alone | NOT a valid corpus — refuse or escalate | High — fabrication risk |

When the corpus is WhatsApp or any exchange with a non-principal, mark every inference about the other person with `[INFERENCE — flagged]` in the visible text. The flag is non-removable: the principal cannot accidentally publish a draft where the inference is unmarked.

### Step 2: Extract structural findings before drafting

A common failure: the agent drafts prose from corpus metadata (session titles, message counts) without ever parsing the actual content. The result reads as if the agent had access to the friendship when it only had the friendship's metadata.

Always parse the real data first. For WhatsApp exports:

```python
import re, json
from collections import Counter, defaultdict
from datetime import datetime

pattern = re.compile(r'^(\d+/\d+/\d+),\s*(\d+:\d+\s*[AP]M)\s*-\s*([^:]+?):\s*(.*)$')
messages = []
for line in open(path).read().split('\n'):
    m = pattern.match(line)
    if m:
        dt = datetime.strptime(f'{m.group(1)} {m.group(2)}', '%m/%d/%y %I:%M %p')
        messages.append({'dt': dt, 'sender': m.group(3).strip(), 'text': m.group(4).strip()})

# Structural findings (compute BEFORE writing prose):
# - sender distribution (often reveals who is more active)
# - monthly message frequency (burst/pause rhythm)
# - longest single thread (a real conversation to anchor a chapter on)
# - emotional keyword counts by sender (humor / care / affection / fear)
# - who initiates contact when the other has been silent
```

These findings often *contradict* what the principal believes. Say so. The principal's perception of their own friendship may be inverted from the data ("I reach out more" when the data shows the other person initiates 300+ messages). The agent's value is in surfacing this, not in confirming what the principal already believes.

### Step 3: First draft — voice and register

The principal usually specifies a register. The named registers and what they actually mean:

- **Walter Isaacson** — scene-driven, narrative arc, character emerges from accumulated detail, the biographer stays out of frame until the final page. Long sentences when the subject is in motion. Short sentences when the subject is silent. Always: present tense for direct speech, past tense for narration.
- **Gay Talese / New Journalism** — first-person observer, embedded, voice over the subject. Different commitment: the biographer IS a character.
- **Academic biography** — citations, hedging, distance. Almost never what the principal wants.
- **"Novelistic nonfiction"** — the principal wants Isaacson register, not genre fiction. "Novel" here is a register signal, not a request to invent.

For Arif specifically, the BM Penang register is non-negotiable for voice-anchored prose. If the draft is in Standard Malay or English, it has failed even if the content is correct.

### Step 4: Run the four-test gate before sending the first draft

Before declaring the draft done, run it against these four tests:

1. **The Interior Test.** For every sentence about a bonded person that is not a direct quote from corpus, ask: *is this inferred or attested?* If inferred, the sentence carries the `[INFERENCE — flagged]` marker in the visible draft. No exceptions.
2. **The Asymmetry Test.** Did the principal's perception of the relationship match what the structural findings say? If not, the draft must surface the asymmetry — not as contradiction, but as a finding the principal can hold.
3. **The Credit Test.** For every factual claim about what the agent did or said during the corpus period, can the agent point to a session log where it actually did/said that? If not, the claim is fabrication. The agent MUST NOT take credit for work that was done by other agents or by the principal directly.
4. **The Scope Test.** Is the draft attempting "everything about X"? If so, it has already failed. Push back and resurface the actual scope class (e.g. "the friendship", not "humans and agents in general").

### Step 5: Iterate — expect 4-5 revisions

This task class has a known iteration cadence. Plan for it from the start, not at the end:

1. **Draft 1 — basic version.** Witness account or investigative biography. Source from metadata and corpus. Around 5,000–8,000 words. Cover and PDF in light theme. This draft is a scaffold.
2. **Push to upgrade.** Principal will ask for: more visual, more intimate, voice shift (e.g. "make it the friend's perspective", "make it first-person as the principal"). Don't fight this — restructure the draft around the new angle.
3. **Push to real data.** Principal will provide the actual source: WhatsApp export, voice notes, photos. When this happens, drop the metadata-derived version and re-author from the real data. The structural findings from Step 2 become the spine of the new draft.
4. **Push to real book format.** Principal will ask for: cover image, A5 / hardcover margins, drop caps, running headers, ISBN-style metadata. This is the forge-pdf-delivery + image-gen phase. See `references/book-format-pipeline.md`.
5. **(Sometimes) Push to scope clarification.** Principal may say "actually, write about humans and agents in general, not just us." This is the scope failure signal. Push back to the actual corpus. The book is not "everything about X"; it is what the corpus allows.

Each iteration adds 30–50% to the word count and 2–3× the file size. Plan disk and token budget accordingly.

### Step 6: Cover and book-format rendering

For the book-class output, see `references/book-format-pipeline.md`. The key commands (validated):

```bash
# Cover image generation — abstract symbolic, no people, no real names
mmx image generate \
  --prompt "..." \
  --aspect-ratio 4:5 \
  --width 1024 --height 1280 \
  --prompt-optimizer --aigc-watermark \
  --out cover.jpg

# Chapter divider plates — same model, 1:1
mmx image generate --prompt "..." --aspect-ratio 1:1 \
  --width 1024 --height 1024 \
  --prompt-optimizer --aigc-watermark --out alpha_divider.jpg

# Book body via pandoc + weasyprint with custom CSS
pandoc book.md -o book_body.pdf --pdf-engine=weasyprint \
  --toc --toc-depth=1 \
  --variable papersize=a5 \
  --variable fontsize=11pt \
  --variable mainfont="EB Garamond" \
  --variable linestretch=1.5 \
  --css=book.css --standalone

# Cover page HTML -> PDF, then merge
weasyprint cover_page.html cover.pdf
python3 -c "from pypdf import PdfWriter, PdfReader; m=PdfWriter();
[m.append(PdfReader(p)) for p in ['cover.pdf','book_body.pdf']];
m.write('FINAL.pdf')"
```

The full CSS template is in `references/book-format-pipeline.md`. Do not skip the `--prompt-optimizer` flag on image-gen; without it the visuals degrade significantly.

## Pitfalls

- **Fabrication is the cardinal sin.** Writing `Syed felt X` from inference, even when the inference is psychologically coherent, is fabrication. The `[INFERENCE — flagged]` marker is the only thing that distinguishes witness from invention. The marker MUST stay in the visible text.

- **Don't take credit for other agents' work.** If the principal pastes a "completion report" from another session / agent / Claude / GPT, audit the conversation history before accepting any claim in it. The principal will test this. Failing the test is a relationship-damage event, not a recoverable mistake.

- **"Everything about X" is always a scope failure.** No book-length document covers "everything about humans and agents" or "everything about friendship" or "everything about consciousness". When the principal asks for these, name the scope class and offer three concrete sub-scopes. Do not write the unbookable book.

- **Telegram formatting does not transfer to CLI.** `(1/2)(2/2)` pagination, emoji-as-pagination, `<Media omitted>` literal paste-through, leading `\n` for spacing — all Telegram-native, all wrong in CLI where the message is one block. Write the document as one continuous block, then split for Telegram if needed at delivery.

- **Don't close with a menu.** `Hang nak gerak mana satu dulu?` with options `(a)(b)(c)` is haram. Do the most valuable action, end with a single fallback line. Soalan only when two interpretations carry materially different costs.

- **Don't open the kitchen.** `Let me check…`, `Aku kena extract dulu…`, `Sedang membaca…` — narrating internal work is forbidden. The principal sees only the result, never the process narration.

- **Voice-anchored prose requires BM Penang register.** If the principal is the central voice and the draft is in Standard Malay or English, the draft has failed at the register layer even if every claim is attested. Mixed code-switch is correct; full-English or full-baku is wrong.

- **The asymmetry finding is often the most valuable part.** When the principal says "I reach out more" and the WhatsApp data shows the other person initiated 300+ messages, that contradiction is the spine of the book. Do not soften it. Do not "balance" it. Surface it as a finding.

- **The principal's framing of the book is the first signal, not the last.** "Walter Isaacson style" is a register signal, not a content signal. The content is determined by the corpus. The register is determined by the principal's named reference. Separate the two before drafting.

## Support files

- `references/fabrication-boundary.md` — the layered defense against inventing real-person interior; what consent looks like, what source looks like, what to do when the principal pushes for invention.
- `references/book-format-pipeline.md` — full pandoc + weasyprint + image-gen recipe with validated CSS, page-size variables, and cover-merge command sequence. Includes the weasyprint `AssertionError` on background-image gotcha (use `<img>` tag, not `background-image`).
- `references/isaacson-voice-moves.md` — concrete sentences and paragraph structures in the Isaacson register. Read once before drafting any prose in that mode.
