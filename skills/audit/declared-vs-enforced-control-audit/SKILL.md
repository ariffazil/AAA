---
name: declared-vs-enforced-control-audit
description: "Use when a service claims a control you must verify."
---

# Declared vs Enforced Control Audit

## When to use

Any claim of the form *"requests to this endpoint require X"* — an approval gate, a signature, a scope check, a deny list, a rate limit, an authorization tier. Also whenever a spec, docstring, client library, or proposal template describes a control and you are about to repeat that description to a human, or rely on it yourself.

The trigger is always the same shape: **the claim lives in one layer (documentation, client code, a plan, operator copy) and the enforcement would live in another (server code, dispatcher, middleware, policy engine).** Establish which layer actually checks before you speak.

## Procedure

1. **Find the claim.** Enumerate every place the control is asserted: module docstrings, client-side helper signatures, READMEs, proposal/prompt templates, human-facing copy. Each is a claim, not evidence.
2. **Find the enforcement point.** Read the request path in the server: the dispatcher, the auth check, any middleware. Note which checks are actually *called* on the way to a protected action. A guard that exists but is never invoked is dead code, not a control.
3. **Probe the running artifact — do not audit the source alone.** Start it on an **isolated loopback port** with a **throwaway credential**; never the live credential, never through the live ingress or tunnel. Then issue one request per route and record status code and body.
4. **Include positive and negative controls.** At least one route that *must* be allowed and one that *must* be denied. If every probe returns the same refusal, you have learned nothing about the deny list — only that your credential is wrong.
5. **Diff declared against enforced, and record every `ABSENT` row.** The deliverable is a compact table: claim → where it could be enforced → probe result. The absent rows *are* the finding.
6. **Tear down.** Kill the probe process and confirm the port is free (`ss -lntp | grep <port>`). A stray probe server holding the real port is worse than no probe.

## Interpreting results

- **A rejection proves enforcement. A downstream error does not.** If a guarded action fails from *inside* the action — a missing binary, a timeout, a filesystem error — the request cleared every policy gate on the way in. That is evidence of **absence**, not of a working gate. Read where the failure originated, not just its status code.
- **The declared and enforced layers are written by different hands at different times.** Expect drift; do not smooth it over. Test the instance in front of you and do not generalize from a sibling service.
- **A control exercised only in the client is not a control.** If the caller is the only party checking the condition, any other caller — or the same caller with curl — walks straight past it.
- **Name-level verification is not verification.** A function that exists, a header that is sent, a parameter a helper demands: none of these mean the receiving side reads them.
- **Contract drift runs in the harmless direction too.** Clients routinely call paths the server does not route. Record those: a 404 on the client's own health check is a bug someone will otherwise rediscover from scratch.

## Reporting rules

- State what is **enforced**, then what is **declared but unchecked**, then the consequence in one sentence. Do not bury the gap under a list of the parts that work.
- Never describe a system as gated on a control you have not watched reject. If a bare token reaches a sensitive action, say the token is the whole lock.
- A gap is a finding to **record**, not a repair to perform inside the audit. Building the missing check is a separate, scoped mutation.
- Prefer running the subject's own verifier or self-test over summarizing it. Independent observation beats the author's assurance, always.

## Pitfalls

- **Never probe the live service.** Loopback port plus throwaway credential keeps the finding from costing a production side effect. A probe that captures a photo or mutates state on the real path has turned an audit into an action.
- **Bind the probe above 1024 and away from the real port.** The real service may be listening on this host; colliding with it fails confusingly or shadows it.
- **A uniform failure across all probes is a failed probe, not a hardened service.** Verify credential and port before concluding anything.
- **Record the probe set with the verdict.** A control verdict without the routes and status codes that produced it is an assertion, not a witness.
- **Re-run the probe after any fix.** `ENFORCED` written once and never rechecked is exactly how a repaired gap silently regresses.

## Support files

- `scripts/contract_probe.py` — runnable probe. Takes a JSON spec of routes (path, method, whether a token is attached, and whether each *should* be allowed or denied), hits a loopback base, prints the result table, and flags any probe whose outcome contradicts its declared expectation. Optionally diffs a source file against marker strings to show which checks exist in the code at all.
