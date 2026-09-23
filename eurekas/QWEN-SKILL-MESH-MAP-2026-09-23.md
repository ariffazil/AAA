# Qwen Skill Mesh — Verified Map + Entropy Plan

> **Date:** 2026-09-23 ~07:50 MYT · **Actor:** FI-003 (Qwen Code) · **Mode:** OBSERVE + plan
> **Lane:** `skill-mesh` FLOW — Step 0 (Gate) partial · Step 2 (inventory) done · Step 4/5 (audit/taxonomy) plan
> **Prior input:** a pasted agent report was received and is treated as UNVERIFIED stdout.
> Every number below carries the command that produced it. Corrections to that report are in §4.

## 1. Topology (the structural fact the prior report missed)

| Root | Reality | Command |
|---|---|---|
| `/root/AAA/skills` | canonical store (real dir) | `readlink -f` |
| `/root/.claude/skills` | **symlink → `/root/AAA/skills`** | `readlink -f /root/.claude/skills` |
| `/root/.agents/skills` | **symlink → `/root/AAA/skills`** | `readlink -f /root/.agents/skills` |
| `/root/.hermes/skills` | separate real dir (view tree) | `readlink -f` |
| `/root/.qwen/skills` | separate real dir (harness overlay), 24 entries | `ls -1 \| wc -l` |

Consequence: listing Qwen skills "in `/root/.claude/skills`" and again "in `/root/.agents/skills`"
counts **the same inodes three times**. All figures below are deduped by `realpath`.

## 2. Verified Qwen map — 28 unique physical `SKILL.md`

Command: `find` over 5 roots, path matched `-ipath '*qwen*'`, deduped by `os.path.realpath`,
frontmatter `name:` parsed from each body.

**Canonical root-level (12)** — `/root/AAA/skills/`
`AAA-voice-cloning-qwen-cloud` 9717 · `fi-qwen-upgrade` 1754 · `qwen-harness-tools` 3506 ·
`qwencloud-deploy` 5717 · `qwencloud-image-generation` 23925 · `qwencloud-model-selector` 15068 ·
`qwencloud-ops-auth` 11343 · `qwencloud-text` 20240 · `qwencloud-update-check` 2035 ·
`qwencloud-usage` 12382 · `qwencloud-video-generation` 20349 · `qwencloud-vision` 19428

**Workshop (3)** — `domains/general/workshop/qwencloud/`
`qwen-token-plan-team-edition` 11711 · `qwencloud-cli` 4430 · `qwencloud-mesh` 11732

**Alias (1)** — `/root/AAA/skills/qwen-meta-mesa` → symlink → `meta-mesa`
routing `name: meta-mesa`, body **13,401 bytes**. Not a phantom (see §4.2).

**Harness overlay local** — `/root/.qwen/skills/` (24 entries: 9 dirs w/ `SKILL.md`, 16 symlinks
incl. `aaa-canonical → /root/AAA/skills`). Only 2 are qwen-pathed, and they are a duplicate pair.

**Archive copies still carrying live routing names (4)** — under `.archive/`:
`fi-qwen-upgrade` ×2 (1699 B, sha `14f749ef…`) · `AAA-voice-cloning-qwen-cloud` ×2 (9661 B).

## 3. Sanctioned census

Command: `python3 /root/scripts/skills-census.py` (the only sanctioned counter — rule 7)

```
total_skills_on_disk 565 · canonical 773 · viewed 725 · profile 298 · overlay 164
whole_mesh 729 · loadable 711 · shells 4 · symlink_dependents 699
duplicate_identity_groups 26 · duplicate_identity_skills 49
broken_symlinks 0   (STOP CONDITION 2 — met)
total_diverged 0 · overlay qwen: '769 view + 29 local' · VERDICT: WARN
```

**Instrument-vs-disk drift (UNRECONCILED):** census reports qwen overlay `29 local`;
`ls -1 /root/.qwen/skills` = 24 entries and `find /root/.qwen/skills -name SKILL.md` = 9.
Both commands recorded; neither is adopted. → `skill-drift` §1 row.

## 4. Corrections to the pasted report

**4.1 Coupling is 59, not ~22.**
Command: `find /root/AAA/skills -name SKILL.md -not -ipath '*qwen*' -not -path '*.archive*'`
× `grep -qiE '\bqwen[0-9-]|qwen-vl|qwen-tts|dashscope|tongyi|wan2'` → **59 unique skills**.
The prior figure undercounted by ~2.7×. Any plan sized on "~22 routers" is undersized.

**4.2 `qwen-meta-mesa` is NOT a phantom — the prior plan's Step 1 was built on a false diagnosis.**
It is an alias symlink → `meta-mesa`, body **13,401 B**, live. The prior report almost certainly
read `find <dir> -type f` (which does not follow symlinks) and concluded "no body, no scripts".
Archiving it on that diagnosis would have retired a live capability — the exact failure
`skill-mesh` names ("Never evict on appearance").

**4.3 `/root/.claude/skills` is not a second surface.** It is a symlink to the canonical store.

**4.4 Pricing/quota scatter is 8 Qwen-relevant files across 5 skills, not "5 places":**
`qwencloud-model-selector/references/{model-list,pricing,pricing-disclaimer,recommendation-matrix}.md` ·
`qwencloud/qwen-token-plan-team-edition/references/seat-quota-snapshot.md` ·
`qwencloud/qwencloud-mesh/references/quota-snapshot.md` ·
`domains/general/forge/model-routing/tokenrouter-guide/references/qwen-token-plan-seat-wiring.md` ·
`workshop/image-gen/image-identity-transfer/references/2026-08-28-dashscope-quota-and-mcp-fallback.md`

**4.5 `fi-zai-probe` is not a Qwen skill** — Z.AI GLM is a different vendor. Wrong bucket.

**4.6 MISSED: a real LIVE routing collision.** `/root/.qwen/skills/youtube-extraction-datacenter-ip/`
holds a nested copy at `…/youtube-extraction-datacenter-ip/SKILL.md`. Both bodies
`sha256 dab7962801845ece…` — **identical**, same `name:`. This is `MIRROR_DRIFT`, not
`DUPLICATE_OWNER` (hashes match), so it is a mechanical re-sync (skill-mesh C-7) — no F13 needed.

**4.7 MISSED: `.archive` inside the scanned store carries colliding routing names.**
`fi-qwen-upgrade` ×3, `AAA-voice-cloning-qwen-cloud` ×3, plus a library-wide 26 groups / 49 skills
measured by census (which itself EXCLs `.archive`, so it under-reports this surface).

## 5. UNKNOWNs — these block closure

- **GATE 0 OPEN.** Which byte-exact body the loader serves for `fi-qwen-upgrade` is **UNKNOWN**.
  All three bodies contain every probe string tried (`Atomic-Swap Upgrade`,
  `proven 2026-08-14/18/21`, `Never delete the \`.old\` tree same-day`), so content cannot
  discriminate. Inferred (not proven): loader skips dot-dirs, so `.archive` is not offered —
  the session listed `fi-qwen-upgrade` once with no ambiguity error. Requires
  `references/skill-library-integrity.md` §1 `scripts/skill_resolution_audit.py`.
- Whether the 59 coupled skills each carry their *own* Qwen fallback path (**prior claim of
  "six routers" is UNVERIFIED** — only the names were confirmed to exist).
- Whether the three "which Qwen model" skills (`qwen-harness-tools`,
  `qwencloud-model-selector`, `tokenrouter-guide`) actually overlap in *content* — not yet diffed.

## 5b. GATE 0 RESULT (run 07:55–07:58 MYT) — **FAIL**

Command: `python3 /root/AAA/skills/skill-mesh/scripts/skill_resolution_audit.py --root /root/AAA/skills --root /root/.qwen/skills --root /root/.hermes/skills`
→ **`EXIT=1`** · 584 with `SKILL.md` · **6 UNRESOLVABLE** · **29 basename≠`name:`** (two consecutive runs identical → sensor stable; the earlier count of 7 differed because the *tree* moved, not the sensor).

**The 6, classified by hash (skill-mesh C-7):**

| Name | Pair | sha | Class | Disposition |
|---|---|---|---|---|
| `claude` | AAA vs `.hermes` `apex_verdict_hold/` | identical `09cd895b` | MIRROR_DRIFT | mechanical (P1) |
| `hermes` | AAA vs `.hermes` `apex_verdict_hold/` | identical `a00751a6` | MIRROR_DRIFT | mechanical (P1) |
| `google-workspace-gws` | `.qwen` vs AAA | **DIVERGED** `f32515c3` vs `227e5b60` | DUPLICATE_OWNER | **HOLD for human** |
| `human-state-estimation` | `.qwen` vs AAA | **DIVERGED** `ea894fcc` vs `e5e82ac0` | DUPLICATE_OWNER | **HOLD for human** |
| `malaysia-reality-interface` | `.qwen` vs AAA | **DIVERGED** `766f43f6` vs `fd655791` | DUPLICATE_OWNER | **HOLD for human** |
| `organ-capability-map` | `.qwen` vs AAA | **DIVERGED** `f31acf76` vs `f5225a8c` | DUPLICATE_OWNER | **HOLD for human** |

**Which body the loader serves remains UNKNOWN.** `get_scan_ordered_skills_dirs` does not exist in
the 0.24.3 chunks (`getScanOrdered|scanOrdered|skillsDirs|externalDirs` → no hits), so the documented
replication procedure for rule 11 cannot be run. The live index lists each of these names **once**,
which is consistent with first-wins *and* with only-one-being-scanned — it does not discriminate.

**The 29 mismatches are mostly case-only** (`forge-*` vs `FORGE-*`, `agi-*` vs `AGI-*`). Since
`skill-mesh` rule 10 makes frontmatter `name:` the routing identity with folder as fallback, and all
these skills appear under their declared name in the live index, this class is **probably benign** and
must NOT be mass-renamed on the script's own advice without confirming the loader keys on the folder.

**The gate script cannot see `.archive`** — line 56 prunes any dir starting with `.`/`backup`/`archive`.
So the `fi-qwen-upgrade` ×3 and `AAA-voice-cloning-qwen-cloud` ×3 collisions are **outside this
instrument's scope by construction**, and are still present (live `0d194f79` vs archive `14f749ef` —
diverged, not mirror). A sensor that cannot see a known defect is the "decoration" failure (rule 12).

## 5c. CONCURRENCY HOLD (decisive — no mutation executed)

A second lane was writing this tree throughout the run:

- `/root/AAA/proposals/skill_resolution_audit_receipt_2026-09-23.txt` 07:54:44
- `..._qwen_receipt_...` 07:54:50 · `..._post_archive_receipt_...` **07:56:15**
- `alias_namefield_mapping_v2/v3/v4.py` 07:43–07:45 · `apply_retarget.py` 07:47
- `ALIAS-RERESOLVE-MAPPING{,-v2,-v3,-FINAL}-20260923.json` 07:42–07:45
- **`qwencloud-model-selector/references/qwen-sot.md` created — this is plan Step 6, already built by them**
- `qwencloud-model-selector/references/model-list.md` modified — plan Step 3, in flight

Evidence the tree moved mid-audit: `…/youtube-extraction-datacenter-ip/youtube-extraction-datacenter-ip/`
existed at 07:52 (identical sha `dab79628`) and was **gone by 07:57** — plan **Step 1 executed by the
other lane**, unresolvable count 7 → 6.

Per `skill-mesh` PITFALLS: *"Hold a repair when a second session is writing the same tree. 'Authorized
but racy' and 'not authorized' are different verdicts."* → **Steps 1 and 3–6 are taken; Step 2 and all
mutation are HELD, not skipped.** Census moved with their work: `duplicate_identity_groups` 26 → **25**,
`duplicate_identity_skills` 49 → **47**, `broken_symlinks` **0**.

## 6. Plan (revised — Lane B reversible first, F13 only on freeze)

| # | Action | Lane | Gate |
|---|---|---|---|
| 0 | Run `skill_resolution_audit.py` — close Gate 0 for the 3 colliding names | B | none |
| 1 | **Delete-free dedupe** of the nested `youtube-extraction-datacenter-ip` copy → `.archive/`, verify loader offers one | B | hashes already identical |
| 2 | Move `.archive/` routing-name collisions **out of every scanned root** (binding per C-2), then re-verify loader does not offer them | B | none |
| 3 | Promote `qwencloud-model-selector/references/model-list.md` → single SOT (`sot: qwen-model-list`); re-point `qwen-harness-tools`, `tokenrouter-guide` seat-wiring, `qwencloud-usage`; stamp the other 4 `superseded-by:` | B | reversible |
| 4 | Workshop trio stays as **adapters** (team-seat quota / CLI shim / mesh transport), cross-linked to root skills — they own wiring the root skills do not | B | reversible |
| 5 | Verify the coupling set (59) before naming one canonical Qwen-image router; **do not pick a winner from names alone** | B | evidence first |
| 6 | Write `references/qwen-sot.md` — canonical model IDs + last-changed date, the 5 wired surfaces (`fi-zai-probe`) and which skill owns each | B | reversible |
| 7 | `chattr +i` freeze on **meta only** (SOT + router + archive markers), bodies stay warm | **A — F13 binary** | escalate |

**Do NOT execute unattended:** skill-mesh ESCALATE rule — a merge of unknown-authoring skills, or
moving where the catalog *is*, is F13-class. Steps 1–6 produce artifacts; Step 7 needs the go/no-go.

## 5d. SOVEREIGN DECISION + EXECUTION (08:09–08:11 MYT)

Sovereign reply to the single binary: **`ikut aaa`** → canonical `/root/AAA/skills` is truth.

**Preconditions checked before mutating** (concurrency released, no silent content loss):
- Lane-2 quiet: no writes under `/root/AAA/skills` or `/root/.qwen/skills` in 10 min except
  `.learning/cron.log`; no `alias|retarget|reresolve` process alive. → HOLD released.
- Diffed all 4 diverged pairs: canonical is **newer + larger** and carries governance fields
  (`capability_tier`, `ecology_state`); overlay is older but carries **trigger phrases canonical
  lacks**. Per rule 4 (*"a merge must not lose discovery — carry every trigger phrase from every
  source"*) those were **folded into canonical first**, then repointed. `count(old)==1` asserted.

| Fold | +chars | desc_len after | YAML |
|---|---|---|---|
| `google-workspace-gws` | +124 | 265 | OK |
| `human-state-estimation` | +214 | 373 | OK |
| `malaysia-reality-interface` | +193 | 366 | OK |
| `organ-capability-map` | +121 | 301 | OK |

Note: `human-state-estimation` was the one the loader was **actually serving from the overlay**
(live index showed its long description), so folding it was load-bearing — repointing alone would
have silently degraded a live skill.

**Which body the loader served, read off this session's own live index (closes rule 11 empirically):**
served **canonical** for `google-workspace-gws`, `malaysia-reality-interface`, `organ-capability-map`;
served **overlay** for `human-state-estimation`. First-wins is therefore *not* uniform across names.

**Mutation (archive-then-repoint, never delete):**
- 4 overlay dirs → `/root/.qwen/skills-retired/2026-09-23-ikut-aaa/<n>/` + symlink → canonical.
- 2 `apex_verdict_hold/{claude,hermes}` (sha **identical** `09cd895b`/`a00751a6`, zero-loss P1) →
  same treatment toward `/root/AAA/skills/...`.
- Ledger: `/root/.qwen/skills-retired/ROLLBACK-MANIFEST.jsonl` — **10 lines**, accumulating.
- Rollback bodies: **6 × `SKILL.md` present** (`test -f`-verified, not merely cited).

## 5e. STOP CONDITION — measured after, same arguments

| Check | Before | After |
|---|---|---|
| `UNRESOLVABLE (name → >1 distinct file)` | **6** | **0** ✅ |
| `broken_symlinks` (census) | 0 | **0** ✅ |
| `total_diverged` | 0 | 0 ✅ |
| `duplicate_identity_groups` | 26 → 25 | **21** |
| `duplicate_identity_skills` | 49 → 47 | **43** |
| `DIR-BASENAME vs name:` mismatch | 29 | **27** |
| census `VERDICT` | WARN | WARN |
| gate `EXIT` | 1 | **1** |

All 6 repoints: `link=Y body=Y`. `total_skills_on_disk` 565 unchanged.

## 5f. `tutup baki` — the three evidence questions, closed (08:12–08:15 MYT)

### (1) The 27 basename mismatches → **CLOSED, benign — my own prior risk framing was wrong**

Test: does any mismatched dir rely on its folder as the routing key?

- **0 / 27** lack a frontmatter `name:` → folder is only ever the *fallback* (rule 10), never the key here.
- **No two** mismatched dirs share a frontmatter `name:` → no collision of the class the script warns about.
- `UNRESOLVABLE = 0`, and this session's live index serves them under their **frontmatter** names
  (`FORGE-cross-agent-handoff`, `AGI-decisions-reflect`, `AAA-OCR-optical-compression`, …).
- 15/27 differ by case only; 12 are substantive (`dir 'text-to-speech' → name 'token-plan-tts'`,
  `dir 'xauusd-trading' → name 'XAUUSD-trading-stack'`, `dir 'claude' → name 'arifOS ACT — Constitutional Reflex'`).

→ These are **cosmetic debt, not unreachable capability**. Reclassify `FAIL → INFO` (rule 13 ladder).
The gate's `EXIT=1` conflates a hard defect (ambiguous name, now 0) with a cosmetic one
(folder≠name) under a single code — that is the sensor defect, not the folders.

### (2) `.archive` → **CLOSED, no defect — and my earlier "blind sensor" claim was WRONG**

I previously asserted the gate was "decoration" for not seeing `.archive`. **That was false.**

Method (corrected): computed frontmatter names present *only* under `.archive` (no live body in any
of the 5 skill roots) → **120 names**, then compared each against this session's own live index.

- Archive-only names **absent** from the live index: `airtable`, `arxiv`, `apple-reminders`,
  `notion`, `web-search`, `baoyu-infographic`, `skill-library-integrity`, `skill-inventory`,
  `skill-drift`, `skill-audit-methodology`, `skill-taxonomy-reclassification`,
  `skills-cold-storage-ops`, `forge-vss-parser`, `agent-fork-governance`, …
- The one apparent hit, `computer-use`, is a **bundled** skill (index labels it `(bundled)`) — it
  resolves from Qwen's own bundle, not from `.archive`. Its presence was a scope flaw in my walk
  (5 roots, bundle excluded), not evidence of archive scanning.
- The six folded meta-skills correctly do **not** appear — `skill-mesh` replaced them, as documented.

→ **The loader does not scan `.archive`.** The gate pruning dot-dirs (line 56) **matches** loader
behaviour; both are correctly scoped. `fi-qwen-upgrade` ×3 and `AAA-voice-cloning-qwen-cloud` ×3 are
**inert**, not a live collision. Item withdrawn.

**Methodology error recorded:** my first pass used a hand-written `seen` set recalled from memory
rather than the actual index, and reported 7 false positives. Superseded by the method above.

### (3) The remaining duplicate identities → **MEASURED, and blanket `ikut aaa` would be destructive**

Not 21 — **29 groups / 61 skills**, because census EXCLs differ from this walk (this walk spans 5
roots and does not exclude `.frozen`). Rule 8: the number names its own denominator.

Direction of freshness across all 29:

| Direction | Count |
|---|---|
| **HARNESS copy is NEWER than canonical** | **17** |
| canonical is newest | 9 |
| `.frozen/2026-09-20-case-dupes` (deliberate freeze) | 3 |

**This is the load-bearing finding.** 17 of 29 have the *view* newer than the *writer*:

- `PETRONAS-intelligence-router` — harness 09-17 **8298 B** vs canonical 09-15 **4462 B**
- `seven-zen-organs-enforcement` — harness 09-15 85276 vs canonical 08-22 83634
- `FORGE-skill-linter` — harness 09-16 7263 vs canonical 08-22 5935
- `firecrawl-web-search` — harness 09-14 9209 vs canonical 08-22 8815

Root cause: **`/root/.kimi-code/skills` holds independently-edited real copies of canonical skills**
(23 of the 26 HOLD groups), i.e. rule 1 (*one writer, many views*) is violated in the harness
direction too — views were edited directly and **canonical is stale** for 17 of them.

→ Applying `ikut aaa` (canonical wins) here would **rewind 17 skills to older content**. That is
exactly what the qwen fold-first step existed to prevent, and it is **not** what "tutup baki" can
close mechanically. Per C-7 these stay `DUPLICATE_OWNER = HOLD`, now with direction evidence attached
instead of a bare hash difference.

Split, ready for a decision:
- **9 safe** (canonical newest — view is stale; fold+repoint, same recipe as §5d)
- **3 frozen** (`.frozen` sits *inside* the scanned store while census EXCL lacks `.frozen` —
  either exclude it, or move the freeze outside every walked root per C-2)
- **17 HOLD** (view newer — needs per-pair merge-up, not repoint)

## 5g. `merge up` — EXECUTED (08:42–08:50 MYT), with three self-inflicted breakages found and fixed

Sovereign go/no-go: **`merge up`**. Method: section-level merge (H2 buckets), not line-level —
sampling showed `"debt"` vs `"debt."` counts as unique on *both* sides, so a line-level union would
duplicate every bullet.

**The loss guard earned its keep three times before it passed:**

| Run | abort | what the guard caught |
|---|---|---|
| 1 | **23/27** | base **preamble dropped** (`sec_map['']` never emitted) + older frontmatter keys not carried |
| 2 | **15/27** | remaining "loss" was almost entirely **conflicting `description:`** |
| 3 | **0/27** | after splitting the metric — see below |

**Metric correction (the substantive one):** my first metric conflated *loss* with *supersession*.
A conflicting frontmatter value that the **newer** base wins is merge semantics, not loss. Split into
`body_loss` (aborts) and `fm_superseded` (recorded per entry, informational). Aborting on
supersession would have blocked every merge in existence.

**Applied:** 27 entries, `body_loss=0` everywhere · YAML validated on **all 29 targets, 0 bad** ·
53 originals archived · manifest **72 lines** · `.frozen/2026-09-20-case-dupes` → `.archive/`.

**Three breakages I caused, found by re-probing, fixed:**

1. **2 broken symlinks.** Moving `/root/.hermes/skills/apex_verdict_hold/` to archive took its
   `claude/` and `hermes/` children, orphaning `.hermes/apex_verdict_seal/{claude,hermes}`.
   → restored both as symlinks → AAA.
2. **1 abort (`arifOS ACT`)** — group ordering: `apex_verdict_hold` sorts before `arifOS ACT` and
   consumed the shared parent dir, so the later group saw "member vanished". kimi#2 repointed,
   kimi#1 dependent path recreated. Ledger was 71→72 after the repair.
3. **`broken_symlinks 0 → 2`, `VERDICT WARN → FAIL`** — caused by (1); now **0 / WARN** again.

**Two of my own alarms were false:**
- *"harness content missing from live canonical"* → measured **0** for all 7 `CANON_NEWEST`. The
  earlier gap was punctuation-only and `norm()` already collapses it.
- *"`canonical backups: 0` means writes were skipped"* → for `CANON_NEWEST` `base == tgt`, so
  skipping is correct; content check confirms no body lines missing.

**Two numbers corrected as unfair comparisons:** my final gate run added `kimi`+`opencode` roots the
baseline never had. Re-run with the **original 3 roots**:

| Metric (same 3 roots) | Baseline | Now |
|---|---|---|
| `UNRESOLVABLE` | **6** | **0** ✅ |
| `DIR-BASENAME mismatch` | 29 | **27** |
| skills with `SKILL.md` | 584 | 587 |

**Census: `broken_symlinks 0` ✅ · `VERDICT WARN` ✅ · but `duplicate_identity_groups 21 → 31` ⚠️**

Root cause of the *scope* confusion: census `ROOTS` = canonical + hermes + **`profiles/aaa-hermes`**,
plus `OVERLAY_ROOTS` including **gemini, codex, continue** — roots I never scanned. Independent
recount over census's exact scope: **38 groups**, second-path attribution `profile 32 · kimi 28 ·
claude 8 · codex 6`. **Most groups do not involve canonical at all** (profile↔kimi pairs such as
`FORGE-cicd-docker-deploy`, `FORGE-pr-review`, `FORGE-mcp-ops`) → largely **pre-existing**, outside
the 29 I touched.

**Delta 21 → 31 — later EXPLAINED, retracting the "UNEXPLAINED" label below.** I wrote here that I
could not close the arithmetic and handed it to the next census audit. One step later (§5h) I found
the mechanism: `skills-census.py` keys on `realpath(dp)` — the **directory**, not `SKILL.md` — and
`dup_reimplemented = foreign_homes ∩ canon_homes`. Both the merge-up (§5g) and the profile/kimi
work (§5h) left the harness **directory real** while symlinking only the file, so every home stayed
distinct and each promotion re-registered as a duplicate. The measurement I could not close
(promotions ≈4 vs delta 10) was uncloseable *because* the dominant term was not promotions at all —
it was the symlink granularity. Corrected in place per rule 17 rather than appended as a second
report. Root cause of both regressions: **mine**, fixed by converting to directory views (§5h).

## 5h. Items 1 + 2 CLOSED (08:55–09:10 MYT) — item 3 partially pre-executed, remainder needs the binary

### Item 1 — gate severity split, `EXIT 1 → 0` ✅

Two defects in one script, not 27 bad folders:

1. **Wrong key.** Collisions grouped on `os.path.basename(dirpath)` — the *folder*. The loader
   dedupes on frontmatter `name:` (rule 10), so two different skills merely living in a same-named
   dir (`…/hermes/`) were reported as one unresolvable name. Rekeyed to the routing name.
2. **Severity collapsed.** `return 1 if (collisions or mismatches) else 0` put cosmetic folder/name
   drift and a genuinely unresolvable name under one code. `frontmatter_name()` falls back to the
   folder, so **every reported mismatch *proves* a frontmatter `name:` exists** → the folder is
   never the routing key → that class cannot make a skill unreachable.

Now `FAIL` only on collisions; mismatch is `INFO` carrying *"do NOT mass-rename — path dependency +
rule 16 dependents sweep first"*.

Backup preserved pre-patch: `skill_resolution_audit.py.bak-20260923-fi003` = `e22d08fd90e4d237`,
current = `fd8a9a6a62957b1c`.

| Same 3 roots | Baseline | Now |
|---|---|---|
| `UNRESOLVABLE` | 6 | **0** ✅ |
| mismatch | FAIL 27 | **INFO 27** |
| `EXIT` | 1 | **0** ✅ |

### Item 2 — profile + kimi are VIEWS ✅ `duplicate_identity 21 → 7`

**Two corrections to my own characterisation:**
- I wrote *"kebanyakannya divergen"*. Measured: **23 of 32 IDENTICAL**, 9 diverged — mostly mechanical.
- **My file-level symlink approach is what raised the census.** `skills-census.py` keys on
  `realpath(dp)` — the **directory**, not `SKILL.md` — and
  `dup_reimplemented = foreign_homes ∩ canon_homes`. Rule 1's view shape is a **directory**
  symlink. I had symlinked only the file, so every harness dir stayed *real* and each promotion
  re-registered (`31 → 51`). **That regression was mine, not the instrument's.**

**Sequence that fixed it without losing a byte:**
1. Measured sidecars first — **111 files existed in harness but not canonical**
   (`liveness.json`, `kimi/SKILL_MD.md`, `opencode/README.md`, …). Converting dirs first would
   have orphaned all 111.
2. Promoted **112 sidecar files** (additive, never overwrite) → built-in loss gate (`lost=0`) →
   **then** converted **46 + 39 dirs** to directory views.
3. 2 dirs **correctly blocked** — they hold nested skill children
   (`.hermes/skills/apex_verdict_hold{hermes,claude}`, kimi `apex-gates/apex_verdict_hold{claude}`);
   converting them is precisely the parent-dir orphan bug from §5g.

**A defect I introduced, caught by the gate I had just patched:** sidecar promotion copied
`apex_verdict_seal/hermes/SKILL.md` into canonical while `apex_verdict_hold/hermes` already held
that routing name → canonical-internal duplicate, `UNRESOLVABLE 1`. Measured `body_loss=0`
(duplicate was a normalized subset) → merged + collapsed to symlink → `0`.

| Metric | Session start | Now |
|---|---|---|
| census `duplicate_identity_groups` | 26 → 21 | **7** |
| census `duplicate_identity_skills` | 49 → 43 | **17** |
| census `broken_symlinks` / `total_diverged` | 0 / — | **0 / 0** ✅ |
| gate `UNRESOLVABLE` (3-root and 5-root) | 6 | **0** ✅ |
| gate `EXIT` | 1 | **0** ✅ |
| broken symlinks, all roots | — | **0** ✅ |

**Rollback (`test -f`-verified):** manifest **340 lines** · **147** archived `SKILL.md` ·
`APEX-ACT-home-before-merge` EXISTS.

**Remaining 7** — `apex-verdict-hold`, `forge`, `init`, `mmx-cli`, `nusantara-substrate`,
`reflective`, `verify-runtime` = the `DIVERGED` class never auto-merged. **C-7 `DUPLICATE_OWNER`
= HOLD for the human.** Deliberately untouched.

### Item 3 — `chattr +i`: core ALREADY DONE by another lane; remainder is the binary

`lsattr` on the meta set (measured, not assumed):

| File | flag | mtime | **ctime** |
|---|---|---|---|
| `references/model-list.md` | **`----i----` FROZEN** | 07:56:31 | **08:14:16** |
| `references/qwen-sot.md` | **`----i----` FROZEN** | 07:56:31 | **08:14:16** |
| `references/pricing.md` | unlocked | 2026-08-26 | — |
| `references/pricing-disclaimer.md` | unlocked | 2026-08-26 | — |
| `references/recommendation-matrix.md` | unlocked | 2026-08-26 | — |
| `references/sources.md`, `cli-usage.md`, `error-handling.md`, `agent-compatibility.md` | unlocked | — | — |
| `qwencloud-model-selector/SKILL.md` | unlocked | — | — |
| `forge-multimodal-router/SKILL.md` | unlocked | — | — |

`ctime 08:14:16` on both SOT files ≠ any action of mine — I never ran `chattr`. **A concurrent
lane executed the Step-7 freeze ceremony at 08:14:16 today.** The two files the plan named as
"the single source" are already immutable.

What the plan called meta and that is **still unlocked**: the 4 pricing/quota files (the original
"five places to be wrong about the same number"), `sources.md`, the router body, and the rollback
manifest. No writer on them in 30 min. Rollback for any freeze: `chattr -i <file>` (skills tree is
*not* one of the three canon-locked trees — `canon-mutate status` shows only `governance`, `canon`,
`GENESIS` carry `+i`).

`skill-mesh` ESCALATE: *"Produce the artifact, take the go/no-go, do not execute unattended."*
Artifact above; go/no-go **taken 09:12 MYT** → executed in §5i.

## 5i. Item 3 EXECUTED (09:12 MYT) — 5 frozen + verified, 1 element of my own proposal held

Sovereign echoed the binary back → go.

**Frozen this run** (`chattr +i`, all pre-checked quiet for 30 min, all non-empty):

| File | bytes | `lsattr` after | behaviour (0-byte append) |
|---|---|---|---|
| `references/pricing.md` | 5119 | `----i---------` | **EPERM** ✅ |
| `references/pricing-disclaimer.md` | 6396 | `----i---------` | **EPERM** ✅ |
| `references/recommendation-matrix.md` | 15604 | `----i---------` | **EPERM** ✅ |
| `references/sources.md` | 1169 | `----i---------` | **EPERM** ✅ |
| `forge-multimodal-router/SKILL.md` | 16927 | `----i---------` | **EPERM** ✅ |

Sizes unchanged after the write test — the attempt was refused, nothing was written. Verified by
`lsattr` **and** by behaviour, not by assuming the flag took.

Already frozen before this run by the concurrent lane (`ctime 08:14:16`): `model-list.md`,
`qwen-sot.md`. Together the two originally-scoped "single source" files plus all three price/quota
numbers are now immutable — **the price figures can no longer change silently**, which was the
stated purpose.

**Element of my own proposal I did NOT execute, with reason:** the rollback **manifest**.

`ROLLBACK-MANIFEST.jsonl` flag `--------------e--`, still appendable, **340 lines**. Freezing it
would block `>>` on the very file that records how to undo everything else — `chattr +i` refuses
append, while rule 19 requires the manifest be *accumulating and never truncated*. Freezing the
undo path is strictly worse than leaving it warm: it protects a ledger nobody can write by
destroying the property the ledger exists to have. Held deliberately, not overlooked.

**Unfreeze recipe** (skills tree is not canon-locked — `canon-mutate status` shows only
`governance`, `canon`, `GENESIS` carry `+i`): `chattr -i <file>` then edit, then `chattr +i` again.
