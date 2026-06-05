"""U-IN-02 — missing colon → E002 (FR-05 / SC-02)."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

_SRC = str(Path(__file__).resolve().parent.parent.parent / "src")


@pytest.mark.u_in_02
def test_u_in_02_missing_colon():
    """U-IN-02: CLI \"meter\" (no colon) → stderr E002, exit≠0, no conversion stdout."""
    # Given: CLI argument "meter" without colon
    # When: python -m boundary "meter"
    result = subprocess.run(
        [sys.executable, "-m", "boundary", "meter"],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": _SRC},
    )

    # Then: stderr E002, exit≠0, stdout has no conversion lines
    assert "E002" in result.stderr
    assert result.returncode != 0
    assert result.stdout.strip() == ""
