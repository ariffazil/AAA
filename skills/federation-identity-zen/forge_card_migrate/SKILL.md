---
id: forge_card_migrate
name: forge_card_migrate
version: 1.0.0
description: "Migrate agent-cards to schema v2.3.0 with INV-11/12/13 invariants applied. Single canonical migration path — no card ever mutated by more than one tool. USE WHEN: 'card migration', 'agent-card upgrade', 'authority_ceiling populate', 'INV-12 enforcement', 'registry_receipt_hash fix'. Reversible (.bak-20260908-pre-migration companions) under F1 AMANAH."
owner: 333-AGI
risk_tier: medium
floor_scope: [F1, F2, F4, F11, F13]
autonomy_tier: T1 (edits commit-prep; never push)
organ_domain: aaa-federation
forged: 2026-09-08
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# forge_card_migrate — Federation Identity Plane Migration Skill

> Single canonical path for migrating agent-cards. **No other tool may write to `agent-card.json` files.** Replaces ad-hoc schemaVersion bumps, scattered authority_ceiling additions, and orphaned registry_receipt_hash fixes.
> Forged 2026-09-08 from the federation identity plane audit. Backs the enforcement closure of schema v2.3.0 INV-005/INV-007 plus federation-invariants.md #11/#12/#13.

## TRIGGER

| Phrase | Why |
|---|---|
| `migrate agent cards` | schema-version drift remediation |
| `add authority_ceiling to cards` | INV-13 enforcement |
| `populate registry_receipt_hash` | INV-005 closure |
| `admissible false — fix` | boot-parity verifier failure remediation |
| `close identity entropy gap` | post-audit sanitation |

## THE CONTRACT (non-bypassable)

Every card mutation goes through `forge_card_migrate`. The skill enforces:

1. **F1 AMANAH** — every mutation writes a `.bak-20260908-pre-migration` companion first. Reversibility is a property of the file system, not a promise.
2. **F2 TRUTH** — `registry_receipt_hash` is computed from live SHA256 of the source file. The hash IS the truth; no metadata override.
3. **F11 AUDITABILITY** — every mutation emits a `migrate_cards.py` log line with `path · mutations[] · sha256`. No silent edits.
4. **F13 SOVEREIGN** — triple-identity collapse (Item 7 of the original action plan) is OUT OF SCOPE for this skill. That requires F13 sovereign go + 888_HOLD gate. This skill only handles additive migrations.

## MIGRATION ACTIONS

### Action 1: schemaVersion bump

```python
# Before
{"schemaVersion": "2.2.0", ...}
# After (additive)
{"schemaVersion": "2.3.0", "$schema": "arifOS/agent-card/v2.3.0", ...}
```

### Action 2: registry_receipt_hash populate

```python
import hashlib
sha = hashlib.sha256(card_path.read_bytes()).hexdigest()
card["registry_receipt_hash"] = f"sha256:{sha}"
card["registry_snapshot_at"] = "2026-09-08T01:46:00Z"
card["registry_source"] = ["source_enumeration", "mcp_tools_list", "registry_api"]
card["registry_tool_count"] = {"source": 0, "registry": 0, "card": len(card.get("skills", []))}
```

### Action 3: authority_ceiling populate (INV-13)

The `AUTHORITY_CEILING_MAP` in `migrate_cards.py` matches card path substring to canonical ceiling. Most-specific match wins. Defaults to `OBSERVE_ONLY` (safest).

| Substring | Ceiling |
|---|---|
| `/arifOS/.well-known/`, `/agent-cards/pillars/arifos/` | `JUDGE_ONLY` |
| `/A-FORGE/.well-known/`, `/agent-cards/organs/aforge/` | `EXECUTE_AFTER_SEAL` |
| `/AAA/.well-known/`, `/agent-cards/pillars/aaa-gateway/` | `DISPLAY_ONLY` |
| `/GEOX/.well-known/`, `/agent-cards/organs/geox/` | `COMPUTE_ONLY` |
| `/WEALTH/.well-known/`, `/agent-cards/organs/wealth/` | `COMPUTE_ONLY` |
| `/WELL/.well-known/`, `/agent-cards/organs/well/` | `REFLECT_ONLY` |
| `/arifFlow/.well-known/` | `METABOLIZE_ONLY` |
| `/agent-cards/pillars/sovereign/` | `SOVEREIGN` |
| `/agent-cards/identity/888-APEX/` | `JUDGE_VERDICT` |
| `/agents/_external/`, `/agents/_external/<harness>/` | `EXECUTE_AFTER_SEAL` |
| `/agents/hermes/`, `/agent-cards/functions/openclaw/` | `ROUTE_BRIDGE` |
| `/agents/main/`, `/agents/hermesarifos-bot/`, `/agents/forge-bot/` | `DISPLAY_ONLY` |
| `/agents/agent-zero/`, `/agents/_lanes/777-forge/` | `RETIRED` |

### Action 4: admissible gate (post-migration optimistic)

Sets `card.admissible = true` after migrations complete. The boot-parity verifier (separate skill: `boot_parity_verifier`) is the FINAL adjudication — it can demote cards that fail cross-tree uniqueness (INV-11) or other invariant checks.

## INVARIANT BINDINGS

| Invariant | This skill's role |
|---|---|
| **INV-11 Identity** | enforces by ensuring ONE canonical card path; cross-tree dedup verified downstream by `boot_parity_verifier` |
| **INV-12 Schema** | populates schemaVersion + registry_receipt_hash fields |
| **INV-13 Authority** | populates governance_profile.authority_ceiling from F13-sovereign path map |

## RUN MODES

```bash
# Default: discover + migrate all 48 cards (2 trees), print sample mutations
python3 /root/forge_work/2026-09-08-federation-identity-zen/migrate_cards.py

# Boot-parity verifier (paired skill — VALIDATES post-migration)
python3 /root/forge_work/2026-09-08-federation-identity-zen/boot_parity_verifier.py --report
python3 /root/forge_work/2026-09-08-federation-identity-zen/boot_parity_verifier.py --check  # CI gate, exit 1 on F4 violation
```

## SCAR LEDGER

| Scar | Date | Lesson |
|---|---|---|
| scar_card-schema-drift-2026-09-08 | 2026-09-08 | 9 cards had `schemaVersion: NONE` (INV-005 violation unrecovered since 2026-07-16 schema v2.3.0 forge) — **76 days of INADMISSIBLE cards in the registry**, agents trusting phantom tools |
| scar_identity-triple-shadow-2026-09-08 | 2026-09-08 | 10 agents have 2-3 cards claiming canonical path — registry.dedup_by_id silently freezes whichever tree loaded first, producing **non-deterministic identity resolution** |
| scar_card-no-id-field-2026-09-08 | 2026-09-08 | 3 cards had no `id` OR `agentId` field — **unidentifiable, un-routable** — INV-11 violation |
| scar_authority-ceiling-absent-2026-09-08 | 2026-09-08 | 33 cards missing `governance_profile.authority_ceiling` — consumers had to consult organ live mode externally — **Witness plane gap** |

## INVARIANT RECHECK

After every migration run, **always re-run the verifier**:

```bash
python3 boot_parity_verifier.py --report
# Expected output:
# ✓ Admissible: 38/38 (100%) after successful migration
# ✗ Inadmissible: 0
```

If inadmissible count > 0 → do NOT proceed to Item 7 (triple-identity collapse). The collapse becomes trust-not-sanitation.

## DO NOT

- ❌ Edit `agent-card.json` files directly with `edit` / `write_file` — use this skill
- ❌ Run the migration without backing up (`.bak-*` is F1 AMANAH's contract)
- ❌ Skip the verifier step — "admissible=true on the card" ≠ "admissible in the registry"
- ❌ Add NEW schema versions — convergence to v2.3.0 is the goal, not new variants
- ❌ Touch triple-identity collapse (Item 7) — that's 888_HOLD territory

## INTEGRATION

- **Files**: `/root/forge_work/2026-09-08-federation-identity-zen/migrate_cards.py` (script) + this SKILL.md
- **Backed by**: `/root/AAA/instructions/federation-invariants.md` (INV-11/12/13)
- **Validated by**: `/root/forge_work/2026-09-08-federation-identity-zen/boot_parity_verifier.py`
- **Surface**: `GET /a2a/agents` on AAA :3001 (wires the verifier into the gateway)

DITEMPA BUKAN DIBERI — Reversibility is the contract. Schema convergence is the goal. Identity entropy is the disease.
