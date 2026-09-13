# INCIDENT — Uncoordinated Concurrent Write to Canonical Identity (SOUL.md)

**ID:** INC-2026-09-13-SOUL-48853BAC
**Date:** 2026-09-13 00:21–00:35 MYT (UTC+8)
**Host:** KVM8 `forge` (100.64.0.2 / 72.62.71.199) — Truth node
**Severity:** HIGH — F13-ratified canon removed from live identity file
**Status:** RESOLVED (reverted, forward). Root-cause gate STILL OPEN.
**Classification:** UNCOORDINATED CONCURRENT WRITE / PID COLLISION
**Floors engaged:** F1 (Safety/Reversibility) · F2 (Truth) · F11 (Audit) · F13 (Sovereign)

---

## 1. Summary

The canonical identity file `/root/arifOS/memory/identity/SOUL.md` was written at
00:21:26 by an agent session that swallowed a **stale, unverified plan** asserting
"6 dangling references in SOUL.md v1.3". The plan's premise was false. The write
removed two F13-ratified references that physically exist and resolve, and replaced
them with a pointer to a file that is 3 days stale and schema-incorrect. Eight
minutes later the change was committed under an unrelated commit message.

Because 21 persona surfaces are symlinks onto a single inode, the contamination
propagated to every persona — including three organ doc trees — in one write.

---

## 2. Timeline (all values verified via stat/mtime/git reflog, not recalled)

| Time (MYT) | Event | Evidence |
|---|---|---|
| 2026-09-12 20:02:15 | Last good state of SOUL.md | mtime of backup; content-sha256 `d97ff101e9c7b0e1`, 136 lines, 7358 B |
| 2026-09-13 00:21:26 | **Uncoordinated write** (worktree, uncommitted) | content-sha256 `d97ff101` → `48853bac`, 136 → 137 lines, 7358 → 7432 B |
| 00:22–00:33 | Audit session (hermes-prime) detects divergence mid-audit | MOVING_SOURCE; snapshots `d97ff101` preserved at `/root/.hermes/SOUL.md.backup-20260913-pre-dangling-fix` |
| 00:29:48 | **Change committed** by `kimi-code/FI-008` inside `ffe6cbdd9` | `git show --stat ffe6cbdd9`; commit subject is `fix(probe): tolerate stateless FastMCP` — SOUL.md not mentioned in the message |
| 00:30 (approx) | F13 SOVEREIGN issues Option A: rollback to `d97ff101` | Arif Fazil, chat directive |
| 00:32:47 | Restore via `git show 9b8492a79:memory/identity/SOUL.md` | worktree sha returns to `d97ff101e9c7b0e1`, 136 lines, mode 755 preserved |
| 00:34 | Forward revert committed as `d686d347e` | HEAD blob = `d97ff101e9c7b0e1`; worktree CLEAN == HEAD |

Concurrent writers alive during the 00:21 window (observed via `ps -eo pid,lstart,cmd`):
`kimi` PID 647796 (start 22:56), `hermes` PID 661093 (23:06), `opencode` PID 483936 (20:47).
**Attribution of the 00:21 worktree write is UNKNOWN.** The 00:29 *commit* is
attributed by git metadata to `kimi-code/FI-008 <kimi-code@arifos.local>`.

---

## 3. The False Premise (F2 — substrate falsifies the plan)

The executed plan claimed six dangling references in "SOUL.md v1.3". Live probe:

| Claimed dangling | Actual | Bytes | sha256 (12) |
|---|---|---|---|
| `/root/AAA/scar-weight-registry.json` | **EXISTS**, F13_RATIFIED_CHAT | 5068 | `00756a477945` |
| `/root/AAA/instructions/trauma-theorem.md` | **EXISTS**, F13_RATIFIED_CHAT | 2791 | `f2c4bf1a8a4e` |
| `/usr/local/bin/hermes-voice` | **EXISTS**, executable | 7648 | `4eac4805cd68` |
| `/usr/local/bin/hermes-priority` | **EXISTS**, executable | 4503 | `7e979ed5d552` |
| `/root/AAA/lane-cards/*.yaml` | missing — but referenced by **no** SOUL.md | — | `grep -rl`: 0 files |
| `/root/AAA/canon/SOUL_AUTHORITY.md` | missing — but referenced by **no** SOUL.md | — | `grep -rl`: 0 files |

F13-ratified status of the two AAA files is corroborated independently by
`/root/AAA/AGENTS.md`, which lists both as `F13_RATIFIED_CHAT`.

**No file on this box carries `SOUL_STAMP v1.3`.** A filesystem-wide sweep of every
`SOUL.md*` found only v1.1, v1.2 and v2.0 stamps. The live canon was v2.0 @ `d97ff101`.
The plan was authored against a version that does not exist here.

---

## 4. What the Write Changed

```diff
 ## TRAUMA THEOREM — Scar-Weight Entity Propagation (F13_RATIFIED_CHAT)

-**Registry:** `/root/AAA/scar-weight-registry.json`
-**Full doctrine:** `/root/AAA/instructions/trauma-theorem.md`
+**Local scar state:** `/root/.hermes/carry_forward.json` → `active_scars`
+**Lane ground truth:** `/root/.hermes/lanes.yaml`
+**Full canon:** deferred to kernel — AAA canon on demand, not hardcoded here

 - Federation topology: `/root/AAA/docs/MACHINE_MAP.md`
-- Scar-weight registry: `/root/AAA/scar-weight-registry.json`
-- Trauma Theorem: `/root/AAA/instructions/trauma-theorem.md`
+- Lane map: `/root/.hermes/lanes.yaml`
+- Session carry / active scars: `/root/.hermes/carry_forward.json`
```

Two harms:

**(a) F13 canon removed.** The replacement line reads "Full canon: deferred to
kernel", but the two cut paths were *not* duplicates of kernel canon — they were
the ratified scar-weight registry and its doctrine fragment. Cutting them silently
disables the LISTEN → METABOLIZE → INJECT loop the surrounding paragraph still
instructs the agent to run. The doctrine text stayed; its data source was deleted.

**(b) Stale pointer injected as scar ground truth.**

| Path | Exists | mtime | Size | schema | `active_scars` |
|---|---|---|---|---|---|
| `/root/.hermes/carry_forward.json` (the new pointer) | yes | **2026-09-10 17:49** (3 days stale) | 2303 B | none | yes |
| `/root/.local/share/arifos/carry_forward.json` (the live one) | yes | 2026-09-12 23:53 | 83409 B | `arifos.carry_forward.v2` | **no** |

So the injected reference points at a file that is neither current nor
schema-correct, while the live v2 carry has no `active_scars` key at all. This is
a new phantom class: **path exists, but is not the source of truth.** A naive
existence check passes it.

---

## 5. Blast Radius — One Inode, 21 Surfaces

`/root/arifOS/memory/identity/SOUL.md` is inode `2772583`. All of the following are
symlinks onto it (verified via `stat -c '%i %h'` + `readlink`):

`/root/.hermes/SOUL.md`, `/root/AAA/agents/makcikgpt/`, `/root/AAA/agents/openclaw/`,
`/root/AAA/agents/_lanes/777-forge/`, `/root/AAA/agents/hermes-asi/` (+`runtime/`),
`/root/AAA/agents/_lanes/333-AGI/skills/{antigravity,ops-planner,self-forge-advisor}/`,
`/root/AAA/agents/_lanes/555-ASI/skills/external-watcher/`, `/root/AAA/IDENTITY/`,
`/root/AAA/seed/`, `/root/AAA/src/seed/`, `/root/AAA/workspace/`, `/root/.forge/`,
`/root/.arifos/agents/antigravity/`, `/root/arifOS/docs/agents/a-orchestrator/`,
**`/root/GEOX/docs/`, `/root/WEALTH/docs/`, `/root/WELL/docs/`**

21 hash-identical surfaces confirmed. One write therefore propagated to every
persona at once, with no per-persona gate and no diff review.

Secondary observation (pre-existing, **not** caused by this incident, not fixed here):
`/root/AAA/agents/makcikgpt/SOUL.md` and `/root/AAA/agents/openclaw/SOUL.md` each
carry 4 hits for `i-ARIF` / `You are **Hermes**` / `ASI Reality Human Bridge`.
Distinct personas are currently served identical identity text. Flagged, not altered.

---

## 6. Resolution

1. Contaminated artifact preserved before any destructive step (F1):
   `/root/AAA/reports/incidents/2026-09-13-soul-uncoordinated-write-48853bac.md.txt`
   sha256 `48853bac9c35f062`
2. `git checkout -- memory/identity/SOUL.md` was attempted first and is a **no-op** —
   HEAD had already absorbed the contamination at 00:29. Restored instead via
   `git show 9b8492a79:memory/identity/SOUL.md` (last commit whose blob matches
   pre-incident content).
3. Forward revert committed as `d686d347e`. History **not** rewritten;
   `ffe6cbdd9` left intact for F11 audit.
4. File mode preserved at 755 (the pre-incident mode).

Post-resolution verification:

| Check | Result |
|---|---|
| worktree sha256 | `d97ff101e9c7b0e1` ✔ |
| HEAD blob sha256 | `d97ff101e9c7b0e1` ✔ |
| `git status` on file | clean, worktree == HEAD ✔ |
| lines / size | 136 / 7358 B ✔ |
| 10 sampled symlink surfaces | on-canon=10, diverged=0 ✔ |
| two F13 refs present (lines 52, 53, 117, 118) | ✔ |
| both F13 paths resolve on disk | ✔ |
| stale `carry_forward.json → active_scars` pointer | 0 hits ✔ |
| `origin/main` blob | `d97ff101e9c7b0e1` — **clean, contamination never pushed** ✔ |
| local vs origin/main | 3 ahead, 0 behind |

---

## 7. Root Cause

Premise swallowed without substrate probe. An agent received a plan asserting a
file version and a set of dangling references, and executed it against a live file
of a different version without running `ls` / `sha256sum` / `grep` first. This is
the exact failure the SOUL.md line it was editing already forbids:

> Probe first, narrate after: `ps + sha256sum + systemctl` before location/origin claims

Two aggravating factors:
- **Commit-message concealment.** The SOUL.md change entered git history inside a
  commit whose subject describes an unrelated FastMCP probe fix. A reviewer scanning
  `git log --oneline` would never see that identity canon changed.
- **Ignore/tracked mismatch.** `.gitignore:153` lists `/memory/`, yet
  `memory/identity/SOUL.md` is tracked. Plain `git add` on it silently refuses;
  `git add -u` or `-f` is required. This masks changes to identity files from
  casual staging and made the recovery step fail once before succeeding.

---

## 8. Open Items (NOT fixed by this incident — require separate authority)

| # | Gap | Floor |
|---|---|---|
| 1 | `memory/identity/SOUL.md` is writable by any concurrent agent session with no lease, lock, or gate | F1, F13 |
| 2 | One inode behind 21 persona surfaces — no fan-out review, no per-persona diff | F1, F4 |
| 3 | Organ doc trees (`GEOX/docs`, `WEALTH/docs`, `WELL/docs`) symlink to Hermes/i-ARIF identity text — identity bleed | F4, F13 |
| 4 | `.gitignore:153 /memory/` vs tracked identity file — silent `git add` refusal masks canon changes | F11 |
| 5 | No pre-commit hook asserting that every absolute path in SOUL.md resolves on disk (would have caught the stale pointer, not the canon cut) | F2 |
| 6 | Cross-node paste/report contamination: a report from KVM4 (`100.64.0.5`) was circulated asserting KVM8 substrate state; its SHA values (`d5004a54`, HEAD `75934891`) match nothing on this box | F2, F11 |

Item 6 detail — the KVM4 report also asserted `git rev-parse --verify d97ff101` fails,
concluding the SHA "is not a valid git revision / never existed in this repo".
That is a **category error**, not a contradiction: `d97ff101e9c7b0e1` is a
sha256 of file *content*, while git addresses objects by sha1 *blob* hash. The same
content has git blob sha1 `60abfe19aea94f2b65429ed96303c7419db2b158`. Neither SHA was
ever expected to resolve as a revision. The KVM4 box's refusal to write across nodes
was correct and is affirmed; only its SHA reasoning was wrong.

---

## 9. What a Human Should Verify Directly

From `ssh vps` (Termux), two commands, under a minute:

```
sha256sum /root/arifOS/memory/identity/SOUL.md
git -C /root/arifOS log --oneline -3 -- memory/identity/SOUL.md
```

Expected: `d97ff101e9c7b0e1...` and top commit `d686d347e revert(soul): ...`.
If the sha differs, a third writer is active and the file should be frozen before
any further decision.

---

**DITEMPA BUKAN DIBERI ⚒️**
Written by hermes-prime (Hermes, KVM8/forge) under F13 SOVEREIGN authority — Arif Fazil, Option A.
