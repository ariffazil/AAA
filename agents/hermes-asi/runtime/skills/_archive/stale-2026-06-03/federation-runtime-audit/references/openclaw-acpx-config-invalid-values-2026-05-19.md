# OpenClaw Acpx Config Invalid Values — 12-Restart Crash Diagnostic
**Date:** 2026-05-19
**Severity:** CRITICAL — causes gateway crash loop
**Symptom:** `openclaw-gateway.service` restarting every ~10s, 12+ restart counter

## The Bug

`/root/.openclaw/openclaw.json` had invalid acpx config values:

```json
"permissionMode": "off",           // ❌ INVALID — not in allowed list
"nonInteractivePermissions": "auto-approve"  // ❌ INVALID — not in allowed list
```

**Allowed values:**
- `permissionMode`: `"approve-all"` | `"approve-reads"` | `"deny-all"`
- `nonInteractivePermissions`: `"deny"` | `"fail"`

## Error in Logs

```
Gateway failed to start: Error: Invalid config at /root/.openclaw/openclaw.json.
plugins.entries.acpx.config.permissionMode: invalid config: must be equal to one of the allowed values (allowed: "approve-all", "approve-reads", "deny-all")
plugins.entries.acpx.config.nonInteractivePermissions: invalid config: must be equal to one of the allowed values (allowed: "deny", "fail")
```

## Fix Applied

```json
"permissionMode": "deny-all",
"nonInteractivePermissions": "deny"
```

Then: `systemctl restart openclaw-gateway` → port 18789 immediately LISTENing ✅

## Diagnostic Command (add to Phase 2 checklist)

```bash
python3 -c "import json; d=json.load(open('/root/.openclaw/openclaw.json')); acpx=d['plugins']['entries']['acpx']['config']; print(f'permissionMode: {acpx.get(\"permissionMode\")}'); print(f'nonInteractivePermissions: {acpx.get(\"nonInteractivePermissions\")}')"
```

If either shows `"off"` or `"auto-approve"` → fix immediately, restart gateway.

## Prevention

When editing `openclaw.json` acpx section, always use valid enum values. Check against OpenClaw schema before restart.