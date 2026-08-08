---
id: FORGE-did-web-identity
name: FORGE-did-web-identity
version: 1.0.0-2026.07.17
description: "Decentralized identifier (did:web) identity management for federation organs and agents."
owner: A-FORGE
risk_tier: high
floor_scope: ['F1', 'F2', 'F11', 'F13']
autonomy_tier: T2
---
# ⚒️ did:web Identity — Decentralized Identifier

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Implement and maintain `/.well-known/did.json` for federation organs under `arif-fazil.com`. Support `did:web` resolution, key management (verification methods), service endpoints, and rotation patterns.

## When to Use
- Setting up `did:web` identity for a new federation organ subdomain
- Updating verification methods (key rotation, addition, revocation)
- Adding service endpoints (MCP, A2A, WebMCP) to the DID document
- Resolving `did:web` identifiers from external agents or systems

## When NOT to Use
- Non-DID identity (API keys, JWTs) — use organ auth middleware
- Governance metadata — use `governance-jsonld`
- Federation topology — use `federation-manifest`

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Key rotation is irreversible once published; stage new keys before activating |
| F2 TRUTH | `did.json` must reflect live keys and endpoints — no phantom services |
| F4 CLARITY | One verification method per key type; no redundant entries |
| F11 AUDIT | Every key rotation logged to VAULT999 with receipt |
| F13 SOVEREIGN | Key material belongs to Arif; rotation requires sovereign approval |

## Commands & Patterns

```jsonc
// /.well-known/did.json — canonical structure
{
  "@context": ["https://www.w3.org/ns/did/v1"],
  "id": "did:web:arif-fazil.com",
  "verificationMethod": [{
    "id": "did:web:arif-fazil.com#key-1",
    "type": "Ed25519VerificationKey2020",
    "controller": "did:web:arif-fazil.com",
    "publicKeyMultibase": "z6Mkr..."
  }],
  "authentication": ["did:web:arif-fazil.com#key-1"],
  "assertionMethod": ["did:web:arif-fazil.com#key-1"],
  "service": [{
    "id": "did:web:arif-fazil.com#mcp",
    "type": "McpServer",
    "serviceEndpoint": "https://arifos.arif-fazil.com/mcp"
  }]
}
```

```bash
# Serve did.json via Caddy
# /etc/caddy/conf.d/did.conf
well-known {
    @did path /.well-known/did.json
    handle @did {
        root * /var/arifos/did
        file_server
    }
}
```

## Refusal Surface
- ❌ Using `did:key` or `did:eth` when `did:web` is the federation standard
- ❌ Hardcoding private key material in the DID document or source
- ❌ Multiple controllers per `did:web` — keep it single-controller
- ❌ Removing verification methods without verifying no active references
