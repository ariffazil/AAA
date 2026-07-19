#!/usr/bin/env python3
"""
generate_contracts.py — Single-source contract generation pipeline.

Reads TOOL_MANIFEST.yaml → generates:
  1. tool_list.json — Machine-readable tool catalog
  2. openapi.json — OpenAPI 3.0 spec for ChatGPT connector  
  3. mcp_annotations.json — MCP readOnlyHint/destructiveHint annotations
  4. surface_hash.txt — SHA-256 of the canonical manifest

CI gate: if any surface doesn't match, build fails.
P0 contract generation — eliminates 5-surface drift.
"""

import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).parent
MANIFEST_PATH = ROOT / "TOOL_MANIFEST.yaml"
OUTPUT_DIR = ROOT / "generated"


def load_manifest() -> dict:
    """Load and validate the canonical tool manifest."""
    with open(MANIFEST_PATH) as f:
        manifest = yaml.safe_load(f)
    
    assert manifest["schema_version"] == "1.0.0", "Unknown schema version"
    return manifest


def compute_hash(manifest: dict) -> str:
    """Compute SHA-256 of the canonical manifest (without the hash field)."""
    m = dict(manifest)
    m.pop("canonical_hash", None)
    canonical = json.dumps(m, sort_keys=True, indent=2)
    return hashlib.sha256(canonical.encode()).hexdigest()


def generate_tool_list(manifest: dict) -> dict:
    """Generate tools/list compatible JSON from manifest."""
    tools = []
    for organ_name, organ in manifest["organs"].items():
        for tool in organ.get("tools", []):
            entry = {
                "name": tool["name"],
                "description": tool["description"],
                "organ": organ_name,
                "port": organ["port"],
                "classification": tool["classification"],
                "access": tool["access"],
                "modes": [m["name"] for m in tool.get("modes", [])],
                "annotations": tool.get("annotations", {}),
            }
            tools.append(entry)
    
    return {
        "generated_from": "TOOL_MANIFEST.yaml",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manifest_hash": manifest.get("canonical_hash", "TBD"),
        "tool_count": len(tools),
        "tools": tools,
    }


def generate_openapi(manifest: dict) -> dict:
    """Generate OpenAPI 3.0 spec for ChatGPT connector."""
    paths = {}
    
    for organ_name, organ in manifest["organs"].items():
        for tool in organ.get("tools", []):
            if tool["access"] != "public":
                continue
            
            path = f"/mcp/{organ_name}/{tool['name']}"
            modes_enum = [m["name"] for m in tool.get("modes", [])]
            
            schema = {
                "post": {
                    "operationId": f"{organ_name}_{tool['name']}",
                    "summary": tool["description"],
                    "description": f"Organ: {organ_name} | Classification: {tool['classification']}",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "mode": {
                                            "type": "string",
                                            "enum": modes_enum,
                                            "description": "Operation mode"
                                        },
                                        "arguments": {
                                            "type": "object",
                                            "description": "Tool-specific arguments"
                                        }
                                    },
                                    "required": ["mode"] if modes_enum else []
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Success"},
                        "403": {"description": "Access denied — requires authentication"},
                        "888": {"description": "HOLD — requires human approval"}
                    },
                    "x-organ": organ_name,
                    "x-classification": tool["classification"],
                    "x-annotations": tool.get("annotations", {}),
                }
            }
            paths[path] = schema
    
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "arifOS Federation — ChatGPT Connector API",
            "version": manifest.get("canonical_hash", "TBD")[:12],
            "description": "Auto-generated from TOOL_MANIFEST.yaml. Single source of truth.",
        },
        "servers": [{"url": "https://mcp.arif-fazil.com"}],
        "paths": paths,
    }


def generate_mcp_annotations(manifest: dict) -> dict:
    """Generate MCP readOnlyHint/destructiveHint annotations."""
    annotations = {}
    for organ_name, organ in manifest["organs"].items():
        for tool in organ.get("tools", []):
            annotations[tool["name"]] = {
                "organ": organ_name,
                "classification": tool["classification"],
                "annotations": tool.get("annotations", {}),
            }
    return {
        "generated_from": "TOOL_MANIFEST.yaml",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tools": annotations,
    }


def generate_surface_hash(manifest: dict) -> str:
    """Generate the surface hash file for CI verification."""
    h = manifest.get("canonical_hash", compute_hash(manifest))
    return f"{h}  TOOL_MANIFEST.yaml\n"


def main():
    print("═" * 60)
    print("  Contract Generation Pipeline")
    print("═" * 60)
    
    manifest = load_manifest()
    
    # Compute hash and stamp manifest
    h = compute_hash(manifest)
    manifest["canonical_hash"] = h
    
    # Write back with hash
    with open(MANIFEST_PATH, "w") as f:
        yaml.dump(manifest, f, sort_keys=False, allow_unicode=True, default_flow_style=False)
    
    print(f"\n  Canonical hash: {h}")
    
    # Ensure output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 1. Tool list
    tool_list = generate_tool_list(manifest)
    path = OUTPUT_DIR / "tool_list.json"
    path.write_text(json.dumps(tool_list, indent=2))
    print(f"  ✅ tool_list.json — {tool_list['tool_count']} tools")
    
    # 2. OpenAPI spec
    openapi = generate_openapi(manifest)
    path = OUTPUT_DIR / "openapi.json"
    path.write_text(json.dumps(openapi, indent=2))
    path_count = len(openapi["paths"])
    print(f"  ✅ openapi.json — {path_count} endpoints")
    
    # 3. MCP annotations
    annotations = generate_mcp_annotations(manifest)
    path = OUTPUT_DIR / "mcp_annotations.json"
    path.write_text(json.dumps(annotations, indent=2))
    print(f"  ✅ mcp_annotations.json — {len(annotations['tools'])} tools")
    
    # 4. Surface hash
    hash_content = generate_surface_hash(manifest)
    path = OUTPUT_DIR / "surface_hash.txt"
    path.write_text(hash_content)
    print(f"  ✅ surface_hash.txt")
    
    print(f"\n  All surfaces generated from single source.")
    print(f"  Hash: {h}")
    print(f"  CI gate: verify surface_hash.txt matches TOOL_MANIFEST.yaml")
    print("═" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
