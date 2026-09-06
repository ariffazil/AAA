# SPEC — Boot-Parity Verifier v0

> **CLASS:** OBSERVE-class gate · SPEC ONLY (no implementation yet)
> **FORGED:** 2026-09-06 · musyawarah 2026-09-06-federation-invariants
> **MODEL:** `forge_runtime_verify` (git source vs installed wheel vs import path → MATCH|DRIFT, fail-closed)
> **STATUS:** DRAFT — ratify via musyawarah convergence + F13 before implementation

## Problem

Three nodes (KVM8 seat/court, KVM4 workshop, KVM2 witness) can silently disagree on constitutional state. Today they do: constitution presence differs, SOT copies are partial and non-overlapping (OBS 2026-09-06). Routing and governance decisions are made from divergent truth.

## Mechanism

A **parity manifest** — a signed list of `{artifact, sha256, authority}` tuples covering:

| Artifact | Authority (one writer) |
|----------|----------------------|
| Constitution canon (`/root/arifOS/GENESIS/`) | KVM8 arifOS |
| `federation-models.json` | KVM8 AAA |
| `MACHINE_MAP.md` | KVM8 Hermes |
| Triadic snapshot (writer key id) | KVM8 WELL snapshotter |
| Naming canon (CANONICAL_GLOSSARY hash) | KVM8 AAA |

**Fire points:**
1. Node boot (systemd unit `fed-parity-verify.service`, oneshot, Before=network-online)
2. Cross-node handshake (A2A agent hello carries manifest head hash)
3. Optional cron: hourly re-verify (cheap — 5 hashes)

**Verdict semantics (fail-closed):**
- `MATCH` — all hashes equal → proceed
- `DRIFT` — any hash differs → node enters OBSERVE_ONLY (never blocks observation; blocks mutation — K-2 degradation asymmetry)
- `UNKNOWN` (manifest unreachable/unverifiable signature) → treat as DRIFT for mutation purposes. Void Guard: no-data ≠ all-clear.

**Explicitly NOT:**
- Not a judge — parity only, never content adjudication (888-APEX unaffected)
- Not forced tool parity — role-specific organs stay role-specific (specialization ≠ drift)
- Not a new organ — a mode on existing `forge_runtime_verify`, per "no new tools, harden existing ones"

## Rollout (staged, reversible)

1. **Phase 0 (warn-only):** deploy on KVM4 + KVM2, log DRIFT, block nothing. 48h.
2. **Phase 1 (gate mutation):** DRIFT → OBSERVE_ONLY on the divergent node.
3. **Phase 2 (attestation):** manifest signature fan-out (requires key distribution decision — F13).

## Open questions for musyawarah / F13

- KVM2 fork disposition: re-sync to canon vs ratify intentional divergence (MACHINE_MAP ruling needed)
- Signing key custody for manifest (KVM8 kernel vs sovereign-held)
- Whether A2A hello payload grows a manifest field (wire-format change, AAA gateway)
