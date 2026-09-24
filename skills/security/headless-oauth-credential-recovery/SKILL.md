---
name: headless-oauth-credential-recovery
description: "Use when a headless service's OAuth token dies."
version: 1.0.0
tags: [oauth, credentials, google, headless, re-auth, token-lifecycle]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Headless OAuth Credential Recovery

A server-side OAuth lane has no browser, so the consent step has nowhere to happen. Every recovery
is really two questions: **why did the token die** (which decides whether re-consenting helps at
all), and **who performs the one click the host cannot**.

## Rule 0 — diagnose the DEATH, before you re-consent

A refresh failure and a scope failure both look like "auth broke". They need opposite responses.

| Signal on refresh | Means | Re-consent helps? |
|---|---|---|
| `invalid_grant` | the **token is dead** — expired or revoked | yes, but only once the cause is fixed |
| `403 insufficient scopes` | the token is **alive** but under-scoped | yes — and that is a scope change, so it needs explicit approval |

Never reach for `--scopes` on an `invalid_grant`. Widening scopes does not revive a dead grant, and
it converts a restore into a silent privilege change.

## Rule 1 — most "random" OAuth deaths are a publishing-status timer

**Google expires refresh tokens issued by an OAuth client whose app is in `Testing` publishing
status after 7 days, every time.** A lane on such a client dies on a fixed cadence and gets
diagnosed as unstable for months.

Confirm it arithmetically in one probe — compare the credential's issue time to the failure:

```bash
stat -c '%y %n' <credentials-store>     # when the token was issued
# dead ≈ issued + 7d  →  Testing-status expiry, not revocation and not a scope fault
```

If the delta is ~7 days, **re-consenting is a 7-day lease, not a fix.** Say that plainly rather than
performing the restore and letting it fail again on schedule.

Two permanent fixes, both requiring the app owner in the provider console:

1. **Publish the app to Production.** Refresh tokens stop expiring on a timer.
2. **Create a client of type "TVs and Limited Input devices".** This is the only client type that
   supports the **device flow** — the operator enters a short code at the provider's device page,
   with no browser on the server and no tunnel. For a headless lane this is the correct end state:
   it removes the human-browser step entirely and makes re-auth scriptable.

Check the client's type before assuming device flow is available; a `Desktop`/`installed` client does
not support it, and no code change can add it.

## Rule 2 — the loopback redirect can never reach the host

Consent flows redirect to `http://localhost:<port>`. `localhost` resolves **on the machine running
the browser**, so a listener on the server is unreachable when the operator approves from a phone or
laptop — the callback dies in their address bar. There is no redirect-URI trick around this for an
installed-type client; loopback is the only host it accepts.

Two handoffs that work, in order of preference:

- **Operator-built tunnel** — `ssh -N -L <port>:127.0.0.1:<port> <host>`, held open while they
  approve. The callback reaches the server listener and the exchange completes itself.
- **Code paste** — they approve, the browser lands on a failed `localhost` URL, and they send that
  URL back. Extract `code=` and exchange it **server-side with the same `redirect_uri` used in the
  authorize URL** — the provider rejects a mismatched one.

Burn this into the handoff: the operator owns exactly one step, the consent click. That is a
credential boundary. Do not try to satisfy it by other means, and do not present the restore as
"done" while that step is outstanding.

**Never drive an automated or headless browser past the provider's sign-in.** "This browser or app
may not be secure" is a security control, not an obstacle to engineer around. Report the boundary
and request the consent step.

## Rule 3 — preserve the grant's shape when you write it back

The store usually holds more than one scope grant, and the cache is keyed by the **space-joined
scope string** of each. A rewrite that emits only the scope you cared about silently deletes every
other lane's token.

- Request the **same scope union** as the existing grant, so the grant level is unchanged and no
  sibling lane breaks.
- **Enumerate the existing cache keys before writing.** A lookup for a key that vanished fails as an
  auth error, not as a missing-key error, so the damage looks like a new outage.
- Treat any scope change as a **separate, explicitly-approved** action — never as a side effect of a
  restore.

## Reading a credential store (for diagnosis only)

Encrypted stores are usually a small key file beside the ciphertext. A common shape: base64 key,
then **AES-256-GCM with a 12-byte nonce prefix**, then ciphertext holding
`{client_id, client_secret, refresh_token, type}`; a separate plaintext cache keyed by scope holds
`{access_token, refresh_token, expires_at, id_token}`. Expiry may be a structured date
(`[year, yday, hour, min, sec, nanos, ...]`), not an epoch integer — read the type before comparing.

Decrypt to **diagnose**, never to publish. Keep values out of your output and out of chat; report
fingerprints and lengths, not secrets. Rotate rather than scrub if a value escapes.

## Pitfalls

- **A helper the service user must run cannot live under `/root`.** `/root` is not traversable by a
  non-root service identity, so the script fails `Permission denied` even when executed as that
  user. Deploy it into the service's own tree (`/opt/<service>/`), owned by that user, and invoke
  with `sudo -u <user>`. Diagnose this as a **path** problem, not a credential problem — the error
  text is identical to a real access denial on the secret itself.
- **Do not report the lane restored while the consent step is outstanding.** A dead token plus a
  written-ahead restore plan is `PENDING_OPERATOR`; the alerting lane is still blind.
- **A scope error and a dead token are not interchangeable.** See Rule 0. Reporting one as the other
  either widens privilege silently or sends the operator through a consent that cannot help.
- **"It worked after re-auth last time" is not evidence it will hold.** If the app is in `Testing`,
  it will not. Check the publishing status before promising a fix.
- **Do not impersonate or re-exec as the service identity to read its store** as a shortcut around
  the boundary. Read what is readable, report the boundary, and route the mutation through its lane.

## When the restore needs more than one call

Seed the operator's step with everything already staged — the exact consent URL, the tunnel command,
and the paste-back fallback — so the handoff is one action rather than a conversation. State the
listener's live window, and what happens when it lapses.
