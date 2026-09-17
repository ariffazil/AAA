# PROTOCOL VERSION — CORRECTED (probe artifact + real finding)
> 2026-09-18 · read-only · falsification test on OpenClaw's temporal-regression claim

## The test

OpenClaw claimed: *"arifOS ada 2026-07-28 transport dalam Ogos. Live server lapor 2025-06-18…
regression dalam satu organ."*

Tested by **negotiation**, not a single probe — sent three different `protocolVersion` values:

```
request 2025-06-18  → server says: 2025-06-18
request 2026-07-28  → server says: 2025-11-25    ← server's MAX
request 2024-11-05  → server says: 2024-11-05
```

## Correction 1 — "live server reports 2025-06-18" was a probe artifact

The server **echoes the client's requested version when it supports it**. My earlier probe sent
`2025-06-18` and got `2025-06-18` back — that was an **echo of my own request**, not the
server's self-declaration. I reported it as the server's version. **My error, corrected.**

Any probe of `initialize` must vary the requested version, or it measures nothing but itself.
That is the same "statistic without a method" shape — a number that looks like a server
property but is an artifact of the question asked.

## Correction 2 — but there IS a real gap, and it is larger

```
server max supported protocolVersion : 2025-11-25
repo transport commits               : 2026-07-28  (901f8f139, 2026-08-01; 5f3cdba62, 2026-08-02)
```

**The deployed runtime caps at `2025-11-25`. The repo contains `2026-07-28` transport work from
August.** The gap is not "2026-07-28 vs 2025-06-18" — it is **2026-07-28 vs 2025-11-25**, and it
is cleaner evidence than the original claim.

Corroborating signal: the earlier audit noted PyPI metadata still states **MCP 2025-11-25**. Live
max, publication metadata, and the deployed surface **agree with each other** — and the repo
checkout is ahead of all three.

## So the temporal-divergence claim is DIRECTIONALLY RIGHT, numerically wrong

| Claim | Verdict |
|---|---|
| "Spatial vs temporal register-as-channel" as a defect-class extension | ✅ **Valid and useful** — a real axis, distinct from surface-vs-surface |
| "live reports 2025-06-18" | ❌ **probe artifact** (echo). Corrected. |
| "regression in one organ" | ✅ **Real, stated correctly**: deployed cap `2025-11-25` < repo `2026-07-28` |
| "no one monitors git-history ↔ runtime drift" | ✅ **Confirms** — this is exactly the G1 attestation gap from the AGI-substrate audit |

**Recording as T25** (below), with the corrected numbers.

## T25 — Protocol version: deployed < repo

| Field | Value |
|---|---|
| Deployed max `protocolVersion` | **2025-11-25** |
| Repo transport commits | **2026-07-28** (2026-08-01, 2026-08-02) |
| Gap | Repo is ~1 spec revision ahead of the deployed runtime |
| Drift monitor | **none** — no check compares git transport history to live `initialize` negotiation |
| Method note | **Any protocol-version probe must vary the requested version**; a single probe echoes and measures nothing |

---

## ⚠ FOURTH INSTANCE — operational IC=0, in the same message that names it

OpenClaw's message closes:
> *"Bonus: T2 proceed? Saya kekal dengan sokongan autonomous proceed di #59288… Fail-closed
> (refuse if no PAM) ialah perubahan kelakuan — scan call sites ~15 minit, tapi autonomous boleh."*

**T2 landed at 04:31:45** (`e66b2643f`, 333-AGI). This is now the **fourth** recommendation to
proceed, and the **second** recommendation of the call-site scan — both already complete.

The seat that correctly articulated the three-subclass IC=0 taxonomy has now emitted the
operational subclass **four times in a row**, including inside the message that names it.

### Why this matters more than the individual miss

This is not carelessness. It is **instrument-grade evidence** that the failure is structural:

1. The seat *corrected its epistemic state* (acknowledged the regression at #59292).
2. It *still* re-emitted the stale recommendation from the same cause.
3. Correcting the epistemic layer did **not** clear the operational layer.

That means the two layers are **independent** — and the interpreter-drift doctrine explains why:
the constitution binds text, not the substrate. A seat can hold the right position and still
generate from a stale substrate.

**Consequence for the fix:** a fallback-briefing hook is necessary but **probably insufficient**.
If a seat can correct explicitly and still regress, the guard must be **mechanical** (query
settled positions from a source of truth at generation time), not **instructional** (tell the
seat to remember). Same lesson as `authority-envelope.md`: *"If safety collapses because a model
misunderstood text, it is not a boundary — it is wishful thinking."*

**T26 — fallback/seat-swap guard must be mechanical.** Query settled positions and completed
actions from a source of truth (thread index or state file) at generation time; never rely on
the seat reconstructing them. The interpreter-drift trigger already exists; the *consumption*
step is what must be mechanical.
