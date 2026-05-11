---
name: hermes-telegram-pairing-approve
description: Approve Telegram pairing codes for Hermes Agent DM access
triggers:
  - "hermes pairing approve telegram"
  - "pairing code not found"
  - "approve telegram pairing"
---

# hermes-telegram-pairing-approve

Approve Telegram pairing codes for Hermes Agent DM access.

## Two Pairing Systems (Critical Distinction)

| System | Command | Used for |
|--------|---------|----------|
| **Hermes Agent** | `hermes pairing approve telegram <CODE>` | Telegram DMs to Hermes Agent |
| **OpenClaw** | `openclaw devices approve <requestId>` | OpenClaw gateway device auth |

Do NOT confuse them. `openclaw devices approve` will reject with "unknown requestId" because it uses a different ID format than Telegram pairing codes.

## Workflow

1. **List pending codes first** (always):
   ```
   hermes pairing list
   ```

2. **Identify the correct code** from the pending list:
   - Pending Pairing Requests table shows active codes + age
   - Approved Users table shows already-approved user IDs

3. **Approve with correct platform + code**:
   ```
   hermes pairing approve telegram <CODE>
   ```

4. **Verify**: Run `hermes pairing list` again to confirm the user moves from Pending to Approved.

## Key Insight
The code in the user's request may differ from what's actually pending. The pairing UI generates a fresh code per session. Always `list` before approving.

## Pitfalls
- `openclaw devices approve <CODE>` → "unknown requestId" (wrong subsystem)
- `hermes pairing approve telegram <WRONG_CODE>` → "Code not found or expired"
- Pairing codes expire; check `Age` column in `hermes pairing list`