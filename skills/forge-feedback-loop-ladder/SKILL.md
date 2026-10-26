---
id: forge-feedback-loop-ladder
name: "Forge Feedback Loop Ladder — Build the Red Signal First"
description: "Use when a bug resists a first fix or has no red signal. Escalates through ten loop-construction rungs — failing test, HTTP probe, CLI fixture, headless browser, trace replay, throwaway harness, fuzz, bisect, differential, HITL — and forbids hypothesis-stacking until one rung goes red on that exact bug."
version: 1.0.0
owner: HERMES
risk_tier: medium
floor_scope: [F1, F2, F11]
autonomy_tier: T1
forged: 2026-10-23
forged_by: HERMES (F13 order, contrast-hardening batch; absorbed from mattpocock/skills diagnosing-bugs)
tags: [debugging, diagnosis, feedback-loop, bisection, reproduction, falsification]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
trigger_when:
  - bug_resists_first_fix
  - intermittent_or_flaky_failure
  - "cannot reproduce"
  - performance_regression
  - agent_about_to_stack_hypotheses
related_skills: [skill-artifact-redact, verify-before-report, live-system-investigation, helix-diagnosis, check-work]
---

# Forge Feedback Loop Ladder — Build the Red Signal First

> **Doctrine:** diagnosis is not staring at code. It is constructing a signal that goes
> **red on this bug**. Everything after that — bisection, instrumentation, hypotheses — only
> consumes the signal. No signal, no diagnosis.
> **Consumers:** `skill-artifact-redact` (every rung artifact), `verify-before-report` (the fix claim)

## What this is

The missing first step in most failed debugging sessions. An agent reads the stack trace,
forms three hypotheses, patches the most plausible one, and declares a fix it never
reproduced. This skill forces the opposite order: build a cheap, tight, repeatable
pass/fail signal **first**, prove it is red on the unfixed state and green on the fixed
state, and only then allow a hypothesis to become a change.

## USE WHEN

1. A reported bug has no failing test, no reproduction script, and no recorded trace.
2. A first fix did not hold, or the symptom moved instead of disappearing.
3. The failure is intermittent, environment-dependent, or "works on my machine".
4. You are about to propose a cause you have not seen fail in front of you.
5. A performance regression needs a measured baseline before any optimisation.

## DO NOT USE WHEN

1. A red signal already exists (failing test, recorded trace, reproducible curl) — go straight to bisection or instrumentation; do not rebuild what you have.
2. The behaviour is a documented design limit or a policy decision, not a defect — no amount of looping makes a specification bug.
3. The question is "is the system down?" — run `probe-before-panic` inventory first; a blind loop against a stopped service manufactures false findings.
4. The fault is inside a closed third-party binary with no seam — capture a trace and hand off to the vendor instead of looping forever.

## §1. The law (three sentences)

1. **Build the loop before the theory.** If you cannot make the failure repeat on demand, you cannot claim a cause.
2. **Spend disproportionate effort here.** Writing the loop is the work; the fix is usually downstream and small.
3. **A loop that never goes red is worthless.** Prove it red on the broken state, then green on the fixed state — a falsification pair, not a single green run.

## §2. The ladder — escalate only when the rung below cannot reach the bug

| # | Rung | Build cost | What it proves | Exit criterion (move down) |
|---|---|---|---|---|
| 1 | Failing test (unit / integration / e2e) at the seam that reaches the bug | low | the bug exists in code we own | cannot reach the path from any test seam |
| 2 | HTTP / curl script against a running service | low | the deployed behaviour, not just the library | failure needs UI or client state |
| 3 | CLI invocation with a fixture input, diff stdout against a known-good snapshot | low | deterministic input → output delta | needs multi-step interaction |
| 4 | Headless browser (Playwright/Puppeteer) asserting DOM/console/network | medium | client-side and wire-level truth | failure is server-side, or needs real devices |
| 5 | Replay a captured trace: save a real request/payload/event log, replay through the code path in isolation | medium | the exact production input, offline | capture cannot be replayed deterministically |
| 6 | Throwaway harness: minimal subset of the system, mocked deps, one function call | medium | the bug in isolation, no surrounding noise | bug only appears in full topology |
| 7 | Property / fuzz loop: 1000 random inputs, look for the failure mode | medium | the class of input that triggers it | bug is deterministic on one known input |
| 8 | Bisection harness: automate "boot at state X, check, repeat" so `git bisect run` works | high | the commit/version that introduced it | history unavailable or squashed |
| 9 | Differential loop: same input through old vs new (or two configs), diff outputs | high | the delta between two known states | only one state is reachable |
| 10 | HITL script: drive the human through the exact clicks, capture the result | last resort | a failure only a human can trigger | never — but ask once, bounded (see `agent-question-budget`) |

Rung 10 is the only rung that spends human attention. Exhaust 1–9 first; when you reach it,
ask for one bounded action with the reason, not a menu.

## §3. Binding: redaction is part of the loop, not after it

Every rung produces captured text — headers, URLs, env dumps, traces, HAR files. Gate it
**before** it reaches chat, a receipt, a log, or `state.db`:

```bash
python3 /root/AAA/skills/skill-artifact-redact/scripts/redact.py --check capture.txt   # exit 1 = secret present
python3 /root/AAA/skills/skill-artifact-redact/scripts/redact.py capture.txt > safe.txt
```

Build the loop against environment variables so credentials never enter the command line
or the captured output:

```bash
set -a; source /root/.secrets/vault.env; set +a
curl -sS -H "Authorization: Bearer $TOKEN" "$API/path" | python3 .../redact.py > /tmp/r.json
```

A loop that leaks a live token into a trace is a worse outcome than the bug.

## §4. Binding: probe before panic

"No signal" is not "system down", and "down" is not "broken". Before looping:

1. Inventory the lane (process, port, container, log tail, exit code) — `probe-before-panic`.
2. Confirm the rung can reach the component at all. A curl against a stopped service
   returns connection refused; that is a reachability finding, not the bug.
3. Record the probe output as the loop's **precondition**, redacted.

4xx/5xx means the server answered — the lane is UP. Only conn-refused/timeout is DOWN.

## §5. The one-loop discipline

Before trusting a rung, answer these in writing:

- **Red proof:** the exact command, its exit code / diff, and the timestamp when it failed.
- **Green proof:** the same command after the change, with the same inputs.
- **Determinism:** run it 3× on the broken state. Three reds, or the loop is flaky and must be tightened (rung 5 or 7) before any fix is claimed.
- **Scope:** which component the signal isolates — and which it cannot see.

A fix without a green proof on the same loop is **PRODUCED**, not verified. Say so.

## §6. Anti-patterns

- ❌ Three hypotheses stacked before one reproduction ("it's probably the cache") — the first is usually wrong and consumes the loop budget.
- ❌ Fixing by adding logging until the symptom disappears — instrumentation is rung-adjacent, not a fix.
- ❌ Green run on a different input than the red run — different question, different answer.
- ❌ Loop built against production with live credentials and real users — use a fixture or a replay.
- ❌ Declaring the bug "not reproducible" before reaching rung 6 — that is a statement about your loop, not the bug.
- ❌ Pasting the raw trace into chat to "show the work" — gate it through redaction first.

## §7. Receipt shape (what to hand the next agent)

```yaml
bug: <one line>
loop_rung: 2
red_proof: {cmd: "...", exit: 1, at: "2026-10-23T02:10:00Z", runs: 3/3}
green_proof: {cmd: "...", exit: 0, at: "2026-10-23T02:40:00Z"}
isolates: <component>
cannot_see: <what the loop cannot detect>
artifacts: /tmp/<name>.redacted.txt
```

## §8. Cross-references

| # | Skill | Role | When |
|---|---|---|---|
| 1 | `forge-feedback-loop-ladder` (v1.0.0) | this skill | — |
| 2 | `skill-artifact-redact` (v1.0.0) | gates every captured artifact | each rung |
| 3 | `live-system-investigation` | live probe technique for rungs 2, 5 | before claiming a state |
| 4 | `helix-diagnosis` | structural loop/helix reading when the loop crosses layers | when a rung shows broken coupling |
| 5 | `check-work` · `verify-before-report` | post-fix verification | after the green proof |
| 6 | `agent-question-budget` | bounds the rung-10 human ask | at rung 10 only |

## §9. Floors

| Floor | Obligation |
|---|---|
| F1 AMANAH | Fixtures and replays before live production loops; no irreversible probe to learn a cause. |
| F2 TRUTH | Red proof and green proof are both shown; "not reproducible" is scoped to the loop, not the bug. |
| F11 AUDIT | Rung number, commands, exit codes and timestamps recorded so the diagnosis is re-runnable. |

## §10. Changelog

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-10-23 | Initial forge. Ten-rung ladder absorbed from mattpocock/skills `diagnosing-bugs`, bound to `skill-artifact-redact` and `probe-before-panic`; red/green falsification pair made mandatory. |
