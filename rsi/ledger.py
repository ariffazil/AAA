#!/usr/bin/env python3
"""ledger.py — WIRE into the capability ledger that ALREADY EXISTS.

F13 directive 2026-09-15: "WIRE, jangan build. Capability ledger SUDAH ADA
(schema+probe+tests). Missing link: scar seal → ledger entry ingestion."

SOT is `/root/AAA/ops/capabilities/capability-ledger.yaml` — 3-dimensional
(implemented × reachable × governed), flock-serialized, schema-validated,
probe-tested. This module does NOT create a second registry. It:

  1. Ingests a verified capability atom into the existing ledger as an entry in
     the canonical 3-dim shape, using the same flock + surgical text edit that
     `probe-capabilities.py` uses (preserves hand formatting, no YAML round-trip).
  2. Keeps `/root/AAA/rsi/state/capability-graph.json` as a DERIVED VIEW — the
     same pattern the skill-matrix indexer already uses. If the derived file is
     deleted it can be rebuilt from the ledger; the ledger cannot be rebuilt from
     the view. Ownership follows storage.

A parallel capability registry would be DUPLICATE_SOT — the exact defect this
loop classifies. So the loop writes to the one that exists.
"""
from __future__ import annotations

import fcntl
import os
import re
from datetime import datetime, timezone

LEDGER = "/root/AAA/ops/capabilities/capability-ledger.yaml"
LOCK = "/root/AAA/ops/capabilities/capability-ledger.lock"
PROBE = "/root/AAA/ops/capabilities/probe-capabilities.py"

# Canonical vocabularies, read from the ledger's own README/schema (not invented).
IMPL_STATES = ("absent", "partial", "implemented", "retired", "vendor_candidate",
               "implemented_or_claimed", "external_institutional_api")
REACH_STATES = ("unreachable", "not_wired", "working_unprobed", "reachable", "degraded",
                "pending_production_probe", "intentionally_unreachable",
                "unknown_by_governed_probe")
AUTHORITIES = ("observe", "draft", "external_write", "financial_write", "admin_write")


class LedgerLock:
    """Exclusive writer lock — same discipline as probe-capabilities.py::LedgerLock.

    A two-writer race already happened once (2026-09-12). The loop is a second
    writer, so it takes the same lock rather than a new one.
    """

    def __enter__(self):
        os.makedirs(os.path.dirname(LOCK), exist_ok=True)
        self.fd = open(LOCK, "a+")
        fcntl.flock(self.fd, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        if getattr(self, "fd", None):
            fcntl.flock(self.fd, fcntl.LOCK_UN)
            self.fd.close()
        return False


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def ledger_capability_ids() -> list[str]:
    if not os.path.exists(LEDGER):
        return []
    return re.findall(r"^\s*- id:\s*(\S+)\s*$", open(LEDGER, encoding="utf-8").read(), re.M)


def exists(cap_id: str) -> bool:
    return cap_id in set(ledger_capability_ids())


def _slug(atom: dict) -> str:
    """A capability id in the ledger's own dot-namespace convention."""
    raw = (atom.get("target") or f"capability.{atom['pattern_type'].lower()}")
    return re.sub(r"[^a-z0-9_.]", "_", raw.lower())


def ingest(atom: dict, receipt: dict) -> dict:
    """Append a verified atom to the EXISTING ledger in its canonical shape.

    Honest field mapping — the loop does not get to claim more than it earned:

      implementation.state  = `implemented`   only if a promotion actually landed
      reachability.state    = `working_unprobed`  (no probe has run against it yet)
      governance.authority  = `observe`        the loop never claims write authority
      governance.activation_gate = `888_HOLD`  external writes stay gated

    A capability written this way is a CLAIM with a timestamp and a witness, not a
    certification. `probe-capabilities.py --capability <id>` is what turns
    reachability into evidence.
    """
    cap_id = _slug(atom)
    applied = bool(receipt.get("passed"))
    entry = {
        "id": cap_id,
        "title": cap_id.split(".")[-1].replace("_", " ").title(),
        "domain": atom.get("layer", "capability"),
        "lifecycle": "active" if applied else "partial",
        "implementation": {
            "state": "implemented" if applied else "partial",
            "evidence": [{
                "type": "rsi_atom",
                "ref": atom.get("atom_id"),
                "claim": (atom.get("claim") or "")[:200],
            }],
        },
        "reachability": {
            "state": "working_unprobed",
            "trigger": "cron: aaa-rsi-loop (7 */6 * * *)",
            "last_probe_at": None,
            "last_probe_status": "never_probed",
        },
        "governance": {
            "authority": "observe",
            "activation_gate": "888_HOLD",
        },
        "_ingested_by": "hermes-rsi-loop",
        "_ingested_at": _now(),
        "_independence": receipt.get("independence_class"),
        "_provisional": bool(receipt.get("provisional")),
    }

    with LedgerLock():
        text = open(LEDGER, encoding="utf-8").read()
        if re.search(rf"^\s*- id:\s*{re.escape(cap_id)}\s*$", text, re.M):
            return {"action": "ledger_entry_present", "capability": cap_id,
                    "applied": False,
                    "reason": "already in the ledger — the loop never rewrites an "
                              "existing entry (that is the probe's job, with evidence)"}
        block = _render(entry)
        marker = "\ncapabilities:\n"
        if marker not in text:
            return {"action": "ledger_shape_unexpected", "capability": cap_id,
                    "applied": False,
                    "reason": "no `capabilities:` key — refused rather than rewrite SOT"}
        head, _, tail = text.partition(marker)
        new_text = head + marker + tail.rstrip("\n") + "\n" + block
        tmp = LEDGER + ".rsi.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(new_text)
        os.replace(tmp, LEDGER)

    return {"action": "ledger_entry_appended", "capability": cap_id,
            "target": f"{LEDGER}#{cap_id}", "applied": True,
            "note": "entry is a claim with a witness; run probe-capabilities.py "
                    "--capability <id> to convert reachability into evidence"}


def _render(e: dict) -> str:
    ev = e["implementation"]["evidence"][0]
    return f"""
  # ── ingested by RSI loop {e['_ingested_at']} ──────────────────────────────
  - id: {e['id']}
    title: "{e['title']}"
    domain: "{e['domain']}"
    lifecycle: {e['lifecycle']}
    _ingested_by: {e['_ingested_by']}
    _independence: {e['_independence']}
    _provisional: {str(e['_provisional']).lower()}

    implementation:
      state: {e['implementation']['state']}
      evidence:
        - type: {ev['type']}
          ref: "{ev['ref']}"
          claim: "{ev['claim'].replace(chr(34), chr(39))}"

    reachability:
      state: {e['reachability']['state']}
      trigger: "{e['reachability']['trigger']}"
      last_probe_at: null
      last_probe_status: "{e['reachability']['last_probe_status']}"

    governance:
      authority: {e['governance']['authority']}
      activation_gate: {e['governance']['activation_gate']}
"""


def validate() -> dict:
    """Run the ledger's OWN validator against the ledger after ingest."""
    import subprocess
    out = subprocess.run(["/usr/bin/python3", PROBE, "--validate"],
                         capture_output=True, text=True, timeout=120)
    return {"exit": out.returncode, "stdout": (out.stdout or "").strip()[-600:],
            "stderr": (out.stderr or "").strip()[-300:]}


if __name__ == "__main__":
    print("ledger:", LEDGER)
    print("entries:", len(ledger_capability_ids()))
    print("validate:", validate())
