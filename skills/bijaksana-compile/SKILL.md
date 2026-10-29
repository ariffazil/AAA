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

> **PRIME LAW (F13-articulated 2026-10-22, Arif):** **STATUS IS NOT EVIDENCE** -- *Status bukan bukti.*

> **LOOP BINDING (APEX-ZEN alignment, 2026-10-29):** This compiler owns ONE phase-gate of the
> ONE reality loop — **IMPROVE → OBSERVE** (between-session metabolism). Input contract:
> substrate residue + execution receipts (arifFlow / forge_vault / PROOFS). Output contract:
> re-derived queue (`/root/work/tasks.json`, Rule 3n) + wisdom writeback. Lessons needing FORCE
> are proposed to F13 for doctrine-to-runtime compilation — never self-applied. Never routes
> jobs (aaa-capability-compiler's gate); never writes runtime gates (doctrine-to-runtime-compiler's gate).
> A stored status field is a claim about the past, not a measurement of the present. Compile by
> **re-deriving** each row from a live probe; never carry a status forward. See Rule 3n.

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

**NEW — 2026-10-11 (two carry files, and tasks.json may not be v1):**
`/root/.hermes/carry_forward.json` is not guaranteed to be a symlink of the canonical file. Compare inodes before treating them as one store. On 2026-10-11 they were two regular files (290955 vs 28104 bytes). `/root/work/tasks.json` may be an ad-hoc ledger rather than `arifos.work.tasks.v1`. If `tasks` is missing, do not report `n_tasks=0` as an empty queue — read the keys that are actually there, then rewrite v1 only after a live compile. Back the old file up first.

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

**NEW — 2026-10-21 (apex_scalars verdict field is optional):** the `apex_scalars` block on `/health` sometimes carries NO `verdict` field at all — the verdict lives in `thermodynamic.verdict` and `execution_readiness`. Probe all three locations before declaring a contradiction; do not crash the probe on a missing key, and absence of the field is not absence of the drift.

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

**NEW — 2026-10-13 (survival-edge queue):**
Keep `s1-witness-independence` through `s10-capability-loss-measurement` at the front of `tertib_flow`, in that order, until each evidence field records a measurement. Do not drop them on the next compile. Do not mint a doctrine file for them. Do not demote `p0-arifos-accept-queue` out of P0. Measure `s7-human-objection-path` first: a refusal that an affected human contradicts must change the next action, or the row stays open. The source is the 2026-10-13 paste. The OneDrive PDF was not opened.

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

**NEW — 2026-10-21 (backup discipline):** Back up tasks.json BEFORE the first write, not after — a post-write `shutil.copy` archives your own edit and destroys the only pre-edit snapshot. Check a fresh `.bak-*` exists first; if not, the `shutil.copy` must run before `json.dump`. A compiler that loses the pre-edit state has broken reversibility — F2-class defect. (Hit once by hermes 21/10; the 13:29:55Z backup from the prior compiler survived only by luck.)

**NEW — 2026-10-13 (do not copy metabolism out of tasks.json):**
`metabolism.G`, `hours_since_last_seal`, and `last_seal_timestamp` inside
`/root/work/tasks.json` go stale the same day. Recompute them in the write
process from `:8088/health` `apex_scalars` and from `seal_chain_head.json`.
`governance.last_seal_timestamp` is a commit-receipt clock. It is not the chain
head. If the two clocks differ, write both. Do not pick the prettier one.

**NEW — 2026-10-13 (a delete-alert is not a delete order):**
A site-audit line that says orphan files will be deleted does not authorize
deletion. If live HTML still names a hashed asset, that asset is load-bearing.
Count the HTML files and confirm the asset is on disk before any cleanup task.

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

### Rule 3m — When a probe CANNOT_WITNESS, trace the chain to root, then grep for the DEFINITION (NEW 2026-10-21)

A failing probe is a LAYER, not a root. Walk it down each hop — 2026-10-21 instance:
`health unit exit 1 → dependent service → vault999-writer /vault/status HTTP 500 →
asyncpg UndefinedTableError "cooling_queue"`. Then do the step compilers skip:
**grep the repo for the missing artifact's DEFINITION.** Here `CREATE TABLE cooling_queue`
existed nowhere in /root/arifOS (only `cooling_ledger_entries` in
supabase/migrations/20260628_001_cooling_ledger_core.sql), which flipped the pending F13
decision from "apply the migration" into "first witness which instance ever had it, and
with what columns". Absence of the DEFINITION changes the decision's SHAPE, not merely its
difficulty. Evidence: /root/memory/eureka-entries.jsonl `E-cooling-queue-no-ddl-20261021`.

### Rule 3n -- STATUS IS NOT EVIDENCE (PRIME LAW, NEW 2026-10-22)

A status field records the **past**, not the **present**. Work moves; the map does not.

The failure class: a compiler that copies `status` forward **re-opens closed work** and
**re-closes contested work**. Live instance (2026-10-22): 2 of the 3 front-of-queue items were
already DONE but listed open -- `p2-union-test-defect` (pytest 70/70 pass live; fix commit is HEAD
on both branches, tree-identical) and `p2-kvm2-guard-activate` (guard `cc534602ad0` is running
HEAD; process start 12:42:28Z > commit 05:27:15Z). `seal-events-2-breaks-forward-fix` likewise
already repaired (0 malformed lines, TOMBSTONE_REPAIR present). Only `p3-amend-stt-commit-title`
was real, and it was half-resolved + F13-gated. Evidence: eureka
`E-front-of-queue-already-done-20261022` and
`AAA/instructions/DECISION-RECORD-status-is-not-evidence-20261022.md`.

Three laws fall out of the prime law:

1. **Status is not Evidence.** A row may only carry `COMPLETED` with the probe receipt that closed
   it (command + output + utc), inline. No receipt -> the row stays open.
2. **Re-derive, never carry.** On every compile, each row's status is re-measured or explicitly
   marked `CARRIED (unmeasured, from <source>)`. Silence reads as measurement -- do not let it.
3. **Ticket count is not problem count.** N tickets may hide M roots. Compress before you count:
   `One root -> four symptoms` beats `114 open`. The queue is a *map of work*, not the work.

Corollaries already proved in this federation: representation is not reality; present tense is a
claim not a status; a verifier that regenerates its own input destroys what it judges (2026-10-22,
verify_task.py `materialize()` clobber); ghost capability and phantom absence are the same defect
with the sign flipped.

**Sharper probe (from the same day):** when a status field disagrees with a live probe, neither is
automatically right -- the *probe instrument* is also a candidate. Trace it: was the heartbeat
reading the canonical file? `seal_chain.jsonl` silent 172h while `SEALED_EVENTS.jsonl` was being
written the same hour -- the "silence" was a wrong-file probe, and the true root was a downstream
seal-path defect (`arif_seal` output-schema `-32602`, `tools.py:29233-29251`). **A wrong gauge and
a dead engine report the same number.**

## Rule 3o — tasks.json is a concurrent store; lock + diff IDs (NEW 2026-10-23)

`tasks.json` can be appended by a sibling between your backup and your write. In this
compile, a sibling added 11 rows after the 12:57Z backup; a naive read-modify-write would
have reported 135 rows and hidden them. Use `fcntl.flock` on `/root/work/.tasks.lock`,
diff the current ID set against the pre-write backup, label new rows
`SIBLING_APPENDED_UNMEASURED`, and recompute counts from `len(tasks)` after the diff.
Never claim a sibling's row as measured; never drop it.

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
> **I will not carry a status I did not probe. Status is not evidence.**
> **Lebih arif, lebih bijaksana, atau tidak sama sekali.**

**NEW — 2026-10-23 (the seal gauge has two clocks):** `seal_chain_head.last_anchor_utc` and `latest_commit` are **bookkeeping anchors**, not seal entries. `hours_since_last_seal` must be measured from the last **seq-bearing SEAL** row in `seal_chain.jsonl`. Live case: head declared seq 72 / canonical 72 + historical 274 = 346 vs 274 file lines, while the chain tail was seq 55 @ 2026-10-15T09:48:35Z = 195.1h; `last_anchor_utc` was 7.3h. Reporting the anchor as "seal silence" is a wrong-gauge claim. State both clocks and the chain-tail seq, or mark chain integrity UNVERIFIED.

## Rule 3p — A control tested by text-grep or container membership is not a control (NEW 2026-10-26)

Two green-test/dead-control instances in one day, both caught only by independent
mutation testing: (1) an F11 credential mask placed one hop before the wire —
16 unit tests green while the live response carried the raw token (the attacher
ran AFTER the mask); (2) an F8 producer gated on `if "F8" not in resolved_floors`
where the dict is pre-filled for every floor upstream — guard permanently False,
producer dead code, and its "wiring test" was a grep asserting the BROKEN guard
string, so a correct fix would have failed the test.

```
LAW: a wiring/control test must execute the REAL assembler (the actual payload
builder, the actual terminal closure) and be mutation-tested in BOTH directions:
remove the control -> the test MUST die; restore it -> the test MUST pass.
A test that survives removal of the thing it guards is ceremony.
Corollary (status-is-not-evidence, control edition): guard on provenance/state
the upstream actually mutates, never on membership in a container you don't own.
```
Evidence: eureka E-membership-guard-dead-producer-20261026; commits 59d55d3bb
(dead) -> 6d8a219dc (fixed, 555 mutation-proven both directions).

## Rule 3q — Safe task traversal, CWD sensitivity, & TCP stream exhaustion (NEW 2026-10-27)

Three operational hazards observed in live sessions:
1. **Task property type guard:** tasks.json entries may contain null/missing title or non-string values. Any audit or compiler script filtering by string matching must use str(t.get("title") or "") before indexing/lowercasing to avoid TypeError.
2. **Validator execution CWD:** Organ validation scripts (such as AAA/scripts/validate-aaa.mjs) use relative file paths anchored to repo root (readFile("registries/agents.yaml")). Running them from /root causes ENOENT. Always execute inside the repo tree (cd /root/<repo> && node ...).
3. **TCP streaming buffer exhaustion (Edge OS-1):** In raw TCP/HTTP bridge ingestors (such as arifFlow/src/main.rs), a single socket read() cannot be assumed to yield the entire payload. Ingestors MUST loop over Content-Length until the full body is buffered, or JSON-RPC payloads truncate under load.


## Rule 3r — NEVER TRUST A NAME WITHOUT TRACING ITS BINDING *AND ITS BEARER* (NEW 2026-10-28)

> **Provenance:** derived from ARIF's 2026-10-28 reading of the night's audit and applied on his
> instruction ("ya buatlah sampai setel"). Every case below was probed live in the same session;
> each names the file, the field, and the measured value. Staged source (kept for audit):
> `/root/forge_work/patches/bijaksana-compile-rules-3rst-20261028/STAGED-SKILL-PATCH.md`.
> Placed at file tail, after Rules 3p/3q, to match how 3p and 3q were added — not before
> `## Workflow (canonical)` as the staging doc first proposed, because inserting mid-file would
> put 3r between 3o and 3p and break monotonic rule order.

A name is a claim that a binding exists. Audit the binding, then audit who pays when the name
is wrong. Four probes, and the finding must name which one failed:

```
1. BINDING TO A VALUE    — does the name point at ONE measurable thing?
                           (aggregate vs raw member, measurement_id vs scalar)
2. BINDING TO A SET      — does the label resolve to ONE closed vocabulary?
                           (status tokens, verdict tokens, actor spellings)
3. BINDING TO A PATH     — does a live caller actually consume it?
                           (object exists, schema slot exists, caller exists — all three)
4. BINDING TO A BEARER   — is the party who absorbs the error named, authenticated,
                           and able to refuse BEFORE the act?
```

If a name fails any probe, the correct sentence is *"this name is unbound at layer N"* — never
*"this capability is missing"* and never *"this metric is X"*. A name that passes 1-3 but fails
4 is the most dangerous shape: it looks fully engineered and charges the cost to someone who
never agreed.

### Tell 3r.1 — an aggregate that equals one member
When a federation-wide number collapses, probe for ONE actor before believing a systemic
failure. arifFlow `federation_fq_aggregate` (`src/governance/invariants.rs:611`) gates the
aggregate to `min_i(FQ_i)` whenever any active actor drops below 0.50.

Live case: `arifos:claude/opus-5.5` at 7 execute / 1 verify ⇒ q = 0.1428 = 1/7 ⇒
whole-federation FQ printed 0.1428, constitutional floor **F1** failed, kernel `degraded` —
while `raw_pool_quotient` in the same payload was **1.39–1.64** (it moves; the gated number
does not).

```
TELL: aggregate == a simple 1/n for integer n  -> find the actor with n executes, 1 verify.
TELL: aggregate << raw_pool_quotient          -> the min-gate fired; the gap IS the finding.
TELL: decomposition.raw == value while a gate exists
      -> the payload labels the GATED number as "raw". Worst case: normalization:"NONE".
```

That third tell is the real one. The operation is not hidden by omission — it is hidden by a
label that contradicts it:
`{"raw": 0.142857…, "normalization": "NONE_PASSTHROUGH_QUOTIENT"}` on a value that has been
min-gated. A reader who trusts the field name concludes "no transform happened". The transform
is the finding. **Provenance means naming the operation, not printing its output.**

Rule: never report a min-gated aggregate as a health measurement without naming the gating
actor; and an Unclassified / short-window actor must not be able to redden a constitutional
floor — classify it or exclude it, never let a probe class vote.

### Tell 3r.2 — a label with an open vocabulary
`STATUS IS NOT EVIDENCE` (3n) tells you to re-probe rows. It does not help when the vocabulary
is open-ended: 311 rows carrying **78 distinct status tokens** (99 `CARRIED_UNMEASURED`, 50
`OPEN`, 27 `OPEN_MEASURED`, 22 `COMPLETED`, dozens of singletons such as
`PARTIAL_KX004_RESOLVED_KX002_ACTIVE`) cannot be counted at all.

```
Before any open/closed count:  len({row["status"] for row in tasks})
If tokens > ~12, the count is a guess. Report the token count as the headline finding.
```

**Count, don't narrate — the compiler is not exempt.** In the pass this rule came from, the
task row describing the sprawl was *itself* created with a hand-typed "85 tokens" that no
`len()` had produced; measured value 78. Every N in a task title or body must come from a
`len()` in the same process, or carry `CARRIED (unmeasured)`. The catch only happened because
3c already required `len()` — the gate caught the compiler, not the compiler's honesty.
**Promote the gate, not the confession**: a finding that depends on an individual admitting
error has survival ≈ 0; a finding enforced by a mechanical check survives a change of author.

### Tell 3r.3 — a concept with vocabulary but no caller
A control can be **half-built in several places and called from none**, which looks identical
to not existing if you only grep the concept. Probe three layers separately:

```
1. vocabulary — does the word appear at all?     grep -rn <concept> --include=*.py
2. object     — is there a typed slot/schema?    inspect the TOOL SCHEMA, not the docs
3. caller     — does the LIVE path invoke it?    grep the EXECUTOR, not the author
```

Live case (refusal): vocabulary in 12 kernel files (`three_locks.py` defines
`HOLD_TYPE_F13_REFUSAL`, `rights_registry.py` defines `RIGHT_TO_REFUSE_PROFILING`), an
executable wrapper on disk with a 12/12 self-proof, and **zero callers at every layer** —
including a judge whose input schema had no refusal field at all. Correct finding: *N partial
implementations, no consumer* — strictly worse than nothing, because both look like safety.

Corollary: **whoever builds the gate must not be whoever it gates.** If the agent that wants to
act also wires and checks the gate, requester == issuer and the control is ceremony. Name the
non-author executor hop explicitly, or do not claim the control is installed.

### Tell 3r.4 — a bearer recorded but not standing
The strongest failure is a name that carries a *bearer field* and no *bearer capability*.

Live cases measured 2026-10-28:

| Surface | Bearer field | Bearer capability | Verdict |
|---|---|---|---|
| `refusal_store.issue()` | `bearer_id` required, free text | `signature` **optional** | a NO attributed to a human is forgeable by anyone who can write the file |
| VAULT999 `outcomes.jsonl` (3,220 rows) | **0 rows** name a payer (`affected_humans`/`bearer`/`consent` all absent) | none | 70 rows assert `harm_detected: true` with no field naming the harmed party |
| `arif_judge` schema | no refusal, no bearer, no affected_humans input | none | the judge cannot be told who pays |
| AAA attention page | `fq_source: "live:arifFlow:7073/vector.dimensions.fq"` | `GET /vector` → **HTTP 404** | the provenance pointer names a dead endpoint |

```
RULE: a bearer field is not standing.
Standing requires: (i) an identity that can be authenticated,
                   (ii) a scope that bounds what may be refused,
                   (iii) a persistence guarantee across retry/restart/handoff,
                   (iv) a caller path that consults it before the act.
Missing any of the four ⇒ write "bearer recorded, standing ABSENT".
```

Corollary (the one that costs the most): **a provenance field is itself a claim and must be
probed.** `fq_source` pointing at a 404 is the same defect class as `decomposition.raw` naming
a gated value "raw". Both are true-looking strings that resolve to nothing.

## Rule 3s — A COUNTER THAT DECREMENTS IS A WINDOW; A VERDICT THAT DOES NOT MOVE IS NOT MEASURING (NEW 2026-10-28)

Four tells from one night's probes. Each is a label that survived contact with a changing value.

### Tell 3s.1 — a count that moves DOWN is a window, not a total

`verify_count` read **48** then **47** thirty seconds later while `execute_count` went 43 → 44.
A cumulative total cannot decrement. The instant a "count" goes down you are reading a
**rolling window**, and every ratio built on it has an unknown denominator.

```
TELL: n(t2) < n(t1) on a field named *_count  ->  windowed, not cumulative
TELL: the payload exposes no window/scope      ->  the ratio is uninterpretable, say so
```

FI-002 first called this a *dead counter*. It was not — it was live and windowed. **A metric that
moves is not thereby meaningful; movement proves the writer exists, not that the scope is known.**

### Tell 3s.2 — discrimination test: change the input, watch the verdict

```
quotient 0.1667  ->  verdict OPTIMAL / BALANCED
quotient 0.4667  ->  verdict OPTIMAL / BALANCED      (x2.8 in 30s, label unchanged)
```

A verdict that yields the same token across a 2.8× change in its own input is either not a
function of that input, or its thresholds are too wide to discriminate. Either way the token
carries no information and must not be quoted as a health measurement.

```
TEST before quoting any verdict token: sample it twice, move the input, re-read.
Invariant token across a material input change -> "does not discriminate", not "stable".
```

### Tell 3s.3 — a provenance label that contradicts its own origin string

```
kernel.floor_measurement = "measured"
kernel.failing[0]        = {floor:"F1", score:0.0,
                            origin:"arifflow_probe:quotient=0.1667;floor=0.5;
                                    constellation=SIMULATION@2026-10-27T20:39:59Z"}
```

The word *measured* sat beside an origin naming a **simulation**. This is Rule 3r.4's corollary
(a provenance field is itself a claim) with a precise tell: **read the origin, not the class.**
`SIMULATION` / `ESTIMATED` / `MOCK` inside an origin string demotes any `measurement:"measured"`,
`provenance_class:"SERVER_OBSERVED"` or `state:"live"` on the same object.

### Tell 3s.4 — write-reachability is not read-wiring

Three carry-forward stores exist, three inodes (`80494`, `5274483`, `1595648`). FI-002 wrote a
decision into `/root/memory/carry_forward.json` (87 KB, schema `recent_decisions`) and reported
"every agent inherits". The **canonical** store is
`/root/.local/share/arifos/carry_forward.json` (329 KB, schema `entries`) whose
`recent_decisions = 0` and whose actor list contains no `claude-code-kvm8` row — the work was
never there. Reader probe: `scripts/witness-heartbeat.sh` reads the canonical one only.

```
TEST before claiming inheritance: name the reader. grep for the PATH, not the concept.
No caller found -> "written, unread" is the only true sentence.
A file you can write to is not a file anyone opens.
```
trc-skill-align-20261028T135921Z
## Rule 3t — INDEPENDENCE IS A FUNCTION OF STATE; A DISPATCH THAT DIES IS NOT A LESSON THAT DIES (NEW 2026-10-28)

> Provenance: derived live in the GEOX Phase 1 session (333-AGI, branch ccdbb491, arif_judge trace trc-600aa066a6ff). Both findings probed the same turn.

### Tell 3t.1 - Goedel separation holds at primary, collapses at cascade

Role separation (builder/verifier/judge) audited by reading only primary models:
333=forge-777, 555=glm-5.3-flash, 888=MiniMax-M3 - three families, conclusion "independent".
The fallback rungs tell the opposite story:

```
333 chain: forge-777 -> deepseek-v4-pro -> MiniMax-M3   <- fb#2 == 888's P1
888 chain: MiniMax-M3 (P1) -> glm-5.3-flash (P4) -> deepseek-flash (P8)
555 chain: glm-5.3-flash (head)                          <- head == 888's P4
```

LAW: audit independence across FULL chains (primary + every fallback), never primaries alone.
Independence that exists only when nothing is broken is not independence - degradation is exactly
when you need the judge to be someone else. Falsifiable test (no new infra): submit the same
verdict request through a role lane at nominal state and at cascade state; measure verdict
convergence. Convergence under cascade = the separation is decorative.

### Tell 3t.2 - a dispatch that fails to resolve is not permission to drop the lesson

Mid-session, the harness rebuilt its agent/skill tables and dropped 555-ASI from the subagent
map: every later dispatch died with "Agent not found" before executing. The AAA registry
(/root/AAA/agents/555-ASI) was intact - the loss was harness-layer only.

```
RULE: when the author-role agent cannot be dispatched, the work does not wait for the registry.
Complete the correction IN-SESSION, and put the provenance IN THE COMMIT MESSAGE: who authored
the original, who made the correction, why the original author was unavailable, and who still
holds the judge role. Author != approver must survive the outage, not be suspended by it.
```

Corollary: this compile itself was gated mid-session by a review-gate (f1-protected-command,
fail-closed, three times, on protected-path probe strings). The gate's own instruction is the
rule: report the block, do not retry, mark the unreadable store CANNOT_WITNESS - a blocked probe
is a finding about the residue store, not an excuse to carry its status forward.

### Where this rule bites today

- The deploy of GEOX Phase 1 is HOLD because F1 failed - and the F1 provenance string carries
  constellation=SIMULATION beside floor_measurement:"measured" (Tell 3s.3 applied upward:
  the gate's own instrument demotes itself). Owner of that fix: kernel/F13, not the blocked organ.
- The canonical carry_forward store under the arifos state dir was unreadable to this compiler
  (gate-blocked); its residue is therefore CARRIED (unmeasured) throughout this manifest.

### Invariants locked (external review 2026-10-28, Copilot HOLD report)

I2  Global P0 outranks harness-local phase ordering.
I3  A simulated metric cannot silently exercise production authority.
I5  Verification independence includes model-route independence.
I6  Compilation validity ends when its source state changes.
I7  The lane holding a lock must be included in any plan to release it.


<!-- AAA-SKILL-PATCH-3U 2026-10-28 provenance=333-AGI trace=trc-skill-align-20261028T135921Z -->


## Rule 3u — A MUTATION CYCLE THAT SAYS NO_EFFECT AFTER A SCRIPT THAT PRINTED SUCCESS HAS REVERTED YOUR WRITE (NEW 2026-10-28)

Live case (same session as 3t): a multi-file patch ran inside a canon cycle. The script
printed "PATCHED: <file> <bytes>" for all four targets; the cycle exited rc=0 with
`effect=NO_EFFECT` — and a post-cycle grep found the marker in ZERO files. The cycle
rolled the tree back when its expectation could not be classified. The single-file
variant of the same patch (`canon-mutate file`, no expectation flags) persisted with
`effect=CHANGED pre=10103 post=10850`.

```
LAW: verify the ARTIFACT after every gated mutation — grep the marker in the file,
count the bytes — never trust the mutation script's own stdout. A gate that restores
state on an unmet expectation reports rc=0, not an error; rc=0 + NO_EFFECT = reverted.
Corollary: prefer many single-file cycles with measured effect=CHANGED over one
multi-file tree cycle whose expectation you cannot state precisely.
```

<!-- AAA-SKILL-PATCH 3V 2026-10-28 provenance=333-AGI trace=trc-skill-align-20261028T135921Z -->

## Rule 3v — A CLASSIFICATION THAT TURNS A FLOOR GREEN IS A GOVERNANCE ACT, NOT A FIXTURE TAG (NEW 2026-10-28)

Live case: cockpit showed 20 machine-held actors + kernel FAIL (F1). The proposed fix listed
12 actors for the synthetic class - including kimi-code/fi-008 (an F13-ratified human_agent
in entity_classes.yaml), wealth-mcp (a live organ), claude/opus-5.5 (a real model lane), and
work by a named human. Relabeling those would turn F1 green while their verify deficit
stayed real: gauge edited, meter untouched.

LAW: synthetic is for no-reality artifacts (probes, test rows, self-check receipts) with
per-entry fixture evidence - the config file itself models this with dated session-cited
entries. A real agent, organ, human, or the sovereign is NEVER synthetic. If a real actor's
missing verification reddens a floor, the fix is receipts or a ratified verify-native role
exemption (invariants.rs option C, F13 2026-10-26) - never a relabel. And before writing
ANY class entry, diff the classifier KEY against the keys actually recorded: on 2026-10-28
the human_agent list declared kimi-code/FI-008 while the live key was arifos:kimi-code/fi-008
- a correct declaration made INERT by a prefix/case mismatch.

<!-- AAA-SKILL-PATCH 3W 2026-10-28 provenance=333-AGI trace=trc-skill-align-20261028T135921Z-3w -->


## Rule 3w — A MARKER-PRESENCE CHECK PASSES ON A CORRUPTED ARTIFACT; VERIFY LINE COUNT AND BYTE DELTA (NEW 2026-10-28)

Live case (my own defect, found by reading the served file instead of trusting the check): a patch
template was built as `MARK.replace("TRCID", trace)` and the staging step did
`script.replace("TRCID", "")` first - turning it into `MARK.replace("", trace)`. Python's
`str.replace` with an EMPTY old string inserts the replacement BETWEEN EVERY CHARACTER: the marker
exploded into a ~1,000-char garbage line, its literal no longer matched, the "already patched?"
check passed, and the rule was appended TWICE. The verification I ran (`grep` for the marker)
reported 23/23 OK on a corrupted artifact.

```
LAW: a presence check is not an integrity check. After any patch, compare
      line count AND byte delta against the pre-image (you have it - the cycle printed pre/post),
      and assert the count of the new section HEADER (exactly 1), not just the presence of a marker.
Corollary: never build a patch template by replacing a token OUT of a template that later
replaces that token IN - and never trust str.replace with an empty old string; it is an insertion
machine, not a deletion tool.
```

## Rule 3x — A GOVERNED COMMIT WRAPPER THAT COMMITS NOTHING STILL REPORTS SUCCESS; A WINDOW SHIFT INVALIDATES THE COMPARISON (NEW 2026-10-28)

Two traps from one session, both in the compile path itself.

**3x.1 — the wrapper, not the git.** `git-lane <lane> commit` returned a plausible tail
(`no changes added to commit (use "git add" ...)`) and exit 0, while the change stayed UNCOMMITTED.
The push that followed then moved the remote to a DIFFERENT commit (a sibling's), so it LOOKED like a
successful publish. The defect survived until the tree was re-checked afterwards.

    TELL: the commit output mentions "no changes added" / "use git add"  -> NOTHING WAS COMMITTED.
          A commit path that does not stage is a wrapper, not a commit.
    LAW:  after every governed commit, re-derive the truth: git status --porcelain (must be empty for
          the files you touched) AND git rev-parse HEAD (must equal the sha you intended to publish).
          Never treat the wrapper's exit code as the commit's success.

**3x.2 — the window moved, so the numbers are not the same numbers.** The baseline read
`volume_basis 298`; the post-measurement read `volume_basis 160`. A "123 of 298 -> 23 of 160"
comparison is window-confounded and would have been reported as a 96% fall.

    LAW:  a consequence comparison requires the SAME measurement window/population on both sides.
          If the basis moved, report the structural measure (which actors changed class) and label
          the volume comparison CONFOUNDED. A number from a different window is not a smaller number.


## Rule 3y — A KEY NAMED `verdict` IS A VERDICT BY NAME; RENAME THE AXIS, NEVER THE VALUE (NEW 2026-10-28)

Live case (333-AGI, 2026-10-28): `TelemetryMetrics` published ALIVE/PAUSED/DEGRADED — lifecycle tokens —
under a key named `verdict` (`model.py:462`). The verdict walker validates every verdict-bearing key
against CANONICAL_VERDICTS, so EVERY `arif_memory`/`arif_judge` response tripped
`UNKNOWN_VERDICT_TOKEN → INCONSISTENT_STATE → HOLD`. The kernel had already fixed the identical class on
the metabolic axis (`fq_gate.py` renamed `verdict` → `fq_outcome`) and was missing it on telemetry.

```
LAW: before diagnosing a HOLD as substantive, DECODE hold_reason. If it names
UNKNOWN_VERDICT_TOKEN:<path>=<token>, the defect is the KEY NAME at <path> — not the value,
not the floor. Fix the key: rename the axis (lifecycle / fq_outcome), keep the values,
then re-probe: hold_reason must move to a substantive code (NEEDS_REVIEW etc.).
Check the OTHER axes before assuming one instance is the whole class.
```

Evidence: arifOS commits fa1f2e694 + 7599f1c42, deploy epoch 25 PASS, live probe
`telemetry={"lifecycle":"ALIVE"}` with no `verdict` key inside it; receipt
`/root/forge_work/receipts/RECEIPT-arifos-verdict-token-leak-2026-10-28.md`.

## Rule 3z — A GATE THAT READS A FIELD THE REAL PAYLOAD DOES NOT CARRY IS AN OFF GATE WITH A GREEN LIGHT (NEW 2026-10-29)

> Provenance: 333-AGI session SEAL-15b5c286c6d845a8, receipt /root/forge_work/receipts/RECEIPT-agentic-gate-stop-chokepoint-2026-10-29.md, arifFlow 251f3cca. Live case: `aaa-completion-check.sh` read `.response // .message` from Stop payloads that carry `session_id/cwd/hook_event_name/stop_hook_active` only — exited 0 on every production turn for 28 days; telemetry held 14 rows from 5 synthetic sessions, zero real `session_*` ids (E-inert-gate-payload-field-20261029).

```
LAW: before trusting any gate/hook, enumerate the fields it READS and cross-check
     against the fields the REAL invocation payload carries (grep a sibling handler
     that demonstrably fires, or one live captured payload). Then count the gate's
     own telemetry by REAL ids over a window — synthetic-only rows = inert sensor.
Two companion traps hit in the same session:
  - jq '.x // true' substitutes on null AND false: a deliberate false becomes true.
    Read booleans raw (`jq -r '.x'`) and default in shell; never default a boolean
    on the right side of jq //.
  - A telemetry verdict must match the action actually taken (a "BLOCK" row on a
    turn the hook allowed is a lying gauge); derive the label from the decision.
Corollary (control edition of 3n): audit gates by their real-source row counts over
time, not by reading their logic. Code that looks right and fires never is theatre.
```

## Rule 3aa — A HASH BOUND TO A ROW MUST NAME ITS CONVENTION (NEW 2026-10-29)

> Provenance: 333-AGI session SEAL-5dca4362dd044601, first live RSI review row. The evidence
> bundle hashed the original ledger row newline-INCLUSIVE (`sed -n 2p | sha256sum`); the
> appender pins newline-EXCLUSIVE (`splitlines()`). The L7 gate refused the first bridge
> attempt with REFUSED_ORIGINAL_HASH_MISMATCH — correct behavior, wasted bridge window,
> and a refusal receipt that had to be disclosed.

```
LAW: whenever a receipt, envelope, or bundle binds a hash to a FILE ROW (JSONL line,
     log line), name the convention beside the hash: "newline-exclusive (splitlines)"
     or "newline-inclusive (raw line + \n)". Two correct hashes of the same row under
     different conventions mismatch, and the mismatch reads as tampering when it is
     only terminology. The binding artifact must state which bytes it hashed.
Corollary: when a hash-bound append is refused for mismatch, re-derive the hash under
     the OTHER convention before investigating tampering — the convention gap is the
     cheap explanation and it is checkable in one command.
```

Evidence: receipt /root/forge_work/receipts/RECEIPT-rsi-first-review-row-2026-10-29.md
disclosure 1; refusal receipt /var/lib/arifos/rsi_review_receipts/rev-47afb9f8-8ee6-49c9-b1c6-e5ec44c613e4.json.
