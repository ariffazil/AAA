---
name: searah-investigative-workflow
description: End-to-end investigative document workflow for arifOS — BIT verification, legal review gate, SEAL 999 protocol, and Arif Fazil identity standards
triggers:
  - searah investigation pdf
  - bit verification before publish
  - lawyer review gate before sending
  - seal 999 investigative document
  - wsj grade expose arif fazil
tags:
  - governance
  - investigative
  - legal
  - searah
created: 2026-05-07
---

# SEARAH Investigative Document Workflow — arifOS Standard

## Context
This skill captures the complete workflow used to produce the SEARAH-EXPOSE document — a WSJ-grade investigative report about the PETROS/SEARAH/Eni gas deal. The document is signed by Arif Fazil with his real name, distributed to journalists and politicians, and carries a SEAL 999 commitment.

**Arif's core principle:** "I don't do anonymous. I sign." Every document bearing his name must be factually bulletproof before it leaves his hands.

## Phase 1 — BIT Verification (F2 TRUTH Gate)

### ALWAYS Verify BIT Claims Before Publishing
A false BIT claim will destroy the entire document's credibility and create legal exposure.

**BIT verification protocol:**
1. Query UNCTAD BIT database (https://investmentpolicy.unctad.org/international-investment-agreements)
2. Verify: does the treaty actually exist AND is it in force?
3. Check: expired treaties are listed as "lapsed" — not in force
4. Document the verification result with timestamp and URL

**Known SEARAH case:**
- Claimed: Italy-Malaysia BIT (1988) was "in force since 1990"
- UNCTAD finding: NO such treaty exists. Confidence: 0.00.
- Result: Claim retracted. Document corrected before distribution.
- **Lesson:** A single false claim in a legal document about a RM70B deal gives hostile lawyers everything they need to dismiss the entire report.

## Phase 2 — Legal Review Gate (F6 EMPATHY)

### NEVER Send Without Legal Review
Arif Fazil signs with his real name. The lawyer review is non-negotiable before any distribution.

**Legal review checklist:**
- [ ] All BIT/treaty claims verified against primary sources (UNCTAD, official government sources)
- [ ] No access of classified documents (Official Secrets Act exposure)
- [ ] Defamation risk assessed — truth is defense, but legal costs are real
- [ ] Sources are all public record (Companies House, press releases, Hansard)
- [ ] Author identity decision: real name vs. anonymous (Arif: always real name)

**What lawyer review changes:**
- Email subject lines may need rephrasing
- Specific directors named may trigger personal legal threats
- Distribution sequence may need to change (international first = Rappler)

## Phase 3 — SEAL 999 Protocol

### SEAL Block Components (Minimum Viable)
Every sealed document must carry:
1. **Document title + date**
2. **"SEAL 999 — DITEMPA BUKAN DIBERI"** tagline
3. **HMAC-SHA256 commitment** — hash of document content (SHA256)
4. **DB hash** — hash of underlying evidence database
5. **Correction notice** — if any previous version had errors, disclose them
6. **F2 WITNESS footer** — "All claims verified against primary sources"

### SEAL Block Design Rules
- Use Courier 7pt minimum (6.5pt clips in some PDF viewers)
- Pad: 6mm left/right, 4mm top/bottom
- Hash strings must not wrap — use Table with single column width = content width
- Separate hash rows into individual Table rows
- Correction notice: plain text disclosure, not buried in footnotes

## Phase 4 — Distribution Strategy

### Recommended Sequence (SEARAH Case)
1. **Lawyer review** — gate, no bypass
2. **Email to 2 confirmed recipients** — Mahathir (mahathir@mahathir.com) + Maria Ressa (news@rappler.com)
3. **Twitter DM templates** for 5 others — pre-drafted, Arif sends manually
4. **International first** — Rappler publication = international press picks up = harder to suppress

### The 7 SEARAH Targets (Post-PH Purge, Post-Petronas-Retiree Addition)
| # | Name | Role | Channel |
|---|------|------|---------|
| 1 | Hisham Jalil | UMNO Supreme Council | Twitter DM |
| 2 | Jeffrey Kitingan | STARParti President, Senator | Twitter DM |
| 3 | Tun Dr Mahathir Mohamad | Former PM, PEKAT MARA | Email |
| 4 | Tan Sri Wan Zulkifli | Ex-PETRONAS CEO (2009-2015) | Twitter DM |
| 5 | Tan Sri Hassan Merican | Ex-PETRONAS CEO (1995-2009) | Twitter DM |
| 6 | Altimet | Rapper, Sarawak voice | Twitter DM |
| 7 | Maria Ressa | Nobel laureate, Rappler | Email |

### Email Subject Lines (WSJ-grade)
- **Mahathir:** "Dokumen sulit untuk perhatian Tun — perjanjian gas RM70 bilion"
- **Maria Ressa:** "Exclusive: Malaysia's USD 15B Gas Deal Has No BIT Protection"

## Phase 5 — Real Risk Assessment

### Legal Risks (Honest Assessment)
| Risk | Level | Notes |
|------|-------|-------|
| Malaysian civil defamation | MODERATE | Truth is defense; legal costs RM 50K-500K+ |
| Official Secrets Act | LOW | Only if classified docs used — all sources public |
| UK libel tourism | LOW | Very low probability |
| Business pressure via GLC connections | HIGH | Most realistic harm — PETRONAS network |
| Personal threats/intimidation | MODERATE | Depends on who knows Arif |

### The One Thing That Protects Arif
**All sources are public record.** Companies House UK, UNCTAD database, Eni press releases, Malaysian Parliament Hansard — none of these are classified. A document grounded entirely in public record is defensible.

## Phase 6 — What "DITEMPA BUKAN DIBERI" Means in Practice
1. Sign with real name — no anonymous distribution
2. Fix every factual error before sending, not after
3. Lawyer review is a gate, not a formality
4. SEAL 999 is a real commitment — the hash commits to the exact content
5. If challenged: own the document, defend the facts, update if wrong

## Dependencies
```bash
pip install reportlab  # PDF generation
pip install PyMuPDF    # PDF verification
```

## Key Files
- `/root/AAA/SEARAH/generate_pdf_v14b.py` — canonical PDF generator
- `/root/AAA/SEARAH/SEARAH-EXPOSE-v14-FINAL.pdf` — final sealed document
- `/root/AAA/SEARAH/fix_bit_errors.py` — BIT correction overlay tool
- `/root/AAA/memory/investigations/SEARAH-TRUTH-DB.md` — evidence database
