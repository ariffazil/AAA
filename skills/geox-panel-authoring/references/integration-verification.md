# GEOX GUI Integration & Verification Recipe

> Provenance: 2026-08-10 Phase 1 cross-tab integration session (incident: edits
> to `MainLayoutForge` compiled and built fine but were tree-shaken because the
> live entry chain reaches `OperatorCockpit`, not `MainLayoutForge`).
>
> ⚠️ **Chain FLIPPED later the same day (re-verified 2026-08-10, V2/V3/V5 patch
> session):** `main.tsx → src/App.tsx` now renders `MainLayoutForge`, and
> `OperatorCockpit.tsx` is the dead file. A concurrent refactor switched the
> entry. The tables below reflect the CURRENT verified state — when in doubt,
> re-trace with the commands in "The entry-chain trap".
>
> Use this whenever you wire an existing panel into the GEOX GUI shell, or when a
> build "succeeds" but you suspect a component isn't actually shipping to users.

## Build

```bash
cd /root/GEOX/geox-gui
npm run build           # vite build + node scripts/copy-cesium-runtime.mjs
```

Output lands in `/root/GEOX/static/gui/` (NOT under `geox-gui/dist/` — check
`vite.config.ts` if unsure). The new bundle hash is announced in the build log
(e.g. `assets/index-tfH83oGm.js`).

## Deploy (Caddy-served path)

```bash
JS=$(ls -t /root/GEOX/static/gui/assets/index-*.js | head -1)
mkdir -p /var/www/html/geox/gui/assets
cp /root/GEOX/static/gui/index.html /var/www/html/geox/gui/index.html
cp /root/GEOX/static/gui/assets/* /var/www/html/geox/gui/assets/
```

> Old bundles accumulate in `/var/www/html/geox/gui/assets/` — harmless because
> `index.html` pins the current hash, but the directory can be pruned periodically.

## Verify (symbol counts in the deployed bundle)

**Do NOT grep for the React component name** — minifiers (esbuild) rename
`LogDock`, `MultiWellCorrelationPanel`, etc. to short identifiers. Count will be 0.

Grep for **distinctive runtime string literals** that survive minification:
- MCP lane names: `geox_well_view`, `geox_petrophysics`, `geox_seismic_interpret`
- JSX label text: `888_JUDGE`, `REQUESTING SEAL…`, `SEAL granted`
- Content keywords the panel owns: `horizon`, `cutoff`, `well_view`, `SEAL`

```bash
JS=/var/www/html/geox/gui/assets/index-tfH83oGm.js
for s in MultiWellCorrelationPanel LogDock PetrophysicalTracks SeismicInterpretationCanvas; do
  printf "%-32s %s\n" "$s:" "$(grep -oF "$s" "$JS" | wc -l)"
done
for s in geox_well_view geox_petrophysics geox_seismic_interpret; do
  printf "%-32s %s\n" "$s:" "$(grep -oF "$s" "$JS" | wc -l)"
done
```

Or run the bundled helper:

```bash
bash <skill_dir>/scripts/verify-bundle-symbols.sh "$JS" \
  LogDock PetrophysicalTracks SeismicInterpretationCanvas MultiWellCorrelationPanel \
  geox_well_view geox_petrophysics geox_seismic_interpret
```

## The entry-chain trap

| File | Reachable from `main.tsx`? |
|---|---|
| `src/main.tsx → src/App.tsx → MainLayoutForge` (+ `forge/domain/*`, Phase 1 panels) | **Live** (verified 2026-08-10) |
| `src/AppForge.tsx` and `src/components/Cockpit/OperatorCockpit.tsx` | **Dead** (verified 2026-08-10) |

**Symptom of dead-code edits:** `tsc --noEmit` and `vite build` both pass, but the
component's runtime string literals are 0 in the deployed bundle. Fix: either flip
`main.tsx` to import `'./AppForge'`, or add `import { OperatorCockpit } from
'./components/Cockpit/OperatorCockpit'` into `src/App.tsx`. (As of the last
verification, the shell edits that people expect to ship — cockpit header,
session gate, identity wiring — all live in dead `OperatorCockpit.tsx`.)

**Always confirm before claiming shipped:**

```bash
cat src/main.tsx                                          # which App does main import?
grep -E "import.*from.*Layout|export default" src/App.tsx # which layout does it render?
grep -rn "import.*YourPanel" src/                         # every importer of your panel
```

## Deploy sync verification (deterministic builds)

Vite produces deterministic hashes from a given source tree. After any rebuild that
doesn't change the module graph, the bundle hash is identical and the deploy is still
valid. Verify sync with `md5sum` and skip redundant re-deploys:

```bash
md5sum /root/GEOX/static/gui/assets/index-*.js /var/www/html/geox/gui/assets/index-*.js
```

If the hashes match → deploy is current, no re-copy needed. (Confirmed in the
2026-08-10 session: rebuilding after `git checkout HEAD --` of an unrelated file
produced the identical `index-tfH83oGm.js` hash.)

## Phase 1 evidence (2026-08-10, re-verified on bundle `index-43ScDMHf.js`)

| Component | Bundle presence | Why |
|---|---|---|
| `LogDock` | ✓ | imported by `MainLayoutForge` |
| `PetrophysicalTracks` | ✓ | imported by `MainLayoutForge` |
| `SeismicInterpretationCanvas` | ✓ (`REQUEST JUDGE SEAL` ×2, `F13 Docking Protocol` ×1) | imported by `MainLayoutForge` |
| `MultiWellCorrelationPanel` | ✓ (`REQUEST JUDGE SEAL` ×2 total incl. its button) | imported by `MainLayoutForge` |
| `OperatorCockpit` | ✗ (`geox-cockpit-shell` ×0, `SessionGate` ×0) | dead — nothing imports it |

## Related pitfalls (verified 2026-08-10)

- **Patch tool V4A fuzzy matcher** injects leading whitespace into inserted lines,
  producing mixed indentation. Plan a normalization pass after the initial patch:
  re-read the modified region, then `patch` again to restore uniform indent.
- **Concurrent file deletion** — another subagent/script can delete tracked files
  between your edits and final deploy. Always run `git status --short` before
  declaring done; `git checkout HEAD -- <path>` restores. (The forbidden
  `WellCorrelationPanel.tsx` was deleted by an external process during the
  2026-08-10 session — restored via `git checkout HEAD --`. The deploy was
  unaffected because the file is not reachable from the live entry.)
- **Pipe exit codes** — `cmd1 | cmd2; echo $?` shows `cmd2`'s exit (usually 0 for
  `tail`). Use `echo ${PIPESTATUS[0]}` to get `cmd1`'s real exit code.