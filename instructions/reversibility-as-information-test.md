# Reversibility as Information-Preservation Test

> **Status:** DRAFT_AWAITING_F13 — extracted from AGENT-STACK-2026 headroom CCR + caveman two-layer analysis (2026-09-19)
> **Source eureka:** Compression Ratio ≠ Information Retention. The test of compression is whether the original can be reconstructed.
> **Applies to:** Memory writes, cache eviction, scar compression, observation retention, VAULT999 store, model context compression.
> **Filter test passed:** ✅ survives implementation changes ✅ re-examinable in 2 years ✅ not vendor-specific ✅ changes future architecture decisions ✅ not merely tool preference.

## The Mistake The Industry Makes

Marketing conflates **compression ratio** with **information retention**:

```text
"50% compression" ← sounds better than 33%
```

But the question is not how small. The question is:

```text
Can the original be reconstructed?
```

If yes → compression. If no → **destruction**.

`headroom` (CCR = Compress-Cache-Retrieve) makes this distinction explicit. The original is cached locally. The agent can call `headroom_retrieve` to fetch it back. Loss is recoverable.

`caveman` (HONEST-NUMBERS.md) makes the same admission explicitly: local savings are *inferred*, not billing-verified. Some "compression" is actually lossy truncation.

## The Doctrine

```text
Compression without reversibility
=
Information destruction
```

Every system that purports to "compress" must answer:

1. **Is the original recoverable?** (yes → compression, no → destruction, partial → lossy)
2. **What is the cost of recovery?** (cheap → compression, expensive → lossy, infinite → destruction)
4. **What is the loss budget?** (zero → reversible, small → lossy with audit, large → destructive — and the system must say so)

## Three Classes of Compression

| Class | Reversibility | Recovery cost | Acceptable use |
|---|---|---|---|
| **Reversible** | Total | O(1) | Memory, cache, context window. Default. |
| **Lossy** | Partial | O(re-fetch) | Logs, telemetry, telemetry summaries. Audit-marked. |
| **Destructive** | None | ∞ | Forbidden unless explicitly scoped + attested. |

The federation must declare which class each compression operates in. Implicit destructive compression is the failure mode.

## Concrete Tests

| Test | Question | If NO |
|---|---|---|
| **T1 — Retrieval test** | Can the original be reconstructed from the compressed form + auxiliary data? | Mark as lossy. |
| **T2 — Cost test** | What does reconstruction cost? If unbounded → destructive. | Mark as lossy or destructive. |
| **T3 — Audit test** | Is the loss budget declared in advance and attested? | Mark as destructive. |
| **T4 — Receipt test** | Does the compressed output carry a receipt indicating class? | Mark as destructive. |

A system that fails T1–T4 must not call its operation "compression." It is destruction.

## Federation Mapping

| Subsystem | Class | Test passed? |
|---|---|---|
| VAULT999 | Reversible (append-only) | ✅ T1–T4 |
| Claim-Receipt Binding | Reversible (handle in same breath) | ✅ T1–T4 |
| Memory Promotion Gate | Lossy (L1–L6 tiering) | ⚠️ T3 partial — loss budget must be declared |
| `forge_context_compressor` | Lossy (C_dark budgeted) | ⚠️ T3 partial |
| `forge_skill_seal` | Destructive unless promoted | ❌ T1 — irreversible by design |
| Flow Ledger (arifFlow) | Reversible (jcs_body_hash, parent_receipt_hashes) | ✅ T1–T4 |

## Falsifiability

If systems that declare "lossy compression" but fail T2 (unbounded recovery cost) cause no observable harm over 24 months, the doctrine is over-specified. If "reversible" claims that fail T1 (cannot reconstruct) cause no governance failures, the doctrine is theatre.

## Related Doctrines

- State-Transition Discipline — naming what survives vs what is consumed.
- Witness Zen Doctrine — every loss must be witnessed.
- Capability-Gate — capability that loses information is not a capability, it's a degradation.
- Capability-Rich / Authority-Poor Theorem — destructive compression is authority-poor in disguise.

## Compression

> **The test of compression is reconstruction. If you cannot retrieve the original, you did not compress — you destroyed.**

DITEMPA BUKAN DIBERI ⚒️