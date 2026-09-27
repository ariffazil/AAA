# Capture-Before-Explain — Symptom Reports from a Running System

When the human reports a qualitative symptom about a system that is currently
running ("something feels off", "register changed", "feels different than
yesterday", "why is X slow"), the default reflex to read documentation and
draft a system-level explanation is the wrong move. The right move is to
capture one execution trace first, because the trace is the only artifact that
describes what is actually running.

## The pattern in three shapes

**Shape A — Different runtime paths.**
DM and SADO both produce "intelligent" output, but the assembly chain differs.
Agent reads both `channel_prompts` blocks and drafts a multi-page explanation
of "identity assembly chaos." One captured prompt assembly for each path —
with byte counts per layer — answers the question in one row. The prose is
decoration.

**Shape B — Stale cache.**
User says "model feels slower." Agent drafts a benchmark comparison. One
sample of the model's actual latency from a live log line answers it. The
benchmark is decoration.

**Shape C — Broken configuration.**
User says "the bot stopped replying in group X." Agent reads docs about
group policy. One probe of `detect_lane(uid, cid=X)` returns `guest` instead
of `x_lane`. The probe is the answer; the docs explain what was *designed*
to happen, not what *runs*.

All three shapes share the same fix: **capture one trace of the running
system before drafting any explanation of the running system.**

## What counts as a capture

A capture is not a quote from documentation. It is a reading of the live
system at the moment the symptom was reported. Acceptable captures:

- The full byte-level prompt assembly for one turn (base SOUL + lane_card
  + channel_prompt + memory tail + model routing).
- One log line from the gateway at the relevant timestamp.
- The output of a probe function that reads the live registry
  (`detect_lane`, capability map query, MEMORY file tail).
- A side-by-side comparison: trace A from the moment of the symptom, trace
  B from a known-good baseline (different lane, different time, different
  config).

What does not count: a paragraph from the SOUL.md or constitution, an
architecture diagram, a hypothesis about what the plugin "probably does", or
a memory of how it worked last week.

## The two-question test before drafting any explanation

1. **Can I capture one real trace of the running system right now?** If yes,
   do that first. The trace replaces the explanation.
2. **Can I capture a baseline trace to diff against?** If yes, the diff
   replaces the explanation AND the prose around it. If no, capture only
   the symptom side and name what the baseline would be — don't narrate
   without the second point.

If both return null, the agent may draft an explanation from documentation,
labelled `INFERRED — capture unavailable`. Unlabelled documentation-derived
explanations are the failure mode.

## Why this matters more than the audit-forward reflex

`probe-before-panic` covers "declare down only after inventory." `scar-integration`
covers "don't repeat the prior failure." This is narrower: it is about
qualitative human complaints about a live system. The complaint is evidence
about a *perceived* delta, not a labelled defect. The capture is the only
artifact that turns the perception into a measured delta. Without it, the
agent narrates a story that the human has to keep supervising because the
agent is building the system in real time in front of them.

## Worked shape — the audit chain

| Pusingan | What the human said | What the agent did | What one trace would have done |
|---|---|---|---|
| 1 | "fix HERMES in SADO" | Audited lanes.yaml, channel_prompts, plugin code | Captured one DM turn + one SADO turn assembly → diff → answer |
| 2 | "audit the audit" | Audited the architecture doc, proposed authority probe | Same — the trace from pusingan 1 is still the answer |
| 3 | (writes a doctrine) | Drafted a SOUL.md patch + 3-question menu | The trace, presented as a 5-line diff, replaces the patch |
| 4 | (pastes agent's draft with "extract ONE invariant") | Finally stops | The seven-line invariant replaces the entire chain |

Each row's last column was available on pusingan 1. The audit text is the
cost of skipping the trace; the compression in pusingan 4 is the correction.

## The naming reflex to break

When an agent catches itself writing "the root cause is X" within the first
two turns of a qualitative complaint, **the diagnosis slot is too early**.
Back up. Re-name the report. The human reported experience; the agent's
working hypothesis is "X is the root cause"; the trace would test that
hypothesis. Until the trace runs, "root cause" is a claim with no evidence
weight, and the human is supervising speculation.

Reframe in one line:

> "I'm about to name a root cause. I haven't captured one trace yet.
> Proceeding with diagnosis without the trace is the failure mode. Holding
> for the trace, or asking the human one short question that puts the
> perception in their own words."

Then either capture or ask. Don't draft.
