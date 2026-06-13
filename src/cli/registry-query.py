#!/usr/bin/env python3
"""arifos-registry query script — P4 (2026-06-13)
Reads AAA registry YAML/JSON files and outputs parsed JSON.
Usage: python3 /root/AAA/src/cli/registry-query.py <filename>
"""

import sys, json, os

try:
    import yaml
except ImportError:
    # Fallback: treat as JSON only
    yaml = None

REGISTRY_DIR = "/root/AAA/registries"


def main():
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {
                    "error": "Usage: registry-query.py <filename>",
                    "available": sorted(os.listdir(REGISTRY_DIR)),
                }
            )
        )
        sys.exit(1)

    filename = sys.argv[1]
    filepath = os.path.join(REGISTRY_DIR, filename)

    if not os.path.exists(filepath):
        print(
            json.dumps(
                {
                    "error": f"File not found: {filename}",
                    "available": sorted(os.listdir(REGISTRY_DIR)),
                }
            )
        )
        sys.exit(1)

    with open(filepath, "r") as f:
        content = f.read()

    if filename.endswith((".yaml", ".yml")):
        if yaml:
            data = yaml.safe_load(content)
        else:
            print(json.dumps({"error": "PyYAML not installed, cannot parse YAML"}))
            sys.exit(1)
    elif filename.endswith(".json"):
        data = json.loads(content)
    elif filename.endswith(".md"):
        # Markdown: return as raw text + line count
        data = {
            "type": "markdown",
            "lines": len(content.splitlines()),
            "preview": content[:200],
        }
    else:
        data = {
            "type": "unknown",
            "filename": filename,
            "lines": len(content.splitlines()),
        }

    print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()
