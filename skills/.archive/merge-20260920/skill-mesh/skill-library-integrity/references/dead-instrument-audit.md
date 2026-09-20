# Dead instruments — auditing a skill-declared guard before trusting it

The skill store carries scripts that its own `SKILL.md` bodies cite as guards. Most are documents. This is the procedure for telling them apart, and the classes to report.

## The four liveness tests

Run all four on every script a skill declares as enforcement:

```bash
python3 -m py_compile <script>        # 1 DOES IT RUN AT ALL
grep -n 'exit\|return' <script>       # 2 CAN IT RETURN NON-ZERO
grep -rn "<relpath-or-name>" /root \
  --exclude-dir=.git --exclude-dir=node_modules   # 3 DOES ANYTHING CALL IT
ls -l <its output artifact>; stat -c %y <its log> # 4 HAS IT EVER PRODUCED OUTPUT
```

Judge liveness by mtime and its own artifacts, **not** by running it — and if a probe touches a file (a `__pycache__`, a log line), say so, because that mtime is no longer usable as evidence.

## The classes to report

| Class | Signature | Consequence |
|---|---|---|
| **BROKEN** | fails test 1 — syntax error, `ModuleNotFoundError` at module scope, unimportable package | has never run; it raises on every invocation |
| **NO-CALLER** | passes 1–2, fails 3 | a document. Zero references outside its own directory means prose, not wiring |
| **NO-EXIT** | passes 1 and 3, fails 2 | cannot refuse. An audit that always exits 0 publishes findings nothing acts on |
| **ORPHAN + CANNOT FAIL** | fails both 2 and 3 | the worst class: looks authoritative, is never run, and could not refuse if it were |
| **REAL** | passes all four, with a recorded refusal | keep it, and say so |

Report the **union**, not the first class you find — the interesting instrument is the one that is both unrun and incapable of failing.

## Calibration

On a store of ~100 declared scripts, expect the NO-CALLER and NO-EXIT classes to be a **minority but a large one** — tens of scripts each, not one or two. A sweep that reports zero is itself suspect: check the detector against a script you already know is dead before publishing the number.

## Related defects in the same family

- **`--strict` trap.** A guard whose refusal is opt-in and whose callers never pass the flag is a brake nobody pulls. Print the exact exit-code logic when reporting it.
- **The exit-code polarity flip.** A lookup tool where missing-owner exits non-zero and owner-exists exits 0 is correct; where the polarity is inverted, every caller's `if` reads backwards. Check polarity as well as presence.
- **Never-run refusal branch.** A guard that has produced output on its pass path but has **no observed instance** of its refusal path is only half-verified — label the refusal branch UNVERIFIED rather than assuming it works.
- **Two brakes.** A second implementation of one control is two half-brakes that drift apart, never redundancy. If the federation has a single-owner rule for controls, cite it.
- **Byte-identical twins.** A skill-local copy identical to a retired tool's copy tells you which is downstream — check digests before judging which artifact is authoritative.
- **A gated-but-declared defect is not an undeclared one.** The healthy pattern is: an undeclared defect fails the check, a declared one passes with a notice. Support that in any guard you write — it lets real gaps stay visible instead of being fixed by deleting the check.

## When the declared manifest is not the live config

A harness may declare one manifest path while a different file is what actually runs. An existence-only check on the declared path certifies the wrong artifact.

- Compare **deployed copy vs canonical source by digest**, not by name.
- Compare the **live wired config** against the declared manifest path.
- If a drift guard passes while deployed code differs in size or content from canon, the guard's coverage — not the drift — is the finding. Extend the check rather than reporting the drift alone.
