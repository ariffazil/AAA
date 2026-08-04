# Security

## Secrets

- **Secrets:** `/root/.secrets/kunci-mas.env` (mode 600). `${ENV_VAR}` placeholders only. Never commit, never paste, never `> mode 600`. Audit: `/root/.secrets/INDEX.md`.
- **Public exposure:** Cloudflare Tunnel + Caddy only. Organs bind `127.0.0.1`. No public MCP door except the standard `*.arif-fazil.com` URLs.
- **Inbound auth:** Cryptographic only (Ed25519 + SCT — Session Capability Tokens, `sct_v1.*`). CAPTCHA on inbound federation = **HARAM**; captcha tools are outbound-only utilities.
- **CPA delivery:** `forge_send_confirm` (form mode) · `forge_transfer_confirm` (financial). F13 consent gate.
- **PATTERNS security scan:** `forge_security_drift_scan` (ports/services/cron drift). `make security-audit` runs per-organ audits.

### Cryptographic secret distribution

```
/opt/arifos/app/.signing_key      mode 640   owner: root   group: arifos
/opt/arifos/app/.arifos_secrets/  mode 750   owner: root   group: arifos
```

`arifos` group = federation trust circle (`root`, `arifos`, `nobody`, `ariffazil`).
**Never use `/etc/environment` for cryptographic secrets** — mode 644 is world-readable.
For HMAC session secrets, pass `ARIFOS_SESSION_SECRET_FILE=/opt/arifos/app/.signing_key`.

### Permission repair discipline

Before any recursive `chown` / `chmod` / `setfacl` on `/var/lib/arifos`:
snapshot ACLs → kill file holders → mutate → verify both readers (arifos, nobody)
can write → restart daemon + probe health.
Full recipe: `/root/RUNBOOK.md` §9.

## Memory landscape (6 levels)

```
L1 Redis   — now / ephemeral              L4 Supabase  — official structured (25 domain tables)
L2 Redis   — session thread               L5 Graphiti   — relationships (FalkorDB + Ollama)
L3 Qdrant  — fuzzy similarity             L6 VAULT999   — immutable sealed truth
```

Rule: memory is **not truth** until it has provenance. Truth is **not final** until sealed.
VAULT999 canonical: `/root/arifOS/VAULT999/outcomes.jsonl`. Symlink `/root/VAULT999`.
Derivative: Supabase `vault_sealed_events` (queryable, **never** source of truth).
`chattr +a`. Merkle anchor every 100 receipts. **Never edit. New entries only.**

## Testing strategy

- **Root aggregator:** `make prove` (health + SOT check + security audit + floor benchmark + organ boundary benchmark + VAULT999 verify + vault verify + reality replay + click-depth audit + pointer integrity).
- **Constitutional drift:** `make floor-benchmark`, `make organ-boundary-benchmark` → `/root/benchmarks/`.
- **Vault integrity:** `make vault999-verify`, `make vault-verify`, `make vault-status`.
- **Reality ledger:** `make reality-record`, `make reality-unresolved`, `make reality-verify`, `make reality-replay`.
- **MCP surface drift:** `forge_surface_guard check`, `forge_surface_audit mode=audit`.
- **Per-organ:** see §7.2. arifOS has 4/4 M2 fail-closed totality tests + 13-floor benchmark.
- **Wire (system-level):** `make scorecard` (canonical federation scorecard).

### A-FORGE test suite

> **Canonical list** in `/root/A-FORGE/package.json` (`scripts.test`) and
> `/root/A-FORGE/dist/test/` directory. Run via `npm test` from `/root/A-FORGE`.
> Don't hand-edit the list — it is the registry of test files.
