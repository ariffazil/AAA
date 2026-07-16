# ⚒️ Next.js Mastery — App Router Engineering

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Build and maintain Next.js SPA surfaces with App Router discipline: server components first, ISR for content, API routes for organ bridges, strict client/server boundary.

## When to Use
- Scaffolding or modifying a Next.js app in the federation (cockpit, organ surfaces)
- Routing decisions — parallel/intercepting routes, group layouts, loading/error boundaries
- Data fetching strategy — server component fetch vs SWR vs ISR
- API route design for organ proxying (`/api/observatory/v1/*`)

## When NOT to Use
- Plain React without Next.js router — use `react-spa-discipline`
- Static site generation outside Vercel/Node — use Vite/build tool skill
- Backend logic that belongs in FastAPI or Express organ servers

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Keep page/route changes reversible; git stash before layout refactors |
| F2 TRUTH | `generateStaticParams` must match actual data; never fake revalidate values |
| F4 CLARITY | One data-fetching pattern per route group; no mixing server/client fetch |
| F7 HUMILITY | Default to `loading.tsx` + `error.tsx` on every route segment |
| F11 AUDIT | API routes log request origin; ISR revalidation events write to VAULT999 |
| F13 SOVEREIGN | Public-facing routes reviewed by Arif before deploy |

## Commands & Patterns

```bash
# Create a new route segment under app router
# /root/AAA/src/app/<segment>/page.tsx (server component by default)
# /root/AAA/src/app/<segment>/loading.tsx
# /root/AAA/src/app/<segment>/error.tsx

# ISR pattern — revalidate every 60s, on-demand revalidation endpoint
export const revalidate = 60;
// POST /api/revalidate?secret=<token>&path=<path>

# API route pattern — proxy to organ
export async function GET(req: NextRequest) {
  const res = await fetch(`http://localhost:8088/mcp`, { ... });
  return NextResponse.json(await res.json());
}

# Server component fetch — direct, no hooks
async function Page() {
  const data = await fetch('http://localhost:8088/health').then(r => r.json());
  return <pre>{JSON.stringify(data, null, 2)}</pre>;
}
```

## Refusal Surface
- ❌ Client-side data fetching when server component can do it
- ❌ `useEffect` for API calls that belong in `generateStaticParams` or RSC
- ❌ Mixing Pages Router and App Router in the same surface
- ❌ Hardcoding organ ports in client components — use env proxy
- ❌ Skipping error/loading boundaries on user-facing routes
