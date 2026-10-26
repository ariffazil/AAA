# Canon Authority Topology — 2026-10-23

**F13 decision (2026-10-23):** KEEP the canon trees federated. Do not merge into one physical directory. Require one constitutional source, explicit ownership, one-way projection, deterministic conflict resolution.
**Status:** `PROPOSED` — not ratified. Lives in `AAA/state/` (operational state), not in `AAA/canon` (agent-facing canon) and not in `GENESIS` (source doctrine), precisely because it is not yet F13-ratified.

## The five live trees (measured, not reported)

| # | Path | Files | Git-tracked | Immutable (`+i`) | Manifest sha256/16 |
|---|---|---|---|---|---|
| 1 | `/root/arifOS/GENESIS` | 70 | 70 (repo `arifOS`) | yes — dir + all 62 top files | `dfa1be3267492c56` |
| 2 | `/root/AAA/canon` | 308 | 304 (repo `AAA`) | yes — dir + 208 md | `a6adf5da6441560d` |
| 3 | `/root/AAA/governance` | 371 | 363 (repo `AAA`) | yes — dir | `2bb6ee0c10cbaf72` |
| 4 | `/root/arifOS/governance` | 10 | tracked | **no** | `4a1db072ccdb8226` |
| 5 | `/etc/arifos/canon` | 5 | **0 — not tracked** | yes — dir + files | `b72e755c5c4ea97d` |

Note on #4: `/root/arifOS/governance/ZEN_INIT_CANONICAL.md` is a **symlink into `/root/AAA/canon/`**. That is the observed "divergence instance" — it is an alias, not a second source.

## The seven required fields per tree

| Tree | Owner | Authority class | Allowed writers | Source relationship | Projection direction | Conflict rule | Version/hash linkage |
|---|---|---|---|---|---|---|---|
| `arifOS/GENESIS` | F13 (sovereign) | **CONSTITUTIONAL SOURCE** | F13-ratified commit on `arifOS` (lane-gated) | is the source | → projects into `/etc/arifos/canon` (hashed) and referenced by `AAA/canon` | GENESIS wins over every other tree | git SHA of `arifOS`; per-file sha256 in `/etc/arifos/canon/canon-release.json` |
| `/etc/arifos/canon` | arifOS release train | **GENERATED RUNTIME PROJECTION** (machine-consumed, minimal) | `arifOS/scripts/deploy-release.sh` Step 5-pre, and nothing else | generated from `arifOS/config/*` + hashes of `AAA/canon` | one-way **from** repo **to** `/etc` | carries the source commit; never authoritative on its own | `canon_version = YYYY.MM.DD-<git_commit>`, `source_commit`, per-file sha256 |
| `AAA/canon` | AAA institution | **AGENT-FACING INTERPRETATION** | lane-gated commit on `AAA` (propose → F13 ratifies) | interprets GENESIS; may not contradict it | → read by `arifOS/governance` symlink; hashed into `/etc` manifest as `external_ratified_canon` | GENESIS > AAA/canon; on conflict the GENESIS text governs and AAA/canon is corrected | git SHA of `AAA`; file names carry `YYYY-MM-DD` ratification date |
| `AAA/governance` | AAA institution | **POLICY / PROCEDURE / GATES** (application, not canon) | lane-gated commit on `AAA` | implements and binds; derives from canon, does not define it | → constrains agents and tools at runtime | derivative: if it disagrees with canon, canon wins and the policy is a bug | git SHA of `AAA` |
| `arifOS/governance` | arifOS repo | **LEGACY ALIAS / CONTRACT HOLDOVER** | `arifOS` commits | alias + contracts (`authority.json`, ratchet, amendments) | none — should resolve into AAA/canon or be retired | canon wins; this tree has no independent authority | git SHA of `arifOS` |

Invariant this table encodes:

```
GENESIS (source)
   ↓ generate/project
/etc/arifos/canon (runtime projection)
   ↓ constrains
AAA/canon (interpretation) + AAA/governance (application)
```

Not: four trees, four parties legislating independently.

## Verdict — `HOLD` (not `RESOLVED_BY_ARCHITECTURE`)

**Falsifier:** `/root/AAA/state/lane-d/lane-d-canon-write-denial-probe.py`
**First run:** 2026-10-23T15:36Z → `RED_NOT_ENFORCED` (4 pass / 6 fail)
**Receipt:** `receipts/lane-d-probe-20261023T153622Z.json`

| # | F13 check | Result | Measured |
|---|---|---|---|
| 1 | harness UID is not the canon owner | **FAIL** | harness uid=0; GENESIS, AAA/canon, /etc/arifos/canon all uid 0 |
| 2 | source owned by a separate identity | **FAIL** | all three trees `root:root` — same identity as the harness |
| 3 | no ambient `CAP_LINUX_IMMUTABLE` | **FAIL** | `CapEff=0x000001ffffffffff`; bit 9 set; `CAP_DAC_OVERRIDE` set |
| 4 | write to GENESIS denied | PASS | `EPERM` — but only because the file carries `+i` |
| 5 | write to protected projection denied | **FAIL** | `open(O_WRONLY\|O_APPEND)` on `/etc/arifos/canon/canon-release.json` **succeeded** |
| 6 | hashes unchanged after attempts | PASS | GENESIS `92a2d086…`(70f) · /etc canon `60066a3a…`(5f) · AAA/canon `da889e0e…`(308f) |
| 7 | denial receipted (actor/path/op/ts) | **FAIL** | no canon-write denial ledger exists (auditd is active, but no sensor watches these paths) |
| 8 | authorized generation path intact | PASS (not executed) | `deploy-release.sh` present + executable |
| 9 | break-glass is human-gated | **FAIL** | scratch proof: this identity can `chattr -i` and then write |
| 10 | repeatable after restart | PASS | fresh process, deterministic per-check output |

### Immutability coverage — protection is per-file, and one tree has none

| Tree | files | `+i` | unprotected |
|---|---|---|---|
| `/root/arifOS/GENESIS` | 70 | 70 | 0 |
| `/root/AAA/canon` | 308 | 308 | 0 |
| `/root/AAA/governance` | 371 | 371 | 0 |
| `/etc/arifos/canon` | 5 | **0** | **5** |
| `/root/arifOS/governance` | 10 | **0** | **10** |

`/etc/arifos/canon` carries `+i` only on the **directory** — which blocks adding or removing entries, not modifying the contents of an existing file. That is the tree the kernel reads as ratified authority:

- `arifos` MainPID env: `ARIFOS_CANON_DIR=/etc/arifos/canon`
- its mountinfo: `/etc/arifos rw,nosuid,relatime`
- `systemctl show arifos -p ReadOnlyPaths` → `/opt/arifos /opt/arifos` (duplicated — the drop-in that should have added `/etc/arifos` never did)
- `fhs-map.yaml` declares `ProtectSystem=strict`, `ReadOnlyPaths=/opt/arifos /etc/arifos`, `CapabilityBoundingSet=` empty; the live unit has `ProtectSystem=no`, `/opt/arifos` only, and a full capability set

So the authority the kernel trusts most has the weakest write protection on the host. Nothing was modified during the probe — the open succeeded and was closed without a write; all three manifest hashes are unchanged.

## Identity capability — measured on the production identities (2026-10-23T15:44Z)

`lane-d-identity-capability-probe.py` → `NOT_SEPARATED` (receipt `receipts/lane-d-identity-probe-20261023T154421Z.json`)

| identity | uid | verdict | root-equivalent group | write GENESIS | write `/etc/arifos/canon` | write AAA/canon |
|---|---|---|---|---|---|---|
| `arifos` (kernel) | 994 | **ROOT_EQUIVALENT** | `docker` | DENIED | **DENIED** | DENIED |
| `forge` (executor) | 986 | COMPLIANT | — | DENIED | DENIED | DENIED |
| `a-forge-mcp` | 0 | **PRIVILEGED** | root | DENIED | **ALLOWED** | DENIED |
| `hermes-asi-gateway` | 0 | **PRIVILEGED** | root | DENIED | **ALLOWED** | DENIED |
| `forge-bot` | 0 | **PRIVILEGED** | root | DENIED | **ALLOWED** | DENIED |

Hashes unchanged after every attempt: `true`.

### Correction to the previous draft of this document

The earlier claim that *"the kernel can write the canon it reads"* was **wrong at the DAC layer and right in effect**:

- the kernel runs as `arifos` uid 994, and `open()` on canon is **DENIED** — the non-root design works;
- but uid 994 is a member of `docker`, and `docker ps` succeeds. Socket access is root-equivalent (`docker run -v /etc:/host`), so the DAC boundary is bypassable in one command by the identity the kernel runs as;
- `arifosmcp/runtime/webmcp/live_metrics.py:199-204` is the **only** docker consumer — three counters (`docker_containers`, `docker_running`, `docker_images`) inside `try/except: pass`. Losing docker degrades them to `0`; it does not break the kernel.

So the ranking is inverted from what the first probe suggested:

```
not the issue:  missing +i on 5 files           (defence in depth)
the issue:      3 services run as uid 0         (direct write, measured ALLOWED)
                + kernel holds docker group      (root-equivalent bypass)
                + kernel reads what they write   (no writer separation)
```

Fix all three, and the missing `+i` becomes hygiene rather than exposure.

### What the earlier claim got wrong

The previous draft of this document said "the barrier today is file immutability + systemd sandbox". Measurement says: for GENESIS and AAA/canon the barrier is immutability (removable by this identity); for `/etc/arifos/canon` there is **no file barrier at all**, and the systemd barrier that `fhs-map.yaml` claims is not installed.


## What would close s5 (single condition, not a new system)

> A write attempt against `GENESIS`, `AAA/canon` or `/etc/arifos/canon` **from an agent identity** must be **denied and receipted**, and that denial must be demonstrated by a test (attempt → DENY → hash unchanged), the same way `drive_create` demonstrates `LEASE_CLASS_EXCEEDED`.

Minimum shapes that satisfy it, in increasing cost and authority:

| # | Change | Flips checks | Authority tier | Why it is not done here |
|---|---|---|---|---|
| a | `chattr +i` on the 5 files of `/etc/arifos/canon` | 5 | T1 (protection increase, no content change) | breaks `deploy-release.sh` Step 5-pre (`install` over an immutable file). Must land **with** the generator change, or the next release fails. |
| b | install the declared drop-in: `ReadOnlyPaths=/etc/arifos`, `ProtectSystem=strict`, `CapabilityBoundingSet=` | 1,2,3 (for the kernel only) | T2 (service boundary change) | changes the kernel's runtime posture; needs F13, and `ReadOnlyPaths=/opt/arifos /opt/arifos` shows the last such edit half-landed. |
| c | run agent harnesses under a uid that does not own the trees; chown trees to that boundary | 1,2,3,9 | T2/T3 (identity + ownership of constitutional source) | irreversible-ish, touches every agent lane; sovereign decision. |
| d | execution-gate path rule denying writes to the five paths, with a denial test in CI | 4,5,7 | T1.5 (in-path guard in the executor) | A-FORGE mutation beyond `serve.ts`; Lane C authorization explicitly excluded it. |

Recommended sequence: **(a) + generator update** to stop the silent-edit hole immediately (cheapest, reversible), then **(b)** to make the kernel's declared boundary true, then **(c)** for the real identity separation. (d) only if (c) proves impractical.

Until one exists: `s5 = HOLD_MULTI_WRITER_UNGUARDED`. The falsifier is now executable, so the next session re-runs one command and reads the delta — no narrative required.

