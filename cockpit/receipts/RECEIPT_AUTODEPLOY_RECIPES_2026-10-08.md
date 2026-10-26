# RECEIPT — Auto-deploy recipes (3 files)

**Date:** 2026-10-08 09:48 UTC
**Class:** T0 documentation (no mutation anywhere)
**Trigger:** Arif's "all 3" word at 09:46 UTC.

## What was produced

Three ready-to-paste recipes in `/root/AAA/cockpit/recipes/`. Each is a
standalone guide Arif can execute from his laptop without agent help.

| # | File | Layer | Mutation by whom |
|---|---|---|---|
| 1 | `RECIPE_VPS_CRON_AUTODEPLOY.md` | VPS-side | Arif, via SSH to 72.62.71.199 |
| 2 | `RECIPE_GITHUB_WEBHOOK_AUTODEPLOY.md` | GitHub UI + VPS listener | Arif, via GitHub settings + VPS |
| 3 | `RECIPE_CLAUDECODE_HOOK_AUTODEPLOY.md` | Laptop Claude Code settings.json | Arif, on his own machine |

## What was NOT done (F13 held)

- No mutation to `arif-forge` VPS. No SSH attempted (no key in this container).
- No mutation to `github.com/ariffazil/arif-fazil.com` settings (webhooks).
- No mutation to Arif's laptop Claude Code `~/.claude/settings.json`.
- No mutation to any SKILL.md or tool registry.
- No "autonomous" hook that bypasses F13 — every recipe requires an
  explicit Arif action to install; none auto-push, auto-merge, or
  auto-seal.

## How the three recipes relate

```
Recipe 1 (cron)        — VPS polls every 5 min.  Simple, 5-min lag.
Recipe 2 (webhook)     — GitHub POSTs to VPS.  Real-time, needs TLS.
Recipe 3 (claude code) — Laptop hook on `git push`.  Real-time, per-machine.
```

Arif can pick any one, two, or all three. Recipes 1 + 2 together is
the belt-and-braces option: webhook handles the common case, cron
catches missed deliveries (GitHub does not retry by default). Recipe 3
is independent and useful when Arif is pushing from his laptop
specifically.

## F13 status of the deploy loop right now

- `origin/main` is at `be0d018` (Kinabalu amendment + refinement). ✅
- GitHub Actions `Build — Flagship Site` is green. ✅
- Live site is **still serving the old version** (last-modified
  2026-10-08 04:12:15 UTC for all Kinabalu surfaces). ❌
- None of the 3 recipes is installed yet (they are templates only).

Until Arif executes at least one of the recipes from his laptop, the
Kinabalu branch is merged but not deployed. The agent has done all it
can from this container.

## Membrane compliance

- F13 SOVEREIGN: every recipe is a template. Arif pastes, Arif runs.
- F1 AMANAH: each recipe has a Rollback section (one `crontab -e` away,
  one webhook delete, one settings.json revert).
- F11 AUDITABILITY: each recipe has Step N verification commands.
- F4 CLARITY: each recipe is self-contained — no need to read the
  other two to execute any one of them.
