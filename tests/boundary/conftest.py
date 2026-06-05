"""Boundary-layer pytest helpers."""

import os
import subprocess
import sys
from pathlib import Path

_SRC = str(Path(__file__).resolve().parent.parent.parent / "src")


def run_boundary_cli(*cli_args: str) -> subprocess.CompletedProcess[str]:
    """Run `python -m boundary` with PYTHONPATH set to src."""
    return subprocess.run(
        [sys.executable, "-m", "boundary", *cli_args],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": _SRC},
    )
