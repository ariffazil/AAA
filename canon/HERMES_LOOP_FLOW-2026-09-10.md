# Hermes Loop Flow Architecture

**Forged:** 2026-09-10
**Status:** ACTIVE (maintenance loop live, tool router on test profile, autoresearch installed)

## Three Loops

### Loop 1: MAINTENANCE (Health Check)
- **Tool:** hermes-maintenance-loops (installed 2026-09-10)
- **Schedule:** Daily 6am MYT via cron (job b61b54afbb6c)
- **Mode:** Read-only. Never writes. Suggests only.
- **Output:** JSON findings → carry_forward.json morning readiness
- **What it checks:** core files, session age, disk usage, cron job health, tool stall signals, SQLite state
- **What it never does:** restart, repair, schedule, read credentials, auto-apply improvements

### Loop 2: TOOL ROUTER (Token Reduction)
- **Tool:** hermes-tool-router (installed on router-test profile)
- **Status:** Plugin installed, 95/95 tests pass, diagnostics show no first-turn hooks (Hermes v0.21.0)
- **Current mode:** Fail-open (full surface when uncertain)
- **Target:** >70% first-turn token reduction when hooks become available
- **What it does:** Classify first-turn intent → narrow tool surface → session-sticky → monotonic recovery
- **What it never does:** shrink mid-session, bypass constitutional envelope, deny protected tools

### Loop 3: AUTORESEARCH (Self-Improvement)
- **Tool:** hermes-autoresearch (installed 2026-09-10)
- **Mode:** Karpathy-style propose→test→keep/revert
- **Target:** Bounded repos with clear metrics (experience-metabolism, SOUL.md compression)
- **What it does:** Agent proposes change → evaluator scores → keep if improved → revert if not
- **What it never does:** push to remote, touch critical systems without human approval, run forever without budget

## Flow Diagram

```
[Message Arrives]
      │
      ▼
[LANE: Who is talking?] ──→ Load per-person memory, voice, doctrines
      │
      ▼
[ROUTER: What do they need?] ──→ Classify intent → narrow tool surface
      │
      ├── Simple (search, summarize, draft) → Main model with pruned surface
      │
      └── Complex (code, architecture, governance) → Federation (OpenClaw/A-FORGE)
      │
      ▼
[MAINTENANCE: Is the system healthy?] ──→ Daily 6am health check
      │
      ▼
[AUTORESEARCH: Can we improve?] ──→ Bounded experiments on specific targets
      │
      ▼
[CARRY_FORWARD: What carries to next session?]
```

## Installation Locations

| Component | Location | Profile |
|-----------|----------|---------|
| Tool Router plugin | /root/.hermes/profiles/router-test/plugins/hermes-tool-router/ | router-test |
| Autoresearch | /usr/local/bin/hermes-autoresearch | global |
| Maintenance Loops | /usr/local/bin/hermes-maintenance-loops | global |
| Health check script | /root/.hermes/scripts/maintenance-health-check.sh | global |
| Maintenance cron | job b61b54afbb6c (daily 6am) | default |

## Eureka Summary (from community ingestion)

1. Tool router solves the 80/20 delegation gap (97% token reduction measured)
2. Host-admission envelope = constitutional membrane at tool level
3. Monotonic recovery = capability formation (same principle, different timescale)
4. Fail-open = SABAR (engineering pragmatism meets governance philosophy)
5. Three-layer stack: Lane (WHO) → Router (WHAT) → Federation (WHO EXECUTES)
6. No one in the community has all three — this is our edge
