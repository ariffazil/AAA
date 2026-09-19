# Batch audit brief — read-only subagents across many control surfaces

## Why fan out

A federation-sized sweep — commit hooks, kernel gates, scheduled jobs, receipts, human-facing governors, skill-store instruments — exceeds one context. One subagent per surface, each writing its own report file, keeps evidence intact and lets the parent aggregate in code without holding the raw output.

## Rules to paste into EVERY child brief

Without these verbatim, children produce narrative instead of evidence.

```
DEFINITIONAL TEST for every control:
  THEATRE   = cannot withhold the action it claims to govern (always exit 0,
              always advisory, dry-run by default, or no caller at all)
  DISABLED  = could withhold but is configured so it never does
  BROKEN    = crashes or never executes (syntax error, missing module, dead path)
  REAL      = can and does withhold
  UNPROVEN  = no evidence either way  <- the default

COST TEST: did an agent pay work — tokens, commits, log lines, ceremony, retries —
for output identical to what it would have been without this control?

EVIDENCE LAW (non-negotiable):
  - every finding carries the EXACT command run and the observed output (trimmed)
  - every claim cites path and line number
  - every count must be measured in this session — never relayed from a document,
    never derived by arithmetic on numbers you did not measure
  - a control proven capable of blocking is reported REAL, even if it weakens the
    headline. Do not confirm a narrative; report what you could not determine as
    UNDETERMINED.

READ-ONLY: do not modify, create, move, delete or commit anything. Do not fix an
obviously broken script — report it broken. Even a repair you are certain of is out
of scope; the repair is a separate authorized act.
```

## Also require

- **The output path** for the child's report file, so the parent reads the artifact rather than trusting the summary.
- **An explicit read-only probe allowance**, or the child will refuse to run a diagnosis. Allow read-only GETs, `sqlite3 -readonly`, `systemctl status|show`, `ss -tlnp`. Forbid restarts, writes to any ledger, and config edits.
- **Permission to run a script only if its own docstring marks it read-only** — and to state that judgement in the report.
- **A required closing section of UNDETERMINED items.** Children otherwise drop what they could not prove, and the gaps are half the value.

## Aggregating

- A child's summary is a **self-report, not a witness.** Spot-check each headline count against that child's own report file before repeating it, and reconcile any child's number against a sibling's overlapping measurement.
- Expect children to be **blocked mid-audit by the very gates they are auditing.** That is a finding, not a failure — require them to record every block with the matched pattern, and collect those into the parent report.
- Rank the final report by **damage to an agent's ability to finish work**, not by count. Fold in what the children could not reach.
