---
name: react-frontend-integration
description: "Modify React/Vite apps to swap iframe rendering for direct component imports, and deal with the cascading build/compilation effects. Covers import graph expansion pitfalls, JSX fragment fixes, and build verification patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [react, vite, frontend, iframe, component-integration, build, jsx]
related_skills: [systematic-debugging, spike, live-data-dashboards]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# React Frontend Integration

Modify a Vite+React application to change how components are rendered — typically swapping iframe-based embedding for direct React component imports. This is a common React modernization pattern.

## When to use

- Replacing iframe-based sub-app rendering with direct React component rendering
- Integrating existing React components into a shell/cockpit/layout component
- Adding new imports that pull previously-uncompiled files into the build graph
- Any Vite+React build that fails after adding imports to a shell component

## The core workflow

```
1. Read shell component (find the iframe rendering site)
2. Add imports for target components
3. Replace iframe with conditional JSX (component vs iframe per view)
4. Add layout CSS for the new panels
5. Build — expect import-graph expansion errors
6. Fix latent errors in newly-pulled files
7. Verify build + lint
8. Deploy output
```

See `references/import-graph-expansion-grex-logdock.md` for a real-world case study with exact error transcript, verification steps, and module count deltas.

## Pitfall: Shell wired but App.tsx still points elsewhere — DEAD CODE without errors

**The trap (forged 2026-08-10):** you correctly wire components into `MainLayoutForge.tsx` (the new shell), but `src/App.tsx` still imports and renders the OLD shell (`OperatorCockpit`). The build succeeds. The bundle has all the new components. The browser loads the app. **But none of your wiring ever renders** — `MainLayoutForge` is unreachable because `App.tsx` never imports it. Zero build errors. Zero runtime errors. Pure silent dead-code failure.

**Symptom:** new tabs/features don't appear in the UI; you can prove the bundle contains them by `grep`-ing the JS file (e.g. `grep -c "MultiWellCorrelationPanel" bundle.js` returns > 0), but they never show up.

**Verify by tracing the entry chain:**

```bash
# 1. Identify the actual entry point
cat src/main.tsx          # → renders <App />
cat src/App.tsx            # → what App renders matters!
cat src/components/Cockpit/OperatorCockpit.tsx  # old shell, does it have your changes? NO
cat src/components/Layout/MainLayoutForge.tsx   # new shell, has your changes? YES
# If App.tsx imports OperatorCockpit (not MainLayoutForge), your changes are dead code.

# 2. Fix: redirect the entry
# /root/GEOX/geox-gui/src/App.tsx
- import { OperatorCockpit } from './components/Cockpit/OperatorCockpit';
+ import { MainLayoutForge } from './components/Layout/MainLayoutForge';
  function App() {
    return (
      <div className="app">
-       <OperatorCockpit />
+       <MainLayoutForge />
      </div>
    );
  }
```

**Anti-pattern: iframe-as-leftover from migration.** Even after App.tsx is fixed, old `src: '/gui/old_iframe/index.html'` entries in the shell's VIEWS array keep pointing to dead iframe shells. Strip ALL iframe `src` entries that conflict with the new component rendering.

## Pitfall: Stale bundle hash — HTML references old JS

**The trap (forged 2026-08-10):** you deploy a new `index-tfH83oGm.js` to `/var/www/html/geox/gui/assets/`, but the served `index.html` still references the OLD hash `index-DQoCrhZP.js`. The browser loads the old bundle with zero errors. Your new code silently never runs.

**Verify zero-trust:**

```bash
# 1. What's the BUILT hash?
JS=$(ls -t /root/GEOX/static/gui/assets/index-*.js | head -1)
echo "Built: $JS"

# 2. What does the SERVED HTML reference?
curl -s https://geox.arif-fazil.com/gui/ | grep -o 'index-[A-Za-z0-9]*\.js'

# 3. If they don't match → STALE BUNDLE GHOST.
# Deploy ONLY when both match. The browser cache-busts with ?nocache=$(date +%s).
```

**The fix is two-way:** copy the new `index.html` (which has the new hash references) AND the new assets to the Caddy-served path. If you copy assets but not index.html, the served HTML references hashes that don't yet exist (404). If you copy index.html but not assets, the served HTML references hashes that do exist (old ones) → ghost bundle.

**Browser cache layer:** even after fixing the server, browsers cache the old HTML by ETag/Last-Modified. During QA: hard-refresh (Cmd+Shift+R), use incognito, or visit `?nocache=$(date +%s)`. In production, set proper `Cache-Control: no-cache` on the index.html.

**This is the #1 trap.** When you add an import like `import { Foo } from '../Foo/Foo'` to a shell component, Vite now compiles `Foo.tsx` as part of the dependency tree. If `Foo.tsx` was previously uncompiled (not imported from the entry point), any latent syntax errors will suddenly surface as build failures.

**Why this happens:** Vite/esbuild only compiles files reachable from the entry point. Files behind lazy imports, files in other app shells, or files never imported at all are invisible to the bundler until you add a direct import.

**What to do:**
1. Check `npm run build` BEFORE adding imports — note the module count (e.g., "1744 modules")
2. Add imports, run build again — if module count jumps and errors appear in newly-reached files, this is import graph expansion
3. Verify the errors are pre-existing by stashing changes and rebuilding: `git stash && npm run build && git stash pop`
4. Apply minimal fixes to the newly-reached files (see JSX fragment fix below)
5. Do NOT revert your imports — the pre-existing errors needed fixing anyway

## Pitfall: Missing JSX fragment in ternary else-branch

A common latent JSX syntax error: the else-branch of a ternary contains multiple sibling elements without a `<>...</>` wrapper.

**Symptoms:**
```
Expected ")" but found "{" [esbuild]
```
or
```
')' expected [typescript]
```

**Broken pattern:**
```tsx
{condition ? (
  <ComponentA />
) : (
  <div>First</div>
  {/* Comment */}
  <div>Second</div>
)}
```

**Fixed pattern:**
```tsx
{condition ? (
  <ComponentA />
) : (
  <>
    <div>First</div>
    {/* Comment */}
    <div>Second</div>
  </>
)}
```

**Why it's latent:** If the file was never compiled before (import graph wasn't reaching it), esbuild never parsed it and the error was invisible.

## Verification pattern for Vite/React projects

There is no `pytest` equivalent for a Vite frontend. The verification pair is:

```bash
# 1. Build (catches all TypeScript/JSX errors, tree-shaking issues)
cd <project> && npm run build 2>&1

# 2. Lint modified files only (fast, targeted)
npx eslint src/path/to/ModifiedFile.tsx src/path/to/OtherModified.tsx --ext ts,tsx
```

**Why targeted lint:** A full `npm run lint` may have pre-existing errors in untouched files. Linting only the files you changed confirms your changes are clean.

**Build success criteria:** exit code 0, module count matches expectations, no new warnings in your files.

## Iframe-to-component swap pattern

When replacing iframe rendering in a shell component (OperatorCockpit, AppShell, etc.):

### Step 1: Update the view config

```tsx
// BEFORE
{ id: 'seismic', src: '/gui/seismic_viewer/index.html', ... }

// AFTER — mark as component-rendered
{ id: 'seismic', src: 'react:seismic', ... }
```

### Step 2: Add imports

```tsx
import { SeismicInterpretationCanvas } from '../SectionCanvas/SeismicInterpretationCanvas';
```

### Step 3: Replace iframe with conditional rendering

```tsx
{currentView.id === 'seismic' ? (
  <div className="geox-panel">
    <SeismicInterpretationCanvas />
  </div>
) : currentView.id === 'well' ? (
  <div className="geox-panel geox-panel-split">
    <div className="geox-panel-left"><LogDock /></div>
    <div className="geox-panel-right"><PetrophysicalTracks /></div>
  </div>
) : (
  <iframe ref={iframeRef} src={currentView.src} ... />
)}
```

### Step 4: Add panel CSS

```css
.geox-panel { flex: 1; overflow: auto; background: #0a0a0f; }
.geox-panel-split { display: grid; grid-template-columns: 1fr 1fr; }
.geox-panel-left, .geox-panel-right { overflow: auto; }
```

### Step 5: Build, fix, verify, deploy

```bash
npm run build 2>&1 | tail -5
# Deploy output
cp dist/index.html /deploy/path/index.html
cp dist/assets/* /deploy/path/assets/
```
