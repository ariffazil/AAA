# OBSERVATORY FOLDER STRUCTURE

> **Canonical folder layout for all 3 Trinity surfaces.**
> Governed by ARIF-SITES source repo. Deployed via atomic symlink swap.
> DITEMPA BUKAN DIBERI — Forged, Not Given.

---

## Table of Contents

1. [Trinity Overview](#1-trinity-overview)
2. [SOUL: arif-fazil.com](#2-soul---arif-fazil-com)
3. [MIND: arifos.arif-fazil.com](#3-mind---arifos-arif-fazil-com)
4. [BODY: aaa.arif-fazil.com](#4-body---aaa-arif-fazil-com)
5. [Deploy Mechanic](#5-deploy-mechanic)
6. [Shared Asset Protocol](#6-shared-asset-protocol)
7. [Caddy Route Patterns](#7-caddy-route-patterns)
8. [Symlink-Swap Deploy Procedure](#8-symlink-swap-deploy-procedure)
9. [Deploy-State Receipt](#9-deploy-state-receipt)

---

## 1. Trinity Overview

```
┌─────────────────────────────────────────────────────────┐
│               /var/www/html/  (webroot)                 │
│                                                          │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│   │    arif/     │  │   arifos/    │  │    aaa/      │  │
│   │   Ψ SOUL     │  │   Ω MIND     │  │   Δ BODY     │  │
│   │ arif-fazil   │  │ arifos.arif  │  │ aaa.arif     │  │
│   │   .com       │  │  -fazil.com  │  │  -fazil.com  │  │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│          │                 │                 │           │
│          └──────────┬──────┴──────┬──────────┘           │
│                     │             │                      │
│              ┌──────▼──────┐      │                      │
│              │  _shared/   │◄─────┘                      │
│              │ (canonical) │  symlink from arifos/       │
│              └─────────────┘       and aaa/              │
│                                                          │
│   ┌──────────────────────────────────────────┐           │
│   │  arif.releases/     (previous releases)   │           │
│   │  arif.fallback/     (instant rollback)    │           │
│   └──────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

### Surface Roles

| Surface | Domain | Organ | Role | Deploy Mechanic |
|---------|--------|-------|------|----------------|
| **Ψ SOUL** | arif-fazil.com | Identity | Human identity, canonical docs, essays, wealth dashboard | ARIF-SITES atomic swap (symlink) |
| **Ω MIND** | arifos.arif-fazil.com | Governance | Observatory SPA, federation map, agent reference | Direct file sync (out-of-path) |
| **Δ BODY** | aaa.arif-fazil.com | Operations | AAA Cockpit SPA, A2A gateway, federation apps | Direct file sync (out-of-path) |

---

## 2. SOUL — arif-fazil.com

```
/var/www/html/arif/
│
├── index.html                           ← Root SPA (human identity)
├── human.md                             ← Human description for AI crawlers
├── robots.txt                           ← Crawler directives
├── sitemap.xml                          ← SEO sitemap
├── soul.json                            ← SOUL organ manifest
├── build-info.json                      ← Current build metadata
├── root-shell.css                       ← Global shell CSS
├── _redirects                           ← Cloudflare Pages _redirects
├── _routes.json                         ← Cloudflare Pages _routes
│
├── canon/                               ← Canonical documents
│   ├── *.md
│   └── *.pdf
│
├── essays/                              ← Human essays
│   └── *.md
│
├── wealth/                              ← WEALTH dashboard
│   ├── index.html                       ← WEALTH SPA root
│   ├── api/                             ← WEALTH API (proxied to port 3457)
│   │   └── wealth/
│   │       └── health                   ← Health endpoint
│   └── gold/                            ← Gold chart (proxied to port 3456)
│       ├── index.html
│       └── api/
│           └── gold/
│               └── ticker
│
├── makcikgpt-md/                        ← MakcikGPT content (MD for AI crawlers)
│
├── 000/                                 ← Genesis section
│   └── index.html
│
├── 999/                                 ← Validation section
│   └── index.html
│
├── assets/                              ← Static assets (images, fonts)
│
├── data/                                ← Data files
│
├── proof/                               ← Proof artifacts
│
├── _shared/                             → symlink to /var/www/html/_shared/
│
├── .well-known/
│   ├── webmcp.json                      ← 14+ tools
│   ├── mcp.json                         ← MCP discovery
│   ├── agent.json                       ← A2A agent identity
│   ├── did.json                         ← did:web for identity
│   ├── did-configuration.json           ← DID configuration
│   ├── governance.jsonld                ← 13 constitutional floors
│   ├── arifos-federation.json           ← 8 federation nodes
│   ├── capabilities.json                ← Declared capabilities
│   └── AGENTS.md.sig                    ← Signed AGENTS.md
│
└── api/                                 ← API endpoints (proxied to kernel)
    ├── status
    ├── federation-probe
    ├── build-info
    └── deploy-state.json                ← Deploy receipt (ephemeral)
```

### .well-known/webmcp.json structure

```json
{
  "name": "arif-fazil.com WebMCP Surface",
  "version": "1.1",
  "description": "Browser-native agent tool surface for arif-fazil.com",
  "sovereign": "did:web:arif-fazil.com",
  "constitutional_kernel": "https://arifos.arif-fazil.com",
  "tools": [
    { "name": "observatory_state", "description": "Live federation state" },
    { "name": "federation_probe", "description": "Probe all organs" },
    { "name": "federation_manifest", "description": "Federation topology" },
    { "name": "canon_document", "description": "Read canonical document" },
    { "name": "essay_read", "description": "Read human essay" },
    { "name": "llms_context", "description": "LLM training context" }
  ]
}
```

---

## 3. MIND — arifos.arif-fazil.com

```
/var/www/html/arifos/
│
├── index.html                           ← Observatory SPA
├── federation.html                      ← Federation map (SPA or static)
├── agents.md                            ← Agent reference doc
├── llms.txt                             ← LLM context (trainable)
├── llms-full.txt                        ← Full LLM context
├── llms.json                            ← Structured LLM index
├── manifest.txt                         ← Short manifest
├── robots.txt
├── sitemap.xml
│
├── federation-manifest.json             ← Federation node list
│
├── _shared/                             → symlink to /var/www/html/_shared/
│
├── api/observatory/v1/                  ← Proxied to arifOS kernel (:8088)
│   ├── snapshot                         ← GET live state
│   ├── health-public                    ← GET public health
│   ├── capabilities                     ← GET declared capabilities
│   └── seal/*                           ← GET seal chain (operator-only)
│
├── .well-known/
│   ├── webmcp.json                      ← Observatory tools (8+)
│   ├── mcp.json                         ← MCP server discovery
│   ├── agent-card.json                  ← A2A agent card
│   ├── agent.json                       ← Agent identity
│   ├── did.json                         ← did:web
│   ├── governance.jsonld                ← 13 floors (machine-readable)
│   ├── arifos-federation.json           ← Federation definition
│   ├── openapi.json                     ← OpenAPI spec
│   ├── ai-plugin.json                   ← AI plugin manifest
│   └── observatory.json                 ← Observatory metadata
│
└── arifos/                              ← Static files (e.g. logos)
```

### .well-known/webmcp.json structure

```json
{
  "name": "arifOS Observatory WebMCP Surface",
  "version": "2.0",
  "description": "Constitutional witness, federation observatory, live reality snapshot",
  "sovereign": "did:web:arif-fazil.com",
  "constitutional_kernel": "https://arifos.arif-fazil.com",
  "tools": [
    { "name": "observatory_snapshot", "description": "Live kernel snapshot" },
    { "name": "federation_health", "description": "All organs health" },
    { "name": "seal_chain_status", "description": "VAULT999 chain head" },
    { "name": "constitutional_floors", "description": "F1-F13 state" },
    { "name": "llms_txt_context", "description": "llms.txt content" },
    { "name": "agent_card_resolve", "description": "A2A agent cards" },
    { "name": "federation_manifest", "description": "Topology map" },
    { "name": "governance_audit", "description": "Floor compliance" }
  ]
}
```

---

## 4. BODY — aaa.arif-fazil.com

```
/var/www/html/aaa/
│
├── index.html                           ← AAA Cockpit SPA
├── robots.txt
├── sitemap.xml
├── manifest.json                        ← PWA manifest
├── iron-shell.css                       ← Shell CSS
├── panel-boundary.js                    ← Panel boundary controller
├── status.json                          ← Current status
├── humans.txt                           ← Human attribution
│
├── _state/                              ← Live state (out-of-path persistent)
│   └── seal_chain_head.json             ← Mirrored VAULT999 chain head
│
├── a2a/                                 ← A2A gateway (proxied to :3001)
│
├── agents/                              ← Agent reference
├── agents.md                            ← Agent listing
│
├── cockpit/                             ← Cockpit components
├── docs/                                ← Federation docs
├── assets/                              ← Static assets
├── images/                              ← Images
├── public/                              ← Public files
│
├── apps/                                ← Federation apps
│   ├── vault/                           ← VAULT999 viewer
│   │   └── index.html
│   └── observatory/                     ← Embedded observatory
│       └── index.html
│
├── mcp/                                 ← MCP GUI
├── mcp-gui/                             ← MCP GUI app
├── webmcp/                              ← WebMCP app
├── scamper/                             ← Scamper tool
├── nabilah/                             ← Nabilah section
├── briefings/                           ← Briefings
│
├── _shared/                             → symlink to /var/www/html/_shared/
│
└── .well-known/
    ├── webmcp.json                      ← 18+ agents / tools
    ├── mcp.json                         ← MCP discovery
    ├── agent-card.json                  ← A2A agent card
    ├── agent.json                       ← Agent identity
    ├── arifos.json                      ← arifOS integration metadata
    └── ai-plugin.json                   ← AI plugin manifest
```

### .well-known/webmcp.json structure

```json
{
  "name": "AAA Cockpit WebMCP Surface",
  "version": "2.0",
  "description": "AAA control plane — agent registry, A2A gateway, federation cockpit",
  "agents": [
    { "id": "333-AGI", "class": "AGI", "role": "reasoning" },
    { "id": "555-ASI", "class": "ASI", "role": "stewardship" },
    { "id": "888-APEX", "class": "APEX", "role": "judgment" },
    { "id": "A-AUDIT", "class": "AUDIT", "role": "oversight" },
    { "id": "A-ARCHIVE", "class": "ARCHIVE", "role": "vault" },
    { "id": "OpenCode", "class": "FORGE", "role": "execution" }
  ],
  "tools": [
    { "name": "agent_registry", "description": "All registered agents" },
    { "name": "a2a_task_status", "description": "A2A task status" },
    { "name": "federation_health", "description": "Federation health" },
    { "name": "vault_viewer", "description": "VAULT999 viewer" }
  ]
}
```

---

## 5. Deploy Mechanic

Three deploy mechanics — choose by surface:

| Mechanic | Surfaces | Source | Rollback | Persistence |
|----------|----------|--------|----------|-------------|
| **ARIF-SITES atomic swap** | SOUL (`arif/`) | `/root/ARIF-SITES/sites/arif-fazil.com/` | Symlink revert to `.fallback/` | Volatile — replaced on every deploy |
| **Direct file sync** | MIND (`arifos/`) BODY (`aaa/`) | Edit directly in `/var/www/html/` | Manual restore from backup | Persistent — survives no deploy script |
| **Out-of-path persistent** | `wealth/`, `gold/`, API data | Edit directly | Manual restore | Never touched by deploy scripts |

### Surface-to-Mechanic Matrix

```
┌──────────────────┬──────────────────────┬──────────────────────┐
│ Surface          │ Source Repository    │ Webroot Path         │
├──────────────────┼──────────────────────┼──────────────────────┤
│ Ψ SOUL           │ /root/ARIF-SITES/    │ /var/www/html/arif/  │
│ Ω MIND           │ (direct)             │ /var/www/html/arifos/│
│ Δ BODY           │ (direct)             │ /var/www/html/aaa/   │
│ WEALTH dashboard │ (direct)             │ /var/www/html/wealth/│
│ Gold chart       │ (direct)             │ /var/www/html/gold/  │
└──────────────────┴──────────────────────┴──────────────────────┘
```

### Atomic Swap Layout

```
/var/www/html/
├── arif/                  → symlink to arif.releases/20260715T120000Z/
├── arif.fallback/         → symlink to previous working release
└── arif.releases/
    ├── 20260714T000000Z/   ← previous
    ├── 20260715T120000Z/   ← current active
    └── 20260716T080000Z/   ← next (staged)
```

**Why symlink swap over in-place sync:**
- Zero partial-deploy window — swap is atomic (`mv -T`)
- Instant rollback — `mv -T arif arif.fallback && mv -T arif.releases/N arif`
- Previous release survives on disk until pruned
- Deploy script never writes into the live tree

---

## 6. Shared Asset Protocol

### Canonical Location

```
/var/www/html/_shared/          ← Single source of truth
├── design-system/
│   ├── tokens.css              ← Design tokens (colours, spacing, typography)
│   ├── components.css          ← Shared UI components
│   └── arifos-logo.svg         ← Canonical logo
├── trinity-nav.js              ← Navigation bar (all 3 surfaces)
├── observatory.js              ← Observatory widget
├── arrow-of-time.js            ← Timeline visualisation
├── arrow-of-time-soul.js       ← SOUL variant
├── arrow-of-time-mind.js       ← MIND variant
├── arrow-of-time-body.js       ← BODY variant
├── trinity-nav.html            ← Navigation HTML template
├── observatory.json            ← Observatory data
└── webmcp/
    ├── arifos-webmcp-adapter.js ← WebMCP kernel adapter
    └── observatory-tools.js     ← Observatory MCP tools
```

### Symlink Wiring

```bash
# SOUL — direct checkout (ARIF-SITES copies _shared from source)
# Already part of the ARIF-SITES repo at sites/arif-fazil.com/_shared/

# MIND — symlink to canonical
ln -sfn /var/www/html/_shared /var/www/html/arifos/_shared

# BODY — symlink to canonical
ln -sfn /var/www/html/_shared /var/www/html/aaa/_shared
```

### Caddy Route

All 3 Caddy blocks import the same snippet:

```caddy
(shared_assets) {
    handle /_shared/* {
        uri strip_prefix /_shared
        root * /var/www/html/_shared
        file_server
    }
}
```

### Update Protocol

1. Edit files in `/var/www/html/_shared/` directly — changes are live immediately
2. For SOUL (ARIF-SITES managed): also copy `_shared/` into `/root/ARIF-SITES/sites/arif-fazil.com/_shared/` so the next atomic deploy preserves the changes
3. Verify all 3 surfaces reflect the change

---

## 7. Caddy Route Patterns

### Ψ SOUL: arif-fazil.com

```
arif-fazil.com {
    import tls_origin
    import shared_assets
    encode zstd gzip
    root * /var/www/html/arif

    # .well-known files served from static root
    handle /.well-known/* {
        uri strip_prefix /.well-known
        root * /var/www/html/arif/.well-known
        try_files {path} /index.html
        file_server
    }

    # AI crawler → raw .md bypass
    @ai-bot {
        header_regexp User-Agent (?i)GPTBot|ClaudeBot|...
        path /wealth/makcikgpt/*
    }
    handle @ai-bot {
        rewrite * {path}.md
        file_server
    }

    # API routes → arifOS kernel (:8088)
    handle /api/* { reverse_proxy 127.0.0.1:8088 }
    handle /mcp*  { reverse_proxy 127.0.0.1:8088 }

    # Genesis & validation sections
    @genesis path /000/*
    @validation path /999/*

    # SPA fallback
    handle {
        try_files {path} /index.html
        file_server
    }
}
```

### Ω MIND: arifos.arif-fazil.com

```
arifos.arif-fazil.com {
    import tls_origin
    import shared_assets
    encode zstd gzip
    root * /var/www/html/arifos

    # Observatory .well-known served from static root
    @observatory_discovery path /.well-known/openapi.json
        /.well-known/ai-plugin.json /.well-known/agent-card.json
        /.well-known/did.json /.well-known/mcp.json
        /.well-known/webmcp.json /.well-known/observatory.json
        /.well-known/governance.jsonld /.well-known/arifos-federation.json
    handle @observatory_discovery {
        root * /var/www/html/arifos
        file_server
    }

    # Other .well-known → kernel
    handle /.well-known/* { reverse_proxy 127.0.0.1:8088 }

    # LLM context — no-cache
    handle /llms.txt { header Cache-Control "no-cache"; file_server }

    # Observatory API → kernel
    handle /api/observatory/v1/* { reverse_proxy 127.0.0.1:8088 }

    # SPA fallback
    handle {
        try_files {path} /index.html
        file_server
    }
}
```

### Δ BODY: aaa.arif-fazil.com

```
aaa.arif-fazil.com {
    import tls_origin
    import shared_assets
    encode zstd gzip
    root * /var/www/html/aaa

    # Seal chain head — live heartbeat from disk
    handle /api/seal-chain/head {
        import cors_public
        header Content-Type "application/json"
        header Cache-Control "no-cache"
        rewrite * /_state/seal_chain_head.json
        file_server
    }

    # A2A static files
    @a2a_static path /a2a/agents.json /a2a/status.json /a2a/index.html
    handle @a2a_static { file_server }

    # A2A gateway → AAA server (:3001)
    handle /a2a/* { reverse_proxy 127.0.0.1:3001 }
    handle /api/* { reverse_proxy 127.0.0.1:3001 }
    handle /mcp-apps/* { reverse_proxy 127.0.0.1:3001 }
    handle /health { reverse_proxy 127.0.0.1:3001 }

    # SPA fallback
    handle {
        try_files {path} /index.html
        file_server
    }
}
```

---

## 8. Symlink-Swap Deploy Procedure

### Prerequisites

```bash
# Ensure release archive directory exists
mkdir -p /var/www/html/arif.releases
mkdir -p /root/forge_work/deployments/arif-fazil.com
```

### Full Procedure

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
SITE="arif-fazil.com"
SOURCE="/root/ARIF-SITES/sites/${SITE}"
RELEASE="/var/www/html/arif.releases/${TS}"
WEBROOT="/var/www/html/arif"
ARCHIVE="/root/forge_work/deployments/${SITE}/${TS}"

# Step 1 — Build release
echo "[1/6] Building release ${TS}"
mkdir -p "$RELEASE"
cp -r "$SOURCE"/* "$RELEASE/"

# Step 2 — Wire shared assets
echo "[2/6] Wiring _shared symlink"
ln -sfn /var/www/html/_shared "$RELEASE/_shared"

# Step 3 — Dry run
echo "[3/6] Dry-run: would swap ${RELEASE} → ${WEBROOT}"
diff -r "$WEBROOT" "$RELEASE" --exclude=.well-known 2>/dev/null || true

# Step 4 — Atomic swap
echo "[4/6] Performing atomic swap"
# Preserve fallback
[ -L "$WEBROOT" ] && cp -rL "$WEBROOT" "${WEBROOT}.pre-swap.${TS}" || true
# Stage new release
ln -sfn "$RELEASE" "${WEBROOT}.staging"
# Atomic swap
mv -T "${WEBROOT}.staging" "$WEBROOT"

# Step 5 — Post-deploy verification
echo "[5/6] Verifying deployment"
curl -sI "https://${SITE}/" | head -3
curl -s "https://${SITE}/.well-known/webmcp.json" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(f'OK — {len(d.get(\"tools\",[]))} tools')"

# Step 6 — Write deploy receipt
echo "[6/6] Writing deploy receipt"
mkdir -p "${WEBROOT}/api"
cat > "${WEBROOT}/api/deploy-state.json" << RECEIPT
{
  "surface": "${SITE}",
  "deployed_at": "${TS}",
  "source_commit": "$(git -C /root/ARIF-SITES rev-parse --short HEAD 2>/dev/null || echo 'unknown')",
  "previous_target": "$(readlink ${WEBROOT} 2>/dev/null || echo 'direct')",
  "swap_type": "symlink",
  "receipt_hash": "$(echo "${TS}$(git -C /root/ARIF-SITES rev-parse HEAD 2>/dev/null)" | sha256sum | cut -d' ' -f1)",
  "organs_healthy": {
    "arifos": $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8088/health 2>/dev/null || echo 0),
    "aforge": $(curl -s -o /dev/null -w "%{http_code}" http://localhost:7071/health 2>/dev/null || echo 0)
  }
}
RECEIPT

echo "Deploy complete. Rollback: ln -sfn ${WEBROOT}.pre-swap.${TS} ${WEBROOT}"
```

### Rollback

```bash
# Find the previous release
ls -lt /var/www/html/arif.releases/

# Swap back
TS_ROLLBACK="20260715T120000Z"  # from desired release dir
ln -sfn "/var/www/html/arif.releases/${TS_ROLLBACK}" /var/www/html/arif

# Verify
curl -sI https://arif-fazil.com/ | head -3
```

### Bounded Archive

```
/var/www/html/
└── arif.releases/
    ├── 20260714T000000Z/      ← kept (used by .fallback)
    ├── 20260715T120000Z/      ← kept (current active)
    └── 20260716T080000Z/      ← kept (latest)

/root/forge_work/deployments/arif-fazil.com/
    ├── 20260714T000000Z.json  ← receipt
    ├── 20260715T120000Z.json  ← receipt
    └── 20260716T080000Z.json  ← receipt

Pruning policy: keep last 5 releases, delete older on each new deploy.
```

---

## 9. Deploy-State Receipt

Every deploy **must** write a deploy-state receipt. Schema:

```json
{
  "surface": "arif-fazil.com",
  "deployed_at": "20260716T080000Z",
  "source_commit": "bf2bdcb",
  "previous_target": "20260715T120000Z",
  "swap_type": "symlink",
  "receipt_hash": "a1b2c3d4e5f6...",
  "tools_deployed": 14,
  "caddy_config_hash": "f6e5d4c3b2a1...",
  "organs_healthy": {
    "arifos": 200,
    "aforge": 200
  },
  "organs_deployed": {
    "arifos_tools": 17,
    "aforge_tools": 60
  }
}
```

Located at `https://<surface>/api/deploy-state.json`.

For SOUL (symlink-swapped): lives inside the release — replaced each deploy.
For MIND/BODY (direct): persists across updates if the deploy tool writes it.

---

## Floor Compliance

| Floor | How this layout satisfies it |
|-------|------------------------------|
| **F1 AMANAH** | Symlink swap = atomic. Fallback dir = instant rollback. Previous release preserved. |
| **F2 TRUTH** | deploy-state.json records actual deployed commit, time, and health. |
| **F4 CLARITY** | One canonical `_shared/` for all shared assets. No duplication. ΔS ≤ 0. |
| **F8 LAW** | Caddy routes are deterministic, documented, and match live config. |
| **F11 AUDIT** | Every deploy writes a receipt. Rollback is a recorded event. |
| **F13 SOVEREIGN** | `deploy-site.sh --dry-run` default — `--apply` requires explicit sovereign intent. |

---

*Canonical: 2026-07-16 · Part of ARIF-SITES governance surface.*
*DITEMPA BUKAN DIBERI*
