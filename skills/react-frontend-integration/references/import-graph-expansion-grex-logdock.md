# Import Graph Expansion — GEOX LogDock Case Study

## Symptom

Build fails with 26 modules (down from 1744) after adding imports to OperatorCockpit.tsx:

```
LogDock.tsx:681:6: ERROR: Expected ")" but found "{"
file: /root/GEOX/geox-gui/src/components/LogDock/LogDock.tsx
```

## Root cause

LogDock.tsx had a pre-existing JSX syntax error: the ternary else-branch
(`{mode === 'mcp' ? <PetrophysicalTracks /> : ...}`) contained multiple sibling
elements (a div + a comment + another div) without a `<>...</>` fragment wrapper.

The file was never compiled before because:
- Entry point: main.tsx → App.tsx → OperatorCockpit.tsx
- OperatorCockpit never imported LogDock directly
- LogDock was only imported by WellContextDesk, which is imported by MainLayout
- MainLayout is NOT in the main.tsx → App.tsx → OperatorCockpit chain
- Vite only compiles files reachable from the entry point

## Verification that error was pre-existing

```bash
git stash && npm run build  # 1744 modules, BUILD SUCCEEDS
git stash pop                # restore changes
npm run build               # 26 modules, BUILD FAILS (LogDock.tsx error)
```

## Fix applied (2 lines)

**File:** `geox-gui/src/components/LogDock/LogDock.tsx`

Line 642 — add fragment open tag after `) : (`:
```
      ) : (
+     <>
      <div className="flex-1 flex overflow-hidden">
```

Line 690 — add fragment close tag before `)}`:
```
      </div>
+     </>
      )}"
```

## Module count delta

| State | Modules | Status |
|-------|---------|--------|
| Before (no LogDock import) | 1744 | PASS |
| After (LogDock imported) | 2332 | PASS (after fragment fix) |

The delta (2332 - 1744 = 588) represents LogDock and its dependency subtree
being pulled into the compilation graph for the first time.
