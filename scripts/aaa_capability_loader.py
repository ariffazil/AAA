#!/usr/bin/env python3
"""
aaa_capability_loader.py — Phase A

Parses AAA_CAPABILITY_REGISTRY.yaml into an in-memory CapabilityIndex.
Pure data transformation. No MCP backend spawn. No network. No state mutation.

Authorized by F13 directive, 2026-08-11 (SEAL_PHASE_A_ONLY).
"""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Optional

import yaml


# Canonical seven axes (binding — matches AAA_CAPABILITY_REGISTRY.yaml)
CANONICAL_AXES: tuple[str, ...] = (
    "sense",
    "know",
    "remember",
    "understand",
    "verify",
    "forge",
    "witness",
)

# Canonical capability names from the ratified architectural doctrine
DOCTRINE_CANONICAL_NAMES: tuple[str, ...] = (
    "reality.search",
    "knowledge.docs",
    "memory.recall",
    "code.navigate",
    "evidence.scan",
    "forge.repository",
    "witness.append",
)

F_RATING_VALUES: tuple[str, ...] = ("SAFE", "REVIEW", "HOLD")
SEAL_VALUES: tuple[str, ...] = ("pending", "ratifying", "sealed", "void")
TRANSPORT_VALUES: tuple[str, ...] = ("stdio", "http")


@dataclass(frozen=True)
class BackendService:
    """One (axis, capability) pair that a backend serves."""

    axis: str
    capability: str
    authority_mode: Optional[str] = None  # for cross-axis entries
    rank: Optional[int] = None


@dataclass(frozen=True)
class CapabilityBackend:
    """One backend (a single MCP server). May serve multiple capabilities."""

    name: str
    transport: Literal["stdio", "http"]
    F_rating: Literal["SAFE", "REVIEW", "HOLD"]
    seal: Literal["pending", "ratifying", "sealed", "void"]
    enabled: bool
    services: tuple[BackendService, ...] = ()
    url: Optional[str] = None
    gate: Optional[str] = None
    note: Optional[str] = None

    def serves_capability(self, capability: str) -> bool:
        return any(s.capability == capability for s in self.services)

    def is_ready(self) -> bool:
        """A backend is runtime-ready iff enabled=True AND seal is ratifying/sealed."""
        return self.enabled and self.seal in ("ratifying", "sealed")


@dataclass(frozen=True)
class CapabilityIndex:
    """Parsed, in-memory index of the capability registry."""

    version: str
    sovereign: str
    status: str
    source_path: str
    source_sha256: str
    axes: dict[str, list[str]] = field(default_factory=dict)
    backends: dict[str, CapabilityBackend] = field(default_factory=dict)
    canonical_names: set[str] = field(default_factory=set)
    enabled_count: int = 0
    catalogued_count: int = 0
    invariants_declared: dict[str, Any] = field(default_factory=dict)
    architectural_verdict: Optional[str] = None
    raw: dict[str, Any] = field(default_factory=dict)


class RegistryLoadError(Exception):
    """Raised when the registry cannot be loaded or parsed."""


def _coerce_literal(value: str, allowed: tuple[str, ...], field: str) -> str:
    """Validate that value is in allowed tuple."""
    if value not in allowed:
        raise RegistryLoadError(
            f"Field '{field}' has invalid value {value!r}. Allowed: {allowed}"
        )
    return value


def _parse_service(
    name: str,
    axis: str,
    capability: str,
    raw: dict[str, Any],
) -> BackendService:
    """Build a BackendService from a backend mapping."""
    return BackendService(
        axis=axis,
        capability=capability,
        authority_mode=raw.get("authority_mode"),
        rank=raw.get("rank"),
    )


def _parse_backend_entry(
    name: str,
    raw: dict[str, Any],
    axis: str,
    capability: str,
) -> dict[str, Any]:
    """
    Parse the shared backend fields. Returns a dict suitable for assembling
    into a CapabilityBackend after all declarations across axes are merged.
    """
    if not isinstance(raw, dict):
        raise RegistryLoadError(
            f"Backend '{name}' in {axis}.{capability} must be a mapping, got {type(raw).__name__}"
        )

    try:
        transport = _coerce_literal(
            raw["transport"], TRANSPORT_VALUES, f"backends.{name}.transport"
        )
        F_rating = _coerce_literal(
            raw["F_rating"], F_RATING_VALUES, f"backends.{name}.F_rating"
        )
    except KeyError as e:
        raise RegistryLoadError(
            f"Backend '{name}' in {axis}.{capability} missing required field {e}"
        ) from None

    # seal is optional — defaults to 'pending' if absent.
    seal = _coerce_literal(
        raw.get("seal", "pending"), SEAL_VALUES, f"backends.{name}.seal"
    )

    return {
        "transport": transport,
        "F_rating": F_rating,
        "seal": seal,
        "enabled": bool(raw.get("enabled", False)),
        "url": raw.get("url"),
        "gate": raw.get("gate"),
        "note": raw.get("note"),
        "authority_mode": raw.get("authority_mode"),
        "rank": raw.get("rank"),
    }


def _merge_backend_entry(
    existing: CapabilityBackend,
    addition: dict[str, Any],
    axis: str,
    capability: str,
) -> CapabilityBackend:
    """
    Merge a second declaration of an already-known backend.

    Cross-axis policy: transport, F_rating, seal, url, gate must match
    (a backend is one process — same transport). Note and authority_mode
    are merged into services. enabled is taken as OR (any true = true).
    """
    if existing.transport != addition["transport"]:
        raise RegistryLoadError(
            f"Backend '{name}' declared with conflicting transports: "
            f"{existing.transport!r} vs {addition['transport']!r}"
        )
    if existing.F_rating != addition["F_rating"]:
        raise RegistryLoadError(
            f"Backend '{name}' declared with conflicting F_ratings: "
            f"{existing.F_rating!r} vs {addition['F_rating']!r}"
        )
    if existing.seal != addition["seal"]:
        raise RegistryLoadError(
            f"Backend '{name}' declared with conflicting seals: "
            f"{existing.seal!r} vs {addition['seal']!r}"
        )
    # Merge services
    new_service = _parse_service(name, axis, capability, addition)
    merged_services = existing.services + (new_service,)
    # enabled is OR
    merged_enabled = existing.enabled or addition["enabled"]
    # url: prefer non-None
    merged_url = existing.url if existing.url is not None else addition["url"]
    # gate: prefer non-None
    merged_gate = existing.gate if existing.gate is not None else addition["gate"]
    # note: concatenate if both present
    notes = []
    if existing.note:
        notes.append(existing.note)
    if addition["note"]:
        notes.append(addition["note"])
    merged_note = " | ".join(notes) if notes else None

    return CapabilityBackend(
        name=name,
        transport=existing.transport,
        F_rating=existing.F_rating,
        seal=existing.seal,
        enabled=merged_enabled,
        services=merged_services,
        url=merged_url,
        gate=merged_gate,
        note=merged_note,
    )


def _sha256(path: Path) -> str:
    """Compute SHA-256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_registry(path: Path | str) -> CapabilityIndex:
    """
    Load and parse AAA_CAPABILITY_REGISTRY.yaml into a CapabilityIndex.

    Does NOT spawn any MCP backend. Does NOT touch harness configs.
    Reads the file once and returns an immutable index.

    Same backend name may appear under multiple axes/capabilities — those
    declarations are merged into one CapabilityBackend with multiple services.

    Raises RegistryLoadError on malformed/contradictory state.
    """
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise RegistryLoadError(f"Registry file not found: {p}")
    if not p.is_file():
        raise RegistryLoadError(f"Registry path is not a regular file: {p}")

    sha = _sha256(p)

    try:
        with open(p, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise RegistryLoadError(f"YAML parse error in {p}: {e}") from e

    if raw is None:
        raise RegistryLoadError(f"Registry file is empty: {p}")
    if not isinstance(raw, dict):
        raise RegistryLoadError(
            f"Registry root must be a mapping, got {type(raw).__name__}"
        )

    for field in ("version", "sovereign", "status", "axes"):
        if field not in raw:
            raise RegistryLoadError(f"Registry missing required top-level field '{field}'")

    architectural_verdict = None
    if isinstance(raw.get("architectural_ratification"), dict):
        architectural_verdict = raw["architectural_ratification"].get("verdict")

    axes_in = raw["axes"]
    if not isinstance(axes_in, dict):
        raise RegistryLoadError("'axes' must be a mapping")

    axes: dict[str, list[str]] = {}
    backends: dict[str, CapabilityBackend] = {}
    canonical_names: set[str] = set()

    for axis_name, axis_data in axes_in.items():
        if axis_name not in CANONICAL_AXES:
            raise RegistryLoadError(
                f"Unknown axis '{axis_name}'. Allowed axes: {list(CANONICAL_AXES)}"
            )
        if not isinstance(axis_data, dict):
            raise RegistryLoadError(f"Axis '{axis_name}' must be a mapping")
        caps = axis_data.get("canonical_capabilities")
        if not isinstance(caps, dict) or not caps:
            raise RegistryLoadError(
                f"Axis '{axis_name}' missing or empty 'canonical_capabilities'"
            )

        axes[axis_name] = []
        for cap_name, cap_data in caps.items():
            if not isinstance(cap_data, dict):
                raise RegistryLoadError(
                    f"Capability '{cap_name}' in axis '{axis_name}' must be a mapping"
                )
            cap_backends = cap_data.get("backends")
            if not isinstance(cap_backends, dict) or not cap_backends:
                raise RegistryLoadError(
                    f"Capability '{cap_name}' in axis '{axis_name}' missing 'backends'"
                )
            axes[axis_name].append(cap_name)
            canonical_names.add(cap_name)
            for backend_name, backend_raw in cap_backends.items():
                parsed = _parse_backend_entry(
                    backend_name, backend_raw, axis_name, cap_name
                )
                service = _parse_service(backend_name, axis_name, cap_name, parsed)
                if backend_name in backends:
                    # Cross-axis: merge
                    merged = _merge_backend_entry(
                        backends[backend_name], parsed, axis_name, cap_name
                    )
                    backends[backend_name] = merged
                else:
                    backends[backend_name] = CapabilityBackend(
                        name=backend_name,
                        transport=parsed["transport"],  # type: ignore[arg-type]
                        F_rating=parsed["F_rating"],  # type: ignore[arg-type]
                        seal=parsed["seal"],  # type: ignore[arg-type]
                        enabled=parsed["enabled"],
                        services=(service,),
                        url=parsed["url"],
                        gate=parsed["gate"],
                        note=parsed["note"],
                    )

    enabled_count = sum(1 for b in backends.values() if b.enabled)
    invariants_declared = raw.get("invariants", {})

    return CapabilityIndex(
        version=str(raw["version"]),
        sovereign=str(raw["sovereign"]),
        status=str(raw["status"]),
        source_path=str(p),
        source_sha256=sha,
        axes=axes,
        backends=backends,
        canonical_names=canonical_names,
        enabled_count=enabled_count,
        catalogued_count=len(backends),
        invariants_declared=invariants_declared if isinstance(invariants_declared, dict) else {},
        architectural_verdict=architectural_verdict,
        raw=raw,
    )


# --- CLI ---

def _print_summary(index: CapabilityIndex) -> None:
    print(f"REGISTRY: loaded")
    print(f"  path:     {index.source_path}")
    print(f"  sha256:   {index.source_sha256}")
    print(f"  version:  {index.version}")
    print(f"  status:   {index.status}")
    print(f"  verdict:  {index.architectural_verdict or '(none)'}")
    print(f"  axes:     {len(index.axes)} recognized")
    print(f"  canonical capabilities: {len(index.canonical_names)}")
    print(f"  backends: {index.catalogued_count} catalogued")
    print(f"  enabled:  {index.enabled_count}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: aaa_capability_loader.py <path-to-AAA_CAPABILITY_REGISTRY.yaml>", file=sys.stderr)
        return 2
    try:
        index = load_registry(argv[1])
    except RegistryLoadError as e:
        print(f"REGISTRY: load_failed", file=sys.stderr)
        print(f"  reason: {e}", file=sys.stderr)
        return 1
    _print_summary(index)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
