#!/usr/bin/env python3
"""docforge.cli — build / gate / seal a document, one command.

    python3 -m docforge engines [--selftest]      what can render, right now
    python3 -m docforge gates <file.pdf> [...]    run the verification chain
    python3 -m docforge build <spec.json>         compose -> render -> gate -> seal
    python3 -m docforge verify <ledger.jsonl>     re-check the whole chain

THE ORDER IS THE CONTROL
  build runs the gate chain BEFORE it seals. A document that fails a gate is not
  sealed — it is left on disk with a failure report, because a seal over a
  broken artifact launders the defect into the permanent record. Sealing is not
  a formality performed after the fact; it is the statement that verification
  already happened, so it must be impossible to reach without it.

WHY A SPEC FILE AND NOT FLAGS
  Six independent axes decide the output — source, template, theme, engine,
  gate profile, seal. Expressing that as flags invites an operator to omit one
  and get a silently different document. A spec is a reviewable artifact: it can
  be diffed, versioned, and committed beside the thing it produced.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from . import seal as sealmod
from .engines import ENGINES, PandocPreprocessor, inventory, resolve
from .gates import PROFILES, run_chain

HERE = Path(__file__).resolve().parent
DEFAULT_SPEC_GATES = {"profile": "print-light", "forbid_paths": True}


# ── engines ──────────────────────────────────────────────────────────────────


def cmd_engines(args) -> int:
    rows = inventory()
    width = max(len(r["engine"]) for r in rows)
    print("engine inventory — availability probed NOW, not assumed")
    print()
    for r in rows:
        mark = "OK  " if r["available"] else "DOWN"
        ver = r["version"] or r["reason"]
        caps = ",".join(k for k, v in r["caps"].items() if v)
        print(f"  [{mark}] {r['engine']:<{width}}  {ver}")
        print(f"          caps: {caps}")
    p = PandocPreprocessor()
    ok, ver, why = p.detect()
    print(f"  [{'OK  ' if ok else 'DOWN'}] {'pandoc':<{width}}  {ver or why}")
    print(f"          caps: preprocessor: markdown -> html (cannot read PDF)")
    print()
    print(f"  routing by suffix: " + ", ".join(
        f"{s}->{'/'.join(e)}" for s, e in
        ((".html", ["weasyprint", "chromium"]), (".typ", ["typst"]),
         (".md", ["weasyprint", "chromium"]), (".py", ["reportlab"]))))

    if args.selftest:
        print()
        print("SELFTEST — does each available engine actually emit a PDF?")
        tmp = Path("/tmp/docforge-selftest")
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir(parents=True)
        html = tmp / "t.html"
        html.write_text("<!DOCTYPE html><html><head><meta charset='utf-8'>"
                        "<style>@page{size:A4;margin:15mm}body{font-family:sans-serif}"
                        "</style></head><body><h1>docforge selftest</h1>"
                        "<p>one paragraph</p></body></html>")
        typ = tmp / "t.typ"
        typ.write_text('#set page(paper: "a4")\n= docforge selftest\none paragraph\n')
        failures = 0
        for name, eng in ENGINES.items():
            if name == "reportlab":
                continue  # needs a builder callable, exercised by the test suite
            ok, ver, why = eng.detect()
            if not ok:
                print(f"  [SKIP] {name}: {why}")
                continue
            src = typ if name == "typst" else html
            out = tmp / f"{name}.pdf"
            try:
                r = eng.render(src, out)
                head = out.open("rb").read(5)
                real = head == b"%PDF-"
                print(f"  [{'OK  ' if real else 'BAD '}] {name} {r.version} "
                      f"{r.seconds}s -> {out.stat().st_size}B "
                      f"{'real PDF' if real else 'NOT a PDF'}")
                failures += 0 if real else 1
            except Exception as exc:  # noqa: BLE001 - report, never mask
                print(f"  [FAIL] {name}: {exc}")
                failures += 1
        print()
        print("selftest:", "all available engines produced real PDFs" if not failures
              else f"{failures} engine(s) failed")
        return 1 if failures else 0
    return 0


# ── gates ────────────────────────────────────────────────────────────────────


def _print_findings(findings) -> bool:
    ok_all = True
    for f in findings:
        ok_all &= bool(f.ok)
        print(f"  [{'PASS' if f.ok else 'FAIL'}] {f.gate:<13} {f.detail}")
    return ok_all


def cmd_gates(args) -> int:
    pdf = Path(args.pdf).resolve()
    opts: dict = {"forbid_paths": True}
    if args.profile:
        opts["profile"] = args.profile
    if args.expect_pages is not None:
        opts["expect_pages"] = args.expect_pages
    if args.must_contain:
        opts["must_contain"] = args.must_contain
    if args.expect_images is not None:
        opts["expect_images"] = args.expect_images

    print(f"gate chain: {pdf.name}")
    if opts.get("profile"):
        print(f"profile   : {opts['profile']} "
              f"{json.dumps(PROFILES.get(opts['profile'], {}), separators=(',', ':'))}")
    print()
    findings = run_chain(pdf, opts)
    ok = _print_findings(findings)
    print()
    print("VERDICT:", "PASS — artifact may be delivered" if ok
          else "FAIL — do not deliver; fix the source and rebuild")
    return 0 if ok else 1


# ── build ────────────────────────────────────────────────────────────────────


def _compose(spec: dict, run_dir: Path) -> str:
    """Resolve template + theme + source into one standalone HTML document.

    Returns the CANONICAL text the content hash is taken over — the composed
    document with its hash placeholders still literal, so the hash is
    computable before it is injected into the thing it describes.
    """
    tpl_dir = HERE / "templates"
    registry = json.loads((tpl_dir / "registry.json").read_text())

    tname = spec.get("template", "base-a4")
    if tname not in registry["templates"]:
        raise RuntimeError(f"unknown template {tname!r}; known: "
                           f"{sorted(registry['templates'])}")
    tmeta = registry["templates"][tname]

    theme_name = spec.get("theme", tmeta.get("theme", "light"))
    themes = registry["themes"]
    if theme_name not in themes:
        raise RuntimeError(f"unknown theme {theme_name!r}; known: {sorted(themes)}")

    structure = (tpl_dir / tmeta["file"]).read_text()
    theme_css = (tpl_dir / themes[theme_name]).read_text()

    src = Path(spec["source"])
    if not src.is_absolute():
        src = (run_dir / src).resolve()
    if not src.exists():
        raise RuntimeError(f"source not found: {src}")

    if src.suffix.lower() in (".md", ".markdown"):
        pp = PandocPreprocessor()
        ok, _, why = pp.detect()
        if not ok:
            raise RuntimeError(f"markdown source needs pandoc: {why}")
        body_path = run_dir / "_body.html"
        pp.to_html(src, body_path)
        body = body_path.read_text()
        body = body.split("<body", 1)[1].split(">", 1)[1].rsplit("</body>", 1)[0]
    else:
        body = src.read_text()

    stats = spec.get("stats", {}) or {}
    composed = (structure
                .replace("{{THEME_CSS}}", theme_css)
                .replace("{{TITLE}}", spec.get("title", spec.get("edition", "Document")))
                .replace("{{SUBTITLE}}", spec.get("subtitle", ""))
                .replace("{{EDITION}}", spec.get("edition", ""))
                .replace("{{EDITION_DATE}}", spec.get("edition_date", ""))
                .replace("{{STAT_NEW}}", str(stats.get("new", 0)))
                .replace("{{STAT_OPEN}}", str(stats.get("still_open", 0)))
                .replace("{{STAT_CONTESTED}}", str(stats.get("moved", 0)))
                .replace("{{STAT_SETTLED}}", str(stats.get("settled", 0)))
                .replace("{{BODY}}", body))
    return composed


def cmd_build(args) -> int:
    spec_path = Path(args.spec).resolve()
    spec = json.loads(spec_path.read_text())
    run_dir = Path(spec.get("run_dir") or spec_path.parent).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"spec      : {spec_path}")
    print(f"run dir   : {run_dir}")

    # 1. compose
    composed = _compose(spec, run_dir)
    content_sha = sealmod.sha256_text(composed)
    print(f"template  : {spec.get('template', 'base-a4')}  "
          f"theme: {spec.get('theme', 'light')}")

    render_html = (composed
                   .replace("{{CONTENT_HASH}}", content_sha)
                   .replace("{{ARTIFACT_HASH}}",
                            f"delivered in {spec.get('edition','DOC')}.sha256 "
                            "&mdash; a file cannot embed its own hash"))
    work = run_dir / "_render.html"
    work.write_text(render_html)

    # 2. render
    src_path = Path(spec["engine_source"]) if spec.get("engine_source") else work
    engine, note = resolve(src_path, prefer=spec.get("engine"))
    out = run_dir / spec.get("artifact_name", f"{spec.get('edition','DOC')}.pdf")
    print(f"engine    : {note}")
    result = engine.render(src_path, out, spec.get("engine_opts", {}))
    print(f"rendered  : {out.name}  {out.stat().st_size}B  {result.seconds}s")

    # 3. gates BEFORE seal
    gopts = dict(DEFAULT_SPEC_GATES)
    gopts.update(spec.get("gates", {}))
    findings = run_chain(out, gopts)
    print()
    print("gate chain:")
    ok = _print_findings(findings)
    print()
    if not ok:
        print("REFUSED TO SEAL — one or more gates failed.")
        print("The artifact is on disk for inspection but carries no seal, because")
        print("a seal over a failed artifact writes the defect into the record.")
        return 1

    # 4. seal
    row = sealmod.seal(
        edition=spec.get("edition", "DOC"), edition_date=spec.get("edition_date", ""),
        source_text=composed, pdf=out, run_dir=run_dir, gates=findings,
        engine=result.engine, engine_version=result.version,
        profile=gopts.get("profile", ""), template=spec.get("template", "base-a4"),
    )
    print("SEALED")
    print(f"  content_sha256  {row['content_sha256']}")
    print(f"  artifact_sha256 {row['artifact_sha256']}")
    print(f"  sidecar         {row['sidecar']} (sha256sum -c: "
          f"{'OK' if row['sidecar_verified'] else 'FAILED'})")
    print(f"  chain_prev      {row['chain_prev']}")
    print(f"  signature       {row['signature']} — {row['signature_note']}")
    return 0


def cmd_verify(args) -> int:
    ledger = Path(args.ledger).resolve()
    ok, lines = sealmod.verify_chain(ledger)
    print(f"chain verify: {ledger}")
    for l in lines:
        print("  " + l)
    print()
    print("VERDICT:", "INTACT — linkage unbroken, every artifact re-hashed matches"
          if ok else "BROKEN — see findings above")
    return 0 if ok else 1


def cmd_feedback(args) -> int:
    """Record, list, retire and export the standing instructions."""
    from .feedback import FeedbackStore, capture_candidates

    db = Path(args.db or "/root/AAA/forge_work/brief-state.sqlite3")
    store = FeedbackStore(db)

    if args.fb_action == "add":
        text = args.text
        if not text and args.from_file:
            text = Path(args.from_file).read_text()
        if not text:
            print("nothing to add — pass text or --from-file", file=sys.stderr)
            return 2
        cands = capture_candidates(text) if args.split else [text]
        if not cands:
            print("no directive-shaped line found; nothing recorded. "
                  "Use --whole to record the message as one instruction.")
            return 1
        for c in cands:
            r = store.add(c, edition_ref=args.edition, source=args.source,
                          chat_id=args.chat_id, message_id=args.message_id)
            mark = "already standing" if r.get("duplicate") else "recorded"
            print(f"  {mark}: fb_id={r['fb_id']} [{r.get('direction','?')}] {r['rule']}")
        return 0

    if args.fb_action == "list":
        rows = store.all_rows() if args.all else store.active()
        if not rows:
            print("  no standing instructions")
            return 0
        for r in rows:
            state = "ACTIVE " if r["active"] else "retired"
            print(f"  {r['fb_id']:>3}  {state}  [{r['scope']}] {r['rule']}")
            print(f"        heard as: \"{r['raw_text']}\""
                  + (f"  (since {r['created_at'][:10]}, "
                     f"applied {r['applied_count']}x)" if r["active"] else
                     f"  (retired: {r['retire_reason']})"))
        return 0

    if args.fb_action == "retire":
        try:
            ok = store.retire(int(args.fb_id), args.reason or "")
        except ValueError as e:
            print(f"refused: {e}", file=sys.stderr)
            return 2
        print("retired" if ok else "no live rule with that id")
        return 0 if ok else 1

    if args.fb_action == "export":
        out = store.export_rules(Path(args.out) if args.out else None)
        print(f"exported {len(store.active())} standing instruction(s) -> {out}")
        return 0

    print("unknown feedback action", file=sys.stderr)
    return 2


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="docforge", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("engines", help="engine inventory")
    e.add_argument("--selftest", action="store_true",
                   help="render a probe document through every available engine")
    e.set_defaults(func=cmd_engines)

    g = sub.add_parser("gates", help="run the verification chain on a PDF")
    g.add_argument("pdf")
    g.add_argument("--profile", choices=sorted(PROFILES))
    g.add_argument("--expect-pages", type=int)
    g.add_argument("--expect-images", type=int)
    g.add_argument("--must-contain", action="append")
    g.set_defaults(func=cmd_gates)

    b = sub.add_parser("build", help="compose, render, gate, seal")
    b.add_argument("spec")
    b.set_defaults(func=cmd_build)

    v = sub.add_parser("verify", help="re-check a seal chain")
    v.add_argument("ledger")
    v.set_defaults(func=cmd_verify)

    f = sub.add_parser("feedback", help="standing instructions from Arif's own comments")
    f.add_argument("fb_action", choices=["add", "list", "retire", "export"])
    f.add_argument("text", nargs="?", help="for add: the comment or instruction")
    f.add_argument("--from-file", help="for add: read the text from a file")
    f.add_argument("--whole", dest="split", action="store_false", default=True,
                   help="add: record the whole message as ONE instruction "
                        "(default is to split directive lines out of it)")
    f.add_argument("--edition", help="add: the edition the comment was about")
    f.add_argument("--chat-id", help="add: provenance — which chat the comment "
                                     "came from (recorded, never used for routing)")
    f.add_argument("--message-id", help="add: provenance — the platform message id, "
                                        "so a later capture can tell if it was handled")
    f.add_argument("--source", default="telegram_reply",
                   choices=["telegram_reply", "manual", "system"])
    f.add_argument("--db", help="state database (default: the brief state db)")
    f.add_argument("--all", action="store_true", help="list: include retired rules")
    f.add_argument("--fb-id", help="retire: the fb_id to withdraw")
    f.add_argument("--reason", help="retire: why (required — an unexplained "
                                    "retirement is indistinguishable from a bug)")
    f.add_argument("--out", help="export: destination path")
    f.set_defaults(func=cmd_feedback)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
