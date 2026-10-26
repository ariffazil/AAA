# A2A Auth Hardening — Preservation Record (2026-10-24)

**Branch:** `preserve/live-auth-hardening-2026-10-24` @ `16d43d9a`
**Base:** `180ec14c` (aaa/warga-claude-code) · **Witnessed delta:** 185+/53− across 5 paths
**Provenance:** the hardening ran LIVE in `aaa-a2a.service` (PID 1991167, loaded
2026-10-22 19:34:57) but existed in no commit. This branch is its Git lineage.

## Failure class prevented

The live A2A gateway ran security-critical auth code with zero Git custody.
If the worktree were lost, the fix would be lost with it — while the remote
backup looked healthy. (`deployed_commit=6fdd993` in `/health` was a
provenance lie; the only honest identifier was the worktree sha.)

## The four consequence commits

| Commit | Scope | Failure prevented |
|---|---|---|
| `1474cfe5` | proxy trust | spoofed XFF entry anywhere in chain → loopback bypass. Now rightmost-only. |
| `4303b0fe` | TDZ + replay + freshness | unsigned 403 crashed the gateway (TDZ); tasks/send had NO replay guard; no time bound |
| `fcddcf1c` | actor authorization | `anonymous` was canonical; unsigned agent dispatch; claimed actor was decorative (now DID-bound, scope-checked) |
| `16d43d9a` | identity key dedup | lowercase key duplicated canonical identity; registry/doc drift |

Commit order A→C→B is dependency-safe: the TDZ declaration must exist before
any commit whose code reads `effectiveSourceAgent`. Scopes match the handoff
table exactly.

## Acceptance gates — all green (2026-10-24T05:36–06:00Z)

**A1 authority fidelity** — diff touches exactly the 5 declared paths; no
actor added; no seal-path change; no executor judgment authority.

**A2 custody integrity** — canonical key `333-AGI_public.pem` (`b4dc3682…`)
untouched; final tree sha256-identical to live worktree (`5429511b` server /
`e02994e4` envelope / `ad1956d9` deprecated / `4885cabf` agents.json);
`git apply -R` reverts cleanly to HEAD; gitleaks: no leaks.

**A3 truthful reporting** — staging diff = live worktree bytes (sha-verified);
staging probes ≠ live probes (separately reported); `deployed_commit` stamp
known-defective upstream (separate defect, not fixed here).

**Functional (staging `:3101`, throwaway DID, socat non-loopback source):**

| Probe | Result |
|---|---|
| XFF spoof `127.0.0.1, 1.2.3.4` from non-loopback | PASS — 403 loopback-only (old code: bypass) |
| XFF legit rightmost `1.2.3.4, 127.0.0.1` | PASS — Caddy tunnel path preserved (DID_REQUIRED) |
| no XFF from non-loopback | PASS — 403 loopback-only |
| claimed actor `anonymous` | PASS — 403 not-canonical |
| TDZ: service alive after 403s | PASS — active through battery |
| unsigned agent dispatch (`/a2a/message/send` + `/a2a` JSON-RPC) | PASS — 403 DID_REQUIRED |
| valid signed dispatch (positive control) | PASS — auth cleared; dispatch hit env dependency |
| byte-identical replay | PASS — `-32004` duplicate rejected |
| stale `issued_at` (−6 min) | PASS — `-32005` freshness window |
| actor outside DID scope | PASS — 403 ACTOR_BINDING |
| actor in DID scope | PASS — binding accepted, dispatched |
| envelope-claim enforcement (message/send own set) | PASS — 888_HOLD deny layers fire before dispatch |

Existing suites: `envelope_v1` 8/8 · `proof-gate-honesty` PASS ·
`seed-agents` 31/3-fail — **identical 3 failures pre-exist at base `180ec14c`**
(verified on a clean baseline worktree; not a regression).

## Not done here (deliberate)

- **No deploy/restart of `aaa-a2a`** — live already runs this exact code
  (byte-verified); a restart adds downtime risk with zero auth delta.
- **No thaw of `/root/AAA`** — immutable (`chattr +i`); source-to-live
  convergence for the other 179 worktree entries is a later phase.
- Stale keys at `/root/.local/share/arifos/agent_keys/` (d73852df/cb747ac1)
  — left untouched pending the `p0-identity-key-split-333agi` decision.
