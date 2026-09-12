# Addendum — HERMES Reality Bridge (Social Media Section)
**Date:** 2026-09-12 · **Status:** SUPERSEDES parts of `HERMES_REALITY_BRIDGE_TOOLS.md` (does NOT overwrite it)
**Trigger:** Arif's Layer-1 refinement (Bluesky + YouTube + Reddit core; XPOZ Free trial; X deferred) + two corrections.

> This addendum preserves the old assumptions, marks them superseded, records
> evidence strength, and separates verified-official-source facts from vendor
> assertions. The parent doc remains the historical record.

## 1. Corrections to the parent doc

| # | Parent doc said | Corrected reality | Evidence |
|---|---|---|---|
| 1 | "X: Basic $200/mo, 1500 free reads/mo" | X is **pay-per-usage, credit-based, no monthly subscription**. Post reads $0.005/resource; cost varies by endpoint/scope. Low-volume test can be cheap if budget-capped. | **CLAIM** — official docs.x.com/x-api/getting-started/pricing |
| 2 | "Reddit PRAW 100 req/min free" | Still ~100 QPM OAuth, **but new OAuth apps require approval** (Responsible Builder Policy). | **PLAUSIBLE** — needs primary-source confirmation; treat as gate, not fact |
| 3 | "Bluesky" (absent) | Bluesky public AppView + firehose (`com.atproto.sync.subscribeRepos`) are **no-auth**. | **CLAIM** — official docs.bsky.app (API directory) |
| 4 | "Bluesky 50M+ users" | User-count figure is marketing, not API fact. | **HYPOTHESIS** — do not cite as canonical |

## 2. New empirical findings (this session, 2026-09-12)

| Finding | Observation | Consequence |
|---|---|---|
| Bluesky AppView 403 | `public.api.bsky.app` AND `api.bsky.app` return 403 (edge/WAF) from af-forge VPS, even with browser UA | Bluesky **polling needs egress review** (proxy/alternate host) before live |
| Bluesky relay reachable | `bsky.network` returned HTTP 200 | Firehose path is available as fallback (needs strict filter/queue) |
| Reddit keyless 403 | `www.reddit.com/*.json` returns 403 without OAuth | Confirms Reddit OAuth is mandatory now (Phase A = 888) |

## 3. Updated verdict (supersedes parent's social section)

| Layer | Decision | Gate |
|---|---|---|
| Bluesky | **Proceed now** (zero-auth polling) | none — but egress review for this VPS |
| YouTube | **Proceed now** (metadata-only) | YOUTUBE_API_KEY (GCP project = 888) |
| Reddit | **Proceed carefully** (OAuth) | Reddit app + OAuth = 888 |
| XPOZ Free | **Trial first** (500 free credits, 200-credit budget, $0 spend) | XPOZ signup + key = 888 |
| XPOZ Pro | **888 HOLD** | $20/mo recurring |
| X official API | **Defer** | pay-per-usage, budget-capped only |
| Apify / scraping | **Do NOT enable by default** | 888 per platform/use-case |
| LinkedIn / Meta monitoring | **Owned-channel only** | compliant approved route required |

## 4. Architectural invariant (new)

XPOZ is a **replaceable data adapter**, not the HERMES core. Native free adapters
(Bluesky, YouTube, Reddit) are the system of record. Every XPOZ result is tagged
`provenance="xpoz"` so it can be dropped or swapped without touching the native
signal store, policy, ranking, or memory schema.

## 5. Evidence-strength ledger

- **CLAIM** (verified official source): X pay-per-usage pricing · Bluesky no-auth AppView/firehose · YouTube 10k units/day + 100 search.list calls/day · TikTok Research API academic-eligibility-only.
- **PLAUSIBLE** (corroborated, not primary): Reddit new-OAuth-approval requirement · XPOZ 500-free-credits / $20 Pro / credit-cost table (vendor's own materials).
- **HYPOTHESIS**: Reddit initial community allowlist (validate activity/moderation/relevance before production jobs).
- **UNKNOWN**: XPOZ's contractual/data-use position (needs its own review before trial data enters memory).

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE.
