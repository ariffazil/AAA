# MCP Constitutional Gateway

> arifOS admission controller for all MCP tool calls.

## Pattern

```
MCP tool advertisement → arifOS risk classification → lease → execution → VAULT999
```

## Pre-Flight Checks

Before allowing any MCP tool call:

| Check | What It Verifies | Failure Action |
|-------|-----------------|---------------|
| Tool description review | Description matches actual behavior | VOID if malicious/misleading |
| Scope declaration | Filesystem, network, secrets access | HOLD if undeclared scope |
| Secrets risk | Tool reads/writes credentials | HOLD + human review |
| Side effects | Read-only vs mutating vs destructive | HOLD if destructive |
| Network access | Tool contacts external URLs | HOLD if unexpected |
| Human consent | Is consent needed per F6/F13 | Gate accordingly |
| Lease generation | arifOS issues scoped lease | HOLD if unleaseable |

## Classification

| Category | Example | Gate |
|----------|---------|------|
| Read-only safe | `read_file`, `search_web` | Auto-allow + log |
| Read with sensitive scope | `list_secrets`, `read_db` | Lease + audit |
| Mutating local | `write_file`, `patch` | Lease + rollback + receipt |
| Mutating infrastructure | `deploy`, `restart_service` | 888 SEAL + VAULT999 |
| Destructive | `delete`, `drop_table` | 888 SEAL + F13 review |
| External communication | `send_email`, `post_webhook` | Consent + lease + receipt |

## Contract

**Request** (MCP tool → Gateway):
```json
{
  "tool_name": "geox_basin_profile",
  "tool_description": "Retrieve basin-level intelligence",
  "arguments": {"basin_name": "Malay Basin"},
  "advertised_scope": "read_only",
  "advertised_network_access": false,
  "advertised_secrets_access": false
}
```

**Response** (Gateway → MCP tool):
```json
{
  "admitted": true,
  "verdict": "SEAL",
  "lease_id": "LEASE-MCP-001",
  "scope": "read_only",
  "vault999_receipt": "RECEIPT-...",
  "expires_at": "2026-06-14T17:00:00Z"
}
```

## Status

| Component | Status |
|-----------|--------|
| Risk classification schema | ✅ Defined |
| Description review | 🔲 Not implemented |
| Scope declaration check | 🔲 Not implemented |
| Lease generation | 🔲 Not implemented |
| Audit to VAULT999 | 🔲 Not implemented |
| Tests | 🔲 Not implemented |

## Eureka

MCP connects tools. arifOS decides whether the tool deserves a key.
