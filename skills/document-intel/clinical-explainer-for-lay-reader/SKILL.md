---
name: clinical-explainer-for-lay-reader
description: "Use when a diagnosis must reach a non-clinical reader."
version: 1.0.0
owner: HERMES
category: document-intel
tags: [health, explainer, pdf, typst, lay-reader, patient-advocacy, family]
triggers:
  - buat pdf untuk family member pasal condition
  - a diagnosis must be explained to a parent, spouse or friend who is not clinical
  - turning a specialist dossier into something a family can act on
capability_tier: fed-document
---

# Clinical Explainer for a Lay Reader

When a diagnosis lands on a person the principal cares about, the requester does not want a dossier — they want a document they can hand over that makes the next appointment better.

## When to use

- "Buat satu PDF aku nak share dengan [name]" after a condition has been raised.
- A family member must decide whether to operate, wait, or change doctor, and does not understand the vocabulary.
- You already built a specialist roster and now need the *reader's* version of it.

## When NOT to use

- Interpreting the principal's own reports and images → `medical-document-interpretation`.
- Who-is-the-best-doctor research → the dossier skills. This skill hands over **questions**, never a ranking.
- Anything that reads as a substitute for the treating clinician.

## Non-negotiables

1. **It is not medical advice, and the treating doctor stays the owner.** State it once, at the end, in one line — "dokumen ini untuk membantu kau bertanya, bukan menggantikan doktor yang memegang kes". Repeating the disclaimer in every section turns the document into noise and signals you do not trust the reader.
2. **Never rank doctors.** Name the centre's checkable capability (case volume the institution publishes, programme accreditation, the only centre in the country that does procedure X) and the *type* of specialist to see for which sub-problem. Then give the reader the question that closes the gap.
3. **Pre-empt self-blame in the first two pages.** For a congenital or chronic paediatric condition the first thing a parent does is audit their own pregnancy and diet. One short paragraph stating the condition is not caused by anything they did — with the base rate, e.g. about 1 in 100 births — unblocks everything that follows. Without it the rest of the document argues with guilt instead of with the disease.
4. **Name the most common false belief explicitly.** Every condition has one; for a septal defect it is that medicine can close the hole, and that a child who looks well on medication is therefore fine. Put it in a bordered callout in the reader's own words.
5. **A number without a source does not go in.** Give ranges ("85–90% of small defects close in the first year") not one confident figure, name the guideline or body, and mark what is genuinely unknown — per-doctor outcomes are not published anywhere.
6. **Translate the guideline timeline into an action window.** "Surgery is usually completed between 6 and 12 months, and before 18 months" is only useful next to "your child is 2". That pairing is the single most actionable sentence in the document; say it plainly instead of softening it into "discuss with your doctor".
7. **Two lists, never one.** "What not to panic about" and "go to hospital now" are separate pages or separate headed blocks. Merged, the parent skims both and remembers neither.
8. **Attribute correctly.** The principal is the *giver*, not the author. Do not sign his name to prose he did not write; dedicate the document to people by name only when he named them.

## Structure (nine sections, this order)

1. **What is actually happening** — anatomy in everyday words, one simple schematic (two boxes and an arrow beats a rendered heart).
2. **Why it matters** — the mechanism of harm in one paragraph, then the sentence that separates mild from serious.
3. **Small vs large** — how the decision is made, what the numbers mean, and the guideline timing placed next to this person's age.
4. **Signs to watch** — observable at home, written as things a carer can see (sweating while feeding, the weight line flattening, fast breathing in sleep, blue lips). Include the instruction to write them down with dates and carry the notes into the appointment.
5. **The treatment ladder** — lifestyle, drugs, tests, procedures, with the honest trade-off at each rung. Explain what a test is *for*, not how it is done.
6. **Where to go, and how to get in** — referral letter first, then the appointment line, what to bring, what to ask about payment before paying a deposit, the emergency number.
7. **The questions** — eight to twelve, specific and answerable. Always include "how many cases like this do you do a year", "what happens if we wait six months", and "who monitors after".
8. **Don't panic / act now** — two separate lists.
9. **Checklist before the hospital** — tick boxes, then blank ruled lines for notes.

A closing paragraph belongs on the last page: the best doctor is not the most famous, it is the one who can explain the case in words the parent understands and does not get defensive at hard questions.

## Register

- Malay as spoken in a Penang household: `kau`, short sentences, concrete nouns. No corporate or clinical register.
- **Banned in the body:** `symptoms`, `appointment`, `outcome`, `management`, `modality`, `prognosis`. Use `tanda`, `temu janji`, `hasil`, `rawatan`.
- Every unavoidable technical term gets a gloss in brackets on first use — `echo (imbasan ultrasound jantung)`, `murmur (bunyi tambahan)`.
- Never explain the same thing twice in different sections; the reader is stressed, not slow.
- No statistics tables and no bibliography in the body. One source line at the back, small type.

## Build and verify

1. Generate the `.typ` from a Python emitter; copy images into the build directory under names the emitter controls.
2. `typst compile guide.typ guide.pdf`.
3. **Text gate before layout:** `pdftotext guide.pdf out.txt`, then assert that every section heading is present, every person the requester named is present, and the banned-word list returns zero hits. This catches the register sliding back into clinical English.
4. **Layout gate after:** rasterise at 50 dpi, `montage` the pages, and read the sheet for stranded headings, clipped callouts, half-empty pages.
5. Deliver as `MEDIA:/path.pdf` with a plain-language filename — never a `/tmp` path, never a build-directory scratch name.

## Starter skeleton

Paste-and-modify Typst source, at sizes that compiled clean on A4. Keep the double bracket close on the callout block.

```typst
#set page(paper: "a4", margin: (x: 20mm, top: 18mm, bottom: 18mm))
#set text(font: ("DejaVu Sans",), size: 10.5pt, lang: "ms", fill: rgb("#22303c"))
#set par(justify: true, leading: 0.72em, spacing: 1.05em)
#show heading.where(level: 1): it => block(above: 16pt, below: 9pt)[
  #text(size: 19pt, weight: "bold", fill: rgb("#8d1c2b"))[#it.body]
  #v(-3pt) #line(length: 100%, stroke: 1.1pt + rgb("#8d1c2b"))
]
#set page(footer: context [
  #set text(size: 7.8pt, fill: rgb("#5d6b78"))
  #grid(columns: (1fr, auto), [<DOCUMENT TITLE>], [#counter(page).display()])
])

#page(header: none)[
  #v(34pt)
  #align(center)[#text(size: 9pt, weight: "bold", fill: rgb("#8d1c2b"))[PANDUAN UNTUK IBU BAPA]]
  #v(14pt)
  #align(center)[#text(size: 27pt, weight: "bold")[<TITLE LINE>]]
  #v(26pt)
  #block(fill: rgb("#eef1f4"), inset: 14pt, radius: 3pt, width: 100%)[
    #align(center)[#text(size: 10.2pt, style: "italic")[Untuk <NAME>.]]
    #v(6pt)
    #text(size: 9pt, fill: rgb("#5d6b78"))[<what this document does for the reader>]
  ]
]

#pagebreak()
= Apa sebenarnya yang berlaku
<anatomy in everyday words>

#v(6pt)
#block(fill: rgb("#eef1f4"), inset: 12pt, radius: 3pt, width: 100%)[
  #grid(columns: (1fr, 18pt, 1fr), gutter: 0pt,
    align(center)[#text(size: 9pt, weight: "bold")[LEFT] #linebreak() #text(size: 8.4pt)[low pressure]],
    align(center + horizon)[#text(size: 15pt, fill: rgb("#8d1c2b"))[⇄]],
    align(center)[#text(size: 9pt, weight: "bold")[RIGHT] #linebreak() #text(size: 8.4pt)[high pressure]],
  )
]

// CALLOUT — note the double close
#block(stroke: (left: 3pt + rgb("#8d1c2b")), inset: (left: 11pt, y: 3pt))[
  #text(size: 10pt)[*Satu ayat yang perlu kau dengar betul-betul:* <the correction that changes behaviour>.]
]

#pagebreak()
= Senarai semak sebelum ke hospital
- #text(size: 10.4pt)[☐  <item>]

#v(14pt)
== Ruang nota
#line(length: 100%, stroke: 0.5pt + rgb("#5d6b78"))
#v(12pt)
#line(length: 100%, stroke: 0.5pt + rgb("#5d6b78"))

#align(center)[#text(size: 8.5pt, fill: rgb("#5d6b78"))[Dokumen ini untuk membantu kau bertanya, bukan untuk menggantikan doktor yang memegang kes.]]
```

## Pitfalls

- **Nested typst blocks need two closing brackets** — `#block(...)[#text(...)[...]]`. A single close produces `error: unclosed delimiter` pointing at an unrelated line; count brackets in the emitter string, not on the rendered page. This bit twice in one build.
- **A callout built as one joined emitter string swallows its own closing bracket.** The box renders open and every later page inherits the indent.
- **The register leaks in the third draft.** The first pass is human, the edits push it clinical. Run the banned-word grep on the compiled text, not on the source.
- **Escaping:** `$` opens math, `@` opens a label reference, `#` opens a call — escape all of them plus `[` `]` in every string injected from scraped or generated data.
- **Do not pad to look thorough.** Nine pages with one idea each beats nine pages of dense prose for a frightened reader. If a page cannot earn its space, cut the page, not the whitespace.
- **Do not moralise at the parent, and do not praise them either.** No "you are strong", no lifestyle lecture. The document's job is the next appointment.
- **A referral path beats a phone number.** Public specialist clinics require a referral letter first; put that step first or the reader turns up and is turned away.
- **Check the build directory still holds the images.** Regenerating the source is not enough if the emitter copied photos under a name a later edit no longer matches — the compile fails on a missing file, not on a logic error.
