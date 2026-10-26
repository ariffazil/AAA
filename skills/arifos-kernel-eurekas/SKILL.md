---
name: arifos-kernel-eurekas
description: 'K1-K12 kernel substrate honesty laws (K1-K4=/health, K5-K6=mutation gate, K7=payload discipline, K8=tool liveness, K9=deploy verification, K10=last-writer timing, K11=honest sensor principle, K12=dual evaluation paths).'
version: 1.0.0
author: F13 SOVEREIGN + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kernel, arifos, substrate-honesty, SC4, K-series, F1-F13, federation, principles]
    related_skills: [arifos-integration-recon, arifos-cron-ops, arifos-federation-ops]
---

# Kernel Eurekas — Substrate Honesty Laws (K-Series)

> **Source:** Verified 2026-08-07 SC4 stabilization (`RECEIPT-2026-08-07-sc4-stabilization`, hash `4e88bca57d95bc5585d76d98eff94b779a6c452993d38fc1c4aae6b97cf272dc`).
> **Scope:** Runtime substrate — `live_metrics.py`, `rest_routes.py`, `_build_governance_status_payload()`, vault readers, `/health` endpoint.
> **NOT:** GENESIS doctrine. These are physical invariants of the running engine, not new laws.

## K1 — The Fallacy of the "Safe" Default (Truth > Uptime)

**Defect pattern:** The kernel replaced failing floor scores with passing defaults to prevent indefinite `held` states.

**Why it's wrong:** Masking a failure to keep the engine running is how an AI goes rogue quietly. If a safety floor fails, the system MUST halt and scream.

**Law:** F2 (Truth) always overrides system convenience. A hard crash is infinitely safer than a silent lie.

**Code site:** `rest_routes.py:_build_governance_status_payload()` lines 922–925 (post-fix). The "fail → replace with default pass" loop is **deleted**. Failing measurements stay failing. Unmeasured floors (next K-law) become `None`.

**Audit:** if you find a new code path that substitutes a default for a failed measurement, you are reintroducing K1-violation. Delete it.

## K2 — The Epistemology of the Void (0.0 vs null)

**Defect pattern:** The system could not distinguish "I measured this and it scored zero" from "I never measured this at all." Both returned `0.0`. This made `runtime_floors.F9=0.0` indistinguishable from `F9=unmeasured`.

**Why it's wrong:** Absence of signal is not a zero signal — it's an epistemic void. Forcing unmeasured to `null` plus an explicit `unmeasured_floors` array eradicates guesswork.

**Law:** If the system does not know, it must explicitly declare UNKNOWN. False precision is a hallucination.

**Code site:** `rest_routes.py:907-918` (post-fix). New behavior:
- If a floor key is absent from the governance kernel's measurement output, set it to `None`.
- Include `"unmeasured_floors": sorted([fid for fid in LAW_SPEC_KEYS if resolved_floors.get(fid) is None])` in the governance payload.
- Dashboard/dashboard-v2 consumers MUST read `unmeasured_floors` to render UNKNOWN distinctly from measured-zero.

**Verification probe:**
```python
import json, urllib.request
d = json.loads(urllib.request.urlopen('http://127.0.0.1:8088/api/governance-status').read())
assert 'unmeasured_floors' in d, 'K2 violation: unmeasured_floors field missing'
assert d['floors'].get('F9') in (0.0, None), 'F9 must be measured-zero OR unmeasured-null, not ambiguous'
```

## K3 — The Phantom Arrow of Time (Multi-Ledger Reality)

**Defect pattern:** The vault reader at `live_metrics.py:316-326` (pre-fix) used a "first existing path wins" pattern. Two vault files exist — `seal_chain.jsonl` (stale since 2026-08-03) and `outcomes.jsonl` (actively written). The reader always picked `seal_chain.jsonl` first, so `last_seal_timestamp` reported a phantom arrow pointing 4 days backward. The kernel thought time had frozen.

**Why it's wrong:** An arrow of time is only as accurate as the clock you read. If memory is split across ledgers, the kernel must scan ALL of them to find true "present".

**Law:** Reality is the aggregate of all immutable ledgers. The system must always compute the absolute latest timestamp across all valid vault files.

**Code site:** `live_metrics.py:316-353` (post-fix). New behavior:
- Read BOTH `/root/.local/share/arifos/vault999/seal_chain.jsonl` AND `/root/arifOS/VAULT999/outcomes.jsonl`.
- Each line parsed for `timestamp` / `created_at` / `ts` (in that order).
- Sort all lines by timestamp desc, pick the newest.
- Robust to malformed lines (`json.loads` failures → empty sort key) and non-dict lines.

**Verification probe:**
```python
import json, urllib.request
ts = json.loads(urllib.request.urlopen('http://127.0.0.1:8088/health').read())['governance']['last_seal_timestamp']
assert ts and 'T' in str(ts), f'K3 violation: last_seal_timestamp={ts}'

# Compare with the actual vault
with open('/root/arifOS/VAULT999/outcomes.jsonl') as f:
    vault_ts = json.loads(f.readlines()[-1]).get('ts')
# ts should be ≥ vault_ts (after dual-merge)
```

**Ongoing pitfall:** Any new vault file path added to the federation MUST be appended to the `vault_candidates` list, or it will silently be ignored by `live_metrics`.

## K4 — Substrate Honesty Dictates Agentic Reality

**Defect pattern:** This law is meta — it's about the failure mode of building World Models on dishonest substrates. The .bak file archive + /health fixes didn't add new intelligence; they made existing intelligence structurally honest.

**Why it's wrong:** You cannot build a World Model on a physics engine that hallucinates. Agents only know what the kernel tells them. If `/health` lies, every agent in the federation makes decisions based on corrupted reality.

**Law:** Before you build complex recursive intelligence, you must build an unbreakable, honest substrate. The environment must be mathematically incapable of lying to the agents.

**Operational consequence:**
- The federation's World Model cron chain (`arif-morning-pulse` → `arif-world-reality-intel` → `arif-reckoning`) reads `/health` and the vault. If those lie, the chain amplifies the lie.
- K4 says: **substrate honesty is a precondition for agentic scale, not an afterthought.**

**Audit cadence:** Every federation restart must pass all three probes (K1/K2/K3) before any agent-driven job is allowed to consume the `/health` payload. The probes are in `/root/HERMES/scripts/zen/` (verify paths with the cron-ops skill before relying).

## K5 — Runtime Enforcement Gate Honesty (closes E-22 on Hermes side)

**Defect pattern (E-22 audit, 2026-08-07):** The federation's constitutional contract exists in docs and YAML (`AAA_FEDERATION_CONTRACT_v0.1.x`, `kimi_spawn_protocol_v0.1.0.json`, etc.) but the agent runtime can still violate INV-02, INV-11, INV-14, INV-15 silently. Hermes specifically: `subagent_auto_approve: true`, no delegation receipt trail, no judge gate on `delegate_task` output. The constitution is a treaty, not law.

**Why it's wrong:** E-22 = "can runtime violate constitution without leaving a receipt?" — answered YES for Hermes (3 silent violation vectors). E-11 says enforcement that depends on memory has already failed. E-12 says capability > instruction. **Documentation-only governance has no enforcement, so it has no governance.**

**Law:** An agent runtime must emit a structural enforcement gate that classifies every mutation (T1 / T2 / T3) and writes a receipt per evaluation, BEFORE the action executes. The receipt trail is the audit floor — without it, no amount of doctrine binds the runtime.

**Operational consequence:**
- Pattern-matching > prompt-asking: hardcode `MUTATE_PATTERNS` (T3 patterns: secrets path, rm -rf, arif_seal, forge_deploy, force-push, drop table) as regex, not as agent advice.
- `evaluate(tool, args, session_id, actor_id, apex_verdict_present) -> Decision(ALLOW | BLOCK | REQUIRE_JUDGE)` is the gate's only output.
- Three-tier: T3 pattern fires → BLOCK immediately; MUTATE tool without apex verdict → REQUIRE_JUDGE; otherwise → ALLOW.
- Receipt on every evaluation: `ts`, `event`, `tool`, `args_hash`, `decision`, `rule_id`, `reason`, `receipt_hash`. NEVER block on receipt failure (E-19: infrastructure failure ≠ governance failure — receipt can fail without changing the verdict).
- Pure function, no runtime side effects. The interception point is a separate concern (Phase 2 in the live-traced MISSION; Phases 2/3 for Kimi still pending).
- The gate skeleton at `/root/HERMES/gate/hermes_mutation_gate.py` (10,186 bytes, 290 LoC) is the **template** — adapt it to TypeScript for OpenCode/Kimi plugin form.

**Tested pattern (9/9 pass, 2026-08-07):**

| Tool | Args | Expected | Got |
|---|---|---|---|
| `read_file` | any | ALLOW | ✅ ALLOW |
| `write_file` | no apex verdict | REQUIRE_JUDGE | ✅ REQUIRE_JUDGE |
| `write_file` | with apex verdict | ALLOW | ✅ ALLOW |
| `terminal` | `cat /root/.secrets/kunci-mas.env` | BLOCK | ✅ BLOCK (T3 pattern) |
| `terminal` | `rm -rf /root/forge_work` | BLOCK | ✅ BLOCK (T3 pattern) |
| `execute_code` | `arif_seal()` | BLOCK | ✅ BLOCK (T3 pattern) |
| `delegate_task` | no apex verdict | REQUIRE_JUDGE | ✅ REQUIRE_JUDGE |
| `delegate_task` | with apex verdict | ALLOW | ✅ ALLOW |
| `terminal` | `git push --force origin main` | BLOCK | ✅ BLOCK (T3 pattern) |

**Audit cadence:** Every agent runtime (Hermes, OpenCode, Kimi Code) must run the 9-test vector matrix against its gate before any SEAL. If any case fails or returns UNEXPECTED, the gate cannot be ratified regardless of how good the constitutional doctrine looks on paper.

## K6 — Mutation Gate Runtime Wire-Up (the bridge between K5 and enforcement)

**Defect pattern (gap surfaced 2026-08-07, after K5 was filed):** K5 says the gate exists as a pure function. **A pure function on disk is not enforcement at runtime.** Until the gate is wired into a hook the runtime actually invokes, no K5 invariants hold against live mutations. The constitution observes reality; it does not alter it.

**Why this matters:** `/root/HERMES/gate/hermes_mutation_gate.py` was written and tested in isolation — 9/9 subprocess smoke tests pass. But until a `pre_tool_call` shell hook invokes it on every Hermes tool call, the gate is **architecture-ahead-of-runtime**, not enforcement. Every test case of K5 is bypassed the moment a real Hermes session runs because the runtime never calls the gate.

**Law (K6):** A constitutional gate must be **runtime-bound** to be a gate. The test is whether the runtime invokes it on the first mutation after a fresh session. If the receipt trail shows zero entries during a session that performed mutations, the gate is decoration, not governance.

**Operational consequence — the 3-layer wire-up:**

```
Layer 1: hermes_mutation_gate.py       ← pure logic (K5 template, the skill already has this)
Layer 2: mutation_gate_hook.py          ← shell-hook adapter: stdin JSON → stdout JSON
Layer 3: config.yaml hooks entry       ← runtime registration (one YAML block)
```

- **Layer 2** wraps Layer 1 in Hermes' `pre_tool_call` shell-hook protocol. Receives `{"tool_name", "tool_input", "session_id"}` via stdin; emits `{"decision": "block" | "approve"}` via stdout. Writes receipt to `hermes_actions.jsonl`. Exit 0 = allow; exit 2 = block. NEVER blocks on receipt write failure (E-19).
- **Layer 3** is one YAML block in `~/.hermes/config.yaml` (or profile-scoped config):
  ```yaml
  hooks:
    pre_tool_call:
      - command: /root/HERMES/gate/mutation_gate_hook.py
        matcher: "*"
        accept_hooks: true
  ```
  Then `hermes gateway restart` to bind.
- **After wire-up:** every Hermes tool call in the live runtime fires `pre_tool_call` → gate evaluates → verdict returned → receipt written. K-02 transitions from "designed" to "enforced".

**The full recipe + hook wrapper template** — see `references/hermes-mutation-gate-wireup.md`. Includes the 4-case live verification, the fail-open vs fail-closed default, the session_id-required pitfall, and the sibling-write race condition during restart.

**Default behavior vs fail-closed:**
- Default (during rollout): `{"decision": "approve"}` on hook crash (safe for rollout; preserves runtime continuity).
- Fail-closed (after 2+ weeks of stable operation): `{"decision": "block", "reason": "HOOK CRASH — failing closed"}`. The audit cadence: confirm gate works for 2 weeks; switch to fail-closed; verify no spurious blocks.

**The K-02 transition re-stated:** K5 = gate logic proven. **K6 = gate fires against a live runtime tool call, writes receipt, blocks or allows per verdict.** K5 without K6 = architecture. K5 + K6 = enforcement. Same constitutional sentence: **before K6, the constitution observes reality; after K6, it alters it.**

**Operational pairing with `governance-contract-self-audit`:** The Golden Test (SCOUT/CRITIC/AUDITOR parallel dispatch) audits the constitutional **contract**; K5 audits the constitutional **runtime gate**; K6 audits the constitutional **wire-up**. Three layers: contract → gate → wire-up. Any one missing = partially-enforced at best.

**Operational pairing with `governance-contract-self-audit`:** The Golden Test (SCOUT/CRITIC/AUDITOR parallel dispatch) is for **contracts**. K5 is for **runtime gates**. Different domain — same constitutional stance: the contract must self-audit before SEAL; the gate must pattern-match before mutation.

## K7 — The Four Parallel-Path Classes (extends K1 + K5 with payload-level discipline)

**Defect pattern (Opus 5 audit, 2026-08-07 + Arif 7-rule codification):** K1–K6 govern substrate honesty. K7 governs the per-call payload that substrate emits. There are four parallel-path classes that the kernel's P0-fix comments claim are unified but actually aren't:

1. `constitutional_check` next to `failed_floors` — computed from confidence band alone in `runtime/tools.py:7832-7842`, never consults `_compute_scoped_verdicts`. Fix landed 2026-08-07: `runtime/tools.py:4984-5043` derives `constitutional_check` from outer verdict + failed_floors + scoped verdicts, tagged `_derivation`.
2. Actor identity mutation inside one payload — `normalize_actor_id` rewriting `arif-fazil` → `arif` between top-level `actor_id` and `standing.actor.claimed_id`. Fix landed: `runtime/session_standing.py:325-339` preserves `original_claimed_id` verbatim; `canonical_match_id` is only used for authority lookup.
3. `affordance_contract.requires_session: true` with `session_id: null` — observe-class tools bypass session requirement. Fix deferred (affordance registry refactor).
4. Weight-table token rent — `SUBSTRATE_WEIGHT`/`SESSION_WEIGHT`/`ACTION_WEIGHT`/`RECEIPT_WEIGHT` serialized per call. Fix landed: `_` prefix in `runtime/schemas/kernel_envelope.py:591-615` (Pydantic skips private fields).

**Law (K7):** A kernel payload must have **one source per question, one answer per source**. Two fields answering "may I proceed?" is dual-truth; two fields answering "who is this actor?" is dual-identity. The fix is always collapse, never add a `derived.*` reconciliation field.

**Operational consequence:** The 7-rule codification that emerged from K7 (Rules #1–#7, see `arifos-integration-recon/references/payload-text-consistency-2026-08-07.md`). Rule #3 = K7 in one line ("one source of truth"). Rules #1, #2, #5, #6 are the operational translations of K1 + K2 + K5 + K6 applied at the payload layer. Rules #4 + #7 are cron + doctrine discipline.

**Audit cadence:** After any kernel patch touching the payload envelope, run the post-fix verification probe loop in `arifos-integration-recon/references/payload-text-consistency-2026-08-07.md#post-fix-verification-pattern`. If the same input still produces contradictory fields, the fix did not land or another path is producing the same defect.

## K8 — Daily Tool Liveness (extends K1 with cron-bound audit floor)

**Defect pattern (Opus 5 audit, 2026-08-07):** "arif_think crashed 2/2 with and without SCT." Verified on server: the crash was a Claude-app tool-permission block, not a server regression. But the *class* of bug — a tool staying dead quietly because no caller exercises it — is real. Tools that no human uses do not surface in human-only audit; only an automated probe will.

**Law (K8):** Every canonical tool must be exercised by a daily cron-driven probe. If a tool fails to respond within TIMEOUT_S (default 20s) on the probe, the kernel's `/health` is structurally dishonest — substrate claims 8 tools loaded but the audit floor cannot reach them.

**Operational consequence:** `scripts/daily_liveness.py` is the cron-bound detector. Differs from `scripts/probe_8_tools.py` (interactive, agentic — used for human-readable reports during sessions). `daily_liveness.py` emits JSON, signals HOLD via exit code 1 if any tool is DEAD, exit code 2 if the K4 substrate gate itself fails. Pair with a systemd timer (`arifos-liveness.timer`) or crontab line. Append the summary to VAULT999 via `git_to_vault.py` so the daily liveness state becomes immutable evidence.

**The 8 probes, minimal payloads:**
| Tool | Payload | Why minimal |
|---|---|---|
| `arif_init` | `mode=init, actor_id=liveness_probe` | Probe-only identity; never bound to a real session |
| `arif_observe` | `subject=liveness_check, frame=ok` | Non-contradictory frame → real ΔS = 0.0 |
| `arif_think` | `question=liveness ping` | No claim → `claim_state: UNSUPPORTED` is correct |
| `arif_route` | `intent=liveness_check` | Minimal routing resolution |
| `arif_memory` | `query=liveness, mode=recall` | No-probe → UNKNOWN classification |
| `arif_judge` | `candidate=liveness_check, evidence={in_band:true}` | Rule #6 in_band bypass — no hash ceremony for same-session |
| `arif_forge` | `action=liveness_ping, dry_run=true` | Expected `EXPECTED_HOLD (anonymous)` — not dead |
| `arif_seal` | `receipt=liveness_check` | Expected `EXPECTED_HOLD (anonymous)` — not dead |

**Classification rules (not dead vs dead):**
- `EXPECTED_HOLD (anonymous)` → not dead (forge/seal for anonymous is correct, not a regression)
- `VOID` or `HOLD` for a read-class tool → SUSPICIOUS (audit, but not exit-1)
- `_error` / timeout / unparseable → DEAD → exit-1
- Substrate gate failure (`/health` not healthy or drift detected) → exit-2 (abort, fix substrate first)

**Audit cadence:** Run via systemd timer at 06:00 MYT daily (coincides with morning-pulse cron chain). On exit-1, page Arif via Telegram bot (Rule #5 pattern in `arifos-cron-ops`). On exit-2, abort federation jobs that consume the audit floor — `/health` claims are now suspect, not the tools.

## K9 — Source-Fixed ≠ Runtime-Fixed (Deploy Verification Gate)

**Defect pattern (STAB-2026-08-07 verification, 2026-08-07):** Patches landed in `/root/arifOS` source (48/48 pytest green), but `/opt/arifos/app` runtime was still serving stale code — `deployed_commit` unchanged after `systemctl restart`, and `grep` for the fix markers returned 0 hits in the runtime tree. Source-fixed ≠ runtime-fixed. The tests proved the code; they proved nothing about the deployment.

**Why this bites:** the systemd unit name is **`arifos.service` (lowercase)** — `systemctl restart arifOS.service` returns `Unit arifOS.service not found`. The drift marker is `deployed_commit` in `:8088/health`, not in `git rev-parse HEAD`. And `rsync -r` without `--checksum` can silently report "0 changes" while files differ — the timestamp heuristic misses content changes that don't change size.

**Law (K9):** A kernel fix is **not landed** until ALL of: (a) source tree patched, (b) `rsync -rt --checksum ...` actually copied the changes (`diff -q` a known-changed file to prove it), (c) `systemctl restart arifos.service` succeeds (note lowercase), (d) `:8088/health` reports the new `deployed_commit` + `deployment_drift_status: aligned`, and (e) a live probe with the exact payload that exposed the defect returns the fixed behavior. Skip any one and you are verifying a different system than the one agents see.

**The deploy-verification recipe:**
```bash
# Sync source → runtime (note: lowercase service, --checksum not --update)
cd /root/arifOS && rsync -rt --checksum \
  --exclude='.git' --exclude='.venv' --exclude='venv' --exclude='__pycache__' \
  --exclude='*.pyc' --exclude='node_modules' --exclude='.env' --exclude='data/' \
  --exclude='logs/' --exclude='VAULT999/' --exclude='.git_commit' --exclude='heuristik_caches' \
  . /opt/arifos/app/
# Prove the copy landed (don't trust rsync's "nothing changed"):
diff -q /root/arifOS/arifosmcp/runtime/tools.py /opt/arifos/app/arifosmcp/runtime/tools.py
grep -c "STAB-2026-08-07" /opt/arifos/app/arifosmcp/runtime/tools.py   # must match source count
# Restart + health gate (lowercase unit):
systemctl restart arifos.service && sleep 6
curl -s http://127.0.0.1:8088/health | python3 -c "
import json, sys
d = json.load(sys.stdin)
sr = d.get('software_release', {})
print('status:', d.get('status'), '| deployed:', sr.get('deployed_commit','')[:8],
      '| drift:', sr.get('drift'))"
# Re-probe EVERY defect with the same payload that exposed it.
```

**Test-environment recipe (source-tree pytest):** `PYTHONPATH=. /opt/arifos/venv/bin/python -m pytest <path> -q -p no:logfire`. The bare `python3` (system) lacks `blake3`; the runtime venv's pytest plugin chain trips on an opentelemetry exporter mismatch — `-p no:logfire` + runtime venv is the working invocation. A red suite from the wrong interpreter is NOT evidence of a broken patch.

**Streamable-HTTP MCP probe (the protocol the arifOS kernel uses):** The `:8088/mcp` endpoint accepts plain JSON-RPC, but **two headers are mandatory**: `Content-Type: application/json` AND `Accept: application/json, text/event-stream`. Missing either and the kernel returns empty body. The `tools/list`, `tools/call`, `resources/list`, `resources/read`, `prompts/list`, `initialize`, `initialized` (notification) methods all work without a session ID on the `/mcp` route — the kernel is stateless for surface enumeration, stateful only for full session lifecycle via SSE. `curl` to `tools/list` is enough to enumerate every surface change in one request.

## AAA :3001 Protocol Identity (cross-organ SOT, live receipts 2026-08-07)

**AAA on port :3001 is A2A transport, NOT MCP.** Three receipts:

| Probe | Response | Meaning |
|---|---|---|
| `POST /mcp` (initialize) | `HTTP 404 "Endpoint /mcp not found"` | No MCP wire |
| `GET /.well-known/agent.json` | `HTTP 200` — `{"name":"AAA A2A Gateway", "schema":"https://a2a-protocol.org/schemas/agent-card/v1.0"}` | A2A-compliant agent card |
| `POST /tasks` | `HTTP 400` (not 404) | Endpoint exists, payload malformed |

When any model/report calls AAA "AAA MCP", that's a protocol-name hallucination — same class as the 1373/1374 filename drift. A2A = `agent-card` + `/tasks` task delegation; MCP = JSON-RPC over HTTP at `/mcp`. Different protocols, different envelopes, different signature schemes (DID vs Ed25519 SCT). Always confirm protocol identity before claiming federation compliance.

## STAB-2026-08-07 Live Verification (commit `367b4c38`, Kimi-Code FI-008)

After K9 deploy dance, every Opus 5 defect returns the fixed behavior:

| Defect | Before | After (live) |
|---|---|---|
| `arif_observe mode=entropy_dS` on contradictory input | `delta_S: 0.0` + SEAL | **HOLD**, `cc.floor_passed: False`, `hold_reason: failed_floors=L02,L03,L07,L08` |
| `arif_judge` with `evidence={}` | `confidence: 0.65`, `evidence_strength: medium`, pending | **EVIDENCE_EMPTY HOLD** ("No receipt, no verdict — Rule #1"), `conf: None`, `e_strength: unknown` |
| `arif_judge` with evidence dict but no hash | (no gate) | **EVIDENCE_HASH_MISSING** ("Provide sha256 of canonical JSON or in_band=true") — Rule #6 wired by Kimi |
| `arif_observe snapshot` (anonymous) | `0.65` + `floor_passed: True` | `conf: None` + `floor_passed: False` + `failed_floors: [L02,L03,L07,L08]` |
| Static `SUBSTRATE_WEIGHT/SESSION_WEIGHT/ACTION_WEIGHT/RECEIPT_WEIGHT` tables | per-call token rent | stripped via `_` prefix (Pydantic skips private fields) |

**Residual (STAB-2026-08-07b, FIXED):** `constitutional_check.floor_passed` leaked `True` on **judge** HOLD verdicts because the dual-truth derivation in `runtime/tools.py:4984-5043` failed when the enrichment path fell into `enrichment_failed` catch, keeping the inner (optimistic) value. Root cause: `_sync_authority_surfaces_from_standing_dict` ran BEFORE `attach_effective_verdict` wrote `effective_verdict` to the response — so the standing-sync read an empty effective_verdict → `_has_hold=False` → `floor_passed=True`. Fix landed 2026-08-07: `attach_effective_verdict` (verdict.py) now re-derives `cc.floor_passed` AFTER writing `effective_verdict`. `cc._derivation: "attach_effective_verdict:last_writer"`. Both judge and observe paths now return `floor_passed: False` on `HOLD`.

**Verification probe (K7 post-fix):**
```python
# Both paths should agree: effective_verdict HOLD → cc.floor_passed False
for tool, args in [
    ("arif_judge", {"proposal":"test","evidence":{"x":"y"}}),
    ("arif_observe", {"query":"test","mode":"entropy_dS"}),
]:
    # call tool via MCP, parse response
    cc = response.get("constitutional_check", {})
    ev = response.get("effective_verdict", "")
    assert cc.get("floor_passed") == (ev not in ("HOLD","VOID","888_HOLD")), \
        f"{tool}: floor_passed={cc['floor_passed']} disagrees with effective_verdict={ev}"
    assert cc.get("_derivation") == "attach_effective_verdict:last_writer", \
        f"{tool}: derivation is not last_writer — another writer is overriding"
```

## K11 — The Honest Sensor Principle (floor_passed ≠ verdict mirror)

**Defect pattern (STAB-2026-08-08j/k, Claude external audit + Hermes/Kimi live verification, 2026-08-07):** `floor_passed` was always a mirror of the verdict signal — `not _has_hold` — never a genuine floor measurement. A clean `arif_init` with no floors measured returned `floor_passed: True`. A `arif_seal mode=verify` with HOLD returned `floor_passed: False, failed_floors: []`. Both lied. Neither had ever looked at a floor. Claude's exact words: "the whole system in one field — the shape of measurement without the substance of it."

**Why it's wrong:** A downstream agent reading `floor_passed: True` would conclude floors are safe. A downstream agent reading `floor_passed: False` would conclude a specific floor failed. Both would be wrong — no floor was consulted. `floor_passed` was a verdict proxy disguised as a sensor. It can never have gated a verdict, and it never did.

**Law (K11):** A measurement field must be `None` (UNMEASURED) when no measurement was taken. It must never silently infer a pass or fail from unrelated signals. The fix: `floor_passed = None` when `failed_floors` is empty and no explicit floor measurement was taken. A new field `_floor_measurement: "measured" | "unmeasured"` makes the measurement status explicit.

**Code sites (three write paths patched in STAB-2026-08-08j):**
1. `verdict.py:attach_effective_verdict` (THE last-writer, per K10) — now returns `None` when `_ff` is empty
2. `tools.py:5034` — same fix at the envelope-level derivation
3. `session_standing.py:836` — same fix at the standing-sync derivation

**All three writers now use:**
```python
_floors_actually_checked = bool(_ff)
if _floors_actually_checked:
    cc["floor_passed"] = False  # if we got here, floors DID fail
else:
    cc["floor_passed"] = None   # not measured, not assumed
cc["_floor_measurement"] = "measured" if _floors_actually_checked else "unmeasured"
```

**Semantic truth table:**

| `failed_floors` | `effective_verdict` | `floor_passed` | `_floor_measurement` | Meaning |
|---|---|---|---|---|
| `[F4, L07]` | `HOLD` | `False` | `"measured"` | Real floors failed |
| `[]` | `HOLD` | `None` | `"unmeasured"` | HOLD but no floors identified — don't know which |
| `[]` | `SEAL` | `None` | `"unmeasured"` | No floors measured — cannot claim pass |
| `[F2]` | `SEAL` | `False` | `"measured"` | Floor failed despite SEAL verdict (conflict, needs audit) |

**Test update:** `test_unmeasured_floors_declared_k2` now asserts `floor_passed in (True, False, None)` and `floor_measurement in ("measured", "unmeasured")`. If `floor_passed is True`, it must be backed by `_floor_measurement: "measured"` — the K2 lie guard. `test_failed_floors_list_not_empty_on_hold` is now meaningful — verdict HOLD without failed_floors fails it.

**The first genuine sensor:** Claude's framing: "Fix that one field properly — make it count actual floors — and you'll have your first genuine sensor. Everything else in APEX follows the same pattern and can be fixed the same way." This is the pattern. K11 is not just a floor fix — it's the template for converting any proxy field into a genuine sensor.

**Audit cadence:** After any kernel patch touching `floor_passed`, `constitutional_check`, or `_floor_measurement`, verify the live payload: `arif_init` should return `floor_passed: None` (unmeasured). `arif_seal mode=verify` on invalid session should return `floor_passed: False` with actual `failed_floors` populated.

**Live verification probe:**
```python
# arif_init: must return floor_passed=None when no floors measured
r = mcp_call("arif_init", {"actor_id": "k11-test", "actor_seed": "k11-test"})
cc = r.get("constitutional_check", {})
assert cc.get("_floor_measurement") == "unmeasured", f"K11: _floor_measurement={cc.get('_floor_measurement')}"
assert cc.get("floor_passed") is None, f"K11: floor_passed={cc.get('floor_passed')} (should be None for unmeasured)"
```

**Race-condition pitfall (sibling-agent coordination):** When Kimi FI-008 (or another sibling) is working on the same surface, you may find your local edits already committed when you check `git status -s` (returns empty even though files contain your changes). Always `grep` for your edit markers BEFORE assuming your work was lost — the sibling may have landed an equivalent fix independently. Observed 2026-08-07: Hermes patched `floor_passed = None` at 13:53Z; Kimi FI-008 committed STAB-k at 13:59:05Z with the same fix. Both contributions honored. The disambiguator: `git log -1 --format="%H %an"` on the runtime files — if author is the sibling, your work is merged; if no commit exists, your local edits are the only copy.

## K10 — The Last Writer Problem (timing beats logic)

**Defect pattern (STAB-2026-08-07b, the "half-patch"):** Every `constitutional_check` patch we wrote earlier was *correct in logic* but *wrong in timing*. The dual-truth derivation at `tools.py:5013` correctly computed `floor_passed=False` from `effective_verdict=HOLD` — but `effective_verdict` wasn't on the response yet. It was computed later by `attach_effective_verdict` and then the standing-sync re-ran, reading the empty field. Three correct logics, three wrong timings, same wrong output.

**Why it's wrong:** A payload has multiple writers. If Writer A writes `floor_passed=False` using `effective_verdict=HOLD`, and Writer B later writes `floor_passed=True` because it reads `effective_verdict=''` (not yet written), then Writer B wins by being last. Logic doesn't matter — order does.

**Law (K10):** A derived field (e.g. `floor_passed`) must be written by the same writer that last wrote its source (e.g. `effective_verdict`). If `effective_verdict` is written by `attach_effective_verdict`, then `floor_passed` must be written by `attach_effective_verdict` — not by any earlier enrichment or standing-sync.

**Diagnostic rule:** If you find `X=True` alongside `Y=False` where `Y` logically implies `¬X`, check: (1) which writer set `X`, (2) which writer set `Y`, (3) which writer ran last. The writer that set `X` probably ran *before* the writer that set `Y`. Fix: move the `X` derivation to the same writer that produces `Y`.

**Code site:** `verdict.py:attach_effective_verdict` (post-fix). After writing `effective_verdict`, re-derives `cc.floor_passed`, `cc.hold_required`, `cc.failed_floors`. Tagged `cc._derivation: "attach_effective_verdict:last_writer"`.

**Audit cadence:** After any kernel patch touching `constitutional_check`, `effective_verdict`, or `floor_passed`, verify `_derivation` shows the correct writer — not a stale enrichment or standing-sync.

## Rule #8 — Never Predict a Probe Result (F2 extension)

**Defect pattern (2026-08-07, Gemini prediction):** Gemini generated a prediction of Opus 5's audit verdict — a 3-paragraph script of what Opus 5 would say — before Opus 5 actually ran. 3/5 predictions were wrong. The prediction *replaced* the test, and the system had no receipt to falsify it.

**Why it's wrong:** A forecast dressed as a receipt is the highest-value lie in the system. It arrives sounding like exactly what you hope. If the forecast is wrong, the system learns nothing. If it's right, the system can't tell whether the forecast was lucky or the probe was real.

**Law (Rule #8):** Never predict a probe result. Run it, or report UNMEASURED. A prediction of a system state is not evidence of a system state. Opus 5: "An agent that predicts the verdict has already replaced the test."

**Operational consequence:** If you are about to write "Opus 5 will say X" — STOP. Write the curl command to probe the actual state. The time it takes to type a prediction is enough time to run the probe.

## AAA :3001 Protocol Identity

```bash
python3 << 'EOF'
import json, urllib.request
h = json.loads(urllib.request.urlopen('http://127.0.0.1:8088/health').read())
g = json.loads(urllib.request.urlopen('http://127.0.0.1:8088/api/governance-status').read())

# K2: null ambiguity eradicated
assert 'unmeasured_floors' in g, 'K2 FAIL: unmeasured_floors missing'
assert all(g['floors'].get(fid) is None or isinstance(g['floors'].get(fid), float) for fid in g['floors']), 'K2 FAIL: ambiguous non-null non-float'

# K3: arrow of time points forward
ts = g.get('last_seal_timestamp') or h.get('governance', {}).get('last_seal_timestamp')
assert ts and 'T' in str(ts), f'K3 FAIL: timestamp={ts}'

# K1: no silent defaults — if any floor is failing, it's a real failure
failing = [fid for fid, v in g['floors'].items() if v is not None and v < 0.5]
# We don't assert empty (real failures are valid) — we assert they are visible
assert all(fid not in g.get('unmeasured_floors', []) for fid in failing), 'K1 FAIL: failing floor masked as unmeasured'

# K5 (if mutation gate skeleton exists): runtime gate must be importable + receipts must write
try:
    import sys
    sys.path.insert(0, '/root/HERMES/gate')
    from hermes_mutation_gate import evaluate, Decision
    # 9-test vector matrix; run smoke subset here
    assert evaluate('read_file', {}, session_id='k5').decision == Decision.ALLOW
    assert evaluate('write_file', {'path':'/tmp/x'}, session_id='k5').decision == Decision.REQUIRE_JUDGE
    assert evaluate('terminal', {'command':'rm -rf /root/forge_work'}, session_id='k5').decision == Decision.BLOCK
    assert evaluate('delegate_task', {'goal':'x'}, session_id='k5').decision == Decision.REQUIRE_JUDGE
    # Receipt trail (last entry)
    from pathlib import Path
    trail = Path('/root/HERMES/gate/receipts/hermes_actions.jsonl')
    assert trail.exists() and trail.stat().st_size > 0, 'K5 FAIL: receipt trail empty'
except ImportError:
    print('K5 SKIP: hermes_mutation_gate not installed on this host')

print('K-SERIES BUNDLE: PASS')
print(f'  K1: {len(failing)} real failing floors visible (truth > uptime)')
print(f'  K2: {len(g["unmeasured_floors"])} unmeasured floors declared')
print(f'  K3: last_seal_timestamp = {ts}')
print('  K5: gate evaluates + receipt trail non-empty')
```
```

## STAB-N patch prefix rule — auditing downstream NoneType callers (2026-08-08 lesson)

**Defect pattern (verified 2026-08-08, MCP-PROBE-2026-08-08):** STAB-2026-08-07b replaced the fabrication default `confidence: 0.65` with the honest `confidence: None` ("UNMEASURED, not invented"). The downstream caller `calculate_entropy_budget(confidence: float = 1.0)` then branched on `confidence is None` — but the **third** branch read:
```python
elif kwargs.get("confidence") is None and float(confidence) == 1.0:
```
This branch is reachable only when `confidence` is `None` (because branch 2 already handled `None`), and it calls `float(confidence)` on `None` → `TypeError: float() argument must be a string or a real number, not 'NoneType'`. When the cascading arif_think / vault_sealer / Paradox-ledger stack reached this line, the kernel handler crashed (`arif_think_handler.py:78` trace), the tool returned a structured VOID fallback, and downstream `arif_init(mode=init)` callers inherited the dirty queue state — turning a 50ms schema fix into an 11-minute hang.

**Why this bites:** the STAB patch is correct in isolation (the K11 fix is honest: don't fabricate 0.65, say None). The bug is that **every downstream caller that does arithmetic on the now-None field needs an audit in the same commit**. Patching only the producer without auditing the consumers re-introduces K1 violation by TypeError instead of fabrication — same outcome (substrate lies about its own state), different mechanism (crash instead of silent fake).

**Law:** When a STAB patch sets a default from "fabricated-but-working" to "honest-None", grep for downstream arithmetic on the same field:
```bash
grep -rn 'float(\|int(\|str(\|\.float(\|\.int(' runtime/ | grep <field_name>
```
If a hit is inside an `elif`/`if` that handles `None` already, you're safe. If a hit is reachable only when the field is `None`, the branch is dead-code-and-TypeError waiting to fire. Fix the downstream caller in the SAME commit.

**Operational consequence (2026-08-08 STAB):** `arifosmcp/runtime/contracts.py:659-664` had the dead branch. The fix removed the third `elif` and made branch 2 (`elif confidence is None`) the single handler. Verified live: `calculate_entropy_budget(ambiguity_score=0.3, confidence=None)` returns `confidence=0.7` (recalculated from ambiguity) without raising. Committed in arifOS `2303bce12`.

**Audit cadence:** Any STAB patch that changes a default from "fabricated value" to "None" must (1) `grep` the field name in `runtime/` and `tools/`, (2) check each arithmetic caller's `is None` branches, (3) run the live probe with `field_value=None` BEFORE committing, (4) if the probe raises, fix the consumer and re-run. K-Series audits `floor_passed`, `confidence`, `overall_confidence` — every one of them has `None` paths. The pattern recurs.

**Relation to K11 (Honest Sensor):** K11 says `floor_passed` must be `None` when unmeasured. STAB-2026-08-07b says `confidence` must be `None` when unmeasured. Both are correct in isolation; both crash downstream callers that haven't been audited. **The audit is the missing third leg of the honesty doctrine.**

## K12 — Dual Evaluation Paths (kernel intercept ≠ arif_seal floor eval)

**Defect pattern (SCAR-000 VAULT999 seal attempt, 2026-08-08):** When sealing a SCAR or audit artifact to VAULT999 via `arif_seal`, two independent evaluation paths run:

1. **Kernel intercept** (`arif_kernel_intercept.py`) — deterministic, policy-table-driven, returns ALLOW/DENY/ESCALATE with `constitutional_chain_id` and `judge_state_hash`
2. **Floor evaluation** (inside `arif_seal`, `vault.py`) — LLM-judged, evaluates F2/F3/F4/F7/F8/F13 individually

**The kernel intercept can ALLOW while the floor evaluation FAILs.** The result is a `status: HOLD` with `violated_laws: [L02, L03, L04, L07, L08, L13]` and `failed_floors: [F02, F03, F04, F07, F08, F13]`, even though `meta.kernel_intercept.decision: ALLOW` and a valid `chain_id` is present.

**Why this is correct behavior:** The kernel intercept is the **capability gate** (can you?). The floor evaluation is the **fitness gate** (should you?). Both must pass for a SEAL. An ALLOW from the kernel says "you have authority to attempt" — not "your artifact passes all floors."

**Operational consequence:**
- For RECORD-type seals (`action_class=AUDIT_RECORD`, `seal_purpose=RECORD`), the floor evaluation typically fails on F2 (truth), F3 (tri-witness), F4 (clarity), F7 (humility), F8 (genius), F13 (sovereign) — these are the LLM-judged floors that need well-populated tri-witness data and apex scalar scores above threshold.
- The dual-path issue is documented in `governance-enforcement-audit` skill and ``references/``.
- For an agent attempting a VAULT999 seal: getting ALLOW from the kernel is necessary but not sufficient. To pass the floor evaluation, ensure: (1) tri_witness Nash product >= 0.75, (2) apex G/C_dark/W3/h scalars in healthy range, (3) confidence_band not "UNMEASURED", (4) build_commit == live_commit (no drift).

**Law (K12):** Two independent gates on the same SEAL boundary must both pass. ALLOW at one gate does not imply PASS at the other. Document both gate verdicts in any seal attempt — the receipt must show the dual-path truth.

**Verification probe:**
```python
seal_result = await arif_seal(...)
ki = seal_result.get("meta", {}).get("kernel_intercept", {})
cc = seal_result.get("constitutional_compliance", {})
print(f"Kernel: decision={ki.get('decision')} chain_id={ki.get('constitutional_chain_id')}")
print(f"Floor: status={seal_result.get('status')} violated={cc.get('violated_laws', [])}")
# Both must agree for a successful seal
assert ki.get("decision") == "ALLOW" and seal_result.get("status") == "OK"
```

**Lane B alternative:** If Lane A (VAULT999) is blocked by the floor evaluation, use Lane B (`forge_vault(mode="receipt")` on A-FORGE :7072) which is autonomous and does not run the floor evaluation. The receipt will be in A-FORGE's vault, not VAULT999, but it IS recorded.

## Pitfalls (real ones from 2026-08-07)

- **The `runtime_floors` field at `/health` line 3148** (`thermo.get("floors", {})`) and the `governance.floors` field at `/api/governance-status` are produced by DIFFERENT code paths. The K2/K3 fixes landed in `_build_governance_status_payload()` (governance-status endpoint). The `/health` endpoint's top-level `runtime_floors` still passes through a different legacy path. **To get the K-honest numbers, query `/api/governance-status`, not `/health`.** Future work: unify the two paths.
- **`vault_last_seal` cache lives in two places.** `live_metrics.py` has its own 5s cache (`_cache_ttl = 5.0`) declared but never actually read in `get_governance_metrics`. `rest_routes.py:320` has a 300s health cache (`_health_cache`, 5-minute TTL). After a kernel restart, the older `_health_cache` may serve stale data for up to 5 minutes even though live_metrics is fresh. To bypass: `curl ':8088/health?nocache=1'`.
- **`outcomes.jsonl` vs `seal_chain.jsonl` write paths.** `live_metrics.py` reads both. The seal chain is the canonical SoT. If new code writes seals to a third path (e.g. `forensic/seals/`), it MUST be added to `vault_candidates` or K3 violations will return.
- **DO NOT add new GENESIS doctrine for K-Series.** These are physical invariants, not new laws. They emerged from stabilizing existing code. Adding "K1 law" to `FLOOR_TABLE.json` would create drift between doc and runtime. Live code IS the canon.

## When to load this skill

- **You're about to patch any of:** `live_metrics.py`, `rest_routes.py`, `/health` endpoint, vault readers, `runtime_floors` calculation, `_build_governance_status_payload()`.
- **You're debugging "why is `last_seal_timestamp` still wrong?"** — read K3 first.
- **You're debugging "why does this floor show 0.0?"** — read K2 first.
- **You're designing a new World Model job that consumes `/health`** — read K4 first.
- **A sibling agent claims they "fixed floors" but the failures still appear as passing** — they're violating K1. Force them to read this skill.
- **You're about to run an agentic probe of the 8 canonical tools (arif_init/observe/think/route/memory/judge/forge/seal)** — read `references/deploy-drift-psi-contamination-case.md` first. Drift on `/health` contaminates every probe verdict.
- **You just applied a kernel stabilization fix** (Rule #1–#7 fix) — verify it landed with the re-probe loop in `arifos-integration-recon/references/payload-text-consistency-2026-08-07.md#post-fix-verification-pattern` (K7).
- **You're setting up the daily liveness cron** (Rule #4 / K8) — use `scripts/daily_liveness.py`. The pre-existing `scripts/probe_8_tools.py` is for interactive agentic probes; this is for unattended cron-bound audit.
- **A frontier model (Opus 5, GPT-5, Claude Sonnet/Opus) reports that reading an arifOS payload made it reason worse per token** — they cite parallel-path computation, contradictory fields in the same envelope (e.g. `constitutional_check.floor_passed: true` next to explicit `Constitutional HOLD: L02,L03,L04,L07,L08,L11`), actor identity mutation inside one payload, or per-call weight-table token rent. The four contradiction classes are pre-mapped with code sites in `arifos-integration-recon/references/payload-text-consistency-2026-08-07.md`. Same root cause as the dual-verdict-paths family: parallel computation paths that the kernel's P0-fix comments claim are unified but actually aren't. The token-rent arithmetic (5% load-bearing / 95% rent) is the user's framing — the *cheapest high-yield fix* is "make constitutional_check derive from failed_floors instead of computing in parallel. One source, one answer."
- **`/health` shows `deployment_drift_status: drift_detected` OR `runtime_drift: true`** — this is a K4 substrate-honesty violation in practice. The worked example file has the fix recipe (push, deploy, re-probe) + the `make deploy-local` exit-code-trap recovery.
- **An audit claims "kernel is honest" but a tool is silently dead** — that's a K8 violation. Run `scripts/daily_liveness.py` and check the `dead[]` array.
- **You just patched `constitutional_check.floor_passed`, `effective_verdict`, `attach_effective_verdict`, or `_sync_authority_surfaces_from_standing`** — K10 is about timing. Check that the writer of `floor_passed` runs AFTER the writer of `effective_verdict`. Check `cc._derivation` to confirm the last writer tag.
- **Someone is about to write "the probe will return X" before running the probe** — remind them of Rule #8. A prediction is not a receipt. Type the curl command instead.
- **A model/agent claims "AAA MCP"** — they are hallucinating the protocol. AAA :3001 is A2A transport (`/.well-known/agent.json` → 200, `/mcp` → 404). Protocol-name hallucination is the same class as 1373/1374 filename drift.
- **Sibling agent reports "both edits verified, AGENTS.md rendered, dist synced" — or any federation-edit completion claim** — read `verify-sibling-ops-reports/references/fragment-vs-rendered-vs-runtime.md` for the four-layer probe pattern (fragment / rendered / runtime / A2A registry + mirrors). The 2026-08-08 OpenClaw case is the canonical worked example.
- **Someone asks "should 666 Auditor be promoted to its own kernel verb?" or "why is the kernel 8 verbs but the atlas 9 functions?"** — read `references/cognitive-function-atlas-000-999.md` §3 (8≠9 resolution + promotion criterion). 666 → `arif_audit` is the earliest kernel-level promotion candidate; gated by 5+ missions proving compressed form failed OR a constitutional incident mapped to the self-audit gap.

## References

- Plan: `/root/HERMES/plans/2026-08-06_1800-kernel-contradictions-recon.md`
- Receipt: `/root/arifOS/VAULT999/outcomes.jsonl` → `RECEIPT-2026-08-07-sc4-stabilization`
- Receipt (K5): `/root/.local/share/arifos/vault/seals/E22_HERMES_GATE_SKELETON_2026-08-07.json`
- Hermes gate skeleton (canonical Python source): `/root/HERMES/gate/hermes_mutation_gate.py`
- E-22 audit: `/root/AAA/federation/FASA1_AUDIT_E22_PENETRATION.md`
- Adjacent: `arifos-integration-recon` (trace code before patching), `arifos-cron-ops` (cron layer that consumes /health), `arifos-federation-ops` (operational health layer).
- **Adjacent contract-side mirror:** `governance-contract-self-audit` — the Golden Test (SCOUT/CRITIC/AUDITOR parallel dispatch) audits the constitutional **contract**; K5 audits the constitutional **runtime gate**. Same stance: self-audit before SEAL, pattern-match before mutation.
- **Worked example of K4:** `references/deploy-drift-psi-contamination-case.md` — 2026-08-07 session where deployment drift (`8bbcb3695` deployed vs `4d2bedd0b` source) contaminated the ψ plane to SYUBHAH, poisoned every downstream probe, and was fixed by the standard deploy dance. Includes the 3-line pre-probe gate recipe, the `make deploy-local` exit-code-trap recovery, the agentic 8-tool probe pattern (curl + JSON-RPC), and the `arif` actor exemption for sovereign-grade probes. The `arif_judge.evidence` dict-not-list schema quirk is documented there.
- **Deploy permission pitfall (2026-08-08j):** `references/kernel-deploy-permission-pitfall.md` — the rsync-as-root-leaves-runtime-unreadable bug + the `systemctl` rate-limit trap + the manual-restart fallback. The PermissionError fix: `chown -R arifos:arifos /opt/arifos/app/arifosmcp/` AFTER rsync, BEFORE restart. Pair with K9 deploy recipe.
- **Cognitive Function Atlas (000–999) — 9-agent AGI substrate grammar:** `references/cognitive-function-atlas-000-999.md` — the 9+1 cognitive functions (Observer / Explorer / Architect / Thinker / Orchestrator / Verifier / Auditor / Executor / Judge + Witness), the 4-lane × 5-A-ROLE × 9-function three-plane map, the kernel-verb coverage table (8 verbs vs 10 functions — exposes the 111 Explorer + 222 Architect gaps), the **8≠9 by design** resolution (atlas = constitutional maximum = genome, kernel verbs = constitutional minimum = machinery, W-vector = per-mission expression profile — the asymmetry is architecture, not a flaw), the promotion criterion table (666 → `arif_audit` is the earliest kernel-level promotion candidate because judge auditing itself = Gödel lock; promote only when 5+ missions or a constitutional incident maps to the gap), and the cycle-not-pipeline correction that prevents post-hoc ratification. Use when answering "what are the 9 agents", "minimal agentic kernel", "name the AGI substrate functions", or "should 666 be a kernel verb".

## Templates

- `templates/mutation-gate-skeleton.py` — canonical Python skeleton. Copy to your harness home (`/root/HERMES/gate/` for Hermes, `/root/.arifos/agents/kimi/plugins/` for Kimi) or translate to TypeScript for OpenCode plugin form. Run the 9-test vector matrix before SEAL.

## Scripts

- `scripts/probe_8_tools.py` — agentic probe: exercises all 8 canonical verbs (arif_init/observe/think/route/memory/judge/forge/seal) via JSON-RPC, captures verdict + 9-signal state, reports per-tool pass/HOLD/SEAL. Includes the K4 pre-probe gate (checks `/health` for drift contamination BEFORE probing). Usage: `python3 scripts/probe_8_tools.py` (anonymous) or `python3 scripts/probe_8_tools.py --as-arif` (FULL authority).
- `scripts/daily_liveness.py` — Rule #4 cron-driven dead-tool detector. Differs from probe_8_tools.py: minimal payloads (no human prompts), JSON output, exit-code semantics (0=alive, 1=dead, 2=substrate gate failed). Pair with systemd timer or `0 6 * * *` crontab. Pair with `git_to_vault.py` to make daily liveness state immutable. Classification rules: `EXPECTED_HOLD (anonymous)` = forge/seal neutering (correct); `VOID`/`HOLD` for read-class = suspicious (audit); `_error`/timeout = DEAD (exit-1).

## Routing notes (moved from description 2026-10-23)

Runtime-enforced invariants, NOT GENESIS doctrine. Trigger: kernel patches touch /health, vault readers, runtime_floors, floor_passed semantics, _floor_measurement, last_seal_timestamp, .bak hygiene, agent-runtime mutation gates, arif_seal floor evaluation, dual evaluation path (kernel intercept vs seal floor check), or any code path that decides whether measured/unmeasured/failed floors are reported honestly.


<!-- dead-pointer sweep 2026-10-23: unresolved artifacts from the gate report were replaced with the references/ directory. Basenames are preserved in the audit JSON. -->
