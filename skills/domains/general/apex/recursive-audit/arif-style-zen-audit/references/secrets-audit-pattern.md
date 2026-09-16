# Secrets / Vault Audit Pattern (forged 2026-08-26)

When the audit target is `/root/.secrets/` (kunci-root.env, vault, key rotation), use this sub-pattern within the ZEN audit framework.

## Gate checklist (secrets-specific)

| Gate | Probe command | Pass criteria |
|---|---|---|
| File existence | `stat kunci-root.env kunci-root.flat.env` | Both present, single canonical |
| Permissions (files) | `find . -type f ! -perm 600` | Zero results (all 600) |
| Permissions (dirs) | `find . -type d ! -perm 700` | Zero results (all 700) |
| Structure | `grep -c '^export' kunci-root.env` | Matches expected count |
| Symlink integrity | `readlink -f` each alias | All resolve to canonical |
| Vault sync | `make vault-verify` | Exit 0, 0 drift |
| Orphan files | `ls *.bak*` in main dir | Zero results (all in env-backups/) |
| Key age | `stat -c '%Y'` on special files | Flag anything >90d |
| Group-readable | `find . -perm /g+r` | Zero results |
| Process leaks | `grep -r 'kunci' /proc/*/environ 2>/dev/null` | Zero results |
| Stray copies | `find . -name '*.env' -not -path './env/*'` | Only canonical + flat |

## Tier classification (auto-fix vs F13)

**Tier 1 — Auto-fix (reversible, no F13):**
- `chmod 700` on world-readable dirs
- `chmod 600` on group-readable files
- Move orphan `.bak*` files to `env-backups/` with date stamp
- Regenerate flat via `make vault-generate` + verify

**Tier 2 — F13 decision required:**
- Key rotation (requires provider-side action — Cloudflare, Docker Hub, webhook, cosign)
- Ingesting stray env files into canonical pipeline
- Deleting backup files (confirm vault-sync captured first)
- Any structural change to kunci-root.env prefix groups

## Pitfall: vault-verify drift after backup moves

Moving `.bak*` files does NOT affect vault-verify (it checks canonical ↔ flat, not backups). But regenerating flat AFTER moves is good hygiene — run `make vault-generate && make vault-verify` as a pair.

If vault-verify fails after auto-fix, regenerate flat before reporting:
```
cd /root/.secrets && make vault-generate && make vault-verify
```

## Pitfall: .env.postgres orphan pattern

Watch for standalone `.env` files in `/root/.secrets/` that contain vars NOT in canonical. Check if any var is missing from kunci-root.env before deleting:

```bash
# Step 1: list all .env in main dir (not in env/ subdir)
find /root/.secrets/ -maxdepth 1 -name '*.env*'

# Step 2: for each, extract var names
grep -oE '^export [A-Z_]+=' file.env | sort -u

# Step 3: check which vars are missing from canonical
comm -23 <(var_set_from_orphan | sort) <(var_set_from_kunci_root | sort)
```

Ingest missing vars first (add to kunci-root.env with appropriate prefix group), then delete the orphan. Never delete a stray .env without checking — it may be the ONLY source for a critical var.

## Stale special files (non-env, secrets-bearing)

Always check these paths during a secrets audit:
- `cosign.key` + `cosign.pub` (supply chain signing)
- `vault-signing-ed25519` + `.pub` (vault signing)
- `webhook-secret` (incoming webhook auth)
- `.cloudflare_token` (full DNS/origin control)
- `.docker-hub-auth` (image pull scope)
- `mapbox-token.txt` (usage quotas)
- `yt-cookies.txt` (YouTube session)
- `federation-backup-passphrase` (Restic encryption)

Age >90d = flag for rotation. Provider-side action required — cannot rotate from VPS alone.

## Provenance template (for sealed audit output)

```
HERMES_SECRETS_AUDIT::v1.0
canonical_file: /root/.secrets/kunci-root.env
canonical_size: <bytes>
canonical_mtime: <ISO-8601 UTC>
flat_file: /root/.secrets/kunci-root.flat.env
flat_size: <bytes>
flat_mtime: <ISO-8601 UTC>
key_count: <N>
source_categories: <list>
tier1_fixed: <list>
tier2_pending_f13: <list>
vault_verify: PASS|FAIL
drift_count: <N>
orphan_files_before: <N>
orphan_files_after: <N>
```