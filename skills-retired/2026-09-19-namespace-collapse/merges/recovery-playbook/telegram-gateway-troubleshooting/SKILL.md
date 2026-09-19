---
name: telegram-gateway-troubleshooting
description: Fix Telegram echo loops via require_mention config.
tags: [telegram, gateway, troubleshooting]
---

# Telegram Gateway Troubleshooting

## Echo Loop Diagnosis

### Symptoms
- Bot responds to every message including its own outputs
- Infinite loop: output → input → output → input
- Session fills with "(no response)", "🤐", or repeated status messages
- Token burn continues even with no human interaction

### Root Cause
`require_mention: false` in `~/.hermes/config.yaml` means the gateway treats ALL messages as input, including the bot's own replies.

### Diagnosis Steps

1. **Check config setting:**
   ```bash
   grep -n "require_mention" ~/.hermes/config.yaml
   ```
   Look for the Telegram section (usually around line 1190-1200).

2. **Verify the problem:**
   - If `require_mention: false` exists in the telegram section → echo loop will occur
   - The bot will respond to every message, including its own

3. **Check gateway status:**
   ```bash
   systemctl status hermes-asi-gateway.service
   ```

### Fix

1. **Edit config:**
   ```bash
   sed -i 's/require_mention: false/require_mention: true/' ~/.hermes/config.yaml
   ```
   
   Or manually edit `~/.hermes/config.yaml` and change:
   ```yaml
   telegram:
     require_mention: true  # was: false
   ```

2. **Restart gateway:**
   ```bash
   systemctl restart hermes-asi-gateway.service
   ```

### Critical Pitfall: Restart Behavior

**When you restart the gateway from within a session that the gateway hosts:**
- The restart command will succeed
- The gateway will restart with new config
- **Your session will be terminated with exit code -15 (SIGTERM)**
- This is **expected behavior**, not an error

The session drop happens because:
- The gateway process hosting your session is being restarted
- All active sessions are terminated during restart
- You cannot restart the gateway "from within" without losing your session

**Correct approach:**
- Apply the config fix
- Tell the user to restart from an external shell
- Or accept that your session will end after restart

### Verification

After restart:
```bash
# Check gateway is running
systemctl status hermes-asi-gateway.service

# Verify config is applied
grep "require_mention" ~/.hermes/config.yaml

# Test by sending a message without @mention
# Bot should NOT respond unless @mentioned
```

## Related Issues

### Bot Responds to All Messages
- **Cause:** `require_mention: false`
- **Fix:** Set to `true`

### Gateway Won't Start
- Check logs: `journalctl -u hermes-asi-gateway.service -n 50`
- Verify config syntax: `hermes config validate`
- Check for port conflicts: `ss -tlnp | grep :8080`

### Session Drops Unexpectedly
- Gateway restart (see pitfall above)
- OOM kill: check `dmesg | grep -i oom`
- Config error: validate config syntax