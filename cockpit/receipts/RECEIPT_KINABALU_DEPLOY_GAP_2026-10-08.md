# RECEIPT — Kinabalu Deploy Gap (2026-10-08 09:30 UTC)

**Class:** Diagnostic receipt (no mutation; read-only investigation)
**Complements:** RECEIPT_KINABALU_MERGE_TO_MAIN_2026-10-08

## What was confirmed

1. `origin/main` is at `be0d018` (merge completed).
2. `Build — Flagship Site` (run 37756636482) completed with `conclusion=success`
   at 2026-10-08 09:26:54 UTC.
3. The build job is **build-only** by design. The `deploy.yml` header reads:
   `Build validation only. Deploy path: VPS scripts/deploy-vps.sh → /var/www/html/arif`.
4. No deploy step exists in the GitHub Actions workflow. No Cloudflare, R2,
   Vercel, or `wrangler pages deploy` calls in any workflow file.

## What that means

- The `arif-fazil.com` site is published by the VPS (`72.62.71.199`, af-forge)
  using a script at `scripts/deploy-vps.sh` on the VPS itself.
- GitHub Actions produces the build artifact but does not push it anywhere.
- The VPS must pick up the new commit (cron, webhook, or manual SSH run)
  for the live site to refresh.
- From this container, the VPS is not reachable: no SSH key, no deploy token,
  no Cloudflare API token. The agent cannot trigger VPS-side deploy.

## Live site state (post-merge, post-CI)

```
https://arif-fazil.com/earth/kinabalu-cross-section.html
  last-modified: 2026-10-08 04:12:15 UTC   (UNCHANGED from pre-merge)
  cf-cache-status: DYNAMIC
https://arif-fazil.com/earth/kinabalu-basin.pdf
  content-length: 21,335                   (UNCHANGED; expected ~999,184)
  last-modified: 2026-10-08 04:12:15 UTC
  cf-cache-status: REVALIDATED then MISS (refetched from origin, byte-identical)
https://arif-fazil.com/earth/kinabalu-basin/
  last-modified: 2026-10-08 04:12:15 UTC
  cf-cache-status: DYNAMIC

origin body check (cache-bypass):
  "Model A · your hypothesis" / "Model B · Morley" / "Model C" / "Model D"
  → 0 occurrences in /earth/kinabalu-cross-section.html
```

## What unblocks the deploy (Arif can do from laptop)

1. `ssh 72.62.71.199 "cd /opt/arif-sites && bash scripts/deploy-vps.sh"`
   (path inferred; exact form depends on VPS layout).
2. If a cron is already scheduled, wait one cycle (5–15 min typical) and recheck.
3. Cloudflare dashboard → Caching → Purge by URL or Purge Everything, if
   the VPS deploy has updated origin but edge is stuck on stale cache.

## What the agent can do from this container

- Re-probe T1 state (live headers + body markers) every 1–2 min until change
  is observed.
- Not trigger deploy (no VPS or Cloudflare credentials).
- Not push fast-forward to main again (already done).

## Membrane compliance

- F13 SOVEREIGN: merge executed under Arif's word; deploy held under
  membrane because VPS mutation requires credentials the agent does not
  have and Arif must invoke from his trusted machine.
- F2 TRUTH: this receipt records the actual gap, not a fabricated deploy
  success.
