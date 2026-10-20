---
name: monetary-amount-integrity
description: "Use when parsing, carrying, or displaying a money amount."
version: 1.0.0
tags: [money, amount, parsing, payments, ledger, rounding, finance]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Monetary Amount Integrity

An amount is not a number with a currency label. It is a **claim about who gets how much**, and
the chain from an untrusted string to a sealed ledger row has five places where a factor of 100 or
a stale copy silently changes it.

Covers: reading an amount out of a payload (QR, invoice, API, form, spreadsheet), validating it,
carrying it through approval, and writing it to a ledger.

## Rule 0 — an amount found in an untrusted source is a claim, not a value

A number lifted from a QR payload, a PDF, an email, a vendor API or a spreadsheet cell is what the
*source says*, not what is owed. It enters the system as a claim and is promoted only by an
authority that can be named: a network-resolved recipient, a signed invoice, a bank statement.
Nothing downstream may read an unverified amount as verified because it parsed cleanly.

## The path: string → integer minor units → approval digest → ledger

### 1. Validate the FORMAT before the value

An amount that fails the format is not a small amount, it is not an amount. Reject it and stop; do
not strip, coerce, or continue.

```
valid:    ^[0-9]{1,13}$                 minor units, no separator
          ^[0-9]{1,11}\.[0-9]{1,2}$      major units, 1–2 decimals
expires:  1.  12.  .5   1,000   ' 10'   1.2.3   +5   -5   (1.00)   RM12
```

Trailing dot, leading dot, thousands separators, whitespace, signs, accounting parentheses and
currency symbols all read as *valid* to a permissive `float()` and as *missing* to a regex that
forgets them. Both outcomes are silent. Return a typed parse failure carrying the offending string.

### 2. Classify zero separately from invalid

`0`, `00`, `0.00` are well-formed and carry no intent. That is a different finding from
`INVALID`: a zero-amount payment request, a zero invoice line, and a zero transfer all deserve
HOLD-and-ask, not silent rejection and not silent acceptance. Give each its own reason code.

### 3. Convert with string arithmetic, into explicit minor units

Never `float()`. Never let `Decimal` cross a JSON boundary and come back as a different type.
Exponent belongs to the currency, not to the parser: MYR 2, JPY 0, KWD 3. Unknown currency → HOLD,
never a default of 2.

```python
def to_minor(amount: str, exponent: int) -> int | None:
    """String arithmetic only. None when the value cannot be represented exactly."""
    if not re.fullmatch(r"[0-9]{1,11}(\.[0-9]{1,%d})?" % exponent, amount):
        return None
    whole, _, frac = amount.partition(".")
    if len(frac) > exponent:
        return None          # more precision than the currency allows: not our call to round
    return int(whole or 0) * 10**exponent + int((frac or "").ljust(exponent, "0"))
```

### 4. A bare integer is AMBIGUOUS, not rounded

`1250` in an amount field reads either as 1250 minor units or as RM 1250.00 — a **100× difference
on the number a human approves**. The parser does not get to choose. Report both readings and
return HOLD:

```json
{"ambiguous": true,
 "readings": {"as_minor_units": 1250, "as_major_units_minor": 125000}}
```

This is generic, not QR-specific: CSV columns, form fields, OCR output and API responses all lose
the decimal point in transit. Any amount field whose spec does not fix the unit needs this finding.

### 5. Show, approve, and execute must be the same object

```
digest(shown to the human) == digest(approved) == digest(executed)
```

If the digest covers only the final transaction, a change between display and execution re-signs
itself and nothing catches it. The binding must cover what the human actually saw — recipient,
amount, fees, reference, expiry — computed server-side, verified again at the executor. The
executor takes a digest, looks up the canonical object, and re-verifies; it never accepts a
ready-made payload from an upstream caller, because that path bypasses every other control.

## Display rules

- **Amount and currency travel together, always.** A minor-unit integer without its exponent is
  unreadable; a formatted string without its currency is unreadable to the next service.
- **Render from minor units at the edge, once.** Grouping separators, decimal marks and symbol
  position are presentation. Storing them loses the value; re-parsing them is a second parser with
  its own defects.
- **Show what was NOT verified next to the number.** A recipient name extracted from a payload is a
  claim; labelling it as bank-verified when no resolution happened is a false attestation, and it
  is the field a payer will actually read.

## Pitfalls

- **`float()` in the money path is a defect class, not a style preference.** It is exact only for
  dyadic fractions, it compares unequal to its own string round-trip at scale, and it makes
  `0.1 + 0.2 != 0.3` a production incident. Assert its absence: add a test that greps the money
  module's source for `float(` and fails on a hit. A convention nobody tests is a convention that
  ends at the next contributor.
- **Validate format before magnitude limits.** Checking `amount < limit` first means `1,000` fails
  as "too small" and `-5` passes as "under limit". Order: format → representation → business limit.
- **A currency with 0 or 3 decimals breaks the ×100 reflex.** JPY 1000 is 1000 minor units; KWD 1.5
  is 1500. Any `* 100` literal in the path is a latent bug for every non-2-decimal currency.
- **Rounding is a decision with a bearer.** Banker's rounding, half-up and truncation differ by a
  cent each; whichever you pick, name it and record it. Silent rounding accumulates into an
  unexplained balance difference that nobody can then reconcile.
- **Sum in minor units, never in formatted strings.** A monthly total built by adding `"12.50"`
  strings, or by adding floats then formatting, drifts from the ledger and is discovered by an
  auditor rather than by a test.
- **The exporter is part of the money path.** CSV/Excel output that writes a formatted string, or
  that lets a spreadsheet reinterpret `1234.50` as a date, corrupts the value after the parser has
  done everything right. Write minor units or a quoted ISO-formatted decimal, never a bare number
  in a column a spreadsheet will coerce.
- **An amount field with no unit in its name invites the 100× error.** `amount`, `total`, `value`
  say nothing. Name them `amount_minor_units` / `amount_major_units`, and make the exponent a
  sibling field rather than a convention held in someone's head.
