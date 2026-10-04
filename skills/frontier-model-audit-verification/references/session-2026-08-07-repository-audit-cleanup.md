# Session 2026-08-07 — Repository Audit & Cleanup

Session-level reference for the audit-cleanup cycle that produced durable
lessons about EMD/Gemini audit reliability, GitHub protected-branch workflows,
and source-of-truth recovery via quarantine.

## 1. EMD/Gemini/888 audit premised on wrong shapes — verify the actual schema

**Pattern.** When a frontier-model auditor (Gemini, EMD, 888, Frontier) pastes a list
of "deltas absent from all canon registries", the auditor has likely searched for one
*assumed* field shape and concluded entries are missing when they're actually there
under a different key.

**Verified case (2026-08-07):**

EMD claimed *"6 deltas — active, layer-tagged repos absent from all canon registries"*
(`arifOS-model-registry`, `compose`, `EEE`, `A2B`, `searxng`, `ariffazil`).

Live ground truth from `web-canon/canon/federation.json`:

```json
{
  "asset": "arifOS-model-registry",   ← shape uses "asset" not "id"
  "layer": "L3",
  "github": "ariffazil/arifOS-model-registry",
  "kind": "reference",
  "posture": "READ_ONLY",
  ...
}
```

All 6 were registered. EMD was searching for `id`, `name`, or another key. Its premise was wrong.

**Discipline (probe BEFORE responding to "X is missing"):**

```bash
# Read the actual schema, not the auditor's assumed schema
python3 -c "import json; d = json.load(open('canon/federation.json')); print(list(d.keys()))"
python3 -c "import json; d = json.load(open('canon/federation.json')); print(json.dumps(d['assets'][0], indent=2))"

# Search the actual key, not the auditor's assumed key
python3 -c "import json; d = json.load(open('canon/federation.json')); print([a.get('asset') for a in d.get('assets', [])])"
```

Then map each auditor claim to a real probe:

| Auditor claim | Live check | Verdict |
|---|---|---|
| "X is missing from registry" | `python3 -c "...['X' in str(data)]"` | PASS / FAIL |
| "Layer drift on Y" | `python3 -c "...Y.get('layer')"` | PASS / FAIL |
| "Z has no posture" | `python3 -c "...Z.get('posture')"` | PASS / FAIL |

**One real delta does emerge.** In the same session, HERMES posture in
`canon/sites.yaml` was genuinely `REFLECT_ONLY, deployable: false, port: 8644`
while HERMES was live at port 18089 with a Telegram gateway. That is a real
posture drift. Patch:

```yaml
# Before
posture: REFLECT_ONLY
deployable: false
port: 8644

# After
posture: LIVE
deployable: true
port: 18089
```

Same audit pattern repeated for FRAME ("undeclared runtime organ"): the
service was already in `federation.json` assets[] under one entry; the auditor
just expected `organs[]`. Re-classify, deduplicate, ship.

## 2. GitHub protected-branch workflow for sovereign code repos

Both `ariffazil/arif-fazil.com` and `ariffazil/web-canon` have `main` as a protected branch
that **rejects direct push with GH006: Protected branch update failed**.

```
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: - Changes must be made through a pull request.
To github.com:ariffazil/arif-fazil.com.git
 ! [remote rejected] main -> main (protected branch hook declined)
error: failed to push some refs to 'github.com:ariffazil/arif-fazil.com.git'
```

**Workflow (proven 2026-08-07, 2 repos, 6 commits shipped):**

```bash
# 1. From local main with uncommitted changes, create a dated feature branch
cd /root/<repo>
BRANCH="<type>/<short-desc>-$(date +%Y%m%d)"
git checkout -b "$BRANCH"

# 2. Push the branch
git push -u origin "$BRANCH"
# Returns: * [new branch]      <branch>  -> <branch>
# Plus: remote: https://github.com/ariffazil/<repo>/pull/new/<branch>

# 3. STOP. Do NOT merge automatically.
# Sovereign code repos require PR review. The PR URL is the deliverable.
# Arif (or his delegated reviewer) merges from GitHub UI.
```

**Why this matters:**

- `git push origin main` will always fail with GH006 on these repos. Don't try to
  retry with `--force` (still rejected; `--force-with-lease` also rejected;
  protection includes required-review rules).
- Branch + PR is F1-safe: reversible, auditable, reviewable.
- If a session asks "commit and push", the right action is "commit, push to a feature
  branch, report the PR URL". F1-equivalent: local commit = audit-trail;
  PR-pending = reversible; merge = the irreversible act which is for Arif.

**Efficiency caveat.** The Hermes-AI git interaction pattern may try `git push origin main`
first as a default — catch the GH006 error and branch instead, don't try
`git push --force`.

## 3. Quarantine recovery (source-of-truth restoration)

When `/root/forge_work/_quarantine/` contains a `_quarantine_<name>_<date>/`
sibling of a missing source dir, **recovery is reversible + content-parity verified**:

```bash
QUAR="/root/forge_work/_quarantine/<dir>-<date>"
[ -d "$QUAR" ] && [ -d "$QUAR/.git" ] && echo "quarantine source-of-truth exists"

# Content parity check
diff <(ls /root/_quarantine_FRAME_20260807/src/frame_organ/) \
     <(ls /opt/frame/app/frame_organ/)
# (empty = IDENTICAL — safe to restore)

# Restore
mv /root/_quarantine_FRAME_20260807/ /root/FRAME/

# Verify live organ still healthy (no path dependency broken)
curl -sf "http://127.0.0.1:<port>/health" -o /dev/null -w "%{http_code}\n"
```

**Verified case (2026-08-07):**

- `/root/FRAME/` was nuked (likely by a sibling agent) but
  `/root/_quarantine_FRAME_20260807/` held the full source — including
  `.git/`, `Makefile`, `pyproject.toml`, `src/`, `tests/`.
- Content parity with `/opt/frame/app/` runtime: IDENTICAL.
- After `mv` + `git push -u origin master`, FRAME was live again at
  port 18085, 10 baseline organs, 7 chambers active.

**Pattern.** Quarantine is not just for irreversible deletes — it is a
recoverable-state substrate. The 7-day grace period (per ZEN doctrine) is
the window to recover. After that, quarantine is purged.

## 4. Audit completion doctrine — single-cycle, single-receipt

The cleanup cycle (26 repos → 12 controlled) shipped in **one cycle, one branch**:

- 3 stale repos purged (or already purged by sibling agent — verify before re-purging)
- 2 orphan dirs locked (syedos git init+push, FRAME recovered from quarantine)
- 2 dirty-stub repairs caught (AAA SKILL.md replaced working 154-line skill
  with 1-line stub; web-canon HERMES posture REFLECT_ONLY→LIVE)
- 1 single-branch pair of pushes (`fix/hermes-posture-20260807` shipped 2 commits:
  HERMES posture + FRAME classification + syedos APEX-collision note)

**Why a single branch.** Cross-branch dependencies compound review burden. If
HERMES and FRAME + syedos were on separate branches, the PR review becomes a
mini-project. Folding them into one branch + one PR keeps the sovereign
decision surface coherent.

**Efficiency:** ~25 minutes from probe → commit → push for the 12-repo audit.
Two protected-branch workflows (arif-fazil.com + web-canon). Single receipt.

## 5. Honest correction pattern — "the audit premise was wrong"

When a frontier-model audit claims "X is missing from registry Y" and live
ground truth shows X IS in registry Y (under a different schema key), the
honest correction is:

> "EMD claimed '6 deltas absent from canon registries'. Live ground truth shows all 6 already registered in `federation.json` under `assets[]` — EMD was looking for the wrong schema shape. Only HERMES posture drift was a real delta; patched."

Not:

> "EMD was right, here's the corrected v2." (false agreement)
> "EMD was wrong, ignore everything." (false dismissal)

The right pattern: take the OBSERVATIONS seriously, verify the HYPOTHESES
against source, keep what survives, patch what's real, disclose what you
folded in.

## 6. Tool-state recovery probes (quick reference for next time)

```bash
# All 9 federation organs healthy (live health)
for p in 8088 7071 7072 7073 3001 8081 18082 18083 18085; do
  curl -sf "http://127.0.0.1:$p/health" -o /dev/null -w "$p: %{http_code}\n" --max-time 2
done

# External surfaces
for url in https://arif-fazil.com https://syedos.arif-fazil.com; do
  curl -sf -o /dev/null -w "$url : %{http_code}\n" --max-time 4 "$url"
done

# Live webroot surface integrity
ls /var/www/html/arif/ | wc -l
# 47 = expected (roots + 19 surface dirs + dotfiles + symlinks)

# Dirty repo count (post-cleanup target = 0)
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,arifFlow,HERMES,FRAME,arif-fazil.com,web-canon}; do
  dirty=$(git -C "$d" status -s 2>/dev/null | wc -l)
  echo "$d: $dirty"
done

# Verify-pages gate (content discoverability)
bash /root/arif-fazil.com/scripts/verify-pages.sh 2>&1 | tail -3
# Expected: VERDICT: PASS — safe to deploy.
```