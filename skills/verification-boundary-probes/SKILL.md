---
name: verification-boundary-probes
description: "Use when a verifier or guard must be proven to fail."
version: 1.0.0
author: HERMES (forged)
license: internal
risk_tier: T1
floor_scope: [F1, F2, F4, F11]
capability_tier: fed-long-context
ecology_state: WARM
tags: [verification, testing, governance, evidence]
related_skills: [inbound-evaluation-intake, audit-ops, chokepoint-enforcement-audit]
---

# Verification Boundary Probes — prove the guard actually fails

## When to Use

- An outside reviewer, auditor or sibling agent reports that a check "always passes".
- You have just written or patched a `verify_*`, `check_*`, redactor, or response assembler.
- A gate is declared live and you need the counter-example that proves it fires.
- Someone asks "is this control real?" and the answer must be a failing input, not a passing one.

## Governing rule

A control is proven by the input it REJECTS. Every probe below is constructed to make the guard fail
on purpose; a guard that cannot be made to fail has not been shown to work.

Run probes with the project venv (`./.venv/bin/python`), on temp paths, with synthetic canaries only.
Keep the script — its output is the receipt and the rerun is the regression test.

## The three defects that survive casual review

### 1. Tolerant verifier — certifies rows it never read

A reader skips lines it cannot parse (`try: json.loads / except: continue`) and a `verify_*` function
consumes that reader. Verification then runs over the *parsed subset* and returns success for the
whole file.

Probe matrix on a temp store, N valid records:

1. valid chain → expect `True`
2. append one malformed line → expect `False`
3. file containing only malformed lines → expect `False`
4. truncate the FINAL record → expect `False`
5. corrupt a MIDDLE record → expect `False`

Step 5 usually already passes (the chain link breaks), which is exactly why the bug survives review —
the obvious corruption case works while the tail silently vanishes from the count.

Rule: strict parse in the verification path. A lenient mode, if needed for inspection, is a separate
explicitly named method, never the default.

### 2. Non-recursive redactor — leaks every secret inside a list

A walker recurses into `dict`, matches keys like `api_key|token|secret|password|authorization`, and
treats `list` only as a size cap (`[list:12 items]`), never recursing into elements.

Probe four shapes:

- `{"api_key": x}` → redacted
- `{"outer": {"api_key": x}}` → redacted
- `{"items": [{"api_key": x}]}` → redacted (this is the one that fails)
- `{"items": [x]}` with a bare secret string → redacted

Assert at the SINK — the payload as actually emitted to the transport or log — not the redactor's
return value. The leak is in what leaves the process.

### 3. Refusal carrying success narrative

A response assembler hard-codes happy-path `facts` ("session bound", "identity verified", "ready to
proceed") and `next_safe_action` ("proceed to <next verb>"), and a later stage flips `status` to
HOLD / error code MISSING_INPUT without clearing them. Structured verdict says refusal; prose says go.
An agent reading the prose obeys the prose.

Probe: call the tool through the REAL transport with required fields absent, then grep the RAW
response for the success strings. Assert on BOTH `structuredContent` and the text content — a check on
one leaves the other free to contradict it.

Rule: derive facts and next-action from the final input-contract outcome; on refusal keep the
missing-field correction and suppress every success claim.

## Grading a reported finding

| Probe result | Verdict | What to state |
|---|---|---|
| Reproduced on the deployed path | CONFIRMED | Quote the probe output; fix it |
| Reproduced only in the isolated component tested; production uses another path | SCOPE-LIMITED | Name the production caller, or its absence |
| Their probe was wrong / wrong version / wrong args | REFUTED | Show the corrected run, not an argument |
| Cannot reproduce and cannot explain why | UNMEASURED | Say so; never upgrade to "not a bug" |

## Pitfalls

- **A passing test proves nothing about the failing branch.** Every control needs a paired negative
  case (absent/supplied, valid/altered, dict/list) or it is a demo, not a test.
- **Corrupt-input tolerance is caller-specific.** Skipping a bad line is right in an ingest or
  telemetry reader and fatal in a verifier. When one helper serves both, the verifier inherits the
  wrong tolerance — split the helper, do not loosen the check.
- **Assert on the emitted artifact, not the function's return value.** Redactors, serialisers and
  response builders can return clean while emitting dirty.
- **Do not grade a finding by reading the reporter's description of the code.** Open the file and run
  the boundary; a report can be right about the symptom and wrong about the line.
- **Fix the general class, not the reported instance.** "Traverse list elements" generalises;
  "patch line 434" does not. Grep for sibling call sites before declaring the class closed.
