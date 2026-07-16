# ⚒️ React SPA Discipline — Component Architecture

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Enforce consistent React component architecture: state management strategy, hydration boundaries, client/server split, composition patterns.

## When to Use
- Building or refactoring React components in AAA cockpit or organ UIs
- Choosing state management — useState vs useReducer vs zustand vs context
- Client/server component boundary decisions in Next.js or Vite SPA
- Component decomposition — container/presentational, compound components, hooks

## When NOT to Use
- Routing or data fetching specific to Next.js — use `nextjs-mastery`
- CSS/styling decisions — use `tailwind-tokens`
- Backend logic — route to FastAPI or Express organ

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Refactor one component at a time; keep parallel implementations until verified |
| F2 TRUTH | Props and state types must match runtime shape; no `any` on organ data |
| F4 CLARITY | One state management pattern per feature; avoid prop drilling >3 levels |
| F7 HUMILITY | Default to controlled components with loading/empty/error states |
| F11 AUDIT | Component side effects (fetch, WebSocket) log to console in dev |

## Commands & Patterns

```tsx
// Client/server split — "use client" only when necessary
// Default: server component → fetch data → pass as props

// State management guidelines:
// - Local UI state → useState
// - Form state → useReducer + zod validation
// - Cross-component → zustand (not context for performance)
// - Server cache → SWR or React Query (not zustand)

// Component interface pattern
interface Props {
  data: OrganHealth;
  onRefresh?: () => void;
  className?: string;
}

// Hydration-safe pattern
const [mounted, setMounted] = useState(false);
useEffect(() => setMounted(true), []);
if (!mounted) return <Skeleton />;
```

## Refusal Surface
- ❌ `any` typed organ responses — always use generated types
- ❌ Mixing zustand + context for the same domain
- ❌ Client components that could be server components
- ❌ Direct DOM manipulation outside useEffect cleanup
- ❌ Prop drilling beyond 3 levels without composition refactor
