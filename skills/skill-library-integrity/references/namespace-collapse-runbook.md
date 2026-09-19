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

## The eight defect classes and the one correct remedy each

| Class | Looks like | Remedy |
|---|---|---|
| alias-parading | body is a redirect to another skill | kill it, or repoint to the successor — never leave a redirect that still loads |
| per-harness clone | N bodies, same doctrine, different mascot + state path | ONE canonical with a harness-binding table; the variants become rows |
| case-twin | `X` and `x`, two bodies | one body, one name — casing is not doctrine |
| vendor / foreign profile | another product's bundled skills inside your catalog | relocate to the harness that owns them, or freeze |
| archive-still-loading | an `.archive*` directory inside the walked tree | an archive inside the walk is not an archive; move it out |
| incident fossil | a skill whose whole purpose is one dated event | extract the heuristic into the lane's playbook, freeze the incident |
| contradicting twin | two independent write-ups of ONE procedure that have drifted into disagreeing, where one instruction cannot execute at all | merge the identity AND correct the instruction in the same pass — see §8 |
| mode-router umbrella | a thin body whose stated modes are EACH already owned by a live skill; it carries provenance and a routing table, not a procedure | retire it, after re-pointing every surface that names it — see §9 |

A **mode-router umbrella** is the one class where the body itself looks reasonable and the defect is
structural: every mode resolves to an owner, so the router adds a hop and a stale copy of the routing
map. Detect it by writing each mode's owning skill name beside it and checking that skill really owns
that mode — if all of them do, the router is an identity wearing a capability's clothes.

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
- **Decide "lost content" by CONCEPT, not by LINE.** A line diff (`diff old new | grep '^<'`) is not
  content-loss proof: a consolidation rewrites a rule in fewer words, moves it into another section, or
  merges two clauses into one, so a rule that is fully present reads as deleted because its *sentence*
  changed. Before re-adding anything a diff appears to have dropped, grep the NEW body for the
  distinguishing noun phrase of the rule — the heuristic's name, the threshold, the field name — not the
  old sentence. Acting on the diff alone re-adds content that already exists, bloat the survivor, and
  re-introduces the very duplication the merge removed.
- Freeze the sources with their own ledger; never delete in the same pass.
- Verify: merged file exists and is larger than any single source, all sources gone from the walk, all
  sources present in the freeze tree, the ledger parses.
- **Ship the retention gate as a SCRIPT and re-run it yourself against the disk.** When the merge is
  delegated, a child's "checks passed" is a self-report, not evidence: children have certified merges
  whose merged body no longer contained the retired names. Ask for the gate's raw output, then run the
  gate again yourself — `scripts/discovery_guard.py <merged_skill_dir> <frozen_source_dirs...>` must
  print `VERDICT: DISCOVERY PRESERVED` before the sources may stay out of the walk.
- **State the constraint, not the command, in delegated task context.** A task payload containing a gated
  operation's literal token (a destructive shell verb, a credential-path pattern) is refused by the
  pre-tool gate before any worker starts, and the refusal consumes the whole delegation. Phrase the
  instruction as the behaviour you want ("leave that attribute untouched") rather than as the command
  that would change it; a worker does not need the literal string in order to obey the rule.

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

Report in the currency the owner asked for, not in the number that is easiest to produce. For an entropy
sweep:

- **identities removed** and **capabilities preserved**, each with the successor that carries it;
- the **ratio** between them as the primary KPI — identities removed / capabilities preserved, given as a
  pair with the capability count. A sweep that removed names without preserving anything and a sweep that
  preserved everything without removing an identity are different results, and either number alone can be
  dressed up as progress;
- **false positives**, counted and published next to the findings: say how many candidates a naive
  detector would have flagged and how many survived inspection. An audit that reports only findings
  manufactures work;
- name, per tier: what was removed, the evidence that classified it, and the successor if any;
- the witness table (census before/after, freeze ledger, git status when the store is a repo, backup path
  with sha256);
- defects FOUND but not caused, labelled as such;
- finish by naming what you deliberately did NOT do and the authority it needs.

Never lead with a raw file or skill count — a count moves when a file is renamed, and the point of the
sweep is that the capabilities did not move.

## 8. Contradicting twins — the duplicate that drifted into an impossible instruction

Deduplication asks "are these the same thing?". Ask the harder question too: **do they disagree?**

Two skills written independently from one procedure are NOT byte-twins — they share almost no lines, so a
content diff finds nothing and both look healthy. What drifts is the substrate: one names a write target,
command, or endpoint that cannot work; the other names one that can. The pair then teaches two different
procedures for one task class, and the agent that loads the wrong one walks into an unexplained wall — a
failure that looks like a broken tool rather than a broken document.

How to detect it, since file comparison will not:

1. **Write the one-sentence question the family answers.** If two bodies return the same sentence they are
   the same capability — then read their *instructions* side by side, not their prose.
2. **Run each instruction against reality.** Does the target path accept a write (permissions, immutable
   attribute, mount, ownership)? Does the named command exist? Does the endpoint answer? The instruction
   that cannot execute is the defect, and it is the only side whose correction is not a judgment call.
3. **Verify any claim about readers or ownership by looking for the readers.** Labels written beside a
   file ("stray", "unused", "deprecated", "SOT", "canonical") drift in the opposite direction from the
   substrate: the surface with the most RECENT writes and the live citations is the executing one, whatever
   its label says. Grep for who reads a path before believing who claims to own it.
4. **Merging the identity and correcting the instruction are ONE operation, not two.** A merged body that
   keeps the dead instruction is worse than the duplicate it replaced: it now speaks with one voice, and
   that voice is wrong. Fix the text, then freeze the retired body — the frozen copy still holds the
   original wording as evidence of what was wrong.

Symptom that points here: a family of "same capability" bodies whose SHARED content is nearly zero
(measure it: shared non-trivial lines / union). Zero overlap with an identical purpose means two people
solved the same problem separately and neither read the other's answer.

## 9. Sweep the CLASS, and orchestrate the sweep without racing yourself

**A wrong instruction is rarely confined to the file where you found it.** A defect that is a *pattern*
(a stale target, a mislabelled surface, an inverted SOT claim) was almost certainly copied forward by
whoever wrote the second skill. Measured: one inverted-ledger instruction existed in three separate
skills, and repairing the two named in the audit left the third — the one that actually owned the write
path — still teaching the impossible action. After fixing any instance, grep the whole store for the
pattern (`grep -rn '<the wrong target>' --include=*.md <store>`), classify each hit as instruction vs
history, and fix the instructions. Repair the dependents, not the detector: when a path or claim is
corrected, the consumers of that claim are part of the same defect.

**Separate the two kinds of stale reference before repairing either.** A dead path inside a dated
`references/<session>.md` is a RECEIPT — evidence of what happened, and it is allowed to point at
something that has since moved. A dead path in `SKILL.md` is an INSTRUCTION — the agent will try to
follow it. Only the second is a defect; repairing the first destroys provenance.

**Three states, not two.** A target under a locked tree is not automatically unusable: a sanctioned lane
may clear the attribute for one operation and restore it. So classify each reference as *executes*,
*needs a sanctioned lane* (state the lane — the defect is the omission), or *cannot execute* (repair it).
An impossible instruction wastes action forever; an incomplete one wastes one attempt and then teaches
the lane.

**Orchestration — the parent's own mistakes cost more than a child's.** When the collapse is delegated:

1. **Do not stage or commit while a child is still writing in the same worktree.** `git add <dir>` picks
   up a sibling's half-written file and the history records it as a finished deliverable. Stage explicit
   paths only, and wait for the batch to report before committing anything they touched.
2. **The parent's sweep runs LAST.** Children retire bodies; every retirement leaves dangling view
   symlinks in the mirror trees. A sweep run while children are still working is stale before it finishes,
   and the next census reports the parent's own in-flight work as a defect.
3. **Re-run the measurement after every child returns, not once at the end.** A count of broken links
   read 24, then 18, then 0 inside one day as repairs landed — each reading was true when taken and wrong
   minutes later. Report the state and its trajectory ("0 now; 24 this morning; expected during a merge,
   repaired same day") rather than a single frozen sample, and never quote an earlier sample as current.
4. **Children find defects outside their slice and leave them, correctly.** Harvest those reports and
   assign them — an out-of-scope finding is usually the same class as the one they were sent to fix, and
   it is the cheapest instance to repair because the pattern is already loaded.
