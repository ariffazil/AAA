#!/usr/bin/env python3
"""Scheduler Registry sweep — ONE accounting unit across all surfaces.

Unit of account = a distinct execution obligation (not a file, line, or timer).

Surfaces swept (read-only, OBSERVE):
  1. root crontab
  2. /etc/cron.d/*
  3. systemd timers
  4. Hermes jobs.json

Output: /root/AAA/registries/scheduler/scheduled_units.yaml
Drift discipline: registry is the declared desired-state; weekly federation
housekeeping re-sweeps and diffs — any unit in live-but-not-registry (ghost)
or registry-but-not-live (phantom) raises a named alarm with owner.

333-AGI 2026-09-17 · T1 read-only · DITEMPA BUKAN DIBERI
"""

import json
import re
import subprocess
import yaml
from datetime import datetime, timezone
from pathlib import Path

REGISTRY = Path("/root/AAA/registries/scheduler/scheduled_units.yaml")

AGENT_FAMILIES = re.compile(
    r"rsi|skill[-_]?(learn|audit|matrix|census|entropy)|dream|memory[-_]helix|"
    r"musyawarah|apex[-_]zen|selfimprove|attention[-_]closure|agent[-_]card|"
    r"p0_metabolize|reexamine|metabolize|trajectory|attestation|chaos",
    re.I,
)
HUMAN_FAMILIES = re.compile(
    r"arif|syed|brief|reckoning|intel|iron[-_]radar|geo[-_]econ|digest|"
    r"triage|pulse[-_]event|vitality|flow[-_]event|scanner[-_]event|weekly[-_]digest|"
    r"wealth|trading|fomc|well[-_]ingest|google[-_]fit|3baik|attention|f13",
    re.I,
)
MACHINE_OVERRIDE = re.compile(
    r"cockpit|zombie|backup|vault|replica|certbot|clamav|"
    r"sysstat|e2scrub|docker.*prune|logrotate|apt|man-db|dpkg|tmpfiles|phoenix|gc\b|"
    r"prune|rotation|supply[-_]chain|sovereignty",
    re.I,
)


def classify(cmd: str, name: str = "") -> tuple[str, str]:
    """Return (plane, s_class) — PROVISIONAL heuristic, human-confirmable."""
    text = f"{cmd} {name}"
    delivery = "telegram" if re.search(r"telegram|267378578|1042200555|cron-deliver|deliver", text, re.I) else ""
    if HUMAN_FAMILIES.search(text) and not MACHINE_OVERRIDE.search(text):
        plane = "human"
    elif AGENT_FAMILIES.search(text) and not MACHINE_OVERRIDE.search(text):
        plane = "agent"
    else:
        plane = "machine"
    if re.search(r"deliver|cron-deliver|267378578|1042200555|sendMessage", text, re.I):
        s = "S2"  # delivers to a recipient
    elif plane == "human":
        s = "S1"
    elif re.search(r"autopause|heal|reaper|reconcil|watchdog|sentinel|probe|flip|doctor|sweep", text, re.I):
        s = "S0"
    else:
        s = "S0"
    return plane, s


def sweep_root_crontab(units):
    out = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
    for line in out.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"((?:[\d*/,-]+\s+){5})(.*)", line)
        if not m:
            continue
        sched, cmd = m.group(1).strip(), m.group(2).strip()
        plane, s = classify(cmd)
        units.append(
            {
                "id": f"root-cron::{cmd.split()[0].split('/')[-1]}::{sched.replace(' ', '_')}",
                "surface": "root-crontab",
                "schedule": sched,
                "plane": plane,
                "class": s,
                "command_head": cmd[:140],
                "delivery": "telegram" if "cron-deliver" in cmd or "digest_inbox" in cmd else "log/state",
            }
        )


def sweep_cron_d(units):
    for f in sorted(Path("/etc/cron.d").glob("*")):
        if not f.is_file():
            continue
        for line in f.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or re.match(r"^[A-Z_]+=", line):
                continue
            m = re.match(r"((?:[\d*/,-]+\s+){5})(?:root\s+|arifos\s+)?(.*)", line)
            if not m:
                continue
            sched, cmd = m.group(1).strip(), m.group(2).strip()
            plane, s = classify(cmd)
            units.append(
                {
                    "id": f"cron.d::{f.name}::{line.split()[5] if len(line.split()) > 5 else ''}::{sched.replace(' ', '_')}",
                    "surface": "cron.d",
                    "file": f.name,
                    "schedule": sched,
                    "plane": plane,
                    "class": s,
                    "command_head": cmd[:140],
                    "delivery": "telegram" if "cron-deliver" in cmd else "log/state",
                }
            )


def sweep_systemd(units):
    out = subprocess.run(
        ["systemctl", "list-timers", "--all", "--no-legend", "--no-pager"], capture_output=True, text=True
    ).stdout
    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 5 or not line.strip():
            continue
        # LAST column before UNIT; find unit ending in .timer
        m = re.search(r"(\S+\.timer)\s+(\S+\.service)", line)
        if not m:
            continue
        timer = m.group(1)
        plane, s = classify(timer)
        units.append(
            {
                "id": f"systemd::{timer}",
                "surface": "systemd",
                "schedule": "OnCalendar/OnUnitActiveSec (unit file)",
                "plane": plane,
                "class": s,
                "command_head": m.group(2),
                "delivery": "internal",
            }
        )


def sweep_hermes(units):
    p = Path("/root/.hermes/cron/jobs.json")
    if not p.exists():
        return
    jobs = json.loads(p.read_text())
    if isinstance(jobs, dict):
        jobs = jobs.get("jobs", [])
    for j in jobs:
        name = j.get("name") or j.get("id")
        deliver = j.get("deliver") or "none"
        plane, s = classify(f"{name} {deliver}", name)
        if j.get("enabled"):
            s = "S2" if deliver.startswith("telegram") else s
        units.append(
            {
                "id": f"hermes::{j.get('id')}",
                "surface": "hermes",
                "name": name,
                "schedule": (j.get("schedule") or {}).get("display", "?"),
                "enabled": bool(j.get("enabled")),
                "plane": plane,
                "class": s,
                "delivery": deliver,
                "last_status": j.get("last_status"),
            }
        )


def main():
    units = []
    sweep_root_crontab(units)
    sweep_cron_d(units)
    sweep_systemd(units)
    sweep_hermes(units)
    counts = {}
    for u in units:
        counts[u["plane"]] = counts.get(u["plane"], 0) + 1
    doc = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generator": "sweep_scheduled_units.py v1",
            "unit_of_account": "distinct execution obligation (not file/line/timer)",
            "classification": "PROVISIONAL heuristic — F13-confirmable per unit",
            "surfaces": ["root-crontab", "cron.d", "systemd", "hermes"],
            "counts": {"total": len(units), **counts},
            "law": "registry=declared desired-state; live-vs-registry diff = named alarm with owner; retirement requires tombstone",
        },
        "units": units,
    }
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=200))
    print(json.dumps(doc["meta"]["counts"], indent=1))


if __name__ == "__main__":
    main()
