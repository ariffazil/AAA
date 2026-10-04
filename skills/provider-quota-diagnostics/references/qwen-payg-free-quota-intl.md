# Qwen PAYG Free Quota — Model Studio Singapore (intl endpoint)

Knowledge bank for the **general pay-as-you-go** Qwen/DashScope path — the FREE tier.
Distinct from Qwen Token Plan (dedicated `sk-sp-H.*` keys) which never touches free quota.

## Two DashScope endpoints — pick by region, not by habit

| Endpoint | Region | Free quota? | Notes |
|---|---|---|---|
| `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | Singapore (International) | ✅ YES | This is the one with free quota |
| `https://dashscope.aliyuncs.com/compatible-mode/v1` | China (Beijing) | ❌ No (SG-only benefit) | Wrong endpoint = no free quota |

**Critical gotcha:** A PAYG key can return **401 on one endpoint and 200 on the other**.
Observed 2026-08-11: `DASHSCOPE_API_KEY` (prefix `sk-ws-H…`) →
- `dashscope.aliyuncs.com/compatible-mode/v1` → **401 invalid_api_key**
- `dashscope-intl.aliyuncs.com/compatible-mode/v1` → **200, 157 models**

So a 401 on Qwen PAYG does NOT always mean the key is dead — it often means the
config points at the wrong regional endpoint. **Probe BOTH endpoints before declaring a key revoked.**

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
for base in https://dashscope.aliyuncs.com https://dashscope-intl.aliyuncs.com; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 "$base/compatible-mode/v1/models" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY")
  echo "$base/compatible-mode/v1 → HTTP $code"
done
```

## Key types — only general PAYG keys consume free quota

| Key type | Prefix | Consumes free quota? |
|---|---|---|
| General PAYG (Model Studio) | `sk-ws-…` / `sk-…` | ✅ YES — draws from free quota |
| Token Plan dedicated | `sk-sp-H.DIEXP / DIIYD / IEHM` | ❌ NO — never touches free quota |
| Coding Plan dedicated | — | ❌ NO — never touches free quota |

**The same API key calls all models.** Deduction priority is automatic:
`free quota → resource plan → savings plan → pay-as-you-go`. No manual switching.

## Free-quota mechanics (per the docs)

- **Per-model independence:** each model has its OWN free quota (typically 1,000,000 tokens).
  Quota cannot be merged or transferred between models.
- **Snapshot versions count separately:** `qwen3.7-max-2026-05-17` and `qwen3.7-max`
  are two independent models, each with its own quota.
- **No automatic rollover:** when one model's quota runs out, the system does NOT
  switch to another model that still has quota — you must change the `model` param.
- **Validity:** 30–90 days from activation / model release / approval (whichever is later).
  Countdown is NOT paused by inactivity. Expired quota is voided, not reissued.
- **Shared across RAM users:** one Alibaba Cloud account + its RAM users share a single quota.
- **Combined input+output:** the displayed remaining is one shared total, not tracked separately.
- **Scope:** real-time inference only. Does NOT cover batch, fine-tuning, deployment,
  custom models, PAI-DSW, or OSS fees.

## Free Quota Only (worry-free mode)

When enabled and quota is exhausted → service stops with error code
`AllocationQuota.FreeTierOnly` (HTTP 403). This is the PAYG analogue of token-plan
`insufficient_quota` (429) — different status code, same "quota gone" meaning.
Enable per-model or batch on the console Free Quota tab. Setting changes take ~minutes
to propagate, so don't hammer calls immediately after toggling.

## Wiring into Hermes / FED

**Direct provider** (in each `~/.hermes/profiles/<p>/config.yaml`):
```yaml
alibaba-intl:
  api: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
  key_env: DASHSCOPE_API_KEY
  transport: openai_chat
  models:
    - id: qwen3-max
    - id: qwen-plus
    - id: qwen-turbo
    - id: qwen-coder-plus
    - id: qwen-vl-plus
```

**FED / LiteLLM:** add a route tier under the target alias in
`/root/A-FORGE/litellm-config.yaml` with `api_base` = the intl endpoint and
`api_key: os.environ/DASHSCOPE_API_KEY`. Restart `litellm-federation`.

## The 402 non-fallback + gateway delivery pitfall (observed 2026-08-11)

When the Hermes gateway is pointed at FED and the alias's tiers are all credit-dead:
```
ERROR agent.conversation_loop: Non-retryable client error: Error code: 402 -
{'error': {'message': 'litellm.BadRequestError: OpenAIException - Insufficient Balance.
Received Model Group=hermes-asi\nAvailable Model Group Fallbacks=None', 'code': '402'}}
```
LiteLLM treats 402 as a client error → no cascade fallback. The agent surfaces
"⚠️ The model provider failed after retries."

**Second-order trap:** the gateway then fails to deliver that error over Telegram with
`Forbidden: the bot can't send messages to the bot` when the requester is itself a bot
account in a bot-populated group. So the user sees a bare "failed after retries" with
no detail. When diagnosing, pull the real cause from
`journalctl -u <hermes-gateway-unit>` — NOT from the chat surface.

## Diagnosis decision tree

```
401 on Qwen PAYG key
  └─ probe intl endpoint too → 200? key is FINE, config points at wrong region
403 AllocationQuota.FreeTierOnly
  └─ free quota exhausted AND Free-Quota-Only enabled → wait/reset or complete account info
429 insufficient_quota
  └─ that's a TOKEN-PLAN key, not PAYG → see qwen-token-plan-quota.md
402 Insufficient Balance (FED alias)
  └─ LiteLLM won't fall back → demote dead tier order:99, promote alive, restart
```

---

## GitHub FRAME repo — why it says "Not Found"

**Symptom:** Searching `github.com/ariffazil/FRAME` returns 404 in browser/API, user assumes repo doesn't exist.

**Reality:** Repo EXISTS at `git@github.com:ariffazil/FRAME.git`, authenticated clone works, commit history visible. **Private repository** — requires auth token to access via API or HTTPS URLs. Public interface shows nothing.

**Pattern recognition:** When searching for any `ariffazil/ORGAN_NAME` repo and getting 404:
1. Check if it's in federation organs.yaml (`source_path: /root/<ORGAN>/`)
2. Try `ls -la /root/<ORGAN>` — if directory exists, it's likely private
3. Don't assume missing just because public search fails

**Resolution:** For private repos, always use SSH URL (`git@github.com:...`) or cached local copy. Don't rely on public discovery.

---

## Memory pressure handling: Page cache drop before earlyoom kill (2026-08-11)

**Situation:** Earlyoom near trigger point (mem <10%, swap <5%). Heavy processes like opencode would be killed if allowed to reach critical state.

**Principle:** Never kill active worker unless absolutely necessary. Drop kernel page cache instead — reversible, zero data loss, non-destruction action.

**Recipe:**
```bash
# Check current state
free -m

# Flush dirty pages first (critical for safety)
sync

# Drop caches (safe, kernel refills as needed)
echo 3 > /proc/sys/vm/drop_caches

# Verify RAM freed
free -m

# Confirm no kills happened
journalctl -u earlyoom --since "30 min ago" | grep -icE 'kill|oom|SIGTERM'  # should be 0
```

**Why this works:** Cache is reclaimable memory not currently used by applications. Dropping increases available RAM without touching working sets. Kernel refills from disk automatically based on LRU policy.

**When to escalate:** If drop_caches doesn't recover mem above ~15% AND swap below 20%, then consider:
1. Kill idle processes first (low CPU opencode sessions, duplicates)
2. Add temporary swap space via file-backed swap
3. Restart high-memory processes strategically (not random kill)

**Never do:** Repeated `swapoff`/`swapon` — fragments swap device, causes performance issues over time. Prefer cache drop + selective process management.

---

## Additional Pitfalls Section Header

For consistency, ensure all skill entries have proper formatting under a new "Pitfalls" header section. This maintains structure across multi-topic skills.
