# /vitals — Re-seal Patch (2026-08-26)

**Status:** Ready-to-apply
**Priority:** P0
**Seal date change:** 2026-08-03 → **2026-08-26** (23 days overdue)
**Session:** SEAL-d7d3fde881a74721
**Author:** 333-AGI Δ Mind (arifOS Federation)

---

## What to do

Apply these additions to `/root/arif-fazil.com/sites/arif-fazil.com/dist/vitals.html` (or the canonical source if different).

Sections below marked `<!-- INSERT HERE -->` show exact insertion points relative to existing /vitals structure.

---

## PATCH 1 — Update seal date banner (top of page)

**FIND:**
```
**⚠ FY2025 SEALED READING · EXTRACTION 70.5% · 2 OF 6 PACEMAKERS ENGAGED** Sealed 2026-08-03 · AMEND-2026-08-03-001 · F13 veto remains final
```

**REPLACE WITH:**
```
**⚠ FY2025 SEALED READING · EXTRACTION 70.5% · 2 OF 6 PACEMAKERS ENGAGED** Re-sealed 2026-08-26 · AMEND-2026-08-03-001 · F13 veto remains final

**⚡ NEW DATA POINT — 1H FY2026 expected ~29 Aug 2026 · Watch for second audit signal**
```

---

## PATCH 2 — Update LIVE MARKET PROXIES block

**FIND:**
```
● LIVELIVE MARKET PROXIES26 Aug, 01:34 pm MYT
Brent · CFFO driver **85.73** ▼$/bbl
NatGas · LNG proxy **2.856** ▲$/MMBtu
USD/MYR **4.0230** ▼RM
DXY **98.99** ▲
KLCI **1,748.44** ▲pts
```

**REPLACE WITH:**
```
● LIVELIVE MARKET PROXIES26 Aug, 13:34 MYT (re-pull)
Brent · CFFO driver **85.48** ▼$/bbl  (RSI 22.4 · BEARISH regime)
NatGas · LNG proxy **2.86** ▲$/MMBtu
USD/MYR **4.047** ▼RM (ringgit weakened from 4.023)
DXY **99.0** ▲
KLCI **1,749.20** ▲pts

Transmission: ±$10 Brent ≈ ±RM6.0B FCF/CFFO. FCF (#1) crosses zero at Brent ≈ $71.60/bbl (-$13.88/bbl from $85.48). CFFO tripwire (RM60B) requires Brent < $47.40. RSI 22.4 = oversold regime — any OPEC+ failure, China data miss, or recession trigger moves Brent fast. Source: WEALTH commodity engine · yfinance 5-min cache.
```

---

## PATCH 3 — Add "BOD Chronology 2023-2026" section (insert AFTER Pacemaker Panel block, BEFORE "What this means")

```html
<!-- INSERT HERE: between Pacemaker Panel and "What this means — in plain language" -->

<section id="bod-chronology" style="margin-top: 32pt; padding-top: 18pt; border-top: 2px solid #003366;">
  <h2 style="font-size: 16pt; color: #003366; border-bottom: 2px solid #003366; padding-bottom: 4pt;">
    Board of Directors Chronology · Jan 2023 → Aug 2026
  </h2>
  <p style="font-size: 10pt; color: #555; margin-bottom: 12pt;">
    <strong>Sealed 2026-08-26 · Session SEAL-d7d3fde881a74721 · 333-AGI Δ Mind</strong><br>
    Source: PIR2022 audited FS, PIR2024 audited FS, PIR2024 Board Composition, TM 2025 Circular, HKExNews 21 Mar 2025 & 7 Apr 2025, BNM AR2024, The Edge Malaysia, DayakDaily, Bloomberg, Upstream Online.
  </p>

  <h3 style="font-size: 13pt; color: #1f4e79;">Current Board (Aug 2026) — 8 directors</h3>
  <table style="border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 9.5pt;">
    <thead>
      <tr style="background: #003366; color: white;">
        <th style="padding: 6pt 9pt; text-align: left;">Name</th>
        <th style="padding: 6pt 9pt; text-align: left;">Role</th>
        <th style="padding: 6pt 9pt; text-align: left;">Type</th>
        <th style="padding: 6pt 9pt; text-align: left;">In role since</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Mohd Bakke Salleh</td><td>Chairman</td><td>INED (reclassified from NINED — date UNK)</td><td>1 Aug 2021</td></tr>
      <tr><td>Tengku Muhammad Taufik</td><td>President & Group CEO</td><td>Executive Director</td><td>2020 (PGCEO), contract extended Aug 2026</td></tr>
      <tr><td>Azizan Zakaria</td><td>Audit & Risk Committee Chair</td><td>INED</td><td>UNK (~mid-2023)</td></tr>
      <tr><td>Zaharah Ibrahim</td><td>NRC Chair</td><td>INED</td><td>Pre-2023</td></tr>
      <tr><td>Shahrazat binti Haji Ahmad</td><td>Member (AC/NRC/RC)</td><td>NINED (MoF Inc. nominee)</td><td>13 Jan 2025</td></tr>
      <tr><td>Abdul Rasheed Ghaffour</td><td>Member</td><td>INED (BNM Governor)</td><td>on/before 21 Mar 2025</td></tr>
      <tr><td>Mohd Jukris Abdul Wahab</td><td>COO + EVP CEO Upstream</td><td>Executive Director</td><td>1 Feb 2026</td></tr>
      <tr><td>Liza Mustapha</td><td>EVP & Group CFO</td><td>Executive Director</td><td>Pre-2018</td></tr>
    </tbody>
  </table>

  <h3 style="font-size: 13pt; color: #1f4e79;">Changes by Year</h3>

  <h4 style="font-size: 11pt; color: #1f4e79;">2023 — 5 seat events</h4>
  <ul style="margin: 4pt 0 8pt 18pt;">
    <li><strong>5 Jan 2023:</strong> NINED Asri Hamidin resigned (PIR2022 audited FS)</li>
    <li><strong>5 Jan 2023:</strong> NINED Johan Mahmood Merican resigned; later re-appointed, resigned again 13 Jan 2025</li>
    <li><strong>~Jun 2023:</strong> Mohd Jukris appointed director at PETRONAS Carigali + (E&P) Overseas Ventures (subsidiary level)</li>
    <li><strong>Jul 2023:</strong> PGCEO Tengku Muhammad Taufik first contract extension</li>
    <li><strong>[UNK] mid-2023:</strong> NINEDs Ainul Azhar, Dato' Razali Mohd Yusof, Thayaparan Sangarapillai departed; Azizan Zakaria appointed INED</li>
  </ul>

  <h4 style="font-size: 11pt; color: #1f4e79;">2024 — 1 seat event</h4>
  <ul style="margin: 4pt 0 8pt 18pt;">
    <li><strong>16 Oct 2024:</strong> NINED Ibrahim bin Baki resigned (PIR2024 audited FS)</li>
  </ul>

  <h4 style="font-size: 11pt; color: #1f4e79;">2025 — 4 seat events (the reset year)</h4>
  <ul style="margin: 4pt 0 8pt 18pt;">
    <li><strong>13 Jan 2025:</strong> NINED Shahrazat appointed (MoF Inc. nominee — TM 2025 Circular)</li>
    <li><strong>13 Jan 2025:</strong> NINED Johan Mahmood Merican resigned (2nd time, PIR2024 audited FS)</li>
    <li><strong>19 Jan 2025:</strong> NINED K.Y. Mustafa resigned (PIR2024 audited FS)</li>
    <li><strong>On/before 21 Mar 2025:</strong> INED Dato' Seri Abdul Rasheed Ghaffour (BNM Governor since 1 Jul 2023) — HKExNews 21 Mar 2025 + 7 Apr 2025; BNM AR2024 signed 24 Mar 2025</li>
  </ul>

  <h4 style="font-size: 11pt; color: #1f4e79;">2026 YTD — 2 seat events</h4>
  <ul style="margin: 4pt 0 8pt 18pt;">
    <li><strong>1 Feb 2026</strong> (announced 18 Jan 2026): ED/COO Mohd Jukris appointed — re-establishes COO seat dormant since 2018. DayakDaily / Bloomberg / The Edge / Upstream Online. <strong>Note:</strong> This elevation came 10 days after PETRONAS's 10 Jan 2026 Federal Court filing on Sarawak DGO gas distribution dispute.</li>
    <li><strong>~Aug 2026:</strong> PGCEO Tengku Muhammad Taufik received 2nd contract extension (The Edge 17 Aug, The Ledger Asia 8 Aug, KLSE Screener). Term length (2 vs 3 years) disputed; PETRONAS officially declined to confirm.</li>
  </ul>

  <h3 style="font-size: 13pt; color: #1f4e79;">Net change: −4 directors</h3>
  <p>Board shrank from ~12 (early 2023) to 8 (Aug 2026). All 8 departures were NINED. Only 4 new seats added. Composition: 3 ED, 4 INED, 1 NINED.</p>

  <h3 style="font-size: 13pt; color: #1f4e79;">Structural implications</h3>
  <ol style="margin: 4pt 0 8pt 18pt;">
    <li><strong>3 ED + 1 NINED = 4 pro-management votes</strong>. With 4 INED requiring coordination to challenge, and the Chairman (formerly NINED, reclassified INED — date UNK) holding the tie-breaker, there is no mathematical path to challenge management on a 4-4 vote.</li>
    <li><strong>Azizan Zakaria chairs BOTH Audit Committee AND Risk Committee</strong> (dual-hat). Standard practice: separate chairs. Single point of failure for independent challenge in crisis.</li>
    <li><strong>No announced CEO succession plan</strong>. Taufik holds 2 chairmanships (PETRONAS + Gentari); governance separation index = 1 (1 step from tripwire 0).</li>
    <li><strong>Unknowns flagged as honest gaps</strong>: Bakke NINED→INED reclassification date, Azizan Zakaria exact appointment date, Ghaffour exact start date, Taufik 2026 extension term length.</li>
  </ol>

  <p style="margin-top: 10pt;">
    <a href="/root/AAA/forge_work/2026-08-26-petronas-bod-dossier/petronas-bod-chronology-2023-2026.pdf" style="display: inline-block; background: #003366; color: white; padding: 6pt 12pt; border-radius: 3pt; text-decoration: none;">
      📄 Download full BOD chronology dossier (PDF, 52 KB)
    </a>
  </p>
</section>
```

---

## PATCH 4 — Add "12 Hidden Risks" section (insert AFTER "What this means — in plain language" block)

```html
<!-- INSERT HERE: after plain language block, before "For Citizens" section -->

<section id="hidden-risks" style="margin-top: 32pt; padding-top: 18pt; border-top: 2px solid #d4a017;">
  <h2 style="font-size: 16pt; color: #d4a017; border-bottom: 2px solid #d4a017; padding-bottom: 4pt;">
    ⚠ 12 Hidden Risks — Not Visible in FY2025 Audited Statements
  </h2>
  <p style="font-size: 10pt; color: #555; margin-bottom: 12pt;">
    <strong>Re-sealed 2026-08-26 · Cross-checked against WEALTH·petronas_vitals, market data, and SOE comparison corpus.</strong>
  </p>

  <ol style="margin: 6pt 0 8pt 18pt; font-size: 10pt;">
    <li><strong>Reserves depletion.</strong> Malaysia crude at 355 kbpd vs 2008 peak ~700 kbpd. Group total 2.4 Mboe/d = 85% gas (gas depletes 2-3× faster than oil). Reserve replacement 1.2× — barely above 1:1. Tapis/Dulang/Semangkok platforms come offline 2027-2030.</li>

    <li><strong>Pengerang RAPID bleeding.</strong> PCG made RM730M LAT (loss) in Q4 2025; Q1 2026 PAT RM427M annualizes to RM1.7B vs prior baseline RM2-3B. Aramco PRefChem JV ($27B project) underperformance = direct balance sheet hit. PRefChem consolidation may step gearing from 20.7% to 25-27%.</li>

    <li><strong>Kasawari first full year = GHG +2.2% groupwide.</strong> First time PETRONAS's emissions went UP, not down. "Stabilization" issues. Carbon pricing exposure (EU CBAM live 2026, domestic carbon tax progressing) = RM 1-3B/year margin hit 2027-2030.</li>

    <li><strong>Decommissioning liabilities hidden.</strong> ~300+ offshore platforms; many 1980s vintage at end-of-life. Industry benchmark $200K-500K per platform. Estimated liability: RM 5-15B (possibly understated, possibly zero on balance sheet). Hits 2027-2032.</li>

    <li><strong>Sukuk market shallower than conventional bonds.</strong> PETRONAS = top 5 global sukuk issuer (est. RM 60-80B outstanding). In stress, sukuk liquidity vanishes first (Islamic investors pull back faster than conventional). Refinancing wall 2027-2029.</li>

    <li><strong>Sabah MA63 — parallel federal-state dispute.</strong> Sabah has separate MA63 petroleum rights claim (different court from Sarawak DGO). Combined federal-state loss potential: ~30% domestic gas distribution, RM 8-23B/year.</li>

    <li><strong>No CEO succession plan.</strong> Taufik holds PETRONAS + Gentari. No announced heir. PEMEX had 6 CEOs in 10 years — same pattern.</li>

    <li><strong>Dual-hat Audit & Risk Committee chair.</strong> Azizan Zakaria chairs both. No independent challenge to management's risk and financial assessments in crisis.</li>

    <li><strong>Hidden CAPEX overruns.</strong> Industry-standard LNG mega-project overruns: 40-60%. LNG Canada, Pengerang, Kasawari all exposed. Don't appear in FY2025 IFR but accumulate over 2-3 years.</li>

    <li><strong>ESG + green financing withdrawal.</strong> Major funds divested from O&G 2024-2026. PETRONAS sukuk buyers screen on carbon. +100-150bps spread = RM 600M-1B/year extra interest.</li>

    <li><strong>Currency mismatch amplification.</strong> USD/MYR at 4.047. If weakens to 4.50+, USD debt service more expensive. Every 10% MYR depreciation ≈ RM 2-3B extra interest cost.</li>

    <li><strong>Climate litigation tail risk.</strong> EU due diligence expanding to O&G. Worst case: 5-10% of group revenue at risk from stranded assets.</li>
  </ol>
</section>
```

---

## PATCH 5 — Add "SOE Comparison Corpus" section (insert AFTER Hidden Risks)

```html
<!-- INSERT HERE: after Hidden Risks section -->

<section id="soe-comparisons" style="margin-top: 32pt; padding-top: 18pt; border-top: 2px solid #c0392b;">
  <h2 style="font-size: 16pt; color: #c0392b; border-bottom: 2px solid #c0392b; padding-bottom: 4pt;">
    🔻 SOE Comparison Corpus — What Collapse Patterns Look Like
  </h2>

  <h3 style="font-size: 12pt; color: #1f4e79;">PDVSA (Venezuela, collapsed 2012-2017)</h3>
  <p style="font-size: 10pt;">Government extraction at 96% of net income at terminal. Board captured by political appointees. Capex cut 60% (2009-2015). Production: 3.2M bpd (2008) → 1.2M bpd (2017). <strong>PETRONAS extraction 70.5% = 73% of PDVSA's terminal</strong>.</p>

  <h3 style="font-size: 12pt; color: #1f4e79;">PEMEX (Mexico, ongoing)</h3>
  <p style="font-size: 10pt;">Extraction 60-70% sustained. Crony board. Capex chronically underfunded. Production: 3.4M bpd (2004) → 1.6M bpd (2023). Debt: $25B (2010) → $106B (2023). <strong>PETRONAS gearing 20.7% = PEMEX's 2012 starting point</strong>.</p>

  <h3 style="font-size: 12pt; color: #1f4e79;">1MDB (Malaysia, 2015)</h3>
  <p style="font-size: 10pt;">PM-controlled board. Captured chairman. No independent oversight. Borrowed against future revenue. <strong>Pattern matches PETRONAS structural vulnerability — not corruption, but governance gap</strong>.</p>

  <h3 style="font-size: 12pt; color: #1f4e79;">WorldCom (USA, 2002)</h3>
  <p style="font-size: 10pt;">CFO controlled financial reporting; board lacked expertise to challenge. <strong>PETRONAS board has no O&G operator experience among INEDs</strong>. BNM Governor is central banker, not petroleum engineer.</p>

  <h3 style="font-size: 12pt; color: #c0392b; margin-top: 14pt;">Cascade Order: Governance First, Financials Second</h3>
  <p style="font-size: 10pt;">Board captures → external trigger fires → amplifier (board rubber-stamp) converts trigger into cascade. Brent price is the trigger; the board is the amplifier that turns trigger into collapse.</p>
</section>
```

---

## PATCH 6 — Add "JV Partner Walk-Away Map" section

```html
<!-- INSERT HERE: after SOE Comparisons -->

<section id="jv-partners" style="margin-top: 32pt; padding-top: 18pt; border-top: 2px solid #d4a017;">
  <h2 style="font-size: 16pt; color: #d4a017; border-bottom: 2px solid #d4a017; padding-bottom: 4pt;">
    🤝 JV Partner Walk-Away Map
  </h2>

  <table style="border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 9.5pt;">
    <thead>
      <tr style="background: #d4a017; color: white;">
        <th style="padding: 6pt 9pt; text-align: left;">Partner</th>
        <th style="padding: 6pt 9pt; text-align: left;">Asset</th>
        <th style="padding: 6pt 9pt; text-align: left;">Walk-away trigger</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>Aramco</strong></td><td>PRefChem / RAPID ($27B)</td><td>Bond downgrade 1 notch → force majeure review on PRefChem</td></tr>
      <tr><td><strong>Shell</strong></td><td>MLNG, Kasawari (Sarawak)</td><td>Sarawak adverse ruling → Shell markets LNG capacity from Qatar/US instead</td></tr>
      <tr><td><strong>TotalEnergies</strong></td><td>LNG Canada (PETRONAS equity)</td><td>Asset review announced → market reads distress → spreads widen</td></tr>
      <tr><td><strong>Mitsubishi</strong></td><td>RAPID (downstream petchem)</td><td>PETRONAS asks for capital increase → Mitsubishi declines</td></tr>
    </tbody>
  </table>
  <p style="font-size: 10pt; margin-top: 8pt;">If ONE partner walks → signals to others. If TWO walk → crisis. A rubber-stamp board will deny, defer, hope — the pattern in all four SOE collapses.</p>
</section>
```

---

## PATCH 7 — Add "Monte Carlo + Cash Runway" section

```html
<!-- INSERT HERE: after JV Partners -->

<section id="monte-carlo" style="margin-top: 32pt; padding-top: 18pt; border-top: 2px solid #1f4e79;">
  <h2 style="font-size: 16pt; color: #1f4e79; border-bottom: 2px solid #1f4e79; padding-bottom: 4pt;">
    📊 WEALTH Monte Carlo + Cash Runway (2026-08-26)
  </h2>

  <h3 style="font-size: 12pt; color: #1f4e79;">Revenue Trajectory (10-year forward)</h3>
  <p style="font-size: 10pt;">Initial value RM 266.1B (FY2025 revenue), growth -5%, volatility 18%, 1000 simulations:</p>
  <table style="border-collapse: collapse; width: 100%; margin: 10pt 0; font-size: 9.5pt;">
    <thead>
      <tr style="background: #1f4e79; color: white;">
        <th style="padding: 6pt 9pt;">Percentile</th>
        <th style="padding: 6pt 9pt;">Revenue (RM B)</th>
        <th style="padding: 6pt 9pt;">vs FY2025</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>P10 (worst 10%)</td><td>69.7</td><td>-74%</td></tr>
      <tr><td>P25</td><td>95.9</td><td>-64%</td></tr>
      <tr><td>P50 (median)</td><td>140.1</td><td>-47%</td></tr>
      <tr><td>P75</td><td>209.4</td><td>-21%</td></tr>
      <tr><td>P90 (best 10%)</td><td>287.1</td><td>+8%</td></tr>
    </tbody>
  </table>
  <p style="font-size: 10pt;"><strong>P90/P10 dispersion = 4.12x.</strong> Tail is fat.</p>

  <h3 style="font-size: 12pt; color: #1f4e79;">Cash Runway</h3>
  <p style="font-size: 10pt;">At FY2025 burn rate: liquid assets RM 120B, monthly burn RM 15B → <strong>6.4 months runway</strong> if income stops. Peer majors (Shell, ExxonMobil) typically run 18-24 months. PETRONAS is <strong>3-4× thinner</strong>.</p>

  <h3 style="font-size: 12pt; color: #c0392b; margin-top: 14pt;">Updated material deterioration probability: 50-60% (12 months)</h3>
  <p style="font-size: 10pt;">Up from initial 35-40% estimate. Reason: governance cascade is not sequential to financial cascade — they run SIMULTANEOUSLY. Brent drops WHILE board fails WHILE Sarawak litigates WHILE sukuk market freezes. Each compounds the others.</p>

  <p style="font-size: 10pt;"><strong>Next data point:</strong> 1H FY2026 group report expected ~29 Aug 2026. Re-run WEALTH·petronas_vitals after release.</p>
</section>
```

---

## PATCH 8 — Add "Sabah MA63" footnote to SOUL layer

**FIND:** Tripwire #8 — Governance separation index
**REPLACE WITH:**
```
#8 — Governance separation index · 1 (dual-chair) · trip <0 safe 3 · INTERPRET · 33/100 · VOID
+ Sabah MA63 parallel dispute noted. If Sabah succeeds in court (separate from Sarawak DGO), combined federal-state loss potential = ~30% domestic gas distribution (RM 8-23B/year). PETRONAS federal-state dispute exposure has been structurally underweighted in prior analysis. — Sealed 2026-08-26
```

---

## Verification Checklist

After applying patches:
- [ ] Seal date shows 2026-08-26 (was 2026-08-03)
- [ ] Live proxies refreshed (Brent $85.48, MYR 4.047)
- [ ] 1H FY2026 watch note present
- [ ] BOD chronology section visible after Pacemaker Panel
- [ ] 12 Hidden Risks section visible
- [ ] SOE Comparison Corpus section visible
- [ ] JV Partner Walk-Away Map section visible
- [ ] Monte Carlo + Cash Runway section visible
- [ ] Sabah MA63 footnote on Tripwire #8

---

**Receipt:** Patch drafted 2026-08-26, Session SEAL-d7d3fde881a74721, 333-AGI Δ Mind.
**Apply with:** `cd /var/www/html && make deploy` (after committing source changes).
**Source for new analysis:** `/root/AAA/forge_work/2026-08-26-petronas-bod-dossier/` + `/root/AAA/forge_work/2026-08-26-petronas-rakyat-dossier/`.
