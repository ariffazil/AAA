# AAA Terminal — one truth, one renderer, many viewers

```
commander files + live probes
            │
            ▼
     arifos-hero.sh          ← only process allowed to think
            │
            ▼
        state.json           ← only computed truth file
            │
   ┌────────┼────────┬─────────┬─────────┐
   ▼        ▼        ▼        ▼         ▼
 MOTD      PS1      now     boot      status
```

## Owners

| File | Responsibility | Who writes |
|---|---|---|
| `arifos-hero.sh` | Observe + render | this directory |
| `state.json` | Computed reality | hero only |
| `broadcast.txt` | Commander's intent | Arif / closer |
| `holds.txt` | Extra holds; delete line = resolved | Arif / closer |
| `todays-law.txt` | One law | Arif / closer |
| `mission.txt` | Current mission | Arif / closer |
| `orders.txt` | Role orders | rare |
| `handover.log` | **moved** → `/root/AAA/telemetry/handover.log` | clerks append via `/root/AAA/telemetry/handover-append.sh` |
| `atlas` in state.json | Absolute SOT paths | hero |

`/root/.local/share/arifos/state.json` is timezone SOT. It is not this file.

## Viewers (no logic)

| Surface | What it does |
|---|---|
| MOTD `05-arifos-board` | **one board** on KVM8/KVM4/KVM2 (`arifos-board` = `now`) |
| `/root/scripts/arifos-hero.sh` | pointer |
| `/root/scripts/arifos-board.sh` | pointer |
| `arifos-banner-cache.sh` | pointer |
| PS1 | reads `mode` from `state.json` once: `[\u@\h HOLD]\$ ` |
| `now` | deep probe; overlapping FQ/WELL/mode read `state.json` |
| `boot.sh` | agent clerk card — files only, no curl. Surfaces V/X/debt. |
| `/root/scripts/boot.sh` | pointer |
| `BOOT.md` | boot contract |
| `FLOW.md` | arifFLOW = metabolism, not agent |

## Drift test

Change `todays-law.txt`. Run `hero`. MOTD, `status`, `now` show the new law. No other file edits.

## Rule

If a new file starts computing FQ, WELL, or holds — delete that logic. Hero already did.
