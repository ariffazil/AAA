---
name: federation-agent-card-ops
description: "Operate the AAA agent-card registry — the 3-layer identity geometry (IDENTITY/HARNESS/BINDING), the identity-vs-runtime-provider split (WHO vs WHICH engine), and CIV33 registry mechanics. Use when adding/removing/compressing agent-card layers, wiring a new harness (opencode, claude-code, grok...), classifying cards, diagnosing unclassified/drift cards, or when Arif asks how federation identity SHOULD be structured."
tags: [agent-card, identity, registry, aaa, harness, geometry, civ33]
---

# Federation Agent-Card Ops

> **CORRECTION 2026-10-25 (verified against `agent-card-registry.js` + live load):**
> the canonical identity store is **`/root/AAA/agent-cards/`** (CIV-33 tree). The loader scans
> three roots in order — `a2a-server/agent-cards/` (legacy, 37 cards) → `agent-cards/` (CIV-33,
> 19 refreshed) → `agents/` (warga, 35) — and later scans **refresh** same-id entries, so the
> CIV-33 card wins over the legacy copy. `a2a-server/agent-cards/` is the **legacy scan root**,
> not the canonical store; the text below that inverts this is retained for audit only.
> Live evidence: 91 files loaded → 57 unique cards (binding 32 / harness 15 / identity 6 /
> retired 2 / unclassified 2). Canon: `canon/AGENT-REGISTRY-ALIGNMENT-2026-10-25.md` §4 D2.
>
> *Historical text (pre-correction):* "The AAA agent-card registry (`/root/AAA/a2a-server/agent-cards/`) is the canonical identity store for every federation agent. `agent-cards/` at the AAA root is **LEGACY** — extensions/functions only."

Registry loader: `/root/AAA/a2a-server/agent-card-registry.js` (loaded by `server.js`, served via A2A).

## The 3-layer geometry (ratified 2026-08-09)

Arif compressed the original 7-layer tree down to **three layers only** — do not reintroduce more:

```
L1 IDENTITY  ◄── who you are (sealed, F13)
     333-AGI · 555-ASI · 888-APEX   (+ species genome weights)

L2 HARNESS   ◄── which engine runs you (registered, swap-able)
     opencode FI-001 (PRIMARY) · claude-code 002 · kimi 003 · codex 004 ·
     copilot 005 · aider 006 · gemini 007 · grok 008 · antigravity 009 ·
     continue 010 · qwen 011 · openclaw (gateway)

L3 BINDING   ◄── what the identity attaches to (everything else)
     forge/* (FI tiers) + organs/* + roles/* + functions/* + extensions/* + pillars/*
```

CIV33_LAYERS map in the registry: `identity → 'identity'`, `harnesses → 'harness'`, and `forge/functions/roles/organs/extensions/pillars → 'binding'`. `_retired → 'retired'`.

## Identity contract vs runtime provider contract (the split)

| Contract | WHO (identity) | WHICH (engine) |
|---|---|---|
| Fields | id, bound_to, class, species, authority_boundary, skills | primary_model, fallback, baseURL, apiKey, order |
| Governed by | Constitution F1–F13 | Ops: quota/health/cost |
| Changes | Rare, F13 only | Daily |
| Lives in | agent-cards/ (sealed) | federation-models.json + litellm-config.yaml (mutable) |

Evidence the split is by design: agent cards carry `model` AND `bound_to` as separate fields; `principal_agent.principle_origin` = "Underlying LLM provider"; opencode card has `replaces: [codex, claude-code]` (harness swaps, identity stays); the 9-ATLAS tensor makes harness the replaceable WHERE dimension.

**Audit line:** a spawned agent zen-ing FED must touch runtime provider contracts ONLY. agent-cards / bound_to / class / species must stay untouched. Verify with `find /root/AAA/a2a-server/agent-cards -type f -newermt '<start-time>'`.

## Registry mechanics — pitfalls (all hit live 2026-08-09)

1. **Map keyed by agentId, LAST WRITE WINS.** Registry scans three roots in order: `a2a-server/agent-cards/` (legacy) → `/root/AAA/agent-cards/` (CIV-33) → `/root/AAA/agents/` (warga). The warga scan runs LAST and overwrites same-id cards — and warga paths don't match the `/agent-cards/` regex, so civ_layer became null → mass "unclassified". **Fix (in place):** in `register()`, never downgrade a classified card to unclassified: if existing card has civ_layer and new one doesn't, carry the existing layer forward.
2. **CIV layer detection is sourcePath-regex based:** `sourcePath.match(/\/agent-cards\/([^/]+)\//)`. Cards NOT under an agent-cards/ path (warga `agents/` tree) get civ_layer null unless the guard above preserves it. Test cards, retired cards, and persona-only cards (agy, mesa-test-agent, 777-forge RETIRED, trading-companion, hermes bare card, arifOS_bot, PROSPECT) legitimately stay unclassified — that's not a bug, don't chase it.
3. **Verify with the registry API, not server.js routes.** `node -e "const {AgentCardRegistry}=require('./a2a-server/agent-card-registry'); ...getStats()/getByLayer()"` is authoritative. The A2A HTTP surface (`/a2a/discover`) is NOT the registry: `agent/getCard` returns the gateway's own card, and `agents/discover` may return 0 — the gateway pattern hides the internal registry.
4. **After any CIV33_LAYERS patch:** restart `aaa-a2a` (T2, reversible — backup the .js first), then re-run getStats to confirm layer distribution.

## Arif's blueprint-first workflow (2026-08-09 lesson)

When Arif asks "what should X have" / "show me the geometry":
- **Show the target-state blueprint/diagram FIRST. Do NOT implement before the shape is approved.** He rejected an already-applied patch with "Nope. Show me how AAA SHOULD BE" — the deliverable was the geometry, not the edit.
- **Compress aggressively.** He iterated 7 → 4 → 3 layers in three messages ("I want three only"). Fewer layers = better. Every layer must earn its existence; when in doubt merge into BINDING.
- **"Serabut" = too dense.** Answer with the compact table/diagram, then offer the cleanup as an option — don't bury the answer in caveats.
- Keep provider routing OUT of AAA identity layers: FED config is operational, not a card layer.

## FI slot drift remediation & canonical signing (2026-08-11 lesson)

This is the most common drift pattern in the harness layer (L2). When Arif says "fix all and make it SOT, no chaos", this is the playbook.

### Canonical SOT — read this FIRST, before touching anything

```yaml
# /root/AAA/registries/forge_instruments.yaml
version: 1
instruments:
  - id: FI-001
    name: OpenCode
  - id: FI-002
    name: Claude Code
  # ... up to FI-008 (canonical slots)
```

Only slots FI-001 through FI-008 are currently in SOT. Anything else (FI-009, FI-010, FI-011) is **OUT_OF_SOT** by definition — it didn't exist when the SOT was forged.

### Authoritative fields (the "what's real" rule)

| Field | Status | Use |
|---|---|---|
| `fi_slot` | ✅ AUTHORITATIVE | Routing, registry lookups |
| `capabilities.forge_tier` | ✅ AUTHORITATIVE | Tier permissions |
| `tier` | ⚠️ LEGACY | Preserved for audit; DO NOT use for routing |

The `tier` field is a historical relic from before the `fi_slot`+`forge_tier` pair was standardised. Treat `tier` as a read-only archive — always patch `fi_slot` and `forge_tier` instead, even if `tier` shows the wrong value. Mention legacy `tier` in the patch report so the user knows it's preserved.

### Status taxonomy (when a card has no clean SOT slot)

| Status | When | Required fields |
|---|---|---|
| `ACTIVE` | Canonical SOT slot, current usage | (no extra fields) |
| `RETIRED` | Slot was reassigned to a different harness | `retired_reason`, `retired_at`, `replaced_by` |
| `RETIRED_DUPLICATE` | Duplicate card kept for backward compat | `retired_reason`, `replaced_by` |
| `OUT_OF_SOT` | No assigned slot in current SOT | `sot_note`, `drift` (the old slot fields) |
| `EDGE` | Not a Forge Instrument (e.g., openclaw gateway) | `sot_note` |

### The signing tool — `sign_agent_card.py`

```bash
# Sign one card with did:arif:aaa
python3 /root/AAA/auth/sign_agent_card.py <card.json>

# Verify a signature
python3 /root/AAA/auth/sign_agent_card.py --verify <card.json>

# Verify the whole registry
python3 /root/AAA/auth/sign_agent_card.py --verify-all
```

Key facts:
- Uses Ed25519 from `/root/AAA/auth/keys/aaa_private.key`
- Signer DID is `did:arif:aaa` (hardcoded in script — AAA gateway is the issuer)
- Re-signing is safe: script deletes the old `signatures` array before re-canonicalising
- Verification checks against `/root/AAA/artifacts/sovereign-did/did_registry.yaml` (NOT against the public key in `/root/AAA/IDENTITY/keys/`)
- After re-signing, **always run `--verify`** before declaring done — stale signatures (e.g., from a different key version) will fail with "Signature was forged or corrupt"

### Playbook when Arif says "Fix all and make it SOT"

1. **Probe the registry state.** `ls /root/AAA/a2a-server/agent-cards/harnesses/*.json` and `find /root/AAA/agents/_external -name agent-card.json`. Build the matrix: fi_slot, forge_tier, tier per file.
2. **Diff against SOT.** `python3 -c "import yaml; print([i['id']+':'+i['name'] for i in yaml.safe_load(open('/root/AAA/registries/forge_instruments.yaml'))['instruments']])"`.
3. **Classify each drift** (fi_slot/forge_tier mismatch, missing field, prose-string slot, slot collision, retired-but-still-active).
4. **Patch in a single script** (e.g., `/tmp/fix_slot_drift.py`) — easier to roll back than scattered edits.
5. **Sign everything that changed.** Even files that already have a valid signature: re-signing guarantees a single canonical `created` timestamp per batch.
6. **Full verification sweep** with `find ... | xargs python3 /root/AAA/auth/sign_agent_card.py --verify`. Target: `PASS: N | FAIL: 0`.
7. **Report with the alignment matrix table** — show each file's fi_slot, forge_tier, tier, status. Arif wants to see the table.

### Arif's "no chaos no contradictions" rule

- Don't introduce new terminology mid-patch (e.g., "FI-001a"). Stay strictly within the existing slot namespace.
- Don't change `tier` if `fi_slot`+`forge_tier` are correct — even if `tier` looks "wrong" historically.
- Don't delete deprecated files silently. Mark them RETIRED with `replaced_by` pointer.
- Don't sign out-of-SOT cards without explicit status annotation.

## Support files

- `references/three-layer-geometry-2026-08-09.md` — the 7→4→3 compression transcript, CIV33_LAYERS before/after, live layer distribution (identity 3 / harness 12 / binding 16 / unclassified 7), and the exact register() guard patch.
- `references/auditing-spawned-build-agents.md` — 6-step audit for a spawned agent's "runtime-only" change table (hash-snapshot baseline, repo-vs-live config path trap, hardcoded-secret scan, identity mtime sweep, doctrine-inversion flag, SOT-vs-live drift), plus the HAProxy 503 root-cause pattern (`/health` vs `/health/liveliness`, redacted health-check key).
- `references/fi-slot-drift-remediation.md` — full transcript of the 2026-08-11 9-card slot drift remediation (aider/grok-build collision, codex tier=FI-004, antigravity tier=FI-009, mesa-test-agent prose string "FI-009 (next slot after FI-008)", continue-cli/gemini-cli out-of-SOT) + the canonical patch script template + the verification matrix.
- `references/i-arif-identity-refactor-2026-08-12.md` — the i-ARIF identity layer refactor: promoting a non_component into a real IDENTITY class organ, updating call_map/STATE/organs/litellm-config, the mirrored-litellm-chain pattern, and the 6-layer stack as implemented.
- `references/actor-naming-trinity-bug-2026-08-12.md` — the **actor naming trinity bug**: three different naming forms for the same actor across registry/exemption-dict/hook (`qwen-code-fi003` / `qwen-code` / `qwen-code/FI-003`) → canonicalization returns None → fallthrough to GUEST. Contains the 4-step diagnostic recipe, the three-patch fix (registry / CANONICAL_ACTORS / settings.json), the symmetry rule (QWEN/KIMI/CODEX uppercase together), the duplicate-key pitfall (`codex` lowercase + `CODEX` uppercase — Python silently keeps the first), and the commit pipeline that locks the fix against kernel reloads. Run this recipe on any session that returns GUEST despite Ed25519 exemption being in place.

## Promoting non_components to real organs

The `non_components:` section in `/root/AAA/federation/organs.yaml` lists entities that are explicitly NOT runtime organs. When an entity gets promoted (e.g., i-arif from "product_brand" to "IDENTITY class organ"), you MUST:

1. **Probe non_components FIRST.** `grep "id: <name>" /root/AAA/federation/organs.yaml`. If it's listed there, it was intentionally excluded.
2. **Move, don't delete.** Remove from `non_components:` BUT leave a tombstone entry with reason `PROMOTED_TO_ORGAN — refactored <date> per <directive>`. This preserves the audit trail.
3. **Add as a real component** with appropriate `class:` and `authority_ceiling:`.
4. **Register in call_map.yaml, STATE.yaml, and litellm-config.yaml** — organs.yaml alone is not sufficient.

**Pitfall:** Adding an organ to `components:` without checking `non_components:` creates a hidden contradiction — something listed as both "not an organ" and "an organ." grep both sections before declaring done.

## Mirrored litellm chain (new agent, same providers)

When a new agent shares the same model chain as an existing agent:

1. `grep -n 'model_name: <canonical_agent>' /root/A-FORGE/litellm-config.yaml` to find all chain entries.
2. Duplicate every entry block — same providers, same order weights, same api_base/api_key.
3. Replace `model_name` with the new agent's name. Update notes to reflect new agent.
4. Add fallback in `router_settings.fallbacks` pointing new agent → canonical agent + others.
5. Validate: `python3 -c "import yaml; yaml.safe_load(open('/root/A-FORGE/litellm-config.yaml'))"`.
6. Verify block count: `grep -c 'model_name: <new_agent>' litellm-config.yaml` should match the canonical agent's count.

The `model_socket` string in `call_map.yaml` is the canonical routing reference even though litellm-config.yaml has the actual chain. Keep them in sync.

## IDENTITY class organs (added 2026-08-12)

When promoting an identity layer agent (i-ARIF), the organ class taxonomy gained a new value:

| Class | Purpose | Examples |
|-------|---------|----------|
| CORE | constitutional authority | arifos, a-forge, aaa, geox, wealth, well |
| METABOLISM | pulse/receipts | arifflow |
| MEMORY | immutable/durable | vault999 |
| EDGE | agent/UI/bridge | hermes, openclaw, opencode, arif-fazil-com |
| SUPPORT | helper daemon | aaa-signing, surface-guard, well-witness |
| DATA | data-plane | postgres, redis, qdrant, nats |
| ADVISORY | recommendation only | fed, flame |
| **IDENTITY** | **sovereign identity core** | **i-arif** |

The IDENTITY class is the only class that is `bound_to: F13-SOVEREIGN` directly. It is the only class where `authority_ceiling: IDENTITY_SOVEREIGN` is used. `receive_only_from:` (instead of `routes_to:`) — identity organs don't dispatch tasks, they receive routed questions from reality bridges.

<!-- SKILL-WITNESS-NOTE (auto, additive-only) -->
Witnessed reality moved this skill's selection to **ROUTE or MERGE**.
Scar signatures: 2026-10-18-git-lane-identity-binding-and-agy-harness
Do not treat this skill as neutral until the signatures are resolved.
<!-- /SKILL-WITNESS-NOTE -->
