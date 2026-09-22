# llms.txt → mcp-ops workflow mapping (canonical alignment)

> **Source of truth:** `https://modelcontextprotocol.io/llms.txt` (parsed 2026-09-21).
> **Canon:** the Model Context Protocol is governed by 11 Working Groups, 7 Interest Groups,
> and a SEP (Specification Enhancement Proposal) lifecycle. This file maps every llms.txt
> section to its `mcp-ops` stage or "out of band (kept in reference)".

## Section → stage parity table

| llms.txt section | mcp-ops stage | Coverage |
|---|---|---|
| **getting-started/** | | |
| `intro` | 1 LEARN | covered (paraphrased) |
| `architecture` | 1 LEARN | covered (5 layers enumerated) |
| `server-concepts` | 1 LEARN | covered (tools/resources/prompts + utilities) |
| `client-concepts` | 1 LEARN | covered (sampling/elicitation/roots + deprecation note) |
| `versioning` | 1 LEARN | era table included |
| **develop/** | | |
| `connect-local-servers` | 3 PROBE | covered (handshake law) |
| `connect-remote-servers` | 3 PROBE | covered (transport + auth shape) |
| `build-with-agent-skills` | 4 BUILD | covered (Stage 3d) |
| `build-server` | 4 BUILD | covered (Stage 3a FastMCP scaffold) |
| `build-client` | 4 BUILD | covered (Stage 3c mcporter codegen) |
| `client-best-practices` | 4 BUILD | covered (Stage 3f: SEP-1303/1613/2106/986) |
| **sdks/** | 1 LEARN | covered (Tier table reference) |
| **tutorials/security/** | | |
| `authorization` | 5 SECURE | covered (5-step shape: discovery → PRM → registration → token → bearer) |
| `security_best_practices` | 5 SECURE | covered (Stage 4d) |
| **tools/** | | |
| `inspector` (overview) | 6 TEST | covered |
| `inspector/web` | 6 TEST | out-of-band (link) |
| `inspector/cli` | 6 TEST | covered (`npx @mcpjam/inspector@latest ...`) |
| `inspector/tui` | 6 TEST | out-of-band (link) |
| `inspector/configuration` | 6 TEST | covered (flags/env) |
| `inspector/authorization` | 6 TEST | covered (OAuth verification) |
| `inspector/protocol-eras` | 6 TEST | covered (legacy vs stateless negotiation) |
| `inspector/recipes` | 6 TEST | covered (transports/import/MCP Apps/Docker/network) |
| `debugging` | 6 TEST | covered |
| **examples.md** | n/a | out-of-band (link) |
| **specification/2026-07-28/** | | |
| `index`, `changelog`, `deprecated`, `architecture` | 1 LEARN | era reference |
| `basic/` (overview, `versioning`, `patterns/{mrtr,subscriptions,cancellation,progress}`) | 1 LEARN | referenced |
| `basic/transports/{stdio,streamable-http}` | 3 PROBE | covered (Stage 2a/3e) |
| `basic/authorization/{index,as-discovery,client-registration,security}` | 5 SECURE | covered |
| `client/{roots,sampling,elicitation}` | 1 LEARN | referenced (sampling/elicitation) + deprecation note for roots |
| `server/{index,discover,prompts,resources,tools}` | 4 BUILD | referenced |
| `server/utilities/{caching,completion,logging,pagination}` | 4 BUILD | referenced |
| **specification/2025-11-25 + earlier eras** | 3 PROBE | era coverage matrix in Stage 5 |
| **extensions/** | | |
| `overview` | 7 EXTEND | covered (four-extension paragraph) |
| `client-matrix` | 7 EXTEND | out-of-band (link) |
| `apps/overview` | 7a Apps | covered (Stage 3b + 7a) |
| `apps/build` | 7a Apps | covered |
| `auth/overview` | 7b Auth-ext | covered |
| `auth/oauth-client-credentials` | 5c M2M | covered (Stage 4c) |
| `auth/enterprise-managed-authorization` | 5b EAP | covered (Stage 4b) |
| `tasks/overview` | 7c Tasks | covered (Stage 6c) |
| `skills/overview` | 7d Skills-over-MCP | covered (Stage 6d + Stage 3d Build-with-Agent-Skills) |
| **registry/** | | |
| `about` | 8 PUBLISH | covered |
| `quickstart` | 8 PUBLISH | covered |
| `faq` | 8 PUBLISH | out-of-band (link) |
| `package-types` | 8 PUBLISH | out-of-band |
| `remote-servers` | 8 PUBLISH | out-of-band |
| `authentication` | 8 PUBLISH | covered (Stage 7e) |
| `versioning` | 8 PUBLISH | covered (Stage 7c) |
| `github-actions` | 8 PUBLISH | covered (Stage 7d) |
| `moderation-policy` | 8 PUBLISH | out-of-band (link) |
| `registry-aggregators` | 8 PUBLISH | covered (Stage 7b) |
| `terms-of-service` | 8 PUBLISH | out-of-band (link) |
| **seps/** | | |
| ~50 SEPs live in this dir; sampled into Stage 8a | 9 GOVERN | 16 SEPs mapped to federation work; rest out-of-band (link-only) |
| **community/** | | |
| `contributing` | 9 COMMUNITY | out-of-band (link) |
| `communication` | 9 COMMUNITY | out-of-band (link) |
| `working-interest-groups` | 9b WG/IG | covered (Stage 8b WG + IG list) |
| `charter-template` | 9 COMMUNITY | out-of-band (link) |
| `roadmap` | 9 COMMUNITY | out-of-band (link) |
| `design-principles` | 9 GOVERN | out-of-band (link) |
| `sep-guidelines` | 9 GOVERN | out-of-band (link) |
| `governance` | 9 GOVERN | covered (Stage 8e four mechanisms) |
| `contributor-ladder` | 9 GOVERN | out-of-band (link) |
| `feature-lifecycle` | 9c/9h | covered (Stage 8c Active/Deprecated/Removed + Stage 8h RETIRE) |
| `sdk-tiers` | 9d | covered (Stage 8d) |
| `security` (policy) | 5 SECURE | covered (Stage 4d) |
| `antitrust` | 9 GOVERN | out-of-band (link) |
| **working-groups** (11) | 9b | brief list (Stage 8b) |
| **interest-groups** (7) | 9b | brief list (Stage 8b) |

## Coverage delta vs v3.0.1 (the previous pass)

| Coverage surface | v3.0.1 | v3.1.0 |
|---|---|---|
| Learn (concepts, architecture, SDKs) | implicit only | **NEW Stage 0 LEARN** |
| Connect local/remote servers | partial (3-step handshake) | covered (Stage 2 PROBE) |
| Build with Agent Skills | not covered | **NEW Stage 3d** |
| Apps UI build recipes | partial | covered (4b + 7a) |
| Authorization (OAuth 2.1 + PRM + EAP) | brief mention | **NEW Stage 4 SECURE** (4 sub-stages) |
| Tools/Inspector (5 tabs) | partial | covered (Stage 5 + `absorbed-mcp-testing.md`) |
| Tasks extension | not covered | **NEW Stage 6c** |
| Skills-over-MCP (SEP-2640) | not covered | **NEW Stage 6d** |
| Client-credentials (SEP-1046) | not covered | **NEW Stage 4c** |
| Enterprise-Managed Auth (SEP-990) | not covered | **NEW Stage 4b** |
| MCP Registry full coverage | partial | covered (Stage 7 PUBLISH, 5 sub-stages) |
| SEP catalog (16 active SEPs) | not covered | **NEW Stage 8a SEP table** |
| Working Groups + Interest Groups | not covered | **NEW Stage 8b** |
| Feature Lifecycle | partial | covered (Stage 8c + 9h RETIRE) |
| SDK tiers | not covered | **NEW Stage 8d** |
| Design principles, sep-guidelines, contributor-ladder, security, antitrust | not covered | out-of-band (links preserved) |

## Sources cited inside mcp-ops v3.1.0

- `https://modelcontextprotocol.io/llms.txt` — parsed 2026-09-21
- `https://modelcontextprotocol.io/specification/2026-07-28/` — preferred modern era
- `https://modelcontextprotocol.io/specification/2025-11-25/` — legacy handshake
- `https://modelcontextprotocol.io/extensions/` — Apps / Auth-extensions / Tasks / Skills
- `https://modelcontextprotocol.io/registry/` — Registry + aggregators + moderation
- `https://modelcontextprotocol.io/seps/` — SEP catalogue (sampled)
- `https://modelcontextprotocol.io/community/` — Working/Interest groups + governance
- RFC 8414 (AS metadata) + RFC 8705 (PRM) + RFC 9728 (Protected Resource Metadata)
