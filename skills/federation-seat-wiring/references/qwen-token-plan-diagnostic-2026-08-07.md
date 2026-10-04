# Qwen Token-Plan Diagnostic Reference (2026-08-07)

Live evidence from the Qwen pool exhaustion event of 2026-08-07, captured while diagnosing the federation-wide cascade failure.

## Pool architecture

The federation runs against Aliyun's "Token Plan" service (international, ap-southeast-1 region). It exposes two distinct quota meters:

| Meter | Keys | Endpoint | Reset window | Account model |
|---|---|---|---|---|
| **Team pool** | QWEN_API_KEY, QWEN_BAILIAN_KEY, QWEN_OPENCODE_API_KEY, QWEN_HERMES_API_KEY, QWEN_TEAM_OWNER_API_KEY | token-plan.ap-southeast-1.maas.aliyuncs.com | Weekly (rolling) | Single org-wide quota — one seat exhausts → all 5 fail |
| **Individual pool** | QWEN_INDIVIDUAL_API_KEY | token-plan.ap-southeast-1.maas.aliyuncs.com | Weekly (rolling) | Separate meter, Arif's personal |
| **PAYG** | DASHSCOPE_API_KEY (=BAILIAN_PAYG_API_KEY) | dashscope-intl.aliyuncs.com | Pay-as-you-go | Requires payment info on file in console |

Team and individual share the same endpoint URL but have **separate quota meters**. The portal at <https://home.qwencloud.com> shows both.

## Quota-error shapes (verbatim from probes)

```json
// Team pool exhaustion
{"error":{"message":"Your token-plan quota has been exhausted.",
          "type":"insufficient_quota","code":"insufficient_quota"}}

// Individual pool exhaustion — reset timestamp IS in body
{"error":{"message":"Your token-plan 1-week quota has been exhausted. The quota will reset at 08-07 07:38:00 UTC.",
          "type":"insufficient_quota","code":"insufficient_quota"}}

// PAYG in free-tier-only mode (no payment info)
{"error":{"message":"The free quota has been exhausted. To continue accessing the model on a paid basis, please complete your payment information （or disable the \"use free tier only\" mode in the management console if already completed).",
          "type":"AllocationQuota.FreeTierOnly","code":"AllocationQuota.FreeTierOnly"}}
```

## Per-key model rosters (probed 2026-08-07)

| Key | # models | Sample IDs |
|---|---|---|
| QWEN_API_KEY (team) | 22 | qwen3.6-plus, qwen3.6-flash, qwen3.7-max, qwen3.7-plus, qwen3.8-max, qwen-image-2.0, qwen-image-2.0-pro, wan2.7-image, wan2.7-image-pro, deepseek-v3.2, deepseek-v4-flash, deepseek-v4-flash-0731, deepseek-v4-pro, glm-5, glm-5.1, glm-5.2, kimi-k2.5, kimi-k2.6, kimi-k2.7-code, qwen-audio-3.0-tts-plus, qwen-audio-3.0-realtime-plus, MiniMax-M2.5 |
| QWEN_INDIVIDUAL_API_KEY | 11 | qwen3.7-max, qwen3.7-plus, qwen3.6-flash, glm-5.2, deepseek-v4-pro, wan2.7-image, wan2.7-image-pro, qwen-audio-3.0-tts-plus, deepseek-v4-flash-0731, qwen3.8-max, qwen-audio-3.0-realtime-plus |

**Models on team roster but NOT individual:** qwen3.6-plus, qwen-image-2.0, qwen-image-2.0-pro, deepseek-v3.2, glm-5, glm-5.1, kimi-k2.5, kimi-k2.6, kimi-k2.7-code, MiniMax-M2.5.
**Plus any with `qwen3.7-flash` or `qwen3-coder-plus` — these were used in the cascade prior to the swap and DO NOT EXIST on the individual roster.** Always probe `/v1/models` before swapping Qwen tiers.

## What doesn't work (and why)

- **Numeric balance REST endpoint** — gated behind Alibaba console session cookie. API keys can't pull remaining-token numbers. Use the console.
- **Real-time USD-equivalent metering** — quota is a weekly token bucket, not a USD ledger. Even if the team pool has $25 left, it's still rate-limited by the bucket.
- **Cross-pool transfer** — individual pool can't rescue team pool. They're separate accounts under the same org.

## Cascade fall-through verification

After re-wiring all 7 Qwen cascade entries from DASHSCOPE_API_KEY to QWEN_INDIVIDUAL_API_KEY, the federation cascade now looks like (per `litellm-config.yaml` model_list):

```
hermes-asi:
  order 1: MiMo V2.5 (mimo-v2.5 token-plan)
  order 1: DeepSeek V4 Flash (deepseek direct)
  order 2: MiniMax M3 (minimax direct)
  order 3: Qwen 3.8-max (QWEN_INDIVIDUAL_API_KEY, token-plan)
  order 4: Qwen 3.6-flash (QWEN_INDIVIDUAL_API_KEY, token-plan)

agi-333 / asi-555 / opencode / openclaw / dispatch:
  similar cascade shape with Qwen tiers always at the tail (order 3-4)
```

LiteLLM's `usage-based-routing` strategy + `cooldown_time: 300` means a single failed tier cools for 5 minutes before being retried. The cascade effectively degrades gracefully: real upstream failures roll through MiMo → DeepSeek → MiniMax → Individual Qwen tiers without the agent seeing 5xx.

## Recovery options

1. **Wait for weekly reset** — individual key resets `08-07 07:38:00 UTC` (= 15:38 MYT). After reset, all 6 team keys come back online simultaneously.
2. **Disable "use free tier only" in DashScope console** — unblocks PAYG `DASHSCOPE_API_KEY` for token purchases (separate billing).
3. **Buy Token Plan credit packs** — $15/20K tokens × 5 packs mentioned in notes; top-ups extend the bucket immediately.
4. **Pre-rotate to a different provider** — MuleRouter, OpenRouter, or tokenrouter have separate meters and bypass Qwen entirely.

## Tooling artifacts

- `/root/.local/share/arifos/fed_provider_state.json` — fed-sync output (refreshed every 15 min). Shows `quantum_state: ALIVE|DEGRADED|DEAD` per provider.
- `/root/scripts/fed-sync.sh` — auto-sync timer. Don't trust its `enabled_providers` reordering blindly; verify agent bindings after it runs.
- `/root/.secrets/kunci-mas.env` — golden vault, all 6 Qwen keys live here. Source of truth.
- `/root/.secrets/kunci-mas.flat.env` — systemd-loaded copy, regenerated by `make -f /root/.secrets/Makefile vault-generate`.
