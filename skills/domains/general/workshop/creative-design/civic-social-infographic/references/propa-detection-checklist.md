# Propa Detection Checklist — Civic Inputs

When a user hands you a corporate PR page, government narrative, or "feel-good" infographic and asks for a reality version, run this audit BEFORE building. Each pattern comes from a real Aug 2026 PETRONAS session.

## The 7 Patterns

### 1. Y-axis truncation
**What it looks like:** Line/bar chart starts at 100 instead of 0. Trend looks explosive.
**Why it's propa:** A 27% rise on a chart from 100→128 reads as a 28% gain visually. On a chart from 0→128 it reads as the same number that already existed as a small slice. Same data, different story.
**Counter:** Rebuild with `ax.set_ylim(0, max*1.15)` or honest `<div>` bars from 0.

### 2. Strategic omission
**What it looks like:** "PETRONAS cash RM204B!" headline. Body never mentions the USD5B bond issued the same quarter.
**Why it's propa:** The contradiction is the actual story. Hiding one half of a paired fact lets the other half shine.
**Counter:** Always pair on-book cash with on-book debt issued in the same period. Render both as hero numbers side-by-side.

### 3. Categorical error
**What it looks like:** "Cash RM204B = 60% of Malaysia's federal operational expenditure." Comparing corporate balance-sheet cash to federal income-statement spending.
**Why it's propa:** Different entities, different accounting basis. Government can only access PETRONAS cash via dividend extraction — which is the actual story.
**Counter:** Reframe as: "Cash is corporate asset, not federal revenue. The only path from RM204B cash to federal budget is via dividend extraction — which is exactly the governance issue."

### 4. Symmetric narrative substitution
**What it looks like:** "Cash RM204B AND bond issued USD5B" presented side-by-side without admitting contradiction.
**Why it's propa:** Both true individually. Together they ARE contradictory (have cash, why borrow?). The narrative pretends they coexist as if both reasonable — but one is a symptom of the other.
**Counter:** Call out the contradiction explicitly: "Cash di-bank RM204B. Hutang USD5B. Mana logik?"

### 5. Scale-less aggregation
**What it looks like:** "Dividen RM32B–RM50B." A wide range that doesn't match any single year's actual figure.
**Why it's propa:** Implies the upper bound as plausible. Audited FY2025 was RM20B. The range inflates by 2.5x.
**Counter:** Always cite the actual audited number, with year. "FY2025 dividen: RM20B (board decision 27/2/2026), turun 38% dari FY2024 RM32B."

### 6. Anonymous dossier
**What it looks like:** Heavy analytical document with no author, no institution, no contact. Compiled from various sources without attribution.
**Why it's propa:** Plausible deniability. Anyone can dispute any claim. No accountability for fabrication.
**Counter:** Add a visible source list. If specific claims have no source, mark them `[UNVERIFIED]` rather than asserting.

### 7. Selective highlight / tactical good news
**What it looks like:** Government pension fund paid out on time for 12 consecutive months. No mention of the underlying fiscal deficit or debt service charges consuming 16.8% of federal revenue.
**Why it's propa:** A genuine achievement (timely payments) is weaponised to imply fiscal health while the structural problem gets no airtime.
**Counter:** Acknowledge the genuine achievement in its own box. Then put it in context: "Pension paid on time. Meanwhile debt service charges consume 16.8% of federal revenue. Both true."

## Audit Process

Before building the reality infographic:

1. List every numerical claim in the source
2. For each, find the audited or public-record anchor (FY report, board decision, Companies House filing)
3. Flag discrepancies (inflated range, mislabelled category, omitted pair)
4. Build the counter-frame using only the verified numbers + their implied contradiction

## What to never do

- Don't "balance" by adding a softening paragraph. The contradiction is the point.
- Don't assert numbers the source didn't cite. If you can't verify a number in 2 minutes, drop it or mark unverified.
- Don't attack the named individuals unless F6 maruah is preserved (institutional critique, not personal defamation).
- Don't fabricate source citations. If the audited anchor doesn't exist, say so.

## Source-quality hierarchy

1. Audited Integrated Financial Report (FY2025 IFR for PETRONAS-class entities)
2. Company announcement at regulator (Bursa Malaysia, Companies House UK, SEC EDGAR)
3. Joint announcement / press release at company HQ
4. Tier-1 media (Reuters, Bloomberg, FT, Astro Awani, Bernama with editor traceability)
5. Industry analysis (Wood Mackenzie, Rystad, S&P Global — paywalled but cited)
6. Wikipedia / encyclopedia (only for orientation, never as primary)
7. Forum / blog / opinion (skip)

If a number only exists at level 6-7, do not include it as fact in the infographic.
