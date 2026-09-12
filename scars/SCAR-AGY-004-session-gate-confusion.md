# SCAR-AGY-004 - SESSION_GATE Confusion Cascade

Scar ID: SCAR-AGY-004 (catalog: Scar #21)
Domain: A-FORGE Tooling / Session Ownership / ACT Semantics
Severity: P1 (342 errors in 60 days across 6 tools)
Status: SEALED (autonomous scar extraction, 2026-09-12)
Confidence: 0.90

---

## 1. Failure Pattern

A-FORGE tools return SESSION_GATE errors when agents call them without session ownership. Distribution (60d):

  aforge_forge_vault        : 138 errors  ("Tool is IRREVERSIBLE. SESSION_UNKNOWN")
  aforge_forge_filesystem   :  73 errors  ("Tool is IRREVERSIBLE. SCT_VERIFY_...")
  aforge_forge_git          :  40 errors  ("Tool requires session ownership")
  aforge_forge_canonize     :  25 errors  ("Tool requires session ownership")
  aforge_forge_kernel       :  24 errors  ("Tool requires session ownership")
  aforge_forge_entropy_sweep:  42 errors  ("Tool requires session ownership")
                              -----
  TOTAL                     : 342 errors

## 2. The Echo

Agent treats A-FORGE tools as a "free library" callable from any context. The tool surface advertises itself as generic, but the governance layer requires:
1. An arifOS session_id bound to the calling actor
2. A valid ACT (legacy SCT) signed by the kernel
3. An audit trail with session chain hash

Without all three, the tool refuses. Agent retries with the same args.

## 3. The Law

Before any A-FORGE forge_* call:

1. Call arif_init(mode=init) FIRST. Capture session_id + session_token from response.
2. Pass session_id AND session_token to every forge_* call.
3. If tool returns SESSION_GATE: re-init, do NOT retry.
4. NEVER call forge_vault / forge_canonize / forge_kernel without explicit session_token.

Forbidden:
- Calling forge_* before arif_init
- Reusing a stale session_id from a previous session
- Calling forge_* from the orchestrator (only workers should mutate)

## 4. The Eureka (unused capability)

- arifos_arif_init(mode=init) - mint session + ACT in one call
- aforge_forge_lease(mode=request) - explicit lease for bounded mutation
- arifos_arif_route(intent=...) - delegates to right organ WITHOUT requiring A-FORGE session

## 5. Verified Fix

```python
# Step 1: Bind session (do this BEFORE any forge_* call)
init = arif_init(mode=init, actor_id=333-AGI, requested_authority=LIMITED_MUTATE)
session_id = init.session_id
session_token = init.session_token

# Step 2: Every forge_* call carries both
forge_vault(mode=read, name=..., session_id=session_id, session_token=session_token)
```

## 6. Hardening

- **A-FORGE forge_* tool docs**: state "REQUIRES arif_init session + ACT" in tool description
- **OPENCODE pre-tool-check**: emit warning if session_token is empty before forge_* call
- **FORGE-act-federation-ingress**: add a one-line `bound?` predicate

```yaml
scar_id: SCAR-AGY-004
n_incidents: 342
severity: P1
law: arif_init FIRST. Carry session_id + session_token into every forge_* call.
eureka: arif_init(mode=init) + forge_lease + arif_route
confidence: 0.90
```
