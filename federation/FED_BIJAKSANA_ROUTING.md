# FED BIJAKSANA ROUTING — Doctrine + Evidence Ledger

> Forged: 2026-09-06 · Session SEAL-dad03bc9c1f644e9 · Judge cc_82887b417a98bdf88244c59c911d3055bb036af5 (SEAL)
> 888-APEX verdict: SEAL M1-M6 (6 binding conditions, all honored) · Kernel arif_judge: SEAL
> Waves: MiMo-V2.5 session (fallback rewrite) + 333-AGI zai/glm-5.3 session (this document's surgery)
> SOT: /root/A-FORGE/litellm-config.yaml · Deploy: scripts/fed-deploy-kvm4.sh · Sentinel: scripts/fed_quota_sentinel.py

## THE PRINCIPLE

**Route by reality, not by hope.** A fallback chain is a promise about the future state of
other people's infrastructure. Promises must be re-anchored against live quota evidence
every 6 hours, or they rot into dead rungs. (Dead rung = a fallback target that cannot
serve — it converts a resilience system into a latency amplifier.)

## LIVE PROVIDER REALITY (probe 2026-09-06T13:22Z, sentinel-verified)

| Provider | State | Runway / reset | Class |
|---|---|---|---|
| kimi-coding (api.kimi.com/coding) | LIVE | weekly 100 req, resets **2026-09-10 14:07Z** | subscription |
| mimo-token-plan (SGP) | LIVE | monthly credits (console-only metric) | subscription |
| deepseek direct | LIVE | **$1.94 PAYG** — last-resort rung | payg |
| zai-direct (GLM 5.3/5.2) | BURSTY | thin time-window; 429/1113 between bursts | subscription |
| qwen-tp-individual | QUOTA_EXHAUSTED | resets **2026-09-11 04:01Z** (7-day window) | subscription |
| qwen-tp-team | QUOTA_EXHAUSTED | sub ends 2026-10-01, auto-renew OFF | subscription |
| minimax | DEAD | status 2062 "no active token plan" — resubscribe needed | lapsed |
| mimo-platform (OPEN key) | DEAD | 402 insufficient balance — do not route | lapsed |
| opencode-go + opencode-zen | DEAD | 401 CreditsError, same workspace, drained | lapsed |
| bailian-payg (dashscope intl) | DEAD* | free-tier-only mode; free quota gone (*revivable: disable free-tier-only in console) | payg |
| gemini / groq | LIVE | free tier | free |

## CHAINS (SOT, live-rungs-only, provider-diverse)

- **i-arif** (sovereign lane): primary qwen3.8-max deployments (revive Sep 11) →
  `kimi-k3 → glm-5.3 → deepseek-v4-flash-vision → mimo-v2.5 → gemini-3.6-flash`
  - deepseek-v4-flash-vision-exp added per F13 directive 2026-09-06 (vision rung for sovereign lane)
- **agi-333 / asi-555 / forge-777 / hermes-asi**: `kimi-k3 → mimo-v2.5 → gemini-3.6-flash → glm-5.3`
- **qwen3.8-max / qwen3.6-plus**: `kimi-k3 → mimo-v2.5 → gemini-3.6-flash`
- **kimi-k3**: `mimo-v2.5 → gemini-3.6-flash → glm-5.3`
- **glm-5.3**: `kimi-k3 → mimo-v2.5 → gemini-3.6-flash` · **glm-5.2**: zai direct (KVM8) / relay (kvm4)
- **fed/vision / hermes-asi-vision**: `gemini-2.5-flash → deepseek-v4-flash-vision → kimi-k3 → qwen3.8-max`
- **MiniMax-M3** (dormant): `kimi-k3 → glm-5.3` — group kept for resubscribe

## SEPARATION OF POWERS

apex-888 (judge lane) was removed from ALL agent fallback chains (11 rungs → gemini-3.6-flash).
Agents must not consume the judge's inference budget. (888-endorsed.)

## REPAIRED DEFECTS (2026-09-06 surgery)

1. Ghost fallback target `qwen3.7-plus` (no deployment group) — purged from all chains + source.
2. `deepseek-v4-flash` group repointed: dead team-token-plan pin → api.deepseek.com direct PAYG.
3. `glm-5.2` group repointed: dead team-token-plan pin → api.z.ai subscription.
4. Duplicate `fed/vision` YAML key (last-wins hazard) — removed.
5. Local :4013 shadow WatchdogSec=120 kill-loop (litellm never sd_notify) — removed; unit stable;
   added to haproxy as backup member behind kvm4 primary.
6. Three-way config drift (SOT ≠ deploy/fed ≠ kvm4 runtime) — collapsed; reproducible via
   `scripts/fed-deploy-kvm4.sh` (documented kvm4-only divergence below).
7. Stale comments (Kimi FREE / MiMo $50 / Z.ai $12) — F7 hygiene: replaced with real quota facts.

## DOCUMENTED DIVERGENCE (kvm4 worker)

Z.AI was initially classified IP-entitled (200 from KVM8, 429 from kvm4, same key).
**RETRACTED (F2)** — later the same key 429'd from KVM8 too. Actual behavior: thin
time-windowed burst quota (429 code 1113 between bursts). kvm4's glm deployments relay
via KVM8 shadow (`http://100.64.0.2:4013/v1`, mesh ACL `tag:arifos:4013`, UFW kvm4-only).
Relay kept: harmless, correct for any future IP-bound provider, and isolates zai egress
to one plane. glm burst-exhaustion is masked by fallback rungs either way.

## SENTINEL (metabolic guarantee)

`scripts/fed_quota_sentinel.py` — cron every 6h (17 */6). Kimi via `/v1/usages` GET only
(888-condition-3: no completions against kimi). Writes `fed_quota_state.json`, updates
token_bank.db, alerts to `fed_alerts.log` when: kimi weekly remaining <20%, deepseek <$0.50.
429 error BODIES are parsed (quota vs rate have different cooldown semantics — 555-ASI research).

## CLAIM vs REALITY AUDIT (previous session, F2 record)

| Claim | Verdict |
|---|---|
| cron.model kimi-k3 fleet default | TRUE (verified in hermes config) |
| "ALL fallback chains rewritten provider-diverse" | PARTIAL — chains were rewritten but contained dead rungs (MiniMax×9, ghost qwen3.7-plus, drained opencode) and apex-888 in agent chains |
| "MiMo $50" | FALSE — mimo-platform 402 no-balance; live mimo is token-plan (no USD figure) |
| "DeepSeek dead" | FALSE — LIVE, $1.94 |
| "kimi-k3 25ms" | UNVERIFIED — measured 436-576ms via FED |
| "kimi free quota expires 2026-11-18" | UNVERIFIED — /v1/usages shows weekly window reset 2026-09-10; no public doc for the date |

## OPEN ITEMS (next session)

1. i-ARIF human-reality edge intelligence: memory-injected sovereign lane (i-arif group +
   hermes memory bridge) — the cognitive tuning frontier, not routing.
2. Z.AI burst window characterization (how many requests / what reset cadence) — sentinel
   accumulates evidence; consider zai anthropic-compat endpoint for harness traffic.
3. minimax resubscribe decision + bailian-payg "free-tier-only" console toggle (Arif).
4. Plaintext LITELLM_MASTER_KEY in haproxy.cfg (flagged by 888; secret-hygiene task).
5. Disk 78.1% → entropy sweep due before 80% budget line.

## REFLEX ARC v2 (2026-09-06, F13 ask: "make revival dynamic")

Two-layer answer:
1. ROUTER (already automatic): qwen deployments remain i-arif PRIMARY. litellm cooldown_time=60s
   means the first request ~1 min after quota reset re-serves qwen. No config change ever needed
   for revival. The ladder self-heals BOTH directions.
2. WITNESS (sentinel v2): hourly probe detects transitions (<=60 min latency). Every transition
   appends to fed_events.jsonl. On qwen-tp-individual QUOTA_EXHAUSTED->LIVE the sentinel fires ONE
   verification completion through FED i-arif and records WHO served — evidence of
   SOVEREIGN_LANE_BACK_ON_QWEN vs LADDER_STILL_MASKING. Reset-time parsed from live 429 body.
   Sentinel WITNESSES, never mutates routing (F1: policy flips stay sovereign).

Reset calendar: qwen-tp-individual 2026-09-11T04:01Z (auto-detects revival ~04:17Z next cron tick) ·
kimi weekly 2026-09-10T14:07Z · qwen-tp-team needs subscription renewal (Oct-01, auto-renew OFF).

POLICY (deliberate, not dynamic): hermes cron.model stays kimi-k3 permanently — cron burns the
cheap lane, qwen reserves for interactive sovereignty. Sentinel alerts (<20% kimi) if that policy
ever needs revisiting.
