# GEOX Dependency Alignment Plan (D5) — 2026-10-07
**Lane B RECEIPT — NO mutation executed. Awaiting F13 word before any `uv pip install`.**

## Current state (live, this audit window)

| Package | Declared (pyproject) | Declared (info reqtxt) | Installed (.venv) | Risk |
|---|---|---|---|---|
| fastmcp | 3.4.6 (pyproject pin) | 4.0.10 (info reqtxt freeze) | 3.4.6 | MIXED — pyproject vs reqtxt disagree |
| fastmcp-slim | n/a | 4.0.10 | 3.4.6 | DRIFT |
| mcp | n/a | 2.2.0 | 1.30.0 | **MAJOR DRIFT** |
| pydantic | ≥2.13.4 | 2.13.4 | 2.13.5 | patch (ok) |
| uvicorn | ≥0.52.1 | 0.54.0 | 0.54.0 | match |
| starlette | n/a | 1.3.1 | 1.7.0 | MINOR |
| httpx | ≥0.28.1 | n/a | 0.28.1 | match |
| httpx2 | ≥2.9.1,<3.0 | n/a | 2.13.1 | match |

`requirements.txt` itself documents the drift at the top of the file
(`KNOWN PRE-EXISTING INSTALL DRIFT`). The server runs and serves 27 tools
on the installed versions; the drift is acknowledged, not breaking.

## Authority ranking (per forge-mcp-gui doctrine)

1. **pyproject.toml** + **uv.lock** = sole resolver authority
   (.github/dependabot.yml + ci-uv-lock-invariant.yml)
2. `requirements.txt` = informational freeze of MCP-relevant direct deps
3. **Installed `.venv`** = what runs

A realignment MUST go through pyproject/uv.lock, not `pip install` ad-hoc.

## Three realignment paths (Arif chooses ONE)

### Path A — Pin to INSTALLED (3.4.6 / 1.30.0)
- Update `pyproject.toml` `fastmcp[apps,tasks]==3.4.6` (already pinned)
- Add `mcp==1.30.0` to pyproject
- Refresh `requirements.txt` to match
- Run `uv lock` + `uv sync`
- Risk: LOWEST. No upgrade. Live server already runs on these.
- Reversible: trivial `git revert`.

### Path B — Upgrade INSTALLED to DECLARED (4.0.10 / 2.2.0)
- Run `uv lock --upgrade-package fastmcp fastmcp-slim mcp`
- Resolve transitive conflicts (starlette, anyio, pydantic)
- Run `uv sync` and reboot server
- Risk: **MEDIUM**. FastMCP 4 has breaking changes (3.4.6→4.0 is a major
  version). The server's `tools_wiring.py`, `server.py`, and `uri_schemes.py`
  import patterns would need re-verification. May break live `/mcp` until
  redeployed and smoke-tested.
- Reversible: medium (lockfile revert + redeploy).

### Path C — Defer
- Leave as documented.
- Open an issue: "GEOX MCP stack drift — review before 2026-12-31"
- Risk: NONE now, accrues over months.
- Reversible: trivially a non-event.

## Why I am NOT auto-executing

- D5 is **external port territory** (`pip install` against a running
  production server).
- Per F13 + Attention Membrane: live external services require the
  sovereign's word before mutation.
- Path A is the safest. Path B is the "right" answer but needs a window.

## Awaiting F13 binary

A / B / C. One binary only.

— End of D5 plan —