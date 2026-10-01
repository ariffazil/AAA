#!/usr/bin/env python3
"""BL12 keyspace contract tests (F13 order 2026-10-01, trc-20261001-fi003-keyspace-repair).

Before this repair, fed_router's penalty lookup was structurally incapable of firing: it
compared the producer's raw keys ('333-agi') against the caller's raw ids ('333-AGI'), in
two disjoint namespaces, with an exact dict lookup. Silence read as health.

These tests prove BOTH directions, so the fix is not "make it never fire":
  A. when a real actor carries REDUCE_WEIGHT, every legitimate spelling of that actor pays
  B. an UNATTRIBUTED row can never be reached by any caller, including the literal string
  C. failures fall closed (0.0), never penalising on bad data
"""
import importlib
import json
import os
import sys
import tempfile

sys.path.insert(0, "/root/AAA/scripts")
import fed_router as m  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + ("" if cond else f"  -> {detail}"))
    if not cond:
        FAILS.append(name)


def arm(per_actor):
    """Point the loader at a synthetic calibration file and force a reload."""
    d = tempfile.mkdtemp(prefix="bl12-")
    p = os.path.join(d, "calibration.json")
    with open(p, "w") as fh:
        json.dump({"schema": "bl02.per_actor.v3", "per_actor": per_actor}, fh)
    m._CALIB_FILE = p
    m._CALIB_CACHE.update({"t": 0.0, "idx": {}, "rows": 0, "matched": 0,
                           "penalized": 0, "unmatched": 0, "error": None})


RED = {"routable": True, "routing_keys": ["333-agi"], "routing_advisory_bl12": "REDUCE_WEIGHT@bias=0.41"}

print("A. a real REDUCE_WEIGHT actor is reached from every legitimate spelling")
arm({"333-agi": dict(RED)})
for caller in ("333-agi", "333-AGI", "333_AGI", "333-AGI/FI-003", "333-agi/dynamic-gate", " 333-AGI "):
    check(f"caller {caller!r} -> 15.0 penalty", m._bl12_agent_penalty(caller) == 15.0,
          str(m._CALIB_CACHE))

print("\nB. an UNATTRIBUTED row is unreachable by construction")
arm({"UNATTRIBUTED": {"routable": False, "routing_keys": [],
                      "routing_advisory_bl12": "REDUCE_WEIGHT@bias=0.99"}})
for caller in ("UNATTRIBUTED", "unattributed", "arif", "http", "333-AGI"):
    check(f"caller {caller!r} cannot be penalised", m._bl12_agent_penalty(caller) == 0.0,
          str(m._CALIB_CACHE))
check("index is empty, so state reads VOCABULARY_GAP not ARMED",
      m._CALIB_CACHE["rows"] == 0, str(m._CALIB_CACHE["rows"]))

print("\nC. a penalised actor does not leak onto strangers, and the default 'http' is unmatched")
arm({"a-forge": dict(RED, routing_keys=["a-forge"]), "qwen-code": dict(RED, routing_keys=["qwen-code"])})
check("a-forge penalised", m._bl12_agent_penalty("A-FORGE") == 15.0)
check("qwen-code penalised", m._bl12_agent_penalty("QWEN-Code") == 15.0)
check("grok-build (no row) NOT penalised", m._bl12_agent_penalty("grok-build") == 0.0)
check("router default 'http' NOT penalised", m._bl12_agent_penalty("http") == 0.0)
check("unmatched lookups are counted, not hidden", m._CALIB_CACHE["unmatched"] >= 2,
      str(m._CALIB_CACHE))

print("\nD. non-penalty advisories cost nothing")
arm({"hermes-asi": {"routable": True, "routing_keys": ["hermes-asi"],
                    "routing_advisory_bl12": "NOMINAL_INSUFFICIENT_CONFIDENCE"}})
check("NOMINAL_* advisory -> 0.0", m._bl12_agent_penalty("hermes-asi") == 0.0)
check("but it still counts as a vocabulary MATCH", m._CALIB_CACHE["matched"] == 1,
      str(m._CALIB_CACHE))

print("\nE. fail-closed on broken or absent data")
m._CALIB_FILE = "/nonexistent/calibration.json"
m._CALIB_CACHE.update({"t": 0.0, "idx": {"x": "REDUCE_WEIGHT"}, "error": None})
check("missing file yields 0.0, never a stale penalty", m._bl12_agent_penalty("x") == 0.0,
      str(m._CALIB_CACHE))
check("load error recorded visibly", m._CALIB_CACHE["error"] is not None, str(m._CALIB_CACHE["error"]))

d2 = tempfile.mkdtemp()
p2 = os.path.join(d2, "bad.json")
open(p2, "w").write("{not json")
m._CALIB_FILE = p2
m._CALIB_CACHE.update({"t": 0.0, "idx": {"x": "REDUCE_WEIGHT"}})
check("corrupt file yields 0.0 and records error", m._bl12_agent_penalty("x") == 0.0,
      str(m._CALIB_CACHE["error"]))

print("\nF. backward compatibility with a pre-v3 file (no routable field at all)")
arm({"legacy-actor": {"routing_advisory_bl12": "REDUCE_WEIGHT@bias=0.3"}})
check("v2-era row still reachable (routable defaults True)",
      m._bl12_agent_penalty("LEGACY-ACTOR") == 15.0, str(m._CALIB_CACHE))

print("\n" + ("ALL BL12 KEYSPACE TESTS PASSED" if not FAILS else f"FAILURES: {FAILS}"))
sys.exit(1 if FAILS else 0)
