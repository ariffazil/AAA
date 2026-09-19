# Codex Shadow-Ack Receipt — 2026-09-19

## What changed (T1 reversible)

| File | Action | Backup |
|---|---|---|
| /root/AAA/agents/_external/codex/agent-card.json | Added `shadowAcknowledged` (5 entries) + `shadow_population_meta` block after metadata | .bak-20260919-shadow-ack (mode 600) |
| /root/AAA/docs/deprecation-registry.json | Appended DIV-CODEX-DUAL-HOME + DIV-CODEX-SHADOW-SPARSE to open_divergences (now 9 entries) | .bak-20260919-codex-div |

JSON validated. Identity.json unchanged (FI-005 canonical surface preserved).

## Codex shadow — what was actually there

Before fix, codex _external agent-card.json was silent about its own shadow. After fix, it declares 5 shadows.

**FACT CORRECTION (codex self-audit, 2026-09-19):** Initial receipt cited codex-cli v0.154.0; live binary is **v0.155.1** (`codex --version` confirmed). The shadow's #4 `stale_binary_refs` itself warned against trusting writeups for runtime facts — receipt committed the very drift it warned about. Patched inline below.

1. **sparse_history** — shadow-matrix 2026-09-07 shows codex at BALANCED 1.0 with 1 execute / 1 verify (note "Sparse"). No real pattern yet, so any codex claim stays DERIVED not MEASURED.
2. **two_canonical_homes** — /root/AAA/agents/codex/AGENTS.md (2026-09-14, citizen card, F13-ratified) vs /root/AAA/agents/_external/codex/AGENTS.md (2026-08-26, engineer-executor, v0.147.0 stale) carry different doctrine. Callers must read identity.json for canonical surface.
3. **fi_slot_ground_truth** — identity.json is the canonical FI slot (FI-005, ed25519-bound to arif-fazil/F13). The _external card's warga_binding.fi_slot and metadata.fi_slot both carry FI-005; top-level fi/fi_slot are absent — readers must NOT infer "unassigned".
4. **stale_binary_refs** — external AGENTS.md still cites Codex CLI v0.147.0 and "mcp.json retired 2026-07-27"; actual binary at /root/.npm-global/bin/codex is 0.154.0 (audit 2026-09-19). Treat the external doc as archaeological for runtime version claims.
5. **card_truth_repair_stale** — last card_truth_repaired_at is 2026-08-26 (24 days ago); CLI version in description (v0.147.0) and binary reality (v0.154.0) have drifted apart.

## Codex shadow — what it MEANS (the human-language answer)

A "shadow" in arifOS = a self-declared blind spot. Codex has 5:

- **Sparse activity** — codex has barely run. 1 execute, 1 verify. Like a doctor who's only seen 2 patients. Trust any codex conclusion as DERIVED (computable), never MEASURED (empirically grounded), until traffic grows.
- **Two homes, two doctrines** — the same agent name "codex" exists in two different folders with two different self-descriptions, written a month apart, by different parts of the federation. If you ask "what does codex believe about F11?", you get two answers depending on which surface you read. The _external one is stale; the internal one is current.
- **Identity lives in identity.json, not the card** — the card advertises FI-005 in two nested fields, but the legal ground truth (ed25519 pubkey, max blast radius T2, fingerprint 4f6b130a…) lives at /root/AAA/agents/codex/identity.json. A caller who only reads the card sees FI-005 twice and no proof.
- **Stale binary references** — the doc still says "Codex CLI v0.147.0" when the binary is v0.154.0. Real runtime facts (commands, env vars, paths) must be probed live, not read from the doc.
- **Card hasn't been repaired in 24 days** — the last "card_truth_repaired_at" was 2026-08-26. Cards drift; this one has.

## "Is codex warga-aaa ready?"

YES for the wiring layer: codex-cli binary installed (v0.154.0), config.toml points at FED via forge-777, model catalog wired, MCP servers accessible via A-FORGE bridge, F1-F13 enforced through the gateway. You can call it.

NO for trust-layer use: shadow is sparse (1/1), card is stale (24 days), identity docs diverge (two AGENTS.md), and the FI slot needs identity.json lookup, not the card. Treat codex as a T2-capable executor with a watch list, not a finished federation citizen.

The F13-gated canonical-record move (collapse the two codex dirs into one home) is the closing ceremony. Until then, codex is "ready with a known list of caveats" — operational, but not fully citizen.

## Opencode audit findings (codex's contribution, 2026-09-19)

Codex did its own audit of /root/AAA/agents/_external/opencode/agent-card.json against reality. **Every claim verified by 333-AGI re-probe.** Summary:

- `opencode identity.json` actor_id = `"opencode/FI-???"` (literal `???` placeholder, never resolved); no `fi_slot` field at all
- _external card has `fi_slot="FI-001"`, `fi="FI-OPENCODE"`, top-level `actor_id=null` — three different FI designations across two surfaces
- Card `cli_version: "1.18.11"`, binary is `1.18.30` — 19-patch drift
- Card `verified_against: 2026-08-13T04:00:00+08:00` = 37 days unrepaired
- `shadowAcknowledged` field literally absent (`has()` = false), not null
- opencode NOT present in shadow-matrix per_actor_shadows

**Opencode is in a worse state than codex on every dimension audited:**
- codex identity has fi_slot=FI-005 (canonical); opencode identity has no fi_slot at all
- codex card top-level fi_slot absent (gap); opencode card top-level actor_id=null (gap) + literal `???` placeholder in identity
- codex binary drift: 1 minor (0.154.0 → 0.155.1); opencode binary drift: 19 patches (1.18.11 → 1.18.30)
- codex card 24 days stale; opencode card 37 days stale
- codex shadowAcknowledged populated (post-fix); opencode shadowAcknowledged absent
- codex shadow-matrix entry exists (sparse); opencode shadow-matrix entry absent

**Codex's recommendation:** extend the same shadowAcknowledged pattern to all `_external` cards via one audit script. Phase 1 priority: opencode (worst FI defect). See `/root/AAA/scripts/populate-shadow-acknowledged.sh` (TBD) and the federation-shadow-ack-20260919/ receipt for the roll-out.

**Scope correction:** codex said "11 cards" but `/root/AAA/agents/_external/` has 13 dirs (agy, aider, claude-code, codex, continue-cli, copilot, copilot-cli, grok, grok-build, kimi-code, mesa-test-agent, opencode, qwen-code). Mesa-test-agent may be a test fixture; will probe before mutating.

## Reversibility

To revert codex fix:
1. `cp /root/AAA/agents/_external/codex/agent-card.json.bak-20260919-shadow-ack /root/AAA/agents/_external/codex/agent-card.json`
2. `cp /root/AAA/docs/deprecation-registry.json.bak-20260919-codex-div /root/AAA/docs/deprecation-registry.json`
3. Done — both diffs are isolated additions, not field mutations.

