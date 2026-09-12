# HERMES Reality Bridge — Complete Tool Matrix

> **Purpose:** Every API, SDK, MCP server, and GitHub repo needed for HERMES agents to bridge human reality — YouTube, social media, email, maps, weather, messaging, local services.
> **Date:** 2026-09-12 · **Author:** 333-AGI · **Status:** ARCHITECTURAL DECISION SEALED

---

## 0. ARCHITECTURAL DECISION (2026-09-12 SEAL)

### Three-State Capability Model

| State | Meaning | Example |
|-------|---------|---------|
| **Implemented** | Source code, bridge, manifest, or skill exists | `forge_gmail` bridge/manifests exist |
| **Reachable** | A currently running agent can actually invoke it | APA service or connector resolves and returns |
| **Governed** | Invocation has auth scope, receipts, rate/cost limits, retention rules, and irreversible-action holds | Sending email, calendar creation, vendor ingestion |

**Key principle:** `capability_exists != agent_reachable != governed_action`

### Verdict: FREEZE broad MCP expansion

- Do NOT create new MCP servers for capabilities that already exist as REST APIs
- Do NOT treat "code exists somewhere" as "agent can use it now"
- Do NOT treat "agent can reach it" as "safe for autonomous action"
- **Only genuine new-surface trial candidate:** XPOZ (social listening)
- **Payment rails (DuitNow/FPX):** F13/888 HOLD — never autonomous

### Evidence Quality Discipline

- `repo code exists` ≠ `running`
- `server registered` ≠ `exposed`
- `tool exposed` ≠ `authorized`
- `authorized` ≠ `safe for autonomous action`
- `curl works once` ≠ `operationally reliable`

---

### Domain Scorecard

| Domain | Decision | Rationale |
|--------|----------|-----------|
| Email/Calendar/Drive/Sheets | **No new integration. Verify routing only.** | APA bridge code exists; verify Hermes can invoke the approved route now. |
| Weather | **No new MCP. Hardened via REST.** | Open-Meteo GET injected into morning-readiness.py (commit 54f7c3b). |
| YouTube | **No new MCP. Add resilience tests.** | youtube-transcript-api v1.2.4 installed. Test under auth/quota/transcript-availability failures. |
| Maps | **No new MCP.** | GEOX + mcp-geo cover geospatial. |
| GrabMaps | **Skip.** | Community wrapper, no Malaysia-local advantage over GEOX/mcp-geo. |
| SerpApi | **Not a gap.** | Cost/quality procurement decision ($25/mo). Existing search routes sufficient. |
| Social listening (XPOZ) | **Only genuine new-surface trial.** | Read-only pilot with 10-20 BM-English queries against existing search routes. |
| DuitNow/FPX | **F13/888 HOLD.** | Payment rails require legal entity, merchant mandate, fraud model. Never autonomous. |

### Missing Work (architectural closure, not tool expansion)

1. **Capability ledger** — canonical record per capability (endpoint, owner, auth, cost, last probe, fallback, sunset)
2. **Continuous reachability probes** — periodic non-destructive health checks per capability
3. **Governed action membrane** — reads observable; writes require 888 HOLD
4. **Behavioral edge bridges** — voice, memory, proactivity, multimodality (higher-value than API wiring)
5. **Evidence quality discipline** — prevent "surface inflation" from recurring

### XPOZ Trial Design (if pursued)

| Gate | Requirement |
|------|-------------|
| Scope | 10-20 fixed BM-English queries (Malaysian energy, geology, PETRONAS, tech, crisis) |
| Comparator | SearXNG, Brave, Firecrawl, Minimax, ordinary web search |
| Measures | Recall, precision, time-to-signal, provenance, BM-English handling, latency, unit cost |
| Governance | No posting, DMs, account actions, or autonomous public interaction |
| Data policy | No raw social content into long-term memory; minimal derived claims only |
| Stop rule | Reject if recall doesn't exceed cost + privacy + provenance overhead |
| Approval | Vendor-key = 888 HOLD procurement decision |

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE · 2026-09-12*

---

## 1. YOUTUBE — Video Intelligence

| Tool | Type | Auth Required | GitHub / PyPI | Notes |
|------|------|----------|---------------|-------|
| **youtube-transcript-api** | Python lib | None | jdepoix/youtube-transcript-api | Transcript extraction, supports translation, proxy rotation |
| **yt-dlp** | CLI / Python | None | yt-dlp/yt-dlp | Video/audio download, metadata, subtitles. The backbone. |
| **YTAI** | Python SDK + MCP + CLI + FastAPI | None | vibheksoni/youtube-ai | Search, metadata, transcripts, comments, downloads. 9 MCP tools. |
| **yt-transcript-pro** | Python lib | None | PyPI: yt-transcript-pro | Production-grade: batch, playlist, channel. 4 backends cascade. |
| **youtube-watch-mcp** | MCP server | None | PyPI: youtube-watch-mcp | get_info, get_transcript, search_transcript, get_segment. |
| **youtube-agent** | CLI + Agent | None | OliverNyx/youtube-agent | SQLite FTS catalog, clip extraction. Agent-friendly JSON output. |
| **YouTube Data API v3** | REST API | Google Cloud project | developers.google.com/youtube/v3 | Search, playlists, channels. 10K units/day free. |
| **youtube-transcript** | CLI | None | HanifCarroll/youtube-transcript | Fast CLI via yt-dlp captions. JSON + Markdown. |

**HERMES Pick:** YTAI (9 MCP tools) + yt-dlp (download backbone) + youtube-transcript-api (fast transcript)

---

## 2. SOCIAL MEDIA — Unified Publishing & Intelligence

### 2a. Unified Multi-Platform APIs

| Tool | Platforms | Type | Source | Notes |
|------|-----------|------|--------|-------|
| **SocialAPI.ai** | IG, FB, Threads, TikTok, YT, X, LinkedIn, Google Business, WhatsApp, Telegram | REST + MCP (78 tools) | docs.social-api.ai | Unified inbox, publishing, scheduling. OAuth 2.1. |
| **BulkPublish** | 15 platforms | Python SDK + MCP | azeemkafridi/bulkpublish-api | pip install bulkpublish. MIT. Scheduling, RSS. |
| **Late SDK** | 13 platforms | Python SDK + MCP | getlate.dev / PyPI: late-sdk | Scheduling, media download, analytics, OAuth connect. |
| **Upload-Post** | 20+ platforms | Python SDK | Upload-Post/upload-post-pip | Video, photo, text, documents. Scheduling, analytics. |
| **XPOZ** | Twitter, Instagram, Reddit, TikTok | Python SDK + MCP | xpozpublic/xpoz-python-sdk | 42 methods. Social listening. No platform auth needed. |

### 2b. Platform-Specific

| Platform | API | Auth | Notes |
|----------|-----|------|-------|
| **Twitter/X** | X API v2 | OAuth 2.0 | Basic: 1500 tweets/mo read. $100/mo Pro. Use XPOZ instead. |
| **Instagram** | Graph API | Facebook OAuth | Free for business accounts. |
| **Facebook** | Graph API | OAuth 2.0 | Pages, posts, comments. |
| **TikTok** | TikTok API | OAuth 2.0 | Video upload. Strict review. |
| **LinkedIn** | Marketing API | OAuth 2.0 | Restricted review. |
| **Reddit** | PRAW | OAuth 2.0 | pip install praw. 100 req/min free. |
| **Threads** | Threads API | Instagram OAuth | Publishing, replies. |

**HERMES Pick:** SocialAPI.ai (78 MCP tools) + XPOZ (social listening) + BulkPublish (15-platform publishing)

---

## 3. EMAIL — Read, Send, Search

| Tool | Type | Providers | Source | Notes |
|------|------|-----------|--------|-------|
| **Nylas CLI + MCP** | CLI + MCP (16 tools) | Gmail, Outlook, Exchange, Yahoo, iCloud, IMAP | nylas/cli | Agent Account, calendar, contacts. 2-min setup. MIT. |
| **email-mcp** | MCP (42 tools) | SMTP/IMAP, SendGrid, Mailgun, Resend, Slack, Discord | sandraschi/email-mcp | Web dashboard, AI compose, auto-respond, contacts. |
| **Google MailPilot** | MCP (25+ tools) | Gmail IMAP/SMTP | johnneerdael/google-mailpilot | CONDSTORE sync, IDLE push, FTS5 search, calendar. |
| **Emalia** | Python lib + Agent | Any IMAP/SMTP | PyPI: emalia | Typed IMAP/SMTP toolkit. Policy-gated. Works without LLM. |
| **Gmail API** | REST | Gmail only | Google | Full read/write. OAuth. Complex setup (1-4 hours). |
| **Microsoft Graph** | REST | Outlook/M365 only | Microsoft | Email + calendar + contacts. Azure AD auth. |
| **SendGrid** | Transactional | Send-only | sendgrid/sendgrid-python | pip install sendgrid. 100 emails/day free. |

**HERMES Pick:** Nylas CLI (16 MCP tools) + email-mcp (42 tools) + Emalia (lightweight IMAP)

---

## 4. MAPS & DIRECTIONS — Geospatial Intelligence

| Tool | Type | Auth | Source | Notes |
|------|------|------|--------|-------|
| **Mapbox MCP Server** | MCP | Mapbox token | mapbox/mcp-server | Geocoding, POI, routing, matrices, optimization, isochrones. |
| **Google Maps MCP (cablate)** | MCP (18 tools) | Google Maps API | cablate/mcp-google-map | 14 atomic + 4 composite. Weather, air quality, batch geocode. |
| **Google Maps MCP (OtoDock)** | MCP (11 tools) | Google Maps API | OtoDock/google-maps-mcp-server | Places, directions, geocoding, roads, elevation, traffic. |
| **Google Grounding Lite** | MCP | Google Cloud | developers.google.com/maps/ai/grounding-lite | search_places, compute_routes, lookup_weather. |
| **mcp-geo** | MCP | None (OSM) | PyPI: mcp-geo | Geocoding, routing, OSM queries, elevation, isochrones. |
| **osm-mcp** | MCP (11 tools) | None | ni-c/osm-mcp | Geocoding, routing (foot/car/bike), optimization, POI. Free. |
| **maps-mcp** | MCP (7 tools) | Google Maps API | PyPI: maps-mcp | Geocoding, places, travel time, nearby. |
| **GrabMaps MCP** | MCP | AWS + GrabMaps | hithereiamaliff/mcp-grabmaps | SE Asia (MY, SG, ID, TH, VN, PH, MM, KH). |

**HERMES Pick:** osm-mcp (free, 11 tools) + cablate/mcp-google-map (18 tools, composites) + GrabMaps (SE Asia)

---

## 5. WEATHER — Forecasts & Conditions

| Tool | Type | Auth | Source | Notes |
|------|------|------|--------|-------|
| **Open-Meteo** | REST API | None | open-meteo.com | 30+ models, historical from 1940. CC BY 4.0. |
| **open-meteo-mcp** | MCP | None | PyPI: open-meteo-mcp | Current, datetime range, details. stdio/SSE/HTTP. |
| **open-meteo-mcp (schlpbch)** | MCP | None | schlpbch/open-meteo-mcp | Weather + snow + air quality + geocoding. |
| **mcp-weather** | MCP | None | agentic-forge/mcp-weather | FastMCP. Smart location resolution. |
| **OpenWeatherMap MCP** | MCP | OWM token | NimbleBrainInc/mcp-openweathermap | 5 tools. Air quality. 1M calls/mo free. |

**HERMES Pick:** open-meteo-mcp (free, no auth) + OpenWeatherMap MCP (1M free calls, air quality)

---

## 6. MESSAGING — Communication Channels

### 6a. Multi-Channel Platforms

| Tool | Channels | Type | Source | Notes |
|------|----------|------|--------|-------|
| **unified-channel** | 19: Telegram, Discord, Slack, WhatsApp, iMessage, LINE, Matrix, MS Teams, Feishu, etc. | Python | gambletan/unified-channel | 1 API, 19 channels. Middleware pipeline. |
| **PraisonAI Bots** | Telegram, Discord, Slack, WhatsApp, Signal, LINE, iMessage, Email, AgentMail | Python + CLI | praison.ai | BotOS orchestration. Durable delivery. |
| **Omni** | WhatsApp, Discord, Slack, Telegram, A2A, Gupshup, Twilio | TS + Python | automagik-dev/omni | Event-driven, NATS, identity graph. |
| **ellmos connectors** | Telegram, Discord, Signal, WhatsApp, Home Assistant, Webhook | Python (stdlib) | ellmos-ai/connectors | Zero dependencies. |

### 6b. Platform-Specific

| Platform | Tool | Auth | Notes |
|----------|------|------|-------|
| **Telegram** | Telegram Bot API | Bot token (free) | Already in Hermes. |
| **WhatsApp** | Business Cloud API | Meta OAuth | Webhook required. |
| **Discord** | Discord Bot API | Bot token | Gateway WebSocket. |
| **Slack** | Slack Bot API | OAuth 2.0 | Socket Mode. |
| **Signal** | signal-cli | Device link | Local bridge. |
| **SMS/Voice** | Twilio Agent Connect | Account SID | twilio/twilio-agent-connect-python |
| **LINE** | LINE Messaging API | Channel token | JP/TH/TW focused. |

**HERMES Pick:** unified-channel (19 channels) + Twilio Agent Connect (production SMS/Voice)

---

## 7. LOCAL SERVICES — Ride-Hailing, Food, Business

| Tool | Service | Type | Source | Notes |
|------|---------|------|--------|-------|
| **GrabFood Partner MCP** | GrabFood/GrabMart | MCP | @aisar-labs/grab-merchant-mcp | 12 tools: orders, menus, hours. OAuth2. |
| **GrabFood API SDK** | GrabFood | Python SDK | grab/grabfood-api-sdk-python | Official Grab SDK. |
| **Grab MCP (sim)** | Grab rides + food | MCP | c0dn/silver-Ag-MCP | Dev/testing simulation. |
| **GrabMaps MCP** | SE Asia places | MCP | hithereiamaliff/mcp-grabmaps | 8 SE Asian countries. |
| **Google Places** | Local business | Via Google Maps MCP | See Maps section | search_places, place_details. |
| **OSM Overpass** | Local POI | Via osm-mcp | See Maps section | find_nearby_pois, poi_details. Free. |

**HERMES Pick:** GrabMaps MCP (SE Asia) + GrabFood Partner MCP + osm-mcp POI (free)

---

## 8. IMPLEMENTATION PRIORITY

### Phase 1 — Core Reality Bridge (Week 1-2)

| # | Tool | Why First | Install |
|---|------|-----------|---------|
| 1 | **unified-channel** | 19 messaging channels in 1 API | pip install unified-channel[telegram,discord,slack,whatsapp] |
| 2 | **open-meteo-mcp** | Free weather, no auth | pip install open-meteo-mcp |
| 3 | **osm-mcp** | Free maps, geocoding, routing, POI | pip install osm-mcp |
| 4 | **youtube-transcript-api** | YouTube transcripts | pip install youtube-transcript-api |
| 5 | **Nylas CLI** | Email + calendar + contacts | curl -fsSL https://nylas.com/install.sh \| bash |

### Phase 2 — Enhanced Intelligence (Week 3-4)

| # | Tool | Why | Install |
|---|------|-----|---------|
| 6 | **email-mcp** | 42 email tools | pip install email-mcp |
| 7 | **SocialAPI.ai** | Unified social publishing | SDK install |
| 8 | **XPOZ** | Social listening, no auth | pip install xpoz |
| 9 | **cablate/mcp-google-map** | 18 Google Maps tools | npx @cablate/mcp-google-map |
| 10 | **YTAI** | YouTube MCP (9 tools) | pip install ytai |

### Phase 3 — Local Services & Deep Integration (Week 5+)

| # | Tool | Why | Install |
|---|------|-----|---------|
| 11 | **GrabMaps MCP** | SE Asia places/routes | npm/Docker |
| 12 | **GrabFood Partner MCP** | Food delivery management | npx @aisar-labs/grab-merchant-mcp |
| 13 | **Twilio Agent Connect** | Production SMS/Voice | pip install twilio-agent-connect |
| 14 | **Omni** | Event-driven omnichannel | Docker/Bun |
| 15 | **OpenWeatherMap MCP** | Air quality + historical | pip install mcp-openweathermap |

---

## 9. COST MATRIX

| Category | Free Option | Paid Option | Monthly Cost |
|----------|------------|-------------|--------------|
| **YouTube** | yt-dlp + youtube-transcript-api | YouTube Data API v3 | Free (10K units/day) |
| **Social Media** | XPOZ (listening) | SocialAPI.ai (full) | $0-99/mo |
| **Email** | Emalia (IMAP/SMTP) | Nylas (multi-provider) | Free-$49/mo |
| **Maps** | osm-mcp (OpenStreetMap) | Google Maps / Mapbox | Free-$200/mo credit |
| **Weather** | Open-Meteo | OpenWeatherMap | Free (1M calls/mo) |
| **Messaging** | Telegram Bot (free) | Twilio (SMS/Voice) | Free-$0.0075/SMS |
| **Local Services** | GrabMaps (free dev) | GrabFood Partner | Free-usage based |

---

## 10. TOTAL TOOL COUNT

| Category | Tools Found | MCP Servers | Free Options |
|----------|------------|-------------|--------------|
| YouTube | 8 | 2 (YTAI, youtube-watch-mcp) | All free |
| Social Media | 12+ | 3 (SocialAPI, BulkPublish, Late) | XPOZ, Reddit PRAW |
| Email | 7 | 3 (Nylas, email-mcp, MailPilot) | Emalia, Gmail API |
| Maps | 8 | 7 | osm-mcp, mcp-geo |
| Weather | 5 | 4 | All free (Open-Meteo) |
| Messaging | 10+ | Via unified-channel | Telegram, Discord free |
| Local Services | 6 | 3 (GrabMaps, GrabFood, Grab sim) | osm-mcp POI |
| **TOTAL** | **56+** | **22+ MCP servers** | **Most have free tiers** |

---

*DITEMPA BUKAN DIBERI — 333-AGI — 2026-09-12*
