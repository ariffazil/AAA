# DeepSeek Credit Exhaustion → LiteLLM Model Group Reorder (2026-08-09)

## Session context

Arif reported OpenCode failing with:
```
litellm.BadRequestError: OpenAIException - Insufficient Balance.
Received Model Group=opencode
Available Model Group Fallbacks=None
```

DeepSeek API credit exhausted. The `opencode` model group in
`/root/A-FORGE/litellm-config.yaml` had DeepSeek V4 Pro + Flash at `order:1`.
LiteLLM returned 400 → treated as client error → **no fallback triggered** →
agent died.

## Root cause: LiteLLM 400 vs fallback behavior

LiteLLM's router only triggers fallback (cascade to next `order` entry) on
specific error types:
- 429 (rate limited / quota)
- 500 (server error)
- timeout / connection errors

HTTP 400 (Bad Request — including `Insufficient Balance`) is treated as a
**client error**, not a provider failure. The router does NOT fall back. This
is by design: 400 means "your request is wrong", not "the provider is down".

But DeepSeek returns 400 for credit exhaustion, which IS a provider state
problem, not a request problem. The error code classification doesn't match
the operational reality.

## Fix: demote exhausted providers, promote known-good

### Manual approach (single model group)

Edit `/root/A-FORGE/litellm-config.yaml`:
- Change exhausted provider entries from `order: 1` to `order: 99`
- Promote known-good providers (Qwen Individual = RM0 flat, MiMo) to `order: 1`
- Remove any duplicate `order: 1` entries (multiple same-order = parallel,
  but if one is dead it wastes a retry)

### Automated approach (all model groups at once — PREFERRED)

Use `execute_code` with PyYAML to parse, reorder, and write back:

```python
import yaml
from collections import defaultdict

with open('/root/A-FORGE/litellm-config.yaml') as f:
    config = yaml.safe_load(f)

model_list = config['model_list']
groups = defaultdict(list)
for i, entry in enumerate(model_list):
    groups[entry['model_name']].append((i, entry))

for name, entries in groups.items():
    has_deepseek = any('deepseek' in e['litellm_params']['model']
                       for _, e in entries)
    if not has_deepseek:
        continue

    non_ds = [(i, e) for i, e in entries
              if 'deepseek' not in e['litellm_params']['model']]
    ds = [(i, e) for i, e in entries
          if 'deepseek' in e['litellm_params']['model']]

    order = 1
    for i, e in non_ds:
        e['litellm_params']['order'] = order
        order += 1
    for i, e in ds:
        e['litellm_params']['order'] = 99

with open('/root/A-FORGE/litellm-config.yaml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False,
              allow_unicode=True)
```

This fixes ALL model groups in one operation — no patch tool struggles with
duplicate YAML blocks.

### Post-fix: restart + verify

```bash
# 1. Restart litellm (config doesn't hot-reload)
systemctl restart litellm-federation.service

# 2. Wait for port to come up (takes ~10-15s for prisma init)
sleep 10 && ss -tlnp | grep 4011

# 3. Verify with a real chat probe through affected model group
source /root/.secrets/kunci-mas.env
curl -sf http://127.0.0.1:4011/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"opencode","messages":[{"role":"user","content":"Reply with exactly: OK"}],"max_tokens":10}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('Reply:', d.get('choices',[{}])[0].get('message',{}).get('content','?'), '| model:', d.get('model','?'))"
```

## Model group ordering after fix (2026-08-09)

| Group | order:1 | order:2 | order:3 | order:4 | order:99 |
|---|---|---|---|---|---|
| `opencode` | qwen3.8-max | mimo-v2.5-pro | MiniMax-M3 | qwen3.7-max | deepseek-v4-pro |
| `agi-333` | qwen3.8-max | mimo-v2.5-pro | MiniMax-M3 | — | deepseek-v4-pro |
| `asi-555` | mimo-v2.5-pro | MiniMax-M3 | qwen3.8-max | — | deepseek-v4-flash |
| `apex-888` | MiniMax-M3 | — | — | — | deepseek-v4-pro |
| `hermes-asi` | mimo-v2.5 | MiniMax-M3 | qwen3.8-max | qwen3.6-flash | deepseek-v4-flash |

## Architecture notes

- **HAProxy :4000** = front door (bound 127.0.0.1)
- **litellm-federation :4011** = backend (bound 0.0.0.0)
- **litellm-escape :4012** = escape hatch (bound 127.0.0.1, DeepSeek + MiMo only)
- **fed-clean-proxy :4001** = strips Responses-API features for Codex CLI
- Systemd service file says `--port 4000` but HAProxy intercepts :4000
- Config: `/root/A-FORGE/litellm-config.yaml` (single file for all groups)
- Auth: `LITELLM_MASTER_KEY` env var from `/root/.secrets/kunci-mas.env`

## Diagnostic probe order for "FED down" reports

1. `ss -tlnp | grep -E '4000|4011|4012'` — are processes listening?
2. `curl -sf http://127.0.0.1:4011/v1/models -H "Authorization: Bearer $LITELLM_MASTER_KEY"` — does litellm respond with auth?
3. `curl -sf http://127.0.0.1:4011/v1/chat/completions -H "Authorization: Bearer $LITELLM_MASTER_KEY" -d '{"model":"opencode",...}'` — does the model group serve?
4. If chat fails: check error message for `Insufficient Balance` / `400` → provider credit issue, not FED issue
5. If auth fails: check `$LITELLM_MASTER_KEY` is exported in the calling shell

## Related files

- `/root/A-FORGE/litellm-config.yaml` — the canonical LiteLLM config (all model groups)
- `/root/.config/opencode/opencode.json` — OpenCode's provider config (references `litellm-federation` provider at :4000)
- `/root/HERMES/config.yaml` — Hermes config (`provider: fed` → :4000)
- `/root/HERMES/model-picker.yaml` — Hermes model picker (tier definitions, not FED wiring)
