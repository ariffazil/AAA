# FED OSS Distillation — 2026-10-03

> **Author:** 333-AGI (FI-001) under F13 directive "map FED reality + make sure all warga have the correct FED model + deep research external OSS to distill".
> **Session:** SEAL-1233ff7266744510
> **Status:** DRAFT_RECEIPT (2026-10-03) — operational distillation receipt; not doctrine, no F13 instrument claimed. Applied live: config/SOT alignment + i-arif restore + retry patch (restart receipt §3, 11:01 MYT).
> **Precedent:** FED-EUREKA-DISTILLATION-2026-09-07.md · TOMBSTONE law: routing SOT = /root/.config/federation-models.json (never fed_signatures.yaml)

## 1. FED reality map (live-probed 2026-10-03 10:27-10:45 MYT)

**Is FED federated under AAA? YES — as an ADVISORY plane, correctly bounded.**

| Layer | Where | State (OBS) |
|---|---|---|
| Governance registration | `/root/AAA/federation/organs.yaml` → `id: fed, class: ADVISORY, authority_ceiling: ADVISORY_ONLY` | ✓ registered; "answers WHERE to call; does not call; not an organ" |
| Route advisor | `fed-router.service` :7074 → `/root/AAA/scripts/fed_router.py` (AAA-owned script) | ✓ healthy (KVM8) + node-local twin healthy (KVM2 127.0.0.1:7074) |
| Static routing SOT | `/root/.config/federation-models.json` (agents, capability_signatures ×16, fallback_chains) | ✓ single writer per tombstone law (fed_signatures.yaml ABSENT, do not resurrect) |
| Inference gateway | HAProxy :4000 (KVM8 intake, B3 auth-hardened 2026-10-02 F13 SAH) → litellm-federation container :4013 (Up 13h healthy) | ✓ 200 liveliness loopback+tailnet; :4012 zen passthrough |
| Cascade execution | `/root/A-FORGE/litellm-config.yaml` — 113 entries, 39 groups, `routing_strategy: latency-based-routing`, `order:` filtering CONFIRMED LIVE in litellm router.py:12784 | ✓ order-aware + latency-tiebreak + cooldown(30s)/allowed_fails(2) + context_window_fallbacks + enable_pre_call_checks |
| Telemetry | `token_bank.db` (fed_report_latency, balances, spend) via :7074 | ✓ 27 providers probed 2026-10-03T02:17Z |

**KVM topology (MACHINE_MAP.md sovereign naming decree, live-verified):**
- **KVM8** (forge, 100.64.0.2) = TRUTH: kernel :8088, all organs, HAProxy :4000, litellm PRIMARY :4013, fed-router :7074, HERMES @ASI_arifos_bot, all 12 FI seats.
- **KVM4** (srv1946043, 100.64.0.5) = EXECUTION: litellm docker :4000 (Up 4d healthy, passive `backup` in haproxy), OpenClaw edge :18789, agy/kimi/grok/aider + ccc pool.
- **KVM2** (flow-edge, 100.64.0.4) = WITNESS: local fed-router :7074 healthy (ADVISORY_ONLY), Wawa bot (hermes-agent Up), caddy, ollama :11434, SAF identity. No primary warga — federation consumer only.

## 2. Warga alignment — EXECUTED (was the real defect)

**Defect found (OBS):** `opencode.json` trinity agents carried NO `model` field — model names lived only in decorative descriptions. All 6 agents silently inherited top-level `litellm-federation/forge-777`, meaning **888-APEX (constitutional judge) rode the forge chain** = separation-of-powers violation at config level. Three surfaces contradicted each other (opencode.json descriptions vs rules doc 2026-09-10 vs SOT).

**Resolution law applied:** SOT (federation-models.json) wins per tombstone; rules doc demoted to projection; opencode.json now ENFORCES:

| Warga | Enforced binding | Chain head (live) | Verification |
|---|---|---|---|
| 333-AGI | litellm-federation/forge-777 | mimo-v2.6-pro-payg → glm-5.3-flash | PONG 942ms (served via MiniMax-M3 failover — clean) |
| 555-ASI | litellm-federation/asi-555 | glm-5.3-flash | PONG 1392ms finish=stop |
| 555-ASI-VISION | litellm-federation/asi-555 | (attachment-capable) | chain verified; vision passthrough UNTESTED (label: DER) |
| 888-APEX | litellm-federation/apex-888 | **MiniMax-M3 = empirical P1** | PONG 1883ms finish=stop |
| image-analyzer | litellm-federation/asi-555 | — | chain verified |
| dispatch | kimi/kimi-for-coding-highspeed | (SOT; kimi-moonshot probe LIVE) | provider key verified present |

Backups: `opencode.json.bak-fedalign-20261003T023940Z`, `federation-models.json.bak-fedalign-*`. Rules doc (`arifos-governance.md`) table re-titled "projection of federation-models.json", ghost `fed_signatures.yaml` reference removed. SOT entries annotated `alignment_note_2026_10_03`.

**Empirical bench state (SOT `empirical_bench_findings_2026_10_03`, corrected):** MiniMax-M3 P1 confirmed (G_m 0.88, 100% reliability) · GLM-5.3 SOUND, REASONING_HEAVY, deep-async lane (G_m 0.72; "86% corruption" claim VOID — max_tokens starvation) · qwen3.8-max intermittent only at 30s client timeout (fine ≥60s). **No cascade integer mutation was needed or executed** — the demotion rationale evaporated with the correction; HERMES's HOLD on the swap was correct and is now moot.

## 3. External OSS scan → distilled

**Method:** context7 (litellm docs, live-version cross-check inside container) + web scan (2026 router landscape). Epistemic labels inline.

| Source | Finding | Disposition |
|---|---|---|
| LiteLLM (OSS, berriai) | 2026 consensus #1 self-hosted gateway (DigitalOcean/Reddit surveys); FED already rides it. Native: `order` filtering, latency-based-routing, retry_policy, tag routing (`tag_routing_prefix: "route:"`), `reasoning_effort`/`thinking` passthrough, `usage.completion_tokens_details.reasoning_tokens` | **VALIDATED — stay. Distill features below.** |
| RouteLLM (LMSYS, OSS) | Learned strong/weak classifier from preference data; OpenAI-compatible | **Phase-2 candidate, NOT built.** FED already collects the training fuel (route_latency telemetry + bench corpus). Kill criterion: build only if manual cascade tuning produces ≥2 more paper-tiger-class incidents/quarter. (Canon #0: no architecture without demonstrated failure class.) |
| Portkey gateway (OSS core) | Semantic caching cuts redundant-call cost | **Idea banked.** litellm has native response caching (redis) — FED runs redis :6379. Cheap pilot possible without new software. |
| OpenRouter routers (Auto/Fusion/Pareto) | Task-aware routing, deliberation panel, coding shortlist | Already flagged in AGENT_MODEL_MAP 2026-08-13. Fusion ≡ existing musyawarah/forge_parallel pattern; Pareto ≡ fed-coding signature. **No action — concepts already owned.** |
| Awesome-Routing-LLMs (curated list) | Research index for routing-LLM paradigm | Bookmarked as the standing literature feed for Phase-2. |

**APPLIED now (additive, no restart):** `_meta.reasoning_model_registry_2026_10_03` in federation-models.json — machine-readable headroom law sealing the bench failure class: `min_max_tokens` per reasoning model, `reasoning_content` parse contract, and the rule *content=='' ∧ finish_reason=='length' ∧ registry-model ⇒ TOKEN STARVATION, not corruption — raise tokens before any demotion claim.*

**APPLIED LIVE (restart window 2026-10-03 11:01 MYT, 25s, controlled T2):**

```yaml
# /root/A-FORGE/litellm-config.yaml → router_settings (commit 4b8ab1cc — NOW LIVE)
router_settings:
  num_retries: 3            # was 1 — contradicted declared fallback discipline ("retry 3x backoff")
  retry_policy:
    TimeoutErrorRetries: 3
    RateLimitErrorRetries: 3
    AuthenticationErrorRetries: 1   # don't hammer dead keys
    NotFoundErrorRetries: 0         # never retry a 404
    ContentPolicyViolationErrorRetries: 2
    InternalServerErrorRetries: 3
    DefaultRetries: 2
  # optional Phase-1.5: enable_tag_filtering: true + tag_routing_prefix: "route:"
  #   → per-warga deployment steering without touching cascade integers
```

**P1 REPAIR — i-arif sovereign lane (found during this audit, restored live):**
`model=i-arif` returned "Invalid model name" on KVM8 primary (OBS 10:52 MYT) — 8 deployments accidentally dropped by bulk checkpoint `bc98843d` (2026-09-30), leaving organs.yaml + router fallbacks dangling. Restored verbatim from `bc98843d^` (A-FORGE `6a05314f`), canonical `deepseek-v4-pro` group added to repair forge-builder/forge-economy dangling fallback targets (`b4670f33`). All 10 env keys present. Post-restart regression: **i-arif PONG 3036ms finish=stop; /v1/models 2/2; apex-888 1485ms · asi-555 4567ms · forge-777 3128ms · hermes-asi 1665ms — all finish=stop; 0 config errors.** No live breakage had occurred (HERMES rides hermes-asi + direct names + i-arif-sovereign AUDIO provider — OBS /root/.hermes/config.yaml). Benign residual: `gemini-2.5-flash` fallback source is KVM4-only lane (never fires on KVM8; kept for config lineage).

## 4. Open items (declared, not hidden)

1. ~~Vision passthrough on asi-555~~ **CLOSED (OBS 10:47 MYT):** 1×1 red PNG through asi-555 → "Maroon", finish=stop. 555-ASI-VISION + image-analyzer bindings fully verified.
2. **forge-777 order-1 (mimo-v2.6-pro-payg)** consistently served via MiniMax-M3 failover (2 probes) — normal cooldown or standing mimo failure? UNBENCHED; one probe run will tell (no mimo-v2.6 samples in route_latency).
3. **KVM4 litellm = divergent FORK, not stale copy (MEASURED):** 10 KVM4-only groups (gemini-*/mistral/codestral/fed-audio-asr/tts/i-arif-era lanes) vs 14 KVM8-only (forge-* subagents, mimo-v2.6 family, hermes-default, deepseek-flash, MiniMax-M3.1). **Blind sync in either direction breaks a node's locals.** Union review with per-node env validation = scoped next-window task; backup node only matters if primary dies (primary healthy).
4. ~~Staged retry patch~~ **APPLIED LIVE (commit 4b8ab1cc, restart receipt above).**
5. **Firecrawl credits low** (vendor notice during research) — top-up is F13 money-class; flagged, not acted.

## 5. Kill criterion for this artifact

If federation-models.json ceases to be the routing SOT, or litellm is replaced as gateway, §2-3 tables are historical — supersede, do not maintain in parallel (one writer, many views).

*DITEMPA BUKAN DIBERI ⚒️*
