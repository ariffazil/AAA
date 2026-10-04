---
id: forge-federation-probe
name: forge-federation-probe
version: 1.0.0
description: 'Adversarial probe of arifOS federation organs — authority ceilings, deployment drift, vault integrity, circuit breakers, claim provenance. Replaces ad-hoc MCP probes with a single canonical entry point. Use this skill whenever the federation needs to be re-verified after deploys, before sealing, or as part of the constitutional benchmark.'
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F1, F2, F4, F11]
tags: [forge, mcp, probe, federation, authority, claim-provenance, audit]
host_compatibility:
- hermes
- openclaw
- opencode
- kimi
- kimi-code
- claude-code
- codex
dependencies:
  servers: []
  tools:
    - forge_filesystem_read
    - forge_shell_dryrun
examples:
- "Re-verify the federation after deploy: forge-federation-probe"
- "Pre-seal authority check: forge-federation-probe --phase=authority"
- "Audit circuit breaker after :5001 incidents: forge-federation-probe --phase=breakers"
tests:
- "forge-federation-probe --phase=health exits 0 when all organs return authority_ceiling"
- "forge-federation-probe --phase=authority surfaces C13 contradiction when ANY organ has authority_ceiling=ABSENT"
- "forge-federation-probe --phase=drift identifies source-vs-built-vs-deployed divergence with field paths"
---

# ⚒️ forge-federation-probe — Adversarial Federation Probe

> **Forged:** 2026-08-08 after MCP-PROBE found 13 field contradictions across the federation
> **Doctrine:** DITEMPA BUKAN DIBERI · Authority > Capability · Source ↔ Runtime ↔ Live must agree
> **Reference event:** `/root/forge_work/2026-08-08-mcp-probe/{R1..R4}-*.json` (the original receipts)

## USE WHEN

The task involves:
- Verifying the federation after a deploy (any organ)
- Checking that authority ceilings are declared on all organs (Phase 4 governance)
- Auditing vault integrity (VAULT999 hash chain, audit-receipt writer circuit breaker)
- Cross-checking source ↔ runtime ↔ live for drift
- Generating a federation probe receipt for VAULT999 sealing
- Pre-seal claim-provenance check on the federation itself

## DO NOT USE WHEN

- The task is to **build** MCP servers (use `forge_ephemeral`)
- The task is to **deploy** (use the per-organ `make deploy-local` contract)
- The probe is single-organ (use `mcpjam server doctor --url :PORT/health` instead)

## Iron Rule

> **A probe that finds nothing is a probe that was run badly.**
> A probe that finds contradictions and is **repeatable** becomes infrastructure.

This skill replaces the original MCP-PROBE workflow documented at `/root/forge_work/2026-08-08-mcp-probe/` with a single canonical script + reusable manifest. Reference files:
- `references/federation-deployment-model-2026-08-08.md` — per-organ source/runtime/deploy topology (edit this when systemd units change)

## The 8 Probes (Phase 4 Governance + Phase 5 Inference Brain)

The skill runs 8 probes in sequence. Each is independent and idempotent.

### Phase 1: Health Gate
- For each organ (arifOS:8088, A-FORGE:7071, A-FORGE-bridge:7072, GEOX:8081, WEALTH:18082, WELL:18083, AAA:3001):
  - GET `/health` → must return 200 with parseable JSON
  - **FAIL** if unreachable or empty

### Phase 2: Authority Ceiling (C13 mitigation)
- For each organ's `/health` response:
  - Field `authority_ceiling` must be present and non-null
  - Expected values: arifOS=`SOVEREIGN`, A-FORGE=`777_FORGE`, GEOX=`555_COMPUTE_ONLY`, WEALTH=`555_COMPUTE_ONLY`, WELL=`REFLECT_ONLY`, AAA=`DISPLAY_ONLY`
- **FAIL** if absent — that's the exact bug R2-CONTRADICTION-REGISTER C13
- **FAIL** if value doesn't match ORGAN.md

### Phase 3: Tool Count Semantics (C1-C4 mitigation)
- For arifOS `/health`:
  - Field `tool_count_semantics` must be present (the legend that explains 8 vs 48 vs 62)
- **FAIL** if absent — the legend was being stripped from default /health

### Phase 4: Apex Scalars Delegation (C11 mitigation)
- For A-FORGE `/health`:
  - Field `apex_scalars_policy` must be present
  - Each apex scalar must have `source_required` (why UNMEASURED is honest)
- **FAIL** if absent or scalars are decorative nulls

### Phase 5: Circuit Breaker State (M5 root cause)
- For arifOS `/health`:
  - Field `vault_sealer_breaker` must be present
  - If state=`open` → soft fail with retry_after_s
- **FAIL** if absent — means the :5001 cascade isn't observable

### Phase 6: Deployment Drift
- For each organ: compare source HEAD vs deployed_commit
  - Get source HEAD: `git -C /root/<organ> rev-parse HEAD`
  - Get deployed: from `/health.software_release.deployed_commit` (arifOS) or `/health.deployed_commit` (others)
- **FAIL** if diverge — source ≠ deployed means a bug in src/ isn't live

### Phase 7: Claim Provenance (Phase 4 governance)
- For each `/health` apex_scalars entry that has `value`:
  - The field MUST have a `source` or `g_canonical_source` field naming the kernel
- **FAIL** if a measured value lacks provenance

### Phase 8: Inference Brain + FI Coding Harnesses (Phase 5, added 2026-08-12)
- **The brain** (litellm-federation :4011):
  - GET `/v1/models` with `Authorization: Bearer $LITELLM_MASTER_KEY` → must return ≥1 model
  - **CRITICAL**: auth header is **required**. Unauthenticated probe returns `401 Unauthorized`, NOT "0 models". The previous probe script silently treated 401 as "no brain" — wrong.
  - Probe end-to-end: `POST /v1/chat/completions` on `hermes-asi` with `max_tokens=10`, expect HTTP 200 + non-null `choices[0].message`
  - **FAIL** if brain unreachable, auth fails, or model returns empty/error
- **The 8 FI CLI coding harnesses** (binary presence + reachability):
  - `opencode`, `claude-code`, `qwen-code`, `antigravity`, `codex`, `copilot`, `grok-build`, `kimi-code`
  - Each must have a binary in PATH that responds to `--version`
  - **FAIL** if any binary missing — that FI agent cannot dispatch

> **Why Phase 8 matters:** Phases 1-7 verify GOVERNANCE truth (authority ceilings, drift, breakers). Phase 8 verifies the inference path actually works. Federation probes can PASS Phases 1-7 while the brain is dead, leaving every coding agent unable to dispatch a single LLM call. The 2026-08-12 audit found exactly this: Phase 1-7 GREEN, end-to-end chat completion only verified by manually probing :4011 with auth header.

## CLI Surface

```bash
# Run all 8 probes — returns JSON + exit code
forge-federation-probe

# Run single phase
forge-federation-probe --phase=authority
forge-federation-probe --phase=health
forge-federation-probe --phase=drift
forge-federation-probe --phase=breakers
forge-federation-probe --phase=apex
forge-federation-probe --phase=tools
forge-federation-probe --phase=provenance
forge-federation-probe --phase=brain          # Phase 8: inference brain + FI harnesses

# Output as receipt (for VAULT999)
forge-federation-probe --format=receipt --receipt-id=R5-FEDERATION-VERIFY-2026-08-08

# Write to /root/forge_work/ for git_to_vault ingestion
forge-federation-probe --output=/root/forge_work/$(date +%F)-probe/federation.json
```

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | All probes PASS |
| 1 | Health gate fail (organ unreachable) |
| 2 | Authority ceiling missing/incorrect |
| 3 | Tool semantics legend missing |
| 4 | Apex scalars decorative |
| 5 | Circuit breaker not observable |
| 6 | Deployment drift detected |
| 7 | Provenance missing |
| 8 | Inference brain (litellm-federation :4011) unreachable / auth failed / end-to-end chat completion failed / FI binary missing |

## Output Format

Default JSON:
```json
{
  "probe_run": "forge-federation-probe-2026-08-08T08:30:00Z",
  "phases": {
    "health": {"arifOS": "PASS", "A-FORGE": "PASS", ...},
    "authority": {"arifOS": "PASS (SOVEREIGN)", "A-FORGE": "PASS (777_FORGE)", ...},
    ...
  },
  "failures": [],
  "warnings": [],
  "counts": {"PASS": 42, "FAIL": 0, "WARN": 1}
}
```

Receipt format (for VAULT999):
- Adds `payload_hash`, `run_id`, `probe_version` fields
- Adds `evidence_paths[]` naming every field_path checked

## The Deployment Contract (Phase 4 recommended)

Each organ MUST expose a `make deploy-local` target that:
1. Snapshots the current state (`git rev-parse HEAD > /tmp/deploy-prev-HEAD`)
2. Rsyncs source → runtime (if separate)
3. Clears `__pycache__/` for changed modules
4. Restarts the systemd unit
5. Probes `/health` and asserts `authority_ceiling` present

Status after the 2026-08-08 sweep:

| Organ | Has `make deploy-local`? | Has `make verify`? | Source dir | Runtime dir |
|---|---|---|---|---|
| arifOS | ✅ Yes | ❌ (use `make prove`) | `/root/arifOS/` | `/opt/arifos/app/` |
| A-FORGE | ✅ Yes (`e1eb1d4f`, 2026-08-08) | ✅ Yes | `/root/A-FORGE/src/` | `/root/A-FORGE/dist/src/` |
| GEOX | ❌ No | ❌ No | `/root/GEOX/` | `/root/GEOX/` (no separate runtime) |
| WEALTH | ✅ Yes (`33d8fa8`, 2026-08-08) | ✅ Yes | `/root/WEALTH/` | `/root/WEALTH/` (no separate runtime) |
| WELL | ✅ Yes (`16cf76c`, 2026-08-08) | ✅ Yes | `/root/WELL/` | `/root/WELL/` (no separate runtime) |
| AAA | ✅ Yes (`4e11d6b8`, 2026-08-08) | ✅ Yes | `/root/AAA/` | `/root/AAA/` (no separate runtime) |

**Recommendation:** every organ should have `make deploy-local` + `make verify` + `make prove`.
`verify` runs the `authority_ceiling` assert against `/health` (fast, ~50ms).
`prove` runs `forge-federation-probe` against the just-deployed state (full 7 phases, ~2s).

## Pitfalls

- **Probe is a probe, not a fix.** Don't use `forge-federation-probe --fix` — it doesn't exist. Fixes belong in the organ's own code.
- **Don't run probes against the federation during deploys.** Health endpoint may flap. Wait 5s after `systemctl restart`.
- **`forge-federation-probe` exit code 1 means organ is down.** Fix the organ, not the probe.
- **Phase 5 (circuit breaker) shows the *current* state.** A breaker that opened 30s ago will say `closed` now. For forensics, check `journalctl -u arifos.service | grep "circuit breaker OPEN"`.
- **Phase 6 (drift) compares source HEAD to deployed_commit.** A `--no-verify` git push will pass Phase 6 but fail Phase 1 next time the source is touched.
- **Deployed-commit field name varies per organ** (verified 2026-08-08, the probe checks all of these in order): arifOS uses `/health.software_release.deployed_commit`; most organs use `/health.deployed_commit`; WELL uses `/health.source_commit`; GEOX uses `/health.git_version` (prefixed `geox-`, which the probe strips). If you add a new organ, pick one naming convention and document it in ORGAN.md — Phase 6 will skip the organ otherwise.
- **WEALTH subprocess fails on `/dev/null`** (verified 2026-08-08). WEALTH runs as user `wealth`, which lacks `/dev/null` write permission in its sandbox. `subprocess.run(["git", ...])` returns empty stdout even though the command succeeds. Mitigation: write `/root/<organ>/.git_commit` (the fallback file WEALTH reads after git fails) from your deploy step. The probe will pick it up via `git_commit_fallback`.
- **`:7072` and `:7071` are two separate `/health` handlers in A-FORGE.** The canonical `apex_scalars_policy` lives on `:7071`; the bridge `:7072` only ships minimal `{ok, service, version, commit}`. The probe checks both ports. Adding a field to `:7071/health` does NOT propagate to `:7072/health` — patch `serve.ts` separately and rebuild.
- **A-FORGE `dist/build-commit.txt` is NOT touched by `npm run build`** (verified 2026-08-08). The bridge at `:7072` reads it for `BUILD_COMMIT`. Only `make deploy` writes it; `make deploy-local` (post-`e1eb1d4f`) also writes it. After any manual `npm run build`, run `git rev-parse --short HEAD > dist/build-commit.txt` before restart, otherwise Phase 6 will flag drift.
- **Don't include `federation_geometry` claims from organs that own zero federation subjects** (A-FORGE, GEOX, WEALTH, WELL all report `subjects: 0`). The field exists for federation conformance but the values are honest-zero, not measurement. Treat `subjects: 0` as "this organ doesn't track subjects" not "federation is broken". For real subject counts, query AAA `/health.chain` or arifOS `/health.seal_readiness`.
- **Phase 8 brain probe REQUIRES auth header.** `GET http://127.0.0.1:4011/v1/models` without `Authorization: Bearer $LITELLM_MASTER_KEY` returns HTTP 401 — NOT "0 models exposed". The previous probe-script silently parsed the 401 response as `{data: []}` and reported "brain down". Always source the master key from env (`os.environ["LITELLM_MASTER_KEY"]`) and add the header. Source env from `/root/.secrets/kunci-mas.env` first.
- **Phase 8 end-to-end chat probe: pick the cheapest model, not the strongest.** Use `hermes-asi` with `max_tokens=10`. Other lanes (apex-888, agi-333, asi-555, i-arif) route to deeper reasoning models and cost 10-100× more tokens per probe. `hermes-asi` defaults to `MiniMax-M3` (cheap). Aim for ~150-200 total tokens per probe run; never spend budget on probe traffic.
- **MCP `tools/list` requires `Mcp-Session-Id` header** on A-FORGE (:7071), GEOX, WEALTH, WELL (verified 2026-08-12). The session id is returned in the response header of the `initialize` request. arifOS :8088 does NOT require this — its `initialize` is stateless. The hand-shake is: POST `initialize` → capture `Mcp-Session-Id` from response headers → POST `tools/list` with that header. Without it, every non-arifOS organ returns `400 Bad Request: Mcp-Session-Id header is required` and the probe silently reports "0 tools exposed". The brain-probe (`tools_exposed_via_mcp`) and organ tool counts diverge if you skip this step.
- **A-FORGE drift is governance drift, not functional drift.** When `deployed_commit: ""` (empty marker file) but `tools_loaded == tools_loaded == tool_count`, the runtime is FUNCTIONAL — the drift is only in the truth ledger. Don't try to redeploy A-FORGE just because Phase 6 fails; first verify `forge_health_check`, `forge_status`, `forge_registry_status` all return `err=False` + `status=SEAL`. If yes, drift is informational, not actionable.
- **litellm-federation `:4011` is on systemd, not the escape `:4012`.** `/etc/systemd/system/litellm-federation.service` ExecStart is `--config /root/A-FORGE/litellm-config.yaml --port 4011`. The escape config `:4012` (`/root/A-FORGE/escape-config.yaml`) is a manually-run backup that only exposes 3 models (escape-gemini, glm-5.2, zai-pro). Phase 8 probes `:4011`. If you see only 3 models exposed, you're hitting the escape config — fix the systemd unit, not the probe.

## Deep Audit Variant (source-level, delegated)

The 7 probes above are a **quick health check** (~2s, no code reading). For deep source-level auditing of a specific organ — tracing execution paths through actual Rust/Python/TypeScript code, testing constitutional claims against live evidence, identifying bridge nodes and strawberry components — use the **6-phase deep audit delegation pattern**.

→ `references/deep-audit-delegation-pattern.md`

This spawns an independent auditor via `delegate_task` with 6 sequential phases (Reality Inventory → Flow Trace → Constitutional Test → Bridge Node Analysis → Strawberry Principle → Adversarial Review) producing 7 deliverables. Takes minutes, not seconds. Results route through `arif_judge` before integration.

Use the quick probe for: post-deploy checks, health sweeps, drift detection.
Use the deep audit for: governance verification, pre-seal organ audits, architecture-vs-reality validation.

**Worked example:** arifFLOW audit 2026-08-10 — 6-phase deep audit of the Rust metabolism daemon (:7073). Read 17 source modules (~6,200 lines Rust), 2 Python clients, 1 Shell script. Probed 5 live HTTP endpoints, ran 96 unit tests (all passing). Key findings: (1) 5/7 F0-F6 invariants tautological, (2) dual FQ formulas (legacy vs v2.1) measure inverse properties creating operator confusion, (3) system fails OPEN contradicting stated Fail-Closed constraint, (4) receipt chain validation bypassed via push_force, (5) no persistence (all state in RAM), (6) no automatic enforcement timer. Verdict: HOLD. Full deliverables at `/root/forge_work/arifflow-audit/` (7 files). 11 verified pitfalls captured in `references/deep-audit-delegation-pattern.md`.

## Related Skills

- `federation-constitutional-audit` — **deep 6-phase adversarial audit** (the canonical methodology for the "Deep Audit Variant" described above). Use when the probe finds contradictions that need root-cause investigation, or when F13 demands comprehensive organ verification.
- `forge-mcp-probe` — single-organ MCP conformance testing (P0–P16 adversarial harness)
- `forge-mcp-testing` — MCPJam Inspector harness for one organ at a time
- `audit-and-validate-deliverables` — generic artifact audit pattern
- `frontier-model-audit-verification` — Rule #7 probe-to-witness applies here
- `a-forge-ops` — A-FORGE specific (TS build, dist/, deploy-local, forge_vault, egress)
- `arifos-federation-ops` — kernel/seal/topology/VAULT999 operations on arifOS specifically
- `federation-infra-verification` — broader infra probe for declared-vs-live state, with extractive-map output shape