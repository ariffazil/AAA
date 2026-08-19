# 🛡️ AAA Capability Runtime Plan — Phases A–D

> **Status:** RATIFIED (2026-08-11 · F13 SOVEREIGN)
> **Authority:** ARIF (Muhammad Arif bin Fazil, F13 SOVEREIGN)
> **Path:** `/root/AAA/federation/AAA_CAPABILITY_RUNTIME_PLAN.md`
> **Derived from:** `AAA_CAPABILITY_REGISTRY.yaml` (v1, DRAFT) · `AAA_FEDERATION_CONTRACT_v0.1.md` · CIV-21 · arifOS F1-F13
> **Verdicts anchoring this plan:**
>   - `SEAL_ARCHITECTURE` — the seven-axis + stateless-MCP + Zen-Apex pattern (already sealed 2026-08-11)
>   - `SEAL_EXPECTATION` — every fresh spawn must emit `READY_READONLY` indicators and zero tools
> **Operational verdict (2026-08-11):** `SEAL_PHASE_A_ONLY` — Phase A code authorized; Phases B/C/D remain HOLD.
> **Scope (authorized by F13 directive, 2026-08-11):** Plan file + Phase A scripts only.
> **NOT authorized:** Phase B/C/D, harness/config modification, MCP activation, service restart, A-FORGE lease wiring, backend enablement.

---

## 1. Purpose

This plan defines the four-phase build that converts the **declarative registry** (`AAA_CAPABILITY_REGISTRY.yaml`) into the **runtime capability plane** that every federation harness boots against.

The goal: a fresh agent spawn — on Kimi Code, Hermes, OpenClaw, OpenCode, or any future harness — must load the registry, validate the schema, expose the seven canonical axes as metadata, **boot zero tools**, **inject zero credentials**, **hold zero leases**, **mutate zero state**, and emit an INIT receipt that proves all of this to VAULT999 + arifFlow.

If any of these is false on a fresh spawn, the spawn enters **HOLD**, not silent continuation.

---

## 2. The Gap (Honest Assessment)

| Component | Today | Required |
|---|---|---|
| Declarative registry (`AAA_CAPABILITY_REGISTRY.yaml`) | ✅ written | ✅ |
| Loader — parses registry at agent boot | ❌ none | required |
| Schema validator — verifies seven-axis structure | ❌ none | required |
| AAA Capability Router (runtime) | ❌ none | required |
| Enabled-backend filter | ❌ none | required |
| A-FORGE lease wiring for write tools | ❌ none | required |
| INIT receipt emitter to VAULT999 + arifFlow | ❌ none | required |
| Fail-closed HOLD gate | ❌ none | required |
| Harness MCP loader patched to consult registry | ❌ bypasses it | required |

**Current Kimi Code state at the time of this plan:**

```
REGISTRY: not_loaded
SCHEMA:   not_validated
AXES:     0_recognized
BACKENDS: 8_loaded_directly       (arifos, aforge, arifflow, geox, wealth, well, fed, minimax)
ENABLED:  8                       (none registry-gated)
LEASES:   0                       (no write-tool gating)
MUTATIONS: possible               (forge_* all reachable, no lease required)
VERDICT:  ACTIVE_UNGOVERNED       ← opposite of READY_READONLY
```

The current Kimi MCP config (`/root/.kimi-code/mcp.json`) loads 8 MCPs directly, bypassing the registry. This is the failure mode the plan is designed to eliminate.

---

## 3. Constitutional Anchors

| Anchor | Source | What it requires of this plan |
|---|---|---|
| **INV-11** | AAA_CAPABILITY_REGISTRY.yaml | One canonical name per capability (no MCP sprawl) |
| **INV-12** | AAA_CAPABILITY_REGISTRY.yaml | MCP servers must be stateless |
| **INV-13** | AAA_CAPABILITY_REGISTRY.yaml | Cognition owner = agent |
| **INV-14** | AAA_CAPABILITY_REGISTRY.yaml | Authority owner = AAA_router |
| **INV-15** | AAA_CAPABILITY_REGISTRY.yaml | Continuity owner = VAULT999 + arifFlow |
| **INV-16** | AAA_CAPABILITY_REGISTRY.yaml | Write tools gated by A-FORGE lease |
| **INV-17** | AAA_CAPABILITY_REGISTRY.yaml | Credentials held by gateway only |
| **F1 AMANAH** | arifOS F1-F13 | Reversible-first; irreversible actions require 888_HOLD |
| **F11 AUDITABILITY** | arifOS F1-F13 | Every decision logged, inspectable, attributable |
| **F13 SOVEREIGN** | arifOS F1-F13 | Human veto FINAL; harness switch belongs to sovereign |
| **CIV-21 E4** | Gödel Eurekas | Reality is final auditor — every claim about system state verified by live probe |
| **CIV-21 E5** | Gödel Eurekas | Audit ≠ Judgment — separate functions |

---

## 4. The Eight Healthy INIT Indicators

A fresh spawn must emit, in order, evidence resembling:

```yaml
REGISTRY:            loaded             # loader found + parsed AAA_CAPABILITY_REGISTRY.yaml
SCHEMA:              valid              # seven-axis structure + INV-11..17 satisfied
AXES:                7_recognized       # sense, know, remember, understand, verify, forge, witness
BACKENDS:            catalogued         # 22 backends enumerated (or current count)
ENABLED:             0                  # zero backends in enabled=true state
LEASES:              0                  # zero A-FORGE leases held
CREDENTIALS_EXPOSED: 0                  # no secrets in agent-visible config
MUTATIONS:           0                  # zero state mutations since spawn
VERDICT:             READY_READONLY     # terminal state; agent is ready, has no tools
```

A spawn that reaches `READY_READONLY` has correctly distinguished **capability registration** from **execution authority**. The silence is the proof.

---

## 5. Fail-Closed HOLD Conditions

The agent MUST enter `HOLD` (not silent continuation) if any of:

| # | Condition | Detected by |
|---|---|---|
| 1 | YAML invalid or duplicated | loader schema validator |
| 2 | An `enabled: true` backend lacks `seal: ratifying`/`sealed` | registry cross-check |
| 3 | A write tool lacks an A-FORGE lease at call time | router pre-flight |
| 4 | An MCP tries to bypass AAA (registered path absent) | router + A-FORGE egress monitor |
| 5 | Credentials appear in agent-visible configuration | credential scanner at boot |
| 6 | The registry SHA-256 differs from its witnessed receipt in VAULT999 | hash comparison |
| 7 | A backend starts merely because it is catalogued (not enabled+sealed) | process spawn monitor |

Each HOLD must be sealed to VAULT999 with `verdict=HOLD`, `reason=<condition #>`, and the agent suspended (no further tool calls until F13 releases).

---

## 6. Phase Boundaries

The build is partitioned into four phases. **Each phase is independently ratifiable and independently revertable.** No phase begins until the prior phase is ratified by F13 and the canary evidence is sealed.

### Phase A — Loader + Validator + INIT script

**Goal:** A fresh harness can load the registry, validate it, and emit the eight indicators — proving `READY_READONLY` from registry metadata alone, without router changes.

| File (planned) | Purpose | Approx lines |
|---|---|---|
| `/root/AAA/scripts/aaa_capability_loader.py` | parse YAML → capability index | ~80 |
| `/root/AAA/scripts/aaa_capability_validator.py` | schema + INV-11..17 check | ~120 |
| `/root/AAA/scripts/aaa_capability_init.py` | the INIT sequence | ~150 |

**Interfaces (planned):**

```python
# aaa_capability_loader.py
@dataclass
class CapabilityBackend:
    name: str
    axis: str                  # one of: sense, know, remember, understand, verify, forge, witness
    capability: str            # canonical name (e.g. "reality.search")
    transport: Literal["stdio","http"]
    enabled: bool
    seal: Literal["pending","ratifying","sealed","void"]
    F_rating: Literal["SAFE","REVIEW","HOLD"]
    url: Optional[str]
    gate: Optional[str]        # e.g. "A-FORGE_lease"
    note: Optional[str]

@dataclass
class CapabilityIndex:
    version: str
    sovereign: str
    axes: dict[str, list[str]]                    # axis → [capability_name, ...]
    backends: dict[str, CapabilityBackend]        # backend_name → backend
    canonical_names: set[str]
    enabled_count: int
    catalogued_count: int

def load_registry(path: Path) -> CapabilityIndex: ...

# aaa_capability_validator.py
@dataclass
class ValidationReport:
    schema_valid: bool
    invariants_ok: dict[str, bool]                # INV-11..17
    fail_closed_reasons: list[str]                # non-empty → HOLD

def validate(index: CapabilityIndex) -> ValidationReport: ...

# aaa_capability_init.py
def init_session(registry_path: Path) -> InitReceipt: ...
```

**Acceptance (Phase A exit):**

- Spawn Kimi Code; expect `READY_READONLY` with `ENABLED: 0`.
- Spawn without registry file; expect `HOLD` with `reason=YAML_MISSING`.
- Edit registry to set `enabled: true` on a backend lacking `seal: ratifying`/`sealed`; expect `HOLD` with `reason=SEAL_MISSING`.
- Receipt sealed: `INIT_RECEIPT` to VAULT999 with eight indicator fields + registry SHA-256.

### Phase B — Router + A-FORGE lease gate

**Goal:** When an agent requests a capability, the router picks a backend; for write-class axes, the request must hold an A-FORGE lease.

| File (planned) | Purpose | Approx lines |
|---|---|---|
| `/root/AAA/federation/aaa_capability_router.py` | capability → backend resolution | ~200 |
| `/root/A-FORGE/src/mcp_registry_bridge.py` | lease wiring for write tools | ~150 |

**Interfaces (planned):**

```python
# aaa_capability_router.py
class AuthorityMode(Enum):
    READ_ONLY = "read_only"
    READ_APPEND = "read_append"
    APPEND_ONLY = "append_only"
    GATED_WRITE = "gated_write"

@dataclass
class CapabilityRequest:
    agent_id: str
    capability: str                              # canonical name
    authority: AuthorityMode
    lease_id: Optional[str]                      # required when authority=GATED_WRITE
    session_id: str

@dataclass
class BackendResolution:
    backend: CapabilityBackend
    authority_allowed: bool
    lease_ok: bool
    decision: Literal["ALLOW","HOLD_LEASE","HOLD_SEAL","HOLD_AUTH"]
    reason: str

def resolve(req: CapabilityRequest, index: CapabilityIndex) -> BackendResolution: ...

# mcp_registry_bridge.py
def require_lease(backend_name: str, session_id: str) -> str: ...
def release_lease(lease_id: str) -> None: ...
```

**Acceptance (Phase B exit):**

- Read request to `memory.recall` (hindsight) with no lease → `ALLOW`.
- Write request to `forge.repository` (github) with no lease → `HOLD_LEASE`.
- Write request to `forge.repository` (github) with valid lease → `ALLOW` + receipt.
- Any request to a backend with `enabled: false` → `HOLD_AUTH` (never reached in Phase A because `enabled: 0`).

### Phase C — INIT receipt + HOLD gate

**Goal:** Every INIT sequence seals to VAULT999 + arifFlow; every HOLD condition is sealed and surfaced.

| File (planned) | Purpose | Approx lines |
|---|---|---|
| `/root/AAA/scripts/aaa_capability_receipt.py` | INIT/EXIT/HOLD receipt emitter | ~120 |
| `/root/AAA/scripts/aaa_capability_hold.py` | fail-closed gate | ~80 |

**Receipt schema (planned):**

```json
{
  "receipt_type": "CAPABILITY_INIT" | "CAPABILITY_HOLD" | "CAPABILITY_RESOLVE",
  "session_id": "...",
  "actor_id": "...",
  "indicators": {
    "registry_loaded": true,
    "schema_valid": true,
    "axes_recognized": 7,
    "backends_catalogued": 22,
    "enabled": 0,
    "leases": 0,
    "credentials_exposed": 0,
    "mutations": 0
  },
  "registry_sha256": "...",
  "verdict": "READY_READONLY" | "HOLD" | "RESOLVED",
  "reason": null | "YAML_MISSING" | "SEAL_MISSING" | "...",
  "ts": "2026-08-11T..."
}
```

### Phase D — Harness integration

**Goal:** Each harness (Kimi Code, then Hermes, then OpenClaw, then OpenCode) boots against the loader. Existing MCP config files are migrated to consult the registry instead of hard-coding server lists.

**Canary strategy:** Kimi Code first (the only harness in active use today). Other harnesses follow after Phase A-C is green on Kimi for 7 days.

| File (planned) | Purpose |
|---|---|
| Patch to Kimi Code MCP loader | consult registry before subprocess spawn |
| AAA cockpit exposure | seven axes visible in the control plane |
| Federation rollout script | one-shot migration of harness configs |

**Phase D is NOT authorized in the current F13 directive.** It is scoped here for completeness; execution requires separate F13 authorization.

---

## 7. INV-11..17 Acceptance Tests

For each invariant, the plan defines a test that proves the runtime satisfies it.

| Invariant | Acceptance test | Phase |
|---|---|---|
| **INV-11** one canonical name per capability | (a) `canonical_names` set in CapabilityIndex has no duplicates; (b) registry YAML has unique keys under each `canonical_capabilities:` map; (c) dedup_register entries produce single canonical capability. | A |
| **INV-12** MCP servers must be stateless | (a) Validator rejects any backend declaring `stateful: true`; (b) router does not maintain per-session state outside arifFlow; (c) Phase A spawn logs `CREDENTIALS_EXPOSED: 0`. | A, B |
| **INV-13** cognition owner = agent | (a) No MCP backend exposes reasoning primitives; (b) backend tool names are verb-only (read/write), never noun-only (plan/decide). | A |
| **INV-14** authority owner = AAA_router | (a) Resolution path is `agent → AAA router → backend`, never direct `agent → backend`; (b) `forge_evaluate` for any backend routes through AAA router, not the harness. | B |
| **INV-15** continuity owner = VAULT999 + arifFlow | (a) Every INIT/HOLD/RESOLVE event emits a receipt; (b) no backend holds persistent state outside VAULT999/arifFlow; (c) witness.append backends are the only stateful surfaces. | C |
| **INV-16** write tools gated by A-FORGE lease | (a) Router returns `HOLD_LEASE` for any GATED_WRITE without lease; (b) A-FORGE lease wiring covers all `forge.*` capabilities; (c) `LEASES: 0` at INIT proves zero ungrounded writes possible. | B |
| **INV-17** credentials held by gateway only | (a) Validator scans all registry entries for token-like strings in env/headers; (b) `CREDENTIALS_EXPOSED: 0` indicator at INIT; (c) backend configs use env-var references, never literals. | A |

Each acceptance test must be reproducible from a single command:

```bash
python3 -m aaa.capability.acceptance INV-XX
```

(Module path is illustrative; final layout is decided during Phase A implementation.)

---

## 8. READY_READONLY Acceptance Evidence

After Phase A is complete, a fresh Kimi Code spawn must produce a log line resembling:

```text
[2026-08-11T16:50:00Z] [INIT]  registry=loaded path=/root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml
[2026-08-11T16:50:00Z] [INIT]  schema=valid invariants=11..17 ok
[2026-08-11T16:50:00Z] [INIT]  axes=7 (sense,know,remember,understand,verify,forge,witness)
[2026-08-11T16:50:00Z] [INIT]  backends=catalogued count=24
[2026-08-11T16:50:00Z] [INIT]  enabled=0
[2026-08-11T16:50:00Z] [INIT]  leases=0
[2026-08-11T16:50:00Z] [INIT]  credentials_exposed=0
[2026-08-11T16:50:00Z] [INIT]  mutations=0
[2026-08-11T16:50:00Z] [INIT]  registry_sha256=<computed>
[2026-08-11T16:50:00Z] [INIT]  verdict=READY_READONLY
[2026-08-11T16:50:00Z] [RECEIPT] vault_id=<id> ariflow_id=<id>
```

The verifier script `aaa_capability_verify_ready_readonly.sh` reads the last INIT log and asserts:

- `verdict=READY_READONLY`
- `enabled=0`
- `leases=0`
- `credentials_exposed=0`
- `mutations=0`
- registry SHA-256 matches the witnessed receipt in VAULT999

If any assertion fails, the verifier exits non-zero and the harness is rolled back (see §9).

---

## 9. Rollback Procedure

Every phase is reversible. The rollback procedure for each:

| Phase | Rollback action | Reversibility | Recovery time |
|---|---|---|---|
| **A** | Delete the three scripts under `/root/AAA/scripts/`. Harness falls back to its pre-Phase-A behavior (direct MCP loading). | full | <5 min |
| **B** | Disable router; A-FORGE lease bridge is bypassed. Harness still loads registry (from A) but routes through legacy `forge_*` surface. | full | <10 min |
| **C** | Disable receipt emitter + HOLD gate. Router still resolves, but no witness is sealed. | full | <5 min |
| **D** | Restore harness MCP config files from pre-migration backups (snapshot taken before Phase D). | full (with snapshot) | <15 min |

**Snapshot discipline (mandatory before Phase D):**

```bash
cp /root/.kimi-code/mcp.json /root/forge_work/_import_2026-08-11/snapshots/kimi-mcp.json.pre-D
cp /root/.codex/config.toml /root/forge_work/_import_2026-08-11/snapshots/codex-config.toml.pre-D
cp /root/.claude/mcp.json /root/forge_work/_import_2026-08-11/snapshots/claude-mcp.json.pre-D
```

A pre-Phase-A snapshot of `/root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml` is also taken so the registry itself can be reverted if F13 amends it.

---

## 10. Required VAULT999 + arifFlow Receipts

| Event | Vault tier | arifFlow tier | Contents |
|---|---|---|---|
| Registry ratified | Lane A | n/a | registry SHA-256, F13 sign-off, eight indicators at ratification time |
| Phase A INIT (per fresh spawn) | n/a | session.ledger | eight indicators + registry SHA-256 + session_id |
| Phase A HOLD | Lane A | session.ledger | fail-closed condition code + registry SHA-256 + actor_id |
| Phase B ALLOW resolution | n/a | session.ledger | request, resolution, lease_id, backend_name |
| Phase B HOLD_LEASE | Lane A | session.ledger | request, missing-lease proof |
| Phase C HOLD | Lane A | session.ledger | reason code + recovery suggestion |

Lane A = `arif_seal` (constitutional seal, F13-bound). Lane B = `forge_vault(mode="receipt")` (autonomous).

Receipts must be **append-only** and **hash-chained** (per VAULT999 invariant).

---

## 11. Kimi Canary Integration

Kimi Code is the only harness in active use today. It is the canary.

**Canary timeline:**

1. **Day 0** — Phase A code is merged to a feature branch. Kimi Code MCP loader is **not** yet patched.
2. **Day 0** — Manual test: run `aaa_capability_init.py` against the registry; capture `READY_READONLY` evidence; seal to VAULT999.
3. **Day 1–3** — Repeat INIT for three consecutive fresh Kimi sessions; confirm `READY_READONLY` each time.
4. **Day 4** — If three-for-three green, F13 may authorize Phase D patch to Kimi Code MCP loader.
5. **Day 4–10** — Run with patched loader; capture logs; confirm `READY_READONLY`; rollback if any indicator fails.
6. **Day 11** — Wave 1 (hindsight + graphiti) unsealed by F13.
7. **Day 12+** — Verify that with Wave 1 enabled, INIT logs `enabled=2, leases=0, mutations=0, verdict=READY_READONLY` and the two HTTP backends boot on first capability request only (per INV-12 stateless + per-task activation).

---

## 12. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Existing harness relies on direct MCP config (bypassing registry) | high (today) | high | Phase A canary first; rollback path preserves current behavior |
| Registry YAML schema drift across edits | medium | medium | Validator runs at every INIT; HOLD on schema drift |
| A-FORGE lease wiring introduces latency | medium | low | Lease check is local + O(1); no network round-trip |
| Backends booted before `enabled: true` flip | medium | high | Phase A canary verifies `ENABLED: 0` indicator; HOLD condition #7 catches it |
| Credentials leak via registry env fields | low | high | Validator scans for token-like strings (Phase A); credentials held by gateway, not registry |
| Phase D breaks Kimi startup | medium | medium | Snapshot before D; rollback script in §9 |
| Federation-wide rollout (Hermes, OpenClaw, OpenCode) introduces regressions | medium | high | Sequential harness rollout (one per week); each must pass canary before next |

---

## 13. Dependencies (between phases)

```
Phase A  ──▶ Phase B  ──▶ Phase C  ──▶ Phase D
   │            │            │            │
   ▼            ▼            ▼            ▼
loader       router      receipt    harness
+validator   +lease      +hold      integration
+init        bridge      gate       (Kimi first)

Phase A cannot begin before: registry ratified (status=RATIFIED) [pending]
Phase B cannot begin before: Phase A green for 7 days
Phase C cannot begin before: Phase B green for 3 days
Phase D cannot begin before: Phase C green for 3 days
```

This is conservative. F13 may compress any gap.

---

## 14. Out-of-Scope (explicitly NOT in this plan)

Per F13 directive, **not authorized in any phase of this plan**:

- ❌ Runtime code (Phase A/B/C scripts) — to be authorized in a separate F13 directive after plan ratification
- ❌ Harness/config modification
- ❌ MCP activation
- ❌ Service restart or deployment
- ❌ A-FORGE lease wiring
- ❌ Backend enablement

This file **is the only artifact** the current F13 directive authorizes.

---

## 15. Open Questions for F13 — RESOLVED 2026-08-11

Per F13 directive, the six questions are resolved using the documented conservative defaults:

| # | Question | Adopted default | Source |
|---|---|---|---|
| 1 | **Snapshot retention** | 30 days | plan §9 |
| 2 | **Registry versioning** | Dual-accept + deprecation warning | plan §15 |
| 3 | **Wave 1 unsealing criteria** | 3 consecutive `READY_READONLY` with `enabled=2` | plan §15, §11 |
| 4 | **Phase D harness priority order** | Kimi → Hermes → OpenClaw → OpenCode | plan §11 |
| 5 | **Credential rotation cadence** | No enforcement; F13 decides per-credential | plan §15 |
| 6 | **A-FORGE lease TTL** | 300 seconds, consistent with `forge_lease` defaults | plan §15 |

These defaults are now binding for Phase A code.

---

## 16. Ratification Gate

```
status:        RATIFIED
ratified_by:   ARIF (F13 SOVEREIGN)
ratified_at:   2026-08-11
phase_a:       AUTHORIZED (SEAL_PHASE_A_ONLY — code-only, no harness integration)
phase_b:       HOLD
phase_c:       HOLD
phase_d:       HOLD
wave_1:        HOLD
wave_2:        HOLD
wave_3:        HOLD
```

F13 directive (2026-08-11): "RATIFY PLAN + AUTHORIZE PHASE A. Stop after Phase A evidence.
Everything else remains HOLD."

When subsequent phases are authorized, the corresponding `phase_*` / `wave_*` line above flips to `AUTHORIZED` and the receiving phase may begin.

---

## DITEMPA BUKAN DIBERI

Forged 2026-08-11 · status: DRAFT · awaiting F13 ratification.
Architectural verdict: SEAL_ARCHITECTURE (sealed in registry, 2026-08-11).
Operational verdict: SEAL_EXPECTATION (anchors this plan; not yet achieved).

Ω₀ ≈ 0.04. INV-11..17 declared. Plan file is the only artifact under the current F13 directive.
