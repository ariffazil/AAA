---
name: malaysia-tenancy-disputes
description: >
  Malaysian rental dispute advisory — landlord maintenance obligations,
  repair vs replacement of fixtures, deposit forfeiture risk, written-notice
  escalation, TTPM tribunal route, and copy-paste formal letters with cited
  agreement clauses.
version: 1.0.0
tags: [tenancy, malaysia, landlord, tenant, tppm, rental, dispute, aircond]
triggers:
  - 'user is tenant or landlord with a repair, aircond, deposit, or maintenance dispute'
  - 'owner xnak bayar or boleh potong sewa or camne nak paksa owner'
  - 'user shares a tenancy agreement PDF and asks about rights'
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Malaysia Tenancy Disputes

## Core rules (state these first, they drive everything)

1. **No Residential Tenancy Act in force (as of 2026)** — the tenancy agreement governs; Contract Act 1950 + common law fill gaps. ALWAYS read the actual agreement clauses before advising (extract the PDF with pdftotext/pymupdf).
2. **NEVER withhold rent** to force repairs. Standard agreements forfeit the ENTIRE deposit (rental + utility + access card), allow padlock, and add RM50/day penalties on late payment. Withholding RM1,800 risks forfeiting RM4,500+. Pay rent on time; add note: "paid without prejudice to my claim re: [issue]".
3. **Repair ≠ Replacement** (the key legal distinction):
   - Repairs ≤ RM200/item → tenant pays (typical SC clause)
   - Repairs > RM200 → 50/50 shared (typical SC clause)
   - Replacement of an aging unit that cannot be repaired → LANDLORD 100%. "Tukar unit baru" is a capital asset replacement, NOT a "repair" — the RM200/50-50 clause does not cover it.
   - Fair wear & tear clause (standard 3(f): "fair wear and tear is accepted") shields the tenant from age-related failure.
4. **Landlord must provide working fixtures** — Schedule B ("fixtures and fittings... in good working condition") = if the AC never worked, landlord is in breach from day one; a tenant who serviced per the SC maintenance clause has a clean record.
5. **Escalation ladder** (document everything):
   - WhatsApp written notice → 7 days
   - Formal letter via registered post (proof of delivery, ~RM10) → 7 days
   - TTPM (Tribunal Tuntutan Pengguna Malaysia): ~RM5, no lawyer needed, 2-3 months, enforceable order (replacement cost, deposit deductions, damages).
   - Evidence file: technician written diagnosis, service receipts, WhatsApp screenshots, payment proofs, letter + pos receipt.

## Predatory clauses to flag (knowledge, not always challengeable)
- Padlock / self-help repossession on 1-month arrears — self-help eviction is questionable; normally needs court order.
- RM50/day late penalty ≈ 1,000% APR — likely a penalty (not liquidated damages), possibly unenforceable.
- "Terminate for any reason deemed valid" with 1-month notice — vague, tenant-hostile.
- Access card deposit not listed among refundable deposits.
- AC service every 6 months with receipt forwarded to landlord — binds tenant to maintenance burden.

## Deliverable shape (what Arif wants)
- Copy-paste formal letter (Malay) WITH clause numbers cited — he explicitly asked "buat surat n tunjuk clause". The letter is a document trail, not a negotiation — it becomes tribunal evidence.
- After the letter: WhatsApp first → registered post if silent → TTPM filing with evidence checklist.
- Reply shape per turn: verdict + ONE next action. He asks sequentially; don't dump the whole ladder every time.
- When he's anxious about risk ("aku lah rugi"), quantify the asymmetry (deposit forfeit vs replacement cost) so the math makes the decision.
## Manglish/BM verbal shorthand (recognise, don't literal-parse)

The operator and 3rd-party personas often use Manglish abbreviations that need mapping to actual tenancy concepts:

| User term | Actual concept | Section to apply |
|---|---|---|
| **"TPUM"** | "Tanya pasal umah" — opening phrase for rental queries | Top of skill |
| **"Plus 1"** | Add 1 occupant (pasangan/kawan) — needs landlord consent | templates/occupancy-plus-1-letter.md |
| **"Tukar aircond"** | AC replacement request (not repair) — landlord liable | templates/aircond-replacement-letter.md |
| **"X sejuk"** | AC not cooling — symptom of compressor/gas failure | SC4/SC5 clause cite |
| **"Refund deposit"** | End-of-tenancy deposit return | Predatory clauses section |
| **"Owner x nak bayar"** | Landlord refuses repair payment | Repair vs Replacement section |
| **"Boleh potong sewa?"** | Withhold rent? **NEVER** — forfeit risk | Core rule #2 |
| **"Pukul berapa"** | What time can landlord enter? Quiet hours | Implied klausa 24h notice |
| **"Buat surat"** | Generate formal letter (PDF + DOCX deliverable, not just markdown) | Templates below |

If user opens with **"TPUM"** or **"Plus 1"**, do NOT load the aircond template by reflex. Match the actual issue.

## Cross-class signal: person-lane target is ALSO a tenant

When serving a `person-lane-operator` persona (e.g., Syed Khairuddin), the persona's life includes tenancy rights, landlord disputes, and housing decisions. The person-lane skill references tenancy disputes as an **adjacent domain** — load this skill when the persona's conversation drifts to housing.

**Concrete rule:** if the active persona has tenancy data in `references/<persona>-tenant-status.md`, merge that context with the dispute advice. Do not treat housing and personal-caregiver as separate universes.

## PDF + DOCX deliverable pattern (not just markdown)

When user says **"buat surat proper"** or **"nak hantar kat landlord"**:

1. Generate the markdown source first (template above)
2. **Render to PDF** via weasyprint (works for now) — `pandoc X.md -o X.pdf --pdf-engine=weasyprint`
3. **Render to DOCX** via pandoc — `pandoc X.md -o X.docx` (for user editing)
4. Save under `~/.hermes/profiles/<profile>/letters/` or persona-specific path
5. Tell user only `[TARIKH SERVIS]` / `[NAMA]` placeholders remain to fill in

The 3-format deliverable (md/pdf/docx) is the standard. Don't ship just markdown when user says "proper" — they want a printable, signable artifact.

## Files

- templates/aircond-replacement-letter.md — formal Malay letter citing SC4/SC5/3(f)/Schedule B
- templates/occupancy-plus-1-letter.md — formal Malay letter for adding 1 occupant (pasangan), with Manglish glossary
- references/neu-suites-ta-clauses.md — worked example: [ADDRESS-REDACTED] TA exact clause wording
- `references/` — full BM/Manglish abbreviation mapping for tenancy + adjacent real-estate conversations


<!-- dead-pointer sweep 2026-10-23: unresolved artifacts from the gate report were replaced with the references/ directory. Basenames are preserved in the audit JSON. -->
