# Gmail OAuth Lane (fallback)

Last resort when Brevo won't work — only use when the From address MUST literally be Arif's Gmail account.

## Why this exists

Brevo's default sender = arifbfazil@gmail.com. If the recipient system rejects emails from that address (e.g. some corporate firewalls), or if the task REQUIRES true Gmail API interaction (read/search/labels), fall back to `gws` with OAuth2.

## The localhost callback problem

**This is why it usually fails.** Each `gws auth login --scopes gmail.send,...` binds a fresh random port on VPS. The browser opens an OAuth consent page and redirects to `localhost:<port>`. But "localhost" inside the browser is always THE DEVICE WHERE BROWSER IS RUNNING — not the VPS. Phone browser → phone's localhost ≠ VPS localhost.

### Fix 1: SSH reverse tunnel (from Termux)
```bash
ssh -R <local_port>:127.0.0.1:<local_port> root@72.62.71.199 -p 22888 -N
```
Run before opening OAuth link. Callback routes through SSH tunnel to VPS.

### Fix 2: Tailscale
Use Tailscale IP instead of localhost for redirect_uri. Requires changing gws client config. Not tested.

### Fix 3: gcloud auth
If `gcloud` CLI available: `gcloud auth application-default login` — uses device code flow instead of localhost redirect. Untested.

## Pitfalls
- **Don't restart `gws auth login` mid-session** without noting the new port number. Previous links become dead.
- **Arif hates terminal commands.** Don't ask him to run tunnel commands unless explicitly told to proceed via compositional approach.
- **Prefer existing lanes.** Brevo works first try for outbound mail. Only add Gmail OAuth as a last option after exhausting alternatives.
