#!/usr/bin/env python3
"""
Generate deterministic test fixtures for video-evidence-packager v0.
Creates: short video (5s), corrupt file, empty file.
Requires: ffmpeg.
"""
import os
import subprocess
import sys

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
os.makedirs(FIXTURES_DIR, exist_ok=True)


def generate_short_video():
    """5-second test video with color bars and 1kHz tone."""
    path = os.path.join(FIXTURES_DIR, "short_5s.mp4")
    if os.path.exists(path):
        print(f"  EXISTS  {path}")
        return path
    cmd = [
        "ffmpeg", "-y", "-v", "quiet",
        "-f", "lavfi", "-i", "testsrc=duration=5:size=640x480:rate=25",
        "-f", "lavfi", "-i", "sine=frequency=1000:duration=5",
        "-c:v", "libx264", "-preset", "ultrafast",
        "-c:a", "aac", "-b:a", "64k",
        "-shortest",
        path,
    ]
    subprocess.run(cmd, check=True, timeout=30)
    print(f"  CREATED {path}")
    return path


def generate_corrupt_file():
    """A file with random bytes — not a valid video."""
    path = os.path.join(FIXTURES_DIR, "corrupt.xyz")
    if os.path.exists(path):
        print(f"  EXISTS  {path}")
        return path
    with open(path, "wb") as f:
        f.write(os.urandom(1024))
    print(f"  CREATED {path}")
    return path


def generate_empty_file():
    """Zero-byte file."""
    path = os.path.join(FIXTURES_DIR, "empty.mp4")
    if os.path.exists(path):
        print(f"  EXISTS  {path}")
        return path
    with open(path, "w") as f:
        pass
    print(f"  CREATED {path}")
    return path


if __name__ == "__main__":
    print("Generating test fixtures...")
    generate_short_video()
    generate_corrupt_file()
    generate_empty_file()
    print("Done.")
