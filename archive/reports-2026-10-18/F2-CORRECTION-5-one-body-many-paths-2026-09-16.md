# F2 CORRECTION #5 — two sensors were publishing false causes; the store is now one body per skill

**Date:** 2026-09-16T03:05Z · **Actor:** HERMES (edge bridge, session `20260916_103651_63c575`)
**Supersedes:** CORRECTION #3 §2 (C7 reading) and CORRECTION #4 §3 (which keyed on the wrong field).
**Consequence class (C18):** sensors corrected + 7 store operations, routing unchanged, fully
reversible (quarantine + git). No kernel/canon/floor surface touched.

---

## 1. THE OTHER LANE'S RECEIPTS — VERIFIED, ONE WRONG

| Claim | Verdict |
|---|---|
| `7e5d8b3` — drop the C14 listing-vs-walk predicate + wire the suite into C12 | **VERIFIED.** In `/root/scripts` (its own git repo — my first check looked in AAA and said "no-such-object"; the object was real, my search root was wrong). Diff = 25 lines + 143-line regression suite. |
| C14 first version could FAIL a healthy tree | **VERIFIED** — and the pinned negative case is real: `tests/test_c14_view_resolution.py` R4 constructs listing=3/resolved=3 and asserts the superseded predicate misfires. Suite passes 9/9, runs every cycle via C12. |
| Sweep live: `fail=0 warn=4`, no new false alarms | **VERIFIED at the time.** `warn=4` = 1×C7 + 3×C14. |
| Three symlink-farm WARNs are a level decision for the owner | **DECIDED and executed** (§3). |
| `FEDERATED_SKILLS_REGISTRY_V3` stale at 481 | **NOT ANYMORE.** `disk_reconciliation.refreshed = 2026-09-16T02:37:01Z` (10:37 local), `canonical_skills: 482` = disk. The cron the other lane predicted did re-sync. |
| *"Profile simpan copy flat-layout lama… remedy dia re-sync"* | **WRONG — and its remedy was a corruption path** (§2). |

## 2. `C7` PUBLISHED A FALSE CAUSE, AND THE REMEDY WOULD HAVE OVERWRITTEN CANON

Proof by inode — the profile path and the canon path are the same file:

```
FORGE-mcp-testing           profile inode 5333599 == canon inode 5333599   → /root/AAA/skills/FORGE-mcp-testing
RSI-recursive-improvement   profile inode 5334035 == canon inode 5334035   → /root/AAA/skills/RSI-recursive-improvement
KERNEL-trinity-33           profile inode 5334168 == canon inode 5334168   → /root/AAA/skills/KERNEL-trinity-33
reflective/sovereign-recognize profile inode 5329896 == canon inode 5329896 → /root/AAA/skills/reflective/sovereign-recognize
```

They are **symlinks**, created by consolidation `e3c582e11` (09:41 today). `C7` compared that
resolved target against the live owner and printed the difference as *"profile copy diverged"*.
The remedy that label implies — copy the live owner over the profile path — **writes through the
link onto a body inside the canonical store** and silences the warning by overwriting canon.

That is the fourth instance tonight of one family: **a sensor whose scope is narrower than the
claim it publishes.**

## 3. WHAT WAS EXECUTED

**`/root/scripts/hermes-chaos-sweep.py`** (commit `55661ac`) — `C7` now reports a profile path that
resolves into canon as an **INFO view**, never a copy, and says where the divergence really lives.
New checks placed where the defect is, each stating which frontmatter field it keys on:

```
C15 canonical_id_duplicate     keyed on  id:     6 → 3   WARN
C17 canonical_route_duplicate  keyed on  name:   4 → 0   WARN
C16 canonical_case_twin        case-twin family  5 → 4   WARN (divergent)
C7  profile_stale_mirror       view, not copy           INFO
C14 symlink-farm               by-design property       WARN → INFO
```

**Why `C17` is the one that matters:** the loader reads `name:`
(`tools/skills_tool.py:275 frontmatter.get("name", <folder>)`) and dedupes **FIRST-WINS** — two
bodies sharing a routing name means one can never load, chosen by walk order, silently. `id:` and
`name:` are different strings by design (`id: aaa-agent-invariants` / `name: ASI-agent-invariants`),
which is why a check must say which one it keyed on. My first version of `C15` returned `id:`
whenever `id:` preceded `name:` — i.e. always — so it was keyed on the id while claiming to be keyed
on the name. **Caught because two of my own implementations disagreed (7 vs 4) and I would not
commit a sensor that failed its own test.** `declared_name()` becomes `declared_identity()`
returning both.

**`C14` WARN → INFO:** a by-design property can never clear, and a warning that can never go green
stops being read (attention-kill criterion). The instruction text is the value; the level was noise.
The verdict line now means something: `warn=3`, all three a real store decision.

**`/root/scripts/skill-store-converge.py`** (new) + **applied, 7 operations, committed `d8e38ad43`**

Rule derived at run time, never hardcoded: survivor = newest `SKILL.md`; a pair converges **only if**
(1) no file exists in the loser that is absent from the survivor, **and** (2) the routing `name:` is
identical. Otherwise HELD with the reason named. Action is `mv` to quarantine + a relative symlink —
**path count preserved, body count one, nothing deleted.**

```
APPLIED (7)   routing name identical, loser a strict content subset
  FORGE-mcp-testing · RSI-recursive-improvement · FORGE-document-intelligence
  COPILOT-zen-router · caller-trace · cognitive-level-assertion-protocol · sovereign-recognize
HELD (5)      name choice is routing is agent behaviour → not the tool's call
  trinity-33-canonical → kernel-trinity-33        (routing would change)
  FORGE-act-federation-ingress → forge-act-…       (routing would change)
  FORGE-artifact-publisher → forge-…               (routing would change, case)
  RSI-federation-mesh → rsi-…                      (routing would change)
  agent-onboarding — 35 lines + 6 files exist only in the loser  (merge, not dedupe)
```

**Verified after:** `find -L` canon 506 → **506** (no path lost) · loader 409 → **409** (no
capability lost) · sweep `C15 6→3`, `C17 4→0`, `C16 5→4` · git records the 7 as mode `120000`
symlinks, so a fresh checkout reproduces them · 19 files changed, exactly the intended paths.

**New standing trap, recorded not hidden:** plain `find` on canon now reads **458**, not 465 — seven
canonical paths are views now. That is precisely what `C14` exists to catch, and it is the same
property the harness roots already have.

**The tool found three of its own bugs before shipping** — each caught by a dry run, none fired:
1. it merged `apex_verdict_hold/hermes` with `apex_verdict_seal/hermes` (two different skills whose
   *variant* subdirs share a folder name) and would have replaced one skill's body with a link to
   another's;
2. the first fix ("parent holds SKILL.md") leaked on `FORGE-onboarding/` (a stale container with
   only `claude/` and no SKILL.md);
3. the second fix ("parent holds ≥2 harness children") leaked on the same dir.
The shipped test is the plain shape check, with the reason it is safe written next to it.

## 4. WHAT THIS CHANGES FOR THE OPEN QUEUE

- **`KERNEL-trinity-33`** stays F13: two bodies, one shared `id: trinity-33-canonical`, two different
  routing names. Content is a strict subset — the *only* open question is which name routes. Answer
  `kernel-trinity-33` and the pair converges mechanically in one command.
- **The other four HOLDs** are the same shape: a routing name would change, or content exists only in
  the loser. Three are a rename; one (`agent-onboarding`) is a real merge with 35 unique lines.
- **Hermes's own loader scans exactly one tree** (`/root/.hermes/skills`, 409 skills). The canonical
  store is **not** in its routing table at all. Its trinity entry is `trinity-33-canonical` — i.e.
  Hermes currently routes to the *fork's name*. That is a routing fact worth one decision, and it is
  the same decision as §4 above.

## 5. VERDICT

| Item | State |
|---|---|
| `7e5d8b3` / C14 fix / regression suite | **VERIFIED — real, wired, runs every cycle** |
| `C7` label | **FIXED — a resolving profile path is a view, never a copy** |
| My first `C15` (keyed on the wrong field) | **CAUGHT BY SELF-TEST before commit — fixed at the root** |
| Registry `481` | **not stale — refreshed 10:37, says 482** |
| Store | **7 families converged, 5 held with the reason named** |
| Paths / capability after | **506 → 506 paths · 409 → 409 loadable** |
| Routing changed | **none** |
| Kernel floors / FLOOR_TABLE / arifOS | **untouched** |

DITEMPA BUKAN DIBERI ⚒️
