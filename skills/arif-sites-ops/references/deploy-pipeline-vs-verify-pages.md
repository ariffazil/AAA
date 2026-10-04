# Deploy pipeline: `make deploy` vs `make verify-pages` vs manual rsync

Verified 2026-08-07 on the hub-hero upgrade. Two deploy entrypoints, two very
different gates — and a manual third path that bypasses both. Picking the wrong
one wastes a session on a "make deploy failed" error that is not about your work.

---

## The three deploy paths (verified 2026-08-07)

### 1. `make verify-pages` — the **content** gate

```bash
cd /root/arif-fazil.com && make verify-pages
```

What it runs: `bash scripts/verify-pages.sh https://arif-fazil.com sites/arif-fazil.com/dist`.

What it checks: every `dist/*/index.html` (file existence) against `https://arif-fazil.com/<route>/`
(live HTTP 200). Asserts pages are reachable; **does NOT catalog-check individual paths
or assert content**. Green = paths serve 200.

Exit codes: `VERDICT: PASS — safe to deploy.` (gate passed) or `VERDICT: HOLD` (gate blocked).

This is the gate the skill calls "canonical deploy gate." Accurate for "can I deploy
my static shells?" — wrong for "did `make deploy` block?"

### 2. `make deploy` — the **full** deploy chain

```bash
cd /root/arif-fazil.com && make deploy
```

What it runs (in order, per `Makefile`):

```text
verify  ← runs verify-surfaces.cjs + verify-pages.sh + verify-content.sh + caddy validate + dist dev-only scan
sync-aaa  ← rsync /root/AAA/dist/ → sites/arif-fazil.com/dist/aaa/
build   ← prebuild generators (8 node scripts) + tsc + vite build + render-propa + inject-panel + generate-discovery
verify-pages   ← same content gate, runs again
reload   ← caddy validate + systemctl reload caddy
```

The non-obvious gate is `verify-surfaces.cjs` — it reads `surfaces.json` (the
SOLE catalogue of route truth the federation trusts) and probes every entry.
**It is stricter than `make verify-pages`** and will FAIL on:

- `status: "live"` paths that now return 308 (legacy paths after the 5-lane reorg)
- `status: "gone"` paths that return 200
- `redirect_to` mismatches where the catalog and Caddy disagree

When `make deploy` fails at `verify` with 13 surfaces red on 308s, **your hero
work is not broken**. The catalog truth has drifted from the live site. See
"Catalog drift" below.

### 3. Manual rsync — the **content** deploy

```bash
# untracked shells (the safe path)
rsync -av sites/arif-fazil.com/dist/<route>/ /var/www/html/arif/<route>/

# git-tracked shells where src gets reverted — write live first, sync src after
cp /var/www/html/arif/<route>/index.html \
   sites/arif-fazil.com/public/<route>/index.html
```

What it does: ships the new file to `/var/www/html/arif/` (what Caddy serves).
Skips the entire gate chain. Use when:

- You patch is small and reversible
- You can `curl` the live page and grep for the change yourself
- `make deploy` is blocked on catalog drift that is not your problem

This is what 2026-08-07's hub-hero work actually deployed through — the heroes
went live via rsync, not `make deploy`.

---

## Catalog drift (`surfaces.json` vs live) — 13 surfaces, 2026-08-07

`sites/arif-fazil.com/surfaces.json` was the canonical authority for which
paths serve what. After the 2026-08-06 5-lane reorg moved every route, the
catalog was NOT updated. Today (2026-08-07) `make deploy` fails on:

| Catalog path | Catalog status | Live behavior | Truth |
|---|---|---|---|
| `/economics/` | `live` | 308 → `/world/economics/` | should be `redirect` w/ `redirect_to` |
| `/writing/` | `live` | 308 → `/words/writing/` | should be `redirect` |
| `/doctrine/` | `live` | 308 → `/words/doctrine/` | should be `redirect` |
| `/999/` | `live` | 308 → `/work/proof/` | should be `redirect` |
| `/oil/`, `/gas/`, `/gold/` | `live` (no expected_http) | 308 → `/world/economics/<x>/` | should be `redirect` |
| `/propa/`, `/malaysia/` | `live` | 308 → canonical | should be `redirect` |
| `/politics/shadow/{,board/,derita/}` | `live` | 308 → canonical | should be `redirect` |
| `/pulse/` | `gone` (expected 4xx) | 200 (deployed) | should be `live` |

Fix (T1, reversible, separate day's work): mark each path `status: "redirect"`
with `redirect_to: "<canonical>"`, update `/pulse/` to `live`. Do NOT patch the
gate script (`verify-surfaces.cjs`) — fail-closed doctrine says fix the gap
source.

---

## `make deploy` decision tree

```text
Made a static-shell change (hero, copy, etc.)
  │
  ├─ Used `write_file` against `public/<route>/`?
  │     │
  │     ├─ route's `public/<route>/` is untracked (new dir)?
  │     │     → rsync is fine: src → dist (via npm build) → live (via rsync)
  │     │     → run `make verify-pages` (the content gate)
  │     │
  │     └─ route's `public/<route>/` is git-tracked (committed pre-2026-08-06)?
  │           → WRITE LIVE FIRST, then sync src + commit separately
  │           → the postbuild mirror step + a `git checkout` event can both
  │             revert your src change mid-session
  │           → verify with `curl -s https://arif-fazil.com/<route>/ | grep <marker>`
  │             on the live page, NOT the src file
  │
  └─ Time to deploy via `make deploy`?
        │
        ├─ `make verify-pages` PASSED → run `make deploy`
        │     │
        │     └─ `make deploy` failed at `verify` (verify-surfaces.cjs)?
        │           → it is almost certainly catalog drift (13 surfaces on 308s)
        │           → fix `surfaces.json` OR manually rsync + verify-pages
        │           → do NOT patch the gate
        │
        └─ `make verify-pages` FAILED → fix the content gate first, then re-run
```

---

## `verify-pages` content trust gap (verified 2026-08-07)

The gate asserts HTTP 200 only. **It will pass for stale content** if the file
exists at the expected path. Two real instances:

1. **`/world/`** had live `3809 B` content (old 10-item nav, no hero). After
   patch + rsync, live went to `9026 B`. But between the rsyncs the src had
   been silently reverted by a `git checkout` (git-tracked file). When I
   `curl`'d live after deploy, the gate had reported PASS on what was actually
   stale content.

2. **`/words/`** and **`/work/`** showed the new hero on first deploy but the
   stale hero-core glyph block on a later probe — same gate PASSED both times.

**Mitigation:** after every content deploy, manually grep the live page for a
unique marker:

```bash
for r in /words/ /world/ /work/; do
  printf "%-12s hero=" "$r"
  curl -s "https://arif-fazil.com$r" | grep -oE "class=\"kicker\".*<" | head -1
done
```

If you don't see your new content, the patch didn't reach the live webroot —
the diff is between `sites/arif-fazil.com/dist/<route>/` and
`/var/www/html/arif/<route>/`. Use `diff <(curl -s URL) <(cat dist_file)`
to localise.

---

## When `make deploy` blocks on catalog drift but your work IS live

Reproducing 2026-08-07 verbatim:

```text
1. Made hub-hero work, ran `npm run build`, `rsync -av dist/{words,world,work}/ /var/www/html/arif/{words,world,work}/`
2. Curl each page → hero IS live, sizes 10695/9026/10670
3. `make verify-pages` → PASS, 114/114
4. `make deploy` → FAIL at `verify` step, 13 surfaces on 308s
5. Concluded: heroes deployed through rsync path; catalog drift is the next problem
6. Reported day-done
```

The right move in this state: do NOT try to "fix the deploy." Report the catalog
drift as a separate problem for the next session. `make deploy` is the
sanctioned entrypoint, but the manual rsync + `verify-pages` path is documented
in "Editing an existing static shell (the live site edit path)" and is the
fallback when catalog drift is independent of the day's work.

---

## Probe recipes

```bash
# Confirm what `make verify` actually checks (not verify-pages)
cd /root/arif-fazil.com && sed -n '27,40p' Makefile

# Check if a public/<route>/ is git-tracked
git -C /root/arif-fazil.com ls-files sites/arif-fazil.com/public/<route>/

# Check sizes (src → dist → live) to detect drift
for layer in src dist live; do
  case $layer in
    src) f=/root/arif-fazil.com/sites/arif-fazil.com/public/<route>/index.html ;;
    dist) f=/root/arif-fazil.com/sites/arif-fazil.com/dist/<route>/index.html ;;
    live) f=/var/www/html/arif/<route>/index.html ;;
  esac
  printf "%-4s %6d  %s\n" "$layer" "$(stat -c %s $f 2>/dev/null)" "$f"
done

# Run only the content gate (NOT the full make verify)
cd /root/arif-fazil.com && bash scripts/verify-pages.sh https://arif-fazil.com sites/arif-fazil.com/dist
```

## Related

- See `references/constitution-surfaces-000-999.md` for the /000 and /999
  special-wiring notes.
- The `surfaces.json` doctrine-introspection drift section in SKILL.md is a
  SEPARATE class of catalog issue (doctrine claims 64 surfaces, file has 70) —
  the catalog-vs-live drift above is a different problem in the same file.
