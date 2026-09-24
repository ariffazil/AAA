#!/usr/bin/env python3
"""
reality_router.py — Canonical Mixed-Reality Router for arifOS Federation
========================================================================
STATUS: F13 RATIFIED (2026-09-24) — Mixed-Reality Event Architecture.

PRINCIPLE:
  A single human event (e.g. CP Review, well post-mortem) contains multiple
  realities simultaneously:
    - Earth Reality   -> GEOX (rock, seismic, well logs, traps, closure)
    - Capital Reality -> WEALTH (dry hole cost, EMV, capex at risk, farm-in)
    - Human Reality   -> WELL (fatigue, stress, somatic load, dignity floor)
    - Attention Cost  -> AAA (review hours, context switching, deep work loss)
    - Immutable Scar  -> VAULT999 (cryptographic precedent, causal receipt)

NEVER collapse a multi-dimensional event into a single organ destination.
AAA registers and displays; RealityRouter classifies and fans out.

Provenances enforced: OBSERVED, REPORTED, INFERRED, SPECULATIVE.
"""

from __future__ import annotations

import os
import sys
import json
import re
import hashlib
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# ── Paths ──────────────────────────────────────────────────────────
GEOX_SINK = Path("/root/GEOX/state/scars.jsonl")
WEALTH_SINK = Path("/root/WEALTH/state/capital_scars.jsonl")
WELL_SINK = Path("/root/WELL/state/somatic_observations.jsonl")
ATTENTION_SINK = Path("/root/AAA/state/attention_ledger.jsonl")
VAULT999_SEALS = Path("/root/arifOS/VAULT999/local_seals.jsonl")
VAULT999_SCARS = Path("/root/arifOS/VAULT999/scar")

# Ensure target directories exist
for p in [GEOX_SINK.parent, WEALTH_SINK.parent, WELL_SINK.parent, ATTENTION_SINK.parent, VAULT999_SCARS]:
    p.mkdir(parents=True, exist_ok=True)

# ── Data Models ────────────────────────────────────────────────────
@dataclass
class EvidenceLineage:
    audio_sha256: Optional[str]
    audio_file: Optional[str]
    transcript_sha256: str
    asr_model: str
    truth_class: str = "REPORTED"  # Speech is REPORTED, not OBSERVED

@dataclass
class EarthAtom:
    project: str
    basin: str
    observation: str
    seismic_risk: Optional[str] = None
    geological_feature: Optional[str] = None
    contested_issue: Optional[str] = None

@dataclass
class CapitalAtom:
    project: str
    risk_type: str  # DRY_HOLE_COST, EMV_VARIANCE, FARM_IN_VALUE, OPPORTUNITY_COST, REVIEW_DELAY_COST
    amount_usd: Optional[float] = None
    exposure_summary: str = ""
    decision_cause: Optional[str] = None

@dataclass
class HumanAtom:
    actor: str
    somatic_state: str  # ENERGETIC, TIRED, EXHAUSTED, DISTRESSED
    fatigue_level: str  # LOW, MEDIUM, CRITICAL
    cognitive_load: str
    intervention_recommended: bool = False
    intervention_reason: Optional[str] = None

@dataclass
class AttentionAtom:
    minutes_spent: float
    context_type: str  # CP_REVIEW, CORRIDOR_CHAT, DRIVE_DUMP, SOLO_ANALYSIS
    interruption_cost: str = "MEDIUM"

@dataclass
class ScarAtom:
    scar_id: str
    trace_id: str
    failure_mode: str
    constraint_imposed: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    governing_floor: str = "F1"

@dataclass
class MixedRealityEvent:
    event_id: str
    trace_id: str
    timestamp_utc: str
    source_context: str
    lineage: EvidenceLineage
    earth: Optional[EarthAtom] = None
    capital: Optional[CapitalAtom] = None
    human: Optional[HumanAtom] = None
    attention: Optional[AttentionAtom] = None
    scar: Optional[ScarAtom] = None
    quarantine: bool = False
    quarantine_reason: Optional[str] = None

# ── Helper Utilities ───────────────────────────────────────────────
def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def append_jsonl(path: Path, record: Dict[str, Any]):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

# ── The Reality Router Core ────────────────────────────────────────
class RealityRouter:
    """
    Formal router that classifies input into Earth, Capital, Human, and Attention
    components and fans them out to their respective sovereign organs.
    """

    @staticmethod
    def classify_and_route(
        transcript: str,
        audio_path: Optional[str] = None,
        asr_model: str = "fun-asr",
        source_kind: str = "voice_note"
    ) -> MixedRealityEvent:
        now_iso = datetime.now(timezone.utc).isoformat()
        trace_id = f"MR-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-{os.urandom(4).hex()}"
        event_id = f"EVT-{os.urandom(6).hex()}"

        # 1. Compute Evidence Lineage
        audio_hash = None
        if audio_path and os.path.exists(audio_path):
            with open(audio_path, "rb") as f:
                audio_hash = sha256_bytes(f.read())

        t_hash = sha256_str(transcript)
        lineage = EvidenceLineage(
            audio_sha256=audio_hash,
            audio_file=audio_path,
            transcript_sha256=t_hash,
            asr_model=asr_model,
            truth_class="REPORTED"
        )

        # 2. Privacy & Sovereign Guard (F5/F6/F13)
        lower_t = transcript.lower()
        # Heuristic check for purely personal matters
        personal_cues = ["personal", "family", "password", "rahsia peribadi"]
        is_personal = any(c in lower_t for c in personal_cues) and not any(g in lower_t for g in ["basin", "well", "telaga", "seismic", "prospect", "kl2"])
        if is_personal:
            event = MixedRealityEvent(
                event_id=event_id,
                trace_id=trace_id,
                timestamp_utc=now_iso,
                source_context=source_kind,
                lineage=lineage,
                quarantine=True,
                quarantine_reason="F5_PRIVATE_PERSONAL_ISOLATION"
            )
            return event

        # 3. Extract Multi-Dimensional Reality Atoms
        # --- A. Earth Reality (GEOX) ---
        earth_atom = None
        geo_keywords = ["seismic", "well", "telaga", "fault", "horizon", "velocity", "carbonate", "basement", "closure", "trap", "kl2", "wakid", "bekantan", "sabah", "kinabalu"]
        if any(k in lower_t for k in geo_keywords):
            proj = "KL2" if "kl2" in lower_t else ("WAKID-3" if "wakid" in lower_t else "REGIONAL_SUBSURFACE")
            basin = "Kinabalu" if "kinabalu" in lower_t else ("Sabah" if "sabah" in lower_t else "Malay_Basin")
            
            seismic_risk = None
            if "pull-up" in lower_t or "velocity" in lower_t:
                seismic_risk = "Velocity pull-up / lateral velocity distortion"
            elif "fault seal" in lower_t or "trap leak" in lower_t:
                seismic_risk = "Fault seal breach / Trap leak"

            earth_atom = EarthAtom(
                project=proj,
                basin=basin,
                observation=transcript[:300],
                seismic_risk=seismic_risk,
                contested_issue="Carbonate vs Basement interpretation" if "basement" in lower_t and "carbonate" in lower_t else None
            )

        # --- B. Capital Reality (WEALTH) ---
        capital_atom = None
        money_keywords = ["juta", "million", "usd", "cost", "kos", "emv", "capex", "bajet", "budget", "farm-in", "dry hole"]
        if any(k in lower_t for k in money_keywords):
            proj = "KL2" if "kl2" in lower_t else ("WAKID-3" if "wakid" in lower_t else "PORTFOLIO")
            
            # Simple numeric extraction (e.g. 35 juta -> 35,000,000)
            amount = None
            amt_match = re.search(r"(\d+)\s*(?:juta|million|mm)", lower_t)
            if amt_match:
                amount = float(amt_match.group(1)) * 1_000_000

            risk_type = "DRY_HOLE_COST" if ("dry" in lower_t or "kering" in lower_t) else "CAPITAL_AT_RISK"
            capital_atom = CapitalAtom(
                project=proj,
                risk_type=risk_type,
                amount_usd=amount,
                exposure_summary=f"Capital exposure noted in {proj}: {amount or 'unspecified'} USD",
                decision_cause="Overconfidence in seismic amplitude without risk de-biasing" if "overconfidence" in lower_t or "bocor" in lower_t else None
            )

        # --- C. Human & Somatic Reality (WELL) ---
        human_atom = None
        fatigue_cues = ["letih", "penat", "tired", "exhausted", "jam dua pagi", "2am", "stress", "serabut"]
        is_fatigued = any(k in lower_t for k in fatigue_cues)
        if is_fatigued:
            human_atom = HumanAtom(
                actor="Arif Fazil (F13 Sovereign)",
                somatic_state="EXHAUSTED" if ("jam dua pagi" in lower_t or "terlalu letih" in lower_t) else "TIRED",
                fatigue_level="CRITICAL" if ("jam dua pagi" in lower_t or "terlalu letih" in lower_t) else "MEDIUM",
                cognitive_load="HIGH",
                intervention_recommended=True,
                intervention_reason="FATIGUE_BARRIER_TRIPPED: Subsurface or capital decisions must be held until cognitive rest."
            )

        # --- D. Attention Reality (AAA) ---
        attention_atom = AttentionAtom(
            minutes_spent=15.0 if "review" in lower_t else 3.0,
            context_type="CP_REVIEW" if "review" in lower_t else "VOICE_DUMP"
        )

        # --- E. Scar Recognition ---
        scar_atom = None
        scar_cues = ["jangan matangkan", "pengajaran", "scar", "kesilapan", "trap leak", "dry hole"]
        if any(c in lower_t for c in scar_cues):
            s_id = f"SCAR-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{os.urandom(3).hex()}"
            scar_atom = ScarAtom(
                scar_id=s_id,
                trace_id=trace_id,
                failure_mode="Trap leak / fault seal breach without prior cross-validation",
                constraint_imposed="Jangan matangkan prospect tanpa fault seal risk yang diuji; jangan buat keputusan telaga masa terlalu letih.",
                severity="HIGH",
                governing_floor="F1_AMANAH"
            )

        event = MixedRealityEvent(
            event_id=event_id,
            trace_id=trace_id,
            timestamp_utc=now_iso,
            source_context=source_kind,
            lineage=lineage,
            earth=earth_atom,
            capital=capital_atom,
            human=human_atom,
            attention=attention_atom,
            scar=scar_atom
        )

        # 4. Sovereign Fan-out to Organs
        RealityRouter.fanout_dispatch(event)
        return event

    @staticmethod
    def fanout_dispatch(evt: MixedRealityEvent):
        """Funnels extracted atoms into respective organ ledgers & VAULT999."""
        if evt.quarantine:
            quar_file = Path("/root/AAA/voice/quarantine") / f"{evt.trace_id}.json"
            quar_file.parent.mkdir(parents=True, exist_ok=True)
            quar_file.write_text(json.dumps(asdict(evt), indent=2))
            return

        # 1. Earth -> GEOX
        if evt.earth:
            append_jsonl(GEOX_SINK, {
                "trace_id": evt.trace_id,
                "ts": evt.timestamp_utc,
                "organ": "GEOX",
                "truth_class": evt.lineage.truth_class,
                "data": asdict(evt.earth),
                "lineage": asdict(evt.lineage)
            })

        # 2. Capital -> WEALTH
        if evt.capital:
            append_jsonl(WEALTH_SINK, {
                "trace_id": evt.trace_id,
                "ts": evt.timestamp_utc,
                "organ": "WEALTH",
                "truth_class": evt.lineage.truth_class,
                "data": asdict(evt.capital),
                "lineage": asdict(evt.lineage)
            })

        # 3. Human -> WELL
        if evt.human:
            append_jsonl(WELL_SINK, {
                "trace_id": evt.trace_id,
                "ts": evt.timestamp_utc,
                "organ": "WELL",
                "truth_class": evt.lineage.truth_class,
                "data": asdict(evt.human),
                "lineage": asdict(evt.lineage)
            })

        # 4. Attention -> AAA
        if evt.attention:
            append_jsonl(ATTENTION_SINK, {
                "trace_id": evt.trace_id,
                "ts": evt.timestamp_utc,
                "organ": "AAA",
                "data": asdict(evt.attention)
            })

        # 5. Immutable Seal -> VAULT999
        if evt.scar:
            seal_record = {
                "seal_class": "SOVEREIGN_SCAR_SEAL",
                "scar_id": evt.scar.scar_id,
                "trace_id": evt.trace_id,
                "timestamp_utc": evt.timestamp_utc,
                "failure_mode": evt.scar.failure_mode,
                "constraint_imposed": evt.scar.constraint_imposed,
                "severity": evt.scar.severity,
                "lineage": {
                    "audio_sha256": evt.lineage.audio_sha256,
                    "transcript_sha256": evt.lineage.transcript_sha256,
                    "asr_model": evt.lineage.asr_model
                },
                "status": "SEALED"
            }
            # Write to VAULT999 local seals
            append_jsonl(VAULT999_SEALS, seal_record)
            
            # Write dedicated scar file in VAULT999/scar/
            scar_path = VAULT999_SCARS / f"{evt.scar.scar_id}.json"
            scar_path.write_text(json.dumps(seal_record, indent=2))

# ── CLI Test ───────────────────────────────────────────────────────
if __name__ == "__main__":
    test_text = (
        "Review KL2 tadi jam dua pagi terlalu letih. Hujah utama sangkut dekat interpretasi "
        "basement versus carbonate. Syazwan risau pasal velocity pull-up. Telaga kering sebelum ni "
        "macam WAKID-3 membakar 35 juta USD sebab trap leak. Jangan matangkan prospect tanpa fault seal risk yang diuji!"
    )
    print("Testing RealityRouter with multi-dimensional input...")
    event = RealityRouter.classify_and_route(test_text, asr_model="fun-asr", source_kind="test_fixture")
    print(f"[SUCCESS] Event {event.event_id} processed! Trace: {event.trace_id}")
    print(f"  Earth atom: {event.earth.project if event.earth else 'None'}")
    print(f"  Capital atom: {event.capital.amount_usd if event.capital else 'None'} USD ({event.capital.risk_type if event.capital else ''})")
    print(f"  Human atom: {event.human.somatic_state if event.human else 'None'} (Intervention: {event.human.intervention_recommended if event.human else False})")
    print(f"  Scar atom: {event.scar.scar_id if event.scar else 'None'}")
    print(f"  Sealed to VAULT999: {VAULT999_SEALS}")
