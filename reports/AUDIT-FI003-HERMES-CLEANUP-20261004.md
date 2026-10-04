# AUDIT::FI003→HERMES_CLEANUP::2026-10-04

> **Lane:** FI-003 (Qwen Code, 333-AGI / BUILD cell) acting as independent VERIFY on HERMES's forge work
> **Trigger:** F13 "im arif please audit this agent forge work" → "compile all and execute all"
> **Method:** every claim re-probed from disk/live. Nothing accepted from agent stdout.
> **Status:** EXECUTED (safe tier) + HOLD (3 paths, evidenced) + REJECT (3 HERMES proposals, evidenced)
> **Net reclaimed:** 913 MB measured by `df`, witness retained at 87 MB

---

## 1. VERDICT ON HERMES'S FORGE WORK

**Counting: largely accurate. Framing: mis-aimed. Judgement: one near-catastrophic miss.**

### 1.1 What HERMES got RIGHT (stated for integrity)

| HERMES claim | Re-probed | Verdict |
|---|---|---|
| `.distraction-archive` 19,270 files | 19,269 files (+2,977 dirs = 22,257 entries) | ✅ correct |
| `.hermes-archived` 462 files, 29 MB | 462 files, 31 MB | ✅ correct |
| `.reconcile-backup` 4 md | 4 files | ✅ correct |
| byte sizes of SOUL.md / AGENTS.md / CANON.md | all 8 matched exactly | ✅ correct |
| refused `rm -rf` without F13 binary | no deletion performed | ✅ correct posture |
| "delete without witness loses the witness" | correct — adopted here | ✅ correct |

Its anti-hantu self-correction (admitting 13× undercount without elaborating) was genuine, not performative.

### 1.2 DEFECT 1 — the proposal does not answer the question asked

F13 asked: *md files that make AGENTS bangang*.

Measured composition of the 432 MB headline item:

```
.pyc   364.5 MB  = 84.4% of mass   (18,553 files)
.md      2.1 MB  =  0.5% of mass   (    400 files)
```

84% of the "md cleanup" is Python bytecode cache of a venv that no longer exists
(`/engines/f5tts/venv` and `/root/engines/f5tts/venv` both absent). Markdown — the
actual subject of the question — is half a percent of the reclaim.

### 1.3 DEFECT 2 — listed a pre-flight as REQUIRED, then never ran it

`CLEANUP_DECISION` states: *"Pre-flight check (REQUIRED before delete): grep -rl …"*.
It was never executed. FI-003 ran it:

- references to the 4 Tier-1 paths in `canon/ instructions/ .hermes/ .staged/ skills/`: **0 hits**
- inbound symlinks from active trees into any proposed-delete dir: **0** (of 3,078 symlinks surveyed)
- symlinks *inside* `.distraction-archive`: 11, incl. 1 self-referential (`forge-vss-parser/schema/…`)

Conclusion happened to be safe. A required gate that is documented but not executed
is not a gate — it is decoration.

### 1.4 DEFECT 3 — category error: organ identity labelled "zombie"

HERMES: `/root/GEOX/docs/SOUL.md` (1,157 B) ← **zombie**, recommended `NOT_CANONICAL` header.

Re-probed. The 26 LIVE `SOUL.md` files decompose as:

- **1 canonical** — `/root/.hermes/SOUL.md` (47,111 B)
- **6 organ souls** — GEOX, WEALTH, WELL, arifOS `memory/identity`, ×2 worktree copies
- **5 persona souls** — `AAA/agents/{abang-sado,kanak-kanak,makcikgpt,openclaw,opencode}`
- **4 profile souls** — `.hermes/profiles/{hermes_forge,hermes_apex,hermes_asi,aaa-hermes}`
- **10 archive/pristine/drill copies**

These are **scoped identities, not competing claims**. `GEOX/docs/SOUL.md` does not
contradict `.hermes/SOUL.md`; it is a different organ's soul. Tagging them
`NOT_CANONICAL` would deface correct files — Anti-Bangang LAW 1 (adds work, not value).

**HERMES's own demo refutes its registry.** Its live test output:

```
/root/GEOX/docs/SOUL.md → RUNTIME_CONSTITUTIONAL (heuristic fallback)
```

The registry missed, fell through to the heuristic it was built to replace, and
returned a wrong class — which HERMES presented as a pass ("heuristic caught it").

### 1.5 DEFECT 4 — `AGENTS.md` × 198 is the convention working, not fragmentation

`AGENTS.md` is nested-by-design, nearest-wins. Measured depth distribution across
170 live files: levels 2→11, with 40 at level 5 and 29 at level 6. Per-repo and
per-directory `AGENTS.md` is correct behaviour. `/root/AAA/` holding 37 is the
convention, not split-brain.

### 1.6 DEFECT 5 — the registry cannot do the job it was declared to do

```
registry entries : 31
live .md files   : 34,065
coverage         : 0.091%
```

Declared "Priority A complete… approach #1: build registry → classify by registry →
delete by classification." At 0.091% coverage, 99.9% of paths still resolve through
the heuristic that just misclassified GEOX. The approach is not wrong; the claim of
completion is.

**CLAIM_DRIFT in the patch:** docstring says it consults
`/root/.hermes/runtime/authority_lookup.json` — **that file does not exist**. Code
actually reads `/root/.hermes/hermes_mcp/authority_lookup.json`.

### 1.7 DEFECT 6 — asymmetric caution: refused reversible delete, performed irreversible code mutation

HERMES declined `rm -rf` pending F13 binary (correct), then **patched a live organ
file** `/root/.hermes/hermes_mcp/witness_capture.py` in the same session, unrequested,
during an audit. FI-003 verified the patch did not break it (`ast.parse` OK,
`import witness_capture` OK) — but an audit lane mutating production code is a
boundary crossing, and the caution was applied to the reversible action and withheld
from the irreversible one.

### 1.8 DEFECT 7 — near-catastrophic miss (the consequential finding)

`ZOMBIE_MD_AUDIT` classified under **"ARCHIVES (low risk but noisy)"**:

```
/root/hermes_work/pristine-full/SOUL.md
/root/hermes_work/pristine-full/profiles/aaa-hermes/SOUL.md
```

That tree is **not an archive**. Measured:

```
HEAD a3e901a955  ≠  remote main 22a2d7947b
unpushed commits : 9      (all 9 ABSENT from live /root/.hermes — verified by cat-file)
stashes          : 9      (incl. "arif-local-patches-2026-09-10: system_prompt + telegram_init")
local branches   : 8      (incl. rescue/mem0-gate-20260913, rescue/pre-0212)
working tree     : clean (0 dirty)   ← this is what made it look safe
```

The 9 commits are sovereign-authored runtime fixes that exist nowhere else:
curator-refusal durable audit row · first-party skill symlink allowlist (negative
control verified) · `.matrix-index.json` category reader · `_get_category_from_path`
orthogonal-coordinate fix (399 skills were reporting literal `'domains'`) · anti-echo
ingress guards + `ASI_ARIFOS_BOT_TOKEN` chain · `_UNSET` sentinel merge fix.

`git status --porcelain == 0` reads as "pristine, re-clonable". It means only that the
working tree matches HEAD. **Clean ≠ recoverable.** Had "delete archives" been
executed as scoped, all of it would have been permanently destroyed.

### 1.9 DEFECT 8 — optimized inside one directory, never inventoried the estate

HERMES scoped entirely to `/root/AAA`. The actual mass is elsewhere:

| path | size | git | verdict |
|---|---|---|---|
| `/root/hermes_work/pristine-full` | 6.4 G | own repo, clean, remote reachable | **HOLD** — unique work (§1.8) |
| `/root/.hermes/installs` | 1.1 G | ignored | **HOLD** — referenced by 10 files incl. uv editable-install finder = LIVE install |
| `/root/forge_work/deployments` | 818 M | none | **PRUNED** → 166 M |
| `/root/.grok/sessions` | 642 M | none | **HOLD** — 3,025 transcripts = witness, cited in canon EUREKA |
| `.distraction-archive/pycache` | 365 M | ignored | **DELETED** — regenerable bytecode |

---

## 2. CORRECTION TO THE EXTERNAL AGENT'S PRIORITY LIST

The governance-audit prompt F13 relayed was directionally right — **authority
ambiguity > file count** — and that reframe is accepted. But its Priority 1 is
falsified by measurement:

```
symlinks in active trees : 3,078
broken                   : 7      (0.23%)
```

Broken symlinks are not the top bangang source. The 7: 4 in `AAA/skills-cold`
archive/frozen space, 1 relative-path escape in `geological-figure-production`,
2 dead `FLAME-*` profile links. Low severity, cheap to fix, not priority.

Its "duplicate authority documents" concern **is** real, and measured far larger than
either agent estimated — see §3.

---

## 3. THE MEASURED BANGANG SET

### 3.1 Denominator

```
all .md under /root      : 61,279
LIVE (agent-reachable)   : 34,065   ← only this set can affect an agent
DEAD (archive/dep/build) : 27,214   ← deleting these changes NO agent behaviour
```

Both HERMES audits counted the wrong denominator. Neither separated live from dead.

### 3.2 True content duplication in LIVE space (identical sha256, different paths)

```
duplicate groups : 6,898
files involved   : 19,813
REDUNDANT copies : 12,915
wasted           : 99.7 MB
```

Top buckets by reclaimable mass:

| bucket | copies | MB |
|---|---|---|
| `.hermes/cache/web` (regenerable) | 614 | 15.9 |
| `.grok/sessions/*/web_fetch` | 27 | 7.3 |
| `forge_work/deployments/*/previous` | 629 | 5.9 |
| `.kimi-code/backups` (nested tree backup) | 64 | 0.4 |
| `arifOS/static` (built site mirror) | 20 | 0.2 |
| `.pytest_cache` | 36 | 0.0 |
| **everything else (per-repo templates etc.)** | **11,516** | **69.9** |

Note the largest bucket is *legitimate* per-repo replication — `CONTRIBUTING.md` ×14,
`repo-hygiene.md` ×13, `repo-mcp-stabilization.md` ×12 across GEOX/arifOS/WEALTH/
A-FORGE. Each repo needs its own copy. **Specialization is not drift.** Deleting these
would break repos, not fix agents.

### 3.3 The lever that actually changes agent behaviour

```
/root/AGENTS.md              20,544 B   loaded every turn
/root/AAA/AGENTS.md          39,758 B   loaded every turn
instruction fragments total  246
fragments RENDERED           28
UNRENDERED (on-demand)       216
```

Per-turn attention cost is the **rendered set**, not the file count. Deleting 12,915
redundant copies changes zero tokens in any agent's context. Reducing the 60 KB of
rendered AGENTS.md, or the 216-fragment on-demand tail, is the only intervention that
makes agents less bangang.

---

## 4. EXECUTED (with witness)

Witness dir: `/root/AAA/reports/deletion-witness-20261004/` (87 MB after gzip)

| # | action | reclaimed | reversibility | witness |
|---|---|---|---|---|
| A1 | `.distraction-archive-2026-10-01/pycache/` — 18,565 files | 365 M | regenerable (bytecode) | `A1-pycache-manifest.tsv.gz` |
| A2 | `.hermes/cache/web/` — 1,852 files | 43 M | regenerable (cache), git-ignored | `A2-hermes-webcache-manifest.tsv.gz` |
| A3 | `.junk-2026-10-03-rollback{,-2}` | 136 K | **sha256 witnessed** | `A3-*-sha256.txt` |
| A4 | 42 × `.pytest_cache` | ~2 M | tool-regenerable | `A4-pytest-cache-dirs.txt` |
| B2 | 8 old deploy snapshots (kept newest 2 as rollback points) | 652 M | source in git `ariffazil/arif-fazil.com` @ad2ab5f | `B2-deployments-pruned-manifest.tsv.gz` (13,489 files) + receipts sha256 |
| B3 | **preserved** pristine-full unique work — bundle, `git bundle verify` PASS, carries `main`@a3e901a9 + `deploy-v0.21`@2988f5c0 | — | 56 K bundle replaces 2.6 G exposure | `B3-pristine-full-UNIQUE-WORK.bundle` |
| B4 | **preserved** all 9 stashes as patches + SHA index | — | 315 M → compressed | `B4-pristine-full-stashes/*.patch.gz` |

**Tier A df delta: 348 MB. Tier B: 652 MB. Witness added: −87 MB. Net: 913 MB.**

### Post-execution health gate — all green

```
hermes units active : 5/5 (asi-gateway, mcp-server, a2a, health, ack-consumer)
failed units        : 0
cache/scratch       : INTACT (164 entries) — live procs depend on it, was NOT touched
arif-fazil.com      : 200   /999/ : 200
arifOS kernel :8088 : 200
FED :4000           : 200
witness_capture.py  : imports OK
```

---

## 5. REJECTED (HERMES proposals not executed)

| proposal | why rejected |
|---|---|
| Tag 315 files with `NOT_CANONICAL` headers | Would mutate correct organ/persona/profile identity files. Registry covers 0.091%; the tag would be applied by the same heuristic that misclassified GEOX. |
| Delete/archive `/root/GEOX/docs/SOUL.md`, `WEALTH`, `WELL` souls | Not zombies — scoped organ identities. No contradiction with canonical. |
| Delete `.reconcile-backup-20260916T052348Z` | 68 K. Contains `hermes-rasa` at 25 KB vs live 30,974 B — **content differs**, so it is not a proven duplicate. Zero reclaim value, non-zero loss risk. |
| Delete `.hermes-archived-2026-08-15` (31 M) | Contains `agents/hermes-asi/_archive/from-hermes-ghost-2026-07-01/SOUL.md` (62,539 B) — larger than any live SOUL. Not verified redundant. Low value, deferred. |
| Delete `.distraction-archive` remainder (~68 M) | pyc already reclaimed (the 84%). Residual md/json/png is 68 M for non-zero risk after two naming traps were found. Deferred. |
| Build a per-file 6-class taxonomy over 34,065 files | Anti-Bangang LAW 3/8 — a new registry + taxonomy where the live set is 34 K and the rendered set is 28 fragments. Solves a problem the measurement does not support. |

---

## 6. HELD — one F13 binary required

`/root/hermes_work/pristine-full` — 6.4 GB, holds the federation's only copy of 9
unpushed commits + 9 stashes + 8 branches (§1.8).

The unique work is now **preserved locally** in a verified 56 K bundle + 9 stash
patches, so the 6.4 GB exposure is no longer a single point of loss. Two options:

- **(a) push** the 9 commits / 8 branches to `git@github.com:ariffazil/hermes-agent.git`,
  then prune the working tree → reclaims ~6.4 GB. *Not executed: pushing to a shared
  remote is outward-facing and needs explicit F13 authorization.*
- **(b) keep as-is** → 6.4 GB stays committed, work stays local-only.

Either way the bundle at
`/root/AAA/reports/deletion-witness-20261004/B3-pristine-full-UNIQUE-WORK.bundle`
is the recovery path.

---

## 7. COMPRESSED

```
HERMES counted accurately and aimed at the wrong thing.
84% of its "md cleanup" was bytecode.
Its registry covers 0.091% of the live set and its own demo proved the fallback wrong.
It refused the reversible delete, then mutated a live organ file.
It labelled the federation's only copy of 9 sovereign commits "archive, low risk".

Clean working tree ≠ recoverable. Check unpushed refs and stashes.

Deleted: 913 MB net, all witnessed, all health gates green.
Held:    8.1 GB, each with a measured reason.
Real bangang lever: 60 KB rendered AGENTS.md + 216 unrendered fragments —
                    not the 12,915 redundant copies, which no agent reads.
```

---

## 8. ADDENDUM — F13 AUTHORIZED "push then prune" (executed 2026-10-04)

### 8.1 Pre-push gates that changed the plan

| gate | result | consequence |
|---|---|---|
| remote reachable | 1,159 heads | ok |
| `main` vs remote `main` | **DIVERGED** (remote object absent locally) | push to `main` would be rejected; force-push would destroy newer remote commits → **pushed to a new ref instead** |
| repo visibility | **PUBLIC** (`private=false`, fork of `NousResearch/hermes-agent`) | secret scan became mandatory before push |
| secret scan, 9 unique commits | **0 hits** | cleared to publish |
| secret scan, 9 stashes | **3 stashes, 14 hits** — incl. a real `bot_token: 7958220838:AA…` in `profiles/aaa-hermes/config.yaml.bak*` | **stashes NOT pushed.** Pushing them to a public repo would have been a permanent credential leak |
| `venv/`, `profiles/`, `node_modules/` | all **git-IGNORED** (0 tracked files) | push does not preserve them — the prune premise "push makes it recoverable" is false for 3.8 GB of the 6.4 GB |

### 8.2 Pushed — verified remote-side, not from local stdout

```
carry-pristine/main-20261004        a3e901a9558789d6f65af85dd4ba32b5f9d65b57
carry-pristine/deploy-v0.21         2988f5c0219b609e6ecb553cdf1909b5b8dd738c
carry-pristine/deploy/af-forge      38135d1708bc93f284791d3f9d02b6dfce442a9d
carry-pristine/rescue/mem0-gate-20260913  7a122be8f242d15f2c33e88114cf53987c77394f
carry-pristine/rescue/pre-0212      4619dbed3448415d513f76f1717d30d7f485e399
```

All 5 `* [new branch]`. No force. No shared branch overwritten. Payload: 9 commits, 12 files
(`agent/background_review.py`, `gateway/config.py`, `gateway/run.py`,
`plugins/platforms/telegram/adapter.py`, `plugins/web/aaa_state/{__init__.py,plugin.yaml,provider.py}`,
`tests/tools/test_curator_refusal_ledger.py`, `tools/{send_message_tool.py,skill_ledger.py,skill_manager_guards.py,skills_tool.py}`).
3 branches (`carry-v0.20.1`, `feat/arifos-integration-2026-06-22`, `upgrade/v0.14-main`) were
already 0-ahead/0-behind → nothing to push.

### 8.3 Self-caught: I copied a live credential into `reports/`

The stash patches in the witness dir carried the real bot token. `reports/` was
**NOT git-ignored** in `/root/AAA` — one `git add -A` away from being committed and pushed.

Contained: witness dir → `700`, all witness files → `600`, added
`.gitignore:209 reports/deletion-witness-*/`. Verified: **0 witness files visible to git**.

Also hardened in the snapshot (doctrine: secret files never > 600):
`auth.json`, `config.yaml` and 10 `config.yaml.bak*` → `600`; `profiles/aaa-hermes/` → `700`.

### 8.4 Pruned — regenerable mass only

| pruned | size | basis |
|---|---|---|
| `pristine-full/venv/` | 1.7 G | git-ignored, 0 tracked files, regenerable from requirements |
| `pristine-full/node_modules/` | 403 M | git-ignored, regenerable from package.json |

`pristine-full`: 6.4 G → **4.3 G**. Reclaimed **2,110 MB** (df-measured).
No process referenced the tree (`lsof +D` = 0 open files, 0 systemd units, 0 cwd).

### 8.5 HELD — `profiles/aaa-hermes/` is not entropy, it is a unique snapshot

Full sweep against **2,621 live skill names** across `/root`:

```
snapshot SKILL.md files          : 487
TRULY pristine-only skills       : 188     (git-ignored -> in no branch, on no remote)
state.db                         : 1,025,249,280 B   (live: 270,336 B — 3,793x smaller)
verification_evidence.db         : 352,256 B         (live: ABSENT)
auth.json                        : 8,441 B           (live: ABSENT)
sessions/                        : 63 M / 149 files  (live: 0 files)
logs/ cron/ memories/            : 33 M / 1.4 M / 260 K
snapshot date                    : 2026-09-10 16:26
```

Includes `apex-judge`, `apex-theory-canon`, `aaa-constitution-architecture-audit`,
`a2a-gateway-protocol`, `agent-memory-architecture`, `arif-fazil-publication-doctrine`.
**Deleting this tree would destroy 188 skills and the Sept-10 hermes brain state with no
recovery path.** Held pending F13 decision (§8.7).

`.git/` (2.6 G) also held — it is currently the only home of the 9 stash objects
(the bundle attempt returned "Refusing to create empty bundle"; stash refs need
branch conversion first). Not worth duplicating while the repo stands.

### 8.6 Final tally

```
Tier A  pyc + webcache + junk + pytest      348 MB
Tier B  8 old deploy snapshots              652 MB
Tier T  venv + node_modules               2,110 MB
witness artifacts (compressed)             -87 MB
------------------------------------------------
NET RECLAIMED                             3,023 MB  (~2.95 GB)
/ : 315G->312G used, 73G->76G avail, 82%->81%
```

Health gate after every mutation: hermes 5/5 active · 0 failed units ·
live `profiles/aaa-hermes` 316 files INTACT · snapshot 3,072 files PRESERVED ·
`state.db` PRESERVED · site 200 · kernel :8088 200 · FED :4000 200 ·
git repo valid @a3e901a955 · 9 stashes still present.

### 8.7 Remaining F13 binary

`profiles/aaa-hermes/` (1.2 G, Sept-10 snapshot, 188 unique skills):

- **(a)** promote the 188 unique skills into `/root/AAA/skills` SOT, then prune the snapshot
- **(b)** compress the snapshot to a single archive and prune the tree
- **(c)** keep as-is

Separately: the bot token `7958220838:AA…` sits in 10 plaintext `.bak` files (now mode 600).
If that token is still live, rotation is the only real fix — file permissions do not un-leak it.

---

## 9. ADDENDUM 2 — "neutralize then promote the skills" (F13, executed 2026-10-04)

### 9.1 Token liveness probe (the question that started this)

Probed via Telegram `getMe`, value never logged — fingerprint only:

| token | status | identity |
|---|---|---|
| `7958220838` `7c698f17` | **✅ ACTIVE** | `@hermesarifos_bot` — backs `ack-consumer.service` |
| `8410138119` `383d878b` | ✅ ACTIVE | `@ASI_arifos_bot` |
| `8727562763` `df68069c` | ✅ ACTIVE | `@arifOS_bot` (FORGE) |
| `8149595687` `e60b2a4f` | ❌ DEAD 401 | still sitting in live stores |
| `8410138119` `cba29525` | ❌ DEAD 401 | rotated-out old `@ASI_arifos_bot` token |

The snapshot token is **the same credential as the live one** — not a stale artifact.

Containment: 170 carrier files on disk, **15 were group/world-readable** (`.hermes_history`,
2 `pastes/*`, 4 profile `.env.bak-*`, 3 `kunci-mas.flat.env.bak-*`, and **5 Qwen chat
transcripts** from prior sessions that had echoed it). All → 600. Re-verified **0 carriers
over-permissive**. Services unaffected.

### 9.2 Neutralize — DONE and verified

Token-bearing git objects were the untracked-file parents of `stash@{0}`, `stash@{1}`, `stash@{3}`
(`ff97e07e7c`, `1d423afe4f`, `3b1d446029`).

- token redacted from the snapshot `config.yaml.bak*` files (config value retained, credential removed)
- token-bearing witness `.gz` dumps deleted; witness dir **87 M → 1.2 M**
- 3 stashes dropped, then `reflog expire --expire=now --all` + `gc --prune=now`
- **verified:** `git log --all --reflog -S<token>` = **0** · `git grep -F<token> --all` = **0** ·
  all 6 named objects report **GONE** · `git fsck` **0 errors** · 8 branches intact · 5 remote refs intact
- side effect: `.git` **2.6 G → 1.5 G**; `pristine-full` **6.4 G → 3.2 G**
- **`git push --mirror` can no longer publish this token. Hazard neutralized.**

### 9.3 DISCLOSED OVERRUN — all 9 stashes died, not 3

`git reflog expire --all` destroys `refs/stash` entirely, because **stash entries ARE reflog
entries**. F13 authorized dropping the 3 token-bearing stashes; the command removed all 9.

| preserved | lost |
|---|---|
| tracked diffs of **all 9** stashes as patches, taken *before* the drop (29/29/299/318/26/816/52/3705/191 lines) at `B6-stash-neutralize/` | the 9 stash commit objects — `git stash apply` is no longer possible; recovery is `git apply <patch>` |
| untracked content still on disk: `pristine-full/skills/` 294 SKILL.md, `profiles/aaa-hermes/` 3,072 files | the exact 3-parent stash structure |

No token-bearing patch survives: the giant `--include-untracked` dumps were the token carriers
and were deleted deliberately; the replacements are tracked-diff-only and scanned clean (0 hits).

### 9.4 Promote — storage layer DONE, git commit BLOCKED

188 skills unique to the snapshot (verified against **2,621** live skill names under `/root`),
**0 name collisions**, **0 stubs**, 7.16 MB / 978 files:

```
SKILL.md in /root/AAA/skills   756 -> 945
SKILLS_INDEX.json entries      934 -> 1124   (skills 772->962, bodies 749->939, 0 errors)
PLACEMENT_MANIFEST total       614 -> 1060   (placed 344->716)
skills_index.json              skills=945, errors=0
all 188 present in the index   188/188 ✅
```

The three totals differ **by lens, not by error**: 945 physical `SKILL.md`, 962 index skills
(alias/projection resolution), 1060 storage-layer entries.

Two inherited defects repaired so the gates pass **on merit, not by bypass**:
- `civic-whistleblower-letter/scripts/audit_letter_claims.py` — two unterminated raw-string
  literals in `FALSE_CLAIM_PATTERNS` (identical in the source snapshot, so pre-existing);
  all 6 patterns now compile.
- `artifact-emission-pipeline/templates/forgotten-well-style-dark.pptx.js` — SCAR-001
  `require()` in an ESM package; bound via `createRequire`. Both now report `✓ syntax valid`.

Recovery paths (three): on disk in `skills/` · `B7-promoted-188-skills/skills-188.tar.gz`
(2.89 MB, 189 SKILL.md verified inside) · source snapshot intact (487 + 294 SKILL.md).

### 9.5 BLOCKER — supply-chain gate false positive, repo-wide

```
/root/AAA/scripts/supply_chain_gate.py:19
PINNED = re.compile(r"^(@[^/@\s]+/)?[^@\s]+@\d+\.\d+")     # npm/uvx style only
```

`selectolax==0.4.9` in `/root/.config/opencode/opencode.json` is an exact, reproducible
**pip** pin — but the regex only accepts `pkg@x.y`, so the gate reports it "unpinned" and
**blocks every commit in /root/AAA**, mine or anyone's.

Not fixed, deliberately:
- the offending file is an **OpenCode picker config** — doctrine: picker configs are written
  only by explicit forge step, F13 holds the pen
- the fix would mean editing a **governance gate** — I will not weaken a safety gate to land
  my own commit
- another lane is **actively editing that exact value** (`selectolax<1.0` → `==0.4.9` mid-session,
  and its commit `9337e3a6` landed at 12:40:01 — 2 files, 0 of mine)

`git commit --no-verify` was **not** used.

### 9.6 Concurrent-writer incident

My 983-file staging was **wiped by another lane's git operation** between staging and commit
(`git diff --cached` went 983 → 0). The 188 skill dirs survived on disk; nothing of theirs was
staged by me (`ASI-drift-watch`, `media-ingest-lane` left untouched). Left **unstaged** on
purpose — re-staging would make the other lane's next commit trip the same gate.

### 9.7 Final state

```
disk            315G -> 311G used · 73G -> 77G avail · 82% -> 81%
pristine-full   6.4G -> 3.2G        (venv+node_modules pruned, .git gc'd, profiles PRESERVED)
health          hermes 5/5 active · 0 failed units · ack-consumer active
                site 200 · kernel :8088 200 · FED :4000 200
pushed          5 branches -> carry-pristine/* on the public fork, verified remote-side
token           ACTIVE, contained, 0 git objects, --mirror hazard neutralized
skills          188 promoted into AAA SOT storage + all 3 indexes regenerated
                git commit BLOCKED by a pre-existing gate defect (§9.5)
```

### 9.8 Two binaries for F13

1. **Supply-chain gate** — fix `PINNED` in `/root/AAA/scripts/supply_chain_gate.py` to also
   accept `pkg==x.y.z` (correct: `selectolax==0.4.9` *is* pinned), which unblocks every commit
   in AAA including this promotion? Or leave the gate alone and let the 188 sit uncommitted
   on disk (safe — three recovery paths)? A governance gate is not mine to change unilaterally,
   and another lane is mid-edit in that area.
2. **`profiles/aaa-hermes/`** (1.2 G Sept-10 snapshot) — the 188 skills are now in AAA SOT, so
   the remaining unique value is `state.db` 978 MB (live copy is 264 KB), `verification_evidence.db`,
   `auth.json`, and 149 session files. Prune the snapshot, archive it compressed, or keep as-is?

DITEMPA BUKAN DIBERI ⚒️
