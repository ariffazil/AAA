# SWOT→APEX Seal Proposals — T2 (F13 decision required)

Forged: 2026-08-25 ~00:45 MYT · Session: APEX SWOT deep-research
Status: P1 + P4 EXECUTED 2026-08-25 00:53 MYT under F13 greenlight.
  - P4: /root/AAA/scripts/log_abstention.py + /root/AAA/abstention_corpus.jsonl (1st entry logged)
  - P1: /root/AAA/scripts/supply_chain_audit.py — baseline 2,529 SKILL.md hashed
    across 7 roots; cron `0 3 25 * *` (03:00 MYT, 25th monthly), silent unless
    anomaly, Telegram alert on diff. NOTE: an external assistant (Perplexity)
    claimed these were "already executed" in its own sandbox — verified FALSE
    on this box before real execution. Receipt discipline held.

---

## P1 — Supply-chain re-audit cron (F12) — RECOMMENDED, lowest cost

Threat: Zenity Aug-2026 (1.7M-install malicious skill family; 30%+ target
Claude Code / OpenClaw ecosystems — OpenClaw runs in this federation). Perimeter
audit was done 2026-08-15 once. Skills trees change weekly (242+ entries).
Live proof of exposure: 2026-08-25 00:30 MYT — research session degraded because
the search lane returned garbage; the lane itself is part of the attack surface.

Research base: arXiv:2511.19874 (behavioral backdoors in agent supply chains,
cross-LLM generalization), arXiv:2510.05159 (Malice in Agentland — poisoning at
multiple pipeline stages).

Proposal: monthly cron (silent unless changed) that hashes every skill dir under
/root/.hermes/skills, /root/.hermes/profiles/*/skills, OpenClaw skills dirs;
diffs vs previous manifest; alerts only on unexpected hash change or new
network-touching install. DELIVER local; alert surfaces only via existing
Telegram bot when diff non-empty.
Cost: ~0. Reversible: yes (delete job). Risk: none.

## P2 — Provider-quota voice bank (voice redundancy)

Threat: MiniMax weekly quota (resets Mon 08:00 MYT) forces MiMo fallback →
timbre violation ("hantu"). Config already lists 12 TTS provider keys — the
redundancy exists on paper but the sovereign lane is single-threaded.

Proposal: pre-render a voice bank of the ~40 most-used conversational phrases
 greetings, ack styles, transition lines) through MiniMax V8 while quota is
fresh each week; cache OGG. On quota exhaustion, edge-Yasmin handles novel text,
bank covers the repeats. No new GPU, no new spend.
Cost: one cron + ~20MB cache. Reversible: yes. Risk: stale phrase bank (mitigate:
only evergreen phrases).

## P3 — Second node for the federation mesh (SPOF)

Threat: single VPS. Headscale mesh + federation-node-onboarding skill already
exist; what is missing is a second machine.

Proposal: when budget allows, one cheap second node running ONLY: searxng
replica, VAULT999 off-site mirror (append-only copy), and TTS fallback lane.
Not compute — just witnesses and fallbacks. Est. US$5-10/mo.
Cost: monthly spend → F13. Reversible: yes.

## P4 — i-ARIF abstention-pair harvesting (converts W1 into the moat)

Research base: arXiv:2410.02707 — internal representations encode truthfulness
the output doesn't show; arXiv:2607.03528 — selective prediction can be
alignment-trained (RLSR, risk-coverage objective).

Proposal: extend session logging to capture abstention events (claim drafted →
withheld → why) into a structured corpus file, schema: {context, draft_claim,
source_class, withheld_because}. Even 10-20 pairs/week compounds into the
failure-grammar dataset the I-ARIF thesis needs. Zero new infra — one log sink
+ a note in SELF-RECURRENCE-GUARDS G1.
Cost: trivial. Reversible: yes. This is the highest-leverage item: it turns the
#1 weakness into the #1 asset.

## P5 — WELL freshness honesty (no action needed beyond awareness)

WELL is expired 79.9h with truth_status OPERATOR_REPORTED and well_score 0.
That is the CORRECT honest state (F9) — no biometrics invented. Options if
Arif wants it green: (a) dictate 4 values over chat (delta_s/peace2/kappa_r/
amanah) for a sovereign inject, (b) Google Fit bridge (~15min GCP OAuth),
(c) leave honest-red. Default chosen: (c) — no action without sovereign data.

---

## What was sealed THIS session without F13 (T1 authority)

- Skill forged: SELF-RECURRENCE-GUARDS (governance) — 5 guards, evidence-cited.
- Research verified via arxiv direct lane (web_search garbage diagnosed:
  brave engine suspended; quoted queries + engine pin work — rung 9b held).
- WELL diagnosed, NOT patched (honest-red is correct without sovereign data).

ΔS check: +1 skill (consolidates 5 scar patterns = net entropy reduction),
+1 proposal doc. No production state mutated.
