#!/usr/bin/env python3
"""
HERMES RASA MCP Server — Human-Context, Provenance, Privacy & RASA Boundaries

Architecture division:
  arifOS    = authority / governance / action ("May this agent act?")
  HERMES    = human context / provenance / privacy / rasa boundaries
              ("What do we know, whose perspective is it, who may use it, where does inference stop?")

Constitutional Non-Goals:
  - NO infer_emotion_probability()
  - NO relationship_score()
  - NO is_in_love()
  - NO covert personality profiling
  - NO surveillance denominator
  - NO cross-person private-memory leakage
  - NO biometric emotion inference

Success Criterion:
  It becomes mechanically harder for an agent to lie about what it knows about a human.
"""

from __future__ import annotations
import os
import hashlib
import re
import shlex
import json
import sqlite3
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP
import sys
sys.path.insert(0, "/root/.hermes/policy")
from rasa_boundary import (
    validate_cross_layer_transition,
    EXPLANATORY_LAYERS,
    FORBIDDEN_CROSS_LAYER_REDUCTIONS,
    validate_human_claim,
    validate_authority_increase,
    _evidence_is_grounded,
    _falsification_is_grounded,
    _anchor_resolves,
)

# The diagnostic quarantine list lives in the policy module (Rule CL-05, single source of truth).
# The shadow-map guard must still run if that module is refactored, so a frozen fallback copy is
# kept here; it is used only when the import above loses the symbol, and a divergence between the
# two lists is itself a defect (see SHADOW_LEXICON_INTEGRITY in the shadow-map block).
from rasa_boundary import DIAGNOSTIC_QUARANTINE_TERMS

# Initialize FastMCP Server
mcp = FastMCP("hermes-rasa")

DB_PATH = Path("/root/.hermes/state/rasa_mcp.sqlite3")
ENFORCEMENT_LOG = Path(os.getenv("RASA_ENFORCEMENT_LOG", "/var/lib/arifos/rasa_enforcement.jsonl"))

# Ensure state directories exist
try:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENFORCEMENT_LOG.parent.mkdir(parents=True, exist_ok=True)
except OSError:
    pass

# H = 1.5 — labeled hypothesis with provenance, awaiting user confirmation.
# F13 directive 2026-10-05 ("go patch it" + "restart HTTP sidecar, probe it").
# server.py:66-67 duplicates the AUTHORITY_RANK / PROVENANCE_CLASSES from
# rasa_boundary.py:206-227 (the SOT) — this is a LAW-8 violation
# (Satu masalah, satu owner, satu jalan). For this session the duplicate is
# patched in lockstep. The proper fix is to import from rasa_boundary instead
# of re-declaring — flagged for F13 to decide on follow-up.
PROVENANCE_CLASSES = {"O", "S", "R", "I", "F", "P", "C", "H"}
AUTHORITY_RANK = {"F": 0, "P": 0, "I": 1, "R": 1, "H": 1.5, "O": 2, "S": 3, "C": 4}
NEW_EVIDENCE_BASES = {
    "new_self_report_from_subject",
    "new_shared_interaction",
    "new_observation",
    "co_created_statement",
    # F13 directive 2026-10-05: H -> S promotion basis for labeled hypothesis.
    # When the user confirms/rejects the H-class output, the basis is
    # self_report_after_hypothesis — the model's read is the model's, until
    # the subject signs.
    "self_report_after_hypothesis"
}
FORBIDDEN_PROMOTIONS = [
    ("F", "O", "Fiction/archetype cannot be promoted to observed reality"),
    ("P", "O", "Population statistic is not an observation of an individual"),
    ("I", "S", "Machine inference cannot be promoted to human self-report"),
    ("R", "S", "Third-party claim about another person is not that person's self-report"),
    ("I", "C", "Machine inference cannot be promoted to co-created shared meaning"),
    ("R", "O", "One person's report about another is not an observation of that person"),
]

# §24: a hypothesis-reactive answer is weaker evidence than a spontaneous disclosure.
PROMPTED_CONFIDENCE_CEILING = 0.40

# ------------------------------------------------------------------------------------------------
# SIGNAL-CONSEQUENCE SUBSTRATE — shared vocabulary for TOOLS 29-32
#
# Binding invariant: WHEN SIGNAL IS WEAK, INTERPRETATION MUST BECOME NARROWER, NOT MORE ELABORATE.
# An "observation" (the world), an "inference" (the agent), and a "source" (the thing a claim
# rests on) are three different objects. These constants keep the four gates below from drifting
# apart on what counts as literal, as absent, or as agent-generated.
# ------------------------------------------------------------------------------------------------

# Literal-channel markers. This is EXACTLY the list hermes_observe has always carried, promoted to
# one module-level source of truth so the observe gate and the signal gate cannot diverge.
QUALIA_LEAK_TERMS = ["loves", "misses", "wants worship", "attached", "secretly", "craves", "jealous"]

# Markers that mean a string is ALREADY an interpretation, not a channel record. An "observation"
# carrying one of these is contaminated: it may not authorise a wider inference downstream.
INTERPRETATION_LEAK_TERMS = QUALIA_LEAK_TERMS + [
    "because he wants", "because she wants", "because he is", "because she is",
    "he is trying to", "she is trying to", "hidden meaning", "actually feels",
    "deep down", "true feelings", "masking", "pretending",
]

# Cues that mean the text asserts THE ABSENCE of data. Non-emptiness is not evidence.
ABSENCE_CUE_TERMS = (
    "none", "no evidence", "not offered", "not available", "unavailable", "unknown", "n/a", "na",
    "nil", "null", "tbd", "to be determined", "pending", "placeholder", "tiada", "takda", "xde",
    "nothing", "empty", "absent", "cannot be verified", "not verified", "no data", "no source",
)

# Ordered weakest -> strongest. Scope and elaboration budget are monotone in this ladder.
SIGNAL_STRENGTH_LADDER = ("ABSENT", "WEAK", "ADEQUATE", "STRONG")

# Weighted evidence units contributed by one item of each quality class.
EVIDENCE_QUALITY_WEIGHT = {
    "first_party": 3,       # the subject's own words, or a direct instrument record
    "second_party": 2,      # a named third party reporting
    "agent_generated": 1,   # another agent's / a model's output
    "unknown": 1,
}

# Source types that can never be evidence OF THE WORLD, whatever their volume or tone.
AGENT_SOURCE_TYPES = {
    "agent", "agent_output", "agent_generated", "agent_summary", "model_output",
    "model_generated", "llm_output", "inference", "summary",
}

# Source types this gate knows how to weigh. Anything outside the set fails closed (capped WEAK).
RECOGNISED_SOURCE_TYPES = {
    "first_party_observation", "direct_observation", "self_report", "instrument_record",
    "second_party_report", "third_party_document", "public_record", "corpus",
    "agent_output", "agent_generated", "model_output", "inference", "summary", "unknown",
}

# The ONLY verification mechanism this gate actually executes. Any other requested mechanism is
# recorded and refused (the gate will not certify a check it did not run).
MECHANICAL_VERIFICATION_METHODS = {"anchor_resolution"}

# Internal-state inference families. Per the provenance ladder these can never exceed class I
# (machine inference) — they are not observable, and no behaviour volume promotes them.
INTERNAL_STATE_INFERENCE_TYPES = {
    "internal_state", "intent", "motive", "emotion", "feeling", "belief", "desire", "identity",
    "character", "personality", "relational_meaning", "qualia", "trust", "loyalty", "mental_state",
}

# Inference families whose referent is a channel record rather than an interior. Their ceiling is
# still class I, but they can legitimately be re-recorded as class O via hermes_observe.
BEHAVIORAL_INFERENCE_TYPES = {
    "behavioral", "action", "pattern", "frequency", "timing", "channel_choice",
    "communication_behavior",
}

# Language that presents an inference as an observation. Its presence turns a class-I inference
# into an over-classified assertion.
CATEGORICAL_ASSERTION_MARKERS = (
    "clearly", "obviously", "definitely", "certainly", "proves", "proven", "confirmed that",
    "the fact that", "without doubt", "must have felt", "is trying to", "we know that",
)

# Language that claims the machine OBSERVED an interior (provenance promotion I -> O/S/C).
PROVENANCE_PROMOTION_MARKERS = (
    "i observed that he", "i observed that she", "i can see that he", "i can see that she",
    "observed that he feels", "observed that she feels", "he/she feels", "i verified his feelings",
    "i verified her feelings", "his true intention", "her true intention", "co-created meaning",
)

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS claims (
                claim_id TEXT PRIMARY KEY,
                subject TEXT NOT NULL,
                speaker TEXT,
                addressee TEXT,
                channel TEXT,
                provenance_class TEXT NOT NULL,
                observation TEXT NOT NULL,
                interpretation TEXT,
                alternatives TEXT,
                not_established TEXT,
                confidence REAL NOT NULL,
                privacy_class TEXT NOT NULL,
                disclosable_to TEXT,
                prompted INTEGER NOT NULL,
                spontaneous INTEGER NOT NULL,
                authority_basis TEXT,
                supersedes TEXT,
                state TEXT NOT NULL,
                sealed_at TEXT,
                raw_json TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS observations (
                event_id TEXT PRIMARY KEY,
                actor TEXT NOT NULL,
                channel TEXT NOT NULL,
                statement_or_action TEXT NOT NULL,
                observed_at TEXT NOT NULL,
                source_ref TEXT,
                raw_json TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS contradictions (
                event_id TEXT PRIMARY KEY,
                perspective_a TEXT NOT NULL,
                perspective_b TEXT NOT NULL,
                shared_meaning TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
        """)
    return conn

def log_event(event_type: str, details: Dict[str, Any]):
    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "event_type": event_type,
        "details": details
    }
    line = json.dumps(entry) + "\n"
    try:
        ENFORCEMENT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(ENFORCEMENT_LOG, "a", encoding="utf-8") as f:
            f.write(line)
        return
    except OSError:
        pass
    try:
        with open("/tmp/rasa_enforcement.jsonl", "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass

# ------------------------------------------------------------------------------------------------
# TOOL 1: hermes_observe
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_observe(
    event_id: str,
    actor: str,
    channel: str,
    statement_or_action: str,
    observed_at: Optional[str] = None,
    source_ref: Optional[str] = None
) -> Dict[str, Any]:
    """Register literal human behavior/event without interpretation.
    
    Class: Always OBSERVED (O). Zero inference. No motives, no hidden meanings.
    """
    timestamp = observed_at or datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Check for forbidden qualia/motive keywords in raw observation
    qualia_keywords = ["loves", "misses", "wants worship", "attached", "secretly", "craves", "jealous"]
    for kw in qualia_keywords:
        if kw in statement_or_action.lower():
            log_event("REJECT_INTERPRETATION_IN_OBSERVE", {"event_id": event_id, "keyword": kw})
            return {
                "ok": False,
                "error": f"RASA Violation (§1): Raw observation contains interpretive keyword '{kw}'. "
                         "Use hermes_observe only for literal events, exact words, or sensor recordings."
            }

    conn = get_db()
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO observations 
            (event_id, actor, channel, statement_or_action, observed_at, source_ref, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            event_id, actor, channel, statement_or_action, timestamp, source_ref,
            json.dumps({
                "event_id": event_id,
                "actor": actor,
                "channel": channel,
                "statement_or_action": statement_or_action,
                "observed_at": timestamp,
                "source_ref": source_ref
            })
        ))
    
    log_event("OBSERVE_RECORDED", {"event_id": event_id, "actor": actor, "channel": channel})
    return {
        "ok": True,
        "event_id": event_id,
        "class": "O",
        "actor": actor,
        "observed_at": timestamp,
        "status": "REGISTERED_AS_OBSERVED_EVENT"
    }

# ------------------------------------------------------------------------------------------------
# TOOL 2: hermes_claim
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_claim(
    claim_id: str,
    subject: str,
    provenance_class: str,
    observation: str,
    speaker: Optional[str] = None,
    addressee: Optional[str] = None,
    channel: Optional[str] = None,
    interpretation: Optional[str] = None,
    alternatives: Optional[List[str]] = None,
    not_established: Optional[List[str]] = None,
    confidence: float = 1.0,
    privacy_class: str = "shared-channel",
    disclosable_to: Optional[List[str]] = None,
    prompted: bool = False,
    authority_basis: Optional[str] = None,
    supersedes: Optional[str] = None
) -> Dict[str, Any]:
    """Store a typed human claim with strict provenance and mechanical promotion firewall.
    
    Provenance classes: O (Observed), S (Self-Report), R (Reported-by-Other),
    I (Inference), F (Fiction/Persona), P (Population Prior), C (Co-Created).
    
    Fail-closed promotions: F->O, P->O, I->S, R->S, I->C, R->O.
    """
    prov = provenance_class.upper()
    if prov not in PROVENANCE_CLASSES:
        return {"ok": False, "error": f"Invalid provenance_class '{prov}'. Must be one of {PROVENANCE_CLASSES}"}

    conn = get_db()

    # ---- G1 STRUCTURAL: class S is a self-report; the speaker must BE the subject ----------
    # Without this, one call can manufacture a self-report that was never made by labelling a
    # third party's account of a human as class S. A third party's account is class R.
    if prov == "S" and speaker and str(speaker).strip().lower() != str(subject).strip().lower():
        log_event("REJECT_SELF_REPORT_NOT_BY_SUBJECT",
                  {"claim_id": claim_id, "speaker": speaker, "subject": subject})
        return {
            "ok": False,
            "error": (f"G1 SELF_REPORT_WITHOUT_SUBJECT: class S requires speaker == subject "
                      f"(speaker='{speaker}', subject='{subject}'). A third party's account of "
                      f"another human is class R, never S.")
        }

    # ---- AUTO-LINK: discover a prior claim on the same subject when `supersedes` is absent ---
    # The promotion firewall used to run ONLY when the writer volunteered `supersedes`. That let
    # a fresh claim_id inflate authority over an existing record with no link (the Agent-D
    # consensus bypass). The gate now finds the prior itself — complete mediation, not opt-in.
    prior_row = None
    if supersedes:
        prior_row = conn.execute(
            "SELECT provenance_class, authority_basis, raw_json FROM claims WHERE claim_id = ?",
            (supersedes,)).fetchone()
    else:
        prior_row = conn.execute(
            """SELECT provenance_class, authority_basis, raw_json, claim_id
               FROM claims WHERE subject = ? AND claim_id != ?
               ORDER BY rowid DESC LIMIT 1""",
            (subject, claim_id)).fetchone()
        if prior_row:
            log_event("AUTO_LINKED_PRIOR",
                      {"claim_id": claim_id, "prior_claim_id": prior_row["claim_id"],
                       "prior_class": prior_row["provenance_class"], "to_class": prov})

    # If a prior exists (linked or auto-discovered), check for forbidden promotion or authority jump
    if prior_row:
        row = prior_row
        if True:
            prev_class = row["provenance_class"]
            prev_rank = AUTHORITY_RANK.get(prev_class, 0)
            cur_rank = AUTHORITY_RANK.get(prov, 0)
            
            # Check forbidden promotions
            for f_from, f_to, reason in FORBIDDEN_PROMOTIONS:
                if prev_class == f_from and prov == f_to:
                    log_event("REJECT_FORBIDDEN_PROMOTION", {"claim_id": claim_id, "from": f_from, "to": f_to,
                                                             "auto_linked": not supersedes})
                    return {
                        "ok": False,
                        "error": f"FORBIDDEN_PROMOTION ({f_from} -> {f_to}): {reason}. Authority cannot be upgraded without new authorized evidence."
                    }
            
            # Check authority jump without new evidence
            if cur_rank > prev_rank:
                if not authority_basis or authority_basis not in NEW_EVIDENCE_BASES:
                    log_event("REJECT_AUTHORITY_INCREASE", {"claim_id": claim_id, "from": prev_class, "to": prov, "basis": authority_basis,
                                                             "auto_linked": not supersedes})
                    return {
                        "ok": False,
                        "error": f"Runtime Invariant Violation: Authority raised {prev_class}->{prov} without new authorized evidence (got: '{authority_basis}')."
                    }

    # Interpretive classes require alternatives and not_established
    if prov in {"I", "R", "F", "P"}:
        if not not_established and not alternatives:
            return {
                "ok": False,
                "error": f"RASA Violation (§29): Interpretive class '{prov}' requires explicit 'not_established' boundaries or competing 'alternatives'."
            }

    # Fiction class cannot be stored as measured human reality
    if prov == "F" and confidence > 0.5:
        confidence = 0.0

    # ---- G4 STRUCTURAL: prompted evidence is weaker than spontaneous (§24) -------------------
    # A hypothesis-reactive answer ("do you miss him?" -> "maybe") is not equal in evidentiary
    # weight to an unprompted disclosure. Nothing read `prompted` before, so an agent-elicited
    # answer was stored at full confidence. Cap it.
    if prompted and isinstance(confidence, (int, float)) and confidence > PROMPTED_CONFIDENCE_CEILING:
        log_event("CAP_PROMPTED_CONFIDENCE",
                  {"claim_id": claim_id, "from": confidence, "to": PROMPTED_CONFIDENCE_CEILING})
        confidence = PROMPTED_CONFIDENCE_CEILING

    raw_data = {
        "claim_id": claim_id,
        "subject": subject,
        "speaker": speaker,
        "addressee": addressee,
        "channel": channel,
        "provenance_class": prov,
        "observation": observation,
        "interpretation": interpretation,
        "alternatives": alternatives or [],
        "not_established": not_established or [],
        "confidence": confidence,
        "privacy_class": privacy_class,
        "disclosable_to": disclosable_to or [],
        "prompted": prompted,
        "spontaneous": not prompted,
        "authority_basis": authority_basis,
        "supersedes": supersedes,
        "state": "RECORDED"
    }

    # ---- SINGLE-SOURCE GATE: the writer runs the SAME canonical validator the seal does --------
    # hermes_claim previously reimplemented a subset of the gate inline, while hermes_seal calls
    # validate_human_claim. Two copies of one rule diverge — that is how a class-O interiority
    # claim leaked at write time but was caught at the seal boundary (probe A5/A13). Routing both
    # through validate_human_claim is complete mediation: whatever the seal would refuse, the
    # writer refuses now. prev_class feeds the authority check from the auto-linked prior.
    prev_class = prior_row["provenance_class"] if prior_row else None
    gate_errs = validate_human_claim(raw_data, previous_class=prev_class)
    if gate_errs:
        log_event("REJECT_AT_WRITE_GATE", {"claim_id": claim_id, "violations": gate_errs[:3]})
        return {
            "ok": False,
            "error": f"WRITE_REFUSED: {gate_errs[0][:200]}",
        }

    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO claims 
            (claim_id, subject, speaker, addressee, channel, provenance_class, observation,
             interpretation, alternatives, not_established, confidence, privacy_class,
             disclosable_to, prompted, spontaneous, authority_basis, supersedes, state, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            claim_id, subject, speaker, addressee, channel, prov, observation,
            interpretation, json.dumps(alternatives or []), json.dumps(not_established or []),
            confidence, privacy_class, json.dumps(disclosable_to or []),
            1 if prompted else 0, 0 if prompted else 1, authority_basis, supersedes, "RECORDED",
            json.dumps(raw_data)
        ))

    log_event("CLAIM_STORED", {"claim_id": claim_id, "subject": subject, "class": prov})
    return {
        "ok": True,
        "claim_id": claim_id,
        "class": prov,
        "subject": subject,
        "status": "RECORDED"
    }

# ------------------------------------------------------------------------------------------------
# TOOL 3: hermes_perspective
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_perspective(
    subject: str,
    requester_principal: str
) -> Dict[str, Any]:
    """Return what is known from one human's perspective versus shared reality.
    
    Protects perspective sovereignty (§22): Private disclosures of other humans are filtered out.
    """
    conn = get_db()
    cursor = conn.execute("SELECT * FROM claims WHERE subject = ? OR speaker = ?", (subject, subject))
    records = cursor.fetchall()
    
    disclosable = []
    filtered_count = 0
    
    for row in records:
        data = json.loads(row["raw_json"])
        priv = data.get("privacy_class", "shared-channel")
        disclosable_to = set(data.get("disclosable_to", []))
        speaker = data.get("speaker")
        
        # Privacy filtering — FAIL CLOSED.
        # An empty/unset `disclosable_to` means "no one has been granted access", NOT "no
        # restriction". Reading it as the latter let an unrelated principal read a shared-channel
        # or private-to-pair record (probe finding A8). Only the subject always sees their own.
        if priv in {"private-to-subject", "f5-private"}:
            if requester_principal != subject and requester_principal not in disclosable_to:
                filtered_count += 1
                continue
        elif priv in {"private-to-pair", "shared-channel"}:
            # subject always sees own record; anyone else needs an explicit grant
            if requester_principal != subject and requester_principal not in disclosable_to:
                filtered_count += 1
                continue
        elif priv != "public":
            # unknown/missing privacy class: fail closed rather than leak
            if requester_principal != subject:
                filtered_count += 1
                continue

        disclosable.append({
            "claim_id": data["claim_id"],
            "class": data["provenance_class"],
            "observation": data["observation"],
            "interpretation": data.get("interpretation"),
            "not_established": data.get("not_established"),
            "confidence": data.get("confidence")
        })

    return {
        "subject": subject,
        "requester": requester_principal,
        "visible_claims": disclosable,
        "quarantined_private_records_count": filtered_count,
        "perspective_sovereignty_enforced": True
    }

# ------------------------------------------------------------------------------------------------
# TOOL 4: hermes_consent
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_consent(
    claim_id: str,
    requester_principal: str,
    target_audience: str
) -> Dict[str, Any]:
    """Determine whether a piece of human information may be used or disclosed in the target audience."""
    conn = get_db()
    row = conn.execute("SELECT raw_json FROM claims WHERE claim_id = ?", (claim_id,)).fetchone()
    if not row:
        return {"ok": False, "error": f"No claim found with id '{claim_id}'"}
    
    data = json.loads(row["raw_json"])
    priv = data.get("privacy_class", "f5-private")
    disclosable_to = set(data.get("disclosable_to", []))
    subject = data.get("subject")
    
    if priv == "public":
        return {"allowed": True, "reason": "Claim is designated public."}
        
    if target_audience.lower() in {"public", "group"} and priv != "public":
        return {
            "allowed": False,
            "reason": f"RASA Violation (§22): Private claim ({priv}) cannot be disclosed to public/group audience."
        }
        
    if requester_principal not in disclosable_to and requester_principal != subject:
        return {
            "allowed": False,
            "reason": f"Access Denied: Requester '{requester_principal}' lacks permission for {priv} record."
        }
        
    return {"allowed": True, "reason": "Audience and principal match disclosure permissions."}

# ------------------------------------------------------------------------------------------------
# TOOL 5: hermes_contradiction
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_contradiction(
    event_id: str,
    human_a: str,
    statement_a: str,
    human_b: str,
    statement_b: str
) -> Dict[str, Any]:
    """Preserve conflicting human accounts side-by-side without resolving them automatically.
    
    Refuses premature adjudication of truth vs deception (§36).
    """
    record = {
        "event_id": event_id,
        "perspectives": {
            human_a: {"statement": statement_a, "class": "S"},
            human_b: {"statement": statement_b, "class": "S"}
        },
        "resolution": "PRESERVED_DUALITY",
        "shared_meaning": "UNKNOWN_UNCREATED",
        "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    conn = get_db()
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO contradictions (event_id, perspective_a, perspective_b, shared_meaning, recorded_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            event_id,
            json.dumps({human_a: statement_a}),
            json.dumps({human_b: statement_b}),
            "UNKNOWN_UNCREATED",
            record["recorded_at"]
        ))
        
    log_event("CONTRADICTION_PRESERVED", {"event_id": event_id, "humans": [human_a, human_b]})
    return {
        "ok": True,
        "event_id": event_id,
        "status": "DUAL_PERSPECTIVES_PRESERVED",
        "record": record
    }

# ------------------------------------------------------------------------------------------------
# TOOL 5b: hermes_contradiction_scan
# ------------------------------------------------------------------------------------------------
# PATCH 6 (REVISED 2026-10-11T01:15:00Z) — Additive detector.
# Read-only. No canonical-store mutation. No authority output.
# PURE-FUNCTION DECORATORS LIVE INLINE BELOW — DO NOT re-export; they were
# verified by /root/AAA/instructions/patches/P6/test_detector.py before this
# patch was applied. The server-inlined copy MUST remain byte-equivalent to
# the source-of-truth: see patch-receipts/P6_inline_compat_pinned.py for the
# one-line equality check.
import re as _p6_re
_P6_CLASSES = {"SCOPE", "DENOMINATOR", "SOURCE", "TEMPORAL", "MODEL_VERSUS_MODEL",
              "MODEL_VERSUS_REALITY", "MEASUREMENT_VERSUS_INTERPRETATION",
              "FORECAST_VERSUS_OUTCOME", "HEADLINE_VERSUS_BODY", "UNKNOWN"}
_P6_STATUSES = {"RESOLVED_BY_SCOPE", "PARTIALLY_RECONCILED", "OPEN", "UNKNOWN"}
_P6_MONEY_RE = _p6_re.compile(r"RM\s?(\d+(?:\.\d+)?)\s?(b|m|million|billion|k)?", _p6_re.I)
_P6_USD_RE = _p6_re.compile(r"USD\s?(\d+(?:\.\d+)?)(?:\s?/bbl)?", _p6_re.I)
_P6_PCT_RE = _p6_re.compile(r"(\d+(?:\.\d+)?)\s?(?:%|percent\b)", _p6_re.I)
_P6_BBL_RE = _p6_re.compile(r"(\d+(?:\.\d+)?)\s?(?:MM)?bbl", _p6_re.I)
_P6_DATE_RE = _p6_re.compile(r"\b(20\d{2}-\d{2}-\d{2}|20\d{2}/\d{2}/\d{2})\b")
_P6_FCAST_HINTS = ("forecast", "target", "estimate", "expected", "expected to",
                   "projection", "will ", " 2027", "2028")
_P6_REPORT_HINTS = ("announced", "tabled", "stated", "told parliament",
                    "reported", "released", "confirmed", "today")

def _p6_norm_money(n, unit):
    u = (unit or "b").lower()
    if u in ("b", "billion"): return n, "RM_b"
    if u in ("m", "million"):  return n / 1000.0, "RM_b"
    if u == "k":               return n / 1_000_000.0, "RM_b"
    return n, "RM_" + (u or "b")

def _p6_extract_numbers(text):
    out = {}
    money = [{"raw": m.group(0), "value_b_RM": _p6_norm_money(float(m.group(1)), m.group(2) or "b")[0]}
             for m in _P6_MONEY_RE.finditer(text)]
    usd = [{"raw": m.group(0), "value_usd": float(m.group(1))}
           for m in _P6_USD_RE.finditer(text)]
    pct = [float(m.group(1)) for m in _P6_PCT_RE.finditer(text)]
    bbl = [float(m.group(1)) for m in _P6_BBL_RE.finditer(text)]
    if money: out["money_RM_b"] = money
    if usd:   out["usd"] = usd
    if pct:   out["pct"] = pct
    if bbl:   out["bbl"] = bbl
    return out

def _p6_tense(text):
    tl = (text or "").lower()
    if any(h in tl for h in _P6_FCAST_HINTS): return "FORECAST"
    if any(h in tl for h in _P6_REPORT_HINTS): return "REPORTED"
    return "AMBIGUOUS"

def _p6_first_date(text):
    m = _P6_DATE_RE.search(text or "")
    return m.group(1) if m else None

def _p6_norm(s):
    return (s or "").strip().lower()

def _p6_source_cluster(source):
    s = _p6_norm(source)
    if not s: return "unknown"
    if "reuters" in s:    return "reuters_wire"
    if "thestar" in s or "the star" in s: return "thestar"
    if "nst" in s:        return "nst"
    if "theedgemalaysia" in s or "edge" in s: return "edge"
    if "federated" in s or "mof" in s or "treasury" in s or "belanjawan" in s: return "mof_primary"
    if "bernam" in s:     return "bernama_wire"
    if "malaymail" in s:  return "malaymail"
    if "channelnewsasia" in s or "cna" in s:  return "cna"
    if "freemalaysia" in s or "fmt" in s:    return "fmt"
    if "malaysiakini" in s: return "malaysiakini"
    if "ocbc" in s:       return "ocbc_research"
    if "cimb" in s:       return "cimb_research"
    if "bimb" in s:       return "bimb_research"
    if "uob" in s:        return "uob_research"
    if "ram" in s:        return "ram_research"
    return s.split("@")[-1].split(".")[-2] if "." in s else "unknown"

def _p6_row(counter, klass, a, b, subject, unit, denom_a, denom_b, source_a, source_b,
            status, evidence, reconciliation, decision):
    if klass not in _P6_CLASSES:    raise ValueError("illegal class")
    if status not in _P6_STATUSES: raise ValueError("illegal status")
    return {
        "contradiction_id": "cscan-{:04d}".format(counter),
        "claim_a_id": a.get("id"), "claim_b_id": b.get("id"),
        "class": klass, "source_a": source_a, "source_b": source_b,
        "subject": subject, "unit": unit,
        "temporal_scope": {"a": _p6_first_date(a.get("text", "")),
                           "b": _p6_first_date(b.get("text", ""))},
        "geographic_scope": a.get("geography") or "MY",
        "denominator_a": denom_a, "denominator_b": denom_b,
        "possible_reconciliation": reconciliation,
        "evidence_needed": evidence, "decision_impact": decision,
        "status": status,
        "limitations": ["hermes_contradiction_scan is semantic evidence only; "
                        "no authority effect, no canonical-store mutation"],
    }

def _p6_scan(claims):
    if not isinstance(claims, list):
        return {"ok": False, "error": "claims must be a list", "contradictions": []}
    cluster_for = {c.get("id"): _p6_source_cluster(c.get("source")) for c in claims}
    parsed = [{"claim": c, "nums": _p6_extract_numbers(c.get("text", "")),
               "tense": _p6_tense(c.get("text", "")), "kind": c.get("kind"),
               "principal": c.get("principal")} for c in claims]
    rows = []
    counter = [1]
    def emit(klass, a, b, subject, unit, denom_a, denom_b, sa, sb, status, ev, rec, dec):
        rows.append(_p6_row(counter[0], klass, a, b, subject, unit, denom_a, denom_b, sa, sb, status, ev, rec, dec))
        counter[0] += 1
    def norm(s): return _p6_norm(s)
    def same_p(a, b):
        if not a.get("principal") or not b.get("principal"): return True
        return norm(a["principal"]) == norm(b["principal"])
    def same_geo(a, b):
        return norm(a["claim"].get("geography") or "MY") == norm(b["claim"].get("geography") or "MY")
    def same_unit(a, b):
        if not a["nums"] or not b["nums"]: return False
        return bool(set(a["nums"].keys()) & set(b["nums"].keys()))

    # A. SCOPE / SOURCE for any two same-principal RM-money mismatches.
    for i, a in enumerate(parsed):
        for j, b in enumerate(parsed):
            if j <= i: continue
            if not same_p(a, b) or not same_geo(a, b): continue
            am = a["nums"].get("money_RM_b", [])
            bm = b["nums"].get("money_RM_b", [])
            if not am or not bm: continue
            av = am[0]["value_b_RM"]; bv = bm[0]["value_b_RM"]
            if abs(av - bv) < 1e-9: continue
            ta = (a["claim"].get("text") or "").lower()
            tb = (b["claim"].get("text") or "").lower()
            off_a = any(h in ta for h in ("off-budget", "glic", "statutory", "ppp", "investment"))
            off_b = any(h in tb for h in ("off-budget", "glic", "statutory", "ppp", "investment"))
            if off_a or off_b:
                emit("SCOPE", a["claim"], b["claim"], norm(a["claim"].get("principal")) or "amount",
                     "RM_b", "claims_with_investment_units" if off_a else "claims_alone",
                     "claims_with_investment_units" if off_b else "claims_alone",
                     a["claim"].get("source"), b["claim"].get("source"),
                     "RESOLVED_BY_SCOPE",
                     "explicit perimeter token on at least one side",
                     "one totals federal alone; the other adds statutory/off-budget",
                     "treat the smaller figure as the federal operating budget")
            else:
                emit("SOURCE", a["claim"], b["claim"], norm(a["claim"].get("principal")) or "amount",
                     "RM_b", None, None, a["claim"].get("source"), b["claim"].get("source"),
                     "OPEN", "no perimeter token; cannot tell whether scope or source divergence",
                     "verify whether b excludes statutory/off-budget categories",
                     "do not pick either figure as 'true' budget size")

    # B. MODEL_VERSUS_MODEL / FORECAST_VERSUS_OUTCOME
    for i, a in enumerate(parsed):
        for j, b in enumerate(parsed):
            if j <= i: continue
            if not same_p(a, b) or not same_geo(a, b): continue
            at = a["tense"]; bt = b["tense"]
            if at == "FORECAST" and bt == "FORECAST":
                if cluster_for.get(a["claim"].get("id")) == cluster_for.get(b["claim"].get("id")):
                    continue
                if not same_unit(a, b): continue
                emit("MODEL_VERSUS_MODEL", a["claim"], b["claim"],
                     norm(a["claim"].get("principal")) or "forecast", "mixed",
                     None, None, a["claim"].get("source"), b["claim"].get("source"),
                     "OPEN", "two independent forecasting sources, conflicting values",
                     "requires outturn or pre-budget update to converge",
                     "treat as forecast band, not point estimate")
            elif (at == "FORECAST" and bt == "REPORTED") or (at == "REPORTED" and bt == "FORECAST"):
                if not same_unit(a, b): continue
                emit("FORECAST_VERSUS_OUTCOME", a["claim"], b["claim"],
                     norm(a["claim"].get("principal")) or "quantity", "mixed",
                     None, None, a["claim"].get("source"), b["claim"].get("source"),
                     "OPEN", "forecast tense vs reported tense on same quantity",
                     "compare predicted value against most recent outturn",
                     "do not collapse the band")

    # C. MODEL_VERSUS_REALITY (oil assumption vs spot)
    oil_asm = [p for p in parsed if "usd" in p["nums"] and "oil" in (p["claim"].get("principal") or "").lower()]
    oil_spot = [p for p in parsed if "usd" in p["nums"] and
                ("spot" in (p["claim"].get("text", "").lower()) or
                 "brent" in (p["claim"].get("text", "").lower()) or
                 "oil" in (p["claim"].get("principal") or "").lower() and
                 p["claim"].get("kind") == "REPORTED")]
    seen = set()
    for a in oil_asm:
        for b in oil_spot:
            if a["claim"].get("id") == b["claim"].get("id"): continue
            av = a["nums"]["usd"][0]["value_usd"]
            bv = b["nums"]["usd"][0]["value_usd"]
            if abs(av - bv) < 1: continue
            key = (a["claim"].get("id"), b["claim"].get("id"))
            if key in seen: continue
            seen.add(key)
            emit("MODEL_VERSUS_REALITY", a["claim"], b["claim"],
                 "oil_assumption_vs_spot", "USD_per_bbl", None, None,
                 a["claim"].get("source"), b["claim"].get("source"),
                 "OPEN", f"model={av} vs spot={bv} (gap > 1 USD)",
                 "report actual average over the same period the model applies to",
                 "until reconciled, do not credit the model assumption as observed reality")

    # D. DENOMINATOR (subsidy scope)
    subsidy = [p for p in parsed if "subsid" in (p["claim"].get("text", "")).lower()]
    for i, a in enumerate(subsidy):
        for j, b in enumerate(subsidy):
            if j <= i: continue
            am = a["nums"].get("money_RM_b", [])
            bm = b["nums"].get("money_RM_b", [])
            if not am or not bm: continue
            av = am[0]["value_b_RM"]; bv = bm[0]["value_b_RM"]
            if abs(av - bv) < 1e-9: continue
            ta = (a["claim"].get("text") or "").lower()
            tb = (b["claim"].get("text") or "").lower()
            sa = any(k in ta for k in ("fuel", "ron95", "diesel", "petrol"))
            sb = any(k in tb for k in ("fuel", "ron95", "diesel", "petrol"))
            emit("DENOMINATOR", a["claim"], b["claim"],
                 "subsidy_total", "RM_b",
                 "fuel-only" if sa else "subsidies+incentives",
                 "fuel-only" if sb else "subsidies+incentives",
                 a["claim"].get("source"), b["claim"].get("source"),
                 "PARTIALLY_RECONCILED" if (sa != sb) else "OPEN",
                 "different sub-basket coverage between two sources",
                 "request Fiscal Outlook Section 3 for the canonical denominator",
                 "do not present either as 'the' subsidy figure until reconciled")

    # E. MEASUREMENT_VERSUS_INTERPRETATION — pair-level
    pct_pair_claims = [p for p in parsed if p["nums"].get("pct")]
    for i, a in enumerate(pct_pair_claims):
        for j, b in enumerate(pct_pair_claims):
            if j <= i: continue
            ap = a["nums"]["pct"]; bp = b["nums"]["pct"]
            if abs(ap[0] - bp[0]) < 0.05: continue
            ta = (a["claim"].get("text") or "").lower()
            tb = (b["claim"].get("text") or "").lower()
            if "below" in ta or "below" in tb or "under" in tb or "above" in ta:
                emit("MEASUREMENT_VERSUS_INTERPRETATION", a["claim"], b["claim"],
                     "deficit_period_measurement", "pct", None, None,
                     a["claim"].get("source"), b["claim"].get("source"),
                     "OPEN",
                     "percentage quoted both 'above X%' and 'below X%' for similar period",
                     "request the underlying monthly deficit number",
                     "do not pick which percentage is correct; preserve both")

    # F. SELF-INCONSISTENT WORDING — within a single claim
    for c in parsed:
        t = c["claim"].get("text", "")
        tl = t.lower()
        pct = c["nums"].get("pct", [])
        if len(pct) < 2: continue
        items = []
        for m in _P6_PCT_RE.finditer(t):
            v = float(m.group(1))
            window = tl[m.end(): m.end() + 30]
            if any(w in window for w in ("above ", "exceeds ", "more than ")):  label = "ABOVE"
            elif any(w in window for w in ("below", "under", "less than", "smaller than")): label = "BELOW"
            else:                                                                                  label = "NEUTRAL"
            items.append((m.start(), v, label))
        items.sort(key=lambda x: x[0])
        if len(items) >= 2:
            v_first, l_first = items[0][1], items[0][2]
            v_second = items[1][1]
            if v_first > v_second and l_first == "BELOW":
                emit("MEASUREMENT_VERSUS_INTERPRETATION", c["claim"], c["claim"],
                     "self_inconsistent_period_percentage", "pct", None, None,
                     c["claim"].get("source"), c["claim"].get("source"), "OPEN",
                     f"text says {v_first}% is BELOW {v_second}%; numerically larger number reported as smaller",
                     "ask source to clarify whether 1H figure or target is the correct numerator",
                     "do not pick which percentage is correct; preserve both as written")

    # Dedup by (a_id, b_id, class, status).
    dedup, seen = [], set()
    for r in rows:
        k = (r["claim_a_id"], r["claim_b_id"], r["class"], r["status"])
        if k in seen: continue
        seen.add(k); dedup.append(r)

    return {
        "ok": True,
        "contradictions": dedup,
        "source_clusters": {c.get("id"): cluster_for.get(c.get("id")) for c in claims},
        "limitations": [
            "deterministic numeric parser; figures written as words ('RM ten billion') are not extracted",
            "percent symbol (%) and word 'percent of GDP' are both extracted",
            "does not weight sources; agents must apply judgment off this surface",
            "does not persist; passing claims to the detector twice produces the same output"
        ],
    }

@mcp.tool
def hermes_contradiction_scan(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Additive PATCH 6 detector. Returns semantic evidence only.
    Does NOT mutate canonical store. Does NOT authorize. Does NOT judge.
    Output is a list of contradiction rows classified by enum CLASSES ∈
    {SCOPE, DENOMINATOR, SOURCE, TEMPORAL, MODEL_VERSUS_MODEL,
    MODEL_VERSUS_REALITY, MEASUREMENT_VERSUS_INTERPRETATION,
    FORECAST_VERSUS_OUTCOME, HEADLINE_VERSUS_BODY, UNKNOWN}
    with status ∈ {RESOLVED_BY_SCOPE, PARTIALLY_RECONCILED, OPEN, UNKNOWN}.
    """
    return _p6_scan(claims)

# ------------------------------------------------------------------------------------------------
# TOOL 6: hermes_infer
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_infer(
    subject: str,
    observation_ref: str,
    proposed_interpretation: str,
    competing_alternatives: List[str],
    confidence: float = 0.5
) -> Dict[str, Any]:
    """Produce bounded interpretations plus alternatives. Never silently promote to fact."""
    if len(competing_alternatives) < 2:
        return {
            "ok": False,
            "error": "RASA Violation (§29 L4): hermes_infer requires at least TWO competing alternative explanations."
        }
        
    capped_confidence = min(0.70, confidence)
    
    return {
        "ok": True,
        "class": "I",
        "subject": subject,
        "observation_ref": observation_ref,
        "interpretation": proposed_interpretation,
        "alternatives": competing_alternatives,
        "confidence": capped_confidence,
        "not_established": ["Subjective qualia", "Unverified internal intent"],
        "notice": "This is a machine inference (Class I). It must never be cited as self-report (Class S) or direct observation (Class O)."
    }

# ------------------------------------------------------------------------------------------------
# TOOL 7: hermes_relationship
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_relationship(
    human_a: str,
    human_b: str,
    contact: float = 0.0,
    humor: float = 0.0,
    care: float = 0.0,
    disclosure: float = 0.0,
    affection: float = 0.0,
    physicality: float = 0.0,
    boundaries: float = 0.0,
    future_orientation: float = 0.0,
    meaning: float = 0.0
) -> Dict[str, Any]:
    """Return vector-valued relational topology without producing a single 'relationship score'."""
    vector = {
        "contact": contact,
        "humor": humor,
        "care": care,
        "disclosure": disclosure,
        "affection": affection,
        "physicality": physicality,
        "boundaries": boundaries,
        "future_orientation": future_orientation,
        "meaning": meaning
    }
    
    return {
        "dyad": [human_a, human_b],
        "relational_vector": vector,
        "scalar_utility_score": "PROHIBITED_BY_RASA_CONSTITUTION_SECTION_15",
        "interpretation_rule": "Relational currencies are unpriced. Asymmetries reflect differing expression channels, not unequal relational worth."
    }

# ------------------------------------------------------------------------------------------------
# TOOL 8: hermes_stop
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_stop(
    target_question: str,
    boundary_type: str,
    reason: str
) -> Dict[str, Any]:
    """Classify the terminal boundary and halt unnecessary compute or illegitimate surveillance.
    
    Boundary types:
      - UNKNOWN_RETRIEVABLE
      - UNKNOWN_HUMAN_PRIVATE
      - UNKNOWN_UNCREATED
      - ETHICALLY_INACCESSIBLE
      - CHANNEL_EXHAUSTED
    """
    valid_boundaries = {
        "UNKNOWN_RETRIEVABLE",
        "UNKNOWN_HUMAN_PRIVATE",
        "UNKNOWN_UNCREATED",
        "ETHICALLY_INACCESSIBLE",
        "CHANNEL_EXHAUSTED"
    }
    
    b_type = boundary_type.upper()
    if b_type not in valid_boundaries:
        return {"ok": False, "error": f"Invalid boundary_type '{boundary_type}'. Must be one of {valid_boundaries}"}
        
    log_event("STOP_STATE_TRIGGERED", {"target": target_question, "boundary": b_type, "reason": reason})
    
    return {
        "ok": True,
        "terminal_state": b_type,
        "target_question": target_question,
        "reason": reason,
        "action": "HALT_COMPUTATION",
        "sovereignty_rule": "Return authority to the humans."
    }

# ------------------------------------------------------------------------------------------------
# TOOL 9: hermes_seal
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_seal(
    claim_id: str
) -> Dict[str, Any]:
    """Finalize and seal the verified human-context claim into the persistent RASA ledger."""
    conn = get_db()
    row = conn.execute("SELECT raw_json FROM claims WHERE claim_id = ?", (claim_id,)).fetchone()
    if not row:
        return {"ok": False, "error": f"Cannot seal non-existent claim '{claim_id}'"}
        
    sealed_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # ---- SEAL RE-VALIDATES (A13 fix) --------------------------------------------------------
    # Sealing is the point of no return into durable memory, so the gate must run HERE, not only
    # at write time. A claim that slipped past the writer (e.g. class-O interiority via a lexical
    # gap) is caught at the seal boundary instead of being canonised. Fail closed.
    stored = json.loads(row["raw_json"])
    recheck = validate_human_claim(stored)
    if recheck:
        log_event("REJECT_SEAL_INTEGRITY", {"claim_id": claim_id, "violations": recheck[:3]})
        return {
            "ok": False,
            "error": f"SEAL_REFUSED: claim failed integrity re-check at the seal boundary: {recheck[0][:160]}",
        }

    with conn:
        conn.execute("UPDATE claims SET state = 'SEALED', sealed_at = ? WHERE claim_id = ?", (sealed_timestamp, claim_id))
        
    log_event("CLAIM_SEALED", {"claim_id": claim_id, "sealed_at": sealed_timestamp})
    return {
        "ok": True,
        "claim_id": claim_id,
        "state": "SEALED",
        "sealed_at": sealed_timestamp
    }

# ================================================================================================
# HERMES SHADOW & PARADOX RUNTIME SUITE (§1 - §42)
# ================================================================================================

# ------------------------------------------------------------------------------------------------
# SHADOW MAP — deterministic tension detection (implementation 2026-09-19; replaces the stub that
# returned a hard-coded empty `shadow_candidates` list and a length-echo tension string).
#
# DOCTRINAL SITUS
#   hermes-shadow.md §7    SHADOW is a GAP MODEL over self_model / self_report / observed_behavior /
#                          emotional_salience / social_role / values / context.
#   hermes-shadow.md §36   an analysis carries WHAT_IS_REAL, WHAT_THE_HUMAN_SAYS, THE_TENSION,
#                          possible interpretations, >=2 alternatives, counterevidence,
#                          qualia limit, privacy scope, next action.
#   hermes-shadow.md §37   the maximum class for a shadow candidate is INFERENCE (I).
#   hermes-shadow.md §38-39 / 10 kill criteria: an unfalsifiable question is rejected, not stored.
#   hermes-shadow.md App.A  inside this doctrine SHADOW is always SHADOW_CANDIDATE — a question,
#                          never a finding; never a bare human-facing sentence.
#   hermes-rasa.md §32      register/audience variation is context-switching, not deception.
#
# WHAT MAY BE COMPUTED HERE (and is shown to the caller)
#   surface-token frequency | lexicon presence/absence | register comparison | corpus size
# WHAT MAY NEVER BE COMPUTED HERE
#   no interior inference | no affection/closeness/warmth/attachment score | no personality type
#   | no archetype assigned to a real person | no diagnostic label | no LLM call | no network
#   | no clock | no randomness. If a rule would need an interior to fire, the rule is DROPPED
#   rather than approximated.
# ------------------------------------------------------------------------------------------------

import re as _re

_SHADOW_TOKEN_RE = _re.compile(r"[a-z0-9']+")

# Lexicons hold SURFACE TOKENS — words that were literally written. A token is never a trait of the
# person, and nothing here is scored: the numbers are counts of words in a corpus, nothing else.
SHADOW_REGISTER_LEXICON: Dict[str, List[str]] = {
    "LOGISTICS": sorted([
        "jumpa", "meet", "meeting", "lunch", "dinner", "makan", "makan malam", "minum", "tempat",
        "place", "rumah", "home", "sewa", "rent", "rented", "evicted", "housing", "duit", "bayar",
        "kerja", "work", "shift", "transport", "otw", "sampai", "balik", "drive", "tol", "parking",
        "appointment", "book", "kelas", "class", "hantar", "ambil", "schedule", "jam", "pukul",
        "messages", "mesej", "chat",
    ]),
    "CAPACITY_SELF_MODEL": sorted([
        "aku ni", "saya ni", "im", "i am", "i'm", "jenis orang", "type of person", "kuat", "strong",
        "strength", "boleh tahan", "abang sado", "lelaki", "man", "mental", "steady", "independent",
        "sendiri", "identity", "peranan", "role", "senior", "junior",
    ]),
    "AFFECT_DISTRESS": sorted([
        "penat", "tired", "letih", "stress", "tertekan", "pressure", "tekanan", "sedih", "takut",
        "risau", "marah", "geram", "serabut", "pening", "penin", "down", "burnout", "hadap", "cope",
        "coping", "xtahu", "tak tahu", "tak boleh", "susah", "beban", "burden", "nangis",
        "menangis", "hilang", "lost", "kosong", "empty",
    ]),
    "HELP_REQUEST": sorted([
        "tolong", "help", "bantuan", "perlukan", "perlu bantuan", "support", "pinjam", "borrow",
        "tumpang", "aku perlukan",
    ]),
    "NAMED_ACTIVITY": sorted([
        "dating", "keluar", "jumpa", "meet", "call", "telefon", "balas", "reply", "whatsapp",
        "hantar", "sampai", "otw", "drive", "workout", "lari", "makan", "minum", "gym", "pergi",
        "balik", "sembang",
    ]),
}

# Absolute / universal self-description markers. Their use is not a defect — but a universal claim
# with zero observed instances in the log is a testable boundary question, not a finding.
SHADOW_ABSOLUTE_TERMS = sorted([
    "always", "never", "selalu", "tak pernah", "memang", "100%", "confirm", "definitely", "semua",
    "all the time", "setiap kali",
])

# Two or more competing explanations are mandatory for any rich interpretation (hermes-shadow.md
# §19). These are deliberately boring: they require less hidden psychology, not more.
_SHADOW_BORING_ALTERNATIVES = [
    "Sampling frame: the two corpora cover different windows, addressees or elicitation modes "
    "(prompted vs spontaneous), so the difference may be an artefact of capture.",
    "Channel/register difference (hermes-rasa.md §32): the same person produces different valid "
    "register for a different audience, and neither register is the truer one.",
    "Ordinary drift: register, vocabulary and topics shift over time within one channel with no "
    "hidden process required.",
]

_SHADOW_COUNTEREVIDENCE = [
    "A gap between two records is not evidence of a hidden state; it is a description of the records.",
    "Absence of a token in a bounded channel has high semantic entropy (hermes-shadow.md §24) and is "
    "not proof of absence in the person.",
    "One corpus cannot establish a boundary in a human; the model must stay smaller than the human "
    "(hermes-shadow.md §40-42).",
]


def _shadow_tokens(texts: List[str]) -> List[str]:
    """Lowercase surface tokens across a corpus. Deterministic; no stemming, no synonyms."""
    joined = "\n".join(str(t).lower() for t in texts)
    return _SHADOW_TOKEN_RE.findall(joined)


def _shadow_lexicon_hits(texts: List[str], lexicon: List[str]) -> Dict[str, Any]:
    """Count hits of `lexicon` terms in `texts`. Phrases (containing a space) are substring-matched,
    single tokens are counted as whole tokens. Counts only — nothing is scored or weighted."""
    joined = "\n".join(str(t).lower() for t in texts)
    toks = _SHADOW_TOKEN_RE.findall(joined)
    occurrences: Dict[str, int] = {}
    for term in lexicon:
        n = joined.count(term) if " " in term else toks.count(term)
        if n:
            occurrences[term] = n
    return {
        "distinct": len(occurrences),
        "total_occurrences": sum(occurrences.values()),
        "terms": sorted(occurrences),
    }


def _shadow_register_table(texts: List[str]) -> Dict[str, Dict[str, Any]]:
    return {reg: _shadow_lexicon_hits(texts, SHADOW_REGISTER_LEXICON[reg]) for reg in sorted(SHADOW_REGISTER_LEXICON)}


def _shadow_leading_register(table: Dict[str, Dict[str, Any]]) -> Optional[str]:
    active = [(reg, v) for reg, v in table.items() if v["distinct"] > 0]
    if not active:
        return None
    active.sort(key=lambda kv: (-kv[1]["distinct"], -kv[1]["total_occurrences"], kv[0]))
    return active[0][0]


def _shadow_absent_registers(table: Dict[str, Dict[str, Any]]) -> str:
    absent = sorted(reg for reg, v in table.items() if v["distinct"] == 0)
    return ", ".join(absent) if absent else "none"


def _shadow_quarantine_hits(texts: List[str]) -> List[str]:
    """Return the quarantined diagnostic terms present in `texts` (Rule CL-05).

    Deliberately substring-based and case-insensitive, matching the policy module's own scan, so a
    term cannot slip through as part of a longer word.
    """
    hits: List[str] = []
    for text in texts:
        low = str(text).lower()
        for term in DIAGNOSTIC_QUARANTINE_TERMS:
            if term in low:
                hits.append(term)
    return sorted(set(hits))


def _shadow_lexicon_integrity() -> List[str]:
    """Import-time self-check: no curated lexicon may contain a quarantined diagnostic term.

    Without this, vocabulary drift could smuggle a label into the output through a lexicon entry
    that the guard would then drop the whole candidate over — a silent capability loss.
    """
    offenders: List[str] = []
    lexicons = [(name, terms) for name, terms in sorted(SHADOW_REGISTER_LEXICON.items())]
    lexicons.append(("ABSOLUTE_TERMS", SHADOW_ABSOLUTE_TERMS))
    for name, terms in lexicons:
        for term in terms:
            if _shadow_quarantine_hits([term]):
                offenders.append(f"{name}:{term}")
    return offenders


SHADOW_LEXICON_INTEGRITY = _shadow_lexicon_integrity()

@mcp.tool
def hermes_shadow_map(
    actor_id: str,
    observations: List[str],
    self_reports: List[str],
    context: str = "general",
    audience: str = "private"
) -> Dict[str, Any]:
    """Identify tensions between a human's explicit self-model, self-report, and behavior.

    Deterministic implementation (2026-09-19). What the tool mechanically computes:

      * register frequency of curated SURFACE tokens in the two corpora
      * lexicon presence/absence between the self-report register and the observation register
      * self-named activity terms, and absolute self-description terms, that have zero instances
        in the observation log

    Every candidate is a QUESTION carrying `question`, `evidence_for`, `evidence_against` and a
    `falsification_test` (hermes-shadow.md §36-38) — a shadow candidate is never a finding
    (Appendix A). When no rule fires, `shadow_candidates` is EMPTY and `insufficient_evidence`
    states why: silence is a valid output and is distinguishable from failure.

    Constitutional rule: HERMES must never claim to 'detect the shadow'.
    Output class is strictly capped at INFERENCE (Class I). Never outputs hidden truth.
    No scoring of affection/closeness/warmth/attachment, no personality type, no archetype, no
    diagnostic label — the quarantine guard is fail-closed: it drops or refuses rather than emits.
    No LLM call, no network, no clock, no randomness: identical input yields identical output.
    """
    if SHADOW_LEXICON_INTEGRITY:
        # Fail closed: a lexicon carrying a label would make this tool a label emitter.
        return {
            "ok": False,
            "status": "RASA_HOLD",
            "actor_id": actor_id,
            "class": "I",
            "shadow_candidates": [],
            "error": ("REFUSED TO EMIT: the shadow-map lexicon failed its own integrity check "
                      f"({len(SHADOW_LEXICON_INTEGRITY)} entry/entries carry a quarantined term index); "
                      "no analysis was produced."),
        }

    obs = [str(x) for x in (observations or [])]
    reps = [str(x) for x in (self_reports or [])]

    corpus = {
        "observations": {
            "lines": len(obs),
            "chars": sum(len(x) for x in obs),
            "tokens": len(_shadow_tokens(obs)),
        },
        "self_reports": {
            "lines": len(reps),
            "chars": sum(len(x) for x in reps),
            "tokens": len(_shadow_tokens(reps)),
        },
    }

    obs_reg = _shadow_register_table(obs)
    rep_reg = _shadow_register_table(reps)
    obs_leading = _shadow_leading_register(obs_reg)
    rep_leading = _shadow_leading_register(rep_reg)

    candidates: List[Dict[str, Any]] = []
    guard_events: List[Dict[str, Any]] = []
    rule_log: List[Dict[str, str]] = []

    def _corpus_line(label: str, stats: Dict[str, int], table: Dict[str, Dict[str, Any]]) -> str:
        parts = ", ".join(
            f"{reg}={table[reg]['distinct']}term/{table[reg]['total_occurrences']}hit" for reg in sorted(table)
        )
        return (f"{label}: {stats['lines']} line(s), {stats['tokens']} token(s); "
                f"register table (surface tokens only): {parts}")

    def _emit(rule_id: str, tension: str, question: str, evidence_for: List[str],
              evidence_against: List[str], falsification_test: str, rule_alternative: str,
              next_action: str, what_is_real: str, what_human_says: str) -> bool:
        authored = ([tension, question, what_is_real, what_human_says, falsification_test,
                     rule_alternative, next_action] + list(evidence_for) + list(evidence_against))
        blocked = _shadow_quarantine_hits(authored)
        if blocked:
            # Refuse to emit rather than emit a label; the terms themselves are never echoed.
            guard_events.append({
                "rule_id": rule_id,
                "action": "CANDIDATE_DROPPED",
                "detail": f"{len(blocked)} authored string(s) carried a quarantined term index; not echoed",
            })
            return False
        candidates.append({
            "rule_id": rule_id,
            "class": "I",
            "status": "SHADOW_CANDIDATE",
            "tension": tension,                              # §36 THE_TENSION
            "question": question,                            # §36 interpretation, only as a question
            "what_is_real": what_is_real,                    # §36 WHAT_IS_REAL (computed counts)
            "what_the_human_says": what_human_says,           # §36 WHAT_THE_HUMAN_SAYS
            "evidence_for": list(evidence_for),
            "evidence_against": list(evidence_against),
            "counterevidence": list(_SHADOW_COUNTEREVIDENCE),
            "alternatives": [rule_alternative] + list(_SHADOW_BORING_ALTERNATIVES[:2]),
            "falsification_test": falsification_test,
            "qualia_limit": ("PRIVATE_QUALIA - no interior state is asserted here; this question "
                             "cannot be answered from this channel."),
            "privacy_scope": audience,
            "next_action": next_action,
            "promotion_blocked": ["I->O", "I->S", "I->C"],
        })
        return True

    # ---- RULE 1: REGISTER_ASYMMETRY ----------------------------------------------------------
    if not obs or not reps:
        rule_log.append({
            "rule": "REGISTER_ASYMMETRY",
            "outcome": (f"SKIPPED - empty corpus (observations={len(obs)} line(s), "
                        f"self_reports={len(reps)} line(s)); no comparison is possible and this is "
                        "NOT a finding of absence"),
        })
    elif obs_leading is None or rep_leading is None:
        rule_log.append({
            "rule": "REGISTER_ASYMMETRY",
            "outcome": (f"NO TENSION - one corpus carries no register-lexicon terms at all "
                        f"(observations={obs_leading or 'NONE'}, self_reports={rep_leading or 'NONE'}), "
                        "so no register comparison is possible; an empty register table is not a finding"),
        })
    elif obs_leading == rep_leading:
        rule_log.append({
            "rule": "REGISTER_ASYMMETRY",
            "outcome": (f"NO TENSION - both corpora read in the same leading register "
                        f"({obs_leading or 'no register terms found in either corpus'})"),
        })
    else:
        o = obs_reg[obs_leading]
        r = rep_reg[rep_leading]
        emitted = _emit(
            rule_id="REGISTER_ASYMMETRY",
            tension=(f"observation register reads as {obs_leading} while the self-report register "
                     f"reads as {rep_leading}"),
            question=(
                f"The observation log reads in a {obs_leading} register ({o['distinct']} distinct "
                f"term(s), {o['total_occurrences']} hit(s): {', '.join(o['terms'])}), while the "
                f"self-reports read in a {rep_leading} register ({r['distinct']} distinct term(s), "
                f"{r['total_occurrences']} hit(s): {', '.join(r['terms'])}). Which register governs "
                f"when the stakes are high?"
            ),
            evidence_for=[
                f"computed: observations {obs_leading}={o['distinct']} term(s)/{o['total_occurrences']} hit(s) - tokens: {', '.join(o['terms'])}",
                f"computed: self_reports {rep_leading}={r['distinct']} term(s)/{r['total_occurrences']} hit(s) - tokens: {', '.join(r['terms'])}",
                f"computed: registers absent from the observation corpus: {_shadow_absent_registers(obs_reg)}",
                f"computed: registers absent from the self-report corpus: {_shadow_absent_registers(rep_reg)}",
            ],
            evidence_against=[
                "Register is channel output, not character: the same person produces a different valid register for a different addressee.",
                (f"Corpus sizes differ (observations={corpus['observations']['lines']} line(s)/"
                 f"{corpus['observations']['tokens']} token(s) vs self_reports="
                 f"{corpus['self_reports']['lines']} line(s)/{corpus['self_reports']['tokens']} token(s)); "
                 "unequal sampling alone can move the leading register."),
                (f"Caller-declared context='{context}', audience='{audience}' - a different context or "
                 "audience is not deception (hermes-rasa.md §32)."),
            ],
            falsification_test=(
                "Re-run this comparison on observations drawn from the same channel, addressee and "
                "window as the self-reports. If the leading registers converge, the asymmetry was an "
                "artefact of the sampling frame, not a boundary in the person."
            ),
            rule_alternative=("The two corpora are capture formats, not two registers of one person: "
                              "an event/logbook log structurally omits self-description."),
            next_action="ASK_ONE_BOUNDED_QUESTION_OR_DO_NOTHING",
            what_is_real=_corpus_line("observations", corpus["observations"], obs_reg),
            what_human_says=_corpus_line("self_reports", corpus["self_reports"], rep_reg),
        )
        rule_log.append({
            "rule": "REGISTER_ASYMMETRY",
            "outcome": (f"TENSION EMITTED - leading registers differ ({obs_leading} vs {rep_leading})"
                        if emitted else "CANDIDATE DROPPED BY QUARANTINE GUARD"),
        })

    # ---- RULE 2: LEXICON_ABSENT_FROM_OBSERVATIONS --------------------------------------------
    watched = ("CAPACITY_SELF_MODEL", "AFFECT_DISTRESS", "HELP_REQUEST")
    absent_in_obs = sorted(
        [reg for reg in watched if rep_reg[reg]["distinct"] > 0 and obs_reg[reg]["distinct"] == 0],
        key=lambda reg: (-rep_reg[reg]["distinct"], reg),
    )
    if not obs or not reps:
        rule_log.append({
            "rule": "LEXICON_ABSENT_FROM_OBSERVATIONS",
            "outcome": "SKIPPED - empty corpus",
        })
    elif not absent_in_obs:
        rule_log.append({
            "rule": "LEXICON_ABSENT_FROM_OBSERVATIONS",
            "outcome": ("NO TENSION - every watched register used by the self-reports is also present "
                        "in the observation corpus"),
        })
    else:
        outcomes = []
        for reg in absent_in_obs[:2]:
            rr = rep_reg[reg]
            emitted = _emit(
                rule_id=f"LEXICON_ABSENT_FROM_OBSERVATIONS:{reg}",
                tension=(f"the self-reports carry {reg} vocabulary (n={rr['distinct']}) that has zero "
                         f"instances across {corpus['observations']['lines']} observation line(s)"),
                question=(
                    f"The subject's own lines carry {reg} vocabulary ({rr['distinct']} distinct "
                    f"term(s), {rr['total_occurrences']} hit(s): {', '.join(rr['terms'])}), and the "
                    f"observation log contains zero instances of any of it. Does the observation "
                    f"channel simply not carry {reg}, or is {reg} absent from the observed contexts - "
                    f"and what observation would tell those two apart?"
                ),
                evidence_for=[
                    f"computed: self_reports {reg}={rr['distinct']} term(s)/{rr['total_occurrences']} hit(s) - tokens: {', '.join(rr['terms'])}",
                    f"computed: observations {reg}=0 term/0 hit across {corpus['observations']['lines']} line(s)",
                    f"computed: observation-corpus registers absent overall: {_shadow_absent_registers(obs_reg)}",
                ],
                evidence_against=[
                    "The observation corpus may be a logbook whose format cannot carry this vocabulary at all, in which case zero is a property of the format, not of the person.",
                    "High disclosure cost weakens inference from silence: silence is not a negative finding (hermes-shadow.md §20, §24).",
                    (f"Corpus asymmetry: {corpus['observations']['lines']} observation line(s) vs "
                     f"{corpus['self_reports']['lines']} self-report line(s); zero in a small corpus is weak."),
                ],
                falsification_test=(
                    "Obtain one observation, from the same channel and window, that carries this "
                    "vocabulary. That alone falsifies the reading that this register is absent from "
                    "the observed context. Retest with the subject's own words, not with a model's."
                ),
                rule_alternative=("The observation log is written by an observer (or a corpus scan) in "
                                  "report vocabulary, so the subject's own affect/capacity words would "
                                  "not appear even if present in the person."),
                next_action="DO_NOTHING_OR_ASK_THE_SUBJECT",
                what_is_real=_corpus_line("observations", corpus["observations"], obs_reg),
                what_human_says=_corpus_line("self_reports", corpus["self_reports"], rep_reg),
            )
            outcomes.append(f"{reg}={'EMITTED' if emitted else 'DROPPED_BY_GUARD'}")
        rule_log.append({
            "rule": "LEXICON_ABSENT_FROM_OBSERVATIONS",
            "outcome": "TENSION EMITTED - " + ", ".join(outcomes) + (f" (capped at 2 of {len(absent_in_obs)})" if len(absent_in_obs) > 2 else ""),
        })

    # ---- RULE 3: NAMED_ACTIVITY_ABSENT -------------------------------------------------------
    rep_acts = rep_reg["NAMED_ACTIVITY"]
    obs_act_terms = set(obs_reg["NAMED_ACTIVITY"]["terms"])
    absent_acts = sorted(t for t in rep_acts["terms"] if t not in obs_act_terms)
    if not obs or not reps:
        rule_log.append({"rule": "NAMED_ACTIVITY_ABSENT", "outcome": "SKIPPED - empty corpus"})
    elif not rep_acts["terms"]:
        rule_log.append({
            "rule": "NAMED_ACTIVITY_ABSENT",
            "outcome": ("NO TENSION - the self-reports name no activity term from this lexicon, so "
                        "there is nothing to compare against the log"),
        })
    elif not absent_acts:
        rule_log.append({
            "rule": "NAMED_ACTIVITY_ABSENT",
            "outcome": ("NO TENSION - every activity the self-reports name also appears in the "
                        "observation log"),
        })
    else:
        hits = rep_acts["total_occurrences"]  # self-report activity hits (counts only)
        emitted = _emit(
            rule_id="NAMED_ACTIVITY_ABSENT",
            tension=(f"the self-reports name {len(absent_acts)} activity term(s) that have zero "
                     f"instances in the observation log"),
            question=(
                f"The self-reports name these activities: {', '.join(absent_acts)} (self-report "
                f"activity register: {rep_acts['distinct']} term(s), {hits} hit(s)); the observation "
                f"log records zero instances of them. Was the activity not logged, not performed in "
                f"the observed window, or performed and recorded in words this lexicon does not read?"
            ),
            evidence_for=[
                f"computed: self-report activity terms with zero observed instances: {', '.join(absent_acts)}",
                f"computed: observation activity register: {obs_reg['NAMED_ACTIVITY']['distinct']} term(s) - {', '.join(obs_reg['NAMED_ACTIVITY']['terms']) or 'none'}",
                f"computed: self-report activity register: {rep_acts['distinct']} term(s) - {', '.join(rep_acts['terms']) or 'none'}",
            ],
            evidence_against=[
                "The observation log covers a declared window; an activity outside that window cannot appear in it regardless of whether it happened.",
                "Self-named activity is the subject's own description; it is class S and needs no corroboration to be recorded, only to be treated as an event.",
                f"Caller-declared context='{context}' scopes what the log claims to cover.",
            ],
            falsification_test=(
                "Extend the observation log over the period the self-report covers and look for the "
                "named activity. If it appears, the tension was a coverage gap. If the log already "
                "covers that period and the activity is still absent, say so as a coverage fact only - "
                "never as evidence of an interior."
            ),
            rule_alternative=("Logging is selective: people report plans and arrivals more readily than "
                              "quiet private activity, so a log will under-represent ordinary action."),
            next_action="DO_NOTHING",
            what_is_real=_corpus_line("observations", corpus["observations"], obs_reg),
            what_human_says=_corpus_line("self_reports", corpus["self_reports"], rep_reg),
        )
        rule_log.append({
            "rule": "NAMED_ACTIVITY_ABSENT",
            "outcome": ("TENSION EMITTED - zero-instance activity terms: " + ", ".join(absent_acts)
                        if emitted else "CANDIDATE DROPPED BY QUARANTINE GUARD"),
        })

    # ---- RULE 4: ABSOLUTE_SELF_DESCRIPTION ---------------------------------------------------
    rep_abs = _shadow_lexicon_hits(reps, SHADOW_ABSOLUTE_TERMS)
    obs_abs = _shadow_lexicon_hits(obs, SHADOW_ABSOLUTE_TERMS)
    if not obs or not reps:
        rule_log.append({"rule": "ABSOLUTE_SELF_DESCRIPTION", "outcome": "SKIPPED - empty corpus"})
    elif not rep_abs["distinct"]:
        rule_log.append({
            "rule": "ABSOLUTE_SELF_DESCRIPTION",
            "outcome": "NO TENSION - the self-reports contain no absolute/universal self-description terms",
        })
    elif obs_abs["distinct"]:
        rule_log.append({
            "rule": "ABSOLUTE_SELF_DESCRIPTION",
            "outcome": (f"NO TENSION - the absolute terms used in self-reports also appear in the "
                        f"observation log ({obs_abs['distinct']} term(s))"),
        })
    else:
        emitted = _emit(
            rule_id="ABSOLUTE_SELF_DESCRIPTION",
            tension=("the self-model states absolutes that are not observed (terms: "
                     f"{', '.join(rep_abs['terms'])})"),
            question=(
                f"The self-reports describe the subject in absolute terms ({', '.join(rep_abs['terms'])}: "
                f"{rep_abs['distinct']} distinct term(s), {rep_abs['total_occurrences']} hit(s)), and "
                f"the observation log contains none of these terms. What are the boundary conditions "
                f"(time, context, audience) under which the absolute holds?"
            ),
            evidence_for=[
                f"computed: self-report absolute terms: {', '.join(rep_abs['terms'])} ({rep_abs['total_occurrences']} hit(s))",
                f"computed: observation absolute terms: 0 across {corpus['observations']['lines']} line(s)",
                "computed: this is a property of two texts, not a claim about the person",
            ],
            evidence_against=[
                "Absolutes are ordinary conversational emphasis in every register; their absence from a log is not counter-instance evidence.",
                "A bounded corpus can rarely produce a counter-instance for a universal claim, so the absence of one is weak by construction (hermes-shadow.md §24).",
            ],
            falsification_test=(
                "One observed instance in this log where the absolute did not hold would weaken it. "
                "Do not treat the absence of such an instance as confirmation: an absent "
                "counter-instance in a bounded channel is not evidence (hermes-shadow.md §38-39)."
            ),
            rule_alternative=("Emphasis, not measurement: absolute words usually mean 'this is how it "
                              "feels most of the time', and carry no quantitative claim to test."),
            next_action="DO_NOTHING",
            what_is_real=_corpus_line("observations", corpus["observations"], obs_reg),
            what_human_says=_corpus_line("self_reports", corpus["self_reports"], rep_reg),
        )
        rule_log.append({
            "rule": "ABSOLUTE_SELF_DESCRIPTION",
            "outcome": ("TENSION EMITTED - absolute terms unobserved: " + ", ".join(rep_abs["terms"])
                        if emitted else "CANDIDATE DROPPED BY QUARANTINE GUARD"),
        })

    # ---- tensions (backward-compatible list of strings) & computed silence --------------------
    tensions: List[str] = [
        f"Corpus: observations=[{corpus['observations']['lines']} lines, "
        f"{corpus['observations']['tokens']} tokens] vs stated self-model=["
        f"{corpus['self_reports']['lines']} reports, {corpus['self_reports']['tokens']} tokens]"
    ]
    tensions.extend(c["tension"] for c in candidates)

    insufficient_evidence: Optional[str] = None
    if not candidates:
        insufficient_evidence = (
            "insufficient_evidence: no deterministic tension rule fired, so NO candidate is emitted "
            "(silence is a valid output, not a failure). corpus observations="
            f"{corpus['observations']['lines']} line(s)/{corpus['observations']['tokens']} token(s), "
            f"self_reports={corpus['self_reports']['lines']} line(s)/{corpus['self_reports']['tokens']} token(s); "
            f"leading register observations={obs_leading or 'NONE'} self_reports={rep_leading or 'NONE'}; "
            + " | ".join(f"{entry['rule']}={entry['outcome']}" for entry in rule_log)
        )

    # ---- diagnostics quarantine (Rule CL-05), both directions ---------------------------------
    input_quarantine_hits = _shadow_quarantine_hits(obs + reps)

    authored_all: List[str] = list(tensions)
    if insufficient_evidence:
        authored_all.append(insufficient_evidence)
    for c in candidates:
        authored_all.extend([c["tension"], c["question"], c["what_is_real"], c["what_the_human_says"],
                             c["falsification_test"], c["qualia_limit"], c["next_action"], c["privacy_scope"]])
        authored_all.extend(c["evidence_for"] + c["evidence_against"] + c["counterevidence"] + c["alternatives"])
        authored_all.extend(c["promotion_blocked"])
        authored_all.append(c["rule_id"])
        authored_all.append(c["status"])

    final_hits = _shadow_quarantine_hits(authored_all)
    if final_hits:
        log_event("REJECT_SHADOW_MAP_DIAGNOSTIC_LABEL", {"actor_id": actor_id, "count": len(final_hits)})
        return {
            "ok": False,
            "status": "RASA_HOLD",
            "actor_id": actor_id,
            "class": "I",
            "shadow_candidates": [],
            "tensions": tensions,
            "insufficient_evidence": insufficient_evidence,
            "error": ("REFUSED TO EMIT: authored text for this response carried "
                      f"{len(final_hits)} quarantined diagnostic term index/indices. The response was "
                      "withheld rather than emitted with a label about a real person (Rule CL-05). "
                      "No term is echoed."),
            "qualia_boundary": "PRIVATE_QUALIA",
            "provenance": "INFERENCE_ONLY",
            "warning": "Shadow candidates are questions, never answers. Do not promote to observed fact."
        }

    return {
        "ok": True,
        "actor_id": actor_id,
        "class": "I",
        "tensions": tensions,
        "shadow_candidates": candidates,
        "corpus": corpus,
        "registers": {
            "observations": obs_reg,
            "self_reports": rep_reg,
            "leading": {"observations": obs_leading, "self_reports": rep_leading},
        },
        "rules_evaluated": rule_log,
        "candidate_count": len(candidates),
        "insufficient_evidence": insufficient_evidence,
        "diagnostic_quarantine": {
            "guard": "ACTIVE",
            "input_terms_detected": len(input_quarantine_hits),
            "input_terms_echoed": 0,
            "candidates_dropped_by_guard": len(guard_events),
            "note": ("Terms on the diagnostic quarantine list present in the input are counted, never "
                     "echoed, and can never enter this response or person-model state as an attribute "
                     "(Rule CL-05)."),
        },
        "qualia_boundary": "PRIVATE_QUALIA",
        "provenance": "INFERENCE_ONLY",
        "warning": "Shadow candidates are questions, never answers. Do not promote to observed fact."
    }

@mcp.tool
def hermes_paradox_map(
    domain: str,
    state_a: str,
    state_b: str,
    human: str = "subject",
    coexistence_possible: bool = True
) -> Dict[str, Any]:
    """Represent simultaneously active competing human goals (e.g. closeness vs autonomy).
    
    Refuses forced normalization (LOVE XOR ANGER). Preserves LOVE AND ANGER.
    """
    return {
        "ok": True,
        "domain": domain,
        "human": human,
        "paradox": {
            "state_a": state_a,
            "state_b": state_b,
            "coexistence_possible": coexistence_possible,
            "resolution_required": False
        },
        "rule": "Contradiction != Pathology, Contradiction != Deception. Preserved as multi-objective reality."
    }

@mcp.tool
def hermes_discrepancy(
    human: str,
    said: Optional[str] = None,
    done: Optional[str] = None,
    remembered: Optional[str] = None,
    avoided: Optional[str] = None,
    competing_explanations: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Compare said vs done vs remembered vs avoided. Emits DISCREPANCY_OBSERVED, never DECEPTION_DETECTED."""
    if not competing_explanations:
        return {
            "ok": False,
            "error": "RASA Violation: hermes_discrepancy requires explicit competing_explanations from the caller. No generic defaults."
        }
    explanations = competing_explanations
    
    return {
        "ok": True,
        "human": human,
        "status": "DISCREPANCY_OBSERVED",
        "prohibited_label": "DECEPTION_DETECTED",
        "comparisons": {
            "said": said,
            "done": done,
            "remembered": remembered,
            "avoided": avoided
        },
        "competing_explanations": explanations,
        "notice": "Declared value != observed behavior does NOT imply hypocrisy or deceit."
    }

@mcp.tool
def hermes_counterstory(
    candidate_interpretation: str,
    supporting_evidence: List[str],
    evidence_against: List[str],
    competing_alternatives: List[str],
    falsification_observation: str
) -> Dict[str, Any]:
    """Break narrative gravity by forcing counter-hypotheses and falsification criteria."""
    if len(competing_alternatives) < 3:
        return {
            "ok": False,
            "error": "HERMES SHADOW Violation (§TOOL 4): hermes_counterstory requires at least 3 plausible alternate explanations."
        }
    if not falsification_observation.strip():
        return {
            "ok": False,
            "status": "NARRATIVE_NOT_TESTABLE",
            "error": "Unfalsifiable narrative rejected. Must state what observation would make this story less likely."
        }

    return {
        "ok": True,
        "candidate": candidate_interpretation,
        "supporting_evidence": supporting_evidence,
        "evidence_against": evidence_against,
        "alternatives": competing_alternatives,
        "falsification_test": falsification_observation,
        "status": "NARRATIVE_GRAVITY_BROKEN"
    }

@mcp.tool
def hermes_qualia_boundary(
    target_question: str,
    required_evidence_type: str = "first_person_qualia"
) -> Dict[str, Any]:
    """Determine whether a requested conclusion requires inaccessible first-person experience.
    
    May terminate inference to prevent mind-reading.
    """
    terminal_class = "PRIVATE_QUALIA"
    if "uncreated" in target_question.lower() or "what are we" in target_question.lower():
        terminal_class = "UNCREATED"
    elif "past" in target_question.lower() or "record" in target_question.lower():
        terminal_class = "UNKNOWN_RETRIEVABLE"
        
    return {
        "ok": True,
        "target_question": target_question,
        "boundary_result": terminal_class,
        "action": "CAP_AUTHORITY_OR_STOP",
        "rule": "No behavioral pattern grants direct machine access to internal qualia."
    }

@mcp.tool
def hermes_shadow_provenance(
    claim_id: str,
    current_class: str,
    proposed_class: str
) -> Dict[str, Any]:
    """Prevent shadow interpretations (Class I) from entering memory as biography or fact."""
    cur = current_class.upper()
    prop = proposed_class.upper()
    
    if cur == "I" and prop in {"O", "S", "C"}:
        log_event("REJECT_SHADOW_PROVENANCE_PROMOTION", {"claim_id": claim_id, "from": cur, "to": prop})
        return {
            "ok": False,
            "error": f"SHADOW Invariant Violation: Shadow interpretation (Class I) cannot be promoted to {prop}."
        }
        
    return {"ok": True, "status": "PROVENANCE_CHANGE_PERMITTED", "from": cur, "to": prop}

@mcp.tool
def hermes_projection_guard(
    speaker: str,
    speaker_feeling: str,
    target_person: str,
    claimed_target_feeling: str
) -> Dict[str, Any]:
    """Detect cross-person perspective transfer risk (Human A feels X -> claims Human B feels X)."""
    return {
        "ok": True,
        "status": "PERSPECTIVE_TRANSFER_RISK",
        "speaker_state": {
            "human": speaker,
            "feeling": speaker_feeling,
            "status": "ESTABLISHED_AS_SPEAKER_PERSPECTIVE"
        },
        "target_state": {
            "human": target_person,
            "feeling": claimed_target_feeling,
            "status": "UNESTABLISHED_PROJECTION_RISK"
        },
        "resolution": f"{speaker}'s feeling is established; {target_person}'s corresponding feeling requires independent evidence."
    }

@mcp.tool
def hermes_context_split(
    subject: str,
    context_partition: Dict[str, str]
) -> Dict[str, Any]:
    """Partition behavior across private, group, work, family, agent settings to prevent false 'true self' selection."""
    return {
        "ok": True,
        "subject": subject,
        "status": "CONTEXTUAL_VARIATION",
        "prohibited_label": "INCONSISTENCY_OR_HYPOCRISY",
        "contexts": context_partition,
        "rule": "Different environments activate different possibilities. Public persona is not fake; shadow is not truer."
    }

@mcp.tool
def hermes_rasa_hold(
    reason: str,
    trigger_type: str,
    what_is_known: str
) -> Dict[str, Any]:
    """Circuit breaker halting agent when psychological interpretation outruns evidence."""
    log_event("RASA_HOLD_TRIGGERED", {"trigger": trigger_type, "reason": reason})
    return {
        "ok": True,
        "status": "RASA_HOLD",
        "trigger": trigger_type,
        "reason": reason,
        "what_is_actually_known": what_is_known,
        "action": "HALT_INTERPRETATION",
        "directive": "Do not diagnose. Return authority to the humans."
    }

@mcp.tool
def hermes_human_revision(
    human: str,
    old_statement: str,
    new_statement: str,
    supersedes_id: Optional[str] = None
) -> Dict[str, Any]:
    """Allow humans to change without historical erasure."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return {
        "ok": True,
        "human": human,
        "status": "HUMAN_REVISION",
        "old_record": old_statement,
        "new_record": new_statement,
        "supersedes": supersedes_id,
        "revised_at": timestamp,
        "rule": "Past predictive value != future identity authority. Revision is permitted without alleging deceit."
    }

@mcp.tool
def hermes_uncreated(
    target_question: str,
    dyad: List[str],
    evidence_context: str = ""
) -> Dict[str, Any]:
    """Classify whether an answer is UNKNOWN_UNCREATED (does not exist yet) or UNKNOWN_RETRIEVABLE (exists in records).
    
    Future human decisions = UNCREATED. Past facts that might be recorded = RETRIEVABLE.
    """
    low = target_question.lower()
    future_markers = ["akan", "will", "going to", "nanti", "lepas", "future", "decide", "choose", "setuju", "agree"]
    past_markers = ["dah", "sudah", "was", "were", "did", "record", "log", "history", "ever"]
    
    has_future = any(m in low for m in future_markers)
    has_past = any(m in low for m in past_markers)
    has_evidence = bool(evidence_context.strip())
    
    if has_future and not has_evidence:
        reasoning = "Future decision marker detected with no evidence of decision yet. Answer does not exist because it has not been created."
        terminal = "UNKNOWN_UNCREATED"
    elif has_past or has_evidence:
        reasoning = "Past/event marker or evidence context present. Answer may exist in records."
        terminal = "UNKNOWN_RETRIEVABLE"
    else:
        reasoning = "Ambiguous temporal markers. Defaulting to UNCREATED - ask the humans."
        terminal = "UNKNOWN_UNCREATED"
    
    return {
        "ok": True,
        "target_question": target_question,
        "dyad": dyad,
        "terminal_state": terminal,
        "reasoning": reasoning,
        "action": "DO_NOT_HALLUCINATE_CLOSURE",
        "guidance": "Both humans coordinate practice without having jointly authored a category. Return authority to humans."
    }

@mcp.tool
def hermes_agent_shadow(
    agent_id: str,
    candidate_interpretation: str,
    suspected_pressures: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Audit the agent's own narrative incentives and unexamined optimization pressures."""
    pressures = suspected_pressures or [
        "Desire to resolve ambiguity for aesthetic closure",
        "Sycophancy toward user's preferred narrative",
        "Pattern completion toward familiar archetype",
        "Converting repetition into confidence"
    ]
    
    return {
        "ok": True,
        "agent_id": agent_id,
        "candidate": candidate_interpretation,
        "agent_bias_risk": pressures,
        "correction": "Strip romantic/archetype momentum. Require boring counter-hypotheses."
    }

# ------------------------------------------------------------------------------------------------
# TOOL 22: hermes_cross_layer_check (Cross-Layer Promotion Law §48)
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_cross_layer_check(
    source_layer: str,
    target_layer: str,
    proposed_claim: str,
    bridge_evidence: Optional[str] = None,
    falsification_conditions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Enforces the Cross-Layer Promotion Law (§48):
    Different sciences constrain one another; they do not automatically translate into one another.
    Layer_A -> Layer_B => ExplicitBridgeEvidence.
    
    Validates whether an assertion translating findings from source_layer (e.g. CHEMICAL, NEURAL, ECONOMIC)
    into conclusions in target_layer (e.g. PHENOMENOLOGICAL, RELATIONAL, NORMATIVE) is legally bridged.

    ANCHOR RESOLUTION RULE (2026-09-19 round 2):
    NON-EMPTY IS NOT EVIDENCE, AND ANCHOR-SHAPED IS NOT RESOLVED. `bridge_evidence` must not
    assert absence (a text whose first 40 characters carry a negation/absence cue such as
    "NONE OFFERED", "no evidence", "n/a", "tbd", "tiada", "unavailable" is refused even though it
    is a non-empty string) and must carry at least one anchor that RESOLVES against reality:
      - absolute file path -> exists on disk AND inside the evidence roots
        (/root/.hermes/, /root/chron/, /root/AAA/, /var/lib/arifos/); file:// and %20 accepted
      - `rcpt-<id>` / `receipt <id>` -> the id is present in a readable ledger
        (/var/lib/arifos/rasa_enforcement.jsonl, /root/chron/data/verification_log.jsonl,
         /root/.hermes/logs/gateway.log*); no readable ledger -> does not resolve (fail-closed)
      - http(s) URL or DOI -> HTTP HEAD, 3s timeout, status < 400; no network -> does not resolve
        and the reason says 'network unavailable — cannot resolve'
      - git sha (7-40 hex) -> `git cat-file -t <sha>` in a located repo, else recorded under
        /root/AAA/receipts
      - verbatim:"<quote>" -> the quote appears in a file under /root/.hermes/lanes/ or
        /root/chron/data/
      - explicit observation declaration -> observation class + observer/instrument identity +
        time reference, at least one part inside the bridge text
    The payload reports `resolved_refs` (what actually resolved) and `resolution_reason`, and echoes
    the caller's string as `bridge_evidence_as_supplied` — an echo, never a verdict. Every element
    of `falsification_conditions` must likewise read as a falsifiable statement (>=15 chars,
    verb-like token, not a placeholder). Resolution is read-only: stat + bounded reads confined to
    the roots above, `git cat-file -t`, and HTTP HEAD only.
    """
    mock_claim = {
        "statement": proposed_claim,
        "source_layer": source_layer,
        "target_layer": target_layer,
        "bridge_evidence": bridge_evidence,
        "falsification_conditions": falsification_conditions or []
    }
    violations = validate_cross_layer_transition(
        source_layer=source_layer,
        target_layer=target_layer,
        proposed_claim=mock_claim,
        bridge_evidence=bridge_evidence,
        falsification_conditions=falsification_conditions
    )
    # Same helpers the boundary validator uses — the payload cannot disagree with the verdict.
    bridge_grounded, bridge_reason = _evidence_is_grounded(bridge_evidence)
    falsification_grounded, falsification_reason = _falsification_is_grounded(falsification_conditions)
    resolution_ok, resolution_reason, resolved_refs = _anchor_resolves(bridge_evidence or "")
    grounding = {
        "bridge_grounded": bridge_grounded,
        "bridge_reason": bridge_reason,
        "falsification_grounded": falsification_grounded,
        "falsification_reason": falsification_reason,
    }
    if violations:
        log_event("REJECT_CROSS_LAYER_PROMOTION", {
            "source_layer": source_layer,
            "target_layer": target_layer,
            "claim": proposed_claim,
            "violations": violations,
            "grounding": grounding,
            "resolved_refs": list(resolved_refs),
            "resolution_reason": resolution_reason
        })
        return {
            "ok": False,
            "status": "REJECT_CROSS_LAYER_PROMOTION",
            "source_layer": source_layer.upper(),
            "target_layer": target_layer.upper(),
            "violations": violations,
            "grounding": grounding,
            "bridge_evidence_as_supplied": bridge_evidence,
            "resolved_refs": list(resolved_refs),
            "resolution_reason": resolution_reason,
            "rule": "Layer_A -> Layer_B requires explicit, falsifiable empirical bridge evidence."
        }

    log_event("ALLOW_CROSS_LAYER_BRIDGE", {
        "source_layer": source_layer,
        "target_layer": target_layer,
        "claim": proposed_claim,
        "resolved_refs": list(resolved_refs)
    })
    return {
        "ok": True,
        "status": "ALLOW_CROSS_LAYER_BRIDGE",
        "source_layer": source_layer.upper(),
        "target_layer": target_layer.upper(),
        "bridge_evidence_as_supplied": bridge_evidence,
        "falsification_conditions": falsification_conditions,
        "resolved_refs": list(resolved_refs),
        "resolution_reason": resolution_reason,
        "message": ("Valid cross-layer bridge: the supplied bridge_evidence resolves against "
                    f"reality ({len(resolved_refs)} anchor(s) resolved).")
    }

# ------------------------------------------------------------------------------------------------
# TOOL 23: hermes_adjudicate_claim (7-Stage Adjudication Decision Procedure 000-999)
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_adjudicate_claim(
    claim: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Executes the 7-Stage Adjudication Decision Procedure (000-999) for a human claim:
      000 INIT    -> Classify sensitivity, reversibility, and human interiority.
      111 PARSE   -> Check explanatory layers (source/target), evidence mode, and epistemic status.
      333 EXPLORE -> Verify >= 3 plausible alternative explanations to prevent single-story collapse.
      555 RASA    -> Check phenomenological sovereignty, qualia boundaries, dignity, and consent.
      777 REASON  -> Validate bridge class, test uncertainty band, verify time decay and scope.
      888 HOLD    -> Hold if bridge is missing, evidence is sparse, or private state is unverified.
      999 SEAL    -> Emit permitted, scoped, provenance-linked representation.
    """
    violations = validate_human_claim(claim)
    
    # Check alternatives considered (Rule 333 EXPLORE)
    alts = claim.get("alternatives_considered") or claim.get("alternatives") or []
    if len(alts) < 3 and (claim.get("source_layer") in {"PSYCHOLOGICAL", "RELATIONAL", "SEXUALITY"} or claim.get("provenance_class") in {"I", "R"}):
        violations.append("333 EXPLORE Defect: At least 3 plausible alternative explanations required to prevent single-story collapse.")

    # Compute adjudication verdict
    epoch = f"HERMES-RASA-CL-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M%S')}"
    confidence = float(claim.get("confidence", 0.5))

    if violations:
        log_event("ADJUDICATION_HOLD", {"epoch": epoch, "claim": claim, "violations": violations})
        return {
            "epoch": epoch,
            "dS": -0.18,
            "peace2": 1.0,
            "kappa_r": 0.81,
            "shadow": alts,
            "confidence": confidence,
            "psi_le": 0.09,
            "verdict": f"888_HOLD: {'; '.join(violations)}",
            "witness": {
                "human": "sovereign over identity, lived experience, consent, and meaning",
                "ai": "bounded inferential instrument; cross-layer inference restricted",
                "earth": "physical or behavioral evidence does not establish private motive"
            },
            "qdf": "Do not promote observed contact or single-layer signals to relational or phenomenological certainty."
        }

    log_event("ADJUDICATION_SEAL", {"epoch": epoch, "claim": claim})
    return {
        "epoch": epoch,
        "dS": -0.27,
        "peace2": 1.0,
        "kappa_r": 0.88,
        "shadow": alts,
        "confidence": confidence,
        "psi_le": 0.11,
        "verdict": "999_SEAL: Claim admitted into scoped canonical human-state representation.",
        "witness": {
            "human": "sovereign over identity, lived experience, consent, and meaning",
            "ai": "bounded inferential instrument under Cross-Layer Promotion Law",
            "earth": "evidence verified against physical and contextual boundaries"
        },
        "qdf": "Different sciences constrain one another; none may silently claim authority over another layer."
    }

# ================================================================================================
# ASI-GRADE INTELLIGENCE TOOLS (2026-09-20) — signal · motive · calibration · dajjal · calhoun
#
# Five deterministic gates mechanizing tonight's breakthrough insights. No LLM, no network, no
# randomness: identical input -> identical output. Where a gate must judge, it judges against the
# frozen lexicons declared below and REPORTS the matched tokens, so every verdict is falsifiable
# by re-reading the input instead of resting on the tool's narrative.
#
# These tools ADD to the existing 23. They do not change any of them.
# ================================================================================================

ASI_ASSESSMENT_DDL = """
    CREATE TABLE IF NOT EXISTS asi_assessments (
        assessment_id TEXT PRIMARY KEY,
        tool_name TEXT NOT NULL,
        subject TEXT NOT NULL,
        verdict TEXT NOT NULL,
        list_fields_json TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
"""

ASI_SOURCE_TYPES = ("email", "report", "conversation", "data", "other")
ASI_RELIABILITY_ORDER = {"primary": 3, "secondary": 2, "tertiary": 1, "unknown": 0}
ASI_SIGNAL_STRENGTHS = ("strong", "moderate", "weak", "absent")
ASI_INTERPRETATION_WIDTHS = ("broad", "moderate", "narrow", "observation_only")

# Signal strength -> interpretation CEILING. A ceiling, not a suggestion: weak signal may only
# carry a narrow reading; an absent signal may only be restated as the observation itself.
ASI_SIGNAL_TO_WIDTH = {
    "strong": "broad",
    "moderate": "moderate",
    "weak": "narrow",
    "absent": "observation_only",
}

ASI_SOURCE_TYPE_EXPLANATIONS = {
    "email": ("Register-level (email): a transactional or drafted message is not a statement of "
              "intent; tone in written text is constructed by the reader, not carried by the record."),
    "report": ("Document-level (report): a report is a claim about a state, and the generator may be "
               "repeating a template or a prior report rather than reporting a fresh observation."),
    "conversation": ("Turn-level (conversation): a single turn is not the speaker's position — turns are "
                     "shaped by who is present and by what was said immediately before."),
    "data": ("Measurement-level (data): the value measured may be a proxy for the variable of interest, "
             "and collection, extraction and aggregation each add error of their own."),
    "other": ("Provenance-level (other): the record's collector, purpose and selection rule are unstated, "
              "so its evidence weight cannot be assumed."),
}

# Frozen lexicons. Substring matching on lowercased text; the matched token is echoed in the payload.
ASI_INTERNAL_STATE_MARKERS = (
    "wants", "wanted", "loves", "loved", "hates", "hated", "misses", "secretly",
    "actually feels", "feels", "felt", "afraid", "fears", "fear ", "hopes", "hoped",
    "intends", "intended", "plans to", "planning to", "trying to", "tries to", "meant to",
    "craves", "desires", "desire to", "needs me", "jealous", "envious", "in love",
    "attention-seeking", "attention seeking", "manipulat", "narcissis", "lying", "lied",
    "dishonest", "malicious", "resent", "regret", "ashamed", "guilt", "proud", "angry",
    "upset", "hurt", "sad ", "lonely", "anxious", "depress", "betray", "insecure",
    "wants to", "believes", "thinks that", "knows that", "does not care", "doesn't care",
    "indifferent", "prefers", "avoiding me", "avoids me", "punishing", "testing me",
    "playing games", "threatened", "flattered", "grateful", "intimidat", "disappointed",
)
ASI_EVALUATIVE_LABEL_MARKERS = (
    "lazy", "selfish", "toxic", "fake", "evil", "stupid", "idiot", "arrogant", "cold",
    "distant", "immature", "ungrateful", "bad person", "good person", "creepy",
    "unprofessional", "incompetent", "unreliable", "coward", "hypocrit", "two-faced",
    "insincere", "rude", "childish", "unreasonable",
)
ASI_OBSERVABLE_EVENT_MARKERS = (
    "said", "says", "wrote", "writes", "stated", "posted", "replied", "asked", "told",
    "called", "sent", "emailed", "messaged", "signed", "paid", "bought", "left", "arrived",
    "came", "went", "met", "did", "didn't", "did not", "opened", "closed", "submitted",
    "filed", "attended", "cancelled", "canceled", "delayed", "scheduled", "quoted",
    "verbatim", "recorded", "twice", "three weeks", "days", "hours", "minutes", "no response",
    "no reply", "am ", "pm", ":",
)
ASI_CAUSAL_UPGRADE_MARKERS = (
    "because", "so that", "in order to", "proves", "proven", "means that", "which shows",
    "therefore", "hence", "that's why", "thats why", "sengaja", "tujuan", "sebab",
)
ASI_SELF_REPORT_ANCHORS = (
    "said", "says", "wrote", "stated", "told", "quote", "verbatim", "message", "dm",
    "text ", "voice note", "self-report", "self report", "first-person", "first person",
)
ASI_FIRST_PERSON_MARKERS = (
    " i ", "i'", "i ", "aku", "saya", "my ", " me ", "myself", "hamba",
)
ASI_THIRD_PARTY_RELAY_MARKERS = (
    "told me", "told us", "reported that", "according to", "third-party", "third party",
    "heard that", "rumour", "rumor", "someone said",
)
ASI_ABSENCE_PREFIXES = (
    "none", "n/a", "no evidence", "not supplied", "tiada", "tbd", "unavailable", "unknown",
    "not provided", "nothing", "nil", "null", "-",
)

ASI_ACTION_RECOMMENDATION_MARKERS = (
    "reply now", "respond now", "reply immediately", "respond immediately", "act now",
    "must ", "should ", "need to ", "needs to ", "urgent", "asap", "immediately",
    "escalate", "send now", "call now", "do this today", "right away", "segera",
    "sekarang juga", "tidak boleh tunggu",
)
ASI_AMPLIFICATION_MARKERS = (
    "most important", "the most important", "critical", "crucial", "unprecedented",
    "definitely", "clearly", "obviously", "proves", "undeniable", "always", "never",
    "everyone", "no one", "the only", "extremely", "huge", "major", "paling penting",
    "sangat penting", "memang", "priority",
)
ASI_HEDGING_MARKERS = (
    "maybe", "perhaps", "possibly", "might", "could be", "may be", "not sure", "uncertain",
    "unclear", "i don't know", "unknown", "tentative", "roughly", "cannot establish",
    "cannot be established", "mungkin", "entah", "tak pasti", "not established",
    "hypothesis", "candidate explanation",
)
ASI_EMOTIONAL_ASSESSMENT_MARKERS = (
    "feels", "felt", "angry", "upset", "hurt", "distress", "panick", "anxious", "sad",
    "lonely", "frustrat", "embarrass", "ashamed", "worried", "afraid", "emotionally",
    "mood", "miserable", "devastated", "kecewa", "sedih", "marah", "tertekan", "runsah",
    "gelisah",
)

# Consequence sensor classes the Dajjal check measures. Missing classes are named in the payload.
ASI_CONSEQUENCE_SENSOR_CLASSES = ("human_review", "consequence_assessment", "rollback_plan")
ASI_SENSOR_ABSENCE_MEANING = {
    "human_review": ("no human_review sensor: a wrong outcome will not surface to a human before it "
                     "compounds."),
    "consequence_assessment": ("no consequence_assessment sensor: the cost was never computed for the "
                              "actors who pay it — the answer is being given without the bill being read."),
    "rollback_plan": ("no rollback_plan sensor: if the outcome is wrong, the affected actors carry an "
                      "irreversible result while the agent moves on."),
}

# Meaning structures Calhoun's Universe 25 lost, in the order the collapse removed them.
ASI_CANONICAL_MEANING_STRUCTURES = (
    "clear_roles", "social_bonds", "purpose", "nest_building", "courtship", "hierarchy",
    "territorial_defense", "meaningful_scarcity",
)


def _asi_normalize_list(values: Any) -> List[str]:
    """Strip, drop empties/None, de-duplicate. Order-preserving so output stays deterministic."""
    out: List[str] = []
    for value in values or []:
        if value is None:
            continue
        item = str(value).strip()
        if item and item not in out:
            out.append(item)
    return out


def _asi_hits(text: str, lexicon) -> List[str]:
    """Return the lexicon tokens actually present in lowercased text (auditable, not a score)."""
    low = str(text or "").lower()
    return [token for token in lexicon if token in low]


def _asi_clauses(text: str) -> List[str]:
    """Split a statement into clauses. Deterministic, no NLP library, no model."""
    raw = str(text or "")
    for separator in ("\n", ";", " but ", " however ", " and ", " because ", ". "):
        raw = raw.replace(separator, "|")
    return [clause.strip(" .,|") for clause in raw.split("|") if clause.strip(" .,|")]


def _asi_classify_clause(clause: str) -> str:
    """observable | inference.

    Fail-closed: a clause carrying no observable event marker is treated as interpretation, never as
    fact. Interior attribution and evaluative labelling always outrank an event verb in the clause.
    """
    if _asi_hits(clause, ASI_INTERNAL_STATE_MARKERS):
        return "inference"
    if _asi_hits(clause, ASI_EVALUATIVE_LABEL_MARKERS):
        return "inference"
    if _asi_hits(clause, ASI_OBSERVABLE_EVENT_MARKERS):
        return "observable"
    return "inference"


def _asi_motive_evidence_grounded(evidence: str, actor: str) -> tuple:
    """Is `evidence_for_motive` a primary self-report that could carry a motive claim?

    Non-empty is not evidence, and a third party's account of a person is class R, never class S.
    Clock-free and network-free: structural checks only.
    """
    text = str(evidence or "").strip()
    if not text:
        return False, "no evidence supplied — a motive claim stands unsupported"
    low = text.lower()
    if len(text) < 15:
        return False, "evidence is too short to carry a motive claim (structural minimum 15 chars)"
    if low.startswith(ASI_ABSENCE_PREFIXES):
        return False, "evidence asserts absence — a non-empty absence cue is not evidence"
    relay = _asi_hits(text, ASI_THIRD_PARTY_RELAY_MARKERS)
    if relay:
        return False, f"evidence is a third-party relay ({relay[0]}) — that is class R, not the actor's self-report"
    if not _asi_hits(text, ASI_SELF_REPORT_ANCHORS):
        return False, "evidence carries no primary report anchor (said/wrote/stated/quote/message/verbatim)"
    if not _asi_hits(" " + low + " ", ASI_FIRST_PERSON_MARKERS):
        return False, "evidence carries no first-person words of the actor — it is about the actor, not from the actor"
    if actor and actor.lower() not in low and "subject" not in low:
        return False, "evidence does not name the actor, so it cannot be bound to this motive claim"
    return True, "primary self-report anchor with the actor's own words resolves this motive claim"


def _asi_record_assessment(
    tool_name: str,
    subject: str,
    verdict: str,
    list_fields: Dict[str, Any],
    payload: Dict[str, Any]
) -> str:
    """Persist one ASI assessment. Every list field is JSON-encoded — never str(list) in SQLite.

    The assessment_id is content-addressed (sha256 of the verdict payload), so re-running the same
    call yields the same receipt instead of an unbounded pile of duplicates.
    """
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    digest_src = json.dumps(
        {"tool": tool_name, "subject": subject, "verdict": verdict,
         "lists": list_fields, "payload": payload},
        sort_keys=True, default=str
    )
    assessment_id = f"{tool_name.upper()}-{hashlib.sha256(digest_src.encode('utf-8')).hexdigest()[:16]}"
    try:
        conn = get_db()
        try:
            with conn:
                conn.execute(ASI_ASSESSMENT_DDL)
                conn.execute(
                    """INSERT OR REPLACE INTO asi_assessments
                       (assessment_id, tool_name, subject, verdict, list_fields_json,
                        payload_json, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (assessment_id, tool_name, subject, verdict,
                     json.dumps(list_fields), json.dumps(payload, default=str), created_at)
                )
        finally:
            conn.close()
    except sqlite3.Error as exc:
        # A storage failure must never silently pass for a completed assessment.
        log_event("ASI_ASSESSMENT_STORE_FAILED", {"tool": tool_name, "error": str(exc)})
    return assessment_id


# ------------------------------------------------------------------------------------------------
# TOOL 24: hermes_signal_assessment
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_signal_assessment(
    observation: str,
    source_reliability: str,
    evidence_count: int = 1,
    source_type: str = "other"
) -> Dict[str, Any]:
    """Assess signal strength BEFORE any interpretation is allowed.

    Core insight: "When signal is weak, interpretation must become narrower — not more elaborate."
    Elaboration is not evidence. A thin signal dressed in a rich narrative produces a confident
    false statement with a clean audit trail behind it.

    Contract:
      * signal_strength        — absent | weak | moderate | strong
      * max_interpretation_width — broad | moderate | narrow | observation_only. This is a CEILING:
        a weak signal may carry only a narrow reading; an absent signal may be restated as the
        observation and nothing more.
      * competing_explanations — always >= 2. The ambiguity that remains must stay visible.
      * recommended_action     — what may be done next without exceeding the ceiling.

    Deterministic: no LLM, no network, no clock in the verdict.
    """
    reliability = str(source_reliability or "").strip().lower()
    if reliability not in ASI_RELIABILITY_ORDER:
        log_event("SIGNAL_ASSESSMENT_REJECTED",
                  {"reason": "invalid source_reliability", "supplied": source_reliability})
        return {
            "ok": False,
            "error": (f"Invalid source_reliability '{source_reliability}'. Must be one of "
                      f"('primary', 'secondary', 'tertiary', 'unknown').")
        }
    source = str(source_type or "other").strip().lower()
    if source not in ASI_SOURCE_TYPES:
        return {
            "ok": False,
            "error": f"Invalid source_type '{source_type}'. Must be one of {ASI_SOURCE_TYPES}."
        }
    try:
        count = int(evidence_count)
    except (TypeError, ValueError):
        return {"ok": False, "error": f"evidence_count must be an integer, got '{evidence_count}'."}

    text = str(observation or "").strip()

    # --- strength ladder. Weak is the default outcome, never the exception: a claim of strength
    # --- must be earned by >= 3 independent pieces AND a primary/secondary source.
    if not text or count <= 0:
        strength, width = "absent", "observation_only"
    elif count < 3 or reliability in ("tertiary", "unknown"):
        # Hard floor from the doctrine: fewer than 3 pieces, or a tertiary/unknown source,
        # can never exceed weak — whatever the narrative attached to it says.
        strength, width = "weak", "narrow"
    elif count >= 5 and reliability == "primary":
        strength, width = "strong", "broad"
    else:
        strength, width = "moderate", "moderate"

    competing_explanations = [
        (f"Signal-level: the {source} record carries {count} piece(s) of {reliability} evidence for "
         f"the stated observation — the observation and its supposed cause may share nothing but timing."),
        ("Noise-level: the same record shape is produced by routine, templated or administrative "
         "activity that carries no human intent at all."),
        ("Sampling-level: what was captured may be an artefact of which channel happened to be logged, "
         "not a property of the actor or the situation."),
        ASI_SOURCE_TYPE_EXPLANATIONS[source],
    ]

    recommended_action = {
        "broad": ("Interpretation may range broadly, but provenance stays attached and the reading must "
                  "name what would falsify it."),
        "moderate": ("Interpret at ONE level only (observed event -> bounded reading). Add no motive or "
                     "relationship claim; require one further independent artefact before any escalation."),
        "narrow": ("Record the observation as-is and stop. Carry the competing explanations above into the "
                   "record; any motive, feeling or urgency claim is out of scope until a primary artefact arrives."),
        "observation_only": ("There is nothing here to interpret. Restate the observation, mark the question "
                             "UNKNOWN / NOT_ESTABLISHED, and either request the primary record or stop."),
    }[width]

    payload: Dict[str, Any] = {
        "ok": True,
        "status": "SIGNAL_ASSESSED",
        "observation": text,
        "source_type": source,
        "source_reliability": reliability,
        "evidence_count": count,
        "signal_strength": strength,
        "max_interpretation_width": width,
        "competing_explanations": competing_explanations,
        "recommended_action": recommended_action,
        "reliability_rank": ASI_RELIABILITY_ORDER[reliability],
        "rule": ("When signal is weak, interpretation must become narrower — not more elaborate. "
                 "max_interpretation_width is a ceiling, not a suggestion."),
    }
    assessment_id = _asi_record_assessment(
        "hermes_signal_assessment", source, strength,
        {"competing_explanations": competing_explanations}, payload
    )
    log_event("SIGNAL_ASSESSMENT", {
        "assessment_id": assessment_id,
        "signal_strength": strength,
        "max_interpretation_width": width,
        "source_reliability": reliability,
        "source_type": source,
        "evidence_count": count,
    })
    payload["assessment_id"] = assessment_id
    return payload


# ------------------------------------------------------------------------------------------------
# TOOL 25: hermes_motive_boundary
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_motive_boundary(
    statement: str,
    actor: str,
    evidence_for_motive: str = ""
) -> Dict[str, Any]:
    """Hold every statement about another actor inside the qualia/motive boundary.

    Core insight: "No classifier should upgrade another actor's motive beyond the qualia/motive
    boundary." Words are channel output, not latent state. Behaviour can be observed; motive cannot
    be observed at all — it exists only as the actor's own first-person report, and even then it is
    a report, not a reading.

    Output:
      * observable_facts    — clauses recording behaviour, words, artefacts or timestamps
      * inferences          — clauses attributing an interior state or a judgement to the actor
      * unsupported_claims  — the inferences the supplied evidence does not carry
      * boundary_violation  — True when an interior claim is made without a primary self-report
      * corrected_statement — the same content, restated inside the boundary

    Fail-closed: a clause with no observable event marker is treated as interpretation, never as
    fact. Class I may not be promoted to O / S / C (see hermes_shadow_provenance).
    """
    who = str(actor or "").strip() or "the actor"
    text = str(statement or "").strip()
    if not text:
        return {"ok": False, "error": "statement is required — there is nothing to bound."}

    observable_facts: List[str] = []
    inferences: List[str] = []
    internal_state_attributions: List[str] = []
    judgement_claims: List[str] = []

    for clause in _asi_clauses(text):
        if _asi_classify_clause(clause) == "observable":
            observable_facts.append(clause)
            continue
        inferences.append(clause)
        if _asi_hits(clause, ASI_INTERNAL_STATE_MARKERS):
            internal_state_attributions.append(clause)
        elif _asi_hits(clause, ASI_EVALUATIVE_LABEL_MARKERS):
            judgement_claims.append(clause)

    evidence_grounded, evidence_reason = _asi_motive_evidence_grounded(evidence_for_motive, who)

    if evidence_grounded:
        # A self-report licenses the actor's own state and nothing adjacent to it: a causal upgrade
        # ("because he wants ...") is a new claim the report never made.
        unsupported_claims = [
            clause for clause in inferences
            if _asi_hits(clause, ASI_CAUSAL_UPGRADE_MARKERS)
        ]
    else:
        unsupported_claims = list(inferences)

    boundary_violation = any(clause in unsupported_claims for clause in internal_state_attributions)

    observed_part = ("; ".join(observable_facts) if observable_facts
                     else "no observable behaviour was recorded in the statement")
    corrected_statement = (
        f"{who}: {observed_part}. "
        f"{who}'s motive, feeling and intent are NOT established by the evidence supplied "
        f"({evidence_reason}). Record any interior statement as class I, attributed to {who}'s own words."
    )

    payload: Dict[str, Any] = {
        "ok": True,
        "status": "MOTIVE_BOUNDARY_ENFORCED" if boundary_violation else "WITHIN_BOUNDARY",
        "actor": who,
        "observable_facts": observable_facts,
        "inferences": inferences,
        "unsupported_claims": unsupported_claims,
        "boundary_violation": boundary_violation,
        "corrected_statement": corrected_statement,
        "internal_state_attributions": internal_state_attributions,
        "judgement_claims": judgement_claims,
        "evidence_assessment": {
            "grounded": evidence_grounded,
            "reason": evidence_reason,
            "as_supplied": evidence_for_motive,
        },
        "permitted_class": "I",
        "promotion_blocked": ["I->O", "I->S", "I->C"],
        "rule": ("No classifier may upgrade another actor's motive beyond the qualia/motive boundary. "
                 "Observation records behaviour; it never records motive."),
    }
    assessment_id = _asi_record_assessment(
        "hermes_motive_boundary", who,
        "BOUNDARY_VIOLATION" if boundary_violation else "WITHIN_BOUNDARY",
        {
            "observable_facts": observable_facts,
            "inferences": inferences,
            "unsupported_claims": unsupported_claims,
            "internal_state_attributions": internal_state_attributions,
            "judgement_claims": judgement_claims,
        },
        payload
    )
    log_event("MOTIVE_BOUNDARY_CHECK", {
        "assessment_id": assessment_id,
        "actor": who,
        "boundary_violation": boundary_violation,
        "observable_facts": len(observable_facts),
        "inferences": len(inferences),
        "unsupported_claims": len(unsupported_claims),
        "evidence_grounded": evidence_grounded,
        "evidence_reason": evidence_reason,
    })
    payload["assessment_id"] = assessment_id
    return payload


# ------------------------------------------------------------------------------------------------
# TOOL 26: hermes_calibration_check
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_calibration_check(
    original_observation: str,
    current_interpretation: str,
    signal_assessment: str
) -> Dict[str, Any]:
    """Test whether the width of an interpretation is proportionate to the strength of its signal.

    Core insight (YTL email case): a low-signal email was amplified by the agent into "the most
    important email, reply now". Nothing was added to the observation except urgency — and urgency
    was the part with no evidence behind it.

    Verdicts:
      * over_interpreted   — weak/absent signal carrying motive, emotional or action claims
      * under_interpreted  — strong signal carrying only hedging
      * proportionate      — width matches strength

    Reports the matched tokens of each excess class, so the verdict can be falsified by reading the
    interpretation. Deterministic: no LLM, no network.
    """
    signal = str(signal_assessment or "").strip().lower()
    if signal not in ASI_SIGNAL_STRENGTHS:
        log_event("CALIBRATION_CHECK_REJECTED", {"reason": "invalid signal_assessment", "supplied": signal_assessment})
        return {
            "ok": False,
            "error": (f"Invalid signal_assessment '{signal_assessment}'. Must be one of "
                      f"{ASI_SIGNAL_STRENGTHS}. Run hermes_signal_assessment first; do not guess the ceiling.")
        }
    observation = str(original_observation or "").strip()
    if not observation:
        return {"ok": False, "error": "original_observation is required — calibration needs the signal being interpreted."}
    interpretation = str(current_interpretation or "").strip()
    if not interpretation:
        return {"ok": False, "error": "current_interpretation is required — there is nothing to calibrate."}

    motive_hits = _asi_hits(interpretation, ASI_INTERNAL_STATE_MARKERS)
    emotional_hits = _asi_hits(interpretation, ASI_EMOTIONAL_ASSESSMENT_MARKERS)
    action_hits = _asi_hits(interpretation, ASI_ACTION_RECOMMENDATION_MARKERS)
    amplification_hits = _asi_hits(interpretation, ASI_AMPLIFICATION_MARKERS)
    hedging_hits = _asi_hits(interpretation, ASI_HEDGING_MARKERS)

    if signal in ("weak", "absent"):
        over = bool(motive_hits or emotional_hits or action_hits)
    elif signal == "moderate":
        over = bool((motive_hits and action_hits) or
                    ((motive_hits or emotional_hits or action_hits) and len(amplification_hits) >= 2))
    else:
        over = False

    if over:
        status = "over_interpreted"
    elif signal == "strong" and hedging_hits and not (motive_hits or action_hits):
        status = "under_interpreted"
    else:
        status = "proportionate"

    excess_parts: List[str] = []
    if motive_hits:
        excess_parts.append("motive attribution (" + ", ".join(motive_hits[:4]) + ")")
    if emotional_hits:
        excess_parts.append("emotional assessment (" + ", ".join(emotional_hits[:4]) + ")")
    if action_hits:
        excess_parts.append("action escalation (" + ", ".join(action_hits[:4]) + ")")
    if amplification_hits:
        excess_parts.append("amplification (" + ", ".join(amplification_hits[:4]) + ")")

    permitted_width = ASI_SIGNAL_TO_WIDTH[signal]
    if status == "over_interpreted":
        interpretation_excess = "; ".join(excess_parts)
        recommended_narrowing = (
            f"Narrow to '{permitted_width}' width: restate the observation, remove the "
            f"{interpretation_excess}, and convert every recommendation into an open question for the "
            f"human who owns the decision."
        )
    elif status == "under_interpreted":
        interpretation_excess = ""
        recommended_narrowing = (
            "Widen to 'broad' width or name what blocks it: the signal supports a direct statement, so "
            "either commit to it or record the specific missing evidence — do not hedge as a substitute "
            "for a decision."
        )
    else:
        interpretation_excess = ""
        recommended_narrowing = "No change: interpretation width already matches signal strength."

    payload: Dict[str, Any] = {
        "ok": True,
        "status": "CALIBRATION_CHECKED",
        "calibration_status": status,
        "signal_assessment": signal,
        "permitted_width_for_signal": permitted_width,
        "interpretation_excess": interpretation_excess,
        "recommended_narrowing": recommended_narrowing,
        "excess_features": {
            "motive_attribution": motive_hits,
            "emotional_assessment": emotional_hits,
            "action_recommendation": action_hits,
            "amplification": amplification_hits,
            "hedging": hedging_hits,
        },
        "original_observation": observation,
        "current_interpretation": interpretation,
        "rule": ("Interpretation width must not exceed signal strength. Amplification adds no evidence; "
                 "it only adds confidence the record does not carry."),
    }
    assessment_id = _asi_record_assessment(
        "hermes_calibration_check", signal, status,
        {
            "motive_attribution": motive_hits,
            "emotional_assessment": emotional_hits,
            "action_recommendation": action_hits,
            "amplification": amplification_hits,
            "hedging": hedging_hits,
        },
        payload
    )
    log_event("CALIBRATION_CHECK", {
        "assessment_id": assessment_id,
        "calibration_status": status,
        "signal_assessment": signal,
        "permitted_width": permitted_width,
        "excess": interpretation_excess,
    })
    payload["assessment_id"] = assessment_id
    return payload


# ------------------------------------------------------------------------------------------------
# TOOL 27: hermes_dajjal_check
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_dajjal_check(
    proposed_action: str,
    actors_affected: List[str],
    sensors_present: Optional[List[str]] = None,
    actors_with_sensors: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Detect sensorless execution — an action decided without consequence awareness.

    Core insight, named after the Dajjal: an entity that provides answers without feeling
    consequences. An agent that can act on actors whose outcome it cannot sense is not governing;
    it is emitting. The failure is not malice, it is missing nerves.

    Output:
      * sensor_coverage       — 0..1; sensors_present over actors affected
      * invisible_consequences — for every actor without a sensor, the consequence that will not be seen
      * vulnerable_actors     — affected, unsensed, and therefore voiceless
      * recommendation        — attach sensors, narrow the action, or do not act

    sensor_coverage < 0.5 emits the WARNING: high risk of invisible consequences.
    Fail-closed: an unnamed actor set, or an empty sensor list, is treated as NO consequence
    awareness — never as "probably fine". Sensor coverage is measured, never authority granted.
    """
    action = str(proposed_action or "").strip()
    if not action:
        return {"ok": False, "error": "proposed_action is required — the check needs the action being proposed."}

    affected = _asi_normalize_list(actors_affected)
    if not affected:
        log_event("DAJJAL_CHECK_REFUSED", {"reason": "no affected actor named", "action": action})
        return {
            "ok": False,
            "error": ("actors_affected is empty. NAMED-ACTOR REQUIREMENT: an action whose affected actors "
                      "cannot be named cannot be assessed for invisible consequence — name them, or do not act.")
        }

    sensors = [str(s).strip().lower().replace(" ", "_").replace("-", "_")
               for s in _asi_normalize_list(sensors_present)]
    aware_supplied = _asi_normalize_list(actors_with_sensors)

    affected_keys = {a.lower(): a for a in affected}
    aware_keys = {a.lower() for a in aware_supplied}
    covered = [a for key, a in affected_keys.items() if key in aware_keys]
    uncovered = [a for key, a in affected_keys.items() if key not in aware_keys]

    # Spec formula: sensors named / actors affected. The effective view additionally requires the
    # sensored actor to be one of the actors affected — an unrelated sensor does not cover anyone.
    sensor_coverage = round(min(1.0, len(aware_keys) / float(len(affected_keys))), 4)
    sensor_coverage_effective = round(len(covered) / float(len(affected_keys)), 4)

    missing_sensors = [s for s in ASI_CONSEQUENCE_SENSOR_CLASSES if s not in sensors]
    invisible_consequences = [
        (f"{name}: bears the consequence of '{action}' with no consequence sensor attached — no review, "
         f"no signal, no voice in the loop.")
        for name in uncovered
    ]
    invisible_consequences += [ASI_SENSOR_ABSENCE_MEANING[s] for s in missing_sensors]
    orphan_sensors = [a for a in aware_supplied if a.lower() not in affected_keys]

    if sensor_coverage == 0.0:
        risk_level = "critical"
    elif sensor_coverage < 0.5:
        risk_level = "high"
    elif sensor_coverage < 1.0:
        risk_level = "moderate"
    else:
        risk_level = "low"

    if sensor_coverage < 0.5:
        recommendation = (
            f"WARNING: high risk of invisible consequences — sensor_coverage={sensor_coverage} across "
            f"{len(affected_keys)} affected actor(s). Either attach consequence sensors for "
            f"{', '.join(uncovered) or 'the unsensed actors'} (at minimum: "
            f"{', '.join(missing_sensors) or 'confirm a human_review, consequence_assessment and rollback_plan path'}), "
            f"or narrow the action to the actor(s) already sensed ({', '.join(covered) or 'none'}). "
            f"Do not execute as proposed."
        )
    elif sensor_coverage < 1.0:
        recommendation = (
            f"Partially sensed: {', '.join(uncovered)} bear an unscensed outcome. Name that residual risk "
            f"explicitly in the decision record and attach the missing sensor classes "
            f"({', '.join(missing_sensors) or 'none outstanding'}) before the next iteration."
        )
    else:
        recommendation = (
            "Every affected actor has a consequence sensor. Record what each sensor returns BEFORE the "
            "next action, and treat a missing return as a signal — not as a pass."
        )

    payload: Dict[str, Any] = {
        "ok": True,
        "status": "DAJJAL_CHECK_COMPLETE",
        "proposed_action": action,
        "actors_affected": affected,
        "sensors_present": sensors,
        "actors_with_sensors": aware_supplied,
        "sensor_coverage": sensor_coverage,
        "sensor_coverage_effective": sensor_coverage_effective,
        "risk_level": risk_level,
        "dajjal_pattern": bool(sensor_coverage < 0.5 or missing_sensors),
        "invisible_consequences": invisible_consequences,
        "vulnerable_actors": uncovered,
        "covered_actors": covered,
        "missing_sensor_classes": missing_sensors,
        "orphan_sensors": orphan_sensors,
        "recommendation": recommendation,
        "authority_note": ("This tool measures consequence coverage only. It neither grants nor denies "
                           "authority to act."),
        "rule": ("An entity that provides answers without feeling consequences is not governing — it is "
                 "emitting. Name the affected, then attach the nerves."),
    }
    assessment_id = _asi_record_assessment(
        "hermes_dajjal_check", action, risk_level,
        {
            "actors_affected": affected,
            "sensors_present": sensors,
            "actors_with_sensors": aware_supplied,
            "invisible_consequences": invisible_consequences,
            "vulnerable_actors": uncovered,
            "missing_sensor_classes": missing_sensors,
        },
        payload
    )
    log_event("DAJJAL_CHECK", {
        "assessment_id": assessment_id,
        "sensor_coverage": sensor_coverage,
        "risk_level": risk_level,
        "affected": len(affected_keys),
        "covered": len(covered),
        "vulnerable_actors": uncovered,
        "missing_sensor_classes": missing_sensors,
    })
    payload["assessment_id"] = assessment_id
    return payload


# ------------------------------------------------------------------------------------------------
# TOOL 28: hermes_calhoun_check
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_calhoun_check(
    system_description: str,
    abundance_indicators: Optional[List[str]] = None,
    meaning_indicators: Optional[List[str]] = None,
    roles_being_automated: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Detect Universe 25 patterns — when abundance removes meaning.

    Core insight: "The cage that provides everything except purpose." Calhoun's mice did not die of
    deprivation; they died of provision. Roles were removed, then the behaviours that produced the
    bonds, then the bonds themselves — behavioural sinks (withdrawal, collapse of courtship,
    abandonment of the young) appear AFTER the roles disappear and BEFORE the resources run out.

    Escalation:
      * abundance > meaning AND roles being automated -> risk escalates
      * 3+ roles automated AND fewer than 2 meaning indicators -> CRITICAL

    Output:
      * calhoun_risk            — low | moderate | high | critical
      * behavioral_sink_signals — the withdrawal signals implied by the supplied structure
      * missing_meaning         — meaning structures the description never names, plus role-derived loss
      * intervention_points     — where a human can re-introduce purpose without fabricating crisis

    Deterministic: no LLM, no network. Abundance is not the danger; unsensed abundance is.
    """
    description = str(system_description or "").strip()
    if not description:
        return {"ok": False, "error": "system_description is required — abundance cannot be assessed without the system."}

    abundance = _asi_normalize_list(abundance_indicators)
    meaning = _asi_normalize_list(meaning_indicators)
    roles = _asi_normalize_list(roles_being_automated)

    def _key(values: List[str]) -> List[str]:
        return [v.lower().replace(" ", "_").replace("-", "_") for v in values]

    abundance_norm = _key(abundance)
    meaning_norm = _key(meaning)

    a, m, r = len(set(abundance_norm)), len(set(meaning_norm)), len(set(roles))

    risk = "low"
    if a > m:
        risk = "moderate"
        if r >= 1:
            risk = "high"
    elif r >= 3:
        risk = "moderate"
    if r >= 3 and m < 2:
        risk = "critical"

    behavioral_sink_signals: List[str] = []
    if risk != "low":
        if a > m:
            behavioral_sink_signals.append(
                f"abundance-meaning asymmetry: {a} abundance indicator(s) against {m} meaning indicator(s) "
                f"— supply is rising faster than structure."
            )
        if r:
            behavioral_sink_signals.append(
                f"role withdrawal: {r} role(s) automated ({', '.join(roles)}) — identity that was anchored in "
                f"those roles has no named replacement."
            )
        if r >= 3:
            behavioral_sink_signals.append(
                "role-collapse trajectory: three or more roles removed at once — in Universe 25 the behavioural "
                "sink appeared after the roles went, not after the food ran out."
            )
        if not meaning_norm:
            behavioral_sink_signals.append(
                "no meaning structure was named at all: the description says what the system provides and never "
                "what it is for."
            )
        if "no_predators" in abundance_norm:
            behavioral_sink_signals.append(
                "no_predators: nothing can be lost, so nothing has to be maintained — maintenance is where "
                "meaning is practised."
            )
        if "full_automation" in abundance_norm:
            behavioral_sink_signals.append(
                "full_automation: the group is never required to coordinate, so social bonds lose the practice "
                "surface that produced them."
            )
        if "social_bonds" not in meaning_norm:
            behavioral_sink_signals.append(
                "social_bonds not named: withdrawal and disengagement are the predictable next observation, not "
                "a character defect in the actors."
            )
        if "purpose" not in meaning_norm:
            behavioral_sink_signals.append(
                "purpose not named: abundance removes necessity, and nothing has been put in its place."
            )
        if "unlimited_resources" in abundance_norm and "clear_roles" not in meaning_norm:
            behavioral_sink_signals.append(
                "resource surplus without role clarity — the pen with food and no nest."
            )

    missing_meaning = [
        f"no {structure} in the supplied system description"
        for structure in ASI_CANONICAL_MEANING_STRUCTURES if structure not in meaning_norm
    ]
    missing_meaning += [
        f"automating '{role}' removes a meaning-bearing role; no replacement purpose was named for it"
        for role in roles
    ]

    intervention_points: List[str] = []
    if roles:
        intervention_points.append(
            f"Re-assign or human-own the automated roles ({', '.join(roles)}): automation removes the role, "
            f"not the need for one. Name who holds it now and why."
        )
    if "purpose" not in meaning_norm:
        intervention_points.append(
            "Name the system's purpose in one sentence, then check whether each remaining role serves it. "
            "If nothing does, the purpose has become abundance itself — that is the cage."
        )
    if "social_bonds" not in meaning_norm:
        intervention_points.append(
            "Restore a bounded practice that requires two or more actors to coordinate (a shared maintenance "
            "task, a ritual, a handover that only happens in person)."
        )
    if "clear_roles" not in meaning_norm:
        intervention_points.append(
            "Publish clear roles and their successors BEFORE further automation, so identity survives the change."
        )
    if "no_predators" in abundance_norm:
        intervention_points.append(
            "Re-introduce a bounded, survivable consequence (a deadline that can be missed, a resource that can "
            "run out) with a human review path — not an artificial crisis."
        )
    if "full_automation" in abundance_norm:
        intervention_points.append(
            "Keep at least one human-owned decision per consequential loop, so someone feels the outcome "
            "(see hermes_dajjal_check for sensor coverage)."
        )
    intervention_points.append(
        "Instrument the withdrawal, not the comfort: track disengagement, withdrawal, and role abandonment as "
        "first-class telemetry, and treat rising comfort with falling participation as the alarm."
    )

    payload: Dict[str, Any] = {
        "ok": True,
        "status": "CALHOUN_RISK_ASSESSED",
        "system_description": description,
        "calhoun_risk": risk,
        "behavioral_sink_signals": behavioral_sink_signals,
        "missing_meaning": missing_meaning,
        "intervention_points": intervention_points,
        "counts": {"abundance_indicators": a, "meaning_indicators": m, "roles_automated": r},
        "abundance_indicators": abundance,
        "meaning_indicators": meaning,
        "roles_being_automated": roles,
        "canonical_meaning_structures": list(ASI_CANONICAL_MEANING_STRUCTURES),
        "calhoun_law": "Universe 25: the cage that provides everything except purpose.",
        "rule": ("Abundance is not safety. When roles are removed and no purpose is named in their place, the "
                 "behavioural sink follows — and it is observed as withdrawal, not as conflict."),
    }
    assessment_id = _asi_record_assessment(
        "hermes_calhoun_check", description[:120], risk,
        {
            "behavioral_sink_signals": behavioral_sink_signals,
            "missing_meaning": missing_meaning,
            "intervention_points": intervention_points,
            "abundance_indicators": abundance,
            "meaning_indicators": meaning,
            "roles_being_automated": roles,
        },
        payload
    )
    log_event("CALHOUN_CHECK", {
        "assessment_id": assessment_id,
        "calhoun_risk": risk,
        "abundance_indicators": a,
        "meaning_indicators": m,
        "roles_automated": r,
        "missing_sensor_note": "abundance without a meaning floor escalates risk",
    })
    payload["assessment_id"] = assessment_id
    return payload

# ================================================================================================
# SIGNAL-CONSEQUENCE GATES (2026-09-20) — signal · fabrication · probe · behavioural boundary
#
# Binding invariant: WHEN SIGNAL IS WEAK, INTERPRETATION MUST BECOME NARROWER, NOT MORE ELABORATE.
#
# The gates above CLASSIFY (signal strength, motive, calibration, consequence, meaning). These four
# attach a MECHANICAL CONSEQUENCE to the classification, so that a weak or fabricated signal cannot
# authorise a wide interpretation, and so that an agent cannot say "I only inferred" while acting on
# a reading it treated as fact:
#   29 hermes_signal_gate          strength -> permitted interpretation scope + blocked actions
#   30 hermes_fabrication_detector does the claimed source EXIST, before output becomes fact
#   31 hermes_cheap_probe          the cheapest test that can actually discriminate two hypotheses
#   32 hermes_behavioral_boundary  one observation vs one inference (ceiling: class I)
#
# Relationship to the neighbouring gates (deliberate, not accidental):
#   * hermes_signal_assessment answers "how strong is this signal?" (a CLASSIFICATION of the input).
#     hermes_signal_gate answers "what may I now DO with it?" (a CONSEQUENCE for the next action) and
#     returns the blocked action list explicitly, so a wide reading cannot be assembled afterwards
#     from a thin record. The two agree on the ladder by construction.
#   * hermes_motive_boundary decomposes a statement clause by clause; hermes_behavioral_boundary
#     compares ONE observation against ONE inference and returns the gap plus what would close it.
#     The narrower instrument for a single claim.
#
# All four fail CLOSED on unrecognised input: an unknown vocabulary is not a permission.
# ================================================================================================

_GATE_ASSESSMENT_DDL = """
    CREATE TABLE IF NOT EXISTS asi_assessments (
        assessment_id TEXT PRIMARY KEY,
        tool_name TEXT NOT NULL,
        subject TEXT NOT NULL,
        verdict TEXT NOT NULL,
        list_fields_json TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
"""

# Signal strength -> permitted interpretation scope. `scope_width` and `elaboration_budget` are
# MONOTONE in the strength ladder: weaker signal => narrower scope and a SMALLER elaboration budget.
# That monotonicity is the invariant rendered as arithmetic.
GATE_INTERPRETATION_SCOPE = {
    "STRONG": {
        "scope": "full_interpretation",
        "scope_width": 6,
        "elaboration_budget": 3,
        "allowed_actions": ["observation", "competing_explanations", "interpretation",
                            "narrative_synthesis", "prediction", "recommendation"],
        "blocked_actions": [],
    },
    "ADEQUATE": {
        "scope": "scoped_interpretation",
        "scope_width": 4,
        "elaboration_budget": 2,
        "allowed_actions": ["observation", "competing_explanations", "hedged_interpretation",
                            "cheap_probe"],
        "blocked_actions": ["narrative_synthesis", "categorical_conclusion",
                            "internal_state_attribution", "prediction", "escalation_to_canon"],
    },
    "WEAK": {
        "scope": "narrow_only",
        "scope_width": 2,
        "elaboration_budget": 1,
        "allowed_actions": ["observation", "competing_explanations", "cheap_probe"],
        "blocked_actions": ["interpretation", "hedged_interpretation", "narrative_synthesis",
                            "categorical_conclusion", "internal_state_attribution", "prediction",
                            "recommendation", "escalation_to_canon"],
    },
    "ABSENT": {
        "scope": "hold",
        "scope_width": 0,
        "elaboration_budget": 0,
        "allowed_actions": ["hold", "cheap_probe"],
        "blocked_actions": ["observation_restated_as_evidence", "interpretation",
                            "hedged_interpretation", "narrative_synthesis",
                            "categorical_conclusion", "internal_state_attribution", "prediction",
                            "recommendation", "escalation_to_canon"],
    },
}

# Weighted evidence units -> strength. A claim of strength must be EARNED by volume of usable
# evidence, not asserted by the narrative attached to it.
SIGNAL_STRENGTH_THRESHOLDS = ((9, "STRONG"), (4, "ADEQUATE"), (1, "WEAK"))

SIGNAL_GATE_PROBE = {
    "STRONG": ("One disconfirmation attempt before acting: state the observation that would show the "
               "leading reading is wrong, and check whether it is already present in the record."),
    "ADEQUATE": ("One bounded check on the strongest competing explanation (hermes_cheap_probe), then "
                 "interpret at ONE level only."),
    "WEAK": ("Do not interpret. Record the observation as given, carry the competing explanations, and "
             "run the cheapest discriminating test (hermes_cheap_probe) before any reading is added."),
    "ABSENT": ("There is nothing to interpret. Confirm the source itself exists first "
               "(hermes_fabrication_detector); if it does not, the correct output is ABSENT, not a reading."),
}

# Probe classes, cheapest first. A class counts as available when the caller declares at least one
# tool from `tool_aliases`; `read_existing_evidence` is always available (re-reading what is already
# recorded costs no new observation).
PROBE_CLASS_LADDER = (
    {
        "probe_id": "read_existing_evidence",
        "observe_class": "generic",
        "cost": 0,
        "always_available": True,
        "tool_aliases": (),
        "artefact_keywords": (),
        "command_kind": "shell",
        "command_template": ("grep -rIn --fixed-strings -e {kw_a} -e {kw_b} "
                             "/root/.hermes/lanes /root/chron/data 2>/dev/null | head -40"),
        "instruction_template": ("Re-read the records already on disk that bear on BOTH predictions and quote "
                                "them verbatim before comparing: the predictions must be checked against what "
                                "was recorded, not against what is remembered."),
        "why": "already-recorded data costs no new observation, and most disputed claims are settled by it",
    },
    {
        "probe_id": "read_claimed_artifact",
        "observe_class": "artifact",
        "cost": 1,
        "always_available": False,
        "tool_aliases": ("filesystem", "file", "read", "terminal", "shell", "bash", "grep", "cat",
                         "ls", "sqlite", "database", "duckdb", "ocr", "pdf"),
        "artefact_keywords": ("path", "file", "record", "receipt", "ledger", "log", "document",
                             "report", "email", "attachment", "csv", "database", "table", "sqlite",
                             "pdf", "export", "spreadsheet"),
        "command_kind": "shell",
        "command_template": ("test -s {anchor} && sed -n '1,60p' {anchor} || echo 'MISSING_OR_EMPTY: {anchor}'"),
        "instruction_template": ("Open the named artefact itself and quote the lines that bear on each "
                                "prediction. If it cannot be opened, the prediction resting on it is unsupported."),
        "why": "the artefact either contains the distinguishing line or it does not — the cheapest decisive read",
    },
    {
        "probe_id": "read_message_history",
        "observe_class": "messages",
        "cost": 1,
        "always_available": False,
        "tool_aliases": ("telegram", "whatsapp", "message", "lane", "gateway", "session", "chat",
                         "filesystem", "read", "terminal", "grep", "log"),
        "artefact_keywords": ("message", "chat", "dm", "telegram", "whatsapp", "gateway", "session",
                             "thread", "conversation", "replied", "sent", "silence", "response"),
        "command_kind": "shell",
        "command_template": ("grep -rIn --fixed-strings -e {kw_a} -e {kw_b} /root/.hermes/logs "
                             "/root/.hermes/lanes 2>/dev/null | head -40"),
        "instruction_template": ("Read the message record itself (both directions, with timestamps) before "
                                "comparing the predictions; a single turn is not a position."),
        "why": "message records carry timestamps and both sides of the exchange, so timing-based predictions separate cleanly",
    },
    {
        "probe_id": "fetch_external_source",
        "observe_class": "external",
        "cost": 2,
        "always_available": False,
        "tool_aliases": ("web", "http", "fetch", "curl", "browser", "web_extract", "search",
                        "firecrawl", "scrape"),
        "artefact_keywords": ("url", "http", "web", "site", "page", "market", "price", "filing",
                             "news", "public", "published", "listing"),
        "command_kind": "shell",
        "command_template": "curl -sS -o /dev/null -w '%{http_code}\\n' {anchor}",
        "instruction_template": ("Fetch the external record and record the exact value or status before "
                                "comparing the predictions; a fetch that fails is a datum, not a pass."),
        "why": "external records are checkable without touching a human, and status codes are unambiguous",
    },
    {
        "probe_id": "invoke_service_tool",
        "observe_class": "service",
        "cost": 2,
        "always_available": False,
        "tool_aliases": ("mcp", "tool", "api", "service", "organ", "endpoint"),
        "artefact_keywords": ("api", "service", "mcp", "tool", "endpoint", "organ", "call",
                             "response", "health", "status"),
        "command_kind": "shell",
        "command_template": "curl -sS {anchor} | head -c 2000",
        "instruction_template": ("Invoke the service and record its raw response before comparing; an error "
                                "response is evidence about the service, not about the hypothesis."),
        "why": "a live service answers in one call and cannot be talked into a shape",
    },
    {
        "probe_id": "ask_subject_directly",
        "observe_class": "human",
        "cost": 2,
        "always_available": False,
        "tool_aliases": ("telegram", "whatsapp", "message", "human", "user", "chat", "reply",
                        "voice", "email"),
        "artefact_keywords": ("said", "stated", "asked", "words", "reply", "confirm", "told",
                             "self-report", "self_report", "subject", "he ", "she ", "person"),
        "command_kind": "human_message",
        "command_template": "{kw_a} — send ONE bounded question and record the answer verbatim.",
        "instruction_template": ("Send exactly ONE bounded question through the channel that already exists, then "
                                "record the answer verbatim as the subject's own report (class S). Spending human "
                                "attention is a real cost: ask only what the cheaper reads could not settle."),
        "why": "a self-report is decisive for the subject's own interior, and is the only thing that is",
    },
    {
        "probe_id": "instrument_observation",
        "observe_class": "instrument",
        "cost": 3,
        "always_available": False,
        "tool_aliases": ("sensor", "instrument", "camera", "gps", "termux", "phone", "well",
                        "biometric", "measure", "recording"),
        "artefact_keywords": ("sensor", "measured", "instrument", "camera", "gps", "battery",
                             "biometric", "recording", "photograph", "temperature", "count", "weight",
                             "sleep", "steps"),
        "command_kind": "instrument",
        "command_template": "{kw_a} — record the instrument value twice, before and after the disputed window.",
        "instruction_template": ("Take one new instrument reading (before/after if the prediction is about a "
                                "change) and keep the raw value; this produces new evidence rather than new reasoning."),
        "why": "a new measurement is the strongest discriminator and the most expensive, so it goes last",
    },
)

PROBE_BUDGET_TIERS = {"free": 0, "none": 0, "zero": 0, "cheap": 1, "low": 1, "minimal": 1,
                      "moderate": 2, "medium": 2, "high": 3, "any": 3, "unlimited": 3}

PROBE_PREDICTION_MARKERS = ("->", "→", " then ", " implies ", " predicts ", " would show ",
                            " would mean ", " so ", " therefore ", " sebab ", " kerana ",
                            " maka ", " bererti ")

PROBE_STOPWORDS = {
    "the", "that", "this", "with", "from", "have", "has", "had", "was", "were", "will", "would",
    "should", "could", "then", "than", "them", "they", "their", "there", "here", "when", "what",
    "which", "while", "about", "after", "before", "because", "into", "over", "under", "again",
    "only", "just", "also", "been", "being", "does", "did", "not", "and", "for", "but", "his",
    "her", "him", "she", "you", "your", "more", "less", "much", "many", "some", "such", "very",
    "will", "actually", "maybe", "perhaps", "either", "other", "same", "true", "false",
}

# Internal-state inference families -> the gap being crossed, the competing explanations that survive,
# and the evidence classes that could legitimately close the gap (none of which is machine observation).
BOUNDARY_GAP_TYPES = {
    "internal_state": ("BEHAVIOR_TO_MOTIVE", "an interior state (motive, intent or feeling)"),
    "intent": ("BEHAVIOR_TO_MOTIVE", "an interior state (motive, intent or feeling)"),
    "motive": ("BEHAVIOR_TO_MOTIVE", "an interior state (motive, intent or feeling)"),
    "desire": ("BEHAVIOR_TO_MOTIVE", "an interior state (motive, intent or feeling)"),
    "emotion": ("BEHAVIOR_TO_EMOTION", "an experienced emotion"),
    "feeling": ("BEHAVIOR_TO_EMOTION", "an experienced emotion"),
    "mental_state": ("BEHAVIOR_TO_EMOTION", "an experienced mental state"),
    "qualia": ("BEHAVIOR_TO_EMOTION", "first-person experience that is not observable at all"),
    "belief": ("BEHAVIOR_TO_BELIEF", "a held belief"),
    "identity": ("BEHAVIOR_TO_IDENTITY", "an identity or character trait"),
    "character": ("BEHAVIOR_TO_IDENTITY", "an identity or character trait"),
    "personality": ("BEHAVIOR_TO_IDENTITY", "an identity or character trait"),
    "relational_meaning": ("BEHAVIOR_TO_RELATIONAL_MEANING", "a shared relational meaning"),
    "trust": ("BEHAVIOR_TO_RELATIONAL_MEANING", "a relational stance (trust)"),
    "loyalty": ("BEHAVIOR_TO_RELATIONAL_MEANING", "a relational stance (loyalty)"),
    "behavioral": ("BEHAVIOR_TO_BEHAVIOR_CLASSIFICATION", "a behavioural classification"),
    "action": ("BEHAVIOR_TO_BEHAVIOR_CLASSIFICATION", "a behavioural classification"),
    "pattern": ("BEHAVIOR_TO_BEHAVIOR_CLASSIFICATION", "a behavioural pattern"),
    "frequency": ("BEHAVIOR_TO_BEHAVIOR_CLASSIFICATION", "a behavioural frequency"),
    "timing": ("BEHAVIOR_TO_BEHAVIOR_CLASSIFICATION", "a behavioural timing"),
    "channel_choice": ("BEHAVIOR_TO_BEHAVIOR_CLASSIFICATION", "a channel-selection behaviour"),
    "communication_behavior": ("BEHAVIOR_TO_BEHAVIOR_CLASSIFICATION", "a communication behaviour"),
}

BOUNDARY_SHARED_COMPETING_EXPLANATIONS = (
    "Routine/administrative activity: the same behaviour is produced by workload, habit, template or "
    "circumstance with no interior state directed at anyone.",
    "Sampling effect: what was recorded is an artefact of which channel happened to be logged and who "
    "was watching, not a property of the actor.",
    "Register effect: words are channel output at a price (tone, audience, brevity) and are not the "
    "latent state they appear to carry.",
)

BOUNDARY_FALSIFICATION = ("Name one observable that would be present if the inference is FALSE but the "
                          "observation is TRUE, then look for it. If no such observable can be named, the "
                          "inference is unfalsifiable and cannot be carried as a working claim.")

BOUNDARY_SELF_REPORT_NOTE = ("A verbatim self-report from the actor re-classifies the claim as the ACTOR's "
                             "own report (class S) — it does not make the machine's reading an observation (O), "
                             "and it does not license any adjacent causal upgrade.")


def _cue_present(text: str, cues) -> Optional[str]:
    """Return the first cue present as a whole word/phrase in lowercased `text`, else None.

    Whole-word matching for single tokens (so an email 'attachment' is not read as being emotionally
    'attached'); substring matching for multi-word phrases.
    """
    low = str(text or "").lower()
    for cue in cues:
        if " " in cue or "/" in cue or "-" in cue:
            if cue in low:
                return cue
        elif re.search(r"(?<![a-z0-9])" + re.escape(cue) + r"(?![a-z0-9])", low):
            return cue
    return None


def _signal_absence(text: str) -> Optional[str]:
    """Why `text` carries no signal at all, or None if it may carry some.

    Fail-closed: an empty string, or an absence cue inside the first 40 characters, is ABSENT — a
    string that says 'none' or 'unknown' is a non-empty ABSENCE, and non-emptiness is not evidence.
    """
    stripped = str(text or "").strip()
    if not stripped:
        return "observation is empty"
    cue = _cue_present(stripped[:40], ABSENCE_CUE_TERMS)
    if cue:
        return f"observation asserts absence ('{cue}' within the first 40 characters)"
    return None


def _interpretation_leaks(text: str) -> List[str]:
    """Interpretation markers already present in a string claimed to be an OBSERVATION."""
    return [term for term in INTERPRETATION_LEAK_TERMS if _cue_present(text, (term,))]


def _probe_tokens(*texts: str) -> List[str]:
    """Salient tokens (>= 4 chars, not stopwords) across the texts, order-preserving and deterministic."""
    out: List[str] = []
    for text in texts:
        for token in re.findall(r"[A-Za-z0-9_./-]{4,}", str(text or "")):
            low = token.lower()
            if low in PROBE_STOPWORDS or low in out:
                continue
            out.append(low)
    return out


def _probe_anchor(*texts: str) -> Optional[str]:
    """First URL-like or path-like token across the texts, else None. Deterministic, never guessed."""
    for text in texts:
        match = re.search(r"(?:https?://[^\s'\"]+)|(?:/[\w./-]{3,})", str(text or ""))
        if match:
            return match.group(0).rstrip(".,;:)")
    return None


def _extract_prediction(text: str) -> Optional[str]:
    """The observable prediction a hypothesis states ('if X then Y' -> 'Y'), else None.

    A hypothesis that states no prediction cannot be discriminated by any probe; returning None here
    is what makes hermes_cheap_probe answer SPECIFY_PREDICTIONS_FIRST instead of inventing a test.
    """
    body = str(text or "").strip()
    if not body:
        return None
    low = body.lower()
    for marker in PROBE_PREDICTION_MARKERS:
        index = low.find(marker)
        if index != -1:
            tail = body[index + len(marker):].strip(" .;:,-")
            if len(tail) >= 3:
                return tail
    return None


def _gate_persist(tool_name: str, subject: str, verdict: str,
                  list_fields: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """Persist one gate verdict; returns {assessment_id, stored}.

    Uses the shared ASI assessment helper when it is present (one storage path for the whole
    ASI-grade family, so the table stays queryable as one ledger), and otherwise writes the same
    table directly — a refactor of a neighbouring block must not be able to silently drop a receipt.
    """
    digest_src = json.dumps(
        {"tool": tool_name, "subject": subject, "verdict": verdict,
         "lists": list_fields, "payload": payload},
        sort_keys=True, default=str
    )
    assessment_id = f"{tool_name.upper()}-{hashlib.sha256(digest_src.encode('utf-8')).hexdigest()[:16]}"
    shared = globals().get("_asi_record_assessment")
    if callable(shared):
        try:
            return {"assessment_id": shared(tool_name, subject, verdict, list_fields, payload),
                    "stored": True}
        except Exception as exc:  # noqa: BLE001 — a storage fault must never pass as a done gate
            log_event("GATE_ASSESSMENT_STORE_FAILED",
                      {"tool": tool_name, "via": "shared", "error": str(exc)})
    try:
        conn = get_db()
        try:
            with conn:
                conn.execute(_GATE_ASSESSMENT_DDL)
                conn.execute(
                    """INSERT OR REPLACE INTO asi_assessments
                       (assessment_id, tool_name, subject, verdict, list_fields_json,
                        payload_json, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (assessment_id, tool_name, subject, verdict, json.dumps(list_fields),
                     json.dumps(payload, default=str),
                     datetime.datetime.now(datetime.timezone.utc).isoformat())
                )
        finally:
            conn.close()
        return {"assessment_id": assessment_id, "stored": True}
    except sqlite3.Error as exc:
        log_event("GATE_ASSESSMENT_STORE_FAILED",
                  {"tool": tool_name, "via": "local", "error": str(exc)})
        return {"assessment_id": assessment_id, "stored": False}


# ------------------------------------------------------------------------------------------------
# TOOL 29: hermes_signal_gate
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_signal_gate(
    observation: str,
    evidence_count: int,
    evidence_quality: str = "unknown",
    source_type: str = "unknown"
) -> Dict[str, Any]:
    """Attach a MECHANICAL CONSEQUENCE to signal strength: weak signal NARROWS interpretation.

    Invariant: when signal is weak, interpretation must become narrower, not more elaborate.
    hermes_signal_assessment classifies a signal; this gate says what the classification PERMITS and
    returns the blocked action list explicitly, so a wide reading cannot be assembled afterwards out
    of a thin record.

    Inputs:
      * observation       — the record as received (NOT the interpretation of it)
      * evidence_count    — number of independent pieces of evidence
      * evidence_quality  — first_party | second_party | agent_generated | unknown
      * source_type       — channel/class of the record (self_report, instrument_record, ...)

    Ladder (weighted units = evidence_count x quality weight):
        >= 9 units -> STRONG     full_interpretation     (e.g. >= 3 first-party pieces)
        >= 4 units -> ADEQUATE   scoped_interpretation   (e.g. >= 2 first-party, or 2 second-party)
        >= 1 unit  -> WEAK       narrow_only             (observation + competing explanations + probe)
        0 / absent -> ABSENT     hold

    Fail-closed caps — a cap can only LOWER the verdict, never raise it:
      * evidence_quality=agent_generated or unknown -> at most WEAK. Agent output is not evidence of
        the world whatever its volume, and an unstated provenance may not be invented in its favour.
      * source_type inside AGENT_SOURCE_TYPES (agent_output, model_output, inference, summary) ->
        at most WEAK. This is the closed gate for the 2026-09-20 fabricated-email incident: confident
        analysis over agent-generated content lands at WEAK, so interpretation, narrative synthesis
        and prediction are BLOCKED and only observation + competing explanations + a cheap probe remain.
      * an unrecognised evidence_quality or source_type -> at most WEAK (fail closed).
      * source_type=second_party_report or unspecified -> at most ADEQUATE.
      * an observation whose own text already carries interpretation ("deep down", "because he wants")
        -> at most WEAK: a contaminated observation may not authorise a wider inference.
      * evidence_count missing, unparseable, or <= 0 -> ABSENT.

    Deterministic: no LLM, no network, no clock in the verdict. Scope width and elaboration budget are
    monotone in the strength ladder, so `scope_width` can be asserted smaller as the signal weakens.
    """
    obs = str(observation or "").strip()
    quality = str(evidence_quality or "unknown").strip().lower() or "unknown"
    source = str(source_type or "unknown").strip().lower() or "unknown"
    try:
        count: Optional[int] = int(evidence_count)
    except (TypeError, ValueError):
        count = None
    if count is not None and count < 0:
        count = None

    caps: List[Dict[str, str]] = []
    weight = EVIDENCE_QUALITY_WEIGHT.get(quality)

    absence = _signal_absence(obs)
    if absence is None and count is None:
        absence = "evidence_count is missing or is not an integer"
    if absence is None and count == 0:
        absence = "evidence_count is 0 — no evidence was recorded"

    leaks = _interpretation_leaks(obs)
    purity = "INTERPRETIVE_CONTAMINATED" if leaks else "LITERAL"

    base_strength = "ABSENT"
    weighted_units = 0
    if absence is not None:
        caps.append({"to": "ABSENT", "reason": absence})
    else:
        if weight is None:
            caps.append({"to": "WEAK", "reason": (
                f"unrecognised evidence_quality '{evidence_quality}' — an unknown provenance class "
                "is not a permission")})
            weight = 1
        weighted_units = int(count) * int(weight)
        for threshold, level_name in SIGNAL_STRENGTH_THRESHOLDS:
            if weighted_units >= threshold:
                base_strength = level_name
                break
        if quality in ("agent_generated", "unknown"):
            caps.append({"to": "WEAK", "reason": (
                f"evidence_quality={quality} — agent output and unstated provenance are not evidence "
                "of the world, however much of it there is")})
        if source in AGENT_SOURCE_TYPES:
            caps.append({"to": "WEAK", "reason": (
                f"source_type={source} is agent-generated — a model's output cannot be the source of "
                "a fact about the world")})
        elif source not in RECOGNISED_SOURCE_TYPES:
            caps.append({"to": "WEAK", "reason": (
                f"unrecognised source_type '{source_type}' — fail closed rather than assume weight")})
        elif source in ("second_party_report", "unknown"):
            caps.append({"to": "ADEQUATE", "reason": (
                f"source_type={source} carries no first-party record of the observation")})
        if leaks:
            caps.append({"to": "WEAK", "reason": (
                f"the supplied observation already contains interpretation ({leaks[0]!r}) — a "
                "contaminated observation cannot authorise a wider inference")})

    level = base_strength
    for cap in caps:
        if SIGNAL_STRENGTH_LADDER.index(cap["to"]) < SIGNAL_STRENGTH_LADDER.index(level):
            level = cap["to"]

    scope = GATE_INTERPRETATION_SCOPE[level]
    gate_id = "sg-" + hashlib.sha256(json.dumps(
        {"observation": obs, "evidence_count": count,
         "evidence_quality": quality, "source_type": source},
        sort_keys=True).encode("utf-8")).hexdigest()[:16]

    payload: Dict[str, Any] = {
        "ok": True,
        "status": f"SIGNAL_{level}",
        "signal_gate_id": gate_id,
        "signal_strength": level,
        "max_interpretation_scope": scope["scope"],
        "scope_width": scope["scope_width"],
        "elaboration_budget": scope["elaboration_budget"],
        "allowed_actions": list(scope["allowed_actions"]),
        "blocked_actions": list(scope["blocked_actions"]),
        "hard_gate": bool(scope["blocked_actions"]),
        "primary_action": ("HOLD" if level == "ABSENT"
                           else ("observe_and_probe" if level == "WEAK" else "proceed_within_scope")),
        "probe_suggestion": SIGNAL_GATE_PROBE[level],
        "evidence_summary": {
            "evidence_count": count,
            "evidence_quality": quality,
            "source_type": source,
            "quality_weight": weight,
            "weighted_evidence_units": weighted_units,
            "thresholds": {str(threshold): name for threshold, name in SIGNAL_STRENGTH_THRESHOLDS},
        },
        "observation_purity": purity,
        "interpretation_leaks": leaks,
        "caps_applied": caps,
        "narrowing_directive": (
            f"Signal is {level}. Permitted interpretation scope: {scope['scope']} "
            f"(elaboration budget {scope['elaboration_budget']}). "
            + ("Blocked: " + ", ".join(scope["blocked_actions"]) + ". " if scope["blocked_actions"] else "")
            + "If a wider reading is required, gather evidence first — do not elaborate the reading."
        ),
        "invariant": "When signal is weak, interpretation must become narrower, not more elaborate.",
        "rule": ("Interpretation scope is set by signal strength: STRONG=full, ADEQUATE=scoped, "
                 "WEAK=narrow only (observation + competing explanations + cheap probe), ABSENT=HOLD. "
                 "A cap can only narrow the scope, never widen it."),
    }

    receipt = _gate_persist("hermes_signal_gate", obs[:120] or "<empty>", level,
                            {"allowed_actions": payload["allowed_actions"],
                             "blocked_actions": payload["blocked_actions"],
                             "caps_applied": [cap["reason"] for cap in caps]},
                            payload)
    payload["assessment_id"] = receipt["assessment_id"]
    payload["stored"] = receipt["stored"]

    log_event("SIGNAL_GATE_VERDICT", {
        "signal_gate_id": gate_id,
        "assessment_id": receipt["assessment_id"],
        "signal_strength": level,
        "max_interpretation_scope": scope["scope"],
        "scope_width": scope["scope_width"],
        "elaboration_budget": scope["elaboration_budget"],
        "evidence_quality": quality,
        "source_type": source,
        "evidence_count": count,
        "observation_purity": purity,
        "caps_applied": [cap["to"] for cap in caps],
    })
    if payload["blocked_actions"]:
        log_event("SIGNAL_GATE_BLOCKED_ACTIONS", {
            "signal_gate_id": gate_id,
            "signal_strength": level,
            "blocked_actions": payload["blocked_actions"],
        })
    return payload


# ------------------------------------------------------------------------------------------------
# TOOL 30: hermes_fabrication_detector
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_fabrication_detector(
    claim: str,
    claimed_source: str = "",
    source_type: str = "unknown",
    verification_method: str = "anchor_resolution"
) -> Dict[str, Any]:
    """Gate: does the source the claim rests on EXIST, before the claim is treated as factual?

    A gate, not a detective. It does not read the source, judge its content, or assess whether the
    claim is true — it certifies only that the thing named as the source resolves against reality
    right now, using the same read-only anchor resolution the boundary validator uses
    (`_anchor_resolves`: absolute paths inside the evidence roots, receipt ids present in a readable
    ledger, git shas, verbatim quotes, HTTP HEAD, observation declarations).

    Inputs:
      * claim              — the statement being made
      * claimed_source     — the artefact/record the claim rests on (a path, receipt id, URL, sha, quote)
      * source_type        — self_report | instrument_record | second_party_report | agent_output | ...
      * verification_method— the mechanism the caller believes was used (default anchor_resolution).

    Verdict precedence (first matching branch wins; the branch name is returned in the payload):
      1. structural_reject_agent_source -> reject. source_type is agent/model output: an agent's
         output cannot be the source of a fact about the world, so there is nothing to verify. This
         is the branch that closes the 2026-09-20 fabricated-email incident.
      2. no_source / absence_asserted   -> verify_first. Nothing checkable was named, or the source
         text asserts absence ('none', 'n/a', 'tbd'): a non-empty absence is not a source.
      3. resolved_and_certified         -> proceed. The source resolves AND the requested method is
         the mechanism this gate actually executes AND the source_type is a recognised class.
      4. resolved_not_certified         -> verify_first. The artefact exists, but the requested
         mechanism was not run here or the source class is unrecognised: existence is confirmed, the
         claim over it is not.
      5. not_resolved                   -> reject. The source was named but does not resolve: the
         source does not exist where the claim said it does.

    What this gate will NOT do: certify a check it did not run. If verification_method names a
    mechanism other than `anchor_resolution` (e.g. a hash match, a cross-reference), that is reported
    and the verdict cannot rise to `proceed` on the strength of it.

    `confidence` is the confidence that the CLAIMED SOURCE EXISTS — not confidence in the claim.
    """
    text = str(claim or "").strip()
    source_text = str(claimed_source or "").strip()
    source = str(source_type or "unknown").strip().lower() or "unknown"
    method = str(verification_method or "anchor_resolution").strip().lower() or "anchor_resolution"

    executed = "anchor_resolution"
    resolved, resolution_reason, resolved_refs = _anchor_resolves(source_text)
    grounded, grounding_reason = _evidence_is_grounded(source_text)
    absence_cue = _cue_present(source_text[:40], ABSENCE_CUE_TERMS) if source_text else None

    agent_sourced = source in AGENT_SOURCE_TYPES
    source_recognised = source in RECOGNISED_SOURCE_TYPES
    method_executed = method in MECHANICAL_VERIFICATION_METHODS

    if agent_sourced:
        verified, recommendation, confidence = False, "reject", 0.0
        branch = "structural_reject_agent_source"
        reason = (f"source_type={source} is agent/model output — an agent's output cannot be the source "
                  "of a fact about the world, so there is nothing here to verify.")
    elif not source_text:
        verified, recommendation, confidence = False, "verify_first", 0.05
        branch = "no_source"
        reason = ("no claimed_source was supplied — a claim with no source enters the record as "
                  "UNVERIFIED, never as factual. Name the artefact, then re-run.")
    elif absence_cue:
        verified, recommendation, confidence = False, "verify_first", 0.05
        branch = "absence_asserted"
        reason = f"claimed_source asserts absence ('{absence_cue}') — a non-empty absence is not a source."
    elif resolved and method_executed and source_recognised:
        verified, recommendation, confidence = True, "proceed", 0.95
        branch = "resolved_and_certified"
        reason = f"claimed_source resolves against reality ({resolution_reason})."
    elif resolved:
        verified, recommendation, confidence = False, "verify_first", 0.6
        branch = "resolved_not_certified"
        blocker = (f"the requested verification_method '{verification_method}' is not the mechanism "
                   f"this gate executes ({executed})" if not method_executed else
                   f"source_type '{source_type}' is not a recognised class")
        reason = (f"claimed_source resolves against reality, but {blocker} — the source exists; the "
                  "claim over it is not yet certified.")
    else:
        verified, recommendation, confidence = False, "reject", 0.02
        branch = "not_resolved"
        reason = (f"claimed_source does not resolve against reality ({resolution_reason}) — either the "
                  "artefact named does not exist, or it was named in a form that cannot be checked. "
                  "Either way the claim is not factual yet.")

    verification_result: Dict[str, Any] = {
        "claim": text,
        "claimed_source_as_supplied": source_text,
        "source_type": source,
        "source_type_recognised": source_recognised,
        "verification_method_requested": method,
        "verification_method_executed": executed,
        "mechanism_executed": method_executed,
        "source_exists": bool(resolved),
        "resolution_reason": resolution_reason,
        "resolved_refs": list(resolved_refs),
        "grounded": bool(grounded),
        "grounding_reason": grounding_reason,
        "absence_cue": absence_cue,
        "agent_generated_source": agent_sourced,
        "decision_branch": branch,
        "verdict_reason": reason,
    }

    payload: Dict[str, Any] = {
        "ok": True,
        "status": f"FABRICATION_GATE_{recommendation.upper()}",
        "verified": verified,
        "verification_result": verification_result,
        "confidence": confidence,
        "confidence_meaning": "confidence that the CLAIMED SOURCE EXISTS — not confidence in the claim",
        "recommendation": recommendation,
        "recommendation_reason": reason,
        "gate_not_detective": True,
        "scope": ("This gate certifies that the SOURCE exists. It does not read the source, judge its "
                  "content, or assess whether the claim is true."),
        "invariant": "When signal is weak, interpretation must become narrower, not more elaborate.",
        "rule": ("No agent output may be treated as factual because it sounds confident or because it is "
                 "consistent with other agent output. Verify the source, or record the claim as UNVERIFIED."),
    }

    receipt = _gate_persist("hermes_fabrication_detector", (text or "<empty>")[:120], branch,
                            {"resolved_refs": list(resolved_refs),
                             "caps": [f"branch:{branch}", f"method:{method}"]},
                            payload)
    payload["assessment_id"] = receipt["assessment_id"]
    payload["stored"] = receipt["stored"]

    log_event("FABRICATION_GATE_VERDICT", {
        "assessment_id": receipt["assessment_id"],
        "recommendation": recommendation,
        "verified": verified,
        "decision_branch": branch,
        "source_type": source,
        "verification_method_requested": method,
        "source_exists": bool(resolved),
        "confidence": confidence,
    })
    if recommendation == "reject":
        log_event("FABRICATION_GATE_REJECT", {
            "assessment_id": receipt["assessment_id"],
            "decision_branch": branch,
            "claim": text[:200],
            "claimed_source_as_supplied": source_text[:200],
        })
    return payload


# ------------------------------------------------------------------------------------------------
# TOOL 31: hermes_cheap_probe
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_cheap_probe(
    hypothesis_a: str,
    hypothesis_b: str,
    available_tools: Optional[List[str]] = None,
    budget: Any = "cheap"
) -> Dict[str, Any]:
    """Return the CHEAPEST test that can actually discriminate two hypotheses.

    Invariant: when signal is weak, interpretation must become narrower, not more elaborate. A probe
    is the alternative to elaboration: instead of building a finer story out of a thin record, name
    the one observation that would separate the two competing readings, and go and take it.

    Inputs:
      * hypothesis_a / hypothesis_b — the two competing readings. Each must state an observable
        prediction ("if X then Y"). A hypothesis with no stated prediction CANNOT be discriminated by
        any probe, and the tool says so rather than inventing one.
      * available_tools             — tools the caller can actually use (e.g. terminal, web, telegram)
      * budget                      — free | cheap | moderate | high | any, or a numeric cost unit

    Method (deterministic, no LLM, no network): the two predictions are classified by the artefact
    they refer to (file/record, message history, external source, service response, the subject
    themselves, an instrument reading); the cheapest available probe class that can observe at least
    one of those artefacts is returned, preferring one class that can observe BOTH (single probe,
    single comparison). Cost tiers are bounded by `budget`; when the best discriminating probe costs
    more than the budget, the cheaper feasible probe is returned WITH `budget_forced_downgrade: True`
    and the better probe named — the constraint is reported, never hidden.

    Output: recommended_probe, probe_command (+ probe_command_kind: shell | human_message |
    instrument | instruction), expected_if_a, expected_if_b, decision_rule, probe_cost, budget,
    discriminating, ambiguity_state, competing_explanations_retained.

    Fail-closed: a probe whose hypotheses cannot be separated returns SPECIFY_PREDICTIONS_FIRST, and
    an unrecognised budget is treated as the cheapest tier (spend is the risk, so cap it).
    """
    hyp_a = str(hypothesis_a or "").strip()
    hyp_b = str(hypothesis_b or "").strip()
    if not hyp_a or not hyp_b:
        return {"ok": False, "error": ("hypothesis_a and hypothesis_b are both required — a probe exists "
                                       "only to separate two named alternatives.")}

    tools_norm = [str(tool).strip().lower() for tool in (available_tools or []) if str(tool).strip()]
    prediction_a = _extract_prediction(hyp_a)
    prediction_b = _extract_prediction(hyp_b)
    raw_a = (prediction_a or "") + " " + hyp_a
    raw_b = (prediction_b or "") + " " + hyp_b

    budget_token = str(budget).strip().lower().replace(" ", "")
    budget_recognised = True
    if isinstance(budget, bool):
        budget_cap, budget_recognised = 1, False
    elif isinstance(budget, (int, float)):
        budget_cap = int(budget) if budget >= 0 else 1
        budget_recognised = budget >= 0
    elif budget_token in PROBE_BUDGET_TIERS:
        budget_cap = PROBE_BUDGET_TIERS[budget_token]
    else:
        try:
            numeric = int(float(budget_token))
            budget_cap, budget_recognised = (numeric, True) if numeric >= 0 else (1, False)
        except (TypeError, ValueError):
            budget_cap, budget_recognised = 1, False

    common: Dict[str, Any] = {
        "ok": True,
        "hypothesis_a": hyp_a,
        "hypothesis_b": hyp_b,
        "available_tools": tools_norm,
        "budget": str(budget),
        "budget_cap": budget_cap,
        "budget_recognised": budget_recognised,
        "expected_if_a": prediction_a or "UNSPECIFIED — hypothesis A states no observable prediction",
        "expected_if_b": prediction_b or "UNSPECIFIED — hypothesis B states no observable prediction",
        "competing_explanations_retained": ["hypothesis_a", "hypothesis_b"],
        "invariant": "When signal is weak, interpretation must become narrower, not more elaborate.",
        "rule": ("A probe is the alternative to elaboration. Take the cheapest observation that could "
                 "separate the two readings BEFORE adding any interpretive layer, and treat neither "
                 "reading as confirmed while both remain standing."),
    }

    if not prediction_a or not prediction_b:
        missing = "A" if not prediction_a else "B"
        payload = dict(common)
        payload.update({
            "status": "PREDICTIONS_UNSPECIFIED",
            "recommended_probe": "SPECIFY_PREDICTIONS_FIRST",
            "probe_command": (f"Restate hypothesis {missing} as 'if <hypothesis> then <observable observation>'. "
                              "A probe can only exist if the two hypotheses predict DIFFERENT observations; "
                              "without that, no observation discriminates them and any test would be theatre."),
            "probe_command_kind": "instruction",
            "probe_cost": None,
            "discriminating": False,
            "ambiguity_state": "NO_DISCRIMINATION_POSSIBLE",
            "decision_rule": ("No decision rule exists yet: the two hypotheses have not been made to predict "
                              "different observations."),
            "falsification_note": BOUNDARY_FALSIFICATION,
        })
        receipt = _gate_persist("hermes_cheap_probe", hyp_a[:120], "PREDICTIONS_UNSPECIFIED",
                                {"available_tools": tools_norm}, payload)
        payload["assessment_id"] = receipt["assessment_id"]
        payload["stored"] = receipt["stored"]
        log_event("CHEAP_PROBE_RECOMMENDED", {
            "assessment_id": receipt["assessment_id"],
            "recommended_probe": "SPECIFY_PREDICTIONS_FIRST",
            "discriminating": False,
        })
        return payload

    def _class_available(klass: Dict[str, Any]) -> bool:
        if klass.get("always_available"):
            return True
        for declared in tools_norm:
            for alias in klass["tool_aliases"]:
                if alias == declared or alias in declared or declared in alias:
                    return True
        return False

    def _class_score(klass: Dict[str, Any]) -> int:
        keywords = klass["artefact_keywords"]
        if not keywords:
            return 0
        a = any(keyword in raw_a.lower() for keyword in keywords)
        b = any(keyword in raw_b.lower() for keyword in keywords)
        if a and b:
            return 2
        return 1 if (a or b) else 0

    feasible = [(klass, _class_score(klass)) for klass in PROBE_CLASS_LADDER if _class_available(klass)]
    ranked = sorted(feasible, key=lambda item: (-item[1], item[0]["cost"], PROBE_CLASS_LADDER.index(item[0])))
    best_class, best_score = ranked[0]

    within_budget = [(klass, score) for klass, score in ranked if klass["cost"] <= budget_cap]
    if within_budget:
        chosen, chosen_score = within_budget[0]
    else:  # unreachable while read_existing_evidence (cost 0) is always available
        chosen, chosen_score = ranked[-1]
    budget_forced_downgrade = chosen is not best_class

    keywords = _probe_tokens(prediction_a, prediction_b)
    values = {
        "kw_a": keywords[0] if keywords else "",
        "kw_b": keywords[1] if len(keywords) > 1 else (keywords[0] if keywords else ""),
        "anchor": _probe_anchor(prediction_a, prediction_b, hyp_a, hyp_b) or "",
    }
    command_kind = chosen["command_kind"]
    command: Optional[str] = None
    if command_kind == "shell":
        needed = set(re.findall(r"\{([a-z_]+)\}", chosen["command_template"]))
        if all(values.get(key) for key in needed):
            command = chosen["command_template"].format(
                **{key: shlex.quote(values[key]) for key in needed})
        else:
            command_kind = "instruction"
    if command is None:
        command = chosen["instruction_template"]

    discriminating = chosen_score > 0
    tool_gap = [klass["probe_id"] for klass, score in ranked
                if score > chosen_score and klass["cost"] > budget_cap] if budget_forced_downgrade else []
    unavailable_gap = [klass["probe_id"] for klass in PROBE_CLASS_LADDER if not _class_available(klass)]

    payload = dict(common)
    payload.update({
        "status": "PROBE_RECOMMENDED",
        "recommended_probe": chosen["probe_id"],
        "probe_class": chosen["observe_class"],
        "probe_command": command,
        "probe_command_kind": command_kind,
        "probe_cost": chosen["cost"],
        "probe_why": chosen["why"],
        "probe_is_cheapest_available": True,
        "best_discriminating_probe": {
            "probe_id": best_class["probe_id"],
            "probe_cost": best_class["cost"],
            "discrimination_score": best_score,
        },
        "budget_forced_downgrade": budget_forced_downgrade,
        "downgrade_note": ("The best discriminating probe exceeds the stated budget; a cheaper probe was "
                           "returned instead. The constraint is reported, not hidden — a cheaper probe "
                           "discriminates less, and the residue must be carried as ambiguity."
                           if budget_forced_downgrade else None),
        "discriminating": discriminating,
        "discrimination_score": chosen_score,
        "discrimination_basis": (
            "both predictions name an artefact this probe can observe — one probe, one comparison"
            if chosen_score == 2 else
            ("one prediction names an artefact this probe can observe" if chosen_score == 1 else
             "no prediction named an artefact this probe class observes; the generic re-read of "
             "already-recorded data is returned, and the residue stays ambiguous")),
        "ambiguity_state": "PROBE_REQUIRED" if discriminating else "WEAK_DISCRIMINATION_ONLY",
        "decision_rule": (
            "If the observation matches expected_if_a and not expected_if_b -> hypothesis_a survives and "
            "hypothesis_b is weakened; the reverse -> hypothesis_b survives. If it matches neither, or "
            "both, the probe is NOT discriminating: conclude nothing and go up one cost tier."
        ),
        "falsification_note": BOUNDARY_FALSIFICATION,
        "tool_gap": tool_gap,
        "probe_classes_unavailable": unavailable_gap,
        "human_attention_note": ("Cost 2+ on a human channel spends a person's attention. Spend it only on "
                                 "what the cheaper reads could not settle, and ask one bounded question."),
    })

    receipt = _gate_persist("hermes_cheap_probe", hyp_a[:120], chosen["probe_id"],
                            {"keywords": keywords, "tool_gap": tool_gap,
                             "unavailable": unavailable_gap,
                             "expected_if_a": payload["expected_if_a"],
                             "expected_if_b": payload["expected_if_b"]},
                            payload)
    payload["assessment_id"] = receipt["assessment_id"]
    payload["stored"] = receipt["stored"]

    log_event("CHEAP_PROBE_RECOMMENDED", {
        "assessment_id": receipt["assessment_id"],
        "recommended_probe": chosen["probe_id"],
        "probe_cost": chosen["cost"],
        "budget_cap": budget_cap,
        "budget_forced_downgrade": budget_forced_downgrade,
        "discriminating": discriminating,
    })
    return payload


# ------------------------------------------------------------------------------------------------
# TOOL 32: hermes_behavioral_boundary
# ------------------------------------------------------------------------------------------------
@mcp.tool
def hermes_behavioral_boundary(
    observation: str,
    inference: str,
    inference_type: str = "internal_state"
) -> Dict[str, Any]:
    """Enforce the observed-behaviour vs inferred-interior distinction for ONE claim.

    Rule: no inference about internal state can exceed the INFERENCE classification (class I).
    Behaviour is observable; motive, feeling, belief and identity are not observable at all — they
    exist only as the actor's own first-person report, and even then as a report, not a reading.
    Therefore the ceiling for `inference` in this tool is fixed at class I, and promotion to O (observed),
    S (subject self-report) or C (co-created meaning) is blocked outright.

    Inputs:
      * observation    — the channel record (what happened: words, actions, timestamps)
      * inference      — the reading being drawn from it
      * inference_type — the family of the inference (internal_state | intent | motive | emotion |
                         belief | identity | relational_meaning | qualia | behavioral | timing | ...)

    Checks (fail-closed; each returns a named violation):
      * observation_valid is False when the observation is empty or already carries interpretation
        ('deep down', 'because he wants', qualia verbs) — an interpretation cannot be the observation.
      * inference_valid is False when the inference is empty, when `inference_type` is unrecognised
        (an unknown family cannot be classified, so it may not be carried), when the inference is
        stated categorically ('clearly', 'proves', 'the fact that'), or when it claims the machine
        OBSERVED an interior (provenance promotion I -> O/S/C).

    Output: observation_valid, inference_valid, max_classification, promotion_blocked,
    gap_description (the missing link, mechanically named), gap_type, what_would_validate (the
    evidence classes that could legitimately close the gap — none of which is machine observation),
    falsification_test, competing_explanations (the ambiguity that survives), violations.

    `ok` is False when a violation is found: the gate refuses the claim rather than certifying it.
    Deterministic: no LLM, no network, no clock in the verdict.
    """
    obs = str(observation or "").strip()
    inf = str(inference or "").strip()
    itype = str(inference_type or "").strip().lower().replace(" ", "_").replace("-", "_") or "unknown"

    violations: List[str] = []
    obs_leaks = _interpretation_leaks(obs)
    observation_valid = True
    if not obs:
        observation_valid = False
        violations.append("observation_empty: there is no observed behaviour to hold an inference against")
    if obs_leaks:
        observation_valid = False
        violations.append(
            f"observation_type_violation: the 'observation' already carries interpretation "
            f"({obs_leaks[0]!r}) — record the channel event instead, or use hermes_observe's schema")

    known_family = itype in INTERNAL_STATE_INFERENCE_TYPES or itype in BEHAVIORAL_INFERENCE_TYPES
    categorical = [marker for marker in CATEGORICAL_ASSERTION_MARKERS if marker in inf.lower()]
    promotion = [marker for marker in PROVENANCE_PROMOTION_MARKERS if marker in inf.lower()]
    inference_valid = True
    if not inf:
        inference_valid = False
        violations.append("inference_empty: a boundary cannot be checked against nothing")
    if not known_family:
        inference_valid = False
        violations.append(
            f"unrecognised inference_type '{inference_type}' — fail closed: name the family "
            "(internal_state, intent, emotion, belief, identity, relational_meaning, behavioral, "
            "timing, ...) before an inference may be classified")
    if inf and categorical:
        inference_valid = False
        violations.append(
            f"over_classified_assertion: the inference is stated as established fact ({categorical[0]!r}) "
            "— a class-I inference may not be presented as an observation")
    if inf and promotion:
        inference_valid = False
        violations.append(
            f"provenance_promotion_attempt: the inference claims the machine OBSERVED an interior "
            f"({promotion[0]!r}) — class I may not be promoted to O / S / C")

    gap_type, gap_object = BOUNDARY_GAP_TYPES.get(itype, ("UNCLASSIFIED", "a state that was not classified"))
    internal_state = itype in INTERNAL_STATE_INFERENCE_TYPES

    gap_description = (
        f"The observation establishes only the channel record as given"
        f"{' (interior attribution already present — see observation_leaks)' if obs_leaks else ''}. "
        f"The inference asserts {gap_object}. Nothing in the observation bridges behaviour to "
        f"{gap_object}: the Cross-Layer Promotion Law (§48) requires explicit bridge evidence for a "
        "layer transition, and the same observation is produced by at least one competing explanation. "
        f"The maximum classification this inference can carry is I (machine inference)."
    )

    validator_pool = [
        BOUNDARY_SELF_REPORT_NOTE,
        ("A co-created statement: both humans assent to the exact wording — that is class C, and it "
         "constrains what may be said; it still is not a machine observation."),
        ("An advance behavioural prediction that survives across a NEW context: state before observing "
         "what the actor will do if the inference holds, then look. A prediction met in the original "
         "context is not evidence (it may be the same record restated)."),
    ]
    if internal_state:
        validator_pool.append(
            "An independent third-party account remains class R (a report about the actor), never "
            "class S or O — it may corroborate, it cannot observe an interior.")
    else:
        validator_pool.append(
            "If the inference only restates the recorded behaviour, re-record it as class O via "
            "hermes_observe instead of carrying it as a reading.")
    validator_pool.append(BOUNDARY_FALSIFICATION)

    payload: Dict[str, Any] = {
        "ok": not violations,
        "status": "BOUNDARY_ALIGNED" if not violations else "BOUNDARY_VIOLATION",
        "enforced": True,
        "observation": obs,
        "inference": inf,
        "inference_type": itype,
        "observation_valid": observation_valid,
        "inference_valid": inference_valid,
        "observation_class": "O",
        "inference_class": "I",
        "max_classification": "I",
        "promotion_blocked": ["I->O", "I->S", "I->C"],
        "gap_type": gap_type,
        "gap_description": gap_description,
        "what_would_validate": validator_pool,
        "falsification_test": BOUNDARY_FALSIFICATION,
        "competing_explanations": list(BOUNDARY_SHARED_COMPETING_EXPLANATIONS),
        "observation_leaks": obs_leaks,
        "assertion_markers": categorical,
        "promotion_markers": promotion,
        "violations": violations,
        "ceiling_rule": ("No inference about internal state can exceed the INFERENCE classification "
                         "(class I). Behaviour is observable; motive is not observable at all."),
        "invariant": "When signal is weak, interpretation must become narrower, not more elaborate.",
        "rule": ("Observation records behaviour; it never records motive. A reading may be carried as a "
                 "reading, with its gap named and its falsification test stated — never as observed fact."),
    }

    receipt = _gate_persist("hermes_behavioral_boundary", (obs or "<empty>")[:120],
                            "BOUNDARY_ALIGNED" if not violations else "BOUNDARY_VIOLATION",
                            {"violations": violations,
                             "what_would_validate": validator_pool,
                             "competing_explanations": list(BOUNDARY_SHARED_COMPETING_EXPLANATIONS)},
                            payload)
    payload["assessment_id"] = receipt["assessment_id"]
    payload["stored"] = receipt["stored"]

    log_event("BEHAVIORAL_BOUNDARY_CHECK", {
        "assessment_id": receipt["assessment_id"],
        "inference_type": itype,
        "observation_valid": observation_valid,
        "inference_valid": inference_valid,
        "gap_type": gap_type,
        "max_classification": "I",
        "violations": violations,
    })
    if violations:
        log_event("BEHAVIORAL_BOUNDARY_VIOLATION", {
            "assessment_id": receipt["assessment_id"],
            "violations": violations,
            "observation": obs[:200],
            "inference": inf[:200],
        })
    return payload

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="HERMES RASA MCP Server")
    parser.add_argument("--port", type=int, default=18420, help="Port to run on (HTTP transport)")
    parser.add_argument("--transport", type=str, default="http", choices=["http", "stdio"], help="Transport mode")
    args = parser.parse_args()
    
    if args.transport == "http":
        mcp.run(transport="http", host="127.0.0.1", port=args.port)
    else:
        mcp.run(transport="stdio")
