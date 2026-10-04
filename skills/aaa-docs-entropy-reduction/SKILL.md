---
name: aaa-docs-entropy-reduction
description: >
  Reduce markdown document-tree entropy by classifying into tiers, detecting duplicates, extracting eureka insights, 
  and consolidating pointers. Uses STATE.md's four-tier model as the canonical framework. Load when organizing 
  or auditing any AAA/docs-like document tree, when asked to "clean up docs", reduce markdown entropy, classify 
  documents by tier, find duplicate MD files, extract key insights from old docs, or consolidate scattered doctrine.
tags: [docs, entropy, classification, pointer-convention, state-md]
---

# AAA Docs Entropy Reduction

Reduce markdown document-tree entropy while preserving institutional knowledge. Uses the **STATE.md four-tier model** as the canonical classification framework.

## When to apply

- User asks to "clean up docs" or "reduce entropy" in `/root/AAA/docs` or similar document trees
- Audit reveals many overlapping/stale markdown files
- Before merging multiple doctrine documents into one SOT
- After GENESIS-level insights are forged — old spec files should become pointers
- Whenever someone pastes a long list of doc files and says "classify these"
- **Repo audit requested** — "audit entropy", "validate all JSON", "check for doc drift", "create README" on any git-tracked repo (not just `/root/AAA/docs`)
- **JSON corruption suspected** — registries, manifests, or traces behaving unexpectedly

## The Four-Tier Classification

| Tier | Role | Example Paths | Rule |
|------|------|---------------|------|
| **A — Constitution** | Institution-defining law | `STATE.md` (~200–400L) | Edit ONLY here for law changes. One truth. Never merge other tiers INTO this file. |
| **B — Canon** | Elaboration/understanding | `philosophy/`, `doctrine/`, `canon/` | Header: `<!-- FEDERATED | tier:B-canon -->` + `Canonical SOT: STATE.md`. Adds depth, never contradicts A. |
| **C — Operational** | Procedures/contracts | `operations/`, `contracts/`, `transport/`, `geox/` | Header: `<!-- OPERATIONAL | tier:C-ops -->` + `Constitutional Context: STATE.md`. If the institution survives losing it, it's C. |
| **D — Receipts** | Proof/evidence | `sessions/`, `audit-*`, `receipts/` | PRESERVE. Never merge. Evidence > compression. Proof must survive even if doctrine dies. |
| **Legacy** | History/archives | `architecture/`, `archive/` | Archive when dead. Fold only when actively useful, not just because it exists. |

### The Four Survival Tests

Ask each file **one question**:

1. **If this file is deleted tomorrow, does the INSTITUTION die?** → Tier A (`STATE.md`)
2. **Is there KNOWLEDGE lost?** (not just procedure) → Tier B (Canon)
3. **Is there only PROCEDURE lost?** → Tier C (Operational)
4. **Is there EVIDENCE preserved?** → Tier D (Receipts) — preserve

**Forbidden:** mega-STATE (merging everything into one file = entropy singularity).
**Formula:** `STATE.md = Constitution, not Library.`

## Workflow: Classify → Extract → Remove → Tag

### Step 1: Full inventory walk

```bash
cd /root/AAA/docs
find . -name '*.md' -type f | wc -l
```

Load every file's first 300 chars and check for:
- Pointer headers (`# POINTER`, `Canonical SOT:`)
- Tier stamps (`FEDERATED`, `OPERATIONAL`)
- Date markers (`2026-05`, `2026-06`, `2026-07`)
- File size (< 50 bytes = trivial stub)

### Step 2: Detect exact duplicates

```python
import os, hashlib
from collections import defaultdict

files = {}
for root, dirs, fnames in os.walk('/root/AAA/docs'):
    for fname in fnames:
        if fname.endswith('.md'):
            content = open(os.path.join(root, fname)).read()
            norm = '\n'.join(l.strip() for l in content.split('\n') if l.strip())
            h = hashlib.sha256(norm.encode()).hexdigest()
            files.setdefault(h, []).append(os.path.relpath(os.path.join(root, fname), '/root/AAA'))

# Keep the deepest path (e.g., sessions/architecture/ version over docs/ version)
for h, paths in files.items():
    if len(paths) >= 2:
        for p in paths[:-1]:
            print(f"DELETE DUPLICATE: {p} ← kept: {paths[-1]}")
```

### Step 3: Identify stale files (>12 months old)

Date markers older than current epoch (e.g., before 2026-08):

```bash
grep -rl '2026-0[0-7]\|2026-\(5\|6\|7\)' docs/*.md docs/*/*.md | wc -l
```

Files with old dates but containing **eureka-worthy content** get extracted BEFORE deletion.

### Step 4: Extract eureka insights (CRITICAL STEP)

Before removing stale files, scan their **first 3000 characters** for:

| Keyword Pattern | What It Indicates | Action |
|-----------------|-------------------|--------|
| `theorem`, `law`, `principle`, `axiom` | Formal doctrine worth canonizing | Extract to appropriate canon/philosophy tier |
| `invariant` | Constitutional invariant worth preserving | Check if covered in STATE.md; if missing, add |
| `eureka` | Novel insight worth distilling | Distill into 1-sentence entry in canon tier |
| `formula`, `equation` | Quantitative relationship worth preserving | Add to appropriate section of STATE.md |
| `survival`, `test.*survive` | Survival criterion worth codifying | Add to STATE.md §12 (Survival tests) |

**Priority order for extraction:**
1. Files with ≥2 eureka keyword matches AND size > 10KB
2. Any file tagged as "canonical" or "SOT" in its header
3. Files referenced by other surviving docs (cross-reference check)

### Step 5: Convert surviving files to proper tier stamps

After extraction and cleanup, stamp remaining relevant files:

For Tier B (Canon):
```markdown
<!-- FEDERATED | tier:B-canon -->
> **Canonical SOT:** [`STATE.md`](./STATE.md) — unified constitutional working file.
>
> This elaborates — does not fork law. Edit STATE.md for doctrine changes.
> Probes: `scripts/state-probe.sh` · `scripts/protocol-enforce.sh`
```

For Tier C (Operational):
```markdown
<!-- OPERATIONAL | tier:C-ops -->
> **Constitutional Context:** [`STATE.md`](./STATE.md)
>
> Procedure only — not institution.
```

### Step 6: Cleanup

```bash
# Remove confirmed duplicates
git rm docs/<duplicate-file>.md

# Move truly historical files to archive
mkdir -p docs/archive/2026-07/
mv docs/<stale-files>* docs/archive/2026-07/

# Stage and commit
cd /root/AAA && git add -A && git commit -m "docs(zen): reduce entropy — <action>"
```

## Common Patterns

### Already-converted-to-pointers

These files already point to STATE.md and don't need reclassification:
```
CONSTITUTIONAL_SEPARATION_AXIOM.md
CONSTITUTIONAL_LAYER_SEPARATION.md
AAA_ABOVE_PROTOCOL.md
ACT_AUTHORITY_LAYER.md
PROTOCOL_ENFORCEMENT_MATRIX.md
AAA_STATE_PROTOCOL_AUDIT.md
IDENTITY_NAMING_REGISTRY.md
AAA_NEXT_90D.md
STATE_OPS.md
```

They're 9 files × ~280 bytes = minimal storage cost. They serve as human-navigable TOC entries. **Keep them.**

### Exact duplicate patterns

The most common source of duplication:
- Top-level file at `docs/X.md` AND subdirectory copy at `docs/subdir/X.md`
- Renamed copy: `docs/MCP_RESOURCES.md` vs `docs/MCP-RESOURCES-MAP.md` (same content, different name)
- Session architecture copies: `docs/SESSION_*.md` duplicated in `docs/sessions/architecture/`

**Rule:** Keep the most deeply nested version (e.g., `docs/sessions/architecture/`) and delete the top-level copy.

### Cross-reference audit

For files marked STALE but large (>15KB), run a cross-reference check against STATE.md keywords:

```python
state_md = open('/root/AAA/docs/STATE.md').read().lower()
file_lower = open(path).read().lower()[:3000]
state_kw = set(w for w in re.findall(r'\b\w+\b', state_md))
overlap = len(state_kw & set(w for w in re.findall(r'\b\w+\b', file_lower)))
```

High overlap = likely redundant. Low overlap = possibly contains UNIQUE knowledge worth keeping.

## Structured-Data Validation (JSON/YAML)

Entropy isn't just duplicate markdown — broken JSON/YAML silently corrupts
registries, manifests, and traces. **Always validate all structured data
files as part of the inventory walk.**

```python
import json, os, glob

repo = "/root/<REPO>"
for jf in glob.glob(os.path.join(repo, "**", "*.json"), recursive=True):
    if ".git" in jf:
        continue
    try:
        json.load(open(jf))
    except Exception as e:
        print(f"INVALID  {os.path.relpath(jf, repo)}: {e}")
```

### Common JSON pitfalls (verified 2026-08-14)

- **JS-style number literals.** `+0.01` is valid in JavaScript but **not
  valid JSON** — the spec forbids a leading `+` on positive numbers. This
  is the #1 cause of broken JSON in repos touched by AI agents that emit
  JS-flavored literals. Fix: strip the `+` → `0.01`.
- **Trailing commas.** `{"a": 1,}` is valid in JS/Python dicts but not JSON.
- **Single quotes.** JSON requires double-quoted strings.
- **Unescaped newlines in strings.** Use `\n`, not literal line breaks.

After fixing, re-run the validation loop to confirm **zero** invalid files
before committing.

## Doc-Drift Checking (Claimed vs Actual)

Many doctrine/SOT documents contain hard-coded file counts, layer tables,
or path references. Over time these drift from reality. **Always verify
claims against the filesystem.**

```python
# Example: ZEN_HELIX.md claims H1=4, H2=52, H3=22, H4=6, H5=25, H6=1
# Check actual counts:
import os
for layer in ["H1-capture", "H2-experience", ...]:
    path = os.path.join(repo, layer)
    actual = sum(len(files) for _, _, files in os.walk(path))
    print(f"{layer}: {actual}")
```

If drift is found, **update the doctrine document to match reality** (not
the other way around) — unless the doctrine is aspirational by design, in
which case flag the gap rather than silently correcting.

## README Creation

If the repo lacks a README.md, create one as the final step of any audit.
Include: architecture overview, directory layout with file counts, key
file inventory, and an audit log table. The README is the entry point for
future agents and humans — it should let a newcomer orient in under 60
seconds.

## SOT-MANIFEST Drift (HTML comment block)

Most federation READMEs start with a `<!-- SOT-MANIFEST ... -->`
HTML comment containing `live_commit`, `last_verified`, port claims,
and organ metadata. This is the **single most stale part** of any
federation README — nobody sees it when browsing GitHub, so it silently
rots.

```bash
# Extract claimed commit and compare to actual HEAD
head -20 README.md | grep -oP 'live_commit: \K[0-9a-f]+'
git rev-parse --short HEAD
```

**Common drift fields:**

| Field | How to verify | Fix |
|-------|---------------|-----|
| `live_commit` | `git rev-parse --short HEAD` | Update to current HEAD |
| `last_verified` | `date -u +%Y-%m-%d` | Update if >7 days stale |
| `forge_instruments:` count | Count from federation config | Update prose + manifest |
| `domain_organs:` count | Count from organ registry | Update prose + manifest |

**Stale prose counts:** README prose often hardcodes counts like
"31+ skills" or "11 forge instruments". Verify against the filesystem
and update BOTH prose tables AND diagram labels (mermaid, ASCII art):

```bash
find skills/ -name 'SKILL.md' -not -path '*/_retired/*' | wc -l
```

If prose says "31+" and actual is 428, update every occurrence.

See `references/repo-housekeeping-aaa-hermes-2026-08-13.md` for a
worked example.

## .bak File Entropy & .gitignore Coverage

Backup files accumulate silently when `.gitignore` has timestamped
patterns (`*.bak-*`) but not the plain `*.bak` pattern. Always check:

```bash
# Find untracked .bak files in active repo (not archive/)
find . -name '*.bak' -not -path '*/.git/*' -not -path '*/archive/*'

# Verify .gitignore covers plain *.bak
grep -q '^\*\.bak$' .gitignore && echo "COVERED" || echo "MISSING"
```

Fix: add `*.bak` as a catch-all line in `.gitignore`.

## Runtime-State Files Tracked as Source (Entropy Class)

Some files are mutated by the application at **runtime** (timestamps, lane
mappings, gateway state) yet are accidentally tracked in git. Every session
that touches the repo then shows them as dirty, producing a stream of
low-value commits that pollute the log.

**Detection — spot the pattern with commit history:**

```bash
git log --oneline --follow -10 -- <suspect-file>
```

If the file appears across many commits from different sessions/authors with
trivially different content (a timestamp, a mapping value), it is **runtime
state, not source**.

**Common runtime-state files that should NOT be git-tracked:**

| File | Why it mutates | Repo seen in |
|------|---------------|-------------|
| `lanes/.runtime.json` | Hermes updates `_last_update` timestamp + chat→lane mappings at every message | /root/HERMES |
| `gateway_state.json` | Gateway process writes PID, restart count, last-seen | /root/HERMES |
| `channel_directory.json` | Channel discovery cache | /root/HERMES |
| `.update_check` | Last update-check timestamp | any Hermes install |
| `processes.json` | Background process registry | any Hermes install |

**Fix (deterministic, safe):**

```bash
git rm --cached <file>          # untrack but keep on disk
echo "<file>" >> .gitignore     # prevent re-tracking
git add .gitignore
git commit -m "fix(entropy): untrack <file> — runtime state, not source"
```

**Verification after fix:**

```bash
git status   # working tree should be clean
# Confirm file still exists on disk:
test -f <file> && echo "OK — file preserved locally"
```

**Pitfall:** Runtime `.json` files that serve as *configuration templates*
(e.g., `config.yaml`, `lanes.yaml`) ARE source and must stay tracked. The
test is: *does the application mutate this file during normal operation?*
If yes → `.gitignore`. If the human edits it deliberately → tracked.

**Verified 2026-08-14** in /root/HERMES: `lanes/.runtime.json` was tracked
across 16 commits, each differing only in `_last_update` timestamp or
chat→lane fallback mapping. Untracked + gitignored in commit 1d64c5f.

## Self-Referential Symlink Detection

A self-referential symlink (points to its own parent directory) is
worse than a broken symlink — it doesn't show as broken with
`find -xtype l`, but silently creates infinite directory traversal.

```bash
find . -type l -not -path '*/.git/*' | while read l; do
  target=$(readlink "$l")
  dir=$(dirname "$l")
  if [ "$(cd "$dir" && cd "$target" 2>/dev/null && pwd)" = "$(cd "$dir" && pwd)" ]; then
    echo "SELF-REF: $l -> $target"
  fi
done
```

Known pattern: `mcp_servers/mcp_servers` → `mcp_servers` (own parent).

## Pre-Commit Secret Scan

Before `git add -A && git commit`, scan staged files for potential secrets:

```bash
git diff --cached --name-only | grep -iE '\.key$|\.pem$|secret|credential|password|token'
```

False positives are common (skill scripts about secrets, not containing
them). Manually verify each hit before committing.

## Verification Protocol

After entropy reduction, run these checks:

0. **All JSON files valid (MANDATORY):**
   ```python
   import json, os, glob
   repo = "/root/<REPO>"
   bad = []
   for jf in glob.glob(os.path.join(repo, "**", "*.json"), recursive=True):
       if ".git" not in jf:
           try: json.load(open(jf))
           except Exception as e: bad.append((jf, str(e)))
   assert not bad, f"Invalid JSON: {bad}"
   ```

1. **STATE_READY probe passes:**
   ```bash
   /root/AAA/scripts/state-probe.sh && echo "STATE_READY" || echo "DEGRADED"
   ```

2. **No broken cross-references:**
   ```bash
   grep -r "STATE\.md" docs/*.md docs/*/*.md | wc -l
   grep -r "POINTER\|Canonical SOT" docs/*.md docs/*/*.md | wc -l
   ```

3. **Git diff review:**
   ```bash
   cd /root/AAA && git diff --stat HEAD
   # Expect: many deletions, few modifications (stamp additions), zero additions
   ```

## Edge Cases

### "NEEDS?" files (no clear tier match)

About 30% of files fall here — they have no clear date marker, no pointer header, and content that doesn't obviously match A/B/C/D. For these:

1. Read first paragraph + heading
2. Ask: "Is this about HOW we do things (C), WHAT we believe (B), or WHO/WHY (A)?"
3. If unsure, tag as `tier:B-canon` conservatively — canon elaboration won't break anything; operational changes could.

### Large stale files (>20KB)

Even with old dates, some files contain dense conceptual material that hasn't been fully distilled:
- `CONSTITUTIONAL_PRIMITIVES.md` (39KB) — 8-primitive agent anatomy
- `EUREKA_SIX_PLANE_EXECUTION_LOOP.md` (30KB) — Six planes, Anti-Authorization Theorem
- `QUANTUM_REALITY.md` (23KB) — QP-1 through QP-7 principles

**Extract before delete:** Pull out theorem names, principle numbers, and invariant definitions into the appropriate section of STATE.md.

## Pitfalls

- **Don't merge everything into STATE.md.** State is a constitution, not a library. 200–400 lines is the sweet spot. Beyond that, you've committed the entropy singularity error.
- **Don't delete Tier D (receipts).** These are proof, not doctrine. Evidence preservation takes priority over compression.
- **Don't confuse TIMESTAMP with RELEVANCE.** A file dated 2026-07 might still contain valuable eureka. Always check the content, not just the date.
- **Cross-reference maintenance:** After deleting/moving files, update any references in surviving docs. Broken links are a different kind of entropy.
- **Backup before bulk deletes:** Use git staging so you can recover with `git reset` if needed. Never trust `rm` without a safety net.
- **Don't create a new file when a pointer will do.** If STATE.md already covers the topic, add a pointer file — don't fork new content.
- **Don't skip JSON validation on repos that "look clean."** The `/root/memory` repo had exactly 1 broken JSON in 18 files — a `+0.01` literal in an RSI trace. Invisible until you run the validator.
