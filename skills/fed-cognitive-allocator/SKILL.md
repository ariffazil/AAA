---
id: fed-cognitive-allocator
name: fed-cognitive-allocator
version: 1.0.0
description: 'Operate and audit FED (`fed_route` at :7074) as the Federation Cognitive Allocator — the organ that decides which intelligence tier, reasoning depth, modality, and provider family serves each task. FED is constitutionally load-bearing (666_JUDGE/999_SEAL provider allowlist), not a cost router. Use when investigating why an LLM call was routed to a specific provider, when constitutional tier enforcement is questioned, when FLAME-vs-FED routing is confused, or when the federations-intelligence plane is being audited.'
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F2, F4, F11]
tags: [federation, routing, model, llm, constitutional, fed, cognitive-allocator]
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
- hermes
- openclaw
- agy
dependencies:
  skills:
  - federation-infra-verification
  - federation-model-routing
  - kernel-security-claim-audit
  servers: []
  tools:
  - fed_status
  - fed_route
  - fed_probe
  - fed_contrast
examples:
- "Why did my call route to deepseek-v4-flash instead of v4-pro?"
- "What providers can serve 666_JUDGE verdicts?"
- "Why is FLAME in the FED provider table?"
- "Audit the routing decision for a specific task — was the right tier chosen?"
- "Trace constitutional tier enforcement from request to provider"
tests:
- "Probe fed_status at :7074 with proper session header → returns providers array"
- "Confirm constitutional rule restricts 666/999 to 4 providers"
- "Verify effort_level parameter maps to model tier as documented"
- "Cross-check fed_route output against actual provider call"
version_lock:
  schema_version: '1'
  artifact_hash: pending
---

# FED — Federation Cognitive Allocator

> **Forged:** 2026-08-08 by 333-AGI after FED_RECLASSIFICATION_PROBE
> **SOT:** `/root/AAA/scripts/fed_router.py` (live source), `/root/.config/federation-models.json` (canonical registry)
> **Sister:** `federation-model-routing` (LiteLLM proxy chain), `federation-infra-verification` (live state probing)
> **Doct:** DITEMPA BUKAN DIBERI

## USE WHEN

The task involves:

- Understanding why a specific LLM call was routed to a specific provider
- Auditing constitutional tier enforcement (which providers may serve 666/999)
- Investigating the relationship between FLAME (free inference) and FED (routing)
- Distinguishing between `arif_route` (organ routing) and `fed_route` (intelligence routing)
- Validating claims that the federation has a "cost router" or "traffic router"
- Adding or removing providers from the constitutional allowlist
- Diagnosing effort-level mapping (low/medium/high/ultra to model tier)

## DO NOT USE WHEN

- The task is to route a specific LLM call (just use `fed_route` directly)
- The task is to audit the LiteLLM proxy chain (use `federation-model-routing`)
- The task is to diagnose a specific provider key issue (use `provider-quota-diagnostics`)

## The Correction

FED was previously classified as a "cost router" or "delete candidate" in earlier audits. **Both classifications are wrong.** The live source at `/root/AAA/scripts/fed_router.py` shows FED is the **Federation Cognitive Allocator**.

### What FED actually decides

| Parameter | Meaning |
|---|---|
| `task` | Natural language intent — what the agent wants done |
| `model` | Preferred model (default: deepseek-v4-pro) |
| `modality` | `text` \| `vision` \| `audio` \| `video` \| `omni` |
| `agent_id` | Calling agent: `opencode` \| `hermes` \| `kimi` \| `apex-888` \| `openclaw` |
| `constitutional_tier` | **333 (primary) \| 555 (research) \| 666 (judge) \| 999 (seal)** — maps to agent class authority |
| `effort_level` | `low` \| `medium` \| `high` \| `ultra` — reasoning depth |
| `tokens_in_estimate` / `tokens_out_estimate` | For cost logging (not the decision itself) |
| `operation` | `sense` \| `metabolize` \| `act` \| `auto` — EMD lane awareness (Fasa 1, 2026-08-08) |

The `constitutional_tier` parameter is the smoking gun. **Cost is one input, not the goal.** `effort_level=ultra` triggers "frontier models + multiple reasoning passes (SEAL-grade)" — a multi-stage cognitive allocation, not a price lookup.

### The constitutional rule

From `/root/.config/federation-models.json`:

> `deepseek-v4-pro, glm-5.2, qwen3.8-max, and MiniMax-M3 may serve 666_JUDGE and 999_SEAL roles.`

Only 4 providers are constitutionally eligible for the two highest tiers. FED enforces this — agents cannot bypass it by calling the provider directly (well, they can, but FED will not route constitutional work to anything else).

## EMD Lane Awareness (Fasa 1 — 2026-08-08, commit a3a1bf36)

FED now understands the **Encode → Metabolize → Decode** dimension (Arif's EMD framework — models classified by mechanics, not vendor). `fed_route` accepts `operation` (`sense|metabolize|act|auto`; `auto` infers from `agent_id`, so old callers are unaffected) and every response carries an `emd` block:

```json
{"verdict": "EMD_ALIGNED|EMD_MISMATCH", "operation": "act", "model_class": "act",
 "reasons": ["ACT <-> ACT aligned"], "suggested": []}
```

### Definitive EMD Model Classification Matrix (Arif-ratified 2026-08-10)

| EMD Layer | Primary Role | Assigned AI Models | Core Capability & Signature |
|---|---|---|---|
| **Encode (E)** — Context Compiler | Multimodal ingestion, long-context parsing, schema normalization | gemini-3.1-pro · MiniMax-M3 · qwen-vl-max | 1M+ Token / Multimodal Compilers: Ingests massive repos, PDFs, UI/UX layouts, raw video frames → structured context states |
| **Metabolize (M)** — Primary Reasoning Engine | Epistemic truth validation (F2), logic verification, code synthesis | deepseek-v4-pro · qwen3.8-max · kimi-k3 | Precision Logic & Autonomous SWE: Solves algorithms, proves mathematical constraints, multi-day autonomous coding loops |
| **Decode (D)** — Action & Generation | High-throughput tool calls, fast sub-agent execution, media synthesis | gemini-3.5-flash-lite · mimo-v2.5/v2.5-pro · Veo 3.1 · Nano Banana · opencode-go | Sub-100ms Action & Media Output: Fast JSON schema execution, web search grounding, voice synthesis (ASR/TTS), media generation |

**Functional Orthogonality (no redundancy):**
- **deepseek-v4-pro** = algorithmic surgeon (math, logic, unit-testable code) vs **qwen3.8-max** = long-horizon system architect (multi-file AST, autonomous PR workflows)
- **gemini-3.1-pro** = multimodal deep context (code + Search + visual docs) vs **MiniMax-M3** = high-volume fleet worker (5.1B token monthly, cost-free background scanning)
- **mimo-v2.5** = voice + off-peak execution (ASR/TTS + 20% night discount) vs **gemini-3.5-flash-lite** = sub-agent tool calling in active conversational loops

- **`EMD_MODEL_CLASS`** (14 models): sense = MiniMax-M3, qwen3.8-max, mimo-v2.5(-pro), qwen3.6-flash (with per-model `vision_in`/`audio_in` flags); act = deepseek-v4-pro, deepseek-v4-flash, wan2.7-image(-pro), qwen-audio-3.0-tts-plus; neutral = glm-5.2, qwen3.7-plus, kimi-k2.7-code, flame-free.
- **`AGENT_DEFAULT_OPERATION`**: openclaw=sense · asi-555=sense · hermes=metabolize · agi-333=metabolize · apex-888=metabolize · opencode=act · kimi=act.
- **3 rules**: R1 agent-shift (operation ≠ agent nature → MISMATCH, e.g. openclaw forced act); R2 model-lane (act work on sense-optimized model & inverse); R3 modality-gate (vision/audio/generation payload to capability-blind model → F2 violation).
- **FLAG only, never blocks** — ranked routes always returned, caller decides (F4). Hard-reject would be a F13 constitutional amendment, separate track.
- Full dicts + verified test matrix: `references/emd-lane-awareness.md`.

**The effort-override blind spot EMD exposes:** EFFORT_MODEL_MAP (`low`→flame-free, `medium/high/ultra`→deepseek-v4-pro) silently OVERRIDES the requested model. Asking for a vision-capable model (MiniMax-M3, qwen3.8-max) with `effort_level` set lands on deepseek-v4-pro — vision stripped. EMD flags this as MISMATCH (R2+R3). That is the intended telemetry, not a bug.

**Arif's FED-change workflow (binding):** draft → he reviews ("aku nak metabolize") → he says **"Forge"** → patch → verify → commit. Keep **Fasa 1** (code patch to fed_router.py + single `fed-router.service` restart) separate from **Fasa 2** (litellm-config alias additions + `litellm-federation.service` restart) — never combine Python-logic changes with infra restarts in one step (F1 reversibility, ΔS ≤ 0).

## FED inference surfaces (topology after HAProxy migration 2026-08-09)

When Arif or any opencode user says "FED failed", they almost always mean the **chat-completion path**, not the MCP route-advisor. The inference side is now a 3-layer chain — probe the LAYER, not just the alias:

| Layer | Port | Transport | Purpose | When "FED failed" fires |
|---|---|---|---|---|
| `fed-router` (FastMCP) | `:7074` | Streamable-HTTP MCP | `fed_route`, `fed_status`, `fed_probe`, `fed_contrast`, `fed_health` | Almost never — MCP errors surface verbatim with code+message |
| **HAProxy front** | `:4000` | OpenAI-compatible HTTP | Single client door → fed_primary / escape_backup | 503 = both backends unhealthy; 401 = key issue |
| `litellm-federation` (primary FED) | `0.0.0.0:4011` | OpenAI-compatible HTTP | `agi-333`, `asi-555`, `apex-888`, `opencode`, `openclaw`, `dispatch`, … | **Every time.** opencode UI collapses upstream 401/503/etc. into one-word "FED failed" |
| `litellm-escape` (survival) | `127.0.0.1:4012` | OpenAI-compatible HTTP | DeepSeek + MiMo only, no Tailscale dep — HAProxy `backup` target | Only when primary is down |
| Legacy shims (NOT FED) | `:4001` `:4002` | HTTP | `fed-clean-proxy` (Codex Responses-stripper) `:4001`; `mimo_vision_shim` `:4002` | **Never touch these** — Codex + Hermes vision depend on them |

**Port collision rule (2026-08-09 lesson):** legacy shims hold `:4001`/`:4002`. New litellm instances
MUST use free ports (currently 4011/4012) — pointing them at shim ports causes `Errno 98 address
already in use` crash-loops AND an infinite routing loop if HAProxy routes into a shim that forwards
back to :4000. Full postmortem + fix recipe: `references/fed-haproxy-migration-2026-08-09.md`.

**The 401 → "FED failed" tripwire.** opencode's `provider.litellm-federation.apiKey = "{env:LITELLM_MASTER_KEY}"` only resolves if that env var is in the opencode process environment. If opencode is launched from a shell without `source /root/.secrets/kunci-mas.env`, the key is empty → upstream returns `HTTP 401 Authentication Error, No api key passed in` → opencode UI shows "FED failed" with zero upstream context. The gateway itself is fine; the symptom is upstream env-missing. Reproduced 2026-08-08: same `:4000/v1/models` endpoint, two probes, one returned `401`, the other returned the full 12-model roster.

**The diagnostic recipe** (use BEFORE declaring "FED is broken"):

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -s -w '\nHTTP %{http_code}\n' --max-time 5 \
  http://127.0.0.1:4000/v1/models \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" | head -c 400

# Compare against the no-key probe (mirrors what opencode sees):
curl -s -w '\nHTTP %{http_code}\n' --max-time 5 \
  http://127.0.0.1:4000/v1/models \
  -H "Authorization: Bearer no-key-test" | head -c 400
# 200 with model list  = FED alive, opencode is the bug
# 401 No api key       = LITELLM_MASTER_KEY missing in opencode's env
# 5xx / connection fail = upstream litellm-federation.service issue, not FED
```

**Pre-flight wrapper (installed 2026-08-08):** `/root/scripts/fed-doctor.sh` runs the full dual-probe and returns `UP / KEY_MISSING / DOWN` with the real upstream error body. Wire it as `alias opencode='/root/scripts/opencode-fed-preflight.sh'` in `~/.bashrc` so every opencode launch surfaces the real diagnostic instead of "FED failed". Recipe + scripts: `references/fed-doctor-preflight-2026-08-08.md`.

**Two-name diagnosis table (Arif-style quick read):**

| Symptom in opencode | Surface | Probe | Real fix |
|---|---|---|---|
| "FED failed" on chat | HAProxy :4000 / fed :4011 | `curl :4000/v1/models` w/o key → 401 | `source /root/.secrets/kunci-mas.env` before launching opencode |
| "FED failed" + curl 200 | HAProxy :4000 | Check upstream model roster vs opencode agent whitelist | Wire missing alias (see `federation-seat-wiring`) |
| 503 from :4000 | HAProxy | `ss -tlnp \| grep -E '4011\|4012'` — both backends down? | `systemctl status litellm-federation litellm-escape haproxy`; check for port collisions (see migration ref) |
| `fed_route` returns error | `fed-router` :7074 | Re-run with `Accept: application/json, text/event-stream` header | Header + session ID (see §How to probe FED) |
| `fed_health` says UP but UI fails | All surfaces | `ss -tlnp \| grep -E '4000\|4011\|7074'` — listeners present? | `systemctl status litellm-federation fed-router haproxy` |

## How to probe FED

```bash
# 1. Get the session ID (MCP requires Accept header)
SID=$(curl -si http://127.0.0.1:7074/mcp -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2025-11-25' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' \
  | grep -i 'mcp-session-id' | awk '{print $2}' | tr -d '\r')

# 2. Get current provider state
curl -s http://127.0.0.1:7074/mcp -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"fed_status","arguments":{}}}'

# 3. Route a task (example: constitutional tier 666 with high effort)
curl -s http://127.0.0.1:7074/mcp -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"fed_route","arguments":{"task":"audit constitutional verdict","agent_id":"apex-888","constitutional_tier":666,"effort_level":"high","tokens_in_estimate":5000,"tokens_out_estimate":2000}}}'
```

The `Accept: application/json, text/event-stream` header is **required** — without it you get `Not Acceptable: Client must accept both application/json and text/event-stream`.

## Wiring a new provider into FED (step-by-step, proven 2026-08-08)

Full transcript: `references/provider-wiring-qwen-individual-2026-08-08.md`.

1. **Probe the key LIVE before touching anything** (F2 reality-first). `GET {endpoint}/models` with the bearer key → confirms auth + model list. Then a tiny `chat/completions` (`max_tokens:5`, "say OK") on each model you intend to route → confirms quota actually exists. A 429 `exhausted_quota` means the plan is dead (Qwen Team was exactly this).
2. **Check what LiteLLM already uses.** `grep -n "api_key" /root/A-FORGE/litellm-config.yaml` — the execution path may already be on the new key even though FED metadata points at the old one (this session's actual bug: LiteLLM on `QWEN_INDIVIDUAL_API_KEY`, FED registry on exhausted `QWEN_API_KEY`).
3. **Query token_bank.db for an existing provider row BEFORE inserting.** A sibling agent may have already inserted it under a slightly different name (this session: `qwen-token-plan-individual` existed; I created `qwen-individual` → duplicate). Align your code's provider name to the DB row's name via `sed -i` — never the reverse. `SELECT * FROM providers WHERE provider_name LIKE '%<pool>%'`.
4. **Insert provider row** (Track A if API-probed, confidence 1.0) + `route_health` rows (status LIVE, one per model). Back up the DB first: `cp token_bank.db /root/forge_work/backups/token_bank-<change>-<ts>.db`.
5. **Add `MODEL_ROUTES` entries** in `/root/AAA/scripts/fed_router.py`: new provider as `direct` class — priority 2 for deepseek family (after native direct), priority 1 for qwen-native models. Mark `"constitutional": True` on models eligible for 666/999 (deepseek-v4-pro, glm-5.2, qwen3.8-max).
6. **Add pricing-table entries in BOTH dicts** — `_estimate_cost` and `_estimate_cost_per_1k` (~lines 97 and 111). Missing one = cost surface shows default pricing.
7. **Update `/root/.config/federation-models.json`** — add/refresh provider entry with `api_key_ref`, live probed models, quota snapshot; reconcile `_meta.alive_pools` against ACTIVE provider_ids (it can carry phantom names with no matching provider).
8. **Append a billing-model tag to the DB `notes` field** (see pitfall below) then `systemctl restart fed-router.service`.
9. **Verify per tier via `fed_route`** (use `scripts/fed_mcp_probe.py`): tier 666/999 must rank the new provider #1 for its constitutional models; tier 333 cascade must include it. Note: setting `effort_level` overrides the `model` param (Effort Dial) — omit it when testing a specific model's routes.

## FED vs FLAME vs arif_route (the three routers)

| | FED (`fed_route`) | FLAME (`flame_api`) | `arif_route` (kernel) |
|---|---|---|---|
| **Question** | Which intelligence? | Which free inference lane? | Which organ? |
| **Authority** | 777_FORGE (read-allocate) | ADVISORY (no constitutional weight) | Constitutional |
| **Tier parameter** | 333/555/666/999 | none | none |
| **Cost** | Tracked but not goal | $0.00 (free tier) | n/a |
| **Constitutional rule** | 666/999 → 4 providers only | none | none |
| **Destination** | LiteLLM proxy → upstream | Direct inference mesh | GEOX/WEALTH/WELL/A-FORGE |

**FLAME is one of FED's routing destinations.** The `FLAME_PRICING` table in `fed_router.py` proves this — FED tracks FLAME as a `$0.00` provider, allocates to it when the task doesn't require constitutional weight.

## Constitutional boundary (proposed)

```
FED authority ceiling: 777_FORGE
F1 (AMANAH):     Reversible-first. No mutation of provider balances without arithmetic audit.
F2 (TRUTH):      Every route has a confidence_score; every recommendation has a reason.
F4 (CLARITY):    Output is ranked routes, not single answer; caller decides.
F11 (AUDIT):    Every call writes to token_bank.db; ledger is append-only.
F12 (INJECTION): Provider allowlists enforced at config layer; route surfaces filtered.
F13 (SOVEREIGN): Constitutional tier >= 666 requires human ack before allocation.

What FED may NOT do:
- Mutate production state
- Seal to VAULT999 (that's arif_seal)
- Bypass constitutional tier restrictions
- Run without balance confidence >= 0.5
- Allocate constitutional tier to untested providers (<10 samples)
- Route to providers whose API key is in /root/.secrets/ but not in FED config
```

## Pitfalls

- **Do not delete FED.** Every agent class (333-AGI, 555-ASI, 888-APEX, Hermes) routes through FED aliases. Removing it collapses the entire intelligence plane.
- **Do not merge into FLAME.** FLAME is a single inference lane. FED is the allocator across lanes. Merging them would collapse 14 tools and tier-routing into a single endpoint.
- **Do not merge into `arif_route`.** `arif_route` is for organ routing; FED is for intelligence routing. Different questions, different answers.
- **The `constitutional_tier` parameter is load-bearing.** If an agent sends a request without it, FED defaults to 333 (primary) — which may not be appropriate for the task. Always specify the tier.
- **The `effort_level` is not a price dial.** `low` = flash, `medium` = pro, `high` = pro + reasoning, `ultra` = frontier + multiple passes. Always specify reasoning depth explicitly.
- **FLAME is not a fallback for 666/999.** The constitutional rule restricts higher tiers to 4 specific providers. FLAME is only eligible for 333/555.
- **Tier ≥ 666 also rewrites the `model` parameter (verified live 2026-08-08).** Requesting `model=qwen3.8-max, tier=888, effort_level=high` returns routes with `deepseek-v4-pro` at ranks 1-3 (provider differs: deepseek direct, qwen-token-plan-individual, etc.) — the constitutional hard-gate forces the model to `deepseek-v4-pro` regardless of whether the requested model is itself constitutionally eligible. The other 3 constitutional providers appear only as **provider fallbacks serving the same deepseek-v4-pro**. If you need a different model at high tier, request tier=333/555 instead, or hit the LiteLLM alias directly (skipping FED). Combined with the Effort Dial, the route API is biased toward `deepseek-v4-pro` at every tier above 333 unless you explicitly omit `effort_level`.
- **FED MCP responses are SSE-framed AND double-encoded.** A raw `tools/call` returns `event: message\ndata: {...}` where the JSON-RPC body is itself a string-escaped blob. `json.load` on the raw stream fails. Strip the `event: `/`data: ` prefix, then `json.loads` twice: once for the JSON-RPC envelope, once on `result.content[0].text`. Use `scripts/fed_mcp_probe.py` — it handles both.
- **`fed_probe` MCP tool signature is broken (as of 2026-08-08).** FastMCP rejects `{"provider":...,"model":...}` with `Unexpected keyword argument`. It is advertised in `/health` but unusable via MCP. Use `fed_status` for full provider/latency/health/spend state instead. Re-verify the signature before assuming it is fixed.
- **Static balances in `federation-models.json` are purged by design.** The file's `_meta.balance_policy` says any `balance_usd` there is STALE/FALSE. Live balance = FED :7074 (`token_bank.db`) only. Do not read the registry for money.
- **Zero-balance ≠ dead for plan-based providers.** MiniMax ($0.00, monthly plan) and qwen-token-plan-team ($0.00, credits exhausted) are NOT dead — the plan billing model differs from prepaid. Track A balance gate (<$1.00) can HARD-demote these unfairly; trust `notes` + `track_type` before treating a zero as unusable.
- **Credit-based plans need a billing-model tag in `notes` or they sink.** The balance-gate `is_monthly_plan` exemption (added to `fed_router.py` 2026-08-08) keys off the provider's `notes` containing `monthly_token_plan` / `credit pack` / `credit-based` / `monthly plan` / `credit_plan`. Wiring a credit-plan provider WITHOUT appending one of these tags → route silently HARD-demoted (+10 priority, `LOW_BALANCE_HARD`) and never ranks #1.
- **Provider names are not canonical across surfaces.** One plan appeared as `qwen-individual` (my code), `qwen-token-plan-individual` (sibling's DB row), and a phantom `qwen-token-plan-individual` in `_meta.alive_pools`. Always query the DB before inserting; align code to the DB name. `federation-models.json` `_meta.alive_pools` can list pools that have no provider entry — reconcile it against ACTIVE provider_ids after any provider change.
- **EMD is flag-only by design.** The skill explicitly avoids hard-reject so it stays inside FED's `ADVISORY_ONLY` ceiling (777_FORGE). Hard-rejecting vision payloads to deepseek-v4-pro would force a constitutional amendment (F13) — separate track. CALLER decides whether to honour the flag. Tests confirm: routes cascade returned on every MISMATCH case.
- **`curl | python3` traps in shell pipelines.** The `terminal` tool flags `curl ... | python3` (security scan + auto-approval pattern) AND empty stdout can sneak through if the JSON parse silently fails on SSE frames. When probing MCP tools, save to `/tmp/<n>.json` first, then read the file with `read_file` (or `python3 < /tmp/<n>.json`) — never pipe raw curl to interpreter inline. Two empty-file incidents this session: looks like a syntax error, actually a redirect-order issue with the security scan block. **Always `wc -c /tmp/<n>.json` before parsing.**
- **Keys are not canonical across surfaces (2026-08-09 outage postmortem).** During the 11h FED outage (tailscaled dead → litellm couldn't bind 100.64.0.2:4000 → socat stuck → Hermes "provider failed after retries"), a SECOND latent bug hid behind the transport failure: `/root/.hermes/.env` held a STALE LiteLLM virtual key (`sk-lit...4b32`) that the proxy rejects (`token_not_found_in_db`, 401), while kunci-mas.env holds the current master key (`sk-lit...74ed`). The gateway only survived because `/usr/local/bin/hermes-asi-wrapper.sh` hardcodes the good key via `export OPENAI_BASE_URL/OPENAI_API_KEY`. Any process sourcing `/root/.hermes/.env` (CLI, scripts, future restarts) got 401 → "FED failed" that looks like a transport issue. **Fix: reconcile `.env` keys to kunci-mas programmatically, verify with a `curl :4000/v1/models` using the `.env` value, then test the REAL path (`hermes chat -q` via default profile).** Also: a transport-only fix can pass while the app layer still has a stale-key restart-bomb — always probe the key the file claims, not the key the wrapper exports.
- **Reasoning models + small `max_tokens` = empty content (false "dead model").** hermes-asi (MiMo V2.5) streams `reasoning_content` deltas first; with `max_tokens` ≤ 30 the ENTIRE budget is consumed by reasoning and `content` stays `""` while the HTTP status is 200 and the stream "works". This reproduces Hermes' "waiting for stream response, no chunks yet" symptom even when the transport is healthy. **Test reasoning models with `max_tokens` ≥ 256 and check `finish_reason` + `usage.reasoning_tokens`; an empty `content` with non-empty `reasoning_content` is a token-budget artifact, not a dead provider.**
- **`systemctl daemon-reload` is mandatory after editing any `.service` or `.service.d/override.conf`.** 2026-08-09: the fix changed `litellm-federation` drop-in to `--port 4011`, but the crash-loop restarts kept reusing the OLD cached ExecStart (`--port 4001`) — systemd reads unit files at daemon-reload, not at every restart. Symptom: on-disk config correct, running process wrong, `NRestarts` climbing. **Always `daemon-reload` BEFORE `restart`, then verify with `ps aux | grep litellm` that the live command line carries the new port.**
- **Sibling "works" claims need an independent live probe with realistic parameters (2026-08-09).** OpenCode reported "hermes-asi responds ✅" after the outage — its test used tiny `max_tokens`, so the 200 was real but the content was empty. The claim was true at the transport layer and false at the application layer simultaneously. Also its FED explainer listed `dispatch → … MiniMax M3 (order 2)` but the live `litellm-config.yaml` has only 2 dispatch blocks: `mimo-v2.5-pro` (order 1) → `qwen3.8-max` (order 2). **Trust `grep -c 'model_name: dispatch' <config>` + `curl :4000/model/info`, not pasted tables.** Same doctrine as the delegated-subagent rule in `a2a-gateway-protocol`.
- **Don't auto-codify new EMD lanes without F13.** Adding a new lane (e.g., `dream`, `audit`) is a constitutional grammar change. Draft → Arif reviews → "Forge" → patch. Don't auto-expand the matrix.
- **HAProxy :4000 looks DEAD on `/health` but is alive.** HAProxy is a TCP proxy — it has no HTTP `/health` endpoint. `curl :4000/health` returns connection refused or timeout. The correct probe is `ss -tlnp | grep 4000` (check for LISTEN state) or `curl :4000/v1/models -H "Authorization: Bearer $LITELLM_MASTER_KEY"`. False-alarm: port sweep shows "DEAD" but traffic is flowing. Added 2026-08-10.
- **LiteLLM :4011 returns 401 without key — looks dead but is healthy.** Without `LITELLM_MASTER_KEY`, `curl :4011/health` returns HTTP 401. With the key, it returns 200 + full health JSON. The correct probe always includes `-H "Authorization: Bearer $LITELLM_MASTER_KEY"`. False-alarm: "litellm down" when the real issue is missing env var. Added 2026-08-10.
- **Roadmap claims can be stale — always verify against live state.** `FED_UPGRADE_ROADMAP.md` listed "P0.1 LiteLLM revive — Not started" and "P0.2 Capability routing — Partial" but live probes showed both were already complete (LiteLLM healthy, 5 capability signatures built at 18-21ms). Before executing a roadmap, `cat` the source AND probe the ports. Added 2026-08-10.
- **Spend forensics = LiteLLM Postgres, not the proxy admin API (2026-08-15).** When Arif says cost is painful ("pokai bayar token api"), the authoritative spend ledger is Postgres `litellm` DB (`postgresql://arifos_admin@127.0.0.1:5432/litellm`, table `"LiteLLM_SpendLogs"`, time col `"startTime"` — camelCase, NOT `request_time`; check `information_schema.columns` first). The proxy HTTP admin endpoint (`:4000/1/spend/logs`) returns 404 on this setup. Always convert to RM (USD × ~4.2) — RINGGET FRAMING is standing policy; raw tokens are a footnote. Attribution pitfalls: `api_key='litellm_proxy_master_key'` = Hermes gateway (the real bill), `litellm-internal-health-check` = free noise, ignore; `metadata`/`requester_metadata` are empty — attribute via `api_key` + `extract(hour from "startTime")` (UTC; convert `(h+8)%24` for MYT) to tell autonomous 24h burn from human-hours burn; dual routes (`openai/mimo-v2.5` master-key vs `mimo-v2.5` other-key) are the same upstream model — rank by spend, not row count; huge avg tokens/call (mimo ~100k) = long-context agent loops, not runaway users. Added 2026-08-15.
- **MuleRouter key exists but service is dead.** `MULEROUTER_API_KEY` is in kunci-mas.env but `GET /vendors/openai/v1/models` returns 0 models. Do not route production work through MuleRouter until the service recovers. Native MiniMax API (`api.minimax.io`) is the fallback. Added 2026-08-10.
- **FRAME is the third sibling organ — include it in any intelligence-plane placement/coupling evaluation.** FED (allocator, 777_FORGE) and FLAME (free lane, ADVISORY) are not the whole plane. **FRAME** (`frame-organ` :18085) is the Federation Reference & Assessment Measurement Engine — a substrate organ with `OBSERVE_ONLY`/`ADVISORY_ONLY` ceiling that probes all 10 organs and emits reality-drift signals ("drift signal is observation, not verdict"). When asked to evaluate placement/merge/gate scenarios, **score constitutional ceilings FIRST**: any scenario that silently turns FRAME into a routing-governor (closed feedback loop) or an upstream verification gate breaks OBSERVE_ONLY → that is a de-facto **F13 constitutional amendment**, not an ops move. Ranked axes: ceilings → authority separation (least privilege) → blast radius / F1 reversibility → closed-loop value → audit(F11) → isolation(F12/FLAME Zero-Fly-Zone) → cost. To get closed-loop insight WITHOUT granting mutation power, add a **read-only telemetry tap** — surface the observer's drift signals to Arif/arifOS for judgment rather than letting the observer apply them. Full framework + 4-scenario matrix + live truth: `references/organ-placement-evaluation-2026-08-11.md`. Added 2026-08-11.

## Audit evidence (2026-08-08)

| Claim | Evidence |
|---|---|
| FED is the cognitive allocator | `fed_route` signature with `constitutional_tier` and `effort_level` params |
| 666/999 is provider-restricted | `constitutional_rule` in `federation-models.json` |
| FLAME is one of FED's destinations | `FLAME_PRICING` table in `fed_router.py` |
| FED is load-bearing | 9 named aliases (`agi-333`, `asi-555`, `apex-888`, etc.) in `litellm-config.yaml` |
| FED is not dead | `fed-router.service` running since Aug 5, 14 MCP tools |

## Support files

| Path | Purpose |
|---|---|
| `scripts/fed_mcp_probe.py` | Stdlib MCP client — handles SSE unwrap + double-decode. Usage: `python3 scripts/fed_mcp_probe.py fed_status` / `fed_route '{...}'` |
| `references/live-state-2026-08-08.md` | Live baseline snapshot (provider state, health, latency, spend, LiteLLM chains, known issues). Re-probe before SEAL-grade claims. |
| `references/provider-wiring-qwen-individual-2026-08-08.md` | Full provider-wiring recipe (exact SQL, code diffs, failure modes: duplicate rows, phantom alive_pools, balance-gate demotion, effort-dial override). Reuse as template for any new provider. |
| `references/emd-lane-awareness.md` | EMD lane awareness (Fasa 1, 2026-08-08) — capability matrix, agent defaults, 3 mismatch rules, verified 5-case test matrix, effort-override × EMD interaction, revert recipe. |
| `references/qwencloud-individual-plan-2026-08-08.md` | QwenCloud Individual Pro knowledge bank — allowed models (exact-string), pricing tiers, billing mechanism (5hr unlimited/7-day limit), night discount (22:00-08:00 MYT 50% off qwen3.8-max), terms restrictions. Source-of-truth for any future QwenCloud decision. |
| `references/fed-probe-and-fallback-audit-2026-08-08.md` | The 3 recurring audit failure modes: `fed_probe` blind spot (only deepseek probed), token-starvation vs reasoning-loop diagnostic distinction, ghost-fallback audit recipe. Triple-step refresh path for credit-based providers. Load on any "is provider X still alive?" or "why did this call hang?" question. |
| `references/fed-doctor-preflight-2026-08-08.md` | `fed-doctor.sh` and `opencode-fed-preflight.sh` — the two-FED-surface diagnosis, dual-probe recipe, `KEY_MISSING` / `UP` / `DOWN` return shape, and the `~/.bashrc` alias wiring. Load on any "FED failed" from opencode. |
| `references/fed-haproxy-migration-2026-08-09.md` | **Current FED inference topology** (HAProxy :4000 → fed :4011 / escape :4012; legacy shims :4001/:4002). Port-collision crash-loop postmortem, daemon-reload trap, failover validation recipe, dispatch true chain, wiring-audit snapshot. Load before ANY port/service change to FED. |
| `references/fed-swot-benchmark-2026-08-10.md` | Full SWOT analysis + external router benchmark (FED vs OpenRouter vs MuleRouter vs TokenRouter). Composite scoring, capability signature response times, infrastructure state snapshot, roadmap reality check. Load on any "assess FED health" or "compare routers" task. |
| `references/organ-placement-evaluation-2026-08-11.md` | **Constitutional-ceiling-first framework** for evaluating placement/coupling/merge scenarios of the intelligence plane (FED/FLAME/FRAME). 4 canonical scenarios (siblings / FRAME-governor / merge-into-FED / FRAME-gate), ranked scoring axes, charter-safe read-only telemetry tap pattern, FRAME charter + ORGAN_PORTS. Load on any "where should organ X sit / should we merge X and Y / should FRAME gate" question. |

## Related

- `federation-model-routing` — LiteLLM proxy chain, model alias resolution, context window detection
- `federation-infra-verification` — probing federation state against live evidence
- `provider-quota-diagnostics` — diagnosing provider exhaustion and key validity
- `FORGE-model-monitor` — model fallback chain monitoring (overlaps on health-check patterns; FED skill is routing-focused, model-monitor is monitoring-focused)
- `FLAME-router` — free inference lane classification (FLAME is one of FED's routing destinations)