# Kimi Spawn Protocol ↔ FederationEnvelope v0.1 Mapping

> **CCC-T-04 (2026-09-18)** — bridge document, no new doctrine
> **From:** `/root/AAA/federation/protocols/kimi_spawn_protocol_v0.1.0.json` (PARTIAL-SEAL+)
> **To:** `/root/AAA/federation/protocols/federation_envelope.yaml` v0.1 (PATCH_READY)

## Field mapping

| Kimi spawn field | FederationEnvelope v0.1 field | Notes |
|---|---|---|
| `archetype` (e.g. `af_forge`) | `agent_id` derivation | `<harness>/<archetype>` naming |
| `spawn_reason` | `judgment_ref` rationale | free-text, evidence-anchored |
| `risk_tier` | `tier` | direct: T1/T2/T3 |
| `expected_entropy_reduction` | `constraints` extension | not in envelope yet — added in v0.2 |
| `parent_session_id` | `session_id` | direct |
| `parent_spawn_id` | `parent_receipt` | direct (spawn_id ↔ receipt_id) |
| (Kimi spawn) | `authority` = archetype_ceiling[archetype] | OBSERVE_ONLY / DRAFT_ONLY / EXECUTE_REVERSIBLE / EXECUTE_AFTER_SEAL |
| (Kimi spawn) | `reversal` = YES (T1), PARTIAL (T2), NO (T3) | fail-closed mapping |
| (Kimi spawn) | `harness` = `kimi` | literal |
| (Kimi spawn) | `transport` = `MCP` | kimi spawns use MCP session |
| (Kimi spawn) | `judgment` = `SEAL` (default for spawn) | only mutate on F13 veto |
| (Kimi spawn) | `envelope_id` = `uuid v4` | mint on emit |
| (Kimi spawn) | `emitted_at` | ISO-8601 UTC at emit time |
| `archetype_confidence_ceiling[archetype]` | not in envelope v0.1 | kept internal; do not leak |

## Gap to close (CCC-T-04b)

Kimi's `aaa-witness-pre.sh` should call a sibling envelope emitter that writes to `/root/.local/share/arifos/kimi_envelope_emits.jsonl` using this mapping. Future work — not part of this Phase 1 actual delta.

## Verdict

Field set is ~85% compatible. Missing: `constraints` enrichment with `expected_entropy_reduction` (defer to v0.2). Connection mechanism: same pattern as Hermes — sibling file, no regression risk.

> **DITEMPA BUKAN DIBERI ⚒️**
> **Path:** `/root/AAA/federation/protocols/kimi-envelope-mapping.md`
> **Status:** PATCH_READY — bridge document
