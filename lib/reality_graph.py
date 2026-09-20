"""reality_graph.py — P_next: Reality Graph substrate (DRAFT 2026-09-21)

Reality Graph ≠ Reality.

It is the federation's time-indexed, provenance-bound, challengeable MAP of reality.

Hierarchy:
    REALITY  >  OBSERVATION  >  EVIDENCE  >  REALITY GRAPH
           >  DERIVED STATE  >  MODEL  >  NARRATIVE

If the graph disagrees with a fresh observation: GRAPH LOSES.
Never alter reality interpretation to preserve graph consistency.

Bitemporal semantics:
    valid_time  = when it was true in the world
    known_time  = when the federation learned it

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ── Epistemic classes (per CHRON + APEX-ZEN) ────────────────────────

EPISTEMIC_OBSERVATION    = "OBS"        # direct measurement
EPISTEMIC_DERIVATION     = "DER"        # computed from observations
EPISTEMIC_INTERPRETATION = "INT"        # model-based interpretation
EPISTEMIC_SPECIFICATION  = "SPEC"       # declared / designed
EPISTEMIC_SEAL           = "SEAL"       # F13-sealed

# ── Node types (12) ────────────────────────────────────────────────

NODE_ENTITY     = "ENTITY"        # something that exists
NODE_ACTOR      = "ACTOR"         # something that acts
NODE_ARTIFACT   = "ARTIFACT"      # something made/manipulated
NODE_OBSERVATION = "OBSERVATION"  # captured measurement
NODE_CLAIM      = "CLAIM"         # asserted proposition
NODE_EVENT      = "EVENT"         # something that happened
NODE_STATE      = "STATE"         # snapshot of attributes at time T
NODE_EXPECTATION = "EXPECTATION"  # forward-looking claim
NODE_ACTION     = "ACTION"        # performed change
NODE_OUTCOME    = "OUTCOME"       # observed result of action
NODE_DECISION   = "DECISION"      # chosen path
NODE_RECEIPT    = "RECEIPT"       # proof of consequence

NODE_TYPES = {
    NODE_ENTITY, NODE_ACTOR, NODE_ARTIFACT,
    NODE_OBSERVATION, NODE_CLAIM, NODE_EVENT, NODE_STATE,
    NODE_EXPECTATION, NODE_ACTION, NODE_OUTCOME,
    NODE_DECISION, NODE_RECEIPT,
}

# ── Edge types (16) ────────────────────────────────────────────────

EDGE_ABOUT              = "ABOUT"             # x is about y
EDGE_OBSERVED_BY        = "OBSERVED_BY"       # x was observed by actor
EDGE_ASSERTED_BY        = "ASSERTED_BY"       # x was asserted by actor
EDGE_SUPPORTED_BY       = "SUPPORTED_BY"      # claim is supported by evidence
EDGE_DERIVED_FROM       = "DERIVED_FROM"       # x is derived from y
EDGE_PRECEDES           = "PRECEDES"          # x comes before y
EDGE_SUPERSEDES         = "SUPERSEDES"        # x replaces y
EDGE_CONTRADICTS        = "CONTRADICTS"       # x disagrees with y
EDGE_TRIGGERED          = "TRIGGERED"         # event triggered action
EDGE_ACTED_ON           = "ACTED_ON"          # action acted on target
EDGE_CAUSED             = "CAUSED"            # x caused y
EDGE_RESULTED_IN        = "RESULTED_IN"       # x resulted in y
EDGE_EXPECTED           = "EXPECTED"          # expectation x
EDGE_VERIFIED_BY        = "VERIFIED_BY"       # outcome verified by witness
EDGE_FALSIFIED_BY       = "FALSIFIED_BY"      # outcome falsified by witness
EDGE_AUTHORIZED_BY      = "AUTHORIZED_BY"     # action authorized by decision
EDGE_EXECUTED_BY        = "EXECUTED_BY"       # action executed by actor
EDGE_WITNESSED_BY       = "WITNESSED_BY"      # outcome witnessed by witness

EDGE_TYPES = {
    EDGE_ABOUT, EDGE_OBSERVED_BY, EDGE_ASSERTED_BY,
    EDGE_SUPPORTED_BY, EDGE_DERIVED_FROM,
    EDGE_PRECEDES, EDGE_SUPERSEDES, EDGE_CONTRADICTS,
    EDGE_TRIGGERED, EDGE_ACTED_ON, EDGE_CAUSED, EDGE_RESULTED_IN,
    EDGE_EXPECTED, EDGE_VERIFIED_BY, EDGE_FALSIFIED_BY,
    EDGE_AUTHORIZED_BY, EDGE_EXECUTED_BY, EDGE_WITNESSED_BY,
}

# ── The canonical RealityAssertion ─────────────────────────────────

@dataclass(frozen=True)
class RealityAssertion:
    """The minimum sufficient unit of federation knowledge.

    Every persistent claim about reality is a RealityAssertion. No exceptions.
    """
    # Identity
    assertion_id: str

    # The claim itself
    subject: str              # what is this about (e.g. "arifOS-runtime")
    predicate: str           # the property (e.g. "built_commit")
    object: str              # the value (e.g. "eeed6ce")

    # Epistemic class
    epistemic_class: str     # OBS / DER / INT / SPEC / SEAL
    confidence: float        # 0.0 - 1.0

    # Bitemporal
    valid_from: str           # ISO-8601: when became true in world
    valid_until: Optional[str] # ISO-8601: when stopped being true (None = still valid)
    observed_at: str          # ISO-8601: when observed
    recorded_at: str          # ISO-8601: when written to graph (defaults to observed_at)

    # Provenance
    source_refs: tuple        # URLs/paths/refs to original sources (no values, only refs)
    evidence_refs: tuple      # evidence (logs, hashes, snapshots)
    actor_id: str             # who recorded (F13 / agent / organ)

    # Authority
    authority_scope: str      # what kind of authority (OBSERVE_ONLY / MUTATE / SEAL)

    # Challengeability
    falsifier: Optional[str]  # how to falsify this assertion
    supersedes: tuple = ()    # assertion_ids this replaces
    contradicted_by: tuple = ()  # assertion_ids that contradict this

    # Operational
    freshness: str = "fresh"  # fresh / aging / stale / unknown
    privacy_scope: str = "internal"  # internal / shared / public
    trace_id: str = ""

    def __post_init__(self):
        if self.epistemic_class not in {EPISTEMIC_OBSERVATION, EPISTEMIC_DERIVATION,
                                        EPISTEMIC_INTERPRETATION, EPISTEMIC_SPECIFICATION,
                                        EPISTEMIC_SEAL}:
            raise ValueError(f"invalid epistemic_class: {self.epistemic_class!r}")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be in [0,1], got {self.confidence}")
        if self.freshness not in {"fresh", "aging", "stale", "unknown"}:
            raise ValueError(f"invalid freshness: {self.freshness!r}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ── The canonical RealityEdge ──────────────────────────────────────

@dataclass(frozen=True)
class RealityEdge:
    """Connection between two RealityAssertions."""
    edge_id: str
    edge_type: str           # from EDGE_TYPES
    from_id: str             # assertion_id of source
    to_id: str               # assertion_id of target

    # Per F13 feedback: every edge needs provenance + uncertainty + falsifier
    confidence: float = 1.0
    observed_at: str = ""
    source_refs: tuple = ()
    falsifier: Optional[str] = None

    # Bitemporal
    valid_from: str = ""
    valid_until: Optional[str] = None

    def __post_init__(self):
        if self.edge_type not in EDGE_TYPES:
            raise ValueError(f"invalid edge_type: {self.edge_type!r}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ── Convenience constructors ──────────────────────────────────────

def observation(
    subject: str, predicate: str, object: str,
    actor_id: str, source_refs: tuple, evidence_refs: tuple,
    confidence: float = 0.95,
    observed_at: Optional[str] = None,
    authority: str = "OBSERVE_ONLY",
    privacy: str = "internal",
    trace_id: str = "",
    epistemic_class: str = EPISTEMIC_OBSERVATION,
) -> RealityAssertion:
    """Factory for direct-observation assertions (the most common kind)."""
    obs_at = observed_at or datetime.now(timezone.utc).isoformat()
    return RealityAssertion(
        assertion_id=f"assert-{uuid.uuid4().hex[:12]}",
        subject=subject, predicate=predicate, object=object,
        epistemic_class=EPISTEMIC_OBSERVATION,
        confidence=confidence,
        valid_from=obs_at,
        valid_until=None,
        observed_at=obs_at,
        recorded_at=obs_at,
        source_refs=source_refs,
        evidence_refs=evidence_refs,
        actor_id=actor_id,
        authority_scope=authority,
        falsifier=None,
        supersedes=(),
        contradicted_by=(),
        freshness="fresh",
        privacy_scope=privacy,
        trace_id=trace_id,
    )


def supersede(old: RealityAssertion, new: RealityAssertion, reason: str) -> RealityAssertion:
    """Mark `new` as superseding `old`. Returns the new assertion with supersedes filled.

    Per F13: bitemporal — old remains valid UNTIL new's valid_from.
    """
    # We can't mutate frozen, so we create a new assertion with supersedes filled
    from dataclasses import replace
    return replace(
        new,
        supersedes=(*new.supersedes, old.assertion_id),
        valid_until=None,
    )


# ── The graph itself ───────────────────────────────────────────────

class RealityGraph:
    """In-memory canonical graph. Persists to JSONL."""

    def __init__(self, path: str | os.PathLike | None = None):
        self.path = Path(path) if path else None
        self.assertions: dict[str, RealityAssertion] = {}
        self.edges: dict[str, RealityEdge] = {}
        if self.path and self.path.exists():
            self._load()

    def add_assertion(self, a: RealityAssertion) -> None:
        self.assertions[a.assertion_id] = a

    def add_edge(self, e: RealityEdge) -> None:
        self.edges[e.edge_id] = e

    def contradict(self, a: RealityAssertion, b: RealityAssertion) -> tuple[RealityAssertion, RealityAssertion]:
        """Mark two assertions as contradicting. Returns updated versions."""
        from dataclasses import replace
        if a.assertion_id == b.assertion_id:
            raise ValueError("cannot contradict self")
        a2 = replace(a, contradicted_by=(*a.contradicted_by, b.assertion_id))
        b2 = replace(b, contradicted_by=(*b.contradicted_by, a.assertion_id))
        self.assertions[a.assertion_id] = a2
        self.assertions[b.assertion_id] = b2
        return a2, b2

    def predecessors(self, assertion_id: str) -> list[RealityAssertion]:
        """Find all assertions that PRECEDE this one."""
        result = []
        for e in self.edges.values():
            if e.to_id == assertion_id and e.edge_type == EDGE_PRECEDES:
                src = self.assertions.get(e.from_id)
                if src: result.append(src)
        return result

    def contradictions(self, assertion_id: str) -> list[RealityAssertion]:
        """Find all assertions that contradict this one."""
        a = self.assertions.get(assertion_id)
        if not a: return []
        return [self.assertions[i] for i in a.contradicted_by if i in self.assertions]

    def supersession_chain(self, assertion_id: str) -> list[RealityAssertion]:
        """Walk the chain of supersessions for this assertion."""
        a = self.assertions.get(assertion_id)
        if not a: return []
        chain = []
        for old_id in a.supersedes:
            old = self.assertions.get(old_id)
            if old:
                chain.append(old)
                chain.extend(self.supersession_chain(old_id))
        return chain

    def query(self, subject: Optional[str] = None, predicate: Optional[str] = None,
              epistemic_class: Optional[str] = None, valid_at: Optional[str] = None) -> list[RealityAssertion]:
        """Filter assertions by criteria."""
        results = []
        for a in self.assertions.values():
            if subject and a.subject != subject: continue
            if predicate and a.predicate != predicate: continue
            if epistemic_class and a.epistemic_class != epistemic_class: continue
            if valid_at:
                if a.valid_until and a.valid_until < valid_at: continue
                if a.valid_from > valid_at: continue
            results.append(a)
        return results

    def save(self) -> None:
        if not self.path: return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w") as f:
            json.dump({
                "assertions": {k: v.to_dict() for k, v in self.assertions.items()},
                "edges": {k: v.to_dict() for k, v in self.edges.items()},
                "saved_at": datetime.now(timezone.utc).isoformat(),
            }, f, indent=2, sort_keys=True)

    def _load(self) -> None:
        try:
            data = json.load(self.path.open())
            for k, v in data.get("assertions", {}).items():
                # Reconstruct RealityAssertion from dict
                self.assertions[k] = RealityAssertion(**{kk: tuple(vv) if isinstance(vv, list) else vv for kk, vv in v.items()})
            for k, v in data.get("edges", {}).items():
                self.edges[k] = RealityEdge(**{kk: tuple(vv) if isinstance(vv, list) else vv for kk, vv in v.items()})
        except Exception as e:
            print(f"[reality_graph] load warning: {e}")


# ── The critical invariant: GRAPH LOSES to fresh observation ──────

def reconcile(graph: RealityGraph, fresh_observation: RealityAssertion) -> dict:
    """When a fresh observation contradicts a graph assertion, the graph LOSES.

    Returns a dict describing the reconciliation:
      { "graph_lost": bool, "old_id": str, "new_id": str, "reason": str }
    """
    # Find existing assertion with same subject+predicate
    existing = [a for a in graph.assertions.values()
                if a.subject == fresh_observation.subject
                and a.predicate == fresh_observation.predicate]

    if not existing:
        # No conflict — just add
        graph.add_assertion(fresh_observation)
        return {"graph_lost": False, "new_id": fresh_observation.assertion_id,
                "reason": "no prior assertion for subject+predicate"}

    # Conflict: graph must lose
    results = []
    for old in existing:
        # The fresh observation supersedes the old
        new = supersede(old, fresh_observation, reason="fresh observation supersedes")
        graph.assertions[old.assertion_id] = replace_with_validity(old, until=fresh_observation.valid_from)
        graph.assertions[new.assertion_id] = new
        # Mark mutual contradiction
        graph.contradict(old, new)
        results.append({
            "graph_lost": True,
            "old_id": old.assertion_id,
            "new_id": new.assertion_id,
            "old_object": old.object,
            "new_object": new.object,
            "subject": old.subject,
            "predicate": old.predicate,
            "reason": "fresh observation supersedes prior assertion (GRAPH LOSES)",
        })

    return results[0] if len(results) == 1 else {"graph_lost": True, "conflicts": results}


def replace_with_validity(a: RealityAssertion, until: str) -> RealityAssertion:
    """Mark an assertion as no longer valid after a given time."""
    from dataclasses import replace
    return replace(a, valid_until=until)


import os  # needed above
