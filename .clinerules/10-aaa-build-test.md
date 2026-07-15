---
paths:
  - "src/**"
  - "package.json"
  - "vite.config.ts"
  - "tsconfig.json"
  - "tailwind.config.js"
  - "a2a-server/**"
  - "contracts/**"
  - "schemas/**"
---

# AAA Build, Test, Run Discipline

## Before Editing

Always run the live probes (Step 111 of Reflexion Loop):
```bash
curl -s http://localhost:3001/health         # AAA a2a server live
curl -s http://localhost:7071/health         # A-FORGE live (dependency)
npm run build -- --dry-run                   # build integrity
npm run lint                                 # code quality
python3 eval/run_aaa_eval.py --dry-run       # gold eval harness
```

If touching A2A:
```bash
curl -s http://localhost:3001/a2a/agents.json    # agent card integrity
curl -s http://localhost:18789/health            # OpenClaw gateway
```

## After Editing

Always verify:
```bash
npm run build                # MUST pass
npm run lint                 # SHOULD pass
npm run validate:aaa         # registry + contract + card consistency
npm run a2a:conformance      # A2A protocol conformance suite
```

## Forbidden Without 888_HOLD (ask Arif)

- Changing A2A authentication
- Modifying deliberation verdicts in `src/gateway/deliberation.ts`
- Editing the agent registry / agent card schema
- Vault seal policy changes
- Production deployments
- Anything that affects warga-vs-non-warga boundary

## TypeScript Rules

- Path alias `@/` → `src/` — use it, no `../../../` chains
- Strict mode is OFF — but you must still type your public APIs
- React 19 — use the new `use()` hook, server components only if explicitly needed
- shadcn primitives — extend, don't fork
- Tailwind 4 — use the new CSS-first config

## Commit Discipline

- Conventional commits: `feat(scope):`, `fix(scope):`, `chore:`
- Reference the agent: `feat(cockpit): ... [by AAA/333-AGI]`
- Tag consequential commits with `[HOLD-AUDIT]` if 888_HOLD was invoked

*DITEMPA BUKAN DIBERI*