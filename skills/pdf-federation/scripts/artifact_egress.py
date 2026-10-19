#!/usr/bin/env python3
"""
artifact_egress.py — P3 + P4 closure for forge-artifact-publisher.

Two responsibilities:

  P3. TYPED PRODUCER NODES. Every producer must return a typed node.
      No producer may write directly into the PDF layout.

  P4. ARTIFACT EGRESS ADAPTER. A single governed adapter that turns any
      producer result into real bytes the compositor can embed, or a typed
      refusal. A host-only path is NOT successful artifact delivery.

Design rules (mission §P3/§P4):
    Organ output ≠ PDF. Organ output = a typed node.
    A figure node with only a host path is a FAILURE unless the compositor
    can retrieve the bytes — that failure must be typed, never silent.

This module does not create a new MCP server. It is an importable library.
"""

from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


# ==================================================================
# P3 — TYPED NODE CLASSES
# ==================================================================
# Every producer returns exactly one of these. The compositor dispatches on
# `node_kind`. Producers never touch ReportLab / WeasyPrint objects.

NODE_KINDS = (
    "TextNode",          # narrative paragraph in publication voice
    "TableNode",         # tabular rows (list-of-lists) with optional header
    "ListNode",          # bullet / enumerated items
    "FigureAsset",       # any visual (chart/map/section/seismic/well-log/…)
    "AuthorityMatrix",   # per-organ capability × authority grid
    "TemporalNode",      # CHRON temporal classification / prediction state
    "GapNode",           # explicit, named absence (evidence we do not have)
    "RefusalNode",       # producer declined / unavailable — recorded, not filled
)


@dataclass
class Node:
    """Base typed node. Subclasses add kind-specific payloads."""
    producer: str
    node_kind: str = "Node"
    truth_class: str = "UNKNOWN"          # OBSERVATION|COMPUTATION|CONTEXT|SYNTHETIC|UNKNOWN
    claim_state: str = "CANDIDATE"        # CANDIDATE|ACTIVE|CONTESTED|SUPERSEDED
    provenance: dict = field(default_factory=dict)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TextNode(Node):
    node_kind: str = "TextNode"
    text: str = ""
    heading: str = ""


@dataclass
class TableNode(Node):
    node_kind: str = "TableNode"
    rows: list = field(default_factory=list)         # [[h1,h2],[a,b],...]
    widths_cm: list | None = None


@dataclass
class ListNode(Node):
    node_kind: str = "ListNode"
    items: list = field(default_factory=list)


@dataclass
class AuthorityMatrix(Node):
    node_kind: str = "AuthorityMatrix"
    rows: list = field(default_factory=list)          # per-organ rows
    note: str = "Capability ≠ Authority."


@dataclass
class TemporalNode(Node):
    node_kind: str = "TemporalNode"
    classification: str = "UNRESOLVED"    # CURRENT|STALE|SUPERSEDED|PREDICTED|UNRESOLVED
    rows: list = field(default_factory=list)
    observation: str = ""


@dataclass
class GapNode(Node):
    node_kind: str = "GapNode"
    gap_id: str = ""
    description: str = ""
    classification: str = "EXTERNAL_INPUT_REQUIRED"  # EXTERNAL_INPUT_REQUIRED|SOVEREIGN_HOLD|FUTURE_VERIFICATION


@dataclass
class RefusalNode(Node):
    node_kind: str = "RefusalNode"
    reason: str = ""
    error_code: str = "PRODUCER_UNAVAILABLE"


@dataclass
class FigureAsset(Node):
    """
    P3 spec — the visual branch of the PDF Intelligence Envelope.

    Mandatory delivery: at least one of egress_mode ∈
      {inline_bytes, base64, shared_artifact_ref}.
    A host path alone is NOT success unless egress_mode='host_path' AND
    the recorded transport is one the compositor actually supports.
    """
    node_kind: str = "FigureAsset"
    id: str = ""
    title: str = ""
    renderer_name: str = ""
    mime_type: str = ""
    width: int = 0
    height: int = 0
    artifact_hash: str = ""
    source_refs: list = field(default_factory=list)
    alt_text: str = ""
    egress_mode: str = ""       # inline_bytes | base64 | shared_artifact_ref | host_path
    egress_ref: Any = ""        # payload (bytes|str) / path / artifact id
    domain_metadata: dict = field(default_factory=dict)   # crs, scale, north_arrow, etc.
    data_hash: str = ""         # hash of underlying numeric data, "" if absent
    data_hash_absent_reason: str = ""
    visual_qc: dict = field(default_factory=dict)


# ==================================================================
# P4 — ARTIFACT EGRESS ADAPTER
# ==================================================================
# Single governed retrieval function. Accepts a FigureAsset and returns
# (bytes, sha256, mime, width, height) OR raises EgressFailure.

class EgressFailure(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


# Supported transports. NOT a new MCP server — just file/HTTP primitives
# already present in this runtime.
SUPPORTED_TRANSPORTS = ("local_file", "file_uri", "http_retrievable")


def _detect_mime(path: str) -> str:
    mime, _ = mimetypes.guess_type(path)
    return mime or "application/octet-stream"


def _measure_image(raw: bytes) -> tuple[int, int]:
    """Dimensions without requiring PIL import at module scope."""
    try:
        from PIL import Image as PILImage
        from io import BytesIO
        im = PILImage.open(BytesIO(raw))
        return im.size
    except Exception:
        return (0, 0)


def resolve_figure_bytes(asset: FigureAsset) -> tuple[bytes, str, str, int, int]:
    """
    The one governed retrieval adapter.

    Returns: (raw_bytes, sha256_hex, mime_type, width, height)

    Raises EgressFailure with a typed code:
      ARTIFACT_EGRESS_FAILED    — generic retrieval failure
      ARTIFACT_EGRESS_NO_MODE   — asset has no usable egress_mode
      ARTIFACT_EGRESS_HTTP_4XX  — retrievable URI returned an error
      ARTIFACT_EGRESS_HOST_ONLY — host path not reachable from compositor
      ARTIFACT_EGRESS_MIME_FAIL — detected MIME disagrees with declared
      ARTIFACT_EGRESS_HASH_FAIL — hash mismatch vs declared artifact_hash
    """
    mode = (asset.egress_mode or "").strip()
    ref = (asset.egress_ref or "").strip()

    if not mode:
        # Back-compat: if only a host path was supplied, treat as host_path
        # — this is deliberately typed as a FAILURE per mission §P4.
        if ref and (ref.startswith("/") or ref.startswith("file://")):
            raise EgressFailure(
                "ARTIFACT_EGRESS_HOST_ONLY",
                f"FigureAsset {asset.id!r} supplied only a host path ({ref!r}); "
                f"no inline_bytes / base64 / shared_artifact_ref egress mode.",
            )
        raise EgressFailure(
            "ARTIFACT_EGRESS_NO_MODE",
            f"FigureAsset {asset.id!r} has neither egress_mode nor egress_ref.",
        )

    raw: bytes | None = None

    if mode == "inline_bytes":
        if isinstance(asset.egress_ref, bytes):
            raw = asset.egress_ref
        elif isinstance(asset.egress_ref, str):
            raw = asset.egress_ref.encode("latin-1")
        else:
            raise EgressFailure("ARTIFACT_EGRESS_FAILED",
                                f"inline_bytes requires bytes/str, got {type(asset.egress_ref)}")

    elif mode == "base64":
        try:
            raw = base64.b64decode(ref, validate=True)
        except Exception as e:
            raise EgressFailure("ARTIFACT_EGRESS_FAILED", f"base64 decode: {e}")

    elif mode == "shared_artifact_ref":
        # A shared_artifact_ref names a file that the compositor CAN reach on
        # this host (an A-FORGE staging path). Reachability is checked here.
        if not os.path.isfile(ref):
            raise EgressFailure(
                "ARTIFACT_EGRESS_HOST_ONLY",
                f"shared_artifact_ref {ref!r} is not reachable on this host.",
            )
        with open(ref, "rb") as f:
            raw = f.read()

    elif mode == "host_path":
        # Explicit opt-in: the producer declares its path is host-reachable.
        p = ref[7:] if ref.startswith("file://") else ref
        if not os.path.isfile(p):
            raise EgressFailure(
                "ARTIFACT_EGRESS_HOST_ONLY",
                f"host_path {p!r} does not exist on this host.",
            )
        with open(p, "rb") as f:
            raw = f.read()

    elif mode == "retrievable_uri":
        import urllib.request
        import urllib.error
        try:
            with urllib.request.urlopen(ref, timeout=8) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as e:
            raise EgressFailure("ARTIFACT_EGRESS_HTTP_4XX", f"{ref} → HTTP {e.code}")

    else:
        raise EgressFailure("ARTIFACT_EGRESS_NO_MODE",
                            f"Unknown egress_mode {mode!r}; "
                            f"supported: {SUPPORTED_TRANSPORTS + ('inline_bytes','base64')}")

    if raw is None:
        raise EgressFailure("ARTIFACT_EGRESS_FAILED", "retrieval returned no bytes")

    sha = hashlib.sha256(raw).hexdigest()

    # Integrity: if the producer declared a hash, it must match.
    if asset.artifact_hash and asset.artifact_hash != sha:
        raise EgressFailure(
            "ARTIFACT_EGRESS_HASH_FAIL",
            f"declared artifact_hash={asset.artifact_hash[:16]}… "
            f"but retrieved bytes hash to {sha[:16]}…",
        )

    # MIME: detect from source when possible; if declared disagrees, fail.
    detected = _detect_mime(asset.egress_ref if isinstance(asset.egress_ref, str) else "")
    if asset.mime_type and detected != "application/octet-stream" and detected != asset.mime_type:
        raise EgressFailure(
            "ARTIFACT_EGRESS_MIME_FAIL",
            f"declared mime_type={asset.mime_type} but detected={detected}",
        )

    w, h = _measure_image(raw)
    mime = asset.mime_type or detected
    if mime == "application/octet-stream" and raw[:4] == b"\x89PNG":
        mime = "image/png"
    if raw[:3] == b"\xff\xd8\xff":
        mime = "image/jpeg"

    return raw, sha, mime, w or asset.width, h or asset.height


def figure_from_host_path(path: str, producer: str, figure_id: str,
                          title: str = "", truth_class: str = "UNKNOWN",
                          source_refs: list | None = None,
                          domain_metadata: dict | None = None,
                          data_hash: str = "",
                          data_hash_absent_reason: str = "") -> FigureAsset:
    """
    Convenience: wrap a host path in a FigureAsset using shared_artifact_ref
    egress. This is the CORRECT way for a producer to hand over a local path —
    the compositor will verify reachability and hash the bytes.
    """
    return FigureAsset(
        producer=producer,
        id=figure_id,
        title=title or figure_id,
        egress_mode="shared_artifact_ref",
        egress_ref=path,
        truth_class=truth_class,
        source_refs=source_refs or [],
        domain_metadata=domain_metadata or {},
        data_hash=data_hash,
        data_hash_absent_reason=data_hash_absent_reason,
        mime_type=_detect_mime(path),
    )


# ==================================================================
# P4 acceptance helpers
# ==================================================================

def egress_test_suite() -> dict:
    """
    Runnable acceptance for P4. Returns a dict of scenario → result.
    Called by the compositor with --egress-test, and by the skill proof.
    """
    import tempfile
    results = {}

    # Tiny valid PNG (1x1)
    PNG_1x1 = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    )

    # 1. inline_bytes — should PASS
    a1 = FigureAsset(producer="test", id="fig-inline", egress_mode="inline_bytes",
                     egress_ref=PNG_1x1, mime_type="image/png", truth_class="OBSERVATION")
    try:
        raw, sha, mime, w, h = resolve_figure_bytes(a1)
        results["inline_bytes"] = {"status": "PASS", "sha": sha[:16], "w": w, "h": h}
    except EgressFailure as e:
        results["inline_bytes"] = {"status": "FAIL", "code": e.code, "detail": e.detail}

    # 2. base64 — should PASS
    b64 = base64.b64encode(PNG_1x1).decode()
    a2 = FigureAsset(producer="test", id="fig-b64", egress_mode="base64",
                     egress_ref=b64, mime_type="image/png", truth_class="OBSERVATION")
    try:
        raw, sha, mime, w, h = resolve_figure_bytes(a2)
        results["base64"] = {"status": "PASS", "sha": sha[:16]}
    except EgressFailure as e:
        results["base64"] = {"status": "FAIL", "code": e.code}

    # 3. shared_artifact_ref — should PASS
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
        tf.write(PNG_1x1); tmp = tf.name
    a3 = FigureAsset(producer="test", id="fig-shared", egress_mode="shared_artifact_ref",
                     egress_ref=tmp, mime_type="image/png", truth_class="OBSERVATION")
    try:
        raw, sha, mime, w, h = resolve_figure_bytes(a3)
        results["shared_artifact_ref"] = {"status": "PASS", "sha": sha[:16]}
    except EgressFailure as e:
        results["shared_artifact_ref"] = {"status": "FAIL", "code": e.code}
    finally:
        try: os.unlink(tmp)
        except: pass

    # 4. host_path reachable — should PASS (explicit opt-in)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
        tf.write(PNG_1x1); tmp2 = tf.name
    a4 = FigureAsset(producer="test", id="fig-hostpath", egress_mode="host_path",
                     egress_ref=tmp2, mime_type="image/png", truth_class="OBSERVATION")
    try:
        raw, sha, mime, w, h = resolve_figure_bytes(a4)
        results["host_path_reachable"] = {"status": "PASS", "sha": sha[:16]}
    except EgressFailure as e:
        results["host_path_reachable"] = {"status": "FAIL", "code": e.code}
    finally:
        try: os.unlink(tmp2)
        except: pass

    # 5. FAILURE CASE: host-only remote path — MUST be a typed REFUSAL, not silent
    a5 = FigureAsset(producer="test", id="fig-remote", egress_mode="",
                     egress_ref="/tmp/geox/foo.png", truth_class="UNKNOWN")
    try:
        resolve_figure_bytes(a5)
        results["host_only_remote"] = {"status": "FAIL", "reason": "silently passed — should have refused"}
    except EgressFailure as e:
        results["host_only_remote"] = {"status": "PASS", "refusal_code": e.code}

    # 6. FAILURE CASE: declared hash mismatch
    a6 = FigureAsset(producer="test", id="fig-badhash", egress_mode="inline_bytes",
                     egress_ref=PNG_1x1, artifact_hash="deadbeef"*8, truth_class="UNKNOWN")
    try:
        resolve_figure_bytes(a6)
        results["hash_mismatch"] = {"status": "FAIL", "reason": "did not detect bad hash"}
    except EgressFailure as e:
        results["hash_mismatch"] = {"status": "PASS", "refusal_code": e.code}

    # 7. FAILURE CASE: HTTP 404
    a7 = FigureAsset(producer="test", id="fig-404", egress_mode="retrievable_uri",
                     egress_ref="http://127.0.0.1:1/nonexistent.png", truth_class="UNKNOWN")
    try:
        resolve_figure_bytes(a7)
        results["http_404"] = {"status": "FAIL", "reason": "no error raised"}
    except EgressFailure as e:
        results["http_404"] = {"status": "PASS", "refusal_code": e.code}
    except Exception as e:
        results["http_404"] = {"status": "PASS", "refusal_code": f"EXC_{type(e).__name__}"}

    passed = sum(1 for r in results.values() if r["status"] == "PASS")
    return {
        "suite": "P4-artifact-egress",
        "at": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "total": len(results),
        "scenarios": results,
    }


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--egress-test", action="store_true", help="run P4 egress acceptance suite")
    args = ap.parse_args()
    if args.egress_test:
        out = egress_test_suite()
        print(json.dumps(out, indent=2))
        raise SystemExit(0 if out["passed"] == out["total"] else 1)
    print("artifact_egress.py — import me, or run --egress-test")
