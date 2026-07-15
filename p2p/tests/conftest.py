"""Pytest configuration — expose /root/AAA on sys.path so `p2p` is importable.

The p2p package lives at /root/AAA/p2p/ — adding /root/AAA to sys.path lets
tests do `from p2p.audit import ...` and `from p2p.protocol import ...`.
The earlier `from p2p.X` import path is preserved as an alias for
out-of-tree callers.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]  # /root/AAA
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# Optional legacy alias: if anyone does `from p2p.X`, expose it.
import importlib  # noqa: E402

_p2p = importlib.import_module("p2p")
sys.modules.setdefault("AAA", importlib.import_module("types").ModuleType("AAA"))
sys.modules["AAA.p2p"] = _p2p