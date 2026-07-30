# Federation Contract v2.1.0

> **SOT:** 2026-07-28 | **seal_seq:** SEAL-8a8e064d1fe34443
> **Authority:** F13 SOVEREIGN — Muhammad Arif bin Fazil
> **Canonical location:** `/root/AAA/docs/FEDERATION_CONTRACT.md` (symlinked from `/root/FEDERATION_CONTRACT.md`)
> **Supersedes:** All prior organ-specific FEDERATION_CONTRACT.md copies, `/root/FEDERATION.md`
> **Pointer:** Floors / autonomy / memory / conventions → `/root/AGENTS.md`  
> **Topology SOT:** `/root/AAA/docs/ORGAN.md` · machine `/root/AAA/federation/organs.yaml`  
> **Doctrine:** Satu domain. Satu web surface. Banyak organ, tetap bersempadan.

---

## 1. Federation Identity

The **arifOS Federation** is a governed intelligence system: one sovereign (Arif, F13), one kernel (arifOS), core organs + linked planes (see ORGAN.md), and a single VPS (72.62.71.199) with Cloudflare Tunnel + Caddy ingress.

**Governing principle:** No organ may seal without arifOS. No organ may self-authorize mutation.

---

## 2. Organs — Constitutional Spine

> **Full topology SOT:** [`/root/AAA/docs/ORGAN.md`](/root/AAA/docs/ORGAN.md) · machine [`/root/AAA/federation/organs.yaml`](/root/AAA/federation/organs.yaml)  
> This section is a **thin contract summary** only — do not maintain a second full map here.

| Layer | Organ | Function | Port / surface |
|-------|-------|----------|----------------|
| **L0** | arifOS | Law / judge / seal gate | `:8088` · `/arifos/` |
| **L1** | AAA | Cockpit / A2A | `:3001` · `/aaa/` |
| **L1** | arifFLOW | Metabolism (never judge/exec) | `:7073` |
| **L1** | A-FORGE | Execution after SEAL | `:7071/:7072` · `/forge/` |
| **L2** | GEOX | Earth evidence | `:8081` · `/geox/` |
| **L2** | WEALTH | Capital compute | `:18082` · `/wealth/` |
| **L2** | WELL | Vitality (REFLECT_ONLY) | `:18083` · `/well/` |
| **EDGE** | HERMES | Telegram bridge | gateway · not an organ |
| **MEMORY** | VAULT999 | Immutable receipts | path · not a port |

APEX is **not** a separate organ (judgment lives in arifOS). FED/FLAME are advisory planes — see ORGAN.md §3.

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
