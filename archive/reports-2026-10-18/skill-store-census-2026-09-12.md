# TIER 1 — Skill-Store Census: Dispute Settled

> **Date:** 2026-09-12 ~01:20 MYT (Asia/Kuala_Lumpur)
> **Authority:** ARIF (F13 SOVEREIGN) directive — "Proceed to Tier 1 Audit: Settlekan dispute nombor skill stores dulu. Jangan bina archive gate atas data yang tak tally."
> **Actor:** hermes-asi (aaa-hermes profile, session 20260912_003048_fd509c)
> **Status:** SETTLED — and the settlement falsifies both prior numbers.
> **Data artifact:** `/root/AAA/reports/skill-store-census-2026-09-12.json`
> sha256 `5d0f82d40cc757b184ae073d09c1b6f0ed7fc561dc40b80db14427b08abc2e27`
> **Method:** `/root/AAA/scripts/skill_store_census.py` (absolute roots, relative-path keys)

---

## 1. The dispute

Three numbers for the same store, same absolute path, same night:

| Source | Time | hermes_live | archive |
|---|---|---|---|
| My probe (`find … \| wc -l`) | ~00:37 | **213** | — |
| Prior session paste | ~21:25 | **353 loadable** | **37 archived-only** |
| My census v1 | ~01:14 | **339** | 32 |
| My census v2 (corrected) | ~01:18 | **351** | **32** |

Per F13 directive, no archive gate may be built on this. Correct — but the reason is stronger than "numbers disagree."

## 2. Root cause: the store was being restructured *during* measurement

`/root/.hermes` is a git repository. Witnessed from `git log`:

- **`5403fa7`** — *"1095 skill files deleted from Hermes (canonical lives in AAA/skills + /root/.agents/skills per 2026-08-26 zen consolidation)"*
- **`e37f8fe`** — *"+ new warga/counseling/federation-health skills + aaa-hermes profiles"*
- **Last commit `8376d3e`** — 2026-09-12 **00:40:16 +0800**, an escalation fix from a *different* session.

Tracked vs disk right now:

    git ls-tree -r HEAD --name-only -- skills | grep -c 'SKILL.md$'   ->  162
    find skills -name SKILL.md | wc -l                                ->  351
    git status --porcelain skills | grep -c '^??'                     ->  174 untracked

My **213** was a true snapshot at 00:37 — taken *before* the 00:40 commit wave.
The paste's **353** was a true snapshot at ~21:25 — a different point in the same restructuring.
**Neither was wrong. Both were stale on arrival.**

Concurrency witness: **12 distinct session IDs** active tonight in `agent.log`
(`20260911_211551_48e3170f`, `_91bf5b1c`, `20260912_002807_2e79d10a`,
`_003048_fd509c`, `_004445_3f85b790`, `_005640_b0089a0f`, `_005706_f3a574`, …),
plus **31 `Refusing background curator patch`** events, plus `tools/skills_sync.py`
which runs at every startup and relocated `FORGE-act-federation-ingress` ↔
`FORGE-sct-federation-ingress` **6 times** between 11:28 and 00:57.

`.bundled_manifest` mtime = **00:57:08** — 276 entries, rewritten mid-audit.

## 3. My own third measurement artifact (scar class repeat)

Census **v1 reported 339. That was my defect, not the system's.**

v1 keyed skills by `basename(realpath(dir))`. That collapses legitimately distinct
skills sharing a leaf name:

    audit-seal/SKILL.md        vs  substrate/audit-seal/SKILL.md
    apex_verdict_hold/claude/  vs  apex_verdict_seal/claude/  vs  FORGE-onboarding/claude/
    know-physics/              vs  knowledge/know-physics/

11 colliding names → **12 files erased from the count**. 339 + 12 = 351.

v2 keys by **relative path from store root** and uses leaf-names only for
cross-store set math. Corrected.

**This is the third measurement artifact I produced tonight, same class as scar #2**
("49 skill mati" from a relative-path bug): *output preceded verification*.
Caught by my own reconciliation pass before the number was reported to you — which
is the control working, not the failure absent.

## 4. Settled numbers (snapshot 2026-09-12 01:18 MYT, stability-checked 3×)

| Store | SKILL.md files |
|---|---|
| `/root/.hermes/skills` (live) | **351** |
| `/root/AAA/skills` (live) | **213** |
| `/root/.hermes/profiles/aaa-hermes/skills` (live) | **291** |
| `/root/.hermes/skills-archive` | **246** |
| **archived-only** (in archive, in no live store) | **32** |

Stability re-check: `351 / 351 / 351` across three samples 2 s apart — currently quiescent.
Zero symlinked SKILL.md files, zero symlinked dirs, zero cross-store realpath sharing
(so no double-counting from symlinks).

The 32 archived-only names are listed in the JSON artifact. They include
`human-paradox-geometry`, `chat-image-generation`, `fed-vision-architecture` —
the same three the prior session flagged as Class B HOLD (34 / 18 / 10 uses).

## 5. Consequence for Tier 2 (archive gate)

**A count-based gate cannot be built on this store.** Not because the count is wrong
now — because the count has **no stable referent** while sibling sessions restructure it.

The gate must key on **identity + provenance**, not on a total:

    per-skill: name, store, use_count, patch_count, first_seen_commit, last_seen_commit

`use_count` and `patch_count` live in `/root/.hermes/skills/.usage.json` and
`.curator_ledger.jsonl` (both modified tonight). A gate reading those survives
restructuring; a gate reading `wc -l` does not.

The 2026-09-09 curator event that archived 37 skills *"tanpa sesiapa tahu"* —
including one with 34 uses — is the exact failure this design must catch.
Keying on per-skill usage makes that unrepeatable regardless of what the total does.

## 6. What I did NOT do

- No archive restoration (F13 out of scope).
- No identity reconciliation (F13 out of scope) — the 174 untracked SKILL.md files
  and the `162 tracked vs 351 on disk` gap are **reported, not resolved**.
- No `run_turn.py` patch, no gateway restart (Option A deferred by F13 verdict NO).
- No writes to `SEALED_EVENTS.jsonl`.

## 7. Open loops handed forward

1. **174 untracked SKILL.md** in `/root/.hermes/skills` — `git status` shows `174 ??`.
   Witness-restore incomplete, or deliberate? Owner: whoever runs F13 triage #4.
2. **162 tracked vs 351 on disk** — HEAD does not describe the live catalogue.
3. **12 concurrent sessions mutating one store** with 31 curator refusals — no
   locking discipline witnessed. This is the real Tier 2 finding.
4. **`skills_sync` rename oscillation** (`act` ↔ `sct`, 6 times) — a bundled-skill
   name conflict fighting itself on every startup.

DITEMPA BUKAN DIBERI ⚒️
