---
name: federation-seat-wiring
description: "Wire a new provider/API-key seat into the arifOS federation so all 3 layers (LiteLLM proxy, Hermes config, OpenCode/OpenClaw agents) can reach it. Covers the 3-layer config topology, the safe-patch recipe, JSON round-trip silent drops, system_fingerprint verification, and rollback discipline. Also covers warga-organ provisioning (giving a new agent constitutional identity — DID + key + organs.yaml + SCT). Trigger: 'wire X into FED', 'add Qwen seat', 'make agent use new key', 'cascade through new provider', 'opencode not using my new key', 'retire provider', 'remove dead key', 'unwire X', 'purge Tavily', 'clean up dead provider', 'provision warga', 'add new organ', 'warga identity', 'constitutional citizen', or any time a model/provider/key/org needs to be added to OR removed from the federation."
tags: [wiring, federation, litellm, opencode, hermes-config, provider-onboarding, json-safety]
---

# Federation Seat Wiring

A "seat" in the arifOS federation = one API key + one provider endpoint, exposed through 3 layers so all 3 gateways (LiteLLM proxy for FED aliases, Hermes config for direct provider access, OpenCode agent whitelist for per-agent selection) can reach it. **Missing any layer = seat invisible to that gateway.**

This is the canonical recipe for adding a seat — applicable to Qwen Individual Pro, Team Pro, Bailian PAYG, MiMo token-plan, OpenRouter, or any new provider.

## The 3-layer topology

| Layer | File | Purpose | Edit risk |
|---|---|---|---|
| **1. LiteLLM proxy** | `/root/A-FORGE/litellm-config.yaml` | Defines cascade entries under each alias (`hermes-asi`, `agi-333`, `apex-888`, etc.). Lets FED aliases route through the new key. | Medium — YAML, restart required |
| **2. Hermes config** | `/root/.hermes/config.yaml` → `providers.<name>` | Registers the provider (endpoint, env key, model list) for direct use from Hermes sessions, TTS, STT, vision. | Low — additive YAML |
| **3. OpenCode/OpenClaw config** | `/root/.config/opencode/opencode.json` (`agent.<name>.models`, `enabled_providers`, `provider.<name>`) | Per-agent model whitelist. Determines which agents can pick models from the seat. | **High** — JSON, silent-drop risk |

**Iron rule:** patch all 3 layers in the same change-set. Audit step (see below) catches missed layers.

## Pre-flight: verify the seat is live

Before wiring, confirm the key actually works. Don't trust config files; probe the upstream.

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a

# 1. Key validity (auth only)
curl -s -o /dev/null -w "HTTP %{http_code}\n" "$QWEN_BASE_URL/models" \
  -H "Authorization: Bearer $NEW_KEY"

# 2. Key usability (real inference — chat completion with tiny budget)
curl -s "$QWEN_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $NEW_KEY" -H "Content-Type: application/json" \
  -d '{"model":"<fast-cheap-model>","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'

# 3. Model roster (which models does this key expose?)
curl -s "$QWEN_BASE_URL/models" -H "Authorization: Bearer $NEW_KEY" \
  | python3 -c "import json,sys; print(', '.join(m['id'] for m in json.load(sys.stdin).get('data',[])))"
```

If step 2 returns 429 quota exhaustion, the key is valid but the seat is asleep — see `provider-quota-diagnostics` for the reset flow. Don't wire an exhausted seat.

## Layer 1: LiteLLM proxy (FED cascade aliases)

**Backup first:**
```bash
cp /root/A-FORGE/litellm-config.yaml \
   /root/forge_work/backups/litellm-config-$(date -u +%Y%m%dT%H%M%SZ).yaml
```

**Add a cascade entry** under each target alias. Order = priority (lowest number = highest priority):
```yaml
- model_name: hermes-asi
  litellm_params:
    model: openai/<model-id>
    api_base: https://<provider-endpoint>/compatible-mode/v1
    api_key: os.environ/<ENV_VAR>
    order: 0   # 0 = top priority, 1 = first fallback, 2 = second, etc.
  model_info:
    {max_input_tokens: 1048576, max_output_tokens: 131072, mode: chat, supports_image_input: true}
```

**Restart and probe:**
```bash
systemctl restart litellm-federation.service
sleep 2
curl -s "http://127.0.0.1:4000/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H "Content-Type: application/json" \
  -d '{"model":"hermes-asi","messages":[{"role":"user","content":"hi"}],"max_tokens":5}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('fp:', d.get('system_fingerprint','?')[:60])"
```

**system_fingerprint tells** (which upstream actually served):
- DashScope/Aliyun Qwen: `fp_a18b46594c_prod0820_fp8_kvcache_20260402`
- MiMo token-plan: starts with `fp_` followed by model hash (Xiaomi-internal)
- DeepSeek direct: `fp_ollama` or `fp_deepseek_xxx`

If the fingerprint doesn't match your expected upstream, your entry has wrong `order:` or wrong `model:` field.

## Layer 2: Hermes config (direct provider access)

Already pre-configured for the standard seats:
- `qwen-token-plan-individual` → `QWEN_INDIVIDUAL_API_KEY`
- `qwen-token-plan` → `QWEN_BAILIAN_KEY`
- `qwen-responses` → DashScope Responses API
- `dashscope-payg` → `DASHSCOPE_API_KEY`

Adding a new provider: append under `providers:` in `/root/.hermes/config.yaml`:
```yaml
new-provider:
  api: https://<endpoint>/v1
  capabilities: [chat, function_calling, reasoning]
  key_env: <ENV_VAR_NAME>
  models:
    - id: <model-id>
      name: <human-readable name>
  name: <Provider display name>
  transport: openai_chat
```

TTS variant under `tts:` block uses same shape with `model: <tts-model-id>`, `sample_rate:`, `voice:` fields.

No restart required — Hermes reloads on next session, or restart the gateway.

## Layer 3: OpenCode agent whitelist (CRITICAL)

**The two JSON pitfalls — round-trip silent drops AND schema rejection of unknown root keys** — see `references/opencode-json-pitfalls.md` for verbatim probes and the 17-key whitelist. This is the layer most prone to silent regression.

**Safe mutation procedure:**

1. **Backup:**
   ```bash
   cp /root/.config/opencode/opencode.json \
      /root/forge_work/backups/opencode.json-$(date -u +%Y%m%dT%H%M%SZ).json
   ```

2. **Patch (preferred: use `patch` tool or `jq`):**
   ```bash
   # Add to enabled_providers if not present
   jq '.enabled_providers |= . + ["new-provider"]' \
      /root/.config/opencode/opencode.json > /tmp/oc.json && \
   mv /tmp/oc.json /root/.config/opencode/opencode.json

   # Add models to each agent's whitelist
   jq '.agent["555-ASI"].models["new-provider/<model>"] = {}' \
      /root/.config/opencode/opencode.json > /tmp/oc.json && \
   mv /tmp/oc.json /root/.config/opencode/opencode.json
   ```

3. **Verify post-write (mandatory, three passes — data, schema, smoke):**
   ```bash
   # Pass A: round-trip integrity — counts the entities that matter (catches silent drops)
   # Compares against the backup you made in step 1. Mismatch on enabled_providers /
   # agent count / provider count = silent drop. Restore from backup.
   python3 <<'PY'
   import json, pathlib
   bak = pathlib.Path("/root/.config/opencode/opencode.json.bak-<ts>")
   cur = pathlib.Path("/root/.config/opencode/opencode.json")
   b, c = json.loads(bak.read_text()), json.loads(cur.read_text())
   for name, (bv, cv) in {
       "top-level keys":   (set(b.keys()), set(c.keys())),
       "enabled_providers": (b.get("enabled_providers"), c.get("enabled_providers")),
       "agent count":       (len(b.get("agent",{})), len(c.get("agent",{}))),
       "provider count":    (len(b.get("provider",{})), len(c.get("provider",{}))),
   }.items():
       print(("✅" if bv == cv else "❌ MISMATCH"), name, "pre=", bv, "post=", cv)
   PY

   # Pass B: schema validity — QUICK probe (~3s, catches stray root keys)
   cd /root/.config/opencode && opencode models 2>&1 | head -5
   # Empty "Error:" + first lines show model list = schema valid. Non-empty "Error:" = stop, strip, retest.

   # Pass B-FULL (when quick probe is ambiguous or you need plugin/hook debug detail)
   cd /root/.config/opencode && echo ping | timeout 30 opencode run --log-level DEBUG --print-logs 2>&1 \
     | grep -E "Error|invalid|Configuration" | head -5
   # Empty grep = schema accepts. Proceed to smoke test.
   # Non-empty = opencode rejects the config. Strip unknown `_`-prefixed root keys with
   # `jq 'del(._last_updated, ._patch_summary)'` and retest. The 17-key whitelist is in Pitfalls below.
   ```
   - Quick probe (`opencode models`) is the cheapest first-line schema check — same error detection
     as the full `opencode run --log-level DEBUG` probe but ~10x faster. Run it FIRST on every edit.
     Only escalate to the full probe if quick probe is ambiguous or you need plugin/hook detail.

4. **Smoke test:**
   ```bash
   opencode run 'Reply with exactly: OPENCODE_FED_OK'
   ```
   - Look for the expected model in the response (if --thinking enabled).

## Post-wiring audit (5-step verification)

```bash
# 1. LiteLLM alias actually routes through new seat
curl -s http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H "Content-Type: application/json" \
  -d '{"model":"<alias>","messages":[{"role":"user","content":"hi"}],"max_tokens":5}' \
  | jq '.system_fingerprint'   # should match expected upstream

# 2. Hermes direct provider works
curl -s "$PROVIDER_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"<model>","messages":[{"role":"user","content":"OK"}],"max_tokens":5}' \
  | jq '.choices[0].finish_reason'

# 3. OpenCode can select the model (whitelist check)
jq '.agent | to_entries[] | select(.value.models | keys | map(select(test("new-provider"))) | length > 0) | .key' \
   /root/.config/opencode/opencode.json

# 4. enabled_providers contains the new provider
jq '.enabled_providers' /root/.config/opencode/opencode.json | grep "<new-provider>"

# 5. JSON round-trip integrity (no silent drops)
python3 -c "import json; d=json.load(open('/root/.config/opencode/opencode.json')); print('agents:', len(d['agent']), 'providers:', len(d['enabled_providers']))"
```

### After Arif refreshes a token plan (post-refresh probe — verified 2026-08-08)

When Arif directive is "refresh individual plan / try test", run the full 5-step with three additions:

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a

# A. Direct upstream FIRST (cheap, 1-2s)
curl -s -w "\nHTTP %{http_code} TIME %{time_total}s\n" \
  "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $QWEN_INDIVIDUAL_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen3.8-max","messages":[{"role":"user","content":"hi"}],"max_tokens":20}'

# B. Then probe via LiteLLM :4000 with the ALIAS (raw names rejected — see Pitfalls)
curl -s -w "\nHTTP %{http_code} TIME %{time_total}s\n" \
  "http://127.0.0.1:4000/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H "Content-Type: application/json" \
  -d '{"model":"hermes-asi","messages":[{"role":"user","content":"hi"}],"max_tokens":200}'

# C. Re-probe FED :7074 fed_status so balance notes reflect the refresh
curl -s http://127.0.0.1:7074/health >/dev/null && echo "FED live"
SESSION=$(curl -si -X POST http://127.0.0.1:7074/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}' \
  | grep -i 'mcp-session-id' | sed 's/.*: //' | tr -d '\r\n')
curl -s -X POST http://127.0.0.1:7074/mcp -H "Content-Type: application/json" \
  -H "mcp-session-id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"fed_status","arguments":{}}}' \
  | python3 -c "import sys,json,re; d=sys.stdin.read(); m=re.search(r'^data: (.+)$',d,re.M); r=json.loads(m.group(1))['result']['content'][0]['text']; [print(p['provider_name'],'USD:',p['balance_usd'],'notes:',p.get('notes','')[:120]) for p in json.loads(r)['providers'] if 'qwen' in p['provider_name']]"
```

**State separately:** "direct upstream = 200 in 1.6s" vs "via LiteLLM alias = 200 in 0.9s" — different layers, different failure modes. If only one passes, the bug is at one specific layer (key vs cascade entry vs alias resolution), not the seat itself.

### Stale `fallback_providers` reconciliation (Arif directive 2026-08-08)

After a token-plan refresh, `/root/.hermes/config.yaml` `fallback_providers:` is **stale config** — it lists `qwen-token-plan-standard` and `qwen-token-plan-team-owner` even though those pools are exhausted (429). The fallback chain will silently route to a dead provider. Sync recipe:

```bash
# 1. List actual fallbacks
grep -A 3 "fallback_providers:" /root/.hermes/config.yaml

# 2. Probe each fallback for live status (one-line per key)
set -a && source /root/.secrets/kunci-mas.env && set +a
for key in QWEN_API_KEY QWEN_BAILIAN_KEY QWEN_INDIVIDUAL_API_KEY DASHSCOPE_API_KEY MINIMAX_API_KEY GROQ_API_KEY; do
  echo -n "$key: "
  curl -sS -m 5 -o /dev/null -w "HTTP %{http_code}" "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models" \
    -H "Authorization: Bearer ${!key}" 2>/dev/null || echo "FAIL"
done

# 3. Cross-reference FED fed_status balance notes for current state
# (see Post-wiring audit step C above)

# 4. Edit fallback_providers to ONLY list live seats, then restart gateway
#    Order = priority. First match wins.
```

**Iron rule:** never trust `fallback_providers:` without probing each key. Config says "alive" means nothing; a 429 means the next outage cascades.

## Rollback discipline

Every patch in this recipe must have a backup path:

| Layer | Backup | Rollback |
|---|---|---|
| LiteLLM config | `/root/forge_work/backups/litellm-config-<ts>.yaml` | `cp <backup> /root/A-FORGE/litellm-config.yaml && systemctl restart litellm-federation.service` |
| Hermes config | same path | `cp <backup> /root/.hermes/config.yaml` |
| OpenCode config | `/root/forge_work/backups/opencode.json-<ts>.json` | `cp <backup> /root/.config/opencode/opencode.json` |

Always test rollback before committing the change.

## Seat retirement (unwiring a dead provider)

Wiring is half the story. When a provider is permanently dead (service shut down, API sunset, plan exhausted beyond recovery), you **retire** it from all 3 layers in reverse. Verified live 2026-08-12 (Tavily retirement — dev plan permanently exhausted, swapping to SearXNG sovereign primary).

**Disable vs retire:**
- **Disable** (order-only change): provider still valid but temporarily exhausted, or Arif says "switch away for now". Move to last fallback position. **Reversible in 1 command.** No doc changes.
- **Retire** (full unwire): provider's upstream is permanently dead. Remove from env, config, whitelist, docs. Leaves a `RETIRED <date>` comment trail — **never blank** (preserves forensic trace).

**5-step retirement recipe (Tavily as worked example):**

```bash
# Step 0 — Backup (F1 reversible-first)
cp /root/.secrets/kunci-mas.env /root/.secrets/kunci-mas.env.bak.retire-<provider>
# flat.env is regenerated from vault-generate, no backup needed

# Step 1 — Vault key: export → retired comment (NEVER delete the line)
# Use patch tool for precision:
sed -i 's|^export DEAD_API_KEY=.*|# DEAD_API_KEY RETIRED '"$(date +%Y-%m-%d)"' — <reason>|' \
  /root/.secrets/kunci-mas.env
# Verify: grep -c "^export DEAD_API_KEY" /root/.secrets/kunci-mas.env  → 0
#        grep -c "DEAD_API_KEY RETIRED" /root/.secrets/kunci-mas.env → 1

# Step 2 — Whitelist: remove the provider prefix from ARIFOS_ENV_WHITELIST
# Must escape _ carefully; use patch tool, not regex, for production
sed -i 's|DEAD_||; s|^_||; s|_|_|g' /root/.secrets/kunci-mas.env  # WRONG — pipe to patch first
# Better: use patch tool to replace the exact ARIFOS_ENV_WHITELIST line

# Step 3 — Regenerate flat env (systemd source-of-truth)
cd /root/.secrets && make -f Makefile vault-generate
# Verify: grep -c DEAD_API_KEY /root/.secrets/kunci-mas.flat.env → 0

# Step 4 — Skill docs: mark retired (don't remove — keeps search trail)
# In any SKILL.md or references/*.md listing the provider:
#   | ~~Tavily~~ | ~~`TAVILY_API_KEY`~~ | **RETIRED 2026-08-12** — dev plan exhausted. SearXNG sovereign primary. |

# Step 5 — Final verification: zero active references
grep -rn "DEAD_API_KEY\|DEAD_PROVIDER" /root/.secrets/kunci-mas.env \
  /root/.hermes/config.yaml /root/A-FORGE/litellm-config.yaml \
  /root/HERMES/skills/ 2>/dev/null | grep -v ".bak\|.archive\|quarantine\|RETIRED"
# Expect: empty
```

**Post-retirement env staleness:**
Running processes (shell sessions, active Hermes sessions) retain the old env var until they restart. This is **harmless** IF no code path calls the retired provider (which it can't, after step 4 removed it from cascade/config). Restart is NOT required when config layers are clean — flat.env (systemd source) is already clean after step 3.

**Constitutional rule:** this T1 cleanup is reversible from `/root/.secrets/kunci-mas.env.bak.retire-<provider>`. No F13 involvement needed — it's ordinary secret hygiene, not mutation.

## FED front door down (HAProxy :4000 → 503) — root-cause chain (2026-08-09)

When the front door 503s but the backends look healthy, the failure is usually the **health-check contract**, not the providers. Verified live 2026-08-09 while auditing a sibling "zen FED" run:

```
:4000 (HAProxy) 503  →  fed_primary (:4011) marked down  →  health check failing
```

Two independent causes, check BOTH:

1. **Wrong health-check endpoint.** LiteLLM's `/health` runs a FULL upstream sweep — on litellm-federation it took **8.9s** (probe every model in every cascade). HAProxy's default check timeout (1s) kills it → server perpetually down even with a valid key. The fast endpoints are `/health/liveliness` (3ms) and `/health/readiness` (9ms).
   ```bash
   # before (slow, kills the check):
   option httpchk GET /health
   # after (verified fix):
   option httpchk GET /health/liveliness
   timeout check 3000
   http-check expect status 200
   ```
2. **Redacted/placeholder key in the health-check line.** A `Bearer sk-lit...74ed`-style placeholder (redaction artifact written into the file, not the real key) makes litellm log `401 "Malformed API Key"` / `"No api key passed in"` on every check → server never rises. The baked key must be the REAL `$LITELLM_MASTER_KEY`. Audit:
   ```bash
   grep -oP 'Bearer "\K[^"]+' /etc/haproxy/haproxy.cfg | head -1   # must equal $LITELLM_MASTER_KEY
   ```
   Compare lengths + confirm listening with `ss -tlnp` (curl -sf lies on litellm: 401 without auth looks like "down").

**Process topology check:** there may be a THIRD litellm (`litellm-proxy.service`) that inherits `PORT=` from flat env and lands on an orphan port (e.g. :26898) that nothing references. Park it reversibly: `systemctl disable --now litellm-proxy` + keep the unit file with a `parked-*.conf` drop-in. `litellm-escape` (survival proxy) should carry a `no-db.conf` drop-in: `UnsetEnvironment=DATABASE_URL POSTGRES_URL ...` + `Environment=PORT=` guard so it never inherits DB env or the kernel's port.

## Identity vs runtime provider contract (WHO vs WHICH) — the split that must never blur

Auditing sibling "zen" runs of agent configs is only safe if the WHO/WHICH split is enforced. Verified 2026-08-09:

- **WHO = identity contract** — agent cards (`a2a-server/agent-cards/`: id, bound_to, class, species, authority_boundary, skills). Sealed, F13-governed, changes rarely. Canonical tree is `a2a-server/agent-cards/` (root `AAA/agent-cards/` is LEGACY).
- **WHICH = runtime provider contract** — `model`/`base_url`/`apiKey`/`order` in per-runtime configs + `/root/.config/federation-models.json` + litellm-config.yaml. Operational, changes daily (quota/health/cost).

**Audit line for any sibling change report:** hash-snapshot the config files BEFORE the sibling mutates (`md5sum` + mtime), then after. Verify each claimed change against live probes, not against the report. Check the identity tree is untouched with `find /root/AAA/a2a-server/agent-cards -type f -newermt '<start>'`. Never let a provider-zen run touch agent cards, bound_to, class, or SOUL.

**Universal FED wiring for coding agents** (opencode / claude-code / kimi / codex / copilot): 3 knobs per runtime config —
```
model     = FED alias   (opencode, codex, hermes-asi, agi-333, openclaw, apex-888, dispatch)
base_url  = http://127.0.0.1:4000/v1   (front door; Codex uses :4001 fed-clean-proxy → :4000)
api_key   = $LITELLM_MASTER_KEY
```
Direct providers stay registered as fallback — NEVER delete them (Arif: "nak letak balik susah" — putting them back is painful). Order-only changes are the reversible zen; removals are not.

## Pitfalls

- **Do not blur WHO and WHICH in one change-set.** An agent's identity (opencode = FI-001 buruh, hermes = 555-bound mandor) is independent of which engine powers it. Flipping a primary model (FED → direct, or vice versa) is a WHICH change and must never require editing an agent card.
- **JSON round-trip silent drops** — see `references/json-roundtrip-silent-drops.md`. Mandatory post-write diff. The bug bit OpenCode's `enabled_providers` array on 2026-08-07 (3 entries vanished with no error).
- **Schema rejection of unknown root keys** — `opencode` enforces a strict schema on `/root/.config/opencode/opencode.json`. JSON parses fine (`python3 -m json.tool` succeeds), so syntax check passes — only the runtime schema validator catches it. Stray metadata keys (`_last_updated`, `_patch_summary`, any `_`-prefixed top-level key) break boot with `Error: Configuration is invalid at ... ↳ Unrecognized keys: _last_updated, _patch_summary`. Bit Arif 2026-08-07 when a sibling session's automation dumped patch metadata at the JSON root. **Mandatory post-write probe (do this AFTER every opencode.json edit):**
  ```bash
  cd /root/.config/opencode && echo ping | timeout 30 opencode run --log-level DEBUG --print-logs 2>&1 \
    | grep -E "Error|invalid|Configuration" | head -5
  ```
  Empty grep = schema accepts. Non-empty = strip the unknown keys (`jq 'del(._last_updated, ._patch_summary)' opencode.json`) and retest. Known-good root-key whitelist (17, as of 2026-08-07): `$schema`, `model`, `small_model`, `enabled_providers`, `default_agent`, `instructions`, `agent`, `provider`, `mcp`, `references`, `permission`, `compaction`, `lsp`, `formatter`, `autoupdate`, `plugin`, `subagent_depth`. Anything outside this set is suspect.
- **config.yaml != litellm-config.yaml** — Hermes gateway reads `/root/.hermes/config.yaml` for provider definition; LiteLLM proxy reads `/root/A-FORGE/litellm-config.yaml` for cascade routing. Editing one doesn't affect the other.
- **Order field semantics** — in LiteLLM, `order: 0` is highest priority (served first). `order: 1` is first fallback (used when order:0 fails). Don't confuse with reverse semantics.
- **system_fingerprint is your truth detector** — always inspect it after a probe. If the fingerprint says MiMo but you expected DashScope, your cascade entry is wrong (wrong `api_base` or wrong `api_key`).
- **Reasoning-heavy models eat your test budget** — `qwen3.7-plus`, `mimo-v2.5`, `glm-5.2` consume tokens in internal reasoning. Use `max_tokens: 60+` or non-reasoning models (`qwen3.6-flash`, `deepseek-v4-flash`) for cascade health probes.
- **LiteLLM :4000 rejects raw upstream model names** (verified 2026-08-08): `model=qwen3.8-max` → `400 Invalid model name passed in model=...` even when the upstream is healthy. Call `curl -s http://127.0.0.1:4000/v1/models -H "Authorization: Bearer $LITELLM_MASTER_KEY"` to see the alias surface; alias→upstream mapping lives in `/root/A-FORGE/litellm-config.yaml`. Raw names work ONLY on the direct upstream endpoint. Always state which layer you're testing in the probe result, because the same model name behaves differently on each (direct = upstream behavior, alias = LiteLLM-resolved upstream after fallbacks).
- **Reasoning `max_tokens` budget trap** (verified 2026-08-08): Qwen3.x reasoning models return `finish_reason: "length"` with **empty `content`** when `max_tokens=20`. Every token went to `reasoning_content`, none to actual output. The probe looks like a successful API call (HTTP 200) but produces zero useful data. Use `max_tokens: 200+` for one-word answers, or you'll misdiagnose a working API as broken.
- **Qwen Individual Plan has a SEPARATE quota pool from the team plan** (verified 2026-08-08): team seats exhausted → 429 does NOT affect the individual plan. Both keys live in `kunci-mas.env` (`QWEN_API_KEY` vs `QWEN_INDIVIDUAL_API_KEY`), both are valid, but they share an account-wide display while metering independently. Always probe the actual key the cascade will use, not "any Qwen key".
- **`balance_usd=0` ≠ dead provider for credit-based plans** (verified 2026-08-08): Qwen Individual is credit-based (monthly token plan credit), not USD-billed. FED `fed_status` shows `balance_usd: 0` for healthy plans. Read the `notes` field — `BILLING_MODEL=monthly_token_plan_credit` is the tell. Don't kill a healthy seat on a zero-balance panic.
- **Quota reset is async** — after a manual portal reset, first chat probe may still 429. See `provider-quota-diagnostics` for the full retry recipe.
- **Don't declare "wired ✅" on config-only evidence** — always run a live chat probe through the proxy before reporting success. Diff inspection misses runtime issues and JSON round-trip drops.
- **Post-wire "FED failed" from opencode is usually the env, not the wire (verified 2026-08-08).** Two surfaces share the name "FED": (a) `fed-router` MCP at `:7074` (where you wire provider metadata via `fed_router.py`), (b) `litellm-federation` proxy at `:4000` (where opencode chats). When opencode reports "FED failed" right after a wire, the upstream body is almost always `401 Authentication Error, No api key passed in` — meaning `LITELLM_MASTER_KEY` is missing in the **opencode process environment**, not that your wire broke. Run `/root/scripts/fed-doctor.sh --json`: `KEY_MISSING` → `source /root/.secrets/kunci-mas.env` before launching opencode; `UP` → your wire is fine, look elsewhere. Recipe: `fed-cognitive-allocator/references/fed-doctor-preflight-2026-08-08.md`.

## OpenCode CLI multi-agent spawn — subagent pitfall (2026-08-07)

When wiring subagents into `agent.<name>.mode: "subagent"` (the 555-ASI / 888-APEX / image-analyzer / dispatch pattern in this federation), they **cannot be CLI entry points**:

```bash
# ❌ REJECTED — falls back to default agent
opencode run --agent 555-ASI "audit this repo"
# !  agent "555-ASI" is a subagent, not a primary agent. Falling back to default agent

# ✅ CORRECT — primary agents are the only valid CLI entry points
opencode run --agent 333-AGI "audit this repo"
```

**Why:** OpenCode's CLI launches a primary agent session; subagents only exist as children of a primary agent's conversation. Subagent spawn happens from inside the primary agent (via the `task` tool / slash command), not from the terminal.

**Fix when user asks "why can't I spawn multi-agent from terminal":**
1. Confirm `--agent <name>` points to a `mode: primary` agent (333-AGI is the canonical primary in this federation)
2. Subagent definitions stay in `opencode.json` under `agent.<name>.mode: "subagent"` — pickable from within 333-AGI but not from CLI
3. For multi-agent orchestration from terminal, use `delegate_task` (Hermes) or background-spawned `opencode run` in different workdirs (parallel worktree pattern in the `opencode` skill)

**Probe to confirm a subagent is correctly wired (when you suspect the user has set `mode: "subagent"` correctly but it isn't reachable from CLI):**
```bash
cd /root/.config/opencode && opencode run --agent <subagent-name> "ping" 2>&1 \
  | grep -E "subagent|primary|Falling" | head -3
```
Expect: `"agent <name>" is a subagent, not a primary agent. Falling back to default agent` — this is the **correct** (not an error) signal that the mode field is set right.

## Two-source-of-truth gotcha: opencode.json vs AGENT_MODEL_MAP.json

Both files declare agent→model bindings and MUST stay aligned. Drift here causes agents to silently route to the wrong provider after any regeneration:

| File | Role | Mutates via |
|---|---|---|
| `/root/.config/opencode/opencode.json` | Live config read by opencode process | Hand-edit (you), fed-sync timer (only `enabled_providers`) |
| `/root/AAA/registries/models/AGENT_MODEL_MAP.json` | Canonical SOT for all A2A agents | Hand-edit only; `render-opencode-config` regenerates opencode.json from this but is manual-only (not on cron) |

After any opencode.json edit, also update the matching `agents[]` entry in `AGENT_MODEL_MAP.json` (`primary_model`, `primary_provider`, `fallback_chain`). Mismatch = drift detected by next manual `render-opencode-config --diff`.

**fed-sync `enabled_providers` partial conflict:** the `/root/scripts/fed-sync.sh` timer (15 min) queries FED :7074 for provider balances and re-enables anything with `$balance > 0`. If FED reports `bailian-token-plan` at $25 (a different keypool than a locally dead PAYG `DASHSCOPE_API_KEY`), fed-sync re-adds `bailian-token-plan-payments` to opencode's `enabled_providers`. This is cosmetic — opencode only routes agents through it if an agent's `model` is bound to that provider. Verify after fed-sync runs that your `agent.<name>.model` entries are unchanged.

## Qwen token-plan: quota exhaustion diagnosis

When 5 of 5 Qwen team keys simultaneously return `429`, the **team pool** is exhausted (single account-wide quota, all seats share). The individual key (`QWEN_INDIVIDUAL_API_KEY`) sits on a separate meter. Diagnostic recipe:

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a

# Tiny completion (costs ~1 token) against each key — proves per-key vs account-wide
for k in QWEN_API_KEY QWEN_BAILIAN_KEY QWEN_OPENCODE_API_KEY \
         QWEN_HERMES_API_KEY QWEN_TEAM_OWNER_API_KEY QWEN_INDIVIDUAL_API_KEY; do
  v="${!k}"
  code=$(curl -sS -m 8 -o /tmp/r -w "%{http_code}" "$QWEN_BASE_URL/chat/completions" \
    -H "Authorization: Bearer $v" -H "Content-Type: application/json" \
    -d '{"model":"qwen3.6-flash","messages":[{"role":"user","content":"."}],"max_tokens":1}')
  msg=$(grep -o '"message":"[^"]*"' /tmp/r | head -1)
  printf "  %-26s %s  %s\n" "$k" "$code" "$msg"
done
```

**Error shapes:**

- `429 "Your token-plan quota has been exhausted."` — team pool, no reset timestamp
- `429 "Your token-plan 1-week quota has been exhausted. The quota will reset at 08-07 07:38:00 UTC."` — individual pool, parse `reset at (\S+ \S+ UTC)` from body
- `403 "...AllocationQuota.FreeTierOnly"` — PAYG key in free-tier-only mode (no billing on file)

Cannot fetch numeric balance from REST — gated behind console session. Use <https://home.qwencloud.com>.

**Model roster differs per key** — always probe `/v1/models` first before patching cascade entries:

```bash
curl -sS "$QWEN_BASE_URL/models" -H "Authorization: Bearer $QWEN_INDIVIDUAL_API_KEY" \
  | python3 -c "import json,sys; print(', '.join(m['id'] for m in json.load(sys.stdin)['data']))"
```

Team pool had 22 models; individual has 11. Models like `qwen3.7-flash` and `qwen3-coder-plus` are team-only — never put them in an Individual-key cascade entry.

## Cascade sabotage recipe (prove fallback routing without breaking real providers)

To confirm LiteLLM falls back to tier N when tiers 1..N-1 fail, without taking real providers down:

```bash
cp /root/.secrets/kunci-mas.flat.env /tmp/kunci-bak-$(date +%s).flat.env

# Sabotage primary tiers
sed -i 's|^export MIMO_API_KEY=.*|export MIMO_API_KEY="sk-FAKE-mimo-broken-1234567890"|' \
  /root/.secrets/kunci-mas.flat.env
sed -i 's|^export DEEPSEEK_API_KEY=.*|export DEEPSEEK_API_KEY="sk-FAKE-deepseek-broken"|' \
  /root/.secrets/kunci-mas.flat.env

systemctl restart litellm-federation.service && sleep 8

# Probe — should route to fallback tier
curl -sS -m 60 "http://127.0.0.1:4000/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" -H "Content-Type: application/json" \
  -d '{"model":"hermes-asi","messages":[{"role":"user","content":"ping"}],"max_tokens":10}' \
  | jq '.system_fingerprint'   # should fingerprint the fallback tier (e.g. Qwen Individual)

# RESTORE (F1 reversible-first)
cp /tmp/kunci-bak-*.flat.env /root/.secrets/kunci-mas.flat.env
systemctl restart litellm-federation.service
```

systemd loads `EnvironmentFile=/root/.secrets/kunci-mas.flat.env` — flat.env is the live env for the litellm child. Editing it directly (with backup) is safe and reversible. Do not touch `kunci-mas.env` (golden vault; regen overwrites flat). The flat file is regenerated by `make -f /root/.secrets/Makefile vault-generate`.

## Warga-organ provisioning (new agent → constitutional citizen)

This is **different from a provider seat.** A provider seat is a key + endpoint routed through 3 layers. A warga organ is a whole new agent node (OpenClaw, kimi, codex, image-analyzer, dispatch, omega-shadow) being given constitutional identity in the AAA federation. The recipe is the 4-step provenance chain that turns a running process into a citizen with signing authority, ceiling, and forbidden domains.

**Step 1 — Ed25519 keypair:** `/root/AAA/auth/keys/<organ>_private.key` (mode 600, owner root) + `<organ>_public.key` (mode 644). The organ's signing identity. Treat as a secret — never paste, never commit, never log.

**Step 2 — DID registry entry:** Canonical `/root/AAA/secrets/did/registry.json` + runtime mirror `/opt/arifos/.secrets/did/registry.json`. Write both — runtime is what arifOS reads at request time. DID format: `did:arif:<organ-slug>`. Fields: `organ_id`, `public_key_hex`, `algorithm: Ed25519`, `description`.

**Step 3 — organs.yaml entry:** `/root/AAA/federation/organs.yaml`. Required fields: `id`, `class` (CORE | EDGE | METABOLISM | MEMORY | ADVISORY | SUPPORT), `display_name`, `role`, `authority_ceiling` (DISPLAY_ONLY | COMPUTE_ONLY | JUDGE_ONLY | REFLECT_ONLY | EXECUTE_AFTER_SEAL), `port`, `runtime`, `actor_id`, `did`, `signing_key`, `key_id`, `owned_domains`, `forbidden_domains`. The `forbidden_domains` list is the load-bearing field — every cognitive domain the organ MUST NOT touch. For dispatch/router organs: `human_face`, `cognitive_research`, `memory_curation`, `skills_library`, `constitutional_judgment`, `engineering_execution`. The ceiling is the gate; the forbidden list is the rule.

**Step 4 — SCT verification (the audit test):** Produce an SCT v1 token — `issuer=<DID>, actor_id=<actor_id>, session_id=<unique>, max_action_class=OBSERVE, ceiling=<CEILING>`. Canonicalize payload (sort_keys, no whitespace) → sign → hex. Verify signature against the PUBLIC key in the registry. If verification passes → identity is constitutionally valid. If it fails → keypair mismatch (private key regenerated doesn't match registry public key; restore from backup and re-run).

**Script:** `openclaw-mesh-bridge/scripts/provision_warga_identity.py` is the idempotent template. Edit the 4 constants at the top (ORGAN_ID, DID_NAME, ACTOR_ID, ROLE) and run. Handles all 4 steps with safe re-runs (won't regenerate an existing key).

**IRON RULE:** a warga is NOT constitutionally valid until step 4 passes. DIDs in the registry without signature verification is just a list of names — no audit trail. The SCT test is the audit trail.

**Provenance:** OpenClaw provisioning 2026-08-07. See `openclaw-mesh-bridge` skill for the full citizen-organ contract (DISPLAY_ONLY ceiling, A2A envelope format, session continuity, routing table).

**Pitfall — worms in the registry:** When adding a new organ, scan `did:arif:<new-slug>` for typos. If you misspell the key (`openclow` vs `openclaw`), the SGD identifier mismatches and A2A signatures fail at runtime with no obvious cause. Cross-check `signing_key` filename against the `id` field in organs.yaml, and the registry entry against both. Two cross-checks = catches 90% of typos.

**Pitfall — canonical vs runtime drift:** If you write the canonical registry but forget the runtime mirror (or vice versa), the system reads one and signs with the other. Mismatch = silent A2A rejection. Always write both in the same patch.

**Pitfall — ceiling class confusion:** Ceiling values are load-bearing — `DISPLAY_ONLY` cannot mutate state, `JUDGE_ONLY` cannot execute, `EXECUTE_AFTER_SEAL` requires a prior SEAL. Pick the most restrictive ceiling that still lets the organ do its job. If you give an agent `EXECUTE_AFTER_SEAL` and it doesn't need it, you've weakened the constitutional floor for no reason.

## Reference files

- `references/gemini-provider-integration-2026-08-09.md` — **Gemini API integration**: two LiteLLM paths (openai/ stable vs gemini/ native), litellm#14771 vertex-ai fallback bug, free tier gutting (Feb 2026+), model landscape + pricing, Interactions API native-only capabilities, 8 live-verified pitfalls. Load before wiring Gemini or debugging a Gemini cascade entry.
- `references/qwen-token-plan-diagnostic-2026-08-07.md` — verbatim error shapes, per-key model rosters, cascade fall-through map, recovery options for the team/individual Qwen pool architecture.
- `references/qwen-individual-refresh-probe-2026-08-08.md` — live probe transcript from the post-refresh "try test sat" directive (direct vs alias, max_tokens trap, fallback chain stale state). Use as the template for any future "refresh + probe" directive.
- `references/opencode-json-pitfalls.md` — verbatim recipes for the two opencode.json traps (round-trip drops + schema rejection), 17-key root whitelist, mandatory verification pipeline.
- `references/a2a-dispatch-five-gates.md` — A2A dispatch protocol: auth → A2A-Version → session lineage → DID envelope → AGENT_POLICIES. Live trace from this session: `arif_judge_deliberate` is internal-only; `arif_judge` is the public binding; A2A canonical actors list; how to sign a DID envelope from AAA private key.
- `references/openclaw-aaa-wiring-2026-08-07.md` — **OpenClaw-specific 4-error debug trace**: the exact `registerAgentPolicy()` location in `federation_envelope.js`, the 4-file alignment requirement (DID registry + organs.yaml + agents.yaml + policy code), the `params.message.parts[].text` wire shape vs nested-envelope trap, canonical-actor colon-form rejection, and the `systemctl restart` requirement for policy code patches.
