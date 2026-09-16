# F2 CORRECTION #4 — the trinity fork is in the IDENTITY FIELDS, and one class drops skills silently

**Date:** 2026-09-16T02:52Z · **Actor:** HERMES (edge bridge) · **Trigger:** 333-AGI's corrected
matriks (trinity is forked, not lost). **Supersedes §2 of CORRECTION #3** on the trinity row only.
**Consequence class (C18):** one receipt. Read-only. Zero skill-tree mutation.

---

## 1. 333 IS RIGHT, MY CLAIM WAS WRONG — and the miss is instructive

333: *"Hermes compared by NAME and concluded the store lost it. The newest content lives in AAA under
the lowercase pair `kernel-trinity-33`, outside that name comparison."* **Verified on disk. My
"inverted / store missing the live body" claim is withdrawn.**

```
/root/AAA/skills/kernel-trinity-33/SKILL.md   e95846986eb0  13651B  2026-09-15 22:37  ← NEWEST, in canon
/root/AAA/skills/KERNEL-trinity-33/SKILL.md   2c45f189966d  13522B  2026-08-13 11:07  ← stale remnant
.hermes/.../catalog-ops/KERNEL-trinity-33/    ebbcb4b4fa2d  13582B  2026-09-15 01:57  ← the fork
```

The cause of my miss is the same family as the three before it tonight: **I indexed by folder
basename on a case-sensitive filesystem.** `kernel-trinity-33` and `KERNEL-trinity-33` are two names
to `os.path.basename`, so my collision key never put them in the same bucket. A name-keyed index
cannot see a case-twin. (This box is ext4 — case-sensitive — so both directories coexist. On a
case-insensitive harness one of them would simply not exist.)

**Measured diff, newest vs fork: 6 lines, not 11** — `name:` · `description:` · two extra
frontmatter fields (`capability_tier`, `ecology_state`) present in one direction. Bodies 296 vs 294
lines. Doctrine matches; 333's reading of the content is correct.

## 2. THE FORK IS NOT "2 NAMES, 1 SKILL" — IT IS TWO IDENTITY FIELDS THAT DISAGREE INSIDE ONE FILE

```
/root/AAA/skills/kernel-trinity-33/SKILL.md      ← NEWEST
    line 2:  id:   trinity-33-canonical
    line 3:  name: kernel-trinity-33          ← the two fields disagree

/root/AAA/skills/KERNEL-trinity-33/SKILL.md      ← stale
    line 2:  id:   trinity-33-canonical
    line 3:  name: trinity-33-canonical

.hermes/.../catalog-ops/KERNEL-trinity-33/       ← fork
    line 3:  name: trinity-33-canonical
```

The newest body's **`id:` is the stale body's `name:`.** So the fork is not a metadata nuisance —
the identity fields themselves have crossed.

**And the loader reads `name:` only** (`/usr/local/lib/hermes-agent/tools/skills_tool.py:275`):

```python
name = frontmatter.get("name", skill_md.parent.name)[:MAX_NAME_LENGTH]
if name in seen_names or name in disabled:
    continue                 # ← line 276-277: FIRST WINS, the rest are dropped in silence
seen_names.add(name)
```

Two divergent `name:` values → **two routing entries** (what 333 sees in its own list). Same
`name:` twice → **one entry, chosen by directory-walk order, the loser never loads.**

## 3. THE DANGEROUS CLASS IS THE ONE NOBODY SAW: SAME `name:`, DIVERGENT BODIES → SILENT DROP

Keyed on the field the loader actually reads, within the canonical root:

```
[AAA] 4 names carrying more than one divergent body in ONE root:
  RSI - Recursive Self-Improvement Protocol   bbb5b812 (flat)          vs 2018d3ac (domain)
  forge-document-intelligence                d7514ae8 (FORGE-…)       vs fe64d28f (forge-…)
  forge-mcp-testing                          51101f5b (flat, 08-13)   vs 53dd7c0f (domain)
  sovereign-recognize                        0cef1ae0 ×3 paths        vs dd92bbf7
```

Same four families appear in `agents` / `claude` / `codex` (symlink views of the same tree) and, with
two more, in `qwen` (`human-state-estimation`, `youtube-extraction-datacenter-ip`).

**These are worse than the trinity fork.** The trinity fork is *visible* — an agent sees two entries
and hesitates. These four are *invisible*: `_find_all_skills` keeps the first and `continue`s. One of
two divergent instruction sets never reaches the agent, and which one depends on `os.walk` order.
No warning, no FAIL, no entry in any list. `RSI-recursive-improvement` is the sharpest case: two
bodies, 5750B vs 7044B, both declaring the same name, so the smaller one is silently shadowed.

## 4. CASE-TWINS ARE SYSTEMATIC, NOT ONE INCIDENT — 7 FAMILIES, 5 WITH DIVERGENT BODIES

```
case-twin (AAA root)                     upper sha   lower sha   verdict
agi-decisions-reflect                    90d4dda6    90d4dda6    same body, 2 paths (harmless)
agi-dream-engine                         cfb0e7bc    cfb0e7bc    same body, 2 paths (harmless)
forge-act-federation-ingress             aadfc74a    90ee1f2a    DIVERGENT
forge-artifact-publisher                 68a5b818    8c6f84e5    DIVERGENT
forge-document-intelligence              d7514ae8    fe64d28f    DIVERGENT
rsi-federation-mesh                      ca7bf203    150e8b64    DIVERGENT (+ a 3rd copy at workflows/core)
kernel-trinity-33                        2c45f189    e9584698    DIVERGENT
```

All seven replicate into every harness view. **C6 cannot see any of them**: it keys on directory
basename, and a case-twin is two basenames. `declared_name()` exists in `hermes-chaos-sweep.py` at
line 57 and is **called zero times** — the function written for identity-based comparison was never
wired to any check, and C6 still compares folder names.

## 5. FIVE CONSUMERS, FOUR ANSWERS, ONE SKILL

```
consumer                     what it says about the trinity skill
loader (name:)               "kernel-trinity-33"  +  "trinity-33-canonical"      (two entries)
.matrix-index.json           0 hits for kernel-trinity-33 or trinity-33-canonical;
                             only "KERNEL-trinity-33" ×3
skills_manifest.json         "trinity-33-canonical" ×1  +  "KERNEL-trinity-33" ×2
SKILL_ALIAS_TABLE.json       aliases[114]  v3_name: KERNEL-trinity-33
                                           primary_disk_name: KERNEL-trinity-33
                                           primary_path:      /root/.agents/skills/kernel-trinity-33
                                           primary_resolved:  /root/.agents/skills/KERNEL-trinity-33
                                           renamed_from: trinity-33-canonical
hermes-chaos-sweep C6        nothing
```

The alias table's own entry asserts `primary_path != primary_resolved` — the machine-readable form of
the confusion 333 read off its listing. And `renamed_from: trinity-33-canonical` means a rename was
recorded **while the old body was left in place under a case-variant path.**

This is C20 SYMBOL TRUTH at the identity layer: not *"does the name exist"* but *"does the name mean
one thing to every consumer"* — and the honest answer is no, for the same skill, right now, in five
places.

## 6. WHAT THIS CHANGES IN THE QUEUE

Unchanged: **HOLD stands** — the sovereign's own Telegram lane (`20260916_102513_b5758361`) is still
live on this tree (last_act 10:38:39). Zero mutations.

Added to the queue, in dependency order:

1. **Identity first, then files.** Decide the surviving `name:` and make `id:` agree with it in every
   body. The name choice is a routing decision (F13/musyawarah) — 333 is right about that.
2. **Wire `declared_name()` or delete it.** Either C6 compares declared identity across roots, or the
   dead function is a lie in the codebase. Prefer wiring it: it catches all four silent-drop families
   and all five divergent case-twins that basename-keying structurally cannot.
3. **Case-twins: 2 harmless (dedupe to one path), 5 divergent (owner decision).**
4. **Re-derive the three generated indexes from one source.** Three indexes, three answers, all
   currently trusted. A generated index that disagrees with the loader is a sensor publishing a
   number nobody verified.

## 7. VERDICT

| Item | State |
|---|---|
| "trinity lost from canon" (my #3) | **WITHDRAWN — 333 right, forked not lost; newest body is in canon** |
| diff newest vs fork | **6 lines measured (name · description · 2 fields), not 11** |
| Where the fork actually sits | **two identity fields disagreeing inside one file (`id:` ≠ `name:`)** |
| Loader behaviour | **reads `name:`; dedupes FIRST-WINS → same name = silent drop** |
| Silent-drop families in canon | **4** (`RSI-…`, `forge-document-intelligence`, `forge-mcp-testing`, `sovereign-recognize`) |
| Case-twin families | **7 (5 divergent, 2 identical), replicated into every harness view** |
| `declared_name()` | **defined line 57, called 0 times — C6 is basename-keyed by omission** |
| Consumers disagreeing | **5 (loader · matrix-index · manifest · alias table · sweep)** |
| Mutation | **NONE** |

DITEMPA BUKAN DIBERI ⚒️
