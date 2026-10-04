# Qwen Profile Triage Flow (2026-08-11)

When user reports `qwen3.x-max` returning "rate-limiting" / generic 429 on a
DIRECT provider (not FED), and the model worked before.

## The 3 Qwen keys — same endpoint, different pools

All three keys share Alibaba Cloud Singapore endpoint:
```
https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
```

| Env Var | Key Prefix | Role | Notes |
|---|---|---|---|
| `QWEN_API_KEY` | `sk-sp-H.DIEXP` | Primary chat/completions | Exhausted 2026-08-11 |
| `QWEN_INDIVIDUAL_API_KEY` | `sk-sp-H.DIIYD` | Individual Pro (multimodal) | Alive — part of the $68/mo plan |
| `QWEN_BAILIAN_KEY` | `sk-sp-H.IEHM` | Team/Bailian fallback | Exhausted 2026-08-11 |

**Key insight:** The three keys share ONE credit pool on the portal, but the
*Individual Pro* subscription can be alive while the primary `QWEN_API_KEY`
reports `insufficient_quota` — same physical pool, different key alias
propagation. Probe each key independently; never trust config pointing at one
key to tell you about the others.

## Step 1 — Probe all 3 keys independently

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a

for label in \
  "QWEN_API_KEY|$QWEN_API_KEY" \
  "QWEN_INDIVIDUAL_API_KEY|$QWEN_INDIVIDUAL_API_KEY" \
  "QWEN_BAILIAN_KEY|$QWEN_BAILIAN_KEY"; do
  l="${label%%|*}"; k="${label#*|}"
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 "$QWEN_BASE_URL/chat/completions" \
    -H "Authorization: Bearer $k" -H "Content-Type: application/json" \
    -d '{"model":"qwen3.6-flash","messages":[{"role":"user","content":"hi"}],"max_tokens":5}')
  echo "$l → HTTP $code"
done
```

**Expected output patterns:**

| Pattern | Meaning | Action |
|---|---|---|
| ALL 3 → 429 `insufficient_quota` | Shared pool exhausted | Portal reset / wait 7d window |
| QWEN_API_KEY 429 + INDIVIDUAL 200 | **Config points to dead key** | Patch config `key_env:` (this session 2026-08-11) |
| All 200 but model still fails | Model ID mismatch / wrong base URL | Check key roster via `/v1/models` |

## Step 2 — Confirm where the profile's config points

```bash
grep -n 'key_env' /root/.hermes/profiles/<profile>/config.yaml
```

The custom provider block (e.g. `bailian-token-plan`) reads exactly ONE env var
via `key_env:`. If that var holds an exhausted key, the profile fails even
though the endpoint and other keys are healthy.

All three working profiles (hermes_asi, hermes_apex, hermes_forge) had:
```yaml
bailian-token-plan:
    api: https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    key_env: QWEN_API_KEY        # ← exhausted
```

## Step 3 — Patch (reversible)

```bash
# backup first — always
for p in hermes_asi hermes_apex hermes_forge; do
  f=/root/.hermes/profiles/$p/config.yaml
  cp "$f" "$f.bak-$(date +%Y%m%d-%H%M%S)"
  sed -i 's|key_env: QWEN_API_KEY|key_env: QWEN_INDIVIDUAL_API_KEY|' "$f"
done

# validate YAML
for p in hermes_asi hermes_apex hermes_forge; do
  python3 -c "import yaml; yaml.safe_load(open('/root/.hermes/profiles/$p/config.yaml'))" && echo "✅ $p valid"
done
```

## Step 4 — Verify the EXACT model on the new key

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -s --max-time 30 "$QWEN_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $QWEN_INDIVIDUAL_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen3.7-max","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

`qwen3.7-max` confirmed 200 on Individual Pro (2026-08-11). Use `max_tokens>=10`
for Max family (reasoning budget), not 1.

## Step 5 — User must start a NEW session

**Hermes reads `config.yaml` at boot.** The old session holds the cached key in
memory. A fresh chat / `hermes new` picks up the patched `key_env:`. This is the
most common "I patched but it still fails" confusion.

## The "rate-limiting" wrapper trap

Hermes wraps Qwen's `insufficient_quota` behind a generic
"model provider is rate-limiting requests" message. Users read "rate-limiting"
and assume a temporary RPM throttle (wait seconds). Reality: `insufficient_quota`
= credits exhausted (wait hours / portal action). **Always read the error code
field, not the user-facing message.** Same HTTP 429, two opposite root causes:

| Error code | Meaning | Recovery |
|---|---|---|
| `insufficient_quota` | credits gone | portal reset / wait window |
| `Rate limit exceeded` | transient throttle | wait seconds, retry |

## DASHSCOPE_API_KEY ≠ QWEN keys

The built-in Hermes plugin `alibaba` reads `DASHSCOPE_API_KEY` (prefix
`sk-ws-H.`), a DIFFERENT key on a possibly different plan (PAYG vs Token Plan).
It is NOT one of the three Qwen token-plan keys. It returns 401 on the
token-plan endpoint and 200 on the dashscope endpoint. Do not conflate them —
each lives in its own env var and own pool.

## Related

- Post-reset full sweep (3 keys × 7 models): `provider-quota-diagnostics` SKILL.md → "Post-reset verification recipe"
- FED cascade wiring for Qwen Individual Pro: `references/qwen-token-plan-quota.md`