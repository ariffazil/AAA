# F2 CORRECTION #3 — C7 mislabels the defect: the profile mirror is a symlink, not a copy

**Date:** 2026-09-16T02:45Z · **Actor:** HERMES (edge bridge) · **Supersedes the C7 reading in
`F2-CORRECTION-2-claude-empty-claim-2026-09-16.md` §2** · **Consequence class (C18):** one receipt.
Read-only. No skill-tree mutation (concurrent writer verified live).

---

## 1. THE MEASUREMENT THAT BREAKS THE PREVIOUS READING

Correction #2 and the 333 report both read C7 as *"the profile holds an old flat-layout copy; re-sync it."*
Those paths are **not copies**. All four are symlinks into the canonical store:

```
profile path (what C7 prints as profile_copy)                     link  target
/root/.hermes/profiles/aaa-hermes/skills/FORGE-mcp-testing         ->    /root/AAA/skills/FORGE-mcp-testing
/root/.hermes/profiles/aaa-hermes/skills/RSI-recursive-improvement ->    /root/AAA/skills/RSI-recursive-improvement
/root/.hermes/profiles/aaa-hermes/skills/KERNEL-trinity-33          ->    /root/AAA/skills/KERNEL-trinity-33
/root/.hermes/profiles/aaa-hermes/skills/reflective/sovereign-recognize -> /root/AAA/skills/reflective/sovereign-recognize
```

There is no second body at the profile path. The profile is already a clean symlink view
(consolidation `e3c582e11`, 333-AGI, 09:41 today). **C7 is comparing a resolved symlink target
against a live owner.** It is not detecting a stale mirror; it is detecting a divergence *inside
the canonical store*, and printing the wrong cause.

**Near-miss worth recording (C18):** the sibling report's remedy — *"re-sync copy basi"* — read
literally means "copy the live body over the profile path". That path is a symlink, so the write
lands **through** it on `/root/AAA/skills/FORGE-mcp-testing/SKILL.md`. The WARN would go green,
no file at the profile path would change, and one of the two canonical bodies would be silently
overwritten. Silencing the sensor is what this whole session exists to prevent; the fix as written
would have done exactly that.

## 2. WHAT IS ACTUALLY DIVERGENT — `C6` RUN ON THE CANONICAL ROOT

C6 checks the LIVE root only. Run against `/root/AAA/skills`, keyed on declared identity and with
harness variants excluded: **482 SKILL.md · 459 names · 4 names with more than one distinct body.**

| name | older body | newer body | shape |
|---|---|---|---|
| `FORGE-mcp-testing` | `51101f5b` 4784B `FORGE-mcp-testing/` | `53dd7c0f` 6584B `domains/general/forge/mcp-ops/…` | intra-canon duplicate (flat + domain) |
| `RSI-recursive-improvement` | `bbb5b812` 5750B `RSI-recursive-improvement/` | `2018d3ac` 7044B `domains/general/apex/recursive-audit/…` | intra-canon duplicate (flat + domain) |
| `sovereign-recognize` | `0cef1ae0` 5611B ×3 (`domains/apex/`, `reflective/`, `primitives/think/reflective/`) | `dd92bbf7` 5672B `domains/general/aaa/substrate/reflective/…` | intra-canon ×4, two distinct bodies |
| `KERNEL-trinity-33` | `2c45f189` 13522B `KERNEL-trinity-33/` (**canon, only body**) | `ebbcb4b4` 13582B `.hermes/skills/domains/general/aaa/catalog-ops/…` | **inverted — canonical store is BEHIND the harness** |

Three of four: canon holds both bodies, the flat one is the pre-reorg remnant, and the profile
symlink happens to point at the losing copy. One of four is the inverse: the newer body exists
**nowhere in canon**. The store is missing content the view has.

So the real defect class is **duplicate-name divergence inside the writer tree**, not profile drift.
An agent loading `/root/.claude/skills` (→ `/root/AAA/skills`) sees two `FORGE-mcp-testing` bodies and
gets whichever the loader reaches first. That is C20 SYMBOL TRUTH applied to skills: *not "does the
name exist" but "does the name mean one thing".*

## 3. TWO INSTRUMENT DEFECTS (both mine to report, neither fixed — writer live)

1. **C7 mislabels.** It compares `glob(pf, "**/SKILL.md")` against `skill_dirs(LIVE)`. Because the
   profile path resolves through a symlink, the comparison silently becomes *canon-vs-live*. Label
   says "profile copy diverged"; cause is "canon has two bodies". Fourth instance tonight of the
   same family: **a sensor whose scope is narrower than the claim it publishes.**
   Correct shape: a profile path that `os.path.islink()` into canon carries no independent copy and
   must not be reported as one; the divergence belongs to a canon-scoped check (C6 extended to
   `CANON`, with the harness-variant exclusion it already has).
2. **The consolidator's basename fallback converts a missing path into a "diverged twin."**
   `federation-skill-consolidate.py:82` — `target_rel = rel if rel.lower() in rel_ci else
   base_ci.get(name.lower())`. For `domains/general/aaa/catalog-ops/KERNEL-trinity-33` (a path canon
   does not have) the fallback matches canon's **flat** `KERNEL-trinity-33` by basename and reports
   `HOLD … diverged twin — merge is a judgement call`. It is not a diverged twin; it is a missing
   canonical path. That misclassification is why **all four C7 names sit inside the tool's HOLD=7**
   and why no scheduled instrument will ever clear them.

   Dry-run, this session: `PROMOTE=0  SYMLINK=1  FILL=0  HOLD=7  NATIVE_KEEP=350  total=358`.
   The single SYMLINK is the same basename fallback (`…/federation-topology/FORGE-act-federation-ingress`
   → canon's flat `FORGE-act-federation-ingress`), which would rewrite a domain-path view to point at
   a flat path — i.e. the taxonomy step the same tool's LAW says it preserves.

## 4. CONCURRENCY — corrected attribution

Correction #2 attributed the second writer to `gateway (01:30) + cli session (10:00)`. Measured now
from `state.db`, not from `ps`:

```
20260916_102513_b5758361  telegram  ARIF DM (267378578)  last_act 10:38:39  "tool running: execute_code"  LIVE
20260916_102513_3511be2b  telegram  ASI (8410138119)    last_act 10:35:27                                LIVE
```

The gateway is long-lived but passive; the CLI session named in #2 is the one that *wrote* that
report. **The competing writer is the sovereign's own Telegram lane, running the same audit on the
same tree right now.** Hold is against a live human lane, not against a daemon — and it clears
itself when that lane closes.

## 5. THE REMEDY, RESTATED (armed, not fired)

Not three operations on a mirror. Two, on the writer tree, and then C7 resolves on its own because
its inputs do:

1. **Converge intra-canon duplicates onto the newer body** — `FORGE-mcp-testing`,
   `RSI-recursive-improvement`, `sovereign-recognize`: replace the stale path with a symlink to the
   live domain path (same shape the consolidation already uses: one body, two paths).
2. **Promote the inverted one** — `KERNEL-trinity-33` 09-15 (`ebbcb4b4`) from the harness view into
   `skills/domains/general/aaa/catalog-ops/KERNEL-trinity-33`, then symlink the flat path. This is
   the direction that must not be done blind; it is the only one of the four that adds content
   rather than removing a remnant.

Then: fix C7's label, extend C6 to `CANON`, and put `base_ci` behind a path-existence test in the
consolidator. Rollback manifest pattern already exists (`/root/skill-audit/rollback-manifest.json`).

**NOT FIRED.** Reason in §4: a live sibling session is measuring this tree. Two writers on one skill
migration is a race with no upside, and a census that lands mid-migration publishes a wrong number —
the exact defect this session was convened to remove.

## 6. VERDICT

| Item | State |
|---|---|
| "profile holds a stale copy" (report #2, 333 §4) | **WRONG — all four profile paths are symlinks into canon** |
| C7 label | **MISLABELLED — reports profile drift, measures canon duplication** |
| Real defect | **4 names with duplicate divergent bodies inside `/root/AAA/skills`** |
| `KERNEL-trinity-33` | **canon BEHIND harness — 09-15 body exists nowhere in canon** |
| Consolidator HOLD=7 | **2 of 7 are basename-fallback artefacts, not diverged twins** |
| Live writer | **sovereign's Telegram lane (b5758361), 10:38:39 — hold clears with that lane** |
| Mutation | **NONE. Kernel floors / FLOOR_TABLE / arifOS untouched** |

DITEMPA BUKAN DIBERI ⚒️
