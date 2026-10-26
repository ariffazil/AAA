# LIMBAYONG FDP — RECONCILIATION LEDGER
## Which section used which number, and where they disagree
### HERMES · 19 October 2026 · built from each section's own HEADLINE, not from memory

---

## 1. THE DEFECT, MEASURED

Ten workstreams. Four different capex figures. Three different plateau figures.
Three different NPVs at the same oil price. Two different first-oil dates.

Every one of these is defensible **in isolation**. That is exactly why it is dangerous:
a board reading any single section would see a coherent document. Only when the pack is
assembled does the divergence appear — and by then each section has already been cited.

## 2. THE TABLE

| Parameter | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S7X | S8 | **CANON** |
|---|---|---|---|---|---|---|---|---|---|---|
| Capex, US$M | — | — | — | 600 (conv) | — | **4,050** | **2,900** | **3,170** | **2,900** | **4,050** |
| Oil rate, bopd | — | 35,000 fc | — | 27,500 hull | — | 40,000 | — | — | 40,000 | 40,000 np / 35,000 fc |
| Liquids, MMbbl | 134 P50 | 139 | — | — | — | 270 boe | 270.8 boe | — | 118 P50 | 139 |
| First oil | — | 2031 | — | — | — | **2030 Q4** | 2030 | 2029 | **2029** | **2030 Q4** |
| NPV10 @ $70, US$M | — | — | — | — | — | — | **+288** | **+1,113** | **+313** | **−580** |
| IRR | — | — | — | — | — | — | **12.3%** | **17.3%** | **12.1%** | **6.6%** |
| Breakeven Brent | — | — | — | — | — | — | $60 | $45 | $65 | **$85** |

**Seven rows. Six disagreements.** The pack was internally incoherent and that was not visible
until it was assembled.

## 3. WHY EACH NUMBER EXISTED — THE HONEST RECONSTRUCTION

| Divergence | Cause | Verdict |
|---|---|---|
| Capex 2,900 vs 4,050 | S7 and S8 ran **before** S6 delivered its WBS. Sequencing failure by me. | S6 wins. 4,050. |
| Capex 3,170 | My own first-pass bottom-up, built at 02:00 before any section existed | Retired |
| Capex 600 (S4) | FPSO conversion only — a legitimate **component**, not a total | OK, labelled |
| Oil 27,500 (S4) | Hull nameplate — a **constraint**, not the design | OK, labelled |
| Oil 35,000 (S2) | Derate of 40,000 for topsides weight/area on a 70 m cylinder | S2 wins for forecast |
| NPV +288 / +313 | Same capex, different model detail | Close enough; both retired below |
| NPV +1,113 | Consolidated basis, capex 3,170 | Retired with the capex |
| NPV −580 | **One engine, one assumptions file, capex 4,050** | **This one** |
| First oil 2029 | Inherited from the FID press framing, never re-derived | Retired |
| First oil 2030 Q4 | 51 months vs Kikeh 43 / GK 44 / Malikai 46 | S6 wins |
| Breakeven $60 / $65 / $45 / $85 | Four models, four answers | $85 from the one engine |

## 4. THE FIX, BUILT — NOT PROPOSED

Three files now exist. Any section that quotes a number must be reproducible from them.

| File | What it does |
|---|---|
| `ASSUMPTIONS.json` | The single source. Every number, with an evidence class and a basis. Versioned. |
| `engine.py` | The one engine. Reads only the assumptions file. No hardcoded numbers. |
| `reconcile.py` | The checker. Compares each section against the canonical set. |

**Output of `python3 engine.py`:**

```
capex_usd_m        4050.0
capex_per_boe      14.71
npv10_usd_m        -580
irr_pct            6.6
brent_npv0         85
brent_10pct        85
brent_15pct        111
peak_cash_usd_m    -4050
payback_year       2037
plateau_boe_d      58,300
first_oil          2030-Q4
fiscal_basis       PETRONAS consolidated (100% WI, no partner)
```

**The canonical verdict changes again, and this is the last time it will move without new data:**

> NPV10 **−US$580M**. IRR **6.6%**. Breakeven Brent **US$85**. 15% IRR needs **US$111**.

## 5. WHAT THE RECONCILER CAN AND CANNOT DO

`reconcile.py` greps prose for numbers. It **works** and it **is noisy** — it flags
legitimate component figures (a $600M conversion cost is not a $600M project). Running it
on this pack returns ~20 hits of which perhaps 8 are real divergences.

**That is the honest state of automated claim-checking over prose.** A regex cannot tell
"capex is US$4.05bn" from "conversion capex is US$600M". The durable fix is not a better
regex — it is **structured claims**: every section emits numbers as data (parameter, value,
unit, class, basis) rather than sentences, and the reconciler compares data to data.

Until sections emit structured numbers, `reconcile.py` is a smoke alarm that cannot tell
smoke from steam. Say that plainly rather than shipping it as a gate.

## 6. THE ORDER OF WORK, CORRECTED

The proposed order was: web evidence → engine + ledger → HERMES scan → GEOX → red team.

**That order has one error.** It puts the engine second. The engine must be **first**,
because the ledger is only meaningful if there is a consumer that will fail when it is
violated. Sequence:

1. **ASSUMPTIONS.json** — one file, every number, every class. *(done)*
2. **engine.py** — the only place a metric is computed. *(done)*
3. **Sections re-run through the engine** — each section quotes engine output, never its
   own arithmetic.
4. **reconcile.py as a smoke alarm**, not a gate. *(done, honestly limited)*
5. **Web evidence** — Sevan SSP300 spec, MMHE scope. Fills ledger gaps, does not
   override the engine.
6. **GEOX / CHRON / red team** — only after 1–4, or they will each re-invent a number.

## 7. WHAT THIS DOES NOT FIX

- **The conversion cost is still unknown.** One assumptions file cannot manufacture a
  number nobody has published. It can only make the gap explicit and singular.
- **No MCP closes this.** Not contradiction_scan, not claim_validate. See §8.
- **PETRONAS internal data stays inside PETRONAS.** If the ledger is ever populated with
  PCSB logs, DST or MISC costs, it cannot sit on this VPS or in any external MCP. Public
  data only. That boundary is not negotiable and is not a tooling problem.

## 8. THE TOOL TEST — DONE, AND IT FAILED

The proposal named `hermes_contradiction_scan` as the first must-run item. It exists and it
is callable. I tested it on this pack's actual contradictions.

**Test 1 — 11 claims including four capex values and three plateau values.** It found
**one** contradiction: NPV +288M vs −668M.

**Test 2 — the same claims stripped to 7, with no NPV pair.** It found **zero**
contradictions, on four contradictory capex figures and three contradictory plateau figures.

| Claim set | Contradictions in the data | Detected |
|---|---|---|
| Full 11-claim set | 4 (capex, plateau, NPV, first oil) | **1** |
| 7-claim set | 2 (capex, plateau) | **0** |

The tool anchors on an "oil_assumption" pattern and catches paired numeric mismatches. It
does not traverse a set of claims looking for shared-parameter divergence. **It is not the
fix for this defect**, and proposing it as "WAJIB jalan" would have produced a green light
that meant nothing.

Also checked, for the record: all eight federation MCP endpoints return HTTP 200 on
`/health`. That is transport liveness only — as this pack's own doctrine says, a 200 is not
a pass. A-FORGE exposes `forge_sandbox_run`, `forge_postgres` and `forge_judge_proxy`; those
are real and available if a deterministic compute lane is wanted.

---

*Every number in §4 is reproducible by running `python3 engine.py` in this directory.
Every divergence in §2 was read from the section files, not recalled.*
