# Board Power-Node & Shadow-of-the-Chairman Analysis

Recipe for the recurring Arif chapter: "evaluate BOD power node capture for X and shadow of the chairman." Goal: show where power actually sits before the numbers are trusted.

## Steps
1. Enumerate board seats from the official site (`company.com/about/our-leaders` or equivalent). Note exact titles, not just names.
2. Cross-check every name against the parent's leadership page (`parent.com/about-us/our-leaders`). **Dual-hat** = same person holds an executive role at the parent AND a seat on the subsidiary board.
3. Classify each seat: Executive chair vs independent non-executive; parent-executive (dual-hat); operator (CEO/MD); unverified.
4. Verify independent-director status. If the site serves placeholder bio text ("Lorem ipsum") for named directors, record it as [OBS] on the site defect + [UNK] on the person's status. Never invent a bio.
5. Board size vs capital commitments: 5 seats against a >US$30bn 2030 capex ambition is a structural flag worth stating.
6. Search equity-sale reports (minority stake, C&I carve-out). They reveal how governance gets diluted and who the counterparty is — a board chaired by the parent's CEO controls the terms of its own dilution.
7. Model the power node: who approves what, who can challenge, what breaks if the dual-hatted chair changes.
8. Render a node-map chart (matplotlib circles + dashed connectors + legend box; palette navy #0e1a2b / gold #c9a227 / red = dual-hat / green = operator / orange = unverified). Pattern lives in the session script `gen_bod_chart.py` (forge_work/gentari-2026/).
9. Tag everything [OBS]/[DER]/[INT]/[UNK].

## Gentari worked example (2026-08-06)
- Board: 5 seats. Chairman = YM Tan Sri Tengku Muhammad Taufik (also President & Group CEO, PETRONAS — dual-hat). Director = Liza Mustapha (also EVP & Group CFO, PETRONAS — dual-hat). CEO/MD = Sushil Purohit (ex-Wärtsilä Energy President; CEO since 1 Jan 2023; 30+ years in global energy sector; sole non-Malaysian on board; sole person without a PETRONAS prior-line). Note: some secondary sources tag him ex-First Solar — this is wrong; Wärtsilä is correct. Directors = Girish Nadkarni (Independent per Tracxn; LinkedIn header "Saudi Energy", Weston CT; Harvard MBA 1988 — Investment Committee member = transactional, not oversight-orthogonal). Ashok Belani (Independent per Tracxn; ex-SLB New Energy EVP, Stanford Eng 1989 — currently Woodside Energy board member, creating a hydrogen-offtake adjacency). "Lorem ipsum" placeholder bios on gentari.com/about/our-leaders for Nadkarni and Belani as of 2026-08-06 — site defect, not a problem to invent around.
- Shadow: the chair of Gentari IS the parent's executive CEO → chair/CEO separation collapsed; single-point approval corridor; "entrepreneurial autonomy" real in operation, narrower in governance.
- Capital path: Bloomberg Oct 2024 — PETRONAS mulling minority stake sale in Gentari (US$300–500M); separate reports of up-to-50% Gentari India C&I unit sale ~US$400M. Petronas spokesperson: "nothing to add."
- Verdict shape: governance is the binding constraint (governance_capacity axis scored 1.00/3), not financials — the lock sits on the governance axis.

## Output shape
Body chapter with node-map chart + 5-seat table (seat / name / role / concurrent position / power implication) + "shadow of the chairman" red box + minority-stake gold box + structural-weakness bullets; Appendix table of bios with epistemic tags.
