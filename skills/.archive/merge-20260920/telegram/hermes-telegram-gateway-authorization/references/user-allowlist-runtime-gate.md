# Telegram User Authorization and Lane Drift

## Reproduction

A user was added to a dedicated `faqwan` lane and BODYBUILDER chat was allowlisted, but the message received no reply. The active gateway logged:

`Blocked unauthorized user 6041855106 in chat -1003749710464`

The chat ID and user ID are preserved here as diagnostic identifiers, not as a reusable authorization rule.

## Finding

The lane and chat config were present, but the gateway process's effective environment had no Faqwan user ID in `TELEGRAM_ALLOWED_USERS` or `TELEGRAM_GROUP_ALLOWED_USERS`. The denial occurs before lane routing, so the lane cannot receive the message.

A YAML/config patch made after the systemd service started is not active until the gateway is reloaded or restarted. A config-file check alone is insufficient evidence of a live fix.

## Remediation pattern

1. Patch the canonical runtime user allowlist through the vault/systemd configuration path.
2. Restart the gateway service.
3. Verify the service is active and the process start time is after the patch.
4. Send a harmless test message from the affected user.
5. Check the journal for the absence of a new `Blocked unauthorized user` entry and confirm a reply is emitted.

## Lesson

Keep three independent assertions separate:

- identity routing: lane/USER/SOUL/MEMORY files;
- chat routing: allowed/free-response chat IDs;
- sender admission: runtime user/group-user allowlists.

A failure in sender admission is not a lane failure.