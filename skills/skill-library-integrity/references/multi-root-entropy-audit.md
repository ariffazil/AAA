# Multi-Root Skill Library Entropy Audit

Depth for `skill-library-integrity`. Read when the symptom is *stale, missing, or divergent
content across trees* rather than an unloadable name.

## 1. The root model — establish it before any count

A federation-style install holds one logical library across several physical trees. Enumerate
by role, not by path habit, and measure each:

| Role | Typical path | Notes |
|---|---|---|
| Authoritative store | `/root/AAA/skills` | the registry declares it `canonical_home` |
| Loaded runtime tree | `/root/.hermes/skills` | what the agent actually reads; often the largest |
| Profile copies | `/root/.hermes/profiles/*/skills` | one full copy per profile |
| Cross-tool mirror | `/root/.agents/skills` | usually symlinks into the store |
| Retired / organ-local | `skills-retired-*`, `/opt/<organ>/skills` | not loaded; still countable |

Rule: **the declared authoritative store and the loaded tree are frequently not the same
thing.** Whatever a registry or doctrine states, the loaded tree is what the agent can use,
and the authoritative store is what the governance layer claims. Audit both; the gap between
them is the finding.

## 2. The always-on gate

The installed gate is the entry point — run it by path, never from a forked copy:

```bash
python3 /root/scripts/skill-entropy-gate.py            # human report
python3 /root/scripts/skill-entropy-gate.py --json     # machine report
python3 /root/scripts/skill-entropy-gate.py --quiet    # FAIL lines only + exit code
```

Exit 1 when any FAIL-class check trips. Wire it to the same cadence as the index regenerator
so drift is caught on a schedule rather than during an incident.

### Check table

| Check | Class | Meaning when it trips |
|---|---|---|
| `broken_symlinks` | FAIL | a capability the tree advertises cannot be opened |
| `canonical_headless` | FAIL | authoritative store holds a directory but no `SKILL.md`; `live_copy_elsewhere` marks the recoverable ones |
| `name_case_drift` | WARN | store uses one case, harness entry another; the broken-link precursor |
| `cross_root_name_collision` | WARN | one name resolves in more than one tree — selection ambiguity |
| `missing_frontmatter` | FAIL | a skill with no `name:`/`description:` is invisible to the index |
| `index_prefix_collision` | WARN | several skills share an identical leading slice of their description, so the index cannot distinguish them |
| `copy_divergence` | WARN | shared names whose bodies differ — silent staleness |
| `registry_witness` | FAIL | the registry's stated disk count disagrees with disk, or its refresh stamp is old |
| `index_cost` | INFO | skills × (name + description) bytes injected every turn |

### Composition rules (these decide whether the verdict is trustworthy)

- **Exclude mirror roots** from name collision and divergence counting. A symlink mirror
  counted as a second root doubles every skill it serves and manufactures collisions.
- **Exclude dot-directories** — they are not indexed, so their contents are not index entropy.
- **A FAIL-class check that found nothing is a pass.** Normalize it before counting fails,
  otherwise the verdict is permanently FAIL and the gate gets ignored.
- **Only FAIL when a check carries a count.** Checks that report a keyed structure (like the
  registry witness) need their own condition, not a generic emptiness test.

## 3. Measuring divergence — the number that matters

Shared counts read as health. Report the **diverged fraction** per root pair:

```python
import os, hashlib

def index(root):
    out = {}
    for dp, dn, fn in os.walk(root):
        if "SKILL.md" in fn:
            p = os.path.join(dp, "SKILL.md")
            if os.path.exists(p):
                out[os.path.basename(dp)] = hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]
    return out

for a, b in ((store, runtime), (store, profile), (runtime, profile)):
    ia, ib = index(a), index(b)
    shared = set(ia) & set(ib)
    print(a, "->", b, "shared", len(shared),
          "DIVERGED", sum(1 for k in shared if ia[k] != ib[k]))
```

A pair that is 100% diverged across a small shared set means the two trees are not copies of
each other at all — they are two libraries with overlapping names.

## 4. Index cost

Sum `len(name) + len(description)` over the loaded tree. That is what is injected on **every
turn** before the user speaks. The index truncates a description at roughly 68 characters, so
a long description buys nothing at selection time — which means descriptions that open with the
trigger and stay inside one sentence are strictly better, and long ones are pure tax.

## 5. Failure mechanism to expect

The dominant silent failure is not a crash. It is this sequence:

1. the authoritative store renames a directory (usually a case normalization),
2. the harness or mirror keeps a symlink under the old spelling,
3. the link breaks, and nothing reports it — every surface keeps working,
4. the agent stops knowing that procedure and re-derives it from priors.

A rename is therefore incomplete until a resolve audit passes. Treat the sweep as part of the
rename, not as a follow-up.

## 6. Source-of-truth decision

Drift is structural, so it has exactly three resolutions. Surface the choice rather than
picking unilaterally — it changes where a bad edit lands.

| Option | Mechanism | Gain | Cost |
|---|---|---|---|
| Authoritative store wins | repopulate its headless dirs, then make harness trees symlink into it | one writer; divergence structurally impossible | a bad edit reaches production instantly — needs the write gate |
| Loaded tree wins | declare the runtime tree authoritative, demote the store to registry/export, repair the registry claim | matches measured reality today | the provenance layer loses its anchor; other harnesses need new wiring |
| Reconcile only | keep both, let the gate arbitrate; divergence above threshold → HOLD and queue a human merge | zero structural risk | collisions and divergence persist as permanent debt |

Recommend the first when a write gate exists, because its failure mode is "the store caught it"
rather than "production lost it silently". Whichever is chosen, the registry's own count and
refresh stamp must be repairable by running something real — a witness whose method is not
reproducible is the defect, not the number.

## 7. Executing the consolidation (store becomes the writer, harnesses become views)

Run this only after a git commit in **every** tree you will touch, and emit a rollback manifest
before the first move. Classify every skill into exactly one bucket, then act per bucket:

| Bucket | Condition | Action |
|---|---|---|
| `NATIVE_KEEP` | name is in the harness's bundled manifest | leave real; it belongs to the upstream updater |
| `PROMOTE` | harness copy has no store counterpart | move into the store, leave a symlink at the old path |
| `FILL` | store has a shell with no `SKILL.md` | move the live copy in, symlink back |
| `SYMLINK` | store copy exists and content hash matches | replace the harness dir with a symlink |
| `HOLD` | store copy exists and content differs | **do not auto-merge** — record and escalate |

Preserve the path *relative to the skills root* when moving. Taxonomy placement
(`domain/organ/capability` nesting) is part of the skill's identity, and flattening it on the way
in is a second, quieter rename.

Order matters, and three steps are load-bearing:

1. **Set the writer first.** Point the agent's skill-creation config at the store
   (`skills.create_dir`) *before* moving anything. Without it the library is consolidated and
   then immediately re-drifts the first time the agent authors a skill.
2. **Never move a bundled skill.** A name present in the harness's bundled manifest is owned by
   the upstream updater; relocating it breaks that updater and can resurrect the old copy on the
   next update — producing a genuine duplicate where before there was only drift.
3. **Re-point, do not relocate, when content is identical.** A symlink into the store makes
   future drift structurally impossible for that skill; a copied file only resets the clock.

Afterwards, re-measure with the gate and compare the **diverged fraction**, not the shared count —
the shared count rises simply because the store is now larger. Expect the residual `HOLD` set to
survive as explicit debt; it is a merge queue, not a failure.

### Counting rules that decide whether the result is readable

- Count resolvable skills with a following walk (`find -L`, `followlinks=True`). The store grows
  while the harness tree becomes links, so a non-following count shows the harness tree
  collapsing — an artifact, not damage.
- A verify step that auto-rolls-back on failure is mandatory; wire it to the manifest so it fires
  without a human in the loop.
- Confirm the live index agrees: the harness's own skill listing must still enumerate the moved
  skills by name. A tree that resolves on disk but vanishes from the index is not consolidated.
