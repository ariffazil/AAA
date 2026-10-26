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
    # The chain is over SEAL rows only. Correction/audit annotations share the
    # ledger (appended, never edited) and carry no artifact_sha256; taking the
    # blind last row made every seal after an audit note crash with KeyError.
    # Fix 2026-10-15: skip non-seal rows when walking backwards.
    for r in reversed(rows):
        if r.get("artifact_sha256"):
            return r
    return None


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
    # A correction row is an annotation, not a link: it carries no artifact, so it
    # must not become the parent of the row that follows it. Chaining through it
    # would either break the chain or, worse, make a correction look like a seal.
    prev_artifact: str | None = None
    for row in rows:
        if not row.get("artifact_sha256"):
            notes.append(f"{row.get('edition_id') or row.get('edition')}: annotation row (kind={row.get('kind')}), not chained")
            continue
        want_prev = prev_artifact
        prev_artifact = row["artifact_sha256"]
        if row.get("chain_prev") != want_prev:
            problems.append(
                f"{row.get('edition')}: chain_prev={row.get('chain_prev')} "
                f"but predecessor is {want_prev}"
            )
        if not row.get("gates_all_pass"):
            failed = [g["gate"] for g in row.get("gates", []) if not g.get("ok")]
            problems.append(f"{row.get('edition')}: sealed with failing gate(s) {failed}")

    # A render can be superseded before delivery (re-run of the same edition).
    # Only the LAST seal row per edition can still be hashed: an earlier render's
    # bytes are overwritten by the re-render. Treat last-row-wins explicitly and
    # SAY it, rather than silently comparing the file against a dead row.
    art_rows = [(i, r) for i, r in enumerate(rows) if r.get("artifact_sha256")]
    last_for: dict[str, int] = {}
    for idx, r in art_rows:
        last_for[r.get("edition")] = idx
    for pos, (idx, row) in enumerate(art_rows):
        if last_for.get(row.get("edition")) == idx:
            continue
        nxt = art_rows[pos + 1][1] if pos + 1 < len(art_rows) else None
        if nxt is None or nxt.get("edition") != row.get("edition"):
            problems.append(
                f"{row.get('edition')}: superseded seal row is not followed by a "
                "seal of the same edition — cannot tell it apart from an edit"
            )
        else:
            notes.append(
                f"{row.get('edition')}: earlier seal {str(row['artifact_sha256'])[:16]}… "
                "superseded before delivery by a later render; its bytes are gone, "
                "not re-hashed"
            )

    # re-hash whatever is still on disk
    checked = 0
    for idx, row in art_rows:
        if last_for.get(row.get("edition")) != idx:
            continue
        rel = row.get("artifact_path")
        candidates = []
        if rel:
            candidates.append(ledger_path.parent / rel)
        candidates.append(ledger_path.parent / row["edition"] / row.get("artifact_file", ""))
        candidates.append(ledger_path.parent / row.get("artifact_file", ""))
        target = next((c for c in candidates if c.is_file()), None)
        if not target:
            # Absent is not resolved: say so instead of skipping in silence.
            notes.append(
                f"{row.get('edition')}: artifact NOT on disk — could not re-hash "
                f"({row.get('artifact_file') or rel})"
            )
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
