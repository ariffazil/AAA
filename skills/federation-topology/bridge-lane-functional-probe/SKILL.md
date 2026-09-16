---
name: bridge-lane-functional-probe
description: Use when a service is 'active' but its lane may be dead.
---

# Bridge / lane functional probe

Trigger: a deployment report, a restart claim, or your own summary says a connector "is up", "is wired", "is live" — and the only evidence is systemd, a config file, or a health endpoint you did not read carefully. Also load when the question is whether a **fix reached the artifact users actually get**.

## Rule 1 — `is-active` is liveness, never function

A unit can be `active (running)` while every call through it fails. Observed on KVM8's APA fleet 2026-09-16: four Google bridges (drive `:18099`, gmail `:18097`, calendar `:18094`, sheets `:18075`) all reported `active (running)` and all four answered `"status": "AWAITING_CREDENTIALS"` on their own `/health` — they pointed at `/root/.secrets/google_token.json`, a plaintext file whose `refresh_token` was an **11-character stub** (a real Google refresh token is 100+ chars).

Probe order, cheapest first, stop at the first real failure:

```bash
systemctl is-active <unit>                                  # liveness only — proves nothing
curl -s http://127.0.0.1:<port>/health | jq '{status, verbs, scopes}'   # the lane's OWN verdict
```

Then fire **one real verb**, because three different failures all look like "down" from outside:

```bash
curl -s -X POST http://127.0.0.1:<port>/ -H 'Content-Type: application/json' \
  -d '{"mode":"<verb>","params":{}}' | head -c 400
```

| Response | Meaning |
|---|---|
| `status: AWAITING_CREDENTIALS` | credential-cold — the file exists but is unusable |
| `verdict: HOLD, error: unknown verb: X` | the lane is fine; **your call is wrong** (verb names come from `/health`'s `verbs` list) |
| connection refused / timeout | genuinely dead |

**Assert the credential file's shape, not just its path.** `stat` for mode, then check the secret's length and first characters in Python without printing it — an 11-char stub and a 100-char token are identical from `systemctl status`.

## Rule 1b — four rungs: DECLARED → REACHABLE → FUNCTIONAL → EFFECTIVE

Score every surface on all four rungs before calling it up, and **say which rung you measured**.

| Rung | Question | Evidence |
|---|---|---|
| DECLARED | is it in the config, catalog, or registry? | the file that lists it |
| REACHABLE | does it answer on its port at all? | `curl` returns **any** HTTP status, or a TCP connect succeeds |
| FUNCTIONAL | does one real verb return real data? | the verb call below, parsed |
| EFFECTIVE | did a consumer act on its output and close? | a receipt, a closed incident, a downstream delta |

```bash
# rung 2, cheapest discriminator — separates "nothing listening" from "up, wrong route"
for p in <port> <port>; do
  printf "%s -> %s\n" "$p" "$(curl -s -o /dev/null -w '%{http_code}' --max-time 4 http://127.0.0.1:$p/health)"
done
```

**Never merge `000` with `404`.** `000` (curl exit 7, connection refused) means nothing is
listening — an ops problem. `404` means the HTTP server is up and the path is absent — a
routing/config problem with a different fix. A unit can be `active (running)` while its port
refuses connections: unit-live, **not reachable**. Both of those are as far from EFFECTIVE as a
catalog entry is.

**A catalog, manifest, or "exposed surfaces" list is DECLARED by definition.** Answering "is X
available?" by reading the catalog is the most common way an agent reports a phantom capability.
An entry that exists in a loader (a tool list, an MCP schema cache, a plugin manifest) is not
reachable — reachability is a live call, and functionality is a live call that returned real data.

When one rung fails, check whether the capability exists somewhere else before declaring it
absent: a whole search path can be dead while a working implementation sits one host away, and
"capability present + route broken" needs a re-point, not a rebuild.

## Rule 2 — the encrypted store and the plaintext store are different lanes

Do not write "no plaintext credentials on disk" while a plaintext token file exists in the secrets tree. On KVM8 both exist for Google: `~/.config/gws/credentials.enc` + `.encryption_key` (mode 0600, encrypted, unpacked via keyring — this one works) and `/root/.secrets/google_token.json` (plaintext, dead). A doc that conflates them, or that labels the `GOOGLE_TOKEN_PATH` bridges as "app-password" consumers when they are OAuth-token consumers, is wrong in a way an outside reviewer will find.

When one lane works and its wrapper does not (the `gws` CLI returns real Drive/Gmail data while `apa-gws-bridge` health reports `scopes_granted: []` / `in_scope: false`), trust the CLI and flag the wrapper as misreporting — two contradictory health signals is itself the finding.

**Reading inbox mail when IMAP is dead:** `gws gmail users messages list --params '{"userId":"me","maxResults":5}'` (the `apa-email-bridge` IMAP lane still holds `YOUR_EMAIL` placeholders). `gws` also serves Drive: `gws drive files list --params '{"pageSize":2,"fields":"files(name,id)"}'`.

## Rule 3 — probe the release channel, not the repo

"Fixed" has three separate meanings and they need three separate probes:

| Claim | Probe |
|---|---|
| the repo has the fix | `git log` on the commit |
| the running service has it | service `/health` `source_commit` vs `git rev-parse HEAD` |
| **users get it** | the published artifact (`curl -s https://pypi.org/pypi/<pkg>/json` → `info.version` **and** per-file `upload_time`) |

A fix can sit on `main` for weeks while `pip install <pkg>` still serves the vulnerable build. The window between "committed" and "published" is where users are exposed — check `upload_time` against the fix commit's date before telling anyone to install.

Install the published artifact in isolation and test it, rather than trusting the repo copy:

```bash
python3 -m pip install --no-deps --target /tmp/<pkg>-probe "<pkg>==<version>"
```

## Rule 4 — a status page is a claim with a shelf life

Public status rows (README tables, `SECURITY.md` gap lists, hand-maintained version fields) go stale silently and can end up **contradicting themselves in the same file**. Seen 2026-09-16 on arifOS: the surface table said `1!2026.9.1` while the SOT header four lines up still said `1!2026.8.2`; `SECURITY.md` still claimed "No CVE disclosure history" weeks after a private report was accepted and fixed.

Sweep: `grep -rn "<old-version>\|<old-claim>" README.md SECURITY.md docs/` and check every hit. Then decide each row honestly — `Open` / `Partial` / `Verified` must mean what the file's own legend says. An external review in flight is `In progress`, **not** `Verified`; and never upgrade a row because a fix landed, because the thing being measured is whether someone *independent* tested it. Rows you cannot evidence should say `unverified`, not go quiet.

## Pitfalls

- **`raw.githubusercontent.com` is CDN-cached.** After a successful push it can serve pre-push content for minutes, faking a "push failed" verdict. Use `gh api repos/<owner>/<repo>/contents/<path> -q .content | base64 -d`, or `git fetch` + `git rev-parse origin/main`.
- **Concurrent writers to one repo.** `! [remote rejected] ... cannot lock ref` (a sibling pushed between your fetch and your push) and ENOENT on `.git/index.lock` (a sibling's `git add` mid-flight) are expected on shared machines — your work is committed locally. Recover with `git fetch`, `git rev-list --count HEAD..origin/main`, rebase only if non-zero, push again; expect 2-3 attempts. Confirm `git ls-remote origin main` == `git rev-parse HEAD` before reporting success.
- **Never `git add -A` while a sibling session is editing.** Add explicit paths; a bare `add -A` sweeps their half-finished work into your commit.
- **A stale `sys_health` probe failure is not automatically a real fault.** When two tools read the same artifact and disagree (a probe reporting `chain_integrity: BROKEN, chain_gaps: 1` while the ledger's own verifier reports `overall: INTACT` with the break annotated `frozen-historical`), the finding is that **your witnessing is broken**, not necessarily the artifact. Report the disagreement; do not pick a side.
- **Metrics that only appear in another agent's cache are not verifiable.** If a reported score (e.g. an FQ reading) is not in a shared store you can read, say "cannot verify from here" rather than relaying it.
- **A headline board is not a probe.** A summary line claiming coverage 100% / debt 0 while an independent store shows enabled jobs that never fired, dead deliveries, and unjoinable receipts is a false all-clear — worse than silence, because it launders trust and suppresses the search for the real fault. Re-read the store the headline summarises before relaying the number. A green board sitting on top of a genuine fix is the most dangerous case: it makes the fix look like proof that everything else is healthy.
- **Verify a claim at the moment you relay it, not the moment it was written.** A parity check that passed when it ran can be invalidated by the very same session's next action — a certified `source == deployed` is stale the moment anyone commits again. Re-probe before repeating it.
- **Difference is not inconsistency until ownership says they should be equal.** Two components differing (an index at 768 dims beside collections at 1024, two model IDs, two agents disagreeing) is not drift until a shared contract says they must match. Find the owner and read its declared contract before alerting — otherwise you manufacture false positives that cost more attention than the real fault.
