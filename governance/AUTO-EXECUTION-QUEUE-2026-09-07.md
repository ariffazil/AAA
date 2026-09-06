# Auto-Execution Queue — 2026-09-07 (post Phase-0, post ratification)

> Compiled per F13 directive: *"compile all remaining task for auto execution."*
> Order = leverage per joule. Each row: scope · gate · verify. Agents pick from top.

| # | Task | Scope | Gate | Verify |
|---|------|-------|------|--------|
| 1 | **Scar Reflex matcher fix** (B13 audit): `reflex_triggers[]` field on scars, path-token exclusion (`/root`,`forge`,`dist`), logged catch, sync test to production logic, register `scarReflex` in `npm test` list, fix dry-run SEAL/gate label | A-FORGE forgeShell.ts + scar index schema | none (reversible) | benign `ls` no longer GATEs; test green in CI list |
| 2 | **A-FORGE commit bundle**: scar gate files + `fed_aware_middleware.py` (URL fix `/route`, telemetry thread) — mixed-author, note attribution FI-008 vs prior session | git | none | `git status` clean; push with F13-consented policy |
| 3 | **WawaBot shim** (~20 lines): message text + agent_id → `fed_route`; conversation class → explicit `fed-conversational`; then acceptance test (chat→RM0 lane, gambar→vision, tugasan→K3-class, kod→deepseek) | `.hermes/hooks/wawabot-cognitive/` or litellm persona config | coordinate (Azwa's live bot — canary first) | 4/4 acceptance cases route correctly; cost drop observed |
| 4 | **epistemic_profiles SOT add** (FED Phase 1): CORRECTED task-class schema (sovereign-decision / audit-godel / exploratory / student-support) + pre-rank filter slot | `federation-models.json` + `fed_router.py` engine | **F13 one-line confirm on corrected schema** (identity-weight variant rejected) | audit-godel excludes audited provider; freshness filter skips stale probes |
| 5 | **Lane A actor binding**: sign Ed25519 challenge (nonce issued under `SEAL-2d9738fac78145bb`) via localhost:18900 lane → unlocks kernel VAULT999 seals for the ratified doctrine set | sovereign signing lane | identity escalation | `actor_cryptographically_verified=true` on re-init |
| 6 | **Scar consolidation** (B8): unify/index 4 stores (30 live + 105 legacy migration to L4 + 7 wiki + AAA narrative); then 4 scar-wirings (B9, `civ-readiness-witness-2026-09-07`) | A-FORGE `.runtime/scars` + AAA | none | one queryable index; wiring receipts |
| 7 | **Z-residue**: Z3 mesh state artifacts → `AAA/skills/`; Z4 organs.yaml (dedupe `openclaw`, fix dead `.openclaw` path, minimax-media revive-or-tombstone); Z6 `.qwen` overlay refresh; Z9 graphiti probe decision | configs | none (A12 minimax-media = F13 taste call, present options) | mesh-sync dry-run clean; organs.yaml self-consistent |
| 8 | **VERIFICATION-TRACKER 7-day truth pass kickoff** (R1) + WIRE-MANIFEST fill (R2) | governance | none | Day-1 wire capture committed |
| 9 | **RBA Phase 1** T09–T16 (G10 first; counterparty registry G2 organ; G8 multi-KPI) | AAA/A-FORGE | none (shadow) | RBA-PROOF artifacts |
| 10 | **Others' dirty repos**: arifOS (`apex_collapse_trigger.py`), GEOX (2 files) — authors or next session | git | none | clean trees |
| 11 | **i-AZWA**: kernel↔card reconciliation (18 sections ↔ card fields) + Azwa F13 seal gate | AAA cards | F13-Azwa (her lane) | `sealed_at` non-null |
| 12 | **Long arc**: Meaning/Identity Layer (attention-graph §12b Phase 3), FLOW_GRAPH.json (zen Phase 7), APEX.lean sorries, G-score pathology loop | per map R-layer | per map | per map |

*Ratified doctrine set: REFLEX-VS-COURT · FED-EUREKA-DISTILLATION · ZEN-CARD (+ map, unsealed reference). F13 chat directive 2026-09-07. DITEMPA BUKAN DIBERI.*
