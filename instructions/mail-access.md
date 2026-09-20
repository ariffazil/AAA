# Mail Access — Reading Gmail from any warga

> **Status:** LIVE, verified 2026-09-20. Read-only by construction.
> **Fragment for:** every agent on KVM8 (forge) that needs to read the principal's mail.
> **Canonical tool:** `/usr/local/bin/mailread`

## The one command

```bash
mailread list 5                        # latest N message ids
mailread search "from:someone" 3        # Gmail search syntax, optional count
mailread meta  <MESSAGE_ID>            # headers: From / Subject / Date
mailread body  <MESSAGE_ID>            # full body
mailread labels                         # list labels
mailread check                          # CAN I read mail? diagnose if not
```

Run `mailread check` FIRST when something is off. It reports identity, group
membership, socket reachability, and performs a live read — so a failure comes
back as a diagnosis, not a traceback.

## Attach who and why

Every read carries an actor id and a purpose, and mints a receipt. Defaults are
`HERMES` / `mailread <action>`; override when the read matters:

```bash
MAILREAD_ACTOR=OpenCode MAILREAD_PURPOSE="semak thread disclosure YTL" mailread body <ID>
```

This is not decoration. An unattributed read is indistinguishable from a fishing
expedition in the audit trail, and the receipt is what makes the read reviewable
later.

## What is deliberately impossible

There is **no** `send`, `forward`, or `delete` in `mailread`. Those are
`EXTERNAL_CONSEQUENCE` / `HIGHER_IMPACT`: they change the world outside the
federation and require a sovereign F13 token. Attempting one prints a refusal —
it does not fall through to the raw CLI.

## How access is granted

The broker (`mailgw-broker.service`) exposes a UNIX socket at
`/run/mailgw/broker.sock`, mode `660`, group `mailgw-clients`. Membership in that
group is the grant.

```bash
# is this identity covered?
mailread check

# grant / revoke (takes effect on the next process spawn, not in-place)
usermod -aG mailgw-clients <user>      # grant
gpasswd -d <user> mailgw-clients       # revoke

# after granting, restart the service that runs as that user
systemctl restart <service>.service
```

**Membership is the boundary.** A process outside the group cannot even `stat`
the socket — `/run/mailgw` is mode `770` — so the denial happens before any
policy check. Denied is denied by the kernel, not by a script's opinion.

## Who has it (2026-09-20)

| Identity | Covered | Why |
|---|---|---|
| `root` | yes | every warga CLI (opencode, qwen-code, kimi, codex, hermes gateway) spawns as root |
| `arifos` | yes | arifOS kernel services |
| `forge` | yes | A-FORGE organ + the five `apa-*` Google bridges |
| `frame` | **no — deliberate** | the witness organ must stay outside; a witness with mail access is not independent |
| others | no | grant explicitly when a real need appears |

## The honest caveat — do not overclaim

Reading works. The boundary is **not complete**.

`/root/A-FORGE/bridges/gws_truth_test.py` measures 12 bypass vectors and reports
`ENFORCED_WITH_ROOT_RESIDUAL`. AppArmor genuinely confines the raw CLI and
genuinely binds root *where it is applied* (proven by
`bridges/evidence/repro-confine-denies-root.sh`), but the citizen processes are
still unconfined and the token store's `.encryption_key` sits in plaintext beside
the ciphertext.

So: `mailread` is a **governed, auditable read path**. It is not a chokepoint,
and no agent should describe it as one. The remaining work is to confine the
callers — tracked as an open loop, F13 decision, not a drive-by fix.

DITEMPA BUKAN DIBERI ⚒️
