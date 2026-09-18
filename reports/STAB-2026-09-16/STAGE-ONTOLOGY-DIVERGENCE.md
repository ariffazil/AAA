# STAGE ONTOLOGY DIVERGENCE — LIVE, ONE HOST, FOUR SURFACES
> Probed 2026-09-18 on KVM8 (forge, 100.64.0.2) · deployed kanon-2026.09.17+eff8a59
> Method: direct MCP JSON-RPC (tools/list, prompts/list) + HTTP /tools + repo canon

## The finding

One server, one host, no cache, no cross-host excuse. **Four surfaces disagree on the
stage number of `arif_judge`:**

| Surface | What it says JUDGE is | Live? |
|---|---|---|
| MCP `tools/list` | `arif_judge` = "KERNEL **666** · Constitutional verdict" | ✅ live wire |
| MCP `prompts/list` | `**888** 🔒 JUDGE · Verdict, not invention. VOID = branch dead.` | ✅ live wire |
| HTTP `/tools` | `arif_judge \| stage **888**` | ✅ live HTTP |
| `constitutional_map.py` (repo canon) | `"666": "arif_judge"`; docstring `JUDGE = "666" (was "888" — corrected)`; `"888": "arif_forge"` marked legacy | ✅ repo |

**Both wire surfaces are live and simultaneous.** A client calling `tools/list` learns
judge=666. The same client calling `prompts/list` learns judge=888. Neither is cached.
The server contradicts itself in its own two protocol endpoints.

## Second divergence — `arif_forge` stage

| Surface | arif_forge stage |
|---|---|
| MCP `tools/list` | **777** ("KERNEL 777 · Execution gate") |
| MCP `prompts/list` | **777** ("🔥 FORGE") |
| HTTP `/tools` | **010** |
| `CORE_NINE_STAGE_MAP` | **777** primary, with a legacy `"888": "arif_forge"` entry |

## Third — the stage count itself differs

- **Tool ontology:** 8 stages, 1:1 with 8 tools — `000,111,333,444,555,666,777,999`
- **Prompt ontology:** 10 stages — `000,111,222,333,444,555,666,777,888,999`
  - `222 🏛 PLAN` and `666 ⚖ DIGNITY` are stage-only (no dedicated tool; 222→arif_think, 666→soft gate)

So "stage" means two different things depending on which surface you read.

## Why `888` and `666` are overloaded

`888` carries at least three incompatible meanings in one codebase:
1. **JUDGE** — prompts/list (live)
2. **legacy arif_forge / deprecated REPLY** — constitutional_map.py:216, :80
3. **APEX sovereign judge / 888_HOLD** — federation doctrine (`888-APEX`, `888_HOLD`, six-graph)

`666` carries two:
1. **JUDGE** — tools/list, constitutional_map
2. **DIGNITY soft gate** — prompts/list

This is exactly the failure the external audit predicted:
`H(tool names) = H(tool names)` passes while `H(tool semantics) ≠ H(tool semantics)`.
A name-only hash would certify this surface as consistent. It is not.

## Why this is the real finding (not the client cache)

The external audit said "public surface broken, 1/17 works". I measured the live tool
surface: 8/8 correct. Then OpenClaw produced the prompt-surface map: JUDGE=888 — also
live-correct. **Both witnesses were right about their surface.**

There was no cache error, no stale mirror, no fabrication. The server genuinely serves two
contradictory stage ontologies from its own two MCP endpoints. The earlier "client cache"
explanation was correct for the audit's 15 unknown names, but it does not explain this —
this one is server-side.

## Consequence

- An agent that reads `prompts/list` and reasons "888 = JUDGE" will form a verdict
  expectation that the tool registry (666) does not carry.
- Any auditor reading HTTP `/tools` reports judge=888; any auditor reading `tools/list`
  reports 666; both are accurate. Audit divergence is *engineered in*, not accidental.
- A G0 capability hash over names alone would pass this. Over normalized
  `{name, kind, schema, stage, authority, ...}` records (RFC 8785 JCS) it would fail —
  which is the audit's recommended fix, now with live proof of necessity.

## ROOT CAUSE — PINNED (2026-09-18)

OpenClaw asked: is the server stale, or is canon not deployed? **Neither.** Both are deployed
and both are internally correct. They are **independently hardcoded and never coupled.**

### Evidence chain

**1. Canon and deployed are byte-identical.**
```
/root/arifOS/arifosmcp/constitutional_map.py                        sha256 cefbfe761ec4…
/opt/arifos/current/venv/…/arifosmcp/constitutional_map.py          sha256 cefbfe761ec4…
```
Both say `JUDGE = "666"`, `"666": "arif_judge"`, `"888": "arif_forge"  # legacy`.
So canon *is* deployed. Option "canon not deployed" is FALSE.

**2. The prompt surface is a second, independent definition.**
`/opt/arifos/current/venv/…/arifosmcp/runtime/fastmcp_ext/prompts.py`:

```python
from __future__ import annotations
import logging
from typing import Any
from fastmcp.prompts import Message, PromptResult     # ← no constitutional_map import
...
name="888 🔒 JUDGE",
meta={"stage": "888_JUDGE", "linked_tools": ["arif_judge"], ...}
```

`prompts.py` **never imports `constitutional_map`.** Zero coupling. The 10-stage ladder
(with 888=JUDGE, 666=DIGNITY) is hardcoded as literals in the prompt registry.

**3. Both files ship in the same build.** Same package, same mtime `Sep 18 00:45`.
So "server stale" is also FALSE — there is no build skew between them; they were built together.

**4. The divergence has been open since 2026-07-04.**
```
03f6cb725  2026-07-04  feat(lifecycle): ZEN-9 surface collapse …
```
That commit moved JUDGE 888→666 in `constitutional_map.py`. The prompt registry was never
updated — ~2.5 months of live divergence.

**5. No gate couples them.** No test compares prompt stages against tool stages.

### Causal chain (complete)

```
constitutional_map.py  ──► tools/list   → judge = 666  ✓ (correct, follows canon)
prompts.py (hardcoded) ──► prompts/list → judge = 888  ✗ (orphaned, never reconciled)
                                    ↓
                    same package, same build, no consistency gate
                                    ↓
              both surfaces live and authoritative-looking, mutually contradictory
```

This is **not** a deployment defect, a cache, or a mirror. It is two sources of truth in one
artifact with no reconciliation — the exact class the external audit named
(`H(names) = H(names)` passing while `H(semantics) ≠ H(semantics)`).

## Status

**P0 governance item → 888 HOLD. Do not self-patch.** The fix is a stage-ontology
reconciliation, which touches canon (constitutional_map), the prompt surface, and the HTTP
projection. Canon redefinition is F13 territory. Prepare a proposal; Arif decides.

Proposed scope for the proposal (no work done yet):
1. Declare the single authoritative stage ontology (tool-view or prompt-view).
2. Regenerate the non-authoritative surfaces from it.
3. Add a stage-consistency gate to CI: every surface's stage code for a given verb must be equal.
4. Define what `888` means federation-wide once and for all, and stop overloading it.
