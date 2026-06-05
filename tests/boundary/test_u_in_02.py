"""U-IN-02 — missing colon → E002 (FR-05 / SC-02)."""

import pytest


@pytest.mark.u_in_02
def test_u_in_02_missing_colon():
    """U-IN-02: CLI \"meter\" (no colon) → stderr E002, exit≠0, no conversion stdout."""
    # Given: CLI argument "meter" without colon
    # When: python -m boundary "meter"
    # Then: stderr E002, exit≠0, stdout has no conversion lines
    pytest.fail("RED: U-IN-02 — boundary 미구현, 의도적 실패")
