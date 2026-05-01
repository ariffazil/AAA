#!/usr/bin/env python3
"""
Hermes ACP Server launcher.
Usage: python3 start_server.py
"""
import sys
sys.path.insert(0, '/root')

import uvicorn
from acp.server import app

if __name__ == "__main__":
    print("[Hermes ACP] Starting on http://0.0.0.0:8082")
    uvicorn.run(app, host="0.0.0.0", port=8082, log_level="info")
