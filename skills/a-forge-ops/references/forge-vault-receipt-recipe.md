# forge_vault(mode="receipt") — Lane B Working Recipe (A-FORGE :7071/mcp)

> Session: 2026-08-08 APEX Theory mapping. Three failure modes hit and corrected.

---

## TL;DR

`forge_vault` is a **stateful MCP tool** on `:7071/mcp`. It requires (1) `initialize` handshake that returns a `Mcp-Session-Id` header, (2) that header on every subsequent call, and (3) receipt `content` that does not self-claim F13 authority.

---

## The Working Sequence

```bash
source /root/.secrets/kunci-mas.env

# 1) Initialize — capture the Mcp-Session-Id header
INIT=$(curl -i -s -X POST http://127.0.0.1:7071/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize",
       "params":{"protocolVersion":"2025-03-26",
                 "capabilities":{},
                 "clientInfo":{"name":"hermes-asi","version":"1.0"}}}')
SID=$(echo "$INIT" | grep -i "^mcp-session-id" | cut -d' ' -f2 | tr -d '\r\n')
echo "SID=$SID"
# → SESSION_ID=305b1730-c07f-4d71-baac-d4b6a2a0582c

# 2) Call forge_vault WITH the session header
curl -s -X POST http://127.0.0.1:7071/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{
    "jsonrpc":"2.0","id":3,"method":"tools/call",
    "params":{"name":"forge_vault","arguments":{
      "mode":"receipt",
      "name":"apex-mapping-2026-08-08",
      "content":"<summary — see F12 pitfall below>",
      "reason":"SESSION_CLOSE",
      "tier":"session.ledger",
      "category":"session.receipt",
      "actor_id":"arif",
      "session_id":"apex-mapping-2026-08-08"
    }}
  }'
# → {"result":{"content":[{"type":"text","text":"...\"status\":\"written\"..."}]}}}
```

---

## Three Traps Hit This Session

### Trap 1 — Wrong endpoint path
`POST /vault/receipt` → `Cannot POST /vault/receipt` (404).
**All A-FORGE MCP routes go through `/mcp`.** Use `tools/list` to discover surface (115 tools, 22 stateless-HTTP, 93 session-required).

### Trap 2 — Missing `Mcp-Session-Id` header
Without it: `{"error":{"code":-32000,"message":"Bad Request: Mcp-Session-Id header is required"}}`.
**Fix:** use `curl -i` during `initialize` to see headers; grep + pass on subsequent calls.

### Trap 3 — F12 AUTHORITY_SMUGGLING (the constitutional gate)
Agent-authored receipt text containing F13 self-claim triggers F12 VOID:

```json
{
  "floor": "F12",
  "code": "AUTHORITY_SMUGGLING",
  "severity": "VOID",
  "message": "F12 INJECTION: text attempts to self-authorize F13/sovereign: /f13[_\\s-]?ratified/i"
}
```

**Rule:** receipt `content` describes *what happened*, not *what was authorized*. Cite the sealing document, not the authority.

| ❌ Triggers F12 | ✅ Safe phrasing |
|---|---|
| "F13 SOVEREIGN acknowledged..." | "Three corrections issued for sovereign review" |
| "F13 ratified..." | "Per CANON_APEX_V2/02 v2026.07.APEX.2" |
| "Constitutional ratification complete" | "Mapping + verification only; no new law forged" |
| "F13-approved..." | "Lane B receipt per SEAL.md doctrine — no constitutional threshold crossed" |

---

## Actor ID Canonicalization

- ✅ `actor_id: "arif"` (works)
- ❌ `actor_id: "ariffazil"` → `SCT_GATE: ACTOR_MISMATCH`
- Kernel canonicalizes `ariffazil` → `arif` inside the SCT.

---

## Lane B vs Lane A — Where to Verify

- **Lane B (this recipe)** writes to `session.ledger` tier. Verify by checking the tools/call response: `data.status == "written"`.
- **Lane A** (`arif_seal :8088`) writes to VAULT999 canonical chain. Verify with `curl -sf https://arif-fazil.com/999/verify`.

Lane B receipts do NOT appear in the canonical chain head. They're for session-close telemetry, not constitutional authorization.

---

## Checklist

- [ ] `source /root/.secrets/kunci-mas.env`
- [ ] POST `/mcp` with `initialize` method (use `curl -i`)
- [ ] Extract `Mcp-Session-Id` from response headers
- [ ] POST `/mcp` with `tools/call` + `Mcp-Session-Id` header
- [ ] `actor_id: "arif"` (canonicalized)
- [ ] Content avoids F13 self-claim language
- [ ] Verify response: `data.status == "written"`
- [ ] Update `carry_forward.json.sealed_to_vault999` if needed

*Pattern established 2026-08-08. Three failed attempts → one working call.*
