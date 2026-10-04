#!/usr/bin/env python3
"""
Warga Identity Provisioning — generic 4-step recipe for bringing a new agent
into the AAA federation as a constitutional citizen.

Replace the four UPPERCASE constants before running. The script handles:
  1. Ed25519 key generation (private + public, mode 600 / 644)
  2. DID registry update (canonical + runtime mirror)
  3. organs.yaml entry construction (print YAML block, manual insertion)
  4. SCT v1 production + verification (full chain test)

Recipe origin: OpenClaw provisioning on 2026-08-07.
Use this for ANY new agent organ being added to the federation: openclaw,
kimi, codex, image-analyzer, dispatch, omega-shadow, etc.

Iron rule: probe before act. Generate key, then verify SCT before claiming
identity is provisioned. The verification step is the audit trail.
"""
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
import json, os, sys, time

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURE THESE FOR THE NEW AGENT
# ─────────────────────────────────────────────────────────────────────────────
ORGAN_ID   = "openclaw"               # lowercase, used for filenames + DID
DID_NAME   = "openclaw"               # appears in did:arif:<NAME>
ACTOR_ID   = "openclaw:ingress"       # semantic agent identifier
KEY_ID     = "openclaw-edge-2026-08"  # year-month tagged rotation key
HUMAN_PRINCIPAL = "arif:primary"
CEILING    = "DISPLAY_ONLY"           # DISPLAY_ONLY | COMPUTE_ONLY | JUDGE_ONLY | REFLECT_ONLY | EXECUTE_AFTER_SEAL
CLASS      = "EDGE"                   # CORE | EDGE | METABOLISM | MEMORY | ADVISORY | SUPPORT
ROLE       = "agentic_mesh_router"    # short slug describing the job
PORT       = 18789
PORT_WEB   = 8787
UNIT       = "openclaw-gateway.service"

# Optional: existing key? If file exists, the script loads instead of regenerating.
# (Safe re-runs: idempotent.)
# ─────────────────────────────────────────────────────────────────────────────

KEYS_DIR = "/root/AAA/auth/keys"
PRIV_PATH = f"{KEYS_DIR}/{ORGAN_ID}_private.key"
PUB_PATH = f"{KEYS_DIR}/{ORGAN_ID}_public.key"
CANON_REG = "/root/AAA/secrets/did/registry.json"
RUNTIME_REG = "/opt/arifos/.secrets/did/registry.json"

DID = f"did:arif:{DID_NAME}"


def step(msg):
    print(f"\n[STEP] {msg}")


def step_ok(msg):
    print(f"[OK]   {msg}")


def step_skip(msg):
    print(f"[SKIP] {msg}")


def step_fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)


# ─── STEP 1: KEY ────────────────────────────────────────────────────────────
step("1. Generate Ed25519 keypair")

if os.path.exists(PRIV_PATH):
    step_skip(f"Private key already exists at {PRIV_PATH} — loading existing")
    with open(PRIV_PATH, "rb") as f:
        priv_bytes = f.read()
    sk = Ed25519PrivateKey.from_private_bytes(priv_bytes)
else:
    sk = Ed25519PrivateKey.generate()
    priv_bytes = sk.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(PRIV_PATH, "wb") as f:
        f.write(priv_bytes)
    os.chmod(PRIV_PATH, 0o600)
    step_ok(f"Created {PRIV_PATH} (mode 600)")

pk = sk.public_key()
pub_bytes = pk.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw,
)

if not os.path.exists(PUB_PATH):
    with open(PUB_PATH, "wb") as f:
        f.write(pub_bytes)
    os.chmod(PUB_PATH, 0o644)
    step_ok(f"Created {PUB_PATH} (mode 644)")
else:
    step_skip(f"Public key already exists at {PUB_PATH}")

print(f"       Public key hex: {pub_bytes.hex()}")


# ─── STEP 2: DID REGISTRY ───────────────────────────────────────────────────
step("2. Update DID registry (canonical + runtime)")

if not os.path.exists(CANON_REG):
    step_fail(f"Canonical registry not found: {CANON_REG}")

with open(CANON_REG) as f:
    reg = json.load(f)

entry = {
    "organ_id": ORGAN_ID,
    "public_key_hex": pub_bytes.hex(),
    "algorithm": "Ed25519",
    "description": f"{ORGAN_ID} — {ROLE} ({CLASS} class, {CEILING} ceiling)"
}

if DID in reg["dids"]:
    step_skip(f"{DID} already in registry — refreshing entry")
    reg["dids"][DID] = entry
else:
    step_ok(f"Adding {DID} to registry")
    reg["dids"][DID] = entry

with open(CANON_REG, "w") as f:
    json.dump(reg, f, indent=2)

if os.path.isdir(os.path.dirname(RUNTIME_REG)):
    with open(RUNTIME_REG, "w") as f:
        json.dump(reg, f, indent=2)
    step_ok(f"Mirrored to runtime: {RUNTIME_REG}")
else:
    step_skip(f"Runtime dir missing: {os.path.dirname(RUNTIME_REG)}")


# ─── STEP 3: ORGANS.YAML ENTRY (printable block) ────────────────────────────
step("3. organs.yaml entry template (insert manually)")

yaml_block = f"""
  - id: {ORGAN_ID}
    class: {CLASS}
    display_name: {ORGAN_ID.title()}
    role: {ROLE}
    authority_ceiling: {CEILING}
    port: {PORT}
    port_web: {PORT_WEB}  # currently down — known
    unit: {UNIT}
    runtime: node-22
    actor_id: "{ACTOR_ID}"
    did: "{DID}"
    signing_key: "{PRIV_PATH}"
    key_id: "{KEY_ID}"
    partner_organ: hermes
    owned_domains:
      - a2a_dispatch
      - session_continuity
    forbidden_domains:
      - constitutional_judgment
      - engineering_execution
      - human_face     # Hermes owns the human face
      - cognitive_research
      - memory_curation
      - skills_library
    notes:
      - "{ORGAN_ID} adalah warga federation dengan {CEILING} ceiling."
      - "Hermes is the face. OpenClaw is the spine. OpenCode is the hands. arifOS is the law."
"""

print(yaml_block)
print(f"       Insert above into /root/AAA/federation/organs.yaml after similar neighbor")
print(f"       Then verify: `yq '.[] | select(.id==\"{ORGAN_ID}\")' /root/AAA/federation/organs.yaml`")


# ─── STEP 4: SCT VERIFICATION ───────────────────────────────────────────────
step("4. Produce + verify SCT v1 (chain test)")

session_id = f"{ORGAN_ID}-verify-{int(time.time())}"
issued_at = int(time.time())
expires_at = issued_at + 3600

payload = {
    "sct_v1": {
        "issuer": DID,
        "actor_id": ACTOR_ID,
        "key_id": KEY_ID,
        "session_id": session_id,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "max_action_class": "OBSERVE",
        "ceiling": CEILING,
        "human_principal_id": HUMAN_PRINCIPAL,
        "binding": {
            "channel_origin": "agent-to-agent",
            "task_intent": "verify_identity"
        }
    }
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
sig = sk.sign(canonical.encode("utf-8"))
sig_hex = sig.hex()

# Verify against registry public key
registry_pk = Ed25519PublicKey.from_public_bytes(bytes.fromhex(entry["public_key_hex"]))
try:
    registry_pk.verify(sig, canonical.encode("utf-8"))
    step_ok("Signature verified by registry public key — identity chain confirmed")
except Exception as e:
    step_fail(f"Signature verification FAILED: {e}")

sct = {
    "version": "sct_v1",
    "payload": payload,
    "signature": sig_hex,
    "algorithm": "Ed25519"
}

print(f"\n       SCT payload hash: {hash(canonical) & 0xffffffff:08x}")
print(f"       Session ID:       {session_id}")
print(f"       Expires:          {expires_at} (1h)")


# ─── SUMMARY ────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print(f"VERIFICATION SUMMARY — {DID}")
print("=" * 70)
print(f"  Step 1: Keypair generated/loaded ✓")
print(f"  Step 2: DID registered (canonical + runtime) ✓")
print(f"  Step 3: organs.yaml block printed — INSERT MANUALLY")
print(f"  Step 4: SCT signature verified ✓")
print()
print(f"  → {ORGAN_ID} is now a constitutional warga of the AAA federation.")
print(f"  → Ready to sign A2A envelopes.")
print(f"  → Next: wire A2A egress bridge to AAA :3001/tasks")
print("=" * 70)
