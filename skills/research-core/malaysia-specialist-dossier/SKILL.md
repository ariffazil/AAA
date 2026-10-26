---
name: malaysia-specialist-dossier
description: "Dossier on Malaysian doctors/hospitals by capability."
version: 1.0.0
category: research-core
tags: [malaysia, health, specialist, hospital, referral, osint, dossier, nsr]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Malaysia Specialist / Hospital Dossier

Build a referral dossier on Malaysian consultants, departments or hospitals: who does which step, which centre carries the volume, and what test must exist before the decision. Enumerate from the National Specialist Register, prove capability from the institution's own service pages, never rank doctors by name.

## When to use

- "Siapa doktor terbaik untuk X di Malaysia" / "which specialist should I see"
- whether a named hospital can actually perform procedure Y
- a profile pack on a named consultant or a whole department
- the same research re-cut into a guide a non-medical relative can carry into a clinic

Sibling skills: `person-dossier-from-public-sources` (single person, epistemic labels), `BIOHACK-PEPTIDES` (compound evidence tiers). This one is **institution + capability + referral path**.

## The question is capability, not ranking

Never return a ranked list of names. No Malaysian registry, hospital or ministry publishes per-doctor outcome data — procedure volume, complication rate, survival by operator. A name ranking is therefore invented by construction, and it is the fastest way to hand a family a decision they will act on with no evidence behind it.

Answer four things instead:

1. **Which centre** carries this condition at national volume, and what the centre itself certifies (accreditation, programme designation, stated case volume).
2. **Who does which step.** The pathway splits into diagnostician → interventionalist → surgeon → intensivist. "The best doctor" is usually three different people; naming the one who does the step in question is the useful answer.
3. **What objective test must exist before the decision** (pH study, manometry, echo measurements, shunt ratio). Without it the choice of operator is premature, and saying so is worth more than any name.
4. **What the patient must ask**, one line per question, phrased so a lay person can read it aloud.

For a child, add the age-dependent deadline: the same defect carries a different decision window at 2 months, 2 years and 12 years, and where the family sits on that timeline changes referral urgency. State the window and the consequence of waiting, without fright language.

## Procedure

1. **Fix the clinical object first** — condition, population (adult / paediatric / congenital), and the decision to be made (diagnose, medicate, operate, second opinion). A dossier without this drifts into a directory.
2. **Enumerate registered specialists** through the National Specialist Register rather than a search engine. NSR gives registered qualifications, awarding body, year and practice addresses, so a credential claim gets checked instead of repeated. Endpoint recipe below.
3. **Separate capability from absence, from the hospital's own pages.** Quote the service list to prove the hospital does the test or the operation, and quote the same kind of list to prove what is missing — a department roster that omits a unit is evidence the unit is not there, not evidence it was overlooked. Absence claims need that warrant as much as positive ones.
4. **Pull each shortlisted doctor's own published profile** for role, sub-specialty and procedures. Role titles carry real weight: clinical director of X, head of Y, fellowship in Z. Sub-specialty is the field that decides who to see; qualifications only say which door they may enter.
5. **Check who publishes on the condition.** PubMed with an affiliation filter (`"Hospital X"[Affiliation]`) surfaces who does the research and consensus work on the exact condition — often a different name from the marketed one. Appearing in the national consensus statement for the condition outranks a longer fellowship list.
6. **Source portraits under the hard rules below.**
7. **Build the artifact**: analyst dossier (position → qualifications → sub-specialty → one paragraph of reading → declared gaps) with closing sections for patient questions and for what the document does not say. PDF via `typst-pdf-report`.

## Endpoints that work

**NSR (nsr.org.my).** Form at `/list11.asp`, POSTs to `/list1pview.asp` with `state_ForSearch`, `allSpecialty_ForSearch`, `name`, plus empty others. Codes worth knowing: state `14` = WP Kuala Lumpur (`12` Selangor, `9` Penang), specialty `305` = Gastroenterology & Hepatology, `604` = Paediatric Gastroenterology, `913` = Upper GI Tract Surgery. Read the `<select>` options for the rest. Drive the form in a real browser and then page `/list1pview.asp?page=N` reading table rows as text — a direct urllib POST returns page one and loses the page count. The name cell links to `/list1viewdetails.asp?Account=N-0-XXXXXX`; that token is opaque and the **visible SR No is not the token**, so harvest the href per name. Detail pages give specialty + sub-specialty, every registered practice address, and a qualifications table (degree / awarding body / year).

**MOH hospitals.** `hkl.moh.gov.my` (the bare `hkl.gov.my` does not resolve); bilingual tree `/en/...` and `/mengenai-kami/jabatan/...`. Department pages carry the service list used for capability claims; `/awam/jadual-klinik` proves a subspecialty clinic exists; `/hubungi-kami/direktori` covers management and support staff, **not** specialist doctors, so an empty directory hit is not evidence of an unstaffed department. `hospital.com.my/department_hkl/*.htm` is an older mirror — fine for departmental history, not for current capability.

**IJN (ijn.com.my).** `/doctors-directory/<specialty>-doctors/` cards are `<div class="doctor-card">` with `.name`, two `.position-text` divs and a `/doctor/<slug>/` link — split on the card div, never regex over `<a>`. Profile tabs: Doctor Profile, Specialties, Procedures, Membership, Fellowship, Registration/License, Awards, Clinic Hours; parse by slicing between labels found *after* the duplicated nav block. Self-published institution numbers live in `Clinical Milestones`, `Management Team` and the Heartbeat / Heart-2-Heart PDFs.

**Third-party corroboration.** Private hospital directories (Pantai/IHH, Gleneagles, Sunway, UKM Specialist Centre), the doctor's own clinic site, and conference speaker pages / workshop faculty PDFs (APDW, MUGIS, MSGH) — the faculty bio states role, training lineage and current institution in one paragraph.

**PubMed E-utilities.** `esearch.fcgi` → `efetch.fcgi?db=pubmed&retmode=xml&id=<ids>`, then read `<Affiliation>` inside each `<Author>` block. Queries that work: `"Hospital Kuala Lumpur"[Affiliation] AND (<condition> OR <procedure>)`, `<Surname> <Initials>[Author] AND Malaysia`, `<title phrase>[Title]`.

## Portrait sourcing rules (hard)

Public hospital sites routinely hide consultant photographs behind a placeholder image. The placeholder gives itself away in the file path (`COPYRIGHT-LOGO`, `male.png`, `female.webp`, `DR-IMAGE-COPYRIGHT-LOGO-*`).

- **Real portraits cluster where the institution markets itself**: management/board page, newsroom articles, conference speaker pages, the doctor's own clinic site, university profile. Harvest there.
- **Verify every candidate with a vision pass before embedding it.** Ask three things: how many people, is it a single identifiable portrait, is there a name or caption inside the frame. Reject group shots, podium shots, magazine covers and collages — a group photo beside one name is a misattribution, not a layout problem.
- **Match on the image's own metadata** (alt text, filename, caption) for at least two name tokens. A surname match alone will pull an unrelated politician out of a news article.
- **No verified portrait → initials block.** Never a different person's face, never a generated face, never a silhouette lifted from another profile.
- Credit each photo under it (institution or outlet), and say in the limits section when a portrait came from a news article rather than the institution.

## Two deliverable shapes

**A. Analyst dossier** — for the principal, who will relay it. Full position titles, credentials, sub-specialty, capability map of the centres, the "who does which step" split, and an explicit gaps section (no outcome data, professions move, register lag).

**B. Lay-person guide** — for a relative who will act on it alone. No clinical jargon left untranslated ("tanda", not "symptoms"; "imbasan jantung", not bare "echo"); one plain diagram of the mechanism beats three paragraphs; the symptom section is a *log to keep*, not a list to memorise; the "what not to panic about / what needs the emergency department tonight" split is mandatory; end with a printable checklist and the appointment phone number.

Both shapes carry the same refusal: no doctor ranking, no outcome numbers, and the named test that must precede the decision.

## Pitfalls

- **The register lists registered practice addresses, not today's clinic roster.** A consultant who moved to private practice can still show the public hospital. Write "registered at", tell the reader to phone before travelling, never "available at".
- **A department's own service list is the only defensible capability claim.** Referral-aggregator and hospital-comparison sites copy each other and invent sub-specialties. Cite the institution's page.
- **Do not soften the refusal into a ranking with adjectives.** "Best for X" answered as "the centre that does the most of X, and the three people who each do one step" is complete; adding a personal top pick reintroduces the fabrication.
- **A public hospital's patient-facing capability can live on a stale mirror** — check the department page on the live domain, not the older `department_*` mirror still describing a decades-old service lineup.
- **Names of the dead persist across the web.** Before recommending a senior figure, confirm they are alive and practising; a memorial page outranks every old profile that still lists them. Say the name once in the limits section so the reader is not blindsided when they meet it in their own searches.
- **Local-language search terms fail on English/German-only databases.** Translate the query, not the answer.
- **A label you cannot read is a blind spot, not a prompt to guess.** When a photo of a vial, packet or report is out of focus or occluded, say which part is unreadable and what would make it readable (closer shot, focus on the label, the vendor name). Never name a product or compound from its packaging silhouette — every lyophilised peptide vial looks identical.
