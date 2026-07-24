# Federation Contract v2

> **SOT:** 2026-07-24 | **seal_seq:** fed-phase-7-zen
> **Authority:** F13 SOVEREIGN — Muhammad Arif bin Fazil
> **Canonical location:** `/root/FEDERATION_CONTRACT.md`
> **Supersedes:** All prior organ-specific FEDERATION_CONTRACT.md copies

---

## 1. Federation Identity

The **arifOS Federation** is a governed intelligence system comprising 7 core organs, 31 GitHub repositories, and a single sovereign (Arif, F13). It operates on a single VPS (72.62.71.199) with Cloudflare Tunnel + Caddy ingress.

**Governing principle:** No organ may seal without arifOS. No organ may self-authorize mutation.

---

## 2. Organs — Authority Boundaries

| Organ | Role | Port | MCP Prefix | Permissions |
|-------|------|------|-----------|-------------|
| **arifOS** | Constitutional kernel | 8088 | `arif_*` | Judges, seals, routes. NEVER executes. |
| **A-FORGE** | Execution shell | 7071/7072 | `forge_*` | Executes after SEAL. NEVER adjudicates. |
| **AAA** | Cockpit + A2A | 3001 | — | Routes, displays. NEVER adjudicates. |
| **GEOX** | Earth intelligence | 8081 | `geox_*` | Computes earth evidence. NEVER decides. |
| **WEALTH** | Capital intelligence | 18082 | `capital_*` | Computes capital math. NEVER allocates. |
| **WELL** | Vitality guard | 18083 | `well_*` | Reflects readiness. NEVER diagnoses. |
| **HERMES** | Multi-modal bridge | Telegram | — | Routes signals. NEVER adjudicates. |

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

## 4. Cross-Organ API Contracts

### 4.1 MCP Transport
- All organs expose MCP via `https://<organ>.arif-fazil.com/mcp`
- Unified gateway: `https://mcp.arif-fazil.com/mcp`
- Tool naming: organ prefix enforced (`arif_*`, `forge_*`, `geox_*`, `capital_*`, `well_*`)

### 4.2 A2A Protocol (AAA :3001)
- Agent discovery: `/.well-known/agent-card.json` on every organ
- Agent cards registered in `AAA/registries/AAA_AGENTS_REGISTRY.json`
- Protocol version: 1.0

### 4.3 Health Standard
- Every organ MUST expose `GET /health` returning JSON with at minimum: `status`, `identity_hash`, `federation_geometry`
- Federation health sweep: `/root/Makefile` health target

### 4.4 Secrets
- Single source: `/root/.secrets/vault.env` (143 env vars)
- Never hardcode, never commit, never paste in chat

### 4.5 VAULT999
- Append-only, hash-chained, at `/root/arifOS/VAULT999/outcomes.jsonl`
- Write only via `arif_seal` (999)
- Never edit, never rewrite

---

## 5. CI/CD Standards

- Every organ runs `gitleaks` secret scanning
- Every organ has a CI badge in README
- Every organ uses date-stamp tags (`vYYYY.MM.DD`)
- Conventional commits with organ prefix: `[FORGE]`, `[ZEN]`, `[REPAIR]`, `[AUDIT]`

---

## 6. Incident Escalation

| Severity | Response | Authority |
|----------|----------|-----------|
| Organ degraded | Auto-restart via systemd | T1 |
| Multi-organ failure | `make prove` + investigate | T2 announce |
| Data loss / vault corruption | Stop all mutations, alert Arif | T3 888_HOLD |
| Security breach | Stop public ingress, rotate secrets | T3 888_HOLD |

---

## 7. New Organ Admission

See `/root/AAA/docs/ORGAN_ONBOARDING.md` for the 10-step checklist.

---

## 8. Federation Verification

```bash
make health                     # 8-service liveness sweep
make prove                      # Full proof pack
for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL,HERMES}; do
  git -C "$d" status -s         # Dirty check
done
```

---

*DITEMPA BUKAN DIBERI — This contract is forged from live state, not written from memory.*
