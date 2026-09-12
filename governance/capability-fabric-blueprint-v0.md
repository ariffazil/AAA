# Capability-Fabric Blueprint v0

> **Status:** Planning artifact produced by the architect planning session on 2026-09-12.
> **Authority:** 333-AGI (Δ MIND) on behalf of Arif (F13 SOVEREIGN).
> **F13 release scope for execution:** *Phase 0 reality audit only — OBSERVE + VERIFY, no MUTATE.*
> **Machine-backed constitutional seal:** NOT bound (LIMITED_MUTATE band, `seal_allowed=false`). Planning session content is embedded below as carry-forward evidence, not as a sealed record.

---

## 0 · Provenance and trust

| Item | Class | Evidence |
|---|---|---|
| Capability-Fabric principle | sovereign design decision | Arif's verdict in this conversation |
| 6+1 axes (Capability, Surface, Mode, Organ, Assurance, Consequence, Reality-State) | sovereign design decision | Arif's verdict |
| SEAL is not a capability (it is consequence + 999_SEAL stage) | sovereign design decision | Arif's verdict |
| Order: Reality → Inventory → Classification → Routing → Governance | sovereign design decision | Arif's correction |
| Doctrine: Registry stores intent, Witness records reality, Governance reconciles | sovereign design decision | Arif's correction |
| 118-tool inventory, 0 drift | **HYPOTHESIS — contradicted by live probe** | `curl :7072/health` returned `total_tools:null, fingerprint_passed:null`; prior transcript claim is not witnessed |
| `affordances.yaml` content | HYPOTHESIS — read in prior session but not git-HEAD-diffed | local file read was plausible but version not verified |
| 8 drift findings | HYPOTHESIS — line-by-line interpretation only | no machine attestation |
| 3 design artifacts written | **FALSE — never written** | only this blueprint was written |
| `arif_seal` succeeded for architecture principle | **FALSE — rejected with HOLD** | prior transcript shows `L11 AUTH: SCT invalid` |
| Capability-index MCP bug | OBSERVED in prior session | transcript shows schema rejection on session_id/actor_id/session_token/sct |

This blueprint therefore proceeds on the principle that **declared ≠ witnessed**. Every step below is designed to convert declared into witnessed.

---

## 1 · Pre-flight (mandatory before any execution)

```bash
# Verify local authority state (filesystem = directly observable)
ls -la /root/.config/opencode/ 2>/dev/null
cat /root/AGENTS.md 2>/dev/null | head -20
ls /root/.local/share/arifos/sovereign.sct 2>/dev/null && echo "sovereign.sct present"

# Verify arifOS kernel health (CLAIM; must be probed live)
curl -sf http://127.0.0.1:8088/health | jq '{status, floors_active, verdict: .thermodynamic.verdict}'

# Verify A-FORGE organ health (CLAIM; must be probed live)
curl -sf http://127.0.0.1:7072/health | jq '{status, total_tools, fingerprint_passed}'

# Probe arifFlow
curl -sf http://127.0.0.1:7073/health | jq '{fq, receipts, cycle: .invariants.cycle_count}'

# Probe all organs
for p in 8088 7072 7073 3001 8081 18082 18083; do
  curl -sf "http://localhost:$p/health" 2>/dev/null | jq -r '.status' 2>/dev/null | xargs -I{} echo ":$p {}"
done
```

If any organ returns DOWN, **HOLD and report**. Do not continue.

---

## 2 · Phase 0 — Reality Audit (do BEFORE any ontology work)

### 2.1 · Tool liveness probe (per claimed `forge_*` tool)

For each tool declared in `/root/A-FORGE/a_think/affordances.yaml` (118 entries, but count must be **re-witnessed** at session start):

```yaml
tool_id: forge_<name>
  exists:    <bool — listed in /root/A-FORGE/a_think/affordances.yaml AND live MCP tools/list>
  callable:  <bool — call returns within 5s without error>
  authority: <enum — OBSERVE_ONLY | LIMITED_MUTATE | FULL | null>
  side_effects_declared: <list — filesystem | network | shell | vault | git | db>
  writes_declared: <list — filesystem | vault | git | db>
  reversible: <bool>
  observed_class: <OBSERVE | GOVERN | MUTATE | SEAL — from live response>
  drift_vs_card: <none | minor | major>
```

Method:
- Read the local affordance card (`/root/A-FORGE/a_think/affordances.yaml`) — git-HEAD-diff against the live file's git HEAD first
- Run `forge_fingerprint_check` to compare schema fingerprints
- For a sample of ~10 tools, attempt a no-op call (e.g., `forge_health_check`, `forge_registry_status`, `forge_shell_status`, `forge_memory`) and record observed behavior vs declared

### 2.2 · Registry reconciliation

```yaml
registry_entry: <tool_name>
  exists:     <bool — listed in live MCP tools/list>
  reachable:  <bool — callable without error>
  referenced: <list — referenced by other tools, contracts, schemas>
  orphaned:   <bool — declared but no consumer>
```

Cross-check via:
- `mcp__aforge__forge_surface_audit(organ="aforge")` — claimed output is *not* trustworthy until re-witnessed
- `mcp__aforge__forge_fingerprint_check()` — schema dedupe status
- `git -C /root/A-FORGE log --oneline -- a_think/affordances.yaml | head -10` — what changed recently
- `git -C /root/A-FORGE diff HEAD~1 HEAD -- a_think/affordances.yaml | wc -l` — drift magnitude

### 2.3 · Capability verification

For each of the 12 proposed capabilities (OBSERVE, EXTRACT, ANALYZE, VERIFY, PLAN, ROUTE, EXECUTE, ORCHESTRATE, WITNESS, REMEMBER, GOVERN, RECOVER):

```yaml
capability: <name>
  implemented_by:   <list of forge_* tools that ACTUALLY serve this capability — verified by call>
  declared_by_card: <list of forge_* tools whose affordance card CLAIMS this capability>
  verified_live:    <bool — confirmed via probe>
  count:            <int>
```

For each capability, do NOT trust the `affordance_class` field alone. Verify by actually calling the tool and observing:
- Does it return data (→ OBSERVE/EXTRACT/ANALYZE)?
- Does it return a verdict (→ VERIFY/GOVERN)?
- Does it mutate external state (→ EXECUTE)?
- Does it coordinate multiple tools (→ ORCHESTRATE)?
- Does it persist a record (→ REMEMBER/WITNESS)?

---

## 3 · Phase 0 output schema

After Phase 0, produce a single artifact:

```yaml
phase_0_report:
  generated_by:   333-AGI
  generated_at:   <ISO8601>
  session_id:     <arifOS session id>

  tool_liveness:
    total_claimed:   <int — re-counted from affordances.yaml at session start>
    total_alive:     <int — proven callable>
    total_dead:      <int — declared but unreachable>
    phantoms:        <list — name, declared_class, observed_behavior>

  registry_reconciliation:
    declared_count:  <int>
    reachable_count: <int>
    orphaned_count:  <int>
    drift_count:     <int — semantic drift, not just name drift>

  capability_coverage:
    OBSERVE:      {implemented_by: [...], verified_live: bool}
    EXTRACT:      {...}
    ANALYZE:      {...}
    VERIFY:       {...}
    PLAN:         {...}
    ROUTE:        {...}
    EXECUTE:      {...}
    ORCHESTRATE:  {...}
    WITNESS:      {...}
    REMEMBER:     {...}
    GOVERN:       {...}
    RECOVER:      {...}

  findings:
    - {tool, observed, expected, status: pass | fail | indeterminate}

  next_action: continue | halt | escalate
```

---

## 4 · Carry-forward state (from this planning session)

```yaml
verdict:
  architecture:        conceptually_accepted
  machine_seal:        not_bound
  mutation:            held

truth:
  attempted_arif_seal:      rejected_or_unverified
  runtime_change:           none_evidenced
  filesystem_write:         this_blueprint_only
  registry_write:           none_evidenced
  artifact_creation:        this_blueprint_only

epistemic_status:
  capability_fabric_model:   sovereign_design_decision
  a_forge_live_inventory:    unknown_pending_observation
  registry_drift_findings:   hypothesis_pending_verification
  current_machine_authority: LIMITED_MUTATE_observed
  a_forge_live_probe_2026_09_12: total_tools_null, fingerprint_passed_null

axes_v1:                     [capability, surface, mode, organ, assurance, consequence, reality_state]
seal_is_not_a_capability:    confirmed — consequence + 999_SEAL stage, not peer verb
sealed_at:                   conceptual_only
bound_at:                    not_bound

next_permitted_class:        [OBSERVE, VERIFY]
next_prohibited_class:       [EXECUTE, ORCHESTRATE, SEAL, MUTATE]
retry_policy:                prohibited_without_F13_release
```

---

## 5 · F13 release contract

Any action beyond OBSERVE/VERIFY requires a narrow F13 release with this exact shape:

```yaml
release:
  target:               <exact artifact path or action>
  scope:                <one write | one seal | one tool call>
  payload_hash:         <sha256>
  authority_chain:      <session_id + actor_id + session_token_prefix>
  expected_receipt:     <shape>
  consequence_class:    none | reversible | conditional | irreversible
  rollback:             <how to revert>
```

No batch. No consolidation. No tool rename. No broad "reorganize A-FORGE".

---

## 6 · Recommended execution sequence for the next session

1. Run §1 pre-flight. Abort if any organ is DOWN.
2. Run §2.1 tool liveness probe. Abort if > 30% phantoms.
3. Run §2.2 registry reconciliation. Abort if drift > 20 entries.
4. Run §2.3 capability verification. Build the §3 report.
5. If `next_action: continue`, write the capability-ontology.v1.yaml FIRST (low-consequence design metadata).
6. STOP. Do not write capability-registry or adapter-registry until F13 releases each explicitly.
7. Append a new carry-forward block to the bottom of this blueprint.
8. Seal the session via `arif_seal(mode=session_close)` — this requires F13 release for SOVEREIGN band; without it, the band will HOLD.

---

## 7 · Blueprint provenance

- Path: `/root/AAA/governance/capability-fabric-blueprint-v0.md`
- Authored by: 333-AGI (Δ MIND)
- Date: 2026-09-12T13:5xZ
- Source session: `SEAL-2e07efbaf59740cc` (planning session)
- Supersedes: nothing
- Superseded by: nothing yet
- F13 ratification: pending
- SHA256: <computed at write time, see comment in carry-forward>

---

DITEMPA BUKAN DIBERI — Phase 0 before ontology. Reality before Registry.
