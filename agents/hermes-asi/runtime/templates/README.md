# Hermes ASI Runtime Templates

Canonical templates for cross-agent communication and constitutional workflows.

## Templates

| Template | Path | Purpose |
|----------|------|---------|
| `888-judge-request.json` | `./888-judge-request.json` | Canonical APEXMax / arifOS 888_JUDGE deliberation payload |

## Usage

### 888_JUDGE Request

```bash
# Direct to APEXMax (port 3002)
curl -X POST http://localhost:3002/a2a/verdict \
  -H "Content-Type: application/json" \
  -d @/root/AAA/agents/hermes-asi/runtime/templates/888-judge-request.json

# Via arifOS MCP (port 8088)
curl -X POST http://localhost:8088/mcp/v1/tools/arif_judge_deliberate \
  -H "Content-Type: application/json" \
  -d @/root/AAA/agents/hermes-asi/runtime/templates/888-judge-request.json
```

## Governance

- All templates versioned under `arifos-888-judge-request-v1`
- Modifications require F13 SOVEREIGN approval
- Templates are read-only at runtime; copies are made per-session
