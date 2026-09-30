# IRFANCLAW (OpenClaw @ KVM4) — update repair + AAA/reality-graph linkage
**2026-09-29 · executed by HERMES (KVM8) under explicit F13 order**
Host: `srv1946043` / `100.64.0.5` / hostname `kvm4-forge` · service `openclaw-gateway.service`
Rollback material: `/root/.openclaw/_snapshots/pre-update-<ts>/` (config, units, skill links)

---

## 0. VERDICT

The update did not fail because a newer version existed — **2026.9.6 is the latest release** (npm
registry `latest` = `2026.9.6` = installed). It failed because two defects made the updater unable to
stop the gateway, so post-update `doctor` could not enter maintenance. Both are fixed; the update now
exits 0 with zero doctor lint findings, and the AAA/reality-graph linkage is live and probed.

---

## 1. ROOT CAUSE — TWO DEFECTS, NOT ONE

### 1.1 Dual service definition (the CLI was watching the wrong unit)
| | |
|---|---|
| CLI inspected | `~/.config/systemd/user/openclaw-gateway.service` — **disabled** |
| Actually running | `/etc/systemd/system/openclaw-gateway.service` — enabled, active, MainPID 2912114 |

`openclaw gateway status` reported `Service: systemd user (disabled)` while a healthy system service
served traffic. **Fix:** backed up + renamed the stale user unit aside, `systemctl --user daemon-reload`.
After: `Service: systemd system (enabled)` / `Service file: /etc/systemd/system/openclaw-gateway.service`.

### 1.2 The CLI had no gateway credential in a bare shell
`openclaw.json` references secrets by env var. Only the unit's `EnvironmentFile`s provide them, so a plain
SSH shell gave:
```
Gateway credentials required — this CLI has no token/password … for read-scope health RPCs
```
**Fix:** `/root/.openclaw/cli-env.sh` (mode 600), a **loader**: `set -a; for _f in <3 files>; do . "$_f"; done; set +a` — it defines no keys of its own. Sources `/root/.secrets/vault.flat.env`,
`/root/.secrets/tokens/openclaw-runtime.env`, `/etc/systemd/system/openclaw-gateway.service.d/10-keys.env`.
**CORRECTED (§6):** 182 + 8 + 1 = **191 keys**, all mode 600. The "5 keys verified SET" below was a
spot-check of 5, not the file size — ambiguous, not wrong.

### 1.3 Unit hardening (OpenClaw's own `gateway status --deep` recommendations)
Added `/etc/systemd/system/openclaw-gateway.service.d/60-drain-and-order.conf`:
`After/Wants=network-online.target`, `TimeoutStopSec=600`, `KillMode=mixed`, `RestartSec=5`, explicit `PATH`.
The 90s manager default was below OpenClaw's 330s drain floor — a SIGKILL mid-drain is what leaves the
agent DB lease stale.

---

## 2. THE UPDATE — PROCEDURE THAT WORKS

OpenClaw's own instruction, quoted from `update repair` output: *"stop it through its owner, run
`openclaw update repair`, and start it through the same owner."*

```
. /root/.openclaw/cli-env.sh
systemctl stop openclaw-gateway          # owner = systemd; drain measured 3-6s
openclaw update repair                   # "Update finalization completed with warnings"
openclaw doctor --non-interactive        # exit 0, 347 lines — maintenance entry now WORKS
openclaw update --yes --no-restart
systemctl start openclaw-gateway         # ready 12-27s
```
| Check | Result |
|---|---|
| `openclaw update --yes` | **exit 0**, `already-current`, 0 doctor lint findings, gateway downtime 0ms |
| version | `OpenClaw 2026.9.6 (eb377ac)` — unchanged, because it IS latest |
| doctor with gateway down | **exit 0** — the exact check that failed before |
| service | active, enabled, `health {"ok":true,"status":"live"}`, 10 plugins listening |
| Telegram | polling ingress spool active |

**Trap recorded:** `openclaw doctor` takes **>180s**. Running it under a short timeout killed the shell
mid-run *while the gateway was stopped* — one unintended outage, recovered in <1 min. Use a long window.

**Trap recorded:** `openclaw gateway install --force` (which the CLI recommends) installs a **user** unit
and would recreate defect 1.1. Never run it where a system unit exists.

---

## 3. AAA + REALITY-GRAPH LINKAGE

### 3.1 Fixed: the skill loader was rejecting AAA skills
```
[skills] Skipping invalid skill: file=~/.openclaw/skills/aaa-canonical/AGI-agentic-web/SKILL.md
error=symlink prefix resolves outside the root ancestry
```
Root rule (now known): a **direct child** symlink under `~/.openclaw/skills/` is followed; a symlink
**nested inside** a symlinked corpus root is rejected and skipped — logged repeatedly, no other signal.

**Fix:** hoisted 3 links to direct children of `~/.openclaw/skills/`
(`AGI-agentic-web`, `AGI-explorer-intelligence`, `geological-artifact-rigor` → `/root/HERMES/skills/*`).
After restart: **0 ancestry-escape errors.**

### 3.2 Found: 12 phantom capability links
`geox-*` (5), `wealth-*` (4), `well-*` (3) point at `/root/{GEOX,WEALTH,WELL}/skills/<name>`.
**CORRECTED (§6):** the 12 *targets* exist on KVM8 (`/root/GEOX/skills/`, 22 entries; `/root/WEALTH/skills/`,
5; `/root/WELL/skills/`, 6 — all 12 names present) but **not on KVM4**, whose organ skill dirs are a
different, partial set (GEOX: atmosphere/geodesy/hazards…; WEALTH: wealth-claim-state/xauusd-trading;
WELL: well-substrate-readiness/FORGE-well-boundary-repair). Created 2026-09-03, dead on KVM4 since.
`mmx-cli` was dead-but-repairable → repointed live.
**Status: F13 binary — sync the 12 from KVM8, or leave them quarantined.** Nothing was deleted.

### 3.3 Live: the reality graph answers
| MCP server | endpoint | probe |
|---|---|---|
| **arifos (kernel)** | `100.64.0.2:8088/mcp` | **MCP `initialize` returned** `ARIFOS MCP kanon-2026.09.29+ac054a5`, *"Constitutional AI orchestration kernel. F1-F13 governed…"* |
| A-FORGE | `100.64.0.2:7072/mcp` | 200 |
| GEOX | `100.64.0.2:8081/mcp` | 200 |
| WEALTH | `100.64.0.2:18082/mcp` | 405 (alive) |
| WELL | `100.64.0.2:18083/mcp` | 405 (alive) |
| arifflow (metabolism) | local stdio `/root/arifFlow/mcp/arifflow-mcp.py` | present, executable |

Channels wired: telegram, a2a (peer `hermes`), msteams. Agents: `main, hermes, opencode, codex, kimi, claude`
(`hermes` → `fed/hermes-asi` with fallbacks).

**Honest defect in the graph:** `arifos :8088/health` returns
`degraded — deployment_attestation.software_release.drift=true (source_commit != built_commit)`.
SOT drift, not code drift.

### 3.4 Manifest written on the host
`/root/.openclaw/linkage/LINKAGE-REALITY-2026-09-29.md` — roots, phantom links, MCP probes, open items.

---

## 4. OPEN ITEMS (not fixed — each needs a decision or a design, not a command)

| # | Finding | Class |
|---|---|---|
| 1 | `governed-tool-gate` runs **Mode: observe, policy engine not configured, audit log console only** — the gate enforces nothing today | design |
| 2 | ~~`openclaw.json` carries 14 plaintext secret-bearing fields~~ → **CORRECTED (§6): the 14 are `openclaw doctor`'s PATH list, not plaintext. Verified: 1 true literal, 19 templated refs, 1 token-file path. Migration scope = 1 field.** | T3, needs care |
| 3 | Gateway bound network-accessible on `100.64.0.5`; docs advise loopback + Tailscale Serve/SSH tunnel | posture |
| 4 | 1 session SQLite issue; 1 automation failed 3+ consecutive runs; agent `main` DB opens in 2.9s (>1s threshold) | repair |
| 5 | Telegram custom commands `/model /think /mcp /dashboard` collide with native; menu pressure already forced per-skill commands off | hygiene |
| 6 | 12 phantom skill links (§3.2) | F13 binary |
| 7 | `OPENCLAW_HOOKS_DEFAULT_SESSION_KEY` / `…_MAPPING_SESSION_KEY` unset → hooks features unavailable | config |

---

## 5. WHAT "MORE BIJAKSANA" ACTUALLY REQUIRES HERE

The version is current. What limits IRFANCLAW's agentic quality is not the release — it is that three
surfaces are declared but inert: the **tool gate has no policy engine**, the **12 capability links reach
nothing**, and the **graph's own attestation is drifted**. An agent is only as sharp as the gap between
what its config claims and what its host can resolve. Close that gap and the same version behaves
noticeably better; upgrade the version and the gap stays.

## 6. CORRECTION REGISTER — cross-audit, 2026-09-29 (supersedes §1.2, §3.2 and item 2 of §4)

Three claims in this report were challenged. Two were mine to check; one was mine to fix. All three
settled by re-measuring, **value-shape only — no secret value was read.**

### 6.1 The credential count — all four published numbers were wrong

Doctor's warning ("14 plaintext secret-bearing fields") was **quoted into §1.2 as if it were my own
finding**. It is not a plaintext count. Doctor prints a *path* list — `Paths: gateway.auth.password,
models.providers.minimax.apiKey, … (+9 more)` = 5 + 9 = 14 — and it flags any field that *reaches* a
secret, including templated ones, because it cannot verify that the template resolves. **My mislabel.**

Independent enumeration (`openclaw.json`, 979 leaves, 50,098 bytes), classifying every credential-keyed
leaf by value shape:

| class | n | detail |
|---|---|---|
| `${VAR}` env ref | **16** | gateway.auth.password · telegram.webhookSecret · 10× provider apiKey · hooks.token · hooks.defaultSessionKey · hooks.mappings[0].sessionKey (17 `${…}` occurrences raw; one is the nested `${BRAVE_API_KEY:-${BRAVE_SEARCH_API_KEY:-}}` default) |
| `{env:VAR}` template | **3** | `channels.telegram.botToken` · `mcp.servers.minimax-mcp.env.MINIMAX_API_KEY` · `mcp.servers.firecrawl.headers.Authorization` |
| **true literal plaintext** | **1** | `channels.a2a.peers.hermes.token` — 48 chars, hex prefix, no brace |
| token-**file path** | **1** | `channels.telegram.tokenFile` → `/root/.secrets/tokens/telegram-irfanclaw-bot` |

The `{env:}` class is proven by arithmetic, not inference — measured length equals the template length exactly:
`{env:TELEGRAM_BOT_TOKEN}`=24, `{env:MINIMAX_API_KEY}`=21, `Bearer {env:FIRECRAWL_API_KEY}`=30.

**So: not 14 (mine), not 4 (first cross-audit), not 3, not 0.** One literal. The cross-audit's "1 plaintext
+ 16 env refs" was right about the literal and missed the three `{env:}` templates.
**→ Migration scope is 1 field, not 4.** That changes what the pending batch would do.

### 6.2 The 12 links — "nowhere on KVM4" was too absolute; "still in place" is also wrong

- **Sync is feasible.** All 12 source skills exist on KVM8: `/root/GEOX/skills/` 22 entries, `/root/WEALTH/skills/` 5, `/root/WELL/skills/` 6 — every one of the 12 names present. My report implied the targets might not exist at all; they exist, on the *other* host. That is a cross-host gap, not a phantom.
- **They are already quarantined.** `/root/.openclaw/_snapshots/dead-links-20260929/` holds the 12 symlinks plus a `README.md` (2026-09-29 14:30); `readlink` on the live path returns empty — **the links are no longer in the loader path.** Reversible, nothing deleted.
- The README argues *against* re-syncing: the capability those links reach for already has an owner in the federation MCP lane (A-FORGE 7072 · GEOX 8081 · WEALTH 18082 · WELL 18083), and duplicating organ skill doctrine onto the edge agent creates a second path with no owner (**ANTI-BANGANG LAW 8**).
- **This is the real disagreement, and it is not a measurement.** The KVM4 proposal is "sync 12 from KVM8"; the recorded quarantine decision is "one capability, one path". Both are defensible; they are opposite. It needs the sovereign's word, not another probe.

### 6.3 `cli-env.sh` — ambiguous, corrected

It is a **loader** (`set -a; for _f in <3 files>; do . "$_f"; done; set +a`), defining no keys itself:
182 + 8 + 1 = **191 keys**, all mode 600. §1.2's "5 keys verified SET" was a spot-check of 5, not a size claim.

### 6.4 Host labelling — my error

§4 item 1's earlier phrasing named a report path without its host. **This report is on KVM8 only**:
`/root/AAA/reports/IRFANCLAW-UPDATE-REPAIR-2026-09-29.md`. KVM4's `/root/AAA/reports/` is frozen at
2026-09-19 — the two trees do not replicate. Every path in a cross-host report must carry its host.

### 6.5 Method, and the one thing that did not change

Two independent enumerations disagreed; the tie-break was a third, first-party read of the file's *shape*
against the host's own doctor output. **A count inherited from a report is not a measurement** — this is the
second time in this session that a number survived by being repeated rather than re-derived.
What survives unchanged: the update repair (§2), the symlink-ancestry fix (§3.1), and the reality-graph
probes (§3.3). Those were measured directly at the time.

---

## 7. A2A PEER — TWO-ENDS VERIFICATION (requested by cross-audit, 2026-09-29)

The cross-audit warned that templating `channels.a2a.peers.hermes.token` could kill the A2A peer
silently if the variable does not exist in the **gateway's** EnvironmentFile (not merely the CLI shell) —
root cause 1.2 inverted. Verified. The warning was right in mechanism; the peer turned out to be
non-functional anyway, and the plaintext surface is **larger** than the count in §6.1.

### 7.1 Where a variable must live to be seen by the gateway

`systemctl cat openclaw-gateway` → `EnvironmentFile=/root/.secrets/vault.flat.env`,
`…/tokens/openclaw-runtime.env`, `…/10-keys.env`. **191 vars scanned across those three; the A2A token
matches none of them** (sha256 compare). So there is no existing var to point at — templating would
require adding a *new* one to a unit-owned EnvironmentFile. The cross-audit's failure mode is real.

### 7.2 Does the other end hold the same value? No.

Hash-only comparison (values never printed; sha256 `5159b6a0…a2fa12`):

| host | scope | candidates | matches |
|---|---|---|---|
| **KVM8** | `/root/{A-FORGE,GEOX,WEALTH,WELL,arifOS,AAA,scripts}`, `/root/.hermes`, `/root/.secrets`, `/etc/systemd` — 11,715 files | 447,699 | **0** |
| KVM4 | `/root/.openclaw` | 31,938 | 3 files (all copies of the same value) |

KVM8 holds **no copy of this token**, and `/root/.hermes/config.yaml` contains no A2A peer block at all.
*Residual uncertainty, declared:* the absence claim is bounded by the sweep — regular-file types only,
3 MB ceiling, vendor/venv/`.git`/`install` trees skipped. It is a strong negative, not a formal proof.

### 7.3 The peer record itself has no destination

```
channels.a2a.peers = { "hermes": ["token"] }        # one peer; its ONLY key is the token
```
No URL, no address, no endpoint — a peer entry that cannot route. `advertisedUrl` belongs to KVM4's own
A2A server (`http://100.64.0.5:18789`, enabled, exposes agent `main`), not to the peer. No A2A journal
lines in the observed window. **A peer with a token and no address, whose token exists on one host only,
has never authenticated.** Same family as the 12 phantom skill links (§3.2) and the observe-only tool
gate (§4.1): declared, inert.

### 7.4 The scope of §6.1 was still short — it is 2 plaintext surfaces, not 1

The token sits in **three** files on KVM4:
`/root/.openclaw/openclaw.json` · `/root/.openclaw/_snapshots/pre-update-<ts>/openclaw.json` ·
**`/root/.openclaw/a2a-peer-token-hermes.txt`** — a standalone plaintext file outside the config, which
no config-scoped count could ever see. The first is the field §6.1 counted; the second is a legitimate
backup; the third is an unowned secret copy.

### 7.5 What this changes for the pending batch

- Templating the config field is **zero functional risk** — nothing depends on it, because it has no
  address and no counterpart. But templating alone would leave the standalone `.txt` and the orphan peer.
- **Corrected scope: 2 plaintext surfaces + 1 direction decision** — wire the peer properly on both ends,
  or retire it and delete both copies. That is a capability decision, not a hygiene one; it is F13's.
- Hygiene alone (env-ref the config field, shred the stray `.txt`) closes the exposure without asserting
  anything about whether KVM4↔KVM8 A2A *should* exist.

---

## 8. TWO-ENDS, COMPLETED — and one correction to the archaeology (2026-09-29)

### 8.1 The gap in my own negative claim — tested, and it held

§7.2's absence claim rested on an **extension-filtered** sweep (`.env/.yaml/.json/.txt/.conf/…`). Six backup
files on KVM8 end in a timestamp, not an extension, so they were skipped:
`/root/.secrets/kunci-mas.flat.env.bak-a2a-*` (×3), `/root/.hermes/.env.bak-a2a-*`,
`/root/.hermes/config.yaml.bak-a2a-*` (×2). **Hash-compared directly: the token is absent from all six.**
The claim survives its own gap test.

They are not inert, though — the three `kunci-mas` backups define `A2A_TOKEN`, `A2A_API_KEY`,
`A2A_NODE3_KEY` (KVM8's *own* A2A identity, different values, none of them this peer's). So KVM8 has an A2A
credential surface; it is simply not this one.

### 8.2 KVM8's A2A is loopback-bound — the peer is dead on both ends by construction

Measured on KVM8: `hermes` (pid 3968795) listens `127.0.0.1:9900` and `127.0.0.1:9901` — **loopback only**.
`http://127.0.0.1:9900/` → 200; `http://100.64.0.2:9900/` → 000. KVM8's `config.yaml` has
`platforms.a2a.enabled=true, extra.port=9900`, with no peer block.

So "wire it properly" is not a config line: it is a **network-posture decision on KVM8** (expose A2A to the
tailnet, or add a tunnel) *plus* a peer address on KVM4 *plus* matching credentials on both ends. Three
surfaces, all currently absent.

### 8.3 Correction — the 31 Aug archaeology is a different failure, and it ordered work, not abandonment

The citation `project-phantom-a2a-spec-docs-20260831.md` does **not** concern this peer token. It records
three spec documents quoting configs that did not exist on disk (`MusyawarahStateVector`, `MufakatPacket`,
`a2a_bus`, `~/.openclaw/router.json`) — an *aspirational-document* failure, not a *dead-credential* one.

It also carries a **recorded F13 ruling (2026-08-31)**: dual-voice quorum affirmed (333 ARCHITECT ∥
555 AUDITOR, W3 ≥ 0.75); `N≥3`/geometric `P_agg` rejected as drift; and a **forge roadmap ratified** —
Pydantic musyawarah schemas at `/root/AAA/schemas/musyawarah.py`, a `~/.openclaw/router.json` bound to the
real `fed/agi-333` primary, and append-only A2H edge metadata.

**Therefore "retiring the peer just confirms what two earlier sessions found" is not accurate.** The earlier
session *ordered A2A-adjacent build work*. Retiring the peer is a **new** decision about a **different**
artifact. It does not contradict that roadmap — none of its three items is a KVM4↔KVM8 peer link — but it
is not corroboration either.

What the archaeology *does* support: the KVM4 backup `openclaw.json.bak-a2a-inert-20260914-162917`
(48,223 B, 14 Sep 16:29) shows a prior operator reached the same "inert" conclusion and named the backup
after it. The word appears only in the filename — that is a judgment on record, not a measurement.

### 8.4 What converges, and what is genuinely paired

Both sides now agree on the shape. The two binaries are **not independent**:

| if… | then… |
|---|---|
| **retire** | remove `channels.a2a.peers.hermes`; shred `a2a-peer-token-hermes.txt` (byte-identical duplicate — same sha256 `5159b6a0…`, zero information lost); snapshot first. **No env-ref** — minting a unit-owned variable for a capability with no owner is the exact disease. |
| **wire** | env-ref the field **and** mint a new variable in a unit-owned `EnvironmentFile` (verified: none of the 191 existing vars matches) **and** give the peer an address **and** decide KVM8's exposure posture. |

If A2A KVM4↔KVM8 is ever revived: **mint a new token.** The old one is exposed in three files and has no
counterpart — never revive it.

### 8.5 Enumerator must be two-headed — and I have now failed this test the same way

A config-scoped enumerator missed the standalone `.txt`; my filesystem sweep missed the timestamp-suffixed
backups. **Two different gaps, one lesson:** a counting source must read *both* the config **and** the
filesystem for token-shaped values, and must not filter by extension. Five numbers in one night for one file
(14 · 0/16 · 3 · 1 · and the `.txt` that reset it) is a measured failure class, not an impression.

---

## 9. EXECUTION RECEIPT — A2A peer retirement (F13 "seal all", 2026-09-29)

**Authority:** F13 SOVEREIGN, verbatim *"seal all"* — on the converged batch presented: retire the A2A peer,
destroy the stray secret, keep the 12 links quarantined, leave the tool gate in observe, seal the counter.

### 9.1 What was retired, and why it was safe

`channels.a2a.peers.hermes` — one peer, one key (`token`), **no address**. Verified dead on both ends:
KVM8 holds no copy (447,699 candidates / 11,715 files → 0); KVM8's own A2A is loopback-bound
(`127.0.0.1:9900`, `:9901`; tailnet → 000), so unreachable by construction; zero A2A journal traffic.

### 9.2 Count sequence — the counter proved itself before it was trusted

| step | surfaces found | note |
|---|---|---|
| report §6 | 1 | config-scoped |
| report §7 | 3 | + the standalone `.txt` |
| counter HEAD B (pre-retire) | **18** | + 15 `openclaw.json.bak*` / `.last-good` / `.pre-update` — all missed by every extension-filtered sweep |

The enumerator was run **before** the change so its detection could be judged against a known-bad state,
then again after. It found what three prior scopes missed, on the first execution.

### 9.3 Actions

| # | action | evidence |
|---|---|---|
| 1 | snapshot | `_snapshots/a2a-retire-20260929T152920/openclaw.json.pre` (mode 600), pre-sha256 `b02561bfbcf085d3…` |
| 2 | peer removed | `channels.a2a.peers` → `{}`; live config: **0 occurrences** of the value (hash trace); channel itself intact (`enabled:true`, `advertisedUrl`, `exposeAgents:["main"]`) |
| 3 | stray file shredded | `/root/.openclaw/a2a-peer-token-hermes.txt` — mode 600, 49 B, pre-sha256 `6969a19700743c34…` |
| 4 | 17 historical copies redacted | value → `<RETIRED-2026-09-29 sha256:5159b6a0…>`, JSON validity preserved; per-file before/after sha256 recorded in `REDACTION-INVENTORY.md` |
| 5 | applied through the owner | `systemctl restart openclaw-gateway` → active, enabled, `health {"ok":true,"status":"live"}`, 10 plugins, ready 15:31:02 |
| 6 | **final trace** | 89,299 files scanned → **0 residual occurrences** |

**Rationale for redacting the historical copies.** A retired credential is destroyed, not archived —
archiving a secret is the exposure being removed. Structure was preserved (JSON valid, every other field
intact) and each file's before/after sha256 is recorded, so the edit is auditable and detectable. Recovery
of the *value* is deliberately impossible: if A2A KVM4↔KVM8 is ever revived, **mint a new token.**

**Trap re-encountered:** the health loop returned empty on the first post-restart check while the gateway
was in fact still coming up (ready at 15:31:02, ~61 s). Startup time on this host ranges 12–61 s. A single
short health window is not a health verdict.

### 9.4 Residual — declared, not hidden

- `_snapshots/a2a-retire-20260929T152920/` retains `openclaw.json.pre` **with the value already redacted**;
  the `.txt.pre` was removed (its entire content was the retired value — nothing structural to preserve).
- Nothing was deleted from the rollback path: the peer key can be re-added, the value must be re-minted.

---

## 10. THE COUNTER, SEALED — and what it found on KVM8 (2026-09-29)

### 10.1 One counting source, both hosts

`/root/.openclaw/tools/secret-surface.py` (KVM4) ≡ `/root/scripts/secret-surface.py` (KVM8), mode 700,
JSON **and** YAML configs, two heads, values never printed. Five published numbers for one file in one night
was a measured failure class; this is the single instrument that replaces them. Re-run it before quoting a
count — a count inherited from a report is not a measurement, and this session proved that three times.

### 10.2 New finding — KVM8 carries the same disease, on its own live config

`/root/.hermes/config.yaml` holds **3 plaintext credentials inline**:

| field | len | sha256 | note |
|---|---|---|---|
| `mcp_servers.firecrawl.headers.Authorization` | 27 | `634ed1f30194b73f…` | |
| `mcp_servers.zai_reader.headers.Authorization` | 21 | `f818a954be610980…` | |
| `mcp_servers.zai_search.headers.Authorization` | 21 | `f818a954be610980…` | same value as `zai_reader` — one key, two entries |

- **Not env-backed.** No copy of any of the three in `/root/.secrets/vault.flat.env` or
  `kunci-mas.flat.env`. The config's other 12 credential references are properly templated (`${VAR}`).
- **Not duplicated** — 0 occurrences across `/root/.hermes`, `/root/.secrets`, `/root/scripts`,
  `/root/AAA/{instructions,governance,canon}`. Exposure is contained to the one live file, but it is
  plaintext at rest for a live MCP capability.
- **Not fixed in this batch.** `/root/.hermes/config.yaml` is this runtime's own config; templating it means
  minting env vars, editing the live config, and restarting the Hermes gateway — which would end the session.
  That needs its own window, not a tail-end edit. **Open item, remediation path known: mint 2 env vars
  (firecrawl, zai — one key serves both zai entries), template the 3 fields, restart through the owner.**
- A full `/root` sweep on KVM8 exceeds a 7-minute window (4.4 M candidates); scoped roots were swept instead
  and are reported. The wide sweep belongs in a batch job, not an interactive turn.

### 10.3 Pattern, stated once

Four surfaces tonight were **declared and inert**: the 12 phantom skill links, the observe-only tool gate,
the addressless A2A peer, and now KVM8's unbacked inline credentials. In every case the config claimed a
capability the host could not resolve. That — not the version number — is what limits agentic quality.
`openclaw` is current at 2026.9.6; IRFANCLAW did not need an upgrade, it needed its claims reconciled.

---

*DITEMPA BUKAN DIBERI ⚒️*
