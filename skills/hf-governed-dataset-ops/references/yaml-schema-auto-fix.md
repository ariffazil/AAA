# HF README YAML Schema Auto-Fix Pattern

**Forged 2026-08-11.** When the HF dataset viewer's pre-receive hook rejects a README push
because the declared YAML schema doesn't match the on-disk data, this is the recovery recipe.

## Symptom (verbatim from HF pre-receive hook)

```
remote: Sorry, your push was rejected during YAML metadata verification:
remote: - Error: Invalid YAML in README.md: unidentified alias "*Dataset:**" (85:13)

remote:  82 |   dataset_size: 129---
remote:  83 | # EEE — Kernel Spine Recovery
remote:  84 |
remote:  85 | **Dataset:** `ariffazil/EEE`
remote: ------------------^
```

**OR (the more common viewer cast error after a successful push):**

```
Couldn't cast
  probe_id: string, timestamp: timestamp[s], organ_id: string, verdict: string,
  degraded: bool, actor_verified: bool, mutation_allowed: bool, ...
to
  {'id': Value('string'), 'timestamp': Value('string'), 'verdict': Value('string')}
because column names don't match
```

Both errors mean the same thing: the YAML in your README declares columns that don't
exist in the actual data files (or vice versa). The HF viewer can't render the dataset
until you reconcile them.

## Recipe

### Step 1 — Probe actual data

```bash
python3 <<'PYEOF'
import json, os
for root, _, files in os.walk('/tmp/hf_repos/<DS>'):
    if '.git' in root.split('/'): continue
    for f in files:
        if not f.endswith('.jsonl') or f.endswith('.bak'): continue
        path = os.path.join(root, f)
        if os.path.getsize(path) < 200: continue  # LFS pointer
        cols, rows = {}, 0
        with open(path) as fh:
            for line in fh:
                if line.strip():
                    try:
                        d = json.loads(line)
                        for k, v in d.items():
                            if k not in cols: cols[k] = v
                        rows += 1
                        if rows > 500: break
                    except: pass
        print(f'{f}: {rows} rows, {len(cols)} cols')
        for c in sorted(cols): print(f'  - {c}: {type(cols[c]).__name__}')
PYEOF
```

### Step 2 — Compare declared vs actual

```bash
# What the README claims
sed -n '/^---$/,/^---$/p' /tmp/hf_repos/<DS>/README.md | grep -E '^\s+- name:'

# What the data has (from step 1)
```

### Step 3 — Generate corrected YAML

For each `.jsonl` file:

```yaml
configs:
  - config_name: <unique-name>
    data_files:
      - split: train  # or 'validation' for val/test splits
        path: <relative/path/to/file.jsonl>
    features:
      - name: <col1>
        dtype: string        # bool, int64, float64, string, sequence, dict
      - name: <col2>
        dtype: bool
      # ...
    splits:
      - name: train
        num_examples: <actual-row-count>
```

### Step 4 — Patch the README frontmatter

```python
# Pseudocode — full script in /tmp/fix_hf_v3.py
import re

with open('README.md') as f:
    rd = f.read()

# 1. Find frontmatter end
fm_end = find_frontmatter_end(rd)  # see Pitfall 1
fm = rd[4:fm_end]
body = rd[fm_end:]

# 2. Strip ALL old configs: blocks (handle duplicates)
while True:
    m = re.search(r'^configs:.*?(?=^\w|\Z)', fm, re.MULTILINE | re.DOTALL)
    if not m: break
    fm = fm[:m.start()] + fm[m.end():]

# 3. Strip ALL old dataset_info: blocks (info now lives in configs)
while True:
    m = re.search(r'^dataset_info:.*?(?=^\w|\Z)', fm, re.MULTILINE | re.DOTALL)
    if not m: break
    fm = fm[:m.start()] + fm[m.end():]

# 4. Append new configs at end of frontmatter
new_configs = "configs:\n" + "\n".join(config_blocks)
new_fm = fm.rstrip() + "\n\n" + new_configs + "\n"
new_rd = "---\n" + new_fm + "---\n\n" + body.lstrip()

with open('README.md', 'w') as f:
    f.write(new_rd)
```

### Step 5 — Commit + push

```bash
git add README.md
git commit -m "fix(docs): correct YAML schema to match actual data columns"
git push
```

If the remote has stale commits (someone pushed earlier and your local diverged):
```bash
git rebase --abort 2>/dev/null
git fetch origin
git reset --hard origin/main
# re-apply the fix, then commit + push
```

If the repo was newly cloned and has no token in the remote URL:
```bash
set -a; source /root/.secrets/kunci-mas.env; set +a
git remote set-url origin "https://ariffazil:${HF_TOKEN}@huggingface.co/datasets/ariffazil/<DS>"
```

## Pitfalls (verified 2026-08-11)

### Pitfall 1 — No clean `---` closer
**Symptom:** `find_frontmatter_end` returns way too early; YAML parses but body text leaks into frontmatter.
**Cause:** I-ARIF-CANON's README opened YAML with `---` but the closing `---` was at the
very end of the file. My first regex `rd.find('\n---\n', 4)` matched the LAST `---`, capturing
the whole body as YAML.
**Fix:** Use a heuristic that detects where YAML syntax breaks. See
`find_frontmatter_end` in `/tmp/fix_hf_v3.py`:
- Walk lines after opening `---`
- Skip empty lines
- A line matching `key:`, `- item`, `# comment`, or indented continuation = still YAML
- A line that matches NONE of those = body text starts here, that's the boundary

### Pitfall 2 — Indented YAML keys
**Symptom:** `find_frontmatter_end` stops at the first indented line (`  features:`).
**Cause:** Regex `^[\w\-][\w\-]*:` doesn't match indented keys.
**Fix:** Allow leading whitespace: `^\s*[\w\-][\w\-]*:`.

### Pitfall 3 — Duplicate `dataset_info:` blocks
**Symptom:** After fix, the file contains a truncated `dataset_in` line.
**Cause:** BBB/CCC/I-ARIF-CANON had `dataset_info:` declared TWICE (once empty, once
populated). My first script only removed ONE occurrence.
**Fix:** Wrap removal in `while True:` loop and check `if not m: break`.

### Pitfall 4 — "val" substring matches "eval"
**Symptom:** `i-arif-redteam-eval.jsonl` gets named config "val" instead of "redteam".
**Cause:** `'val' in 'i-arif-redteam-eval.jsonl'` returns True (substring match).
**Fix:** Use word boundary: `re.search(r'\bval\b', basename)`.

### Pitfall 5 — Config name collisions
**Symptom:** HF rejects push because two configs have the same `config_name:`.
**Cause:** AAA has `data/gold/train.jsonl`, `data/gold/validation.jsonl`,
`data/gold/test.jsonl` — all naively named "gold" without split differentiation.
**Fix:** Map each filename to a unique name (`gold_train`, `gold_validation`,
`gold_test`, `gold_all`); track `used_names` set and suffix counter.

### Pitfall 6 — HF pre-receive hook returns confusing errors
**Symptom:** "pre-receive hook declined" with no details.
**Cause:** HF validates YAML server-side; errors point to line/column but git just
shows the rejection.
**Fix:** Re-run push with `GIT_TRACE=1`:
```bash
cd /tmp/hf_repos/<DS>
GIT_TRACE=1 git push 2>&1 | grep -A2 "remote:"
```
The error usually says `Invalid YAML in README.md: <error> at line X col Y`.

### Pitfall 7 — Schema declares `id` but data has `probe_id`
**Symptom:** Cast error mentions `id` and `probe_id` differently.
**Cause:** I-ARIF-CANON's old YAML said `name: id` for the VAL split, but the actual
data uses `probe_id` (and the JSONL also has `id` for some rows but `probe_id` for others).
**Fix:** Use the dominant column name from `get_actual_schema`. The script samples up to
500 rows — if a column appears in >50% of rows, that's the canonical name.

## Verification

After push, check the viewer resolved:
```bash
curl -sf "https://huggingface.co/datasets/ariffazil/<DS>" | grep -oE 'kind[^"]+' | head -3
```

The error page contains `"kind":"ConfigError"`. After fix, it shows either:
- `"kind":"dataset"` (success, data is now parseable)
- Standard "Retry later" cache message (HF needs ~30s to re-process after schema change)

If the error returns after the cache window (~5 min), your YAML is still wrong.
Re-run the script and check the pre-receive hook for the next failure.

## Reusable script

The full working script (with all 7 pitfalls handled) is at `/tmp/fix_hf_v3.py`.
Run on any cloned HF repo:

```bash
python3 /tmp/fix_hf_v3.py        # fix all repos in /tmp/hf_repos/
python3 /tmp/fix_hf_v3.py --repos AAA BBB   # specific repos only
python3 /tmp/fix_hf_v3.py --dry-run        # show what would change
```

The script auto-generates dedup'd config names, strips old broken YAML, inserts
correct YAML matching on-disk evidence, and reports per-repo success/failure.
