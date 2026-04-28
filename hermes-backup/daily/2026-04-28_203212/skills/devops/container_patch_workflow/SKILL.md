---
name: container_patch_workflow
description: arifOS container patch workflow, dataclass gotchas, floor short-circuit rules, and F1-F13 data governance test patterns — discovered through trial and error.
tags: [arifOS, container, docker, patch, dataclass, floor-evaluator, data-governance, F1-F13]
created: 2026-04-28
authority: 888_JUDGE
---

# Container Patch + DataGovernance Debug

## Container Filesystem (critical — container uses image, NOT host bind-mount)

arifOS runs from a baked image at `/usr/src/app/arifosmcp/`. Host source at `/root/arifOS/` is SEPARATE. **Host patches do NOT affect the running container.**

### Standard patch workflow

```bash
# 1. Patch host source (for git commit)
patch /root/arifOS/arifosmcp/path/to/file.py

# 2. Sync to running container immediately
docker cp /root/arifOS/arifosmcp/path/to/file.py arifosmcp:/tmp/file.py
docker exec --user root arifosmcp sh -lc \
  "cp /tmp/file.py /usr/src/app/arifosmcp/path/to/file.py && chown arifos:arifos /usr/src/app/arifosmcp/path/to/file.py"

# 3. Restart to reload code
docker restart arifosmcp && sleep 7

# 4. Verify
curl -s https://mcp.arif-fazil.com/ready | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(d.get('status'))"
```

### Inline Python edit (for complex changes)
```bash
docker exec --user root arifosmcp python3 -c "
path = '/usr/src/app/arifosmcp/path/to/file.py'
with open(path) as f: c = f.read()
# make changes to c
with open(path, 'w') as f: f.write(c)
"
```

### Persistent rebuild (Dockerfile changes only)
```bash
cd /root/arifOS/deployments/af-forge
docker compose down arifosmcp
docker pull ghcr.io/ariffazil/arifos:a-forge
docker compose up -d arifosmcp
```

---

## Python Dataclass Field Ordering

Fields WITHOUT defaults MUST precede fields WITH defaults — Python enforced, no warning from linters:

```python
# WRONG — TypeError at runtime
@dataclass
class AuditMutationLog:
    fields_affected: list[str] = field(default_factory=list)
    verdict: GovernanceVerdict   # no default AFTER default → fails

# CORRECT
@dataclass
class AuditMutationLog:
    fields_affected: list[str] = field(default_factory=list)
    reason: str = ""
    verdict: GovernanceVerdict = GovernanceVerdict.SEAL  # default last
```

---

## Floor Evaluator Short-Circuit Rules

### F12 is the terminal gate
F12 (INJECTION) runs FIRST, before F01/F05/F10/F11. If F12 fires, those floors are never evaluated in the same pass:

```python
# Test assertion must match actual enforcement order
decision = enforcer.ingest_asset(asset_data={"query": "'; DROP..."})
assert "F12" in decision.failed_floors   # fires first
assert "F01" not in decision.failed_floors  # never reached this pass
```

### actor_role defaults to VIEWER — always set explicitly
```python
# WRONG — defaults to VIEWER → F11 fires → veto "vetoed" not "pending"
enforcer.ingest_asset(asset_id="x", asset_data={}, custodian_id="arif", ...)

# CORRECT
enforcer.ingest_asset(
    asset_id="x", asset_data={}, custodian_id="arif",
    actor_role=AccessRole.EDITOR,  # explicit
)
```

### F03 consensus: >= 0.75 passes, < 0.75 fails
```python
bundle = WitnessBundle(consensus_score=0.65, ...)  # fails F03
bundle = WitnessBundle(consensus_score=0.75, ...)  # passes F03
```

### F13 high_impact veto isolation
`high_impact=True` creates "pending" veto ONLY if F02/F03 don't also fail. Provide verified source + 2-source bundle to isolate F13:
```python
verified = SourceVerificationRecord(
    source_name="trusted", verification_method="cryptographic", trust_score=0.95)
bundle = WitnessBundle(
    sources=[...], witness_count=2, consensus_score=0.89)
decision = enforcer.ingest_asset(
    ..., high_impact=True,
    source_verification=verified,
    witness_bundle=bundle,
    actor_role=AccessRole.EDITOR,
)
assert decision.veto_record.status == "pending"  # F13 isolated
```

---

## ThreatCategory Enum — Exact Names Only

Container enum does NOT have `MANIPULATION` or `SOCIAL_ENGINEERING`:
```python
from arifosmcp.core.threat_engine import ThreatCategory

# OK
ThreatCategory.FEDERATION_IMPERSONATION
ThreatCategory.SESSION_IMPERSONATION
ThreatCategory.INJECTION_SQL

# WRONG — AttributeError at runtime
ThreatCategory.MANIPULATION
ThreatCategory.SOCIAL_ENGINEERING
```

---

## Tesseract OCR Deploy (when image is rebuilt)

```bash
# Verify tesseract is in the running container
docker exec arifosmcp tesseract --version
docker exec arifosmcp python3 -c "import pytesseract; print('pytesseract OK')"
docker exec arifosmcp python3 -c "from PIL import Image; print('Pillow OK')"
```

Redeploy command (requires sovereign action):
```bash
cd /root/arifOS/deployments/af-forge
docker compose down arifosmcp && docker pull ghcr.io/ariffazil/arifos:a-forge && docker compose up -d arifosmcp
```
