#!/usr/bin/env python3
"""site-preflight.py — the active gate for arif-fazil.com deploys.

WHY THIS EXISTS
  arif-sites-ops carries a 92KB merged pitfall ledger. An agent about to deploy should not
  read 92KB of history to avoid four physical traps. Those four are mechanical, so they
  become a check, not prose. Prose stays for the cases a script cannot judge.

CHECKS (all read-only; nothing is written, nothing is deployed)
  a) split-root     — which Caddy handler actually serves <route>, and with which root/try_files
  b) orphan-assets  — live HTML naming a hashed asset that the new dist/ does not contain
  c) phantom-200    — the URL answers 200 with the SPA shell title instead of a real page
  d) redaction      — a deploy receipt contains no unredacted secret (delegates to
                      skill-artifact-redact/scripts/redact.py --check)

EXIT CODES
  0  all checks pass
  1  a check found a real defect (do not deploy)
  2  a check could not be evaluated (UNKNOWN — never reported as PASS)

USAGE
  site-preflight.py --check /world/politics/shadow/
  site-preflight.py --check /words/writing/foo/ --url https://arif-fazil.com/words/writing/foo/
  site-preflight.py --check /world/ --dist /root/arif-fazil.com/sites/arif-fazil.com/dist
  site-preflight.py --check /pm-bayang/ --receipt receipts/HERMES/deploy.json --json
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

VHOST = Path("/etc/caddy/vhosts/arif-fazil.com.conf")
LIVE_ROOT = Path("/var/www/html/arif")
DIST = Path("/root/arif-fazil.com/sites/arif-fazil.com/dist")
REDACT = Path("/root/AAA/skills/skill-artifact-redact/scripts/redact.py")
SITE = "https://arif-fazil.com"
SPA_TITLE_MARKERS = ("Exploration Geoscientist",)
UA = "Mozilla/5.0 (compatible; arifOS-site-preflight/1.0)"


# ── (a) split-root ────────────────────────────────────────────────────────────
def parse_handlers(conf: Path) -> list[dict]:
    """Return [{matcher, root, try_files}] for every `handle` in the vhost.

    Caddy config here is one-directive-per-line and two levels deep, so a depth counter
    is enough; this is not a general Caddyfile parser and says so.
    """
    out, depth, cur = [], 0, None
    for line in conf.read_text(errors="replace").splitlines():
        s = line.strip()
        if s.startswith("}"):
            depth -= 1
            if depth <= 0:
                cur = None
            continue
        m = re.match(r"handle(?:_path)?\s+(\S+)\s*\{", s)
        if m:
            cur = {"matcher": m.group(1), "root": None, "try_files": None}
            out.append(cur)
            depth = 1
            continue
        if cur is not None:
            r = re.match(r"root\s+\*\s+(\S+)", s)
            if r:
                cur["root"] = r.group(1)
            t = re.match(r"try_files\s+(.+)$", s)
            if t:
                cur["try_files"] = t.group(1).strip()
            if s.endswith("{"):
                depth += 1
    return out


def match_route(route: str, handlers: list[dict]) -> dict | None:
    """Longest matching path prefix wins, which is how Caddy orders these."""
    route = "/" + route.strip("/") + "/"
    best = None
    for h in handlers:
        m = h["matcher"]
        if not m.startswith("/"):
            continue            # named matcher (@foo) — cannot resolve statically
        prefix = m.rstrip("*").rstrip("/") + "/"
        if route.startswith(prefix):
            if best is None or len(prefix) > len(best["prefix"]):
                best = {**h, "prefix": prefix}
    return best


def check_split_root(route: str) -> dict:
    if not VHOST.exists():
        return {"check": "split-root", "state": "UNKNOWN", "detail": f"vhost missing: {VHOST}"}
    handlers = parse_handlers(VHOST)
    h = match_route(route, handlers)
    if h is None:
        return {"check": "split-root", "state": "FAIL",
                "detail": f"no Caddy handler matches {route} — the page is not routed",
                "handlers_seen": len(handlers)}
    root = h["root"]
    state = "PASS" if root else "UNKNOWN"
    detail = (f"handler {h['matcher']} -> root {root or '(inherited, not declared in block)'}"
              f" | try_files: {h['try_files'] or '(none)'}")
    mirror = None
    if root:
        served = Path(root) / route.strip("/")
        other = (LIVE_ROOT if Path(root) != LIVE_ROOT else Path("/var/www/html")) / route.strip("/")
        mirror = {"served_path": str(served), "served_exists": served.exists(),
                  "other_root_path": str(other), "other_root_exists": other.exists()}
        if other.exists() and not served.exists():
            state = "FAIL"
            detail += (" | SPLIT-ROOT TRAP: the file exists under the OTHER root — "
                       f"patch/serve {other} , not {served}")
    return {"check": "split-root", "state": state, "detail": detail, "paths": mirror}


# ── (b) orphan hashed assets ──────────────────────────────────────────────────
HASHED = re.compile(r"/assets/([A-Za-z0-9_.\-]+-[A-Za-z0-9_]{6,}\.(?:js|css))")


def check_orphans(route: str, dist: Path, live: Path) -> dict:
    """Route-scoped is the gate; global is reported, never blocking.

    Scope matters. On 2026-10-23 a global scan flagged 3 orphans that belonged to
    `geox/cockpit/`, a page nowhere near the route being checked — a false blocker built by
    a probe that was honest but too wide. A deploy of <route> can only break the HTML under
    <route>, so that is what gates. Everything else is reported as a separate finding.
    """
    if not live.exists():
        return {"check": "orphan-assets", "state": "UNKNOWN", "detail": f"live root missing: {live}"}
    if not dist.exists():
        return {"check": "orphan-assets", "state": "UNKNOWN",
                "detail": f"dist missing: {dist} — cannot compare (build first)"}

    new_assets = {p.name for p in (dist / "assets").glob("*")} if (dist / "assets").is_dir() else set()
    route_dir = live / route.strip("/")

    def orphans_under(base: Path) -> dict[str, set[str]]:
        found: dict[str, set[str]] = {}
        if not base.exists():
            return found
        for html in base.rglob("index.html"):
            try:
                body = html.read_text(errors="replace")
            except OSError:
                continue
            for name in HASHED.findall(body):
                if name not in new_assets and not (live / "assets" / name).exists():
                    found.setdefault(str(html.relative_to(live)), set()).add(name)
        return found

    scoped = orphans_under(route_dir)
    scoped_n = sum(len(v) for v in scoped.values())

    # global sweep, excluding the route (already counted)
    global_extra: dict[str, set[str]] = {}
    for html in live.rglob("index.html"):
        rel = str(html.relative_to(live))
        if rel.startswith(route.strip("/")):
            continue
        try:
            body = html.read_text(errors="replace")
        except OSError:
            continue
        for name in HASHED.findall(body):
            if name not in new_assets and not (live / "assets" / name).exists():
                global_extra.setdefault(rel, set()).add(name)

    if not route_dir.exists():
        state, detail = "UNKNOWN", (f"{route_dir} does not exist live — nothing to compare; "
                                   "this route has never been deployed under this root")
    elif scoped_n:
        state, detail = "FAIL", (f"{scoped_n} hashed asset(s) referenced by HTML under this route "
                                 "are gone from both dist/assets and live assets/ — an rsync "
                                 "would leave 404s")
    else:
        state, detail = "PASS", "every hashed asset used by this route still resolves"

    return {"check": "orphan-assets", "state": state, "detail": detail,
            "orphan_count": scoped_n,
            "sample": sorted({a for v in scoped.values() for a in v})[:8],
            "pages": sorted(scoped)[:8],
            "elsewhere": {"count": len(global_extra),
                          "pages": sorted(global_extra)[:6],
                          "note": "outside this route — reported, not blocking" if global_extra else ""}}


# ── (c) phantom 200 ──────────────────────────────────────────────────────────
def _fetch(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read(400_000), None
    except urllib.error.HTTPError as e:
        return e.code, (e.read(200_000) if e.fp else b""), None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, b"", f"{type(e).__name__}: {e}"


CF_SCRIPT = re.compile(rb"<script\b[^>]*>(?:(?!</script>).)*?(?:__CF\$|challenge-platform)(?:(?!</script>).)*?</script>", re.S)


def _stable(body: bytes) -> bytes:
    """Body minus per-request Cloudflare injection, for parent/child comparison.

    Cloudflare stamps every response with a unique `__CF$cv$params={r:'...'}` nonce, so two
    fetches of the SAME page are never byte-identical (verified 2026-10-23). Comparing raw
    bytes would make the hub-copy check silently always-false — a gate that cannot fire.
    """
    body = CF_SCRIPT.sub(b"", body)
    body = re.sub(rb"__CF\$cv\$params=\{[^}]*\}", b"", body)
    body = re.sub(rb"\s+", b" ", body)
    return body


def _title(body: bytes) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", body.decode("utf-8", "replace"), re.S | re.I)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def check_phantom(url: str, route: str) -> dict:
    """Three ways a 200 lies: SPA shell, hub served at a child URL, or parent fallback."""
    status, body, err = _fetch(url)
    if err:
        return {"check": "phantom-200", "state": "UNKNOWN",
                "detail": f"probe failed ({err}) — reachability unknown, NOT a pass"}
    if status == 404:
        return {"check": "phantom-200", "state": "FAIL", "status": 404,
                "detail": f"HTTP 404 at {url} — the route is not served at all"}
    title = _title(body)
    if any(m in title for m in SPA_TITLE_MARKERS):
        return {"check": "phantom-200", "state": "FAIL", "status": status, "title": title,
                "detail": f"200 but <title> is the SPA shell ('{title}') — the route has no page"}

    # hub-copy detection: Caddy try_files {path}/index.html <parent>/index.html means a
    # missing child gets the PARENT's file served at the child URL (the zombie-link class,
    # verified 2026-10-23 at /world/ai-founders/). Byte-equality with the parent is decisive.
    segs = [s for s in route.strip("/").split("/") if s]
    if len(segs) >= 2:
        parent = SITE + "/" + "/".join(segs[:-1]) + "/"
        pstatus, pbody, perr = _fetch(parent)
        if (perr is None and pstatus == 200 and pbody
                and _stable(pbody) == _stable(body) and len(_stable(body)) > 2000):
            return {"check": "phantom-200", "state": "FAIL", "status": status, "title": title,
                    "detail": (f"200 at {route} is the PARENT page ({parent}) served verbatim — "
                               "hub-copied-at-child-URL zombie, the file was never built")}

    return {"check": "phantom-200", "state": "PASS", "status": status, "title": title,
            "detail": f"200 with page-specific <title> ('{title}')", "bytes": len(body)}


# ── (d) redaction ────────────────────────────────────────────────────────────
def check_redaction(receipt: Path | None) -> dict:
    if receipt is None:
        return {"check": "redaction", "state": "SKIP",
                "detail": "no --receipt given; run it before the receipt leaves the machine"}
    if not receipt.exists():
        return {"check": "redaction", "state": "UNKNOWN", "detail": f"receipt missing: {receipt}"}
    if not REDACT.exists():
        return {"check": "redaction", "state": "UNKNOWN",
                "detail": f"redactor missing: {REDACT}"}
    r = subprocess.run([sys.executable, str(REDACT), "--check", str(receipt)],
                       capture_output=True, text=True)
    classes = [l.split("REDACTED[")[1].split("]")[0]
               for l in r.stderr.splitlines() if "REDACTED[" in l]
    state = "PASS" if r.returncode == 0 else "FAIL"
    return {"check": "redaction", "state": state,
            "detail": ("no secret class matched" if state == "PASS"
                       else f"{len(classes)} secret class hit — redact before this receipt moves"),
            "classes": classes}


def main() -> int:
    ap = argparse.ArgumentParser(description="read-only preflight gate for arif-fazil.com")
    ap.add_argument("--check", required=True, metavar="ROUTE")
    ap.add_argument("--url", default=None)
    ap.add_argument("--dist", default=str(DIST))
    ap.add_argument("--live", default=str(LIVE_ROOT))
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    route = a.check
    url = a.url or SITE + "/" + route.strip("/") + "/"
    results = [
        check_split_root(route),
        check_orphans(route, Path(a.dist), Path(a.live)),
        check_phantom(url, route),
        check_redaction(Path(a.receipt) if a.receipt else None),
    ]
    hard = [r for r in results if r["state"] == "FAIL"]
    unknown = [r for r in results if r["state"] == "UNKNOWN"]
    verdict = "FAIL" if hard else ("UNKNOWN" if unknown else "PASS")

    if a.json:
        print(json.dumps({"route": route, "url": url, "verdict": verdict, "checks": results},
                         indent=2))
    else:
        print(f"site-preflight  route={route}")
        print(f"  url            {url}")
        for r in results:
            print(f"  [{r['state']:7s}] {r['check']:14s} {r['detail']}")
        print(f"  VERDICT        {verdict}")
        if verdict == "PASS":
            print("  note: PASS is mechanical only — it does not judge content or design.")
    return 0 if verdict == "PASS" else (1 if hard else 2)


if __name__ == "__main__":
    sys.exit(main())
