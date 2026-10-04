# FED Full Recovery Procedure (2026-08-09)

## When to use

FED :4000 returns 503 "No server is available", all agents (Hermes, OpenClaw,
Claude Code, OpenCode) fail with 401/402/429/503 errors, and the root cause is
a combination of: HAProxy key mismatch, litellm-config uncommitted changes,
stuck service, and upstream provider exhaustion.

## Symptoms

- `curl http://127.0.0.1:4000/health` → 503 (HAProxy can't reach backend)
- `curl http://127.0.0.1:4011/health` → 000 (litellm-federation not listening)
- OpenCode: `litellm.BadRequestError: OpenAIException - Insufficient Balance`
- OpenClaw: context overflow auto-compaction stuck (no summarizer model)
- Hermes: "rate-limiting" or "provider authentication failed"

## Root cause chain (observed 2026-08-09)

```
1. HAProxy health check has placeholder key → marks :4011 as DOWN → 503
2. litellm-federation stuck in "deactivating (stop-sigterm)" → :4011 not listening
3. Uncommitted litellm-config.yaml changes (deepseek demoted to order:99)
4. DeepSeek API balance = -$0.07 (DB had $14.81 — per-key billing mismatch)
5. MiniMax Token Plan exhausted (429)
6. Qwen Token Plan Team exhausted (0 credits across 3 seats)
7. Kimi Coding usage limit reached (403)
8. DashScope PAYG free tier exhausted (403)
9. Only MiMo v2.5 + Fireworks + Groq + Qwen Individual alive
```

## 4-step recovery

### Step 1: Revert litellm-config.yaml (T1, reversible)

```bash
cd /root/A-FORGE
git diff litellm-config.yaml | head -20  # check what's uncommitted
git checkout litellm-config.yaml          # revert to last committed state
grep "order:" litellm-config.yaml | head -10  # verify deepseek=order:1 restored
```

### Step 2: Restart litellm-federation (T1)

```bash
systemctl restart litellm-federation.service
# Wait 15-20s for prisma migrate to complete
sleep 20
ss -tlnp | grep 4011  # must show LISTEN
journalctl -u litellm-federation.service --no-pager -n 3  # "Application startup complete"
```

**Pitfall:** `systemctl status` can show "active (running)" while the service
is actually in "deactivating (stop-sigterm)" — :4011 stops listening but the
process hasn't fully exited. Always verify with `ss -tlnp | grep 4011`.

### Step 3: Fix HAProxy — key + auth injection (T2)

```bash
source /root/.secrets/kunci-mas.env

# Write new HAProxy config with:
# 1. Real LITELLM_MASTER_KEY in health check
# 2. http-request set-header for auth injection on ALL requests
cat > /etc/haproxy/haproxy.cfg << EOF
global
    log /dev/log local0
    maxconn 2000
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000
    timeout client  50000
    timeout server  50000

frontend fed_gateway
    bind 127.0.0.1:4000
    default_backend llm_nodes

backend llm_nodes
    http-request set-header Authorization "Bearer ${LITELLM_MASTER_KEY}"
    option httpchk GET /health
    http-check send hdr Authorization "Bearer ${LITELLM_MASTER_KEY}"
    http-check expect status 200
    server fed_primary 127.0.0.1:4011 check inter 2s fall 2 rise 2
    server escape_backup 127.0.0.1:4012 check inter 2s fall 2 rise 2 backup
EOF

haproxy -f /etc/haproxy/haproxy.cfg -c  # validate
systemctl reload haproxy
```

### Step 4: Probe upstreams + promote alive providers (T1)

```bash
source /root/.secrets/kunci-mas.env

# Probe each upstream directly
for prov in \
  "deepseek|https://api.deepseek.com/v1|$DEEPSEEK_API_KEY|deepseek-chat" \
  "mimo|https://token-plan-sgp.xiaomimimo.com/v1|$MIMO_API_KEY|mimo-v2.5" \
  "minimax|https://api.minimax.io/v1|$MINIMAX_API_KEY|MiniMax-M3" \
  "qwen-ind|https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1|$QWEN_INDIVIDUAL_API_KEY|qwen3.7-max" \
  "fireworks|https://api.fireworks.ai/inference/v1|$FIREWORKS_API_KEY|accounts/fireworks/models/glm-5p2" \
  "groq|https://api.groq.com/openai/v1|$GROQ_API_KEY|llama-3.3-70b-versatile" \
  "gemini|https://generativelanguage.googleapis.com/v1beta/openai|$GEMINI_API_KEY|gemini-2.5-flash" \
  "kimi|https://api.kimi.com/coding/v1|$KIMI_API_KEY|kimi-k2.7-code"; do
  IFS='|' read -r name url key model <<< "$prov"
  code=$(curl -s -o /dev/null -w "%{http_code}" -m 10 "$url/chat/completions" \
    -H "Authorization: Bearer $key" -H "Content-Type: application/json" \
    -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}],\"max_tokens\":5}")
  [ "$code" = "200" ] && echo "✅ $name ($model)" || echo "❌ $name ($model) → HTTP $code"
done

# DeepSeek balance API
curl -s https://api.deepseek.com/user/balance -H "Authorization: Bearer $DEEPSEEK_API_KEY"

# Promote alive providers in token_bank.db
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
sqlite3 /root/.local/share/arifos/token_bank.db "
UPDATE providers SET track_type='A', confidence_score=0.5, last_probed_at='$NOW'
WHERE provider_name='mimo-platform';"
```

## Verification

```bash
# FED :4000 health (should show healthy_count > 0)
curl -s http://127.0.0.1:4000/health -H "Authorization: Bearer $LITELLM_MASTER_KEY" | jq '.healthy_count'

# FED :4000 chat WITHOUT key (auth injection working)
curl -s http://127.0.0.1:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"hermes-asi","messages":[{"role":"user","content":"say hi"}],"max_tokens":10}'
# Should return 200 with a response from the healthy upstream

# HAProxy logs (should show UP, not DOWN)
journalctl -u haproxy --no-pager -n 5 | grep -E "UP|DOWN"
```

## Post-recovery: model picker cleanup (separate task)

After FED is alive, clean the `/model` picker to show only working providers:
1. Remove 3 duplicate Qwen Token Plan seats from config.yaml (keep individual only)
2. Disable built-in plugins that duplicate config entries
3. FED should be primary, direct providers = fallback
See `provider-quota-diagnostics` SKILL.md "FED-first routing doctrine" section.
