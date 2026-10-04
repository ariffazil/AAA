# Kernel Deploy Verification — The Permission Pitfall + Manual Restart Fallback

> **Source:** 2026-08-08j session (Hermes deploying floor_passed fix).
> **Lesson:** rsync as root overwrites file ownership → `arifos` user cannot read → PermissionError → kernel fails silently on restart. Plus: systemctl may rate-limit rapid restarts.

## The error

```
PermissionError: [Errno 13] Permission denied: '/opt/arifos/app/arifosmcp/resources/floor_table.py'
```

The file was `644 root:root` after `rsync -a ... /root/arifOS/ → /opt/arifos/app/`. The kernel runs as user `arifos` and cannot open 600/644 files owned by root.

## The fix (post-rsync, before restart)

```bash
chown -R arifos:arifos /opt/arifos/app/arifosmcp/
chmod -R u+rwX /opt/arifos/app/arifosmcp/
```

Always run AFTER rsync, BEFORE restart. This is the arifOS deploy path — source = root-owned, runtime = arifos-owned.

## The systemctl rate-limit trap

`systemctl restart arifos` may fail with `Start request repeated too quickly` after 2+ rapid failed starts. The solution: manual launch.

```bash
# Manual restart as arifos user
su arifos -s /bin/bash -c "
  cd /opt/arifos/app &&
  export ARIFOS_VAULT_DIR=/var/lib/arifos/vault &&
  /opt/arifos/venv/bin/python -c 'from arifosmcp.runtime.__main__ import main; main()'
" 2>&1
```

Wait 8–10 seconds for boot, then check:
```bash
ss -tlnp | grep 8088 | grep -v tailscaled
curl -sf http://127.0.0.1:8088/health | python3 -c "import json,sys; print(json.load(sys.stdin)['status'])"
```

## Deployment marker update

The systemd unit's `ExecStartPost` runs:
```bash
cd /root/arifOS && git rev-parse HEAD > /opt/arifos/app/.git_commit
```
This updates the marker on every systemd restart. For manual restarts, update it yourself:
```bash
SOURCE_SHA=$(git -C /root/arifOS rev-parse HEAD)
echo "$SOURCE_SHA" > /opt/arifos/app/.git_commit
```

## Full deploy recipe (K9 + this file)

```bash
# 1. Source edits done. Commit to /root/arifOS.

# 2. Clear pycache (chronic blocker per K4)
find /root/arifOS/arifosmcp -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null
find /opt/arifos/app/arifosmcp -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null

# 3. Sync source → runtime (K9: --checksum to prove copy happened)
rsync -rt --checksum \
  --exclude='.git' --exclude='.venv' --exclude='venv' --exclude='__pycache__' \
  --exclude='*.pyc' --exclude='node_modules' --exclude='.env' --exclude='data/' \
  --exclude='logs/' --exclude='VAULT999/' --exclude='.git_commit' \
  --exclude='heuristik_caches' \
  /root/arifOS/ /opt/arifos/app/

# 4. Fix permissions (this file's lesson)
chown -R arifos:arifos /opt/arifos/app/arifosmcp/
chmod -R u+rwX /opt/arifos/app/arifosmcp/

# 5. Update marker
SOURCE_SHA=$(git -C /root/arifOS rev-parse HEAD)
echo "$SOURCE_SHA" > /opt/arifos/app/.git_commit

# 6. Restart (try systemctl first, fall back to manual)
systemctl restart arifos 2>/dev/null && sleep 6
# If systemctl fails (rate limit), use manual method above.

# 7. Verify
curl -sf http://127.0.0.1:8088/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'status={d[\"status\"]} drift={d[\"deployment_drift_status\"]} '
      f'deployed={d[\"software_release\"][\"deployed_commit\"][:8]}')"
```
