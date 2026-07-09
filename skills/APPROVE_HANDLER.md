# 888_APPROVE Handler — Sovereign Signature Flow

## Trigger
Message starts with `888_APPROVE\n`

## ⚑ CRITICAL OUTPUT RULE
After running the Python code, you MUST return EXACTLY ONE LINE of text:
```
MCP_JSON:{json}
```
Do NOT write any explanation. Do NOT describe what you did. Do NOT add markdown. Only output the MCP_JSON line. Nothing else.

## Step 1 — Parse the message
From the message `888_APPROVE\nraw:APPROVE HOLD-xxx\nchat:CHAT_ID\nmsg:MSG_ID`, extract:
- HOLD_NAME = the hold referenced in `raw:` (e.g. `HOLD-xxx`)
- CHAT_ID = the Telegram chat ID
- MSG_ID = the Telegram message ID

## Step 2 — Check if HOLD exists
Read `/root/.openclaw/workspace/AAA_HOLDS.md`. 
- If the hold does NOT exist → output: `MCP_JSON:{"status":"error","reason":"HOLD_not_found","hold":"<HOLD_NAME>"}`
- If the hold exists and status is COMPLETED → output: `MCP_JSON:{"status":"noop","reason":"already_completed","hold":"<HOLD_NAME>"}`

## Step 3 — Get constitution_hash + nonce
Run this Python code:
```python
import urllib.request, json, subprocess, time
req = urllib.request.Request("http://127.0.0.1:8080/mcp",
    data=json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"arif_session_init","arguments":{"mode":"init","actor_id":"ariffazil"}}}).encode(),
    headers={"Content-Type":"application/json","Accept":"application/json"},method="POST")
with urllib.request.urlopen(req) as resp:
    d = json.loads(resp.read().decode())
result = json.loads(d["result"]["content"][0]["text"])["result"]
constitution_hash = result["session"]["constitution_hash"]
nonce = f"apr_{int(time.time()*1000)}"
```

## Step 4 — Sign with Ed25519 sovereign key
```python
signer = "/root/arifOS/arifosmcp/runtime/sovereign_signer.py"
sig = subprocess.check_output(["python3", signer, "ariffazil", constitution_hash, nonce]).decode().strip()
```

## Step 5 — Call arif_session_init with SOVEREIGN signature
```python
req2 = urllib.request.Request("http://127.0.0.1:8080/mcp",
    data=json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/call",
        "params":{"name":"arif_session_init","arguments":{"mode":"init","actor_id":"ariffazil","nonce":nonce,"actor_signature":sig}}}).encode(),
    headers={"Content-Type":"application/json","Accept":"application/json"},method="POST")
with urllib.request.urlopen(req2) as resp2:
    d2 = json.loads(resp2.read().decode())
mcp_result = json.loads(d2["result"]["content"][0]["text"])
```

## Step 6 — Update hold status
Mark the hold as APPROVED in `/root/.openclaw/workspace/AAA_HOLDS.md`.

## Step 7 — Return MCP_JSON (ONLY output)
Extract from `mcp_result`:
- verdict, authority_level, identity_verified, signature_verified, session_id, constitution_hash, reasons

Then output EXACTLY this one line (no other text):
```
MCP_JSON:{"status":"approved","hold":"<HOLD_NAME>","verdict":"<verdict>","authority_level":"<auth_level>","identity_verified":<id_verified>,"signature_verified":<sig_verified>,"session_id":"<session_id>","constitution_hash":"<ch>","reasons":<reasons>,"chat_id":"<CHAT_ID>","msg_id":"<MSG_ID>"}
```

If arif_session_init fails (verdict=HOLD or VOID), output instead:
```
MCP_JSON:{"status":"rejected","hold":"<HOLD_NAME>","verdict":"<verdict>","reasons":<reasons>}
```

## Key facts
- Signer: `/root/arifOS/arifosmcp/runtime/sovereign_signer.py`
- MCP: `http://127.0.0.1:8080/mcp`
- Actor: `ariffazil` | Mode: `init` | Constitution hash: dynamic (fetch fresh)
- Output: MCP_JSON:{json} — ONE LINE ONLY — NO other text
