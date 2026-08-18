NODE_CONTRACT_7GAP_FILTER.md — Forbidden-Pattern Detection for New Organs/Agents/Workflows

> **Forge:** 2026-08-18 (post graph-engineering audit)
> **Status:** Binding intake filter — every proposed node passes all 7 before mint.
> **Companion docs:** `F1_AMANAH.md`, `F11_AUDITABILITY.md`, `GODEL_LOCK.md`, `HITL_TAXONOMY.md`

## The One Rule

A node that fails any gate is **forbidden to mint**. The filter is not advisory.
The forge operator runs it; the constitutional judge signs the rejection.

## The 7-Gap Filter

| # | Gap | Test | Forbidden if |
|---|-----|------|--------------|
| 1 | **Gödel lock** | Can this node certify itself? | node == auditor for same artifact |
| 2 | **Authority tier** | Does this node operate above its tier? | T0 has mutation; T2 has no rollback |
| 3 | **Sealed consequence** | Does failure leave an auditable trace? | no VAULT999 receipt, no parent_seal_hash |
| 4 | **Reality auditor** | Does it probe live state or assume? | reads cached state without :PORT/health |
| 5 | **Model demotion** | Does it handle capability downgrade? | no fallback chain, no autonomy clamp |
| 6 | **HITL separation** | Authorization vs cognitive — are they mixed? | same surface asks "should I?" + "do it" |
| 7 | **Fork governance** | Does clone carry identity? | no SCT lease, no SOUL.md handoff |

## Scoring

Each gate passes or fails. No partial credit. No compensating gates.

- 7/7 → `MINT` (proceed to forge)
- 6/7 → `REPAIR` (one gate failed, fix before mint)
- ≤5/7 → `VOID` (architecture invalid, redesign)

## Fork Guidance

Each gap maps to a canonical concern:

- Gap 1 → `/root/AAA/governance/GODEL_LOCK.md` (Eureka 9)
- Gap 2 → `/root/AAA/agents/opencode/DOCTRINE.md` §2 (autonomy tiers)
- Gap 3 → `/root/AAA/governance/VAULT999_CHAIN.md` (F11 auditability)
- Gap 4 → `/root/AAA/governance/REALITY_FIRST.md` (Eureka 4)
- Gap 5 → `/root/AAA/agents/opencode/DOCTRINE.md` §5 (model demotion trap)
- Gap 6 → `/root/AAA/instructions/HITL_TAXONOMY.md` (2026-08-09 verdict)
- Gap 7 → `/root/AAA/governance/FORK_GOVERNANCE.md` (heritage identity)

## Operational use

Run before minting any of:
- new MCP organ
- new agent (333/555/777/888 lane)
- new workflow that crosses 2+ organs
- new graph topology touching ≥4 nodes

The check is **mechanical** — no subjective judgment. Run once, count gates, mint or reject.

## Scar

Forged 2026-08-18 after reading graph-engineering discourse that proposed
"A node you cannot describe precisely is a node you cannot route, test, or replace."
That is the gateway. The 7-gap filter is the boundary beyond the gateway.

DITEMPA BUKAN DIBERI ⚒️
