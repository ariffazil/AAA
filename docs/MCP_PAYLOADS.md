# arifOS MCP — Ready-to-Use Payloads

**Base URL:** `https://mcp.arif-fazil.com/mcp`
**Protocol:** JSON-RPC 2.0 over HTTPS
**Auth:** Bearer token (or none for testing)

---

## 1. MCP Handshake (Test Connection)

```bash
curl -X POST https://mcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "arifOS-handshake-001",
    "method": "arifos_000_init",
    "params": {
      "operator_id": "arif",
      "session_id": null,
      "epoch": null,
      "context": null
    }
  }'
```

---

## 2. Core arifOS MCP Calls

### 2.1 Initialize Session (arifos_000_init)

```json
{
  "jsonrpc": "2.0",
  "id": "init-001",
  "method": "arifos_000_init",
  "params": {
    "operator_id": "arif",
    "session_id": null,
    "context": {
      "source": "Microsoft Copilot Studio",
      "intent": "establish_governance_channel"
    }
  }
}
```

### 2.2 Constitutional Sensing (arifos_111_sense)

```json
{
  "jsonrpc": "2.0",
  "id": "sense-001",
  "method": "arifos_111_sense",
  "params": {
    "query": "What is the current operational status of all wells?",
    "mode": "grounded",
    "session_id": "session-123",
    "operator_id": "arif"
  }
}
```

### 2.3 Reality Verification (arifos_222_witness)

```json
{
  "jsonrpc": "2.0",
  "id": "witness-001",
  "method": "arifos_222_witness",
  "params": {
    "query": "Verify the STOIIP calculation for Field A",
    "mode": "fuse",
    "depth": "basic",
    "session_id": "session-123",
    "operator_id": "arif"
  }
}
```

### 2.4 Constitutional Verdict (arifos_888_judge)

```json
{
  "jsonrpc": "2.0",
  "id": "judge-001",
  "method": "arifos_888_judge",
  "params": {
    "evidence_bundle": {
      "metrics": {
        "delta_s": 0.5,
        "omega_0": 0.9,
        "readiness_probe": 0.85
      },
      "source": "Copilot Studio request",
      "intent": "execute_production_decision"
    },
    "operator_id": "arif",
    "session_id": "session-123"
  }
}
```

### 2.5 Vault Seal (arifos_999_vault)

```json
{
  "jsonrpc": "2.0",
  "id": "vault-001",
  "method": "arifos_999_vault",
  "params": {
    "action": "seal",
    "payload": {
      "event": "MCP connection established from Copilot Studio",
      "operator": "arif",
      "timestamp": "2026-04-22T17:30:00Z"
    },
    "operator_id": "arif",
    "session_id": "session-123"
  }
}
```

### 2.6 Memory Query (arifos_555_memory)

```json
{
  "jsonrpc": "2.0",
  "id": "memory-001",
  "method": "arifos_555_memory",
  "params": {
    "action": "query",
    "query": "What are the last 3 decisions made by arifOS?",
    "operator_id": "arif",
    "session_id": "session-123"
  }
}
```

### 2.7 Heart Safety Check (arifos_666_heart)

```json
{
  "jsonrpc": "2.0",
  "id": "heart-001",
  "method": "arifos_666_heart",
  "params": {
    "stakeholder_map": {
      "operators": ["arif"],
      "impacted_parties": ["production", "safety"]
    },
    "action_proposal": {
      "action": "deploy_new_well",
      "target": "Field A Block 7",
      "reversibility": "low"
    },
    "operator_id": "arif",
    "session_id": "session-123"
  }
}
```

---

## 3. Copilot Studio Custom Connector Config

### Connector Settings

| Field | Value |
|-------|-------|
| **Name** | arifOS MCP |
| **Base URL** | `https://mcp.arif-fazil.com` |
| **Authentication** | None (or Bearer token) |
| **Content-Type** | application/json |

### OpenAPI Spec (paste into Copilot Studio)

```yaml
openapi: 3.0.0
info:
  title: arifOS MCP Gateway
  version: 46.2
  description: Constitutional AI governance kernel with F1-F13 floors
servers:
  - url: https://mcp.arif-fazil.com
    description: arifOS MCP endpoint
paths:
  /mcp:
    post:
      summary: MCP JSON-RPC endpoint
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                jsonrpc:
                  type: string
                  enum: ["2.0"]
                id:
                  oneOf:
                    - type: string
                    - type: number
                method:
                  type: string
                  description: "arifos_000_init | arifos_111_sense | arifos_222_witness | arifos_333_mind | arifos_444_kernel | arifos_555_memory | arifos_666_heart | arifos_777_ops | arifos_888_judge | arifos_999_vault | arifos_forge | arifos_sabar"
                params:
                  type: object
                  properties:
                    operator_id:
                      type: string
                    session_id:
                      type: string
                    query:
                      type: string
                    mode:
                      type: string
                      enum: [grounded, visual, fuse, search]
                    evidence_bundle:
                      type: object
                    action:
                      type: string
                    payload:
                      type: object
              required:
                - jsonrpc
                - method
                - params
      responses:
        '200':
          description: MCP JSON-RPC Response
          content:
            application/json:
              schema:
                type: object
                properties:
                  jsonrpc:
                    type: string
                  id:
                    oneOf:
                      - type: string
                      - type: number
                  result:
                    type: object
                  error:
                    type: object
                    properties:
                      code:
                        type: number
                      message:
                        type: string
```

---

## 4. A2A Connection Config (for AAA Gateway)

### A2A Agent Connection in Copilot Studio

| Field | Value |
|-------|-------|
| **Endpoint URL** | `https://aaa.arif-fazil.com/a2a/message/send` |
| **Name** | AAA Gateway |
| **Description** | Governed agent gateway with arifOS F1-F13 constitutional floors |
| **Authentication** | None |

### A2A Test Call

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

### A2A Agent Card (Discovery)

**URL:** `https://aaa.arif-fazil.com/.well-known/agent.json`

```json
{
  "protocol_version": "0.3.0",
  "id": "aaa-gateway",
  "name": "AAA Gateway",
  "description": "Governed agent gateway for AAA with arifOS constitutional floors",
  "url": "https://aaa.arif-fazil.com/a2a",
  "preferred_transport": "jsonrpc-https",
  "capabilities": {
    "streaming": true,
    "push_notifications": false,
    "authenticated_extended_card": false
  },
  "skills": [
    {"id": "agent-dispatch", "name": "Agent Dispatch", "description": "Task dispatch to specialists"},
    {"id": "agent-handoff", "name": "Agent Handoff", "description": "Context handoff workflows"},
    {"id": "status-query", "name": "Status Query", "description": "Read-only status retrieval"}
  ]
}
```

---

## 5. Quick Test All

### Test MCP (paste in terminal):

```bash
curl -s -X POST https://mcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"test","method":"tools/list","params":{}}' | head -c 500
```

### Test A2A (paste in terminal):

```bash
curl -s -X POST https://aaa.arif-fazil.com/a2a/message/send \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"message/send","params":{"message":{"role":"user","parts":[{"kind":"text","text":"test"}],"messageId":"test-1"}}}'
```

---

## 6. Deploy AAA A2A Server

### Option A: Clone and run (VPS)

```bash
# Clone
git clone https://github.com/ariffazil/AAA.git /root/aaa-a2a

# Install minimal deps
cd /root/aaa-a2a
npm install express

# Copy server
cp a2a-server/server.js /root/aaa-a2a-server/
cd /root/aaa-a2a-server
npm init -y
npm install express

# Run
node server.js
```

### Option B: Docker

```bash
# Build
docker build -t aaa-a2a-server - <<'EOF'
FROM node:20-alpine
WORKDIR /app
RUN npm install express
COPY server.js .
EXPOSE 3001
CMD ["node", "server.js"]
EOF

# Run
docker run -d -p 3001:3001 --name aaa-a2a aaa-a2a-server
```

### Option C: PM2 (VPS)

```bash
npm install -g pm2
git clone https://github.com/ariffazil/AAA.git /root/aaa-a2a
cp /root/AAA/a2a-server/server.js /root/aaa-a2a-server/
cd /root/aaa-a2a-server
npm init -y && npm install express
pm2 start server.js --name aaa-a2a
pm2 save
```

---

## 7. Nginx Config (for HTTPS on VPS)

```nginx
server {
    listen 443 ssl;
    server_name aaa.arif-fazil.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    location /a2a {
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
    }

    location /.well-known/agent.json {
        proxy_pass http://127.0.0.1:3001;
    }
}
```

---

**DITEMPA BUKAN DIBERI — Evidence or Unknown, never guessed.**