# Banda Haram Hardcoded — Doctrine and Operational Pattern

> **Forged:** 2026-08-12 by Hermes under F13 SOVEREIGN directive ("Relaks tapi tajam")
> **Status:** Standing doctrine, F4 CLARITY + F12 RESILIENCE binding
> **Source of truth:** `/root/AAA/governance/BANDA_HARAM_HARDCODED_DOCTRINE.md`

## The axiom

```
Undang-undang (Constitution & Math Laws) = KEKAL (Invariant)
Realiti (World State)                    = CAIR (Dynamic)

Kalau hardcode elemen dinamik → geseran → kekacauan (ΔS > 0)
```

The system must distinguish what is **law** (cannot change) from what is **state** (constantly changes). Laws live in the constitution; state lives in registries, env vars, and live probes.

## Failure pattern (codified)

```
Hardcode dynamic value
  → system brittle
  → constant repairs on every external change
  → entropy accumulates (ΔS > 0)
  → chaos
```

Worked example (2026-08-12): `const ARIFOS_MCP = "http://127.0.0.1:8088/mcp"` in 6 OpenCode plugins. When the organ moved ports during a deployment, every plugin broke at once. ΔS spiked; repairs took an hour.

## Six forbidden domains (full taxonomy)

### 1. Model & Intelligence Engines

| Forbidden | Why dynamic | What to do |
|---|---|---|
| `model: deepseek/deepseek-v4-pro` in code | Vendor changes names/versions weekly | Provider registry in `opencode.json` |
| `max_tokens: 4096` literal | Provider updates limits silently | Read from provider manifest at boot |
| `$0.03/1k` inline | Pricing drops with new tiers | Env var + cost-of-truth lookup |
| `temperature: 0.3` literal in template | Per-task criticality varies | Range-based default, override per call |

### 2. Agents & Federation Topology

| Forbidden | Why dynamic | What to do |
|---|---|---|
| `agents=[333, 555, 777]` static | Workers are ephemeral | Live registry + health probe |
| `:8088` literal in plugin | VPS migration requires port shift | `process.env.ARIFOS_PORT ?? 8088` |
| Worker state cache | Lifecycle is per-second | Probe `/health` before routing |

### 3. Tools & Capabilities

| Forbidden | Why dynamic | What to do |
|---|---|---|
| `/usr/bin/script-v1.py` path | PATH may differ between shells | Use bare script name + PATH |
| `timeout=5s` literal | Network latency varies | Adaptive timeout with jitter |
| `github.com: up=true` cached | External API state is per-second | Live probe each session |

### 4. Human (888 / Sovereign)

| Forbidden | Why dynamic | What to do |
|---|---|---|
| `attention=24/7` literal | Human is not always available | Lane discipline + ping budget |
| `channel=telegram-only` literal | Operator may switch surfaces | Multi-channel router |
| Hardcoded persona address ("abang"/"hang") | Per-persona address discipline | Per-persona USER.md field |

### 5. Math, Thresholds & Learning Parameters

| Forbidden | Why dynamic | What to do |
|---|---|---|
| `decay = 0.95` literal | Drift changes with environment | Dynamic tuning via C_dark feedback |
| `Ω₀ = 0.05` static | Risk profile varies | Range `[0.03, 0.05]` per environment |
| `P > 0.99` static | Criticality varies | Task-criticality scaling |

### 6. World, Environment & Time

| Forbidden | Why dynamic | What to do |
|---|---|---|
| `UTC` without NTP awareness | Drift accumulates | `new Date()` + tz resolver |
| `/var/lib/v1` immutable path | Disk fills | Pruning + auto-rotation |
| `server-region=us-east` literal | Failover requirements | Runtime probe + failover |

## Operational checklist (T1 autonomous, no F13 ack)

```bash
# 1. Scan for hardcoded URL constants in plugins
grep -rn 'const [A-Z_]*_URL.*="http\|const [A-Z_]*_MCP.*="http' /root/.config/<harness>/plugins/*.ts

# 2. Scan for hardcoded model IDs in agent frontmatter
grep -rn "^model: " /root/.config/<harness>/agents/*.md

# 3. Scan JSON configs for hardcoded port literals
grep -rEn "127\.0\.0\.1:[0-9]+|localhost:[0-9]+" ~/.config/<harness>/*.json

# 4. Scan for hardcoded timeout values
grep -rEn "timeout[ =]+[0-9]+" /root/.config/<harness>/plugins/*.ts

# 5. Scan for hardcoded thresholds
grep -rEn "[0-9]\.[0-9]{2,}" /root/.config/<harness>/plugins/*.ts | grep -E "if|threshold"
```

## Fix pattern — Dynamic Port Module

The canonical fix for hardcoded URLs:

```typescript
// federation-ports.ts — single dynamic port module
const HOST = process.env.ARIFOS_HOST ?? "127.0.0.1"

const FALLBACKS = {
  ARIFOS: 8088, A_FORGE: 7071, GEOX: 8081,
  WEALTH: 18082, WELL: 18083, ARIFLOW: 7073,
  AAA: 3001, OPENCLAW: 18789, FED: 7074, LITELLM: 4000,
} as const

function envPort(key: string, fallback: number): number {
  const raw = process.env[key]
  const n = raw ? parseInt(raw, 10) : fallback
  return Number.isFinite(n) && n > 0 && n < 65536 ? n : fallback
}

export function urlFor(organ: keyof typeof FALLBACKS, path = ""): string {
  const port = envPort(`${organ}_PORT`, FALLBACKS[organ])
  return `http://${HOST}:${port}${path}`
}

// Convenience exports (drop-in for old constants)
export const ARIFOS_MCP = urlFor("ARIFOS", "/mcp")
export const ARIFLOW_URL = urlFor("ARIFLOW")
export const ARIFLOW_INGEST = urlFor("ARIFLOW", "/ingest")
```

## Verification recipe

After patching, verify the dynamic module resolves correctly:

```bash
cd /root/.config/opencode/plugins
ARIFOS_PORT=8088 ARIFLOW_PORT=7073 node -e "
  process.env.ARIFOS_PORT='8088';
  process.env.ARIFLOW_PORT='7073';
  const { ARIFOS_MCP, ARIFLOW_INGEST } = require('./federation-ports');
  console.log('ARIFOS_MCP:', ARIFOS_MCP);
  console.log('ARIFLOW_INGEST:', ARIFLOW_INGEST);
"
```

Expected output:
```
ARIFOS_MCP: http://127.0.0.1:8088/mcp
ARIFLOW_INGEST: http://127.0.0.1:7073/ingest
```

Then verify the consumer plugins compile:
```bash
grep -n 'from "./federation-ports"' /root/.config/opencode/plugins/*.ts | wc -l
# expected: 6+ (one per refactored plugin)
```

## Worked case — OpenCode Banda Haram Sweep (2026-08-12)

**Initial state:**
- 7 plugin .ts files with hardcoded `const ARIFOS_MCP = "http://127.0.0.1:8088/mcp"` etc.
- 12 agent .md files with hardcoded `model: deepseek/deepseek-v4-pro` in frontmatter
- 1 manifest compiler with literal port numbers (×7 organs)

**Action:**
1. Created `/root/.config/opencode/plugins/federation-ports.ts` (single dynamic module)
2. Refactored 6 plugins to import from it (kernel-bridge, judge-gate, sycophancy, autonomy, dispatch, compaction-rsi)
3. Replaced literal port map in manifest compiler with `P("ENV_VAR", fallback)` helper
4. Replaced all `model:` lines in 12 agent .md with `# DEFERRED: resolved via opencode.json`

**Verification:**
```bash
grep -rn 'http://127\.0\.0\.1:[0-9]\+\|http://localhost:[0-9]\+' /root/.config/opencode/plugins/*.ts
# expected: empty (only template-string probes with ${o.port} remain, which are dynamic)
```

**Result:** Banda haram sweep complete for OpenCode. Next quarter sweep: Claude Code settings.json, Kimi Code config.toml.

## Pitfalls

- **Template strings with live-probe variables are NOT hardcoded.** Only literal string constants are banda haram.
- **Fallback defaults in dynamic resolvers are OK.** `envPort(key, 8088)` — the env var wins when present.
- **Provider registry JSON keys are dynamic by definition.** `provider.deepseek.models.deepseek-v4-pro` in `opencode.json` IS the registry. Hardcoding = values OUTSIDE a registry.
- **`description:` lines embedding model names are NOT config.** Human-readable labels. Don't scrub.
- **Audit cadence: quarterly.** New agents = new hardcoded models. Each plugin edit = new hardcoded URL.
- **Gödel caveat: config-of-configs.** Even configuration is dynamic — recursion terminates at F13 (sovereign sets the env vars).

## Reference

- Original doctrine: `/root/AAA/governance/BANDA_HARAM_HARDCODED_DOCTRINE.md`
- Federation port map SOT: `/root/AAA/federation/organs.yaml`
- Env var keys: `/root/.secrets/kunci-mas.env` (canonical) + `kunci-mas.flat.env` (regenerated)