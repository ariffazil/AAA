---
name: health-provider-navigation
description: "Use when mapping hospital specialists or picking a doctor."
tags: [medical, provider, roster, dossier, routing, malaysia, pdf]
related_skills: [person-dossier-from-public-sources, typst-pdf-report, third-party-advisory-doc]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Health Provider Navigation

The recurring sequence: Arif asks for a deep profile of the specialists at an institution, then asks
"who is the best doctor for <condition> for <a real person>", then asks for a PDF to share with the
family. Treat it as one workflow — a roster with unverified faces or an invented ranking poisons the
guide that follows.

## The four rules that hold across every stage

1. **Roster from the institution, never from an aggregator.** Department pages and the find-a-doctor
   index are authoritative. Reconcile by profile URL, not name string — honorifics vary
   (`DATO'`, `DATO’`, `DATUK`, `PROF. DATO’ SERI`) and name-token matching splits one person in two.
2. **No face without a verified attribution.** A filename or alt-text match is not proof. Verify each
   candidate on a labelled contact sheet before it sits beside a name; where none is verified, use an
   initials block. A wrong face on a real professional is unrecoverable.
3. **Never answer "who is best" with a name.** No per-practitioner outcome data is published. Answer
   with routing by function plus checkable centre-level volume/accreditation evidence.
4. **Credentials ≠ competence — say it in the artifact.** A fellowship says which door a person may
   enter, not how good they are inside it. Transcribe credentials verbatim from the institution and
   state they were not cross-checked against the medical register, which the reader can search.

## Stage 1 — roster dossier

Pull every department/category list plus the find-a-doctor index; dedupe by profile URL. Bracket the
population by designation band (senior consultant / consultant / fellow / medical officer) and note
that fellows and medical officers are who a patient meets first even though they are not the ones
deciding.

Scrape the per-person profile, not the card. **Anchor extraction on the second occurrence of the
first section heading** — tabbed pages print the tab labels once as navigation and again as content,
so a naive first-match split returns an empty body for every profile. Assert a minimum body length on
one profile before looping the roster.

Detect gated portraits before hunting: count distinct image `src` per profile. If many people share a
placeholder filename (`COPYRIGHT-LOGO*`, generic `male.png`/`female.webp`), the institution is not
publishing portraits — and alt text will still carry the real name. Alt text is metadata, not
evidence. Leadership/management pages usually do publish real portraits for the top seats; take that
set and do not extrapolate downward.

Source photos from dated coverage. WordPress news sites expose the post index over REST:
`/wp-json/wp/v2/posts?search=<name>&per_page=10&_embed=1`; `_embedded['wp:featuredmedia'][0]` gives
`source_url`, `alt_text` and the **caption**, and the caption is where the outlet names the person.
Require at least two name tokens across caption + filename, else discard. Second lane: the outlet's
search page → article URLs → scan each article's `<img>` for name tokens. Set a browser User-Agent;
default urllib is refused by most news CDNs.

Verify before placing:

```
montage -label '%f' *.jpg *.png *.webp -tile 4x3 -geometry 380x380+6+6 contact.jpg
```

Read the sheet with the vision pass, per tile: how many people, posed single-subject portrait, any
badge or masthead. Reject group photos, ceremony stages, podium shots, and magazine covers whose
cover lines belong to another publication. Credit every used image under the portrait — the credit is
the audit trail.

Deliverable shape: profiles grouped by discipline (portrait · role chain · credentials verbatim ·
subspecialty · what this means for a patient · declared data gap), a full consultant-level table, a
power map of who holds which seat and which directorates exist, questions to bring into the room, and
a limits section. Institution-in-numbers only from figures the institution itself publishes, each
traceable to a dated milestone page.

## Stage 2 — routing answer for a named patient

Lead with the centre and the reason, not a person — volume and certification are checkable, fame is
not. Split the answer by job: who decides the route (interventionalist), who performs the definitive
procedure (surgeon), who runs critical care, who holds the sub-specialty programme a rare case should
be referred into.

**Pull the age-and-timing threshold forward.** Guidelines carry an age band for intervention;
translate it to this patient's actual age and say whether the window has passed. That sentence is
worth more than any ranking. Then name what documentation determines the decision (measurements,
pressures, growth trend) so the family obtains it before the consultation, give one alternative centre
with its honest trade-off, and close with the practical path (referral letter, phone, subsidy question
before any deposit, emergency number).

## Stage 3 — family-readable guide

Plain language is the product. Convert clinical English on first use and keep the conversion:
symptoms → tanda · appointment → temujanji · echo/scan → imbasan jantung (echo) once, then imbasan ·
murmur → bunyi tambahan (murmur). The disease name and its abbreviation stay, because every doctor
will use them. Same register Arif uses with that person; never "anda"; no bullet-only pages — each
list gets a framing sentence.

Eight beats: what is happening (words + one two-box diagram) → a **no-self-blame paragraph early** for
anything congenital or hereditary → severity and what it decides → what the carer can observe at home
(each sign with its mechanism, plus "write it down with dates") → treatment routes in plain terms
(why one over another: shape and position, not surgeon preference) → where to go and how to start →
ten questions for the room → what not to panic about vs what needs the emergency department tonight,
ending on a checklist page with notes space.

Numbers: quote the range, name who publishes it, then do the arithmetic for this patient. One endpoint
becomes a false deadline. Name the misconceptions the family will hold by default and kill each in one
sentence — for structural heart defects: medicine cannot shrink or close the defect (it only relieves
the signs), and a child who looks well on medicine is not therefore repaired.

Limits go at the back (guideline body, reference text, the institution's own programme pages) with one
closing line that this helps them ask and does not replace the doctor holding the case. Never open with
a disclaimer — it reads as the agent protecting itself rather than a friend helping. No clinical
guessing beyond the referral documents; if severity is unknown, name the measurements that determine it.

## Pitfalls

- **Contact sheets, not single images.** One vision pass over a labelled montage is faster and catches
  the group photo that a single-image check waves through.
- **Do not invent a ranking to satisfy the question.** "Best doctor in Malaysia" invites a name; give
  the routing map and say why a name would be an invention.
- **Scan the finished text for leftover clinical English** (`symptoms`, `appointment`, `scan`) before
  delivery — the translation work is invisible until you grep for the words you meant to replace.
- **Build the PDF with Typst and verify by text extraction plus a rasterised layout pass.** A build that
  exits 0 can still drop a section; see `typst-pdf-report` for escaping and the verification recipe.
- **Institution figures rot.** Anything quoted as a number (caseload, survival, certifications) must be
  attributed to the page it came from in the same document, or it becomes an unverifiable claim.

## Verification before delivery

- Every profiled name appears in the extracted PDF text; every roster row is present.
- Every image has a source credit; no initials block was replaced by an unverified photo.
- The limits section exists and names what is not published (per-practitioner outcomes).
- For a family guide: red-flag block present, ten questions answerable, checklist lines drawn, no
  disclaimer at the front.
