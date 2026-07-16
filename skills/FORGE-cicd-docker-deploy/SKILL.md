# ⚒️ CI/CD + Docker Deploy — Forge Pipeline

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Build GitHub Actions CI/CD pipelines, Docker multi-stage builds, and deploy→verify patterns for VPS af-forge. Cover test → build → deploy → smoke-test → rollback lifecycle.

## When to Use
- Setting up GitHub Actions workflows for any federation organ repo
- Writing Dockerfiles — multi-stage, distroless, healthcheck
- Deploy pipelines — rsync to `/opt/<organ>/app`, systemd restart, health verify
- Rollback procedures — previous deploy restore, git revert + re-deploy
- Smoke tests after deploy — /health probe + one behavior smoke test

## When NOT to Use
- Local development builds — use organ-specific build commands
- Manual server config — use `forge_infra_guardian` or hostinger-vps
- Database migrations — handled separately in `postgres-schema-design`

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Deploys are reversible — keep previous release, support rollback |
| F2 TRUTH | CI must pass lint + typecheck + test before deploy — no skip flags |
| F4 CLARITY | One Dockerfile per organ, one workflow per deploy target |
| F11 AUDIT | Every deploy logged to VAULT999 with commit hash + image digest |
| F12 INJECTION | Docker images scanned for CVEs before production push |
| F13 SOVEREIGN | Production deploy after green tests is T2 ANNOUNCE; broken tests = 888_HOLD |

## Commands & Patterns

```yaml
# .github/workflows/deploy.yml — canonical pattern
name: Deploy
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run lint && npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/ariffazil/${{ matrix.organ }}:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: |
          ssh af-forge "
            cd /opt/${{ matrix.organ }}/app && \
            git pull && \
            systemctl restart ${{ matrix.organ }} && \
            sleep 3 && \
            curl -sf http://localhost:${{ matrix.port }}/health
          "
```

```dockerfile
# Multi-stage Dockerfile pattern
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine AS production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
HEALTHCHECK --interval=30s CMD node dist/health.js
USER node
CMD ["node", "dist/server.js"]
```

```bash
# Deploy → verify sequence
rsync -az --delete /root/<organ>/ /opt/<organ>/app/
systemctl restart <organ>
sleep 3
curl -sf http://localhost:<port>/health | jq .status
# Behavior smoke test: call one tool and verify expected output
```

## Refusal Surface
- ❌ Deploying without CI passing — broken tests = HOLD
- ❌ Docker images with `latest` tag only (must use commit SHA or date stamp)
- ❌ Skipping health probe after deploy
- ❌ Rolling back without verifying the previous state is stable
- ❌ Exposing Docker socket in CI runners
