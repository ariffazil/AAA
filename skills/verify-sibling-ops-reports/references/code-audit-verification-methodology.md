# Code Audit Verification Methodology

> **Pattern:** Independent verification of code-level audit findings.
> **Source:** qwen-code FI-003 A2A Zen audit session (opencode-qwen-zen-20260812)
> **Key stat:** 62.5% of audit findings were false/misleading.

## The Claim-by-Claim Table

For each finding in a sibling's audit report, produce:

| # | Claim | Severity | Verdict | Evidence |
|---|---|---|---|---|
| 1 | (sibling's description) | (sibling's rating) | TRUE / FALSE / MISLEADING / PARTIAL / UNVERIFIABLE | (line reference + actual code context) |

### Verdict categories

| Verdict | Meaning | Example |
|---|---|---|---|
| TRUE | Claim accurate, finding real | No async 202 pattern — zero matches in codebase |
| FALSE | Claim contradicted by code evidence | print() in SSE handler = protocol, not spam |
| MISLEADING | Technically present but mischaracterized | "Legacy V2 formula" is explicitly labeled non-canonical |
| PARTIAL | Finding exists but severity wrong or scope overstated | Missing prefill is real but labels exist in other paths |
| UNVERIFIABLE | No code line cited, can't confirm or deny | Observer-decoder class mismatch with no reference |

### Scorecard

```
| Metric | Value |
|---|---|
| Total claimed findings | N |
| Verified TRUE | X |
| Partial | X |
| Unverifiable | X |
| FALSE / MISLEADING | X |
| Miss rate | (FALSE+MISLEADING) / N |
```

**Threshold:** If miss rate > 30%, flag as EPISTEMIC INFLATION — the audit
is adding noise, not signal. Report this to the user before routing findings
to APEX judge or A-FORGE.

## Epistemic Tags for Code Claims

Tag every verification with standard epistemic labels:

- `[OBS]` — Raw data: what the code actually does (function calls, control flow, data)
- `[DER]` — Derived: what the pattern implies (architectural classification, protocol intent)
- `[INT]` — Interpretive: what might be wrong based on pattern analysis
- `[SPEC]` — Speculative: root cause hypothesis if failure confirmed

## The Protocol-Syntax Distinction (Critical Pitfall)

The most common false-positive pattern in code audits: **classifying standard
protocol patterns as violations because they look wrong in isolation.**

Examples:
- `print()` inside an SSE handler = wire format (not debug spam)
- `sys.stderr` logging = correct diagnostics channel (not prod pollution)
- `observe_only=True` sync relay = validation gate by design (not blocking)
- Node.js gateway without FastMCP = correct — it consumes MCP, doesn't serve it

**Rule:** Before filing a code finding, trace the DATA FLOW, not just the syntax.
A `print()` in isolation is not a `print()` inside `emit_sse()` which is called by
an SSE streaming loop. Context changes everything.

## When to Trigger This Methodology

Use this when:
- A sibling agent pastes an audit report with severity ratings
- An opencode/qwen-code/claude-code session claims code violations
- Any audit report contains CRITICAL/HIGH findings that affect production code
- The user asks "is this audit correct?" or "execute this audit's fixes"

Do NOT use for:
- Simple ops/cleanup claims (use the base skill's webhook/directory probes)
- Configuration-only changes
- Documentation-only findings
