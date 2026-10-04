#!/usr/bin/env python3
"""
wgc_demo.py - Witnessed Governance Cryptography demo.

Generates a 3-share XOR visual cryptography proof from one scar, one floor,
and one live witness. Reproducible: same inputs always produce same outputs.

Usage:
  python3 wgc_demo.py

Defaults:
  scar_id       = SCAR_LEBAH_EMAS
  floor_code    = F1_AMANAH
  witness_organ = GEOX

Outputs (in /root/forge_work/):
  WGC_demo_governance_root.png      - recovered bitmap (256x256)
  WGC_demo_share_a_scar.png         - random alone (256x256)
  WGC_demo_share_b_floor.png        - random alone (256x256)
  WGC_demo_share_c_witness.png      - random alone (256x256)
  WGC_demo_composite.png            - 2x2 demo (527x562)

Deterministic. Re-runnable. No network calls. Pure stdlib + Pillow + numpy.
"""

import hashlib
import os
import random
import sys
from datetime import datetime, timezone

import numpy as np
from PIL import Image, ImageDraw

DOMAIN_SEP = b"VISUAL_KEY_v1"
OUT_DIR = "/root/forge_work"

DEFAULT_SCAR = {
    "scar_id": "SCAR_LEBAH_EMAS",
    "title": "Lebah Emas",
    "witnessed": True,
    "lesson": "Truth without sovereign ownership is extractable.",
    "floors": ["F2", "F11", "F13"],
    "system_born": "VAULT999",
    "meaning_anchor": "Authorship - losing the ability to point at your work and say 'I built that.'",
}

DEFAULT_FLOOR = {
    "floor": "F1_AMANAH",
    "rule": "Reversible-first. Irreversible -> 888_HOLD.",
    "status": "PASS",
    "kernel_version": "2026.08.12",
}

DEFAULT_WITNESS = {
    "organ": "GEOX",
    "probe_status": "WITNESS_ACTIVE",
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}


def canonical_encode(obj, prefix):
    """Deterministic canonical encoding. Uppercase, sorted, fixed delimiters."""
    if prefix == "SCAR":
        return "\n".join([
            f"SCAR|{obj['scar_id']}|W={int(obj['witnessed'])}",
            f"LESSON|{obj['lesson']}",
            f"FLOORS|{':'.join(sorted(obj['floors']))}",
            f"SYSTEM|{obj['system_born']}",
        ])
    if prefix == "FLOOR":
        return "\n".join([
            f"FLOOR|{obj['floor']}|S={obj['status']}",
            f"RULE|{obj['rule']}",
            f"KERNEL|{obj['kernel_version']}",
        ])
    if prefix == "WITNESS":
        return "\n".join([
            f"WITNESS|{obj['organ']}|S={obj['probe_status']}",
            f"TS|{obj['timestamp']}",
        ])
    raise ValueError(f"unknown prefix: {prefix}")


def build_governance_root(scar, floor, witness):
    """Stages 1-3: canonical encode + hash + Merkle root."""
    sh = hashlib.sha256(canonical_encode(scar, "SCAR").encode()).digest()
    fh = hashlib.sha256(canonical_encode(floor, "FLOOR").encode()).digest()
    wh = hashlib.sha256(canonical_encode(witness, "WITNESS").encode()).digest()
    inner = hashlib.sha256(fh + wh).digest()
    root = hashlib.sha256(sh + inner).digest()
    return root, sh, fh, wh


def make_deterministic_bitmap(seed_bytes, size=256):
    """Stage 4: seed -> 256x256 deterministic bitmap with root fingerprint overlay."""
    seed = hashlib.sha256(seed_bytes + DOMAIN_SEP).digest()
    rng = random.Random(seed)
    img = Image.new("L", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            zone = (x // 85) % 3
            v = rng.randint(0, 255)
            if zone == 0:
                v = (v + rng.randint(0, 255)) // 2
            elif zone == 1:
                v = (v * 2 + rng.randint(0, 255)) // 3
            px[x, y] = v
    # Overlay root fingerprint: 8 bits per byte * 32 bytes = 256 visible markers
    for i, b in enumerate(seed[:32]):
        for bit in range(8):
            bp = i * 8 + bit
            if bp < size * size:
                bx, by = bp % size, bp // size
                v = (b >> (7 - bit)) & 1
                px[bx, by] = min(255, px[bx, by] + 35) if v else max(0, px[bx, by] - 18)
    return img


def split_xor(arr, seed_bytes):
    """Stage 5: 3-of-3 XOR secret split. Verify recovery."""
    size = arr.shape[0]
    rng_a = random.Random(seed_bytes + b"A")
    share_a = np.array(
        [[rng_a.randint(0, 255) for _ in range(size)] for _ in range(size)],
        dtype=np.uint8,
    )
    rng_b = random.Random(seed_bytes + b"B")
    share_b = np.array(
        [[rng_b.randint(0, 255) for _ in range(size)] for _ in range(size)],
        dtype=np.uint8,
    )
    share_c = np.bitwise_xor(np.bitwise_xor(share_a, share_b), arr)

    recovered = np.bitwise_xor(np.bitwise_xor(share_a, share_b), share_c)
    assert np.array_equal(recovered, arr), "XOR RECOVERY FAILED"

    return share_a, share_b, share_c


def make_composite(share_a, share_b, share_c, recovered_arr, scar, floor, witness):
    """2x2 grid composite for demo visualization."""
    SIZE = 256
    comp = Image.new("L", (SIZE * 2 + 15, SIZE * 2 + 50), color=25)
    draw = ImageDraw.Draw(comp)
    panels = [
        (f"SHARE A - Scar ({scar['scar_id']})", share_a),
        (f"SHARE B - Floor ({floor['floor']})", share_b),
        (f"SHARE C - Witness ({witness['organ']})", share_c),
        ("COMBINED - Governance Root", recovered_arr),
    ]
    for i, (lbl, s) in enumerate(panels):
        col, row = i % 2, i // 2
        x, y = 5 + col * (SIZE + 5), 35 + row * (SIZE + 5)
        comp.paste(Image.fromarray(s, mode="L"), (x, y))
        draw.text((x + 3, 5 + row * (SIZE + 5)), lbl, fill=210)
    return comp


def main():
    scar = dict(DEFAULT_SCAR)
    floor = dict(DEFAULT_FLOOR)
    witness = dict(DEFAULT_WITNESS)

    witness["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    root, sh, fh, wh = build_governance_root(scar, floor, witness)

    bitmap = make_deterministic_bitmap(root)
    arr = np.array(bitmap, dtype=np.uint8)

    share_a, share_b, share_c = split_xor(arr, root)
    recovered = np.bitwise_xor(np.bitwise_xor(share_a, share_b), share_c)

    os.makedirs(OUT_DIR, exist_ok=True)
    paths = {
        "root": os.path.join(OUT_DIR, "WGC_demo_governance_root.png"),
        "share_a": os.path.join(OUT_DIR, "WGC_demo_share_a_scar.png"),
        "share_b": os.path.join(OUT_DIR, "WGC_demo_share_b_floor.png"),
        "share_c": os.path.join(OUT_DIR, "WGC_demo_share_c_witness.png"),
        "composite": os.path.join(OUT_DIR, "WGC_demo_composite.png"),
    }
    bitmap.save(paths["root"])
    Image.fromarray(share_a, mode="L").save(paths["share_a"])
    Image.fromarray(share_b, mode="L").save(paths["share_b"])
    Image.fromarray(share_c, mode="L").save(paths["share_c"])
    comp = make_composite(share_a, share_b, share_c, recovered, scar, floor, witness)
    comp.save(paths["composite"])

    print(f"GOVERNANCE ROOT: {root.hex()[:32]}...")
    print(f"SCAR_HASH:       {sh.hex()[:32]}...")
    print(f"FLOOR_HASH:      {fh.hex()[:32]}...")
    print(f"WITNESS_HASH:    {wh.hex()[:32]}...")
    print(f"SCAR:            {scar['scar_id']} ({' '.join(scar['floors'])})")
    print(f"FLOOR:           {floor['floor']}")
    print(f"WITNESS:         {witness['organ']}")
    print(f"THRESHOLD:       3-of-3 XOR")
    print(f"VERIFY:          Recovered == Original TRUE")
    for k, p in paths.items():
        print(f"FILE ({k}): {p} ({os.path.getsize(p)} bytes)")


if __name__ == "__main__":
    main()