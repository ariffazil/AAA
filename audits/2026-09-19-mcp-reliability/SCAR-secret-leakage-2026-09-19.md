# SCAR — Secret-value leakage in audit transcript (2026-09-19)

> **Status:** Metabolized. Binding on every FI coding agent that runs an audit in transcript-bearing mode.
> **Severity:** MEDIUM (one transient transcript leak, no persistence to disk or chat).

## What happened

During the `MCP Reliability Audit (2026-09-19)`, I used a bash presence-check:

```bash
echo "BRAVE_API_KEY: ${BRAVE_API_KEY:+PRESENT}${BRAVE_API_KEY:-MISSING}"
```

The intent was to print **presence** without **value**. The actual output **leaked the value** because `${VAR:+...}` only expands a value in the positive branch — but when `set -a; . vault.env` had loaded the variable, the second expression `${VAR:-MISSING}` was empty, so the variable's value appeared in the chat transcript.

This is exactly the defect pattern the F13 standing rule names: "Never paste secrets in chat or VAULT999."

## Why it slipped past doctrine

- The pattern `${VAR:+...}${VAR:-MISSING}` **looks like a presence check**. It is not — when `VAR` is set, both branches use `$VAR`, and the `:-` branch silently contributes the value.
- I had not yet metabolized this pattern into the witness-zen doctrine. Doctrine says "never paste secrets"; doctrine did not name the bash idiom.

## The correct pattern (binding)

```bash
# ✅ SAFE — length-only, value never expanded into stdout
echo "BRAVE_API_KEY: ${BRAVE_API_KEY:+PRESENT (length=${#BRAVE_API_KEY})}${BRAVE_API_KEY:-MISSING}"

# ✅ ALSO SAFE — explicit redaction marker
echo "BRAVE_API_KEY: $( [ -n "${BRAVE_API_KEY+x}" ] && echo "PRESENT (length=${#BRAVE_API_KEY})" || echo "MISSING" )"

# ❌ FORBIDDEN — value expansion in presence-check branch
echo "BRAVE_API_KEY: ${BRAVE_API_KEY:+PRESENT}${BRAVE_API_KEY:-MISSING}"

# ❌ FORBIDDEN — direct value print
echo "BRAVE_API_KEY: $BRAVE_API_KEY"
```

## Regression fixture

To prevent recurrence, every audit-script under `/root/AAA/audits/` MUST grep for the forbidden pattern and fail if found:

```bash
# /root/AAA/audits/lint-no-secret-leak.sh (proposed)
forbidden='\${[A-Z_]+:\+[^\}]*\}\$\{[A-Z_]+:-'
if grep -rE "$forbidden" /root/AAA/audits/ /root/AAA/scripts/ 2>/dev/null; then
  echo "FAIL: secret-leakage pattern found"
  exit 2
fi
```

This is the **scar-to-test** primitive the external audit named as Opportunity #3 — first concrete instance.

## Sealed receipt

```
scar_id    : SCAR-SECRET-LEAKAGE-2026-09-19
detected   : 2026-09-19T16:09+08:00 (this audit, transcript-bearing)
reporter   : codex (FI-005) — self-metabolized
constraint : all future audits must use length-only presence pattern
test       : /root/AAA/audits/lint-no-secret-leak.sh (proposed)
severity   : MEDIUM
supersedes : none
```

DITEMPA BUKAN DIBERI ⚒️ — pain metabolized into constraint.
