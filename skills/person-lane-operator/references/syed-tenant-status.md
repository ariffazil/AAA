# Syed Khairuddin — Tenant Status (Cross-Link Fixture)

> Load this file when Syed mentions housing, aircond, landlord, rent, "TPUM", "plus 1", or any tenancy-related query.
> Cross-links `person-lane-operator` with `malaysia-tenancy-disputes` skill.

## Tenancy Overview

| Field | Value |
|---|---|
| Unit | [ADDRESS-REDACTED] @ 3rdNvenue, Jalan Nipah, Ampang 55000 |
| Landlord | [NAME-REDACTED] (NRIC [IC-REDACTED]) |
| Tenant | [NAME-REDACTED] (NRIC [IC-REDACTED]) — SAME as persona |
| Term | 2 Jul 2026 – 1 Jul 2027 (1 year fixed + 1 year flexible) |
| Monthly rent | RM 1,800, due on/before 9th |
| Deposits at risk | RM 4,700 total (rental RM3,600 + utility RM900 + access card RM200) |

## Active Issues

| Issue | Status | Key Clause |
|---|---|---|
| **AC not cooling** (post-servis, gas added, still warm) | Landlord notified; awaiting response | SC4 (servis 6 bulan), SC5 (repairs >RM200 50/50), 3(f) (fair wear & tear), Schedule B (fixtures good working condition) |
| **Formal letter generated** | `/root/sado/references/letters/SURAT-AIRCOND.pdf` + `.docx` | Citations: SC4 + SC5 + 3(f) + Schedule B |
| **Next step** | Landlord response 7 days → registered post → TTPM (RM5) | Escalation ladder |

## Clause Quick Reference (from agreement)

- **SC4**: Tenant servis AC 6 bulan sekali, hantar resit kat landlord
- **SC5**: Minor repairs ≤ RM200 = tenant pays. > RM200 = 50/50 shared. Replacement (not repair) = landlord 100%.
- **3(f)**: Fair wear and tear ACCEPTED — tenant not liable for age-related failure
- **Schedule B**: Fixtures in good working condition at handover — landlord warrants
- **SC3**: Padlock on 1-month arrears — questionable self-help eviction
- **SC7(a)**: RM50/day late penalty — ≈1,000% APR, possibly unenforceable

## Manglish Shorthand

| Shorthand | Meaning |
|---|---|
| TPUM | Tanya Pasal Umah |
| Plus 1 | Tambah orang duduk dalam unit (occupancy consent) |
| x sejuk | AC tak sejuk |
| nak surat | Nak formal letter untuk landlord |

## Deposit Risk Calculation

If Syed withholds rent or breaches agreement:
- Rental deposit: RM3,600
- Utility deposit: RM900
- Access card: RM200
- **Total at risk: RM4,700**

**Rule:** NEVER advise withholding rent. Pay rent on time + note "paid without prejudice to my claim re: [issue]". Use letters and TTPM, not self-help.

## Template Letters Available

| Letter | Path | Status |
|---|---|---|
| AC replacement (full) | `/root/sado/references/letters/SURAT-AIRCOND.pdf` | ✅ Generated 2026-08-07 |
| AC replacement (Word) | `/root/sado/references/letters/SURAT-AIRCOND.docx` | ✅ Generated 2026-08-07 |
| Plus-1 consent (draft) | `/root/sado/references/SURAT-PLUS-1-LANDLORD.md` | ⏳ Template (needs filling) |

## Pitfalls

1. **"Plus 1" ≠ sublet** — adding a partner to live together is NOT the same as renting out the room. Landlord can't refuse unreasonably, but consent is still required per agreement.
2. **TPUM = Syed slang for tenancy questions** — always check this fixture first when Syed asks about housing.
3. **RM4,700 deposit is Syed's leverage** — always mention deposit exposure when advising. It grounds the decision in real stakes.
4. **Aircond = capital replacement, not repair** — SC5 50/50 does NOT apply. Landlord pays 100% for replacement.
5. **Neu Suites AC common issue** — other tenants may have same problem. Strengthens TTPM case if documented.
