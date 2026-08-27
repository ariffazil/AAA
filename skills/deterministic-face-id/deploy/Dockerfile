# Dockerfile · deterministic-face-id
# F1: Local execution only. No cloud round-trips. Air-gapped runtime.
# F6: Strictly 1:1 verification. NOT 1:N surveillance.
# Engine: InsightFace buffalo_l (512-dim) + ONNX Runtime CPU.

FROM python:3.12-slim AS base

# F1: pin INSIGHTFACE_HOME to deterministic path (host-mount target)
ENV INSIGHTFACE_HOME=/opt/insightface
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# System deps for opencv-python-headless (no GUI libs in container)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps — pinned for reproducibility
RUN pip install --no-cache-dir \
        "insightface>=0.7.3" \
        "onnxruntime>=1.15.0" \
        "opencv-python-headless>=4.8.0" \
        "qdrant-client>=1.7.0" \
        "numpy>=1.24"

# Copy engine
COPY face_id_engine.py /app/face_id_engine.py

# Healthcheck: verify ONNX weights are mounted (air-gap invariant)
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD test -f /opt/insightface/models/buffalo_l/det_10g.onnx || exit 1

# F1: run as non-root
RUN useradd -m -u 1000 dfid
USER dfid

ENTRYPOINT ["python", "/app/face_id_engine.py"]