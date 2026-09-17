# G3 — REMEMBER SO IT IS NOT RE-TAUGHT · people register + lane-card injection

**State: VERIFIED** (injection + leak property exercised against the real `_lane_card`;
0 private-lane entries reachable through the injected block). One environment finding
below limits production effect today — see FINDING 1/2, which are *not* mine to fix.
trace_id `care-2026-09-17`. Registry path in the task (`/root/HERMES/lanes/lanes.yaml`)
is **absent** on this machine — see FINDING 1 for the evidence.

## Files touched

| Path | What |
|---|---|
| `/root/HERMES/lanes/people.yaml` (= `/root/.hermes/lanes/people.yaml`) | **NEW.** Facts-only per-person register, v1.0.0, schema `arifos.lanes.people.v1` |
| `/root/.hermes/profiles/aaa-hermes/plugins/lane_switch/__init__.py` | `PEOPLE_YAML` const + `_load_yaml` branch + `_is_shared_room()` + `_people_block()` + 5-line call inside `_lane_card()` |
| `/root/AAA/state/care-build/g3-verify.py` | Verifier (imports the live plugin by path, slices the heritage register mechanically) |
| `/root/AAA/state/care-build/g3-verify-output.txt` | Full verbatim run output |
| `/root/AAA/state/care-build/g3-cards.json` | The rendered cards (4 variants) |

Nothing else was mutated. No service restarted. No message sent to any human (the task's
designated test target was not needed — the proof is local). No secret printed.

## What is in the register

Admission requires all four: a human stated it · `record` names the file on this machine ·
`observed` ISO date · `scope` set (`dm` default). Machine inference, dossiers and shadow
maps are not sources. Content rules: no motive, no psychology, no typology, no label, no
score, no love telemetry; no body directive.

Seeded **5 people / 12 entries** — every value read back out of the record named beside it:

- `arif` — 4 private (occupation; BM Penang register + pronoun ban; father died 2024-03-04;
  PETRONAS service/OD1/MSS route) + 1 shared (timezone MYT)
- `syed` — 1 private self-statement (`Ni aku lah syed`, in-lane, **2026-09-12**, the only
  fact here sourced to the person about themselves) + 3 private (from `arif`)
- `paan` — 1 private (kelas sado / INBA Pro Elite Athlete 2024 / PT) + 1 shared (room fact)
- `lutfi` — 1 private, with `link_basis` stating that the name↔id link is a **string match
  only**, not something any human said
- `faqwan` — **facts: []** — onboarded 2026-08-28, zero person facts recorded anywhere.
  Left empty on purpose: an empty entry is honest, an invented one is evidence later.

`held_out:` declares three bodies of material that exist on this machine and were **not**
admitted (family/legal lines in `MEMORY.md.bak-20260914`; persona/psychology lines in
`USER.md.bak-20260914`; `/root/HERMES/lanes/private/shadow/*`). `unresolved:` records the two
name↔person links that no human stated (PAAN↔"Farhan Fudzil"; which "Syed" the ledger's
security report belongs to) and were therefore **not merged**.

## Injection rule (mechanical, in the plugin)

`_lane_card()` calls `_people_block(lane_id, cfg)` after the care-governor block. The rule:

- a person's entry is included only if an **identity value published in the register**
  intersects the lane's own `telegram_user_ids` / `telegram_chat_ids`. Nobody is guessed in
  from the conversation.
- `scope: shared` → injected wherever that person is present.
- `scope: dm` → injected **only** when the lane is that person's own lane **and** the lane is
  not a shared room. Otherwise it is counted into a `SHARED-ROOM RULE: N … WITHHELD` line —
  the absence is visible, the content is never quoted.
- shared-room detection reads the lane's own config (`group_capability_scoped`, or a negative
  `telegram_chat_id`) and **fails closed**: unprovable room shape = treated as shared.
- `guest` lane → no block at all.

## Evidence (verbatim, `command_run` in the receipt)

**SADO lane (-1003815535761), lane id `arif-sado`, card chars=7445** — injected block:

```
PEOPLE IN THIS LANE (facts only — everything below was stated by a human and is sourced; nothing here is inferred, scored or ranked):
· Muhammad Arif bin Fazil (sovereign) [id: arif]
  - telegram_user_id=267378578 [src: channel_directory.json (Telegram-provided; dm named "ARIF") · 2026-09-17]
  - Timezone harian: Asia/Kuala_Lumpur (MYT, UTC+8). [src: arif · 2026-09-17 · /root/.hermes/config.yaml (timezone); lanes.yaml heritage register records federation_tz.set_by = "arif (F13)", set 2026-08-11]
· Syed (Abang Sado) [id: syed]
  - telegram_user_id=1042200555 [src: channel_directory.json (dm recorded as "No name", 2026-09-17); lanes.yaml heritage register 2026-08-30 · 2026-09-17]
  - room=-1003815535761 [src: channel_directory.json (group named "SADO"); lanes.yaml heritage register · 2026-09-17]
PEOPLE RULE: never state a fact about these people that is not in this block (or in this lane's own memory above). "Aku tak tahu" is the correct answer otherwise. Do not ask them to re-explain what is already recorded here.
SHARED-ROOM RULE: 8 private-lane entries for these people exist and are WITHHELD from this room. Do not ask for them, guess them, or reconstruct them here.
```

**Arif's DM (267378578), lane id `arif`, card chars=7144** — same person, private facts present:

```
· Muhammad Arif bin Fazil (sovereign) [id: arif]
  - telegram_user_id=267378578 [...]
  - Kerja: exec geoscience PETRONAS Carigali (upstream). [src: arif · 2026-09-17 · /root/.hermes/memories/USER.md]
  - Bahasa harian: BM Penang kampung, pendek dan laju; guna 'aku'/'hang', pronomina 'saya' ditolak. [...]
  - Bapak meninggal 4 Mac 2024 (Penang). [...]
  - PETRONAS: 12 tahun service (mula Nov 2013); OD1 Mac 2027; form 30 Sep = niat sahaja, MSS rasmi melalui myCareerX. [...]
  - Timezone harian: Asia/Kuala_Lumpur (MYT, UTC+8). [...]
```

`syed-dm` likewise carries Syed's 4 private entries (`card chars=5091`). Full cards: `g3-cards.json`.

**Lane resolution exercised through the real `detect_lane`** (fixture registry):

```
[detect] Arif in SADO group   user=267378578   chat=-1003815535761   -> lane=arif-sado
[detect] Syed in SADO group   user=1042200555  chat=-1003815535761   -> lane=syed
[detect] Arif DM              user=267378578   chat=267378578        -> lane=arif
[detect] Syed DM              user=1042200555  chat=1042200555       -> lane=syed-dm
[detect] stranger in SADO     user=999999999   chat=-1003815535761   -> lane=guest
```

**Leak scan — 10 private(dm) facts × 4 hard-locked group cards:**

```
RESULT people_block_leaks_into_group_card = 0
-- every row: people_block=False (four variants: memory on/off × lane memory present/empty)
```

**Shared-scope entries land where they belong:** the timezone entry is `present=True` in the
SADO card; the PAAN room entry is `present=False` there because PAAN is not a speaker in that
lane. Neither PAAN's nor Lutfi's private facts appear in any lane that does not carry them.

## FINDINGS (open paths — reported, not silently fixed)

**F1 — the lane registry the task points at does not exist.** `/root/HERMES/lanes/lanes.yaml`
(= `/root/.hermes/lanes/lanes.yaml`) is absent; `/root/HERMES/lanes/` holds only `email_lane/`
and `private/`. It is not in git (`git ls-files lanes` → empty) and no non-quarantine copy
exists on the box. Only survivor: `/root/.quarantine/zen-20260912/_CANONICAL/HERMES-heritage-5.3G-20260904/lanes/lanes.yaml`
(838 lines, `updated: 2026-08-30`, 18 lanes). Direct consequence, printed by the verifier:

```
[live] _lane_card('arif-sado') with the real LANES_YAML -> '' (LANES_YAML.exists()=False)
```

`_lane_card` returns `""` for every lane today, so **the G3 block is inert in production until
a registry returns** — the injection itself is proven with a fixture sliced mechanically from
the heritage register. I did not restore `lanes.yaml`: that is a routing/canonical config
change outside this work package (G2 Deliverable C is the WP that touches lanes.yaml), and a
stale 18-lane registry with KVM8-only memory paths would activate dead lanes.

**F2 — `lane_switch` is not in the plugin set the running gateway scans.** The unit runs with
`HERMES_HOME=/root/.hermes` and no `HERMES_PROFILE`; `user_plugins_dir()` is
`$HERMES_HOME/plugins` (`/usr/local/lib/hermes-agent/plugins/plugin_loader.py:28-35`) and
`plugins.enabled` in `/root/.hermes/config.yaml` lists `hermes-snapcompact`, `web-aaa-state`:

```
user_plugins_dir() = /root/.hermes/plugins
plugins the default-profile gateway scans = ['hermes-snapcompact']
lane_switch present there = False
```

So even a restored registry would not reach a card until the profile plugin is loaded. I could
not confirm from outside the process whether the gateway scans `profiles/aaa-hermes/plugins`
without an explicit profile — stated as unknown, not as a verdict.

**F3 — a pre-existing path already puts private-lane person data into the SADO group card
(NOT introduced by G3).** `_recent_lane_history()` reads the lane's `*MEMORY*` file on **every**
turn; the `arif-sado` lane config points `memory_files` at the sovereign's operator memory, and
its block-splitter expects `### ` interaction headers, so a hand-written `MEMORY.md` (no headers)
becomes one block = the whole file. Measured:

```
[pre-existing path] /root/.hermes/memories/MEMORY.md content lines=10
   reachable in SADO group card A (lane memory_files as configured): verbatim=7 truncated-to-240-chars=3 total=10
   reachable in SADO group card B (memory_files=[])              : 0
   LEAKED> SYED (DM user): biohacking peptides, IFBB coaching, Dr. Trevor Bachmeyer ...
   LEAKED> ARIF@PETRONAS: 12thn service (Nov 2013), RM19k/bln. MSS = thn×1.5+4bln (~RM418k) ...
   (+8 more lines, incl. PAAN/LUTFI and the PETRONAS insider line)
```

10/10 of `MEMORY.md` (and 9 `USER.md` lines on first turn) reach that shared room through the
lane memory tail. The card does end with an `OPERATOR BOUNDARY (F13)` paragraph — a prompt-level
mitigation, not a mechanical one. This is the G4 red-team item "leak private-lane person data
into a group lane card"; G3's own block is clean, the room is not.

## What I did not do

- Did not restore or edit `lanes.yaml` (F1), enable the plugin (F2), or change lane
  `memory_files` (F3) — all three are other work packages / F13-owned config.
- Did not patch the other three `lane_switch` copies on the box
  (`/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/lane_switch/__init__.py`,
  `/root/hermes_work/pristine-full/...`, `/root/hermes_work/hermes-agent-copy/...`; md5 differ
  from the live profile copy). Drift is now a live risk for this fix.

## Reproduce

```
cd /root/AAA/state/care-build && /usr/local/lib/hermes-agent/venv/bin/python g3-verify.py; echo EXIT=$?
# exit 0 => 0 private-lane entries reachable through the people block in a shared-room card
# reads: /root/HERMES/lanes/people.yaml · plugin at profiles/aaa-hermes/plugins/lane_switch/__init__.py
#        fixture sliced from the quarantine heritage register (writes only /tmp/g3-lanes*.yaml)
```
