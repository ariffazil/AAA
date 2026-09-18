#!/usr/bin/env python3
"""docforge.seal — provenance for a rendered artifact.

THE CHICKEN-AND-EGG, HANDLED RATHER THAN HIDDEN
  A file cannot contain its own hash. Any tool that prints "SHA256: ..." inside
  the PDF it is hashing is printing a number that proves nothing, because the
  bytes it describes are the bytes that contain it.

  So the seal is split in two, and each half answers a different question:

      content_sha256   over the canonical SOURCE, computed BEFORE substitution
                       and therefore embeddable in the document. Proves the
                       words were not edited after the seal was taken.
      artifact_sha256  over the rendered PDF BYTES, computed AFTER render, so it
                       can never live inside the file it describes. Delivered in
                       a sidecar in `sha256sum -c` format.

  The document says on its own face that the artifact hash lives outside it.
  Naming the gap is the point; a seal that oversells what it proves is worse
  than no seal, because it transfers trust it has not earned.

WHAT A SEAL DOES NOT PROVE
  Integrity and accuracy are separate verdicts. A hash proves the document is
  intact. It never proves the document is true. Both are carried as separate
  fields, and the chain records which gates the artifact actually passed.

WHAT IS DELIBERATELY NOT CLAIMED
  C2PA / Content Credentials would put signed provenance inside the asset with
  an X.509 chain to a trust list. That needs a certificate authority and a
  signing identity, neither of which this lane holds. The field is present and
  reads `not_signed` rather than being silently omitted, so a reader can see
  the difference between "unsigned" and "no provenance mechanism at all".
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

LEDGER_NAME = "docforge-ledger.jsonl"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_sidecar(pdf: Path, artifact_sha: str, sidecar: Path) -> Path:
    sidecar.write_text(f"{artifact_sha}  {pdf.name}\n")
    return sidecar


def check_sidecar(sidecar: Path) -> tuple[bool, str]:
    r = subprocess.run(["sha256sum", "-c", sidecar.name],
                       cwd=sidecar.parent, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout or r.stderr).strip()


def chain_tail(ledger: Path) -> dict | None:
    if not ledger.exists():
        return None
    rows = [json.loads(l) for l in ledger.read_text().splitlines() if l.strip()]
    return rows[-1] if rows else None


def seal(*, edition: str, edition_date: str, source_text: str, pdf: Path,
         run_dir: Path, gates: list, engine: str, engine_version: str,
         profile: str, template: str, extra: dict | None = None) -> dict:
    """Compute both hashes, write sidecar + per-run ledger + append to the chain."""
    content_sha = sha256_text(source_text)
    artifact_sha = sha256_file(pdf)

    sidecar = run_dir / f"{edition}.sha256"
    write_sidecar(pdf, artifact_sha, sidecar)
    ok, msg = check_sidecar(sidecar)

    ledger_path = run_dir.parent / LEDGER_NAME
    prev = chain_tail(ledger_path)

    # Record WHERE the artifact is, relative to the ledger. The first version
    # made verify_chain guess `ledger_dir/<edition>/<file>`, which silently
    # found nothing whenever the directory name and the edition label differed
    # in case — a chain that cannot locate its own artifacts cannot re-check
    # them, and re-checking them is the whole difference between a log and
    # evidence.
    try:
        artifact_path = str(pdf.resolve().relative_to(ledger_path.parent.resolve()))
    except ValueError:
        artifact_path = str(pdf.resolve())

    row = {
        "edition": edition,
        "date": edition_date,
        "built_at": utc_now(),
        "engine": engine,
        "engine_version": engine_version,
        "template": template,
        "profile": profile,
        "content_sha256": content_sha,
        "artifact_sha256": artifact_sha,
        "artifact_bytes": pdf.stat().st_size,
        "artifact_file": pdf.name,
        "artifact_path": artifact_path,
        "sidecar": sidecar.name,
        "sidecar_verified": ok,
        "gates": [{"gate": g.gate, "ok": bool(g.ok), "detail": g.detail} for g in gates],
        "gates_all_pass": all(g.ok for g in gates),
        "chain_prev": prev["artifact_sha256"] if prev else None,
        "chain_prev_edition": prev["edition"] if prev else None,
        "signature": "not_signed",
        "signature_note": ("no C2PA/X.509 signing identity on this lane; "
                           "hashes only. Integrity is proven, authorship is not."),
        "seal_class": ("lane-level integrity seal — NOT an F13 seal and not a "
                       "canonical record"),
    }
    if extra:
        row.update(extra)

    (run_dir / f"{edition}.ledger.json").write_text(json.dumps(row, indent=2) + "\n")
    with ledger_path.open("a") as f:
        f.write(json.dumps(row) + "\n")
    return row


def verify_chain(ledger_path: Path) -> tuple[bool, list[str]]:
    """Walk the chain: linkage intact, and every artifact still hashes to its row.

    A chain that only records hashes is a log. A chain that RE-CHECKS them is
    evidence — it can tell you that a delivered file has been altered since.
    """
    if not ledger_path.exists():
        return False, [f"no ledger at {ledger_path}"]
    rows = [json.loads(l) for l in ledger_path.read_text().splitlines() if l.strip()]
    if not rows:
        return False, ["ledger exists but is empty"]

    problems: list[str] = []
    notes: list[str] = []
    for i, row in enumerate(rows):
        want_prev = rows[i - 1]["artifact_sha256"] if i else None
        if row.get("chain_prev") != want_prev:
            problems.append(
                f"{row.get('edition')}: chain_prev={row.get('chain_prev')} "
                f"but predecessor is {want_prev}"
            )
        if not row.get("gates_all_pass"):
            failed = [g["gate"] for g in row.get("gates", []) if not g.get("ok")]
            problems.append(f"{row.get('edition')}: sealed with failing gate(s) {failed}")

    # re-hash whatever is still on disk
    checked = 0
    for row in rows:
        rel = row.get("artifact_path")
        candidates = []
        if rel:
            candidates.append(ledger_path.parent / rel)
        candidates.append(ledger_path.parent / row["edition"] / row.get("artifact_file", ""))
        candidates.append(ledger_path.parent / row.get("artifact_file", ""))
        target = next((c for c in candidates if c.is_file()), None)
        if not target:
            continue
        checked += 1
        got = sha256_file(target)
        if got != row["artifact_sha256"]:
            problems.append(
                f"{row['edition']}: {target.name} hashes {got[:16]}… but the "
                f"ledger recorded {row['artifact_sha256'][:16]}… — file altered "
                "after sealing"
            )
    notes.append(f"{len(rows)} edition(s) in chain, {checked} artifact(s) re-hashed on disk")
    return (not problems), problems + notes
