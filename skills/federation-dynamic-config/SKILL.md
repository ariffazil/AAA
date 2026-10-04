---
name: federation-dynamic-config
description: >
  Banda Haram Hardcoded doctrine — the 6-domain audit and execution pattern for
  eliminating hardcoded dynamic values from federation code. Covers: (1) Model IDs,
  (2) Ports & Topology, (3) Tool Paths, (4) Human Params, (5) Math Thresholds,
  (6) Timeouts & Network. Includes granite-vs-water classification, federation_ports
  module pattern (Python + TypeScript), cognitive-params.yaml registry, and the
  verification scan. Trigger: "ban hardcoded", "dynamic config", "Banda Haram",
  "fix all hardcoded", "env-first", or any port/model/path audit request.
  Doctrine source: /root/AAA/governance/BANDA_HARAM_HARDCODED_DOCTRINE.md
---

# Federation Dynamic Config — Banda Haram Hardcoded

The doctrine: **static values for dynamic domains = death.** Constitution is granite.
World state is water. When you hardcode water, the system becomes brittle and breaks
every time the outside world changes.

## The6 Domains (from sovereign directive, 2026-08-12)

| Domain | What's haram to hardcode | What's granite (OK to hardcode) |
|--------|--------------------------|--------------------------------|
| **1. Model IDs** | Model names, versions, vendor IDs | Provider registry structure (opencode.json) |
| **2. Ports & Topology** | Port numbers, IP addresses, agent roster | Authority ceiling definitions |
| **3. Tool Paths** | Filesystem paths, binary locations, API URLs | Path structure (relative) |
| **4. Human Params** | Attention bandwidth, channel preferences | F13 consent gate |
| **5. Math Thresholds** | OMEGA_0, decay rates, drift thresholds | CONFIDENCE_CAP (F7 floor) |
| **6. Timeouts & Network** | timeout seconds, retry counts, latency | Retry policy structure |

## The Failure Pattern

```
Hardcode dinamik → Sistem rapuh → Sistem repair setiap kali external change
→ Tenaga habis untuk repair → Entropy naik (ΔS > 0) → Kekacauan
```

## The Fix Pattern (3 layers)

### Layer 1: federation_ports module (Python/TypeScript)
Single source of truth for port resolution. Reads from env > organs.yaml SOT > defaults.

**Python pattern:**
```python
import os, yaml
from pathlib import Path

def url_for(organ: str, path: str = "") -> str:
    port = int(os.environ.get(f"{organ.upper()}_PORT", DEFAULTS[organ]))
    return f"http://127.0.0.1:{port}{path}"
```

**TypeScript pattern:**
```typescript
const P = (key: string, fallback: number) => {
  const v = process.env[key]; const n = v ? parseInt(v, 10) : fallback
  return (Number.isFinite(n) && n > 0 && n < 65536) ? n : fallback
}
export const ARIFOS_MCP = urlFor("ARIFOS", "/mcp")
```

### Layer 2: Path env-ification
```python
VAULT999 = os.environ.get("VAULT999_PATH", "/root/VAULT999")
HERMES_HOME = os.environ.get("HERMES_HOME", "/root/HERMES")
CRON_DIR = os.environ.get("HERMES_CRON_PATH", "/root/.hermes/cron")
```
Always: `os.environ.get("KEY", "current_value")` — backward compatible, env-overridable.

### Layer 3: cognitive-params.yaml (WATER constants)
Split Python constants into:
- **GRANITE** (constitutional, F7 bound): stays in Python source
- **WATER** (empirical, runtime-tuned): loaded from YAML, self-healing loop can update

```yaml
# cognitive-params.yaml
memory_decay:
  OMEGA_0: 0.03    # F7 floor = 0.03 (granite enforced in Python)
  LAMBDA_DECAY: 0.05  # tuned, will tune again
```

```python
# config.py
OMEGA_0_FLOOR = 0.03  # GRANITE — constitutional
OMEGA_0 = max(OMEGA_0_FLOOR, _W.get("OMEGA_0", 0.03))  # WATER — from YAML
def reload_params(): ...  # hot-reload without restart
```

## Execution Pattern (per harness)

1. **Scan** — `grep -rn "http://127.0.0.1:\|timeout=[0-9]\|model:.*[a-z]" <harness>/` to find violations
2. **Classify** — granite vs water for each violation
3. **Create** — federation_ports module + cognitive-params.yaml
4. **Patch** — env-first `os.environ.get()` / `process.env` replacements
5. **Annotate** — YAML config lines get `# env: ${VAR_NAME}` comments
6. **Verify** — py_compile + grep for remaining bare literals + runtime URL test

## Verification Checklist

```bash
# After patching, run this scan:
grep -rnE "127\.0\.0\.1:[0-9]+|localhost:[0-9]+" <harness>/  # Should find 0 non-env bare URLs
grep -rnE "timeout=[0-9]" <harness>/*.py  # Should find 0 non-env bare timeouts
python3 -c "from federation_ports import url_for; print(url_for('ARIFOS', '/health'))"
```

## Applied To (2026-08-12)

| Harness | Status | Files |
|---------|--------|-------|
| OpenCode | ✅ SEALED | federation-ports.ts, 6 plugins, 12 agent .md, manifest compiler |
| Hermes | ✅ SEALED | federation_ports.py, cognitive/config.py, config.yaml, 5 Python files |
| Codex | ⚠️ PARTIAL | config.toml has 44 refs (registry, not runtime) |
| AAA agent-cards | ⚠️ SOT | model IDs are definition, not runtime code |

## Pitfalls

- **Don't hardcode env var names.** If the env var is only ever read in one place, it's a renamed constant, not a config. Use the same env var name across all files for the same organ/param.
- **Don't change defaults when patching.** `os.environ.get("X", "current_value")` — the fallback MUST be the current hardcoded value. Zero behavior change on first deploy.
- **Don't touch registry SOT.** Agent-card.json model IDs ARE the source of truth — that's where you define which model an agent uses. The problem is runtime CODE that reads those IDs, not the registry itself.
- **YAML config comments ≠ env var resolution.** Config.yaml can't do `${VAR}` interpolation natively. Comments like `# env: ${ARIFOS_PORT}` are documentation for operators, not runtime resolution. The actual env-first logic lives in the Python/TS module.

## Related Skills

- `FORGE-route-least-power` — route tasks to smallest capability (complementary)
- `asi-agent-invariants` — operating constitution for all agents (overlapping governance)
- `hermes-persona-alignment` — persona config uses same env-first pattern

## References

- `/root/AAA/governance/BANDA_HARAM_HARDCODED_DOCTRINE.md` — the sovereign directive
- `/root/HERMES/scripts/federation_ports.py` — Python reference implementation
- `/root/.config/opencode/plugins/federation-ports.ts` — TypeScript reference implementation
- `/root/HERMES/config/cognitive-params.yaml` — WATER constants registry
