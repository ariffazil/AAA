---
name: malaysia-medical-specialist-sourcing
description: "Use when mapping Malaysian doctors or specialists."
version: 1.0.0
category: research
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Malaysia Medical Specialist Sourcing

Sourcing a Malaysian doctor map from primary records. Complements
`person-dossier-from-public-sources` (artifact shape, epistemic labels) — this
skill is the country-specific retrieval layer.

## Trigger

- "Siapa doktor terbaik untuk X di Malaysia"
- "Deep profile [hospital] doctors", "buat PDF doktor"
- Any ask needing a specialist roster with qualifications

## Order of operations

1. **NSR first**, hospital directory second, media third. A hospital page is
   marketing; NSR is a registration record with a number, degree, awarding body,
   year, and place of practice.
2. Name three layers separately in the output: what the register asserts (fact),
   what the role means (derived), what the doctor is actually good at (reading —
   label it as opinion).
3. Refuse the outcome question. No Malaysian body publishes per-doctor volumes,
   complication rates, or survival. "Best doctor" is unanswerable; "who does this
   operation most often" is answerable only by asking them.

## NSR — National Specialist Register

- Search form: `https://nsr.org.my/list11.asp`
- Results: `POST https://nsr.org.my/list1pview.asp` with
  `applicationNo, name, cityTown_ForSearch, state_ForSearch,
  allSpecialty_ForSearch, sector_ForSearch, citizenship_ForSearch,
  gender_ForSearch, buttonSearch=Search`
- Paging: `GET .../list1pview.asp?page=N`, 10 rows per page
- Detail: `https://nsr.org.my/list1viewdetails.asp?Account=<Account>`

**Account-id trap.** The detail link needs the opaque `Account` value from the
results page (`N-0-102867`), not the SR number. Passing the SR number returns a
bare page with no personal data — which reads exactly like "no record found".

| Field | Value |
|---|---|
| state | `14` KL · `12` Selangor · `16` Putrajaya |
| specialty | `305` Gastroenterology & Hepatology · `604` Paediatric Gastro · `913` Upper GI Tract Surgery |
| cardiology / others | read the live `<select>` options; codes are not guessable |

Scrape the whole state then filter locally. A KL-only gastro search returns 70
rows over 4 pages; only 7 name Hospital Kuala Lumpur, and some of those list HKL
as one of several private practices.

## Hospital directories

- **IJN** — `ijn.com.my/doctors-directory/` per-specialty pages
  (`cardiology-doctors`, `paediatric-cardiology-doctors`,
  `cardiothoracic-and-vascular-surgery-doctors`, `anaesthesiology-doctors`).
  Cards carry name, designation, and the full qualification string as IJN prints
  it. Per-doctor page `/doctor/<slug>/` adds the long position line, a
  qualifications list, and tabbed Profile / Specialties / Procedures / Membership
  / Fellowship / Registration / Awards.
- **HKL** — `hkl.moh.gov.my`. Department pages under `/mengenai-kami/jabatan/...`
  list services and clinic locations (Gastroenterology clinic: Level 1, Main
  Block; general line 03-2615 5555). `/hubungi-kami/direktori` is an
  administrative staff table — no clinicians.
- `hkl.gov.my` has **no DNS**; `hospital.com.my/department_hkl/*.htm` is stale and
  404s on Gastro (usable only for department history).
- `moh.gov.my` and `medic.um.edu.my` refuse this host. `nsr.org.my`,
  `hkl.moh.gov.my`, `ijn.com.my`, `ummc.edu.my` answer a plain urllib GET with a
  browser User-Agent. Search lanes that return: `web_search_exa`,
  `web_fetch_exa`. DuckDuckGo HTML and Brave image search are walled here.

## Portraits — the placeholder trap

IJN serves placeholder images for nearly every consultant: card images and
per-doctor pages point at `COPYRIGHT-LOGO*.png` / `DR-IMAGE-COPYRIGHT-LOGO*.png`.
Real portraits exist on `ijn.com.my/management-team/` (match by `alt` = name),
covering only the dozen people on that page. Of 49 consultants scraped, 5 had a
real IJN portrait.

Rules:

- No portrait → put the person's **initials** in the slot. Never borrow a face from
  another hospital, a namesake, or an uncaptioned media photo.
- Vision-check every candidate before it sits next to a name: one person? face
  clear? does any text name them? A group/event shot, a podium speech, a collage,
  or a magazine cover is not a portrait.
- Media route that works: CodeBlue `codeblue.galencentre.org` WordPress REST API —
  `/wp-json/wp/v2/posts?search=<name>&per_page=5&_embed=1` returns featured media
  plus caption. Accept only when the **caption** names the person.
- Credit the photo source in a small line under each image.

## Two findings that change the recommendation

Check these on primary pages before naming anyone:

- **A hospital with good diagnostics may have no surgical unit for the condition.**
  HKL runs manometry and 24-hour pH studies, but its General Surgery department
  lists Vascular, Breast & Endocrine, Colorectal and Thoracic sub-specialties — no
  Upper GI / anti-reflux unit. Calling a hospital "best for GERD" without checking
  sends the patient for a workup that cannot finish there.
- **Registration is not the current roster.** A specialist can hold a live NSR entry
  with a public hospital while working in private practice (verified: a unit head
  who left in 2024 was still registered to the old hospital). State the lookup
  date; tell the requester to phone and confirm.
- **A deceased specialist may still dominate search results.** Check for an
  obituary or memorial page before quoting a name as an option.

## Output

- Malay, plain register, no jargon — the reader is often a relative, not a
  clinician. Doctor dossiers for Arif ship as a PDF (typst-pdf-report), not prose.
- Per person: designation · qualifications as printed · sub-specialty (the part
  that actually routes the patient) · one paragraph of reading · the data gap.
- Always include a limits section: no outcome data exists, photos unavailable for
  N names, registration dates, not medical advice.
- Verify by `pdftotext` for every name and section heading; rasterize only for
  layout.

## Pitfalls

- A confident career list from an aggregator (ContactOut, Vaidam, RocketReach) is
  not a source. Check each claimed role against NSR or the hospital's own page.
- LinkedIn "Department: Medical · Level: Specialist" plus a current-employer badge
  is a self-report — a lead, not a credential.
- Do not merge two people because names overlap; Malaysian naming
  (`@ Kandavello`, `a/l`, `binti`, dropped patronymics) splits and duplicates.
- Do not infer private matter from a professional page — health, family, politics,
  remuneration. Refused section, every time.
