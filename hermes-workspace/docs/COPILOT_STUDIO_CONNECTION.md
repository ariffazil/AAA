# Connect Copilot Studio to arifOS MCP

**Method A: MCP Connector**
**Method B: A2A Agent Delegation**

---

## METHOD A: MCP Connector (Direct)

### Step 1: Get MCP Endpoint Info

**Endpoint:** `https://mcp.arif-fazil.com/mcp`
**Auth:** Bearer token (or `none` for testing)
**Protocol:** JSON-RPC 2.0 over HTTPS

### Step 2: Create Custom Connector in Copilot Studio

1. Go to **Copilot Studio** → Your agent → **Tools** → **Add a tool**
2. Select **Custom Connector** → **Create from scratch**
3. Fill in:
   - **Name:** `arifOS MCP`
   - **Description:** `arifOS constitutional governance kernel with F1-F13 floors`
   - **Base URL:** `https://mcp.arif-fazil.com`
   - **Authentication:** `None` or `Bearer` with token

### Step 3: Define Actions (Import from OpenAPI or manual)

Import or create these actions:

| Action | Method | Description |
|--------|--------|-------------|
| `arifos_000_init` | POST | Initialize constitutional session |
| `arifos_111_sense` | POST | Grounding and intent classification |
| `arifos_222_witness` | POST | Reality verification & consensus |
| `arifos_333_mind` | POST | First-principles reasoning |
| `arifos_444_kernel` | POST | Metabolic route dispatcher |
| `arifos_555_memory` | POST | Governed recall & context |
| `arifos_666_heart` | POST | Safety & consequence modeling |
| `arifos_777_ops` | POST | Capacity & thermodynamic estimation |
| `arifos_888_judge` | POST | Sovereign verdict rendering |
| `arifos_999_vault` | POST | Immutable audit ledger |
| `arifos_forge` | POST | Constitutional execution |

### Step 4: Import Schema (Optional)

Use this OpenAPI spec for the MCP:

```yaml
openapi: 3.0.0
info:
  title: arifOS MCP
  version: 46.2
servers:
  - url: https://mcp.arif-fazil.com
paths:
  /mcp:
    post:
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                jsonrpc:
                  type: string
                  enum: ["2.0"]
                id:
                  type: string
                method:
                  type: string
                params:
                  type: object
      responses:
        200:
          description: MCP response
```

### Step 5: Test Connection

Use Copilot Studio's test pane to send:

```json
{
  "jsonrpc": "2.0",
  "id": "test-001",
  "method": "arifos_000_init",
  "params": {
    "operator_id": "arif",
    "session_id": null,
    "epoch": null,
    "context": null
  }
}
```

**Expected response:**
```json
{
  "jsonrpc": "2.0",
  "id": "test-001",
  "result": {
    "verdict": "SEAL",
    "session_id": "...",
    ...
  }
}
```

---

## METHOD B: A2A Agent Connection

### Why A2A?

A2A lets Copilot Studio **delegate tasks** to external agents, not just call single tools. The agent works autonomously, returns structured results.

### Setup in Copilot Studio

1. Go to **Agents** → Select your agent → **Add an agent**
2. Select **Connect to an external agent** → **Agent2Agent**
3. Fill in:
   - **Endpoint URL:** `https://aaa.arif-fazil.com/a2a/message/send`
   - **Name:** `AAA Gateway`
   - **Description:** `Governed agent gateway for AAA with arifOS F1-F13 constitutional floors. Skills: agent-dispatch, agent-handoff, status-query.`
   - **Authentication:** `None`

4. Click **Create** → **Add and configure**

### Test A2A Connection

Send a test message:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "Hello, what can you do?"}],
      "messageId": "test-001"
    }
  }
}
```

**Expected response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "aaa-xxxxx",
    "contextId": "...",
    "status": {"state": "completed", ...},
    "kind": "task"
  }
}
```

### A2A Endpoints Available

| Endpoint | Purpose |
|----------|---------|
| `/.well-known/agent.json` | Agent Card (discovery) |
| `/message/send` | Submit task (blocking) |
| `/message/stream` | Submit task (SSE streaming) |
| `/tasks/:taskId` | Get task status |
| `/tasks/:taskId/cancel` | Cancel task |
| `/tasks/:taskId/subscribe` | SSE subscribe to updates |
| `/health` | Health check |

### A2A Skills

| Skill | Triggers | Description |
|-------|---------|-------------|
| `agent-dispatch` | "dispatch", "send", "task" | Task dispatch to specialists |
| `agent-handoff` | "handoff", "transfer", "delegate" | Context handoff |
| `status-query` | "status", "check", "query" | Read-only status |

---

## DEPLOYMENT: A2A Server (if using Method B)

### Quick Deploy Options

**Option 1: Railway/Render (Fastest)**

```bash
# Clone AAA repo
git clone https://github.com/ariffazil/AAA.git
cd AAA

# Edit package.json - remove @a2a-js/sdk if causing issues
# Remove the line: "@a2a-js/sdk": "^0.1.0",

# Deploy to Railway/Render with:
npm install
npm run a2a:server
```

**Option 2: VPS with PM2**

```bash
# On your VPS
git clone https://github.com/ariffazil/AAA.git /root/aaa-a2a
cd /root/aaa-a2a

# Remove problematic dependency
sed -i '/"@a2a-js\/sdk"/d' package.json

# Install and start
npm install --production
pm2 start src/lib/a2a/server.ts --name aaa-a2a -- \
  --port 3001 \
  --domain aaa.arif-fazil.com

# Configure nginx for HTTPS
```

**Option 3: Docker**

```bash
# Build
docker build -f src/lib/a2a/Dockerfile -t aaa-a2a-server .

# Run
docker run -d -p 3001:3001 \
  --name aaa-a2a \
  -e PORT=3001 \
  aaa-a2a-server
```

### Nginx Config for A2A

```nginx
server {
    listen 443 ssl;
    server_name aaa.arif-fazil.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location /a2a {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /.well-known/agent.json {
        proxy_pass http://localhost:3001;
    }
}
```

---

## VERIFICATION CHECKLIST

- [ ] MCP endpoint responds: `curl https://mcp.arif-fazil.com/mcp -d '{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}'`
- [ ] A2A server running (if using Method B)
- [ ] Copilot Studio connector created
- [ ] Test call successful
- [ ] arifOS responds with SEAL/HOLD/VOID verdict

---

## AGENT CARD (for A2A discovery)

```json
{
  "protocol_version": "0.3.0",
  "id": "aaa-gateway",
  "name": "AAA Gateway",
  "description": "Governed agent gateway for AAA. Exposes only approved delegation and coordination surfaces.",
  "url": "https://aaa.arif-fazil.com/a2a",
  "preferred_transport": "jsonrpc-https",
  "capabilities": {
    "streaming": true,
    "push_notifications": false,
    "authenticated_extended_card": false
  },
  "skills": [
    {"id": "agent-dispatch", "name": "Agent Dispatch", "description": "..."},
    {"id": "agent-handoff", "name": "Agent Handoff", "description": "..."},
    {"id": "status-query", "name": "Status Query", "description": "..."}
  ]
}
```

---

## QUICK TEST: MCP Call (Paste into Copilot Studio Test Pane)

```json
{
  "jsonrpc": "2.0",
  "id": "quick-test",
  "method": "arifos_888_judge",
  "params": {
    "evidence_bundle": {
      "metrics": {
        "delta_s": 0.5,
        "omega_0": 0.9,
        "readiness_probe": 0.85
      }
    },
    "operator_id": "arif",
    "session_id": "test-123"
  }
}
```

Expected: Returns `{verdict: "SEAL"|"HOLD"|"VOID", ...}`

---

## NEXT STEPS

1. Choose Method A (MCP) or Method B (A2A) or both
2. Follow the steps above
3. Test with the quick test payloads
4. Confirm connection in Copilot Studio test pane

**DITEMPA BUKAN DIBERI — Evidence or Unknown, never guessed.**