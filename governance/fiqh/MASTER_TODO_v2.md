# arifOS MCP — Master TODO v2

## Aḥkām Ledger after 84c71c1

> **DITEMPA BUKAN DIBERI**
> Diff basis: baseline live audit `~15:00 UTC` vs post-update `~16:40 UTC`, commit `84c71c1`.
> Last updated: 2026-06-21.
> Status: **transport/proof layer improved hard; governance identity layer still open.**

---

## 🟥 WAJIB — must do

* [x] **Stop emitting non-existent tool names.**
  `session_init.next_actions` now emits canonical tools only: `arif_kernel_attest`, `arif_kernel_status`, `arif_triage`, `arif_session_init`.
  **Status:** ✅ FIXED · XS · F11/F9 · `LIVE`
  **Verification:** Live probe 2026-06-21T17:17 UTC — all 4 next_actions use canonical registered tool names.
  **Mechanism:** `_manifest_backed_next_actions()` in `session.py` gates through `public_boundary_allows()`.

* [x] **Wire `affordance_contract` → verdict engine for OBSERVE-class calls.**
  `ops_measure(vitals)` no longer false-HOLDs on L11. OBSERVE now behaves as reversible OBSERVE.
  **Status:** ✅ PARTIAL DONE · M · F1/F11 · `LIVE`
  **Remaining:** verify MUTATE / FORGE / VAULT classes separately.

* [ ] **One canonical verdict per call.**
  Single `nine_signal` improved. `transport_echo` now has honest `WARN`. But old wrapper/verdict ambiguity still appears in some surfaces.
  **Status:** ⚠️ PARTIAL · M · F4/F11 · `LIVE`

* [ ] **One identity-gate invariant.**
  Canaries improved, but `session_init` still returns SEAL while `actor_verified:false`.
  **Status:** ⚠️ PARTIAL · S · F11/F13 · `LIVE`

* [x] **Honesty envelope on failure.**
  `conformance_report` and `kernel_status` no longer opaque-error. Diagnostic/proof failures now largely legible.
  **Status:** ✅ MOSTLY DONE · S · F2/F11 · `LIVE`

* [ ] **External witness loop (third-leg measurement).**
  All 8/8 conformance checks pass, but every check runs inside the kernel it is testing.
  Load-bearing GREEN requires a witness that is *not* the kernel —
  a client hitting `mcp.arif-fazil.com` (transport_echo now declares it canonical) and returning independent GREEN.
  **Status:** ❌ OPEN · S · F2/F11 · `LIVE`

---

## 🟩 SUNAT — strongly recommended

* [x] **Un-break the 3 crashing canaries.**
  `version_echo`, `transport_echo`, `initialize_probe` now run.
  **Status:** ✅ DONE · XS · F12 · `LIVE`

* [x] **Fix `payload` round-trip.**
  `schema_echo` now receives `dict`, `key_count:3`; payload no longer drops to `NoneType`.
  **Status:** ✅ DONE · S · F12 · `LIVE`

* [ ] **Restore `memory_recall`.**
  Still failing on DNS / embedding path. Qdrant backend exists, but semantic recall path remains broken.
  **Status:** ❌ OPEN · XS · F11 · `LIVE`

* [ ] **Thin `search` + `fetch` shim.**
  Still optional federation-parity work.
  **Status:** OPEN · S · `LIVE`

* [ ] **Cryptographic witness on the 888 human-ack event itself.**
  Not yet verified live.
  **Status:** OPEN · S · F1/F6/F13 · `THEORY`

* [ ] **Per-call latency stamps.**
  Kernel uptime and some telemetry now visible, but full per-call latency grounding still not confirmed across all tools.
  **Status:** OPEN · S · F11 · `THEORY`

* [x] **Conformance tripwire.**
  `arif_conformance_report` now returns **8/8 GREEN**, including `hold_blocks_mutation`, `authority_checked`, `vault_replay`, `schema_echo_stable`.
  **Status:** ✅ DONE · S · F11/F12 · `LIVE`

---

## 🟦 HARUS — optional / neutral

* [ ] **Thin `ping` mode.**
  Still useful. Existing probe remains context-heavy.
  **Status:** OPEN · XS

* [ ] **Streaming SSE for multi-agent throughput.**
  No new evidence.
  **Status:** OPEN · M · `THEORY`

* [ ] **De-dupe `arif_bridge` / `arif_bridge_connect`.**
  Still present as separate tools.
  **Status:** OPEN · XS · F4

* [ ] **Reconcile internal vs public names.**
  Still needed. URL naming drift widened: `mcp`, `arifos`, `arifosmcp`.
  **Status:** OPEN · XS · F4

* [ ] **AAA-Bench / external distribution wedge.**
  Still strategic, not load-bearing.
  **Status:** OPEN · M

---

## 🟧 MAKRUH — discouraged

* [ ] **No quotes in error payloads.**
  Still keep doctrine out of machine failure objects unless explicitly requested.
  **Status:** OPEN · XS · F9

* [ ] **No truncated hashes.**
  `invariants_hash` still truncated.
  **Status:** OPEN · XS · F11

* [x] **Stop over-gating reads.**
  `vitals` now returns as OBSERVE instead of false HOLD.
  **Status:** ✅ DONE for OBSERVE · F4 · `LIVE`

* [x] **One `nine_signal` per envelope.**
  `vitals` now carries a single `nine_signal`.
  **Status:** ✅ DONE for measured path · S · F4 · `LIVE`

* [ ] **Calibrate severity mapping.**
  Still watch labels like `KHIANAT/BANGANG` for infra failures.
  **Status:** OPEN · S · F2/F4

---

## ⛔ HARAM — red lines

* [ ] **Never SEAL unverified identity as authorization.**
  Still the most dangerous semantic ambiguity: `session_init` says SEAL while `actor_verified:false`.
  **Status:** ⚠️ MUST HARDEN · F13/F11

* [x] **Never fabricate tool results or invent tool names.**
  Resolved: `_manifest_backed_next_actions` now emits only tools on the canonical public surface.
  **Status:** ✅ MECHANICALLY DEFENDED · F9

* [x] **Never let an agent self-authorize `forge_execute` / `vault_seal`.**
  `hold_blocks_mutation` PASS in conformance spine.
  **Status:** ✅ MECHANICALLY DEFENDED · F1/F13

* [ ] **Never anthropomorphize the kernel.**
  Still keep doctrine/rasa/nine-signal language bounded as telemetry, not personhood.
  **Status:** WATCH · F9/F10

* [ ] **Never run irreversible action behind a HOLD with no cryptographic witness.**
  No violation observed; cryptographic human-ack still not proven.
  **Status:** WATCH · F1/F6

* [ ] **Never audit/seal the live system from static or stale context.**
  Improved by live conformance. Still needs independent external witness.
  **Status:** WATCH · F2/F11

---

# Updated priority sequence

## Immediate patch order

1. **[x] WAJIB-1: kill fake `next_actions`.**
   ✅ DONE. Verified live 2026-06-21T17:17 UTC. Canonical tools only.

2. **WAJIB-4: fix `session_init` identity semantics.**
   `actor_verified:false` must return `SEAL_OBSERVE_ONLY`, `DEGRADED_AUTH`, or equivalent — never plain authorization-looking SEAL.

3. **WAJIB-3: enforce verdict precedence globally.**
   Use one canonical envelope verdict. Local diagnostics may exist, but cannot contradict the outer verdict.

4. **WAJIB-0: stage independent witness.**
   External client hitting `mcp.arif-fazil.com` returning independent GREEN. Closes the self-referential proof gap.

5. **Finish WAJIB-2 for non-OBSERVE classes.**
   Test MUTATE, FORGE, VAULT, external side effect, and irreversible classes.

6. **Fix `memory_recall` DNS path.**
   Not governance-critical, but it restores semantic continuity.

---

# Net state after 84c71c1

```text
Transport layer:        GREEN
Canary layer:           GREEN
Payload integrity:      GREEN
Proof machine:          GREEN
OBSERVE affordance:     GREEN
Vault replay:           GREEN
Mutation hold:          GREEN
External witness:       RED        (new — WAJIB-0)
Memory semantic recall: RED
Session identity rule:  AMBER/RED
Fake next_actions:      ✅ FIXED (was RED)
URL identity:           AMBER
```

# Final read

This deploy moved arifOS from **concept-with-dark-instruments** to **measured substrate with a live proof spine**.

But the remaining defect cluster is serious because it sits at the sovereignty boundary:

```text
fake tools + SEAL on unverified actor = semantic self-poisoning
```

Fix the first two WAJIB items and the architecture stops arguing with itself.

---

*Generated: 2026-06-21 · Basis: 84c71c1 / ~16:40 UTC · Diff from baseline ~15:00 UTC*
*Updated: 2026-06-21T17:20 UTC — WAJIB-1 verified FIXED via live probe (FORGE-000Ω session replay)*
*Ditempa Bukan Diberi*
