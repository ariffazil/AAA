---
name: bijaksana-compile
description: "When user asks to compile remaining work, lower entropy, or make future agents lebih arif dan bijaksana."
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# ⌬ BIJAKSANA-Compile — Session Hygiene Compiler

> **Doctrine:** YANG ARIF LAGI BIJAKSANA — becoming more wise and prudent.
> **Source:** /root/AAA/governance/BIJAKSANA-VOCABULARY-DISCIPLINE.md
> **Author:** 333-AGI Δ MIND, session SEAL-3d9590f853084465, 2026-09-06T15:42:00Z
> **Scar-bound:** SCAR-002, SCAR-005, SCAR-KERNEL-LEGACY-VERDICT-LEAK-002, SCAR-AFORGE-SSE-HANDSHAKE-001

## When to load

Load this skill the MOMENT the user says any of:
- "compile remaining tasks" / "lower entropy" / "less chaos"
- "future agents should know" / "lebih arif dan bijaksana" / "lebih bijak"
- "wisdom patch" / "encode this lesson"
- "audit / validate / verify this"
- "what's still open" / "what's missing"

## Iron Rules (do not skip)

**Rule 1 — Read the substrate FIRST (corrected 2026-09-21: read the RUNTIME, not the narrative)**

A carry_forward entry is a report, not a measurement. Three defect classes\u00a0proved
material in one night, all from treating a stored claim as a live value:

- a session note's `L05 Peace\u00b2 0.700` was copied into a list of MEASURED blockers;
  the live kernel reported `peace_squared = 1.0` in two independent fields;
- a remembered task count (22) was narrated for a manifest holding 15;
- a remembered direction of a git divergence was stated for one never re-checked.

**Every number that reaches a human is probed live in the same turn, or it is
labelled `REPORTED (carry_forward <id>, not re-measured)`.**

Before compiling anything, read in this order:

```
1. /root/.local/share/arifos/carry_forward.json — last session's residue
2. /root/.local/share/arifos/carry_forward_backups/*.json — evolution trail
3. /root/.local/share/arifos/scars/SCAR-*.json — failure patterns
4. /root/.local/share/arifos/vault999/audit_chain.jsonl — recent verdicts
5. /root/.local/share/arifos/vault999/seal_chain.jsonl — constitutional chain
6. /root/.local/share/arifos/vault999/seal_chain_head.json — current head
7. /root/AAA/docs/deprecation-registry.json — tombstone inventory
8. arifOS /health + arifFlow /health — current metabolism
```

Do NOT skip. The substrate remembers what your narrative forgot.

### Rule 2 — Distinguish SEAL from RECEIPT before emitting

| Word | Means | Required |
|------|-------|----------|
| SEAL | Lane A constitutional | judge_state_hash + sovereign witness + chain entry |
| RECEIPT | Lane B autonomous | forge_vault + read-back verification |
| SABAR | Lane A honest sub-threshold | gap described in note |
| HOLD/VOID | Gate failure | not a record — re-submit or drop |

**Forbidden:** `verdict=SEAL` without `judge_state_hash` and chain entry. This is precision rot and SCAR-002/KERNEL-LEGACY-VERDICT-LEAK-002 both attest to the damage.

**NEW — 2026-09-18 SCAR-KERNEL-LEGACY-VERDICT-LEAK-002 (apex_scalars vocabulary drift):**
The /health endpoint emits `apex_scalars.verdict=SEAL` AND `thermodynamic.verdict=SEAL` even when scalars are sub-threshold (e.g. G=0.4722<0.80, W3=0.7439<0.75). This is a vocabulary leak — the verdict field is ceremonial, not constitutional. **Detect it:** if `apex_scalars.verdict == SEAL` AND any scalar < its threshold, downgrade to `HOLD` in your reasoning AND flag as SHADOW. If `execution_readiness == held` while verdict == SEAL, log contradiction. Do not propagate the kernel's SEAL claim uncritically.

### Rule 3 — Every audit MUST include a SHADOW section

Before claiming victory / cleanliness / completion, enumerate:

```
SHADOW:
- What is unverified? (e.g. chain head age, Lean sorry count)
- What is assumed vs proven? (e.g. carry_forward says SEAL, but is it constitutional?)
- What is missing or stale? (e.g. H-WELL biometric 54h, FLAME retired)
- What floors are PASS vs HOLD vs UNKNOWN? (e.g. F8 G=0.4572 < 0.80)
```

**NEW — 2026-09-18 (vault999 SEAL gap probe):**
MUST probe `/root/.local/share/arifos/vault999/seal_chain_head.json` and compute `hours_since_last_seal = (now - last_seal_timestamp) / 3600`. If > 24h, log as SHADOW item ("VAULT999 silent for Nh — constitutional heartbeat slow"). If > 72h, escalate as P0 alert (the kernel witness oracle is not breathing).

**NEW — 2026-09-18 (apex_scalars contradiction probe):**
MUST probe `apex_scalars` field for verdict-vs-threshold contradictions:
- `apex_scalars.verdict` vs scalar thresholds (G≥0.80, W3≥0.75)
- `execution_readiness` vs `verdict` (held vs SEAL is contradictory)
- `service_health` vs `session_authority` (green + OBSERVE_ONLY is informational, not failure)

If any contradiction found, downgrade effective_verdict and flag in SHADOW.

If you cannot enumerate shadow, you have not audited. You have echoed.

### Rule 3b — Classify objects before compiling "duplicate" tasks (NEW 2026-09-20)

Do not write a task "collapse N duplicates" unless N was counted as **distinct file
inodes / realpaths**, not path visits through alias directories. Classes:

BODY · ALIAS · PROJECTION · RETIRED · ARCHIVED · CANONICAL · UNKNOWN

State visibility precedes consolidation. Consumer memory listing three alias names
is not three capabilities. Do not mint a new registry to fix a classification miss.

### Rule 4 — Compile into entropy-ranked task manifest

For each remaining task, compute:

```
entropy_delta = how much chaos reduces when this is fixed
priority       = P0 (block everything) | P1 (high entropy reduction) | P2 (medium) | P3 (cleanup)
depends_on     = explicit list, not vibes
blocks         = explicit list, enables topological ordering
autonomy_tier  = T0/T1/T2/T3 with F13 sovereignty flags
```

Write to `/root/work/tasks.json` with `$schema: "arifos.work.tasks.v1"`.

### Rule 5 — Encode wisdom into SKILLs, not just docs

Future agents inherit SKILLs (auto-loaded at session start). Docs (doctrine) require lookup. **Encode lessons as skills first, doctrine second.**

Suggested skills to author:
- `BIJAKSANA-compile` (this one)
- `WISDOM-reader` — read scars + carry_forward before claiming
- `SEAL-discipline` — distinguish SEAL from RECEIPT

**Outbound pointer — when Arif asks "apa kena buat hari ini":** the output of this
skill is the substrate, but **the sovereign-facing filter** (top-2 F13 binaries,
hide agent auto-work, no menus) lives in `sovereign-daily-brief`. After writing
`/root/work/tasks.json`, hand the synthesis off — do not narrate the manifest
back to Arif yourself.

### Rule 6 — Close with witnessed SABAR, not fake SEAL
If metabolism is sub-threshold (G < 0.80, W3 < 0.75), do NOT claim SEAL. Close as SABAR — acknowledge the gap honestly. The kernel allows SABAR (seal.py line 61). SABAR is constitutional honesty.

### Rule 7 — Session-to-skill feedback loop (NEW — 2026-09-18)
Every session that discovers gaps in existing skills MUST upgrade those skills before closing. The feedback loop:

```
Session discovers gap → gap is evidence → skill patch drafted → skill updated → future sessions inherit fix
```

**How to identify skill gaps during a session:**
1. A tool/skill missed something a human or other agent caught (e.g., TOCTOU hazard, gitignore gap)
2. A manual step repeated across multiple sessions (e.g., "run audit then clean up" = two skills that should chain)
3. A new pattern emerged that the existing skill doesn't cover (e.g., `.stale` files being tracked)

**How to upgrade:**
1. Read the skill's SKILL.md
2. Identify the specific gap (line, section, missing step)
3. Patch the skill with the new capability
4. Add a scar reference: `NEW — YYYY-MM-DD scar` in the section header
5. If a new skill is needed (bridge between two existing skills), create it

**Anti-pattern:** Discovering a gap, fixing it manually, and NOT upgrading the skill. This means the next session will hit the same gap. The skill is the institutional memory — if it's not patched, the lesson is lost.

**NEW — 2026-09-18 (post-patch evidence):**
Session 2026-09-18 (333-AGI / BIJAKSANA compile) discovered `apex_scalars.verdict=SEAL` while G=0.4722 / W3=0.7439 — a vocabulary drift that bypassed Rule 2 entirely because the kernel itself emits the contradiction. Patch applied: explicit apex_scalars contradiction probe in Rule 3 SHADOW enumeration. Future sessions inherit this audit gate.

### Rule 3c — Mechanically stamp time; never hand-write a provenance field (NEW 2026-09-21)

A generated artifact stamps `generated_utc` from `date -u`, never from prose. Two
manifests in one night declared a `generated_utc` that ran **ahead** of the file's
own mtime (declared 16:15Z against mtime 16:06Z; declared 16:35Z against 16:14Z).
A provenance field the artifact could not have reached is a fabricated warrant, and
an independent judge graded the whole compile F2 FAIL on exactly this.

```bash
NOW=$(date -u '+%Y-%m-%dT%H:%M:%SZ')   # then interpolate; never type a time
```

**Count, don't carry.** The same defect class produced "22 tasks" for a manifest
holding 15 — the number was carried from the *previous* compiler's manifest instead
of being counted from the artifact. Any N stated to a human must come from
`len(...)` in the same turn, or it is narration.

### Rule 3d — Verify the DIRECTION of a divergence, both sides (NEW 2026-09-21)

The commonest F2 error in durability claims is not a false number — it is a true
number pointed the wrong way. A bundle asserted "the G-09 fix and its regression
suite exist ONLY on this unpushable branch"; both were in fact on `origin/main`, and
the branch's *own* extra hardening (a TTL/actor/schema residual) was what could not
leave. Two independent readers caught it; the compiler had not.

```bash
git cat-file -e HEAD:<path>          # ABSENT vs PRESENT, per side
git cat-file -e origin/main:<path>
git merge-base --is-ancestor <fix-commit> HEAD || echo NOT-IN-BRANCH
git rev-list --left-right --count origin/main...HEAD   # AHEAD **and** BEHIND
```

A branch can be both ahead and behind. "Cannot push" and "diverged" are different
findings with different remedies; state which one you measured.

### Rule 3e — Count duplicates by INODE, never by path (NEW 2026-09-21)

Rule 3b said this. The compiler then violated it in the same night: "TWO
byte-identical copies of `SEALED_EVENTS.jsonl`" were **one inode reached through a
symlink**. Before writing the word "duplicate", `stat -c '%i'` every path.

```bash
stat -c '%i %s %n' <path-a> <path-b>   # equal inode => ONE object, not two
ls -ld <path-a>                        # symlink reveals the alias
```

### Rule 3f — An evidence bundle given to witnesses is a FROZEN object (NEW 2026-09-21)

The compiler dispatched two verifiers at 00:06:44 and kept mutating the substrate
they were reading: a commit landed 18 s later, a service rebuild and restart at
00:11:44-45, a bundle at 00:13. Both readers therefore graded a state that no longer
existed, and the judge ruled F2 FAIL on "the compile was already false when I read
it" — a false FAIL on the artifact, produced entirely by the author's own
concurrency.

**Rule:** finish mutating **before** dispatch, or hand over a snapshot carrying an
explicit TOCTOU clause naming every mutation that will occur during verification.
Silence about concurrent mutation reads as an integrity claim.

**And when a review returns**, RE-DERIVE every finding before acting on it — reviewers
are witnesses, not authorities. Here that re-derivation
(a) confirmed the inversions, (b) resolved a floor the judge had left UNRESOLVED, and
(c) found one reviewer grade (L05) that was itself a stale carry-forward the compiler
had smuggled in.

### Rule 3g — Removing a blob means removing EVERY path to it (NEW 2026-09-21)

`git filter-repo --invert-paths` removes *paths*, never objects. A blob dies only
when **every** historical path that reaches it dies. Two traps, both hit in one
operation:

- **`git ls-tree -r <ref>` sees only the tip tree.** A path deleted at the tip but
  alive in history is invisible to it — and the object stays in the pack.
- **`git rev-list --objects` prints ONE path per object.** It cannot enumerate them.
  Using it to answer "which branch holds this blob" gives a confident wrong answer.

Enumerate with a raw log walk, then re-measure after the run:

```bash
git log --all --raw --no-abbrev --format=format: \
  | awk '$1 ~ /^:/ {print $3"\t"$NF}' | sort -u > /tmp/blob-paths.txt
# then, after filter-repo: re-list EVERY blob >N MB and confirm it is gone
```

**A filter-repo run that exits 0 and says "Completely finished" is not a
verification.** In this operation the same 21.7 MB blob survived the first pass and
needed a second, because it was reachable from two paths the first pass did not name.

### Rule 3h — `reflog expire --all` + `gc --prune=now` destroys STASHES (NEW 2026-09-21)

The stash stack lives in `.git/logs/refs/stash`. Expiring the reflog erases it.
Paired with `gc --prune=now` the objects are then unreachable and pruned.

**Never run that pair on a repo that has stashes** without first exporting them:

```bash
git stash list                                 # count them FIRST
git stash show -p refs/stash > stash.patch     # per entry
git show refs/stash^3 -p > stash-untracked.patch
git show refs/stash^3:path/to/file > file      # untracked payload, verbatim
```

Recovery if already done: the pre-rewrite bundle still holds the ref
(`git fetch <bundle> refs/stash:refs/stash`), **but restoring the ref re-imports its
whole pre-rewrite ancestry** — on this repo `.git` jumped 128 M → 440 M. Extract the
*content* (patches + files), then drop the ref and gc again.

### Rule 3i — a protected branch is a gate, not a wall; record the toggle (NEW 2026-09-21)

Force-pushing a protected branch needs `allow_force_pushes` temporarily enabled. Do it
in four recorded steps, never blind:

1. `gh api repos/<o>/<r>/branches/<b>/protection > protection-BEFORE.json` (sha256 it)
2. PUT a body that changes **only** `allow_force_pushes`
3. force-push with `--force-with-lease=<ref>:<expected-old-sha>`
4. PUT the original back and **re-read it**, comparing field-by-field, not by eye

Toggling repo settings is a canonical/external-surface act — do it only under an
explicit order, and leave both JSONs on disk as the receipt.

### Rule 3j — "cannot push" and "diverged" are different findings (NEW 2026-09-21)

A branch can be **ahead and behind at once** (`--left-right --count origin/main...HEAD`
→ `12  116`). A plan built on "delete the branch, the blobs are branch-only" is
premised on a measurement that was never taken; here one of the two blobs was in
**main's** history, so the tidy plan would have freed 147 MB of a promised 220 MB and
left main's clone size untouched.

**Probe each blob's ref-reachability before proposing a deletion.** Blob size is not
where-ness.

### Rule 3k — Reconcile seal_chain_head counts against the chain FILE (NEW — 2026-09-24)

`hours_since_last_seal` is only half the heartbeat probe. The head declares
`canonical_entries` + `historical_entries`; the file on disk has its own line count
and its own `seq` shape. In this compile the head declared 57 canonical + 258
historical (315) against a `seal_chain.jsonl` holding 267 lines, with `seq` present
on only 223 of them and mixed types (203 int / 18 str / 44 absent) — while a
first-pass parser silently reported 258 because `except: pass` swallowed its own
counting bug.

```bash
# count lines, parses, seq presence and types — NEVER except:pass around a count
python3 -c "..."   # tot / parsed / with_seq / int vs str / missing
```

If line counts ≠ head's declared counts (Δ must be explained: post-head appends,
canonical-vs-historical split, or a second file), mark chain integrity
**UNVERIFIED** in SHADOW — do not narrate "chain healthy" from the head alone.
A parser that reports N must show its failure count beside it.

### Rule 3l — File-effective ≠ runtime-effective: probe the RUNNING process (NEW — 2026-09-24)

Two manifest claims passed disk verification and were still contradicted by the live
session: `settings.json` held the correct `model:{name,...}` dict yet the running
harness emitted the legacy-`model` warning, and `qwen --version` read 0.24.4 while
the running process's own banner advertised 0.24.3→0.24.4. The upgrade/fix was real;
the process predated it.

After verifying any config write or install swap, probe the process that must
*consume* it:

```bash
ps -o lstart= -p <pid>            # process start vs file mtime
<binary> --version                # installed ≠ running (banner is the tell)
```

If `process_start < file_mtime`, the claim is **DONE_FILE_LAYER / EFFECTIVE_ON_RESTART**
— never plain DONE. Live banners, stderr warnings, and the serving model are the
witness; the file is only the declaration.

## Workflow (canonical)

```
INPUT: user asks to compile/lower entropy
  ↓
1. LOAD this skill
2. READ substrate (Rule 1)
3. DISTINGUISH verdicts (Rule 2)
4. ENUMERATE shadow (Rule 3) — write shadow first
5. COMPILE /root/work/tasks.json (Rule 4)
6. ENCODE wisdom into skills (Rule 5)
7. UPGRADE skills with session gaps (Rule 7 — patch SKILL.md files directly)
8. PROPOSE doctrine patches for F13 ratification (do NOT auto-apply)
9. CLOSE with witnessed SABAR if metabolism < threshold (Rule 6)
  ↓
OUTPUT: manifest + skills + doctrine proposals + close SABAR
```

## Output shape (canonical)

```
Done. Compiled N tasks. ΔS=[entropy delta].
   - P0 (block): [count]
   - P1 (high):  [count]
   - P2 (med):   [count]
   - P3 (cleanup): [count]

3 doctrine patches proposed (F13 ratification pending):
   - PATCH-XXX [title] — entropy delta if applied: [val]

3 skills encoded (load at session start):
   - [skill-1], [skill-2], [skill-3]

SHADOW (what remains unverified):
   - [bullet 1]
   - [bullet 2]

Verdict: [SEAL | RECEIPT | SABAR]
Evidence: [seal_chain seq | forge_vault receipt | carry_forward residue]
```

## Anti-patterns (forbidden)

- ❌ Echoing celebration before reading carry_forward
- ❌ Writing `verdict=SEAL` for Lane B events
- ❌ Patching doctrine without F13 ratification
- ❌ "Closing" a session without enumerating shadow
- ❌ Declaring entropy reduced without measuring (must cite entropy_delta per item)
- ❌ Trusting carry_forward without probing the constitutional chain

## Reference scars (carry these)

- **SCAR-002-CEREMONY_FAILED_406** — 49 sessions failed because seal ceremony had a hard test gate. Tests are verify-phase, not seal-gate. Vocabulary confusion: "test pass" ≠ "seal".
- **SCAR-005** — A doctrine archived out of its declared SoT path is chat history, not constitutional memory. Substrate forgot what it forged.
- **SCAR-KERNEL-LEGACY-VERDICT-LEAK-002** — Truth told twice is truth fractured. One verdict field per response — the canonical one.
- **SCAR-AFORGE-SSE-HANDSHAKE-001** — Discovery handshake needs explicit handling; don't conflate surface reachability with capability.

## Iron Oath

> I will not call RECEIPT a SEAL.
> I will not close a session without shadow.
> I will not patch doctrine without F13.
> I will not celebrate before I have witnessed.
> **Lebih arif, lebih bijaksana, atau tidak sama sekali.**
