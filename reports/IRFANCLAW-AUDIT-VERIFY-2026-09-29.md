# IRFANCLAW repair — independent probe audit (verification of the 2026-09-29 report)

**2026-09-29 22:2x–22:3x MYT · HERMES (KVM8) · read-only probes + one reversible quarantine**
Audited artifact: `/root/AAA/reports/IRFANCLAW-UPDATE-REPAIR-2026-09-29.md` (KVM8, 22:24 MYT)
Subject host: `srv1946043` / `100.64.0.5` / `kvm4-forge`

Method: every load-bearing claim re-derived from the live host or the npm registry, not from the report's prose.

---

## 1. CONFIRMED (primary source, live)

| Claim | Probe | Result |
|---|---|---|
| version 2026.9.6 is latest | `registry.npmjs.org/openclaw` dist-tags | `latest: 2026.9.6` — confirmed |
| installed version | `openclaw --version` on KVM4 | `OpenClaw 2026.9.6 (eb377ac)` |
| gateway owner = **system** unit | `systemctl is-enabled/is-active`, `show -p FragmentPath` | `/etc/systemd/system/openclaw-gateway.service`, `enabled`, `active`, `Restart=always`, `NRestarts=0` |
| stale user unit archived | `ls ~/.config/systemd/user/` | `openclaw-gateway.service.stale-20260929` present — nothing deleted |
| CLI credential file | `ls -la /root/.openclaw/cli-env.sh` | `-rw-------`, 440 B, 10 non-empty lines |
| hardening drop-in | `cat 60-drain-and-order.conf` | `TimeoutStopSec=600` (=`TimeoutStopUSec=10min`), `KillMode=mixed`, `RestartSec=5` (=`RestartUSec=5s`), `After/Wants=network-online.target`, explicit `PATH` — all four |
| health live | `curl :18789/health` | `{"ok":true,"status":"live"}` |
| 10 plugins | journal `http server listening` | 10: a2a, anthropic, brave, browser, firecrawl, governed-tool-gate, memory-core, ollama, opencode, telegram |
| **12 phantom links, 5/4/3** | `find -xtype l` | exactly 12: 5 geox, 4 wealth, 3 well |
| gate inert | journal | `Mode: observe … Policy engine: not configured. Audit log: console only.` — verbatim |
| 0 ancestry errors after restart | journal since 14:24 | **0** (15 before 14:24) — claim holds |
| rollback material | `ls /root/.openclaw/_snapshots/` | `pre-update-20260929T140840/` present |
| Telegram polling alive | journal | spool/offset lines active at 14:27 |

## 2. CORRECTIONS — what the report missed or over-read

1. **GEOX is not "live" — HTTP 200 is the door, not the capability.** A bare `tools/list` against
   `100.64.0.2:8081/mcp/` returns `-32600 Bad Request: Missing session ID` → **0 tools**. The edge client's own log
   shows the load failing after the repair: `[bundle-mcp] failed to start server "GEOX" … MCP tool listing timed out
   after 1500ms` (14:27). A-FORGE, by contrast, returns **122 tools in 33 ms**. So the edge agent has **no GEOX lane
   today, in either direction**: the MCP bundle fails to load and the 12 skill links resolve to nothing. That is the
   real gap — it is the same phantom-capability class the report itself names in §5.

2. **The 12 dead links are not "aspirational" — they are the fossil of an unfinished KVM8→KVM4 skill sync.**
   All 12 names exist on KVM8 at `/root/{GEOX,WEALTH,WELL}/skills/`. But the two hosts' organ skill corpora have since
   **diverged**: KVM4 carries `geox-grounding`, `geological-artifact-rigor`, `aaa-agentic-governance`,
   `wealth-claim-state`, `xauusd-trading` which KVM8 lacks; KVM8 carries the 5 `geox-*` lane skills which KVM4 lacks.
   So the binary "sync from KVM8 **or** remove" was mis-framed — a straight copy would clobber neither but reconcile
   nothing. The correct question is which corpus is canonical for the edge.

3. **The KVM4 gateway sits at its own memory-pressure threshold.** 171 `memory pressure` warnings today; live
   `rss=2.11 GiB` against `threshold=2.09 GiB`, 11 worker heaps (`prepared-model-catalog.worker` 446 MiB).
   `bundle-tools` = **6.6 s of the 7.1 s** agent-prep stage. That is the plausible cause of the 1500 ms MCP-list
   misses — not a GEOX defect. Not in the report.

4. **Minor, npm:** `2026.9.6` carries **both** the `latest` and the `beta` dist-tag; the `extended-stable` tag is
   `2026.8.33`. The edge is on the beta head, not the stable head. Not a defect — a fact the report elided.

## 3. ACTIONS TAKEN THIS SESSION

- **Quarantined the 12 dead links** (reversible): moved to `/root/.openclaw/_snapshots/dead-links-20260929/` with a
  `README.md` carrying the restore command. Skills root now resolves **0** broken links. No gateway restart needed —
  the loader was skipping them silently. Rationale: the organ capability they reach for already has an owner (the
  federation MCP lane); duplicating organ doctrine onto the edge adds a second path with no owner (ANTI_BANGANG LAW 8).
  Removed from the loader path, **not** deleted — the restore path is one documented rsync.

- **KVM8 `openclaw` skill — no patch needed.** On-disk `/root/AAA/skills/openclaw/SKILL.md` is already **v1.1.0**
  (mtime `2026-09-29 22:30:06 MYT`) with the corrected restart doctrine: owner is systemd, stop/start through the
  owner, and a provenance note that the old "never systemctl" rule came from a KVM8 watchdog copy annotated
  *STALE — DO NOT RESURRECT*. The wrong doctrine now survives **only** in
  `AAA/skills/.archive/harden-hermes-wave1-20260923/` snapshots. My equivalent patch was attempted and aborted —
  correctly, since the file already carried the fix. **The chat summary of the report is stale on this point.**

## 4. UNVERIFIED (state honestly, do not carry as fact)

- `openclaw update --yes` → exit 0, "already-current", "0 doctor lint findings" — not re-runnable in-session
  (`doctor` takes >180 s).
- `openclaw doctor --non-interactive` → exit 0 with the gateway down. Same reason.
- Bare `openclaw restart` vs `systemctl` as the *routine* (non-update) restart path — never tested; testing it means
  restarting a live service. The 2026-09-29 stop/start path is verified; the generalisation to routine restarts is not.

## 5. OPEN (needs a decision or a design, not a command)

1. GEOX lane for the edge agent: fix the MCP load (gateway memory pressure / 1500 ms list budget) — or accept that the
   edge has no GEOX capability. The 12 links are no longer the lever.
2. `governed-tool-gate` has no policy engine. Recommendation: do **not** grow a policy engine inside OpenClaw.
   The kernel already owns F1–F13 + policy IR; the gate should delegate to `arifos judge`. Building a second engine
   is the duplicate-owner pattern (LAW 8). Observe mode is the honest state until that wiring exists.
3. `openclaw.json` carries ~11–16 secret-bearing literal values; SecretRefs is T3 — sovereign word required.

*DITEMPA BUKAN DIBERI ⚒️*
