---
name: litellm-proxy-triage
id: litellm-proxy-triage
version: 1.0.0
description: Use when LiteLLM throws errors or hangs — disambiguate upstream vs stale proxy before restarting.
owner: A-FORGE
risk_tier: medium
autonomy_tier: T2
floor_scope: [F1, F2, F3, F4, F8, F11]
tags: [litellm, proxy, federation, fed, context-window, rate-limit, triage, systemd, ipv4]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# LiteLLM Proxy Triage

> **The user-visible error class rarely matches the actual failure mode.**
> "Rate limited" is often a stale proxy. "Context window exceeded" is
> often session bloat, not model size. Disambiguate BEFORE restarting.

## When to Use

- The federation is throwing `ContextWindowExceededError`, `RateLimitError`, `BadRequestError`, or cascading `Timeout exceeded` errors from `:4011` / `:4000`.
- A-FORGE / agent calls hang or fail without obvious cause.
- The user says "vps kena rate limited lagi" or similar — instinct is to refresh, but the actual cause is usually upstream of the proxy.
- `healthy_count: 0, unhealthy_count: 158` in `/health` — looks like all providers down, but rarely is.
- litellm-federation was restarted outside systemd (e.g. from Termux bash) and fed-watchdog is no longer effective.

## When NOT to Use

- Single MCP or organ failure (use `federation-health` for Docker, organ-specific skills for others).
- Provider-side issues confirmed upstream (use provider's own status page).
- Authentication or billing issues (Arif must renew seats, not in T2 scope).

## §1. ERROR → ACTUAL CAUSE MAP

| User-visible error | Common reflex diagnosis | What it actually often is |
|---|---|---|
| `ContextWindowExceededError` | "model too small, switch model" | Session accumulated >100k tokens (bloat). Truncation, not model swap. |
| `RateLimitError` / HTTP 429 | "provider rate limit" | Quota exhausted (per-day/per-week window), OR upstream outage, OR key invalid. |
| `BadRequestError` / HTTP 400 | "malformed request" | Key revoked, model name typo, context window exceeded re-cast as 400. |
| `AuthenticationError` / HTTP 401 | "key expired" | Key rotation needed, OR wrong `api_base` (e.g. direct Moonshot key against a Qwen endpoint). |
| Cascade hangs / `Timeout exceeded` | "provider slow" | LiteLLM proxy itself stale (started before upstream came back); restart needed. |
| FED :4000 down / 503, restart loop | "HAProxy or Headscale down" | Boot crash-loop: `prisma migrate deploy` hangs → systemd restarts forever. `journalctl -u litellm-federation \| grep -c prisma` = hundreds. Bridge: disable `database_url` (stateless boot); real fix: run migrations outside boot. See `references/2026-09-01-prisma-boot-crashloop.md`. |
| `healthy_count: 0, unhealthy_count: 158` | "all providers down" | More often: litellm started when upstream was flapping, never recovered; restart clears it. |
| haproxy `:4000` → 503 "No server available"; remote probes see `http_code=000` / 0 bytes / timeout | "network hang / haproxy deadlock / both nodes down" | **Backend litellm hung with port still bound.** Process alive, listener present, but backend HTTP never answers; haproxy `fall 5` marks it down. `ss -tlnp` proves NOTHING — curl the backend port (`:4013`) directly. See `references/2026-09-02-litellm-hung-backend.md`. |
| A whole lane silently answers as a *different* model | "litellm is misrouting / fallbacks are broken" | **The lane's body is quota-dead and it fell through to its first fallback.** Read the `model` field of the response, not the HTTP code — HTTP 200 tells you nothing about *who* answered. 2026-09-15: 7/7 probes of lane `i-arif` (Hermes's live primary) returned `"model": "deepseek-flash"` because all 7 of its deployments ride quota-dead seats. Also: identical prompts are served from the litellm **Redis response cache** (`namespace litellm-fed`, ttl 1800) — add a per-request nonce or every probe row is garbage. |
| `haproxy -c` on a config that is *clearly* running | — | **A dead-on-arrival config file plus a live process is normal here, not a contradiction.** The worker keeps its in-memory config; the file on disk can be invalid for days. Always run `haproxy -c -f /etc/haproxy/haproxy.cfg` and compare the file's mtime with the worker's `lstart`. 2026-09-15: the file had `use-server`/`server` inside `frontend fed_gateway` (`ALERT: … has no backend capability`), written 1 minute *after* the worker started — so any restart would have taken `:4000` and `:4012` down. |

## §1b. THE TWO GATEWAYS — HAProxy SITS IN FRONT OF LITELLM

`:4013` is the **litellm backend**. `:4000` and `:4012` are **HAProxy frontends**. They fail
independently and they can answer with *different truths about the same model id*. Never treat a
`:4000` result as evidence about `:4013`, or vice versa.

Measured 2026-09-15: `:4000/v1/models` returned KVM4's **47**-model set 6/6 samples while `:4013`
returned **45**. The discriminator is a model id that exists on only one node — `codestral-latest`
returned `402 MistralException: Check your subscription` through `:4000` (real KVM4 deployment) and
`400 Invalid model name` through `:4013`.

| Signal | What it means | Action |
|---|---|---|
| `:4000` answers, but with a model set you don't expect | HAProxy is bound to a *different* node than you assume | `haproxy -c -f /etc/haproxy/haproxy.cfg`, then `curl :<backend_port>/v1/models` directly and md5 both id-sets |
| `haproxy -c` prints `'server' not allowed because frontend 'X' has no backend capability` | Backend-only directives (`server`, `use-server`, `option httpchk`, `http-check`) were written **inside a `frontend` block** | **Fatals.** The file cannot be loaded — the running process is serving an older in-memory config. A reload/restart/**reboot** takes the gateway DOWN. Repair before anything else. |
| `systemctl reload haproxy` fails or changes nothing | the on-disk file is invalid; reload aborts | compare file mtime vs process start time — they will disagree |
| a caller's own `Authorization` header has no effect on routing | the frontend injects the master key **unconditionally**, overwriting the caller's key | if the intent was auth-*conditional* routing, note that `use-server ... if { req.hdr(authorization) -m found }` placed **after** the injecting `set-header` is always true — frontend `http-request` rules run in order |
| an `Authorization "Bearer sk-...xxxx"` literal in the config looks truncated | a masking pass wrote a **masked value** into a live config — the real key is lost | recover from the golden snapshot (`/etc/haproxy/fed-auth.cfg`, 0600), prove it with a 200 probe against **both** nodes, then install. Check every backup: full keys there, truncated here, means the break is new. |
| a rotation/regen script exists but the key never changes | its regex cannot match a truncated literal, or it rewrites only the first of several bearer literals | see §5a — a stale `http-check` bearer marks the primary DOWN and **silently** shifts traffic to the backup |

**Rule: three states, always check all three.** (1) the file on disk, (2) the config the running
process actually loaded (compare mtime vs `lstart`), (3) what each node answers right now.
A valid-looking file plus a previously-loaded process is the normal shape of a silent gateway defect.

## §1b. LIVE QUOTA REALITY — PROBED 2026-09-15 (KVM8)

> **In this federation, a model failure is almost never an auth failure.** A sweep of every
> provider base URL in `model_list` (1-token probes, exact `api_base` values) returned
> **zero 401s**. Every failure was 402/403/429 quota or billing. Mapping "model failed" to
> "key expired" here will trigger four wrong renewals.

| Provider | Live answer | Body (truncated) |
|---|---|---|
| Qwen token-plan ×4 seats | 429 | `insufficient_quota` — "Your token-plan quota has been exhausted." (INDIVIDUAL: "1-week quota … reset at 09-18 04:10:00 UTC") |
| DashScope + `QWEN_PAYG` | 403 | `AllocationQuota.FreeTierOnly` — "The free quota has been exhausted … complete your payment information" |
| Z.ai coding plan | 429 | `{"code":"1310","message":"Weekly/Monthly Limit Exhausted…"}` |
| Z.ai `/api/paas/v4` | 429 | `{"code":"1113","message":"Insufficient balance or no resource package."}` |
| Kimi `api.kimi.com/coding/v1` | 403 | `access_terminated_error` — "monthly usage limit for this billing cycle" |
| OpenCode Go `/zen/go/v1` | 429 | `GoUsageLimitError` — "Weekly usage limit reached. Resets in 6 days." |
| Gemini | 429 | "Your prepayment credits are depleted." — **NOT a dead key** |
| MiniMax · DeepSeek · MiMo (SGP) · SEA-LION | **200** | only four live upstreams out of 114 deployments |

**Two traps this sweep corrected in its own author — both were near-miss false negatives:**
probe the `api_base` **exactly as written in the config**, never a hand-typed neighbouring
path. `api.kimi.com/v1` and `opencode.ai/zen/v1` both return nginx/handler 404s and look
like "misconfigured base URL"; the real values are `api.kimi.com/coding/v1` and
`opencode.ai/zen/go/v1`, and both are quota-dead (403/429), not misrouted.

**Sample ≥3 times before judging a lane.** `QWEN_INDIVIDUAL` answered 429 "1-week quota
exhausted, resets 09-18" at 01:42, **200 `qwen3.8-max`** at 01:52, then timed out 3 of 4
follows at 30 s. A single sample is worthless in both directions.

**MiniMax has two independent quota pools** — never average them:
```
mmx quota show --base-url https://api.minimax.io
  pool=general  interval=0/0  remain%=57  weekly week%=87
  pool=video    interval=3/3  remain%=0   weekly week%=21 -> 85%
```
`video` can read "0 % this interval" and still admit a job (the weekly bucket covers it),
so "interval exhausted" ≠ "cannot generate". Known model-level limit:
`MiniMax-H3` → `2013 TokenPlan or Credit does not currently support MiniMax-H3 series`
(HTTP 400) while `MiniMax-Hailuo-2.3` is admitted.

**Runnable probes (re-runnable, tiny requests, no mutations):**
```bash
/root/forge_work/harden-20260915/model/probe-providers.sh   providers.jsonl
/root/forge_work/harden-20260915/model/probe-model-layer.sh --jsonl lanes.jsonl
```
The lane probe sends a **per-model nonce** because litellm response cache is ON
(Redis, namespace `litellm-fed`, ttl 1800). Without it, four different lanes all report the
same `mimo-v2.5` reply at 69 ms with one shared response id — cache, not routing.

## §2. DISAMBIGUATION PROBE — Run Before Restarting Anything

> **2026-09-15 correction — probe the base URL the config actually uses, and read the body.**
> Two lanes were wrongly declared dead by probing the wrong path: `api.kimi.com/v1` returns a bare
> nginx **404** while the real path is `/coding/v1`; `opencode.ai/zen/v1` returns
> `401 Model X is not supported` while the real path is `/zen/go/v1`. The litellm config already had
> both right. A 404-nginx body and a 401-not-supported body are **path errors, not outages**.
> Before mutating anything, grep the lane's `api_base` out of the config and probe *that* string.

```bash
source /root/.secrets/kunci-root.env

for spec in \
  "MINIMAX_API_KEY:https://api.minimax.io/v1/chat/completions:MiniMax-M3" \
  "DASHSCOPE_API_KEY:https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions:qwen3.7-flash" \
  "QWEN_INDIVIDUAL_API_KEY:https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions:qwen3.8-max" \
  "GEMINI_API_KEY:https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent:GEMINI"; do
  KEY="${spec%%:*}"; rest="${spec#*:}"
  URL="${rest%%:*}"; MODEL="${rest#*:}"
  V="${!KEY}"
  [ -z "$V" ] && echo "$KEY MISSING" && continue
  if [ "$MODEL" = "GEMINI" ]; then
    code=$(curl -4 -s -o /dev/null -w "%{http_code}" --max-time 15 \
      "${URL}?key=$V" -H "Content-Type: application/json" \
      -d '{"contents":[{"parts":[{"text":"reply PONG"}]}],"generationConfig":{"maxOutputTokens":10}}')
  else
    code=$(curl -4 -s -o /dev/null -w "%{http_code}" --max-time 15 \
      "$URL" -H "Authorization: Bearer $V" -H "Content-Type: application/json" \
      -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"reply PONG\"}],\"max_tokens\":10}")
  fi
  echo "$KEY ($MODEL) http=$code"
done
```

**Read the result:**
- All `200` → upstream is fine. **Restart `litellm-federation` via systemd.** Proxy is stale.
- Mix of 200 / timeout / 401 → failing ones are the actual problem. Fix keys or wait for quota.
- All failing → provider outage OR VPS IPv4 network issue. Check `curl -4 -sv --max-time 5 https://1.1.1.1`.

## §3. CONTEXT OVERFLOW VS QUOTA VS OUTAGE — DECISION TREE

```
Error mentions "Context Window"?
  → Check session token count. If >100k, session is bloated.
    Restart the A-FORGE session; do NOT swap models.
    Verify router_settings.context_window_fallbacks routes to a 1M-ctx model
    (Gemini 2.5 Pro, qwen3.8-max Team Owner, kimi-k3, MiniMax-M3).

Error mentions "Rate Limit" / 429?
  → Probe upstream directly (§2).
    Quota exhausted: wait for window reset OR switch seat.
    Outage: stay on healthiest provider, alert user.

Error is generic BadRequest / 400?
  → Check the model_id is in `model_list`. Check key not revoked.

Cascade: many models failing with Timeout exceeded?
  → litellm-federation is stale. Restart systemd (§5).
```

## §4. WHY IPv4 SPECIFICALLY

The arifOS VPS frequently has IPv6 flap on provider APIs (observed 2026-08-27:
`curl` default timed out, `curl -4` succeeded in <1s). When probing provider
health, **always use `curl -4`** to force IPv4. Without it, you can falsely
conclude "all providers down" when they're all fine.

## §5. RESTART DISCIPLINE — Don't Create Orphans

```bash
# ✅ CORRECT — via systemd, fed-watchdog will catch failures
systemctl restart litellm-federation litellm-escape
systemctl status litellm-federation   # verify Active: active

# ❌ WRONG — orphans the process, fed-watchdog can't recover it
nohup litellm --config /root/A-FORGE/litellm-config.yaml --port 4011 &
bash -c 'sleep 2 && litellm ...'
```

After Termux-orphan detected (`ps aux | grep litellm` shows process outside systemd tree):

```bash
kill <orphan_pid>
systemctl restart litellm-federation
ss -tlnp | grep ':4011'   # verify systemd-owned process is listening
```

## §5a. ONE KEY, SEVERAL LITERALS — the silent-failover trap

The master key appears in **more than one place** in the gateway config:

```
http-request set-header Authorization "Bearer <KEY>"     <- what upstream sees
http-check send hdr Authorization "Bearer <KEY>"         <- what the health check sends
```

A rotation script doing `re.subn(..., count=1)` rewrites the first and leaves the second on the
**old key**. The consequence is not an error message: the health check starts failing, HAProxy marks
the **primary** node DOWN after `fall x inter`, and traffic **silently** shifts to the backup — a
latency and topology change with no 4xx anywhere. Verified defect in
`/root/scripts/haproxy-auth-regen.sh` on 2026-09-15.

**Requirements for any auth-regen tool:**
1. replace **all** bearer literals, and print how many it replaced;
2. match a *truncated/masked* literal instead of dying on it (`[0-9a-zA-Z_-]+` cannot match `sk-lit...c8ac`);
3. run `haproxy -c` **before** installing, not after;
4. probe the candidate key against **every** node it will be used on and require 200 before writing it;
5. be dry-run by default; reload only behind an explicit `--apply`;
6. back up, and restore automatically if post-install validation fails.
Reload only after all six.

## §6. PITFALLS

- ❌ Reflexively restarting on every error — masks the actual cause and resets upstream health-check probes that were about to recover.
- ❌ Believing the litellm `/health` output at face value — `healthy_count: 0` after a startup during upstream flap means stale, not actually down.
- ❌ Editing `litellm-config.yaml` without backing up first — keep `*.bak-<UTC-timestamp>` snapshot.
- ❌ Adding new `model_list` entries for the same provider without a clear `order:` — they race and waste quota.
- ❌ Removing `context_window_fallbacks` entries thinking "simpler is better" — this is what prevents cascade hangs.
- ❌ Starting litellm from Termux `bash -c "litellm ..."` to "fix it fast" — orphans the process; fed-watchdog will never recover the next failure.
- ❌ **Python 3.13 import hang** — litellm 1.90.2 hangs indefinitely on `import litellm` with Python 3.13.7. Process starts, consumes CPU/RAM, but never binds to port. Diagnose: `timeout 10 python3 -c "import litellm"` — if no output, this is the issue. Do NOT restart repeatedly — the import itself is broken. Fix: upgrade litellm or downgrade Python. See `references/2026-08-28-litellm-python313-hang.md`.
- ❌ **Trusting the base systemd unit** — `litellm-federation.service` has drop-ins in `/etc/systemd/system/litellm-federation.service.d/` that override ExecStart (port, host, env). Always `systemctl cat litellm-federation.service` (shows merged unit), never read the base unit alone.
- ❌ One tailnet curl timeout = declaring a node down — retry with `-m 20` first; tailnet handshakes can eat the first attempt (2026-09-01: first curl timed out, retry 2s later succeeded).
- ❌ Chasing `PrometheusLogger` `'litellm_requests_metric'` journal spam mid-incident — non-blocking, routing unaffected; defer to maintenance window.
- ❌ **Trusting `ss -tlnp` LISTEN as health** — a hung litellm keeps the port bound while never answering HTTP. Probe the backend with `curl -m 8 http://127.0.0.1:<backend_port>/health/liveliness`; high `etime` + 50-60% CPU + no HTTP = stuck loop. If TERM is ignored, SIGKILL and let fed-watchdog restart it — never race the watchdog by spawning your own. Then wait out haproxy `rise 2 × inter 5s` (~15s) before judging :4000. (2026-09-02 incident: remote nodes read it as network hang; full recipe in `references/2026-09-02-litellm-hung-backend.md`.)
- ❌ **Acting on another agent session's state report without re-probing** — parallel sessions hold stale views (2026-09-02: one reported "gateway FAILED + state.db corrupt"; direct probe showed both healthy). `systemctl status` + `sqlite3 <db> 'PRAGMA quick_check;'` are one command each. Also mask tokens when reading unit env (`sed "s/=.\{6\}/=***MASKED/"`) — `/proc/PID/environ` and `systemctl show -p Environment` emit full secrets.
- ❌ **Health-probing a tailnet peer with the heavy `/health` endpoint** — `/health` returns a ~13KB model list and can time out on a degraded Tailscale path while the service is fine; `/health/liveliness` returns 12 bytes and answers in ms on the SAME path. Before declaring a FED peer down: re-probe with liveliness, retry 3×, and from more than one vantage point. A remote monitor's alert ("FED UNREACHABLE") is a hypothesis, not a verdict (2026-09-03: pulse alert fired on a transient direct↔DERP route flip while three direct probes returned 200 <100ms; next pulse cycle logged HEALTHY with zero changes). Durable fix for flapping monitors: point them at `/health/liveliness` and suppress single-cycle failures — not infra restarts.
- ❌ **Trusting a config note that says live / active / resubscribed / GO-LIVE** — notes rot silently while the seat dies (subscription lapses, quota window rolls over). A note is a CLAIM; only the provider's own endpoint is evidence. Probe each lane's key against its own base URL and read BOTH code and body: `402` = dead subscription, `429` = quota window (the body carries the reset timestamp — record it), `401` = key. Then fix the NOTE too, not just the chain, or the same lie re-grows next month. Corollary: count the residue after any purge (`grep -c mistral|glm-5.3`) — a claim of removal is not a removal, and residue hides in SUB-chains (nested fallback lists like `mimo-v2.5 -> MiniMax-M3 -> gemini -> glm-5.3`), not just the top-level lane fallbacks. Grep the WHOLE file and trust the count over your own "I removed it" memory — a 2026-09-14 purge reported `glm-5.3 = 0` while 3 refs still sat in mimo-v2.5 / kimi-k3 / glm-5.2 sub-chains.
- ❌ **Reordering only the `fallbacks:` list and calling a lane "live-first"** — a lane's own `model_list` deployments (its `order:` rungs) are tried BEFORE its `fallbacks:` entry. If a lane's own deployments are dead-first, it still churns every dead rung on every message even after fallbacks are fixed. Check the lane's deployment `order:` values, not just the fallback block; the cheap fix is giving the live model the lowest `order:`. Corollary: `model_name` ↔ upstream `model` are different namespaces — `model: openai/deepseek-v4-pro` needs both a registered `model_name` AND a valid upstream id; a fallback entry naming an unregistered `model_name` is a dangling rung that fails silently to the next.
- ❌ **Reading `/proc/PID/environ` as the gateway's effective auth config** — hermes resolves Telegram auth via `get_env_value_prefer_dotenv`, i.e. the `.env` in the service `WorkingDirectory` wins over the systemd `EnvironmentFile`. `/proc/environ` (exec-time only) can therefore show one list populated and another absent while the running process actually reads both from `.env`. Check BOTH the unit's `EnvironmentFile` and the working-dir `.env`, and probe names only — never echo the values, those files hold live bot tokens and API keys.
- ❌ **Allowlisting a chat/user ID handed to you as "Farhan" without confirming the person** — the log prints the account's own display name next to the ID (`Unauthorized user: <id> (<Display Name>)`). If that name does not match who you were told it is, verify before trusting the allowlist; an ID is a handle, not an identity.

- ❌ **A `docker run --rm` with no `--name` mints a fresh random name every restart** (crazy_chatelet → awesome_jones → interesting_satoshi) — same service, unrecognizable name, so a peer agent can misread it as a "new/redundant" container and kill a live backend (2026-09-14: Qwen killed KVM8 litellm :4013 as "redundant", taking Hermes's backend down). Always add `--name <service-name>` (== systemd unit name) to docker run in a unit so `docker ps` is self-identifying.

## §7. FED CONFIG STRUCTURE — LANE ≠ MODEL (Zen-FED doctrine, 888-sealed 2026-09-02)

**Canonical order: Capability → Organ → Tool → Skill. A model is tool substrate, never a governance layer.** i-arif / agi-333 / asi-555 / forge-777 / apex-888 / fed/vision are alias LANES (organs), each backed by many provider deployments. One vendor model may legitimately serve multiple lanes. Orthogonalize ROLE / AUTHORITY / CAPABILITY — never vendor models.

Rules before proposing any config mutation ("zen", trim, dedupe):

1. **Probe first — evidence before proposals.** A plan-only reply ("I will scan / I will trim...") is not a deliverable; 888 verdict 2026-09-02 held it as PARTIAL ("niat/pelan, bukan bukti pelaksanaan"). Measure processes, ports, config census, steal-time FIRST, then present findings + graded proposals. The 3-call probe recipe: `references/2026-09-02-fed-config-anatomy.md`.
2. **Inventory Before Mutation:** Discover → Classify → Measure usage → Identify overlap → Decide retirement → **Archive** (registry JSON: model, alias, last_verified, reason) → Remove. Never propose deletion as a first step.
3. **Alias deployment counts look chaotic but are intentional** — agi-333 ~40 deployments, hermes-asi-vision ~21, fed/vision ~21, i-arif ~17, asi-555 ~12, apex-888 ~10, forge-777 ~9 (~152 entries, 2026-09-02). Real rot classes: dead date-snapshots (qwen3.7-max-2026-05-XX) and commented-out blocks — they waste router bookkeeping/cooldown tracking.
4. **Decide model selection fast** (Arif: "jangan fikir sangat model nak pilih apa lama2"). No deliberation theater: flash-class models shuffle in the pool, max/pro models called by explicit name. Present one recommendation, one binary ask.
5. Known gap as of 2026-09-02: **zero embedding/rerank entries** in the config — 999-ARCHIVE lane has no retrieval substrate; plan = a fed/embed alias via DASHSCOPE PAYG (tongyi-embedding-vision-plus + qwen3-rerank are NOT on the Token Plan allowlist). Token Plan base URL `https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` verified correct (58 entries, api_key via env, never hardcoded).

## §8. RELATED FILES

- `references/litellm-fallback-chain.md` — current fallback chain layout, 1M-ctx anchor models, and apex-888 entry shape.
- `references/2026-09-02-litellm-hung-backend.md` — port-bound-but-hung backend → haproxy 503 read remotely as `000/timeout`; diagnosis order, watchdog-owned kill/restart, dual-gateway token HOLD state.
- `references/2026-09-02-fed-config-anatomy.md` — measured config census (alias lanes, dead snapshots), 3-call probe recipe, Zen-FED proposal shapes P1/P2/P3.
- `references/2026-09-03-wawa-pulse-false-alarm.md` — cross-node monitor false alarm: Tailscale direct↔DERP route flip + heavy `/health` (13KB) vs liveliness (12B); persistent-conn-passes/fresh-conn-fails signature; why DERP-only and MTU changes were wrong fixes.
- `scripts/litellm-upstream-probe.sh` — copy of §2 probe, runnable as-is.
- `references/2026-08-27-incident.md` — case study: ContextWindowExceeded misdiagnosed as rate-limit, real cause was Termux-orphan + 131k-cap fallback chain.
- `references/2026-09-15-model-layer-hardening.md` — full model-layer census 2026-09-15: provider reachability matrix, quota-vs-payment-vs-auth disambiguation, dangling-rung log signature, recursive-fallback semantics, the invalid-gateway repair, and the re-runnable probes.
- `references/litellm-fallback-chain.md` — chain layout, 1M-ctx anchors, apex-888 entry shape.

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Restart does not restore health | arifOS 888_JUDGE + Arif | 888 HOLD |
| Quota exhaustion confirmed (not transient) | Arif — seat renewal required | alert with seat list + remaining % |
| Provider outage confirmed upstream | Arif — decision: switch seats or wait | status report |
| Context overflow persists after fallback chain fix | A-FORGE — session accumulation analysis | structured handoff |