---
name: arifos-docker-compose-env-override-gotcha
description: "arifOS deploy: .env edits don't apply when docker-compose.yml has hardcoded environment: block"
triggers:
  - "JWT_ENFORCE_MODE not taking effect after docker compose restart"
  - "docker compose .env override not working"
  - "environment block overrides env_file in docker compose"
tags:
  - docker
  - docker-compose
  - env
  - arifOS
  - deploy
---

# arifOS Docker Compose Env Override Gotcha

## Problem
When `docker compose up -d --force-recreate` is run, container env vars don't update even after editing `.env`.

## Root Cause
`docker-compose.yml` has an `environment:` block per service that **completely overrides** any matching variable set in `.env`.

```yaml
# docker-compose.yml
arifosmcp:
  env_file: [.env]                    # ← .env loaded FIRST
  environment:
    JWT_ENFORCE_MODE: observe          # ← overrides .env, wins every time
```

## Why Restart Doesn't Work
`docker compose restart` only restarts the container without re-reading compose config. The stale env vars baked into the container at create-time persist.

## Solution
1. Edit the **docker-compose.yml** `environment:` block directly — OR
2. Remove the variable from the `environment:` block so `.env` takes effect

Then force-recreate:
```bash
docker compose up -d --force-recreate <service>
```

## Verification
```bash
# Check what env the container actually has
docker exec <container> env | grep JWT

# Check compose environment block
grep -A5 "environment:" /root/compose/docker-compose.yml | grep JWT
```

## Prevention
When adding env vars to `.env`, always verify the same var isn't hardcoded in `docker-compose.yml`'s `environment:` block.

## Discovery Context
Session 2026-05-05: Arif flipped JWT_ENFORCE_MODE in .env. Container kept starting with `observe`. Full path traced to `environment:` block in compose file. Had to use `--force-recreate` to apply new env.
