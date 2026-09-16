# NOC Void Forensics — Propaganda Matrix & Peer Benchmarking

**Proven:** 2026-08-29, PETRONAS 1H FY2026 analysis
**Framework:** WSJ-level investigative methodology for institutional reports

## Void Classification

When analyzing any corporate report, classify what's NOT disclosed:

| Type | Description | Detection Method |
|---|---|---|
| **Structural void** | Not required by accounting standards | Compare IFR content vs full annual report |
| **Strategic void** | Required but omitted or deferred | Compare vs peer disclosure practice |
| **Legal void** | Suppressed for legal/commercial sensitivity | Compare vs competitor disclosure |
| **Narrative void** | Would contradict official narrative | Cross-reference claims vs audit data |

## The Propaganda Matrix

For any corporate report, build a two-column table:

| Official Claim | Evidence | Verdict |
|---|---|---|
| [From press release / CEO statement / IR deck] | [From financial statements / primary data / peer comparison] | TRUE / FALSE / MISLEADING / FRAUD / UNSUBSTANTIATED |

### Verdict Definitions
- **TRUE:** Claim matches evidence across multiple metrics
- **FALSE:** Claim contradicted by evidence from same company's financial statements
- **MISLEADING:** Claim technically true but omits material context
- **FRAUD:** Claim uses visual/mathematical manipulation to deceive
- **UNSUBSTANTIATED:** Claim has no supporting evidence in disclosures

## Knowledge Graph Node Classification

When building institutional analysis, classify ALL findings:

| Node Type | Tag | Definition | Example |
|---|---|---|---|
| Propaganda | [P] | Official claim contradicted by evidence | "PAT +4% resilient" (shareholder PAT -3.9%) |
| Reality | [R] | Evidence-confirmed finding | Crude production -17% YoY |
| Void | [V] | Deliberately or structurally undisclosed | Sarawak Federal Court risk (zero disclosure) |
| Accounting | [A] | Non-cash / composition effect | PRefChem RM14.8B loss recognition |
| Consequence | [C] | Downstream impact of R or V | NCI capture of growth (shareholder PAT -4%) |
| Transition | [T] | What the institution is becoming | Wealth-generating NOC → wealth-absorbing shock buffer |

## Peer Benchmarking Technique

### Step 1: Pull Actual Data
Never accept IR's published chart. Pull quarterly data from SEC EDGAR via yfinance:
```python
import yfinance as yf
t = yf.Ticker('XOM')  # or SHEL, CVX, BP, TTE, COP, EQNR
qis = t.quarterly_income_stmt
# Extract Revenue and Net Income, compute PAT margin
```

### Step 2: Recompute All Ratios
- PAT margin = Net Income / Revenue (use same definition as company)
- ROE = Net Income / Shareholders' Equity
- Debt-to-Equity = Total Debt / Total Equity (standard, not custom)
- CAPEX/Revenue = Capital Expenditure / Revenue
- Free Cash Flow = CFFO - CAPEX

### Step 3: Detect Visual Fraud
Check the IR chart for:
- **Truncated axis:** Does y-axis start at 0 or at a non-zero value?
- **Band type:** Is the peer band min-max or interquartile? Is median shown?
- **Positioning:** Is the company at the correct position within the band?
- **Headline accuracy:** Does "in line" match the actual position?
- **Re-plot with full axis:** The distortion is often the fraud

### Step 4: Build Truth Table

| Peer | Metric A | Metric B | Rank |
|---|---|---|---|
| [actual data from filings] | | | |
| **Peer Average** | | | |
| **Company (reported)** | | | |
| **Company (ex-items)** | | | |

If the company is #1 reported but LAST ex-items, the gap is the composition effect.

## WEALTH MCP Session Pitfall

WEALTH tools require `session_id` parameter for ALL calls. Without it:
```json
{"verdict": "VOID", "error_code": "SESSION_REQUIRED", "errors": ["L11 AUTH: session_id required"]}
```
Always pass `session_id` when invoking WEALTH MCP tools. This is a session-gate, not a bug.

## The One-Sentence Test

After building the full analysis, ask:
> "If I could only say one sentence about this institution's true state, what would it be?"

The one-sentence test forces synthesis over enumeration. If the sentence contains more than 30 words, you haven't synthesized enough.

---

*DITEMPA BUKAN DIBERI ⚒️*
