# numeric-audit-mcp

Deterministic numeric re-computation and audit for intelligence briefs.

**Purpose — one error class, caught automatically:**

> a figure lifted from secondary literature and applied **outside its actual scope**.

A number can be quoted correctly from a real source and still be wrong, because it
belongs to a different exposure class. This server makes that detectable.

**Authority: ANALYSIS_ONLY.** Re-computes and reports. Never judges a bank, never
seals, never writes VAULT999.

## Layout

```
/root/AAA/mcp/numeric_audit/
  server.py                      # FastMCP server (7 tools, 1 resource) — HTTP :3013
  engine.py                      # exact-decimal engine; pure functions, no I/O
  rules/bnm_capital_rwa.json     # scope-tagged risk-weight registry (the knowledge)
  __init__.py
/root/AAA/numeric_audit/
  smoke_test.py                  # real MCP-client smoke test (starts the server)
  refs/cafib.txt                 # extracted text: BNM CAFIB (RWA), BNM/RH/GL 007-21
  refs/sa2024.txt                # extracted text: BNM SA for Credit Risk, 20 Nov 2024
  refs/brief.txt                 # extracted text: the audited brief
  smoke_output.json              # full machine-readable result packet
  run_output.txt                 # full smoke-test stdout
```

## Run

```bash
/opt/arifos/venv/bin/python /root/AAA/mcp/numeric_audit/server.py   # http://127.0.0.1:3013/mcp
/opt/arifos/venv/bin/python /root/AAA/numeric_audit/smoke_test.py   # starts server + calls all tools
```

## Tools

| Tool | What it does |
|---|---|
| `numeric_rule_lookup` | Look up a figure's canonical scope, basis, conditions and citation (doc, clause, date, file:line). Asking for `400` returns *everything* 400 could be and what discriminates them. |
| `numeric_replay_derivation` | Replay a derivation chain and return the full trace — every operand and result as an exact string so it can be re-run by hand. |
| `numeric_check_units_scale` | Lint percent-vs-fraction, bps-vs-percent, ~1000x million/billion drift, two claims of the same quantity disagreeing, and ratio claims with an undeclared basis. |
| `numeric_recompute_sensitivity` | Recompute a sensitivity table from an explicitly declared method; compare row-by-row against the published table. Makes a hidden net-of-replacement step visible. |
| `numeric_scope_check` | **The error-class catcher.** Is the cited figure being applied inside its canonical scope? |
| `numeric_audit_claim` | Claim vs recomputation. A numeric match never overrides a scope failure → `ARITHMETIC_OK_SCOPE_FAIL`. |
| `numeric_audit_brief` | Composite packet over claims + derivation + scope checks + sensitivity → one verdict. |

## Invariants

- All money/capital/ratio arithmetic is `decimal.Decimal`, `prec=60`. **Floats are rejected at the door** (`D()` raises `TypeError`), so no value can drift through binary float.
- Undeclared scope keys never silently match: an unmatched predicate contributes nothing and a figure that resolves to no number is returned as a **gap**, not as OK.
- An unregistered figure returns `FIGURE_NOT_IN_REGISTRY` / `UNVERIFIED` — never blessed by silence.

## Worked case — Bank Muamalat §5, 2026-09-15

**Claim:** risk-sharing exposures attract risk weights up to 400%, applied flatly to all
converted financing → ~RM3bn added RWA and ~RM450m new CET1 per RM1bn, at a 15% CET1 target.

**What the registry resolves the 400% to (BNM CAFIB, BNM/RH/GL 007-21):**

- §3.166 — 300% publicly traded / **400% to all other EQUITY HOLDINGS** (simple risk
  weight method, equity position risk). `cafib.txt:6790`
- Appendix V §8 — specialised-financing supervisory slotting **70 / 90 / 115 / 250 / 400**,
  where 400% is the **Default** category and requires a default finding. `cafib.txt:18024`
- §2.87 — musharakah: **100%** publicly traded equity holding, **150%** non-publicly traded,
  **150%** funds advanced to a joint venture, sub-contract weight for a musharakah with
  sub-contract. `cafib.txt:2148`
- §2.94 — mudarabah mirrors it. `cafib.txt:2282`
- §2.86(c) — diminishing musharakah that is an **asset receivable** is a *credit* exposure
  ("similar to Musharakah with Ijarah"); a retail home financing post-wa'd carries a
  counterparty weight — SA2024 §23.12 **20/25/30/40/90%**. `sa2024.txt:1177`
- §2.93 — mudarabah interbank attracts **credit** risk, *not* equity risk, despite
  contractual similarity. `cafib.txt:2270`

**Recomputed result (same brief inputs: base RWA 26.87188, capital 3.23, target 15%):**

| basis | new CET1 per RM1bn |
|---|---|
| 400% flat (claimed) | **RM0.450bn** |
| 150% (max in scope) | **RM0.075bn** |
| 100% (min in scope) | **RM0.000bn** |

The brief's table is **internally consistent** — `numeric_recompute_sensitivity` reproduces
rows 32.9 / 41.9 / 50.9 / 56.9 and 1.7 / 3.0 / 4.4 / 5.3 exactly, once a net-of-replacement
basis (400% − 100%) is assumed. Its arithmetic is sound; the input it consumed is out of scope.

Verdicts returned: `OUT_OF_SCOPE_FIGURE` (2.67x the largest in-scope weight for generic
risk-sharing financing; 4.44x for diminishing-musharakah retail financing), and
`ARITHMETIC_AND_SCOPE_FAIL` on the headline RM450m. Composite: `NOT_ZERO_BLOCKER`.

The **direction** of the brief's conclusion survives — risk-sharing is capital-expensive.
The **magnitude** — the number a reader quotes at a board — does not, by a factor of 6.

## Adding a rule

Append to `rules/bnm_capital_rwa.json`. A rule needs `figures_pct`, `canonical_scope`,
`applies_to` (pure-data predicates over the closed scope vocabulary), `basis`, `conditions`,
an `evidence_state`, and `source` with `doc`/`clause`/`issued`/`file`/`line`/`quote`.
A figure with no clause is worse than no figure.

DITEMPA BUKAN DIBERI.
