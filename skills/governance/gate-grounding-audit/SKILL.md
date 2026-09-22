---
name: gate-grounding-audit
description: "Use when auditing a gate that validates supplied evidence."
version: 1.0.0
owner: curator
risk_tier: high
floor_scope: [F1, F2, F4, F11]
triggers:
  - "is this gate actually enforcing"
  - "audit the validation layer"
  - "build an evidence gate"
  - "the check passed but should not have"
  - "can this guard be bypassed"
  - "why did HOLD not fire"
  - "verify a control actually controls"
tags: [governance, audit, gate, evidence, controls]
capability_tier: fed-long-context
ecology_state: WARM
---

# Gate Grounding Audit — presence is not evidence

Every governance gate reads a test on a protected operation. This skill is the test of the test:
**does the gate resolve what it was given, or does it only detect that something was given?**

The defect class below is small, common, and survived one repair attempt in the session that produced
this skill — the fix itself had the same defect one level up. Assume it on first contact.

---

## The defect, in one line

```python
has_bridge = bool(bridge_evidence and str(bridge_evidence).strip())   # WRONG
```

Non-emptiness is a proxy for *the caller typed something*. A caller satisfies it with a **negation** —
a string that literally states no evidence exists — because a negation is non-empty. The gate then
ALLOWs, and commonly echoes the caller's own text back as a supporting artifact, so the laundered
verdict is byte-indistinguishable from a witnessed one downstream.

---

## The seven variants (grep the gate for each)

| # | Variant | The tell |
|---|---|---|
| 1 | **Presence-as-evidence** | `bool(x and str(x).strip())` on an evidence/proof/consent/bridge parameter |
| 2 | **Count-as-gate** | `len(alternatives) >= 3` — satisfied by `["a","b","c"]`; the predicate that matters is *alternative hypotheses about the case* |
| 3 | **Keyword suppression** | a HOLD clears when the text merely *mentions* the control word (`bridge`, `we both agree`, `consent:`) |
| 4 | **Opt-in gate** | `if payload.get("field"): run_gate(...)` — omitting one key disables the whole check |
| 5 | **Negated consent** | `any("consent:" in e for e in evidence)` — a description reading *"no consent: was ever given"* passes |
| 6 | **Bogus reference disables auto-link** | `if supersedes: look_up(that_id)` returns `None`, skipping the fallback branch that would have found the prior record — so the firewall never runs |
| 7 | **Echo as witness** | the response carries a field named like the input, holding the caller's string back, labelled as grounding |

Variant 4 is the complete-mediation failure. If one code path to the protected state skips the check,
there is no security property — only an ethics suggestion.

---

## The fix: resolve, never shape-match

```
path      -> os.path.exists()
receipt   -> the id appears in a named ledger (and fail closed if the ledger is unreadable)
URL / DOI -> HEAD, status < 400
quote     -> appears verbatim in a named file
declaration -> names all three of: observation class, observer/instrument identity, timestamp
```

If no anchor resolves, **FAIL CLOSED** and name *which* anchor could not be resolved. State
`cannot resolve — network unavailable` rather than passing quietly on shape. Keep reads confined to a
declared root list, make HEAD the only network call, and never PUT bodies.

**Scan the head of the evidence string for absence cues before scanning it for anchors.** A negation
in the opening wins over a citation later in the same string.

**Falsification conditions are evidence too.** A list of placeholders (`n/a`, `tbd`, single tokens) is
an empty list. Require each element to read as a falsifiable sentence.

---

## The repair loop, and why one pass is not enough

A first tightening typically moves the bar from **non-empty** to **anchor-shaped**: regex-matched
citations that are never dereferenced still pass (`rcpt-anything-i-type`, a bare hex string, a path
that does not exist, a URL under a reserved TLD). Shape is easy to fake; resolution is not.

So run the loop as a falsification exercise, and prove **both directions at once**:

1. **Bypass set must reject.** Keep the literal strings that motivated the gate as a regression
   fixture — the negation statement, `n/a`, a fabricated receipt id, a non-existent path, a reserved
   URL — each paired with a *valid* value on the other parameter, so the parameter under test is the
   only variable.
2. **Positive controls must still allow.** Tightening creates false rejections, and false rejections
   are worse than the bug: honest work starts routing around the gate. Assert a real on-disk path, a
   real verbatim quote, and a well-formed observation declaration all still pass.
3. **Non-vacuity proof.** Run the new tests against a reconstructed pre-fix copy of the module and
   confirm they fail there. A suite that passes on both versions is measuring nothing.
4. **Hermeticity check.** Grep the enforcement ledger for the test suite's own claim ids — a test that
   writes production receipts contaminates the audit trail it is meant to protect.

---

## Auditing: how to read the gate's decision

- **Trace the verdict to its inputs.** If the verdict is a function of caller strings plus fixed
  keyword lists, it is decoration. Name the comparison the gate makes against something outside the
  request — a file, a ledger, an endpoint. If you cannot name one, say so.
- **Check the constant payload.** A SEAL/HOLD response that ships a hardcoded witness attestation or
  fixed metric values makes a bypassed verdict indistinguishable from a witnessed one. Report those
  constants as defects, not as formatting.
- **Follow the wiring, not the module.** A correctly fail-closed function that is imported nowhere is
  dead code; a fail-open sibling that *is* wired will be the live behaviour. Diff the intended and
  imported paths before reporting either as the control.
- **Report the true state.** If the fix needs a gated verb, the change is on disk and **not live**:
  report `BLOCKED_AT_GATE` with the exact held operation and the lane that can apply it. Never
  describe it as staged or applied, and never use a different verb to dodge the gate.

---

## Pitfalls

- **Do not grade a gate by the size of its rejection list.** A gate that refuses nothing and a gate
  that refuses everything are both unverified; only the paired bypass-and-control proof is evidence.
- **A gate that reads its own log is not independent.** Enforcement-ledger counts are a symptom, not
  the decision.
- **Do not fix a gate by weakening the reference rule to make a legitimate fixture pass.** If a real
  observation is being rejected, the answer is to accept an explicit declaration (class + observer +
  timestamp), not to loosen the anchor rule until placeholders pass too.

DITEMPA BUKAN DIBERI ⚒️
