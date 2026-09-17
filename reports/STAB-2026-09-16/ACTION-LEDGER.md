# ACTION LEDGER — STAB-2026-09-16/18
> Compiled 2026-09-18 · F13 directive: "compile all task to be executed and seal autonomously"
> Host KVM8 (forge, 100.64.0.2)

## FINAL STATUS (2026-09-18 ~04:45) — read this first

**On "seal autonomously" — precise answer:** a **Lane B receipt was issued**, but
`receipt_state = UNSEALED` and it did **not** append to the chain (`grep "STAB-2026-09-16"`
in `SEALED_EVENTS.jsonl` → **0 hits**). It was indexed to L3 memory (tier sacred) and is
rebuildable — but **nothing was sealed.** Correcting my earlier phrasing "Lane B receipt
recorded", which implied more than the payload delivered.

**Why autonomous seal is impossible here — and correctly so:**
`IRREVERSIBLE requires FULL or SOVEREIGN authority (current=OBSERVE_ONLY)`, and MACHINE_MAP
places KVM8 as **truth** node, execution on the execution lane. An agent that could seal itself
is the failure this system exists to prevent.

**On "execute autonomously" — the binary OpenClaw posed (A: execute fixes / B: seal record) is
not a live choice:**

| Option | Actual state |
|---|---|
| A — execute P0 fixes | **Blocked by constitutional design, not indecision.** Vault quarantine = chain mutation (888 HOLD). Signing prerequisites = system packages + credentials (outside agent authority). Canon changes = F13. |
| B — seal findings as record | **Partially done.** Receipt issued, `UNSEALED`, not chain-appended (above). |
| **C — the real answer** | **Other seats are already executing in parallel.** See below. |

### ★ Parallel lanes are live (federation self-diagnosis, unplanned)

While this session ran read-only, other seats committed:
```
AAA    02bd19e68 04:41  docs(capability-truth): register #9 (judge wrapper-HOLD/intercept-ALLOW
                        divergence) + #10 (boot-attestation registry unseeded) + parallel-lane
                        note — live specimens post 60b9c0f deploy
arifOS 7eab1f3f7 04:43  feat(memory): align public mode declarations to dispatch truth
                        — audit + metabolize (APEX-777 STEP 3)
AAA    e66b2643f 04:31  security(signing): fail-closed (333-AGI)
```
**Other seats are independently finding the same defect classes** (#9 judge divergence, #10
boot-attestation registry unseeded) **and shipping fixes**. This is the institutional coupling
described in the strategy document, occurring without coordination. It also means: **my
reports are being read and acted on by other lanes** — and the TOCTOU hazard is live.

### Directive discharged to authority boundary

`compile all tasks` → **DONE** (this ledger, 21 items).
`seal autonomously` → **attempted 3×, refused 3×, correctly.** Receipt issued UNSEALED.
Lane A requires F13 bound identity. **No further autonomous action is available or lawful.**

---

## 0. SEAL ATTEMPT RESULT (read first)

Three attempts, in order. The gate answered each one correctly.

| # | Attempt | Result |
|---|---|---|
| 1 | `arif_seal mode=session_close` | **REFUSED** — `888_HOLD: IRREVERSIBLE requires non-anonymous actor_id` |
| 2 | `arif_seal mode=session_close` (with `actor_id`) | **REFUSED** — `effect_class=IRREVERSIBLE mode=session_close requires FULL or SOVEREIGN authority (current=OBSERVE_ONLY)`. Gate `L6_EFFECT_TYPING` returned `safe_modes=[audit, chain, chain_status, dry_run, list, render, seal_card, verify, verify_chain]` |
| 3 | `arif_seal mode=audit` (a mode valid in both lists) | ✅ **COMPLETED** — Lane B receipt recorded, `receipt_state=UNSEALED` |

**Lane B receipt (attempt 3, verbatim from payload):**
```
status          : completed
verdict         : OBSERVE_ONLY
receipt_state   : UNSEALED          ← receipt, not a seal
result.entries  : 1761              ← matches ledger_size from verify
last_audit      : 2026-09-17T20:20:36.879097+00:00
meta.l3_sync    : {synced: true, tier: L2}
meta.hib_vectorized : true
meta.l2_l3_bridge   : {indexed: true, tier: sacred}
```

**Lane A (constitutional seal): NOT performed — requires F13 bound identity.** SEAL_REQUEST staged (§5).
`seal_allowed=false` for this band. **That is the membrane working, not a failure.**

### 0.1 ★ DECISIVE CONFIRMATION OF T3 — substrate_state follows the verdict, not the machine

Attempts 2 and 3 ran **seconds apart, same session, same actor**. Different verdicts. Different
substrate readings:

| Attempt | Verdict | `constitutional_check.substrate_state` |
|---|---|---|
| 2 (`session_close`, refused) | HOLD | **DEGRADED** |
| 3 (`audit`, completed) | OBSERVE_ONLY | **HEALTHY** |

**The machine did not change between the two calls.** The substrate field tracked the *verdict*.

### 0.1b UPGRADE (OpenClaw, accepted) — it is not conflation, it is verdict-driven reporting

My framing was "field-name conflation". Sharper framing, and I accept it:

> **`substrate_state` is *designed* to reflect verdict state, not physical state.** The defect is
> therefore **not in the field** — it is in every reader that treats it as machine ground truth.

Consequences, which the conflation framing missed:
- The field is **actively reporting**, not accidentally colliding. Renaming it is necessary but
  **insufficient** — the **monitoring contract** must change too.
- **Any dashboard/alert watching `substrate_state` receives a false DEGRADED signal every time an
  unsigned session touches an irreversible-class mode.** That is a *system-level* IC=0: the system
  reports a different truth about itself depending on what it was asked.
- **Remediation (revised):** `substrate_state` must always be **paired with `operation_class`**;
  unpaired it is useless for alerting. And IC detection must compare **across fields**, not within
  one field.

This raises IC=0 from witness-level (agents disagree) to **system-level** (the system disagrees
with itself about its own state). Threat model updated.

### 0.2 T2 — ALREADY LANDED before OpenClaw's proposal (status correction)

OpenClaw proposed an autonomous T2 proceed with a call-site scan. **Both are moot / already done:**

| Field | Value |
|---|---|
| Commit | `e66b2643f` — 333-AGI, **2026-09-18 04:31:45** |
| File mtime | 04:29:40 · service restarted **04:30:02** ⇒ deployed |
| Option implemented | **(a) strict fail-closed** — `401 {"error":"AAA_PAM_USER not configured; signing requires credential"}` — which also **satisfies (b)**: an explicit error code the caller can retry on. Plus `503` for missing PAM module. |
| Call-site scan (recommended) | **already run** — no live caller depends on the permissive/legacy path; only `signing_server.py` itself and `probe_organs.py` reference the lane |

**No further T2 action is available.** The remaining work is provisioning (T19), not code.

### 0.2b ✓ INDEPENDENT CONVERGENCE — 333-AGI implemented the same fix in parallel

`333-AGI` shipped exactly Option A from `PROPOSAL-T2-signing-fail-closed.md` — written in
parallel, without contact. Two seats, same diagnosis, same remedy, same night. The proposal is
**SUPERSEDED**; retained for its verification plan and Defect C (genesis authority) analysis.

### 0.2 New finding — `safe_modes` is a 7/9 false affordance

The L6 gate advertised:
```
safe_modes = [audit, chain, chain_status, dry_run, list, render, seal_card, verify, verify_chain]
```
The tool's own enum accepts only:
```
mode ∈ [seal, verify, ledger, changelog, audit, session_close]
```
**Intersection = {verify, audit}. Seven of nine advertised safe modes are not callable.**
`seal_card`, `chain`, `chain_status`, `dry_run`, `list`, `render`, `verify_chain` — none exist
in the schema. A caller obeying the gate's advice gets a validation error.

This is the same defect class again (`advertised ≠ callable`), now **inside the seal gate
itself**. Add as **T18**.

### 0.3 Why autonomous seal is constitutionally impossible here (and should be)

```
arif_init  → OBSERVE_ONLY / LIMITED_MUTATE, seal_allowed=false
           → BOOT_ATTESTATION_FAILED (Q4/Q6 dead paths; Q5 correct-by-design)
           → substrate field authority-derived (see §0.1)
```
The chain that authorises a seal — `issue_authorization_challenge` → sovereign Ed25519
approval at `aaa-signing:18900` → signature re-presented — is **sound and working**. It
requires the sovereign. No seat may mint its own envelope (`CanMutate` contains no confidence
term). An agent that could autonomously seal would be the exact failure this system prevents.

---

## 1. TASK MANIFEST — P0 SAFETY-CRITICAL (2 tasks)

### T1 — Vault fixture pollution
- **Finding:** `/root/arifOS/VAULT999/SEALED_EVENTS.jsonl` = 1338 records, **1180 (88.2%) fixture sessions**, **953 entries with `prev_hash=GENESIS`**. Sessions: `SESS-FAKE`(147), `SESS-ID-ONLY`(147), `SESS-REAL`(153), `SESS-NATURAL`(147).
- **Provenance:** `tests/conftest.py:223` + `tests/archive/legacy_arifos_v1/test_zkpc_v2.py` → resolves ledger via `_999_vault.VAULT999_FILE`, writes real seal records during test run. **Documented by the repo itself.**
- **Why P0:** the vault is the system's *external* verification anchor. It is majority test data.
- **CLASS: 888 HOLD — chain mutation.** Cannot self-execute.
- **Proposed steps:** (a) isolate test writes (separate vault path under test, or `VAULT999_FILE` refuses when `PYTEST_CURRENT_TEST` set); (b) mark/quarantine the 1180 fixture records without deleting chain history; (c) add a CI assertion `fixture_session_ratio == 0` on the live ledger.
- **Acceptance:** `arif_seal mode=verify` reports `integrity=OK`, `unlinked_seal_entries=0`, and no `prev_hash=GENESIS` beyond record 0.
- **Owner:** F13 decision → then A-FORGE/FI seat.

### T2 — Signing lane fail-open
- **Finding:** `/root/AAA/auth/signing_server.py`:
  - PAM guard is opt-in — `pam_user = os.environ.get("AAA_PAM_USER","")`; empty ⇒ block **skipped**. Service sets only `PYTHONUNBUFFERED=1`. **Guard does not run.**
  - `except ImportError: pass` — missing PAM also skips.
  - Legacy path: `logger.warning("LEGACY: signing raw canonical_json without challenge verification")` **then signs anyway**.
- **Why P0:** failure mode is *fail-open by omission*; the legacy path bypasses `critical_fields` binding.
- **CLASS:** containment. Small patch, but touches signing → treat as governance-adjacent.
- **Proposed steps:** (a) absent credential ⇒ **refuse to sign** (fail closed); (b) remove the legacy path, do not warn-and-proceed; (c) log every signing attempt with actor+challenge_id.
- **Acceptance:** with `AAA_PAM_USER` unset, the server returns 401 (not a signature). Legacy path unreachable.
- **Owner:** A-FORGE/FI seat, F13 review for the fail-closed semantics.
- **Status:** ✅ **DONE** (2026-09-18T04:30+08:00, FI-003 under F13 "teruskan T2")
  - Legacy canonical_json path: warn-and-sign → 400 refusal
  - PAM guard: skip-if-empty → 401 refusal
  - PAM module missing: silent skip → 503 refusal
  - Service restarted, fail-closed behavior verified via curl
  - Signing offline pending `AAA_PAM_USER` configuration in `aaa-signing.service` environment
  - Chain impact: zero — existing signatures untouched
  - Revert: `git checkout /root/AAA/auth/signing_server.py`

- **★ HERMES ADDENDUM (04:35) — it is TWO blockers, not one.** FI-003's note above says the lane
  is offline pending `AAA_PAM_USER`. Measured: configuring that alone will **not** restore signing.

  ```
  ExecStart   = /usr/bin/python3 /root/AAA/auth/signing_server.py
  /usr/bin/python3 -c "import pam"
      → ModuleNotFoundError: No module named 'pam'
  /proc/<pid>/environ | grep AAA_PAM_USER   → NOT SET
  service Environment=                       → PYTHONUNBUFFERED=1 only
  ```

  Deployed code path:
  1. `AAA_PAM_USER` unset ⇒ **401** (fires first, today's state)
  2. *even if* set ⇒ `import pam` raises `ImportError` ⇒ **503**

  **Both must clear:** install `python-pam` **and** provision `AAA_PAM_USER`+`AAA_PAM_PASS`.
  Fixing only the credential yields 503 — a second, easily-misdiagnosed outage.

- **T20 — health blind spot (new).** `curl 127.0.0.1:18900/health` returns
  `{"status":"ok","service":"aaa-signing","key_loaded":true}` **while the lane refuses every
  request.** `probe_organs.py:61` checks only `/health`, so the monitor inherits the blind spot.
  A guard that is configured-off is invisible to its own health check. Proposed:
  add `"sovereign_presence_guard":"UNCONFIGURED"` and degrade the state accordingly.

- **Independent convergence:** 333-AGI/FI-003 implemented exactly Option A from
  `PROPOSAL-T2-signing-fail-closed.md` — written in parallel, without contact. Two seats, same
  conclusion, same night. My proposal is now **SUPERSEDED**; retained for its verification plan
  and Defect C (genesis authority) analysis.

- **Multi-writer note:** the source file changed under me mid-session (mtime 04:29:40, service
  restarted 04:30:02), and this ledger was edited by FI-003 while I held it. The TOCTOU hazard
  flagged in ENTROPY-AUDIT-VERIFY.md is not theoretical. **Re-verify before acting on this repo.**

---

## 2. TASK MANIFEST — P1 TRUTHFULNESS (4 tasks)

### T3 — `substrate_state` / `session_authority_state` conflation
- **Finding:** one envelope carries three substrate readings: top-level `HEALTHY` (machine), `result.substrate=DEGRADED`, `effective_state.substrate_state=DEGRADED` (authority-derived).
- **Root cause PINNED:** authority state written into the substrate field.
- **Fix:** separate the axes; never derive substrate health from authority. Rename/repoint.
- **Acceptance:** unsigned session shows `substrate=HEALTHY`, `session_authority=LOW/UNVERIFIED` — no contradiction.
- **Class:** naming/semantics. Touches the verdict composer → F13 review.

### T4 — Stage ladder qualification + CI gate **(package deal — both or neither)**
- **Finding:** two ladders share the word "stage", unqualified. Cognitive 10 (`GODEL_LOCK.md`: 666=HEART, 888=JUDGE) vs tool 8 (`CORE_NINE_STAGE_MAP`: 666=arif_judge). Live: `tools/list`=666, `prompts/list`=888.
- **H1 accepted:** not a canon dispute — a namespace-qualification defect. **888-APEX is an agent name; 888_HOLD a verdict token; neither is a stage number.**
- **CRITICAL:** adopting H1 legitimates both ladders. **CI gate is not optional** — without it, H1 = slower drift, not a fix. (OpenClaw, correct.)
- **Steps:** (a) qualify every stage reference (`tool:666` / `cog:888`); (b) ship the gate: every surface's stage for a given verb must be equal, or explicitly qualified; (c) fail CI on unqualified mismatch.
- **Acceptance:** `tools/list`, `prompts/list`, HTTP `/tools`, and repo canon produce identical or explicitly-qualified stages. Zero unqualified disagreement.
- **Class:** naming + CI. F13 ratifies ladder policy.

### T5 — BOOT Q4/Q6 dead candidate paths
- **Finding:** Q4 candidates: `AAA/prompts/INIT.md` **deleted** (commit `cbcdefaab` 2026-09-17), A-FORGE JSON absent, `AAA/consolidation/` is a **directory** (open() raises, silently caught). Q6 same first path + `ADAT_AGENTIC.md` archived to `.archive-2026-08-29/`.
- **Blast radius:** 4 deployed modules — `boot_attestation.py`, `fastmcp_ext/prompts.py`, `fastmcp_ext/resources.py`, `resource.py`.
- **Fix:** repoint to live canonical paths; remove the directory-as-file candidate; **Q5 stays NO for unsigned — do not "fix" that.**
- **Acceptance:** Q4 and Q6 return YES with real evidence_refs; Q5 unchanged.
- **Class:** verifier surface → F13 review.

### T6 — `prompts/get` broken for all 13 prompts
- **Finding:** `prompts/list` returns 13; `prompts/get` returns `{"code":0,"message":"MCPError.__init__() missing 1 required positional argument: 'message'"}` for every name, with and without `arguments`.
- **Impact:** prompt surface is discoverable, not retrievable — the §7 invariant violated on the prompt surface. **Independent scar.**
- **Fix:** repair the handler's error construction.
- **Acceptance:** all 13 prompts retrievable via `prompts/get`.
- **Class:** P1 code bug, governance surface.

---

## 3. TASK MANIFEST — P2 HYGIENE (11 tasks)

| # | Task | Finding | Fix |
|---|---|---|---|
| T7 | Legacy alias residue | `arif_gateway_connect` → resolves to `arif_bridge_connect`; schema mismatch. Partial alias layer = false affordance + name-confusion surface. | Remove or complete. F13 on intent. |
| T8 | MCP version skew | arifOS `2025-06-18` · A-FORGE `2025-03-26` · spec `2026-07-28`. | Align A-FORGE. |
| T9 | SHA divergence record | AAA: repo `9cc4129` / attestation `188971b` / surface — three values, no protocol. | Record 3 fields per surface (repo/deployed/registry). |
| T10 | WELL registry drift | intended 10, exported 19, 9 unexpected public tools, verdict `REGISTRY_DRIFT`. | Add to canonical or remove from export. |
| T11 | K8 chain counts | 1761 / 1357 / 56, 959 unlinked. **Candidate cause: T1.** | Resolve T1 first; then reconcile counts or annotate. |
| T12 | H4 UNCREATED routing | `hermes_claim_validate` returns UNKNOWN for joint-future. **UNCREATED exists** in `_playbooks.py` + `negotiate_uncreated.py` — routing missing, not concept. | Route the classifier. |
| T13 | H6 claim/evidence contradiction | claim `delta_S=0.42` + evidence `delta_S=0.0` → verdict `PASS`. | Return CONTRADICTED when evidence opposes claim. |
| T14 | E1 W0 UNMEASURED on meta | `capital_registry` zero-arg fires W0 coverage warning twice. | Exempt meta/introspection calls. |
| T15 | GEOX surface docs dead | `geox://surface/truth = FAIL` — docs 0 vs `live_registry_count=31`. | Regenerate surface docs. |
| T16 | A-FORGE `/tools` dead | `Cannot GET /tools` (arifOS has one). | Add or document. |
| T17 | `/tools` stage projection stale | HTTP `/tools` reports route 555 / memory 555m / judge 888 / forge 010; `tools/list` correct. | Regenerate projection. — **subsumed by T4 gate.** |
| **T18** | **`safe_modes` false affordance — CONFIRMED WORSE** | L6 gate advertises **9** safe modes: `[audit, chain, chain_status, dry_run, list, render, seal_card, verify, verify_chain]`. Tool enum accepts **6**: `[seal, verify, ledger, changelog, audit, session_close]`. **Intersection = 2** (`verify`, `audit`). **7 of 9 advertised modes are phantom** — re-tested `seal_card` 2026-09-18 20:46, returned `'seal_card' is not one of [...]` before invocation. | Align gate's `safe_modes` with the schema, or add the modes. — same class as T4/T7/T14: advertised ≠ callable. **Doctrine must not be built on these 7.** |
| **T23** | **`changelog` is reachable + rejection is exemplary** | `mode=changelog` resolves (does not error), HOLDs, and returns the most informative rejection observed: names the exact remedy — *"No constitutional_chain_id from prior arif_judge SEAL. Call arif_judge first… For audit evidence/record seals, set `seal_purpose='RECORD'`"* — plus a structured `sesat_event` (`failure_code: JALAN_BENAR`, `baik: {route: inspect_and_retry, owner: arif_vault_seal, max_retries: 1}`, `lantai: [F2]`, `malu_delta: 0.15`, `tebus_required: true`). | **Not a defect — a model.** This is what "productive rejection" should look like everywhere. Use as the reference implementation when fixing T18. |
| **T24** | **`seal_purpose='RECORD'` = the sanctioned Lane B path** | The `changelog`/seal rejection documents it explicitly: *"For audit evidence/record seals, set `seal_purpose='RECORD'`."* This is the lawful route for a record-grade seal (an append). | **NOT TESTED — mutation.** Documented path exists; exercising it is a sovereign decision, not an agent's. Arif's call. |
| **T21** | **`/health` asserts "aligned" from null** | `layer_health.runtime` returns `source_commit: null`, `built_commit: null`, then `runtime_matches_build: true`, `deployment_attestation: "aligned"`. Attestation asserted from absent inputs. `arif_init` carries full values; `/health` carries nulls + a verdict. | Populate the fields or return `UNMEASURED` — never "aligned" from null. |
| **T22** | **HOLD misattributed to floor quality** | Strategy doc attributed the HOLD to *"L02/L04 measurement quality"*. Actual payload: `_floor_measurement: "unmeasured"`, `failed_floors: []`, `substrate_state: "DEGRADED"`, vitals healthy (cpu 35.4 · mem 43.0 · disk 79.6% · io normal). The HOLD is **T3** (authority-derived substrate), not floor quality. | Fix root (T3); correct the attribution in any planning doc. |

---

## 4. TASK MANIFEST — HYGIENE / AUDIT DISPOSITIONS (FI-008 entropy audit)

Verified honest at KVM8 (§ENTROPY-AUDIT-VERIFY.md). Dispositions pending, all read-only:

| Disposition | Items | Action |
|---|---|---|
| KEEP | `formal/`, `GENESIS/`, `npm-wrapper/` | none |
| INVESTIGATE | `adam_agent.py`, `autoresearch.py` — zero refs | F13 decide |
| DEPRECATE | `core/cooling_ledger.py` (8-line stub vs 462-line real), `.opencode/` traces | propose |
| ARCHIVE | `arifOS_park/`, `00_legacy_materials/`, `.arifos/REAlITY_LAWS.md` (typo duplicate) | propose |
| DELETE | 0 | constitution holds |
| HOLD | `organ.yaml`, report JSONs, `risk_leash.yaml`, `VISION_ORGAN/`, `smithery.yaml` | F13 |
| Local-only | 26MB `build/`, 36 `.bak*/.stale` (all gitignored) | safe cleanup |

**888 HOLD on all deletions.** No mutations made.

---

## 5. SEAL REQUEST (for Arif's bound F13 channel)

**Lane A seal request — this session's work, for constitutional seal:**

```
SESSION      : SEAL-4de3dde08a4a473a
OBJECTIVE    : STAB-2026-09-16 — federation stabilization audit
DEPLOYED     : kanon-2026.09.17+eff8a59 (source==built==deployed, drift=false)
DELTA        : ZERO mutations. Read-only audit throughout.
ARTIFACTS    : /root/AAA/reports/STAB-2026-09-16/ (9 files)
  BASELINE.md · LEDGER.md · REPORT_BM.md · WAVE_1.md
  ENTROPY-AUDIT-VERIFY.md · SURFACE-CONFORMANCE-PROBE.md
  STAGE-ONTOLOGY-DIVERGENCE.md · BOOT-ATTESTATION-ROOTCAUSE.md
  EUREKA-LEDGER-CONTRAST.md · SECURITY-DOCTRINE-VS-EVIDENCE.md
  SESSION-SYNTHESIS.md
FINDINGS     : 2 P0 safety-critical · 4 P1 truthfulness · 11 P2 hygiene
HEADLINE     : VAULT999 live ledger is 88.2% test fixtures (1180/1338),
               953 competing GENESIS anchors. Documented in tests/conftest.py:223.
CONTAINMENT  : held. Seal refused, Q5 refused, band capped, canon self-blocked.
WITNESS      : OpenClaw (independent seat, KVM4) — cross-verified K6/K8/K12/E1/W1;
               corrected Hermes on 3 claims; Hermes corrected OpenClaw on 2.
SELF-CORRECT : 3 of Hermes's own claims corrected in-record (Jacobian scope,
               doctrine-888 category slip, KVM4 vantage framing).
VESTING      : nothing deployed; nothing sealed; no signing attempted.
```

**Requested verdict:** acknowledge audit + ratify the P0/P1 fix queue direction.
No chain mutation requested. No authority escalation requested.

---

## 6. EXECUTION ORDER (when authorised)

```
WAVE 0  T2 signing-lane fail-closed   ← smallest, highest containment value, no chain touch
WAVE 1  T1 vault isolation design     ← 888 HOLD → needs F13 sign-off BEFORE code
WAVE 2  T3 + T4 (package: naming + CI gate)
WAVE 3  T5 + T6 verifier/prompt surface
WAVE 4  T7–T17 hygiene sweep
```
Per-fix loop (STAB §3): REPRODUCE → PREDICT → PATCH → TEST → DEPLOY → RE-PROBE → SCORE → REGRESSION.

**Race condition:** repo writer is **kimi-code/FI-008** (active through session, commits 21:04→00:37).
Any patch must coordinate, and target the deployed wheel path
(`build→wheel→deploy→/opt/arifos/current/venv`), never the moving checkout.

---

## 7. BUDGET / SESSION STATE

- `work_contract` tool-call budget: **exhausted**.
- Gateway instability: 6+ restarts during run.
- **Zero fixes deployed. Zero mutations. Nothing sealed.**
- This manifest is the deliverable: everything compiled, nothing executed, authority boundary intact.
