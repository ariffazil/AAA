#!/usr/bin/env python3
"""reality_graph_projection.py — Map existing federation records → RealityAssertions.

The Reality Graph substrate already exists (reality_graph.py). What's missing is the JOIN:
how do existing records become assertions?

This module maps the federation's actual data shapes into RealityAssertions.
Read-only (OBSERVE) — produces a JSON dump of what assertions would be created.

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reality_graph import (
    RealityAssertion, RealityEdge, RealityGraph,
    observation,
    EDGE_ABOUT, EDGE_PRECEDES, EDGE_CONTRADICTS, EDGE_SUPERSEDES,
    EPISTEMIC_OBSERVATION, EPISTEMIC_DERIVATION,
)


def project_arifos_health() -> list[RealityAssertion]:
    """One assertion per attribute in the arifOS /health response."""
    assertions = []
    try:
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:8088/health", timeout=3) as r:
            d = json.loads(r.read())
    except Exception as e:
        return [observation(
            subject="arifOS-runtime",
            predicate="reachable",
            object="false",
            actor_id="FI-008",
            source_refs=("http://127.0.0.1:8088/health",),
            evidence_refs=(f"exception: {e}",),
            confidence=0.95,
        )]

    sr = d.get("software_release", {})
    ts = datetime.now(timezone.utc).isoformat()

    # Status
    assertions.append(observation(
        subject="arifOS-runtime", predicate="status", object=str(d.get("status", "?")),
        actor_id="arif_init",
        source_refs=("curl http://127.0.0.1:8088/health",),
        evidence_refs=(f"deployment_drift_status={d.get('deployment_drift_status')}",),
        observed_at=ts,
    ))

    # Commit trio
    for key in ["source_commit", "built_commit", "deployed_commit"]:
        v = sr.get(key, "")
        if v:
            assertions.append(observation(
                subject="arifOS-runtime", predicate=key, object=str(v[:12]),
                actor_id="arif_init",
                source_refs=("curl http://127.0.0.1:8088/health",),
                evidence_refs=(f"software_release.{key}={v}",),
                observed_at=ts,
            ))

    # Drift
    drift = sr.get("drift")
    if drift is not None:
        assertions.append(observation(
            subject="arifOS-runtime", predicate="drift", object=str(drift).lower(),
            actor_id="arif_init",
            source_refs=("curl http://127.0.0.1:8088/health",),
            evidence_refs=(f"software_release.drift={drift}",),
            observed_at=ts,
        ))

    return assertions


def project_git_state() -> list[RealityAssertion]:
    """Project git HEAD + dirty state per repo."""
    repos = {
        "arifOS-source": "/root/arifOS",
        "arifOS-runtime": "/opt/arifos",
        "A-FORGE": "/root/A-FORGE",
        "AAA": "/root/AAA",
    }
    assertions = []
    for name, path in repos.items():
        try:
            head = subprocess.check_output(["git", "-C", path, "rev-parse", "HEAD"],
                                            text=True, timeout=5).strip()
            ts = datetime.now(timezone.utc).isoformat()
            assertions.append(observation(
                subject=name, predicate="git_head", object=head[:12],
                actor_id="git",
                source_refs=(f"git -C {path} rev-parse HEAD",),
                evidence_refs=(f"git_head={head}",),
                observed_at=ts,
            ))
            # Dirty count
            dirty_raw = subprocess.check_output(["git", "-C", path, "status", "--porcelain"],
                                                  text=True, timeout=5).strip()
            n_dirty = len([l for l in dirty_raw.split('\n') if l.strip()]) if dirty_raw else 0
            assertions.append(observation(
                subject=name, predicate="dirty_count", object=str(n_dirty),
                actor_id="git",
                source_refs=(f"git -C {path} status --porcelain",),
                evidence_refs=(f"dirty_lines={n_dirty}",),
                observed_at=ts,
            ))
        except Exception as e:
            pass  # not a git repo or not available
    return assertions


def project_chron_predictions() -> list[RealityAssertion]:
    """Project CHRON predictions as EXPECTATION assertions."""
    assertions = []
    p_path = Path("/root/chron/data/predictions.jsonl")
    if not p_path.exists():
        return assertions
    for line in p_path.read_text().splitlines():
        if not line.strip(): continue
        try:
            p = json.loads(line)
        except: continue
        pid = p.get("prediction_id", "")
        if not pid: continue
        status = p.get("status", "?")
        claim = p.get("claim", "")[:80]
        ts = p.get("created_at", datetime.now(timezone.utc).isoformat())
        assertions.append(observation(
            subject=f"prediction:{pid}",
            predicate="status",
            object=status,
            actor_id="chron",
            source_refs=("/root/chron/data/predictions.jsonl",),
            evidence_refs=(f"prediction.claim={claim}",),
            observed_at=ts,
            epistemic_class=EPISTEMIC_OBSERVATION,
            authority="OBSERVE_ONLY",
            privacy="internal",
        ))
    return assertions


def project_recent_canary_receipts() -> list[RealityAssertion]:
    """Project canary receipts as OUTCOME assertions."""
    assertions = []
    rdir = Path("/root/forge_work/canary-receipts")
    if not rdir.exists(): return assertions
    for f in sorted(rdir.glob("*.json"))[-5:]:  # last 5
        try:
            data = json.loads(f.read_text())
        except: continue
        svc = data.get("service", "?")
        verdict = data.get("verdict", "?")
        ts = data.get("ran_at", datetime.now(timezone.utc).isoformat())
        assertions.append(observation(
            subject=f"canary:{svc}",
            predicate="verdict",
            object=verdict,
            actor_id="canary-primitive",
            source_refs=(str(f),),
            evidence_refs=(f"canary.elapsed_s={data.get('elapsed_s')}",),
            observed_at=ts,
        ))
    return assertions


def main() -> int:
    g = RealityGraph()

    print("=== Projecting existing federation records into RealityAssertions ===\n")

    sources = [
        ("arifOS /health", project_arifos_health),
        ("git state (4 repos)", project_git_state),
        ("CHRON predictions", project_chron_predictions),
        ("Recent canary receipts", project_recent_canary_receipts),
    ]

    total = 0
    for name, fn in sources:
        assertions = fn()
        for a in assertions:
            g.add_assertion(a)
        print(f"  {name}: {len(assertions)} assertions")
        total += len(assertions)

    # Add PRECEDES edges for time ordering within each subject
    by_subject: dict[str, list[RealityAssertion]] = {}
    for a in g.assertions.values():
        by_subject.setdefault(a.subject, []).append(a)
    n_edges = 0
    for subject, group in by_subject.items():
        group.sort(key=lambda x: x.observed_at)
        for i in range(1, len(group)):
            edge = RealityEdge(
                edge_id=f"precedes-{group[i-1].assertion_id}-{group[i].assertion_id}",
                edge_type=EDGE_PRECEDES,
                from_id=group[i-1].assertion_id,
                to_id=group[i].assertion_id,
                observed_at=group[i].observed_at,
                confidence=0.99,
                source_refs=("monotonic time ordering",),
            )
            g.add_edge(edge)
            n_edges += 1

    print(f"\nTotal: {total} assertions, {n_edges} PRECEDES edges")

    # Save
    out_path = Path("/root/forge_work/reality-graph-projection.json")
    g.path = out_path
    g.save()
    print(f"Saved: {out_path}")

    # Demo: query for all arifOS-runtime convergence assertions
    print("\n=== Query: arifOS-runtime convergence (bitemporal) ===")
    results = g.query(subject="arifOS-runtime", predicate="convergence")
    for r in results:
        print(f"  {r.assertion_id[:18]}... object={r.object} valid_from={r.valid_from}")

    print("\n=== Query: arifOS-runtime drift (bitemporal) ===")
    results = g.query(subject="arifOS-runtime", predicate="drift")
    for r in results:
        print(f"  {r.assertion_id[:18]}... object={r.object} valid_from={r.valid_from}")

    print(f"\nDone. {total} assertions + {n_edges} edges materialized.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
