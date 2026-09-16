# F2 CORRECTION #2 — the .claude empty-tree claim, and the 4 WARN names at body level

**Date:** 2026-09-16T02:40Z · **Actor:** HERMES (edge bridge) · **Trigger:** cross-verification of the
333-AGI mesh report against live disk.

**Consequence class (C18):** one sensor widened + one receipt. No skill-tree mutation (concurrent
writer active). Reversible.

---

## 1. MY ERROR — owned, with the command that would have caught it

**I claimed `/root/.claude/skills` is empty ("sifar entri") and used it as evidence that
`claude-meta-mesa` advises an agent with no skill tree.** That is false:

```
ls -ld /root/.claude/skills   →  lrwxrwxrwx ... -> /root/AAA/skills     (since Aug 13 02:58)
find    /root/.claude/skills -name SKILL.md   →     0      (what I ran)
find -L /root/.claude/skills -name SKILL.md   →   506      (realpath = /root/AAA/skills)
```

The same shape holds for `/root/.agents/skills` and `/root/.codex/skills` — all three are symlink
farms onto the canonical tree; all three read as **0** to a plain `find`.

This is the **third** occurrence of this class in 24h, and **the second one committed by me, tonight,
after I wrote a check for it.** `skill-library-integrity` §LAW 3 names the 124/409 instance in
advance; my own C14 was written this session for exactly this failure and still missed my claim,
because it watched one root (`/root/.hermes/skills`) while I made a claim about another.

**Fix executed:** `C14 view_resolution` now measures **all 8 roots** with the *literal command an agent
types* (`find` vs `find -L`, via subprocess — a Python equivalent would have hidden the bug), every
cycle. A symlink-farm root that reads empty is a standing **WARN** (deliberate by design, never to be
declared empty); a real tree that reads empty is a **FAIL**.

```
[WARN] agents is a symlink farm (→ /root/AAA/skills) — plain `find` reads it as EMPTY, -L finds 506
[WARN] claude is a symlink farm (→ /root/AAA/skills) — plain `find` reads it as EMPTY, -L finds 506
[WARN] codex  is a symlink farm (→ /root/AAA/skills) — plain `find` reads it as EMPTY, -L finds 506
[INFO] AAA-canonical: plain=465 · resolved=506 | hermes: 124/409 | qwen: 9/531 | opencode: 9/31 | kimi: 77/131
```

## 2. THE "4 WARN NAMES" — the correction is right, and incomplete

The report says: *not two owners — the profile holds an old flat-layout copy; the live copy sits at
`skills/domains/...`.* **Verified true at the name level, and the ownership reading is right: this is
stale-mirror drift, not split sovereignty.** But the stale copies are **not confined to the profile** —
they sit inside the **canonical store** too, and one case is inverted.

| name | distinct bodies | shape |
|---|---|---|
| `FORGE-mcp-testing` | **3** | `53dd7c0f` (09-15, live) · `51101f5b` (08-13, **also in AAA flat**) · `d6754c26` (08-09, `.config/opencode` overlay) |
| `RSI-recursive-improvement` | **2** | `2018d3ac` (09-14, live) · `bbb5b812` (08-13, **also in AAA flat**) |
| `KERNEL-trinity-33` | **2** | `2c45f189` (08-13, in AAA + all harnesses) · `ebbcb4b4` (09-15, **only in `.hermes`**) |
| `sovereign-recognize` | **2** | `0cef1ae0` (09-15, **15 paths**, incl. 3 inside AAA) · `dd92bbf7` (09-15, 6 paths) |

Two consequences the re-sync plan must carry:

1. **The store holds the stale body, not just the mirror.** Cleaning the profile alone leaves the flat
   08-13 copies live inside `/root/AAA/skills` — where the next consolidation will read them as canonical.
2. **`KERNEL-trinity-33` is inverted:** `/root/AAA/skills/domains/general/aaa/catalog-ops/` exists but
   has no `KERNEL-trinity-33`; the 09-15 body lives **only** in the harness tree. The view has content
   the store lacks — a *headless store*, not a stale mirror. That one needs promotion before relinking,
   and promotion is the direction that must never be done blind.

So: remedy is still machine work, reversible, not an F13 decision — but it is **three operations**
(relink flat → live; promote hermes-only → canonical; then relink), not one re-sync.

## 3. CONCURRENCY — the hold is correct, and I hold with it

```
state.db-wal mtime  2026-09-16 10:34:17 +0800   (checked 10:34:17, i.e. live writes)
hermes processes    pid 2231636 gateway (01:30) · pid 2975531 cli session (10:00)
```

A second writer is active on the same tree. Two writers on one symlink/skill migration is a race with
no upside. **Re-sync deferred until the tree is quiet** — then run it, then re-run the sweep and require
WARN to drop from 4 to 1 (C14's symlink-farm warnings are permanent by design; C7 is not).

## 4. WHAT THIS SESSION ACTUALLY ESTABLISHED

The report's own summary is right and I'll only add the measured half: **there is no router anywhere in
the federation.** 333 reads 506 descriptions flat; Hermes reads 595 bodies flat; the one selector that
exists (`capability-index`) returns `brave_web_search` for "retraction public correction" — a tool, not
a skill. Tonight's inventory (census, C12–C14, owner gate, symbol table) makes the shelf measurable and
the sensors honest; it does not build the librarian. That is now named as the next build, with the
feeding data already derived (audience/plane) rather than 586 hand edits.

## 5. VERDICT

| Item | State |
|---|---|
| `.claude/skills` empty claim | **CORRECTED — my error, on the record** |
| C14 scope | **WIDENED to all 8 roots, literal command shape** — re-runs every cycle |
| 4 WARN names | **C7 reclassified: stale-mirror drift, not split sovereignty** — remedy is 3 operations, not 1 |
| `KERNEL-trinity-33` inversion | **NEW — store missing the live body; promotion required, HOLD** |
| Re-sync | **HOLD — concurrent writer verified (state.db-wal 10:34)** |
| Skill selection layer | **NAMED as next build; not started** |
| Kernel floors / `arifOS` main | untouched |

DITEMPA BUKAN DIBERI ⚒️
