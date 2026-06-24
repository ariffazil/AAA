<!-- SOT-MANIFEST
owner: Arif
last_verified: 2026-06-24
valid_from: 2026-06-24
valid_until: 2026-07-24
confidence: high
scope: /root/AAA
-->

# Federation Contract — AAA (Cockpit / Control Plane)

> **Organ:** AAA | **Repo:** `ariffazil/AAA` | **Port:** 3001 (a2a-server)
> **Canonical federation contract:** [`ariffazil/arifos/FEDERATION_CONTRACT.md`](https://github.com/ariffazil/arifos/blob/main/FEDERATION_CONTRACT.md)
> **Role:** Cockpit / control plane — abstract, attest, and abduct across all federation organs.
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## 1. Position in the Federation

```
Arif (F13 SOVEREIGN)
  → arifOS kernel (8088) — constitutional judgment
    → Domain organs (GEOX / WEALTH / WELL) — evidence
      → AAA a2a-server (3001) — A2A v0.3.0 deliberation + 888 JUDGE
        → AAA cockpit — display and human interface
          → A-FORGE (7071/7072) — execution under SEAL
            → VAULT999 — immutable audit ledger
```

AAA is the **Control Plane / Cockpit**. It absorbs the legacy APEX 888 JUDGE deliberation, hosts the React cockpit, and provides the A2A v0.3.0 gateway. It displays; it does not compute domain truth or execute mutations.

---

## 2. Authority

### AAA OWNS
- A2A v0.3.0 agent gateway (`a2a-server/`)
- 888 JUDGE deliberation engine (`a2a-server/deliberation.ts`)
- Cockpit dashboard (`src/`) for human visibility
- Agent cards, agent registry, and skill registries

### AAA NEVER
- Computes domain evidence (geoscience, finance, biometrics)
- Self-executes mutations (deferred to A-FORGE under SEAL)
- Overrides arifOS constitutional floors

---

## 3. External Contracts

| Contract | Canonical Location | Purpose |
|---|---|---|
| Federation topology | `ariffazil/arifos/FEDERATION_CONTRACT.md` | Organ roles and authority chain |
| Constitutional floors | `ariffazil/arifos/static/arifos/theory/000/000_CONSTITUTION.md` | F1–F13 |
| Agent landing | `/root/AAA/AGENTS.md` | Build/test/run rules for this repo |
| Agent invariants | `/root/AAA/skills/aaa-agent-invariants/SKILL.md` | Compact operating constitution |
| Agentic governance | `/root/AAA/skills/aaa-agentic-governance/SKILL.md` | Canonical AAA governance skill |

---

## 4. Services

- **Cockpit UI:** `https://aaa.arif-fazil.com` (Caddy → Vite dist)
- **A2A Server:** `http://127.0.0.1:3001` (systemd `aaa-a2a.service`)

---

## 5. Handoffs

| To | When | Format |
|---|---|---|
| arifOS | Constitutional verdict requests | A2A / MCP bridge |
| A-FORGE | Approved execution under SEAL | Lease + evidence |
| Domain organs | Evidence requests / status display | MCP / A2A |
| VAULT999 | Audit receipts after judgment | Immutable entry |

---

## 6. Verdict

AAA is the cockpit where judgment becomes visible. The kernel decides; AAA displays and routes; A-FORGE executes.

*DITEMPA BUKAN DIBERI.*
