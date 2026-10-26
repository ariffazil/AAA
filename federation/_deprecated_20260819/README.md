# `_deprecated_20260819` — remaining contents are genuinely retired

**2026-10-25 — this folder used to hold two LIVE registries.** It was named *deprecated* but
`scripts/validate-aaa.mjs` read two of its files as source-of-truth. The validator's own error
labels already said `registries/agents.yaml:agents` and `registries/skills.yaml:skills`, proving
the intended location. See `canon/AGENT-REGISTRY-ALIGNMENT-2026-10-25.md` §4 D1 and INV-AR-3.

## Resolved

| File | Action | Why |
|---|---|---|
| `agents.yaml` | **moved → `registries/agents.yaml`** | 34-entry agent policy registry (autonomy, 888-hold scope, approval) — live input to `validate-aaa.mjs` |
| `skills.yaml` | **deleted** | strict subset of `registries/skills.yaml` (196 ⊂ 198, zero unique ids); its one differing entry carried a stale bot handle (`@AGI_ASI_bot` vs `@irfanclaw_arifos_bot`) |

## Still here (no executable consumer)

| File | Why it stays |
|---|---|
| `CAPABILITY_INDEX.json` | superseded capability snapshot |
| `call_map.yaml` | superseded routing map |
| `mcp-catalog.yaml` | superseded MCP catalogue |

## Rule

Nothing under a `_deprecated_*` path may be read by executable code.
Gate: `npm run validate:registry` → INV-AR-8.
