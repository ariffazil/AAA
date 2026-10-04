# Deployment Drift Markers — What Lies About Code Alignment

The arifOS deployment system uses a chain of commit markers to assert source-vs-deployed alignment. As of the 2026-08-06 investigation, this chain has gaps that allow drift to go unreported.

## The marker chain

1. **Deployment marker**: `/opt/arifos/app/.git_commit` — written by `make deploy-local`, represents what was actually deployed
2. **Source marker**: `/root/arifOS/.git_commit` — written by `make deploy-local` from source tree
3. **Build info**: `BUILD_INFO["build"]["commit"]` in `runtime/build.py` — derived from env or `.git_commit`
4. **Live HEAD**: read from `.git/HEAD` and `.git/refs/heads/<branch>` as fallback

## The drift computation

`_compute_runtime_drift()` at `runtime/rest_routes/rest_routes.py:2379`:

```python
def _compute_runtime_drift() -> dict[str, Any]:
    build_commit = BUILD_INFO.get("build", {}).get("commit", "unknown")
    live_commit = "unknown"
    # 1. Try .git_commit markers (canonical)
    for commit_file in ["/opt/arifos/app/.git_commit", "/root/arifOS/.git_commit"]:
        if os.path.exists(commit_file):
            with open(commit_file) as f:
                candidate = f.read().strip()[:7]
            if candidate:
                live_commit = candidate
                break
    # 2. Fallback: git repo HEAD
    if live_commit == "unknown":
        for git_dir in [...]:
            # read .git/HEAD, .git/refs/heads/<branch>
            ...
    _both_known = build_commit != "unknown" and live_commit != "unknown"
    return {
        "runtime_drift": _both_known and (build_commit != live_commit),
        "runtime_matches_build": _both_known and (build_commit == live_commit),
        "build_commit": build_commit,
        "live_commit": live_commit,
    }
```

## How markers lie

**Scenario A**: Manual file copy without re-running `make deploy-local`.
- `/root/arifOS/.git_commit` says `4d2f51a7` (old deploy)
- Source HEAD is `42dec9e5f` (12 commits ahead)
- Deployed runtime has all 12 patches applied (byte-identical files)
- Marker says `4d2f51a7` → `_compute_runtime_drift()` returns `runtime_drift=False`
- **Truth**: code is drifted from marker, marker hasn't been updated
- The `runtime_matches_build` check passes because both sides of the comparison use the same stale marker

**Scenario B**: Container deploys with different build tooling.
- Container has `BUILD_INFO["build"]["commit"]` baked at image build time
- `make deploy-local` writes a new marker after copying files
- The two commit hashes may refer to the same tree but have different SHAs if rerun with different parent context
- Marker would correctly report drift, but the drift is cosmetic (tree is identical)

## What `_compute_runtime_drift` does NOT check

1. **File content diff** — only commit SHA comparison. If a file is modified after `make deploy-local` writes the marker, drift is invisible.
2. **Dirty working tree** — `git_dirty: None` (line 2445) is hardcoded as `None` "would require git status; skipped for performance."
3. **Missing files** — if a file is deleted post-deploy, drift is invisible (file count not compared).
4. **Modified untracked files** — `.git_commit` only covers the deployable tree.

## The 2026-08-06 reality

Investigation found:
- Source repo HEAD: `42dec9e5f` (12 commits ahead of `origin/main`)
- Deployed git repo HEAD: `f171bb14c` (unrelated to either)
- Both `.git_commit` markers: `4d2f51a7` (stale — written by an earlier `make deploy-local`)
- `runtime/tools.py`: byte-identical between `/root/arifOS/` and `/opt/arifos/app/` (manual copy)

`_compute_runtime_drift()` reported `runtime_drift=False` because both markers agreed. Truth: code has moved 12 commits forward from what the markers say.

## When the markers are truthful

The markers are reliable when:
- Deploys always go through `make deploy-local` (or equivalent)
- No manual file edits happen post-deploy
- The source HEAD matches the deploy trigger

They are unreliable when:
- Files are copied via scp, rsync, or manual cp
- Hot-patches are applied without re-running deploy tooling
- Multiple deploy mechanisms are used (container + bare-metal in parallel)

## Investigation pattern

When investigating "is the deployed runtime drifted from source":

```bash
# 1. Compare file content (byte-identical?)
diff -q /opt/arifos/app/arifosmcp/runtime/tools.py /root/arifOS/arifosmcp/runtime/tools.py

# 2. Check git markers
cat /opt/arifos/app/.git_commit /root/arifOS/.git_commit

# 3. Check actual git HEADs
cd /opt/arifos/app && git rev-parse HEAD
cd /root/arifOS && git rev-parse HEAD
cd /root/arifOS && git log --oneline origin/main..HEAD | wc -l

# 4. Compare BUILD_INFO to actual files
# (BUILD_INFO is baked into the container — diff vs source commit)
```

If all three (file content, markers, HEAD) agree → no drift.
If file content agrees but markers/HEAD disagree → marker is stale; treat as drifted.
If file content disagrees → genuine drift; `_compute_runtime_drift` may be lying.

## Fix sketch

To make drift detection truthful:

1. Add file-content hash comparison (sample critical files like `runtime/tools.py`, `runtime/build.py`)
2. Update markers on every file modification, not just deploy
3. Compare against actual deployed commit (read container's baked commit), not the marker
4. Add `git_dirty` to the response (run `git status` on the deployed tree)

None of these are currently implemented. Until they are, treat `deployment_drift_status: aligned` as "marker says aligned", not "code is aligned."

## Related reading

- `references/d-series-defects-20260806.md` — the audit session that revealed the stale marker pattern