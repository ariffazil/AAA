---
name: money-path-discipline
version: 1.0.0
description: "Use when code carries a money amount or a checksum."
owner: HERMES
category: governance
tags: [money, amount, integer-minor-units, checksum, tlv, payment, float, approval-binding]
floor_scope: [F1, F2, F4, F11]
autonomy_tier: T1
ecology_state: WARM
---

# Money Path Discipline

Rules for any code, parser, API, or report that moves an amount of money, or a checksum over data
that carries an amount. Each rule exists because the naive implementation is wrong in a way no
ordinary test catches and no human notices until real money moves.

Companions: `qr-code-ops` (the QR medium), `wealth-ledger-discipline` (the capital ledger).
This skill is about the **number**, wherever it lives.

## Rule 1 — no float, no silent Decimal, anywhere in the money path

A `float` cannot represent most decimal amounts exactly, and a JSON boundary can turn `Decimal`
into `float` without a warning. Either produces a wrong total that passes every unit test written
with round numbers.

- Amounts are **integer minor units** plus an explicit currency and explicit exponent.
- Convert by **string arithmetic**: split on `.`, right-pad the fraction to the exponent,
  `int(whole) * 10**exp + int(frac)`.
- Add a test that greps the money module's source for `float(` and fails if present. A rule with an
  automated check survives; a rule in a code-review comment does not.

## Rule 2 — an amount with no decimal point is ambiguous; report both readings

`"1250"` in a payment field reads as either 1250 minor units (RM 12.50) or 1250 major units
(RM 1250.00). That is a **100×** difference on the number a human approves. Choosing one silently
is the defect, whichever one you choose.

- Name the reading (`as_minor_units`, `as_major_units_minor`) — never return a bare `amount`.
- Raise the ambiguity as a first-class finding and route it to HOLD. A consumer that must choose
  should have to *see* that it is choosing.
- When the payload carries a decimal point the reading is unambiguous — compute exactly, drop the
  flag.

## Rule 3 — validate the amount's shape before classifying its value

`[0-9]+(\.[0-9]{0,2})?` accepts a **trailing dot**: `"1."` and `"12."` are not numbers, yet they
pass and reach a consumer as well-formed. So do `.5`, `1,000`, `1.2.3`, ` 10`.

```
minor units, no separator   ^[0-9]{1,13}$
major units, 1-2 decimals   ^[0-9]{1,11}\.[0-9]{1,2}$
```

Anything else is `INVALID_AMOUNT` → DENY. Zero is a separate case (`AMOUNT_ZERO` → HOLD): a
zero-amount request carries no intent and should not be handled as malformed.

## Rule 4 — checksum coverage comes from the parsed element, never a string search

Computing over `payload[:payload.rfind("6304") + 4]` is wrong: if any field's **data** contains the
literal `6304` (merchant name, reference, free text) the search finds the wrong offset and computes
over the wrong span — a false mismatch, or a match over the wrong bytes.

- Record the **byte offset of every parsed element**; cut at offset + header length of the element
  that actually carries the checksum.
- Prove the parse first: reassembly must equal the input **exactly**. Otherwise every field after
  the split is fiction and the checksum result means nothing.
- Test with data containing the checksum's own tag literal. That is the only test that catches it.

## Rule 5 — a matching checksum proves the bytes, not the payee

A CRC is a corruption check. It says the payload arrived intact; it says nothing about who is on
the other end. Say that every time a checksum result reaches a human — "CRC OK" reads as "verified
merchant" to anyone who is not a payments engineer.

- A human-readable **recipient name** is the only in-payload anti-fraud field most schemes carry.
  Its absence is a finding, not a formatting gap.
- An **amount**, if the code carries one. On a static code it does not; the payer types the sum and
  the total is not bound to the symbol. Say so rather than leaving it implicit.
- An **integrity tag** verified by the acquirer is invisible here. Presence is not verification.

## Rule 6 — bind approval to what the human saw, not to the transaction

A digest over the final transaction always matches itself. If the displayed amount or recipient
changes between render and approval, nothing detects it.

```
digest(rendered_and_signed) == digest(recomputed_at_execution)
```

Cover the exact object the human was shown — recipient, amount, currency, fees, reference, expiry —
sign it from the human's side, and have the executor recompute from the stored canonical object
before acting. The executor takes a **digest**, not an action object; if any caller can build a
payload and send it onward directly, the binding is decoration.

## Rule 7 — verdict vocabulary must not contain permission

`ELIGIBLE`, `HOLD`, `DENY` describe the *inspection*. There is no `ALLOW` or `EXECUTE` in a
validation vocabulary, because permission cannot be minted by whoever ran the checks. Anything
consuming an inspection result must still resolve authority and obtain approval separately.

## TLV parse hardening (payment payloads and any tag/length format)

**Do not descend into scalar tags.** A generic "value looks like TLV → recurse" rule produces false
nesting: `52` = `6010` (MCC) parses as tag `60`, length `10`, and the tail is misread.

```python
NO_NEST = {"00", "01", "52", "53", "54", "58", "59", "60", "61", "63"}
```

Accept a nested parse only if it consumed the value exactly and raised no error:

```python
if depth < MAX_DEPTH and tag not in NO_NEST and length >= 4 and _is_tlv_head(value):
    nested, nested_errors = parse_tlv(value, depth + 1, counter)
    if nested and not nested_errors and _reassemble(nested) == value:
        children = nested
```

**Reassembly proof.** Rebuild from the tree and compare byte for byte; `reassembles: false` is a
first-class finding, not a warning.

```python
def _reassemble(nodes):
    out = []
    for n in nodes:
        body = _reassemble(n["children"]) if n["children"] else n["value"]
        out.append(f'{n["tag"]}{len(body):02d}{body}')
    return "".join(out)
```

**Checksum offset**, using the recorded `start`:

```python
crc_nodes = [n for n in nodes if n["tag"] == "63" and not n["children"]]
if not crc_nodes or len(str(claimed)) != 4:
    state = "malformed"
else:
    cut = crc_nodes[-1]["start"] + 4
    computed = crc16_ccitt_false(payload[:cut].encode("utf-8"))
    state = "ok" if computed.upper() == str(claimed).upper() else "mismatch"
```

CRC-16/CCITT-FALSE: polynomial `0x1021`, init `0xFFFF`, no reflection, no final xor. Keep the
known vector `crc16(b"123456789") == "29B1"` — cheapest way to catch a wrong variant.

**Test corpus that finds the bugs:** checksum vector · merchant name containing the checksum tag
literal · amounts `"1."`, `".5"`, `"1,000"`, `"1.2.3"` · amount `"1250"` with no decimal point ·
MCC `6010` inside tag `52` · duplicate tag · truncated tail · 100k+ random strings from the tag
alphabet with a fixed seed, asserting no uncaught exception. A parser that raises on untrusted input
is an attack surface.

## Reporting shape

Return facts, findings, and a named `unknowns` list — what inspection did **not** establish
(bank-resolved recipient, account status, issuer authenticity, physical substitution, transaction
authorisation). A consumer that acts without reading `unknowns` is misusing the output.

## Pitfalls

- **A redacted display is not a redacted record.** Mask the recipient identifier and the checksum
  in everything the function returns, not only the pretty view — the raw copy reaches logs.
- **Currency exponent is not always 2.** MYR/EUR/USD are 2; JPY is 0; KWD/BHD are 3. Table-driven,
  and an unknown currency is HOLD, never a default of 2.
- **Amount presence and initiation method are independent.** A static code can carry an amount; a
  dynamic code can lack one. Parse both; never derive one from the other.
- **Report the parse error's offset.** "Invalid amount" with no byte position cannot be debugged and
  cannot be told apart from a mis-split.
- **An unreadable input is HOLD, never a fabricated payload.** Size gate, pixel gate, timeout and
  decoder-missing are each a reason code with no payload asserted.

DITEMPA BUKAN DIBERI
