"""U-IN-02 — missing colon → E002 (FR-05 / SC-02)."""

import pytest

from tests._approval import assert_matches_golden
from tests.boundary.conftest import run_boundary_cli


@pytest.mark.u_in_02
def test_u_in_02_missing_colon():
    """U-IN-02: CLI \"meter\" (no colon) → stderr E002, exit≠0, no conversion stdout."""
    # Given: CLI argument "meter" without colon
    # When: python -m boundary "meter"
    result = run_boundary_cli("meter")

    # Then: stderr E002, exit≠0, stdout has no conversion lines
    assert_matches_golden(result.stderr, "u_in_02_missing_colon.approved.txt")
    assert result.returncode != 0
    assert result.stdout.strip() == ""
