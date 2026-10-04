# NotebookLM (Gemini Notebook) MCP Bridge — Sovereignty-Respecting Wiring

> **Canonical query surface for the sovereign's H3 knowledge layer.**
> Built 2026-08-08 in response to "how do I make my agent access my notebook llm?".
> The sovereign selected this path (third-party MCP) over manual export because the cost of one-time Google login <<< the cost of re-exporting every notebook manually.

## Why this lives under agent-memory-architecture

NotebookLM (now **Gemini Notebook** as of July 2026) is a grounded RAG over the sovereign's H3 knowledge. The MCP bridge lets the agent *query* that knowledge on demand. It does NOT ingest NotebookLM content into the federation's L3 vector store. The sovereignty gate stays closed:

```
Sovereign says "ask my geology notebook about trap types"
  → Hermes invokes ask_question on the MCP
  → NotebookLM returns grounded answer + DOM citations
  → Hermes cites it, does NOT vectorize it
  → NotebookLM content stays in Google's domain
```

Default = reference only. Auto-ingestion = violation.

## The MCP server

| Repo | https://github.com/PleasePrompto/notebooklm-mcp |
| Stars | 3.1k · 444 forks · MIT · active |
| Version | v2.0.0 (v1 deprecated) |
| Transforms | Gemini Notebook UI via Patchright (stealth Chromium) — NOT an official Google API |
| Auth | One-time Google OAuth via persistent Chrome profile |

**Not a Google product.** Third-party. Can break if NotebookLM UI changes. The scar doctrine says that risk is acceptable because the bridge is reference-only and degrades gracefully to manual export (Path A from the conversation).

## Install (T1, ~5 min on a Hermes-equipped box)

### Requirements (all verified green on /root 2026-08-08)

- Node ≥ 18 → v22.23.1 ✅
- npx → 10.9.8 ✅
- Chrome stable → `/usr/bin/google-chrome-stable` ✅
- xvfb-run → `/usr/bin/xvfb-run` ✅ (only needed for one-time headless auth)

### Wire it into Hermes

```bash
# Add the MCP server
hermes mcp add notebooklm --command npx --args "notebooklm-mcp@latest"

# Configure for headless server use
hermes mcp configure notebooklm  # set profile=full, headless=true, stealth=enabled

# Verify
hermes mcp test notebooklm
```

### One-time auth (sovereign action required)

```bash
# Launches a visible Chrome under xvfb; sovereign completes Google login
xvfb-run -a npx notebooklm-mcp@latest --setup-auth
```

The MCP generates an OAuth URL. Open it on phone/laptop, log in with the Google account that has the notebooks, authorize. The Chrome profile gets saved to `~/.local/share/notebooklm-mcp/chrome_profile/` (Linux). Every subsequent run reuses the profile — fully headless, no further logins.

> **Iron rule:** the sovereign completes the Google login, not the agent. The agent never holds Google credentials. Profile isolation is by Chrome directory only.

## Tools exposed (v2.0.0, profile=full)

| Tool | Purpose |
|---|---|
| `ask_question` | Query a notebook with grounded, citation-backed answers. Returns answer + `_provenance` envelope. |
| `list_notebooks` | Enumerate the sovereign's notebooks. |
| `add_source` | Add URL or text source to a notebook (URL crawl, text paste). |
| `generate_audio` | Generate Audio Overview (the podcast feature). |
| `download_audio` | Save the podcast to a destination directory. |
| `get_citations` | Extract DOM-level citations from an answer. |

## Pitfalls

- **Do NOT pipe `ask_question` output into the federation's L3 vector store.** That is the single most likely violation. Reference, don't ingest.
- **Do NOT use `add_source` to push sovereign content into a notebook without F13 keyword.** The bridge can ingest into NotebookLM just as easily as it can query — that power runs both ways.
- **Do NOT run this on a public IP.** Default bind is `127.0.0.1`. Setting `NOTEBOOKLM_HOST=0.0.0.0` requires explicit `0.0.0.0 <-> public` justification — same rule as the rest of the federation.
- **Do NOT batch-load all notebooks.** The MCP can list them; that does not mean the agent should pre-fetch every notebook's contents at session start. The sovereignty gate applies per-query.
- **The sovereign's scar layer (H5) never goes near this bridge.** NotebookLM is for H3 (knowledge). Scars are sovereign content with a separate ledger at `/root/.local/share/arifos/scars/`. Do not conflate the two.

## Degradation policy

If the MCP breaks (Google UI change, OAuth expires, vendor abandons the repo):

1. Stop using `ask_question` immediately.
2. Fall back to manual export: sovereign downloads notebook as zip, drops in `/root/second-brain/notebooks/<name>/`, agent reads on demand like any other file.
3. Do NOT patch the MCP server in place — the scar doctrine says third-party surface area is reference-only, never load-bearing.

## Three paths compared (from the conversation)

| Path | Setup | Cost | F13 cost | Sovereignty risk |
|---|---|---|---|---|
| **A. Manual export** | zero | zero | none | zero |
| **B. Unofficial MCP** (this bridge) | ~10 min + 5 min one-time OAuth | third-party risk | small | low (gate intact) |
| **C. Official Enterprise API** | ~1 day + procurement | $$$$ | $$$$ | lowest (vendor-supported) |

The sovereign picked Path B. The reasoning: $0 cost, ~15 min total effort, sovereignty gate preserved, graceful degradation to Path A. Path C deferred until there is a specific programmatic use case that justifies Enterprise tier.

## Reference

- Repo: https://github.com/PleasePrompto/notebooklm-mcp
- Gemini Notebook home: https://notebooklm.google
- Sovereign H3 landing zone (manual fallback): `/root/second-brain/notebooks/`
- Sovereignty doctrine: `/root/AAA/governance/HUMAN_MEMORY_DOCTRINE.md`
- This bridge is referenced from the umbrella SKILL.md at `mlops/agent-memory-architecture`