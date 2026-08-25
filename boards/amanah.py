#!/usr/bin/env python3
"""AMANAH — federation work-order board (AAA control plane).

Truth: amanah.jsonl beside this file. Git history = audit trail.
Single source of truth for open/gated/done work orders across the federation.

Usage:
  amanah add "title" [-p P1] [-g GATE] [-o OWNER] [-s SOURCE]
  amanah list [-s STATUS]          # open|doing|blocked|done|all
  amanah show AMH-001
  amanah done AMH-001 [-e EVIDENCE]
  amanah block AMH-001 -r "reason"
  amanah reopen AMH-001
  amanah note AMH-001 "text"
  amanah gate AMH-001 GATE         # set/clear gate ("" to clear)
"""
import argparse
import datetime
import json
import os
import sys
import tempfile

BOARD = os.path.join(os.path.dirname(os.path.realpath(__file__)), "amanah.jsonl")
STATUSES = ("open", "doing", "blocked", "done")


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load():
    items = []
    if os.path.exists(BOARD):
        with open(BOARD) as f:
            for ln in f:
                ln = ln.strip()
                if ln:
                    items.append(json.loads(ln))
    return items


def save(items):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(BOARD), prefix=".amanah-")
    with os.fdopen(fd, "w") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    os.replace(tmp, BOARD)


def next_id(items):
    mx = 0
    for it in items:
        try:
            mx = max(mx, int(it["id"].split("-")[1]))
        except (KeyError, IndexError, ValueError):
            pass
    return "AMH-%03d" % (mx + 1)


def find(items, iid):
    for it in items:
        if it["id"].lower() == iid.lower():
            return it
    sys.exit(f"error: {iid} not found")


def cmd_add(a):
    items = load()
    it = {
        "id": next_id(items), "title": a.title, "status": "open",
        "priority": a.priority, "gate": a.gate or "", "owner": a.owner or "",
        "source": a.source or "", "created": utcnow(), "updated": utcnow(),
        "notes": [],
    }
    items.append(it)
    save(items)
    print(f"{it['id']} added (open, {it['priority']})")


def cmd_list(a):
    items = load()
    rows = [it for it in items if not a.status or it["status"] == a.status]
    for it in sorted(rows, key=lambda x: (x["priority"], x["id"])):
        gate = f" [gate:{it['gate']}]" if it.get("gate") else ""
        own = f" @{it['owner']}" if it.get("owner") else ""
        print(f"{it['id']}  {it['priority']:<2} {it['status']:<7}{gate}{own}  {it['title']}")


def cmd_show(a):
    it = find(load(), a.id)
    print(json.dumps(it, indent=2, ensure_ascii=False))


def cmd_done(a):
    items = load()
    it = find(items, a.id)
    if a.evidence:
        it["notes"].append(f"{utcnow()} DONE evidence: {a.evidence}")
    it["status"] = "done"
    it["gate"] = ""
    it["updated"] = utcnow()
    save(items)
    print(f"{it['id']} done")


def cmd_block(a):
    items = load()
    it = find(items, a.id)
    it["status"] = "blocked"
    it["notes"].append(f"{utcnow()} BLOCKED: {a.reason}")
    it["updated"] = utcnow()
    save(items)
    print(f"{it['id']} blocked")


def cmd_reopen(a):
    items = load()
    it = find(items, a.id)
    it["status"] = "open"
    it["updated"] = utcnow()
    save(items)
    print(f"{it['id']} reopened")


def cmd_status(a):
    items = load()
    it = find(items, a.id)
    if a.status not in STATUSES:
        sys.exit(f"error: status must be one of {STATUSES}")
    it["status"] = a.status
    it["updated"] = utcnow()
    save(items)
    print(f"{it['id']} -> {a.status}")


def cmd_note(a):
    items = load()
    it = find(items, a.id)
    it["notes"].append(f"{utcnow()} {a.text}")
    it["updated"] = utcnow()
    save(items)
    print(f"{it['id']} noted")


def cmd_gate(a):
    items = load()
    it = find(items, a.id)
    it["gate"] = a.gate
    it["notes"].append(f"{utcnow()} gate -> '{a.gate or 'cleared'}'")
    it["updated"] = utcnow()
    save(items)
    print(f"{it['id']} gate={a.gate or '(cleared)'}")


def main():
    p = argparse.ArgumentParser(prog="amanah", description="AMANAH federation work-order board")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("add")
    s.add_argument("title")
    s.add_argument("-p", "--priority", default="P2", choices=["P0", "P1", "P2", "P3"])
    s.add_argument("-g", "--gate", default="")
    s.add_argument("-o", "--owner", default="")
    s.add_argument("-s", "--source", default="")
    s.set_defaults(fn=cmd_add)

    s = sub.add_parser("list")
    s.add_argument("-s", "--status", default="")
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("show")
    s.add_argument("id")
    s.set_defaults(fn=cmd_show)

    s = sub.add_parser("done")
    s.add_argument("id")
    s.add_argument("-e", "--evidence", default="")
    s.set_defaults(fn=cmd_done)

    s = sub.add_parser("block")
    s.add_argument("id")
    s.add_argument("-r", "--reason", required=True)
    s.set_defaults(fn=cmd_block)

    s = sub.add_parser("reopen")
    s.add_argument("id")
    s.set_defaults(fn=cmd_reopen)

    s = sub.add_parser("note")
    s.add_argument("id")
    s.add_argument("text")
    s.set_defaults(fn=cmd_note)

    s = sub.add_parser("gate")
    s.add_argument("id")
    s.add_argument("gate", nargs="?", default="")
    s.set_defaults(fn=cmd_gate)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
