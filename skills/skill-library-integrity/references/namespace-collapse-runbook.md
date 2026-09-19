# Namespace collapse — retiring skill IDENTITIES

Companion to SKILL.md §6–§7. Use when the defect is *taxonomy entropy*: one capability shipped under
many names (per-harness clones, aliases parading as skills, case-twins, incident fossils, vendor
junk). The goal is to remove IDENTITIES without removing ABILITIES — every retired body is frozen with
its bytes intact and an undo path in a ledger.

## 0. Classify by family, not by file

Group three ways and act on the family. A family you have not named is a family you will re-create.

- **normalized name** — strip brand prefixes, then look for collisions:
  `^(forge|claude|qwen|kimi|opencode|copilot|gemini|grok|aaa|agi|asi|agent|hermes)[-_]+`
- **declared identity** — the frontmatter `id:` field (distinct from `name:`, the routing field)
- **case-insensitive folder name** — case is not doctrine; two bodies is two bodies

## The six defect classes and the one correct remedy each

| Class | Looks like | Remedy |
|---|---|---|
| alias-parading | body is a redirect to another skill | kill it, or repoint to the successor — never leave a redirect that still loads |
| per-harness clone | N bodies, same doctrine, different mascot + state path | ONE canonical with a harness-binding table; the variants become rows |
| case-twin | `X` and `x`, two bodies | one body, one name — casing is not doctrine |
| vendor / foreign profile | another product's bundled skills inside your catalog | relocate to the harness that owns them, or freeze |
| archive-still-loading | an `.archive*` directory inside the walked tree | an archive inside the walk is not an archive; move it out |
| incident fossil | a skill whose whole purpose is one dated event | extract the heuristic into the lane's playbook, freeze the incident |

## 1. Reconnaissance — measure before you cut

| Purpose | Command / path |
|---|---|
| The one census (never hand-count) | `python3 /root/scripts/skills-census.py --json \| --write \| --quiet` |
| Cost>value ranked from the usage ledger | `<retired-root>/_tools/usage_cost_value.py` |
| Collapse + freeze + ledger | `<retired-root>/_tools/namespace_collapse.py` (dry-run default, `--apply`) |
| Resolve aliases to surviving canon | `<retired-root>/_tools/repoint_aliases.py` |
| Sweep dangling links across ALL mirror trees | `<retired-root>/_tools/repair_dangling.py [tree ...] [--apply]` |
| Regenerate the placement manifest | `python3 <AAA>/scripts/placement_manifest.py` |
| Independent mesh check | `bash /root/scripts/skill-mesh-sync.sh --check` |
| Full backup before the first cut | `tar czf <backup>.tar.gz -C <AAA> skills` + record its sha256 |

Read census output as fields, not prose: `canonical_skills`, `viewed_skills`, `whole_mesh_skills`,
`duplicate_identity_groups`, `duplicate_identity_skills`, `total_shells`, `broken_symlinks`, `verdict`.

## 2. Mirror trees — the views a body-level kill forgets

A retired name leaves dangling links wherever a harness mounts the store. Sweep all of them:

```
<store>                              (canonical, when a name is replaced by a link to its successor)
~/.hermes/skills
~/.hermes/profiles/<profile>/skills
~/.agents/skills
~/.claude/skills
~/.codex/skills
~/.qwen/skills
~/.kimi-code/skills
~/.config/opencode/skills
~/.gemini/skills                     (may not exist — absence is not a defect)
~/.arifos/agents/<agent>/skills
```

Resolution rule per dangling link: **repoint** when the link's NAME still maps to a live canonical
skill; **remove** when the name itself is retired; **leave and report** when the name has no single live
resolution — ambiguity is a judgment call, not a sweep action.

## 3. Freeze convention — reversible, and out of every walked tree

Move the body to `<store>-retired/<date>-<reason>/<original/rel/path>`. An archive left INSIDE the
store is one glob away from loading again. If a body must stay in-tree, rename its marker file so no
loader matches it (`SKILL.md` → `SKILL.md.frozen`) — a loader that walks by exact filename skips it.

```json
{
  "ts": "<ISO-8601 UTC>",
  "authority": "<who ordered the retirement>",
  "canon": "<store>",
  "freeze_root": "<retired root>",
  "undo": "mv <frozen_path> <orig_path>   (paths recorded per item below)",
  "items": [
    {
      "rel": "<path relative to store>", "tier": "<defect class>", "reason": "<one clause>",
      "successor": "<canonical replacement or null>",
      "action": "move | unlink_symlink",
      "orig_path": "<abs>", "frozen_path": "<abs>",
      "files": {"<relpath inside the skill>": "<sha256>"},
      "sha256": "<for a single-file or symlink item>"
    }
  ]
}
```

Hash BEFORE the move, never after — the ledger must prove the frozen bytes equal the retired ones.
Write it before the first mutation, dry run included.

## 4. The cost>value lens, and its two hard limits

`~/.hermes/skills/.usage.json` is a per-name ledger: `use_count`, `view_count`, `last_used_at`,
`last_viewed_at`, `created_at`, `patch_count`, `pinned`, `state`. History:
`~/.hermes/skills/.curator_ledger.jsonl`.

Limits that stop it becoming a false oracle:

1. **Scope.** It covers ONE harness. A zero here is not a zero everywhere — never present it as
   library-wide.
2. **Horizon.** Tracking starts when it starts. `use_count == 0` over a short window is evidence of
   cost without demonstrated value, not a verdict. Rank by it, disclose the window, never evict on it
   alone.

A large skill that was never used is a cost signal, not a bug. The decision to freeze it belongs to the
authority that owns the library, together with the reason.

## 5. Merging a family into one skill

- One canonical skill with a **mode per source**, or a **harness-binding table** when the sources differ
  only by which runtime they serve.
- **Every** distinct trigger phrase from **every** source description survives — in the new description
  and in a mapping table `old name -> new mode/section`. Grep each old trigger against the new body
  before retiring the sources; a merge that loses a trigger silently removes a capability from discovery.
- Carry the payload: keep every checklist item, metric formula, probe, red flag and refusal case. A body
  absorbed without its content is a content loss hiding inside a structural repair.
- Freeze the sources with their own ledger; never delete in the same pass.
- Verify: merged file exists and is larger than any single source, all sources gone from the walk, all
  sources present in the freeze tree, the ledger parses.

## 6. Confirming the kill — four checks, in order

1. **Resolve every replacement you created.** A directory retired into a symlink is correct only if the
   link *resolves*. Build it and immediately `readlink -f`. A relative target computed at the wrong
   depth yields a dangling link that still carries the right NAME — it reads as "repointed" in a listing
   and fails only when a loader touches it.
2. **Re-run the census AND the independent mesh check.** The broken-link count must return to its
   pre-sweep value and both must agree; a sweep that moves it from 0 to N retired the body and forgot
   the views.
3. **Resolve names the way the LOADER does, not the way `ls` does.** A surface can advertise a name with
   no body anywhere on disk — phantom capability, one layer above the dead symlink, invisible to
   directory checks because there is no directory to check. Spot-check names from the surface and
   resolve each to a real file; if one resolves to nothing the surface lies and every count derived from
   it inherits the lie.
4. **Read the layers above the store for names you retired** — registry, alias table, ownership map,
   genealogy, and any *layer block* inside the registry, which can claim a whole family whose folders
   hold nothing but a liveness marker. Prune in the same pass or the registry can resurrect what you
   removed.

## 7. Report shape

Name, per tier: what was removed, the evidence that classified it, and the successor if any. Then the
witness table (census before/after, freeze ledger, git status when the store is a repo, backup path with
sha256). Then the findings that outlive the sweep — including defects you FOUND but did not cause,
labelled as such. Finish by naming what you deliberately did NOT do and the authority it needs.
