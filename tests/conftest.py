"""Pytest hooks — prefer src/ packages over same-named tests/ subdirectories."""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"


def pytest_configure(config):
    src = str(_SRC)
    if src in sys.path:
        sys.path.remove(src)
    sys.path.insert(0, src)
    for name in list(sys.modules):
        if name == "entity" or name.startswith("entity."):
            del sys.modules[name]
