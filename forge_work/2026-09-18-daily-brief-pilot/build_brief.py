#!/usr/bin/env python3
"""Build + hash-seal the Hermes Executive Brief pilot.

WHY TWO HASHES (the chicken-and-egg, handled honestly)
  A file cannot contain its own hash. So:
    content_sha256  = SHA-256 over the canonical source (the template with its
                      placeholders still literal). Computed FIRST, then injected
                      into the rendered document. This is what proves the words
                      were not edited after sealing.
    artifact_sha256 = SHA-256 over the rendered PDF bytes. Computed AFTER render.
                      It CANNOT appear inside the PDF it describes, so it is
                      delivered in the sidecar. The PDF says so, rather than
                      printing a hash that proves nothing.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
TEMPLATE = RUN / "brief.template.html"
HTML = RUN / "brief.html"
PDF = RUN / "Hermes-Brief-PILOT-001-2026-09-18.pdf"
SIDECAR = RUN / "PILOT-001.sha256"
LEDGER = RUN / "PILOT-001.ledger.json"

EDITION = "PILOT-001"
EDITION_DATE = "2026-09-18"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not TEMPLATE.is_file():
        print(f"missing template: {TEMPLATE}", file=sys.stderr)
        return 2

    src = TEMPLATE.read_text()
    content_sha = hashlib.sha256(src.encode("utf-8")).hexdigest()
    print(f"content_sha256  {content_sha}")

    out = src.replace("{{CONTENT_HASH}}", content_sha)
    out = out.replace(
        "{{ARTIFACT_HASH}}",
        "delivered alongside in PILOT-001.sha256 &mdash; a file cannot embed its own hash",
    )
    HTML.write_text(out)

    r = subprocess.run(
        ["weasyprint", str(HTML), str(PDF)],
        capture_output=True, text=True, timeout=300,
    )
    if r.returncode != 0:
        print("weasyprint failed:\n" + (r.stderr or "")[:2000], file=sys.stderr)
        return 1

    artifact_sha = sha256_file(PDF)
    print(f"artifact_sha256 {artifact_sha}")

    SIDECAR.write_text(f"{artifact_sha}  {PDF.name}\n")

    prev = None
    ledger_path = RUN.parent / "edition-ledger.jsonl"
    if ledger_path.is_file():
        rows = [json.loads(l) for l in ledger_path.read_text().splitlines() if l.strip()]
        if rows:
            prev = rows[-1].get("artifact_sha256")
    row = {
        "edition": EDITION,
        "date": EDITION_DATE,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "content_sha256": content_sha,
        "artifact_sha256": artifact_sha,
        "chain_prev": prev,
        "seal_authority": "FI Hermes (KVM8) — lane-level integrity seal, NOT an F13 seal",
    }
    LEDGER.write_text(json.dumps(row, indent=2) + "\n")
    with ledger_path.open("a") as f:
        f.write(json.dumps(row) + "\n")
    print(f"chain_prev      {prev}")

    chk = subprocess.run(["sha256sum", "-c", SIDECAR.name],
                         cwd=RUN, capture_output=True, text=True)
    print("sidecar check:  " + chk.stdout.strip())
    return 0 if chk.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
