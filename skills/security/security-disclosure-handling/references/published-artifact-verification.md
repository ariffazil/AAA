# Published-Artifact Verification

Some claims are about what a *consumer* gets, not what the repo contains. "Fixed and
deployed" can be true for the running service and false for `pip install` / `npm i` /
`docker pull`. Three layers, three separate probes:

| Layer | Question | Probe |
|---|---|---|
| repo | Is the fix committed on the default branch? | `git log -1 -- <file>`; `git diff <deployed>..HEAD -- <path>` |
| service | Is the running process serving it? | md5 the repo file against the path the service imports; health endpoint drift field |
| artifact | Does an install get it? | registry JSON + open the published archive |

## Recipe

### 1. What is published, and when?

```bash
curl -s https://pypi.org/pypi/<pkg>/json -o /tmp/p.json
python3 - <<'EOF'
import json
d = json.load(open('/tmp/p.json'))
print('latest:', d['info']['version'])
rows = [(f['upload_time'], v) for v, fs in d['releases'].items() for f in fs]
for r in sorted(rows)[-6:]:
    print(r)
EOF
# npm:    npm view <pkg> time --json | tail -5
# docker: docker manifest inspect <img> | jq .
```

Compare the newest `upload_time` against the fix commit's date. **Artifact older than the
fix = the fix is not shipped**, whatever the repo and the service say. In a disclosure
thread this is the difference between a true acknowledgment and a false one.

### 2. Open the artifact and inspect it

```bash
python3 - <<'EOF'
import zipfile, hashlib
zp = zipfile.ZipFile('/tmp/<pkg>-<version>-py3-none-any.whl')
inside = zp.read('<pkg>/<module>.py')
repo   = open('<repo>/<pkg>/<module>.py','rb').read()
print('artifact:', hashlib.md5(inside).hexdigest())
print('repo    :', hashlib.md5(repo).hexdigest())
print('identical:', inside == repo)

# call-site completeness INSIDE the artifact, not in the repo
print('uses fix:', [n for n in zp.namelist()
      if n.endswith('.py') and b'<new_symbol>' in zp.read(n)])
# any shipped file still importing the deprecated module?
print('stale importers:', [n for n in zp.namelist()
      if n.endswith('.py') and b'from <pkg>.old_guard' in zp.read(n)])
EOF
```

Also read the shipped module's docstring: credit lines and residual notes living in source
are part of what the artifact publishes, and a reviewer will read them.

### 3. If the pipeline is red, read WHY before promising a date

```bash
gh run list --workflow=<publish>.yml --limit 5
gh run view <run-id> --log-failed | tail -40
```

Registry-side settings — trusted-publisher / OIDC claim mismatch, environment name,
workflow filename, repo casing — are fixed on the registry website, not from the host. A
claim dump showing `environment: MISSING` while the registration expects one is a
mismatch, not a transient. One failed run proves it; do not burn repeated dispatches. If a
still-valid token secret exists from the earlier publishing lane, reverting to it is a
one-line change and unblocks the release immediately — record in the workflow comment why
the OIDC lane is off, so the next agent does not "restore" it blindly.

## Dangerous-pattern sweeps: classify COMMENT vs CODE

A grep for a fixed vulnerability returns both the live flaw and the docstring explaining
the fix. Split them before counting either as open or as clean:

```python
for i, l in enumerate(src.split('\n'), 1):
    if '<pattern>' in l:
        print('COMMENT' if l.strip().startswith('#') else 'CODE', f'{path}:{i}: {l.strip()[:100]}')
```

## Pre-empting scanner false positives (reachability, not pattern)

A static scanner flags *shape*; a human must supply *reachability*. For every surviving hit
ask: **is the target caller-supplied, or a fixed host the service chose?** Internal health
probes, vendor API endpoints, and self-identity checks legitimately carry permissive
settings.

Tabulate leftovers as `file:line — who supplies the target — why it is not the same class`,
hand the table to the reviewer, and invite falsification ("test this reasoning rather than
inherit it from me").

## Verifying the fix landed *remotely*

A push and a public read are different events. Raw/CDN paths (`raw.githubusercontent.com`,
jsDelivr, registry mirrors) can serve a cached copy for minutes after a push, so a stale
raw read is not evidence the push failed. Confirm through the API:

```bash
gh api repos/<owner>/<repo>/contents/<path> --jq '.content' | base64 -d | sed -n '1,8p'
```

Treat the API read as authoritative and the raw read as inconclusive — and never "fix" a
file a second time on the strength of a stale raw read.

## Hand-maintained version strings drift on their own

A version/status string in a README (SOT-manifest header, a "Published X" row, a versioning
note) is a drift site: nothing regenerates it, so it quietly contradicts the table a few
lines below it. When one copy is stale, grep every other copy of that value in the repo and
fix them in one commit — and check whether the field's generator covers it, or the drift
returns on the next release.
