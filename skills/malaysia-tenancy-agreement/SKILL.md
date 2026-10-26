---
name: malaysia-tenancy-agreement
description: >
  Analyse Malaysian residential tenancy agreements: who pays for what
  (maintenance vs repair vs replacement), aircond/appliance disputes, tenant
  rights, red-flag clauses, escalation protocol.
version: 1.0.0
tags: [malaysia, tenancy, landlord, tenant, rental, property, aircond]
triggers:
  - Aircond or appliance broken in a rental
  - Owner refuses to repair or replace
  - Deposit dispute or TA clause questions
  - Arif sends a Tenancy Agreement PDF for analysis
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Malaysia Tenancy Agreement Analysis

No Residential Tenancy Act is in force in Malaysia (as of 2026) — **the contract IS the law between the parties**. Read the agreement, then map clauses. Never assume statute fills gaps.

## Extraction

- PDF: `pdftotext -layout file.pdf -` (poppler-utils, usually pre-installed). Fall back to pymupdf if available.
- Read the Schedule FIRST: rent, due date, deposits (rental/utility/access card), term, renewal terms.

## The maintenance → repair → replacement ladder

| Category | Typical payer | Notes |
|---|---|---|
| Routine servicing (AC 6-monthly, filter cleaning) | Tenant | often an SC: "service once every 6 months, receipt to landlord" |
| Minor repairs <= RM200/item | Tenant | common SC threshold |
| Repairs > RM200/item | Shared 50/50 | usually "subject to mutual agreement PRIOR to repair" — get approval in writing first |
| Damage from tenant negligence/default | Tenant 100% | regardless of cost |
| Replacement of aging/broken unit (compressor death, very old unit) | Owner | capex, not maintenance — owner must provide working fixtures |
| Landlord fixtures not working at all | Owner | quiet enjoyment (landlord covenant 4(a) in standard TAs) |

## Aircond-specific decision tree

1. Top-up gas alone fixed it? → tenant cost, done.
2. Cold 2-3 weeks then warm again → gas leak (RM200-500 trace+repair) — likely >RM200 → 50/50.
3. Compressor weak → RM800-1,200 → 50/50 (or owner if unit very old).
4. PCB board → RM400-700 → 50/50.
5. Everything checked, unit old → replacement (RM1,500-2,500) → owner capex.
6. Tenant wants an UPGRADE (1.0 → 1.5/2.0 HP): not landlord obligation — offer to split the difference; landlord may refuse.

## Escalation protocol

1. Get technician WRITTEN diagnosis (WhatsApp ok): problem + cost + repair-vs-replace recommendation.
2. WhatsApp owner citing the exact clause number, attach report, propose the split per clause. Draft in Malay, soft tone, no threats.
3. No response ~1 week → follow up once.
4. Deposit withheld / unresponsive → TTPM (Tribunal Tuntutan Pengguna Malaysia) for consumer claims; legal aid for bigger sums.
5. NEVER DIY-replace a landlord unit and eat the full cost — you do not buy assets for someone else house.

## Red-flag clauses (common in copy-paste TAs) — flag to Arif, do not moralise

- Padlock / self-help re-entry on 1-month arrears (landlord cannot take possession without court order; likely void)
- Late penalty RM50/day on RM1,800 rent ≈ 1,000%/yr — penalty, likely unenforceable as liquidated damages
- "Terminate with 1 month notice for any reason deemed valid" — vague, may be unenforceable
- Access-card deposit listed separately from refundable deposits
- "No claim for compensation" for interruption (clause 3(l)) — one-sided
- Tenant bears ALL stamp duty + preparation costs (5(f)) — common but negotiable next time

## Reply shape (Arif)

- Verdict table first: situation → who pays → clause basis. Directly answer "okey ke kalau aku request X?".
- Offer the exact WhatsApp draft — he forwards/adapts.
- Do not push him to sue; present options including doing nothing.
