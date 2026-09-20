# Inventory Sources & Parse Gotchas

Every count in a taxonomy plan must name its source. These disagree, and the disagreement is
usually the finding.

| Source | Answers |
|---|---|
| `hermes skills list` | installed set + category + source (`builtin` / `local` / `official` / hub) + enabled state; the footer gives per-source totals |
| `find <root> -name SKILL.md \| wc -l` | what is physically on disk (includes skills the loader does not resolve) |
| `<skills_root>/.usage.json` | per-skill `use_count`, `view_count`, `last_used_at`, `state`, `created_at` — **contains entries for skills already deleted from disk**, so it is usage evidence, not an inventory |
| `<hermes_home>/skills_manifest.json` | generated name/description/category index. Lives at the Hermes HOME, NOT inside `skills/` |
| `<skills_root>/.bundled_manifest` | bundled name→md5 map. **Plain `name:md5` text, not JSON** — `json.load()` fails on it; split on the last colon |
| `<skills_root>/.curator_ledger.jsonl` | append-only write history: actor, action, before/after file hashes per change |

## Parsing `hermes skills list`

Long skill names are TRUNCATED (~21 chars) and wrapped onto a continuation row whose trailing
cells (`category`, `source`, `trust`, `status`) are all empty. Drop those rows or you double-count.
Read the untruncated name from the skill's own frontmatter, never from the table.

An empty Category cell IS the uncategorised set. That number — not a directory listing — is what
the plan is written against. The footer line (`N hub-installed, N builtin, N local`) is a third
count that can differ from both.

## Upstream category labels

The canonical label set lives in the install tree, not the docs site:

```
<install_dir>/website/scripts/extract-skills.py   ->  CATEGORY_LABELS dict
```

It maps category dir → display label (e.g. `autonomous-ai-agents` → "AI Agents",
`software-development` → "Software Dev"). The published `/docs/skills` page is a client-side SPA
that renders `/api/skills.json` produced by that generator, so fetching the page returns an empty
shell ("No skills found"). Read the labels from source.

## Drift states against the canonical catalog

```python
state = ('IDENTICAL'   if local_sha  == canon_sha   else
         'CANON_NEWER' if canon_mtime > local_mtime else
         'LOCAL_NEWER')                          # else CANON_ABSENT
```

Match keys must be permissive: the directory name, the same name with a known prefix stripped
(`forge-`, `aaa-`, `agi-`, `asi-`, `apex-`, `audit-`, `rsi-`, `hermes-`, `kernel-`, `flame-`,
`well-`, `wealth-`), and the frontmatter `name:` lowercased. Exact directory-name matching
alone under-reports overlap badly.

Why four states matter: merging a `CANON_NEWER` entry writes staleness into canonical; merging a
`LOCAL_NEWER` entry silently deletes newer authoring. Neither errors. And a bucket that is mostly
`IDENTICAL` + drift is a mirror-hygiene problem, not a taxonomy problem — fixing the mirror removes
most of the "general" pile without touching content.

## Symlinks

Symlinked skills resolve to a real path elsewhere; they count once in the loader but can appear
twice in a directory walk (once as the symlink, once as the target). Resolve real paths before
deduping or cluster sizes inflate.
