# Reality-First Gap Repair — Receipt Shape

When you fix gaps in a live system (cron pipeline, federation organ, recurring render), the seal document should answer five questions and nothing else. Anything else is theatre.

## The five questions

1. **What was claimed broken?** One sentence per gap, in plain language. Cite the claim source (cron output, vision report, audit, peer assertion).
2. **What does reality say?** State the probe that measured the actual state. If the gap is real, name file/line/port. If the claim is false, say so — the gap is then "claim ≠ reality", not "system broken".
3. **What is the minimal fix?** Smallest change that closes the gap. New file paths, exact line in patched file. Anything bigger is over-engineering.
4. **What does NOT change?** Name the files/services/cron schedules you did not touch. The reader needs to know blast radius.
5. **What is now queryable that wasn't before?** This is the recursion test. If the answer is "nothing new is queryable", the fix is decoration.

## Template

```markdown
# <System> Gap Repair — Sealed <date>

> F13 directive: "<exact directive>"
> Agent: <who>
> Verifier: reality probe against substrate

## N gaps closed

### Gap 1 — <one-line summary>

**Before:** <what the gap looked like before>
**Fix:** <file path, what changed>
**Reality probe:** <output of the probe that confirmed the fix>

### Gap 2 — ...

## What did NOT change

- <file/service untouched, with reason>

## Recursion now real

<What new query path exists. What was the old state vs new state.>
```

## Anti-patterns

- **"Comprehensive rewrite"** — if the gap repair touched more than 4 files, it's a rewrite, not a repair. Stop and refactor the plan.
- **"Vision said X, therefore real"** — vision audits hallucinate. Probe the actual code before patching.
- **Receipts without probes** — every "Fix:" line must have a "Reality probe:" line. A fix you didn't verify is a fix you don't know landed.
- **Throat-clearing prose** — no "I reviewed and found that...", no "after careful analysis...". The five-question format forces structural concision; honour it.

## Done shape

A sealed repair reads like a court verdict: a numbered list of findings, each with citation, probe, and change. Anyone can re-run the probes in 10 minutes and reproduce the verdict.