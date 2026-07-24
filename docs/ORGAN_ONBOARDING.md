# Organ Onboarding — 10-Step Checklist

> **SOT:** 2026-07-24 | **seal_seq:** fed-phase-7
> **Canonical:** `/root/AAA/docs/ORGAN_ONBOARDING.md`

Adding a new organ to the arifOS Federation requires constitutional, technical, and documentation integration. Follow all 10 steps.

---

## Step 1: Constitutional Review
- [ ] Define the organ's role (compute, route, reflect, execute — NOT judge)
- [ ] Verify the organ does NOT duplicate an existing organ's authority
- [ ] arif_judge SEAL on the admission proposal

## Step 2: GitHub Repository
- [ ] Create repo under `ariffazil/<organ-name>` on GitHub
- [ ] Standard files: README.md, LICENSE, AGENTS.md, CLAUDE.md, .gitignore
- [ ] Add SOT-MANIFEST block to README.md
- [ ] Add federation organ table to README.md (all 7+ organs)

## Step 3: CI/CD Pipeline
- [ ] Add `.github/workflows/` with gitleaks secret scanning
- [ ] Add CI badge to README
- [ ] Conventional commit format with organ prefix
- [ ] Date-stamp tags only (`vYYYY.MM.DD`)

## Step 4: Secrets & Environment
- [ ] All secrets from `/root/.secrets/vault.env` only
- [ ] No hardcoded keys, no `.env` files committed
- [ ] 5-R protocol documented: READ → RESOLVE → RECONCILE → RESTART → REPORT

## Step 5: MCP Surface
- [ ] Expose MCP via organ-specific prefix (e.g., `geox_*`, `capital_*`)
- [ ] Register prefix in `/root/AAA/docs/MCP_NAMING_STANDARD.md`
- [ ] tools/list returns only organ-prefixed tools
- [ ] No cross-prefix tool registration (F11 violation)

## Step 6: Health Endpoint
- [ ] Expose `GET /health` returning JSON with: `status`, `identity_hash`, `federation_geometry`
- [ ] Add to `/root/Makefile` health sweep

## Step 7: A2A Agent Card
- [ ] Create `/.well-known/agent-card.json` with valid `arifOS/agent-card/v2.2.0` schema
- [ ] Register in `/root/AAA/registries/AAA_AGENTS_REGISTRY.json`
- [ ] Register in `/root/AAA/docs/AGENT_CARD_REGISTRY.md`

## Step 8: VAULT999 Integration
- [ ] Define audit event types for the organ
- [ ] All irreversible actions sealed via `arif_seal` (999)
- [ ] No direct VAULT999 writes outside the seal chain

## Step 9: Documentation Surface
- [ ] Create `llms.txt` for AI agent discovery
- [ ] Register site in `/root/web-canon/canon/sites.yaml`
- [ ] Add to federation navigation (trinity-nav.js, navigation.json)
- [ ] Update `/root/AAA/docs/ORGAN.md` canonical organ map

## Step 10: Deploy & Verify
- [ ] Systemd unit created and tested
- [ ] Caddy reverse proxy configured (if public-facing)
- [ ] `make prove` passes with new organ included
- [ ] 24h monitoring before declaring ACTIVE

---

## Post-Onboarding

- [ ] Monthly SOT stamp refresh on README + AGENTS.md
- [ ] Quarterly organ boundary audit
- [ ] Cross-ref audit on every federation structural change

*DITEMPA BUKAN DIBERI — Organs are forged, not given.*
