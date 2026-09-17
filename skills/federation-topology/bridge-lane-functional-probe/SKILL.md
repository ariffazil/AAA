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

### Rule 1a — a timer-driven oneshot can report `active (exited)` forever

`Type=oneshot` + `RemainAfterExit=yes` on a unit driven by a `.timer` makes systemd mark the unit active as soon as it finishes — **including when it finished by failing** (`exit 1`). `systemctl is-active` then returns `active` indefinitely, the timer consumes its elapse and shows no next trigger, and the probe stalls silently for days while every board built on `is-active` calls it healthy.

```bash
systemctl show -p Type,RemainAfterExit,ExecMainStatus,ActiveEnterTimestamp <unit>.service
systemctl list-timers <unit>.timer --all        # next elapse N/A + a recent last-elapse = stalled
journalctl -u <unit>.service -n 5 --no-pager    # the real exit code
```

Fix for a timer-driven oneshot: `RemainAfterExit=no`, then `daemon-reload` and restart the **timer** (not just the service). `ActiveState` and `ExecMainStatus` are different fields — read both, and never let a monitor report `is-active` alone. `stat` for mode, then check the secret's length and first characters in Python without printing it — an 11-char stub and a 100-char token are identical from `systemctl status`.

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

**Resolve the loopback address explicitly — `127.0.0.1`, never `localhost`.** On a dual-stack
host `localhost` may resolve to `::1` first while the organ binds IPv4 only (or the reverse), and
curl then returns `000` for a perfectly healthy service. This is the most expensive probe error in
the whole table, because a false `000` reads exactly like the genuine ops problem above and sends
you to restart a working unit. Before believing a refusal, re-run against **both**
`http://127.0.0.1:<port>/health` and, if the host is dual-stack, `http://[::1]:<port>/health`; the
listener census tells you which family is actually bound:

```bash
ss -tlnp | grep -E '<port>'          # shows 127.0.0.1:x vs [::]:x vs *:x
```

Use the address form the listener actually bound, and state which one you probed when you report a
down verdict.

**A catalog, manifest, or "exposed surfaces" list is DECLARED by definition.** Answering "is X
available?" by reading the catalog is the most common way an agent reports a phantom capability.
An entry that exists in a loader (a tool list, an MCP schema cache, a plugin manifest) is not
reachable — reachability is a live call, and functionality is a live call that returned real data.

When one rung fails, check whether the capability exists somewhere else before declaring it
absent: a whole search path can be dead while a working implementation sits one host away, and
"capability present + route broken" needs a re-point, not a rebuild.

### Rule 1b-i — a gated lane that returns data has not proven its gate

On a credential/session-gated surface, a successful call is ambiguous between "my identity was
validated" and "the gate only checked that *something* credential-shaped arrived". Separate them
with two probes before reporting a gate as working:

```bash
# 1. genuinely absent credential  -> expect refusal
# 2. fabricated-but-plausible credential (well-formed id, wrong/never-issued value) -> expect refusal
```

If (2) succeeds, the control enforces **presence/reachability, not identity**. Read the validator's
success payload for the tell: a returned `actor_verified: false`, an `*_OBSERVE` / `*_UNBOUND`
code, or a reason string about connectivity means the handshake succeeded because the auth service
answered, not because the token matched.

Two follow-on rules:

- **Class-dependent gates cannot be certified from one class.** If the gate branches on tool/verb
  class or on an allowlist, a report of "every call was refused" or "the gate is fixed" is a
  sample of one branch. Call one surface per branch, and say which classes you covered.
- **Never demonstrate a gate fix on a surface the gate does not govern.** Read-only,
  allowlisted, or observe-class surfaces pass by construction; a green result there is the
  commonest false-confirmation available. Prove the fix on a surface the gate is supposed to stop.

### Rule 1b-ii — the live tool count comes from the server's SOT, not the client's schema

A remote connector's exposed schema, a compat/alias map, or a legacy monolith's decorator list all
over-count. Query the server's own registry export (`registry`-style status call, or the
`PUBLIC_*_NAMES` constant the registrar reads) and report live-registered vs alias-only names
separately. An inflated count from an alias map is contract drift, not fabrication — name it as
such rather than accusing the reporter of inventing the list.

### Rule 1b-iii — an MCP/tool bridge can be dead while its daemon is healthy

An MCP server is a **bridge** (stdio launcher or HTTP endpoint) in front of a separate
**daemon**. The daemon answering `/health` with 200 says nothing about the bridge, and a dead
bridge reaches the agent as *silent absence of tools* — not as an error, not as a failed call.
The most common cause is the launcher script failing to parse at all (left-over git conflict
markers, a syntax error), which makes the gateway respawn it in a tight crash loop while every
external health check stays green.

Full probe procedure — census, stderr log, handshake proof, delta verification, and the repair
authority boundary for a tree with another agent's uncommitted work — is in
`references/mcp-lane-probe.md`. Reusable handshake probe: `scripts/mcp_stdio_probe.py`
(`initialize` → `tools/list`, prints server version and every tool name, non-zero exit on
failure). For HTTP MCP servers that answer a legacy handshake but 400 a modern probe, see the
`mcp-dual-era-transport` skill instead — that is a protocol-era fault, not a dead lane.

Two rules that generalise beyond MCP:

- **Count the sets, never the rows.** A derived census file can lag its own config; diff the
  name lists in both directions before reporting coverage. A server that handshakes fine but is
  missing from the census is *monitor drift* — report the drift, do not relay the census as the
  verdict.
- **Fix a broken launcher in the tree; leave the commit to its owner.** Repairing the file is
  reversible capability work. Committing it is not, when the same file carries another session's
  uncommitted work. Back up, apply the minimal fix, `diff` backup-vs-now so the report proves the
  exact delta, then state plainly that the fix is uncommitted and why.

## Rule 1c — identify the LIVE store before claiming compatibility

When a capability has more than one candidate backing store, enumerating them and testing the one a catalog or collection list mentions is how you certify parity against a **vestigial mirror**. Before any "contracts match / no migration needed" verdict: find the consumer's actual read/write path, list EVERY store on the host for that capability, and census each one's payload — row count **and** the model/dimension column.

```python
# read from the store itself, never from the config that names it
sqlite3 <db> "select model, count(*) from <chunks_table> group by model;"
sqlite3 <db> "select length(<vector_payload>) from <chunks_table> limit 1;"   # chars / ~20 ≈ dim
```

A near-empty store beside a large one is a shadow, not the contract. One host commonly holds several stores for the same capability with **different** contracts (one model at 3072 dims, three others at 768), so staged partial migration is the normal outcome — not the exception. Corroborate compatibility against the store the consumer actually writes, or state plainly which store you measured.

### Rule 1d — a shared launcher path is one point of failure across every unit that names it

Several units can resolve their **interpreter or entrypoint through one shared path**. When that
path is a link whose target changed during a deploy, every consumer is affected at once while no
unit file changed — and the breakage arrives wearing an unrelated-looking error.

- **The reported error names the wrong thing.** A stale interpreter path surfaces as a
  missing-module error from a lazy or optional import (often a traceback/logging dependency), not
  as a clear path error, because the launcher never gets far enough to say otherwise. Reproduce
  against the interpreter directly — *before* concluding a package is absent.
- **Already-running units keep answering health checks from held file handles.** A process already
  up serves from the inode it holds, so liveness stays green across exactly the fleet that would
  fail on its next start. This is the sharpest form of Rule 1: **"service responded" and "service
  can start" are different conditions, and only the second survives a reboot.**
- **Enumerate the consumers before diagnosing.** `grep -rl '<path>' /etc/systemd/system`, then
  `systemctl show <unit> -p ExecStart` for each hit, then test that unit's entrypoint against the
  intended interpreter.
- **Classify every hit — grep overcounts consumers.** Inert `.bak`/`.disabled` unit files are not
  consumers, and a unit naming the path only inside `Environment=PATH` (while its `ExecStart`
  already points elsewhere) is not one either. Say which units genuinely launch through the path.
- **Confirm the resolved target matches doctrine, not merely that it resolves.** Where a successor
  path is declared canonical, a link that resolves to the predecessor reports success while
  running the deprecated origin. After any repair, `readlink -f` the path and compare against the
  declared origin — a link that resolves is not the same finding as a link that resolves
  *correctly*.

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
- **A gate that can block is also a gate that can mis-block — test both directions.** After tightening a gate (anchors, allow-lists, exemptions), run the suite BOTH ways: the previously-blocking benign inputs must now pass, AND the true-positive payloads must still block. An unanchored pattern that matches a currency symbol also matches ordinary technical English (`platform`, `confirm`, `term`, `eperm on`, `openclaw`, `pip install`, `plot`), so one gate can be simultaneously over- and under-triggering. Run the suite from **outside** the gated path — a live gate will refuse its own destructive test payload, which is correct behaviour and means the harness must not depend on being gated.
- **Estimating from a proxy is not measuring.** Bytes÷4 is not a token count (real ratio ≈5.5, read from the API's own usage block), a directory named `memory/` is not an outcome ledger, a skill count is not context burden, and a flag written to disk is not a flag loaded in the running process — compare its mtime against the service start time. Report the quantity from the system that owns it, or label it ESTIMATED and name the proxy.
- **Difference is not inconsistency until ownership says they should be equal.** Two components differing (an index at 768 dims beside collections at 1024, two model IDs, two agents disagreeing) is not drift until a shared contract says they must match. Find the owner and read its declared contract before alerting — otherwise you manufacture false positives that cost more attention than the real fault.
