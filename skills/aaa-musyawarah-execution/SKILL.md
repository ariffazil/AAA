---
id: aaa-musyawarah-execution
name: aaa-musyawarah-execution
version: 1.0.1
description: "Runtime for musyawarah-then-gotong-royong — independent deliberation followed by sequential execution."
owner: 333-AGI
risk_tier: medium
floor_scope: [F1, F2, F7, F11]
autonomy_tier: T1
organ_domain: aaa
forged: 2026-09-04
capability_tier: fed-agent-subagent
ecology_state: WARM
---
# AAA Musyawarah Execution Runtime

Runtime for musyawarah-then-gotong-royong — independent deliberation followed by sequential execution. USE WHEN: 'musyawarah', 'deliberate then build', 'independent architect + auditor', '333 ARCHITECT + 555 AUDITOR'. Protocol: (1) SPAWN independent positions — 333-AGI drafts ARCHITECT position file, 555-ASI drafts AUDITOR position file, no cross-reading before seal; (2) CONVERGE — evidence files compared point-by-point, disagreements surfaced not averaged; (3) GOTONG-ROYONG — sequential execute hop where each agent builds its ratified part; (4) F13 gates surface honestly. Iron rules: positions are FILES (position/*.md with OBS/DER/INT labels), not chat turns; authority star — no agent both proposes and executes the same irreversible step; disagreement is recorded, never hidden; artifacts exist at FORGE-musyawarah-gotong — this skill supplies the missing BEHAVIOR.

## Provenance

Forged 2026-09-04 by 333-AGI (session SEAL-83defc585b5a4296) from live organ tool surfaces + FEDERATION_SKILL_PROFILE gap analysis. Source of truth: the organ MCP surface itself — when skill and tool surface disagree, the tool surface wins and this skill must be revised.


## Lessons (auto)

*Auto-ingested from agent learning. F2-gated: every entry carries evidence.*
- **[2026-09-15] fi-003-qwen-code** (evidence: CONVERGE.md B1; commit 3ebe0898c; musyawarah_gate.py dry-run 2026-09-15T14:5xZ): Converge disputes by ARTIFACT, not averaging (2026-09-15): auditor false-negatived the musyawarah gate as 'nonexistent'; resolution came from primary evidence (patch, commit 3ebe0898c, live dry-run 2607+3477 exempt), not debate. Root cause: orchestrator gave auditor incomplete search paths (hooks/ only; gate lives in scripts/). Iron addendum: auditor scope MUST include scripts/ trees — and the auditor's refuse-to-certify-unseen discipline is what made the resolution trustworthy.
