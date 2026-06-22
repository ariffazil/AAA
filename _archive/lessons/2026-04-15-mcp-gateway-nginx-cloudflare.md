# Lesson Learned: mcp.arif-fazil.com Gateway + Nginx + Cloudflare (2026-04-15)

## What Happened

Deploying a new nginx config for mcp.arif-fazil.com to route `/geox/mcp` to GEOX MCP backend (:8765) failed publicly despite working locally.

## Root Causes

### 1. Cloudflare Caching 404 Responses (Most Critical)
- **What happened:** After a config error, nginx returned 404 for `/geox/mcp`. Cloudflare cached this 404 response globally.
- **Symptom:** `curl https://mcp.arif-fazil.com/geox/mcp` → `HTTP/2 421` (Cloudflare cached error)
- **Why it persisted:** CF cached the 404, so even after fixing nginx, public requests still got the cached error.
- **CF lesson:** CF caches negative responses aggressively. Always purge cache after any backend config change.

### 2. Duplicate Nginx Server Blocks
- **What happened:** A previous `tee -a` appended a second `server { listen 80; ...}` block to the config file instead of replacing it. Nginx loads the first block and ignores the second.
- **Symptom:** Config was syntactically valid but had two conflicting `listen 80` blocks.
- **Lesson:** When editing nginx configs, always overwrite (`>`) not append (`tee -a`). Better: use `cat > file << EOF`.

### 3. Two Nginx Instances (Port Ghost)
- **What happened:** Multiple `nginx -s reload` calls while debugging left two nginx master processes running. The old process kept the old config, new requests went to old process.
- **Symptom:** `curl http://127.0.0.1:80/geox/mcp` → 404 even though new config was reloaded.
- **Fix:** `killall nginx` then `sudo nginx` (start fresh).
- **Lesson:** Never do `nginx -s reload` repeatedly in scripts. Kill and restart cleanly.

### 4. Host Header Rejection by GEOX Backend
- **What happened:** GEOX MCP at :8765 uses FastMCP's HTTP transport, which validates the Host header. Proxying with `proxy_set_header Host $host` sent `Host: mcp.arif-fazil.com` which GEOX rejected.
- **Symptom:** `HTTP/1.1 400 Bad Request — Invalid Host header`
- **Fix:** Use `proxy_set_header Host $proxy_host` instead — sends `Host: 127.0.0.1:8765` which the backend accepts.
- **Lesson:** Not all backends accept arbitrary Host headers. `$proxy_host` (the upstream hostname) works universally.

### 5. Cloudflare Token Permissions
- **What happened:** First CF API token lacked "Cache Purge" permission — could read zones but not purge.
- **Symptom:** `{"code": 1000, "message": "Invalid API Token"}` on purge endpoint.
- **Fix:** Used a replacement Cloudflare token with cache-purge permission (`[REDACTED_CLOUDFLARE_TOKEN]`) which worked.
- **Lesson:** Always test CF tokens for the specific permission needed, not just verify they work for reads.

## Key Rules for Future Nginx + Cloudflare Deployments

### Before Any Nginx Change
1. Run `sudo nginx -t` to validate syntax
2. Kill existing nginx cleanly: `sudo killall nginx; sleep 2`
3. Start fresh: `sudo nginx`
4. Test locally first: `curl http://127.0.0.1:80/<path>`
5. Only then test public HTTPS

### Cloudflare Cache Strategy
1. After ANY backend config change, purge CF cache immediately
2. Test token has "Zone → Cache Purge" permission before deployment
3. If cache is stuck with bad response, wait 2-5 min for TTL expiry OR purge via dashboard

### Nginx Config Best Practices
- Use `cat > file << 'EOF'` not `tee -a` for config edits
- One `server {}` block per file per port
- Use `proxy_set_header Host $proxy_host` for backend proxying (not `$host`)
- Use prefix `location /path/ {}` not regex `location ~ ^/path$` unless exact matching required
- Always restart (not reload) after config changes during debugging

## Cloudflare Pages Parallels (from CF guide)

The issues we hit map to known CF failure patterns:
- "Deploy succeeds but site does not update" (rank #2) = our 404 cache
- "Wrong deploy command" (rank #4) = our proxy_set_header mismatch  
- "Old assets after deployment" (rank #14) = our stale CF cache
- "Support path weak" (rank #15) = CF token permissions issue

Full reference: `/root/.openclaw/workspace/lessons/cloudflare_pages_troubleshooting_guide.md`
