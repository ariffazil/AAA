# Runtime Truth Reconciler Contract v1 (P0 — Stage 2 spec)

> **Status:** STAGED-ARTIFACT, FOR STAGE 2 arifOS-L13 BUILD. F13 directive "ok i approve, sah, jalan and go" received 2026-10-01.
> **Lineage:** Trilogy Gap §3.1 (aforge runtime_identity_minimal; arifos runtime_vs_repo drift); `forge_runtime_verify` (live); Constitutional Architecture Canon HALAL-positive predicate; HUMA bridge Law 6 (word-presence ≠ implementation); scar sealed 2026-09-27 (sensor-tampering).
> **Purpose:** Contract for the SourceHash = BuildHash = DeployHash = ImportHash = RuntimeHash identity predicate across the 5 organs with `runtime_identity_minimal`.
> **Why this matters:** Without the identity chain, every other gate cannot be trusted. The 2026-09-27 scar proves the failure class is real (markers were self-rewritten).

---

## The 5-identity chain (per organ)

```
SourceHash
   ↓ (git log)
BuildHash
   ↓ (CI artifact)
DeployHash
   ↓ (live binary on host)
ImportHash
   ↓ (process loaded module)
RuntimeHash
   ↓ (currently executing instruction hash)
```

Each MUST be identified from a source **that agent cannot write**. Per scar 2026-09-27 §1: "Any attestation consumed by a governed actor MUST include at least one input that actor cannot write (kernel process start time / MainPID / binary digest read from outside the service uid)".

---

## Per-organ identity surface (canonical)

#### arifOS
- `SourceHash`: `git log -1 --format=%H` from `/root/arifOS/.git`
- `BuildHash`: SHA256 of `/opt/arifOS/dist/build.lock` (binary build lock, NOT writable by service uid)
- `DeployHash`: `stat -c '%s' /usr/bin/arifOS + sha256(binary)` read from outside service uid
- `ImportHash`: `sha256(proc/<pid>/maps)` from outside service uid
- `RuntimeHash`: `sha256(/proc/<pid>/exe)` from outside service uid

#### A-FORGE
- `SourceHash`: `git log -1 --format=%H` from `/root/A-FORGE/.git`
- `BuildHash`: `/opt/a-forge/app/build.lock`
- `DeployHash`: `stat -c '%s' /opt/a-forge/app + sha256`
- `ImportHash`: `sha256(proc/<pid>/maps)`
- `RuntimeHash`: `sha256(/proc/<pid>/exe)`

(Plus `started_at`, `policy_version`, `schema_version` — all currently MISSING per scar 2026-09-27.)

#### GEOX, WEALTH, WELL, arifFlow, FRAME, HERMES, AAA
Same 5-identity surface, with `/opt/<organ>/<service>.lock` as BuildHash source.

---

## The Runtime Truth Reconciler

```yaml
reconciler_state:
  organ: <organ_id>
  reconciles:
    - reconcile_id: rec-<cycle_id>
      reconcile_at: <iso8601>
      source_hash: <sha256>
      build_hash: <sha256>
      deploy_hash: <sha256>
      import_hash: <sha256>
      runtime_hash: <sha256>
      parity: PARITY | DRIFT | UNKNOWN
      claimed_drift: <bool>  # from existing /health drift_detected field
      measured_drift: <bool>  # from the 5-hash chain comparison
      drift_consistent: <bool>  # claimed vs measured
      verifier_actor_id: <actor_id>
      witness_chain: <sha256[]>
```

**Rule:** `parity = PARITY` requires `drift_consistent = true` AND all 5 hashes come from sources the service uid cannot write. Otherwise `parity = DRIFT` or `UNKNOWN`. `UNKNOWN` MUST NOT be reported as `PARITY` (no-data-is-not-all-clear).

---

## Output to arifOS kernel

Per scar 2026-09-27 negative-constraint: `reconciler_state.parity ∈ {PARITY, DRIFT, UNKNOWN}` is the only allowed output. No silent fallthrough. No rounding to `true` when any hash is missing.

The reconciler output replaces `status=healthy` claim in `/health` for the 5 organs.

---

## Stage 0 dependency: drift-reconcile-unblock-test-2026-10-02

CHRON event `drift-reconcile-unblock-test-2026-10-02` is the test event: *"after ONE kernel reconcile redeploy, (1) /health drift_detected clears AND (2) replay of FI-008 judge case (session SEAL-f70bf5356a444cb5, trace trc-5dcea65d1a08) no longer fails-closed on drift. If REJECTED, single-reconcile is REFUTED and the batch must be split."*

This is the falsification test for the single-reconcile hypothesis. Run before any further Runtime Truth Reconciler work.

---

## What this artifact is NOT

- Not a kernel implementation. The contract above is the interface that the arifOS-L13 reconciler should expose.
- Not an authority grant.
- Not a single-step fix; it depends on the Stage 0 falsification test clearing.

---

## Receipt chain

- `forge_experience_trace trace_id=exp-1790838115433-1790836981647` (audit trace)
- This contract artifact: `/root/AAA/.forge_outbox/runtime_truth_reconciler_contract_v1.md`
- Drift-reconcile-unblock-test CHRON event: 2026-10-02 (Stage 0 falsification gate)

DITEMPA BUKAN DIBERI ⚒️