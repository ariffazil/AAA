# Human Inference MCP Server

FastMCP server implementing the **Human Meaning Inference Protocol** from the [human-meaning-membrane](/root/AAA/skills/human-meaning-membrane/) governance doctrine.

## What It Does

Exposes a `human_inference` tool that takes a raw observation + contextual grounding and returns a structured JSON inference record validated against the official schema. Every human interpretation MUST pass through this schema before action.

## Governance Rules (Non-Negotiable)

| Rule | Enforcement |
|------|-------------|
| Min 3 candidate interpretations | Auto-appended if fewer provided |
| Confidence hard-capped at 0.9 | Clamped on input |
| Consent defaults to UNKNOWN | Override only with evidence |
| Projection defaults to MEDIUM | Explicit override accepted |
| action_authority defaults to HUMAN_CONFIRMATION_REQUIRED | READ_ONLY only when explicitly safe |

## Install & Run

```bash
cd /root/AAA/mcp-servers/human-inference
pip install -e .
human-inference          # starts MCP server on stdio
```

Or run directly:

```bash
python server.py
```

## Tool: `human_inference`

### Inputs

| Parameter | Type | Required | Default |
|-----------|------|----------|---------|
| `observation` | string | **yes** | — |
| `context` | string | **yes** | — |
| `candidate_interpretations` | string[] | no | auto-generated |
| `unknowns` | string[] | no | auto-generated |
| `projection_risk` | enum | no | `MEDIUM` |
| `verification_path` | string | no | placeholder |
| `consent_status` | enum | no | `UNKNOWN` |
| `action_authority` | enum | no | `HUMAN_CONFIRMATION_REQUIRED` |
| `confidence_band` | [float, float] | no | `[0.3, 0.7]` |

### Output

```json
{
  "valid": true,
  "record": {
    "observation": "...",
    "context": "...",
    "candidate_interpretations": ["...", "...", "..."],
    "unknowns": ["..."],
    "projection_risk": "MEDIUM",
    "verification_path": "...",
    "consent_status": "UNKNOWN",
    "action_authority": "HUMAN_CONFIRMATION_REQUIRED",
    "confidence_band": [0.3, 0.7]
  }
}
```

Validation failures return `"valid": false` with error details.

## Resource: `human-meaning-membrane://inference-schema`

Exposes the raw JSON Schema for introspection.

## Schema

Loaded from `/root/AAA/skills/human-meaning-membrane/references/inference-schema.json` at startup. Falls back to an inline copy if the file is absent.

## Dependencies

- `fastmcp>=2.0.0`
- `jsonschema>=4.0.0`

## arifOS Context

This server is part of the arifOS federation. The human-meaning-membrane doctrine governs how agents model human meaning — the void between what humans SAY and what they MEAN. This server operationalizes that doctrine as a composable MCP tool.
