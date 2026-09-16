# LiteLLM Import Hang on Python 3.13 — 2026-08-28

## Symptom
- `litellm-federation.service` starts but never binds to port 4011
- Process consumes CPU (80-90%) and RAM (600MB+) but no port listener
- `ss -tlnp | grep 4011` shows nothing (or only tailscaled proxy)
- `curl http://127.0.0.1:4011/health` times out
- HAProxy :4000 returns 503 (no backend)

## Root Cause
litellm 1.90.2 `import litellm` hangs indefinitely on Python 3.13.7.
The import chain (via `__init__.py`) triggers heavy module loading that
never completes. strace shows no network calls — it's a pure import deadlock.

## Diagnostic
```bash
# Quick test: does import complete within 10 seconds?
timeout 10 python3 -c "import litellm; print('OK')" 2>&1
# If no output → import hang confirmed

# Check process is running but not listening
ps aux | grep litellm | grep -v grep
ss -tlnp | grep 4011

# Check systemd status
systemctl status litellm-federation.service
journalctl -u litellm-federation.service -n 20 --no-pager
```

## What Does NOT Work
- Restarting the service (same hang every time)
- `pip install --force-reinstall litellm` (also hangs on PEP 668 + slow install)
- Running litellm manually with clean env (same import hang)
- `env -i` minimal environment (still hangs)

## What WORKS — Python 3.12 Venv (Verified 2026-08-28)

### Fix
```bash
# 1. Create Python 3.12 venv (3.12 available at /root/.local/share/uv/python/)
uv venv /root/litellm-venv --python /root/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/bin/python3.12

# 2. Install litellm + deps
uv pip install --python /root/litellm-venv/bin/python "litellm[proxy]>=1.70.0,<1.80.0"
uv pip install --python /root/litellm-venv/bin/python prometheus_client

# 3. Update systemd override
sudo sed -i 's|exec /usr/local/bin/litellm|exec /root/litellm-venv/bin/litellm|' \
  /etc/systemd/system/litellm-federation.service.d/override.conf
sudo sed -i 's|TimeoutStartSec=300|TimeoutStartSec=600|' \
  /etc/systemd/system/litellm-federation.service.d/override.conf

# 4. Restart
sudo systemctl daemon-reload
sudo systemctl restart litellm-federation.service

# 5. Wait 90-120s for litellm import chain to complete, then verify
sleep 120
curl -s http://127.0.0.1:4000/health/liveliness  # should return "I'm alive!"
ss -tlnp | grep 4011  # should show litellm listening
```

### Why It Works
- Python 3.12.13 has compatible import machinery for litellm's heavy init chain
- `LITELLM_LOCAL_MODEL_COST_MAP=True` prevents model cost map download at import
- `prometheus_client` is required by litellm_enterprise but not auto-installed
- TimeoutStartSec=600 needed because import takes 60-90s on this VPS

### Notes
- litellm `/health` (full) may still time out — use `/health/liveliness` for health checks
- HAProxy `/health/liveliness` returns 200 OK — FED is alive
- Wawa node connects via Tailscale mesh to 100.64.0.2:4000

## Impact
- FED (port 4000) returns 503
- All agent model routing through FED is dead
- Wawa node can't reach FED
- Gemini/Ollama fallback still works locally

## Timeline
- 2026-08-27 ~11:14 UTC: litellm killed (TERM, 6h uptime, 1GB peak)
- 2026-08-28 ~00:49 UTC: Restart attempted, import hang confirmed
- 2026-08-28 ~04:48 UTC: Python 3.12 venv fix applied, FED restored
