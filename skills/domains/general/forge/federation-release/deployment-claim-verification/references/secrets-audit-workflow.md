# /root/.secrets/ Audit Workflow

> PROVEN 2026-08-26. Comprehensive audit of 234-key vault.

## Directory Structure

```
/root/.secrets/
├── kunci-root.env          ← CANONICAL (32279B, 310 export lines, 234 unique vars)
├── kunci-root.flat.env     ← Auto-generated flat version for systemd (no 'export')
├── kunci-mas.env           → symlink to kunci-root.env
├── a-forge.env             → symlink to kunci-mas.env
├── sovereign_identity.toml ← Ed25519 identity (was 640, fixed to 600)
├── env-backups/            ← Rotation directory
├── quarantine/             ← Stale keys during rotation
├── auth/                   ← Agent auth configs (claude-code.json, codex.json, etc.)
├── env/                    ← Env snippets (agentmail, github-bridge, supabase)
├── jwks/                   ← JWT signing keys
├── tokens/                 ← Token storage
└── .env.postgres           ← ORPHAN (POSTGRES_URL + SUPABASE_DB_URL outside pipeline)
```

## Build Pipeline

```
Human edits kunci-root.env
    ↓
make vault-generate
    ↓
kunci-root.flat.env (auto-generated, no 'export' prefix)
    ↓
systemd services read flat.env
    ↓
make vault-verify (detects drift)
```

## Audit Checklist

### 1. Permissions
```bash
# All files should be 600
find /root/.secrets -type f ! -perm 600 -ls

# All dirs should be 700
find /root/.secrets -type d ! -perm 700 -ls

# One exception: sovereign_identity.toml should be 600 root:root
stat -c '%a %U:%G %n' /root/.secrets/sovereign_identity.toml
```

### 2. Orphan Files
```bash
# Check for .bak files outside env-backups/
find /root/.secrets -maxdepth 1 -name "*.bak*" -ls
# Move to env-backups/ with date stamp
```

### 3. Vault Sync
```bash
cd /root/.secrets && make vault-verify
# Should show: "VERIFIED — 0 drift, N keys synchronized"
# If drift: make vault-generate then re-verify
```

### 4. Stale Credentials
```bash
# Check age of special files
for f in webhook-secret .cloudflare_token .docker-hub-auth cosign.key; do
  age=$(( ($(date +%s) - $(stat -c %Y /root/.secrets/$f)) / 86400 ))
  echo "${age}d /root/.secrets/$f"
done
# >90d = flag for F13 rotation
```

### 5. Orphan Variables
```bash
# Check for vars in orphan files not in canonical
grep 'SUPABASE_DB_URL' /root/.secrets/kunci-root.env  # Should exist
cat /root/.secrets/.env.postgres  # If exists, ingest or delete
```

## Key Inventory (2026-08-26)

- 234 unique variables, 310 export lines
- 7 source categories merged
- Top prefixes: ARIFOS (43), MIMO (13), HERMES (12), QWEN (11), COPILOT (11)
- 30 sk-* values (provider API keys)
- 4 BASE64 values (wrapped credentials)

## Fix Categories

| Category | Action | F13 Required? |
|---|---|---|
| Dir permissions (755→700) | chmod 700 | No |
| File permissions (640→600) | chmod 600 | No |
| Orphan .bak files | Move to env-backups/ | No |
| Vault drift | make vault-generate | No |
| Stale credentials (>90d) | Rotate at provider | Yes |
| Orphan variables | Ingest into canonical or delete | Depends |
