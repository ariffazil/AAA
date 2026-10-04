---
name: provider-quota-diagnostics
description: "Diagnose API provider quota exhaustion — key validity vs key usability, shared-pool detection, rolling-window quota management, and portal-only billing visibility. Covers Qwen Token Plan (Individual Pro + Team), and the general pattern applicable to any provider that lacks a quota API. Trigger: 'is my API key working', 'check quota', 'insufficient_quota error', 'can we use Qwen', key returns 200 on /models but chat fails, or any provider quota/auth diagnosis."
tags: [quota, api-key, qwen, token-plan, provider, billing, diagnostics]
---

# Provider Quota Diagnostics

## Core lesson: validity ≠ usability

A key that returns HTTP 200 on `/v1/models` proves **authentication works** — the key is valid, not revoked, and hits the right endpoint. It does **NOT** prove the key has remaining quota for actual inference. **Always probe chat completions to test usability.**

```
/v1/models → 200     → key is VALID (authenticated)
chat/completions → 200  → key is USABLE (has quota)
chat/completions → 429  → key is VALID but EXHAUSTED
/v1/models → 401     → key is REVOKED or wrong endpoint
```

## Diagnosis recipe (any provider)

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a

# Step 1: Key validity
curl -s -o /dev/null -w "HTTP %{http_code}" "$PROVIDER_BASE_URL/models" \
  -H "Authorization: Bearer $PROVIDER_API_KEY"

# Step 2: Key usability (actual inference)
curl -s "$PROVIDER_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $PROVIDER_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"<fast-cheap-model>","messages":[{"role":"user","content":"hi"}],"max_tokens":1}'
```

## Error signature table

| HTTP | Error | Meaning | Action |
|---|---|---|---|
| 200 | (success) | Valid + has quota | ✅ Usable |
| 401 | Unauthorized | Key revoked, wrong endpoint, or expired | Check key prefix matches provider; verify endpoint URL |
| 402 | `Insufficient Balance ... Available Model Group Fallbacks=None` | PAYG credit dead on a FED/LiteLLM alias | Demote dead tier to order:99, promote alive tier, restart litellm-federation. 402 is a non-fallback credit error like 400 |
| 403 | `AllocationQuota.FreeTierOnly` | PAYG key on free-tier-only mode, no payment info on file | Add payment method in console OR disable "use free tier only" toggle |
| 404 | (model not found) | Model ID not in this key's roster | `GET /v1/models` to list allowed models per key |
| 429 | `insufficient_quota` | Token-plan quota exhausted | Wait for reset or manual reset on portal |
| 429 | `Your token-plan 1-week quota has been exhausted. The quota will reset at 08-07 07:38:00 UTC.` | Weekly window quota (Qwen Individual) | Compute reset time = error timestamp + rolling 7d, or use portal |
| 429 | `Allocated quota exceeded` | Rolling window exhausted (Qwen-specific) | Portal manual reset or wait |
| 429 | `Rate limit exceeded` | Transient rate limit (different from quota) | Wait seconds/minutes; retry |

**429 vs 429:** `insufficient_quota` / `Allocated quota exceeded` = credits gone (hours/days to recover). `Rate limit exceeded` = temporary throttle (seconds to recover). Same HTTP status, completely different root cause.

**403 vs 429:** `403 FreeTierOnly` is NOT quota exhaustion — it's a billing-mode lock. The key works, the API works, but the console is set to "free tier only" and you've used all free credits. Different fix (add payment), different urgency (zero urgency — key is healthy, billing config is the problem).

**404 vs 401 vs 429:** When swapping API keys in a cascade, always re-probe `GET /v1/models` first. Different keys under the same provider can have different model rosters — Qwen Individual exposes 11 models, Qwen Team/Pro exposes 22. A cascade tier pointing at a model the new key doesn't have will 404 at runtime, not at config-validation time. Treat `/v1/models` as the authoritative roster, not the cascade YAML.

## Qwen Token Plan specifics

See `references/qwen-token-plan-quota.md` for the full Qwen-specific pattern including:
- 3-key shared pool architecture
- Rolling 5h + 7d window mechanics
- Portal-only quota visibility (no API)
- Manual reset availability
- Error message variants per key type

See `references/qwen-all-keys-exhausted-2026-08-07.md` for a session transcript where every Qwen key was dead simultaneously and the full cascade-rewire fix (probe roster → swap endpoint+key → restart proxy → verify text before vision).

## Qwen PAYG free quota (Model Studio Singapore)

See `references/qwen-payg-free-quota-intl.md` for the complete free-quota knowledge bank including:
- Free-quota mechanics (per-model 1M tokens, 30–90 day validity, International scope only)
- The **endpoint distinction**: general PAYG keys work on `dashscope-intl.aliyuncs.com`, not China endpoint
- Token-Plan/Coding-Plan keys vs general PAYG keys — only PAYG keys consume free quota
- Common error codes (`FreeTierOnly`, 90-day expiry behavior)
- LiteLLM/FED 402 non-fallback pattern with gateway delivery pitfall

## Source of truth hierarchy

1. **Portal / billing dashboard** — actual remaining credits (if available)
2. **HTTP response on chat/completions** — whether the key can serve requests NOW
3. **Config files / .env** — what *should* work (may be stale)

Config files declare intent. HTTP responses declare reality. Portal declares financial state. **Never declare a key "usable" based on config alone.**

## Model picker: credential existence ≠ provider health (2026-08-09)

**Symptom:** User opens `/model` picker in Telegram, sees providers that don't
work when selected — "Why got two Alibaba?", rate-limited providers still showing,
dead keys appearing as selectable.

**Root cause:** `list_authenticated_providers()` in
`hermes_cli/model_switch.py` checks `any(os.environ.get(ev) for ev in env_vars)`
— this only verifies the env var **exists**, not that the key is valid, has
quota, or the endpoint is reachable. Same validity≠usability doctrine, one
layer up.

**Duplicate provider rows** happen when a ProviderConfig lists a shared env var
as fallback. Example: `alibaba-coding-plan` in `auth.py` lists
`DASHSCOPE_API_KEY` as fallback — when only that key is set, both `alibaba` and
`alibaba-coding-plan` show in the picker. Fix: either fold into
`PROVIDER_GROUPS` (display fix) or gate the fallback in the picker logic.

**Proposed health-probe filter:** After credential check, probe each provider's
`GET /v1/models` (2s timeout, parallel, 5 min cache). 200→show, 401/403→hide,
429→badge, timeout→hide. `probe_api_models()` in `models.py:3548` already
exists — just not called during picker construction. Patch point is
`list_authenticated_providers()` after `has_creds` check.

Full architecture map + component locations + fix options:
`references/model-picker-architecture.md`

## FED-first routing doctrine (Arif 2026-08-09)

**FED (:4000 HAProxy → :4011 LiteLLM) must be the PRIMARY model router for Hermes.** Direct providers (Qwen Individual, Fireworks, MiMo, Groq, etc.) are FALLBACK only — shown in `/model` picker as escape hatches, not primary entries. `config.yaml` already has `provider: fed` as default; the picker must not clutter the view with 10+ duplicate direct providers when FED is the intended path.

**Picker cleanup strategy:**
1. Keep `fed` as first/primary in model-picker.yaml
2. Keep one direct provider per endpoint as fallback (e.g., `qwen-token-plan-individual` for Alibaba endpoint, `mimo-token-plan` for Xiaomi, `fireworks` plugin for Fireworks)
3. Remove duplicate Qwen Token Plan seats (4 seats same endpoint = keep `qwen-token-plan-individual` only, remove `qwen-token-plan`, `qwen-token-plan-standard`, `qwen-token-plan-team-owner`)
4. Disable built-in plugin providers that duplicate config.yaml entries (`mv alibaba alibaba.disabled`, `mv minimax minimax.disabled`, `mv ollama-cloud ollama-cloud.disabled`, `mv qwen-oauth qwen-oauth.disabled`)
5. `mulerouter` and `sea-lion` can be removed (no unique value; `sea-lion` has no key)
6. Keep unique plugin providers that have no config.yaml equivalent: `deepseek`, `fireworks`, `nous`, `opencode-zen`, `huggingface`, `copilot`, `anthropic`

## Pitfalls

- **Never print or paste API keys in chat or VAULT999.** Show prefix only (e.g. `sk-sp-H.DIIYD`), never the full value.
- **Shared pools are invisible.** Multiple keys under the same plan/organization share one credit pool. Testing one key and declaring it "good" does not mean the others work — but in practice they exhaust together.
- **`/models` 200 is a necessary-but-not-sufficient test.** It proves auth, not quota. Always follow up with a chat completion probe.
- **Model picker shows dead providers.** The picker credential check only tests env var existence, not key validity or quota. A key set but expired/rate-limited/out-of-credit still appears as a selectable provider. See `references/model-picker-architecture.md` for the full component map and health-probe filter design.
- **Quota API unavailability varies by provider.** OpenAI has `/dashboard/billing/usage`. Qwen Token Plan has nothing — portal only. Check provider docs before assuming a quota endpoint exists.
- **Rolling windows ≠ monthly quota.** Qwen Individual Pro uses 5h (12K) + 7d (40K) rolling windows, not a monthly budget. The "remaining days" on the plan refers to subscription expiry, not quota reset.
- **Manual reset is async, not instant.** When the user clicks "Reset Usage Limit" on the portal, the first chat probe may still return `insufficient_quota` for a few seconds. Verify with a retry (1-3 attempts, 2s sleep between) before declaring the reset successful. If still 429 after 3 attempts, the reset didn't propagate — check portal again.
- **After manual reset, also verify ALL sibling keys in the same plan.** Qwen Token Plan Individual + Team + base key share credit pools in practice — testing one key and seeing 200 does not mean the others are free. Run the full sweep (3 keys × 7 text models) before declaring the seat alive. Seen 2026-08-07: a manual reset cleared the 7-day window, the 5-hour window was already Temporarily Lifted (∞ shown on portal), but `QWEN_API_KEY` (DIEXP) and `QWEN_BAILIAN_KEY` (IEHM) returned `insufficient_quota` on the first probe and 200 on the second — same physical pool, different key alias propagation delay.
- **Image and TTS models do NOT speak `/chat/completions`.** `wan2.7-image*` returns HTTP 400 on chat endpoint, `qwen-audio-3.0-tts-plus` returns 500. They need `/images/generations` and `/audio/speech` respectively. Do not count these as model failures during a sweep — verify which endpoint the model actually speaks before flagging it as dead.
- **Verify "wired into FED" claims with a live probe, not just the diff.** After patching `/root/A-FORGE/litellm-config.yaml` or `/root/.config/opencode/opencode.json`, always run a real chat call through `127.0.0.1:4000/v1/chat/completions` and inspect `system_fingerprint` to confirm which backend actually served the request. DashScope/Aliyun Qwen fingerprint starts with `fp_a18b46594c_prod0820_fp8_kvcache_20260402`. Diff-only verification misses JSON round-trip drops (see `references/json-roundtrip-silent-drops.md`).
- **A chat probe can hang (`curl timeout`) instead of returning a clean error.** This happens when the upstream is processing the request but the proxy drops the connection. A timeout is NOT the same as 429 — it can mean (a) the request reached the upstream and is being processed, (b) a network path is broken, or (c) the upstream is overloaded. Treat timeouts as "try again with longer timeout" before declaring failure. The Qwen Individual key on token-plan.ap-southeast-1 regularly takes 20–50s for the first request after a reset (cold path); a 15s timeout will miss it.
- **PAYG vs Token Plan failure modes look identical at the network layer but require different fixes.** Both return 429/403, but Token Plan wants a portal reset or wait, PAYG wants billing config. Always read the error code field (`insufficient_quota` vs `FreeTierOnly`) before recommending the user do anything.
- **Cascade rewiring is a 3-step swap, not 1.** When moving a cascade tier from one API key to another: (1) probe `GET /v1/models` on the new key to see its roster, (2) update endpoint + key in the cascade YAML, (3) restart the proxy service — config changes don't hot-reload. Test with a tiny completion (max_tokens=10) on each affected alias before declaring success.
- **Reasoning-heavy models eat your test budget.** Sending `max_tokens: 20` to `qwen3.7-plus`, `qwen3.8-max`, or `mimo-v2.5` returns empty `content` because the model consumes all tokens in internal reasoning before producing output. **Fix:** use `max_tokens: 200+` for any probe of a reasoning model. HTTP 200 with empty content = model is alive, not broken.
- **`finish_reason: "length"` + empty content is the token-starvation signature.** Same root cause as above, but on a successful 200: the budget was consumed by internal CoT before a single answer token was emitted. Observed 2026-08-08: `agi-333` (qwen3.8-max) with `max_tokens=20` returned exactly this; the identical call with `max_tokens=200` returned clean output in 0.9s. Never diagnose API/proxy/key as dead on this signature — re-probe with a larger budget first.
- **Low-entropy prompts can trigger a reasoning loop on flash-tier models.** qwen3.6-flash took 26s and 3,557 tokens to answer "say hello in 5 words" — the reasoning engine loops on trivial tasks ("V8 to go to the corner shop"). This is NOT a failure: HTTP 200, correct answer, but massive token burn + latency. Diagnostically: a 200 whose `usage.completion_tokens` hugely exceeds the expected answer length is overthink, not a hang — read `usage` before declaring timeout, and set generous `--max-time` (30s+) when probing reasoning models. **Do NOT use qwen3.6-flash for short, low-entropy probes** — the older recommendation to "pick qwen3.6-flash for cascade health probes" is wrong as of 2026-08-08 because of this loop. Use qwen3.8-max instead (clean reasoning, sub-2s for "OK").
- **`fed_probe` only probes providers with real balance APIs.** `/root/AAA/scripts/balance_probe.py` hardcodes `TRACK_A = {"deepseek": ...}` only — credit-based providers (qwen-token-plan-individual) sit in token_bank.db as track A but are silently skipped by `fed_probe` (observed: probe reported "1 probed, 0 failed" with no Qwen row at all). Refresh path: (1) run `python3 /root/AAA/scripts/qwen_credit_monitor.py` — probes key liveness + estimates 5h/7d credit burn; (2) stamp the row via direct sqlite UPDATE on `/root/.local/share/arifos/token_bank.db` (providers table: `last_probed_at`, `last_updated`, `notes` with the audit trail + F2 timestamp); (3) verify via `fed_status` over FED MCP :7074. Without step 2, `fed_status` will keep showing stale `last_probed_at` even after the credit monitor runs.
- **Vision test images need to be real screenshots/charts, not synthetic 1×1 PNGs.** A `data:image/png;base64,<1x1-pixel>` test will 400 from most vision models with "illegal image format" — the model rejects the format before vision routing is even tested. Use a real screenshot or chart screenshot when probing vision cascades.
- **`fed-doctor` is the federation-wide equivalent of this recipe.** `/root/scripts/fed-doctor.sh` runs the dual-probe on `127.0.0.1:4000/v1/models` (with-key vs no-key) and returns `UP / KEY_MISSING / DOWN` JSON in one shot. Use it as the first probe when "FED failed" surfaces in any chat UI — distinguishes gateway-down (rare) from upstream-env-missing (the actual 95% cause, when opencode's process env lacks `LITELLM_MASTER_KEY`). Recipe + pre-flight wrapper: `fed-cognitive-allocator/references/fed-doctor-preflight-2026-08-08.md`.
- **CRITICAL: LiteLLM does NOT cascade fallback on HTTP 400 — credit exhaustion kills agents silently.** When a provider returns `400 Insufficient Balance` (DeepSeek, others), LiteLLM treats it as a **client error**, not a provider failure. The fallback chain never fires. The agent dies with `BadRequestError: OpenAIException - Insufficient Balance. Available Model Group Fallbacks=None`. Only certain error types (429, 500, timeout, connection errors) trigger cascade fallback. **Fix:** when a provider's credit is exhausted, demote it to `order:99` in EVERY model group in `/root/A-FORGE/litellm-config.yaml` and promote known-good providers to `order:1`. Then `systemctl restart litellm-federation` — config changes don't hot-reload. Verify with a real chat probe through the affected model group alias. Full fix recipe + PyYAML reorder script: `references/deepseek-exhaustion-reorder-2026-08-09.md`.
- **Equal-order tiers = round-robin = intermittent provider errors (2026-08-09).** An alias whose tiers all share the same `order` (observed: apex-888 with MiniMax AND deepseek both at `order: 99`) is load-balanced per request — `curl /v1/chat/completions` on the alias can return ALIVE while claude's `/v1/messages` on the SAME alias hits the credit-dead tier and 402s. Probe the same alias via BOTH OpenAI-format and Anthropic-format endpoints to reveal round-robin. **`order` lives INSIDE `litellm_params`** in litellm-config.yaml — probing entry-level `e.get('order')` returns nothing even when orders exist; read `e['litellm_params'].get('order')`. Symptom map: `Credit balance is too low` = MiniMax 402 (credit exhausted); `Insufficient Balance` = DeepSeek 400; `usage limit ... billing cycle` = Kimi 403 (quota). Fix: promote known-good tier to `order: 1`, demote dead tier to `order: 99`, restart litellm-federation.
- **Use PyYAML, not the patch tool, for litellm-config.yaml edits.** The file has many near-identical YAML blocks (same `api_base`, same `api_key`, same `model_info` fields) making `old_string` non-unique for the patch tool. Use `execute_code` with `yaml.safe_load` → reorder by `order` field → `yaml.dump` — one operation fixes all model groups at once. See `references/deepseek-exhaustion-reorder-2026-08-09.md` for the working script.
- **`curl -sf` reports litellm ports as "down" when they're actually listening.** LiteLLM returns 401 on `/health` without `Authorization: Bearer $LITELLM_MASTER_KEY`, and `curl -sf` treats any non-2xx as failure. Use `ss -tlnp | grep <port>` to verify the process is listening regardless of auth state. The fed-watchdog logs show `HTTP 000` for the same reason — the watchdog's curl lacks the auth header on health probes.
- **HAProxy :4000 is the front door, litellm-federation :4011 is the backend.** The systemd service file says `--port 4000` but HAProxy binds :4000 and proxies to :4011. Probing :4000/health through HAProxy works but probing :4011 directly requires the auth key. Both are "correct" — know which layer you're testing.
- **CRITICAL: HAProxy health check key mismatch = silent FED 503 (2026-08-09).** HAProxy's `http-check send hdr Authorization "Bearer <key>"` must contain the REAL `LITELLM_MASTER_KEY`, not a placeholder. If the key is wrong/expired/redacted in `haproxy.cfg`, HAProxy marks the backend as DOWN → 503 "No server is available" even though litellm-federation is running and healthy. **Symptom:** `curl 127.0.0.1:4011/health -H "Authorization: Bearer $LITELLM_MASTER_KEY"` returns HTTP 200, but `curl 127.0.0.1:4000/health` returns 503. **Fix:** `sed -i "s|<placeholder_key>|${LITELLM_MASTER_KEY}|" /etc/haproxy/haproxy.cfg && systemctl reload haproxy`. Verify with `journalctl -u haproxy -n 5` — look for "Server llm_nodes/fed_primary is DOWN, reason: Layer7 timeout" (key mismatch) vs "UP" (fixed). Also check `ss -tlnp | grep 4011` to confirm litellm-federation is actually listening before blaming HAProxy.
- **litellm-federation service can get stuck in `deactivating (stop-sigterm)` state.** When this happens, :4011 stops listening but `systemctl status` shows "active". `ss -tlnp | grep 4011` reveals the truth (no listener). Fix: `systemctl restart litellm-federation` and wait 15-20s for prisma migration to complete before the port listens.
- **`/model` picker shows duplicates from TWO sources (2026-08-09 full map).** The picker merges: (1) `config.yaml` providers (user-defined, 15+ entries) + (2) built-in plugin providers from `/usr/local/lib/hermes-agent/plugins/model-providers/*/` (auto-registered in `auth.py:447` if env var has a key). Duplicates happen when the same API key appears in both. Example: `DASHSCOPE_API_KEY` is set → `dashscope-payg` (config) + `alibaba` plugin + `alibaba-coding-plan` plugin = 3 picker entries for the same Alibaba endpoint. Same for `MINIMAX_API_KEY` → `minimax` (config) + `minimax` plugin. `KIMI_API_KEY` → `kimi-coding` plugin (hardcoded in `auth.py:251`, NOT skipped by auto-extend skip set) + kimi models in 5 config.yaml providers. **Dedup strategy:** (a) remove duplicate seats from config.yaml (keep one per endpoint), (b) disable built-in plugins that duplicate config entries by renaming their dir (`mv alibaba alibaba.disabled`), (c) `list_picker_providers()` in `model_switch.py:2463` already drops providers with empty model lists — leverage this by ensuring dead providers have no models. Also: 4 Qwen Token Plan seats (qwen-token-plan, qwen-token-plan-standard, qwen-token-plan-team-owner, qwen-token-plan-individual) all share the same Alibaba endpoint and all list qwen3.7-max — keep individual only, remove the other 3.
- **Live provider status table (2026-08-09 probe).** ALIVE: Qwen Individual Pro (qwen3.7-max ✅), Fireworks (glm-5p2 ✅), MiMo Token Plan (mimo-v2.5 ✅), Groq (free ✅), OpenCode Go (qwen3.7-max ✅), FED :4000 (hermes-asi → mimo-v2.5 ✅). DEAD/exhausted: DeepSeek (Insufficient Balance 402), Kimi Coding (usage limit reached 403), DashScope PAYG (free tier exhausted 403), Gemini (rate-limited 429), Nous (404), MiniMax (Token Plan rate-limited 429), SEA-LION (no key). Re-probe before acting — status changes as credits replenish or rate limits reset. **UPDATE same-day (evening 2026-08-09): DeepSeek ALIVE again — balance $16.66, `is_available:true`, `deepseek-v4-pro` 1-token probe 200.** The "DEAD" verdict was a morning snapshot; credits were topped up hours later. This table is a snapshot, not doctrine — the final sentence is the rule.
- Full HAProxy key mismatch diagnosis + fix recipe: `references/haproxy-key-fix-2026-08-09.md`
- Gemini API live probe data, free tier limits, model list, deprecation schedule, working probe commands: `references/gemini-api-probe-2026-08-09.md`
- **FED NOT registered in Hermes model picker at all (2026-08-09).** FED (:4000 HAProxy → :4011 LiteLLM) serves 12 model aliases but never appears in `/model` picker. Root cause: FED is not registered as a Hermes provider at ANY level — no `CANONICAL_PROVIDERS` entry in `models.py:1053`, no `custom_providers` entry in `config.yaml`, no plugin under `plugins/model-providers/fed/`. FED only exists as systemd services + env vars (`LITELLM_MASTER_KEY`). **Fix options (effort order):** (A) Add as `custom_providers` in `config.yaml` with `base_url: http://127.0.0.1:4000/v1`, `api_key: ${LITELLM_MASTER_KEY}`, `model: hermes-asi` (T1, simplest, reversible); (B) Create `plugins/model-providers/fed/` plugin with full registry entry + auto-discovery from `:4000/v1/models` (T2, first-class); (C) FED as sole provider, remove all direct provider env vars (T3, needs 888_HOLD). Arif's vision: FED = PRIMARY, direct providers = FALLBACK. Currently Hermes uses `provider: fireworks` as default — FED is not even in the picker.
- **Kimi Code sibling diagnosis verification pattern (2026-08-09).** Kimi Code pasted a detailed 5-item FED failure diagnosis. Verification results: (1) "HAProxy → 401 auth broken" — CONFIRMED but REFINED: 401 on no-key live requests is by design (clients send own key); 503 was from health-check key mismatch (already fixed); (2) "DeepSeek 402" — CONFIRMED; (3) "MiniMax 429" — CONFIRMED; (4) "litellm-config.yaml uncommitted change" — REFUTED: `git diff` was empty; (5) "FED providers DB MiMo/MiniMax dormant" — plausible but unprobed. Lesson: sibling diagnoses are valuable hypotheses but every claim needs live probe verification — at least one claim was wrong, and the refined understanding of 401 changed the fix priority.
- HAProxy auth injection config template (injects master key for all backend requests): `references/haproxy-auth-injection-config.cfg`
- FED full 4-step recovery procedure (revert config → restart → fix HAProxy → probe + promote): `references/fed-recovery-procedure-2026-08-09.md`
- **HAProxy auth injection — make FED work for clients that don't send keys (2026-08-09).** HAProxy health check key fix only solves `/health` probes. Live `/v1/chat/completions` from OpenClaw/Claude Code that don't carry `Authorization` still get 401 from LiteLLM. **Fix:** add `http-request set-header Authorization "Bearer ${LITELLM_MASTER_KEY}"` in the `backend` section of `/etc/haproxy/haproxy.cfg`. This injects the master key into ALL forwarded requests, not just health checks. After: `systemctl reload haproxy`. Verify: `curl -s http://127.0.0.1:4000/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"hermes-asi","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'` (NO Authorization header) → should return 200. Full config template: `references/haproxy-auth-injection-config.cfg`.
- **DeepSeek has a balance API endpoint (2026-08-09).** `GET https://api.deepseek.com/user/balance -H "Authorization: Bearer $DEEPSEEK_API_KEY"` returns `{"is_available":false,"balance_infos":[{"currency":"USD","total_balance":"-0.07",...}]}`. Use this to confirm actual dollar balance — the FED `token_bank.db` had `$14.81` but the API returned `-$0.07` (negative overdraft). Per-key billing can diverge from DB-tracked balance. Always probe the balance API before trusting DB numbers for DeepSeek. **Balance flips fast — statuses are T₀ snapshots.** Same day (2026-08-09): morning probe showed `is_available:false, -$0.07` (source of sibling "DeepSeek dead" claims), evening probe showed `is_available:true, $16.66` with a live `deepseek-v4-pro` 200. Never propagate "provider X dead" from one probe or one sibling report — re-probe balance + one chat completion at decision time. **Env-file gotcha:** kunci-mas.env lines are `export VAR=...`, so `grep -c "^VAR="` returns 0 even when the key exists — grep `^export VAR=` or just `VAR=`.
- **token_bank.db track promotion (2026-08-09).** FED providers in `/root/.local/share/arifos/token_bank.db` have `track_type` column: `A` = active (fed_route can recommend), `B` = dormant (skipped). To promote a provider: `sqlite3 /root/.local/share/arifos/token_bank.db "UPDATE providers SET track_type='A', confidence_score=0.5, last_probed_at='$(date -u +%Y-%m-%dT%H:%M:%SZ)' WHERE provider_name='mimo-platform';"`. Set confidence to 0.5 until a live probe passes, then bump to 0.9+. Kimi Code diagnosed this as the missing "wire" — litellm-config.yaml had the routing but `fed_route()` couldn't recommend dormant providers.
- **Gemini API lifecycle (2026-08-09 deep research + live probe).** Model retirement schedule: `gemini-2.0-flash` retiring Jun 2026 → use `gemini-3.1-flash-lite`. `gemini-2.5-flash` retiring Oct 2026 → use `gemini-3.6-flash` (GA Jul 2026, latest stable). Free tier: 20 RPD for 2.5 Flash, 5 RPD for 2.5 Pro, 10 RPM. `gemini-2.5-flash` at 20 RPD is too tight for agent use — enable pay-as-you-go billing in Google AI Studio ($0.30/1M input, $2.50/1M output). Key works (39 chars, `AIzaSy...` prefix) but 429 = free tier quota exhausted, not key dead. **Live probe (2026-08-09):** `gemini-2.5-flash` → 429 `quotaId: GenerateRequestsPerDayPerProjectPerModel-FreeTier` (quota=20, exhausted). `gemini-3-flash-preview` → ✅ WORKS on both native API and OpenAI-compat endpoint. `gemini-3.5-flash` listed but untested. 50 models available via `GET /v1beta/models?key=$GEMINI_API_KEY`. Native API: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=$GEMINI_API_KEY`. OpenAI-compat: `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions` with `Authorization: Bearer $GEMINI_API_KEY`. **Hermes curated list gap:** `_PROVIDER_MODELS["gemini"]` in `models.py:294` only lists `gemini-3.1-pro-preview`, `gemini-3-pro-preview`, `gemini-3.5-flash`, `gemini-3.1-flash-lite-preview` — missing `gemini-3-flash-preview` (which actually works). Use `/model gemini-3-flash-preview --provider gemini --global` to bypass the curated list. Provider config: `auth.py:235` with `api_key_env_vars=("GOOGLE_API_KEY", "GEMINI_API_KEY")`, `base_url_env_var="GEMINI_BASE_URL"`.
- **FED full recovery procedure (4-step, 2026-08-09).** When FED :4000 returns 503 and all agents fail: (1) `cd /root/A-FORGE && git checkout litellm-config.yaml` (revert uncommitted order changes, restore deepseek=order:1); (2) `systemctl restart litellm-federation` (wait 15-20s for prisma migrate, verify `ss -tlnp | grep 4011`); (3) Fix HAProxy: patch `haproxy.cfg` with real `LITELLM_MASTER_KEY` in health check + add `http-request set-header Authorization` for auth injection, `systemctl reload haproxy`; (4) Probe each upstream directly: `curl -s -w "%{http_code}" <provider>/chat/completions` to identify which are alive vs dead. Promote alive providers in token_bank.db to Track A. Full recipe: `references/fed-recovery-procedure-2026-08-09.md`.

## Hermes profile `key_env` multi-key triage (2026-08-11)

**Symptom:** User reports model returns "rate-limiting" / generic 429 on direct provider. Same endpoint, other models from different keys work fine.

**Root cause:** Hermes profile's custom provider block uses `key_env: QWEN_API_KEY` but that key is exhausted while `QWEN_INDIVIDUAL_API_KEY` (same Alibaba Cloud Singapore endpoint) has remaining credits. Profile only reads ONE env var from its block.

**Pattern across all providers:** Config declares intent (`key_env: X`). If X is exhausted, profile fails even though the API and endpoint are alive. Different keys under the same provider = different credit pools.

**Multi-profile batch fix:** When patching across multiple profiles (hermes_asi, hermes_apex, hermes_forge):
1. Backup each profile separately: `cp $f $f.bak-$(date +%Y%m%d-%H%M%S)`
2. Single `sed -i 's/key_env: OLD/key_env: NEW/g' "$f"` per profile
3. Validate YAML: `python3 -c "import yaml,yaml.safe_load(open('$f'))"`
4. Verify zero legacy remains: `grep -rn 'key_env: OLD' /root/.hermes/profiles/*/config.yaml`
5. User MUST start new session — config reads at boot, old session still holds stale key in memory.

**Cross-session restart required:** Config is read-only at process startup. Patching config.yaml does NOT hot-reload. After any key_env change, tell user to open a new session/channel for the new config to take effect.

**Decision tree:** See `references/qwen-profile-triage-flow.md`.

---

## Qwen PAYG free quota (Model Studio Singapore) — Separate from Token Plan

**Symptom:** User asks about "free model" on Alibaba Cloud; reports seeing dashscope quotas or searching GitHub for FRAME repo not found.

**Discovery:** Alibaba Cloud Model Studio (Singapore region) grants **per-model free quota of 1M tokens** valid for 30–90 days to new users. This is **separate infrastructure** from Qwen Token Plan.

| Aspect | Token Plan | PAYG Free Quota |
|---|---|---|
| Endpoint | `token-plan.ap-southeast-1.maas.aliyuncs.com` | `dashscope-intl.aliyuncs.com` |
| Keys | `QWEN_API_KEY`, `QWEN_INDIVIDUAL_API_KEY`, `QWEN_BAILIAN_KEY` | `DASHSCOPE_API_KEY` (general PAYG) |
| Quota unit | Rolling 5h (12K) + 7d (40K), shared pool | Per-model 1M tokens, independent per model |
| Visibility | Portal only (no API) | Console shows remaining balance |
| Error when exhausted | `insufficient_quota` (429) | `AllocationQuota.FreeTierOnly` (403) |
| Reset | Manual portal reset or wait | Auto-expires after 30–90 days, no manual reset |

**Key insight:** General PAYG keys can access free quota on International scope. Token Plan keys (Coding Plan, Individual Pro, Team) have their own separate credit pool. They share endpoint but different billing system. Only PAYG consumes free quota.

**Common error codes:**
- `FreeTierOnly`: Free tier exhausted, PAYG key needs payment info enabled to continue
- 90-day expiry: Free quota auto-expires, cannot be manually reset (wait for re-registration or top-up)

**FED/LiteLLM integration:** When adding PAYG route to litellm-config.yaml:
```yaml
- model_name: apex-888
  litellm_params:
    model: openai/qwen3-max
    api_base: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    api_key: os.environ/DASHSCOPE_API_KEY
    order: 1
```
Probe the roster first: `curl ... /v1/models | jq '.data[].id'` then test a chat completion with max_tokens small.

**Provider discovery:** When searching `github.com/ariffazil/FRAME` and getting "Not Found", it means repo is PRIVATE (authenticated git clone works, public API returns 404). Not a missing project — internal substrate organ only.

**Reference:** Full details in `references/qwen-payg-free-quota-intl.md`.

---

## Memory pressure handling: Page cache drop before earlyoom kill (2026-08-11)

**Symptom:** `earlyoom` near trigger point (mem <10%, swap <5%). Heavy processes like opencode would be killed if we let it reach critical.

**Principle:** Never kill active worker unless absolutely necessary. Drop kernel page cache instead — reversible, zero data loss, non-destruction action.

**Recipe:**
```bash
# Check current state
free -m
sync  # flush dirty pages first
echo 3 > /proc/sys/vm/drop_caches  # drops page+inode+dentry caches
free -m  # verify RAM freed

# Monitor recovery
journalctl -u earlyoom --since "30 min ago" | grep -icE 'kill|oom|SIGTERM'  # should be 0
```

**Why this works:** Cache is reclaimable memory not currently used by applications. Dropping it increases available RAM without touching working sets. Kernel will refill cache as needed from disk (dirty data stays in RAM until eviction based on LRU).

**When to escalate:** If drop_caches doesn't recover mem above ~15% AND swap below 20%, THEN consider:
1. Killing idle processes first (opencode with low CPU, duplicate sessions)
2. Adding temporary swap space via file-backed swap
3. Restarting high-memory processes strategically (not random kill)

**Pitfall:** Never use `swapoff` / `swapon` repeatedly — can fragment swap device, cause performance issues. Prefer cache drop + selective process management.

---

## FRAME Organ vs Capability Map vs GitHub Repo — Clarification Pattern (2026-08-11)

**User confusion:** "What is FRAME?", "Why FRAME not found on GitHub?"

**Reality:** Three distinct things sharing the name:

### 1. FRAME Organ (Substate · Port :18085) ✅ LIVE
- **Repo:** `github.com/ariffazil/FRAME` (PRIVATE — authenticated git clone works, public API returns 404)
- **Service:** `frame-organ.service` (running, 5+ days uptime)
- **Role:** Federation Reference & Assessment Measurement Engine
- **Measurement:** 5-dimension W-vector (Objective Fidelity, Authority Boundary, Context Integrity, Tool Control, Feedback Integrity)
- **Authority:** OBSERVE_ONLY — measures, never adjudicates

### 2. MCP-FRAME Doctrine (/root/AAA/docs/MCP-FRAME.md) 📚 DRAFT
- **Concept:** Per-agent capability mapping — "which agent has what tools"
- **Status:** Documentation form only, not integrated into runtime yet
- **Purpose:** Define capability-to-agent resolution layer for federation

### 3. Capability Framework (generic term) 📖 GENERIC
- **Context:** Any architecture diagram discussing "capability framework" for agents
- **Ambiguity:** Could refer to AAA capability registry, FRAME organ metrics, or general design patterns
- **Clarify:** Always ask "Which FRAME?" — specify context before proceeding

**Resolution pattern:** When user mentions "FRAME":
1. Check if they mean the running organ (port probe, service check)
2. Check if they mean the capability map doc (file lookup)
3. Ask for context if ambiguous

**Never assume:** "FRAME" alone has three possible meanings in arifOS context.

---

## Post-reset verification recipe

After any portal action (manual reset, credit pack add, plan renewal), verify all 3 keys + all text models in a single sweep:

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
for key_label in "QWEN_API_KEY|$QWEN_API_KEY" "QWEN_INDIVIDUAL_API_KEY|$QWEN_INDIVIDUAL_API_KEY" "QWEN_BAILIAN_KEY|$QWEN_BAILIAN_KEY"; do
  label="${key_label%%|*}"; key="${key_label#*|}"
  for model in qwen3.8-max qwen3.7-max qwen3.7-plus qwen3.6-flash deepseek-v4-pro glm-5.2; do
    code=$(curl -s -o /tmp/p.json -w "%{http_code}" --max-time 30 "$QWEN_BASE_URL/chat/completions" \
      -H "Authorization: Bearer $key" -H "Content-Type: application/json" \
      -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"OK\"}],\"max_tokens\":5}")
    [ "$code" = "200" ] && echo "✅ $label | $model" || echo "❌ $label | $model → $code"
  done
done
```

**Expected after reset:** all 3 keys × 7 text models = 21 ✅ lines. Image (`wan2.7`) and TTS (`qwen-audio-3.0-tts-plus`) models return 400/500 on chat endpoint — that's correct, they need `/images/generations` and `/audio/speech` respectively.
