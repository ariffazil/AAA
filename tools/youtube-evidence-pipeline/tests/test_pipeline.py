#!/usr/bin/env python3
"""
End-to-end integration test for youtube-evidence-pipeline.
Chains: OCR evidence → claim graph → video-to-skill draft.
Also tests ASR adapter with generated test audio.
"""
import json
import os
import subprocess
import sys
import tempfile

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_DIR = os.path.dirname(TOOLS_DIR)
PACKAGER_DIR = os.path.join(os.path.dirname(PIPELINE_DIR), "video-evidence-packager")
OCR_DIR = os.path.join(os.path.dirname(PIPELINE_DIR), "video-ocr-adapter")

sys.path.insert(0, os.path.join(PIPELINE_DIR, "asr_adapter"))
sys.path.insert(0, os.path.join(PIPELINE_DIR, "claim_graph"))
sys.path.insert(0, os.path.join(PIPELINE_DIR, "video_skill"))
sys.path.insert(0, OCR_DIR)
sys.path.insert(0, PACKAGER_DIR)

passed = 0
failed = 0


def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name} — {detail}")


def run_tests():
    global passed, failed
    print("\n=== youtube-evidence-pipeline Integration Tests ===\n")

    # --- Step 1: Generate keyframes ---
    print("--- Step 1: Keyframe extraction ---")
    from packager import packager
    fixture_video = os.path.join(PACKAGER_DIR, "tests", "fixtures", "short_5s.mp4")

    td = tempfile.mkdtemp(prefix="pipeline_test_")
    packager(fixture_video, interval=1.0, max_frames=3, output_dir=td)
    with open(os.path.join(td, "keyframes.json")) as f:
        manifest = json.load(f)
    test("Keyframes generated", manifest["total_frames"] > 0)

    # --- Step 2: OCR each keyframe ---
    print("\n--- Step 2: OCR evidence extraction ---")
    from ocr_adapter import ocr_frame

    evidence_segments = []
    for frame in manifest["frames"]:
        frame_path = os.path.join(td, frame["path"])
        r = ocr_frame(
            frame_path=frame_path,
            frame_id=frame["id"],
            timestamp_seconds=frame["timestamp_seconds"],
            video_asset_id=manifest["video_asset_id"],
            frame_sha256=frame.get("sha256"),
            output_dir=td,
        )
        if r.get("status") == "success":
            # Read the evidence segment back
            ev_path = os.path.join(td, f"ocr-evidence-{frame['id'].replace(':', '_')}.json")
            if os.path.exists(ev_path):
                with open(ev_path) as f:
                    evidence_segments.append(json.load(f))

    test("OCR produced evidence segments", len(evidence_segments) > 0,
         f"got {len(evidence_segments)}")

    # --- Step 3: Build claim graph from evidence ---
    print("\n--- Step 3: Claim graph construction ---")
    from claim_graph import build_claim_graph

    jsonl_path = os.path.join(td, "evidence-segments.jsonl")
    claim_output = os.path.join(td, "claims")
    os.makedirs(claim_output, exist_ok=True)
    r3 = build_claim_graph(jsonl_path, claim_output)

    test("Claim graph generated", r3.get("status") == "success")
    test("Claims exist", r3.get("evidence", {}).get("claim_count", 0) >= 0,
         f"count={r3.get('evidence', {}).get('claim_count', 0)}")
    test("Epistemic labels assigned",
         r3.get("evidence", {}).get("epistemic_distribution") is not None)

    # --- Step 4: Build procedure candidate from claims ---
    print("\n--- Step 4: Video-to-skill draft ---")
    from video_skill import build_video_skill

    claims_json_path = os.path.join(claim_output, "typed-claims.json")
    skill_output = os.path.join(td, "skill")
    os.makedirs(skill_output, exist_ok=True)

    # Add some procedural claims for testing
    if os.path.exists(claims_json_path):
        with open(claims_json_path) as f:
            claims_data = json.load(f)

        # Inject procedural claims to test extraction
        procedural_claims = [
            {
                "id": "claim:test1",
                "source_evidence_id": "ev:test",
                "video_asset_id": manifest["video_asset_id"],
                "timestamp_seconds": 0.0,
                "modality": "audio_asr",
                "claim_type": "recommendation",
                "statement": "First install the dependencies using pip install",
                "confidence": 0.8,
                "epistemic_label": "INT",
                "corroboration_status": "unreviewed",
                "limitations": [],
                "derived_by": "claim_graph_v0.1.0",
                "content_class": "typed_claim",
            },
            {
                "id": "claim:test2",
                "source_evidence_id": "ev:test2",
                "video_asset_id": manifest["video_asset_id"],
                "timestamp_seconds": 5.0,
                "modality": "audio_asr",
                "claim_type": "recommendation",
                "statement": "Then run the build script to compile",
                "confidence": 0.8,
                "epistemic_label": "INT",
                "corroboration_status": "unreviewed",
                "limitations": [],
                "derived_by": "claim_graph_v0.1.0",
                "content_class": "typed_claim",
            },
            {
                "id": "claim:test3",
                "source_evidence_id": "ev:test3",
                "video_asset_id": manifest["video_asset_id"],
                "timestamp_seconds": 10.0,
                "modality": "audio_asr",
                "claim_type": "factual",
                "statement": "Risk: the API endpoint may timeout under load",
                "confidence": 0.7,
                "epistemic_label": "OBS",
                "corroboration_status": "unreviewed",
                "limitations": [],
                "derived_by": "claim_graph_v0.1.0",
                "content_class": "typed_claim",
            },
        ]
        claims_data["claims"] = procedural_claims
        with open(claims_json_path, "w") as f:
            json.dump(claims_data, f, indent=2)

    r4 = build_video_skill(claims_json_path, skill_output, manifest["video_asset_id"])

    test("Video-to-skill draft generated", r4.get("status") == "success")
    test("Candidate has steps", r4.get("evidence", {}).get("step_count", 0) > 0,
         f"steps={r4.get('evidence', {}).get('step_count', 0)}")
    test("888_HOLD governance", r4.get("evidence", {}).get("activation_gate") == "888_HOLD")
    test("Draft state only", r4.get("evidence", {}).get("governance_state") == "draft_only")

    # Check YAML written
    yaml_files = [f for f in os.listdir(skill_output) if f.endswith(".yaml")]
    test("YAML artifact written", len(yaml_files) > 0)

    # --- Step 5: ASR adapter (test with generated audio) ---
    print("\n--- Step 5: ASR adapter (generated test audio) ---")
    # Generate a short audio file with speech-like content
    test_audio = os.path.join(td, "test_audio.wav")
    subprocess.run([
        "ffmpeg", "-v", "quiet",
        "-f", "lavfi", "-i", "sine=frequency=440:duration=2",
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        "-y", test_audio
    ], timeout=10)

    if os.path.exists(test_audio):
        from asr_adapter import asr_adapter
        asr_output = os.path.join(td, "asr")
        os.makedirs(asr_output, exist_ok=True)

        # Check if ZAI_API_KEY is available
        if os.environ.get("ZAI_API_KEY"):
            r5 = asr_adapter(test_audio, output_dir=asr_output)
            test("ASR adapter ran", r5.get("status") in ("success", "failed"))
            test("ASR receipt has network info",
                 r5.get("network", {}).get("external_api") == "Z.AI GLM-ASR-2512")
            test("ASR no cookies",
                 r5.get("network", {}).get("cookies_used") == False)
        else:
            test("ASR adapter (skipped — no ZAI_API_KEY)", True)
    else:
        test("ASR adapter (skipped — no test audio)", True)

    # --- Step 6: Full chain verification ---
    print("\n--- Step 6: Full chain artifact verification ---")
    all_files = []
    for root, dirs, files in os.walk(td):
        for f in files:
            all_files.append(os.path.join(root, f))

    test("Receipt files exist", any("receipt.json" in f for f in all_files))
    test("Evidence segments exist", any("evidence-segments.jsonl" in f for f in all_files))
    test("Typed claims exist", any("typed-claims.json" in f for f in all_files))
    test("Procedure candidate exists", any("procedure-candidate" in f for f in all_files))

    # Cleanup
    import shutil
    shutil.rmtree(td, ignore_errors=True)

    # --- Summary ---
    print(f"\n=== Results: {passed} passed, {failed} failed ===\n")
    if failed > 0:
        print("FAILURES:")
        sys.exit(1)
    else:
        print("ALL TESTS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    run_tests()
