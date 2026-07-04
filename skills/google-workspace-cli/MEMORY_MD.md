# Google Workspace CLI — VPS Headless Setup (arifOS)

## Status: OPERATIONAL ✅

## How It Works on VPS (No Browser)

The `gws` CLI normally needs browser OAuth. On headless VPS, we use a Python helper
that refreshes the existing OAuth token directly — no browser needed.

**Token location:** `/root/HERMES/google_token.json` (refresh token already present)
**Client secret:** `/root/HERMES/google_client_secret.json` (OAuth desktop app credentials)

## Drive CLI Usage

```bash
# List all files
python3 /root/.openclaw/workspace/skills/google-workspace-cli/drive_helpers.py list

# Search files by name
python3 /root/.openclaw/workspace/skills/google-workspace-cli/drive_helpers.py search "query"

# Read file content (text files + Google Docs export)
python3 /root/.openclaw/workspace/skills/google-workspace-cli/drive_helpers.py read <file_id>

# Download file
python3 /root/.openclaw/workspace/skills/google-workspace-cli/drive_helpers.py download <file_id> [local_path]

# Get file metadata
python3 /root/.openclaw/workspace/skills/google-workspace-cli/drive_helpers.py get <file_id>
```

## Key arifOS Files in Drive

| File | ID | Purpose |
|------|----|---------|
| ROOTKEY_SPEC.md | 1FBnM5WT-plgPkUu0r2Pd27DHbueQoh28 | Root key architecture |
| 01_genesis_canon_v_42.md | 1_VqrpZ7nXXTCke0t28eBloZyWIFyAYsc | Genesis canon |
| EPOCH_9-GENESIS.json | 1P8qxyJtAxFafWcnYELcueRR0_GFjrdJq | Epoch 9 genesis |
| arifos_rootkey_zkpc_vault999.zip | 1xnfT_hKqkftxgQMfOMGWRzr9Sonivp0o | Rootkey + ZK proof |

## Auth Refresh (When Token Expires)

Token auto-refreshes on every call. If you see `401 Unauthorized`:
```python
# Manually refresh:
curl -s -X POST https://oauth2.googleapis.com/token \
  -d "client_id=236716421952-qmg43go813lqllc46tvrp4bsi6g6vjd0.apps.googleusercontent.com" \
  -d "client_secret=GOCSPX-[REDACTED-vault]" \
  -d "refresh_token=<from /root/HERMES/google_token.json>" \
  -d "grant_type=refresh_token"
```

## Notes

- Token expiry: stored in `google_token.json` — helper checks before use
- Drive API scope: `drive` (full drive access)
- Token never expires permanently — refresh token is long-lived
- DO NOT share or log the refresh token
