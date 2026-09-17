# G2 — CARE-GOVERNOR · report

> `trace_id: care-2026-09-17` · agent G2 · SPEC: `/root/AAA/state/care-build/SPEC.md` §G2
> State: **A PRODUCED+VERIFIED · B PRODUCED (application HELD: F13) · C PRODUCED+VERIFIED (live activation not reachable — see Defect 1)**

## Deliverable A — fragment

`/root/AAA/instructions/care-governor.md` (2243 bytes). Status line `DRAFT_AWAITING_F13`.
Rule list, not an essay: rules 1–7 exactly as SPEC §G2, imperative, plus a Boundary block.
Composes with — never restates — `governed-uncertainty`, `loved-one-worry-support`, `relationship-kernel`
(the skills are named by name; their procedure text is not copied). Not registered in any index: the
fragments dir is auto-enumerated by `render-agents.sh` (`/root/AGENTS.md` carries an
`UNRENDERED_FRAGMENTS` list, rendered 2026-09-17T13:39Z). Re-rendering `/root/AGENTS.md` was **not**
done — it rewrites a constitutional surface and is outside this WP.

## Deliverable B — SOUL.md diff: PREPARED, NOT APPLIED

**HELD: constitutional file — requires F13 word.** Diff at `/root/AAA/state/care-build/G2-soul-diff.md`.

`/root/HERMES` is a **symlink → `/root/.hermes`** (`lrwxrwxrwx /root/HERMES -> /root/.hermes`).
`/root/HERMES/SOUL.md` and `/root/.hermes/SOUL.md` share inode `5335935` — one file, two names, not two files.
**Canonical: `/root/.hermes/SOUL.md`** (`HERMES_HOME=/root/.hermes` in the gateway unit).

`SOUL.md` untouched: sha256 `030181ab4999ec1a54150041bcb840d5b5eabf89ed23e990c46349d5ff52c43d`,
22070 bytes, mtime `2026-09-17 15:21:32 +0800` — unchanged before and after.
The diff adds a 13-line `## CARE GOVERNOR` block after `VOICE-GOVERNOR`, in the file's own BM-Penang
voice, referring to the fragment by path. Stamp warning recorded in the diff file: SOUL.md line 1 is a
`SOUL_STAMP v1.1` whose sha256 covers the body, so applying the body invalidates it — the executor must
recompute it.

## Deliverable C — lane-card wiring

`/root/.hermes/profiles/aaa-hermes/plugins/lane_switch/__init__.py` — **purely additive, 46 insertions, 0 deletions**:

| line | what |
|---|---|
| 36 | `CARE_GOVERNOR_FRAGMENT = Path("/root/AAA/instructions/care-governor.md")` |
| 226–247 | `_care_governor_block(lane_id, cfg)` — injects the fragment text under a header naming its path; degrades to a path-reference line if the fragment is missing, never to silence |
| 272–277 | call site in `_lane_card`, immediately after the `Authority:` line and before `CAPABILITY MAP` (conduct frames capability) |

Design: emission is **always-on for every non-guest lane** — so it cannot depend on someone remembering to
flag a lane, and it lands on SADO (`-1003815535761`), Arif's DM (`267378578`), and any future personal
lane. `guest` is excluded (F13 zero-data rule, card stays 358 bytes). Opt-out exists for the sovereign:
`doctrines.care_governor: false` on a lane. The plugin never hardcodes the rule text — single source of
truth stays the fragment file.

### Verification (real execution, not code reading)

Reproducible: **`/usr/local/lib/hermes-agent/venv/bin/python /root/AAA/state/care-build/G2-verify-lane-card.py`**
(same script G4's regression checklist can reuse; exit code is the verdict — last run `EXIT=0`, 19/19 PASS,
`RESULT: PASS — all assertions green`).

It exercises `_lane_card` against a probe registry built **from the real lane entries** in the canonical
heritage copy (`/root/.quarantine/zen-20260912/_CANONICAL/HERMES-heritage-5.3G-20260904/lanes/lanes.yaml`
— `arif`, `arif-sado`, `syed`, `guest`, verbatim; nothing invented), with `m.LANES_YAML` pointed at the
probe and the mtime cache reset.

```
trigger mapping: 267378578+SADO(-1003815535761) -> arif-sado
trigger mapping: 267378578+DM(267378578)         -> arif

### OUTPUT _lane_card('arif', include_memory=True)  [9373 chars]
[LANE:arif] Muhammad Arif bin Fazil

Authority: SOVEREIGN

CARE GOVERNOR (conduct — ALWAYS ON, every turn; source: /root/AAA/instructions/care-governor.md):
# CARE GOVERNOR — Conduct Toward Humans (Always On)
> **Status:** DRAFT_AWAITING_F13 (2026-09-17 · G2 care-build) — advisory only until F13 seals it.
...
1. **Never emit a directive about a third party's body** — sleep, food, training load, medication, weight — into a shared room.
--> contains 'CARE GOVERNOR': True

### OUTPUT _lane_card('arif-sado', ...) [9764 chars] --> contains 'CARE GOVERNOR': True
### OUTPUT _lane_card('syed', ...)      [3870 chars] --> contains 'CARE GOVERNOR': True
### OUTPUT _lane_card('guest', ...)      [358 chars] --> contains 'CARE GOVERNOR': False   (correct)
```

11/11 content assertions PASS on the `arif` card: rules 1–5 and 7 present verbatim, `DRAFT_AWAITING_F13`
present, all three skill names present, fragment path present. Ordering check PASS
(`Authority:` < `CARE GOVERNOR` < `CAPABILITY MAP`). Opt-out check PASS. `ast.parse` on the patched plugin PASS.

## Defect found (out of G2 scope — needs a coordinator's word)

**`/root/.hermes/lanes/lanes.yaml` does not exist.** The whole lane layer is dark right now:

```
LANES_YAML.exists(): False
detect_lane(267378578, 267378578) -> guest
detect_lane(267378578, -1003815535761) -> guest
len(_lane_card('arif', True)) = 0
len(_lane_card('arif-sado', True)) = 0
lane_switch: registry load failed: [Errno 2] No such file or directory: '/root/HERMES/lanes/lanes.yaml'
```

`/root/.hermes/lanes/` contains only `email_lane/` and `private/` — no `lanes.yaml`, no
`social-graph.yaml`, no `.runtime.json`. Every sender resolves to `guest` (zero personal data, zero tools)
and the lane card returns empty, so per-person memory, voice, social graph **and this care block** are all
unreachable in production. The only copy on the machine is the quarantine heritage file
(`…/HERMES-heritage-5.3G-20260904/lanes/lanes.yaml`, 22689 bytes, 839 lines, 2026-09-04).
**G2 did not restore it** — resurrecting a canonical registry that governs live multi-human context is a
mutation outside this WP's authority envelope. `next_owner: coordinator / F13`.

Consequence for C: the wiring is written and proven at function level, but **cannot fire in production
until that registry exists**. Reported as written-and-verified, not as live.

## Also not live: the running gateway

Plugin file mtime `2026-09-17 22:52:58 +0800`; gateway `ActiveEnterTimestamp = Thu 2026-09-17 13:03:42 +08`,
`ps lstart = Thu Sep 17 13:02:40 2026`. The plugin is imported at gateway boot, so the running process still
holds the old module. **Activation is HELD** — SPEC forbids restarting `hermes-asi-gateway.service`
(it would kill the live session). `next_owner: coordinator/F13`.

The plugin is git-tracked (`M profiles/aaa-hermes/plugins/lane_switch/__init__.py`); left **uncommitted**
for F11 review, as no commit was ordered.

## Hard-forbidden compliance

No scoring/ranking/metric of any person (H5) · no third-party interior modelled · no proactive message ·
**no write to SOUL.md** (hash re-verified) · no gateway restart · no secret printed · no human-facing send
issued (the designated target was not needed).

## What I could not do

1. Make the block reachable in production — blocked by the missing `lanes.yaml` (Defect 1).
2. Verify the block inside a live LLM turn — would require a gateway restart (forbidden).
3. Apply the SOUL.md diff — HELD for F13.
