# Instrument Liveness — Prove the Tool Ran Before Trusting Its Number

Every defect class the skill library catalogues has an analogue **inside its own tooling**, and that
variant is worse, because a dead audit script fails silently in the one place nobody inspects: the
audit.

## The rule

**A measurement tool is UNPROVEN until it has been executed and produced output.** No figure produced
by a script may be published until the script has been seen to run. A number attributed to an
unexecuted tool is not an estimate — it is unmeasured, and it must be labelled `UNVERIFIED` or dropped,
never reported as a count.

## The three states of a tool inside a skill tree

| State | How it reads | Why it is dangerous |
|---|---|---|
| Tracked + runs | No surprise | — |
| Tracked + broken | Raises on every call | Loud; found the first time someone runs it |
| **Untracked, never run** | Reads as a finished instrument — the skill body cites its output anyway | The number was never produced, and nothing in the tree says so |

The third state is the corpse class wearing a lab coat. A script written during a sweep, used for one
inference, then left uncommitted is indistinguishable — from the skill body that points at it — from a
script that ran a thousand times.

## The two commands (run before publishing any count)

```bash
# 1. Does every script in the skill even parse?
for f in $(find <skill_dir>/scripts -name '*.py'); do
  python3 -m py_compile "$f" 2>/dev/null || echo "BROKEN: $f"
done

# 2. Is it in the repository at all? A '??' here means it was probably never executed.
git -C <repo> status -s <skill_dir>/scripts
```

Run both across the tree after any consolidation wave: a sweep that moves dozens of bodies leaves
behind scripts the mover never invoked, and those are exactly the ones a later session will trust.

## When a tool turns out to be dead

1. **Retract the number — do not re-guess it.** Repair the tool, run it, publish the measured value.
2. **Re-check every claim the tool was cited for.** If the instrument never ran, every figure
   attributed to it over that period is unsourced — including the ones that happen to be correct.
3. **Ship the repair as its own commit**, so the instrument has a hash and the number it later
   produces has a provenance chain (instrument → output → claim).
4. **If the dead tool is a gate** (designed to exit non-zero and block), its death means the control
   did not exist over that period. Report the absence of control, not a bug in a script.
5. **Look for the irony, then fix it.** A dead detector sitting inside the skill that *defines* the
   defect class is the strongest possible instance of that class — and the most likely, because those
   scripts are written mid-sweep and are the first thing left behind.

## Reporting shape

Replace the dead figure rather than annotating around it: `collisions: 0 (measured <when>, by
<script> after repair)`, naming the script path and the commit that shipped it. A number whose
instrument is not named is not a measurement — it is a memory, and memories do not carry state.

## Why this is an entropy source, not a bug list

A broken tool is repaired once. A **never-run** tool keeps generating claims indefinitely, because
nothing in the tree marks it as untested and every downstream reader inherits its authority for free.
Same mechanism as a registry entry with no body, or an instruction that cannot execute: the cost is not
the wasted run, it is the confident number that follows.
