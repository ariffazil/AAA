---
name: arif-os-docker-host-networking
description: Docker container to host port access in arifOS federation — host.docker.internal with host-gateway mode
---

# arifOS Docker Host Networking

## Problem
Docker containers cannot reach host ports via `172.17.0.1` or `172.19.0.1` bridge IPs. Connection hangs or times out.

## Solution
Add `extra_hosts` to the container's `docker-compose.yml` entry:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

This makes `host.docker.internal` resolve to the Docker host's gateway IP, allowing the container to reach host ports.

## Verified Working Configs

### aaa-a2a container
```yaml
aaa-a2a:
  extra_hosts:
    - "host.docker.internal:host-gateway"
```

From inside `aaa-a2a`:
```bash
curl -s http://host.docker.internal:18001/.well-known/agent-card.json
# ✅ works — reaches Hermes A2A adapter on host port 18001
```

### hermes-agent container
```yaml
hermes-agent:
  extra_hosts:
    - "host.docker.internal:host-gateway"
```

## Key IPs (arifOS Federation)
| Target | Host Port | From Container |
|--------|-----------|----------------|
| Hermes A2A adapter | 18001 | `http://host.docker.internal:18001` |
| gateway-relay | 18002 | `http://host.docker.internal:18002` |
| OpenClaw gateway | 18789 | `http://host.docker.internal:18789` |
| AAA A2A gateway | 3001 | `http://host.docker.internal:3001` |

## Common Mistake
Using `172.17.0.1` or `172.19.0.1` directly — these IPs can change. Always use `host.docker.internal` with `extra_hosts` configured.