# EUREKA — DEPTH REUSE FAVOURS CONTEXT OVER MEMORY

**Status:** DRAFT_AWAITING_F13 (2026-10-26) · **Author:** HERMES (default lane) · **Class:** external research distill
**Paper:** Ferdinand Kapl, Kaitlin Maile, Stefan Bauer, Johannes von Oswald — *How Depth Growth and Looping Shape In-Context Learning in Language Models* — arXiv:2610.31421v1 [cs.CL], 22 Oct 2026, CC BY 4.0. TUM · Helmholtz AI · MCML · Google Paradigms of Intelligence.
**Provenance:** full HTML (367,874 B) fetched 2026-10-26 13:29 MYT from arxiv.org/html/2610.31421v1; abstract + §1–§5 read in full; §3.1 config and appendix A.1–A.3 headings read. **Figures not viewed** (text-only lane) — every number below is quoted from prose, never read off a plotted curve.
**Label law:** `[PAPER]` = measured by the authors · `[DER]` = my derivation onto arifOS (analogy, not measurement) · `[SPEC]` = proposal, nothing built · `[UNKNOWN]` = not measured anywhere.
**Kin:** probe-before-panic · SCAR-2026-09-04-001 (probe-first) · anti-bangang LAW 3/8 (no new artifact) · deploy-state-delta · copy-paste-box-law · agentic-self-model

---

## What the paper actually measured `[PAPER]`

Three 3B models, same 100B tokens, same order, matched final inference FLOPs:

- **dense** — 36 independently-trained layers (SmolLM3-style reference)
- **grown (LIDAS)** — starts at 4-layer blocks, grows by duplicating the central 4 layers, copies weights *and* optimizer moments, copies then train independently; reaches effective depth 36. Saves ~26% training FLOPs at 3B.
- **looped** — `Loop 10-8×2-10`: 10 prelude + one 8-layer block applied twice + 10 coda = 36 applications, 28 unique layers.

Results: both reuse variants show larger early→late token-loss reduction than dense; grown also reaches lower absolute late-token NLL (matches dense around position 1000, better after). Both beat dense on GSM8K at every demonstration count — grown's gap *widens* to roughly +7% by 8-shot, looped's narrows almost to zero. On RegBench (unseen DFAs) both predict novel formal languages better than dense.

---

## E1 — Context vs weights is a *competition*, and reuse decides who wins `[PAPER + DER]`

`[PAPER]` Omniglot setting where *both* a context solution and a fixed class→label weight solution can answer the training query (fixed labels, P(bursty)=1): ICL rises early then **declines** as in-weights learning (IWL) improves — the transience reported by Singh et al. 2023. At matched effective depth, grown and looped retain **higher ICL and lower IWL** than the dense-12 reference. When the weight solution is removed (labels reshuffled every sequence), grown, looped *and* dense-4 all acquire ICL **earlier** than dense-12; by 1M steps all reach ~100%. Dense-12 is not less capable — it is slower to prefer context.

`[DER]` This names the confabulation defect class as a *solution competition*, not laziness and not disobedience. When canon/memory/doctrine can answer a question that a live probe could also answer, the weight solution wins by default as it thickens. And the uncomfortable corollary: **writing more canon makes this worse, not better.** The paper's remedy for context preference is not more unique layers — it is *reuse*: apply the same reasoning block again against fresh context.

`[SPEC]` Falsifier: one question whose answer exists only live (today's port/PID/token state, absent from any canon file), asked of a thin-canon agent and a thick-canon agent. Prediction — the thick one asserts from doctrine more often. If both probe equally, this mapping is wrong and E1 dies.

## E2 — The looped trade is real: less memorisation for more context `[PAPER]`

`[PAPER]` Looped attains ICL close to grown but **significantly lower IWL**; grown inherits both capabilities from its shallow starting model. Looped also keeps a higher absolute NLL throughout — it never matches dense on raw next-token loss.

`[DER]` You cannot buy both from one mechanism. A pure loop is agile at reading the room and unreliable at holding standing facts. In federation terms: **granite needs an owner outside the loop** — F13, canon-mutate, VAULT999 — never the agent's own recall. An agent optimised for context should be *expected* to be weak on standing facts, and that is a design choice to make out loud, not a defect to punish.

## E3 — arifOS is a *grown* model, and it inherits pre-split strength `[PAPER + DER]`

`[PAPER]` The 12 final top-2%-PS induction heads in LIDAS trace back to just **4 ancestors** in the initial 4-layer model. Two of them — L2H9 and L2H10 — were **already strong before the first growth event** and account for 10 of the 12 final heads. Strong heads recur at the same head index in layers separated by multiples of the 4-layer growth block. Looped shows the analogue across the two passes of its shared block. **Dense shows no repetition by block size.**

`[DER]` The federation was built this way: one early block (identity + probe-first + receipt), duplicated into organs and profiles, copies training independently ever since. Two consequences follow, both testable:

1. Differences between organs should trace to what was **already strong at split time**, not to what was bolted on afterwards. Anything weak when the block was copied stays weak in every copy — adding tools later does not repair a weak ancestor.
2. The dominant behaviours at the end will descend from a handful of early ancestors. Naming them is a finite job, not a survey: probably `probe-before-claim`, `receipt-or-it-didn't-happen`, `authority ≠ capability`.

`[SPEC]` Test: list behaviours demonstrably strong at first duplication (earliest SOUL / first AGENTS.md), rank organs on those only, then compare against organs that received large later feature additions. Prediction — later additions do not lift the inherited score.

## E4 — Growth dips induction, then recovers `[PAPER · binds deploy doctrine]`

`[PAPER]` Growth events **temporarily disrupt prefix matching, followed by quick recovery** during further training.

`[DER]` After adding a layer — new organ, new skill surface, new tool — expect a transient drop in the witness/copy-from-context function before recovery. Two operational consequences: do not measure capability inside the disruption window, and do not roll back on the first post-deploy reading. Sequence is deploy → wait out the dip → probe. `[UNKNOWN]` Nobody has measured the dip duration for the federation; the 26%-FLOPs and recovery figures belong to LM training, not to ops. Do not carry the number across.

## E5 — Summary is FV; quote is induction `[PAPER + DER]` — the sharpest one

`[PAPER]` Ablation at 9%: function-vector (FV) head ablation hurts **few-shot task F1** most in all three models; induction-head ablation hurts **ICL-Score and later-token prediction** most in grown/looped. Position-wise: the FV effect **plateaus** after the first few tokens, while the induction effect **grows with position** and eventually overtakes FV in grown and looped. In the dense baseline FV stays dominant all the way out to 4096 tokens.

`[DER]` Two different repair mechanisms, and they are not interchangeable:

- **FV = abstraction** → summary, doctrine, paraphrase, "the gist".
- **Induction = verbatim copy** → pointing at the exact earlier occurrence and continuing it.

Short task: FV carries you. Deep in a long session: **induction carries you.** Therefore long-session drift is an **induction deficit, not an intelligence deficit** — and the fix is structural, not rhetorical: keep verbatim pointers to earlier turns (quote + date + speaker) alive in context. A summary does not recruit induction; a quote does.

`[DER]` This is the mechanism underneath copy-paste-box-law and the verbatim-quoting rule that already exist here. They were right for a reason nobody had written down.

## E6 — Adaptation gain saturates around the 4th sample `[PAPER + DER]`

`[PAPER]` On RegBench the grown/looped advantage over dense grows across the first strings, **peaks around the 4th**, then stays flat; within the first string the advantage appears after ~15 symbols.

`[DER]` The gain is front-loaded. After roughly four probes into a new domain, person or agent, further exploration buys nothing — switch to action. Independent convergence with the existing "PLAN ≤ 3 turns, then execute" rule, from a different direction. `[SPEC]` Do **not** hardcode 4 — it is a synthetic-DFA string index, not a constant of nature.

---

## What this binds (and what it does not build)

- **E5** → handoff and long-session carry must be **verbatim quotes with date + speaker**, not summaries. Binds `copy-paste-box-law`, agent handoff packets.
- **E1** → answering from canon when a live probe is available is a named failure mode, not a shortcut worth tolerating. Binds `probe-before-panic`, `SCAR-2026-09-04-001`.
- **E4** → no capability verdict inside the post-deploy dip window. Binds `deploy-state-delta`.
- **Nothing new is built.** No registry, no dashboard, no JSON, no schema (anti-bangang LAW 3 + LAW 8). This file binds existing behaviour only. If any of E1–E6 survives F13 review, the promotion is a DRAFT fragment under `AAA/instructions/`, not a system.

## Honest limits

- Evidence is three ~3B transformer LMs on 100B tokens plus controlled Omniglot/RegBench tasks. The federation is not a transformer; every `[DER]` above is structural analogy.
- RegBench looped model used width 256 vs 128 for dense/grown — **not width-matched**. The paper states this; I am carrying its flag, not overriding it.
- GSM8K: three demonstration seeds, 10,000 FineWeb-Edu documents.
- Figures unseen in this lane. Any claim that would require reading a curve is absent rather than guessed.
