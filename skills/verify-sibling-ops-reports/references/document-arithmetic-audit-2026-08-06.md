# Document arithmetic audit — Petronas Brazil sunk cost (2026-08-06)

Worked example for §4.5: a sibling pasted an audit of WEALTH's `Petronas_Brasil_Total_Sunk_Cost_v2_Aug2026.pdf` ("9 pages, Class: intelligence estimate (OBS/DER/INT), not audited financial statements"). The sibling's conclusion was directionally right; its named *mechanism* was wrong. The independent re-derivation from the primary document is what split the two.

## The claim being verified

Sibling said: "Appendix A has a range arithmetic problem… true optimistic low net sunk should be 6,185 − 450 − 2,500 = 3,235, not 4,235; true pessimistic high should be 7,427 − 450 − 1,500 = 5,477, not 4,477. So the table uses same-column subtraction for low/high rather than true optimistic/pessimistic range logic."

## Step 1 — extract the primary document (never work from the sibling's transcription)

```bash
python3 -c "
import pymupdf
doc = pymupdf.open('...pdf')
for i, page in enumerate(doc):
    print(f'===== PAGE {i+1} ====='); print(page.get_text())
"
```

## Step 2 — re-run every derived row from the document's exact numbers

Appendix A5 as published (MID / LOW / HIGH):

| Row | MID | LOW | HIGH |
|---|---|---|---|
| Gross sunk | 6,711 | 6,185 | 7,427 |
| Less TV/EM-III sale | −450 | −450 | −450 |
| Less TV/EM-III cashflow | −2,060 | −1,500 | −2,500 |
| **Net sunk (published)** | **4,201** | **4,235** | **4,477** |
| Portfolio value held | −3,950 | −3,500 | −4,500 |
| **Real economic loss (published)** | **~200** | **−265** | **977** |

Re-derivation:

- MID net sunk = 6,711 − 450 − 2,060 = **4,201** ✓ (matches)
- LOW net sunk = 6,185 − 450 − 1,500 = **4,235** ✓ (matches — NOT an arithmetic error)
- HIGH net sunk = 7,427 − 450 − 2,500 = **4,477** ✓ (matches)

**Verdict on axis 1 (internal consistency): PASS.** The columns are internally consistent — each derived row equals its own column's inputs. The sibling's stated mechanism ("same-column subtraction" as a bug) is wrong: that's just… how columns work.

## Step 3 — scenario-logic check (axis 2)

The LOW/HIGH columns are **independent input ranges per row**, not optimistic/pessimistic scenario bounds. Real scenario pairing:

| Scenario | Gross | CF recovery | Net sunk |
|---|---|---|---|
| Optimistic (low gross + best recovery) | 6,185 | 2,500 | **3,235** |
| Midpoint | 6,711 | 2,060 | **4,201** |
| Pessimistic (high gross + worst recovery) | 7,427 | 1,500 | **5,477** |

- Published band: 4,235 → 4,477 = **$242M wide**
- True scenario band: 3,235 → 5,477 = **$2,242M wide** (~10× wider)

**Verdict on axis 2: FAIL — scenario-logic compression.** The derived loss tail also widens: real economic loss true range ≈ −$1,265M (gain) to +$1,977M vs published −265 to +977. Midpoint thesis ("roughly break-even") survives; the downside tail is ~2× worse than the document implies.

## Step 4 — anchors vs model outputs (OBS vs INT)

External verification of the document's factual anchors (web_search per claim):

| Claim in document | External anchor | Grade |
|---|---|---|
| OGX deal $850M rescinded Oct 2013 | Business Times / The Edge / Kinibiz | OBS ✅ |
| TV/EM-III 50% bought 2019 ~$1.3B | Petronas media release | OBS ✅ |
| TV/EM-III sold back 2026 at $450M | Petrobras 6-K (SEC), Brazil Energy Insight | OBS ✅ |
| Sépia 21% entry ~$873M (R$14.55B comp) | OEDigital — Petrobras received R$14.55B from TotalEnergies/Petronas/QP | OBS ✅ |
| Mola-1 dry (water found, Macabu Fm) | BNamericas | OBS ✅ |
| C-M-661 returned to ANP | BNamericas | OBS ✅ |
| Sépia-2 FID / P-85 | TotalEnergies + Seatrium releases May 2024 | OBS ✅ |
| Brazil Law 14,596/2023 transfer-pricing | Planalto.gov.br | OBS ✅ |
| TV cashflow ~$2.06B | No public source (Petronas doesn't disclose Brazil P&L) | INT |
| Sépia portfolio NPV ~$4.0B | Model output, not observed | INT |
| Petronas tax exposure $85–280M | Modelled from peer CARF rulings (Shell R$437M, Petrobras R$1.24B) | INT |

8/11 anchors OBS-verifiable; the 3 INT items are model outputs by design. The document's self-label ("intelligence estimate") is accurate — grade it as such.

## The reply shape that worked

1. Verification matrix table (claim → source → OBS/INT)
2. The arithmetic re-derivation showing the sibling was RIGHT on the conclusion, WRONG on the mechanism: "the PDF's column-level arithmetic is internally consistent — it's the *combination* logic that's wrong, not the subtraction itself"
3. True scenario table (optimistic/mid/pessimistic)
4. Verdict: PARTIAL-SEAL on direction ("not catastrophic"), HOLD on the precise number and range until the scenario table is fixed.

## Reusable rules

- **Conclusion ≠ mechanism.** A sibling's verdict can survive while its diagnosis is wrong. Grade both independently; the fix differs by mechanism.
- **Extract and re-derive from the primary source.** The sibling's transcription of the numbers is a self-report; the PDF's own rows are truth.
- **LOW/HIGH independent ranges ≠ optimistic/pessimistic scenarios.** Whenever a document presents a low/mid/high table, run the pairing check (best-with-best, worst-with-worst) before accepting any stated uncertainty band.
- **Financial documents that self-label "estimate" grade their own anchors as INT** — don't inflate model outputs to OBS just because the prose reads confidently.
