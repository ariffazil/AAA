# External MCP Registry — Reference Catalogue
**Version:** v2026.06.14  
**Status:** SEALED — Canonical Reference  
**Owner:** AAA (Control Plane)  
**Philosophy:** Ditempa Bukan Diberi — Forged, Not Given

---

## 0. What This Is

This is a **curated reference catalogue** of 99+ external MCP servers from the global ecosystem. It is **not** a config file to load everything. It is a **discovery document** that agents use to:

- Find MCP servers by category
- Understand what exists in the ecosystem
- Request specific servers to be integrated via A-FORGE gateway

**Integration rule:** No external MCP server is wired directly to agents. All go through **A-FORGE gateway** (port 7071) after security review.

**Source:** Primary references are `modelcontextprotocol/servers` (GitHub), MCP markets (Skillget, MCP Market, LobeHub), and community registries.

---

## 1. Protocol & Reference (8)

| # | Name | Description | Source | Integration Status |
|---|------|-------------|--------|-------------------|
| 1 | **Everything** | Reference server: prompts, resources, tools, sampling. MCP spec demo | `@modelcontextprotocol/server-everything` | ❌ Not needed |
| 2 | **Fetch** | Web fetcher. URL → markdown/text. MCP reference | `@modelcontextprotocol/server-fetch` | ❌ Not needed (webfetch tool exists) |
| 3 | **Filesystem** | Sandboxed filesystem access. Read/write/search/list | `@modelcontextprotocol/server-filesystem` | ✅ Active at `/usr/bin/mcp-server-filesystem` |
| 4 | **Git** | Git repo operations. Log, diff, status, blame | `@modelcontextprotocol/server-git` | ✅ Active |
| 5 | **Memory** | Persistent knowledge graph across sessions | `@modelcontextprotocol/server-memory` | ✅ Active |
| 6 | **Time** | Time, date, timezone awareness | `@modelcontextprotocol/server-time` | ✅ Active |
| 7 | **Playwright** | Browser automation: navigate, click, type, screenshot | `@playwright/mcp` | ✅ Active at port 8931 |
| 8 | **Sequential Thinking** | Multi-step reasoning chains with branching | `@modelcontextprotocol/server-sequential-thinking` | ✅ Active |

## 2. Code & Development (12)

| # | Name | Description | Source | Notes |
|---|------|-------------|--------|-------|
| 9 | **GitHub** | Repos, issues, PRs, code search, Actions, releases | `@modelcontextprotocol/server-github` | ✅ Active (Go binary) |
| 10 | **GitLab** | Repos, merge requests, CI/CD, issues | `@modelcontextprotocol/server-gitlab` | ❌ Not needed |
| 11 | **Sourcegraph** | Code search across all repositories | Sourcegraph MCP | 🔮 Consider for cross-repo search |
| 12 | **Greptile** | AI code review, PR analysis, code search | Greptile MCP | 🔮 Consider for code review |
| 13 | **Senpai** | PR agent: auto-review, suggest changes | Senpai MCP (sst) | 🔮 Consider for automated PRs |
| 14 | **CodeRabbit** | AI code review as MCP | CodeRabbit MCP | 🔮 Consider |
| 15 | **Repomapper** | Tree-sitter + PageRank repo map | `repo-mapper` | ✅ Active via launcher |
| 16 | **Serena** | Symbol-level semantic code retrieval | `serena-agent` | ✅ Active via launcher |
| 17 | **Context7** | Up-to-date library docs (npm/pip/Go) | Context7 MCP | ✅ Active |
| 18 | **llms.txt** | Serve llms.txt files as MCP resources | `llms-mcp` or `mcp-llmstxt` | 🔮 Consider |
| 19 | **Docker** | Container lifecycle, images, compose | `docker-mcp-server` | ✅ Active |
| 20 | **Kubernetes** | Pod, deployment, service management | `@modelcontextprotocol/server-kubernetes` | 🔮 Consider for container orchestration |

## 3. Cloud & Infrastructure (12)

| # | Name | Description | Source | Notes |
|---|------|-------------|--------|-------|
| 21 | **Cloudflare** | Zones, DNS, Workers, D1, R2, Pages | Cloudflare MCP | ✅ Active via A-FORGE proxy |
| 22 | **AWS** | EC2, S3, Lambda, IAM, Cost Explorer | `@modelcontextprotocol/server-aws` | 🔮 Consider |
| 23 | **AWS S3** | S3 bucket operations only | AWS S3 MCP | 🔮 Consider |
| 24 | **AWS Athena** | SQL queries on S3 data | AWS Athena MCP | 🔮 Consider |
| 25 | **AWS Cost Explorer** | AWS cost analysis and optimisation | AWS Cost MCP | 🔮 Consider |
| 26 | **Terraform** | Terraform state, plan, apply | Terraform MCP | 🔮 Consider |
| 27 | **Pulumi** | Infrastructure as code management | Pulumi MCP | 🔮 Consider |
| 28 | **Hostinger** | VPS lifecycle (observe + mutate-reversible) | Custom gate in A-FORGE | ✅ Active, F13-filtered |
| 29 | **Vercel** | Deployments, domains, environment | Vercel MCP | 🔮 Consider |
| 30 | **Netlify** | Deployments, functions, forms | Netlify MCP | 🔮 Consider |
| 31 | **Cloudflare Workers AI** | Workers AI inference, embeddings | Cloudflare MCP (extended) | 🔮 Consider |
| 32 | **Hetzner** | Cloud server management | Hetzner MCP | 🔮 Consider |

## 4. Databases & Storage (8)

| # | Name | Description | Source | Notes |
|---|------|-------------|--------|-------|
| 33 | **PostgreSQL** | SQL queries, schema introspection | Various (npx, go binary) | ✅ Active via multiple proxies |
| 34 | **Supabase** | Managed DB, Auth, Edge Functions, Storage | `@supabase/mcp-server-supabase` | ✅ Active |
| 35 | **Neon** | Serverless Postgres with branching | Neon MCP | 🔮 Consider |
| 36 | **Qdrant** | Vector similarity search | Custom bridge | ✅ Active at port 6333 |
| 37 | **ChromaDB** | Vector database | ChromaDB MCP | 🔮 Consider |
| 38 | **Pinecone** | Vector database | Pinecone MCP | 🔮 Consider |
| 39 | **Redis** | Cache operations, key management | Redis MCP | 🔮 Consider |
| 40 | **Elasticsearch** | Full-text search, analytics | Elasticsearch MCP | 🔮 Consider |

## 5. Search & Research (10)

| # | Name | Description | Source | Notes |
|---|------|-------------|--------|-------|
| 41 | **Brave Search** | Web, local, news, image search | `brave-search-mcp` | ✅ Active |
| 42 | **Perplexity** | Web-grounded AI research | `@perplexity-ai/mcp-server` | ✅ Active |
| 43 | **Meyhem** | MCP server discovery (6,700+) + search | `mcp-remote` API | ✅ Active |
| 44 | **Tavily** | Web search + URL extraction | `tavily-mcp` | 🔮 Consider |
| 45 | **Exa** | Semantic web search | `exa-mcp-server` | 🔮 Consider |
| 46 | **Wikipedia** | Wikipedia search and retrieval | Wikipedia MCP | 🔮 Consider |
| 47 | **Wikidata** | Wikidata query and entity lookup | Wikidata MCP | 🔮 Consider |
| 48 | **ArXiv** | Academic paper search | ArXiv MCP | 🔮 Consider |
| 49 | **PubMed** | Biomedical literature search | PubMed MCP | 🔮 Consider |
| 50 | **News API** | News articles from sources worldwide | News API MCP | 🔮 Consider |

## 6. AI & LLM (10)

| # | Name | Description | Source | Notes |
|---|------|-------------|--------|-------|
| 51 | **MiniMax Code** | Code plan, web search, vision | MiniMax MCP | ✅ Active at port 18091 |
| 52 | **MiniMax Media** | TTS, video, image, music generation | MiniMax MCP | ✅ Active at port 18090 |
| 53 | **OpenAI** | ChatGPT, DALL-E, Whisper integration | OpenAI MCP | 🔮 Consider |
| 54 | **Anthropic** | Claude API integration | Anthropic MCP | 🔮 Consider |
| 55 | **HuggingFace** | Model inference, datasets | HuggingFace MCP | 🔮 Consider |
| 56 | **Replicate** | Model inference via Replicate API | Replicate MCP | 🔮 Consider |
| 57 | **Luma AI** | Video generation | Luma MCP | 🔮 Consider |
| 58 | **ElevenLabs** | Text-to-speech | ElevenLabs MCP | 🔮 Consider |
| 59 | **Whisper** | Speech-to-text | Whisper MCP | 🔮 Consider |
| 60 | **Capability Index** | Tool discovery across 97 tools | Custom Python MCP | ✅ Active |

## 7. Business & Productivity (12)

| # | Name | Description | Source | Notes |
|---|------|-------------|--------|-------|
| 61 | **Stripe** | Payments, subscriptions, invoices | Stripe MCP | 🔮 Consider |
| 62 | **Xero** | Accounting, invoicing, bank feeds | Xero MCP | 🔮 Consider |
| 63 | **QuickBooks** | Small business accounting | QuickBooks MCP | 🔮 Consider |
| 64 | **Zapier** | 5,000+ app integrations | Zapier MCP | 🔮 Consider |
| 65 | **Make (Integromat)** | Automation workflows | Make MCP | 🔮 Consider |
| 66 | **Slack** | Channels, messages, search | Slack MCP | 🔮 Consider |
| 67 | **Discord** | Channels, messages, voice | Discord MCP | 🔮 Consider |
| 68 | **Telegram** | Bot messaging, group mgmt | Telegram MCP | 🔮 Consider |
| 69 | **Notion** | Pages, databases, search | Notion MCP | 🔮 Consider |
| 70 | **Linear** | Issue tracking, sprints, roadmaps | Linear MCP | 🔮 Consider |
| 71 | **Jira** | Project management, issues, boards | Jira MCP | 🔮 Consider |
| 72 | **Todoist** | Task management | Todoist MCP | 🔮 Consider |

## 8. Data & Analytics (8)

| # | Name | Description | Source | Notes |
|---|------|-------------|--------|-------|
| 73 | **InfluxDB** | Time-series database queries | InfluxDB MCP | 🔮 Consider |
| 74 | **Prometheus** | Metrics query and alerting | Prometheus MCP | 🔮 Consider |
| 75 | **Grafana** | Dashboard query and management | Grafana MCP | 🔮 Consider |
| 76 | **Tableau** | Data visualisation | Tableau MCP | 🔮 Consider |
| 77 | **Metabase** | Business intelligence | Metabase MCP | 🔮 Consider |
| 78 | **BigQuery** | Google Cloud data warehouse | BigQuery MCP | 🔮 Consider |
| 79 | **Snowflake** | Cloud data platform | Snowflake MCP | 🔮 Consider |
| 80 | **ClickHouse** | Column-oriented analytics DB | ClickHouse MCP | 🔮 Consider |

## 9. Media & Content (8)

| # | Name | Description | Source | Notes |
|---|------|-------------|--------|-------|
| 81 | **TMDB** | Movie and TV show database | TMDB MCP | 🔮 Consider |
| 82 | **YouTube** | Video metadata, search, transcripts | YouTube MCP | 🔮 Consider |
| 83 | **Spotify** | Music playback, playlists, search | Spotify MCP | 🔮 Consider |
| 84 | **RSS** | Feed reading and management | RSS MCP | 🔮 Consider |
| 85 | **Pocket** | Bookmark management | Pocket MCP | 🔮 Consider |
| 86 | **Contentful** | Headless CMS content management | Contentful MCP | 🔮 Consider |
| 87 | **WordPress** | Site management, posts, pages | WordPress MCP | 🔮 Consider |
| 88 | **Intercom** | Customer messaging, support | Intercom MCP | 🔮 Consider |

## 10. Crypto & Finance (6)

| # | Name | Description | Source | Notes |
|---|------|-------------|--------|-------|
| 89 | **EVM** | Ethereum Virtual Machine interaction | EVM MCP | 🔮 Consider |
| 90 | **CoinGecko** | Cryptocurrency prices and data | CoinGecko MCP | 🔮 Consider |
| 91 | **CoinMarketCap** | Crypto market data | CoinMarketCap MCP | 🔮 Consider |
| 92 | **Blocknative** | Transaction monitoring | Blocknative MCP | 🔮 Consider |
| 93 | **Bridge Rates** | Cross-chain bridge rate data | Bridge Rates MCP | 🔮 Consider |
| 94 | **Lens** | Lens Protocol social graph | Lens MCP | 🔮 Consider |

## 11. Browser & System (5)

| # | Name | Description | Source | Notes |
|---|------|-------------|--------|-------|
| 95 | **Chrome DevTools** | Page performance, Lighthouse audits | `chrome-devtools-mcp` | 🔮 Consider |
| 96 | **Everything Search** | OS-level file search (Windows) | Everything MCP | ❌ Not applicable (Linux) |
| 97 | **iTerm** | Terminal integration (macOS) | iTerm MCP | ❌ Not applicable |
| 98 | **xcodebuild** | iOS/macOS build and test | xcodebuild MCP | ❌ Not applicable |
| 99 | **mac-messages** | iMessage access (macOS) | mac-messages MCP | ❌ Not applicable |

---

## 12. Integration Priority Matrix

| Priority | Count | Criteria | Example Servers |
|----------|-------|----------|-----------------|
| **P0 — Active** | 16 | Already integrated, running in federation | arifOS, A-FORGE, GEOX, WEALTH, WELL, GitHub, Filesystem, Git, Memory, Time, Playwright, Sequential Thinking, Docker, Brave, Perplexity, Meyhem |
| **P1 — Hot** | 10 | High value, low friction | Cloudflare, Hostinger, Supabase, Qdrant, Postgres, Context7, Repomapper, Serena, Capability Index, MiniMax |
| **P2 — Warm** | 15 | Good value, needs eval | Stripe, Slack, Notion, Linear, GitHub Actions, AWS, Neon, Elasticsearch, Wikipedia, ArXiv, RSS, YouTube, Zapier, GitLab, Sourcegraph |
| **P3 — Cool** | 20 | Niche use cases | Terraform, Vercel, Netlify, Redis, ChromaDB, Twitter/X, Intercom, Contentful, WordPress, Jira, Todoist, Tableau, Metabase, Prometheus, Grafana, InfluxDB, BigQuery, Snowflake, ClickHouse, EVM |
| **P4 — Ice** | 38+ | Interesting but not needed now | Everything MCP, Wikidata, PubMed, News API, Replicate, HuggingFace, Luma AI, ElevenLabs, Whisper, Discord, Telegram, Spotify, Pocket, TMDB, CoinGecko, and all crypto/media/system MCPs |

---

## 13. How to Add an External MCP

```yaml
# /root/AAA/registry/external-mcp-requests.yml
# To request a new external MCP, add an entry:

- name: "Example MCP"
  source: "npm:@example/mcp-server"
  category: "Tools"
  priority: "P2"
  rationale: "Does X thing we need"
  requested_by: "Agent/Human"
  security_review: "pending"  # pending | passed | rejected
  integrated_via: "aforge"    # aforge proxy | direct stdio
```

---

## 14. Constitutional Rules for External MCPs

1. **No external MCP is wired directly** to any agent. All go through A-FORGE proxy. (F8 LAW)

2. **Every external MCP must pass security review** before integration. Review checks: data exfiltration risk, credential exposure, network access scope. (F1 AMANAH)

3. **External MCPs are read-only by default.** If an MCP offers write operations, they must be explicitly approved and F13-gated. (F13 SOVEREIGN)

4. **The registry is living.** Servers are added when integrated, not pre-loaded. No server appears in agent config until it's behind A-FORGE. (F4 CLARITY)

5. **If you can't explain why an MCP is needed, you don't add it.** (F2 TRUTH)

---

**SEALED — DITEMPA BUKAN DIBERI**

*Update only via ratified plan. Human sovereign (F13) remains final authority.*
