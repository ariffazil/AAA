---
name: geox-panel-authoring
description: "Author new visualization panels in the GEOX GUI codebase (geox-gui). Canvas+d3.js rendering, useMcpTool MCP data loading, inline CSS-in-JS dark theme, and TypeScript pitfalls. Covers the full lifecycle: study existing components → implement → verify build. NOT for integrating existing panels into the shell (use react-frontend-integration)."
version: 1.3.0
author: Hermes Agent
license: MIT
tags: [geox, react, canvas, d3, visualization, panel, component, typescript, vite]
related_skills: [react-frontend-integration, systematic-debugging]
---

# GEOX Panel Authoring

Create new visualization panels in the GEOX GUI (`/root/GEOX/geox-gui/src/components/`).
Canvas-based rendering with d3.js, MCP data loading via `useMcpTool`, inline CSS-in-JS dark theme.

## When to use

- Building a new panel component in geox-gui
- Adding a new well log visualization, correlation view, or data dashboard
- Any task that creates a new `.tsx` file under `src/components/`

## Reference component

**LogDock** (`src/components/LogDock/LogDock.tsx`) is the canonical reference.
Study it first — it demonstrates every pattern this skill encodes:
canvas rendering, DPI handling, d3 scales, curve drawing, depth axis, cursor tracking,
inline styles, dark theme, useMcpTool integration, and the status bar convention.

## Workflow

```
1. Create directory: src/components/<Name>/
2. Study LogDock for pattern reference (canvas setup, draw loop, margin/scale convention)
3. Define component with inline styles (styles object as React.CSSProperties)
4. Implement canvas drawing with d3 scales
5. Wire useMcpTool for MCP data loading
6. Add loading/error states per data source
7. Verify in two tiers:
   - Tier 1 (visual/runtime-sensitive work): `npm run build` + bundle-symbol spot check
   - Tier 2 (type/lint safety): `npm run typecheck` + `npm run lint`
   For creative UI / governance-lifecycle changes, run Tier 1 before Tier 2.
8. Export as named export
```

## Component anatomy

Every GEOX panel follows this structure:

```
┌─ Header (44px) ────── Title + badge + controls ────────────────┐
├─ Legend/info bar ───── Optional, expandable ───────────────────┤
├─ Main content ─────── Canvas area(s) with overflow scroll ─────┤
│   ┌─ Well/Track Column ─┐  ┌─ Gap ─┐  ┌─ Well/Track Column ─┐│
│   │ Name bar (28px)     │  │       │  │ Name bar             ││
│   │ Canvas (600px)      │  │ lines │  │ Canvas               ││
│   │ Loading/Error state │  │       │  │ Loading/Error state  ││
│   │ Zoom label (24px)   │  │       │  │ Zoom label           ││
│   └─────────────────────┘  └───────┘  └──────────────────────┘│
└─ Status bar (28px) ──── Loaded count | depth | DITEMPA ───────┘
```

## Inline CSS-in-JS pattern

All styles as a `styles` record — no Tailwind classes, no CSS modules:

```tsx
const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'flex', flexDirection: 'column', height: '100%',
    backgroundColor: '#0a0a0f', color: '#e2e8f0',
    fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
    overflow: 'hidden', userSelect: 'none',
  },
  header: {
    display: 'flex', alignItems: 'center', height: 44, minHeight: 44,
    padding: '0 16px', backgroundColor: '#0d0d14',
    borderBottom: '1px solid #1a1a2e', gap: 12,
  },
  // ... etc
};
```

### Dark theme constants

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#0a0a0f` | Container, canvas bg |
| Surface | `#0d0d14` | Header, bars, name bars |
| Border | `#1a1a2e` | All borders and separators |
| Grid lines | `#111119` | Minor grid |
| Major grid | `#1a1a2e` | Major grid lines |
| Text primary | `#e2e8f0` | Titles |
| Text secondary | `#64748b` | Labels, info |
| Text muted | `#475569` | Status bar, hints |
| Accent | `#00d4aa` | Primary accent, active states |
| Gold | `#d4af37` | Correlation lines, secondary accent |
| Error | `#ef4444` | Error states |
| Success | `#22c55e` | Loaded indicators |

## Canvas rendering pattern

### High-DPI setup (mandatory)

```tsx
const dpr = window.devicePixelRatio || 1;
canvas.width = width * dpr;
canvas.height = height * dpr;
canvas.style.width = `${width}px`;
canvas.style.height = `${height}px`;
ctx.scale(dpr, dpr);
ctx.clearRect(0, 0, width, height);
```

### d3 scale setup

```tsx
const yScale = d3.scaleLinear()
  .domain(depthRange)     // [min, max]
  .range([margin.top, margin.top + plotHeight]);

const xScale = d3.scaleLinear()
  .domain([curveMin, curveMax])
  .range([trackLeft, trackRight]);
```

### Curve drawing loop

```tsx
ctx.beginPath();
ctx.strokeStyle = curveColor;
ctx.lineWidth = 1.2;
let started = false;

for (let i = 0; i < depths.length; i++) {
  const d = depths[i];
  if (d < depthRange[0] || d > depthRange[1]) continue;
  const val = curveData[i];
  if (val == null || isNaN(val)) { started = false; continue; }
  const y = yScale(d);
  const x = xScale(val);
  if (!started) { ctx.moveTo(x, y); started = true; }
  else { ctx.lineTo(x, y); }
}
ctx.stroke();
```

### Depth grid lines

```tsx
const depthStep = 50;
ctx.fillStyle = '#64748b';
ctx.font = '9px monospace';
ctx.textAlign = 'right';

for (let d = Math.ceil(depthRange[0] / depthStep) * depthStep; d <= depthRange[1]; d += depthStep) {
  const y = yScale(d);
  // Horizontal grid line
  ctx.strokeStyle = '#1a1a2e';
  ctx.lineWidth = 0.5;
  ctx.beginPath();
  ctx.moveTo(left, y);
  ctx.lineTo(right, y);
  ctx.stroke();
  // Depth label
  ctx.fillText(d.toString(), labelX, y + 3);
}
```

### Cursor tracking

```tsx
const handleMouseMove = (e: React.MouseEvent) => {
  const rect = e.currentTarget.getBoundingClientRect();
  const y = e.clientY - rect.top;
  const yScale = d3.scaleLinear()
    .domain([margin.top, margin.top + plotHeight])
    .range(depthRange);
  const depth = yScale(y) as number;
  if (depth >= depthRange[0] && depth <= depthRange[1]) {
    onCursorMove(depth);
  }
};
```

## useMcpTool data loading pattern

### Import and setup

```tsx
import { useMcpTool } from '../../hooks/useMcpTool';

interface WellIngestResult {
  well_id?: string;
  curves?: { depth?: number[]; gr?: number[]; /* ... */ };
  tops?: { depth: number; name: string; facies?: string }[];
}

function useWellData(wellId: string) {
  const ingestTool = useMcpTool<
    { well_id: string; mode: string },
    WellIngestResult
  >('geox_well_ingest');

  const [data, setData] = useState<WellIngestResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await ingestTool.call({ well_id: wellId, mode: 'auto' });
      if (!result) throw new Error('No data returned');
      setData(result);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }, [wellId, ingestTool]);

  useEffect(() => { loadData(); }, [loadData]);

  return { data, loading, error, reload: loadData };
}
```

### Key points

- `useMcpTool` returns `{ data, status, error, call, reset }` — NOT a Promise; call returns a Promise
- The `call` function handles both iframe (postMessage) and standalone (fetch) modes automatically
- `status` is `'idle' | 'loading' | 'success' | 'error'`
- Each `useMcpTool` instance has its own state — call multiple tools by creating multiple instances
- Load data in `useEffect` with `call` — never call in the render path
- **Dynamic lane routing** — `directMcpCall` injects `X-Routing-Lane` header based on tool name prefix (geox_seismic* → geophysics, geox_petrophysics* / geox_well* → geology, else general). Add new tool prefixes to `resolveRoutingLane()` when extending the MCP surface.
- **Session validation for mutations** — non-read-only tools throw `F13 SOVEREIGN VIOLATION` if session_id is missing or anonymous. Read-only tools (`geox_claim`, `geox_prospect`) are whitelisted in `READ_ONLY_TOOLS`. Add new read-only tools to that set.

## d3.zoom for depth axis

```tsx
useEffect(() => {
  const el = zoomContainerRef.current;
  if (!el) return;

  const totalHeight = TRACK_HEIGHT + margin.top + margin.bottom;

  const zoom = d3.zoom<HTMLDivElement, unknown>()
    .scaleExtent([0.2, 10])
    .translateExtent([[0, 0], [0, totalHeight]])
    .on('zoom', (event) => {
      const t = event.transform;
      const [dMin, dMax] = originalRange;
      const span = dMax - dMin;
      const newSpan = span / t.k;
      const center = dMin + span / 2 - (t.y / totalHeight) * span;
      setDepthRange([center - newSpan / 2, center + newSpan / 2]);
    });

  const sel = d3.select(el);
  sel.call(zoom);
  return () => { sel.on('.zoom', null); };
}, [originalRange]);
```

## Export convention

```tsx
// Named export (required — not default)
export const MyPanel: React.FC<MyPanelProps> = ({ ... }) => { /* ... */ };
```

## Pitfalls

### 1. TypeScript d3 NumberValue narrowing

d3 scale functions return `d3.NumberValue` (which includes `NumberValue`), not `number`.
Inside a `.forEach()` callback, TypeScript cannot narrow the type through the closure.

**Broken:**
```tsx
CURVE_CONFIGS.forEach((cfg) => {
  const curveData = column.curves[cfg.key]; // 'possibly null' error
  const depths = column.curves.depth;       // same error
});
```

**Fix — assign to a local variable first:**
```tsx
CURVE_CONFIGS.forEach((cfg) => {
  const curves = column.curves;
  if (!curves) return;  // guard
  const curveData = curves[cfg.key];
  const depths = curves.depth;
  // ...
});
```

TypeScript does NOT narrow through property access chains across closure boundaries.
Always assign the nullable reference to a `const` and guard before use.

### 2. Per-file tsc gives misleading errors

Running `npx tsc --noEmit src/components/MyPanel.tsx` directly does NOT use the project
`tsconfig.json` and produces spurious JSX/esModuleInterop errors that are NOT real problems.

**Wrong:** `npx tsc --noEmit src/components/MyPanel.tsx`

**Right:**
```bash
# Project-level check (uses tsconfig.json with jsx: "react-jsx", esModuleInterop: true)
npx tsc --noEmit 2>&1 | grep "MyPanel"
guard before use.

### 3. Vite tree-shakes unused components AND dead-code layout chains

A new component with a named export but no imports elsewhere will not appear in the bundle.
This is expected — not an error. The component is verified by tsc (type-safe) and will
appear in the bundle once a parent component imports it.

**But that's necessary, not sufficient.** The parent itself must be reachable from the
live entry chain. If the parent is a layout file (e.g. `MainLayoutForge.tsx`) imported
only from a sibling `App*` file (e.g. `AppForge.tsx`) that the live `main.tsx` does NOT
import, the layout AND everything under it is tree-shaken — even though `tsc` and
`vite build` both succeed. The component "compiles fine" but is invisible in production.

**Always trace the live entry chain before claiming a panel ships:**

```bash
# 1. Find the actual app entry
cat src/main.tsx                     # → import App from './App'
# 2. Follow the import: which App does main import?
head -5 src/App.tsx                  # or src/AppForge.tsx
# 3. Which layout does that App render?
grep -E "import.*Layout|export default" src/App.tsx
# 4. Verify your panel is reachable from that layout (or imported directly)
grep -rn "import.*YourPanel" src/    # every importer
# 5. Build + verify the panel's runtime strings appear in the bundle
JS=$(ls -t ../static/gui/assets/index-*.js | head -1)
grep -oE "your_panel_lane|distinctive_label_string" "$JS" | wc -l
```

**GEOX GUI entry chain as of 2026-08-10 (verified live):**
- Live: `main.tsx → src/App.tsx → MainLayoutForge → forge/domain/{Domain1D, Domain2D}`
  AND `MainLayoutForge` directly imports Phase 1 panels:
  `SeismicInterpretationCanvas`, `MultiWellCorrelationPanel`, `LogDock`,
  `PetrophysicalTracks`, etc.
- Dead: `src/AppForge.tsx` and `src/components/Cockpit/OperatorCockpit.tsx`.
  Nothing in the live chain imports OperatorCockpit, so it (and any edits
  scoped to it — header text, identity wiring, session-gate logic) is
  tree-shaken despite `tsc` and `vite build` both passing.
- All Phase 1 panels ARE in the bundle because MainLayoutForge imports them.
- `MultiWellCorrelationPanel` IS in the bundle (also via MainLayoutForge).

**Rule of thumb for the cockpit shell:** edits inside `OperatorCockpit.tsx`
will pass build/typecheck but NOT ship to production until the entry chain
actually imports it. To activate: flip `main.tsx` to import `'./AppForge'`
or add `import { OperatorCockpit } from './components/Cockpit/OperatorCockpit'`
into `src/App.tsx`. Always state the reachability verdict in your report —
"build passes" is not the same as "change ships."

See `references/integration-verification.md` for the full GEOX build/deploy/verify recipe
and `scripts/verify-bundle-symbols.sh` for a reusable bundle-symbol checker.

### 4. Canvas ref lifecycle

Always null-check canvas and context before drawing:
```tsx
const canvas = canvasRef.current;
if (!canvas) return;
const ctx = canvas.getContext('2d');
if (!ctx) return;
```

The canvas element may be null during the first render cycle or after unmount.

### 5. useEffect for drawing

The `draw` callback must be wrapped in `useCallback` with all dependencies listed,
then called via `useEffect`. This ensures re-draw on depth range, data, or size changes.
The draw function must be a dependency of the effect.

If `draw` references stable component-scoped consts (e.g. `margin.left`, `plotW`
computed from module-level `width`/`height`), include them in the deps array —
they won't cause re-render churn since they're stable across renders, but their
absence triggers `react-hooks/exhaustive-deps` lint warnings.

### 6. Concurrent rebuild of `/root/GEOX/static/gui/` between your build and deploy

The GEOX build target `../static/gui/` is a SHARED directory. Other agents or
cron jobs may run `npm run build` concurrently. If your `npm run build` runs at
T1 and your `cp` deploy runs at T2, a concurrent rebuild at T1.5 can:

- Replace your `index-<hash>.js` with a new hash (your `ls -t | head -1` at
  deploy time picks up THEIR bundle, not yours)
- Leave your verified symbols intact IF the concurrent rebuild used the same
  patched source tree (the symbols re-bake into the new bundle)
- Wreck verification if the concurrent rebuild used a DIFFERENT source state
  (your symbols may vanish from the deployed bundle)

**Defensive deploy sequence:**

```bash
cd /root/GEOX/geox-gui && npm run build
JS_NEW=$(ls -t ../static/gui/assets/index-*.js | grep -v map | head -1)
sha256sum "$JS_NEW"
# Verify your required symbols are actually in the bundle you just built
grep -c "REQUIRED_SYMBOL" "$JS_NEW"
# THEN immediately deploy + re-verify the deployed copy has the same hash + symbols
for TARGET in /var/www/html/geox/gui /opt/geox/app/static/gui; do
  cp /root/GEOX/static/gui/index.html "$TARGET/index.html"
  cp /root/GEOX/static/gui/assets/* "$TARGET/assets/"
  # Prune stale index-* bundles that don't match the new hashes
  for stale in "$TARGET/assets"/index-*.{js,js.map,css}; do
    [ -f "$stale" ] || continue
    case "$(basename "$stale")" in
      "$(basename $JS_NEW)"|"$(basename $CSS_NEW)"|"$(basename $MAP_NEW)") ;;
      *) rm -f "$stale" ;;
    esac
  done
done
# Re-verify deployed symbols
grep -c "REQUIRED_SYMBOL" "$TARGET/assets/$(basename $JS_NEW)"
```

Never trust a bundle hash you didn't observe being written.

### 7. Pre-existing lint issues in files you touch — repair them anyway

If a file you're patching has pre-existing lint issues (unused params, missing
exhaustive-deps, unused imports) on lines you didn't introduce, **fix them as
part of your deliverable**. The codebase runs `npm run lint` with
`--max-warnings 0`, so any warning in a touched file fails the gate even if
it pre-dated your change.

**Quick repairs that satisfy `no-unused-vars` and `exhaustive-deps` without behavior change:**
- Unused forEach index: `(item, i)` → `(item, _i)` (matches the `/^_/` allow pattern)
- Unused function arg: `(arg: T)` → `(_arg: T)`
- Stable consts missing from useCallback deps: add them
  (`margin.left`, `margin.top`, `plotW`, `plotH` — all stable, safe to add)

Filter lint to your files only to confirm ZERO new issues introduced:
```bash
npm run lint 2>&1 | grep -A1 "<YourFile>.tsx" || echo "clean"
```

### 8. Governance state hooks — read-only propagation pattern

When a panel needs governance-gated states (e.g. DRAFT → PENDING REVIEW → ATTESTED),
create a custom hook in `src/hooks/` and wire it into the component. The pattern:

**Hook side** — expose state + transition functions:
```tsx
const { claim, toDraft, requestReview, attest, resetToReality } = useGeologicalClaim('correlation');
const isReadOnly = claim.state !== 'draft';  // canvas locked in non-draft
```

**Component side** — three wiring points:
1. **State guard in event handlers**: `if (isReadOnly) return;` at the top of click/pick handlers
2. **readOnly prop to child components**: Pass to canvas-rendering children so they can:
   - Disable click handlers (`if (readOnly) return;`)
   - Change cursor style (`cursor-not-allowed` when locked)
   - Show lock overlay in draw: `if (readOnly) { ctx.fillText('🔒 LOCKED', ...); }`
3. **State-dependent UI in sidebar/toolbar**:
   - Badges: `[UNVERIFIED]` (yellow), `[PENDING REVIEW]` (amber), `[SEALED - VAULT999]` (green)
   - Buttons change per state: REQUEST VERDICT → ATTEST + DISCARD → nothing (attested)
   - Toolbar buttons: `disabled={isReadOnly}` with visual lock indicator (🔒)

**Attest routing**: `attest()` must route through arifOS (fetch `/api/attest` → `arif_seal`), NOT directly to VAULT999. GEOX's authority ceiling is `555_COMPUTE_ONLY` — its local maximum is `QUALIFIED_CANDIDATE`, not `SEAL`. The GUI sends an intent TO arifOS, which adjudicates and seals. If arifOS is unreachable, attest fails — that's correct behavior (fail-closed for sovereign operations).

**Common mistake**: calling `toDraft(payload)` inside `setState` updater functions.
Since `toDraft` has `updateFloorStatus` as a dependency, it triggers a store update.
This is safe — Zustand store updates are batched and don't cause infinite loops when
called inside `setPicks((prev) => { toDraft(...); return next; })`.

#### 8a. Hook signature migration — ripple through call sites

When changing a hook's function signature (e.g. `attest` from sync `(ref: string)` to
`async (payload: Record<string, unknown>)`), the change ripples through every consumer:

1. **Update the hook** — change the function body and return type
2. **Add new exports** if any (e.g. `resetToReality`) — update the return object
3. **Grep for all call sites**: `grep -rn "\.attest(" src/` or `grep -rn "attest(" src/components/`
4. **Update each call site's arguments** to match the new signature
5. **Update destructuring** if new exports were added (e.g. add `resetToReality` to the destructured object)
6. **Verify** — LSP errors can be stale after patching. Re-read the actual file lines to confirm.

#### 8b. Post-state confirmation panel — don't auto-reset

After reaching a terminal state (e.g. `attested`), show a confirmation panel instead of
resetting to the initial state. The panel should display:
- Receipt/reference ID
- Timestamp
- Type/claim info
- "Return to Reality" button that explicitly resets via the hook's reset function

```tsx
{claim.state === 'attested' && (
  <div className="attestation-confirmation mb-2">
    <h4>🔒 Attestation Confirmed — {claim.type}</h4>
    <p>Receipt: <code>{claim.attestationRef}</code></p>
    <p>Timestamp: {claim.attestedAt}</p>
    <button onClick={resetToReality}>Return to Reality</button>
  </div>
)}
```

Use the `.attestation-confirmation` CSS class from `designSystem.css` (gold border, gold-tinted bg).
Do NOT inline the confirmation styles — the class is centralized for consistency.

#### 8c. STALE structural lock — data freshness guard

Add a `isStale?: boolean` field to the claim interface. When `isStale` is true, block
promotion from stale data:

```tsx
const toDraft = useCallback((payload) => {
  if (claim.isStale) {
    updateFloorStatus('F1', 'red', 'BLOCKED: Stale node. Refresh required before promotion.');
    return; // Block the promotion
  }
  setClaim((prev) => ({ ...prev, payload, state: 'draft', isStale: false }));
}, [updateFloorStatus, claim.isStale]);
```

This prevents silent data corruption when upstream sources change between fetch and commit.
The lock is at F1 (AMANAH/reversibility) — the earliest gate, so it's the cheapest place to block.

### 9. Centralized mutation wrapper (`commitPick` pattern)

When a panel needs audit trail + governance state sync on every mutation, do NOT
scatter `setPicks()` + `toDraft()` across multiple callbacks. Instead, create a
single `commitPick` wrapper that is the ONLY path to mutate picks state:

```tsx
const commitPick = useCallback((
  updater: (prev: LocalPick[]) => LocalPick[],
  action: AuditEntry['action'],
  pickType: AuditEntry['pickType'],
  detail: string,
) => {
  setPicks((prev) => {
    const next = updater(prev);
    // Sync claim state machine — picks are ALWAYS in DRAFT after mutation
    if (pickType === 'horizon' || pickType === 'both') {
      horizon.toDraft({ picks: next.filter((p) => p.type === 'horizon') });
    }
    if (pickType === 'fault' || pickType === 'both') {
      fault.toDraft({ picks: next.filter((p) => p.type === 'fault') });
    }
    return next;
  });
  logMutation(action, pickType, horizon.claim.state, detail);
}, [horizon, fault, logMutation]);
```

**Why this matters:**
- Guarantees EVERY mutation is logged in the audit trail (no accidental direct setState)
- Ensures claim state machine is always in sync (no orphan picks outside DRAFT)
- Single point of truth — adding new audit fields or validation only touches one function
- Eliminates the common bug where `toDraft()` is called in some paths but not others

**Usage:** replace all direct `setPicks()` calls with `commitPick(updater, action, type, detail)`.
The updater function is the same `(prev) => nextState` pattern, but the wrapper handles
logging and governance sync.

### 10. Tension visual channels — CSS class-based governance visualization

When governance states need distinct visual signatures (e.g. "measured zero" vs "unmeasured"),
use CSS classes in `designSystem.css` — NOT inline styles. The key principle: states that
look similar but mean different things MUST use different visual channels (color + pattern +
border style), not just shade variations.

Current tension classes:
| Class | Meaning | Visual |
|-------|---------|--------|
| `.tension-none` | Measured, zero tension | Solid green border, 10% green bg |
| `.tension-unmeasured` | Not yet checked | RED dashed border, 45° red hatched bg |

**Adding new tension channels:**
1. Define the class in `designSystem.css` under the "Tension Visual Channels" section
2. Use distinct color AND pattern — never rely on color alone (accessibility)
3. Hatched/repeating-linear-gradient patterns are the established pattern for "not checked"
4. Solid borders = "measured and confirmed"; dashed borders = "unconfirmed/unmeasured"
5. Wire into components via `className` — the classes are self-contained, no props needed

### 11. Bundle symbol verification — function names vs string literals

Vite esbuild **minifies function names** in production builds. Custom hook names
like `useGeologicalClaim`, component names like `MultiWellCorrelationPanel`, and
internal function names will NOT appear in the bundle. Only **string literals**
used in JSX text, props, console messages, and status strings survive.

**Wrong verification:**
```bash
grep -c "useGeologicalClaim" "$JS"   # ← 0, always — minified away
```

**Right verification** — use string literals that appear in the component's UI:
```bash
grep -c "PENDING REVIEW|SEALED - VAULT999|UNVERIFIED" "$JS"
# Must be > 0 — these are JSX text, not function names
```

See `scripts/verify-bundle-symbols.sh` for a reusable verifier. Always verify
with **distinctive runtime strings**, not identifiers.

See `templates/governance-state-hook.tsx` for a starter hook that demonstrates
the tri-state authority pattern.
