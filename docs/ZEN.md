> ⚠️ SUPERSEDED by docs/ZEN99.md (2026-07-17). Read ZEN99.md first.

# ZEN.md — arifOS AAA Single Entry Point

> **Forged 2026-07-15 · Phase 2 of the entropy-reduction refactor (commit `1dd3a79`).**
> **Read this file first if you are a new agent loading this repo cold.**

This file replaces the Gödel loop of "read AGENTS.md, then CLAUDE.md, then CONTEXT.md". It is the **one document** that links to the rest. Every other file is reachable from here.

---

## 1. Identity Stack — read in this order

| Step | File | Why |
|---|---|---|
| 1 | `README.md` | Public-facing SOT — what AAA is, what it isn't, how to run it |
| 2 | `GENESIS/AAA_MANDATE.md` · `GENESIS/TRUTH_MD.md` · `GENESIS/DUAL_LANGUAGE.md` | Three constitutional docs (013/014/015) |
| 3 | `AGENTS.md` | Federation landing, F1-F13 floors, 7-organ map, autonomy tiers |
| 4 | `CLAUDE.md` | AAA-grade agent surface (the 6 planes, governing principle) |
| 5 | `BOOT.md` | How a session starts (state attestation + agent init) |
| 6 | `CONTEXT.md` | Live focus + carry-forward state (today only) |
| 7 | `docs/FEDERATION_COCKPIT.md` | Canonical identity doc (SOT for organ topology) |
| 8 | `docs/architecture/` | Sub-tree: APEX theory, EUREKA six-plane loop, federation maps |
| 9 | `docs/philosophy/` | Sub-tree: FLOORS doctrine, gateways, paradox anchors |
| 10 | `docs/contracts/` | Sub-tree: SEAL authority, peer federation, surface contracts |

**Live read order**: this file → `README.md` → `AGENTS.md` (if you are an agent harness) → `docs/FEDERATION_COCKPIT.md` (if you need topology).

---

## 2. The Three Truths (always current)

- **AAA is the state + cockpit.** It owns display, routing, registries, approval queues. It **does not** judge, execute, or seal. arifOS judges. A-FORGE executes. arifOS also seals.
- **7 organs, 1 sovereign.** `arifOS` · `A-FORGE` · `GEOX` · `WEALTH` · `WELL` · `AAA` · `VAULT999`. Arif (F13) holds the veto. Organs never self-seal.
- **3 constitutional citizens (HEXAGON).** `333-AGI` (Δ MIND) · `555-ASI` (Ω HEART) · `888-APEX` (ΦΙ JUDGE). `A-AUDIT` and `A-ARCHIVE` are **collapsed 2026-07-15** (cross-cutting functions embedded in every organ, validated by 888-APEX). `777-forge` is A-FORGE's lane persona — **not** a 4th identity.

---

## 3. Hard constraints (non-negotiable)

- **F1–F13 enforced by kernel.** Conformance = `0.80 ≤ G ≤ 1.0` and `C_dark < 0.30`.
- **Gödel Lock (active 2026-07-15).** SEAL-bound claims touching `/AGENTS.md`, `/VAULT999/`, `/GENESIS/`, or `/docs/` require external witness signature. AAA cannot self-seal its own irreversible actions.
- **VAULT999 writes only via `arif_seal`** (after `arif_judge` SEAL verdict). Direct writes from outside the kernel verb chain = constitutional violation.
- **Date-stamp tags only.** Format `vYYYY.MM.DD`. Iron Rule. Legacy `v55.*` tags retained in history but never created new.
- **Namespace discipline.** `arif_*` kernel only (9 verbs). `agi_*` / `asi_*` / `apex_*` for the 3 HEXAGON. `forge_*` A-FORGE. `geox_*` / `capital_*` / `well_*` per organ. `aaa_*` gateway.

---

## 4. Live status (probe before trusting)

```bash
# Mandatory probe at session start
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null 2>&1 && echo "✅ $name :$port" || echo "❌ $name :$port"
done

# Live clock + seal chain head
tail -1 /root/.local/share/arifos/vault999/seal_chain.jsonl

# Honest anomalies (live state may differ from older notes)
cat memory/MEMORY.md 2>/dev/null | tail -20
```

> **Dynamic-state rule** (T₀ → T₁): state observed at T₀ is evidence only for T₀. Before any irreversible act, re-probe at T₁.

---

## 5. Working agreement

- **Solve before asking.** README + AGENTS.md + ZEN.md + `docs/FEDERATION_COCKPIT.md` cover most questions.
- **Reversible first.** Irreversible = `888_HOLD` + Arif's ack.
- **Speak human.** Constitutional machinery (receipts, floor numbers, hashes) stays in agent state. Talk to Arif in plain consequences with RASA.
- **Refuse patterns are HARAM.** "Not my tool" / "no visual tokens" / "can't use browser" → probe the full MCP surface first, then answer.

---

## 6. Where each artifact lives

| Artifact | Path | Authority |
|---|---|---|
| Constitution canon | `arifOS/GENESIS/000_KERNEL_CANON.md` | F13 (referenced from `GENESIS/` here) |
| Identity (3 agents) | `agent-cards/identity/{333-AGI,555-ASI,888-APEX}/` | 888-APEX validated |
| Organs (5 cards) | `agent-cards/organs/{arifos,aforge,geox,wealth,well}.json` | 888-APEX validated |
| Forge harnesses (11) | `agent-cards/harnesses/fi-001..fi-011.json` | A-FORGE bound |
| Master agent registry | `registries/AAA_AGENTS_REGISTRY.json` (v2.0.0) | 888-APEX validated |
| Federation live state | `registries/AAA_FEDERATION_STATE.yaml` | self-refreshing |
| Memory index | `memory/_index.json` (machine-readable) | generated, see `scripts/index_memory.py` |
| Constitutional primitives | `docs/CONSTITUTIONAL_PRIMITIVES.md` v2.0 | EUREKA proof epoch |
| Zen inventory | this file | single point of entry |

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE.*
