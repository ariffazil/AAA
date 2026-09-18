---
name: bridge-lane-functional-probe
description: Use when a service is 'active' but its lane may be dead.
---

# Bridge / lane functional probe

Trigger: a deployment report, a restart claim, or your own summary says a connector "is up", "is wired", "is live" — and the only evidence is systemd, a config file, or a health endpoint you did not read carefully. Also load when the question is whether a **fix reached the artifact users actually get**.

## Rule 1 — `is-active` is liveness, never function

A unit can be `active (running)` while every call through it fails. Observed on KVM8's APA fleet 2026-09-16: four Google bridges (drive `:18099`, gmail `:18097`, calendar `:18094`, sheets `:18075`) all reported `active (running)` and all four answered `"status": "AWAITING_CREDENTIALS"` on their own `/health` — they pointed at `/root/.secrets/google_token.json`, a plaintext file whose `refresh_token` was an **11-character stub** (a real Google refresh token is 100+ chars).

**Re-probed 2026-09-17: still true.** All four are `active (running)` under
`apa-{drive,gmail,calendar,sheets}-bridge.service` (up since Sep 14), and all four still return
`status: AWAITING_CREDENTIALS` with `credentials_configured: false`. The *lane verdict* is
re-verified; the *credential-stub length* is carried from the 09-16 probe and was **not** re-measured
here — that path is gated, so treat it as asserted, not witness.


Probe order, cheapest first, stop at the first real failure:

```bash
systemctl is-active <unit>                                  # liveness only — proves nothing
curl -s http://127.0.0.1:<port>/health | jq '{status, verbs, scopes}'   # the lane's OWN verdict
```

**`is-active` also cannot tell you the unit EXISTS.** Both a stopped unit and a mistyped name print
`inactive`; the only difference is the exit code (`3` = loaded but inactive, `4` = no such unit), and
`LoadState` is the field that names it:

```bash
systemctl is-active <unit>; echo "exit=$?"      # inactive + 3 = exists; inactive + 4 = not-found
systemctl show <unit> -p LoadState,ActiveState --value   # loaded | not-found  ← the discriminator
```

Measured 2026-09-17: probing four Google bridges by a guessed name pattern
(`apa-google-<port>.service`) returned `inactive` for all four, which reads as *these are not units at
all* — they are `apa-drive-bridge.service`, `apa-gmail-bridge.service`, `apa-calendar-bridge.service`,
`apa-sheets-bridge.service`, all `active (running)` since Sep 14. A guessed unit name produces a
confident "down" verdict about a healthy lane, and it is indistinguishable from a real stop unless you
read `LoadState`. Name the unit from the listener census (`ss -lntp`) or from
`systemctl status <pid>`, never from a naming convention.

**Read the lane verdict field, never the `ok` flag — they disagree inside one payload.** The same
probe returned, for all four bridges:

```json
{"ok": true, "status": "AWAITING_CREDENTIALS", "credentials_configured": false, "verbs": [...]}
```

`ok: true` is the bridge process's opinion of itself; `status` is the lane's verdict. A monitor (or a
reader skimming) that checks `ok` reports four healthy connectors over a lane that cannot serve one
request. When a payload carries both a self-flag and a status field, the status field is the finding
and the contradiction is worth naming in the report.

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

**A refusal can be address-specific even on IPv4 — the service may not be bound to loopback at
all.** A proxy bound to an overlay/tailnet address serves every real client while refusing
`127.0.0.1:<port>` outright, so a loopback probe reports `000` for a lane that is completely up,
and the table above sends you to restart a healthy unit. Before any down verdict, take the bind
census and then probe **the address the consumer is configured for** — read it from the consumer's
own process environment, never from an assumption about where the service ought to live:

```bash
ss -lntp | grep -E ':<port>'        # what is actually bound, on which address and family
grep -zoP '_URL=[^\x00]*' /proc/<consumer_pid>/environ   # the address the caller was given
```

The second reading is the one that matters, because it is what the failing caller will actually
dial. A consumer whose `*_BASE_URL` points at an address nothing binds is a **configuration**
fault with a one-line fix, not an outage — and the two are indistinguishable from a single refused
probe.

When both readings agree that the caller points at a hole, prefer **adding the missing `bind`**
over restarting anything: one extra `bind` on the existing frontend is reversible and cannot
disturb the address that already works, whereas restarting a healthy unit is an outage you caused.
A companion trap is the same shape in reverse — an interface that binds only one family answers on
IPv4 and refuses IPv6 (or the reverse), which is why the census, not the convention, decides.

**A catalog, manifest, or "exposed surfaces" list is DECLARED by definition.** Answering "is X
available?" by reading the catalog is the most common way an agent reports a phantom capability.
An entry that exists in a loader (a tool list, an MCP schema cache, a plugin manifest) is not
reachable — reachability is a live call, and functionality is a live call that returned real data.

**A record that says a thing MOVED is also only DECLARED — verify the payload arrived.** A
retirement/merge/handoff record (`moved_to: <target>`, a recorded sha256, a rollback command, a
deprecation window) is a *claim about* the move, not the move. Measured 2026-09-17 on this
federation's skill store: 14 skills were tombstoned with all of those fields present, and **0 of the
14 targets carried their source's content** — every target was a shorter stub. The destination
`skill_view`-ed fine, so nothing errored; the body was simply gone, and the retired name no longer
resolves, so no surface reports it. The test that catches it is the same one the ladder already
prescribes: recover the payload and check it is *reachable at the destination*, by content. A
successful lookup at the target name proves REACHABLE. It proves nothing about whether what you
needed is inside.

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

## Rule 1e — the readiness read is in the body, not the status code

`curl -sf <url>/health && echo "OK"` is the same error as `is-active`: HTTP 200 proves the process
answered, and the lane's own verdict lives in the fields. Read the keys the body **actually has** —
quoting a field a build does not emit is fabrication, and **an absent key is not a pass**.

- **Split the two questions and answer both separately.** *Is the process alive* (HTTP code, `status`)
  and *is the consumer side fed* (counters, measurement-status flags, provenance class). A perfectly
  healthy organ with `subjects: 0` / `ledger_events: 0` is serving nobody — the confident-zero failure
  at the health layer, same shape as the empty-input-space pitfall below. `status: degraded` beside
  working endpoints is a finding to report, not a failure to hide.
- **Read the measurement-status flag beside every number.** A scalar carrying `status: MEASURED` is a
  reading; the same field on a modelled/defaulted build is not. Quote the flag with the value.
- **Name the provenance class when relaying to a human.** `OPERATOR_REPORTED` is self-reported, not
  instrumented; say so, or a self-report silently reads as telemetry.
- **A commit trio (`source_commit` / `built_commit` / `deployed_commit`) is three readings, not one.**
  `drift: true` says the source you are reading is not what is running; quote the commit you probed.
- **A ceiling declared in the payload (`authority` / `authority_ceiling`) is the organ telling you it
  never gates.** An organ whose ceiling is reflection-only must never be relayed as an approval.
- **A protocol precondition is not a dead lane.** A raw HTTP MCP call (`POST /mcp` carrying
  `tools/call`) can answer `SESSION_MISSING: Mcp-Session-Id header required` — the server is up and
  correct. Go through the MCP client / tool bridge, or complete `initialize` first and carry the
  returned session id. Never report the tool down on the strength of a hand-rolled request.
- **When a build's field set changes, list what you could NOT read.** Emit the names of the expected
  keys that are missing from the body alongside the values you did get. Naming a missing read is an
  honest report; asserting a value for an absent key — or letting its absence pass as health — is not.

### Rule 1f — a liveness health endpoint is not a capability health endpoint

A health body reading `{"status":"ok","key_loaded":true}` proves the process is up and a key parsed.
It proves nothing about whether the lane can serve one request. Measured on a signing lane that
returned `ok` to every probe while refusing every signature call — the credential env vars were unset
and a required module was absent, and neither appeared in the payload.

The upgrade contract: an endpoint that gates a capability must report the **blockers**, not just
liveness —

- credential **presence** (the env vars / files it needs, set or not — never their values),
- module/import **availability**, measured by importing under the *serving* interpreter,
- **last successful** operation timestamp,
- recent **rejection rate**, so silent failure modes surface as a number rather than as silence.

Probe the lane by **firing one real verb and reading its refusal**, not by reading the health body.
The body tells you what the author thought to check; the verb tells you what is true. A liveness-only
endpoint is worse than no endpoint, because a monitor built on it reports a dead capability as green.
When a receipt claims a health endpoint was upgraded to report capability, re-probe the live service —
a repaired endpoint sitting uncommitted on disk, with the running process still serving the old code,
reports the old body no matter how good the patch is.

**An install that "succeeded" is not a dependency that imports.** After provisioning a package,
verify with the actual import under the serving interpreter before declaring the blocker cleared — and
check both directions: the name in the code's `import` statement, and the module name the installed
distribution actually provides. Distro and PyPI packages for the same capability routinely ship
**different module names** for near-identical code (a distro package may provide the upper-case form
while the PyPI package provides the lower-case one), so the wrong package installs cleanly, the import
fails, and the failure then reads as a credential or path problem — sending you to the wrong fix.
Report the blocker you cleared, not the command that exited zero.

### Rule 1g — a single field is not the report

When a probe or audit returns a structured artifact, quote the whole payload's field set before
summarising any number from it. Measured: a chain report was relayed as "9 corrupt lines" — the value
of one field — while the same report listed 94 gaps across five classes, an entry count, a scope
field, and an agreement flag. Every reader downstream received a number an order of magnitude off, and
the field that would have corrected it was three lines away in the artifact nobody re-opened.

Read the artifact's own keys first (`keys()` / the header), then quote the fields that bear on the
claim. A denominator without its method, scope, and timestamp is not evidence; state them or label the
figure UNMEASURED. A report is also a claim with a shelf life — check its `measured_at` against now
before acting on it, since a stale report is a measurement of a system that no longer exists.

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
- **A probe that reads an empty input space reports HEALTH.** The most dangerous probe failure is not a wrong answer, it is a confident zero. Built and caught 2026-09-17: a new gate check globbed `<skills_root>/.archive_skills_wave2`, a path that does not exist (the registry is a *sibling* of the skills root, not a child), found no inputs, and printed `0 — clean`. It ran green for two passes and would have reported an intact library forever. **Print the input count beside the result count, and make the empty case an explicit FAIL** (`cannot witness`), never an implicit pass. The tell in the output was `count: 0` sitting next to `tombstones: 0`.
- **Then prove the check can fail before you trust it.** The same pass created the check, watched it print a clean zero, and only discovered it was inert by removing one real input and re-running: a check whose falsifying branch is unreachable is decoration. Extract the predicate, find one input that must take the failing branch, confirm the verdict flips, then restore. If you cannot make it fail, you have not tested it — you have read it.
- **The dedupe key is a coverage decision — it decides what you never looked at.** The same check bucketed candidates by *target* file, and four of the fourteen records share one target: three were never examined, so their loss could not have been found by any amount of careful reading of the output. When several inputs collapse onto one key, prove each still gets checked individually, and report coverage as `checked / total siblings`, not `records matched`.
- **A lookup that cannot match is not evidence of absence — check what the key IS before reading silence as a negative.** Measured 2026-09-17: three CLIs keep a per-version file store named `<hash>@vN`, and `<hash>` is **not** a hash of the stored content (sha256, md5 and sha1 of the blob, and of the path/basename/dirname variants, all miss — and it is not shared across sessions). So searching that store for `sha256(<live_file>)` returns nothing for a file that *was* edited, and the natural reading is "the peer never touched this". Locate the record by **content** (a distinctive line from the payload), never by key. Before treating any empty result as a negative, name the key you searched on and where that key's construction is documented — an undocumented key assumption turns your probe into a random number generator.

  The same rule applies to your **own** checkers, in the positive direction: a predicate that substring-matches prose fires on the prose. Written 2026-09-17, a duplicate-detection check tested for the word `environ` and reported a real duplication where the file only *named* the owning skill in a sentence; the second attempt (`"/proc/" and "environ"`) still fired, because the same file reads `/proc/<pid>/status` for a different probe. Only the command form (`/proc/\S*environ`) told the truth. Assert the thing you mean, not a word that appears near it — and when your check disagrees with the file, suspect the check first.

