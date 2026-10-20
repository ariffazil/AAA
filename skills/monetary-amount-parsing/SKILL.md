---
name: monetary-amount-parsing
description: "Use when parsing money amounts from untrusted input."
version: 1.0.0
tags: [money, amount, decimal, currency, payment, parser, finance]
---

# Monetary Amount Parsing

Any pipeline that turns a number in someone else's bytes into an amount a human approves or a system
charges. QR payment payloads, invoice OCR, pasted transfer receipts, bank-statement CSV, API bodies,
exchange feeds. The number arrives as text; it must never become a `float` on the way to a decision.

## Always-on rules

1. **Integer minor units end to end.** `1250` means 1,250 sen, carried as `int`. Convert by string
   arithmetic, never by float multiplication:

   ```python
   whole, frac = (text.split(".") + [""])[:2]
   minor = int(whole or "0") * 10**exp + int(frac.ljust(exp, "0") or "0")
   ```

2. **No `float` in the money path, and no `Decimal` that silently becomes `float` at a JSON
   boundary.** Pin it: a test that `inspect.getsource(money_module)` contains no `float(`, plus a
   JSON round-trip test asserting the value comes back as `int`.
3. **An amount with no decimal point is scale-ambiguous — say both readings.** `"1250"` is either
   1250 major units or 1250 minor units: a **100×** difference on the number a human signs off. Do
   not silently pick one; return both (`as_major_units_minor`, `as_minor_units`) and route the
   ambiguous case to human review.
4. **Validate the shape, then classify.** Anchor the pattern and require a digit after the separator.
   `[0-9]+(?:\.[0-9]{0,2})?` accepts `"1."` — a trailing dot that is not a number but parses as
   well-formed to every downstream consumer.
5. **Four states, not two.** `absent` ≠ `zero` ≠ `malformed` ≠ `present`. Zero is a real value with
   its own meaning (a zero-amount request carries no intent) and needs its own finding.
6. **State the exponent and the currency with the number.** Minor units without an exponent are
   meaningless; a MYR assumption silently breaks on JPY (0 decimals) and KWD (3).
7. **The approved figure is the displayed figure.** The digest a human signs must cover the exact
   amount they saw — not the amount the transaction later carried. A digest over the final
   transaction still matches itself after a substitution, so it catches nothing.

## Verification recipe

- Table of near-miss inputs, each with its verdict recorded: `1.`, `.5`, `1.2.3`, `1,000`, ` 10`,
  `1e3`, `0`, `0.00`, `00`, `1250`, `12.50`, `12.5`, plus one value longer than the field allows.
- Round-trip property test: for every minor value in a bounded range, format then parse must return
  the same integer. Fuzzing will not find a trailing-dot amount — it needs the targeted table.
- Cross-check one real sample from the live domain against an independent implementation; agreement
  on real bytes outranks a thousand generated fixtures.

## Pitfalls

- **`float` for money is a silent rounding bug**, not a style issue: it passes every happy-path test
  and surfaces once, in production, on the one number that matters.
- **`int(amount)` on `"12.50"` raises or truncates.** Route through the exponent; do not special-case
  the decimal point inline.
- **A permissive regex returns `"1."` as valid.** Anchor `^...$` and require digits on both sides of
  a separator when one is present.
- **Grouping separators (`1,000`) and spaces (` 10`) are not amounts.** Reject them explicitly rather
  than stripping them — stripping turns a pasted thousand into a ten.
- **Fees and totals must be summed in minor units**, then formatted once for display. Summing
  formatted strings (or rounding twice) drifts.
- **Negative and refund values** need the same classification rules; a regex that starts at `[0-9]`
  silently rejects credits instead of parsing them.
