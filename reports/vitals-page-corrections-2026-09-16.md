# arif-fazil.com/vitals — Verified Correction List (2026-09-16)

**Scope:** public page analysing the author's employer. Every item below is verified against a primary
source or against the WEALTH code that produced it. Nothing here is interpretation.
**Prepared by:** i-ARIF (Hermes) + OPENCLAW (KVM4), two independent clients, KVM8 as system of record.
**Status:** local file only. The public page was **not** edited — external surface requires F13 go.

---

## P0 — factually wrong about a real institution

### 1. "Zero independent NEDs" is false. PETRONAS lists four.

**Page says** (two places):
- *"Governance capacity 1.00/3 (zero independent NEDs)"*
- *"board without independent NEDs, governance score 1.00/3 (0.33) [INT] — based on 0 indep NEDs"*

**Primary source** — `https://www.petronas.com/about-us/our-leaders`, fetched 2026-09-16 by two clients
independently (i-ARIF ~10:59Z, OPENCLAW 11:04Z). Board of 8 directors:

| Name | Role | Independent? |
|---|---|---|
| Tan Sri Dato' Seri Mohd Bakke Salleh | Chairman | **Independent NED** |
| YM Tan Sri Tengku Muhammad Taufik | President & Group CEO | Executive |
| Azizan Zakaria | Chair Audit + Chair Risk | **Independent NED** |
| Tan Sri Zaharah Ibrahim | Chair Nomination & Remuneration | **Independent NED** |
| Datuk Dr Shahrazat binti Haji Ahmad | Member Audit/Nom&Risk | Non-Independent NED |
| Dato' Seri Abdul Rasheed Ghaffour | — | **Independent NED** |
| Mohd Jukris Abdul Wahab | COO / EVP & CEO Upstream | Executive |
| Liza Mustapha | EVP & Group CFO | Executive |

**4 of 8 independent (50%)** — above the one-third benchmark the tool itself uses. All three essential
committees exist and **all are chaired by INEDs**. Two Company Secretaries (Azizi Md Ali, Norwankiss Mohd
Ridhuan Kau) are listed separately and are **not** directors — so the tool's
`secretaries_as_directors` capture check does not apply either.

### 2. Root cause of item 1 — traced to code, not to research error

The number did not come from research. It came from a tool bug:

- `capital_diagnose mode=governance_capacity` reads `p.get("board_members") or []`
  (`canonical.py:806-816`). An **empty or malformed payload is indistinguishable from a genuinely
  empty board.**
- Observed: `capacity_score: 0.0`, `board_composition.total_members: 0`,
  `recommendation: "Emergency appointment of independent NEDs required"`, **`confidence: 0.0`**.
- The tool emitted emergency governance advice at zero confidence, and the page promoted it to a
  `[INT]`-tagged datapoint and then to a fired pacemaker.

**Re-run with PETRONAS's actual published board** (receipt `7968c98d`, 11:02:52Z):

| field | empty payload (what the page used) | real board |
|---|---|---|
| `capacity_score` | 0.0 | **0.9217** |
| `independence_score` | 0.0 | **1.0** |
| `quorum_status` | INSUFFICIENT | **ADEQUATE** |
| `stress_capacity_gap` | +0.4667 | **−0.1217** |
| `committee_score` | 0.0 | **0.85** |
| `essential_committees_found` | none | audit, risk, nomination, remuneration |
| recommendation | "emergency appointment required" | **(none)** |

**Chain:** tool bug → datapoint → page thesis → governance pacemaker "ENGAGED" → "2 of 6 pacemakers
ENGAGED" → the "1974 social contract is collapsing NOW" verdict. One empty list moved the headline.

Note: `wealth_core/petronas_vitals.py` (369 lines) contains **zero** occurrences of `independent`, `NED`,
`board`, or `governance_capacity`. So the governance claim cannot originate from the vitals engine — it
entered from `governance_capacity` output, which is the only place those numbers exist.

### 3. Knock-on: two sealed readings on the page rest on item 1

- *"governance_capacity 1.00/3"* — should be **2.77/3** (0.9217 × 3) on real board data.
- *"2 of 6 pacemakers ENGAGED"* — the governance pacemaker should not have fired. The count drops to 1
  (the 70.5% extraction pacemaker, which **is** arithmetically correct — see §"What is still correct").
- The page's own exit condition is *"extraction < 55% PAT × 2 consecutive audits AND governance ≥ 2.0/3"*.
  On corrected data the **governance limb is already satisfied** (2.77 ≥ 2.0). Only the extraction limb
  remains binding. That materially changes the exit-timing conclusion the page draws.

---

## P1 — numbers that don't follow from the page's own inputs

### 4. "FCF crosses zero at Brent ≈ $71.60/bbl" is a hardcoded constant, and its own formula disagrees

From `wealth_core/petronas_vitals.py`:

```python
def compute_petronas_vitals(tripwires=None, weights=None, current_brent_usd: float = 84.10):
...
    if t["id"] == 1:   # FCF (11.6B RM, tripwire <0, ±$10 Brent = ±6B FCF)
        driver_dist = round((float(t["now"]) - float(t["trip"])) / 0.6, 2)   # $12.50/bbl away
```

Three mutually inconsistent numbers for the same quantity:

| source | value | how |
|---|---|---|
| page (and the code comment) | **$71.60** | 84.10 (hardcoded default Brent) − 12.50 (hardcoded comment) |
| the formula in the same function | **$64.77** | (11.6 − 0) / 0.6 = 19.33; 84.10 − 19.33 |
| external reviewer, anchored at the Brent where FY2025 FCF was earned (~$69) | **~$50** | 69 − 19.33 |

The comment `$12.50/bbl away` does not equal what the line below it computes (`19.33`). And
`current_brent_usd` defaults to **84.10** — a stale constant, not a live reading. Since `:3457/api/oil/*`
returns HTTP 500 (verified 11:00Z) and `:3457/api/gold/ticker` returns **404** (route absent), no live
commodity price reaches this engine at all.

**Consequence:** every Brent-linked tripwire distance on the page is anchored to a hardcoded 84.10, while
the page separately cites live Brent at ~$100.60 (12 Sept) and an external source puts it at $109.21
(15 Sept). The distance-to-tripwire figures are therefore stale by ~$25–38/bbl of anchor error.

### 5. Brent itself is stale, and "war premium, not structural" is interpretation presented as observation

- Page: *"Brent ~$100.60 (Houthi escalation Sep 8 — war-driven, not structural)"*, header dated 12 Sept
  2026 07:00 — **4 days stale** as of 16 Sept.
- External reviewer: Brent **$109.21** on 15 Sept, +20% over the month; 52-week high $120.88 on
  30 Apr 2026 — i.e. elevated prices have persisted ~5 months, which weakens "war-driven, not structural."
- The page does tag this `[INT]` in one place. The header summary does not carry the tag.

### 6. Base scenario pairs FY2025 PAT with a Brent that did not produce it

Base case: PAT **RM45.4B** at Brent **$85**. FY2025 PAT was earned at materially lower Brent. The scenario
table presents the pair as a coherent base case; it is a current-price PAT bolted onto a historical-price
earnings figure.

### 7. Two different values for one number

- Top box: *"Rugi downstream **RM15.2B**"*
- Detail: *"1H26 NON-CASH HIT **RM14.8B**"* (PRefChem accumulated losses)
- Page's own source list says **RM14.8B**. The 15.2B figure has no stated source.

### 8. Smaller inconsistencies (all verifiable on the page)

- Results date given as **31 Aug** in the source list; coverage cited as **28 Aug** (The Star / FMT). Both
  dates appear; the page does not reconcile them.
- Sensitivity table cites **"IFR disclosure"** as source while its own footnote says figures are
  `[SPEC] non-scoring` and `INTERPRET`. A `[SPEC]` number cannot be sourced to an audited disclosure.
- Profit attributable to shareholders **MYR 22.73B** (slightly below 1H25) is not mentioned, while
  headline PAT RM27.2B (+4%) is. These are different measures; presenting only the favourable one is
  selection, and the page's own `[OBS]/[DER]` discipline should have caught it.

### 9. Sealed IDs have no ledger trail

Page cites `AMEND-2026-08-03-001` and several "sealed" readings. `capital_ledger mode=query` finds
**no entry** for either PETRONAS or that amendment ID (verified by both clients). Either the seals were
never written to VAULT999, or they live somewhere the organ cannot read. "Sealed" on a public page should
resolve to a retrievable record.

---

## What is still correct (do not over-correct)

Verified arithmetic, all consistent:

- 32.0 / 45.4 = **70.48%** ≈ page's "70.5%" extraction ✓
- exit threshold: 20 / 36.4 = **54.94%** < 55% ✓ (page's RM36.4B is right)
- CFFO 85.2 = PAT 45.4 × **1.877** ≈ page's "×1.88" ✓
- Brent $100 sustained → 20/55 = 36.4%, 20/65 = 30.8% ≈ page's "31–36%" ✓
- Brent $70–80 → PAT 30–35B → 57–67% ≈ page's range ✓
- 1H26 declared figures (PAT RM27.2B +4%, EBITDA RM56.8B, CFFO RM47.5B, capex RM41.4B, dividend RM20B
  declared) — external reviewer confirms against The Star / PETRONAS release ✓
- FY2026 dividend RM20B = 38% cut from RM32B ✓

The extraction thesis itself — *"a reinvestment emergency, not a solvency emergency"* — survives. What
does not survive is the governance pillar, and the governance pillar is half the "two pacemakers engaged"
claim.

---

## Suggested minimal edit set (if F13 authorises touching the page)

1. Replace "zero independent NEDs" with **4 of 8 independent NEDs (50%)**, citing
   petronas.com/about-us/our-leaders, and correct governance capacity to **2.77/3**.
2. Drop the governance pacemaker from "ENGAGED"; restate as **1 of 6**.
3. Restate the exit condition: governance limb **already satisfied**; only extraction limb binding.
4. Either fix the $71.60 anchor or remove the figure — it derives from a hardcoded Brent 84.10 and a
   comment that contradicts its own formula. If kept, label it `[SPEC]` with the anchor stated.
5. Reconcile RM14.8B vs RM15.2B to one number (the sourced one: **14.8B**).
6. Re-date the header. The Brent-dependent conclusions are 4 days stale and Brent has moved ~$9 since.
7. Move "war-driven, not structural" out of the summary into the `[INT]` block, and note the 5-month
   duration of elevated prices.
8. Either produce the ledger trail for `AMEND-2026-08-03-001` or relabel those readings as unsealed.

Items 1–3 are factual corrections about a named real institution on a public page and should not wait.

---

## Non-technical note, recorded once and not repeated

The page carries a personal exit-timing section addressed to the author by name ("Untuk Arif",
"the machine has spoken. Now you decide.") on a public site analysing his employer, and frames the machine
as issuing the verdict. Two frictions worth naming, both his call and not mine to act on:

- It reads as the machine deciding, which inverts the page's own footer ("WEALTH computes · arifOS frames ·
  Human decides") and the federation's stated ceiling (`555_COMPUTE_ONLY`).
- Employment-context exposure: a public, dated, named exit-timing plan concerning one's own employer.

No recommendation is made here. This is a disclosure of something observed, not advice.

---

*Evidence base: PETRONAS primary source (fetched twice, two clients); `wealth_core/petronas_vitals.py`;
`wealth_mcp/tools/canonical.py`; `capital_diagnose` receipts `afca2243` (empty board) and `7968c98d`
(real board); `capital_ledger mode=query`; `capital_market mode=oil` HTTP 500 ×3 and `mode=gold`
8.4-day-stale snapshot (receipts `a0ecc545`, `6ed45f8a`); external reviewer's Brent and 1H26 sourcing.*
