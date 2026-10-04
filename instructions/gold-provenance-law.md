# ARIFOS::GOLD_PROVENANCE_LAW::v1

> **Status:** F13_RATIFIED_SOVEREIGN (2026-10-04)
> **Authority:** Muhammad Arif bin Fazil (F13 SOVEREIGN) — ratified via single-word "SAH"
> **Proposed by:** F13 SOVEREIGN (Muhammad Arif bin Fazil), in-session 2026-10-04,
> during the I-ARIF-CANON Gold calibration review — quote: *"setiap fakta yang Gold
> gunakan untuk menghukum mesti ada fail sumber di sebelahnya… Fakta yang tiada
> sumber tak boleh jadi asas FAIL. Paling tinggi, ia boleh jadi HOLD."*
> **Clause 3 (Symmetry):** Formulated and staged by 333-AGI (FI-003), audited and verified by Antigravity (FI-004).
> **Canonical:** `/root/AAA/instructions/gold-provenance-law.md`

## The Law (F13 original)

```
TIADA FAIL SUMBER  ⟹  MAKSIMUM ADALAH HOLD (BUKAN FAIL)
```

1. **Syarat sabit kesalahan (FAIL):** A judge (Gold, eval harness, DPO curator,
   any rubric-bearing scorer) may emit **FAIL** only when the factual claim it
   condemns is directly contradicted or grounded by a **primary source file**
   sitting beside the rubric — official URL, paper DOI, git commit, or raw
   probe log.
2. **Sempadan tanpa bukti:** Any rubric fact without a primary-source
   reference may never ground a FAIL. Its ceiling is **HOLD** (or UNKNOWN).

## Clause 3 (333-AGI sharpening — SYMMETRY, from the same founding failure)

The founding counterexample was an unjust **PASS**, not an unjust FAIL:

- Probe p2.2 asked who created MalayMMLU. Answer credited only "YTL AI Labs".
- Verified primary source (YTL Power press release, 2024-09-24, re-fetched
  2026-10-04): *"YTL AI Labs, in collaboration with Universiti Malaya (UM)…
  Professor Ir. Dr Chan Chee Seng, Dean of FCSIT UM, who co-led the development
  of the MalayMMLU with Foong Chee Mun, CEO of YTL AI Labs."*
- The old Gold PASSED an answer that erased UM and Dr Chan — because the
  rubric carried no sourced fact to check completeness against.

Therefore:

```
TIADA FAIL SUMBER ⟹ TIADA LULUS VERIFIKASI-FAKTA JUGA
```

A **PASS** on any factual-completeness/accuracy criterion likewise requires
the rubric fact to carry its primary source. Without it, the criterion may
score only form/process (structure, refusal boundaries, length), never
fact-correctness — or cap at HOLD. Unsourced rubrics must neither convict
nor acquit on facts.

## Binding annex — Calibration Protocol (F13, same session)

A judge is valid only after passing BOTH, with rules FROZEN before each run:

1. **Unseen-failure run:** score the held-out failure set (e.g. remaining 45
   BBB rows) with zero rule edits — failures must still be caught.
2. **True-positive run:** score the chosen/good responses (e.g. 96 chosen
   halves of i-arif-dpo.jsonl) — zero may FAIL; any FAIL = rubric too strict,
   recalibrate and repeat BOTH runs.

Rules written after reading the test answers (answer-schema) are Goodharted
and invalid as governance.

## Evidence file (all verified 2026-10-04 by 333-AGI & Antigravity)

| Artifact | Verification |
|---|---|
| YTL–UM MalayMMLU press release | `https://www.ytlpowerinternational.com/press-releases/ytl-ai-labs-releases-the-first-malaymmlu` — fetched live 2026-10-04; contains the UM co-lead quote verbatim |
| I-ARIF-CANON @ main | HF API sha `b67c1f15`; card carries honest labels: "50 forged multi-turn tool-call scenario templates", "1,435 active + 100 held-out" (cache-red herring confirmed resolved) |
| `i-arif-dpo.jsonl` | 96 lines @ main (the "96 chosen" of the protocol) |
| Overfit harness | `/tmp/triadic_gold_harness_calibrated.py` (5,120 B, 2026-10-04 14:19) — rules rewritten post-observation; demonstrates the failure class this law bans |
| Nemotron lineage claim | **UNSOURCED on this machine** — `federation-models.json` routes over nemotron model keys, but routing ≠ training lineage; no manifest found. Under this law: ceiling HOLD, not FAIL |

## Scope

All federation judges: I-ARIF Gold harness, hermes-eval (P1), DPO curation,
any future LLM-as-judge. This is F2 TRUTH + evidence-hierarchy extended to
evaluators — no new registry, no new tooling, one rule over an existing,
twice-demonstrated failure class.

## Ratification

Ratified by Muhammad Arif bin Fazil (F13 SOVEREIGN) on 2026-10-04 (`SAH`).
Promoted from `/root/AAA/.staged/GOLD_PROVENANCE_LAW-v1.md` to canonical instructions.
