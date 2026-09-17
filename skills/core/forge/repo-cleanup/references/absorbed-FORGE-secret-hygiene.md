# Absorbed: FORGE-secret-hygiene

> **Provenance.** Pre-merge body of the `FORGE-secret-hygiene` skill, tombstoned 2026-09-16T22:44:00Z by Wave 2 (`moved_to: core/forge/repo-cleanup/SKILL.md`).
> Recovered verbatim from `/root/.hermes@entropy-wave2-pre-act-20260916T144144Z:skills/FORGE-secret-hygiene/SKILL.md` — content was never carried into the target by the
> original consolidation; recovered 2026-09-17 to complete the recorded merge.
> Original sha256 (tombstone `sha256_before`): `79a6e1d5ba4565afabe94539fe34d1a7f61a2bbf99096145addb5aea8757e1d9`
> Recovery sha256: `79a6e1d5ba4565afabe94539fe34d1a7f61a2bbf99096145addb5aea8757e1d9`
> The `FORGE-secret-hygiene` routing name stays retired — this file is a reference, not a skill.

---

# Secret Hygiene

**Scans Arif's VPS for plaintext secrets, aged credentials, and rotation gaps.**

## Scope

Files scanned:
- `~/.openclaw/openclaw.json`
- `~/.openclaw/env.local`
- `~/.openclaw/.env*`
- `~/.config/opencode/opencode.json`
- `/root/arifOS/**/*.env*`
- `/root/AAA/**/*.env*`
- Docker env files

## Red Flags

```
🚨 IMMEDIATE
  - API key in plaintext (not env var)
  - Private key in git-tracked file
  - Hardcoded password in Dockerfile
  - Token > 365 days old without rotation

⚠️ REVIEW
  - API key > 180 days old
  - Same key used across 3+ services
  - Token stored in workspace (not vault)
```

## Audit Script

```bash
#!/bin/bash
echo "=== SECRET HYGIENE AUDIT ==="
echo "Time: $(date -u)"
echo ""

KEY_PATTERNS="sk-|api_key|apikey|token|secret|password|private_key|client_secret|bearer"

echo "--- Scanning for plaintext secrets ---"
for f in ~/.openclaw/env.local ~/.openclaw/.env* /root/arifOS/.env* 2>/dev/null; do
  if [ -f "$f" ]; then
    echo "File: $f"
    grep -E "$KEY_PATTERNS" "$f" 2>/dev/null | sed 's/=.*/=***REDACTED***/' | while read line; do
      echo "  ⚠️  $line"
    done
  fi
done

echo ""
echo "--- Checking key age (files with mtime) ---"
for f in ~/.openclaw/env.local ~/.openclaw/openclaw.json 2>/dev/null; do
  if [ -f "$f" ]; then
    age_days=$(echo "$(( ($(date +%s) - $(stat -c %Y "$f" 2>/dev/null || echo 0)) / 86400 ))")
    if [ "$age_days" -gt 180 ]; then
      echo "⚠️  $f — $age_days days old (review for rotation)"
    else
      echo "✅ $f — $age_days days old"
    fi
  fi
done

echo ""
echo "--- Git-tracked secrets check ---"
cd /root/arifOS && git log --oneline -1 -- source 2>/dev/null
cd /root/AAA && git log --oneline -1 2>/dev/null
```

## Rotation Policy

| Secret Type | Max Age | Rotation Trigger |
|---|---|---|
| Telegram Bot Token | 12 months | Annual |
| DeepSeek API Key | 6 months | Billing alert |
| MiniMax API Key | 6 months | Billing alert |
| Cloudflare API Key | 6 months | Suspected compromise |
| A2A Bridge Token | 3 months | After team member leaves |
| Database Passwords | 3 months | After any security incident |

## Secret Storage Hierarchy

```
1. Vaultwarden (vaultwarden:8080) — PRIMARY
   - All API keys, tokens, passwords
   - Share with Arif only

2. 1Password CLI (if configured) — SECONDARY
   - Developer secrets

3. SOPS/age encrypted files — CONFIG
   - Encrypted .env files in git

4. NEVER in plaintext:
   - Git-tracked files
   - Slack/Discord messages
   - Telegram history
   - Dockerfiles (use --build-arg or secrets)
```
