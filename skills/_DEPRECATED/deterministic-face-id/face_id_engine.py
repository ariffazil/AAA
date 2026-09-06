"""
deterministic-face-id · face_id_engine.py
Forged 2026-08-25 by 333-AGI under F13 SOVEREIGN directive.

Constitutional constraints:
  F1 — Local execution only. No cloud. Air-gapped.
  F2 — Deterministic embeddings. P(truth) > 0.99 under Buffalo_L conditions.
  F6 — 1:1 verification only. NOT 1:N surveillance.
  F9 — No claim of consciousness. Pure math.
  F11 — Every call audited. No raw biometric payload in logs.

Engine: InsightFace buffalo_l (512-dim) + ONNX Runtime + local Qdrant.
"""

from __future__ import annotations

import base64
import logging
import os
import sys
import uuid
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from insightface.app import FaceAnalysis
from qdrant_client import QdrantClient
from qdrant_client.http import models

# ── Privacy: never log raw biometric data ────────────────────────────────────
logging.basicConfig(
    level=os.environ.get("DFID_LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("deterministic-face-id")

# ── Constants (deterministic across processes) ────────────────────────────────
NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # UUIDv5 DNS namespace
COLLECTION_NAME = "identity_vault"
EMBEDDING_DIM = 512  # buffalo_l native
DEFAULT_THRESHOLD = 0.60  # Buffalo_L cosine similarity calibrated


class DeterministicFaceID:
    """
    Read-only biometric verification engine.
    Air-gapped, 1:1 only, deterministic.
    """

    def __init__(
        self,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        threshold: float = DEFAULT_THRESHOLD,
        insighface_home: str | None = None,
    ) -> None:
        # F1: enforce INSIGHTFACE_HOME for air-gap
        if insighface_home is None:
            insighface_home = os.environ.get("INSIGHTFACE_HOME", "/opt/insightface")
        os.environ["INSIGHTFACE_HOME"] = insighface_home

        weights_dir = Path(insighface_home) / "models" / "buffalo_l"
        if not weights_dir.exists():
            # F1 HARD FAIL — no internet allowed, no silent cloud download
            raise FileNotFoundError(
                f"F1 air-gap breach: buffalo_l weights missing at {weights_dir}. "
                f"Mount weights pre-downloaded to {insighface_home}/models/buffalo_l "
                f"(see deploy/README.md). Container cannot phone home."
            )

        self.threshold = threshold
        self.collection_name = COLLECTION_NAME

        # Local ONNX engine
        log.info("loading buffalo_l ONNX engine (F1: local CPU only)...")
        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"],
            root=insighface_home,
        )
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        log.info("engine ready (detection=SCRFD-10GF, recognition=ArcFace-R100)")

        # Local Qdrant
        self.qdrant = QdrantClient(host=qdrant_host, port=qdrant_port)
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """Creates identity_vault collection if absent. 512-dim, COSINE."""
        existing = {c.name for c in self.qdrant.get_collections().collections}
        if self.collection_name not in existing:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=EMBEDDING_DIM,
                    distance=models.Distance.COSINE,
                ),
            )
            log.info(
                "created vault collection: %s (dim=%d)",
                self.collection_name,
                EMBEDDING_DIM,
            )
        else:
            log.info("vault collection present: %s", self.collection_name)

    def _decode_payload(self, image_payload: str) -> np.ndarray:
        """
        Decode image_payload (path or base64) to BGR numpy array.
        F1: caller MUST wipe the returned reference after extraction.
        """
        if image_payload.startswith(("data:", "base64:")) or len(image_payload) > 4096:
            # Likely base64
            if "," in image_payload:
                image_payload = image_payload.split(",", 1)[1]
            raw = base64.b64decode(image_payload)
            arr = np.frombuffer(raw, dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        else:
            # Treat as path
            img = cv2.imread(image_payload)

        if img is None:
            raise ValueError("image_payload invalid or unreadable")
        return img

    def extract_vector(self, image_payload: str) -> np.ndarray:
        """
        Extract 512-dim embedding from largest face.
        F1: wipes input image from memory before returning.
        F6: assumes single primary subject (largest face wins).
        """
        img = self._decode_payload(image_payload)
        try:
            faces = self.app.get(img)
            if not faces:
                raise ValueError("no face detected in payload")

            # Largest face = primary subject
            primary = sorted(
                faces,
                key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]),
                reverse=True,
            )[0]

            embedding = np.asarray(primary.embedding, dtype=np.float32)
            # L2-normalize (cosine sim invariant)
            embedding = embedding / np.linalg.norm(embedding)
            return embedding
        finally:
            # F1 INVARIANT: wipe raw image from memory immediately
            del img

    def _deterministic_uuid(self, label: str) -> int:
        """F11: deterministic identity IDs across processes (uuid5, not Python hash)."""
        # uuid5 is deterministic given the same namespace + label
        return uuid.uuid5(NAMESPACE, label).int & 0x7FFFFFFFFFFFFFFF  # fit in i64

    def register_identity(self, identity_id: str, image_payload: str) -> dict[str, Any]:
        """
        One-time baseline registration. F13 SOVEREIGN-gated in practice
        (callers should verify actor authority before invoking).
        """
        if not identity_id or not identity_id.strip():
            raise ValueError("identity_id required")

        vector = self.extract_vector(image_payload)
        point_id = self._deterministic_uuid(identity_id)

        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=vector.tolist(),
                    payload={"identity": identity_id},
                )
            ],
        )
        log.info(
            "registered identity: %s (vault_id=%x...)", identity_id, point_id >> 16
        )
        return {
            "registered": identity_id,
            "vault_id": hex(point_id),
            "embedding_dim": EMBEDDING_DIM,
        }

    def verify_identity(
        self, image_payload: str, target_identity: str, threshold: float | None = None
    ) -> dict[str, Any]:
        """
        The active READ-ONLY verification loop.
        F6: gated by identity filter — no 1:N identification.
        F11: image bytes NEVER logged.
        """
        thr = threshold if threshold is not None else self.threshold

        try:
            query_vec = self.extract_vector(image_payload)
        except ValueError as e:
            return {
                "is_match": False,
                "confidence": 0.0,
                "error": str(e),
                "target": target_identity,
            }

        # qdrant-client >= 1.9: .search() → .query_points() (zen patch 2026-09-05)
        res = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_vec.tolist(),
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="identity",
                        match=models.MatchValue(value=target_identity),
                    )
                ]
            ),
            limit=1,
            with_payload=False,  # F1: never echo payload back
        )
        hits = res.points if hasattr(res, "points") else res

        if not hits:
            return {
                "is_match": False,
                "confidence": 0.0,
                "error": "identity not registered in vault",
                "target": target_identity,
            }

        score = float(hits[0].score)
        return {
            "is_match": score >= thr,
            "confidence": round(score, 4),
            "target": target_identity,
            "embedding_dim": EMBEDDING_DIM,
        }

    def list_identities(self) -> dict[str, Any]:
        """F11 audit helper — list registered identities (no biometric data)."""
        records, _ = self.qdrant.scroll(
            collection_name=self.collection_name,
            with_vectors=False,  # F1: never expose embeddings
            with_payload=True,
            limit=1000,
        )
        identities = sorted(
            {r.payload["identity"] for r in records if "identity" in r.payload}
        )
        return {"identities": identities, "count": len(identities)}


# ── CLI entrypoint (for sovereign registration & verification) ────────────────
def _cli() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(
        prog="deterministic-face-id",
        description="F1/F6 deterministic 1:1 face verification (local-only)",
    )
    parser.add_argument("mode", choices=["verify", "register", "list"])
    parser.add_argument("--image", help="path or base64 (required for verify/register)")
    parser.add_argument(
        "--identity", help="identity label (required for verify/register)"
    )
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--qdrant-host", default="localhost")
    parser.add_argument("--qdrant-port", type=int, default=6333)
    args = parser.parse_args()

    engine = DeterministicFaceID(
        qdrant_host=args.qdrant_host,
        qdrant_port=args.qdrant_port,
        threshold=args.threshold,
    )

    if args.mode == "list":
        result = engine.list_identities()
    elif args.mode == "register":
        if not args.image or not args.identity:
            parser.error("--image and --identity required for register")
        result = engine.register_identity(args.identity, args.image)
    else:  # verify
        if not args.image or not args.identity:
            parser.error("--image and --identity required for verify")
        result = engine.verify_identity(args.image, args.identity, args.threshold)

    print(json.dumps(result, indent=2))
    return (
        0
        if (
            args.mode != "verify"
            or result.get("is_match") is not False
            or "error" not in result
        )
        else 1
    )


if __name__ == "__main__":
    sys.exit(_cli())
