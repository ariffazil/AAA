# Witness Verification Addendum — RATIFICATION-2026-09-16 (F2)

Witness: 333-AGI, 2026-09-16 (post-ratification reconciliation pass).
Purpose: F2 TRUTH — the ratified DECISIONS stand (F13); the EVIDENCE TABLE
required disk reconciliation before downstream agents cite phantom paths.

## Verified REAL (disk-witnessed)

| Claim | Verdict | Evidence |
|---|---|---|
| Emerge map-sight ×7 + hubs | REAL | /root/work/code-intel/emerge/{7 views}/ GraphML+JSON + AAA emerge-configs/ |
| Python contracts (1 KEPT / 3 BROKEN) | REAL | AAA importlinter/ + machine runs this session |
| Supply chain ×5 + CODEOWNERS | REAL | cyclonedx endpoints verified; CODEOWNERS ×5 |
| CGC semantic layer | REAL | `/root/.local/bin/cgc` + `/root/.codegraphcontext` (27MB, falkordb): **3,610 files, 28,064 functions, 6,092 classes, 69 interfaces** — `cgc stats` this session (ratification said 3,611 files / 108,449 CALLS: file count ≈confirmed ±1; CALLS count not directly re-witnessed — plausible) |
| codebase-reality skill | REAL | /root/AAA/skills/codebase-reality/SKILL.md (60 lines, in 19ecc5d77) |
| Ratchet CI (post-ratification extension) | REAL+GREEN | arifOS/GEOX/WEALTH `09-boundary-ratchet.yml` — all completed/success on main (GEOX 005740ca via cherry-pick off feature branch where 4128750a originally landed by accident) |

## NOT on disk (phantom paths cited in ratification + SKILL.md)

- `ledger/exceptions-ledger.json` (FI-003 v1) — ABSENT. **Superseded by real per-repo ledgers**: arifOS/GEOX/WEALTH `boundary/EXCEPTIONS-LEDGER.json` (4 seeded entries total, expiry 2026-12-15).
- `schema/code-reality-envelope.v1.json` + `code-reality-reconciliation.v1.json` — ABSENT. SKILL.md line 48 still references them → **broken pointer inside a committed skill**.
- `gates/`, `journeys/` (TS gate + Journey-1 PLAUSIBLE bundle) — ABSENT on KVM8 (may live on FI-003's own machine; UNVERIFIABLE here).
- `forge_work/2026-09-16-code-intel-phase0/` — ABSENT (only `2026-09-16/site-audit` exists).

## Open decision briefs (F13 pen — prepared by 333-AGI)

### 1. Envelope naming (FRAME collision)

- External spec name "CodeRealityFrame" collides with FRAME organ (:18085, observer, OBSERVE_ONLY).
- Naming doctrine (F13_RATIFIED 2026-09-15): compression, not labeling; one name = one referent.
- **Recommendation A (mine): `CodeRealityEnvelope`** — zero collision, matches existing "evidence-bundle" framing in SKILL.md line 48, compresses (envelope = container of 5 evidence classes).
- Option B: `RealityDossier` (closer to SKILL.md's "repo dossiers" language).
- Option C: keep CodeRealityFrame + namespace prefix `code-reality.frame` — NOT recommended: agent-facing ambiguity with FRAME organ violates one-name-one-referent.

### 2. arifFlow reconciliation wiring (epistemic_label enum)

- Live enum (arifFlow/src/receipt.rs:91): Observation|Derivation|Interpretation|Specification|Seal.
- Silent-400 scar: senders passing unknown labels get silent rejection.
- **Recommendation A (mine): DO NOT extend the enum.** Map reconciliation receipts onto existing labels: `step_type=Verify`, `epistemic_label=Derivation`, `payload.kind="code_reality_reconciliation"`. Rationale: 5-label taxonomy is federation-wide doctrine (F2 evidence classes used by every agent); a 6th class = doctrine churn for zero analytic gain (payload.kind already distinguishes).
- Option B (if F13 wants first-class visibility in FQ analytics): add variant `Reconciliation` — prepared patch shape: one enum arm + Display match arm + MCP schema sync + daemon rebuild/restart (:7073, ~5s downtime). Landing only on F13 word.

### 3. Graphiti drift — CLOSED this session

- Forensics: container zepai/knowledge-graph-mcp started 2026-09-15T17:10:21Z manually (restarts=0, policy unless-stopped); systemd unit graphiti-mcp.service exists but DISABLED; historical /mcp traffic present, **zero connections/traffic in final check**; no cron/watchdog references; only .bak configs mention it.
- Action taken: `docker stop graphiti-mcp` (T2 announced) — completes the 2026-09-04 888 retirement. Container+image preserved (F1 reversible). Endpoint :18412 now dead. ollama-docker-bridge.service header comment still names graphiti as consumer — stale comment, noted for the infra ledger.
- If resurrection recurs: suspect manual actor, not automation (all automated lanes verified absent).

### 4. CI fail-on-NEW activation (888 HOLD — standing)

- Current state: ratchet workflows run on push/PR, path-filtered, ALL GREEN, but are NON-BLOCKING (not required checks).
- Standing 888 HOLD in RATIFICATION requires explicit F13 authorization for blocking activation (branch protection required checks).
- Prepared activation packet: add `09-boundary-ratchet.yml` to required status checks for main on the 3 repos (gh api PUT /repos/{o}/{r}/branches/main/protection — needs admin:repo scopes already held). One word from sovereign activates; ledger expiries (2026-12-15) auto-tighten the ratchet after that.

Evidence labels: all rows OBS except "may live on FI-003's machine" (UNKNOWN) and recommendations (INT/SPEC, confidence 0.85).
