# SearXNG Archive Restore — Full Recipe

Scenario: `web.backend: searxng` in config, but SearXNG container is gone (moved to
`_archive/<date>/searxng/` during an entropy sweep, never restarted). Agent's `web_search`
fails silently → agent looks broken in group chat. This is a restore, not a behavioral patch.

## 1. Confirm the diagnosis (before touching anything)

```bash
# Is the config still pointing at searxng?
grep -A4 "^web:" ~/.hermes/config.yaml          # all backends = searxng
grep -A3 "^search:" ~/.hermes/config.yaml

# Is searxng actually running? (empty = down)
docker ps --filter name=searxng --format '{{.Names}}\t{{.Status}}'

# Is the compose project still defined?
docker compose ls 2>/dev/null | grep -i searx

# Did it get archived?
ls /root/_archive/*/searxng/ 2>/dev/null
```

If config says searxng but nothing runs and the compose lives in `_archive/` → restore.

## 2. Restore the compose + settings from the archive

```bash
cd /root
mkdir -p /root/searxng
cp /root/_archive/<date>/searxng/docker-compose.yml /root/searxng/
cp /root/_archive/<date>/searxng/settings.yml     /root/searxng/
```

Note: if `/root/searxng/settings.yml` exists as an EMPTY DIRECTORY (a failed earlier
bind-mount attempt), `rmdir` it first — it blocks the bind mount.

## 3. Add the redis sidecar (settings.yml requires it)

`settings.yml` caches via `redis: url: unix:///run/redis-searxng/redis.sock?db=0`.
The archived compose usually does NOT declare redis, and SearXNG without it crash-loops
redis with `Failed opening Unix socket: bind: Permission denied`. Working compose:

```yaml
version: '3.8'
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    depends_on: [redis]
    ports: ["127.0.0.1:8080:8080"]
    environment:
      - SEARXNG_SECRET=${SEARXNG_SECRET:?SEARXNG_SECRET must be set}
      - SEARXNG_BASE_URL=http://localhost:8080
    volumes:
      - ./settings.yml:/etc/searxng/settings.yml:ro
      - searxng-redis-run:/run/redis-searxng
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/search?q=test&format=json"]
      interval: 30s
      timeout: 10s
      retries: 3
  redis:
    image: redis:7-alpine
    container_name: searxng-redis
    # chmod 777 the socket dir: redis runs as non-root, named volume is root-owned
    command: sh -c "chmod 777 /run/redis-searxng && exec redis-server --unixsocket /run/redis-searxng/redis.sock --unixsocketperm 766"
    volumes:
      - searxng-redis-data:/data
      - searxng-redis-run:/run/redis-searxng
    restart: unless-stopped
volumes:
  searxng-redis-data:
  searxng-redis-run:
```

KEY POINT: the `searxng-redis-run` volume must mount into BOTH containers at
`/run/redis-searxng` — redis writes the socket, searxng reads it.

## 4. Pin the project name (COMPOSE_PROJECT_NAME leak)

If the shell exports `COMPOSE_PROJECT_NAME=af-forge`, `docker compose up` resolves the
project to `af-forge` and pollutes the A-FORGE namespace. ALWAYS pin explicitly:

```bash
cd /root/searxng
set -a && source /root/.secrets/kunci-mas.env && set +a
docker compose -p searxng up -d
```

If you accidentally created orphaned containers/volumes under the wrong namespace:
```bash
docker rm -f searxng-redis searxng
docker volume rm -f af-forge_searxng-redis-data af-forge_searxng-redis-run
# then re-up with -p searxng
```

## 5. Verify end-to-end

```bash
sleep 8
docker ps --filter name=searxng --format '{{.Names}}\t{{.Status}}'
# both Up, health: starting → healthy

curl -s -o /dev/null -w 'HTTP %{http_code}\n' 'http://127.0.0.1:8080/search?q=test&format=json'
# HTTP 200

curl -s 'http://127.0.0.1:8080/search?q=<real+query>&format=json' | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print('results:', len(d.get('results',[])))"
# >5 real results

# redis socket visible inside searxng container:
docker exec searxng sh -c 'ls -la /run/redis-searxng/'  # redis.sock present

# then confirm Hermes' own web_search tool works in-session (proves config→backend path)
```

## Troubleshooting

- redis crash-loop `bind: Permission denied` → the `chmod 777` in the redis command
  is missing, or the socket dir volume isn't shared into the searxng container.
- `Conflict. The container name "/searxng-redis" is already in use` → stale container from
  a prior project-name namespace; `docker rm -f` it first.
- Compose `version:` attribute obsolete warning → harmless, can remove.