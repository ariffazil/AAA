# CORRECTION — SEARAH / PMA ENTITLEMENT CLAIM (v3)

**Staged:** 2026-09-17 · **v3** supersedes v2 and v1.
**Target:** `/root/AAA/canon/PETRONAS/ATLAS.md` lines 68, 106
**Status:** NON-CANONICAL STAGING — pending seal lane.
**Revision chain:** v1 (false attribution) → v2 (corrected attribution) → v3 (primary-record evidence added)

---

## §0 — WHY v3 EXISTS

v1 and v2 both searched in the wrong place: PETRONAS disclosures that predate the event,
and internal canon. Neither searched **ExxonMobil's SEC filings** — even though the PMA
assets were EPMI-operated until 2024–25, and XOM is a US-listed issuer with mandatory
disclosure. F13 (Arif) prompted the correction: *"check la ExxonMobil punya public record."*

---

## §1 — PRIMARY RECORD: EXXONMOBIL 10-K, MALAYSIA

Downloaded from EDGAR (CIK 0000034088), raw-HTML case-insensitive grep:

| 10-K | Period ending | Filed | "Malaysia" | "Esso" |
|---|---|---|---|---|
| FY2023 | 2023-12-31 | 2024-02-28 | **2** | 40 |
| FY2024 | 2024-12-31 | 2025-02-19 | **2** | 38 |
| FY2025 | 2025-12-31 | 2026-02-18 | **0** | 38 |

**FY2025 10-K contains zero mentions of Malaysia.** Not reduced — removed. Esso counts
unchanged, so this is not a parse artefact.

FY2024 10-K, verbatim:
> "Malaysia — Net interests in production sharing contracts covered 0.2 million offshore
> acres at year-end 2024. During the year, a total of 1.5 net development wells were completed."

> "Malaysia — Production activities are governed by production sharing contracts (PSCs)
> negotiated with the national oil company. The PSCs have production terms of 25 years."

Both passages absent from FY2025.

**EX-21 (subsidiaries):** "ExxonMobil Exploration and Production Malaysia Inc." still listed in
FY2023, FY2024 and FY2025 EX-21. Entity survives; **operations do not.**

Interpretation: ExxonMobil exited Malaysia upstream **in equity terms, not merely operatorship**.
Had Exxon retained a PSC interest, the FY2025 10-K would still disclose Malaysian net acreage
and wells, as FY2023/FY2024 did.

---

## §2 — PMA = THE TWO PSCS EXXON TRANSFERRED

Reuters, 20 Jul 2024: *"transfer the operations of all assets of **two** production-sharing
contracts in Malaysia to state energy company Petronas."*

### 2008 PSC — oil, southern Terengganu fields
Fields: **Seligi, Guntong, Tapis, Semangkok, Irong Barat, Tabu, Palas.**
Equity: **EPMI 78% / PETRONAS Carigali 22%** (EIA Malaysia Country Analysis Brief).
Source: Rigzone, "Petronas Inks New Malaysian Production Sharing Contract with ExxonMobil".

### GPSC — gas, 22 fields (>15 per 1998 PR)
Hubs: **Jerneh** and **Lawit** + the 1995 Joint Venture area (EPMI-operated);
**Angsi** (PETRONAS Carigali-operated).
Equity: **EPMI 50% / PETRONAS Carigali 50%.**
Signed 23 June 1998. Combined gas sales from GPSC + existing NGPSA **>12 Tcf**, expected to meet
**~two-thirds of projected Peninsular Malaysia gas demand for >25 years.** Total investment
projected **~US$5 billion (RM12 billion).**
Source: EPMI/PETRONAS announcement, 23 Jun 1998 (Killajoules archive); Oil & Gas Journal.

Wood Mackenzie, *Terengganu Area Report*, defines the area as exactly these two instruments:
> "The current active PSCs include the **2008 PSC**, which covers the oil production from the
> southern fields, and the **Gas PSC**, which covers the northern gas fields and associated gas
> production from the southern fields."

**PMA (Peninsular Malaysia Assets) = 2008 PSC + GPSC. F13's identification is correct.**

---

## §3 — THE CHAIN (dated, sourced)

| Date | Event | Source |
|---|---|---|
| 23 Jun 1998 | EPMI + PCSB sign GPSC (50/50) | EPMI/PETRONAS PR |
| Mar 2008 | EPMI + PCSB sign 2008 PSC (78/22) | Rigzone |
| 19–20 Jul 2024 | Exxon announces transfer of **both** PSCs to PETRONAS Carigali | Reuters; Upstream |
| **1 Apr 2025** | **PCSB becomes GPSC operator** | PETRONAS PR; Rigzone |
| 9 Jun 2025 | Bindu first hydrocarbon — tie-back to **Guntong E** hub (GPSC) | PETRONAS PR |
| Feb 2026 | XOM FY2025 10-K: **Malaysia removed entirely** | SEC EDGAR |
| **1 Jul 2026** | **Searah (Malaysia) assumes operatorship of 5 assets from PCSB** | Bernama; The Edge |
| 20 Jul 2026 | Wood Mackenzie: PETRONAS contributes "near-term production, cash flow and established infrastructure" | Wood Mackenzie PR |

**Exxon (1998–2024) → PETRONAS Carigali (2025–2026) → Searah/Eni (2026–).**

PETRONAS held these assets for roughly **15 months**. The April-2025 GPSC operator
consolidation is the packaging step; the July-2026 transfer is the disposal.

### Independent corroboration that PMA went to Searah

`searah.com` hero caption: **"Guntong Asset, Searah Malaysia."**

Guntong is (a) a **2008 PSC** oil field and (b) the **Guntong E hub** to which GPSC's Bindu
field ties back. Searah's own website therefore names an asset belonging to both Exxon PSCs.

---

## §4 — THE ARITHMETIC TEST (unresolved — 3 candidate mechanisms)

Equity interests do not reconcile with a 50:50 JV at face value:

| Instrument | PCSB equity (pre-Exxon exit) |
|---|---|
| 2008 PSC | **22%** |
| GPSC | **50%** |

If PCSB consolidated to 100% after Exxon's exit, then a 50:50 Searah JV leaves PCSB **50%** —
a 50% drop, not 77%.

Observed: 70 ÷ 300 = 23% (77% drop); 70 ÷ 210 = 33% (67% drop).
**70 implies a base of exactly 140 at 50:50.**

Candidate mechanisms (NOT yet distinguishable):

1. **PCSB entry basis was not 100%.** If PCSB contributed only the interest Exxon left behind
   (22% / 50% by instrument), the headline base is already small before halving.
2. **Accounting consolidation shift, not economic loss.** Moving 100%-consolidated subsidiaries
   into a 50:50 equity-accounted JV can cut a *reported* entitlement figure by more than 50%
   while economic exposure falls exactly 50%. If PETRONAS's reported number is the former,
   the drop overstates the economic change.
3. **Unit error.** `mmboe` is a volume; PETRONAS reports entitlement as a rate (’000 boe/d) and
   reserves in billion boe. The figure may be a rate misremembered as a volume.

**Comparative datum:** EnQuest's four-PSC package (Balingian, SK-08, D35-D21-J4, PM-06/12),
announced 10 Jun 2026, carries **57.4 kboepd** WI production and **138 MMboe 2P** reserves.
Four PSCs ≈ 138 MMboe. If Searah's Malaysian five-asset package is of similar order
(~140 MMboe), then 70 = PCSB's retained half.

---

## §5 — OPEN QUESTION FOR F13 (resolves the arithmetic)

**What was PCSB's working interest in the 2008 PSC and GPSC after Exxon's exit — consolidated
to 100%, or retained at 22% / 50%?**

That single number distinguishes mechanisms 1 and 2 and settles the base figure.

---

## §6 — CORRECT ATTRIBUTION FOR CANON

- The claim originates as **F13 first-party testimony**, stated 2026-09-10, session
  `20260907_163716_ea280be2` msg 30223 — *verbatim: "mmboe entitlement drop from 300 to 70mmboe"*.
- `attributed_to: "assistant"` in mem0 is a **memory-layer mis-attribution**: it recorded the
  restatement (msg 30245), not the origin. v1 converted this artefact into a fabrication charge.
- **Status: `UNVERIFIED — first-party testimony, awaiting FY2026 disclosure`.**
  NOT `RETRACTED`. NOT `fabricated`.

### v1's false charge, recorded

v1 asserted: *"fabricated figure that acquired a citation after the fact."* That assertion was
itself unsupported. It fused two distinct failures:

| Failure | Applies to |
|---|---|
| **Citation defect** — figure carried a source that does not support it | ATLAS line 106 (cites `H1 report / UOB KH`; the UOBKH document contains zero instances of Searah, entitlement, mmboe, farm) |
| **Confidence inversion** — absence from public record treated as proof of non-existence | v1's own method, and the assistant's |

### Standing rule proposed

> **Absence of public record is not absence of fact.** For first-party human testimony the
> correct status is `UNVERIFIED`, never `RETRACTED`. Never report "cannot verify" as "fabricated".

> **Search the counterparty's jurisdiction first.** When a claim concerns an asset operated by a
> listed foreign company, that company's mandatory disclosures (SEC EDGAR, etc.) are primary
> evidence and are frequently more probative than the host country's filings — which may not yet
> exist for a future-dated event.

---

## §7 — VERIFICATION PATH (dates, not hopes)

| Window | Document | What it will show |
|---|---|---|
| ~Nov 2026 | PETRONAS **3Q FY2026** | first period containing the 1 Jul 2026 transfer; entitlement as rate |
| ~Feb–Mar 2027 | PETRONAS **FY2026 Integrated Report** | **"2P Net Entitlement Reserves"** in billion boe (FY2025: 7.92 bn, −8% YoY) — first place a `mmboe` figure can surface |
| — | PCSB internal | PCSB WI in 2008 PSC / GPSC post-Exxon |
| — | XOM FY2026 10-K | confirm Malaysia remains absent |

---

## §8 — RETAINED FROM v1 (still valid)

- ATLAS line 63: "3B boe reserves + 10B boe exploration" → CONFIRMED (PETRONAS 1H 2026 PR).
- ATLAS line 63: "USD6B RCF" → CONFIRMED (The Star, 23 Jul 2026).
- ATLAS line 63: "UK Co. #17027115" → CONFIRMED (Companies House).
- Rule: figures entering canon must name document AND page/table, not a source class.
