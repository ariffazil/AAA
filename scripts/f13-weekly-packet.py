#!/usr/bin/env python3
"""F13 Weekly Packet — batched ratification digest (gotong-royong item #5).

F13 directive 2026-09-15/16 ("execute all") + Hermes item #5: "Layer 3/4
proposals kumpul untuk verdict kau — bukan satu-satu. Berkelompok, sekali
seminggu." Sovereign attention (W888) is the scarcest resource; this packet
compresses every F13-pending queue into ONE weekly decision document.

Sources (presence-optional, fail-soft, counts reported even when empty):
  1. reexamination_queue.jsonl — Arrow-1 corrections awaiting F13 (PROPOSED)
  2. vault999/scars/candidate-*.json — kernel scar candidates (F13 seal)
  3. /root/AAA/scars/candidates/*.md — AAA scar candidates
  4. rsi/state/proposals.jsonl — RSI Layer-3/4 proposals (propose-only lane)
  5. rsi/state/baselines.json — consequence verdicts due this week

Output: /root/AAA/governance/f13-packets/f13-packet-<ISOweek>-<N>.md
Decision protocol: satu verdict per item ID — APPROVE / DEFER / REJECT.

Constitutional: F2 TRUTH (method+timestamp on every count) · F11 AUDIT
(generated_at stamp, source paths printed) · F13 SOVEREIGN (packet proposes
nothing itself — it aggregates; verdicts stay sovereign).

DITEMPA BUKAN DIBERI — FI-003, musyawarah 2026-09-15-rsi-exhale.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

OUT_DIR = Path("/root/AAA/governance/f13-packets")
REEXAM = Path("/root/.local/share/arifos/reexamination_queue.jsonl")
V999_SCARS = Path("/root/.local/share/arifos/vault999/scars")
AAA_SCARS = Path("/root/AAA/scars/candidates")
RSI_PROPOSALS = Path("/root/AAA/rsi/state/proposals.jsonl")
RSI_BASELINES = Path("/root/AAA/rsi/state/baselines.json")


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_jsonl(path: Path, limit_note: str):
    rows, bad = [], 0
    if not path.is_file():
        return None, f"source missing: {path}"
    for line in path.open():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            bad += 1
    note = f"n={len(rows)}" + (f" (skipped {bad} malformed)" if bad else "")
    return rows, f"{limit_note}: {note} @ {path}"


def section_reexam(lines):
    rows, note = load_jsonl(REEXAM, "reexamination queue")
    lines.append(f"### 1. Arrow-1 Reexamination Corrections — {note}\n")
    if rows is None:
        lines.append(f"> {note}\n")
        return
    pending = [r for r in rows if str(r.get("status", "")).upper() in ("PROPOSED", "PENDING")]
    done = len(rows) - len(pending)
    lines.append(f"**Pending F13: {len(pending)}** (resolved: {done}). Item terlama dahulu:\n")
    pending.sort(key=lambda r: str(r.get("created_utc", "")))
    for r in pending[:12]:
        lines.append(f"- `{r.get('task_id','?')}` [{r.get('priority','?')}] {r.get('tool','?')} — "
                     f"{str(r.get('description',''))[:90]} ({r.get('created_utc','?')[:10]})")
    if len(pending) > 12:
        lines.append(f"- … dan {len(pending)-12} lagi (packet penuh di {REEXAM})")
    lines.append("")


def section_scars(lines):
    v999 = sorted(V999_SCARS.glob("candidate-*.json")) if V999_SCARS.is_dir() else []
    lines.append(f"### 2. Scar Candidates\n")
    lines.append(f"- vault999 kernel candidates: **{len(v999)}** @ {V999_SCARS} (semua menunggu F13 seal)")
    for p in v999:
        try:
            d = json.loads(p.read_text())
            lines.append(f"  - `{p.name}` status={d.get('status','?')} — {str(d.get('description', d.get('reason','')))[:80]}")
        except Exception:
            lines.append(f"  - `{p.name}` (unreadable)")
    aaa = sorted(AAA_SCARS.glob("*.md")) if AAA_SCARS.is_dir() else []
    lines.append(f"- AAA candidates: **{len(aaa)}** @ {AAA_SCARS}")
    for p in aaa:
        lines.append(f"  - `{p.name}`")
    lines.append("")


def section_rsi(lines):
    lines.append("### 3. RSI Layer-3/4 Proposals (propose-only lane)\n")
    rows, note = load_jsonl(RSI_PROPOSALS, "rsi proposals")
    lines.append(f"> {note}")
    if rows:
        for r in rows[:10]:
            lines.append(f"- `{r.get('id', r.get('atom_id','?'))}` [{r.get('layer','?')}] {str(r.get('proposal',''))[:90]}")
    lines.append("")


def section_consequence(lines):
    lines.append("### 4. Consequence Verdicts Due (RSI reality test)\n")
    if not RSI_BASELINES.is_file():
        lines.append(f"> source missing: {RSI_BASELINES}\n")
        return
    try:
        d = json.loads(RSI_BASELINES.read_text())
        caps = d.get("capabilities", d) if isinstance(d, dict) else d
        if isinstance(caps, dict):
            caps = list(caps.values())
        for c in caps if isinstance(caps, list) else []:
            if not isinstance(c, dict):
                continue
            lines.append(f"- `{c.get('capability','?')}` pattern={c.get('pattern_type','?')} "
                         f"promoted={str(c.get('promoted_at','?'))[:16]} verdict={c.get('verdict','PENDING')}")
    except Exception as exc:
        lines.append(f"> parse error: {exc}")
    lines.append("")


def main() -> None:
    now = datetime.now(timezone.utc)
    week = f"{now.isocalendar().year}-W{now.isocalendar().week:02d}"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    n = 1
    while (OUT_DIR / f"f13-packet-{week}-{n}.md").exists():
        n += 1
    out = OUT_DIR / f"f13-packet-{week}-{n}.md"

    lines = [
        f"# F13 Weekly Packet — {week} (#{n})",
        "",
        "Status: F13-instrument (weekly ratification packet — verdicts pending F13)",
        "",
        f"Generated: {stamp()} · Generator: /root/AAA/scripts/f13-weekly-packet.py · Method: live disk scan, fail-soft",
        "",
        "**Protokol:** satu verdict per item ID — `APPROVE` / `DEFER` / `REJECT`. Packet ini mengagregat sahaja; ia tidak mencadang apa-apa sendiri.",
        "",
    ]
    section_reexam(lines)
    section_scars(lines)
    section_rsi(lines)
    section_consequence(lines)
    lines.append("---")
    lines.append(f"\n*DITEMPA BUKAN DIBERI — f13-weekly-packet.py, {stamp()}*\n")
    out.write_text("\n".join(lines))
    print(f"F13 PACKET [OK]: {out}")
    print(f"F13 PACKET [OK]: generated {stamp()}")


if __name__ == "__main__":
    main()
