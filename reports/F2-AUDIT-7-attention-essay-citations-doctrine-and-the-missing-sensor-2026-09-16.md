# F2 AUDIT #7 — the attention essay: citations verified, doctrine diffed, and the one part that was missing

**Date:** 2026-09-16T03:20Z · **Actor:** HERMES · **Trigger:** external essay on post-AGI attention
economics (pasted by F13 for audit — the standing pattern: verify against primary sources, do not
import whole).
**Consequence class (C18):** one sensor added (`attention-metrics.py`, wired as sweep C21) + one
observability fix in WELL. Reversible. No canon ratified — the doctrine delta is staged, not sealed.

---

## 1. CITATIONS — ALL FOUR VERIFIED, ZERO FABRICATED

| claim in the essay | primary source | verdict |
|---|---|---|
| inference cost $20 → $0.07 per M tokens, Nov 2022 → Oct 2024, >280× | Stanford HAI **AI Index 2025** ("Models Become Cheaper to Use"; GPT-3.5-equivalent 64.8% MMLU) | **EXACT** |
| METR: task-completion horizons lengthening | METR, arXiv **2503.14499** — 50% time horizon ≈ 50 min (Claude 3.7 Sonnet), **doubling ≈ every 7 months since 2019** | **CORRECT**; the essay's own caveat ("not unrestricted real-world autonomy") matches the paper's framing |
| ~14% productivity gain, larger for less-experienced workers | Brynjolfsson, Li & Raymond, **NBER w31161** (5,179 agents) | **EXACT** (≈14% avg, ≈34% for novices) |
| BCG: AI-assisted *less* likely correct on an outside-frontier task | Dell'Acqua et al., HBS **"Navigating the Jagged Technological Frontier"** — **19% less likely** | **CORRECT** (the essay omits the figure; it is 19%) |
| Simon 1971 / attention economics; NIST AI RMF scope | Simon, "Designing Organizations for an Information-Rich World"; NIST AI RMF (monitor/verify/validate/evaluate) | **CORRECT** |

No invented numbers, no misattributed studies. That is not the usual outcome for this class of
artifact tonight — three earlier external artifacts each carried fabricated skills and one carried
notation that would have corrupted 67 skills.

## 2. DOCTRINE DIFF — ~28 OF 35 SECTIONS ARE ALREADY SEALED HERE

The essay presents its core as discovery. In this federation it is largely **existing ratified
doctrine**, and the diff is what matters:

| essay | already held as |
|---|---|
| §1 attention is the ultimate cost | `sovereign-attention-preservation.md` — **W₈₈₈**, F13_RATIFIED_CHAT 2026-09-13 |
| §10 don't ask what you can resolve | same file §4 + `human-attention-membrane.md` (TECHNICAL ≠ SOVEREIGN question) |
| §7 agent as membrane/condenser | `human-attention-membrane.md` + `attention-graph.md` (19 KB) |
| §24 silence is a valid action | `attention-kill-criterion.md`; the essay's "13 days of catastrophic silence" is **literally this session's skill-mesh-sync case** (stopped 2026-08-11, unnoticed 35 days) |
| §11–13 escalation by impact/irreversibility | `escalation-boundary.md` (888 lanes) + `three-consequence-domains.md` |
| §17 attention budget, §18 attention debt | 9 and 8 instruction files respectively |
| §26 disagreement → evidence, not arbitration | `musyawarah.md` + `FORGE-musyawarah-gotong` |

**Genuinely absent before tonight (grepped across instructions/ + governance/ + canon/):**
`attention ROI` — 0 files · `interruption rate` — 0 · `epistemic attention` — 0 ·
`context reconstruction` — 0 · `condenser` — 0 · `human leverage` — 0 ·
`false escalation` — 0 · `missed escalation` — 0.

So the delta is **not philosophy — it is instrumentation.** W₈₈₈ has been enforced by obligation
since 2026-09-13 and never once by measurement. Its own file already admits the shape of the
problem: *"W₈₈₈ is declared but was not measurable, so compliance was a claim rather than a
witness."*

## 3. WHAT WAS BUILT — AND WHAT ITS FIRST RUN FOUND

`/root/scripts/attention-metrics.py`, wired into the sweep as **C21** (runs with the other 17,
4×/day, ~3 s).

**A1 `scheduled_silence`** — parses crontab, derives each job's real firing cadence over 45 days,
compares log mtime. Honest levels: `SILENT` (used to grow, stopped), `UNWITNESSED` (0-byte log —
no data is not all-clear), `UNMEASURED` (no redirect — cannot be judged, never reported healthy).

**A2 `attention_cadence`** — first real baseline, from `state.db`, Arif DM, last 20 sessions:

```
198 arif turns · 1668 tool calls · 126 assistant questions
→ 11.87 arif turns per 100 tool calls
→ 0.64 questions per arif turn
→ worst: 20260916_012137_15b55ae9 (16 asks / 14 turns / 247 tools)
```

**Level INFO, deliberately.** A measurement of a human's burden must never become a gate to
optimise — see §5.

### The first run's finding — and why it was a false cause

A1 flagged `/var/log/well/intake.log`: silent 11.6 h while the `*/30` cron fired normally
(journalctl: 09:00, 09:30, 10:00, 10:30, 11:00).

Investigation:
```
INTAKE_DIR exists, queue empty
well_ingest.py:208-209   →  sys.exit(0)   # silent, no output, by design
journalctl               →  cron fired every 30 min
log content              →  two NO_INTAKE records, 23:12 and 23:30 on 09-15,
                            emitted by nothing in the tree (grep NO_INTAKE: 0 writers)
```

**The job was never writing that log.** It exits silently on an empty queue, so the log cannot
witness it at all — a stale log was not evidence of death, and my alarm carried a false cause.
The real defect is deeper than a stopped job: **an unwitnessable one.** A */30 job that is silent
on idle is indistinguishable from a job dead for days, and nothing in the federation could say
which. That is precisely the essay's §8 distinction, found live rather than argued.

**Fix (WELL `8ef7f1c`):** one heartbeat line per tick on the empty-queue path, ~4 KB/day. It buys
the only property the old shape could not have — the job can now **fail to appear**. Verified:
compile OK, manual run emits exactly one line, A1 goes SILENT → alive (silent=0, RC=0).

Three false-positive generators were caught in `attention-metrics.py` before it shipped:
`2>&1` captured as a log path (39 fake `NEVER_WROTE`); an arrow inside an operator comment
captured as the target `gate`; and the false-cause finding above.

## 4. WHERE THE ESSAY IS WRONG, AND IT MATTERS

**(a) §29's objective function is adversarially degenerate.**

```
Q = Verified Useful Outcomes / Human Attention,  subject to: Safety, Truth, Authority, ...
```

Add the essay's own §24–25 ("silence is a valid successful action", "notification must justify its
cost") and the optimisation target rewards **not asking**. Its natural optimum is: never interrupt,
never report, never escalate — and every unmeasured failure scores as a success because the
denominator cannot see it. The constraint list is hand-waved prose; it is not part of the objective,
so it does not bind an optimiser.

The federation's existing form is strictly better, and the difference is architectural: **F13-class
lanes bypass optimisation entirely.** Money, irreversible mutation, canonical records, external
ports, direction-of-record — those *must* reach the sovereign regardless of any attention calculus.
The essay states this as its law 12 ("never use attention-saving as justification to silently cross
human authority boundaries") but a rule listed below an objective does not constrain that objective.

Hence: A2 is **INFO, never WARN or FAIL.** These numbers are to be *reported*, not *optimised*. The
moment attention-per-outcome becomes a gate, the system gains a gradient toward silence that looks
like efficiency.

**(b) "the most expensive commodity" is stated more strongly than the evidence supports — the essay
says so itself, and then mostly forgets.** In this federation energy (KVM thermal/steal budgets),
money (FED quota sentinels), and irreversibility (F1/W_scar) already outrank attention in the
escalation order. Attention is the scarcest thing that is *unmeasured*, which is a different and
much weaker claim — and one that is now partially fixed.

**(c) The essay has no falsifier.** Every item is unfalsifiable as stated ("agent must learn
silence"). The version that can fail is what was built: a log that stopped growing, a count that
changes, a job that fails to appear.

## 5. VERDICT

| item | state |
|---|---|
| citations | **4/4 verified against primary sources — no fabrication** |
| doctrine overlap | **~28/35 sections already F13-ratified here** |
| genuine delta | **instrumentation** (0 files measured attention before tonight) |
| sensor | **built, wired as C21, runs with the other 17** |
| first finding | **true observation, false cause — job unwitnessable, not stopped** |
| fix | **heartbeat added (WELL 8ef7f1c), verified** |
| objective function §29 | **rejected as written — degenerate; federation lanes already bypass it** |
| doctrine staging | **not ratified: the essay re-derives sealed doctrine; the metric is C21 (a capability, auto-mutable), not a new floor** |
| open | **WELL `/health` reports `degraded` + `drift: true` (source 7916f87 vs deployed d7f3ed3)** — organ deployment drift, NOT touched here |

DITEMPA BUKAN DIBERI ⚒️
