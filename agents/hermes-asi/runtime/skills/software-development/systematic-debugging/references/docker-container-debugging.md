# Docker Container Debugging Reference

## Container Lifecycle Basics

### Starting containers
- **`docker compose up -d <service>`** — uses project's docker-compose.yml (or `-f` flag). Respects `container_name`, `image`, `command`, `restart` policy.
- **`docker compose start <service>`** — starts an *existing* stopped container (does NOT recreate from image).
- **`docker compose stop <service>`** — stops without removing the container.
- **`docker run -d --name <name> --restart unless-stopped <image>`** — standalone run. Conflicts if name already exists.

### Critical rule
`docker run` and `docker compose` manage **separate container namespaces**. A container created by `docker run --name arifosmcp` is invisible to `docker compose stop arifosmcp`.

## Container Name Conflicts

### Symptom
```
Error response from daemon: Conflict. The container name "/arifosmcp" is already in use
```

### Root causes
1. **Orphaned container** — created by `docker run` (or a previous compose project with different config) but compose wants to create a *new* one.
2. **Different compose project** — `docker compose -p different_project up` creates containers named `different_project_arifosmcp`, but plain `docker compose up` (default project `arifosmcp`) looks for `arifosmcp_arifosmcp`.

### Resolution sequence
```bash
# 1. Find what has that name
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" | grep arifosmcp

# 2. Check if it's the same compose project
docker inspect <container_name> --format '{{.HostConfig.HostProjectName}}'

# 3. Remove the orphaned container
docker rm -f <container_name>

# 4. Then run compose again
docker compose up -d arifosmcp
```

## Restart Loops

### Symptom
Container shows `Restarting (1) X seconds ago` in `docker ps`.

### Diagnosis
```bash
# Get the current exit code and restart count
docker inspect <name> --format '{{.State.ExitCode}} {{.State.Status}} {{.RestartCount}}'

# Get recent logs (may show the crash)
docker logs <name> --tail 50

# Watch the restart cycle
watch -n1 "docker ps --filter name=<name> --format '{{.Status}}'"
```

### Common causes
| Cause | Symptom | Fix |
|-------|---------|-----|
| Missing module (ModuleNotFoundError) | Crash on import during startup | Rebuild image or use older known-good tag |
| Bad env var | Crash after env expansion | Check `.env`, remove stale vars |
| Port binding failure | `Bind for 0.0.0.0:8080 failed: port is already allocated` | Stop conflicting container |
| Entry point crash | Exit code 1 or 143 | Check logs for traceback |
| Health check failing | `health: starting` forever | Remove or fix healthcheck |

### ModuleNotFoundError in Docker (the today's case)
```
ModuleNotFoundError: No module named 'arifosmcp.runtime.tools_hardened_dispatch'
```
- Means the module existed in source when the image was built, but the entry point changed (new imports added that don't exist in the built image).
- **Fix:** Rebuild image from source, OR use a known-good older image tag.
- **Do NOT:** Keep restarting hoping it fixes itself — the bug is in the image.

## Image Tag vs. Container Behavior

### `docker compose up -d <service>` with image tag change
compose does NOT automatically recreate the container when the image tag changes. It will:
1. Pull the new image (updating the image layer cache)
2. But keep running the old container built from the old image

### To actually restart with new image
```bash
docker compose stop <service>      # Stop container
docker compose rm -f <service>     # Remove container
docker compose up -d <service>    # Recreate from new image
```

Or: `docker compose up -d --force-recreate <service>` (single command but warns about volume conflicts).

## Docker Compose Project Isolation

### The problem
```
docker compose ls
NAME      STATUS    CONFIG FILES
af-forge  running  /root/compose/docker-compose.yml
compose   running  /root/compose/docker-compose.yml  ← same dir!
```

If two compose files in the same directory have different project names (`-p`), they create containers with different name prefixes. But if they share the same project name and same directory, they share the same namespace.

### Inspect project name
```bash
docker inspect <container_id> --format '{{.HostConfig.HostProjectName}}'
```

## Pull Policy Gotchas

### `image:` in compose vs local image
If you have a local image `ghcr.io/ariffazil/arifos:8dfc8b18` and compose pulls `ghcr.io/ariffazil/arifos:5b7de86d`, Docker uses the **local image** if digest matches, not re-pulling. But if the compose file has `pull_policy: always` it forces a pull.

### Quick way to force image update
```bash
# Force pull, ignoring local cache
docker pull ghcr.io/ariffazil/arifos:<tag>

# Or tag the image to match what compose expects
docker tag ghcr.io/ariffazil/arifos:v2026.05.17-0 ghcr.io/ariffazil/arifos:5b7de86d
```

## arifOS-specific notes

### Current known-good tag (as of 2026-05-17)
- `8dfc8b18` — known working before the `tools_hardened_dispatch` import was added to `__main__.py`
- `5b7de86d` — likely same issue (built after the problematic commit)
- `v2026.05.17-0` — latest, likely same issue

### When rebuilding is needed
If all remote tags fail with `ModuleNotFoundError`, build from current HEAD:
```bash
cd /root/arifOS
make build  # uses local Dockerfile, guarantees code-image alignment
```