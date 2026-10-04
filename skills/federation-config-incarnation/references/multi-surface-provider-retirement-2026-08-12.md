# Multi-Surface Provider / Key Retirement

> Captured 2026-08-12 from the Tavily purge sweep. Class of work: retire a provider/API key/dependency that touches more than one surface (env SOT, env consumer, runtime config, skill docs).

## Why this exists

A retired provider leaves residue across the federation. Each residue source is a future F12 injection vector, F2 truth violation (config lying about capability), or F11 audit gap. Retire deliberately, surface by surface.

## The 4 surfaces (verified)

| # | Surface | Path | Action |
|---|---|---|---|
| 1 | Env SOT | `/root/.secrets/kunci-mas.env` | `export KEY="..."` → `# RETIRED <date> — <reason>` |
| 2 | Env whitelist | same file, `ARIFOS_ENV_WHITELIST` line | Remove `<PROVIDER>_\|` prefix |
| 3 | Flat env consumer | `/root/.secrets/kunci-mas.flat.env` | `make -f /root/.secrets/Makefile vault-generate` |
| 4 | Skill docs | `*.md` files in `skills/devops/` | `~~Provider~~ \| RETIRED <date>` |

Surfaces NOT touched (historical/forensic):

- `.bak` files (e.g. `kunci-mas.env.bak.20260804...`)
- `.archive-config-backups/`
- `.curator_backups/`
- `.quarantine-*/`
- `tmp/` checkpoints (subsession scratch)

## Backup protocol (T1 reversible)

```bash
# BEFORE first mutation, snapshot the file
cp /root/.secrets/kunci-mas.env /root/.secrets/kunci-mas.env.bak.<reason>-cleanup
# Restore: cp back, then re-run vault-generate
```

## Verified check (4 outputs all must match)

```bash
# 1. SOT has no active export
grep -c "export <KEY>=" /root/.secrets/kunci-mas.env            # 0

# 2. SOT whitelist pruned
grep "<PROVIDER>_" /root/.secrets/kunci-mas.env                  # 0

# 3. Flat env consumed by systemd has no key
grep -c <KEY> /root/.secrets/kunci-mas.flat.env                  # 0

# 4. Skill markdown cleaned (active paths only)
grep -rn "<provider>" /root/.secrets/ /root/.hermes/config.yaml \
  /root/HERMES/skills/devops/ 2>/dev/null \
  | grep -v ".bak\|archive\|quarantine"                         # should show only RETIRED annotations
```

## Shell env vs runtime env drift

After `source /root/.secrets/kunci-mas.env`, the active shell still holds the in-memory value. systemd and child processes started AFTER `vault-generate` read the clean flat.env. **No restart needed** for pure env cleanup — only for services that cached values in-process (none in the standard federation stack).

## When to extend the surface list

If the retirement touches:

- `litellm-config.yaml` → add Surface 5: provider config (search/replace via litellm-tools or restart-required)
- `/etc/systemd/system/` drop-ins → add Surface 5: systemctl daemon-reload
- MCP server binaries/plugins → add Surface 5: plugin registry disable

When the surface list grows beyond 4, convert the recipe into a script:

```bash
#!/bin/bash
# scripts/retire_provider.sh
PROVIDER="$1"
# ... surfaces 1-6 with per-surface assertions ...
```
