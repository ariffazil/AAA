---
name: skill-estate-maintenance
description: "Use when the skills index is bloated or has dead entries."
version: 1.0.0
owner: HERMES
tags: [skills, catalog, prompt-budget, dedupe, prune, entropy]
floor_scope: [F2, F11]
triggers:
  - "skills index too big"
  - "prompt too big from skills"
  - "prune skills"
  - "dedupe skills"
  - "skill catalogue dead entries"
  - "lower entropy of the skills"
---

# Skill Estate Maintenance

Reducing the cost of the skills index — the block injected into every turn of every session — without
deleting capability. The index is a SELECTION surface: name + description + path, paid on every turn
forever. A reduction you cannot reverse is a deletion wearing hygiene as a disguise.

## Rule 0 — measure the rendered block, not the file tree

A directory listing is not a cost. The cost is the string the prompt builder emits:

```python
import sys; sys.path.insert(0, '/usr/local/lib/hermes-agent')
from pathlib import Path
from agent.prompt_builder import build_skills_system_prompt
block = build_skills_system_prompt(skills_dir_override=Path('<profile-skills-dir>'))
print(len(block), len(block) // 4, 'tokens/turn')
```

This rebuilds the real `## Skills` section from disk with no gateway restart, so it is both the meter and
the staleness cure. Supporting read — what the walker actually sees:

```python
from agent.skill_utils import iter_skill_index_files
paths = [str(p) for p in iter_skill_index_files(Path('<skills-dir>'), 'SKILL.md')]
```

- The walker uses `followlinks=True` and prunes `EXCLUDED_SKILL_DIRS` (`.archive`, `.git`, `node_modules`,
  `venv`, …) and `SKILL_SUPPORT_DIRS`. Anything inside those is **already invisible** — counting it inflates
  the estate and cleaning it buys zero tokens.
- The live request dump (`sessions/request_dump_*.json`) holds the string a session actually paid. Grep it
  for `<available_skills>` when a fresh build and a running session disagree.

## Order of operations — never reorder

```
census  ->  dedupe mounts  ->  hide by evidence  ->  verify  ->  [delete = a different act]
```

Everything before `delete` is reversible in one command. Treat unlink/delete as a separate decision with
its own authority, never as the last step of a cleanup script.

## 1 · Census — four numbers, none of them `ls | wc -l`

```bash
find -L <skills-dir> -name SKILL.md | wc -l                      # follow the mounts
{ find -L <dir-a> -name SKILL.md; find -L <dir-b> -name SKILL.md; } \
  | xargs -r realpath | sort -u | wc -l                          # unique skills
```

- **`find` without `-L` undercounts a symlink farm by an order of magnitude.** A profile directory that
  mounts a shared catalogue is mostly symlinks; the plain walk sees a few dozen files against a thousand
  real skills.
- **A `maxdepth` cap drops every nested domain directory** and reports a tidy, wrong number.
- **`ls | wc -l` counts mounts, not skills** — the same skill appears once per mount point.

## 2 · Dedupe mounts — the only zero-risk reduction

A safe removal candidate is a **root-level symlink whose `realpath` equals a deeper real directory**.
Everything else is a judgement call about content.

Before unlinking, three probes, all must be clean:

1. **Record the rollback first** — `os.readlink(link)` for every candidate, written to a durable receipt
   file. Never unlink before the target exists somewhere else on disk.
2. **Inbound symlinks** — walk the profile tree for `-type l` and test every target against the candidate
   list. Another profile pointing into the flat path breaks silently.
3. **Exact-path text references** in live surfaces (config, contracts, cron, instructions, scripts) —
   match the **full path string**, never just the skill name:

```bash
grep -rlF -f /tmp/candidate_paths.txt <live-trees>
```

- A hit inside an **immutable** file (`chattr +i` contract naming a `references/...` path) means that mount
  **stays**. Restore it and drop it from the removal list so the receipt stays honest — editing the
  contract to match the cleanup inverts the authority order.
- After unlinking, re-run the census and call the loader on one removed name to prove the deeper twin still
  resolves.

## 3 · Hide by evidence — reversible, files untouched

`skills.disabled` in the profile config removes names from the injected index while every file stays on
disk, so other harnesses reading the same tree are unaffected.

```bash
hermes config set skills.disabled '<JSON array of names>'
hermes config get skills.disabled            # read back
hermes config unset skills.disabled          # one-line revert
```

- **The CLI prints `'skills.disabled' is not a recognized config key — it was saved anyway`.** The warning
  is advisory; the skills block is read by the prompt builder regardless. Do not "fix" it by hand-editing
  the YAML — verify by rebuilding the block and confirming a disabled name is gone.
- **Hiding is not free**: a disabled name also refuses the loader (`Skill '<name>' is disabled`). Say that
  out loud when proposing the list — it converts a hidden skill into a refusal until re-enabled.
- **Evidence for each name, all four conjunctive**: no recorded load in a 30-day window; not named by any
  other skill body; not named in the non-skill corpus (SOUL, AGENTS, instructions, scripts, cron,
  registries); not present in cron. A name failing any one is kept — hiding a referenced skill is deleting
  capability with a filter.

## 4 · Usage sensor — one harness, and say so

Loads are recorded in the message store (`messages.tool_calls`, a JSON array on assistant rows). Query,
dump, then parse — never aggregate in SQL and never regex prose:

```bash
timeout 300 sqlite3 -cmd '.timeout 20000' "$DB" \
  "SELECT tool_calls FROM messages WHERE timestamp > strftime('%s','now')-2592000 \
   AND tool_calls LIKE '%<tool>%';" > /tmp/calls.txt
```

```python
import json, collections
c = collections.Counter()
for line in open('/tmp/calls.txt'):
    for tc in json.loads(line):
        fn = tc.get('function') or {}
        if fn.get('name') == '<tool>':
            a = json.loads(fn.get('arguments') or '{}')
            if a.get('name'):
                c[a['name']] += 1
```

- **One row can hold several calls** — a row count is not a call count.
- **Regexing `content` over-counts** mentions and misses compacted payloads. `tool_calls` is the only place
  a call is recorded as a call.
- **`LIKE` over a JSON blob is a full scan.** Without a timeout guard it returns nothing and reads as
  "zero uses".
- **This sensor belongs to one runtime.** Sibling harnesses read the same catalogue and write no row here,
  so "no recorded call" is not "unused" — which is exactly why the answer is hide, not delete.

## 5 · Traps that produce a wrong removal list

- **Body-grep is not status.** Grepping `DEPRECATED` across `SKILL.md` returns live skills that merely
  discuss deprecation — measured, most hits were healthy skills and the real tombstones were already inside
  an excluded archive directory. A delete list built from a body grep removes working capability.
- **A `[SKILL_PRUNED]` marker inside a body is a load instruction, not an empty file.** Check size and
  content before calling a marker a tombstone.
- **Alias pointer stubs are deliberate** (`description: "Alias -> <canonical>. Load <canonical> …"`): they
  exist so a pre-merge name keeps resolving. Deleting them defeats the merge; they are hide candidates only
  if the usage and reference probes both clear.
- **A grep hit is not a dependency** — check whether the hit is a registry snapshot, a changelog, a paste
  dump or a session log. Only live surfaces count.
- **Name collisions already fail loud**: the loader refuses an ambiguous bare name and asks for the
  category path; same-`realpath` mounts across categories resolve by rank while different content under the
  same name refuses. Both behaviours are correct — never "fix" a refusal by deleting one of the two.
- **Stale prompt snapshots carry ghosts**: entries for directories that no longer exist anywhere on disk,
  enumerated every turn. The snapshot is derived data — deleting it forces a rebuild.

## 6 · Report shape

Give the number that changed and the one line that reverses it:

```
index  1,254 -> 1,196 entries   (mount dedupe: N links removed, 1 restored - immutable contract)
block  146,864 -> 125,559 chars  (~5,300 tokens/turn)
revert: ln -s <target> <link>    (targets in <receipt>.rollback.json)
```

No revert command, no reduction — that is a deletion.
