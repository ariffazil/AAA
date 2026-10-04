# HAProxy Health Check Key Fix — 2026-08-09

## Symptom

FED :4000 returns 503 "No server is available to handle this request" even though:
- `litellm-federation.service` is active and running
- `ss -tlnp | grep 4011` shows the port is listening
- `curl 127.0.0.1:4011/health -H "Authorization: Bearer $LITELLM_MASTER_KEY"` returns HTTP 200

## Root cause

HAProxy's `http-check send hdr Authorization "Bearer <key>"` in `/etc/haproxy/haproxy.cfg`
contained a placeholder/redacted key (`sk-lit...74ed`) instead of the real
`LITELLM_MASTER_KEY`. HAProxy's health check fails with Layer7 timeout → marks
the backend as DOWN → 503 to all clients.

## Diagnosis steps

```bash
# 1. Check HAProxy logs for backend DOWN
journalctl -u haproxy --no-pager -n 10 | grep "DOWN\|UP\|NOSRV"
# Look for: "Server llm_nodes/fed_primary is DOWN, reason: Layer7 timeout"

# 2. Verify backend is actually listening
ss -tlnp | grep 4011

# 3. Verify backend responds with real key
source /root/.secrets/kunci-mas.env
curl -s -o /dev/null -w "HTTP: %{http_code}" http://127.0.0.1:4011/health \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"
# Should be HTTP 200

# 4. Check what key HAProxy is using
grep "Bearer" /etc/haproxy/haproxy.cfg
# Compare suffix with real key
echo "Real key suffix: ...${LITELLM_MASTER_KEY: -6}"
```

## Fix

```bash
source /root/.secrets/kunci-mas.env

# Backup
cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.bak

# Replace placeholder with real key
sed -i "s|sk-lit\.\.\.74ed|${LITELLM_MASTER_KEY}|" /etc/haproxy/haproxy.cfg

# Validate config
haproxy -f /etc/haproxy/haproxy.cfg -c

# Reload
systemctl reload haproxy

# Verify fix
sleep 2
curl -s -o /dev/null -w "HTTP: %{http_code}" http://127.0.0.1:4000/health \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY"
# Should be HTTP 200 (not 503)
```

## Also check: litellm-federation stuck in deactivating

Sometimes the service gets stuck in `deactivating (stop-sigterm)` state.
`systemctl status` shows "active" but the port isn't listening.

```bash
ss -tlnp | grep 4011  # if empty, port isn't listening
systemctl restart litellm-federation
# Wait 15-20s for prisma migration to complete
sleep 20
ss -tlnp | grep 4011  # should now show litellm listening
```

## FED architecture (port map)

```
HAProxy :4000 (front door, /etc/haproxy/haproxy.cfg)
  ├── fed_primary → 127.0.0.1:4011 (litellm-federation, 5 providers)
  └── escape_backup → 127.0.0.1:4012 (litellm-escape, DeepSeek + MiMo only)

fed-clean-proxy :4001 (strips Responses API features for Codex CLI)
mimo_vision_shim :4002 (Hermes vision path)
```

All three (:4000, :4001, :4002) are NOT zombies — each serves a specific consumer.
Do not kill any without checking who uses it.
