# Federation Contract v2.1.0

> **SOT:** 2026-07-28 | **seal_seq:** SEAL-8a8e064d1fe34443
> **Authority:** F13 SOVEREIGN — Muhammad Arif bin Fazil
> **Canonical location:** `/root/AAA/docs/FEDERATION_CONTRACT.md` (symlinked from `/root/FEDERATION_CONTRACT.md`)
> **Supersedes:** All prior organ-specific FEDERATION_CONTRACT.md copies, `/root/FEDERATION.md`
> **Pointer:** For constitutional floors (F1-F13), autonomy tiers, memory architecture, and code conventions → `/root/AGENTS.md`
> **Doctrine:** Satu domain. Satu web surface. Banyak organ, tetap bersempadan.

---

## 1. Federation Identity

The **arifOS Federation** is a governed intelligence system comprising a **9-node constitutional spine** (5 runtime + 4 domain organs), 32 repositories, and a single sovereign (Arif, F13). It operates on a single VPS (72.62.71.199) with Cloudflare Tunnel + Caddy ingress.

**Governing principle:** No organ may seal without arifOS. No organ may self-authorize mutation.

---

## 2. Organs — Constitutional Spine

| Layer | Organ | Function | Surface |
|-------|-------|----------|---------|
| **L0** | arifOS | Law | `arif-fazil.com/arifos/` |
| **L1** | AAA | Surface | `arif-fazil.com/aaa/` |
| **L1** | APEX | Judgment | (embedded — unbundling target) |
| **L1** | arifFlow | Coordination | (internal) |
| **L1** | A-FORGE | Execution | `arif-fazil.com/forge/` |
| **L2** | GEOX | Earth | `arif-fazil.com/geox/` |
| **L2** | WEALTH | Capital | `arif-fazil.com/wealth/` |
| **L2** | WELL | Human | `arif-fazil.com/well/` |
| **L2** | HERMES | Bridge | `t.me/arifos` |

---

## 3. Authority Chain

```
Human Intent → arif_init (000) → arif_observe (111) → arif_think (333)
→ arif_route (444) → [domain organ computes] → arif_judge (888)
→ SEAL/HOLD/SABAR/VOID → arif_forge (777) → A-FORGE executes
→ arif_seal (999) → VAULT999 records
```

No link may be skipped. No organ may self-authorize.

---

## 4. Unified Web Surface

All public surfaces are paths under `https://arif-fazil.com/`. Legacy subdomains → 301 redirects.

| Path | Organ | Legacy Subdomain |
|------|-------|-----------------|
| `/` | Cockpit (React SPA) | — |
| `/000/` | Genesis | — |
| `/999/` | Seal Verification | — |
| `/arifos/` | Observatory | `arifos.arif-fazil.com` → 301 |
| `/aaa/` | Control Plane | `aaa.arif-fazil.com` → 301 |
| `/geox/` | Earth Lab | `geox.arif-fazil.com` → 301 |
| `/wealth/` | Capital | `wealth.arif-fazil.com` → 301 |
| `/well/` | Readiness | `well.arif-fazil.com` → 301 |
| `/forge/` | Execution | `forge.arif-fazil.com` → 301 |
| `/mcp/` | Gateway | `mcp.arif-fazil.com` → 301 |
| `/wiki/` | Knowledge | `wiki.arif-fazil.com` → 301 |

---

## 5. Cross-Organ Standards

### 5.1 MCP Transport
- All organs expose MCP via localhost ports
- Public ingress: Cloudflare Tunnel → Caddy → organ port
- Tool naming: organ prefix enforced (`arif_*`, `forge_*`, `geox_*`, `capital_*`, `well_*`)

### 5.2 Health Standard
- Every organ MUST expose `GET /health`
- Federation health sweep: `make health`

### 5.3 Secrets
- Single source: `/root/.secrets/vault.env` (143 env vars)
- Never hardcode, never commit, never paste

### 5.4 VAULT999
- Append-only, hash-chained: `/root/arifOS/VAULT999/outcomes.jsonl`
- Write only via `arif_seal` (999)
- Never edit, never rewrite

---

## 6. Standards

- Date-stamp tags: `vYYYY.MM.DD` (Iron Rule)
- Conventional commits with organ prefix
- Every active node has `FEDERATION_MAP.md`
- CI badge in every README

---

*DITEMPA BUKAN DIBERI — Forged from live state, not written from memory.*
