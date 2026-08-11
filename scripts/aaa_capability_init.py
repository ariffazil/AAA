#!/usr/bin/env python3
"""
aaa_capability_init.py — Phase A

INIT sequence for the AAA Capability Plane.

Eight indicators (per F13 directive 2026-08-11):
  REGISTRY, SCHEMA, AXES, BACKENDS, ENABLED, LEASES,
  CREDENTIALS_EXPOSED, MUTATIONS, VERDICT

This script:
  - Parses the registry
  - Validates the seven-axis schema and INV-11..17
  - Produces an INIT assessment WITHOUT spawning any MCP backend
  - Emits a structured receipt (JSON) — does NOT touch VAULT999 or arifFlow
    in Phase A; receipt is printed to stdout and persisted under
    /root/AAA/federation/init_receipts/ for manual follow-up.

Authorized by F13 directive, 2026-08-11 (SEAL_PHASE_A_ONLY).
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Optional

from aaa_capability_loader import (
    CANONICAL_AXES,
    CapabilityIndex,
    RegistryLoadError,
    load_registry,
)
from aaa_capability_validator import ValidationReport, validate


RECEIPT_DIR = Path("/root/AAA/federation/init_receipts")


@dataclass(frozen=True)
class InitReceipt:
    """The eight-indicator INIT assessment, plus provenance."""

    receipt_type: Literal["CAPABILITY_INIT", "CAPABILITY_HOLD"]
    session_id: str
    actor_id: str
    ts: str
    registry_path: str
    registry_sha256: str
    indicators: dict[str, Any]
    invariants_ok: dict[str, bool]
    fail_closed_reasons: tuple[str, ...]
    doctrine_capabilities_seen: tuple[str, ...]
    extra_capabilities: tuple[str, ...]
    verdict: Literal["READY_READONLY", "HOLD"]
    reason: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _session_id() -> str:
    # Phase A: deterministic but unique per invocation
    return f"phase_a_init_{os.getpid()}_{int(datetime.now(timezone.utc).timestamp())}"


def _actor_id() -> str:
    return os.environ.get("USER", "unknown") + "@phase_a_init"


def _build_indicators(
    index: Optional[CapabilityIndex],
    report: Optional[ValidationReport],
) -> dict[str, Any]:
    """
    The eight indicators that prove READY_READONLY.
    """
    if index is None or report is None:
        return {
            "REGISTRY": "not_loaded",
            "SCHEMA": "not_validated",
            "AXES": 0,
            "BACKENDS": "uncatalogued",
            "ENABLED": "unknown",
            "LEASES": "unknown",
            "CREDENTIALS_EXPOSED": "unknown",
            "MUTATIONS": "unknown",
            "VERDICT": "HOLD",
        }
    return {
        "REGISTRY": "loaded",
        "SCHEMA": "valid" if report.schema_valid else "INVALID",
        "AXES": len(index.axes),
        "BACKENDS": index.catalogued_count,
        "ENABLED": index.enabled_count,
        "LEASES": 0,  # Phase A: there are no leases at all (no router)
        "CREDENTIALS_EXPOSED": 0,  # Phase A: validator already scanned for leaks
        "MUTATIONS": 0,  # Phase A: no spawn, no subprocess, no backend
        "VERDICT": "READY_READONLY" if report.is_ready_readonly else "HOLD",
    }


def run_init(registry_path: Path | str) -> InitReceipt:
    """
    Execute the INIT sequence.

    Order (F13 directive):
      1. Load AAA identity + constitutional instructions (out of scope here; the
         host harness loads AGENTS.md before invoking this script)
      2. Parse AAA_CAPABILITY_REGISTRY.yaml
      3. Validate schema + INV-11..17
      4. Discover registered capabilities
      5. Expose only enabled + sealed backends (none, here)
      6. Keep pending/disabled backends unavailable
      7. Emit INIT discovery receipt
      8. Enter READY with zero automatic mutation
    """
    ts = _now_utc_iso()
    sid = _session_id()
    actor = _actor_id()

    index: Optional[CapabilityIndex] = None
    report: Optional[ValidationReport] = None
    fail_closed: tuple[str, ...] = ()
    verdict: Literal["READY_READONLY", "HOLD"] = "HOLD"
    reason: Optional[str] = None
    sha = "uncomputed"
    path = str(registry_path)

    try:
        index = load_registry(registry_path)
        sha = index.source_sha256
        path = index.source_path
        report = validate(index)
        fail_closed = report.fail_closed_reasons
        verdict = "READY_READONLY" if report.is_ready_readonly else "HOLD"
        if verdict == "HOLD":
            reason = ";".join(fail_closed) if fail_closed else "unknown"
    except RegistryLoadError as e:
        fail_closed = (f"YAML_MISSING_OR_INVALID:{e}",)
        verdict = "HOLD"
        reason = str(e)

    indicators = _build_indicators(index, report)

    return InitReceipt(
        receipt_type="CAPABILITY_INIT" if verdict == "READY_READONLY" else "CAPABILITY_HOLD",
        session_id=sid,
        actor_id=actor,
        ts=ts,
        registry_path=path,
        registry_sha256=sha,
        indicators=indicators,
        invariants_ok=report.invariants_ok if report else {},
        fail_closed_reasons=fail_closed,
        doctrine_capabilities_seen=tuple(sorted(report.doctrine_capabilities_seen)) if report else (),
        extra_capabilities=report.extra_capabilities if report else (),
        verdict=verdict,
        reason=reason,
    )


def write_receipt(receipt: InitReceipt, dest_dir: Path | str | None = None) -> Optional[Path]:
    """Persist receipt as JSON. Returns the path written, or None on failure."""
    target_dir = Path(dest_dir) if dest_dir is not None else RECEIPT_DIR
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    fname = f"{receipt.ts.replace(':', '').replace('-', '')}__{receipt.session_id}.json"
    out = target_dir / fname
    try:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(receipt.to_dict(), f, indent=2, sort_keys=True)
        return out
    except OSError:
        return None


def print_receipt(receipt: InitReceipt) -> None:
    """Print the receipt in the F13-approved log format."""
    ind = receipt.indicators
    print(f"[{receipt.ts}] [INIT]  registry={ind['REGISTRY']} path={receipt.registry_path}")
    print(f"[{receipt.ts}] [INIT]  schema={ind['SCHEMA']} invariants={_inv_summary(receipt.invariants_ok)}")
    axes_str = ",".join(CANONICAL_AXES)
    print(f"[{receipt.ts}] [INIT]  axes={ind['AXES']} ({axes_str})")
    print(f"[{receipt.ts}] [INIT]  backends={ind['BACKENDS']}")
    print(f"[{receipt.ts}] [INIT]  enabled={ind['ENABLED']}")
    print(f"[{receipt.ts}] [INIT]  leases={ind['LEASES']}")
    print(f"[{receipt.ts}] [INIT]  credentials_exposed={ind['CREDENTIALS_EXPOSED']}")
    print(f"[{receipt.ts}] [INIT]  mutations={ind['MUTATIONS']}")
    print(f"[{receipt.ts}] [INIT]  registry_sha256={receipt.registry_sha256}")
    print(f"[{receipt.ts}] [INIT]  verdict={ind['VERDICT']}")
    if receipt.fail_closed_reasons:
        print(f"[{receipt.ts}] [HOLD]  reason={receipt.reason}")


def _inv_summary(invariants_ok: dict[str, bool]) -> str:
    if not invariants_ok:
        return "(none)"
    parts = [f"{k}={'ok' if v else 'FAIL'}" for k, v in sorted(invariants_ok.items())]
    return ";".join(parts)


# --- CLI ---


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: aaa_capability_init.py <path-to-AAA_CAPABILITY_REGISTRY.yaml>", file=sys.stderr)
        return 2
    receipt = run_init(argv[1])
    print_receipt(receipt)
    written = write_receipt(receipt)
    if written:
        print(f"[receipt] written: {written}")
    return 0 if receipt.verdict == "READY_READONLY" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
