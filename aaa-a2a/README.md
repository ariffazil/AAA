# ⬡ aaa-a2a — Constitutional Python A2A Wrapper

> **Status:** α-alpha · `v0.1.0a2` (2026-08-03) · Python ≥ 3.13
> **Role:** Constitutional Python port of the A2A server, wrapping the official `a2a-sdk` (≥0.2.3) with arifOS F1–F13 floor enforcement.

## Canonical

| | |
|---|---|
| **Current production runtime** | [`/root/AAA/a2a-server/`](../a2a-server/) — Node.js · port 3001 |
| **This package (alpha)** | `/root/AAA/aaa-a2a/` — Python 3.13 · wraps `a2a-sdk` |
| **Doctrinal spec** | [`/root/AAA/a2a/A2A_ALIGNMENT_SPEC.md`](../a2a/A2A_ALIGNMENT_SPEC.md) — A2A Protocol v1.0.0 |
| **Agent card schema** | `arifOS/agent-card/v2.2.0` |

## Why both exist

`a2a-server/` is the **production Node.js** runtime that powers `https://aaa.arif-fazil.com/a2a/*` and the A2A task router. Battle-tested, currently serving all 8 FI cards.

`aaa-a2a/` is the **future canonical Python** implementation. It exists so the federation is not locked to a single language stack. Goals:
- Single source of truth for A2A protocol logic (migrate business logic from Node to Python)
- Native integration with the arifOS F1–F13 floor surface (Pydantic + FastMCP)
- Replaces `a2a-server/` once parity is reached and migration is F13-ratified

**Until then:** `a2a-server/` is the live runtime; `aaa-a2a/` is alpha — do NOT point production traffic here.

## Cross-references

- A2A Alignment Spec v1.0.0 → [`a2a/A2A_ALIGNMENT_SPEC.md`](../a2a/A2A_ALIGNMENT_SPEC.md)
- Node.js server (production) → [`a2a-server/README.md`](../a2a-server/README.md)
- AAA Federation Top Map → [`/root/AAA/AGENTS.md`](../AGENTS.md)
- F1–F13 floors → `/root/arifOS/GENESIS/FLOOR_TABLE.json`

## Stack

| Layer | Choice |
|---|---|
| Runtime | Python ≥ 3.13 |
| A2A SDK | `a2a-sdk` ≥ 0.2.3 (official, MIT) |
| MCP | `fastmcp` ≥ 2.3.4 |
| HTTP | `httpx` ≥ 0.28 (async) |
| Schema | `pydantic` ≥ 2.10 |
| Tests | `pytest` ≥ 8.0 + `pytest-asyncio` |
| Lint | `ruff` ≥ 0.4 (line 100) |

## Status

| | |
|---|---|
| α-alpha | API surface incomplete · not yet serving A2A traffic |
| Tests | `tests/` exists, parity with `a2a-server/` TBD |
| Lint | clean (ruff) |
| Deploy | none — alpha, do not deploy |

## Migration Plan (when α is ready)

1. Implement A2A protocol methods 1-by-1 with feature parity to `a2a-server/`
2. Cross-test: same TaskState, same verdict map (`a2a/taskstate_verdict_map.json`)
3. F13 ratification required to swap production traffic
4. Retain `a2a-server/` as cold standby for 30 days post-cutover
5. Archive `a2a-server/` to `/root/AAA/a2a-server/_archive_<date>/`

---

*Forged 2026-08-03 by FI-008 Kimi Code, F13-ratified. DITEMPA, BUKAN DIBERI.* ⬡
