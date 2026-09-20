# Detecting theatre controls by measurement

Companion reference. The wider federation lesson: a control that **cannot fail** measures
nothing, yet still confers false confidence — the same defect as a dead symlink named as
if it works, seen from the other side. This file is the executable procedure plus the
failure signatures, all measured live on the arifOS federation 2026-09-19.

## Four tests, run all four

1. **Parse test.** `python3 -m py_compile <script>`, `node --check <js>`, `bash -n <sh>`.
   A syntax error means it has never run — while still looking authoritative in a
   governance directory. Real find: a collision-audit gate with an unterminated f-string
   raised `SyntaxError` on every invocation since the day it was written, was untracked in
   git, and sat inside the skill that defines the dead-instrument doctrine.
2. **Caller test.** `grep -rn <filename> <roots> --exclude-dir=.git`. Zero *executable*
   callers = a hand-run document, not a control. Prose hits (a SKILL.md citing the script)
   are the dominant false positive and make a dead script look wired in.
3. **Exit-path test.** `grep -n 'sys.exit\|exit \|return ' <script>`. A guard that can only
   return 0 cannot guard. Trap: a correct non-zero path behind a flag nobody passes
   (`--strict`) is exit-0 in practice. Real find: **zero** exit statements in 86 lines,
   printing `VERDICT: CRITICAL` on 8 consecutive runs, exit 0 every time, as the only
   skill audit in `/etc/cron.d`.
4. **Wiring test.** Compare the manifest the SOT *declares* against the config actually
   loaded; compare a deployed copy against its canonical source **by digest**. Existence
   checks pass while content drifts. Real find: a hook-drift guard whose check was
   `if not Path(p).exists(): fail(...)` certified a plugin manifest while the live config
   was a different file wiring 1/6-size stubs. Both drift classes were structurally
   invisible to the guard built to find drift.

## The cost test — what makes it actionable

A control is not theatre merely for being weak. It is theatre when it **consumes work for
output identical to running with it absent**:

- Count the lines an agent had to store or read. Real figure: 25,969 `WOULD-HOLD` lines
  across nine commits, ending in the gate's own words *"nothing was blocked"*.
- Time the forcing hook per call. Real figure: ~45 ms, of which 40.6 ms interpreter spawn
  and 4.3 ms import — the governance logic was 0.1–10.6 µs. Six orders of magnitude of
  ceremony per unit of decision, paid in process startup.
- Count how much of a ledger records a NON-event. Real figure: 94.3% of receipts recorded
  an ALLOW.

## Signatures to recognise on sight

| Signature | Meaning |
|---|---|
| Prints a verdict, has no exit path | Decorative. Nothing downstream can act on it. |
| Emits a schema the host rejects | An error on every action that still does not stop it. Worse than silence: trains its reader to ignore errors. |
| Declares a manifest that is not the loaded config | The SOT certifies a file that isn't running. Both look true. |
| Records a verdict then proceeds | Named in the hook SOT itself: *"makes the judge a commentator and the ledger an assertion of governance that never happened."* |
| Satisfied by editing what it reads | **Self-referential** — see below. |
| Holds with no documented unblock | Not safety, a dead end. Dead ends are what make agents useless. |

## The self-referential class (highest severity)

A control satisfiable only by **altering the text under audit** forces destruction of the
evidence it was asked to produce. Two measured instances:

- A register linter's mention-vs-use exemption was implemented on every bank *except* the
  heat-word bank, so a report **quoting** a human's word scored worse than the same report
  with the quotation removed. The prescribed fix for this exact defect was already written
  in this skill library — applied to the register banks, left off the heat bank.
- The same linter failed **its own source document** — the doctrine that grants the word as
  legitimate human register. It contradicted the law it enforces.

**Rule:** when a gate fires on a quotation, fix the gate. Never delete the quotation to
pass. A quotation is data about what someone said, not a claim by the writer.

## Reporting discipline

- Classify THEATRE / DISABLED / BROKEN / REAL / UNPROVEN. Default to UNPROVEN, not guess.
- **Report the REAL ones plainly even when they weaken the headline.** In the run behind
  this file, a fail-closed authority guard with a recorded `release_refused` and a
  pre-tool-call gate with 1,023 recorded blocks (which blocked the audit itself four
  times) were the strongest evidence produced.
- Distinguish *cannot withhold* from *withholds but cannot be answered*. The second is
  often worse and is invisible to a theatre hunt aimed at the first.
- Every count comes from a command run in-session. Never restate a figure found in a
  doctrine document — measured reality was 4.9× the number one doctrine asserted about
  itself.
