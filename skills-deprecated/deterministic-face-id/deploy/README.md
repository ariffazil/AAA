# Deploy Guide · deterministic-face-id
# F1 air-gap protocol for biometric verification engine.

## 0. Constitutional Constraints

| Floor | Constraint |
|---|---|
| **F1** | Local execution only. No cloud round-trips. Air-gapped runtime. Weights pre-downloaded and mounted `:ro`. Container network `internal: true` — drops ALL outbound traffic. |
| **F6** | Strictly 1:1 verification. NOT a 1:N surveillance net. Qdrant search always filtered by `target_identity`. |
| **F11** | Every call audited. Identity IDs deterministic (`uuid5`). Image bytes NEVER logged. |

This skill is **NOT** for:
- Scanning crowds
- Identifying unknown persons
- Any workflow that ships biometric vectors off-host

---

## 1. Pre-flight (host)

### 1.1 Verify Qdrant is live

```bash
curl -sf http://localhost:6333/collections | jq '.collections[] | select(.name == "identity_vault")'
# If absent: will be created on first container start (deterministic 512-dim, COSINE)
```

### 1.2 Pre-download InsightFace `buffalo_l` weights

InsightFace tries to download `.onnx` files on first init. **We must prevent that.** Download once to host, then mount.

```bash
# OPTION A: temporary container with internet, then extract
docker run --rm -v "$PWD/models:/out" python:3.12-slim bash -c '
    pip install insightface onnxruntime opencv-python-headless qdrant-client numpy &&
    python -c "
from insightface.app import FaceAnalysis
import os
os.environ[\"INSIGHTFACE_HOME\"] = \"/root/.insightface\"
app = FaceAnalysis(name=\"buffalo_l\", providers=[\"CPUExecutionProvider\"], root=\"/root/.insightface\")
app.prepare(ctx_id=0, det_size=(640, 640))
print(\"OK\")
"
# Then copy the populated model dir to host
docker cp <tmp_container_id>:/root/.insightface/models ./models/
'

# OPTION B: download the .onnx files directly (alternative for air-gapped host prep)
# Model pack: buffalo_l = det_10g.onnx + w600k_r50.onnx + genderage.onnx + ...
# Available from: https://github.com/deepinsight/insightface/releases
# (use release page to fetch individual .onnx files)
```

### 1.3 Verify weights

```bash
ls -la models/buffalo_l/
# MUST contain at minimum: det_10g.onnx, w600k_r50.onnx
```

---

## 2. Build & Launch

```bash
cd /root/.agents/skills/deterministic-face-id/deploy

# Build (host needs internet for pip install during build ONLY)
docker compose build

# Launch with internal network — NO outbound internet
docker compose up -d

# Verify healthcheck
docker compose ps
# Expected: arif_biometric_lock (healthy)
```

---

## 3. Register Sovereign Identity (F13 SOVEREIGN-gated)

This step is **irreversible-ish**. It writes the baseline embedding for the
sovereign's face. Only F13 may execute this.

```bash
# From host (with the image accessible)
docker compose exec deterministic-face-id python /app/face_id_engine.py register \
    --image /path/to/sovereign_baseline.jpg \
    --identity arif_888

# Expected output:
# {
#   "registered": "arif_888",
#   "vault_id": "0x...",
#   "embedding_dim": 512
# }
```

---

## 4. Verify Identity

```bash
docker compose exec deterministic-face-id python /app/face_id_engine.py verify \
    --image /path/to/incoming_face.jpg \
    --identity arif_888

# Expected output on match:
# {
#   "is_match": true,
#   "confidence": 0.8473,
#   "target": "arif_888",
#   "embedding_dim": 512
# }

# On no-match:
# {
#   "is_match": false,
#   "confidence": 0.21,
#   "target": "arif_888",
#   "embedding_dim": 512
# }
```

---

## 5. Audit

```bash
# List registered identities (no biometric data exposed)
docker compose exec deterministic-face-id python /app/face_id_engine.py list

# Verify container has no outbound network access
docker compose exec deterministic-face-id sh -c \
    "ip route show; ping -c1 -W1 8.8.8.8 || echo 'F1 OK: no outbound'"
# Expected second command to fail (ping should not resolve / should timeout)
```

---

## 6. Rollback

```bash
# Stop & remove container
docker compose down

# Wipe biometric vault (F1 reversible — no irrecoverable data)
curl -X DELETE http://localhost:6333/collections/identity_vault

# Optionally remove weights from host
rm -rf models/
```

---

## 7. Operational Notes

- **Threshold tuning.** Default 0.60 is calibrated for Buffalo_L cosine similarity on
  frontal portraits. For wider angle tolerance, lower to 0.50; for stricter lock,
  raise to 0.70.
- **Multiple registrations.** Each `register` call UPDERTS the vault entry for that
  identity. Use different `--identity` labels for different operators.
- **No video stream yet.** This engine accepts single frames only. Video face tracking
  is documented as a GAP in `forge-multimodal-router` line 137.
- **CPU vs GPU.** Compose currently pins `CPUExecutionProvider`. For GPU acceleration,
  swap to `CUDAExecutionProvider` + install `onnxruntime-gpu` (requires NVIDIA runtime
  in container — separate F13 authority needed).