# FastMCP Session ID Format Mismatch

## The Problem

FastMCP 3.4.4 (streamable-HTTP transport) generates session IDs as raw hex:
`8f8a874b0cc7441584b61ef2e03a2332`

GEOX `validate_session()` only recognizes:
- `act_v1.*` — SCT tokens
- `SEAL-*` (≥12 chars) — kernel-verified sessions
- `ANON-*` — auto-minted anonymous sessions
- `None`/empty — triggers auto-mint in validation

Raw hex FastMCP session IDs fall through to PATH 3 → `SESSION_INVALID`.

## The Layer Ordering Constraint

FastMCP resolves `Mcp-Session-Id` from the HTTP header at the transport
layer, BEFORE any middleware `on_call_tool` hook fires. This means:

- **No header at all** → FastMCP rejects with HTTP 400 before middleware.
  Auto-mint in middleware cannot help. Client must initialize first.
- **Header with raw hex SID** → FastMCP passes through. Middleware fires.
  But `validate_session()` rejects the raw hex.

## The Fix: Middleware Injection Pattern

In `geox_middleware.py` `on_call_tool()`, BEFORE the authority gate:

1. Extract the header SID via `request_context.request.headers`
2. Check if it has a GEOX prefix (`act_v1.`, `SEAL-`, `ANON-`)
3. If GEOX-recognized → pass through as `arguments.session_id`
4. If NOT recognized (raw hex) → mint a fresh `ANON-{uuid}` for arguments
5. Always inject `actor_id="auto-anon"` if missing

The header SID stays untouched (FastMCP transport needs it for session
management). Only `arguments.session_id` gets the ANON-* value.

### Key code shape

```python
hdr_sid = _ensure_session_header(headers, tool_name)
_GEOX_PREFIXES = ("act_v1.", "SEAL-", "ANON-")
if hdr_sid and any(hdr_sid.startswith(p) for p in _GEOX_PREFIXES):
    effective_sid = hdr_sid
else:
    effective_sid = f"ANON-{uuid.uuid4().hex[:16]}"
if "session_id" not in arguments:
    arguments["session_id"] = effective_sid
if "actor_id" not in arguments:
    arguments["actor_id"] = "auto-anon"
```

## Debugging: How to Tell Which Failure You're Hitting

| Symptom | Cause | Fix |
|---------|-------|-----|
| HTTP 400 "Missing session ID" | No header at all; FastMCP rejects before middleware | Client must `initialize` first |
| `SESSION_BINDING · HOLD · SESSION_INVALID` | Header SID is raw hex, passed through | Middleware must mint ANON-* for arguments |
| `P0_IDENTITY_PROPAGATION · HOLD · actor_id is 'anonymous'` | SID absent from arguments, no actor_id | Inject both session_id and actor_id |
| `SESSION_VALID` + tool result | Auto-mint worked | ✓ |

## Behavioral Comparison

**Before auto-mint middleware** (raw hex SID → arguments):
```
P0_IDENTITY_PROPAGATION · verdict=HOLD · actor_id is 'anonymous'
```

**After naive auto-mint** (raw hex SID → arguments as-is):
```
SESSION_BINDING · verdict=HOLD · SESSION_INVALID — session_id format not recognized
```

**After correct auto-mint** (ANON-* minted for unrecognized SIDs):
```json
{"isError": false, "session_id": "ANON-ee67d1989b2d4125", "actor_id": "auto-anon"}
```
