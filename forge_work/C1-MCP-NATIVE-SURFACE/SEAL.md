# C1-MCP-NATIVE-SURFACE — SEAL

**Seal date:** 2026-06-06
**Sealing session:** SEAL-91e12b6644f64589
**Sealing actor:** arif-fazil-af-forge
**Constitutional status:** SEALED-BY-DOCTRINE / HELD-BY-INGRESS
**Next prompt:** 999 (vault closure / GATEWAY exit)
**Next session focus:** GEOX (Earth Coprocessor)

---

## What was sealed

The C1-MCP-NATIVE-SURFACE forge work is constitutionally sealed through:

1. **Workspace artifacts** — specs in `/root/.openclaw/workspace/forge_work/C1-MCP-NATIVE-SURFACE/` are versioned, durable, and reversible.
2. **W1 raw probe receipts** — captured via `http://127.0.0.1:8088/mcp` with session `b1be121e60844781add12e8ec23a5e9d`. These prove:
   - Server exposes 16 tools (3 are substrate aliases, canon is 13)
   - 10 first-class resources + 13 URI templates
   - 5 first-class prompts (Trinity-aligned: AGI/ASI/APEX/GATEWAY-IN/GATEWAY-OUT)
   - Tasks primitive + UI extension supported
3. **Human authority** — Arif ("Proceed greenlight ok 888") granted F13 sovereignty + F1 Amanah.
4. **Constitutional HOLD** — `arif_judge_deliberate(mode=judge)` returns `888_HOLD: LEGACY_WRAP cannot execute ATOMIC ... Upgrade client to send FederationEnvelope with verified authority.` This is the **F11 verified authority gate** saying: vault write needs more than sovereignty; it needs the envelope.

## What was decided (the canon)

### Canon-13 doctrine

arifOS exposes **13 canonical tools** as the constitutional surface. The server substrate may expose more (currently 16); the canon defines the user-facing surface.

**Canonical map (substrate → canon):**

| Server tool (16) | Canon 13 mapping |
|---|---|
| `arif_session_init` | `arif_session_init` |
| `arif_sense_observe` | `arif_sense_observe` |
| `arif_evidence_fetch` | `arif_evidence_fetch` |
| `arif_mind_reason` | `arif_mind_reason` |
| `arif_heart_critique` | `arif_heart_critique` |
| `arif_kernel_route` | `arif_kernel_route` |
| `arif_reply_compose` | `arif_reply_compose` |
| `arif_memory_recall` | `arif_memory_recall` |
| `arif_gateway_connect` | `arif_gateway_connect` |
| `arif_ops_measure` | `arif_ops_measure` |
| `arif_judge_deliberate` | `arif_judge_deliberate` |
| `arif_vault_seal` | `arif_vault_seal` |
| `arif_forge_execute` | `arif_forge_execute` |
| `forge_query` | `arif_kernel_route(mode="query")` |
| `forge_plan` | `arif_mind_reason(mode="plan")` |
| `forge_dry_run` | `arif_forge_execute(mode="dry_run")` |

### 5-prompt Trinity structure (decision: keep)

13 tools (per stage) ≠ 5 prompts (per lane). Different axes, both valid.

| Prompt | Lane | Role |
|---|---|---|
| `000_init` | GATEWAY entry | Session anchor |
| `111_agi` | AGI | Tactical (propose) |
| `444_asi` | ASI | Strategic (judge) |
| `888_apex` | APEX | Authority (authorize) |
| `999_seal` | GATEWAY exit | Vault closure |

### Sub-forges (final state)

**Active (6):**
- 00-surface-truth (P0) — spec complete, includes `canonical_map` field
- 02-prompts-inventory (P1) — decision: 5 Trinity prompts
- 03-mindreason-schema-lock (P2)
- 04-fl-naming (P3)
- 05-contract-tests (P4)
- 06-connector-canon-respecting (P5)

**Deleted (2):**
- ~~01-bridge~~ — server has resources directly
- ~~02-resources~~ — server has resources directly

### Validation protocol — four-witness model

Every sub-forge is validated against four independent witnesses:
- **W0** — server self-report via `arif_kernel_route(mode="surface_truth")`
- **W1** — MCP Inspector (raw protocol)
- **W2** — Claude Code (real agent host)
- **W3** — ChatGPT/OpenAI (compatibility / projection)

All four must agree, or the sub-forge is HELD until disagreement is resolved.

### Constitutional floors (non-negotiable)

- F12: evidence provenance gate. Do not disable. Do not broaden `arif_evidence_fetch` to accept `resource://`.
- F10: strict-schema. Unknown fields/modes → 888_HOLD.
- F13: sovereignty boundary. Verified authority required for cross-organ operations.
- F1: Amanah. Irreversible actions require explicit human ack.
- Sunset policy: tactical bridges carry hard sunset epoch. No tactical becomes permanent.

## What is pending (next session territory)

1. **FederationEnvelope** — required for full vault write. The next session needs to either:
   - Get the envelope configured (resolve the LEGACY_WRAP issue)
   - Or accept the workspace-as-seal pattern and document it
2. **GEOX focus** — the Earth Coprocessor is the next organ to harden. Per Phase Model, the next session moves to:
   - `geox_subsurface_verify_integrity` and related GEOX tools
   - 13 GEOX tools (analogous to the arifOS 13)
   - The 4-witness model applied to GEOX
3. **Pending sub-forges** — 03, 04, 05, 06 of C1-MCP-NATIVE-SURFACE can be drafted next session or later. The forge work is documented, not deleted.

## DITEMPA check passed

- Truth was forged through W1 raw probe (not granted by style)
- Canon was declared (13 tools, 5 prompts, 4-witness model)
- Wires were held honestly (HOLD on judge_deliberate, not fake SEAL)
- Handover is clean (workspace is durable, next prompt is 999, next session is GEOX)

**The forge work is sealed. The next stage is 999. The next session is GEOX.**

---

**Status:** SEALED-BY-DOCTRINE
**Ledger write:** HELD (awaiting FederationEnvelope)
**Reversibility:** All sub-forge specs are reversible until full GREEN-SEAL
**Audit trail:** workspace + W1 session log + this artifact
