---
name: untrusted-payload-inspection
description: "Use when auditing or hardening an untrusted-payload parser."
version: 1.0.0
category: security
tags: [parser, security, qr, emvco, duitnow, ssrf, fuzzing, audit, service-verification]
floor_scope: [F2, F9, F11]
---

# Untrusted Payload Inspection — build it, then audit it against execution

A payload is a container of text. It carries no signature, issuer, expiry or owner of its
own. Any parser of such payloads exists to turn bytes into **typed observations plus named
unknowns** — never into permission.

The boundary that matters is not "image to text". It is:

```
untrusted text  →  trusted identity  →  permission  →  real-world action
```

Only the first arrow belongs to an inspection service. Everything after it needs an authority
plane and a bound human approval, in a different process, with different credentials.

Covers: QR / payment TLV, URL and deep-link payloads, opaque tokens, and any service that
inspects them — including auditing someone else's implementation of one.

## Always-on rules

1. **No `ALLOW` / `EXECUTE` verdict.** Vocabulary is `DENY`, `HOLD`, `ELIGIBLE`. `ELIGIBLE` means
   "no disqualifying static defect found", not "safe". A downstream consumer must still resolve
   authority and obtain approval.
2. **Every result carries an explicit `unknowns` list.** Name what was *not* established
   (`bank_resolved_recipient`, `redirect_chain`, `token_issuer`, …). A verdict without named
   unknowns reads as clearance to whoever consumes it next.
3. **No egress from the inspection plane.** No fetch, no DNS, no preview, no redirect follow.
   Anything needing the network is a separate service with connection-time destination policy
   covering IPv4 *and* IPv6, re-checked on every redirect and retry. DNS-validate-then-resolve-again
   is a rebinding hole.
4. **Payload is data, never instruction.** It never enters a prompt/instruction channel. An LLM can
   explain the evidence; it cannot be the thing that decides.
5. **Escape before parse, prove the parse after.** Strict length-prefixed parsing with a node/depth
   budget, then reassemble and prove bytes-out == bytes-in. If reassembly differs, every field after
   the split is fiction — say so and stop.
6. **Reject is terminal; do not spend it on valid-but-unsupported input.** HOLD a real payload your
   subset cannot fully read (foreign currency, secondary template, non-ASCII merchant name) and name
   the unsupported field. Reserve reject for malformed, truncated, and checksum-mismatched bytes.
7. **Validate a field's shape, don't merely locate it.** Finding the amount tag is not validating it;
   a permissive regex admits non-numbers into a downstream consumer.
8. **Mask identifiers in everything that leaves the function.** Structure, currency and display name
   stay; recipient IDs, hashes and full query strings are masked. Raw payloads never reach logs —
   log a keyed HMAC digest instead.

## Build order (a service that survives review)

1. `model.py` — `Finding(code, severity, detail, layer)`, `Assessment(verdict, findings, facts,
   display, unknowns)`. Codes are stable strings; severity is ordinal.
2. `parse.py` — strict TLV with a `NO_NEST` set for scalar tags, max depth ~3, node budget, and a
   `start` offset recorded on every node (needed for checksum coverage — see references).
3. `classify.py` — typology only (payment / url / deeplink / token / local credential). No trust.
4. `urlsafety.py` — static string defects only: denied schemes, userinfo, IP literal and loopback
   (SSRF shape), punycode, homoglyph skeleton vs brand tokens, shortener, abuse TLD, odd port.
5. `policy.py` — assemble findings into DENY/HOLD/ELIGIBLE from code sets, not ad-hoc booleans.
6. `receipts.py` — SHA-256 hash-chained JSONL; verify-chain must detect a single edited line.
7. `server.py` — stdlib `ThreadingHTTPServer` first, framework adapter second and import-guarded.
   Keep the core runnable with zero third-party packages so it is testable anywhere.
8. `selftest.py` + `tests/` — the selftest runs with no pytest, so the service can prove itself on
   a host with no toolchain.

Ship `docs/ARCHITECTURE.md` (pipeline, plane separation, data contracts, reason-code table) and
`docs/GAPS.md` (one row per real absence, each with a **closure test**, not a wish).

## Decode layer rules

- Gate on **compressed bytes and pixel dimensions before decoding** (header read: PNG dimensions,
  GIF, etc.). A 40 KB file can declare 40 000 × 40 000 pixels.
- Run the native decoder as a subprocess with `RLIMIT_AS`, `RLIMIT_CPU`, `RLIMIT_NOFILE`,
  `RLIMIT_NPROC`, `os.setsid()`, a fixed argv and a timeout. No shell.
- **Keep every candidate.** One hit per decoder, never merged. Two decoders disagreeing is a
  finding (`DENY` on disagreement), not noise to reconcile silently.
- A container is not a sandbox for a native image library. If there is no isolated worker, ship
  text-payload inspection only and say so.

## Auditing a delivered implementation

Full procedure — build, run, probe, fuzz, corroborate — in
`references/delivered-service-audit.md`. The short form: reproduce every claim with a command;
a claim you could not reproduce is labelled, not softened.

Payment/QR parser specifics (CRC coverage, amount shapes, static-vs-dynamic semantics) in
`references/payment-qr-parsers.md`.

## Pitfalls

- **`rfind("6304")` for CRC coverage is wrong.** A merchant name may contain the literal; slice
  from the parsed element's recorded offset instead. A wrong cut can report `ok` on altered bytes.
- **A permissive amount regex is a data-quality bug.** `[0-9]+(?:\.[0-9]{0,2})?` admits a trailing
  dot (`1.`). Classify integer / decimal / zero / invalid explicitly.
- **`amount_present: false` is an observation, not an explanation.** For a static payment code,
  emit an explicit reason that the payer types the sum and the amount is not bound to the symbol.
- **A reported "tests blocked by missing dependency" is often self-inflicted.** Install their own
  dev-requirements before accepting the blocker; then run the suite.
- **Count files in the archive, not the tree in the prose.** A risk register / CSV / appendix named
  in the delivery tree is frequently absent from the ZIP. Missing evidence is a finding.
- **Floating base image + range-pinned deps = the tested pair is unknowable.** Name it as a release
  blocker, because their own supply-chain gate usually forbids exactly that.
- **Fuzz for the invariant, not just the absence of a crash.** A parser that never raises but returns
  a permissive verdict on malformed input is the more dangerous artifact.
- **Random fuzzing will not find a trailing-dot amount.** Mutate *toward* the boundary with a
  targeted table of near-miss values (`1.`, `.5`, `1,000`, `0`, `1e3`) and record each verdict.
- **An audit that leaves your own code untouched was probably shallow.** Run their defects against
  your equivalent function; report the test-count delta and confirm the tightening created no false
  reject on the real fixture.
- **Two implementations agreeing on one real payload is the strongest evidence you will produce.**
  Say so, and treat any disagreement as the finding of the audit.

## Reporting shape

Claim table (TRUE / FALSE / PARTLY + the deciding command) → what is genuinely good, specifically →
defects with severity → what the audit changed in your own code → parity table if two
implementations exist → residual risks **neither** removes (physical sticker swap, payer-typed
amount, screenshot replay, approval substitution, hostile native decoder).

Close on the limit that survives every fix: both implementations stop at evidence, and neither can
authorize the real-world action.
