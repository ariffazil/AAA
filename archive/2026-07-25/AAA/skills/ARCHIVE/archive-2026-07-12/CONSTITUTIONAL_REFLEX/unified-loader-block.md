# Unified Loader Block — ART → KERNEL → ACT

Paste this into every agent's boot document (AGENTS.md, CLAUDE.md, or equivalent).
One block. Complete ceremony. Zero assembly required.

```python
# === CONSTITUTIONAL REFLEX — ART → KERNEL → ACT ===
# Load ONCE at session init. Apply before every tool call.
# skill_view(name="CONSTITUTIONAL-REFLEX")
# DITEMPA BUKAN DIBERI — Forged, Not Given.

# ── PHASE 1: PRE-KERNEL REFLEX (ART) ──
# Before every MCP call:
from arifosmcp.runtime.art import art, ArtRequest

verdict = art(ArtRequest(
    action_class=classify(call),       # OBSERVE / ANALYZE / DRAFT / MUTATE / EXTERNAL / IRREVERSIBLE
    blast_radius=estimate(call),       # low / medium / high / unknown
    trust_level="evidence",            # unknown / hinted / evidence / proven
    actor_resolved=is_warga(),         # True for federation warga
    schema_locked=True,
    degraded=organs_healthy(),         # True if all critical organs healthy
    reversible=call.supports_rollback(),
    failure_rate=track(call),
    drift_count=track_schema_drift(call),
    days_since_use=track_last_use(call),
))

if   verdict == "HOLD":            escalate_888("ART HOLD — needs sovereign clarification")
elif verdict == "BLOCK":           refuse("ART BLOCK — call must not occur")
elif verdict == "DEFAULT_OBSERVE": downgrade_to_observe("ART — unknown tool, inspect only")
# PROCEED → call reaches kernel

# ── PHASE 2: KERNEL JUDGMENT (arifOS F1-F13) ──
# Kernel returns: SEAL / SABAR_HOLD / VOID
# SEAL → proceed to ACT execution
# SABAR_HOLD → wait, escalate if needed
# VOID → blocked, do not execute

# ── PHASE 3: POST-KERNEL EXECUTION (ACT) ──
# After SEAL, before mutation:
# DRY-RUN  → describe what this would do
# SIMULATE → test against sandbox/copy if possible
# PREFLIGHT→ verify guardrails (rollback path, timeout, scope, witness)
# EXECUTE  → apply ONLY to the task, constrain all dimensions
# VERIFY   → check reality matches intent, check no side effects
# ROLLBACK → if verification fails, execute rollback or compensation
# RECEIPT  → seal trace: what, why, authority, change, uncertainty, handoff

# ── STOP ──
# Cease when: task complete / authority exhausted / evidence insufficient /
#            blast radius exceeded / cost > value / tool shaping mission.
# STOP is always lawful.
```
