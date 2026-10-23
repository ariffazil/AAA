# telegram/adapter.py — local patch on the Hermes install tree

Why this file exists: the running Hermes install tree is NOT clean.

    tree:    /usr/local/lib/hermes-agent
    HEAD:    5e16f33277320118d41d1729f4ebac421c12c0b2
             "fix(tests): ..."  2026-10-22 19:28:00 +0800
    dirty:   M plugins/platforms/telegram/adapter.py   (+21 / -3)

A package update, a reinstall, or a `git checkout` on that tree destroys this change
silently, and the behaviour it implements is a ratified F13 decision. So the diff is
frozen here as a patch file.

## What the patch does

`_check_delivery_target()` gained one branch: when the resolved target is a BOT id, the
send becomes a SILENT NO-OP that returns `SendResult(success=True, message_id=None)`
instead of a fail-closed error.

Reason recorded in the code comment (F13, 2026-10-22, "888 kata putus"):
bot-to-bot delivery is handled by the bridge, and the transcript still lands in state.db.
Returning success stops the caller retrying — the retries had produced 2,700+ Forbidden
lines of log noise. Human and unknown targets keep the original fail-closed behaviour.

## How to restore after a tree reset

```bash
cd /usr/local/lib/hermes-agent
git apply --check /root/AAA/state/runtime-manifest/patches/telegram-adapter-bot-to-bot-noop.patch
git apply /root/AAA/state/runtime-manifest/patches/telegram-adapter-bot-to-bot-noop.patch
```

Then restart the gateway and confirm the no-op path is live:

```bash
systemctl restart hermes-asi-gateway.service
journalctl -u hermes-asi-gateway.service -n 50 --no-pager | grep -i "silent no-op"
```

## How to verify the patch still matches the tree (drift check)

```bash
cd /usr/local/lib/hermes-agent
git diff plugins/platforms/telegram/adapter.py > /tmp/now.patch
diff -q /tmp/now.patch /root/AAA/state/runtime-manifest/patches/telegram-adapter-bot-to-bot-noop.patch
```

No output = still identical. Any output = the tree changed under the patch, re-read both
before applying anything.

## Honest limit

This patch is preserved, not upstreamed. It exists only on this host. If the install tree is
replaced by a fresh upstream checkout, the bot-to-bot no-op behaviour disappears and the log
noise returns; the patch is the only record of the decision in code form. The decision itself
is also in the code comment and in carry_forward, so it is recoverable from two places.
