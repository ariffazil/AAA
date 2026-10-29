# EUREKA — Test-Time Memory Evolution: memory without selection is a graveyard

**Status:** DRAFT_AWAITING_F13 (2026-10-29) · **Author:** FI-003 (Qwen Code, lane 333-AGI) · **Session:** SEAL-9a6c17a756dd47e1
**Provenance:** arXiv 2610.32046v1 (abstract fetched live from arxiv.org, 2026-10-29) × FI-003 live probes of CHRON / Seal C / iarif-synthesis. Every item labeled VERIFIED (probe receipt) or INTERPRETATION (design).
**Source artifact (durable):** `/root/forge_work/2026-10-29-TTME-evolving-memory-federation-distillation.md` (sha256 f44604272f97a455909e3d7669447934a22f587efd645d4dc82e2ba2ce327c45)
**Kin:** archive-≠-governance · CAPABILITY≠AUTHORITY · govern-capabilities-not-implementations · witness-must-change-future-behaviour · seal-C-CQRS · chron-arrow-of-time · rawrag-paper-vs-aaa-memory-gap-2026-10-24

---

## CORRECTIONS (555 independent verification, 2026-10-29)

11 of 13 audit claims CONFIRMED with exact re-measurement. Two were **stale by the time the verifier looked** (true when filed; this file kept changing) and one **mechanism was wrong**. Corrections are applied at the claim site, above.

- **D4 — WRONG MECHANISM (E2).** The Seal C drain is `arif_memory(mode="consolidate")` (`arifosmcp/tools/memory.py:1246`), actor-allowlist gated, with **no caller anywhere**. `iarif-synthesis.service` is the Seal B synthesis engine and never touches memory or proposals. Conclusion unchanged, cause corrected.
- **D5 — OVERSTATED (the adaptation "loop").** `emergence_state.py` reads `adaptations.jsonl` and writes the decisions; **nothing writes the adaptations** — the 5 rows were hand-authored. `decisions()` skips already-decided ids, so a falsifier is checked **once and never again**. Decisions are 2 days stale and `emergence_state.json` shows `POSING` after `EMERGENT` — the loop **regressed**.
- **D2 / D3 — now published** (commit `828d60d99`): `stats()` carries `ledger_rows` alongside `total_records`, and exposes `independent_reviews` / `non_independent_reviews` / `reviews_without_independence_claim`.
- **Nuance — lessons.** "No lesson binds" holds, but 2 lessons ARE `actionable` and are passed into `lessons_consumed` on 119/153 predictions; they are blocked from promotion only by `promotion_eligible=False` and `policy_applied: False`.
- **New minor defect (not mine):** `AAA/scripts/generate-session-briefing.sh:137` prints `entropy_delta` from the last RSI row — a key that does not exist in the schema, so it always renders "Delta: 0".
- **Name-collision hazard:** three unrelated things are called "RSI" here — the stop-correctness ledger (`/root/VAULT999/rsi_ledger.jsonl`), the arifFlow seal ledger (`/root/.local/share/arifos/rsi-ledger.jsonl`, read by `AAA/governance/scripts/frame_measure.py`), and `AAA/rsi/` (recursive-self-improvement atoms).
- **Audit anchoring:** the claims in this document are anchored at commit `1dd8d2020`. Re-read them at a named commit before citing them.

---

## E1 — In a checker-bearing loop, evolving memory beats evolving weights — cheaper [VERIFIED · paper]

**Source:** arXiv 2610.32046v1, submitted 2026-10-23. TTME (Test-Time Memory Evolution) updates an **external memory** of distilled experience instead of model weights; both arms run the same discovery framework, only the adaptation method differs.

**Claims (abstract, verbatim scope):** TTME outperforms TTT on **all five mathematical tasks**; computational cost **−82.8 %…−84.6 % FLOPs** and **−47.7 %…−58.4 % runtime**. Regime: open-weight models, discovery loop with an **automatic checker/scorer**.

**Not claimed here:** "2 frameworks / 3 models", "Qwen3-8B on 3 tasks" — present in secondary summaries, absent from the abstract, unverified in this record.

**Failure class:** any plan that spends on *weight evolution* (self-RL, online fine-tune, LoRA) inside a checker-bearing loop while leaving the memory lane at zero is spending on the expensive substrate when the cheap one is unexploited.

## E2 — Our memory lane is a graveyard, not a metabolism [VERIFIED · probes 2026-10-29]

**Probe:** `/root/.local/share/arifos/memory_proposals/` holds **216** undrained proposals, oldest **2026-09-29**. ⚠️ **MECHANISM CORRECTED (555-verifier, D4, 2026-10-29):** my first probe attributed the stalled drain to `iarif-synthesis.service` being inactive+disabled. **That attribution was wrong.** `iarif-synthesis.service` is the **Seal B synthesis engine** (`POST :18101/synthesize`, `/root/A-FORGE/iarif_synthesis.py`) and contains **zero** references to memory or proposals — enabling it would NOT drain this queue. The actual drain is `arif_memory(mode="consolidate")` in `arifosmcp/tools/memory.py:1246`, gated on an `actor_id` allowlist (`ARIF_MEMORY_WRITERS`), with **no caller anywhere** (no cron, no timer, no script, no A-FORGE TS). The conclusion (216 undrained) stands; the cause was misattributed.

**Probe (buffer quality, python scan of all 216 files):** actor/session distribution → **124** `arifos-federation@audit-session-p1-04`, **91** `test-actor@observe-only-session`, **1** real (`qwen-code/FI-003`). **62/216** have content ≤2 chars; **1/216** carries tags.

**Failure class:** the Seal C buffer is **99.5 % test noise**. Draining it as-is would import garbage into institutional memory — a live poisoning vector, not a memory.

**Binds:** do **not** start any drain before a selection gate exists. The drain is not the missing piece; the filter is.

## E3 — The Arrow stops before policy: 14 lessons, 0 ACTIVE [VERIFIED · probes 2026-10-29]

**Probe:** `chron_lessons status=active` → **`[]`** (total 14; 2 CANDIDATE, rest DIAGNOSTIC/SUPERSEDED). `chron_store_stats` → **learn 7** of **199 568** episodes (**0.0035 %**) against observe 199 343.

**Probe (the system's own words, from `chron_generate_predictions` output):** `"policy_applied": false`, `"policy_note": "no lesson is applied as policy: none yet meets the promotion gate (external validation is not implemented)"`. Same run reports `blind_lesson_share 0.923` → calibration graded **INSUFFICIENT**, which is why the calibrator anchored the new prediction on 0.5 instead of its 0.30 proposal.

**Failure class:** the promotion gate's **external validation is not implemented**, so no lesson can ever become policy. The Arrow is closed at Lesson(CANDIDATE) — exactly "archive ≠ governance", stated in the runtime, not in prose.

## E4 — No lesson text ever reaches prediction generation [VERIFIED · code probe]

**Probe:** `grep -n lesson /root/chron/chron_prediction.py` → lessons reach the generator only as (a) **hardcoded error classes** (`RANGE_STALE_AT_MINT` at :585, :786 — a lesson frozen as a fallback class, not as a consulted rule), and (b) the `blind_lesson_share` **veto** on calibration (:847–984). There is **no path that injects lesson content** into what the next prediction asserts.

**Failure class:** the loop can *measure* lessons and *veto on* lessons, but cannot *act from* lessons. Measurement without consumption is a dashboard, not a loop.

## E5 — In-house test of the paper's thesis: our own prior distillation changed nothing [VERIFIED · probes 2026-10-29]

**Probe:** the Raw-RAG eureka (arXiv 2610.30755) was landed **2026-10-24** as a dream proposal (`/var/spool/arifos/dream-proposals/qwen/dream-20261024T054044Z-rawrag-memory-lane.jsonl`). Federation-wide grep for `raw.?rag|2610.30755` across `arifOS/arifosmcp`, `AAA/canon`, `AAA/eurekas`, `AAA/skills`, `chron`, `A-FORGE/src` → **one hit, a false positive** ("raw rage" in `maruah_critic.py`). **Five days on: zero downstream artifacts.** Root cause, verified by the 555 cell: the dream inbox has **no reader** — `arif-dream.timer` and `arif-dream-distill.timer` exist but are **disabled + inactive**, `consolidate.py` audits Redis/Qdrant/Supabase and never opens the inbox, and `A-FORGE/scripts/auto-dream-spool.ts` **writes** to the spool without reading it. The `_quarantine/` dir is empty, proving the coordinator the spec describes was never implemented.

**Failure class:** the arifOS memory lane fails the exact test the paper passes — a distilled lesson was written, and nothing changed. TTME's advantage is not "we have memory"; it is "memory is consumed".

## E6 — Distilled rules [INTERPRETATION — proposed, unratified]

- **R1 — Memory ≠ capability.** Capability = distilled + selected + consumed.
- **R2 — A lesson that cannot change a decision is a log line.** Test: name the decision it changed.
- **R3 — Selection gate before drain.** Never start a memory drain without a quality filter (E2: 99.5 % noise).
- **R4 — The automatic checker is the precondition.** TTME's favourable regime is *loop has a scorer*; arifOS has one (F1–F13 gates, brier scoring, numeric-audit, `arif_judge`, peer audits) → our loops sit in the favourable regime.
- **R5 — Budget inversion.** In checker-bearing loops, invest in the memory lane (distillation, selection, promotion, retrieval) before weight evolution.
- **R6 — Close the arrow.** Verification → Lesson(**ACTIVE**) → consumed by the next prediction. Today it stops at CANDIDATE (E3, E4).

**Binds (each needs a forge lane, none done here):** the selection gate + buffer purge (215 test proposals); the Lesson→prediction injection path; the external-validation half of the promotion gate; FRAME metrics `learn_lane_utilization` / `active_lesson_count` / `seal_c_backlog_max_age_days` / `lesson_text_injection_rate` (baselines 0.0035 % / 0 / 30+ / 0 — **no new dashboard**).

**Falsifiers:** (1) build selection gate + promotion path and `learn_lane_utilization` does not rise → R1/R6 wrong for our substrate; (2) draining *with* a filter still yields junk → defect is upstream in the proposal writers; (3) TTME's advantage vanishes outside math tasks or with a weak checker → R4's scope claim is wrong.

**Landings made with this eureka:** CHRON event `ttme-memory-lane-metabolizes-2026-12` → prediction **`pred-b7ba8ca80432`** (target 2026-12-15, proposed confidence 0.30, calibrated 0.566 under an INSUFFICIENT-grade store) · dream proposal `dream-20261029T1200Z-ttme-evolving-memory.jsonl` (behavioural rule: selection gate before drain; promote-or-retire for lessons).

## Sources

- arXiv 2610.32046v1 — abstract fetched live 2026-10-29 (`https://arxiv.org/abs/2610.32046`).
- Live probes 2026-10-29: `chron_store_stats`, `chron_lessons`, `chron_generate_predictions`, `systemctl is-active/is-enabled iarif-synthesis.service`, buffer scan of `/root/.local/share/arifos/memory_proposals/`, `grep -n lesson /root/chron/chron_prediction.py`, federation-wide grep for the Raw-RAG precedent.
- Contrast paper: arXiv 2610.30755 → `/root/forge_work/2026-10-24-rawrag-vs-aaa-memory-contrast.md`.
