# FED Probe Hygiene & Fallback-Chain Ghost Audit

> **Forged:** 2026-08-08 after live Qwen Individual refresh audit.
> **Session signal:** "Tembak fed_probe sekarang. Biar Track A bawa ground truth dan timestamp yang paling terkini masuk ke dalam memori FED."
> **Operator lesson:** config-lies; only live `:7074/health` + `tools/list` + `token_bank.db` are truth.

This file covers the three recurring failure modes the FED operator hits when
auditing "is provider X really live?" — all three surfaced in the 2026-08-08
audit session and would recur on any future refresh.

---

## 1. The `fed_probe` Blind Spot

`fed_probe` (FED MCP :7074 tool) calls `/root/AAA/scripts/balance_probe.py`
under the hood. That script's `TRACK_A` dict is **hardcoded**:

```python
TRACK_A = {
    "deepseek": {"endpoint": "...", "key_env": "DEEPSEEK_API_KEY", ...},
    # NOTE: openrouter MOVED to Track B (2026-07-30)
}
```

So calling `fed_probe` probes **deepseek only**. The Qwen Individual, Qwen Team,
FLAME, Bailian, MiniMax, and all other Track A rows in `token_bank.db` are
silently skipped — even though they carry `track_type='A'`. Observed output:

```
🔍 FED Balance Probe — Track A (API-PROBED)
   2026-08-08T08:52:42Z
   ✅ deepseek: $14.81 (confidence=1.0)
── Summary ──
   ✅ Probed: 1
   ❌ Failed: 0
```

That "1 probed" is correct from `balance_probe.py`'s perspective but **misleading**
from the operator's: the Qwen rows still show their old `last_probed_at` and
no ground-truth refresh has happened.

### Fix: triple-step refresh for credit-based providers

For any provider in `token_bank.db` whose billing is credit/plan-based (not
USD-prepaid), the audit-grade refresh path is:

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a

# Step 1: live liveness probe (heuristic, key + model roster + credit burn)
python3 /root/AAA/scripts/qwen_credit_monitor.py
#   ↳ outputs to /root/.local/share/arifos/qwen_credits.json + logs verdict

# Step 2: stamp the row directly in token_bank.db with F2 timestamp
python3 -c "
import sqlite3
from datetime import datetime, timezone
DB = '/root/.local/share/arifos/token_bank.db'
ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
NOTE = 'LIVE <ts> — Refreshed by fed_probe audit. <probes>. <finding>.'
conn = sqlite3.connect(DB)
conn.execute('UPDATE providers SET notes=?, last_probed_at=?, last_updated=? '
             'WHERE provider_name=?', (NOTE, ts, ts, '<provider_name>'))
conn.commit()"
#   ↳ /root/AAA/scripts/qwen_credit_monitor.py does NOT update token_bank.db
#     (it only writes qwen_credits.json). You must stamp the row directly.

# Step 3: verify via fed_status (MCP) — same session protocol as fed_probe
python3 /root/AAA/scripts/fed_mcp_probe.py fed_status
#   ↳ OR raw curl per the SKILL.md probing recipe
```

Without step 2, `fed_status` will keep showing stale `last_probed_at` even after
the credit monitor runs successfully. The audit trail lives in the `notes` field;
treat it as the receipt of "this row was ground-truthed by Hermes at <ts>".

---

## 2. Token-Starvation vs Reasoning-Loop — The Diagnostic Distinction

Two failure modes look identical at a glance ("HTTP 200 came back empty or weird")
but require different diagnoses and different fixes. Captured live 2026-08-08:

### Token starvation
- **Signature:** HTTP 200, `choices[0].finish_reason = "length"`, `message.content = ""`.
- **Cause:** `max_tokens` budget was consumed by internal Chain-of-Thought before a single answer token was emitted.
- **Reproducer:** `model=qwen3.8-max, max_tokens=20, prompt="Reply with only the word: OK"` → empty content with `finish_reason=length`.
- **Fix:** re-probe with `max_tokens >= 200`. Reasoning models routinely need 50–500 tokens of CoT before producing a 1-token answer.

### Reasoning loop (overthink)
- **Signature:** HTTP 200, `finish_reason = "stop"`, **correct answer eventually**, but `usage.completion_tokens` vastly exceeds expected length and `time_total` is 10–50s.
- **Cause:** reasoning engine loops on a trivial prompt. "V8 to go to the corner shop" — the model re-derives the answer many times.
- **Reproducer:** `model=qwen3.6-flash, prompt="Say hello in 5 words"` → 26s, 3,557 completion tokens, final answer "Hello There, Wishing You Joy".
- **Fix:** this is NOT a failure — the API, key, and proxy are healthy. Re-pick a model with proportionate reasoning (qwen3.8-max for short tasks; deepseek-v4-flash for trivial). Set generous `--max-time 30+` when probing reasoning models.

### How to tell them apart fast
- `finish_reason="length"` + empty content → starvation (raise budget)
- `finish_reason="stop"` + correct answer + huge `usage` → loop (model choice, not API)
- `finish_reason="length"` + non-empty content → partially-starved, raise budget
- HTTP 429 `insufficient_quota` → quota exhausted (separate skill: `provider-quota-diagnostics`)

**Operator rule:** never diagnose API/proxy/key as dead on the starvation signature alone — re-probe with a larger budget first.

---

## 3. Ghost-Fallback Audit Recipe

`~/.hermes/config.yaml` carries a `fallback_providers:` chain that the LiteLLM
proxy consults when a primary provider fails. **These chains rot** — providers
get exhausted, revoked, or archived while the config still lists them. Live
case 2026-08-08: `qwen-token-plan-standard` and `qwen-token-plan-team-owner`
were listed as Qwen fallbacks, but the underlying team plan seats had been
EXHAUSTED since 2026-08-05 (0/150K credits remaining). The fallback chain
would 429 every time it fired.

### Audit recipe (3 steps, ~30 seconds)

```bash
# Step 1: pull LIVE provider state from FED
python3 /root/AAA/scripts/fed_mcp_probe.py fed_status > /tmp/fed_status.json
#   ↳ look at: track_type, balance_usd, last_probed_at, notes (search EXHAUSTED / QUOTA-0)

# Step 2: cross-check fallback_providers against LIVE state
#   ↳ any provider in fallback_providers whose notes say EXHAUSTED or whose balance=0
#     AND billing model ≠ monthly_token_plan_credit → REMOVE
grep -A 20 "^fallback_providers:" ~/.hermes/config.yaml

# Step 3: replace ghost with F2-stamped live provider (from step 1)
#   ↳ for Qwen: qwen-token-plan-individual (the only LIVE Qwen seat)
#   ↳ for others: query fed_status for the corresponding LIVE row
```

### Patch recipe

When replacing a ghost fallback with a live one:

```yaml
fallback_providers:
  - model: <model_name>
    provider: <LIVE_provider_name>     # ← was: ghost name
    timeout: 30
    note: "<provider> — LIVE F2 confirmed <ISO timestamp>. <probe summary>."
```

The `note:` field is the audit receipt. Future audits should be able to grep
the config for "LIVE F2 confirmed" to find F2-stamped providers without
needing a fresh probe.

### After patching

Verify by running a real chat call through the fallback path:

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a
curl -s -X POST "http://127.0.0.1:4000/v1/chat/completions" \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<fallback_alias>","messages":[{"role":"user","content":"OK"}],"max_tokens":200}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('choices',[{}])[0].get('message',{}).get('content',''))"
```

If output is `"OK."` (or similar), the fallback path is live end-to-end. Inspect
`system_fingerprint` — DashScope/Aliyun Qwen starts with `fp_a18b46594c_prod0820_fp8_kvcache_20260402`,
MiniMax has a different fingerprint, etc. The fingerprint is the receipt for
"yes, the wire actually went through the new fallback".

---

## 4. Operator Checklists

### "Is provider X still alive?" (full audit)

- [ ] `fed_status` — track_type + balance_usd + last_probed_at
- [ ] `qwen_credit_monitor.py` (or equivalent per-provider monitor) — liveness + burn
- [ ] Direct Aliyun/Upstream probe: `GET /v1/models` (auth) + `POST /v1/chat/completions` (quota)
- [ ] LiteLLM proxy probe: `POST 127.0.0.1:4000/v1/chat/completions` via federation alias (max_tokens=200)
- [ ] Stamp `token_bank.db` providers row with F2 timestamp + audit notes
- [ ] Cross-check `fallback_providers` in ~/.hermes/config.yaml against live state

### "Why did this call hang/return empty?"

- [ ] Read `finish_reason` and `usage.completion_tokens`
- [ ] Token starvation? → raise `max_tokens` and re-probe
- [ ] Reasoning loop? → check model choice, set `--max-time 30+`
- [ ] Genuine timeout? → check provider health, network path
- [ ] 429 `insufficient_quota`? → see `provider-quota-diagnostics`

---

## 5. Knowledge-Bank Sources (live 2026-08-08)

| What | Value |
|---|---|
| `qwen3.8-max` direct Aliyun | HTTP 200, 1.6s, 28 output tokens for "What is 2+2? One line." |
| `qwen3.6-flash` direct Aliyun | HTTP 200, **26.1s**, 3,557 tokens for "say hello in 5 words" (overthink) |
| `hermes-asi` via LiteLLM :4000 | HTTP 200, 0.9s, output "OK." (clean, max_tokens=200) |
| `agi-333` via LiteLLM :4000 | HTTP 200, 1.6s (clean, max_tokens=200) |
| `fed/vision` via LiteLLM :4000 | HTTP 200, 1.9s, output "vision_ok" (clean) |
| `raw qwen3.8-max` via LiteLLM :4000 | HTTP **400** `Invalid model name` — must use alias |
| `qwen_credit_monitor.py` after fresh renewal | `5hr: 0.0% | 7d: 0.0% | Verdict: ✅ NORMAL → USE_NORMALLY` |
| `fed_probe` summary (deficient) | `Probed: 1 | Failed: 0` — only deepseek, not Qwen |

## 6. Cross-References

- `references/provider-wiring-qwen-individual-2026-08-08.md` — wiring recipe (use this when adding NEW provider)
- `references/qwencloud-individual-plan-2026-08-08.md` — QwenCloud billing/mechanics
- `references/live-state-2026-08-08.md` — live baseline snapshot
- `references/emd-lane-awareness.md` — EMD lane rules
- Sister skill: `provider-quota-diagnostics` — error signature table + reset recipe
- Sister skill: `federation-model-routing` — LiteLLM proxy chain (bundled, read-only here)

---

*Forged 2026-08-08 by Hermes after the Qwen Individual refresh audit. DITEMPA BUKAN DIBERI.*
*Trinity-33: live `:port/health` beats every prose table. Config-lies; token_bank.db + chat-completion responses are truth.*