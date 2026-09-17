<!-- SOT: execution record. Tier: EXECUTED under F13 greenlight 2026-09-18 (S3 + 37 borrowed bodies). -->
# S3 EXECUTED — collapse complete: 44 shared names → 2, bodies repatriated 37 → 0
> Forged: 2026-09-18 · KVM8 (forge, 100.64.0.2) · Hermes ASI session
> Authority: F13 greenlit S3 twice (*"Jalan S3… bawa balik diff receipt bila divergence ini dah
> di-collapse sepenuhnya"*). Anchor: tag `v2026.09.18-skills-audit` + bundles under
> `/root/AAA/backups/skill-collapse-20260918/`.
> **Every body captured before mutation. `RESTORE.sh` regenerates both sides from the backups.**

---

## 0. The decisive probe that changed the plan (recorded before any mutation)

```
live install /usr/local/lib/hermes-agent   (HERMES_HOME=/root/.hermes)
  skills_dir       = /root/.hermes/skills    <- the READ surface
  external_dirs    = []                      <- AAA is NOT loaded
  skill_create_dir = /root/AAA/skills        <- the WRITE surface
```

Two things followed:

1. **My earlier warning was wrong and I retract it.** I wrote that `hermes update` would overwrite a
   symlink at the updater path. Reading `tools/skills_sync.py` shows the opposite:
   `_update_existing_skill` → if the copy does not match the origin hash it is appended to
   `user_modified` and **kept** (`"~ {name} (user-modified, skipping)"`); `_install_new_skill` says
   *"yours was kept"*; and user-deleted bundled skills are **not re-added**. A diverged or symlinked
   copy is safe. The bundled set never needed pinning — I inferred a blocker instead of probing it.
2. `_defer_to_external` says an `external_dirs` source creates a **name collision the loader refuses**.
   So "just set external_dirs" is not a free fix — it collides with every duplicate name that exists
   in both trees. That is a design constraint on the reachability work, not a detail.

## 1. What was executed

**S3 — one body, one address.** Body in AAA (the write surface); the `.hermes` entry becomes the
read-surface address. Collapsed **42 names** (26 diverged + 14 byte-identical duplicates + the two
covered by a parent container link):

| Class | n | Action |
|---|---|---|
| `aaa_superset` (capability_tier + ecology_state + `[fed:]` marker) | 16 | AAA body kept |
| `merge_union` (AAA governance block + `.hermes` `owner`/`risk_tier` frontmatter) | 6 | **union**: AAA body, `.hermes`-only frontmatter keys merged in |
| `aaa_newer` | 2 | AAA body kept |
| byte-identical duplicates (`core/*`, `knowledge/know-*`) | 13 | collapsed to one body |
| covered by a parent container link (`warga/constitutional`, `…/identity-invariance`) | 2 | resolved by construction |
| **HELD for F13** (`APEX-humility-godel`, `fi-mesh-check`) | 2 | **untouched** — two different designs, your call |

**Borrowed bodies — 37 → 0.** AAA no longer holds a single entry whose body lives outside AAA:

```
12  were borrowed from a runtime PROFILE  (…/profiles/aaa-hermes/skills/)  -> body now in AAA
16  were borrowed from the .hermes tree                                     -> body now in AAA
 9  were borrowed from /root/.understand-anything (a VENDOR install)        -> body now in AAA,
                                                                              vendor left untouched
```

## 2. Final verified state (measured after every mutation)

```
names present in BOTH trees          44  ->  2     (only the two F13-held forks)
still diverged                       26  ->  2
names with a REAL body on both sides 44  ->  2
AAA entries borrowing from outside    0
broken symlinks                       0
load surface (resolvable)           443  ->  445    (no loss; +2 surfaced)
```

## 3. A regression I caused, caught, and fixed — recorded because it is the lesson

Collapsing the `substrate` container deleted `.hermes/skills/substrate/{audit-seal, kernel-bind,
memory-manage, observe-ground, route-dispatch, verify-gate}` — the **six substrate-core skills the
registry says every agent loads ALWAYS, FIRST**. They vanished from the load surface.

Cause: my pre-flight guard checked `os.path.exists(aaa_child)` — and `AAA/skills/substrate/<name>`
*existed* as a thin placeholder directory holding only `liveness.json`, while the real body sat at
`AAA/skills/<name>`. **`exists()` is not `holds a skill`.** The guard passed a name whose skill was
about to be lost.

No body was lost (the real copies were at `AAA/skills/<name>`), and the fix is now the registry's
intended shape: body at `AAA/skills/substrate/<name>`, top-level entry an address to it. Reachability
confirmed restored with a before/after set diff — **0 lost, 2 gained**.

The generalised rule, which belongs in the collapse tooling: *a pre-flight guard must assert the
artifact it is protecting (a `SKILL.md` resolves), never the container it sits in.*

## 4. Reversal

```
/root/AAA/backups/skill-collapse-20260918/
  bodies/              52 SKILL.md files (both sides of every pair, pre-mutation)
  borrowed-bodies/     37 bodies captured before repatriation
  s3-backup-manifest.json · s3-applied.json · borrowed-plan.json
  borrowed-applied.json · substrate-fix.json · final-verify.json
  RESTORE.sh           restores every AAA body from the captured copies
```
Plus tag `v2026.09.18-skills-audit` and the 147 MB pre-work bundle.

## 5. Still open (not in this greenlight)

1. **211 AAA-only skills are unreachable to Hermes** (`external_dirs = []`). This is unchanged by S3 —
   and constrained by `_defer_to_external`: populating `external_dirs` collides with every shared name
   the loader then refuses. The workable route is an **address per skill in `.hermes`**, not a new
   read root. Awaiting your binary.
2. **The two design forks** — `APEX-humility-godel`, `fi-mesh-check`. Substance stated in
   `S3-DIFF-RECEIPT-2026-09-18.md` §2.
3. **`hermes-gateway-image-routing`** reads the same test image as `"ALPHA-ZEN"` on one side and
   `"SADO"` on the other. Now a single body, so the surviving text is the AAA one — but the fork means
   one of those transcripts was fabricated. Deserves an F2 correction.
4. **43 descriptions still carry the `[fed: …]` marker injected mid-sentence**, inside the 57-character
   window selection precision depends on.

---

*One body, one address. A guard that asserts a container is not a guard. DITEMPA BUKAN DIBERI ⚒️*
