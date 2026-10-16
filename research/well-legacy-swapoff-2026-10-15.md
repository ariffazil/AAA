# WELL legacy callers + swapoff precondition (Q5)

## Part 1 — Legacy callers inventory

The expected branch is `well/legacy-callers` on the `WELL` repo (`https://github.com/ariffazil/WELL.git`).

**Verified — branch does not exist on this box:**
- `git remote -v` → `origin = https://github.com/ariffazil/WELL.git`
- `git branch -a` → 7 local branches (`main`, `fix/well-machine-swapoff-precondition`, plus 5 chore/*), 10+ remote branches. **None of them are `well/legacy-callers`.**
- `git log --all --grep=legacy` returned only deprecation-shim / SSE legacy transport / legacy TODO archive commits — none of them a "callers list" inventory.
- `find /root/WELL -type f -name "*legacy*"` returned only `.venv/` test fixtures and unrelated npm-test mirror files.
- `find /root/AAA -maxdepth 4 -name "*legacy*"` and `find /root/.qwen /root/.claude -name "*legacy*"` returned no inventory file.

**Conclusion:** the branch Qwen was supposed to own is not present on KVM8. Per queue, I do not re-do it.

**MENUNGGU ARIF — branch + owners:**

- The legacy callers inventory is in Qwen's lane. Either:
  - Ask Qwen to push `well/legacy-callers` to `origin`, **or**
  - Provide a paste of the inventory for a single-CLI verification on KVM8.

Until one of those lands, this half of Q5 is unsatisfied. No new investigation started.

## Part 2 — Swapoff precondition correction

**Branch:** `fix/well-machine-swapoff-precondition` (local, no push).

**Commit:** `a2bca5e` — *"fix(well-machine-recommend): gate swapoff on swap_used < avail*0.8"* — already in place from the prior session.

**Old logic (server.py, line ~12349)**:
```python
if swap_pct > 30 and mem_psi < 5:
    severity = "AMBER"
    issues.append("Swap ... safe to recover")
    recommendations.append({"action": "swapoff -a && swapon -a  # PSI confirms safe -- no memory thrashing", ...})
```

**New logic (server.py, lines ~12349–12378)**:
```python
swap_used_bytes = swap_used_kb * 1024
avail_bytes    = avail_kb * 1024
swap_fits_in_ram = swap_used_bytes < (avail_bytes * 0.8)

if swap_pct > 30 and mem_psi < 5 and swap_fits_in_ram:
    ...
    recommendations.append({
        ...,
        "precondition": (
            f"mem_psi_avg10={mem_psi:.1f} < 5 AND "
            f"swap_used {swap_used_kb / 1024**2:.1f}GB < "
            f"available {avail_kb / 1024**2:.1f}GB * 0.8 "
            f"({swap_used_bytes / max(avail_bytes, 1):.2f} < 0.80)"
        ),
    })
```

**Why:** PSI < 5 alone measures current-state pressure, not whether reclaimed swap will fit. Adding `swap_used < avail * 0.8` blocks the recommendation when reclaiming would force a thundering page-fault into RAM that cannot hold the working set. The gate is in **both** the severity branch and the recommendation branch — suppressed, not just annotated.

**Tests:** `tests/test_swapoff_precondition.py` — 6/6 pass (safe / unsafe / boundary / PSI-high / low-swap-pct).

**No execution:** `swapoff -a` was **not run**. Real conditions on this host (live `/proc/meminfo` probe at 23:13Z): swap used ≈ 0 (filesystem has no swap), avail 70 GB, PSI unknown. Test was the only run.

**Verification commands (MUSTNOT auto-run):**
```bash
cd /root/WELL
git rev-parse --abbrev-ref HEAD                  # → fix/well-machine-swapoff-precondition
git log -1 --format='%h %s' a2bca5e               # → a2bca5e fix(well-machine-recommend): gate swapoff on swap_used < avail*0.8
pytest -q tests/test_swapoff_precondition.py     # 6/6 pass (no swapoff issued)
git push origin fix/well-machine-swapoff-precondition  # MENUNGGU ARIF
```

## Diff body, reviewable from commit message

```
PSI < 5 alone is not a safe precondition for swapoff -a. PSI is a
current-state pressure metric; it tells you there is no memory thrashing
RIGHT NOW, but says nothing about whether the swapped-out pages will fit
back into available RAM when released. If swap_used > 80% of available
RAM, swapoff -a page-faults every swapped byte back into a working set
that cannot hold them, and the kernel fires the OOM killer.

Add swap_used < mem_available * 0.8 as a second precondition (and as a
gate inside the recommendation.append branch, so the suggestion is
suppressed, not just annotated).

Tests: tests/test_swapoff_precondition.py covers safe / unsafe / boundary /
PSI-high / low-swap-pct scenarios. 6/6 pass.
```
