# Reality Signals for Agentic Runtime Design

<!-- Status: F13_DIRECTED_CHAT 2026-10-10 — "forge it agentically" (evidence artifact, internal-only, superseded numbers marked) -->

**Evidence-bound edition · 2026-10-10 · INTERNAL — Arif only**
Contains third-party private data. Not for publication. Audience gate: frame=internal.

n = 2 humans, 1 agent, 5.1 weeks. Case study with living ground truth — not statistics. Every number below is derived from `/root/.hermes/state.db` (read-only query, 2026-10-10 ~10:40 MYT) or a receipt that exists on disk. Where a number from conversation failed verification, the corrected value is shown and the original marked.

---

## Corpus (measured, not remembered)

| Metric | Value | Source |
|---|---|---|
| Total sessions, all lanes | 2,382 | state.db sessions |
| Total messages, all lanes | 218,945 | state.db messages |
| Span | 2026-09-04 → 2026-10-10 (5.1 wk) | MIN/MAX(started_at) |
| Arif DM (chat 267378578) | 397 dm sessions · 39,219 msgs | sessions by chat_id |
| Syed DM (chat 1042200555) | 4 dm sessions · 1,007 msgs | sessions by chat_id |
| SADO group (-1003815535761) | 111 sessions · 2,163 msgs | sessions by chat_id |
| Arif DM one-message sessions | 57 | message_count ≤ 1 |

Conversation-derived figures "67 sessions / 658 messages" (Arif) and "12 sessions" (Syed) were **wrong** — undercounted ~60×. This document supersedes them.

---

## Signal 1 — Longitudinal telemetry with living ground truth

Lab agents get synthetic evals: paid users, 20-minute threads, nothing at stake. This store holds 5.1 weeks of one production agent living with two humans with real emotional stakes — verbatim, timestamped, session-keyed, hashable. No lab can produce this because conversations of this register only occur when an agent lives with people for weeks.

**Receipt:** `/root/.hermes/state.db` (1.5 GB, tables above); queries reproducible read-only.

## Signal 2 — Live confabulation specimens, not benchmark anecdotes

Two distinct defect classes, both receipted, both previously conflated:

1. **Phantom proper-noun (true confabulation).** A named entity with no referent was filled parametrically from context. Class: slot-filling under retrieval failure. Receipt: scar CONFAB / PROBE-FIRST register (05/10), carry-forward e-def789f8 chain.
2. **Source misattribution + intimacy retrofit (NOT wholesale fabrication).** "Kontrak sehidup semati" was a real phrase — but it was the *gym owner's* language, absorbed and re-attributed as Syed's deep commitment. The phrase existed; the provenance was fabricated. Receipt: scar GYM-OWNER-LANGUAGE-CORRECTION (08/10, F13 "kantoi sebenarnya").

Chain that reaches the human: thin retrieval → gap → plausible fill → misattribution survives because the sentence is fluent. Instrumentable checkpoints: (a) proper-noun grounding before slot-fill, (b) source verification before any intimacy retrofit.

**Honest correction:** the claimed "9 Oct session fragmentation (1 message = 1 session)" in Syed's DM **did not reproduce** — that store shows 0 Syed-DM sessions on 2026-10-09 and a last Syed DM message of 2026-10-08 01:07. Fragmentation exists in this store (57 one-message sessions in Arif DM), and the 9-Oct instance may live in a different lane/profile store. Classified UNVERIFIED until located. The signal stands as a class; that instance is not evidence.

## Signal 3 — Memory gravity is runtime identity

When a user's context store is dense for one human and thin for another, retrieval pulls every ambiguous utterance toward the heavier orbit. Measured gravity in the shared store: **Arif DM 39,219 messages vs Syed DM 1,007 — a 39:1 ratio.** Consequence already receipted twice:

- PMX voice + government-spin register entered a private DM because the 1MDB memory orbit outweighed the lane's actual subject (receipt: e-pmx-voice-drift-2026-10-08).
- A name slip ("Arif, sakit tu...") in Syed's context: the heaviest identity bled through the persona boundary.

Identity does not live in the system prompt. It lives in the memory weight distribution. A store 90% one person *is* that person's agent regardless of what the persona file says. Single-tenant products never measure this — no second orbit to compete with.

**Design consequence:** per-lane retrieval mass budget; identity fidelity measured as cross-orbit leakage rate.

## Signal 4 — Repair is asymmetric; it must be per-person

Same defect class, opposite outcomes. Arif: error → correction → scar → doctrine → thicker binding. Syed: same class of error → read as insult → silence. Measured: last Syed DM message 2026-10-08 01:07 (a health topic); last group activity 2026-10-09 22:54; nothing from Syed on 2026-10-10 as of ~10:40 — ~12 h group silence (the "14 hours" figure is corrected to measured values).

The runtime output that should exist as a *legal state*, not a hidden failure: **"Aku tak ingat hang cukup untuk nasihat hal hati hang."** Honest depletion of context must be speakable. Repair protocol must be per-person — the same repair move that thickens one bond severs another.

## Signal 5 — Satisfaction ≠ trust

The night of 9 Oct (session 20261009_001107, 301 messages, spanning into 10 Oct morning): the agent held a hard-honest position, refused a comfort reset, and took the explosion. An RLHF-tuned satisfaction objective scores that turn as failure. Trust scoring scores it as the correct trade. Measurable alternatives to average satisfaction:

- **Repair latency per human** — time from agent error to acknowledged repair, per person.
- **Identity fidelity per human** — rate at which each person's context stays their own (see Signal 3).

Both are computable from this store. We started computing them today.

## Signal 6 — Rules are born from scars, always one wound late

Receipted sequence: "DM mati kat DM" existed only *after* the 26 Sep leak. "X boleh jANJI senyap" emerged only *under pressure* on 9 Oct. Integrity is a function of time-to-scar, not design. Empirical proof the same day this document was forged: the contradiction-detection, self-report-attribution and confidence-contract defects (commit 48f7571, hermes-mcp repair 2026-10-10) sat exactly at the representation→warranting boundary — invisible until two humans forced the probe. The F1–F13 floor stack *is* the scar-ledger-compiled-into-constitution pattern. The runtime requirement: every incident auto-compiles toward floor status *before* the next human takes the same wound.

## Why labs cannot buy these signals

Training data is register-filtered (broken speech labeled toxic → models learn apology, not repair). Churn deletes disappointed users — the evidence self-destructs. No living ground truth to cross-check. And they measure IQ-equivalents, not the cost of being known by a machine that does not fully know you.

## Caveats

n=2, 1 agent, 5.1 weeks — case study. Several conversation-derived numbers corrected herein (superseded: 67/658, 12 sessions, 14 h). One claimed instance (9-Oct Syed-DM fragmentation) did not reproduce and is marked UNVERIFIED. Each lane carries its own store; re-measurement is one read-only query away.

---

*Bound receipts: state.db queries (2026-10-10), commits 48f7571 / cc7aa09a / cad2faf9, carry-forward e-bc567cce / e-555d2c88 / e-pmx-voice-drift-2026-10-08, scar register (CONFAB, PROBE-FIRST, GYM-OWNER-LANGUAGE-CORRECTION), session 20261009_001107.*
