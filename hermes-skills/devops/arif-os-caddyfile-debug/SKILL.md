---
name: arif-os-caddyfile-debug
description: Debug 404/502/308 on arifOS surfaces — wrong root path, wrong proxy port, image sync
category: devops
tags: [caddy, docker, arifOS, deployment]
last_updated: 2026-05-04
---

## NEW (2026-05-04): Remove Cloudflare DNS challenge entirely

### Symptom: "API token appears invalid" — even with correct token

```
Error: provision tls.issuance.acme: loading DNS provider module: loading module 'cloudflare':
API token '' appears invalid
```

**Root cause:** The Caddyfile has `tls { dns cloudflare {env.CLOUDFLARE_API_TOKEN} }`.
When Caddy is started with `sudo`, the root process can't read the user's env vars.
The token exists in `os.environ` (visible via `python3 -c "import os; print(os.environ['CLOUDFLARE_API_TOKEN'])"`)
but isn't available to `sudo caddy` — even with `sudo -E`.

**Option A (RECOMMENDED): Remove Cloudflare DNS challenge entirely**
Simplify Caddyfile. Use Let's Encrypt HTTP-01 ACME directly. Caddy handles TLS automatically.
Cloudflare becomes irrelevant — grey or orange cloud doesn't matter.

Remove this block from Caddyfile global options:
```
# DELETE THIS:
(tls_origin) {
    tls {
        dns cloudflare {env.CLOUDFLARE_API_TOKEN}
    }
    ...
}
```

Replace `import tls_origin` on each site with a header-only block:
```
arif-fazil.com {
    header {
        Strict-Transport-Security "max-age=15552000; includeSubDomains; preload"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "SAMEORIGIN"
        Referrer-Policy "strict-origin-when-cross-origin"
        -cf-ray
        -cf-request-id
        -server
        Access-Control-Allow-Origin *
        Access-Control-Allow-Methods "GET, POST, OPTIONS"
    }
    ...
}
```

This works because: Caddy gets its own cert from Let's Encrypt via port 80 ACME challenge.
Cloudflare just forwards port 443 traffic. No Cloudflare token needed.

**Option B: Extract token and pass explicitly**
```bash
# Get token from current shell Python
python3 -c "import os; print(os.environ.get('CLOUDFLARE_API_TOKEN',''))"
# Output: ***CF_TOKEN_REDACTED***

# Start Caddy with explicit env vars
CLOUDFLARE_API_TOKEN='cfat_InkyL9...' sudo caddy run --config /root/arifOS/Caddyfile --adapter caddyfile
```

---

## NEW (2026-05-04): Git rebase conflict in rest_routes.py

When merging Caddyfile hotfix branches to main via rebase, Python files can conflict
if both branches modified `rest_routes.py`.

**Common conflict:** `from .floors import` vs `from arifosmcp.runtime.floors import`
The absolute import (no leading dot) is correct — the module is a sibling of `rest_routes/`, not inside it.

```bash
cd /root/arifOS
git diff --name-only --diff-filter=U  # shows conflicted files
# The conflict marker looks like:
#   <<<<<<< HEAD
#   from .floors import get_floor_count
#   =======
#   from arifosmcp.runtime.floors import get_floor_count
#   >>>>>>> <commit>

# Fix: keep the absolute import
git add arifosmcp/runtime/rest_routes/rest_routes.py
git commit --no-edit
git rebase --continue
```

---

## NEW (2026-05-04): Systemd caddy.service using wrong config

Systemd's default caddy service uses `/etc/caddy/Caddyfile` (not `/root/arifOS/Caddyfile`).
Even if you `systemctl enable caddy`, it uses the wrong file.

**Fix — create override:**
```bash
sudo systemctl unmask caddy
sudo mkdir -p /etc/systemd/system/caddy.service.d
sudo tee /etc/systemd/system/caddy.service.d/override.conf > /dev/null << 'EOF'
[Service]
ExecStart=
ExecStart=/usr/bin/caddy run --config /root/arifOS/Caddyfile --adapter caddyfile
ExecReload=
ExecReload=/usr/bin/caddy reload --config /root/arifOS/Caddyfile --adapter caddyfile
User=root
Group=root
EOF
sudo systemctl daemon-reload
sudo systemctl restart caddy
```

---

## NEW (2026-05-04): Port 443 conflict

```
Error: listening on :443: bind: address already in use
```

Another Caddy is already running. Kill all and restart:
```bash
sudo pkill -f "caddy"
sleep 2
sudo caddy run --config /root/arifOS/Caddyfile --adapter caddyfile
```

---

## Key Principle

**Caddy + Let's Encrypt + Cloudflare:** Caddy gets its own TLS cert directly from Let's Encrypt.
Cloudflare just forwards traffic. Whether Cloudflare proxy is grey (DNS-only) or orange (CDN+TLS) doesn't affect Caddy's ability to serve HTTPS. The only requirement: port 80 and 443 must be open and reachable.
### Fix 8: `handle` path matching with dots — use named matchers
- Symptom: `handle /.well-known/mcp/server-card.json { file_server }` — adapted JSON looks correct but returns 404
- Root cause: Caddy's `handle` directive path matcher doesn't correctly handle paths with multiple dot-segments
- Fix: Use named matchers explicitly:
```caddy
# WRONG:
handle /.well-known/mcp/server-card.json {
    file_server
}

# CORRECT:
@mcp-server-card {
    path /.well-known/mcp/server-card.json
}
handle @mcp-server-card {
    file_server
}

# Multiple paths with dots:
@api-mcp {
    path /api/mcp/tools.json /api/mcp/resources.json
}
handle @api-mcp {
    file_server
}
```

### Fix 9: Cloudflare cached 404 — change path as workaround
- Symptom: File exists inside Caddy (`docker exec caddy cat /var/www/html/arifos/.well-known/mcp/server-card.json` returns correct JSON), but external `curl` returns 404 from Cloudflare
- Confirm it's Cloudflare: response `content-type: text/plain` (not `application/json`) = Cloudflare error page, not Caddy
- Verify Caddy origin: `docker exec caddy wget -q -O - --header "Host: arifos.arif-fazil.com" "http://localhost/.well-known/mcp/server-card.json"` returns JSON → Caddy is fine, Cloudflare cached old 404
- If Cloudflare token lacks `cache_purge` permission (API returns `{"success":false,"errors":[{"code":10000,"message":"Authentication error"}]}`), change the URL path instead:
  - Old: `/.well-known/mcp/server-card.json` (cached 404)
  - New: `/mcp-server-card.json` (same content, fresh route)
- Verify token permissions: `curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"`

### Fix 10: Always read the running container's Caddyfile as ground truth
- `docker exec caddy cat /etc/caddy/Caddyfile` — this is what Caddy is actually using
- `docker exec caddy caddy validate --config /etc/caddy/Caddyfile 2>&1` — validates the loaded config
- Check adapted JSON: `docker exec caddy sh -lc "cat /config/caddy/autosave.json" | python3 -c "..."` — see how Caddy interpreted the Caddyfile
- If `reload` doesn't apply changes: `docker restart caddy` (full restart, not just reload)
- The active Caddyfile on this VPS is `/root/arifOS/Caddyfile` (bind-mounted as `/etc/caddy/Caddyfile` in the container)

## Context
When arifOS surfaces return unexpected 404/502/308, the Caddyfile often has one of three bugs:
1. **Wrong root path** — Caddyfile says `/var/www/html/arifOS` but mount is `/var/www/html/arifos` (case mismatch)
2. **Wrong proxy port** — Caddyfile proxies to `arifosmcp:3000` but container listens on port 8080
3. **Wrong network** — Caddy and arifosmcp on different Docker networks; must use same network

## Diagnostic Pattern

### Step 1: Identify the running container's actual state
```bash
# Get container name + image
docker ps --format "{{.Names}}\t{{.Image}}" | grep arif

# Get actual exposed ports (don't trust compose — read the container)
docker inspect <container> --format '{{json .NetworkSettings.Ports}}' | python3 -m json.tool

# Get container networks + IPs
docker inspect <container> --format '{{range $k,$v:=.NetworkSettings.Networks}}{{$k}}:{{.IPAddress}} {{end}}'
```

### Step 2: Test Caddy routes from INSIDE the Caddy container
```bash
CADDY=$(docker ps --format "{{.Names}}" | grep -i caddy | head -1)

# Test with Host header (bypasses Cloudflare cache, no --resolve needed)
docker exec $CADDY wget -q -O - --header "Host: domain.com" http://localhost/path

# Get HTTP status code
docker exec $CADDY wget -q --spider --header "Host: domain.com" http://localhost/path 2>&1 | grep -oP 'HTTP/\d\.\d \K\d+'

# Check what Caddyfile is actually loaded (compare with host source)
docker exec $CADDY cat /etc/caddy/Caddyfile > /tmp/caddy_loaded.conf
diff /root/arifOS/Caddyfile /tmp/caddy_loaded.conf

# Reload Caddy after fix
docker exec $CADDY caddy reload --config /etc/caddy/Caddyfile 2>&1 | grep -E "info|warn|error"
```

### Step 3: Identify common fixes

**Fix 1: Wrong root path (arifOS/arifos case)**
```caddy
# Wrong:
root * /var/www/html/arifOS

# Correct:
root * /var/www/html/arifos
```

**Fix 2: Wrong proxy port**
```caddy
# Wrong (port mismatch):
reverse_proxy arifosmcp:3000

# Correct (port inside container):
reverse_proxy arifosmcp:8080
```

**Fix 3: 308 redirect from Caddy (file exists but browser redirects)**
- Caddy returns `308 Permanent Redirect` when path requires HTTPS and browser hits HTTP
- Use `curl -L` or `wget -L` to follow redirect and confirm content is there
- The 308 is correct behavior — just use `-L` to verify

**Fix 4: arifOS/arifOS hostname spelling in Caddyfile**
- Caddyfile at `/root/arifOS/Caddyfile` block at line 139 starts with `arifos.arif-fazil.com` (no capital O)
- Always check hostname spelling in Caddyfile vs what Cloudflare DNS points to

**Fix 5: Cloudflare serves cached 404 even when origin is correct**
- Symptom: `curl` from outside returns "Not Found" with `content-type: text/plain;charset=UTF-8` — Cloudflare cache. Inside container, `docker exec caddy cat /path/file.json` returns correct JSON
- Confirm: Check response headers — if `cf-cache-status` or `age` header present, it's cached. If `content-type: text/plain` (not `application/json`), it's definitely Cloudflare's error page
- First try: Cloudflare dashboard cache purge (or API purge)
- If token lacks `cache_purge` permission: **change the URL path** — rename to a fresh path (`/mcp-server-card.json` instead of `/.well-known/mcp/server-card.json`), update Caddyfile, restart Caddy, update all links
- Verify origin directly: `docker exec caddy wget -q -O - --header "Host: arif-fazil.com" "http://localhost/.well-known/arif-human.json"` — should return JSON from container if files exist

**Fix 6: `handle_path` directive creates nested subroute handler — use `@matcher` + `uri strip_prefix` instead**
- Symptom: `handle_path /.well-known/* { root * /var/www/html/arif/.well-known file_server }` produces correct adapted JSON but still returns 404 in browser (Cloudflare-cached or actual)
- Root cause: `handle_path` is syntactic sugar that wraps the block as a nested subroute. It runs after other matchers in the same site block. The `uri strip_prefix /.well-known` on a `@well-known` named matcher + `handle @well-known` is the cleaner pattern
- Correct pattern:
```caddy
@well-known { path /.well-known/* }
handle @well-known {
    uri strip_prefix /.well-known
    root * /var/www/html/arif/.well-known
    file_server
    try_files {path} /index.html
}
```
- Same for `/000/*` and `/999/*` chambers — all use named matchers + `uri strip_prefix`
- The SPA catch-all (`handle { file_server try_files {path} /index.html }`) must be LAST and should not have `strip_path_prefix` since it serves the root index.html

**Fix 7: SPA catch-all eats `.json` and `.txt` files**
- Symptom: `.json` files in subdirs return HTTP 200 with HTML "404: Not Found" page instead of JSON
- Root cause: `try_files {path} /index.html` — when exact path file exists but Caddy can't serve it (wrong root, or path strip issue), the fallback is the index.html page, which itself has a 404
- When `uri strip_prefix` is properly configured and root is set to the subdir, `file_server` should serve the exact file before falling back to index.html. If not, check the root path is correct

### Step 4: Image sync issue (compose vs reality)
- Symptom: File exists on disk (`docker exec caddy cat /var/www/html/arif/999/credentials.json` returns JSON), but browser gets HTML with "404: Not Found" title and HTTP 200
- Root cause: Caddyfile uses `try_files {path} /index.html` — when a file doesn't exactly match, Caddy serves the index.html page with HTTP 200. Even when `.json` files exist, the exact path match fails if the route structure doesn't explicitly handle the path before the catch-all
- The `/.well-known/` route is nested INSIDE the arif-fazil.com block AFTER the `_shared` handle, not as a top-level catch-all — it never gets a direct `handle` block, so it falls through to the catch-all
- Fix: Add explicit `handle /.well-known/*` block AND `handle /999/*.json` block with `try_files $uri` before the SPA fallback
```caddy
# Add BEFORE the catch-all file_server block:
handle /.well-known/* {
    root * /var/www/html/arif
    file_server
    try_files {path}
}
handle /999/*.json {
    root * /var/www/html/arif/999
    file_server
    content-type application/json
    try_files {path}
}
```
- Also: `handle /llms.txt` needs explicit route since `.txt` files in root fall to catch-all
- Verify: `docker exec caddy curl -s -o /dev/null -w "%{http_code}" "http://localhost/.well-known/did.json" -H "Host: arif-fazil.com"` should return 200, not 308 or 404

### Step 4: Image sync issue (compose vs reality)
```bash
# Container running different image than compose specifies
docker kill <container>
docker rm -f <container>
cd /root/compose && docker compose up -d arifosmcp
```

## Key Files
- **Authoritative Caddyfile**: `/root/arifOS/Caddyfile` (bind-mounted to container as `/etc/caddy/Caddyfile`)
- **Sites root**: `/root/sites/` (bind-mounted to container as `/var/www/html`)
- **Compose**: `/root/compose/docker-compose.yml` (desired state, not always live)

- **arifOS Caddyfile sync gotcha:**
  - `docker compose up -d --force-recreate caddy` forces a full container recreate so the bind-mounted Caddyfile at `/etc/caddy/Caddyfile` gets a fresh read from host — plain `reload` alone was not picking up source-file changes because Caddy re-reads the config file but doesn't re-evaluate the file mount on `reload`
  - Always verify running config matches source: `diff <(docker exec caddy cat /etc/caddy/Caddyfile) /root/arifOS/Caddyfile`
  - Symptom: you patch the source Caddyfile but the running container still shows old content — recreate the container, don't just reload
  - Cloudflare Worker routes on `.well-known/*` caused HTTP 404 at the edge even when Caddy served HTTP 200 — remove Workers blocking those routes via the Cloudflare API

## Network Topology
- **arifosmcp container listens on port 8080** (UVICORN_DEFAULT_HOST=0.0.0.0:8080 in container)
- Caddy proxies to `arifosmcp:8080` (NOT 3000 — 3000 is the Docker host port mapping, not the container internal port)
- The active compose file that controls running containers is: `/root/arifOS/deployments/af-forge/docker-compose.yml`
- `/root/compose/docker-compose.yml` is the desired-state compose but NOT what Docker is currently using
- The af-forge compose file was never committed to git — find it with: `find /root -path "*/af-forge/docker-compose.yml"`

## Critical: Find What Actually Controls Your Containers
```bash
# 1. Find which compose file created the running container
docker inspect arifosmcp --format '{{index .Config.Labels "com.docker.compose.project.config_files"}}'

# 2. Get the container creation timestamp (to know if it predates any compose changes)
docker inspect arifosmcp --format '{{.Created}}'

# 3. Check live port bindings (don't trust compose — read the container)
docker inspect arifosmcp --format '{{json .HostConfig.PortBindings}}' | python3 -m json.tool

# 4. Check what networks the container is actually on
docker inspect arifosmcp --format '{{range $k,$v:=.NetworkSettings.Networks}}{{$k}}:{{.IPAddress}} {{end}}'
```

## Critical: Bind-Mount Git Checkout Gotcha (2026-04-30)
When a file is bind-mounted into a Docker container, `git checkout -- file` FAILS even after `docker stop`:
```
error: unable to unlink old 'Caddyfile': Device or resource busy
rm: cannot remove 'Caddyfile': Device or resource busy
```
The bind mount holds an open inode reference that prevents unlinking.

**Solution — copy from git HEAD instead:**
```bash
# Get content directly from git object store (bypasses worktree)
git show HEAD:Caddyfile > /tmp/Caddyfile.backup
cp /tmp/Caddyfile.backup /root/arifOS/Caddyfile

# Or use git cat-file pipeline:
git cat-file -p HEAD:Caddyfile > /root/arifOS/Caddyfile
```

**Then reload Caddy:**
```bash
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
docker exec caddy caddy validate --config /etc/caddy/Caddyfile
```

**Why `docker stop` alone doesn't help:** The bind mount is a host-level kernel mount. Stopping the container only stops the process — the mount still holds the inode. Only unmounting the file releases it. On this VPS, unmounting isn't easy (requires host access), so the copy-from-git workaround is preferred.

## Key Files
- **Authoritative Caddyfile**: `/root/arifOS/Caddyfile` (bind-mounted to container as `/etc/caddy/Caddyfile`, read-only)
- **Sites root**: `/root/sites/` (bind-mounted to container as `/var/www/html`)
- **Active compose (controls running containers)**: `/root/arifOS/deployments/af-forge/docker-compose.yml`
- **Desired-state compose (NOT always live)**: `/root/compose/docker-compose.yml`

## Pre-edit checklist
1. Always `git show HEAD:Caddyfile > /tmp/Caddyfile.orig` before editing — this is your revert target
2. After edit: `cp new_Caddyfile /root/arifOS/Caddyfile`
3. Validate: `docker exec caddy caddy adapt --config /etc/caddy/Caddyfile`
4. Reload: `docker exec caddy caddy reload --config /etc/caddy/Caddyfile`
5. Test: `curl -sI https://arif-fazil.com/000 | head -1`

## Verification Checklist
After any Caddyfile fix:
1. Caddy reloads without error (`adapted config to JSON`)
2. arifOS.arif-fazil.com/ → `<title>arifOS // Sovereign Compute Federation</title>` 200
3. mcp.arif-fazil.com/health → JSON health from arifosmcp 200
5. arif-fazil.com/000/ → title `/000 — Wisdom Wall for AI` 200
6. arif-fazil.com/999/ → title `/999 — Verification Room for AI` 200
7. arif-fazil.com/.well-known/did.json → JSON body (not HTML), HTTP 200
8. arif-fazil.com/.well-known/arif-human.json → JSON body (not HTML), HTTP 200
9. arif-fazil.com/999/credentials.json → JSON body (not HTML), HTTP 200
10. arif-fazil.com/llms.txt → plain text (not HTML 404)
5. arif-fazil.com/999/ → title `/999 — Verification Room for AI` 200