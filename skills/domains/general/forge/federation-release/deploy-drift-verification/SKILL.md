---
name: deploy-drift-verification
id: deploy-drift-verification
version: 1.0.0
owner: A-FORGE
risk_tier: low
description: "Use when a code fix isn't reaching the running service."
when_to_use: "After authoring a fix, when a deploy seems to have 'shipped' but old behavior persists, or before claiming any authority/governance change is live."
disable-model-invocation: false
allowed_tools:
- Bash
- Read
- Grep
floor_scope:
- F2
- F4
- F11
autonomy_tier: T0
---
# Deploy-Drift Verification — did the fix actually reach runtime?

A service running is not the same as a service running what you think. For compiled services (TypeScript→`dist/`, any build step), a change passes through THREE layers before it affects behavior, and a fix can rot at any of them while the runtime keeps executing old code and the ledger keeps recording "success".

## The three layers

1. **source (`src/`)** — may hold an uncommitted fix that was never shipped.
2. **compiled artifact (`dist/`)** — may predate source (fix authored, build never re-run).
3. **running process** — loads the compiled artifact at startup; a restart is required to pick it up.

## The layer above the artifact — the request router decides which file is actually served

A file can be present in source, present in `dist/`, synced to the served tree, and validated
config — and the URL still returns a different document. Serving is a separate, ordered resolution
step, and it is a fourth place a fix rots. It fails in exactly the way this skill warns about: a
clean `200` carrying the wrong bytes, so every probe short of a content grep reads as success.

**Config is often split — grep the file that holds the rules, not the one you remember.**
Reverse-proxy configs get refactored into a small dispatcher that imports a directory of per-site
files. Searching the dispatcher returns nothing, which reads as "the rule is gone" and invites an
agent to "restore" a config that was never broken.

```bash
# which file actually holds the site rules?
grep -rn 'import' /etc/caddy/Caddyfile          # e.g. import /etc/caddy/vhosts/*.conf
ls /etc/caddy/vhosts/
grep -n '<pattern>' /etc/caddy/vhosts/<site>.conf
caddy validate --config /etc/caddy/Caddyfile    # dispatcher path still validates the whole tree
```

**Check whether an existing block already covers the path before adding one.** A handler whose
`try_files` includes `{path}/index.html` serves every new subdirectory under its prefix for free —
no config change, only the file plus a sync. Adding a redundant handler is an unaudited config
mutation, not a harmless extra.

```bash
grep -n -A6 'handle /<prefix>/\*' /etc/caddy/vhosts/<site>.conf
```

**Ordering is the failure mode.** First-match-wins: a specific `handle` placed after a catch-all
never fires, and the catch-all serves the shell instead. Bare `redir` directives are evaluated
before `handle` blocks regardless of line order, so a legacy redirect can shadow a handler you just
added. Never gate a redirect on `not header_regexp User-Agent` — it creates a bot-only hole that
browser testing cannot see, while curl from an external host catches it.

**A static file in the served tree can be dead weight — check whether the route is carried by the SPA catch-all.**
On a single-page-app host the catch-all serves the shell for every path under its matcher, whatever
files exist on disk. A page can sit in the webroot at the exact URL, be the file you have been
editing for an hour, and never reach a single user. Probe which document actually answers before
editing either one:

```bash
curl -s "$URL" | grep -o '<title>[^<]*'              # what visitors get
curl -s "$URL" | wc -c                              # shell bundle is small; a real page is not
grep -o '<title>[^<]*' <webroot>/<path>/index.html  # what you were about to edit
```

A different title, or a response sized like the bundle rather than the file, means the route is
client-rendered and the on-disk copy is shadowed. **Edit the source component and rebuild** — editing
the webroot copy is a no-op for that route and the next sync overwrites it anyway.

**One vhost, several `root` directives — one rsync is not a deploy.** A site block can serve
different paths from different trees. A deploy that syncs only the primary webroot reports success
while the surfaces rooted elsewhere keep serving pre-fix bytes, which is the clean-200-wrong-bytes
failure in its whole-tree form. Enumerate the roots, then verify at least one changed file in each:

```bash
grep -n 'root \*' /etc/caddy/vhosts/<site>.conf | sort -u
```

Where a repo ships a companion sync script for the secondary roots, it is part of the deploy rather
than a follow-up — run it last and treat a non-zero exit as a failed deploy, not a warning.

**A directory at the route path terminates the fallback chain.** With
`try_files {path} {path}/index.html /index.html`, a request whose path matches a real directory
satisfies the first term, so the third — the shell — is never reached and the route 403s or 404s.
Keep page assets flat beside the route (`public/<slug>-<name>.pdf`) rather than inside a directory
named after it (`public/<slug>/<name>.pdf`). Same first-match-wins mechanic as handler ordering,
expressed as file layout.

**The opposite failure: a file that never reached the mirror step.** A build that mirrors a
`public/` tree into the served tree usually carries an allowlist for `index.html` — top-level
`index.html` files are assumed to be SPA routes and are skipped so the compiled shell can replace
them. A hand-written static page under a deep path therefore lands in the source tree, is silently
skipped by the mirror, and never exists in the served tree at all. Its URL does not 404: the
`try_files` fallback walks up to the nearest real `index.html` and serves the **parent listing**, so
the page looks published while none of it is reachable.

```bash
# does the served tree hold what the source tree holds?
for f in $(cd <src>/public && find . -name index.html); do
  [ -f "<served>/$f" ] || echo "NOT MIRRORED: $f"
done
grep -n 'ALLOWLIST\|SKIP_DIRS' <scripts>/<mirror-step>.js   # find the gate, then read its entries
```

**Tell a missing artifact from a mis-routed one by checking a SIBLING asset in the same directory.**
When a document URL returns the parent listing, fetch a second file that should sit beside it — a
PDF, an image, a `.json`. If the sibling also returns `200` with `content-type: text/html` and a byte
size matching the listing, nothing was ever placed: a placement fault, not a routing one. `file` is
the cheapest adjudicator, because a wrong body defeats every status-code check:

```bash
curl -so /tmp/x "<url>.pdf" && file /tmp/x      # "HTML document" => never placed, not mis-routed
```

**Close the loop with a content grep, never a status code.** The artifact is verified only when the
response body carries a string unique to it:

```bash
curl -s -o /dev/null -w '%{http_code} %{size_download}\n' "$URL"   # 200 - necessary, not sufficient
curl -s "$URL" | grep -c '<string unique to the new artifact>'      # the actual receipt
```

A `200` with an unexpected body means the fallback fired — the artifact never reached the response.
Report that as "file deployed, handler not resolving it", a different fault from "the deploy did not
run", with a different fix. When a request resolves to the wrong document and no config was edited,
the cause is almost always handler ordering or the `try_files` fallback — not syntax, and not a
stale build.

Worked values for a Caddy-fronted SPA host with a split config and split roots — the dispatcher/
vhost layout, the `@static_dirs` vs `@spa_routes` split, the page-that-exists-twice check, and
the closure probe — are in `references/webroot-serving-resolution.md`.

## Publish ORDER is part of the deploy — a pointer published before its target poisons the edge cache

Every layer above is about whether a fix *reached* the served tree. This one is about the order in
which you put the pieces there, because with content-hashed artifacts the order is not a style
preference — getting it wrong is **permanent**.

Publish in this order, always:

```
1. assets/        the hashed artifact must exist at its URL BEFORE anything names it
2. pointers       every HTML/document that references the new hash
3. generated mirrors / secondary surfaces
```

**Why the order is load-bearing.** A hashed asset is normally served with `cache-control: public,
max-age=31536000, immutable`. If a document naming it goes live first, the first request for the
missing asset returns 404 — and the CDN caches the **404** under that same year-long immutable TTL.
Every later visitor is then served the cached 404 while the correct file sits on disk. The failure
is invisible to every check that looks at the filesystem, and the artifact's presence on disk is
exactly what makes it look deployed.

**Signature:** `curl -sI <asset-url> | grep -i cf-cache-status` → `HIT` with a small `age` on a
`404`. Compare against the served document's own pointer to confirm the mismatch.

**Recovery, in order of preference:**

1. **Purge the URL.** Needs a cache-purge scope on the credential. If the token lacks it you get an
auth error — that is a scope problem, not a transient one; do not retry with different payloads.
2. **Re-key the artifact.** Works with no purge permission, and it is the reliable path. Give the
   *identical bytes* a new filename, then repoint every document that referenced the old name:
   ```python
   # salt the hash so the NAME is guaranteed fresh even when the BYTES are unchanged
   new = hashlib.sha256(data + b"rekey-salt").hexdigest()[:8]
   ```
   Without the salt you regenerate the same poisoned name, because a content hash of unchanged
   content is by definition the same string. Find every referencing file with
   `grep -rl <old-name> <tree>` — the pointer is usually duplicated across many route shells, not
   just the one you edited — and rewrite them all.
   Leave the old file in place: it is still what any in-flight document is pointing at.
3. **Do not wait for expiry.** A year-long immutable entry does not age out on any useful timescale.

**Verify with an unbusted fetch.** A `?v=<timestamp>` query string is a different cache key, so it
returns 200 while real visitors still get 404 — it will report the exact opposite of the truth. The
honest check is the pointer comparison plus a plain fetch:

```bash
D=$(grep -oE 'assets/[a-zA-Z0-9._-]+\.js' <dist>/index.html | head -1)
L=$(curl -s <url>/ | grep -oE 'assets/[a-zA-Z0-9._-]+\.js' | head -1)
[ "$D" = "$L" ] && echo "pointer served: $D" || echo "DRIFT dist=$D live=$L"
curl -so /dev/null -w '%{http_code}\n' <url>/$D      # no query string
```

**A partial sync is the same defect in a different direction.** If the assets reach the served tree
but the document carrying the pointer does not, the new artifact sits there unreferenced and the
site keeps serving the previous build indefinitely. Check BOTH directions: pointer-not-reachable and
artifact-not-referenced are separate faults with separate fixes.

## A generated cache whose upstream is another cache

A build step that regenerates published output can itself read from a *stale cache* rather than from
the canonical source. The tell is a regenerated artifact with a fresh `mtime` and old content: it
looks updated because the timestamp is current, and it is wrong because its input was old.

```bash
# for every generated output, compare its mtime against ITS INPUT, not against the build
stat -c '%y  %n' <canonical-source> <cached-intermediate> <generated-output>
# then count how many cached intermediates are older than their canonical source
```

Two consequences worth acting on:

- **Check the generator's input, not just its output.** Reading the source file confirms the fix is
  present; only reading the *generator* tells you whether the fix can reach the output. A generator
  pointed at a stale intermediate is a build that can never publish the correct content.
- **Wire the generator into the build chain, or it drifts again.** If a regeneration step is not in
  the build's script chain, it runs when someone remembers and not otherwise — so the same staleness
  recurs silently. Adding it to the build is the durable fix; re-running it by hand is a one-time
  repair.
- **After fixing the source, RE-RUN the generator before republishing.** Outputs built before the
  fix still hold the old text on disk and in the served tree.

## The collapsed case: no build step (interpreted service from a live checkout)

When the artifact *is* the checkout — Python via editable install, `uvicorn`, `python -m <pkg>`,
any service with no build step — the dist layer collapses into source and the drift test changes
shape: **the running process is the artifact, and it is holding the modules it imported at start.**

1. **Running on what?** Process start time vs newest source mtime:
   ```bash
   systemctl show <unit> -p ExecStart -p ActiveEnterTimestamp -p MainPID
   ps -o lstart= -p <pid>
   find <install_dir> -name "*.py" -printf '%T+ %p\n' | sort -r | head -3
   # name the drifted SET instead of eyeballing two timestamps:
   find <install_dir> -name "*.py" -newermt '<unit ActiveEnterTimestamp>'
   ```
   Source newer than process start ⇒ the runtime is executing pre-edit code. Nothing else will
   catch this: there is no stale `dist/` to notice and no build log to read. The `-newermt`
   sweep turns the comparison into an enumerated answer — the exact modules the live process
   cannot be holding — and it is the same command that returns EMPTY after the restart, which is
   the after-receipt. Pair it with a named pre/post signal from the completed boot log (a
   traceback or warning count) so "the unit restarted" and "the fix is live" stay two separate
   observations.
2. **Which tree does `import` actually resolve to?** Ask the service's own interpreter:
   `venv/bin/python -c "import <pkg>, <pkg>.<module>; print(<pkg>.__file__)"` — an editable install
   routes through a `.pth` finder back to the checkout, so a same-named copy elsewhere on disk
   is a different program.
   **Run it from a neutral cwd, or from the unit's own `WorkingDirectory=`.** `sys.path[0]` is
   the current directory for `-c` and stdin scripts, so running the check from inside the
   checkout makes the dev tree win and prints exactly the path you were hoping to confirm. cd
   elsewhere first, or pin the deployed location explicitly
   (`sys.path.insert(0, "<deployed-site-packages>")`), and only then does the answer describe
   the service rather than your shell.
3. **Restart, then re-probe.** For a service you are running inside, schedule the restart detached
   (`systemd-run --on-active=Ns systemctl restart <unit>`) and do not judge health during the boot
   window. Coordination mechanics live in `live-service-ops`; this skill owns the *detection*.

## Procedure

Before declaring a fix "done" (especially an authority/governance change), run these in order:

1. **Uncommitted?** `git status --short <src>` — uncommitted changes mean source ≠ last build. A fix left in the working tree was never shipped, whatever the deploys or SHA rotations say.
2. **Stale build?** `stat -c '%y' <src> <dist>` — dist older than src ⇒ build is stale.
3. **Fix present in artifact?** `grep -n "<expected-fix-marker>" <dist>` — confirm the compiled output actually contains the change, not just that a SHA matches.
4. **Runtime on current build?** Compare the health endpoint's reported `commit`/`version` against `git rev-parse HEAD`. A health response naming an old commit means the running process is on a stale build.
5. **Restart + re-verify.** After rebuilding, restart the service and re-probe — a restart without re-probe is not verification.

## Drift Between NODES — the checkout that never moved

The layers above are all within one install. A second axis runs across machines: **a peer node
can hold a checkout of the same repo at an entirely different commit**, and nothing in your
local probe will show it.

**Signal:** a peer agent reports that a commit hash "is not a valid object", a deploy path
"does not exist", or a service "does not respond". None of these is an error. Each is a true
reading of *their* node, and both readings can hold at once — different machine, different
checkout, different deployed set.

**Node lock both sides before accepting or disputing anything.** Collect from each host:
`hostname`, `tailscale ip -4`, `git -C <path> rev-parse HEAD`, and the same path-existence
probe. Only when the two locks match does their finding describe *your* system. The
contradiction is frequently the more valuable result than either report on its own.

```bash
# Enumerate every checkout of the repo on this node, with HEAD and remote
find / -xdev -maxdepth 4 -name .git -type d 2>/dev/null | while read g; do
  d=$(dirname "$g"); r=$(git -C "$d" remote get-url origin 2>/dev/null)
  case "$r" in *<repo-name>*) echo "$d -> $(git -C "$d" rev-parse --short HEAD) | $r";; esac
done

# How far apart are the two checkouts? Is theirs even an ancestor of yours?
git -C <repo> merge-base --is-ancestor <their-commit> HEAD && echo "ancestor - they are BEHIND"
git -C <repo> rev-list --count <their-commit>..HEAD
```

**A peer's older checkout does not invalidate their file-level verification.** Before assuming
their reading is stale, check whether the file actually moved between the two commits:

```bash
git diff --quiet <their-commit> <your-commit> -- <path> && echo "IDENTICAL - their finding stands"
```

**"Behind" and "unpublished" are different findings — measure both, never infer one from the
other.** A checkout that has not fetched shows a large commit gap against your HEAD, and it is
tempting to conclude the work exists on one disk only. Usually it does not: the gap is
*unfetched* origin history, not *unpushed* local history. Measure each range separately:

```bash
git fetch origin                                 # refresh remote refs first
git branch -r --contains <commit>                # empty = not reachable from any remote ref
git rev-list --count origin/main..HEAD            # yours, absent upstream  -> UNPUSHED
git rev-list --count HEAD..origin/main            # upstream, absent here   -> UNFETCHED
```

A commit absent from origin proves unpushed only for the *measured* range. Report the count
with its diffstat — "N commits, M files, K lines" — because a "52 commits / ~19,800 lines on
one disk" claim and a "1 commit / 429 lines" reality imply completely different urgency, and
the party relaying the first will not re-measure. Back-up urgency must be sized by the measured
range, not by the staleness gap.

**Settle whether a push needs a merge before proposing it.** One command decides it, and it
changes the risk class of the remedy:

```bash
git merge-base --is-ancestor origin/main HEAD && echo "fast-forwardable - plain push is enough"
git merge-base origin/main HEAD      # equals origin/main  =>  HEAD already contains main
```

If `origin/main` is an ancestor of HEAD there is no divergence: a plain push suffices, with no
merge, no rebase, and no extra authority decision. Do not present the remedy as an open question
when the ancestry check has already closed it — and do not let a peer's "this may need a
rebase" stand unchallenged when one local command settles it.

**Do not patch until node authority is settled.** A patch applied to one node does not reach
the other; you produce a baseline that is correct on one machine and silently wrong on the
second. Resolve it explicitly — (a) have the stale node pull to the target commit, (b)
designate one node authoritative and the rest read-only, or (c) require every citation to pin
node + commit. Option (c) is weakest but needs no change; state which you are relying on rather
than assuming one.

**Cite code as `<absolute path> @ <short commit>`.** On a host carrying several clones of one
repo, an unpinned path makes "what does the code say" a question with several correct answers.

**Enumerate the WRITE side too — the drift that bites after you have done the work.** Everything
above proves what is *running*; it says nothing about where your own edit landed. A repo checkout
and the deployed tree are different filesystems, and a data/resource file you register into the
repo is NOT served if the unit's `WorkingDirectory` points elsewhere. On an interpreted service
the running code follows the checkout, but **loaded data does not** — it resolves from the
service's configured root at request time.

```bash
# 1. Where does the service actually read data from?
systemctl show <unit> -p WorkingDirectory
# then find the root constant in the loader (env-var overrides are common):
#   RESOURCES_DIR = Path(os.environ.get("<SVC>_RESOURCES_DIR", str(_REPO_ROOT / "resources")))
# 2. Diff repo copy vs deployed copy for EVERY file you touched — not just code
diff -q <repo>/<path> <deployed>/<path>
# 3. Never conclude from "I wrote it" — read the served copy back and count.
```

The failure mode is self-inflicted drift: you register/annotate/seed a resource into the repo,
report it as live, and the running service keeps serving the old file. You have then reproduced
the exact defect you were auditing. **Declare a data write done only after reading it back from
the path the service resolves — and name that path in the report.**

## Multiple deploy scripts in one repo — verify which tree each one writes

A repo can carry several scripts whose names all read like "deploy", each writing a *different*
tree, only one of which the service imports. Running the wrong one produces a green deploy, a
restarted unit, a health endpoint saying `aligned` — and unchanged runtime code.

```bash
# 1. Which tree does the running process import from? (authoritative, from the service itself)
systemctl show <unit> -p WorkingDirectory -p ExecStart
curl -s :PORT/health | jq -r '.runtime_import_path'      # or the pkg's __file__

# 2. Enumerate every deploy script and the destination each writes
grep -n 'SRC=\|DST=\|rsync\|pip install\|VENV\|cp .*app' scripts/deploy*.sh

# 3. Prove it end-to-end: hash ONE file you just changed, in every candidate tree
md5sum <repo>/<pkg>/<changed>.py <deployed>/<pkg>/<changed>.py
#    repo == deployed  -> the deploy reached runtime
#    repo != deployed  -> you ran the script that writes somewhere else
```

Do not accept "the deploy script is the sanctioned path" as evidence it reached the service — the
sanctioned path can be the wrong path, and it will report success either way.

**A `.git_commit` stamp makes drift detection lie.** When the health endpoint computes alignment by
diffing a written stamp file against git HEAD rather than hashing the loaded module, a deploy that
only touched a *different* tree still flips the status to `aligned`. The stamp attests "a deploy
ran", not "this code is running". Always close the loop with a content hash of a file you changed,
read back from the import path the service reported.

## Find the unit by the PORT, not by the name you guessed

`systemctl show <unit>` only works once you already hold the right unit name, and a service name
rarely matches the thing you are looking for. Guessing the name (`<repo>-mcp`, `<pkg>`, `<pkg>mcp`)
returns an empty unit and **no error** — which reads like "the service does not exist" while it is
running fine under a different name. Walk it backwards from the socket instead:

```bash
ss -tlnp | grep ':<port>'                        # -> pid
echo "$?"                                        # capture through nothing; the pipe hides it
ps -p <pid> -o pid,etime,cmd --no-headers         # interpreter + exact launch form
ls -l /proc/<pid>/cwd                             # tree the process resolves relative paths from
cat /proc/<pid>/cgroup                            # 0::/system.slice/<unit>.service  <- the unit
systemctl show <unit> -p ExecStart -p WorkingDirectory -p ActiveEnterTimestamp
```

The `cgroup` line names the owning unit exactly, and `cmd` reveals the launch form. A bare
`<venv>/bin/python -c "from <pkg>.<mod> import main; main()"` is the collapsed case from above:
the process holds modules from an install tree, so the repo you edited may not be the tree at all —
and the same file can exist as a second, independently stale copy inside the venv's
`site-packages`. Hash every candidate before deciding which one is live:

```bash
find / -path /proc -prune -o -path '*/<pkg>/<module>.py' -print 2>/dev/null
md5sum <repo>/<pkg>/<module>.py <deployed>/<pkg>/<module>.py <venv>/lib/*/site-packages/<pkg>/<module>.py
```

## An auto-deploy timer makes the COMMIT the deployment, not the restart

Some hosts run a reconciler on a short timer that pulls `origin/main` and restarts the service
by itself. On such a host the production boundary is **push**, and it is easy to hold the wrong
object in mind: the operator believes they are holding a restart while what actually gates the
deploy is the working tree.

```bash
systemctl list-timers <reconciler>.timer           # armed? how often?
cat /etc/systemd/system/<reconciler>.timer | grep OnCalendar
```

Read the reconciler's own hold conditions before promising anything about it — the common set is
`flock` single-instance, **clean working tree**, fast-forward-only, and "local ahead of origin →
hold". Then verify the gate from the log rather than from the script's intent:

```bash
journalctl -t <reconciler> --since "30 min ago" | tail
# "origin ahead (...) but tree dirty — holding"  <- the only reason the deploy has not fired
```

Consequences worth stating out loud:

- **An uncommitted fix is protected by accident.** The dirty tree is what stops the timer. It is
  also a single point of failure: any other session that commits and pushes ships your work,
  unverified and unreviewed, within one timer interval. Do not present "it is not deployed" as a
  state you control when a third party's push changes it.
- **Do not clean up the tree to "tidy" it.** `git add -A && commit` on a shared host is a deploy
  action, not bookkeeping.
- **Announce the authority boundary in the right terms.** "It will restart the service"
  understates it; "the commit ships it, and the timer restarts the service about N minutes later"
  is the claim the operator can actually reason about.
- When a peer declares a hold on this basis, a hold that depends on a dirty tree is a
  *conditional* hold. Say so, with the condition named.

## Every process, not just the main one

`systemctl show -p MainPID` names ONE process; an interpreted service usually runs several that
each imported the module at their own start time. A worker can hold pre-edit code while the main
unit holds the fix — and workers frequently resolve from a **different tree** than the service.

```bash
# candidate set by ARGV (never by comm/process name)
pgrep -af "<pkg>" ; pgrep -af "/opt/<app>"
# + children of the unit, + any python carrying the venv in its environ
for p in $(pgrep -x python3); do tr '\0' '\n' < /proc/$p/environ 2>/dev/null | grep -q "<venv>" && echo $p; done
```

Filter by **argv, never by name**: a database client or daemon whose *comm* merely contains the
organ name joins the list (it is not running your code at all), while a worker launched as
`python -c` carries no organ name where a name search looks and is silently dropped. Union the
candidate sets, then test each PID against **the file that PID resolves** — a `-m` worker with
`PYTHONPATH=<dev tree>` loads from the dev tree while the service loads from site-packages, so a
single global mtime is the wrong comparison and clears the wrong process.

**`/proc/PID/maps` does not list Python source.** Interpreted `.py` is read, not mmapped; maps
shows only C extensions. Its silence is no information, not absence — resolve the package root
and grep that tree's contents for the guard symbol rather than grepping `import` statements (a
relative or lazy import inside the package pins the whole tree from one root resolution, and an
import-statement grep misses both).

**Exercising a guard is safe when you call the guard itself.** It returns its verdict before any
socket opens, so a blocked address performs no fetch — no need to aim it at a live endpoint, and
never do: if the guard were wrong, the response body would land in whatever audit layer wraps the
call and the test becomes the exfiltration. Import the leaf guard module only; importing a whole
application module can boot the runtime or hang.

## A fail-closed change is a dependency change — verify the chain, not the diff

Converting a permissive path to fail-closed does not merely edit a branch; it makes the service
require a set of prerequisites that previously did not matter. Those prerequisites are **not in the
diff**, so the change reviews clean while the deployed service refuses everything.

Probe the chain in order and name which link fails:

```bash
systemctl show <unit> -p Environment | grep -c <EXPECTED_CRED_VAR>   # first refusal point
<service-interpreter> -c "import <module>"                          # second
<backing-store> ping                                                # third
journalctl -u <unit> --since "<deploy time>" --no-pager | tail -30    # which one actually fired
```

Rules:
- **A successful package install is not a working dependency.** Package name and import name
  diverge routinely — a distro package can ship module `PAM` while the code imports `pam`. Confirm
  what was placed and under which name (`dpkg -L <pkg> | grep -E '\.so|\.py$'`, or
  `find <site-packages> -name '<mod>*'`), then import it **with the interpreter the unit runs**,
  not the one on your PATH. Two packages may be needed for one import.
- **An undeclared dependency is invisible until it breaks.** If the import is absent from
  `requirements.txt`/`pyproject.toml`, nothing catches it on a fresh build. Add it while you are there.
- **Report the true state as `BLOCKED_AT_GATE`, never as done.** If applying the change needs a
  gated verb (service restart, privileged write), the change is on disk and **not live**. Say
  exactly that, name the lane that can apply it, and do not describe it as staged or applied.
- **Do not revert a hardening change to "restore" a lane — measure the pre-change behaviour first.**
  A lane can already be dead upstream of the change (unreachable backing store), so the revert
  restores nothing while reopening the insecure path: a security regression wearing the shape of a
  fix. Establish empirically what worked before, and if the only path that worked was the insecure
  one, say so rather than proposing rollback.
- **After a fail-closed change, health must report capability, not liveness.** A liveness endpoint
  answering `{"status":"ok"}` while the service refuses every request trains monitors to ignore a
  dead lane. Add guard/dependency state to the health payload — a hardening that no probe can see
  is indistinguishable from an outage.

## A handshake that echoes your request measures nothing

Version and capability negotiation commonly **return the value you asked for** when it is
supported. A single probe then reports your own request, not the server's ceiling, and any
conclusion drawn from it is unfounded.

```bash
# vary the input to find the real value
request A -> A
request B -> C   # C is the ceiling; A and C are different surfaces of one organ
```

Same class as a marker probe matching the echo of its own log line. When several surfaces of one
organ report the same fact (root / health / tools / build-info / handshake), probe at least two and
report the disagreement rather than picking a winner — a version read from one endpoint is a claim
about that endpoint only.

## Pitfalls

- **A kernel/monitor "deployed SHA" field may be attesting the DEV CHECKOUT, not the deployment.**
  An attestation that reads `<root>/.git/HEAD` for an organ path answers "what does the repo say",
  not "what is serving" — and when the service runs from a separate deployed tree, the two are
  different commits that both look authoritative. Before treating any `organ_shas` / `git_version`
  / `built_commit` field as deployment evidence, read the code that populates it and confirm which
  path it stats. A monitor can be green, correct, and pointed at the wrong object.
- **A health endpoint may report the DEPLOYED commit while the kernel attests the REPO commit, and
  both are honest.** When they disagree, that disagreement is the finding — not a bug in either.
  Name the three objects explicitly (source of truth repo / deployed tree / running process) and
  say which one each number describes.
- **SHA-vs-`.git_commit` checks miss the middle layers — and pass a third time on an interpreted service.** They pass (or stay silent) on the uncommitted-source case, on the uncompiled-build case, AND when the checkout is current while the process predates the edit. Timestamps beat SHAs on all three: file mtime vs artifact mtime vs process start.
- **Authority/logic fixes rot silently; substrate failures scream.** A stale governance path returns `status: SEAL` and looks like success, while a broken substrate raises a timeout/EROFS/load-spike. Absence of a failure signal is NOT evidence the fix shipped — verify explicitly.
- **Governance gates can be advisory.** A pre-commit hook that prints "DRY-RUN: would have blocked" or warns "requires LSP probe" but still commits is reporting, not enforcing. Trust a gate's blocking behavior only after you have seen it actually refuse a change.
- **SDK major-version drift.** An import/transport error naming a rename (`cannot import name 'McpError'`, missing `_check_accept_headers`) means the installed SDK major differs from what the code targets. Check the declared pin (`requirements.txt`/`pyproject.toml`) vs installed (`pip show`). If the codebase declares the newer spec era (e.g. `2026-07-28` stateless MCP), migrate code FORWARD to the installed SDK — pinning back to the legacy SDK while claiming the modern spec is narrative-over-reality.
- **Symlinked deploy dir ⇒ multiple source trees.** A running service may execute a symlinked tree (`/opt/x/app/pkg -> /root/<other-repo>/pkg`) that is a DIFFERENT copy from the standalone repo you found first. Resolve `readlink -f` on the deployed path and `diff` it against your assumed source BEFORE diagnosing: a stale sibling copy will show you a bug the live code already fixed (e.g. a retired organ still listed in the stale copy's config while live code removed it). Same trap for config paths: check the process's ExecStart, not the path in the docs.
- **A shared interpreter path can itself be a symlink, and one stale target takes every consumer down together.** Where many units launch through the same `<venv>/bin/python`, check whether that path is a real directory or a link (`ls -l`, `readlink -f`). If it is a link, a target that moves or disappears breaks every unit referencing it with no unit file edited — the blast radius is the whole set, not the service you happen to be looking at. Size it by enumerating the consumers (`grep -rl '<venv-path>' /etc/systemd/system`, then `systemctl show <unit> -p ExecStart`) and testing each entrypoint against the intended interpreter rather than the one that currently resolves.
  The error text lies in a specific, repeatable way: a stale interpreter path surfaces as a **missing-package** error from a lazy or optional import (often a traceback-formatting dependency) rather than an unambiguous path error. Run the interpreter path directly to reproduce before believing a module is absent — the module is usually present and the interpreter is not.
- **Liveness is not boot-readiness, and a green fleet can be uniformly unbootable.** Units that are already running keep answering their health check from file handles the kernel is holding open, so every probe returns healthy while no unit could start again. This is the state a missing shared path produces, and it is invisible to exactly the checks you would reach for first. Report "running" and "can start" as two separate findings, and never let the first stand in for the second.
- **Where doctrine names a successor origin for a shared path, check the resolved target against doctrine, not merely that it resolves.** A link repaired to point at the deprecated origin turns an outage into silent drift, and it will look like a fix from every angle except the doctrine document. Confirm the target, cite the doctrine, and if the live set is on the superseded origin, say so as an open finding rather than closing the incident.
- **A process that runs is not a process that works.** Idle daemons expose self-metrics — check them before assuming the pipeline is live. An OTEL collector with `otelcol_receiver_accepted_*` absent and only `otelcol_exporter_queue_*` for one exporter has carried ZERO traffic since boot: it is decorative, and "its config file is missing" is not a P0 if the real data path bypasses it entirely. Trace where the data actually enters (grep for the producer: a patch module, a direct NATS/pg publisher) before assigning severity.
 - **A capability shipped is not a capability in service.** One level up from the idle daemon: an
 ingest lane, an inversion engine, or a sandbox can be present in the deployed source, importable,
 and even listed on the service surface, while the input it consumes has never been ingested. It
 will then emit **plausible numbers from empty or default input** — which is worse than a missing
 tool, because nothing errors and nobody doubts the output. Probe the DATA condition separately
 from the CAPABILITY condition and report them as two facts; "the engine exists" is not "the test
 can run". When someone proposes a run on this basis, check for the input first.
- **Missing config on disk is a latent, not an active, outage.** A service started from a config file that has since been deleted keeps running from memory — healthy now, unbootable on next restart. Say "reboot-fragile", not "down", until you have checked whether it is in the data path at all. When you do rebuild the file, call it a RECONSTRUCTION, not a restore, and validate it with the service's own validator (`<binary> validate --config=...`) before restarting.
- **A source default is not live state.** Code carries seeded default templates — a baseline dict, a port list, a config literal — while the runtime state file may already be correct. Grepping the default and reporting it as the deployed value manufactures a defect that does not exist. Read the runtime artifact (the JSON/YAML the process actually loads) for the current value; read source only to learn the shape.
- **Written ≠ registered ≠ verified — name the LAYER you checked, never collapse three into one boolean.**
  A binding can be declared at one layer and absent at the next, and each layer answers a different
  question: a **config key written** says only that a value was stored; a **provider/handler registered**
  says the runtime can ADDRESS it by name; a **lane script verified end-to-end** says it produces the
  right output at the intended settings. Measured on one voice binding: the provider was registered and
  reachable by name, a separate set of `voice.*` config keys existed that no runtime path reads at all,
  and the shared command the provider wraps hardcodes its own pace — so the same input rendered 33.40 s
  via the provider route and 36.14 s via the lane script, ~8% apart, **both passing their correctness
  checks**. Reachable ≠ calibrated. Run BOTH routes, report the delta, and put the honest state in the
  report ("provider registered, lane verified, keys written but unread") rather than "the voice is now X".
- **An inert config key is not a route, and a dormant scaffold is not an integration.** A module written
  to consume a binding but never wired into the runtime may still pin its OWN constant — including a
  value the authoritative registry has since superseded or deprecated. Reading that file answers "what
  did someone intend", never "what runs". Before citing any config-driven behaviour, name the code path
  that reads the key; if you cannot name it, the key is documentation.
- **Check whether the component self-maintains before calling its state stale.** If a service rewrites its own state file on a cycle, a stale value means the cycle is not running — not that the value needs hand-editing. Restore the schedule and the state often normalises itself, which also changes the diagnosis from "two faults" to "one fault with a symptom".
- **Multi-session edits to the same file — and to live config, where there is no VCS to notice.**
  In a multi-agent environment, `git status` may show a NEW uncommitted change that appeared
  mid-session (another agent editing the same file). Re-check `git status` after you commit; never
  commit working-tree state that is not yours. The sharper case is a **live config file outside any
  repo** (`/etc/<svc>/*.conf`, `/var/www/**`): two agents can write the same file seconds apart,
  neither aware of the other, and nothing reveals the collision. `stat -c '%y'` the file before and
  after your write — an mtime you did not cause means stop and read the current content before
  continuing. A diff of only cosmetic parameters is luck; the same mechanism aimed at a routing or
  proxy target takes the service down with no warning. Assign exactly one writer per live config
  file; everyone else hands over a patch.
- **An interpreted runtime keeps pre-edit modules in `sys.modules` — and a mixed-version agent is the normal outcome.** The process that booted before your patch keeps serving the old module for its whole life; log lines from that PID are the old code's behaviour. An updater that pulls code without restarting the unit will usually say so itself; treat that banner as a receipt, not as noise to dismiss.
- **`dist-info` is an installation record, not the code on disk.** An editable install's package metadata stays frozen at install time while the checkout moves, so `pip show` / reported package version can trail the code the process actually runs. Read the module's `__file__` and the git state of that tree instead of reconciling versions.
- **`grep -c <marker> <path>` cannot tell "guard absent" from "file absent".** A grep against a
  path that does not exist yields zero hits and reads as a missing fix, when the real situation
  is that the path was never a deploy target. Test existence first (`[ -f "$p" ] && grep ...`),
  and enumerate every candidate tree — repo, deployed app dir, venv `site-packages` — before
  concluding anything. On hosts where the service imports from an installed package, the app
  directory you grepped may not contain the package at all, and "absent" then means you looked
  in the wrong place, not that the work was lost.
- **A patch in an install dir has no build fallback.** With source-plus-build, a lost working-tree edit can be rebuilt from a commit; with an interpreted install, the working-tree diff may be the *only* copy of a live fix. Copy it to a named backup with a `sha256sum` manifest before any updater runs, and treat it as unshipped until it is committed.
- **A registry snapshot that names your new commit is not proof the fix is live.** Kernel/monitor snapshots read repo HEAD, so they flip to the patched SHA the moment you commit — while the process still holds the pre-commit module. Re-run the original attack after restart and show the changed verdict; a snapshot agreeing with you is the weakest possible receipt here.
- **Two nodes can hold the same repo at different commits and both report honestly.** Pin every citation as `host + repo path + short sha`; line numbers are not portable between nodes, and a patch built on the wrong node's numbers lands on ghost lines. Load `proxy-verification-audit` when the change being deployed is a security/authority control — it owns proving the control actually refuses something.
- **Prove a library major bump by executing, not by reading.** An SDK going one major version up reads like the headline blocker and usually is not. Check the call surface the code actually uses — constructor keyword arguments, transport argument names, decorator signatures — for removed or renamed parameters, then run one initialize handshake per entrypoint on the new interpreter and confirm each registers its full tool set. Record the cosmetic drift too: a server that does not pass an explicit version of its own will report the library's version in its handshake instead. This is the empirical half of the SDK-drift pitfall above; the static pin comparison tells you a delta exists, only the handshake tells you whether it breaks anything.
- **Two venvs can differ only by their system-site-packages flag, and the difference presents as missing modules.** Identical CPython version and identical core pins (`pydantic`, `starlette`, `uvicorn`, `anyio`) do not mean identical surfaces: read `include-system-site-packages` in each `pyvenv.cfg` before diffing long package lists, because the interpreter with the host global `dist-packages` visible sees hundreds of packages the isolated one does not — one flag, an enormous diff, and a misleading "the new venv is missing X" conclusion. The migration blocker is then rarely the framework major bump but the few entrypoints reaching into the host pool; install those specific packages into the isolated venv and verify by importing them under that interpreter, rather than re-enabling system-site-packages to make the diff go away. Do the install with a dry run first (`pip install --dry-run`) to see the full resolver plan before committing to it.
- **The checkout moves under you — re-pin HEAD immediately before every write.** A registered peer seat can commit to the same repo while your session is live; between auditing a file and patching it, HEAD can advance several commits and every line number, function name, and existence check you gathered now describes a ghost revision. Identify the mover by author — `git log -6 --format='%h | author=%an | %ci | %s'` — because a named FI seat is a coordination problem while an unrecognised author is an incident. Re-run `git log -1` and check for an in-flight writer (`ls .git/index.lock`) at the moment of the commit, not at the start of the task. A discovery that the target moved is itself worth reporting: it is live evidence that the provenance chain is not closed.
- **Select the tree to patch by grepping a string you captured AT RUNTIME.** The envelope or response you observed was produced by the code that is actually executing. Grep that exact string in the candidate tree: if it is absent, you are in the wrong tree and the patch lands silently nowhere. A runtime-observed string is the strongest available tree selector — stronger than a path you assumed, a directory named like the package, or a SHA a monitor reports, because it is bound to observed behaviour rather than to metadata.
- **Two paths for one message is a finding, not an inconvenience.** When the same defect surfaces through a bare builder and through a wrapper (two different strings for the same concept in two code paths), a patch to one path leaves the other emitting the old shape. Enumerate the paths first and cover both, or say explicitly which one you fixed and which remains — a half-applied fix reads as "fixed" to everyone downstream.
