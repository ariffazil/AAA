---
name: provider-retirement-purge
description: "Sweep across keys/, env vars, skill docs, and config files when a third-party service (Tavily, paid APIs, vendor SDKs) is retired or exhausted. Covers the 4-layer purge (SOT → flat.env → skill docs → active configs), backup filtering (tmp/checkpoints/.bak/archives are NOT mutated), and the Tavily-reference-style active-vs-historical grep pattern. Trigger: 'retire provider', 'purge tavily/old vendor', 'remove dead API key', 'decommission provider', 'exhausted plan', 'service deprecated', or any secret-hygiene cleanup that involves a provider tier transition."
version: "1.0.0"
category: devops
tags: [provider-retirement, secret-hygiene, env-cleanup, tavily-style, configuration, f2, f11]
metadata:
  hermes:
    related: [FORGE-secret-hygiene, federation-identity-reconciliation, arifos-federation-ops]
---

# Provider Retirement Purge

When a third-party service is retired (paid plan exhausted, vendor deprecated, replaced by sovereign alternative), the key + references must be purged across multiple layers or the dead key lingers as a security liability and a phantom dependency.

**Sovereign-first doctrine:** never let a third-party API key remain in `kunci-mas.env`, `kunci-mas.flat.env`, or any active config file once the service is no longer in production use.

## When to use

- Provider returns HTTP 429/432 / "exceeded plan" → retire and switch to sovereign alternative (SearXNG, local Ollama, etc.)
- Vendor sunset announcement → revoke key immediately
- Federation decides to drop a paid tier → delete ALL traces across federated skills
- Misrouted traffic / wrong provider flagged by an audit

## The 4-layer purge

| Layer | What to remove | Why |
|---|---|---|
| 1. `/root/.secrets/kunci-mas.env` (SOT) | The `export KEY="value"` line + any `*PROVIDER*` entries from `ARIFOS_ENV_WHITELIST` | Single source of truth — everything else is downstream |
| 2. `/root/.secrets/kunci-mas.flat.env` (regenerated) | Run `make -f /root/.secrets/Makefile vault-generate` | systemd services consume flat.env — must regenerate after SOT edit |
| 3. Skill SKILL.md files referencing the provider | Provider option tables, env var tables, config examples, MCP server entries | Future agents will see the dead key in docs and try to use it |
| 4. `config.yaml` and active service configs | Any `provider: tavily` / `extract_backend: tavily` style references | Active runtime config — must be empty/null/alternative |

## Recipe

```bash
# 1. Backup before mutation
cp /root/.secrets/kunci-mas.env /root/.secrets/kunci-mas.env.bak.<provider>-cleanup

# 2. Patch SOT — comment out export, remove from whitelist
# Replace:   export PROVIDER_API_KEY="..."
# With:      # PROVIDER RETIRED YYYY-MM-DD — <reason>. Key purged.
# Replace:   WHITELIST="...,PROVIDER_,..."
# With:      WHITELIST="..."   # remove PROVIDER_ from list

# 3. Regenerate flat env (systemd consumers)
cd /root/.secrets && make -f Makefile vault-generate

# 4. Verify no active references in production paths
grep -rn "<provider>\|<PROVIDER>" \
  /root/.secrets/kunci-mas.env \
  /root/.hermes/config.yaml \
  /root/HERMES/skills/ \
  /opt/arifos/ \
  2>/dev/null \
  | grep -v "\.bak\|\.archive\|quarantine\|tmp/\|checkpoints/"
# Expect: only "RETIRED YYYY-MM-DD" annotation lines

# 5. Patch skill docs — replace provider row with RETIRED marker:
# | ~~Provider~~ | ~~`PROVIDER_API_KEY`~~ | **RETIRED YYYY-MM-DD** — <reason>. <replacement> is sovereign primary. |

# 6. Restart not needed if no service still imports the key.
```

## Pitfalls

### Stale `flat.env` after SOT edit

If you edit `kunci-mas.env` but forget `make vault-generate`, systemd services (which read `kunci-mas.flat.env` at startup, not the SOT file) continue to expose the old key in their process environment.

**Always regenerate flat.env after any SOT mutation.**

Verify: `grep -c PROVIDER_API_KEY /root/.secrets/kunci-mas.flat.env` → must be 0.

### Backups preserve dead keys (intentional)

`.bak`, `.archive-config-backups/`, and `.curator_backups/` directories are intentionally NOT mutated by cleanup — they are forensic snapshots.

When grepping for "PROVIDER", filter these out: `grep ... | grep -v "\.bak\|\.archive\|quarantine"`

### Session-level env != flat.env (interactive shells)

`set -a && source /root/.secrets/kunci-mas.env && set +a` re-sources the SOT. The session only sees the new value because the SOT was edited. systemd services that haven't restarted since the edit still hold the old key in their process environment.

Most agents re-source env at session start, but the issue can surface in long-running interactive sessions. After a SOT+flat.env purge, restart consumer services if they were running.

### Deeply nested JSON grep false positives

When verifying JSON files with bash commands embedded as doubly-escaped strings (e.g. `/root/.qwen/settings.json` — hooks contain `bash -c '...'` with `\\\\\"` escapes), a naive `grep` will match the pattern in escaped form, but a JSON parse will show the decoded value differs.

Always **verify with Python JSON parsing** to confirm the decoded structure, not just raw string matching.

### Doc references to retired providers look "active"

After purge, the live `kunci-mas.env` and `config.yaml` are clean. But skill SKILL.md files may still list the provider as an option. If you don't patch the docs, future agents will:

1. Discover the option in SKILL.md
2. Try to use it
3. Find no key (because key was purged)
4. Get confused / waste time

Solution: replace the doc row with an explicit "RETIRED YYYY-MM-DD" annotation. This signals "intentionally not available" vs "missing".

## Reference

**Session transcript:** Tavily purge 2026-08-12 — dev plan exhausted (HTTP 432), retired in favor of SearXNG :8080 sovereign search.

**Purged in that session:**
- `/root/.secrets/kunci-mas.env` — `TAVILY_API_KEY` export → retired comment; `TAVILY_` removed from `ARIFOS_ENV_WHITELIST`
- `/root/.secrets/kunci-mas.flat.env` — regenerated (0 active Tavily key)
- `hermes/skills/devops/deep-research-deployment/SKILL.md` — provider table marks Tavily retired
- `hermes/skills/devops/external-mcp-integration/references/deep-research.md` — search provider list updated

*DITEMPA BUKAN DIBIRI — Sovereign infrastructure means dead keys leave cleanly.*