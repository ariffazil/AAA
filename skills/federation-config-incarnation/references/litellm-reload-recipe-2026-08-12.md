# LiteLLM Reload Recipe — 2026-08-12

The specific reload sequence for federation service config changes. Use after any litellm-config.yaml mutation.

## When to reload

Reload litellm-federation when ANY of:
- Added new `model_name:` alias
- Removed alias
- Changed model chain order
- Changed upstream endpoint (api_base)
- Changed API key reference (api_key)
- Changed context window (max_input_tokens / max_output_tokens)
- Changed `model_info` block (e.g. supports_vision, supports_function_calling)

## The recipe (idempotent, safe)

### Step 1 — Pre-reload verification

```bash
# Confirm service is up
systemctl status litellm-federation.service
# OR
ps aux | grep -E "litellm|litellm-federation" | grep -v grep

# Probe current exposed models (this is what dies during restart)
curl -s http://127.0.0.1:4000/v1/models | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('data',[])))"
```

### Step 2 — Validate yaml before restart

```bash
python3 -c "import yaml; yaml.safe_load(open('/root/A-FORGE/litellm-config.yaml'))" \
  && echo "✅ yaml valid" || echo "❌ yaml invalid — do NOT restart"
```

If invalid → fix yaml first. Restarting with broken config drops the proxy.

### Step 3 — Graceful restart

```bash
# Prefer systemd (it manages respawn, env, logging)
systemctl restart litellm-federation.service

# OR direct process restart (if not systemd-managed)
pkill -f litellm
nohup litellm --config /root/A-FORGE/litellm-config.yaml --port 4000 > /var/log/litellm/federation.log 2>&1 &
```

### Step 4 — Wait + verify incarnation

```bash
# Wait for service to come up (systemd restart usually <10s)
sleep 3

# Health probe
curl -sf http://127.0.0.1:4000/health && echo "✅ alive"

# Model count (should match pre-restart + new aliases)
curl -s http://127.0.0.1:4000/v1/models | python3 -c "import sys,json; print(f'exposed: {len(json.load(sys.stdin).get(\"data\",[]))}')"

# Specific new alias present?
curl -s http://127.0.0.1:4000/v1/models | grep -c "<NEW_ALIAS>"

# Existing aliases survived?
curl -s http://127.0.0.1:4000/v1/models | grep -c "hermes-asi"
```

### Step 5 — Functional test

```bash
# Test the new alias actually answers
curl -sf -X POST http://127.0.0.1:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"<NEW_ALIAS>","messages":[{"role":"user","content":"ping"}],"max_tokens":10}'

# Test existing alias still works (no regression)
curl -sf -X POST http://127.0.0.1:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"hermes-asi","messages":[{"role":"user","content":"ping"}],"max_tokens":10}'
```

### Step 6 — Receipt emission

Only after all steps pass, emit SEAL receipt with:
- Pre-reload model count
- Post-reload model count
- New alias status (present + answering)
- Existing alias status (no regression)

## Idempotency notes

- **Restart is idempotent** for existing aliases (config is the same). Only new/changed aliases are affected.
- **No data loss** — litellm holds no session state, only config.
- **Window of downtime**: 1-5s typical (systemd restart), up to 30s if cold-start.
- **Rollback**: if new config breaks, `git revert` the yaml change, then `systemctl restart` again.

## Common failure modes

| Failure | Cause | Fix |
|---------|-------|-----|
| `systemctl status` shows "activating" | Service stuck loading | `journalctl -u litellm-federation -n 50` to see error |
| New alias absent after restart | yaml edit didn't actually save / wrong syntax | `cat /root/A-FORGE/litellm-config.yaml | grep -A2 "NEW_ALIAS"` |
| New alias present but 400 on chat | Upstream key missing or exhausted | `cat /root/.secrets/kunci-mas.env | grep <UPSTREAM_KEY_NAME>` |
| All aliases gone after restart | yaml syntax error broke entire config | Step 2 above should catch this; if missed, `git revert` and reload |
| Service won't restart | Port 4000 still held by previous process | `lsof -i :4000` → kill old pid → retry |

## What reload does NOT touch

- A2A gateway config (separate service)
- Organ daemon configs (separate processes)
- Database state (litellm holds no DB state)
- VAULT999 (write-only hash chain, untouched)
- Other federation routes (hermes, fed_advisor, etc — unless they call litellm which times out)

## Known reloads in 2026-08-12 session

- Attempted for i-ARIF refactor (11 chains added) — NOT YET EXECUTED at session close
- Previous successful reload: hermes-asi registration (date unknown, working as of session close)

## Automation pattern

If you find yourself doing this manually often, the parent agent should add a `/forge-federation-reload` primitive that:
1. Validates yaml
2. Calls `systemctl restart`
3. Probes model count
4. Runs ping test on a configurable alias
5. Emits structured receipt

This would close the gap at the tooling level. (Not yet implemented as of 2026-08-12.)