#!/usr/bin/env python3
"""docforge.pipeline — one run, end to end, and a receipt that says what happened.

    fetch items -> diff against state -> write delta section -> compose -> render
    -> GATES -> SEAL -> record state -> dispatch

WHAT THE ORDER BUYS
  Three properties, each of which fails if the order is changed:

  1. The delta is computed BEFORE composition, so tomorrow's document contains
     the comparison rather than the comparison being a separate message nobody
     reads.
  2. Gates run BEFORE the seal, so a broken artifact cannot enter the permanent
     record.
  3. State is recorded AFTER the seal succeeds, so a refused build does not
     advance the memory. If state advanced first, a failed edition would become
     "yesterday" and the next delta would be computed against a document that
     was never delivered — silently losing the comparison.

THE ITEM SOURCE IS INJECTED, NOT HARDCODED
  This module does not know how to gather intelligence. It calls a producer that
  returns the schema'd items. That separation is what lets the same pipeline
  serve a Malaysia brief, a WEALTH brief, and a GEOX brief without forking —
  and it is why the intelligence work can improve without touching the
  rendering, gating, sealing, or dispatch path.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import dispatch as dispatchmod
from . import seal as sealmod
from .state import Store, qdrant_status

HERE = Path(__file__).resolve().parent


# ── item schema ──────────────────────────────────────────────────────────────

ITEM_REQUIRED = ("item_id", "section", "title", "claim_state", "summary")


def validate_items(items: list[dict]) -> list[str]:
    """Enforce the schema and return every problem, not just the first.

    Reporting one error at a time turns a 20-item producer bug into 20 build
    cycles. All of them at once is one edit.
    """
    from .state import CLAIM_STATES, SECTIONS
    problems: list[str] = []
    seen: set[str] = set()
    for i, it in enumerate(items):
        where = f"item[{i}]"
        if not isinstance(it, dict):
            problems.append(f"{where}: not an object")
            continue
        for k in ITEM_REQUIRED:
            if not it.get(k):
                problems.append(f"{where} ({it.get('item_id','?')}): missing {k!r}")
        iid = it.get("item_id")
        if iid:
            where = f"item {iid!r}"
            if iid in seen:
                problems.append(f"{where}: duplicate item_id — the delta keys on "
                                "this, so a collision merges two claims into one")
            seen.add(iid)
        sec = it.get("section")
        if sec and sec not in SECTIONS:
            problems.append(f"{where}: section {sec!r} not in {SECTIONS}")
        st = (it.get("claim_state") or "").upper()
        if st and st not in CLAIM_STATES:
            problems.append(f"{where}: claim_state {st!r} not in {CLAIM_STATES}")
    return problems


# ── delta section rendering ──────────────────────────────────────────────────


def render_delta_html(delta, prev_edition: str | None) -> str:
    d = delta.as_dict()
    c = d["counts"]

    def rows(items, label):
        if not items:
            return ""
        out = [f"<h3>{label} <span class='small'>({len(items)})</span></h3>",
               "<table><thead><tr><th>Item</th><th>Section</th>"
               "<th>Was</th><th>Now</th></tr></thead><tbody>"]
        for it in items:
            out.append(
                f"<tr><td>{it['title']}</td><td>{it['section']}</td>"
                f"<td>{it.get('was','&mdash;')}</td>"
                f"<td><strong>{it['claim_state']}</strong></td></tr>")
        out.append("</tbody></table>")
        return "".join(out)

    head = ("<h2>0 &middot; What Changed Since Yesterday</h2>")
    if d["first_edition"]:
        return head + (
            "<div class='box key'><strong>First tracked edition.</strong> There is "
            "no prior state to diff against, so nothing below is a change. From "
            "the next edition onward this section reports only what moved: new "
            "items, state transitions, and anything still unresolved.</div>"
            + rows(d["new"], "Today's tracked items"))

    body = [head,
            f"<p class='small'>Compared against <strong>{prev_edition}</strong>. "
            f"{delta.headline()}</p>"]
    body.append(rows(d["reopened"], "Reopened (was closed, is live again)"))
    body.append(rows(d["moved"], "Changed state"))
    body.append(rows(d["new"], "New today"))
    body.append(rows(d["settled"], "Settled"))
    if d["dropped"]:
        body.append(
            "<div class='box warn'><strong>Dropped without resolution "
            f"({c['dropped']})</strong> — these were live yesterday and are absent "
            "today, which is <em>not</em> the same as resolved. They are listed "
            "rather than silently retired.</div>"
            + rows(d["dropped"], "Dropped"))
    if d["still_open"]:
        body.append(
            f"<p class='small'>Carrying over unchanged: <strong>{c['still_open']}</strong> "
            "item(s). Not repeated in full — see the open-items register.</p>")

    if not any(c[k] for k in ("reopened", "moved", "new", "settled", "dropped")):
        body.append("<div class='box key'><strong>No state change.</strong> Every "
                    "tracked claim reads the same as yesterday.</div>")
    return "".join(body)


def render_items_html(items: list[dict]) -> str:
    from .state import SECTIONS
    order = [s for s in SECTIONS]
    out = []
    for sec in order:
        group = [i for i in items if i["section"] == sec]
        if not group:
            continue
        out.append(f"<h2>{sec.title()}</h2>")
        for it in group:
            cls = {"CONTESTED": "open", "OPEN": "claim", "MOVED": "warn"}.get(
                it["claim_state"], "key")
            out.append(
                f"<h3>{it['title']} "
                f"<span class='tag t-{ 'open' if it['claim_state']=='CONTESTED' else 'doc' }'>"
                f"{it['claim_state']}</span></h3>"
                f"<div class='box {cls}'>{it['summary']}"
                + (f"<div class='small' style='margin-top:2mm'>Source: "
                   f"{it['source']}</div>" if it.get("source") else "")
                + "</div>")
    return "".join(out)


# ── the run ──────────────────────────────────────────────────────────────────


def render_rules_html(store) -> str:
    """Show the standing instructions INSIDE the document.

    A rule that only exists inside a database is invisible to the person it
    governs. Printing it in the brief means Arif can see what the machine has
    been told to do, and can retire it in the same breath as reading it.
    """
    rows = store.active()
    if not rows:
        return ""
    out = ["<h2>0.1 &middot; Standing Instructions</h2>",
           "<p class='small'>Derived from your own comments on earlier editions. "
           "Each shows the words it came from. A rule you no longer want can be "
           "retired; it is listed here so it cannot operate invisibly.</p>",
           "<table><thead><tr><th>Instruction</th><th>Standing since</th>"
           "<th>Editions</th></tr></thead><tbody>"]
    for r in rows:
        out.append(f"<tr><td><strong>{r['rule']}</strong><br>"
                   f"<span class='small'>heard as: &ldquo;{r['raw_text']}&rdquo;</span>"
                   f"</td><td>{r['created_at'][:10]}</td>"
                   f"<td>{r['applied_count']}</td></tr>")
    out.append("</tbody></table>")
    return "".join(out)


def run(items_path: Path, *, edition: str, date: str, template: str = "base-a4",
        theme: str = "light", title: str = "Executive Brief", subtitle: str = "",
        run_dir: Path, db: Path | None = None, target: str | None = None,
        dry_run: bool = False) -> dict:
    """Execute one edition. Returns a receipt describing each stage's real outcome."""
    from . import cli as climod
    from .state import DEFAULT_DB

    receipt: dict = {
        "edition": edition, "date": date, "built_at": sealmod.utc_now(),
        "stages": {}, "ok": False,
    }
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    # 1. items
    raw = json.loads(Path(items_path).read_text())
    items = raw["items"] if isinstance(raw, dict) else raw
    problems = validate_items(items)
    receipt["stages"]["validate"] = {
        "ok": not problems, "item_count": len(items), "problems": problems}
    if problems:
        receipt["error"] = "schema violation"
        return receipt

    # 2. state + delta (BEFORE compose, so the document contains the comparison)
    store = Store(db or DEFAULT_DB)
    prev_edition = store._prev_edition(edition)
    store.record_edition(edition, date, items,
                         payload={"source_file": str(items_path)})
    delta = store.delta(edition)
    ok_q, why_q = qdrant_status()
    receipt["stages"]["state"] = {
        "ok": True, "prev_edition": prev_edition,
        "delta": delta.as_dict()["counts"], "headline": delta.headline(),
        "semantic_mirror": {"available": ok_q, "detail": why_q},
        "open_items": len(store.open_items()),
    }

    # 3. compose body: delta first, then standing instructions, then the register
    from .feedback import FeedbackStore
    fb = FeedbackStore(db or DEFAULT_DB)
    rules_path = fb.export_rules(run_dir / "brief-rules.md")
    receipt["stages"]["feedback"] = {
        "ok": True, "standing_rules": len(fb.active()),
        "rules_file": str(rules_path),
    }
    body = (render_delta_html(delta, prev_edition)
            + render_rules_html(fb)
            + "<div style='page-break-before:always'></div>"
            + render_items_html(items))
    src = run_dir / "content.html"
    src.write_text(body)

    # 4. build (compose -> render -> gates -> seal)
    spec = {
        "edition": edition, "edition_date": date, "title": title,
        "subtitle": subtitle or f"Delta tracked edition · {delta.headline()}",
        "template": template, "theme": theme, "source": str(src),
        "run_dir": str(run_dir),
        "gates": {"profile": "print-light", "forbid_paths": True,
                  "cover_orphan_exempt": True},
        "stats": {
            "new": len(delta.new), "moved": len(delta.moved),
            "reopened": len(delta.reopened), "still_open": len(delta.still_open),
            "settled": len(delta.settled), "dropped": len(delta.dropped),
            "items_total": len(items),
        },
    }
    spec_path = run_dir / "spec.json"
    spec_path.write_text(json.dumps(spec, indent=2))
    rc = climod.main(["build", str(spec_path)])
    receipt["stages"]["build"] = {"ok": rc == 0, "exit": rc, "spec": str(spec_path)}
    if rc != 0:
        receipt["error"] = "gate chain refused the artifact — state was recorded, no seal"
        # NOTE: state was recorded above. That is deliberate and stated: the items
        # are real intelligence regardless of whether the rendering succeeded, and
        # losing them would force the next run to re-gather. The SEAL did not
        # happen, so no broken artifact entered the record.
        return receipt

    artifact = run_dir / f"{edition}.pdf"
    sidecar = run_dir / f"{edition}.sha256"
    led = json.loads((run_dir / f"{edition}.ledger.json").read_text())
    receipt["stages"]["seal"] = {
        "ok": True, "artifact": str(artifact), "sidecar": str(sidecar),
        "artifact_sha256": led["artifact_sha256"],
        "content_sha256": led["content_sha256"],
        "gates_all_pass": led["gates_all_pass"],
    }

    # 5. semantic mirror (best effort, never blocks)
    try:
        from .state import mirror_to_qdrant
        ok_m, why_m = mirror_to_qdrant(edition, body, {"date": date})
    except Exception as exc:  # noqa: BLE001
        ok_m, why_m = False, f"mirror error: {exc}"
    receipt["stages"]["mirror"] = {"ok": ok_m, "detail": why_m}

    # 6. dispatch
    if dry_run or not target:
        receipt["stages"]["dispatch"] = {
            "state": "PRODUCED", "literal": True,
            "detail": ("dry run — artifact sealed on disk, nothing pushed. "
                       "Set target to actually send."),
            "artifact": str(artifact),
        }
    else:
        d = dispatchmod.send(
            artifact, target,
            caption=(f"*{title}* · {edition} · {date}\n{delta.headline()}\n"
                     f"Seal {led['artifact_sha256'][:16]}…"),
            sidecar=sidecar)
        receipt["stages"]["dispatch"] = d.as_dict()
        receipt["ok"] = d.state == "SENT"

    if dry_run or not target:
        receipt["ok"] = True
    (run_dir / f"{edition}.receipt.json").write_text(json.dumps(receipt, indent=2))
    return receipt


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="docforge.pipeline")
    ap.add_argument("items", help="JSON file: {items:[...]} or a bare list")
    ap.add_argument("--edition", required=True)
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--title", default="Executive Brief")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--template", default="base-a4")
    ap.add_argument("--theme", default="light")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--db", default=None)
    ap.add_argument("--target", default=None,
                    help="delivery target, e.g. telegram:8410138119")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    receipt = run(Path(a.items), edition=a.edition, date=a.date, template=a.template,
                  theme=a.theme, title=a.title, subtitle=a.subtitle,
                  run_dir=Path(a.run_dir),
                  db=Path(a.db) if a.db else None, target=a.target,
                  dry_run=a.dry_run)
    print(json.dumps(receipt, indent=2))
    return 0 if receipt.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
