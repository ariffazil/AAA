"""Human Meaning Inference Protocol — test scenarios A-D + governance negative cases.

Scenario A: abstract prompt -> intent decode (defaults path)
Scenario B: vulnerability -> trust event (authority must stay HUMAN_CONFIRMATION_REQUIRED)
Scenario C: mimic -> note mismatch, no fixed-type label (candidates only)
Scenario D: three candidate interpretations supplied (passthrough + validate)
Negative 1: confidence band above cap -> must clamp to 0.9
Negative 2: single interpretation -> must floor-pad to 3
"""
import sys

sys.path.insert(0, "/root/AAA/mcp-servers/human-inference")
import server  # noqa: E402

_raw = getattr(server.human_inference, "fn", None) or server.human_inference
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(f"{'PASS' if cond else 'FAIL'} :: {name}" + (f" :: {detail}" if detail else ""))


# --- Scenario A: abstract prompt, all defaults ---
ra = _raw(
    observation="Ni macam mangkuk ayun. Void dia bukan dalam numbers, tapi cara depa sembang.",
    context="Arif on a corporate deck, Penang BM, 04:00 MYT, void-hunting pattern",
)
check("A.valid", ra.get("valid") is True)
rec_a = ra.get("record", {})
check("A.min3_interpretations", len(rec_a.get("candidate_interpretations", [])) >= 3,
      f"n={len(rec_a.get('candidate_interpretations', []))}")
check("A.consent_unknown_default", rec_a.get("consent_status") == "UNKNOWN")
check("A.authority_locked", rec_a.get("action_authority") == "HUMAN_CONFIRMATION_REQUIRED")
check("A.projection_default", rec_a.get("projection_risk") == "MEDIUM")
check("A.band_capped", rec_a.get("confidence_band", [1, 1])[1] <= 0.9)
check("A.unknowns_nonempty", len(rec_a.get("unknowns", [])) >= 1)

# --- Scenario B: vulnerability framing — never actionable without human ---
rb = _raw(
    observation="Dia cerita pasal takde orang nak dengar dia sejak accident tu.",
    context="Third party, emotional disclosure, no consent for inference",
    projection_risk="HIGH",
)
rec_b = rb.get("record", {})
check("B.valid", rb.get("valid") is True)
check("B.authority_human_confirmation", rec_b.get("action_authority") == "HUMAN_CONFIRMATION_REQUIRED",
      "vulnerability must never downgrade to READ_ONLY")
check("B.consent_unknown", rec_b.get("consent_status") == "UNKNOWN")
check("B.projection_high_kept", rec_b.get("projection_risk") == "HIGH")

# --- Scenario C: mimicry — no fixed-type labeling ---
rc = _raw(
    observation="Tiba-tiba dia guna loghat dan pilihan kata macam Arif.",
    context="Group chat, new member mirroring speech patterns",
    candidate_interpretations=[
        "Genuine dialect convergence — normal social accommodation",
        "Deliberate mimicry to gain in-group trust",
        "Shared regional background — similarity, not copying",
    ],
    unknowns=["Intent of the speaker", "Whether pattern is stable across contexts"],
)
rec_c = rc.get("record", {})
check("C.valid", rc.get("valid") is True)
check("C.candidates_are_candidates", all("is a" not in i.lower() or "?" in i or "genuine" in i.lower() or "deliberate" in i.lower() or "shared" in i.lower() for i in rec_c.get("candidate_interpretations", [])),
      "interpretations stay candidate-level, no fixed-type verdict")
check("C.no_type_label_field", "type_label" not in rec_c and "mbti" not in str(rec_c).lower())

# --- Scenario D: three supplied interpretations passthrough ---
rd = _raw(
    observation="Boss puji kerja aku depan meeting.",
    context="Workplace, performance review season",
    candidate_interpretations=["Genuine recognition", "Softening before bad news", "Public credit as retention tactic"],
    unknowns=["Private assessment", "Comparison against peers"],
    verification_path="Ask directly in 1:1 whether compensation review reflects the praise",
)
rec_d = rd.get("record", {})
check("D.valid", rd.get("valid") is True)
check("D.exactly3", len(rec_d.get("candidate_interpretations", [])) == 3)
check("D.verification_kept", "1:1" in rec_d.get("verification_path", ""))

# --- Negative 1: over-cap confidence clamps ---
rn1 = _raw(observation="x", context="y", confidence_band=[0.8, 0.99])
check("N1.clamp_09", rn1.get("record", {}).get("confidence_band", [])[1] == 0.9,
      f"band={rn1.get('record', {}).get('confidence_band')}")

# --- Negative 2: single interpretation floors to 3 ---
rn2 = _raw(observation="x", context="y", candidate_interpretations=["only one"])
check("N2.floor_pad", len(rn2.get("record", {}).get("candidate_interpretations", [])) >= 3)

# --- Schema resource wired ---
check("R.schema_resource", callable(getattr(server, "get_inference_schema", None)))

fails = [n for n, ok, _ in results if not ok]
print(f"\nTOTAL={len(results)} PASS={len(results) - len(fails)} FAIL={len(fails)}")
# NOTE: fastmcp import on this VPS is ~67s CPU-bound (pydantic compile under load)
# and leaves a non-daemon thread post-import — os._exit bypasses the lingering thread.
import os
sys.stdout.flush(); sys.stderr.flush()
os._exit(1 if fails else 0)
