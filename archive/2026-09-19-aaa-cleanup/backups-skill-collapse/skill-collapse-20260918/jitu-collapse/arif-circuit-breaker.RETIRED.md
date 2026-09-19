# RETIRED — superseded by JITU

**Superseded:** 2026-09-18 by F13 directive: *"Kolaps 3 implementasi jadi SATU butang kuasa mutlak."*

**Reason for retirement:** this was a second, independent circuit-breaker implementation with
**zero live callers** (measured: no cron entry, no systemd unit, no import from live code). Two
brakes that do not know about each other are not redundancy — they are a shared blind spot: either
one can be "the" brake in a reader's mind while neither is actually wired.

**The single authority now lives at:** `/root/AAA/federation/kernel/jitu.py`
  trip    `python3 /root/AAA/federation/kernel/jitu.py trip --by F13 --reason "..." [--scope lanes]`
  release `python3 /root/AAA/federation/kernel/jitu.py release --by F13`
  status  `python3 /root/AAA/federation/kernel/jitu.py status`
  shell   `jitu-guard <lane> && <lane command>`   (wired into all automated cron lanes)

**Kept, not deleted** (F1, reversible-first). Restoring this file does NOT restore the brake —
the wiring is what made it live, and that wiring was never there.
