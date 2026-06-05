"""U-IN-01 — empty CLI input → E001 (FR-05 / SC-02)."""

import pytest

from tests._approval import assert_matches_golden
from tests.boundary.conftest import run_boundary_cli


@pytest.mark.u_in_01
def test_u_in_01_empty_input():
    """U-IN-01: CLI \"\" → stderr E001, exit≠0, no conversion stdout."""
    # Given: CLI argument ""
    # When: python -m boundary ""
    result = run_boundary_cli("")

    # Then: stderr E001, exit≠0, stdout has no conversion lines
    assert_matches_golden(result.stderr, "u_in_01_empty.approved.txt")
    assert result.returncode != 0
    assert result.stdout.strip() == ""
