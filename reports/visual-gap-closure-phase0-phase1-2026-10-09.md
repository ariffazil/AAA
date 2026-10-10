# VISUAL GAP CLOSURE — Phase 0 + Phase 1 Audit Findings

> **Date:** 2026-10-09 (MYT) · **Executor:** HERMES (read-only audit lane, per FEDERATION ROLE SEPARATION) · **Authority:** F13 "go" 2026-10-08/09
> **Scope:** Phase 0 (capability baseline) + Phase 1 (receipt-chain integrity). NO mutations performed. Phases 2-4 held pending these findings, per plan.
> **Labels:** OBS = observed · DER = derived · UNVERIFIED = not probed

---

## PHASE 0 — Claim vs Reality Matrix

| Component | Claimed | Reality (this session) | Class |
|---|---|---|---|
| forge-vss-parser | engine+schema+tests | RUN: fixtures 50/50 PASS, boundary-reject 35/35 PASS, 146ms | **VERIFIED-EXECUTED** (OBS) |
| forge-vss-verifier-suite | verifier+ledger adapter | RUN: ledgers_projected 50/50 PASS | **VERIFIED-EXECUTED** (OBS) |
| compile_physique_prompt.py | prompt densifier | RUN: emits compiled prompt + negative ensemble + 4-unit ControlNet manifest | **VERIFIED-EXECUTED** (OBS) |
| physique_topography.schema.json | contract schema | PRESENT at /root/.hermes/skills/aaa-human-physique-topology/schemas/ | IMPLEMENTED (not end-to-end run) |
| VISION_ORGAN | full organ | 17 files: organ_pipeline, compile_contract, scene-contract.schema, vision-invoke schemas+taxonomy, budget_guard, adapters (qwen_vision, minimax_image01), ledger | IMPLEMENTED (E2E UNVERIFIED) |
| cv2 5.x "LIVE on box" (cv-feature-matching skill) | installed | TRUE on **system python** (/usr/bin/python3, 3.13.7: cv2, torch, numpy, pytest ✅). FALSE on Hermes hermetic python (3.14.7: none). | **SPLIT-ENV TRAP** — agents must use /usr/bin/python3 for CV work (DER) |
| MediaPipe / SAM 2 / DensePose / SMPL-X | doctrine refs | NOT installed (both pythons) | GAP confirmed — P3 benchmark-gated, unchanged |
| mata snapshot | <24h freshness law | Snapshot was STALE (2026-09-19). Fresh pane run 2026-10-08T16:38Z ✅ | OBS |

### MATA live pane 2026-10-08T16:38Z (fresh probe — supersedes compile §2 routing until next probe)
- **LIVE:** gemini (auth, 62 models — gen canary NOT run), minimax-video (Hailuo-2.3, 3/day), minimax-chat (M3 vision-in), bailian-tp (**wan2.7-image(-pro)** = image-gen primary), qwen-indiv, fed (HAProxy→KVM4 litellm), pollinations (keyless T2I fallback)
- **DOWN/DEAD:** mimo-tp-vision **429 quota exhausted** · zai-vision **DEAD:429 insufficient balance** · kimi 401 · dsq-free-vl 403 · comfyui DOWN (no unit on KVM8)
- **Consequence (DER):** the whole zai_vision MCP toolset (8 tools) is currently balance-dead; primary understanding lane right now = MiniMax-M3 chat vision + mimo (until quota reset) + gemini. Image-gen = wan2.7 via bailian, pollinations fallback. Any compile-doc route table must be re-read against `mata_last.json`, not prose.

### Phase 0 test-harness notes
- VSS test files are standalone scripts, NOT pytest-collectable ("no tests ran" under pytest; pass when executed directly). Any CI wiring must invoke `python3 test_*.py` directly or the suite silently no-ops — a false-green risk worth a scar if it ever passes unnoticed.

---

## PHASE 1 — Receipt-Chain Integrity Audit

### Contract (canonical spec)
`/root/arifOS/arifosmcp/runtime/receipt_store.py` (OBS): `Receipt.previous_receipt_hash: str` is a REQUIRED field; `verify_chain` walks the ledger and FAILS when `receipt.previous_receipt_hash != prev_hash`. The canonical arifOS contract IS a continuous hash chain. Question (a)-vs-(b) from the prior turn is settled: **the spec mandates chaining** — this is defect class (a), writer non-conformance, not an undocumented standalone ledger.

### Ledger reality (OBS)
`/var/lib/arifflow/receipts.jsonl`: **138,902 receipts parsed, 0 unparsable**. `previous_receipt_hash` null in **138,896**; chained in **6** (0.004%). Top actors: A-FORGE 66,038 · hermes-asi 20,005 · grok-build 13,694 · a-forge 9,398 (note: actor-id casing split A-FORGE/a-forge = identity hygiene defect, minor).

### Root cause (OBS — located in writer)
`/root/A-FORGE/dist/src/infrastructure/receipts/arifflowClient.js:99`:
```js
previous_receipt_hash: params.parent_receipt_id || null,
```
Two defects in one line:
1. **Pass-through-or-null:** chain link is only written when the CALLER explicitly supplies `parent_receipt_id`. Nearly no caller does → 138,896 nulls.
2. **Semantic mix:** it stores a parent **receipt_id** in a field the verifier compares against a **hash**. Even the 6 "chained" rows may not satisfy `verify_chain` semantics (ID≠hash) — verification of those 6 not performed (UNVERIFIED).

### Smallest backward-compatible repair (PROPOSAL — A-FORGE lane owns execution; HERMES does not mutate)
1. In the writer: when `parent_receipt_id` absent, read the last receipt's hash from the ledger tail and store THAT (true hash, not ID). Genesis row: explicit `GENESIS` sentinel, documented in the spec.
2. Append-only preserved; historical rows NEVER rewritten (F1). The 138,896 nulls remain as-is, annotated by a one-time audit marker file beside the ledger (`chain-audit-2026-10-09.json`): "pre-repair history: unchained by writer defect; ordering recoverable via timestamps, integrity NOT provable."
3. `verify_chain` gets a documented epoch boundary: chain verification applies from the repair-forward genesis; pre-boundary rows verify as `PRE_CHAIN_HISTORY` (not PASS, not FAIL — a third honest state per State-Transition Discipline).
4. Fix actor-id casing normalization at write time.
5. Independent verification: after repair, a non-A-FORGE actor (FRAME or HERMES audit lane) runs ordering + hash-replay on 100 fresh receipts. Verifier substrate ≠ executor (scar-2026-10-01-002).

### Separation ruling (honored)
Ledger repair (Phase 1) and image-pipeline extensions (Phases 2-4) remain SEPARATE mutations with separate receipts, per plan. Phase 2 contact-graph edges will write to the VSS assertion ledger (`vss_assertion_ledger.schema.json`) which is NOT the arifFlow receipts ledger — so Phase 2 is not blocked by the chain defect, only Phase-1-receipt-provenance discipline applies. This unblocks the original sequencing concern.

---

## Routing / next actions
- **Work item → A-FORGE lane:** arifflowClient.js:99 repair per proposal above (authenticated authority required; rollback = revert single line + remove sentinel; no history rewrite).
- **Work item → FED lane:** fed_route rank-1 vision-blind defect (glm-5.3-flash ranked first for fed-multimodal-vision; EMD guard catches it downstream — fix rank ordering upstream). Receipt: fed_route probe 2026-10-08T16:31:49Z.
- **Update → compile doc:** MATA 2026-10-08 pane deltas (zai-vision/mimo vision quota-dead) + cv2 split-env trap + Phase 1 findings.
- **Phases 2-4:** GREEN to proceed once F13 dispatches AGY CLI execution lane (contact-graph extension of forge-vss-parser first, per agreed priority).

*Reality > Everything. Declared ≠ Executable ≠ Verified. No mutation was performed in this audit.*
