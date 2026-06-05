"""U-IN-01 — empty CLI input → E001 (FR-05 / SC-02)."""

import pytest


@pytest.mark.u_in_01
def test_u_in_01_empty_input():
    """U-IN-01: CLI \"\" → stderr E001, exit≠0, no conversion stdout."""
    # Given: CLI argument ""
    # When: python -m boundary ""
    # Then: stderr E001, exit≠0, stdout has no conversion lines
    pytest.fail("RED: U-IN-01 — boundary 미구현, 의도적 실패")
