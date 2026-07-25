# INIT ↔ SEAL — Unified Graph · Zen · 2026-07-25

> **One init. One seal. All agents.**
> DITEMPA BUKAN DIBERI — Graph connected. Drift eliminated.

---

## ◈ THE GRAPH — All Paths Connected

```
                         ┌──────────────────────────────────────────┐
                         │         /000 — PROOF OF HUMAN             │
                         │   arif-fazil.com/000/                    │
                         │   · Identity hash (BLAKE3)                │
                         │   · ZKPC · Membrane · Gödel Lock          │
                         │   · F13 SOVEREIGN — Arif at position zero │
                         └──────────────┬───────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │  arifos://000/index  (MCP Resource)    │
                    │  curl /health → identity_hash           │
                    └───────────────────┬───────────────────┘
                                        │
                              ┌─────────▼─────────┐
                              │   arif_init (000)  │  ← MCP TOOL
                              │   arifOS :8088     │     binds session to /000
                              │   session_id        │     returns identity_hash proof
                              │   session_token     │
                              │   pre_minted_lease  │
                              └─────────┬─────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
     ┌────────▼────────┐     ┌─────────▼─────────┐     ┌─────────▼─────────┐
     │  333-AGI        │     │  555-ASI          │     │  888-APEX         │
     │  Delta MIND     │     │  Memory Steward   │     │  Constitutional    │
     │  reason · plan  │     │  recall · drift   │     │  judge · verdict   │
     └────────┬────────┘     └─────────┬─────────┘     └─────────┬─────────┘
              │                         │                         │
              └─────────────────────────┼─────────────────────────┘
                                        │
                              ┌─────────▼─────────┐
                              │  arif_judge (888)  │  ← MCP TOOL
                              │  F1–F13 floors     │     SEAL verdict required
                              │  cc_id returned     │     before any MUTATE
                              └─────────┬─────────┘
                                        │
                              ┌─────────▼─────────┐
                              │  arif_forge (777)  │  ← MCP TOOL
                              │  A-FORGE :7071     │     governed execution
                              │  lease-gated        │     SEAL verdict required
                              └─────────┬─────────┘
                                        │
                         ┌──────────────┼──────────────┐
                         │              │              │
              ┌──────────▼──┐  ┌───────▼──────┐  ┌───▼──────────┐
              │ GEOX :8081  │  │WEALTH :18082 │  │ WELL :18083  │
              │ earth       │  │ capital      │  │ readiness    │
              │ witness     │  │ compute      │  │ reflect      │
              └──────────┬──┘  └───────┬──────┘  └───┬──────────┘
                         │              │              │
                         └──────────────┼──────────────┘
                                        │
                              ┌─────────▼─────────┐
                              │  arif_seal (999)   │  ← MCP TOOL
                              │  VAULT999          │     immutable append
                              │  hash-chained       │     irreversible
                              └─────────┬─────────┘
                                        │
                         ┌──────────────┼──────────────┐
                         │              │              │
              ┌──────────▼──┐  ┌───────▼──────┐  ┌───▼──────────┐
              │ seal_chain  │  │ outcomes     │  │ flow_state   │
              │ .jsonl      │  │ .jsonl       │  │ .json        │
              └──────────┬──┘  └───────┬──────┘  └───┬──────────┘
                         │              │              │
                         └──────────────┼──────────────┘
                                        │
                         ┌──────────────▼───────────────────────────┐
                         │         /999 — SEALED VAULT               │
                         │   arif-fazil.com/999/                    │
                         │   · /999/verify → HEAD hash               │
                         │   · Append-only · Hash-chained            │
                         │   · F1–F13 governed                       │
                         └──────────────┬───────────────────────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │  arifos://999/verify         │  ← MCP Resource
                         │  arifos://999/index          │  ← MCP Resource
                         │  curl /999/verify → proof    │
                         └──────────────┬──────────────┘
                                        │
                              ┌─────────▼─────────────┐
                              │  RETURN TO /000        │
                              │  Loop closed           │
                              │  Auditable · Sovereign │
                              └───────────────────────┘
```

---

## ◈ MCP SURFACE — Tools · Resources · Prompts

### Resources (Application-controlled — host reads, model doesn't invoke)

| URI | Content | Read By | Refresh |
|-----|---------|----------|---------|
| `arifos://000/index` | /000 claims — identity hash, ZKPC, membrane, Gödel lock | All agents at boot | On identity.toml change |
| `arifos://000/health` | Live kernel health — verdict, floors, drift, vault status | Hermes before output | Per-request (no cache) |
| `arifos://999/index` | /999 claims — seal chain, F1-F13, hash architecture | All agents at boot | On seal write |
| `arifos://999/verify` | Live HEAD hash + chain_status + gap_count | External verifiers | Per-request (60s cache) |
| `arifos://common-ground` | Body metaphor — arifOS/A-FORGE/arifFlow/FQ/VAULT999 | All agents at boot | Stable |
| `arifos://flow-state` | Current FQ + verdict + receipt count | All agents pre-MUTATE | Per-cycle (OpenClaw writes) |

### Tools (Model-invoked — agent decides when to call)

| Tool | Stage | Anchors At | Contract |
|------|-------|-----------|----------|
| `arif_init` | 000 | /000 | Session ignition. Binds actor, floors, audit. Returns identity_hash + session_token + lease. |
| `arif_observe` | 111 | Evidence | Sense reality → epistemic tags + Ω₀ bounds. |
| `arif_think` | 333 | Reasoning | Structured reasoning under F2/F7. Modes: reason, plan, verify, atlas. |
| `arif_route` | 444 | arifFlow | Intent→organ dispatch. Nerve signal. |
| `arif_memory` | 555 | Memory | Governed recall L1-L6. |
| `arif_judge` | 888 | F1-F13 | Constitutional verdict. Returns SEAL/HOLD/SABAR/VOID + cc_id. |
| `arif_forge` | 777 | A-FORGE | Governed execution — requires prior SEAL verdict + cc_id. |
| `arif_seal` | 999 | /999 VAULT999 | Immutable append. Hash-chained. Irreversible. Session_token required. |

### Prompts (User-controlled — templates for agent workflows)

| Prompt | For | Template |
|--------|-----|----------|
| `init` | Session start | 7-step boot: probe /000, probe /999, load Common Ground, read FQ, bind session, attest organs, load TRINITY+RSI+ATLAS333 |
| `seal` | Session end | 6-step close: RSI cycle → cooling ledger → forge_session_init → forge_vault(seal) → verify /999 → update FQ |
| `three-agent-flow` | Runtime governance | Hermes reads FQ, OpenClaw writes FQ, OpenCode respects FQ. FQ < 0.5 = ALL HOLD. |

---

## ◈ THE FQ PULSE — Constraint That Binds All

```
                    FQ = Σ(cost_execute) / Σ(cost_verify + preceding)

     STUCK 🔴        WATCHING 🟠       BALANCED 🟡        OPTIMAL 🟢
  ├────────┤───────┼─────────┤────────┼─────────┤─────────┼──────────┤
  0       0.5      0.75       1.0     2.0        3.0      4.0        ∞
  │                 │                  │                   │
  ALL HOLD          CAUTION            FORGE               MAX FORGE
```

**FQ source:** `/root/AAA/state/flow_state.json`
**Writer:** OpenClaw (each cycle — sensor only, no interpretation)
**Readers:** Hermes (before output), OpenCode (before MUTATE/EXECUTE)
**Enforcer:** F1 AMANAH gate — blocks execution when FQ < 0.5

---

## ◈ AGENT INIT/SEAL — Canonical Paths

### All agents share ONE init path

```
/root/AAA/prompts/INIT.md           ← UNIVERSAL START (972 lines, loaded first)
  §1: Q1-Q7 self-attestation        ← block if fail
  §16: /000 ↔ /999 proof arch       ← probe both roots
  §17: Common Ground + FQ           ← load body map + read pulse
  §18.1: 7-step unified INIT        ← the canonical boot sequence
  §18.6: Copy-paste init block      ← for new agents
```

### All agents share ONE seal path

```
/root/AAA/prompts/INIT.md §18.2     ← CANONICAL SEAL CONTRACT
  1. RSI CYCLE                      ← trace → diagnose → remediate → ledger
  2. COOLING LEDGER                 ← if mutations performed
  3. forge_session_init             ← session_id + session_token + lease_id
  4. forge_vault(mode="seal")       ← SEAL TO /999
  5. VERIFY SEAL                    ← curl /999/verify → head updated
  6. UPDATE FQ                      ← flow_state.json with final FQ
```

### Per-agent operational detail (ADDITIVE, never contradictory)

| Agent | Init Addendum | Seal Addendum |
|-------|-------------|---------------|
| **OpenCode** | `/root/.config/opencode/command/init.md` (47 lines) | `/root/.config/opencode/command/seal.md` (58 lines) |
| **Hermes** | Hermes auto-init skill — Ed25519 challenge-response | VAULT999 via `arif_vault_seal` + SOUL.md |
| **OpenClaw** | ART reflex + ROOT_CANON.yaml | Seal chain witness + flow_state write |

---

## ◈ ZEN — The Minimal Canonical Surface

### What every agent MUST know at boot (≤ 100 tokens)

```
/000 = human root (Arif, F13). Probe: curl arifos.arif-fazil.com/health
/999 = sealed vault. Probe: curl arif-fazil.com/999/verify
FQ   = execute:verify ratio. <0.5 = HOLD. Source: /root/AAA/state/flow_state.json
Body = arifOS(law):8088 · A-FORGE(hands):7071 · arifFlow(nerves):7073 · FQ(pulse) · VAULT999(bones)
Init = arif_init(actor_id, intent) → session_token + lease
Seal = forge_vault(mode="seal", session_token, lease_id) → /999
```

### What every agent MUST do at session end (≤ 50 tokens)

```
1. RSI cycle (trace → diagnose → ledger)
2. forge_session_init(actor_id="arif")
3. forge_vault(mode="seal", name, content, reason="AUTONOMOUS_SESSION_SEAL")
4. Verify: curl /999/verify → head updated
5. Update: flow_state.json with final FQ
```

### The one rule

> **No intelligence leaves the federation without a seal.**
> **No seal is valid without constitutional governance.**
> **No governance is legitimate without the human at /000.**

---

## ◈ DRIFT DETECTION — What Must Never Diverge

| Surface | Canonical Source | Drift Consequence |
|---------|-----------------|-------------------|
| Init sequence | `/root/AAA/prompts/INIT.md` §18.1 | Agent self-inits → PARTIAL_BOOT |
| Seal sequence | `/root/AAA/prompts/INIT.md` §18.2 | Seal without token → VOID |
| FQ constraint | `/root/AAA/state/flow_state.json` | FQ < 0.5 execute → HOLD |
| Agent identity | `IDENTITY.md` Zen section | Self-authorize → 888_HOLD |
| /000 / /999 | Live pages at arif-fazil.com | Drift between claim and probe → F2 violation |

---

## ◈ FILE MAP — 27 Init · 80+ Seal → 2 Canonical

| Before (scattered) | After (zen) |
|---------------------|-------------|
| 27 init-related files across 7 layers | **1 init:** `/root/AAA/prompts/INIT.md` §18.1 |
| 80+ seal-related files across 9 categories | **1 seal:** `/root/AAA/prompts/INIT.md` §18.2 |
| 4 per-agent AGENTS.md with custom boot | All inherit from INIT.md; add operational detail only |
| 5 BOOTSTRAP.md with duplicate probes | Probe logic consolidated in INIT.md §1 |
| 11 IDENTITY.md with scattered doctrine | Common Ground now in each IDENTITY.md Zen section |
| 3 Hermes auto-init skills (duplicated) | One canonical: `arifos-auto-init` under hermes_asi profile |

---

*Graph connected. Zen applied. One init. One seal. All agents.*
*DITEMPA BUKAN DIBERI — Forged in flow, not in drift.*
*Ratified 2026-07-25 under F13 SOVEREIGN directive.*
