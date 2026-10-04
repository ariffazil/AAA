# Investbrain integration audit + plan (2026-08-08)

Context for the continuation session. Arif pasted the Investbrain tweet ("Aku nak ni") — wants the
/ world/vitals/ cockpit upgraded with Investbrain intelligence + WEALTH MCP. Plan was presented;
**Arif's Q1–Q4 decision is outstanding** (see bottom). Do not re-research from scratch — verify live
endpoints, then execute the chosen path.

## What Investbrain is
Laravel PHP investment tracker. Repo: `investbrainapp/investbrain` (PHP ~875 stars, active Jul 2026).
License **CC-BY-NC 4.0** — non-commercial fits arif-fazil.com (personal/sovereign), attribution required.
OpenAPI v3 spec repo: `investbrainapp/investbrain-api` (means HTTP-callable, not just browser UI).
Proxmox LXC helper script exists on community-scripts.org (reference only — we deploy bare-metal per
federation doctrine: core organs are systemd, not containers).

## Why it closes Arif's gap (from his tweet)
| Dimension | /world/vitals/ today | Investbrain adds |
|---|---|---|
| Market data | Single WEALTH chain, no fallback | 5 providers, sequential fallback |
| Portfolio | Read-only macro | Holdings, transactions, dividends, cost-basis, daily P&L |
| Portability | VAULT999 receipts (append-only) | JSON export/import of portfolio + transactions |
| AI chat | None | LLM grounded on actual holdings (OpenAI or Ollama-compatible) |

## Market-data provider chain
- Env: `MARKET_DATA_PROVIDER=yahoo,twelvedata,alphavantage,finnhub,alpaca` — tried in order until one succeeds.
- Custom provider: implement `MarketDataInterface` (use existing providers as templates), register in
  Laravel config under `interfaces` section, append the name to `MARKET_DATA_PROVIDER`.
- Yahoo works keyless. Free tiers ~800 calls/day each for the others.
- **API keys to request from Arif:** `TWELVE_DATA_API_KEY`, `FINNHUB_API_KEY`, `ALPHAVANTAGE_API_KEY`,
  `ALPACA_API_KEY` (needs account creation). Yahoo-only fallback chain is viable until keys arrive.

## Planned integration (Path A + Phi bridge, recommended)
- Deploy: Laravel via PHP-FPM 8.3 upstream at `127.0.0.1:8090`, Caddy route `arif-fazil.com/invest/*`,
  SQLite DB (personal/sovereign — no MariaDB), CC-BY-NC attribution footer.
- **Phi bridge (~80 lines PHP):** custom `WealthSovereignProvider` that calls WEALTH `capital_market`
  MCP first; when WEALTH stutters the chain falls through to Yahoo → Twelve Data → … This gives
  Path A's UI/portfolio/AI chat immediately + Path B's sovereign-provider loop in one file.
- Portability loop: keep Investbrain JSON exports under `/root/forge_work/` (reversible, hash-chained).

## Live-site facts from the audit (re-verify before quoting)
- `/vitals/` + `/wealth/vitals/` → 308 → `/propa/`. `/world/vitals/` = live cockpit page.
- LIVE: `/oil|gas|gold/api/{history,ticker,snapshot}`. DEAD: `/klci/api/ticker`, `/usdmyr/api/ticker` (404).
- `wealth.arif-fazil.com/api/snapshot?asset=X` ignores asset (always oil) — use `arif-fazil.com/{asset}/api/snapshot`.
- CSP connect-src must be extended in Caddy for any new third-party data endpoint.

## Decision points outstanding (Arif's call)
- Q1: Path A alone vs Path A + Phi bridge (recommended: + bridge, ~80 lines).
- Q2: which market-data API keys exist already.
- Q3: same host (port 8090, Caddy route) vs separate LXC container.
- Q4: webroot — `/var/www/html/arif/invest/` (sibling to vitals) vs `/var/www/html/investbrain/`.
