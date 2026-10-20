---
name: serving-parity-audit
description: Audit whether a deployed site really serves its repo.
---

# serving-parity-audit

How to answer "what is actually deployed, and does it match the repo" without inventing drift or missing real drift. Load for "audit this site", "is X missing from live", "repo vs live drift", "why is this page stale", or when a relayed audit claims the surface is clean.

Every rule below was established by probing live state, not by reading prose.

## The five trees — name them before comparing anything

A deployed site is not two things (repo, live). It is five, and each pair answers a different question:

| Tree | Tracked? | Comparing it to live answers |
|---|---|---|
| `src/` | yes | is the app source shipped? |
| `public/` | yes | **is the repo's static content served?** |
| `dist/` | usually **no** (gitignored) | is the build current? |
| deploy snapshots / backups | varies | what did live look like before? |
| live webroot(s) | n/a | what a human receives |

**Rule:** `diff dist/ live/` reports BUILD staleness. Reporting it as "repo vs live drift" is a category error — a gitignored build tree has no tracked state to drift from. Compare `public/` when the question is repo drift; compare `dist/` only when the question is build currency.

Verify which tree is tracked before quoting any number:

```bash
git ls-files <path> | wc -l                            # >0 = tracked
cd <repo> && git status --porcelain | wc -l            # dirty count
git rev-list --left-right --count origin/main...HEAD   # behind / ahead
```

`dirty=0` says nothing about deployment. A commit that exists locally and is unpushed is still unshipped — check ahead/behind and say it explicitly. Committed ≠ pushed ≠ deployed ≠ served: four states, four probes.

## Split-root webroots — never assume one root

Caddy/nginx vhosts frequently root different path families at different directories. Comparing a family against the wrong root produces a large, entirely fake drift count.

Build the map from the config, not from memory:

```bash
grep -nE 'handle |root \*|try_files|redir ' /etc/caddy/vhosts/<site>.conf
```

arif-fazil.com example: `/earth* /words* /world* /work* /pilot*` → `/var/www/html` (top level); `/data/*` and the SPA fallback → `/var/www/html/arif`; `/000` `/999` → `/var/www/html/arif/000|999`; `/mcp` → `/var/www/html/mcp`. The bare `/etc/caddy/Caddyfile` only imports vhosts — never audit the importer.

Split roots also mean a post-deploy sync step is mandatory. If one family is stale while its siblings are current, suspect the sync script's family list before suspecting the content.

## Direction of an orphan decides its severity

A two-way diff yields three buckets, and they are not equally interesting:

- **only-in-live** — hand-edited on the server, absent from the repo. Destroyed by the next `rsync --delete`. **Report this first.**
- **only-in-public** — built but never shipped, or deliberately redirected elsewhere. `curl -sI` the route and check for a 301 before calling it missing.
- **differ** — staleness or a genuinely split stream. Compare mtimes on both sides to learn the direction of travel.

Reachable-but-superseded is the dominant real-world state: live returns 200 with a design or index from weeks ago.

## A claim of "no drift" must enumerate the families probed

One clean family is not a clean site. An audit that probes `earth/` and concludes the surface is healthy will miss `world/` serving an obsolete design system, `words/` pointing at a dead bundle hash, and a bot-only corpus whose index is a month old.

Report shape: one row per family — src count, live count, only-src, only-live, differ — then a verdict per family. Anything not probed is `UNMEASURED`, not clean.

## HTTP 200 is not freshness

Deploy gates commonly assert reachability only. A green gate over a stale page is a normal steady state, not a contradiction. Freshness probes:

```bash
stat -c '%y %n' /var/www/html/<fam>/<route>/index.html
curl -s https://<host>/<route>/ | grep -oE '<marker only the current build emits>'
```

Never say "the page is fine" without one of those two.

## Parity probe (run this, don't hand-roll it each time)

Two-way diff per family, each compared against its own serving root. Edit `MAP` to match the vhost you just grepped; exits 1 on any divergence.

```bash
#!/usr/bin/env bash
set -uo pipefail
REPO="${1:-/root/arif-fazil.com}"
SITE="$REPO/sites/arif-fazil.com/public"
TOP="/var/www/html"; ARIF="/var/www/html/arif"
# family:serving_root — keep in sync with /etc/caddy/vhosts/<site>.conf
MAP="earth:$TOP words:$TOP world:$TOP work:$TOP pilot:$TOP makcikgpt-md:$TOP data:$ARIF proof:$ARIF institution:$ARIF human:$ARIF"

fail=0
printf '%-15s %6s %6s %9s %10s  %s\n' FAMILY SRC LIVE ONLY_SRC ONLY_LIVE VERDICT
for pair in $MAP; do
  fam="${pair%%:*}"; root="${pair#*:}"; src="$SITE/$fam"
  [ -d "$src" ] || { printf '%-15s %6s  (skipped)\n' "$fam" "-"; continue; }
  ns=$(find "$src" -type f | wc -l)
  if [ ! -d "$root/$fam" ]; then
    printf '%-15s %6s %6s %9s %10s  LIVE-MISSING\n' "$fam" "$ns" 0 - -
    fail=1; continue
  fi
  nl=$(find "$root/$fam" -type f | wc -l)
  d=$(diff -rq "$src" "$root/$fam" 2>/dev/null)
  os=$(printf '%s\n' "$d" | grep -c "^Only in $src")
  ol=$(printf '%s\n' "$d" | grep -c "^Only in $root")
  nd=$(printf '%s\n' "$d" | grep -c '^Files .* differ')
  if [ "$os" -eq 0 ] && [ "$ol" -eq 0 ] && [ "$nd" -eq 0 ]; then v="IN-SYNC"; else v="DIVERGENT ($nd differ)"; fail=1; fi
  printf '%-15s %6s %6s %9s %10s  %s\n' "$fam" "$ns" "$nl" "$os" "$ol" "$v"
done
exit $fail
```

A one-directional check ("repo file exists on live?") cannot see live-only artifacts — and those are exactly the ones a deploy will destroy.

## Writer / reader split-brain — the silent data-loss class

A generator writes fresh artifacts to directory **A**. The step that feeds the site rsyncs from directory **B**. Both run green, daily, forever; the good artifact never reaches a human.

Detect by comparing the identity fields of the same filename across every copy (writer dir, repo `public/`, live root):

```bash
for p in <writer-dir> <repo>/public/data/<topic> /var/www/html/arif/data/<topic>; do
  echo "== $p"
  python3 -c "import json;d=json.load(open('$p/latest.json'));m=d.get('meta',{});print(m.get('date'),m.get('generated_at'),str(m.get('source'))[:50])" 2>/dev/null
  echo "   archives: $(ls $p/archive 2>/dev/null | wc -l)"
done
```

Different `source` or `generated_at` across copies means **two streams**, not one stale stream. A frozen archive count (archives stop on an old date while newer files exist elsewhere) is the corroborating tell.

Fix: one artifact, one home, and both the writer and the sync point at it. **Repoint the sync source before touching the writer's output directory** — deleting the writer's destination to "clean up" kills the feed with no error anywhere.

## Don't call a directory a ghost before you find its writer

No `.git` does not mean dead or orphaned. Before recommending archive or delete:

```bash
crontab -l | grep -i '<name>'
grep -rn '<name>' /etc/cron.d/ /root/.hermes/cron/jobs.json 2>/dev/null
grep -nE 'Path\("|SRC=|DEST=|OUT_DIR' <the scheduled script>
```

A directory with no git history can still be the live output target of a daily generator. Class a tree by its writer, not by its provenance.

## De-duplicating backup mass — measure content, not apparent size

`du -sh` sums apparent bytes and will quote a duplicated backup set at face value. What matters is reclaimable space. Size-bucket first (cheap), hash only within same-size groups:

```python
import os, hashlib, collections
bysize = collections.defaultdict(list)
for d in BACKUP_DIRS:
    for root, _, files in os.walk(d):
        for f in files:
            p = os.path.join(root, f)
            try:
                s = os.stat(p).st_size
                if s > 1024: bysize[s].append(p)
            except OSError: pass
total = sum(k * len(v) for k, v in bysize.items())
uniq = {}
for s, paths in bysize.items():
    if len(paths) == 1:
        uniq[('single', paths[0])] = s; continue
    for p in paths:
        try: h = hashlib.md5(open(p, 'rb').read()).hexdigest()
        except OSError: continue
        uniq[(h, s)] = s
ub = sum(uniq.values())
print(f"apparent={total/1e9:.2f}GB unique={ub/1e9:.2f}GB reclaimable={(total-ub)/1e9:.2f}GB")
```

Report apparent, unique, and reclaimable as three separate numbers. Never present `du -sh` as "duplicate, safe to delete" — it proves nothing about content.

## Auditing a relayed audit

When someone else's audit arrives claiming the surface is clean, treat it as claims to ground, not conclusions to carry. Reproduce each structural claim with a probe, then mark BETUL / SALAH / SEPARUH with the evidence.

The two failure modes to look for, in order:

1. **Under-coverage presented as coverage** — "no drift" based on one family. Check which families were actually probed; unlisted = unmeasured.
2. **A dangerous recommendation** — "archive/delete this directory" for something that turns out to be an active writer's output. Always find the writer first.

## Reporting shape

Lead with what the relayed audit got right, then the corrections with evidence, then the one finding that costs something if ignored. Enumerate families and verdicts. End with the single next action that needs a human decision — not a menu.
