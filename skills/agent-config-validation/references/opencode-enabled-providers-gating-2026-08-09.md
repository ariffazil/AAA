# OpenCode enabled_providers gating — deepseek restore (2026-08-09)

## Symptom
```
Model not found: deepseek/deepseek-v4-pro. Did you mean: deepseek-v4-pro?
```

## Root cause
An earlier model-switch ("smallmodel", 2026-08-07) removed `deepseek` and
`qwen-token-plan-individual` from `enabled_providers` in
`/root/.config/opencode/opencode.json`. The `provider` blocks and their
`models` maps were **never deleted — only gated**. OpenCode resolves
`provider/model` composites against *enabled* providers, so the id stopped
resolving while the suggestion (`deepseek-v4-pro`) still came from the config.
Config-layer gating problem, not a proxy problem.

## Diagnosis sequence
1. Compare `enabled_providers` vs `provider` block keys:
   `python3 -c "import json; cfg=json.load(open('/root/.config/opencode/opencode.json')); print(set(cfg['provider']) - set(cfg['enabled_providers']))`
   Non-empty set = gating bug.
2. Check the agent's `models` map — it is an ALLOWLIST. A model not listed
   there is not selectable for that agent even with the provider enabled.
3. Prove the upstream is ALIVE before restoring (restoring a dead provider is
   just a nicer error):
   - DeepSeek balance (free): `curl -s https://api.deepseek.com/user/balance -H "Authorization: Bearer $DEEPSEEK_API_KEY"` → `is_available:true`, `total_balance:"16.66"` (2026-08-09 evening)
   - 1-token chat: `curl -s https://api.deepseek.com/v1/chat/completions -d '{"model":"deepseek-v4-pro","messages":[{"role":"user","content":"Reply with exactly: OK"}],"max_tokens":5}'` → 200.
   NOTE: reasoning models return EMPTY `content` with tiny `max_tokens` (budget
   eaten by internal CoT) — 200 with empty content = alive, not broken (see
   provider-quota-diagnostics: re-probe with max_tokens≥200).

## The fix
1. Backup: `cp opencode.json opencode.json.bak-<purpose>-$(date +%Y%m%d-%H%M%S)`
2. Re-add `"deepseek"` to `enabled_providers` (position: after
   `bailian-token-plan-payments`, matching pre-switch order).
3. Re-add `"qwen-token-plan-individual"` too — agent models maps reference
   `qwen-token-plan-individual/deepseek-v4-*` (Aliyun-hosted DeepSeek).
4. Add `"deepseek/deepseek-v4-pro": {}` + `"deepseek/deepseek-v4-flash": {}`
   to the 333-AGI agent `models` map (its description already claimed
   "DeepSeek V4 Pro direct" — config now matches its own text).
5. Validate: `python3 -m json.tool opencode.json` (patch tool auto-lints).
6. Restart opencode — config is read at launch; a running TUI will NOT
   hot-reload it.

## FED nuance (why the error is NOT from FED)
`GET :4000/v1/models` exposes only federation aliases (agi-333, asi-555,
opencode, codex, …). Provider models (deepseek-v4-pro, mimo-v2.5, …) live
INSIDE those aliases as cascade tiers (`litellm_params.model:
openai/deepseek-v4-pro`) and are **never standalone names on FED**. So a
`deepseek/deepseek-v4-pro` reference resolves through the DIRECT
`provider.deepseek` block (baseURL `https://api.deepseek.com`, key
`{env:DEEPSEEK_API_KEY}` from kunci-mas.env). If FED routing is actually
wanted for a bare provider model, it must be added as its own `model_name` in
`/root/A-FORGE/litellm-config.yaml` + `systemctl restart litellm-federation`.

## Environment gotchas
- kunci-mas.env lines are `export VAR=...` — `grep -c "^VAR="` returns 0 even
  when the key exists. Grep `^export VAR=` or just `VAR=`.
- Sibling "provider X dead" reports are T₀ snapshots. DeepSeek was reported
  dead (morning, -$0.07 overdraft) and was ALIVE by evening ($16.66 topped up).
  Balance-check at decision time, never trust the last report.
