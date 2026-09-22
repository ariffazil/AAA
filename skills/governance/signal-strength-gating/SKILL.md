---
name: signal-strength-gating
description: "Use when evidence is thin; cap interpretation to it."
version: 1.0.0
layer: governance
owner: A-FORGE
floors: [F1, F2, F7, F9]
triggers:
  - "analysis from thin evidence"
  - "summarize this digest"
  - "what does this email/report mean"
  - "agent said X"
  - "deep research on this"
  - "weak signal"
  - "one source"
  - "should I elaborate"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Signal-Strength Gating

> **The one rule: when signal is weak, interpretation must become NARROWER — not more elaborate.**

## Why this exists

Elaboration is an amplifier with no gain control. It multiplies whatever went in, including a
fabrication. A wrong premise analysed thoroughly is not closer to truth — it is further from it and
harder to retract, because the length of the analysis reads as diligence and the reader cannot tell
which of forty sentences was load-bearing.

The failure is **inverted effort**: the thinnest evidence produces the longest output. One relayed
summary becomes five hundred words of institutional theory. The output is fluent, structured, and
confident — which is exactly what makes it dangerous, because none of those properties are evidence.

## The gate — classify BEFORE writing, not after

| Signal | Definition | Permitted output |
|---|---|---|
| **STRONG** | >=3 first-party sources, cross-validated | full interpretation, recommendation |
| **ADEQUATE** | 2+ sources, >=1 first-party | interpretation, uncertainty flagged inline |
| **WEAK** | 1 source, OR second-hand, OR agent-generated | observation + competing explanations + ONE cheap discriminating probe. **No narrative.** |
| **ABSENT** | 0 sources, inference only | HOLD. "Insufficient evidence." Name the probe that would settle it. |

**First-party** = you resolved it yourself this session (read the file, called the API, saw the
record). Everything else is second-hand at best.

**Output shape for WEAK**, and nothing more than this:
1. What was actually observed (the literal artifact)
2. Two or three competing explanations, none preferred
3. One cheap probe that discriminates between them
4. Explicit statement of what remains unknown

## Cheap-probe rule — a test, not a paragraph

When a question splits into two branches, the next output is a **test**. Ask: what is the smallest
action that returns a different result under hypothesis A versus hypothesis B? Run it.

- Prefer a command you can run now over a doc you would have to find.
- Prefer one item resolved to the primary record over ten items inferred from the summary.
- If the probe is genuinely unavailable, say so and stop — do not substitute a narrative for it.

A one-line probe beats three pages of ranked hypotheses, every time, and it is falsifiable.

## Specificity is not verification

Fabricated and relayed material arrives with **realistic detail**: exact sender addresses, subject
lines, message IDs, timestamps, file paths, quoted phrasing, plausible job titles. Plausibility rises
with specificity. **Evidential status does not move at all.**

Realistic detail is precisely what makes relayed material dangerous, because a reader — human or
agent — pattern-matches *detail* to *groundedness*. The detail is the camouflage.

**Rule:** before acting on any item quoted out of a relayed source (peer-agent summary, cron digest,
search snippet, pasted transcript, chat forward), resolve at least one item to the primary record. If
you cannot resolve even one, the whole relay is WEAK signal regardless of how many specifics it
carries.

## Relayed agent output is a claim about artifacts, never the artifacts

An agent's confident summary with named entities ("X emailed about Y on date Z", "file N contains
M") is a **claim about** those artifacts. The names create the illusion of a record. Verify the
record.

- A digest is not a source. A tally of it is not a tally of the world.
- When relaying, keep the relay's status: "the agent reports ...", never "... happened".
- Self-reported success from a subagent or scheduled job is a claim; check for a verifiable handle
  (path, ID, URL, hash) and look at it.

## Partial checks cut both ways

A verdict about a corpus requires the corpus, not a prefix. **Always state the denominator**:
"6 of 201 checked; remainder unverified."

Over-claiming a **negative** — dismissing an entire set on a partial look — is exactly as wrong as
over-claiming a positive, and it is harder to catch because it *feels* like scepticism and rigour.

**Correcting an amplification is not licence for the reverse amplification.** When a confident claim
collapses, the honest replacement is narrower, not a louder opposite. Scope the correction to what
the check actually showed. "I checked 6 and found nothing" is not "it does not exist".

## Procedure

1. **Classify the signal** (STRONG / ADEQUATE / WEAK / ABSENT) before drafting anything.
2. **Cap the output to the class.** WEAK -> observation + competitors + one probe. ABSENT -> HOLD.
3. **Resolve one item to the primary record** for any relayed material you intend to act on.
4. **State the denominator** on every coverage, absence, or universal claim.
5. **If the signal is WEAK and you cannot probe**, say so plainly and stop — do not fill the gap
   with theory, framework, or institutional narrative.
6. **On correction, shrink.** Re-scope to what was actually verified.

## Pitfalls

- **Thin evidence -> long analysis** is the signature failure. Length is inverse to evidence here.
- **A human's "low signal" instinct is data.** When the human says the signal feels weak or asks
  "did I really get this?", that is a probe request — run it, do not reassure them.
- **Do not answer a verification question with an explanation.** "Where did this come from?" wants
  the source resolved, not the reasoning restated.
- **Do not let the elegant frame survive the evidence.** A neat theory built on a relayed summary
  collapses completely the moment the summary is checked; if the frame is doing the persuasion, the
  evidence was never doing the work.
- **Never present a relay as a record.** Attribution clauses are not optional politeness; they are
  the claim's actual epistemic status.
- **A deadline-shaped question is not a verification.** "Which of these needs a reply?" presupposes
  the items exist. Answer the existence question first, then the action question.

## Mechanization

The intended mechanical form of this gate is a set of checks on the HERMES MCP surfaces
(`hermes_signal_gate`, `hermes_fabrication_detector`, `hermes_cheap_probe`,
`hermes_behavioral_boundary` under `/root/.hermes/mcp/hermes-rasa/`). **Probe before relying on any of
them** — a tool name in a design note is not a running tool. Until probed, this skill is the
enforcement.

## Related

- `claim-receipt-discipline` — receipt and labelling discipline for a claim already made.
- `synthesis-verification-gate` — claim classification before synthesis output.
- `governed-uncertainty` — the same narrowing rule applied to reading a human.
- `arifos-frozen-snapshot-init` — temporal claims need the clock read first, same discipline.
