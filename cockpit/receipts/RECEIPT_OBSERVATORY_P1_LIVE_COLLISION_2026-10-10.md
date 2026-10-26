# RECEIPT — Observatory P1 "LIVE"-without-observation collision (AUDIT ONLY, NO MUTATION)

**Date:** 2026-10-10 ~15:20 MYT
**Session:** SEAL-177a77d4927d433f
**Authorization:** Arif corrective directive thread — audit + propose only.
**Source channel:** Observatory fetched via `curl` from this box. Copilot external review cited the same finding independently.
**Mutations performed this turn:** ZERO on `/root/`, ZERO on `/root/arif-fazil.com/`, ZERO on `/root/AAA/cockpit/`.

## What the live Observatory currently says (path-of-evidence)

```
File:           /tmp/obs-live.html
Fetched at:     2026-10-10 ~15:20 MYT
Size:           43,093 bytes
sha256:         640f0ae9ddea263613122d914b1380d40af4b9605a5be6b504f7972f8c97902e
URL:            https://arif-fazil.com/arifos/
```

The page is reachable. The renderer is honest in most places — every field exposes `source: missing · confidence: unknown · freshness: unavailable`. Floor cells render as `loaded / not measured`. arifFLOW status remains `HOLD until ARIF GO`. Identity cells render `unavailable` for source/build/deployed/drift/deployment/started/platform/kernel-epoch. The page does **not** greenwash the global absence of evidence.

### Where the contradiction lives (P1 receipt matrix)

| Row | Phase | Current badge | Source | Confidence | Honest label |
|---|---|---|---|---|---|
| line 282 | P1-1 | `SEALED` | declared migration fallback | unknown | `DECLARED` |
| line 283 | P1-2 | `SEALED` | declared migration fallback | unknown | `DECLARED` |
| line 284 | P1-3 | `SEALED` | declared migration fallback | unknown | `DECLARED` |
| line 285 | P1-B | `SEALED` | declared migration fallback | unknown | `DECLARED` |
| **line 286** | **P1-4** | **`SEALED LIVE`** | **declared migration fallback** | **unknown** | **`OBSERVATION_UNAVAILABLE`** |
| **line 287** | **P1-5** | **`CANARY LIVE`** | **declared migration fallback** | **unknown** | **`OBSERVATION_UNAVAILABLE`** |
| **line 288** | **P1-6** | **`CANARY LIVE`** | **declared migration fallback** | **unknown** | **`OBSERVATION_UNAVAILABLE`** |

(P1-1 through P1-B's `SEALED` is also contestable on F2 grounds — a `SEALED` badge with `confidence: unknown` is a derived-status masquerading as observation. But P1-4/5/6 carry the extra collision token `LIVE` and the `CANARY LIVE` token that are most defensibly wrong.)

### Other surfaced tokens (non-collision)

- HTML data-attribute `data-organ="arifos"` ✓
- CSS class `status--live { background: rgba(56,204,132,.12); color: #38cc84 }` — visual style key, not a claim.
- Intent card text `"Witness live federation state"`, `"Probe live JSON snapshot"`, `"public-state.v1 live"` — UI affordance text linking to `/api/...` endpoints. These are page affordances, not P1 badge claims. They are honest because the linked endpoints return JSON that the renderer renders as `unavailable` when snapshot is missing.
- `Conformance (PR7)` row at line 325 carries `FAST / LIVE / FULL` with `skip-state ⇒ AMBER`. The `LIVE` here is a level label within a 3-level scheme, not a runtime status. Borderline; could be relabeled `FAST / LEVEL / FULL` for clarity, but not a hard collision.

### The honest-empty-witness rule

A page that says `source: missing · confidence: unknown` for everything else, but uses `LIVE` in 3 rows beside the same source, is **semantically incoherent**. The renderer is half honest. F1–F12 floor cells render `loaded / not measured` — they have earned a different vocabulary. The P1 badge cells have not.

## Engineering assessment

- **No bug in the renderer.** The CSS class `status--live` is a green chip style, and the renderer probably uses the same chip across `LIVE` runtime badges and `CANARY LIVE` declared badges. The collision is in **what string is placed inside the chip**, not in the chip's presence.
- **No fix without authority.** Three rows in source-tree HTML (`/root/arif-fazil.com/arifos/...`) carry these labels. Per the memo the user showed tonight, source tree changes require an audit-not-regen path. Engineer lane **cannot deploy** — that is Caddy reload + cache invalidation, F13 class.
- **No data pipeline yet.** Even after the label fix, lines 286–288 still say `declared migration fallback` because the runtime data pipeline that would replace "declared" with "observed" has not been wired. The label is honest-empty; the data is honest-empty; only the lexer choice conflates them.

## Recommended corrective (awaits sovereign authorization)

```
Edit 3 lines in /root/arif-fazil.com/arifos/ index source tree:
  line 286: "SEALED LIVE"            → "DECLARED    source: P1-4 config declared; runtime: unavailable"
  line 287: "CANARY LIVE"            → "DECLARED_CANARY  source: P1-5 config declared; runtime: unavailable"
  line 288: "CANARY LIVE"            → "DECLARED_CANARY  source: P1-6 config declared; runtime: unavailable"

For consistency, also consider:
  line 282-285: "SEALED"            → "DECLARED"   (collapses P1-1..P1-B under same rule)

Do NOT perform these edits tonight.
  - editor: confirm whether MAS wishes all 7 rows relabeled, or only the 3 LIVE ones.
  - deploy: requires Caddy reload + cache bust; cannot deploy from engineer lane.
  - audit-first: MAS said "i do audit first" — audit done, corrections proposed, not implemented.
```

## Why no edit executed

1. **F11 AUDIT — every mutation attributable.** A renderer edit is mutating a sourced, signed, served-to-the-public surface. Even a one-character edit changes what the world sees.
2. **F13 SOVEREIGN.** Editor has not given the word. Per "i do audit first," the next action is the user's audit decision, not mine.
3. **anti-collapse doctrine** (F13 2026-09-14). This is a low-risk read-only operation but only if the user wants it. Tonight the user asked for **audit first**, not "fix it."
4. **CAREFUL SCOPE.** "Buat ni semua bagi setel. … auto execute" was rejected last turn. Tonight's message ends with the same structural ambiguity. Proposing, not implementing, until the user explicitly says "do the edit."

## Honest vocabulary

Before edit:

```
RUNTIME_OBSERVATION  →  unknown
PROVENANCE           →  declared migration fallback
CONFIDENCE           →  unknown
CURRENT_LABEL        →  STATUS DEPENDS ON ROW (SEALED, SEALED LIVE, CANARY LIVE)
```

After edit (if approved):

```
RUNTIME_OBSERVATION  →  unknown
PROVENANCE           →  declared migration fallback
CONFIDENCE           →  unknown
CURRENT_LABEL        →  DECLARED, DECLARED, DECLARED, DECLARED,
                        DECLARED, DECLARED_CANARY, DECLARED_CANARY
```

The reducer (declared migration fallback) stays as a separate meta-line. The badge text drops the `LIVE` token. The page becomes internally consistent: every "positive" label either has a runtime observation to back it, or carries a `DECLARED` qualifier.

## Carry-forwards (this turn)

- **Mixed-label-as-truth pattern.** When `source = declared` is paired with `status = LIVE`, the renderer is borrowing live-runtime semantics for a config-declared state. F2 says labels must be epistemic-class-fit. The P1 badge is the failure pattern to avoid in the planned machine-witness/v1 panel renderer.
- **Half-honest page.** It is **not** stale lie (because most fields are honest-empty). It is **half honest** — three rows in P1 use the live-renderer vocabulary where the data does not warrant it.
- **No data pipeline yet.** Even with the label fix, the page will still honestly-empty. Fixing the label is necessary but not sufficient.

## Status of the recommendation

```
Observatory framing               SEAL    (the page is honest empty witness outside P1)
F2 P1 "LIVE"-without-observation  RECOMMENDED CORRECTIVE — AWAITS AUTHORIZATION
Federation-wide green claims      HOLD
Census + local witness snapshot   NEXT (proposed, not approved)
Site regen                         NOT EXECUTED tonight
```

## Hashes (audit trail)

```
/tmp/obs-live.html         sha256  640f0ae9ddea263613122d914b1380d40af4b9605a5be6b504f7972f8c97902e
binding corrective (prior)  sha256  82df10c92dc5107b942ffa71085a66ef16650e172dea50119123d341a6edb483
supersession index         sha256  4c8ad139f1e18c73fc5462c3e0958aa5aed245eeae43f68704313b49e85e7805
scar (preserved)           sha256  c201c11b89195e0e099060f6c9c17029a97f24b68f7ad4f1cd193ed48bb4a2c4
```

## What was NOT done tonight (no scope expansion)

- No edit to `/root/arif-fazil.com/arifos/`.
- No Caddy reload.
- No `/api/...` endpoint call.
- No audit `hd-state.json` (no audit request).
- No carry-forward queue row added.
- No new F13 word request.
- No site regen.

> Audit closed. Recommendation proposed. Implementation awaits sovereign decision.
> Audit selesai. Cadangan dikemukakan. Pelaksanaan menunggu keputusan berdaulat.
