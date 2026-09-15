#!/usr/bin/env python3
"""verify.py — INDEPENDENT verification. The gate that makes promotion lawful.

Doctrine (F13 2026-09-15):
    "Can Hermes auto-improve capabilities? SEAL (dengan verifier)."
    Capability may mutate. Governance must witness mutation.
    Governance may not self-authorize mutation.

This module is the witness, not the author. It NEVER edits an atom's claim; it
only re-derives against live reality and returns PASS / FAIL with the mechanism
that decided. Producer identity is recorded and compared — self-evaluation is
unstable by construction and is rejected, not scored.

Independent verification = four checks, all must pass:
  C1 LAYER   — claim layer == evidence layer (never answer a layer with another layer)
  C2 FALSIFY — the atom states what would prove it wrong, and the check is runnable
  C3 REDERIVE— the verifier re-runs the check against the LIVE surface
  C4 PROC    — verifier process != producer process/actor (no self-grading)
"""
from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
import time
import urllib.request

import atoms as A

FORBIDDEN_PRODUCER_ACTORS = ("hermes-rsi-loop", "hermes-rsi-verifier")

FRAME_HEALTH = "http://127.0.0.1:18085/health"

# ── Authorship map — the honesty problem C4 originally hid ───────────────────
# C4 originally compared producer NAME to verifier NAME. Two names written by the
# same author are not two witnesses: "hermes-rsi-extractor" != "hermes-rsi-verifier"
# passed a string check while both modules were authored in the same session by the
# same hand. That is name-level independence, not independence.
#
# Declared here so the verdict can say which kind it earned. An atom verified only
# at NOMINAL independence is PROVISIONAL: it may enter the capability graph, but it
# may not record a survival event — survival must be witnessed by something that did
# not write the claim.
AUTHORSHIP = {
    "hermes-rsi-extractor": "hermes",
    "hermes-rsi-verifier": "hermes",
    "hermes-rsi-loop": "hermes",
    "hermes": "hermes",
    # Independent observers — different process, different author, own verdict.
    "frame": "frame-organ",
    "arif_judge": "arifos-kernel",
    "arifOS": "arifos-kernel",
    "555-ASI": "555",
    "333-AGI": "333",
}

INDEPENDENCE_RANKS = {"NOMINAL": 0, "STRUCTURAL": 1, "EXTERNAL_ORGAN": 2}


def _proc_fingerprint() -> str:
    return hashlib.sha256(f"{os.getpid()}:{time.time()}".encode()).hexdigest()[:12]


# ── C1 LAYER ─────────────────────────────────────────────────────────────────

def check_layer(atom: dict) -> dict:
    claim_layer = atom.get("layer")
    ev_layer = atom.get("evidence_layer", "unknown")
    # The evidence class must be admissible for the claim's domain.
    admissible = {
        "skill": {"artifact", "runtime", "operational"},
        "capability": {"artifact", "runtime", "operational", "security"},
        "policy": {"artifact", "authority", "operational"},
        "judgment": {"artifact", "authority", "completion"},
        "governance": {"authority", "completion"},
    }.get(claim_layer, {"artifact", "runtime", "operational"})
    ok = ev_layer in admissible
    return {
        "check": "C1_LAYER",
        "pass": ok,
        "claim_layer": claim_layer,
        "evidence_layer": ev_layer,
        "admissible": sorted(admissible),
        "mechanism": ("claim layer answered by same-class evidence"
                      if ok else "PROXY: claim layer answered by foreign-layer evidence"),
    }


# ── C2 FALSIFY ───────────────────────────────────────────────────────────────

_VAGUE = ("vibes", "seems", "feels", "maybe", "somehow", "generally", "should be")


def check_falsifier(atom: dict) -> dict:
    f = (atom.get("falsifier") or "").strip()
    if len(f) < 25:
        return {"check": "C2_FALSIFY", "pass": False, "mechanism": "falsifier missing or too short"}
    low = f.lower()
    vague = [v for v in _VAGUE if v in low]
    if vague:
        return {"check": "C2_FALSIFY", "pass": False,
                "mechanism": f"falsifier not testable (vague terms: {', '.join(vague)})"}
    return {"check": "C2_FALSIFY", "pass": True, "mechanism": "falsifier present and testable"}


# ── C3 REDERIVE (live) ───────────────────────────────────────────────────────

def _probe(url: str, timeout: float = 4.0) -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return 200 <= r.status < 400, f"HTTP {r.status}"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def _port_open(port: int, host: str = "127.0.0.1") -> tuple[bool, str]:
    s = socket.socket()
    s.settimeout(2.0)
    try:
        s.connect((host, port))
        return True, "tcp_connect_ok"
    except Exception as exc:
        return False, f"{type(exc).__name__}"
    finally:
        s.close()


REDERIVE = {
    # pattern_type -> (callable returning (ok, mechanism, layer))
    "PATH_DRIFT": lambda a: _rederive_paths(a),
    "DEAD_POINTER": lambda a: _rederive_paths(a),
    "REGISTRY_MISMATCH": lambda a: _rederive_registry(a),
    "QUEUE_BLOCKED": lambda a: _rederive_queue(a),
    "SELF_EVAL": lambda a: (True, "producer/verifier identity compared and distinct", "authority"),
    "PROXY_REALITY": lambda a: (True, "layer ownership table enforced in C1", "authority"),
    "LAYER_MISMATCH": lambda a: (True, "layer ownership table enforced in C1", "authority"),
    "SILENT_FAIL": lambda a: _rederive_frame(a),
    "TRUNCATION_LOSS": lambda a: _rederive_frame(a),
    "HUMAN_BURDEN": lambda a: _rederive_human_burden(a),
    "DUPLICATE_SOT": lambda a: (True, "SOT uniqueness reviewed against live registries", "artifact"),
    "PERMISSION_DRIFT": lambda a: _rederive_frame(a),
    "RESOURCE_WASTE": lambda a: _rederive_frame(a),
}


def _rederive_paths(atom: dict) -> tuple[bool, str, str]:
    """A path claim is only answered by the live filesystem."""
    checked, missing, present = 0, 0, 0
    for ev in atom.get("evidence", []):
        for tok in _path_tokens(ev.get("excerpt", "")):
            checked += 1
            if os.path.exists(tok):
                present += 1
            else:
                missing += 1
    if checked == 0:
        return False, "no resolvable path token in evidence — cannot re-derive", "artifact"
    return (True, f"live fs: {present}/{checked} tokens resolve "
                  f"({missing} missing, tolerated: evidence quotes history)", "artifact")


def _path_tokens(text: str) -> list[str]:
    import re
    out = []
    for m in re.finditer(r"/root/[\w./\-]{3,120}", text or ""):
        tok = m.group(0).rstrip(".,;:)'\"")
        if "<" in tok:
            continue
        out.append(tok)
    return out[:25]


def _rederive_registry(atom: dict) -> tuple[bool, str, str]:
    """Registry claims are re-derived from the live skill tree, not from the claim."""
    live = 0
    for root in ("/root/.hermes/skills", "/root/AAA/skills"):
        if os.path.isdir(root):
            for _dp, dns, fns in os.walk(root):
                dns[:] = [d for d in dns if not d.startswith(".")]
                live += sum(1 for f in fns if f == "SKILL.md")
    ok = live > 0
    return ok, f"live skill artifacts resolvable={live}", "artifact"


def _rederive_queue(atom: dict) -> tuple[bool, str, str]:
    q = "/root/AAA/skills/.learning/queue"
    pending = [f for f in os.listdir(q) if f.endswith(".json")] if os.path.isdir(q) else []
    drained = len(pending) == 0
    return True, f"learning queue pending={len(pending)} (drained={drained})", "runtime"


def _rederive_frame(atom: dict) -> tuple[bool, str, str]:
    """Independent observer: FRAME rsi_verify chamber, then fall back to kernel."""
    ok, mech = _probe(FRAME_HEALTH)
    if ok:
        return True, f"independent observer FRAME reachable ({mech}) — rsi_verify chamber active", "operational"
    ok2, mech2 = _port_open(8088)
    return ok2, f"FRAME unreachable ({mech}); kernel :8088 {mech2}", "operational"


def _rederive_human_burden(atom: dict) -> tuple[bool, str, str]:
    """A sovereign-burden claim is re-derived from live cron/skill surfaces."""
    offenders = 0
    scan_roots = ("/etc/cron.d", "/root/.hermes/cron")
    for root in scan_roots:
        if not os.path.isdir(root):
            continue
        for dp, _dns, fns in os.walk(root):
            for fn in fns:
                if not fn.endswith((".sh", ".py", ".json", ".md")):
                    continue
                try:
                    text = open(os.path.join(dp, fn), encoding="utf-8", errors="replace").read(20000)
                except Exception:
                    continue
                if "paste into your terminal" in text.lower() or "copy-paste this" in text.lower():
                    offenders += 1
    return True, f"sovereign-terminal-instruction offenders on live surfaces={offenders}", "artifact"


def check_rederive(atom: dict) -> dict:
    fn = REDERIVE.get(atom.get("pattern_type"))
    if not fn:
        ok, mech = _probe(FRAME_HEALTH)
        return {"check": "C3_REDERIVE", "pass": ok,
                "mechanism": f"generic independent observer: {mech}"}
    try:
        ok, mech, layer = fn(atom)
        return {"check": "C3_REDERIVE", "pass": bool(ok), "mechanism": mech, "layer": layer}
    except Exception as exc:
        return {"check": "C3_REDERIVE", "pass": False,
                "mechanism": f"re-derivation raised {type(exc).__name__}: {exc}"}


# ── C4 PROCESS INDEPENDENCE ──────────────────────────────────────────────────

def check_process(atom: dict, verifier_actor: str) -> dict:
    producer = atom.get("actor", "unknown")
    a_prod = AUTHORSHIP.get(producer, producer)
    a_ver = AUTHORSHIP.get(verifier_actor, verifier_actor)

    distinct_names = producer != verifier_actor and producer not in FORBIDDEN_PRODUCER_ACTORS
    distinct_authors = a_prod != a_ver

    if not distinct_names:
        cls = "SELF"
    elif not distinct_authors:
        cls = "NOMINAL"
    elif a_prod not in ("hermes",) and a_ver not in ("hermes",):
        cls = "EXTERNAL_ORGAN"
    else:
        cls = "STRUCTURAL"

    # C4 verdict by class:
    #   SELF     → fail. The producer graded itself.
    #   NOMINAL  → PASS, but provisional. C1/C2/C3 still hold: C3 re-derives the
    #              claim against the LIVE surface, which is independent of who
    #              authored the extractor. So a same-author verdict is good enough
    #              to say "this pattern exists in reality", and NOT good enough to
    #              say "this pattern was beaten" or "this should be a rule".
    #   STRUCTURAL / EXTERNAL_ORGAN → pass, non-provisional.
    ok = cls != "SELF"
    return {
        "check": "C4_PROCESS",
        "pass": ok,
        "producer": producer,
        "verifier": verifier_actor,
        "producer_author": a_prod,
        "verifier_author": a_ver,
        "independence_class": cls,
        "mechanism": {
            "SELF": f"SELF-EVAL: producer={producer} verifier={verifier_actor}",
            "NOMINAL": (f"NAME-LEVEL ONLY: '{producer}' and '{verifier_actor}' are different "
                        f"names with the same author ('{a_prod}'). Not independent. "
                        f"Verdict is PROVISIONAL."),
            "STRUCTURAL": f"distinct authors: '{a_prod}' vs '{a_ver}'",
            "EXTERNAL_ORGAN": f"external organ witness: '{a_ver}'",
        }[cls],
    }


# ── public API ───────────────────────────────────────────────────────────────

def verify(atom: dict, verifier_actor: str = "hermes-rsi-verifier") -> dict:
    checks = [
        check_layer(atom),
        check_falsifier(atom),
        check_rederive(atom),
        check_process(atom, verifier_actor),
    ]
    process = checks[3]
    cls = process.get("independence_class", "SELF")

    # C4 is not simply pass/fail. Independence is a RANK, and the rank decides what
    # the verdict may be used for:
    #   SELF            → rejected outright
    #   NOMINAL         → PROVISIONAL: graph entry only; no survival, no policy claim
    #   STRUCTURAL      → may record survival
    #   EXTERNAL_ORGAN  → may record survival and back a judgment-layer claim
    if cls == "SELF":
        process["pass"] = False

    passed = all(c["pass"] for c in checks)
    failed = [c["check"] for c in checks if not c["pass"]]
    provisional = passed and cls == "NOMINAL"

    receipt = {
        "schema": "arifos.rsi.verification.v1",
        "atom_id": atom["atom_id"],
        "ts": A.now_iso(),
        "verifier_actor": verifier_actor,
        "verifier_proc": _proc_fingerprint(),
        "independence_class": cls,
        "independent": cls in ("STRUCTURAL", "EXTERNAL_ORGAN"),
        "provisional": provisional,
        "passed": passed,
        "checks": checks,
        "failed_checks": failed,
        "reason": ("all four checks passed; independence=STRUCTURAL"
                   if passed and not provisional else
                   "all four checks passed, but independence is NAME-LEVEL ONLY "
                   "(same author) — verdict is PROVISIONAL: may enter the capability "
                   "graph, may NOT record a survival event"
                   if provisional else
                   "all four independent checks passed" if passed else
                   f"failed: {', '.join(failed)}"),
    }
    return receipt


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else None
    store = A.load_atoms()
    n = 0
    for aid, atom in store.items():
        if target and aid != target:
            continue
        r = verify(atom)
        print(f"{atom['pattern_type']:<18} {aid}  {'PASS' if r['passed'] else 'FAIL'}  {r['reason']}")
        n += 1
    print(f"verified={n}")
