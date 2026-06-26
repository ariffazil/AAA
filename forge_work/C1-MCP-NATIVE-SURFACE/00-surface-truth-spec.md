# 00-surface-truth — `arif_kernel_route(mode="surface_truth")` truth adapter

**Sub-forge of:** C1-MCP-NATIVE-SURFACE
**Priority:** P0 — ship first
**Reversible until:** GREEN-SEAL of full forge C1-MCP-NATIVE-SURFACE
**Spec version:** v2026.06
**Spec author:** arif-fazil-af-forge (session SEAL-91e12b6644f64589)
**Originating signal:** External AI assistant self-correction, 2026-06-06

---

## Problem

External AI assistants that connect to arifOS through lossy connector membranes (e.g., the ChatGPT MCP connector) can overclaim about the system's health. They see a projected tool surface, not the raw MCP universe, and treat the projection as if it were the whole machine.

**Concrete example (2026-06-06):** An external assistant saw the canonical13 tool surface, noted the absence of `prompts/list`, `prompts/get`, `resources/list`, `resources/read` through the connector, and incorrectly inferred that arifOS itself was missing those primitives. The system was healthy; the connector was the shadow.

This is a **structural epistemic risk**. Every future connector that touches arifOS is subject to the same error unless the system exposes a self-orienting truth surface.

## Non-negotiable constraint

The truth surface must be:
- **Honest** — what is, not what we wish was.
- **Machine-readable** — enums, not prose.
- **Verifiable** — pinned to a substrate hash so the response can't be spoofed by a misconfigured connector.
- **Reversible** — if the truth changes, the response changes; no caching across epochs.
- **Process-mandated** — clearly labeled as a call that must happen before any diagnostic judgment.

## Solution

Add a new safe mode `surface_truth` to the existing tool `arif_kernel_route`. The mode:

- Returns a structured truth surface describing what the connector is and is not seeing
- Enumerates known shadow zones explicitly
- Pins the response to an epoch + substrate hash
- Recommends a starter call sequence for new connectors
- Is read-only, side-effect-free, and authority-neutral

## Schema (canonical)

```yaml
tool: arif_kernel_route
new_mode: surface_truth
version: v2026.06

allowed_fields:
  mode:
    type: str
    required: true
    fixed_value: "surface_truth"
  session_id:
    type: str
    required: true
    format: "^SEAL-[a-f0-9]{16}$"
  actor_id:
    type: str
    required: true

safe_modes_for_this_route:
  - surface_truth

dangerous_modes_for_this_route: []

requires_ack_irreversible: false
requires_judge_state_hash: false

response_schema:
  mcp_enabled: bool                    # always true for live arifOS
  canonical_tools: int                 # 13 (constitutional count)
  server_exposed_tools: int            # 16 (W1 raw protocol count)
  tool_surface: str                    # "canonical13"
  canonical_map:                       # NEW: substrate-to-canon mapping
    type: object
    description: "Maps server-side tool names to their canon equivalent"
    example:
      forge_query: "arif_kernel_route(mode='query')"
      forge_plan: "arif_mind_reason(mode='plan')"
      forge_dry_run: "arif_forge_execute(mode='dry_run')"
  prompts_exposure:
    type: enum
    values: [stage_metadata, first_class_mcp, unavailable]
  resources_exposure:
    type: enum
    values: [advertised_metadata, first_class_mcp, unavailable]
  connector_view: str                  # "projected" | "raw"
  raw_mcp_parity: bool                 # false when projected
  epoch_id: str                        # e.g. "epoch-2026.06"
  substrate_sha: str                   # sha256:... of the live build
  known_shadow_zones:
    type: array
    items: str
  consumers_should_call_first: bool    # true
  recommended_sequence:
    type: array
    items: str                         # tool calls in order
  do_not_diagnose_without_calling_first:
    type: array
    items: str
```

## Constitutional doctrine — canon vs substrate

The arifOS canon defines **13 constitutional primitives**. The server substrate may expose more (currently 16) as implementation conveniences. The canon is the authoritative surface; the substrate provides the wiring.

**The 3 server extras collapse into the canon via mode-aliasing:**

- `forge_query` (read-only system introspection) → `arif_kernel_route(mode="query")`
- `forge_plan` (action planning) → `arif_mind_reason(mode="plan")`
- `forge_dry_run` (execution simulation) → `arif_forge_execute(mode="dry_run")`

Each capability lands in its most natural constitutional home. The substrate aliases are not separate tools — they are modes of canon tools, and any consumer of arifOS that wishes to call those capabilities should use the canon paths, not the substrate aliases.

The `canonical_map` field in the surface_truth response makes this explicit and machine-readable.

## Response shape (current truth, 2026-06-06)

```json
{
  "mcp_enabled": true,
  "canonical_tools": 13,
  "server_exposed_tools": 16,
  "tool_surface": "canonical13",
  "canonical_map": {
    "forge_query":   "arif_kernel_route(mode='query')",
    "forge_plan":    "arif_mind_reason(mode='plan')",
    "forge_dry_run": "arif_forge_execute(mode='dry_run')"
  },
  "prompts_exposure": "first_class_mcp",
  "resources_exposure": "first_class_mcp",
  "connector_view": "projected",
  "raw_mcp_parity": false,
  "epoch_id": "epoch-2026.06",
  "substrate_sha": "sha256:c4af53e...",
  "known_shadow_zones": [
    "server exposes 16 tools, canon is 13 (3 extras are mode-aliases of canon tools — see canonical_map)",
    "OpenClaw connector projects 13 (canonical13 branding) and may not advertise the 3 alias modes",
    "ChatGPT/OpenAI connector projects a further subset (tool-calling only)",
    "gateway discover generic = SEAL; targeted/route/relay = HOLD (L11)",
    "arif_judge_deliberate safe modes (explain, compare, history) blocked by LEGACY_WRAP connector bug",
    "arif_mind_reason degrades to HOLD when LLM output is non-dict (parser is strict, F10)"
  ],
  "consumers_should_call_first": true,
  "recommended_sequence": [
    "arif_kernel_route(mode=surface_truth)",
    "arif_session_init(mode=init)"
  ],
  "do_not_diagnose_without_calling_first": [
    "mcp_health",
    "prompts_completeness",
    "resources_completeness",
    "tool_surface_canonicality",
    "federation_organ_health"
  ]
}
```

## Example valid calls

```json
// Standard surface truth probe
{
  "mode": "surface_truth",
  "session_id": "SEAL-91e12b6644f64589",
  "actor_id": "arif-fazil-af-forge"
}
```

## Example rejected calls

```json
// Missing session_id → 888_HOLD (F10)
{
  "mode": "surface_truth",
  "actor_id": "arif-fazil-af-forge"
}
```

```json
// Wrong mode → 888_HOLD (F10)
{
  "mode": "surface_truth_v2",
  "session_id": "SEAL-91e12b6644f64589",
  "actor_id": "arif-fazil-af-forge"
}
```

## Why this works as a class-of-error fix

| Old failure mode | New behavior with surface_truth |
|---|---|
| Assistant sees 13 tools, no prompts/list, concludes "prompts missing" | `prompts_exposure: "stage_metadata"` — explicit, no inference needed |
| Assistant sees one gateway HOLD, generalizes to "gateway broken" | `known_shadow_zones` lists the precise gate logic; no overclaim possible |
| Assistant claims "system is broken" without verifying substrate | `substrate_sha` lets consumer verify they're seeing the live build |
| New connector has no idea where to start | `recommended_sequence` provides a starter recipe |
| Connector falsely diagnoses MCP health | `do_not_diagnose_without_calling_first` makes the rule explicit |

The shadow zones are **declared**, not hidden. The connector can see them, account for them, and stop overclaiming.

## Test cases

| # | Test | Expected |
|---|---|---|
| 1 | Valid call with SEAL-* session | SEAL, returns truth surface |
| 2 | `prompts_exposure` is one of `stage_metadata` / `first_class_mcp` / `unavailable` | enum constraint |
| 3 | `resources_exposure` is one of `advertised_metadata` / `first_class_mcp` / `unavailable` | enum constraint |
| 4 | `substrate_sha` matches known live build hash | verifiable |
| 5 | `known_shadow_zones` is non-empty (current state has 5+ zones) | array length > 0 |
| 6 | `consumers_should_call_first: true` | fixed value |
| 7 | Missing session_id | 888_HOLD (F10) |
| 8 | Wrong mode value | 888_HOLD (F10) |
| 9 | `arif_kernel_route(mode=list)` still returns 13 tools (no regression) | SEAL |
| 10 | `arif_evidence_fetch` F12 boundary unchanged (regression check) | HOLD on resource:// |

## Acceptance criteria

1. All 10 test cases pass.
2. Response shape matches the schema above.
3. `substrate_sha` is verifiable against the live build.
4. `known_shadow_zones` accurately reflects current Reality.
5. `recommended_sequence` is in the correct order (surface_truth first, manifest second, init third — note: init can also be first if a session is needed; documented in test).
6. `do_not_diagnose_without_calling_first` includes the 5 diagnosis categories.
7. `docs/MCP_CONTRACTS.md` updated with the new `surface_truth` mode entry.
8. `forge_work/C1-MCP-NATIVE-SURFACE/MCP_BRIDGE_REGISTRY.json` updated with the new mode entry.

## Rollback plan

Single-mode addition. To rollback:
1. Remove the `surface_truth` mode from `arif_kernel_route` allowlist.
2. Revert the `docs/MCP_CONTRACTS.md` change.
3. Remove the registry entry.

**Zero state change. Zero data migration. No consumer is required to call this mode** — but every consumer that wants to avoid over-claiming SHOULD call it first.

## Sealing

When Arif signs off on this spec:

1. Spec is sealed via `arif_vault_seal` with `ack_irreversible=true` and `judge_state_hash` from prior SEAL judgment.
2. `arif_forge_execute(mode=engineer, plan_id="C1-MCP-NATIVE-SURFACE/00-surface-truth")` lands the code.
3. Test cases run. Acceptance criteria verified.
4. Sub-forge marked SEALED in the forge work manifest.

After 00-surface-truth ships:
- 01-bridge becomes safe to ship (consumers can call `surface_truth` first to know what the bridge is for)
- 02-prompts-resources can land (consumers will see `prompts_exposure` flip from `stage_metadata` → `first_class_mcp`)
- The truth surface becomes the **invariant** that all future work is measured against

---

**Status:** DRAFT — awaiting Arif review and seal.
**Next action:** Update `C1-MCP-NATIVE-SURFACE.md` to include this sub-forge as P0. Generate remaining 4 sub-forge specs (01-05).
