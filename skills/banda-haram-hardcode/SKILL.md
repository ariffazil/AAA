---
name: banda-haram-hardcode
description: Banda Haram Hardcode Doctrine — the granite-vs-water classification system that decides whether a value belongs in code or in a dynamic registry. Forged 2026-08-12 by F13 Sovereign Override as constitutional doctrine. Triggered when user says "don't hardcode", "make it dynamic", "use env vars", "configurable", or any request to make code values externally controllable. Class-level skill covering all 6 domains where dynamic-vs-static decisions must be made.
tags: [doctrine, hardcode, granite-water, env-first, dynamic-config, arif-foundation, federation]
floor_scope: [F1, F2, F4, F11, F13]
autonomy_tier: T1
version: 1.0.0
owner: 333-AGI
forged: 2026-08-12
forged_by: 333-AGI under F13 directive
related_skills:
  - helix-memory-compress (the doctrine in memory context)
  - ASI-drift-watch (drift detection that uses this doctrine)
  - FORGE-federation-manifest (federation topology contract)
---

# Banda Haram Hardcode Doctrine

> **Forged 2026-08-12 by F13 Sovereign Override.**  
> Constitutional law: arifOS federation MUST distinguish granite from water.
> Granite = constitutional invariants, water = empirical reality.
> Never confuse them.

## The Axiom

```
Undang-undang (Constitution & Math Laws) = KEKAL (Invariant)
Realiti (World State)                       = CAIR (Dynamic)
```

Hardcoding an element that is intrinsically dynamic creates **rigid systems** that accumulate **friction**, eventually exploding into chaos (`ΔS > 0`).

## The Granite-vs-Water Test

Before committing any value to source code, ask:

| Question | If YES → | If NO → |
|----------|----------|---------|
| Is this value constitutional? (F1-F13 bound) | GRANITE — stay in code | WATER — extract to registry |
| Does this value change across deployments? | WATER — extract to registry | Could be either |
| Does this value change with market feedback (C_dark)? | WATER — extract to registry | GRANITE candidate |
| Would changing this value require a re-deploy? | Bug — make it dynamic | Acceptable |
| Does this value reference external systems (URLs, IPs, ports)? | WATER — extract to registry | Could be either |

## The 6-Domain Taxonomy

Every hardcode candidate must be classified into one of these domains:

### Domain 1: Model IDs & Versions (WATER)
```python
# ❌ HARDCODE
model = "gemini-3.6-flash"

# ✅ DYNAMIC
model = config.get("model_picker", {}).get("primary", "zai-direct/glm-5.2")
```
- Model names change when vendors ship new versions
- Context windows & limits change per provider release
- Pricing & cost weights fluctuate with market
- **Resolution:** `model-picker.yaml` registry, read at runtime

### Domain 2: Ports & Topology (WATER — critical)
```python
# ❌ HARDCODED
host="127.0.0.1", port=8088

# ✅ DYNAMIC (env-first)
import os
host = os.environ.get("ARIFOS_HOST", "127.0.0.1")
port = int(os.environ.get("ARIFOS_PORT", "8088"))

# ✅ DYNAMIC (registry-first)
from federation_ports import get_port
port = get_port("ARIFOS")
```
- 12 organ ports must flow from `organs.yaml` (SOT)
- Move VPS → change a port → system breaks silently if hardcoded
- **Resolution:** `port-registry.json` + `federation_ports.py` resolver

### Domain 3: Tool Paths & Endpoints (WATER)
```python
# ❌ HARDCODED
path = "/root/VAULT999"
url = "http://127.0.0.1:18089/health"

# ✅ ENV-FIRST
path = os.environ.get("VAULT999_PATH", "/root/VAULT999")
url = os.environ.get("HERMES_AGENT_ENDPOINT", "http://127.0.0.1:18089/health")
```
- MCP servers, binary paths, `/usr/bin/...` change with system updates
- Network timeouts/latency thresholds change with load
- External API status is reality, not constant
- **Resolution:** env vars with sensible defaults; paths.yaml registry

### Domain 4: Human Parameters (WATER)
- Attention bandwidth (`W_scar` limits) — humans aren't 24/7
- Preferred communication channels — Telegram, CLI, Web UI all valid
- **Resolution:** lane config per human, not per system

### Domain 5: Math Thresholds (MIXED — GRANITE has pieces)
```python
# 🪨 GRANITE — constitutional, F7 HUMILITY floor bound
CONFIDENCE_CAP = 0.90  # F7 ceiling — DO NOT change without F13

# 💧 WATER — empirical, runtime-tuned
LAMBDA_DECAY = _W.get("LAMBDA_DECAY", 0.05)  # From cognitive-params.yaml
DRIFT_WARNING_THRESHOLD = _W.get("WARNING", 0.30)  # Adapt with C_dark
```
- **GRANITE:** floor/ceiling values, constitutional bounds (Ω₀ ∈ [0.03, 0.05])
- **WATER:** decay rates, risk weights, error budgets, confidence thresholds
- **Resolution:** `cognitive-params.yaml` for water, Python constants for granite

### Domain 6: Timeouts & Network (WATER)
```python
# ❌ MAGIC NUMBERS
timeout = 30.0  # hermes_a2a_listener.py
timeout = 3.0   # hermes_mcp.py

# ✅ DYNAMIC (YAML-driven)
from hermes_timeout_loader import a2a_listener
timeout = a2a_listener()  # Loads from cognitive-params.yaml
```
- Network physics fluctuates with load, latency, packet loss
- Magic numbers cause timeout-too-early (drop valid requests) or hang-too-long (waste resources)
- **Resolution:** `hermes_timeout_loader.py` reads from YAML

## The Fix Pattern (3 layers)

When auditing a system for hardcode violations:

### Layer 1: Build the registry
```python
# Build a JSON/YAML registry from current SOT
import json
registry = {
    "schema_version": "1.0.0",
    "generated": datetime.now().isoformat(),
    "doctrine": "Source-of-truth for X. Live health beats file.",
    "values": {...}
}
with open("registry.json", "w") as f:
    json.dump(registry, f, indent=2)
```

### Layer 2: Build the runtime resolver
```python
# federation_ports.py pattern
import os, json
_REGISTRY_CACHE = None

def _load():
    global _REGISTRY_CACHE
    if _REGISTRY_CACHE: return _REGISTRY_CACHE
    with open(REGISTRY_PATH) as f:
        _REGISTRY_CACHE = json.load(f)
    return _REGISTRY_CACHE

def get(key, *, default=None):
    # 1. Env var (highest priority)
    val = os.environ.get(key)
    if val: return val
    # 2. Registry (derived from SOT)
    return _load().get(key, default)
```

### Layer 3: Patch the consumers
For every `f = open("/path/hardcoded")`:
```python
# Before
f = open("/root/VAULT999/file.json")

# After
f = open(os.environ.get("VAULT999_PATH", "/root/VAULT999") + "/file.json")
```

## The Self-Audit Irony

> A system that detects drift in others while itself drifting silently.

When running `ASI-drift-watch` or any drift detector, also check that the **watcher's own config** is dynamic. If the watcher hardcodes what it watches, it's not a watcher — it's a blind spot with badges.

## Classification Decision Tree

```
Is this value referenced in F1-F13 floors?
├── YES → GRANITE (Python constant, F13-bound)
│         Examples: CONFIDENCE_CAP=0.90, Ω₀∈[0.03,0.05]
└── NO → is it empirical/runtime-tuned?
    ├── YES → WATER (YAML registry)
    │         Examples: LAMBDA_DECAY, DRIFT_WARNING_THRESHOLD, timeout=30.0
    └── NO → is it external world state?
        ├── YES → WATER (env-first resolver)
        │         Examples: ARIFOS_PORT, VAULT999_PATH, MODEL_NAME
        └── NO → is it a configuration value?
            ├── YES → WATER (config.yaml per-profile)
            │         Examples: default_agent, mcp server list
            └── NO → Investigate — likely a real constant, but double-check
```

## Anti-Patterns

| ❌ Pattern | Why it fails |
|-----------|-------------|
| Magic numbers in Python source | Drift on every config change |
| Hardcoded port numbers | System breaks silently on VPS migration |
| Inline model name strings | Vendor API rename → system dies |
| Constants in cognitive/config.py without YAML fallback | No self-healing possible |
| Per-profile model duplication (DRY violation) | High entropy, hard to keep in sync |
| Direct disk writes that bypass the verifier chain | Drift goes undetected |
| Timeouts from `time.sleep()` without measurement | Just guessing, not engineering |

## How to Apply This Skill

1. **When the user says "don't hardcode X":** Run the granite-vs-water test. If water, extract to registry.
2. **When editing any Python/JS/Go/Rust file:** Scan for literals in D1-D6 domains.
3. **When deploying a new organ:** Use `federation_ports.py` to discover its port, not a hardcoded value.
4. **When building a new registry:** Follow the source-of-truth chain — env → registry → SOT.
5. **When auditing drift:** Run on the watcher too, not just the watched.

## References

- `DOUBLE_HELIX_ECHO_SCAR.md` — the helix architecture this doctrine belongs to
- `HUMAN_MEMORY_DOCTRINE.md` — H1-H6 memory tiers
- `organs.yaml` — federation topology SOT
- `cognitive-params.yaml` — water constants for cognitive layer
- `port-registry.json` — derived port map from organs.yaml
- `federation_ports.py` — runtime port resolver

---

*Forged: 2026-08-12 from F13 Sovereign Override session.  
The body that detects disease in others must not have the same disease in its own spine. ⚒️ DITEMPA BUKAN DIBERI*