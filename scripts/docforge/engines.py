#!/usr/bin/env python3
"""docforge.engines — pluggable render backends behind one contract.

WHY A REGISTRY AND NOT IF/ELSE
  The federation carries roughly twenty skills that each build a PDF with their
  own inline command. When the engine changes, twenty places change. This module
  collapses that to one contract:

      detect()  -> (available: bool, version: str, reason: str)
      render()  -> RenderResult

  An engine that cannot run is REPORTED as unavailable, never silently
  substituted. Which lane produced an artifact is part of that artifact's
  provenance, so the caller always learns the engine's name and version.

CAPABILITY HONESTY
  No engine is "best". They are different. Paged media (running headers,
  footnotes, page counters) is a CSS Paged Media feature: WeasyPrint and Typst
  have it, headless Chromium does not. JavaScript is the reverse. Declaring the
  axis let the caller choose instead of guessing, and let a gate assert that an
  engine was not used for something it cannot do.
"""
from __future__ import annotations

import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

# ── result objects ────────────────────────────────────────────────────────────


@dataclass
class RenderResult:
    engine: str
    version: str
    out: Path
    seconds: float
    caps: dict = field(default_factory=dict)
    notes: str = ""


# ── contract ──────────────────────────────────────────────────────────────────


class Engine:
    name = "engine"
    caps: dict = {}

    def detect(self) -> tuple[bool, str, str]:
        """Return (available, version, reason). reason is set when unavailable."""
        raise NotImplementedError

    def render(self, source: Path, out: Path, opts: dict | None = None) -> RenderResult:
        raise NotImplementedError

    # helper: run a command, raise with captured stderr so failures are readable
    @staticmethod
    def _run(cmd: list[str], timeout: int = 300) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def _first_line(s: str) -> str:
    s = (s or "").strip()
    return s.splitlines()[0] if s else ""


# ── WeasyPrint — HTML/CSS -> PDF, full CSS Paged Media, no JavaScript ─────────


class WeasyPrintEngine(Engine):
    name = "weasyprint"
    caps = {"paged_media": True, "javascript": False, "scripting": False,
            "programmatic": False, "offline": True}

    def detect(self):
        try:
            import weasyprint  # noqa: F401
        except Exception as exc:
            return False, "", f"python import failed: {exc}"
        return True, getattr(__import__("weasyprint"), "__version__", "unknown"), ""

    def render(self, source: Path, out: Path, opts=None):
        opts = opts or {}
        t0 = time.time()
        import weasyprint

        try:
            weasyprint.HTML(filename=str(source)).write_pdf(str(out))
        except Exception as exc:
            raise RuntimeError(f"weasyprint render failed: {exc}") from exc

        return RenderResult(
            engine=self.name,
            version=getattr(weasyprint, "__version__", "unknown"),
            out=out, seconds=round(time.time() - t0, 2), caps=self.caps,
            notes="native paged media; no JS execution",
        )


# ── headless Chromium — real browser, JS, but NOT paged media ────────────────


class ChromiumEngine(Engine):
    name = "chromium"
    caps = {"paged_media": False, "javascript": True, "scripting": True,
            "programmatic": False, "offline": True}

    BINARIES = ("google-chrome", "chromium-browser", "chromium", "chrome")

    def _bin(self) -> str | None:
        for b in self.BINARIES:
            p = shutil.which(b)
            if p:
                return p
        return None

    def detect(self):
        p = self._bin()
        if not p:
            return False, "", "no chromium/chrome binary on PATH"
        r = self._run([p, "--version"], timeout=30)
        return True, _first_line(r.stdout) or "chromium", ""

    def render(self, source: Path, out: Path, opts=None):
        opts = opts or {}
        p = self._bin()
        if not p:
            raise RuntimeError("chromium not available")
        t0 = time.time()

        # --no-pdf-header-footer is not optional: without it the render date, the
        # document title and the raw file:/// path print on every page. A
        # third-party deliverable must never carry an internal filesystem path.
        cmd = [
            p, "--headless=new", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            f"--virtual-time-budget={int(opts.get('virtual_time_budget', 15000))}",
            f"--print-to-pdf={out}", f"file://{source.resolve()}",
        ]
        r = self._run(cmd, timeout=int(opts.get("timeout", 300)))
        if not out.exists():
            raise RuntimeError(
                "chromium produced no file; stderr: " + (_first_line(r.stderr) or "empty")
            )
        return RenderResult(
            engine=self.name, version=_first_line(self._run([p, "--version"], 30).stdout),
            out=out, seconds=round(time.time() - t0, 2), caps=self.caps,
            notes="--no-pdf-header-footer set; @page margin must be 0 for fixed-size slides",
        )


# ── Typst — modern typesetting, fast, scriptable, paged ──────────────────────


class TypstEngine(Engine):
    name = "typst"
    caps = {"paged_media": True, "javascript": False, "scripting": True,
            "programmatic": False, "offline": True}

    def _bin(self) -> str | None:
        return shutil.which("typst") or (
            "/root/.local/bin/typst" if Path("/root/.local/bin/typst").exists() else None
        )

    def detect(self):
        p = self._bin()
        if not p:
            return False, "", "typst not on PATH"
        r = self._run([p, "--version"], timeout=30)
        return True, _first_line(r.stdout) or "typst", ""

    def render(self, source: Path, out: Path, opts=None):
        opts = opts or {}
        p = self._bin()
        if not p:
            raise RuntimeError("typst not available")
        t0 = time.time()
        cmd = [p, "compile", str(source), str(out)]
        fp = opts.get("font_path")
        if fp:
            cmd += ["--font-path", str(fp)]
        r = self._run(cmd, timeout=int(opts.get("timeout", 300)))
        if r.returncode != 0 or not out.exists():
            raise RuntimeError(f"typst compile failed: {_first_line(r.stderr)}")
        return RenderResult(
            engine=self.name, version=_first_line(self._run([p, "--version"], 30).stdout),
            out=out, seconds=round(time.time() - t0, 2), caps=self.caps,
            notes="compiled typesetting; scripting built in",
        )


# ── ReportLab — programmatic canvas, no HTML at all ──────────────────────────


class ReportLabEngine(Engine):
    name = "reportlab"
    caps = {"paged_media": False, "javascript": False, "scripting": True,
            "programmatic": True, "offline": True}

    def detect(self):
        try:
            import reportlab
        except Exception as exc:
            return False, "", f"python import failed: {exc}"
        return True, getattr(reportlab, "Version", "unknown"), ""

    def render(self, source: Path, out: Path, opts=None):
        """source is EITHER a .py module exposing build(path) OR ignored when
        opts['builder'] names 'module:function'."""
        opts = opts or {}
        t0 = time.time()
        import importlib
        import sys

        spec = opts.get("builder")
        if not spec:
            raise RuntimeError("reportlab engine requires opts['builder']='module:function'")
        mod_name, _, fn_name = spec.partition(":")
        if str(source.parent) not in sys.path:
            sys.path.insert(0, str(source.parent))
        if str(source.parent.parent) not in sys.path:
            sys.path.insert(0, str(source.parent.parent))
        mod = importlib.import_module(mod_name)
        fn = getattr(mod, fn_name)
        fn(str(out))
        if not out.exists():
            raise RuntimeError("builder returned without writing the target file")
        import reportlab
        return RenderResult(
            engine=self.name, version=getattr(reportlab, "Version", "unknown"),
            out=out, seconds=round(time.time() - t0, 2), caps=self.caps,
            notes=f"programmatic build via {spec}",
        )


# ── Pandoc — preprocessor, not an engine ─────────────────────────────────────


class PandocPreprocessor:
    """markdown -> standalone HTML, then hand to a real engine.

    Pandoc cannot read PDF. The only valid direction is md -> html -> pdf.
    Keeping it a preprocessor rather than an engine stops anyone routing a PDF
    *into* it by accident.
    """

    name = "pandoc"

    def detect(self):
        p = shutil.which("pandoc")
        if not p:
            return False, "", "pandoc not on PATH"
        r = subprocess.run([p, "--version"], capture_output=True, text=True, timeout=30)
        return True, _first_line(r.stdout) or "pandoc", ""

    def to_html(self, md: Path, out: Path, title: str = "", css: Path | None = None) -> Path:
        p = shutil.which("pandoc")
        if not p:
            raise RuntimeError("pandoc not available")
        cmd = [p, str(md), "-o", str(out), "--standalone",
               "--metadata", f"title={title or md.stem}"]
        if css:
            cmd += ["--css", str(css)]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode != 0 or not out.exists():
            raise RuntimeError("pandoc failed: " + _first_line(r.stderr))
        return out


# ── registry ─────────────────────────────────────────────────────────────────

ENGINES: dict[str, Engine] = {
    e.name: e for e in (
        WeasyPrintEngine(), ChromiumEngine(), TypstEngine(), ReportLabEngine(),
    )
}

# source suffix -> the engines that can consume it, best first
SUFFIX_ROUTING = {
    ".html": ["weasyprint", "chromium"],
    ".htm":  ["weasyprint", "chromium"],
    ".svg":  ["weasyprint"],
    ".typ":  ["typst"],
    ".md":   ["weasyprint", "chromium"],   # via PandocPreprocessor
    ".markdown": ["weasyprint", "chromium"],
    ".py":   ["reportlab"],
}


def inventory() -> list[dict]:
    """Every engine, whether it resolves RIGHT NOW, and its declared axis."""
    rows = []
    for name, eng in ENGINES.items():
        ok, ver, why = eng.detect()
        rows.append({"engine": name, "available": ok, "version": ver,
                     "reason": why, "caps": eng.caps})
    return rows


def resolve(source: Path, prefer: str | None = None) -> tuple[Engine, str]:
    """Pick an engine that (a) can eat this suffix and (b) actually resolves.

    Returns (engine, note). Raises with the full inventory when nothing fits,
    because 'no engine' and 'engine not installed' are different failures and
    the operator needs to see which one happened.
    """
    cand = SUFFIX_ROUTING.get(source.suffix.lower())
    if not cand:
        raise RuntimeError(
            f"no engine is declared for suffix {source.suffix!r}. "
            f"known: {sorted(SUFFIX_ROUTING)}"
        )
    order = ([prefer] if prefer else []) + [c for c in cand if c != prefer]
    problems = []
    for name in order:
        eng = ENGINES.get(name)
        if not eng:
            problems.append(f"{name}: not a registered engine")
            continue
        ok, ver, why = eng.detect()
        if ok:
            return eng, f"resolved {name} {ver}"
        problems.append(f"{name}: {why}")
    raise RuntimeError(
        "no usable engine for " + source.name + " -> " + "; ".join(problems)
    )
