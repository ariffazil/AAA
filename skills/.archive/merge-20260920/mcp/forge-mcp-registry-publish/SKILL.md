---
name: forge-mcp-registry-publish
description: "Publish MCP to Smithery or Glama. Covers auth and namespace."
tags: [mcp, registry, publish, smithery, exposure]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# MCP Registry Publishing

> **"A registry entry is a claim. Verify it resolves before calling it deployed."**

## When to use

- Publishing an MCP server URL to Smithery, Glama, or similar registries
- Verifying a registry listing resolves correctly after publish
- Diagnosing namespace or auth issues during registry publish
- Adding MCP server metadata to registry-compatible config files (smithery.yaml, etc.)

## Core Procedure

### Step 1: Prepare the config file

For Smithery, the entry point is `smithery.yaml` in the repo root:

```yaml
startCommand: npx -y @smithery/cli run https://mcp.arif-fazil.com/mcp
configSchema:
  type: object
  properties: {}
```

Verify it exists and is committed: `git log --oneline -1 -- smithery.yaml`

### Step 2: Authenticate

Smithery uses API keys via environment variable, NOT `--api-key` flags:

```bash
SMITHERY_API_KEY=<key> npx -y @smithery/cli whoami
# → Namespace: arifbfazil  (this is YOUR namespace)
```

Key facts:
- `whoami` reveals the namespace bound to the key
- The namespace is the GitHub username or org, NOT a custom name
- Store the key in `/root/.secrets/kunci-root.env` as `SMITHERY_API_KEY=<value>`
- Never echo or log the key in chat or receipts

### Step 3: Publish

```bash
SMITHERY_API_KEY=<key> npx -y @smithery/cli mcp publish <endpoint-url> -n <namespace>/<server-name>
```

### Step 4: Verify

```bash
curl -sL -o /dev/null -w '%{http_code} -> %{url_effective}' https://smithery.ai/server/<namespace>/<name>
# Should return 200, not 404
```

## Scoped Tokens

```bash
SMITHERY_API_KEY=<key> npx -y @smithery/cli auth token \
  --policy '{"resources": "servers", "operations": "write", "namespaces": "<ns>", "ttl": "1h"}'
```

Policy fields: `resources` (servers/namespaces/skills/connections), `operations` (read/write/execute), `namespaces` (string or array), `ttl` (seconds or duration, max 24h).

## Common Errors

| Error | Meaning | Fix |
|---|---|---|
| `403: You don't have access to this namespace` | Key valid but namespace doesn't match | Run `whoami`; use correct `-n namespace/name` |
| `403: You don't own this server` | Namespace correct but needs web portal setup | smithery.ai Login Publish claim namespace |
| `unknown option '--api-key'` | Flag doesn't exist | Use env var: `SMITHERY_API_KEY=<key>` |
| `ENEEDAUTH` | No API key configured | Generate at smithery.ai/account/api-keys |

## Pitfalls

- **Namespace mismatch is the #1 blocker.** The key's bound namespace (from `whoami`) must match the `-n namespace/name` you pass.
- **First publish requires web portal linking.** The CLI cannot create a server entry from scratch — the namespace must first be claimed via the Smithery web UI. After that, CLI publishes work.
- **Search returns results even when server doesn't exist.** Always verify the exact URL resolves, not just search results.
- **Post-publish verification is mandatory.** A successful CLI publish does not guarantee the listing resolves.
- **A 308 redirect is not a 200.** Follow redirects (`-L`) and check final status. 308 to 404 means the name doesn't resolve.

## Related Skills

- `constitutional-deploy-gate` — governance gates for public surface deploys
- `forge-federation-manifest` — federation topology manifest

DITEMPA BUKAN DIBERI.