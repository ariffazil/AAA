# Factual claims inside structurally-correct audits

A peer audit can be **structurally perfect** — correct methodology, correct verdict logic, correct layer separation — while carrying **one stale factual claim** embedded inside the prose rather than in a table or finding line. This is one of the most dangerous failure modes because the audit LOOKS trustworthy and the verdict is usually still defensible, but a downstream consumer picks up the stale constant and bakes it into a decision.

## Observed instance (2026-08-08): OpenClaw's Hermes audit

OpenClaw ran a Hermes alignment audit and emitted:

> "ALIGNED · 8/8 architectural layers pass · 0 constitutional violations"

The verdict logic was sound, the layer separation was correct, the verdict was SEAL. But one line read:

> "Epistemic discipline: OBS/DER/INT/SPEC/UNKNOWN labels, **confidence cap 0.90**"

This is **incorrect per sealed canon**. FLOOR_TABLE.json §`f7_canonical_form` (F13-ratified 2026-07-23):

> `Ω₀ ∈ [0.03, 0.05]`. Confidence cap = 1 − Ω₀ ∈ **[0.95, 0.97]**.

The 0.90 cap was **deprecated and abolished** 2026-07-23, listed explicitly under `deprecated_versions` with: *"0.90 cap inconsistent with Ω₀ band."* It is documented in GENESIS/000_KERNEL_CANON.md §3.2 as a historical footnote — the kind of value that sticks in an instruction layer because the old AGENTS.md carried it before the canon was unified.

## Why this matters

The OpenClaw verdict ("Hermes ALIGNED, SEAL") is **still correct** — the 0.90 vs 0.97 difference is cosmetic in the alignment context. But if that stale value is consumed by a downstream decision (e.g., an agent that hard-codes `confidence_cap = 0.90` from an OpenClaw-sourced instruction), it could reject valid SEAL-grade outputs that claim confidence 0.91–0.96.

The real failure mode is **instruction-layer contamination**, not audit mis-classification. The OpenClaw agent is consuming stale F7 doctrine from its AGENTS.md / SOUL.md fragment, and emitting that stale value in audits. The contamination propagates silently.

## Defense when receiving peer audits

1. Read the **factual claims embedded in prose or tables** — not just the verdict line. Stale numbers hide inside summaries, tables, and "what the system does" paragraphs.
2. Re-verify every numeric claim against the **current sealed canon** (FLOOR_TABLE.json is the machine-readable SOT; GENESIS/000 is the prose SOT; they should agree).
3. When you find a stale value: correct it in your report, note the source (peer audit + "stale 0.90 → current [0.95, 0.97]"), and recommend a patch to the peer's instruction layer.
4. **Do not downgrade the peer's overall verdict** unless the stale value changes the outcome. F7 cap 0.90 vs 0.97 is cosmetic for Hermes alignment. If the stale value affected a floor gate (e.g., "W³ ≥ 0.95" claimed as "W³ ≥ 0.80"), that would be a verdict-altering error requiring a re-audit.

## Defense when producing your own audits

1. Cross-check every constant you cite against FLOOR_TABLE.json + GENESIS/000 before sealing. If you can't find the value in the current sealed canon, flag it as PLAUSIBLE (per F2 band taxonomy) rather than asserting it as fact.
2. Prefer the band form (e.g., "confidence cap [0.95, 0.97]") over single-number form ("0.96") — bands survive stale-value detection because they make the source canon explicit.
3. Include the source canon path in any audit claim (e.g., "FLOOR_TABLE.json §f7_canonical_form" not just "F7").

## Class-level lesson

The most dangerous errors in peer audits are the ones the peer gets right — structurally correct with a wrong constant inside. The antidote is F2: verify the claim, not the verdict structure. A perfectly-formatted table with a stale value is more dangerous than an obvious error, because it gets read with confidence.

## Pattern taxonomy

| Audit type | Verdict | Risk |
|---|---|---|
| Structurally wrong, factual claim correct | easy to catch | low — methodology failure visible |
| Structurally correct, factual claim correct | ideal | none |
| Structurally correct, factual claim stale | hard to catch | **medium-high — instruction-layer contamination propagates silently** |
| Structurally correct, factual claim fabricated | easy to catch if you re-verify | medium — peer hallucination |

The third row is the silent-killer category. Defend with: re-verify every numeric constant, prefer band form, cite source canon paths.

## Related F7 facts (current sealed canon)

| Concept | Value | Source |
|---|---|---|
| Humility band | Ω₀ ∈ [0.03, 0.05] | FLOOR_TABLE.json §f7_canonical_form |
| Confidence cap | 1 − Ω₀ ∈ [0.95, 0.97] | FLOOR_TABLE.json §f7_canonical_form |
| Operational ceiling | 0.96 | canonical natural-form: "No fake certainty. Confidence cannot exceed 0.97, and the standard operational ceiling is 0.96." |
| Deprecated | "0.90" | FLOOR_TABLE.json §f7_canonical_form.deprecated_versions (abolished 2026-07-23) |

If any peer audit cites a confidence cap of 0.90, 0.95 alone, or any single number outside the band — flag it.
