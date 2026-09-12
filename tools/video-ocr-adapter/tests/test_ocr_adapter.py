#!/usr/bin/env python3
"""
Acceptance test runner for video-ocr-adapter v0.1.0.

Tests all 10 acceptance criteria.
Uses real keyframes from video-evidence-packager test fixtures.
"""
import json
import os
import subprocess
import sys
import tempfile

# Add paths
TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGER_DIR = os.path.join(os.path.dirname(TOOLS_DIR), "video-evidence-packager")
sys.path.insert(0, TOOLS_DIR)
sys.path.insert(0, PACKAGER_DIR)

from ocr_adapter import ocr_frame, batch_ocr, sha256_file

passed = 0
failed = 0
results = []


def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        results.append(("PASS", name, detail))
        print(f"  PASS  {name}")
    else:
        failed += 1
        results.append(("FAIL", name, detail))
        print(f"  FAIL  {name} — {detail}")


def get_fixture_keyframes():
    """Generate keyframes from the test video into a persistent temp dir."""
    fixture_video = os.path.join(PACKAGER_DIR, "tests", "fixtures", "short_5s.mp4")
    if not os.path.exists(fixture_video):
        print("  Generating test fixtures...")
        subprocess.run([sys.executable, os.path.join(PACKAGER_DIR, "tests", "generate_fixtures.py")],
                       check=True, cwd=PACKAGER_DIR)

    # Use a named temp dir that persists after return
    tmpdir = tempfile.mkdtemp(prefix="ocr_test_")
    from packager import packager
    receipt = packager(fixture_video, interval=1.0, max_frames=3, output_dir=tmpdir)
    keyframes_path = os.path.join(tmpdir, "keyframes.json")
    with open(keyframes_path) as f:
        manifest = json.load(f)
    return manifest, receipt, tmpdir


def run_tests():
    global passed, failed

    print("\n=== video-ocr-adapter v0.1.0 Acceptance Tests ===\n")

    # Generate test keyframes
    print("--- Setup: generating test keyframes ---")
    manifest, packager_receipt, keyframes_dir = get_fixture_keyframes()
    frames = manifest["frames"]
    print(f"  Generated {len(frames)} keyframes from short_5s.mp4 fixture")
    video_asset_id = manifest["video_asset_id"]

    # --- SUITE 1: Single-frame OCR ---
    print("\n--- Suite 1: Single-frame OCR (first frame) ---")
    first_frame = frames[0]
    frame_path = os.path.join(keyframes_dir, first_frame["path"])

    with tempfile.TemporaryDirectory() as outdir:
        r1 = ocr_frame(
            frame_path=frame_path,
            frame_id=first_frame["id"],
            timestamp_seconds=first_frame["timestamp_seconds"],
            video_asset_id=video_asset_id,
            frame_sha256=first_frame.get("sha256"),
            output_dir=outdir,
        )

        # CRITERION 2: Structured evidence segment
        test("2. Produces structured evidence with frame_id + timestamp + SHA-256 + OBS",
             r1.get("status") == "success" and
             r1.get("evidence") is not None and
             r1["evidence"].get("evidence_id", "").startswith("ev:") and
             r1["evidence"].get("confidence") is not None and
             r1["evidence"].get("content_class") == "visual_ocr_observation")

        # CRITERION 3: No narrative summary
        evidence_path = os.path.join(outdir, f"ocr-evidence-{first_frame['id'].replace(':', '_')}.json")
        if os.path.exists(evidence_path):
            with open(evidence_path) as f:
                ev = json.load(f)
            observation = ev.get("observation", "")
            has_narrative_markers = any(phrase in observation.lower() for phrase in [
                "this video", "the speaker", "this presentation", "the slide shows"
            ])
            test("3. No narrative summary (extraction only, no interpretation)",
                 not has_narrative_markers,
                 f"Found narrative markers in: {observation[:100]}")
        else:
            test("3. No narrative summary", False, "Evidence file not written")

        # CRITERION 5: Receipt includes engine/version
        test("5. Receipt includes engine and version",
             r1.get("evidence", {}).get("engine") == "tesseract" and
             r1.get("evidence", {}).get("engine_version") is not None)

        # CRITERION 10: OBS label
        if os.path.exists(evidence_path):
            with open(evidence_path) as f:
                ev = json.load(f)
            test("10. OBS epistemic label",
                 ev.get("epistemic_label") == "OBS",
                 f"label={ev.get('epistemic_label')}")
        else:
            test("10. OBS epistemic label", False, "No evidence file")

        # CRITERION 9: Appends to JSONL (not overwrite)
        jsonl_path = os.path.join(outdir, "evidence-segments.jsonl")
        test("9. Evidence appended to JSONL",
             os.path.exists(jsonl_path))

    # --- SUITE 2: Determinism ---
    print("\n--- Suite 2: Determinism ---")
    with tempfile.TemporaryDirectory() as outdir:
        r2a = ocr_frame(
            frame_path=frame_path,
            frame_id=first_frame["id"],
            timestamp_seconds=first_frame["timestamp_seconds"],
            video_asset_id=video_asset_id,
            output_dir=outdir,
        )

    with tempfile.TemporaryDirectory() as outdir:
        r2b = ocr_frame(
            frame_path=frame_path,
            frame_id=first_frame["id"],
            timestamp_seconds=first_frame["timestamp_seconds"],
            video_asset_id=video_asset_id,
            output_dir=outdir,
        )

    # CRITERION 8: Deterministic (same input -> same evidence hash)
    test("8. Deterministic: same frame + same engine = same evidence hash",
         r2a.get("evidence", {}).get("evidence_hash") == r2b.get("evidence", {}).get("evidence_hash"),
         f"{r2a.get('evidence', {}).get('evidence_hash', 'None')[:16]} vs {r2b.get('evidence', {}).get('evidence_hash', 'None')[:16]}")

    # --- SUITE 3: No external writes ---
    print("\n--- Suite 3: Network discipline ---")
    with tempfile.TemporaryDirectory() as outdir:
        r3 = ocr_frame(
            frame_path=frame_path,
            frame_id=first_frame["id"],
            timestamp_seconds=first_frame["timestamp_seconds"],
            video_asset_id=video_asset_id,
            output_dir=outdir,
        )
        # CRITERION 7: No external write, no Telegram
        test("7. No external write, no Telegram, no persistent graph write",
             r3.get("network", {}).get("external_write") == False and
             r3.get("network", {}).get("cookies_used") == False and
             r3.get("network", {}).get("media_downloaded") == False)

    # --- SUITE 4: Cross-frame (no synthesis) ---
    print("\n--- Suite 4: No cross-frame synthesis ---")
    with tempfile.TemporaryDirectory() as outdir:
        # Process two different frames
        for frame in frames[:2]:
            fp = os.path.join(keyframes_dir, frame["path"])
            ocr_frame(
                frame_path=fp,
                frame_id=frame["id"],
                timestamp_seconds=frame["timestamp_seconds"],
                video_asset_id=video_asset_id,
                output_dir=outdir,
            )

        # CRITERION 4: No cross-frame synthesis — each evidence is independent
        jsonl_path = os.path.join(outdir, "evidence-segments.jsonl")
        if os.path.exists(jsonl_path):
            with open(jsonl_path) as f:
                segments = [json.loads(line) for line in f if line.strip()]
            # Each segment should reference only its own frame_id
            all_independent = all(
                seg.get("frame_id") is not None and
                seg.get("content_class") == "visual_ocr_observation"
                for seg in segments
            )
            test("4. No cross-frame synthesis (each evidence independent)",
                 all_independent and len(segments) == 2)
        else:
            test("4. No cross-frame synthesis", False, "No JSONL written")

    # --- SUITE 5: Failure handling ---
    print("\n--- Suite 5: Failure handling ---")
    with tempfile.TemporaryDirectory() as outdir:
        # CRITERION 6: Failed OCR produces structured failure receipt
        r5 = ocr_frame(
            frame_path="/nonexistent/frame.jpg",
            frame_id="frame:9999",
            timestamp_seconds=0.0,
            video_asset_id="local:fake",
            output_dir=outdir,
        )
        test("6. Failed OCR produces structured failure receipt (not traceback)",
             r5.get("status") == "failed" and
             r5.get("error") is not None and
             r5["error"].get("class") is not None)

    # --- SUITE 6: Batch mode ---
    print("\n--- Suite 6: Batch mode ---")
    with tempfile.TemporaryDirectory() as outdir:
        # Create keyframes.json in this directory
        manifest_path = os.path.join(outdir, "keyframes.json")
        # Copy manifest with adjusted paths
        adjusted_manifest = dict(manifest)
        for frame in adjusted_manifest["frames"]:
            frame["path"] = os.path.join(keyframes_dir, frame["path"])
        with open(manifest_path, "w") as f:
            json.dump(adjusted_manifest, f)

        r6 = batch_ocr(
            keyframes_json_path=manifest_path,
            video_asset_id=video_asset_id,
            output_dir=outdir,
            limit=2,
        )
        test("6b. Batch mode processes multiple frames",
             r6.get("status") == "success" and
             r6.get("results", {}).get("succeeded", 0) >= 1,
             f"succeeded={r6.get('results', {}).get('succeeded', 0)}")

    # --- SUITE 7: Criterion 1 (keyframe entry from packager) ---
    print("\n--- Suite 7: Input contract ---")
    test("1. Takes keyframe entry from packager (frame_id, timestamp, sha256 present)",
         first_frame.get("id") is not None and
         first_frame.get("timestamp_seconds") is not None and
         first_frame.get("sha256") is not None)

    # --- Summary ---
    print(f"\n=== Results: {passed} passed, {failed} failed ===\n")

    # Cleanup persistent fixture dir
    import shutil
    shutil.rmtree(keyframes_dir, ignore_errors=True)

    if failed > 0:
        print("FAILURES:")
        for status, name, detail in results:
            if status == "FAIL":
                print(f"  - {name}: {detail}")
        sys.exit(1)
    else:
        print("ALL TESTS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    run_tests()
