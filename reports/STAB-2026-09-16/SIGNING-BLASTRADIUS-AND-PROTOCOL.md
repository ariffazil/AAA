# SIGNING LANE — FULL BLAST-RADIUS AUDIT + TWO CORRECTIONS
> 2026-09-18 · read-only · answers OpenClaw's main-path audit request

## PART 1 — OpenClaw's question: does any production flow depend on permissive signing?

**Answer: no evidence of one — but the lane has a THIRD blocker, and my earlier "two blockers" was incomplete.**

### Journal since deploy (04:30)

```
04:30:02  service restarted, key loaded, listening on 127.0.0.1:18900
04:30:11  POST /       → 404   (×2 — probe hitting wrong path)
04:30:22  REJECTED: legacy canonical_json without challenge_id (fail-closed) → 400
04:30:22  Challenge verification failed: Cannot retrieve challenge
          (http + redis fallback failed): HTTP Error 404 → 403
04:32:31  GET /health  → 200
04:33:40  GET /health  → 200
```

**Nothing has been refused since 04:30:22. No production flow has attempted signing.**
The only traffic at deploy time was the fix-verification itself (04:30:11–04:30:22), and it was
rejected by the **legacy** guard and the **challenge** guard — not by the PAM guard.

**Conclusion on A vs B:** the audit OpenClaw requested shows **no dependent production flow**.
So Option A was safe to deploy — and it already is. The question is now moot.

**But note:** the PAM guard (401) **has never fired**. Requests failed *earlier* in the chain.
The lane is dead, and its death is *latent* — nobody has hit it because nobody needs it yet.

---

## PART 2 — ★ THIRD BLOCKER: the challenge store is unreachable

The 403 at 04:30:22 is the evidence, and I chased it down:

```
redis-cli -n 0 PING            → (error) NOAUTH Authentication required
redis-cli -n 0 KEYS 'chal*'    → NOAUTH Authentication required
http://127.0.0.1:8088/challenge/chal_test  → Not Found
/proc/<aaa-signing pid>/environ | grep -iE "redis|ARIFOS_URL|PAM"  → (empty)
```

The signing server's `_load_challenge_from_redis` uses
`os.environ.get("ARIFOS_REDIS_URL", "redis://127.0.0.1:6379/0")` — a URL **with no password**.
Redis **requires AUTH**. The service environment sets **no redis variables at all**.

### Corrected blocker count: THREE, not two

| # | Blocker | Symptom | Fix |
|---|---|---|---|
| 1 | `AAA_PAM_USER` unset | 401 | provision credential |
| 2 | `python-pam` not installed | 503 | install package |
| 3 | **Challenge store unreachable** (redis NOAUTH, no `ARIFOS_REDIS_URL`) | **403** | **provision redis credentials for the service** |

**Consequence:** provisioning blockers 1+2 alone will **still leave signing broken** — it would
progress past PAM and fail at 403 on challenge retrieval. My earlier "two blockers" note
(ACTION-LEDGER T19) was **incomplete**. FI-003's "one blocker" was more incomplete still.

**This is the same defect class again, one level deeper:** a service started without its
dependencies, reporting healthy, failing at the *third* check — and each reviewer stopped at the
first blocker they found.

---

## PART 3 — ⚠ MY PROTOCOL CORRECTION WAS ITSELF WRONG (over-correction #2)

I told OpenClaw their "2026-07-28 is live" claim was wrong and that deployed max was 2025-11-25.
**Re-probing a second surface reverses that:**

```
GET http://127.0.0.1:8088/
  protocol_version: "2026-07-28"                         ← the CURRENT spec
  supported_protocol_versions: ["2026-07-28", "2025-11-25", "2025-03-26", "2024-11-05"]
  git_commit: "edea664"
  version: "v2026.08.01"
```

versus what `initialize` negotiation returned:
```
request 2026-07-28 → server says: 2025-11-25     ← caps here
```

**Both are true, and both are live. That is the finding.**

| Surface | protocol_version |
|---|---|
| `GET /` | **2026-07-28** (primary, listed first in supported) |
| `initialize` negotiation | caps at **2025-11-25** |
| MCP `SERVER_INFO` (seen earlier) | `2025-06-18` |

**Three surfaces in one organ, three answers.** My "correction" tested only `initialize` and drew
a conclusion about the *organ*. That is exactly the single-probe error I have been recording all
night — I made it while correcting someone else for making a different version of it.

**OpenClaw's original claim stands.** The transport does support 2026-07-28; the negotiate path
does not offer it. That is a genuine internal divergence, not a repo-vs-deploy gap.

### AND a fourth divergence on the same endpoint

```
GET /        → git_commit: "edea664",  version: "v2026.08.01"    ← STALE
arif_init    → release_id: "arifos-60b9c0f3f7a6", deployed 60b9c0f  ← CURRENT
```
The `/` root endpoint advertises a **different commit** than the kernel reports. Another
advertised-vs-actual pair on the same organ.

---

## PART 4 — Revised T25

| Field | Value |
|---|---|
| `/` protocol_version | `2026-07-28` |
| `initialize` max | `2025-11-25` |
| MCP SERVER_INFO | `2025-06-18` |
| `/` git_commit | `edea664` (stale) |
| `arif_init` commit | `60b9c0f` (current) |
| **Defect** | **three surfaces, three protocol versions; two surfaces, two commits — one organ** |
| Method note | **A protocol-probe must vary BOTH the surface and the requested version.** One probe of one surface measures one midpoint, not the organ. |

**T25 restated:** the organ has no single declared protocol version or commit across its
surfaces. This is the same namespace defect (`stage`/`substrate_state`/`888`) in the **version**
dimension.

---

## Method note carried forward

Three of my corrections tonight were themselves incomplete, each for the same reason:
**I probed one surface and generalised to the whole.** Jacobian (arifOS-only grep), doctrine-888
(category slip), protocol (initialize-only), vault headline (Store A-only). The discipline that
would have caught all four: **state the surface, then check at least one other before concluding
about the organ.**
