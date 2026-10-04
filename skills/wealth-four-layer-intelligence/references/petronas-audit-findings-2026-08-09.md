# PETRONAS dimensional audit findings — 2026-08-09 session

Companion to `petronas-fy2025-audited-2026-08-09.md` (balance-sheet data bank).
This file: the audit verdicts, corrected facts, and audit technique lessons from
the deep-dive session (net-debt question → dimensional orthogonal audit → 3 MakcikGPT articles).

## Corrected facts (user-verified — do not regress)

- **Tengku Muhammad Taufik contract: THIRD extension** (appointed Jul 2020;
  extensions 2023 and Aug 2026). An earlier draft said "second" — Arif corrected:
  "Wei ni kontrak kali ketiga la. Bukan kedua." Verify count before writing.
- **Group cash RM204.4B is audited** (Note 16). An early estimate of RM175B was
  wrong — always extract from the AFS balance sheet, never estimate.
- **Abang Johari (Premier Sarawak) is a politician, NOT a geologist.** Do not
  fabricate biographical detail; Arif caught this instantly.

## Core audit verdicts (FY2025 audited, KPMG PLT)

- **Group vs parent split is the whole story.** Group net cash ~RM82.8B looks
  healthy; the PARENT (the dividend-paying entity) is net-debt ~RM5–18B once
  intercompany receivables (RM101.3B, not recallable without disrupting subs)
  and financial guarantees (RM12.9B) are handled. Restricted cash RM2.1B +
  decommissioning-earmarked deposits RM22.8B further reduce free cash.
- **Financing pattern proves dividend-funding:** US$5B GMTN issuance Mar 2025
  while FY2025 CFFO−CAPEX−dividend still left ~RM13B surplus → the borrowing
  sits at the parent for dividend liquidity. Revolving credit drawdown doubled
  (RM10.4B → RM25.8B). Net borrowing swung −RM311M → +RM14.2B YoY.
- **Extraction:** dividend flat RM32B despite PAT −18% → payout 58% → 70.5%,
  breaking the 65% tripwire. FY2026 declared dividend cut to RM20B (board
  self-correction — cite as "system can correct itself" evidence, not just doom).
- **Underinvestment:** CAPEX −23% (RM51.9B → RM40.1B); net capex above
  depreciation collapsed RM15.2B → RM4.2B; reserve replacement ratio NOT
  disclosed in AFS (flag as omission every time).
- **Other expenses tripled** RM3.0B → RM8.6B (+187%) with no line-item detail.
- **FX translation loss RM18.8B** hit OCI/equity directly (equity −RM4.5B
  despite profit) — the hidden drain that never touches P&L.
- **Decommissioning provision RM48.9B** (28% due within 10y) + abandonment cess
  payables RM7.1B = future cash claims absent from net-debt headlines.
- **Off-balance-sheet framing:** the $30B GMTN program via PETRONAS Capital Ltd
  (Labuan SPV) is fully CONSOLIDATED and parent-guaranteed — it is NOT
  off-balance-sheet shenanigans. It is DRAWN capacity (in borrowings) plus
  UNDRAWN headroom (~RM128B ceiling). Arif accepted this correction; do not
  re-frame it as hidden debt, frame as headroom + circular parent financing.

## Context facts (2026)

- **Petros leak case:** ex-manager Mohd Khairul Akmal charged (Penal Code
  §203A(1)) for emailing "Q1 2024 Upstream Business Performance — Operational
  & Financial" to Petros CEO/CFO, 8 Jun 2024; whistleblower complaint 6 Dec
  2024; he had applied for Petros Head of Upstream Finance (RM25k/mo) first.
  Trial ongoing Jul–Aug 2026.
- **Petronas–Petros:** Sarawak granted Petros gas-aggregator rights 2024;
  Petronas filed at apex court Jan 2026; talks deadlocked.
- **SEARAH:** Eni–Petronas 50:50 upstream JV, est. mid-2026, 19 assets
  (14 Indonesia / 5 Malaysia), ~300k boe/d; assets reclassified held-for-sale
  (RM30.3B). EnQuest farm-in US$833M across 4 offshore PSCs. Both = balance-sheet
  cleanup that reads as "portfolio optimisation".
- **Subsidy paradox:** MoF monthly fuel subsidy RM700M (Jan 2026) → peak RM7.5B
  (Apr) → ~RM3.5B (Jun); HSBC projects RM58.4B for 2026 vs RM15B budgeted.
  Gov net fiscal position on oil = dividends − subsidy = deeply negative.
- **Predecessor contrast:** Wan Zulkiflee resigned 2020 over a Sarawak payment
  dispute with the PM (principle exit) — the standard MakcikGPT contrasts Taufik
  against. Reuters reported the resignation cause.
- **Reporting cadence:** half-yearly; FY2025 published 27 Feb 2026; H1 2026
  still unpublished as of 9 Aug 2026 — the "2026 data blackout" is itself a
  finding. No Q1/H1 group figures exist; label anything 2026 as UNKNOWN.

## Audit technique (reuse for any SOE deep-dive)

1. Balance sheet: read the COMPANY statement separately from the GROUP statement
   (both are in the AFS). Parent liquidity ≠ group liquidity.
2. Note 21 borrowings + Note 30 financing cash flows: drawdown/repayment by
   instrument reveals whether bonds fund capex or dividends.
3. Note 16 cash: split bank balances / deposits / restricted / held-for-sale.
4. Cross-check "other expenses", financing costs, OCI FX lines for hidden drains.
5. Six-dimension orthogonal table (bonds · cash trace · capex · opex · FX ·
   dividend) — the contradiction between dimensions IS the finding.
6. Deliverable ladder that worked: dimensional audit (chat) → APEX review →
   MakcikGPT article (persona, viral register) → publish via
   `arif-sites-ops` makcikgpt recipe.
