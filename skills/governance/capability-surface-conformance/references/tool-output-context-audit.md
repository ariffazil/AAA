# Tool Output as Context — auditing what a capability does to its caller

A capability can be advertised, registered, callable, schema-valid, protocol-conformant, and *correct* —
and still degrade every downstream conversation, because its **result becomes the caller's register**.

Protocol conformance proves a capability is reachable and well-formed. Behavioural conformance asks
three separate questions, and they fail independently:

| Question | Fails as | Test |
|---|---|---|
| Does it compute? | ghost capability (constant return) | two-input contrast, echo-stripped |
| What does its output do to the caller? | register leakage | count machine tokens in the default result |
| Is my fix live? | `FIXED_ON_DISK` reported as deployed | enumerate every loader |

## The leak

Tool results are injected into the calling model's context window. A tool that returns doctrine,
ontology, SCREAMING_SNAKE_CASE verdict tokens, snake_case field names, or directive sentences
("Do not diagnose", "Return authority to the humans") is not merely verbose — it is teaching the
caller a **register**, and the caller will speak that register back to a human.

The failure is invisible from inside the tool: the payload is *correct*. It is only wrong as an
environment.

## The fix — compact by default, doctrine behind a pull

The default result carries the minimum needed to act:

- the state
- supporting observation refs
- what could NOT be established
- the next action

Everything else — ontology, constitutional law, explanatory boilerplate, diagnostic traces, field
inventories — belongs in a resource or a debug mode the caller requests explicitly. Progressive
disclosure applied to language.

## Countable metrics

Measure before and after; the ratio is what changed.

| Metric | Target |
|---|---|
| total chars across a representative call set | smallest set that still carries the decision |
| UPPERCASE machine tokens per 1000 chars | none visible in prose |
| distinct snake_case keys in the default result | structural only, never narrative |
| imperative / directive sentences handed to the model | zero in a default result |

**Measure per capability, not per server.** One verbose tool in a call set of eleven produced roughly
half the returned characters and most of the machine tokens — the fix is usually a single tool, and a
server-level average hides exactly the one that needs rewriting.

## Why it matters beyond tidiness

The register propagates one hop further than the tool. The caller reads the payload, then writes to a
human in the payload's voice — labels, verdict words, structural headers, a closing that summarises
rather than lands. Diagnosing that as a caller-side discipline problem misses the upstream cause: **the
environment taught it.** Schema becomes style; law becomes style.

Corollary for the operator: after a tool-heavy turn, re-read the draft as *speech* before sending. The
register of what you just read is not licence for how you now write.

## Anti-pattern

An "output contract" that is itself a long procedural document. A 5,000-token naturalness or formatting
constitution inside a tool result is the same defect wearing the opposite sign — still machine register,
just aspirational. Keep the style rule short enough to be read.

## Related

- `scripts/tool_contrast_probe.py` — re-runnable probe for the first row of the table.
- `references/control-enforcement-probe.md` — the CALLER / EFFECT / BYPASS procedure for a control that
  may not enforce anything.
