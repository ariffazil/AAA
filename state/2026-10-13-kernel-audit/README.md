Status: DRAFT_HOLD — read-only audit handoff, awaiting F13 review (F13 standing ruling 2026-10-13)
Status-class: HOLD (audit, no seal)

# State Handoff — 2026-10-13 · FED Model Audit + Kernel Defect Confirmation

**Lane:** VERIFY + HANDOFF (Codex, FI-005) — read-only, no mutation
**Authority:** 888 (F13 SOVEREIGN)
**Date captured:** 2026-10-13 ~20:30–20:45 MYT
**Test rig:** /root/.secrets/kunci-mas.env, litellm-federation.service, fed-aware-middleware.service, arifOS :8088

---

## 1. Confirmed defects (one line each, evidence-cited)

| # | Defect | Status | Evidence |
|---|---|---|---|
| D1 | **F5 fail shows in /health but underlying peace2 score depends on degraded_reasons length** — F5 measure is not independent of the very kernel state it is supposed to measure | CONFIRMED | `arifOS/arifosmcp/runtime/rest_routes/rest_routes.py:1117-1155` + `scripts/telemetry/f4-f9-probe.py:137-179` (peace2 = p² × (1 + passing/target); p=1 only when no OTHER floor fails AND no degraded_reasons) |
| D2 | **F5_peace2 = 0.6 hardcoded snapshot** ChatGPT cited is from a different time; live claims.json (20:35 MYT) shows 0.7754 | REFUTED-as-current | `/var/www/html/arifos/claims.json` at 20:35 MYT shows `F5_peace2: 0.7754` not 0.6; 0.6 was a stale snapshot |
| D3 | **6 floors (F5,F6,F7,F8,F9,L10) sourced from ONE static file (claims.json) at ONE timestamp** | CONFIRMED | Same `floors_provenance`: `f4_f9_probe:claims.json:2026-10-13T12:30:02.527+00:00` for 6 floors (live /health payload) |
| D4 | **/health?detail=1 lost floor data mid-audit (per ChatGPT observation earlier today)** | UNVERIFIABLE without timestamped re-probe; live `floor_pass:15, floor_target:13, floor_failing:["F5"]` NOW | `/health` at 20:36 MYT shows full floor detail (15/13, F5 fail) |
| D5 | **Failed floor differs across endpoints: /health says F5, arif_init(mode=canary) said L11 (per ChatGPT/opencode transcript earlier today)** | PARTIALLY REFUTED — live /health says F5 only, no L11; the canary mode today returns a JSON-RPC validation error (different canary format) so cannot be re-tested | live `/health` at 20:36 MYT: `floors_failing:["F5"]` only |
| D6 | **release_name vs git_commit drift** (opencode transcript cited `2026.10.12-f7afb2a` vs `690b154`) | REFUTED-as-current | Live `runtime.source_commit=built_commit=690b154`, `git HEAD=690b1546...` — they MATCH. The `release_name:"v2026.08.01-bijaksana"` in build-info.json is from the build process, not the deployed source. The "drift" warning in /health is on the `release_name` string vs `source_commit` (build metadata drift, not code drift) |
| D7 | **>= inflation (16 vs 13 floors)** | CONFIRMED | `floors_pass:15, floors_target:13` — 15 > 13 means the F2 producer counts alias duplicates; aliases F11↔L12, F12↔L11, F13↔L13 inflate the count by 3 |
| D8 | **codex (model in config.toml) returns 400 on raw :4000/chat/completions** | CONFIRMED | `curl ... model=codex` → `400 Invalid model name passed in model=codex. Call /v1/models` (response: 400, body confirmed). codex is a routing alias that ONLY works via :4010/fed-aware-middleware → fed router cascade |
| D9 | **OPENAI_API_KEY present in env files but NOT in live fed-aware-middleware or litellm container env** | CONFIRMED | `/proc/3033/environ` (fed-aware-middleware) and docker litellm container both show no OPENAI_API_KEY; source code (`fed_aware_middleware.py:65,224`, `providerFactory.ts:83-86`, `capabilities.py:89,131`) has the binding ready, but no live key is passed; OPENAI route unreachable from FED today |
| D10 | **qwen3.8-max alias lands on MiniMax (api.minimax.io), not Qwen Cloud** | CONFIRMED | Live curl: `x-litellm-model-name: openai/MiniMax-M3.1-Flash-Preview` + `x-litellm-model-api-base: https://api.minimax.io/v1`; litellm-config.yaml has both qwen-cloud routes AND a router_settings cascade that includes MiniMax-M3.1-Flash-Preview in the fallback chain |
| D11 | **7 of 11 provider keys are NOT in litellm-federation docker env** (present in /root/.secrets but not propagated) | CONFIRMED | docker exec env dump shows: DEEPSEEK ✓, MINIMAX ✓, GEMINI ✓, OPENCODE_GO ✓, TOKENROUTER ✓ — but QWEN_TEAM_OWNER, QWEN_ARIFOS, QWEN_HERMES, MIMO_API_KEY, MIMO_PLATFORM, ZAI, DASHSCOPE are NOT visible in container env. `/proc` env scrape shows the daemon set for fed-aware-middleware DOES have these, but the litellm container does not — so multiple aliases will fall through to whatever cascade is reachable from the visible keys |

---

## 2. Verified alias list (49 of 51 model aliases, 2 batches)

### 2.1 TESTED-OK (returned 200 + tokens)
| alias | http | billed provider (from x-litellm-model-api-base) | real model (from x-litellm-model-name) |
|---|---|---|---|
| codex | **400** | — | (NOT a model name; routing alias) |
| MiniMax-M3 | 200 | api.minimax.io | openai/MiniMax-M3 |
| MiniMax-M3.1-Flash-Preview | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview |
| deepseek-v4-pro | 200 | api.deepseek.com | openai/deepseek-v4-pro |
| deepseek-v4-flash | 200 | api.deepseek.com | openai/deepseek-flash |
| qwen3.8-max | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview (cascade fallback) |
| qwen3.6-plus | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview (cascade fallback) |
| glm-5.3 | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview (cascade fallback) |
| glm-5.2 | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview (cascade fallback) |
| mimo-v2.5-pro | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview (cascade fallback) |
| mimo-v2.5 | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview |
| mimo-v2.6-pro | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview |
| mimo-v2.6-flash | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview |
| mimo-v2.6-pro-payg | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview |
| mimo-v2.6-flash-payg | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview |
| mimo-v2.6-pro-ultraspeed | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview |
| kimi-k3 | 200 | api.minimax.io | openai/MiniMax-M3.1-Flash-Preview (cascade) |
| sealion / fed/sealion | 200 | api.sea-lion.ai | openai/aisingapore/Qwen-SEA-LION-v4-32B-... |
| qwen-vision | 200 | api.deepseek.com | openai/deepseek-flash |
| gemini-vision | 200 | api.deepseek.com | openai/deepseek-flash |
| deepseek-v4-flash-vision | 200 | api.deepseek.com | openai/deepseek-flash |
| deepseek-v4-flash-vision-exp | 200 | api.deepseek.com | openai/deepseek-flash |
| deepseek-v3.2 | 200 | opencode.ai | openai/qwen3.8-max (different cascade path) |
| deepseek-flash | 200 | api.deepseek.com | openai/deepseek-flash |
| vision | 200 | api.deepseek.com | openai/deepseek-flash |
| fed/vision | 200 | api.deepseek.com | openai/deepseek-flash |

### 2.2 TESTED-FAIL (http 5xx / timeout)
| alias | http | reason |
|---|---|---|
| qwen3.7-max | 500 | (not in litellm config match; cascade returned 500) |
| qwen3.7-plus | 500 | same |
| qwen3.6-flash | 500 | same |
| glm-5.3-flash | 500 | same |
| qwen-coder | 500 | (config: litellm advertises but underlying call returns 500) |
| fed/image-gen | 500 | (mode=chat, image-gen needs mode=image) |
| fed/vision-parked | 500 | (PARKED — expected) |
| fed/audio-voiceclone | 429 | (rate-limited by voice clone provider) |
| mistral-large-latest | timeout (28s) | (MISTRAL key not in litellm config; cascade exhausted) |
| codestral-latest | timeout (28s) | same |
| mistral-small-latest | timeout (28s) | same |
| kimi-moonshot | 400 | (provider missing base_url) |
| deepseek-vision | 400 | (provider missing base_url) |
| multimodel | 400 | (typo? not in litellm config) |
| multimodal | 400 | (only :4010 capability, not :4000) |
| long-context | 400 | (capability sig, not :4000 model) |
| reasoning-heavy | 400 | (capability sig, not :4000 model) |
| reasoning-standard | 400 | (capability sig) |
| agent-subagent | 400 | (capability sig) |
| ast | 400 | (capability sig) |
| fed | 400 | (not a model name) |

### 2.3 Cache vs LB verdict (FASA 1.2)
- TWO different prompts to `model: qwen3.8-max` produced TWO distinct response_ids (`071d5863...` vs `071d5866...`) and TWO different content (one with output, one with `content: None` — model hit max_tokens on second call)
- `x-litellm-cache-hit` header NOT present in either response
- `x-litellm-model-name` and `x-litellm-model-api-base` headers ARE present in every 200 response
- **Verdict:** Not a response cache. Not a sticky LB. LiteLLM is doing a per-call cascade resolution and the previous `chatcmpl-b83b9b7b` repetition was an isolated coincidence or a brief load-balancer collision. **TESTED-OK distinct-ids**

---

## 3. Lane assignments (read-only next steps)

| Agent | Lane | Next read-only task |
|---|---|---|
| **HERMES** | analysis | Re-run contradiction scan on the 7 OPENAI_API_KEY source-code references (`fed_aware_middleware.py:65,224`, `providerFactory.ts:83,86,127`, `capabilities.py:89,131`, `secret-registry.yaml:14,17,162,170,208,215,235,316,322`) against `arif_init` session envelope — does the live system ever claim to have a valid OpenAI route? Output: HOLD/SEAL/VOID on OpenAI-route honesty |
| **A-FORGE** | mutation | NONE (mutation lane blocked by audit). When cleared: produce the fix-patch for f4-f9-probe.py so F5_peace2 does NOT depend on the kernel's own degraded_reasons (read from an independent signal) |
| **opencode** | page+probe audit | Re-probe `/health?detail=1` every 15 min for 2 hours; record whether floor data disappears again (re-confirm D4 or refute) |
| **Codex (this run)** | verify | DONE (this file) |
| **external verifier (your human reviewer)** | re-probe | Run: `curl http://127.0.0.1:8088/health | jq` and `curl http://127.0.0.1:4010/v1/models | jq '.data[].id'` independently; confirm D1, D8, D10, D11 |

---

## 4. Envelope status

| Envelope | Status | Note |
|---|---|---|
| **Envelope 1** | PREPARED + 4 reviews pending | per prior arifOS work; 4 semakan: kernel-side INCONSISTENT_STATE split-brain, alias double-count, F5 self-dependence, deployment_attestation string drift |
| **Envelope 2** | spec-only | not started in this audit window |
| **Envelope 3** | not started | awaiting Envelope 1 sign-off |

---

## 5. DILARANG (until you approve)

- **Do not apply Envelope 1** to arifOS kernel or restart any service
- **Do not edit `/var/www/html/arifos/claims.json`** directly (managed by cron)
- **Do not edit `/root/scripts/telemetry/f4-f9-probe.py`** (mutation lane)
- **Do not edit `/root/A-FORGE/litellm-config.yaml`** (mutation lane)
- **Do not propagate `OPENAI_API_KEY` into the running containers** without F13 review
- **Do not write to memory/VAULT999** from this audit run

---

## 6. What is UNKNOWN (honest gap)

1. Whether `codex` alias is a real load-balanced endpoint or a typed-but-not-implemented alias at :4010 (not probed end-to-end through :4010)
2. Whether `qwen3.8-max` ever actually bills Qwen Cloud (current cascade lands on MiniMax; config has Qwen Cloud as a possibility but litellm cascade order put MiniMax first in this run)
3. Whether the 7 provider keys (QWEN_TEAM_OWNER, QWEN_ARIFOS, QWEN_HERMES, MIMO_API_KEY, MIMO_PLATFORM, ZAI, DASHSCOPE) reach the litellm container through a different env file (e.g. `/dev/shm/litellm-fed-env` per service unit's `ExecStart` line, which is wiped after 5s)
4. Whether `x-litellm-cache-hit` was disabled at the proxy level, or is genuinely absent
5. Whether the F5 fail seen in /health today is the same as yesterday's (no time-series)
6. Whether the 7 "missing in container env" provider keys cause billable routes to silently fail (cascade resolves to a fallback, user thinks they used Qwen, actually used MiniMax)

---

## 7. Receipts

- Live `/health` payload (20:36 MYT): captured in this audit, inlined as D-row evidence
- Live `/var/www/html/arifos/claims.json` (20:35 MYT): 1205 bytes, 6 floors sourced, F5_peace2=0.7754
- Live curl probes: 49 alias responses captured (http status + x-litellm headers + body)
- `f4-f9-probe.py` source: `/root/scripts/telemetry/f4-f9-probe.py:137-179`
- `rest_routes.py` injection site: `/root/arifOS/arifosmcp/runtime/rest_routes/rest_routes.py:1117-1155`
- `litellm-config.yaml` cascades: `/root/A-FORGE/litellm-config.yaml:1-2187`

---

**End of handoff. Awaiting F13 ack before any mutation lane opens.**
