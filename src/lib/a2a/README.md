# A2A Server for AAA Gateway

**Protocol:** A2A v0.3.0 (Linux Foundation Agent2Agent)
**Governance:** arifOS F1-F13 Constitutional Floors
**Motto:** DITEMPA BUKAN DIBERI — Forged, Not Given

## Overview

This A2A server implements the Agent2Agent protocol for the AAA gateway, enabling:
- Agent discovery via Agent Card
- Task submission and lifecycle management
- Real-time SSE streaming for long-running tasks
- Constitutional governance on all agent interactions
- Bearer/API Key/OAuth2 authentication
- Push notification support
- Authenticated extended card endpoint

## Quick Start

```bash
# Install dependencies
npm install

# Start A2A server
npm run a2a:server

# Or with watch mode for development
npm run a2a:dev
```

Server runs on `http://localhost:3001` by default.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/.well-known/agent.json` | Agent Card for discovery (public) |
| GET | `/agent.json` | Agent Card alias (public) |
| GET | `/a2a/agent/authenticatedExtendedCard` | Extended card (auth required) |
| POST | `/message/send` | Submit task (blocking) |
| POST | `/message/stream` | Submit task (SSE streaming) |
| GET | `/tasks/:taskId` | Get task status |
| GET | `/tasks` | List tasks with optional filters |
| POST | `/tasks/:taskId/cancel` | Cancel a task |
| POST | `/tasks/:taskId/pushNotificationConfig/set` | Set push notification |
| GET | `/tasks/:taskId/pushNotificationConfig/get` | Get push notification config |
| GET | `/tasks/:taskId/subscribe` | SSE subscribe to task updates |
| GET | `/health` | Health check (public) |

## Authentication

The A2A server supports multiple authentication schemes:

| Scheme | Header | Use Case |
|--------|-------|----------|
| Bearer | `Authorization: Bearer <token>` | Internal trusted peers |
| API Key | `X-API-Key: <key>` | Fixed infrastructure peers |
| OAuth 2.0 | Via authorization flow | User-linked or federated callers |
| None | - | Development/testing |

### Example Request with Bearer Token

```bash
curl -X POST http://localhost:3001/message/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer my-secret-token" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "Hello A2A"}],
        "messageId": "test-123"
      }
    }
  }'
```

## Skills

The AAA Gateway supports these skills:

| Skill ID | Name | Description |
|----------|------|-------------|
| `agent-dispatch` | Agent Dispatch | Non-blocking supervised task dispatch |
| `agent-handoff` | Agent Handoff | Delegation through governed handoff |
| `status-query` | Status Query | Read-only task and run status retrieval |

## Skills Detection

The executor automatically detects skills from message content:

- **agent-dispatch**: Contains "dispatch", "send", "task"
- **agent-handoff**: Contains "handoff", "transfer", "delegate"
- **status-query**: Contains "status", "check", "query"

## Task States

| State | Description |
|-------|-------------|
| `submitted` | Task received, processing started |
| `working` | Task actively being processed |
| `input-required` | Needs more input (888_HOLD) |
| `completed` | Task successfully completed |
| `failed` | Task failed (VOID verdict) |
| `canceled` | Task cancelled by client |

## Push Notifications

Configure push notifications to receive task updates at a webhook URL:

```bash
curl -X POST http://localhost:3001/tasks/{taskId}/pushNotificationConfig/set \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tasks/pushNotificationConfig/set",
    "params": {
      "pushNotificationConfig": {
        "url": "https://my-app.com/webhook",
        "token": "secure-token"
      }
    }
  }'
```

## Architecture

```
                    ┌─────────────────────────────────────────┐
                    │              AAA Gateway                 │
                    │                                         │
  Client ───────► │  /.well-known/agent.json (discovery)     │
                    │                                         │
                    │  /message/send ──► TaskStore            │
                    │        │                │               │
                    │        ▼                ▼               │
                    │  AAAAgentExecutor ──► EventBus (SSE)     │
                    │        │                                  │
                    │        ▼                                  │
                    │  Constitutional Governance (F1-F13)      │
                    │                                         │
                    │  /a2a/agent/authenticatedExtendedCard   │
                    │                                         │
                    └─────────────────────────────────────────┘
```

## Client Usage

```typescript
import { createA2AClient, dispatchToAgent } from './client';

// Basic usage
const client = createA2AClient('http://localhost:3001', {
  auth: { type: 'bearer', token: 'your-token' }
});

const task = await client.sendMessage({
  role: 'user',
  parts: [{ kind: 'text', text: 'Analyze reservoir data' }],
  messageId: crypto.randomUUID(),
});

// Using preset agents
await dispatchToAgent('GEOX', 'Process well log data');
```

## Running Tests

```bash
# Start the server in one terminal
npm run a2a:server

# In another terminal, run tests
npx tsx src/lib/a2a/test.ts
```

## Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose -f src/lib/a2a/docker-compose.yml up -d

# Or build manually
docker build -f src/lib/a2a/Dockerfile -t aaa-a2a-server .
docker run -p 3001:3001 aaa-a2a-server
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3001 | Server port |
| `NODE_ENV` | development | Environment mode |
| `A2A_AUTH_BEARER_TOKEN` | - | Bearer token for auth |
| `A2A_AUTH_API_KEY` | - | API key for auth |

## Related

- [A2A Protocol Spec](https://a2aprotocol.ai/docs/)
- [arifOS Documentation](../../docs/)
- [AAA Gateway README](../../README.md)