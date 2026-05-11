# arifOS Container Patch Workflow

## Context
arifOS runs from a baked Docker image (`/usr/src/app/arifosmcp/`), **not** from host bind-mounted source (`/root/arifOS/`). Host edits to source files do NOT affect the running container.

## The Pattern

When modifying arifOS runtime code and wanting it deployed immediately (without rebuilding the image):

### Host edit → Container deploy
```bash
# 1. Edit host source normally
patch /root/arifOS/arifosmcp/runtime/foo.py

# 2. Copy to container (docker cp: HOST → CONTAINER)
docker cp /root/arifOS/arifosmcp/runtime/foo.py arifosmcp:/tmp/foo_new.py

# 3. Replace inside container
docker exec --user root arifosmcp sh -lc \
  "cp /tmp/foo_new.py /usr/src/app/arifosmcp/runtime/foo.py && \
   chown arifos:arifos /usr/src/app/arifosmcp/runtime/foo.py"

# 4. Restart container
docker restart arifosmcp

# 5. Verify health
curl -s https://mcp.arif-fazil.com/health
```

### Verify container is current BEFORE restart
```bash
# Check what's actually deployed
docker exec arifosmcp python3 -c "from arifosmcp.runtime.foo import bar; print('ok')"
```

## Common Failure Modes

### 1. Dataclass field ordering (silent TypeError)
Python raises `TypeError: non-default argument follows default argument` at **instantiation time**, not at definition.

```python
# WRONG — verdict (no default) after reason (has default)
fields_affected: list[str] = field(default_factory=list)
reason: str = ""
verdict: GovernanceVerdict  # 💥 TypeError when instantiated

# RIGHT — all required fields first, then all with defaults
fields_affected: list[str] = field(default_factory=list)
verdict: GovernanceVerdict = GovernanceVerdict.SEAL  # default as last field
reason: str = ""
```

**Symptom**: `TypeError: _write_audit() missing 3 required positional arguments` — this is actually the dataclass being instantiated with wrong field order.

**Fix**: Move `verdict` to last position with a default value.

### 2. Container import errors (module not found)
Container has its own `sys.path` and installed packages. A module that imports on host might fail in container:
```python
# Always check the container's actual imports first
docker exec --user arifos arifosmcp python3 -c "from arifosmcp.core.threat_engine import ThreatCategory; print([c.name for c in ThreatCategory])"
```

### 3. AttributeError on runtime objects
`ThreatAssessment` has `confidence` and `threats` but **no `severity`** field. Accessing `threat.severity` raises `AttributeError`.

```python
# WRONG
severity = threat.severity if threat.severity else 0.0

# RIGHT — derive from irreversibility
severity = threat.irreversibility / IrreversibilityLevel.CRITICAL.value
```

### 4. Enum categories differ between host and container
Container's `ThreatCategory` enum may not have categories that exist in host source:
```python
# Always verify what exists in container
docker exec arifosmcp python3 -c "from arifosmcp.core.threat_engine import ThreatCategory; print([c.name for c in ThreatCategory])"
```
Then use only confirmed-present values.

### 5. Audit log method signature mismatch
`_write_audit()` on `DataGovernanceEnforcer` takes individual fields (`decision_id`, `action`, `asset_id`, etc.), NOT a `decision` object:
```python
# WRONG
self._write_audit(decision=decision, action="ingest", asset_id=asset_id, ...)

# RIGHT
self._write_audit(
    decision_id=decision.decision_id,
    action="ingest",
    asset_id=asset_id,
    actor_id=actor_id,
    session_id=session_id,
    fields_affected=list(asset_data.keys()),
    verdict=GovernanceVerdict.VOID,
    reason="blocked at F12 gate",
)
```

## Pre-restart Validation
Always test imports and basic instantiation inside the container BEFORE restarting:
```bash
docker exec --user arifos arifosmcp python3 -c "
from arifosmcp.runtime.data_governance import DataGovernanceEnforcer
e = DataGovernanceEnforcer()
print('enforcer OK, audit_logs:', len(e.audit_logs))
"
```

## When to Rebuild Instead
If the change is in `__init__.py` exports, `pyproject.toml` dependencies, or Dockerfile, rebuild the image. Patching works for runtime logic changes only.
