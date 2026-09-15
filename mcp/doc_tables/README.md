# doc-tables-mcp

FastMCP server that extracts **tables** from PDFs and HTML as **structured JSON cell
matrices** (never mangled text), and **reconciles an extracted total against the total
printed in the source**.

Built because linear text extraction (`pdftotext -layout`, naive `page.extract_text()`)
destroys table geometry — columns interleave, numbers re-associate with the wrong row
labels — and that failure already put a wrong number into a published brief.

## Why it exists

`pdftotext -layout` on BNM CAFIB page 425 (Appendix VIa derivative worked example) is the
canonical failure case. The tool `doc_tables_text_mangle_check` renders the *same bbox*
two ways and diffs the numbers, so the failure is reproducible evidence rather than
folklore. On that page the cell matrix and the layout-text rendering do **not** produce
the same number sequence.

## Authority

`READ_ONLY`. This organ parses documents. It never mutates them, never writes VAULT999.

## Layout

```
/root/AAA/mcp/doc_tables/
├── server.py            FastMCP server (all tools + extraction engine)
├── run.sh               launcher — pins /opt/arifos/venv/bin/python (never system python)
├── smoke_mcp_client.py  real MCP client smoke test over streamable-http
└── _test_core4.py       direct engine test (fast, no server needed)
```

Shebang and launcher both point at `/opt/arifos/venv/bin/python`, where `pdfplumber
0.11.10`, `lxml`, `bs4`, `pandas` and `fastmcp 3.4.6` already live. No new venv was
needed; nothing was installed into system python.

## Run

```bash
/root/AAA/mcp/doc_tables/run.sh            # http://127.0.0.1:38500/mcp
```

Env overrides: `DOC_TABLES_HOST`, `DOC_TABLES_PORT`, `DOC_TABLES_TRANSPORT=http|stdio`.

## Tools

| Tool | Purpose |
|---|---|
| `doc_tables_health` | Identity, interpreter, dep versions, tool list. |
| `doc_tables_list` | Inventory tables (page, shape, score, caption, bbox) **without** cells. Use to find the right page. |
| `doc_tables_extract` | **The main tool.** Returns 2-D `cells` + `markdown` + `page` + `bbox` + strategy + shape. |
| `doc_tables_reconcile` | Re-derives the printed total from component cells. `RECONCILED` / `MISMATCH` / `UNRECONCILED`. |
| `doc_tables_text_mangle_check` | Region-scoped witness: cells vs layout-text, numbers lost/invented/reordered. |

Every returned number is traceable to a page, a bbox and an extraction strategy.

## Accuracy design (the parts that matter)

1. **Four extraction strategies per page** (`lines`, `lines_text`, `text_lines`, `text`),
   then arbitration — not first-match.
2. **Ruled dominance.** A candidate found by the `lines` strategy is direct geometric
   evidence (visible rules). Borderless `text` candidates overlapping it yield. Without
   this, a prose blob that splits words mid-token (`Upon signi|ng of wa`d`) outscores the
   real table on raw cell count. This defect was found and fixed against CAF SA p36.
3. **No candidate is discarded before arbitration.** An early coarse dedupe once evicted
   the true ruled table in favour of a higher-scoring blob.
4. **Numeric-backbone guard.** Page-scale borderless candidates with no data column
   (`This policy do | c | ument set | s out`) are refused outright, so a narrative page
   returns *no* tables rather than prose dressed as a table.
5. **Label columns are never summed.** A label column is detected by digit density
   (~0.04) vs value columns (~0.5), so `Capital requirement (8%)` contributes 0, not 8.
6. **Accounting negatives only when the whole cell is parenthesised** — `(1,234)` is
   −1234; `Capital requirement (8%)` is not −8.
7. **`value_mode='last'`** reads the final literal in a cell, correct for worked examples
   like `440,000 x 50% = 220,000` → `220000`.

## Reconciliation semantics

Orientation is auto-detected:

- **total_column** — a column headed `Total`; each row's other value cells must sum to it.
- **total_row** — a row labelled `Total`; the cells above must sum to it.

Verdicts:

- `RECONCILED` (`published_safe: true`) — printed total equals the sum of stated components.
- `MISMATCH` — at least one derived-vs-printed check failed. Do not publish.
- `UNRECONCILED` — **not a pass.** No total was located (Void Guard: absence of evidence is
  not evidence of correctness).

Tolerances default to `abs=0.5`, `rel=0.5%`, both overridable.

## Verified output

CAFIB p397 supervisory slotting risk weights — `lines` strategy, 2 rows × 5 cols:

| Strong | Good | Satisfactory | Weak | Default |
| --- | --- | --- | --- | --- |
| 70% | 90% | 115% | 250% | 400% |

CAFIB p425 Appendix VIa, reconciled `RECONCILED`, 3/3 checks, delta 0.0 on all three:

| Type of instrument | CCPRS | IPRS | Total |
| --- | --- | --- | --- |
| Credit equivalent exposure | 440,000 | 40,000 | 480,000 |
| Risk-weighted asset (50%) | 220,000 | 20,000 | 240,000 |
| Capital requirement (8%) | 17,600 | 1,600 | 19,200 |

## Proof

```bash
/root/AAA/mcp/doc_tables/run.sh &
/opt/arifos/venv/bin/python /root/AAA/mcp/doc_tables/smoke_mcp_client.py
```

Calls all five tools through a real `mcp` SDK `ClientSession` over streamable-http and
exits non-zero on failure.
