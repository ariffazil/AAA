# Hermes Execution Log — Banda Haram Hardcoded (2026-08-12)

## Context
Applied the 6-domain taxonomy to Hermes (FI-008) after OpenCode (FI-001). F13 SOVEREIGN gave the full doctrine; Hermes received it and self-executed.

## Files Modified

| File | What | How |
|------|------|-----|
| `federation-ports.ts` (NEW) | OpenCode plugin port registry | `env-first` pattern: `envPort('KEY', fallback)` with exports for all organ URLs |
| `arifos-kernel-bridge.ts` | Remove 3 hardcoded URL constants | `import { ARIFOS_URL, ARIFOS_MCP, ARIFLOW_URL } from "./federation-ports"` |
| `arifos-judge-gate.ts` | Remove `const ARIFOS_MCP = "http://..."` | Same import from federation-ports.ts |
| `sycophancy-detector.ts` | Remove `const ARIFLOW_URL = "http://..."` | Import `ARIFLOW_INGEST as ARIFLOW_URL` |
| `arifos-compaction-rsi.ts` | Remove hardcoded `const ARIFLOW_URL` | Same pattern |
| `aaa-autonomy.ts` | Remove 2 constants + 5 inline URLs | Import constants; inline URLs → `urlFor('ORGAN')` |
| `aaa-dispatch.ts` | Remove `const AAA_URL + ARIFOS_MCP` | Import `ARIFOS_MCP, urlFor` |
| `arifos-federation-manifest-compiler.ts` | 7 organ port constants | `port: P("ARIFOS_PORT", 8088)` pattern (env var + fallback) |
| 12 × agent .md files | Hardcoded `model:` frontmatter | Replaced with `# DEFERRED: resolved via opencode.json provider registry` |
| `/root/HERMES/cognitive/config.py` | 11 cognitive constants in Python | GRANITE stays in Python; WATER loads from `cognitive-params.yaml` with F7 floor enforcement |
| `/root/HERMES/config/cognitive-params.yaml` (NEW) | YAML registry for WATER constants | Self-healing loop can update without restart |
| `/root/AAA/governance/BANDA_HARAM_HARDCODED_DOCTRINE.md` (NEW) | Standing doctrine | Full 6-domain taxonomy + operational rules |

## Key Patterns Discovered

### 1. Granite vs Water (D5 — Math Thresholds)

**GRANITE** = constitutional floor, F1-F13 bound, never changes without sovereign act
```python
CONFIDENCE_CAP: float = 0.90  # GRANITE: F7 HUMILITY floor
```

**WATER** = empirical, runtime-calibrated, YAML-driven
```python
OMEGA_0: float = max(OMEGA_0_FLOOR, _W.get("OMEGA_0", 0.03))
# WATER: loaded from cognitive-params.yaml, clamped to F7 floor
```

The `reload_params()` hook allows hot-reload without Python source change. F7 floor enforced at Python level (`max(0.03, ...)`).

**Pitfall:** Not all D5 constants are WATER — CONFIDENCE_CAP is explicitly constitutional. The granite/water decision is per-constant, not per-file.

### 2. Env-first refactoring for existing code (D6 — Timeouts & Paths)

**Pattern: preserve backward compat**
```python
# BEFORE:
timeout=60.0
host="127.0.0.1"
VAULT999_PATH = "/root/VAULT999"

# AFTER:
timeout=float(os.environ.get("HERMES_HEALTH_TIMEOUT", "60.0"))
host=os.environ.get("HERMES_HOST", "127.0.0.1")
VAULT999_PATH = os.environ.get("VAULT999_PATH", "/root/VAULT999")
```

**Critical:** The env var `fallback` value = the current hardcoded value. This means the behavior is identical until an env var is set. No risk.

### 3. The Self-Referential Drift Anti-Pattern

Hermes has a drift_monitor module that detects semantic drift in memory. But Hermes itself had topology drift — its hardcoded ports silently diverged from `organs.yaml` every time the federation topology changed.

> *The body that detects disease in others has the same disease in its own spine.*

**Detection rule:** After any topology change (new organ, port migration, VPS move), run:
```bash
grep -n "port:" /root/HERMES/config.yaml | head -20
grep -rn "ARIFOS_PORT\|GEOX_PORT" /root/.secrets/kunci-mas.env
```
Compare — if they don't match, drift exists.

### 4. Dual-file memory gotcha (D6 — File Paths)

Hermes memory lives at TWO locations:
- `/root/.hermes/memories/MEMORY.md` (global canonical, 4295 bytes)
- `/usr/local/lib/her Hermes-agent/profiles/aaa-hermes/memories/MEMORY.md` (profile-specific, 2887 bytes)

When compressing or writing memory, **both files must be updated**. Forgetting one causes silent divergence. The memory tool writes to the profile location.

### 5. Profile config DRY violation (D1 + D2)

Three profile directories (`hermes_asi`, `hermes_apex`, `hermes_forge`) each duplicate the same 12 organ port mappings from main `config.yaml`. Fix: header comment marking "INHERITED: defer to main config.yaml + federation_ports.py". True DRY requires a runtime loader (next iteration).

## Verification Scan (post-fix)

```bash
# No hardcoded 127.0.0.1:NUMBER in plugin .ts files
grep -rn 'http://127.0.0.1:[0-9]\+\|http://localhost:[0-9]\+' \
  /root/.config/opencode/plugins/*.ts | grep -v template | grep -v comment
# Result: 0 hits

# Python files: all URLs/paths use os.environ.get
grep -rn '127.0.0.1\|/root/VAULT999' \
  /root/.local/lib/hermes-agent/profiles/aaa-hermes/mcp_servers/*.py | grep -v 'os.environ'
# Result: only comment strings, no hardcoded values
```

## Related Doctrine
- `/root/AAA/governance/BANDA_HARAM_HARDCODED_DOCTRINE.md` — the full 6-domain standing directive
- F4 CLARITY (ΔS ≤ 0) — every env-first refactor reduces entropy by removing a future breakage surface
- F12 RESILIENCE — dynamic config survives vendor updates, port changes, VPS migration
