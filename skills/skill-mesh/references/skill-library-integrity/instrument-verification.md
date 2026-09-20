# Instrument Verification — is this sensor alive, and can it fail?

Companion to SKILL.md §6–§9. The scripts in this skill are **actuators**, not helpers: they produce
the numbers the store is then governed by. An instrument that has never executed, or that cannot
return non-zero, is **a gate that cannot fail** — it emits a plausible number, nothing errors, and no
failure path exists to reveal that nothing was measured.

This is the highest-severity defect in the skill's own tooling, because it is invisible from the
output side. A dead sensor and a live sensor both print a number.

---

## The five checks — run all five, in order, before trusting or citing a sensor

Each takes seconds. Skip none of them.

1. **Does it compile?** `python3 -m py_compile <script>`. A syntax error means it has never run once.
   A script whose f-string is malformed at parse time raises on *every* invocation and reports
   nothing — not a wrong number, no number.
2. **Is it tracked?** `git -C <repo> log --oneline -- <path>`. An **untracked** script sitting in a
   governance or audit directory is a red flag: it was never reviewed, and no diff records what it
   does. Untracked plus never-compiled is the signature of an instrument that exists only as intent.
3. **Does anything call it?** `grep -rn '<filename>' <root>` excluding `.git`, `node_modules`,
   caches. Zero callers means it is not a gate — it is a document, and it only runs if a human types
   its name. Say that plainly rather than describing it as enforcement.
4. **Can it fail?** Read the exit-code logic. A guard that always exits `0` cannot guard. Look for a
   strict flag, a non-zero return on violation, and whether the *caller* honours that code — a script
   that returns `1` into a caller which ignores the status is still a no-op.
5. **When did it last produce output?** Find the artifacts it writes (json reports, logs) and check
   their mtimes against the script's mtime. No artifact, or an artifact older than the last change,
   means the current version has never run.

---

## Rule: run a newly written gate at least once before declaring it working

Writing a check is not installing a control. **Execute it against the real store, read its output, and
confirm the output is non-empty and sensible before you describe the check as existing.** A script
that has been written, committed, and cited as protection — but never actually executed — converts
every later audit that trusts it into a false negative. The defect it was written to catch passes
silently, with a citation attached.

Corollary: **never describe a control by its intent.** "The store has a collision guard" is a claim
about a file. "The collision guard ran and returned 0 real collisions" is a claim about the world.
Only the second belongs in a report.

## Rule: a number is not a measurement until you know which instrument produced it

Record, next to any count that leaves this skill, the script and the run that produced it. An
unattributed count cannot be re-checked, so it cannot be corrected when the instrument turns out to
have been dead — it can only be believed or abandoned.

## Rule: absence of failure is not evidence of success

A sensor that has never raised is a sensor you know nothing about. Before you upgrade "no errors were
reported" into "the store is clean", run check 1. The instrument's silence and the instrument's
deadness are the same observation from the outside.

---

## Rule: a control must not be satisfiable by editing what it reads

When a check matches **content** — a word, a token, a label, a pronoun — it can usually be turned green
by altering the artefact under review rather than by fixing the condition under review. That inversion
is worse than a dead sensor: a dead sensor measures nothing, while an invertible control actively
pushes the operator away from the truth and does it silently, because the green result looks like
success.

The test: **name the action that makes the check pass. If that action is "remove the offending text"
rather than "resolve the underlying condition", the control is inverted.**

- A tone or register linter that flags a word will also flag that word inside a **quotation**, inside
the reader's own message carried back into a reply, and inside an audit that is quoting an offender
verbatim. Deleting the quotation to clear the gate deletes evidence. Exempt the quoted span and keep
the text — and record the exemption.
- A gate that reports violations but enforces none is a log generator. It charges every operation for
noise and returns no constraint. Either wire it to a non-zero exit or stop calling it a gate.

Corollary: **never clear a red gate by changing the artefact's audience, scope or labelling.** Those
declarations answer *who is reading* and *what is in domain*; they are not a lever for making a check
pass. Choose the audience by the reader and report the gate's true state for that reader. If a check
can be cleared by re-labelling the work, it was never constraining the work.

---

## Sweep list — the scripts in this skill, and what to verify on each

The five checks apply to every script under `scripts/`: `discovery_guard.py`, `corpse_audit.py`,
`collision_audit.py`, `dependents.py`, `mirror_or_duplicate.py`, `skill_resolution_audit.py`.

Two of them carry the correct shape and are worth using as the template when repairing others:
`discovery_guard.py` exists specifically to prove that a merged-away name is still findable, and
`collision_audit.py` separates **address bands** (one body, several addresses — informational) from
**real collisions** (bodies differ — the defect), so its headline number cannot be inflated.

When you repair a broken instrument, run it before and after and **publish both numbers**. The before
number is nothing at all (it never ran); the after number is the first real measurement of that
property. Saying "0" without saying "this is the first time it has ever returned anything" hides that
the property was unmeasured until now.

Also apply the checks to the gate scripts invoked by commit hooks and cron. A hook that prints
thousands of violation lines and then reports that it enforced none of them is not a gate; it is a
log generator, and it charges every commit for the noise.

---

## The compounding failure

The worst place for a dead instrument is inside the skill that **defines** the defect class. An audit
that cannot itself execute will report a store clean of exactly the pathology it was written to
detect, and the report will read as authoritative because its own doctrine is correct.

So: when this skill's doctrine is extended, the extension applies to this skill's tooling first.
Every rule added here is also a claim that must be verified against `scripts/`.
