---
name: skill-cluster-merge
version: 1.0.0
description: Use when merging a fragmented skill cluster to one owner.
owner: AAA
risk_tier: low
floor_scope: [F2, F11]
autonomy_tier: T1
ecology_state: WARM
capability_tier: fed-agent-subagent
---

# Skill Cluster Merge

Collapse a fragmented skill namespace (e.g. 26 MCP skills) into ONE canonical owner whose body is
the real operational flow, with every absorbed name kept alive as an alias.

## The shape

```
<owner>/SKILL.md                              <- the FLOW: when to use which reference, in order
<owner>/references/absorbed-<name>.md         <- member body verbatim + provenance header
/root/AAA/skills/.frozen/<date>-<cluster>/    <- untouched originals, never deleted
<name> -> <owner>                             <- symlink alias, in BOTH trees, in git
```

## Pitfalls that cost real work (wave 1, 2026-09-20)

### 1. `git add -A skills/` dereferences alias symlinks
On a symlink-aliased tree, `-A` stages the symlink as a real file copy and the alias stops being
an alias. Stage explicit paths only, then verify:
```bash
git diff --cached --summary | grep -c 'mode change 120000 => 100644'   # must be 0
```

### 2. Parallel children must not share a workspace path
Two children both defaulting to the same dir overwrote one receipt (unrecoverable outside git).
Mandate a unique filename and subdirectory per cluster.

### 3. Check for a second orchestrator BEFORE dispatching
Same mandate can reach two harnesses. Observed: a parallel orchestrator wrote its protocol file
14 seconds before the batch went out, then silently reverted five of a child's aliases mid-run.
A child that detects a sibling must complete the sibling's structure, NOT build a competitor.
Preflight: `find /root -maxdepth 3 -name 'PROTOCOL.md' -newermt '-1 hour'`, and check the target
tree mtime — a tree touched in the last 10 minutes has a live writer.

### 4. Dedupe by realpath, never by `find -L` alone
`find -L` traverses symlinks, so one skill reachable by two paths reports twice. This inflated the
counts to 587 broken links and 367 duplicate names; true figures were 1 and 26.
```bash
find -L <trees> -name SKILL.md -not -path '*/.archive*' -not -path '*/.frozen*' \
  | xargs -r realpath | sort -u
```
Then group by parent-dir basename to count true duplicates.

### 5. Merge is not delete
Keep every absorbed body twice, sha256-checked: as `references/absorbed-<name>.md` and as the
untouched original in `.frozen/`. Divergent copies carry information — fold the delta, never
flatten it.

### 6. Two writers need flock
```bash
flock /root/.git-skill-merge.lock git -C /root/AAA commit -m "..."
```
Even with flock, a sibling's `git add -A` can sweep your files into their commit. Verify content
landed by blob hash, not by commit message: `git log --format=%H -1 -- <path>`.

### 7. Leave genuinely-different capabilities alone
`mcp-ops` (operating MCP servers) is not `mcp-sota-shopping-list` (procurement reference).
Flattening related-but-distinct skills re-creates the fragmentation. Record why you kept a name.

### 8. Verify aliases from the LOADER tree
Runtime walks the harness tree (`~/.hermes/skills`), not the author-owned canonical tree. An alias
present only in canon is invisible at runtime. Check resolution from the loader side.

## Reachability is the whole game (the wave-2 defect)

**A skill can exist, be correct, be advertised in the session prompt, and still be unreachable.**
The Hermes runtime loader searches exactly ONE dir — `/root/.hermes/skills`:

```python
sys.path.insert(0, "/usr/local/lib/hermes-agent")
from tools.skills_tool import _skill_search_dirs, skill_view
print(_skill_search_dirs())          # project_dirs, all_dirs, active
```

Measured 2026-09-20: 566 skill bodies on disk, 396 visible, **182 resolving to NOT_FOUND**.
Canon (`/root/AAA/skills`) is NOT a loader dir — an alias created there is invisible.

### Why it happened
The mesh sync (`AAA/skills/AGI-skill-unification/skill-mesh-sync.sh`) binds Grok / Claude /
Codex trees and **line 9 explicitly excludes Hermes**: *"Does NOT touch Hermes/Kimi trees."*
So Hermes was the one harness never synced. Check that line before trusting any mesh report.

### How to verify — never trust a name LIST
`_find_all_skills()` dedupes by frontmatter `name`, so a symlink alias never appears in it even
when it resolves fine. Test with the resolver, not membership in a list:

```python
skill_view(name).get("success")      # the only valid test
```

Using the list produced a false "68 dead names" reading; the resolver produced the true 182.

### The fix that works
A top-level symlink in `/root/.hermes/skills/<name>` → the canon dir. Resolution falls back to
directory name, so the alias serves the owner's body. 181 created, 181/181 resolved, 0 dead.

### Name safety
Skip names that are not `^[A-Za-z0-9._-]+$` — spaces, em-dashes and parentheses in a skill's
frontmatter `name` cannot become a directory. Rename those instead; do not skip silently.

## Verification battery (all must pass before claiming done)

```bash
# 1. true duplicate names remaining
find -L <trees> -name SKILL.md -not -path '*/.archive*' -not -path '*/.frozen*' \
  | xargs -r realpath | sort -u | sed 's|.*/\([^/]*\)/SKILL.md|\1|' \
  | tr 'A-Z' 'a-z' | sort | uniq -d
# 2. broken symlinks
find <trees> -xtype l
# 3. loader resolution for every absorbed name (must be 0 unresolved)
# 4. no symlink->file typechanges staged in git
```

Report transitions, not Booleans: name the cluster, the before/after counts, the SHAs, and every
name left alone with its reason.
